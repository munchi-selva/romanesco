#!/usr/bin/env python3

EOS = '<eos>'
LBR = '<LBR>'
UNK = '<unk>'
TOKEN_PATTERN = '[,;:!?.“”()—]|[^,;:!?.“”()—\s]+'   # Customized to Shakespearean text

# default values

MODEL_PATH = "model"
VAL_MODEL_PATH = "val"
LOGS_PATH = "logs"

MODEL_FILENAME = 'model'
VAL_MODEL_FILENAME = MODEL_FILENAME + '.val'
VOCAB_FILENAME = 'vocab.json'

CONFIG_FILENAME = 'config.json'

VOCAB_SIZE = 10000
BATCH_SIZE = 64

NUM_EPOCHS = 10
VAL_EPOCHS = 1
PATIENCE = 5

# num_steps and learning_rate are hardcoded here; at the moment,
# the only way to change them is to edit this file
NUM_STEPS = 100 # truncated backprop length
                # formerly 35, experiments with Shakespeare functioned better with 25
LEARNING_RATE = 0.001   # formerly 0.0001

HIDDEN_SIZE = 1024  # RNN state size, formerly 1500
EMBEDDING_SIZE = 256  # embedding vector size

SAMPLE_LENGTH = 100
