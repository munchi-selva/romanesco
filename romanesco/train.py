#!/usr/bin/env python3

import os
import logging

import numpy as np
import tensorflow as tf

from romanesco import reader
from romanesco.vocab import Vocabulary
from romanesco.compgraph import define_computation_graph
from romanesco.util import fit_iter_params
#from romanesco.score import score

from romanesco import const as C


def train(data: str,
          epochs: int = C.NUM_EPOCHS,
          batch_size: int = C.BATCH_SIZE,
          hidden_size: int = C.HIDDEN_SIZE,
          embedding_size: int = C.EMBEDDING_SIZE,
          vocab_max_size: int = C.VOCAB_SIZE,
          save_to: str = C.MODEL_PATH,
          log_to: str = C.LOGS_PATH,
          num_steps: int = C.NUM_STEPS,
          val_data: str = None,
          val_epochs: int = C.VAL_EPOCHS,
          patience: int = C.PATIENCE,
          **kwargs):
    """Trains a language model. See argument description in `bin/romanesco`."""

    # create vocabulary to map words to ids
    vocab = Vocabulary()
    vocab.build(data, max_size=vocab_max_size)
    vocab.save(os.path.join(save_to, C.VOCAB_FILENAME))

    # convert training data to list of word ids
    raw_data = reader.read(data, vocab)

    # define computation graph for training
    inputs, targets, loss, train_step, _, summary = define_computation_graph(vocab_size=vocab.size,
                                                                             batch_size=batch_size,
                                                                             num_steps=num_steps,
                                                                             hidden_size=hidden_size,
                                                                             embedding_size=embedding_size)

    # enable early stopping if a validation data file was specified
    early_stopping = val_data is not None

    if early_stopping:
#        val_model_path = os.path.join(save_to, C.VAL_MODEL_PATH)
#        vocab.save(os.path.join(val_model_path, C.VOCAB_FILENAME))

        # convert validation data to word ids,
        # find number of RNN time steps and batch size suitable for this data set
        val_raw_data = reader.read(val_data, vocab)
        val_data_length = len(val_raw_data)
        val_num_steps, val_batch_size = fit_iter_params(val_data_length, num_steps, batch_size)

        # define computation graph for validation
        val_inputs, val_targets, val_loss, _, _, _ = define_computation_graph(vocab_size=vocab.size,
                                                                              batch_size=val_batch_size,
                                                                              num_steps=val_num_steps,
                                                                              hidden_size=hidden_size,
                                                                              embedding_size=embedding_size)

    saver = tf.train.Saver()

    with tf.Session() as session:
        # init
        session.run(tf.global_variables_initializer())
        # write logs (@tensorboard)
        summary_writer = tf.summary.FileWriter(log_to, graph=tf.get_default_graph())

        if early_stopping:
            # initialize validation performance statistics
            best_val_loss = float("inf")
            epochs_without_improvement = 0

        # iterate over training data `epochs` times
        for epoch in range(1, epochs + 1):
            total_loss = 0.0
            total_iter = 0
            for x, y in reader.iterate(raw_data, batch_size, C.NUM_STEPS):
                l, _, s = session.run([loss, train_step, summary],
                                      feed_dict={inputs: x, targets: y})
                summary_writer.add_summary(s, total_iter)
                total_loss += l
                total_iter += 1
                if total_iter % 100 == 0:
                    logging.debug("Epoch=%s, iteration=%s", epoch, total_iter)
            perplexity = np.exp(total_loss / total_iter)
            logging.info("Perplexity on training data after epoch %s: %.2f", epoch, perplexity)

            save_model = True

            if early_stopping and epoch % val_epochs == 0:
                # Check what the current model's loss is on the validation data
                memory_used = session.run(tf.contrib.memory_stats.BytesInUse())
                logging.debug("Before checking validation data, bytes in use: %d", memory_used)

                # Save the latest model so it can be tested against the validation dataset
#                val_model_path = os.path.join(save_to, C.VAL_MODEL_PATH)
#                saver.save(session, os.path.join(val_model_path, C.VAL_MODEL_FILENAME))
#                latest_val_loss = score(val_data,
#                                        load_from = val_model_path,
#                                        model_filename = C.VAL_MODEL_FILENAME,
#                                        load_meta = True)
                total_val_loss = 0.0
                total_val_iter = 0
                for x, y in reader.iterate(val_raw_data, val_batch_size, val_num_steps):
                    l = session.run([val_loss], feed_dict={val_inputs: x, val_targets: y})
                    total_val_loss += l[0]
                    total_val_iter += 1
                latest_val_loss = np.exp(total_val_loss / total_val_iter)

                memory_used = session.run(tf.contrib.memory_stats.BytesInUse())
                logging.debug("After score, bytes in use: %d", memory_used)

                logging.info("Current model perplexity on validation data: %.2f", latest_val_loss)
                if latest_val_loss < best_val_loss:
                    logging.info("Lowest perplexity on validation data achieved")
                    best_val_loss = latest_val_loss
                    epochs_without_improvement = 0
                else:
                    save_model = False
                    epochs_without_improvement += 1
                    if epochs_without_improvement >= patience:
                        logging.info("No improvement in validation data perplexity for %d epochs: terminating training", epochs_without_improvement) 
                        return

            if save_model:
                saver.save(session, os.path.join(save_to, C.MODEL_FILENAME))
