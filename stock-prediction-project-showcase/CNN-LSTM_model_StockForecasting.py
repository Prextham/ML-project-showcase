# CNN-LSTM Model for Stock Forecasting
# Hey there! This file contains the core architecture for the hybrid
# CNN-LSTM model I designed. I wanted to show just the "brains" of the
# operation, without all the data loading and training.

import tensorflow as tf
from tensorflow.keras import layers

def build_model(time_steps=60, features=17):
    """
    Builds the hybrid CNN-LSTM model.

    The main idea here was to get the best of both worlds:
    1. Use a quick and efficient CNN layer to scan the time-series data
       and pick out important short-term patterns.
    2. Feed those patterns into an LSTM, which is great at understanding
       the longer-term sequence and context.

    It's a nice one-two punch for complex sequence data.
    """
    model = tf.keras.Sequential()

    # First up, the CNN layer. I'm treating the time-series window like a
    # small, one-dimensional "image". The Conv1D acts like a scanner,
    # finding useful patterns (like small dips or spikes) in the data.
    model.add(layers.Conv1D(
        filters=32,
        kernel_size=3,
        activation='relu',
        input_shape=(time_steps, features)
    ))
    model.add(layers.MaxPooling1D(pool_size=2))

    # Next, the LSTM layer. This is the memory and context part of the model.
    # It takes the patterns found by the CNN and figures out how they
    # fit together over the long term. 100 units gave it enough capacity
    # to learn the complex dynamics without being too slow.
    model.add(layers.LSTM(units=100))

    # Finally, a couple of standard dense layers to interpret the LSTM's
    # output and make the final price prediction. I added a Dropout layer
    # here as a simple guard against overfitting.
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(units=50, activation='relu'))
    model.add(layers.Dense(units=1)) # Just one output neuron for our target price.

    return model