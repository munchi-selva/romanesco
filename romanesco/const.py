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
BATCH_SIZE = 32

NUM_EPOCHS = 50
VAL_EPOCHS = 1
PATIENCE = 5

NUM_STEPS = 100 # truncated backprop length

# learning_rate is hardcoded here; at the moment,
# the only way to change it is to edit this file
LEARNING_RATE = 0.001   # formerly 0.0001

HIDDEN_SIZE = 1024  # RNN state size, formerly 1500
EMBEDDING_SIZE = 256  # embedding vector size

SAMPLE_LENGTH = 100
