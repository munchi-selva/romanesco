#!/usr/bin/env python3

import os
import logging

import numpy as np
import tensorflow as tf

from romanesco import reader
from romanesco import const as C
from romanesco.vocab import Vocabulary
from romanesco.compgraph import define_computation_graph
from romanesco.util import fit_iter_params


def score(data: str,
          load_from: str = C.MODEL_PATH,
          batch_size: int = C.BATCH_SIZE,
          hidden_size: int = C.HIDDEN_SIZE,
          embedding_size: int = C.EMBEDDING_SIZE,
          num_steps: int = C.NUM_STEPS,
          model_filename: str = C.MODEL_FILENAME,
#          load_meta: bool = False,
          **kwargs):
    """Scores a text using a trained language model. See argument description in `bin/romanesco`."""

    vocab = Vocabulary()
    vocab.load(os.path.join(load_from, C.VOCAB_FILENAME))

    raw_data = reader.read(data, vocab)
    data_length = len(raw_data)
    num_steps, batch_size = fit_iter_params(data_length, num_steps, batch_size)

#    if data_length < num_steps:
#        logging.warning("Length of input data is shorter than NUM_STEPS. Will try to reduce NUM_STEPS.")
#        num_steps = data_length - 1

#    if data_length < batch_size * num_steps:
#        logging.warning("Length of input data is shorter than BATCH_SIZE * NUM_STEPS. Will try to set batch size to 1.")
#        batch_size = 1

    inputs, targets, loss, _, _, _ = define_computation_graph(vocab_size=vocab.size,
                                                              batch_size=batch_size,
                                                              num_steps=num_steps,
                                                              hidden_size=hidden_size,
                                                              embedding_size=embedding_size)

#    saver = None
#    if load_meta:
#        model_metafile = os.path.join(load_from, model_filename + '.meta')
#        saver = tf.train.import_meta_graph(model_metafile)
#    else:
    saver = tf.train.Saver()

    with tf.Session() as session:
        # load model

        # TODO
        # Would resetting the default graph here prevent apparent memory leaks?
        # tf.reset_default_graph()
        # session.run(tf.global_variables_initializer())

        memory_used = session.run(tf.contrib.memory_stats.BytesInUse())
        logging.info("Before restore, bytes: %d", memory_used)
        saver.restore(session, os.path.join(load_from, model_filename))
        memory_used = session.run(tf.contrib.memory_stats.BytesInUse())
        logging.info("After restore, bytes: %d", memory_used)

        total_loss = 0.0
        total_iter = 0
        for x, y in reader.iterate(raw_data, batch_size, num_steps):
            l = session.run([loss], feed_dict={inputs: x, targets: y})
#            run_metadata = tf.RunMetadata()
#            l = session.run([loss], feed_dict={inputs: x, targets: y},
#                            options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE, output_partition_graphs = True),
#                            run_metadata = run_metadata)
#            with open("/tmp/run_metadata.txt", "a") as metalog:
#                metalog.write(str(run_metadata))
            total_loss += l[0]
            total_iter += 1
        memory_used = session.run(tf.contrib.memory_stats.BytesInUse())
        logging.info("After iterate, bytes: %d", memory_used)
        perplexity = np.exp(total_loss / total_iter)
        return perplexity
