#!/usr/bin/env python3

import logging

def fit_iter_params(data_length: int,
                    ideal_num_steps: int,
                    ideal_batch_size: int):
    """
    Find the number of time steps and batch size that are suitable for an RNN input data set.

    :param data_length: Number of elements in the input data
    :param ideal_num_steps: Preferred number of time steps in the RNN
    :param ideal_batch_size: Preferred batch size
    :returns: Number of steps and batch size that can be used for the given data set
    """
    num_steps = ideal_num_steps
    batch_size = ideal_batch_size

    if data_length < num_steps:
        logging.warning("Length of input data is shorter than preferred number of steps (%d). Reducing number of steps.", num_steps)
        num_steps = data_length - 1

    if data_length < batch_size * num_steps:
        logging.warning("Length of input data is shorter than number of elements in a batch (batch size = %d * num steps = %d). Setting batch size to 1.", batch_size, num_steps)
        batch_size = 1

    return num_steps, batch_size
