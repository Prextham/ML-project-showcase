# Transformer Model for Stock Forecasting

# Hey! This is the architectural snippet for my Transformer model.
# In my final ensemble, this model played the role of the "Holistic Strategist."
# Unlike an LSTM that processes data step-by-step, the Transformer looks at the
# entire 60-day window all at once. This gives it a unique, big-picture
# perspective.
#
# While it might miss some of the sharp daily spikes, its strength is that it's
# much less likely to get fooled by short-term noise. It provided a crucial
# stabilizing view that made the whole ensemble stronger.


import tensorflow as tf
from tensorflow.keras import layers, Model

def transformer_encoder_block(inputs, head_size=256, num_heads=4, ff_dim=4, dropout=0.1):
    """
    This is the core building block of the Transformer.

    Its job is to look at the entire sequence and decide which data points
    are most important for understanding the overall context.
    """
    # Part 1: The Attention Mechanism
    # This is what lets the model look at the full picture. For every single
    # point in time, it can connect it to every other point in the 60-day
    # window, weighing how relevant they are to each other. This creates that
    # smooth, holistic view of the trend.
    attention = layers.MultiHeadAttention(
        key_dim=head_size, num_heads=num_heads, dropout=dropout
    )(inputs, inputs)
    attention = layers.Dropout(dropout)(attention)
    add_attention = layers.LayerNormalization(epsilon=1e-6)(inputs + attention)

    # Part 2: The Feed-Forward Network
    # After the attention layer figures out the context, this simple network
    # just does some additional processing on that information.
    ffn = layers.Dense(ff_dim, activation="relu")(add_attention)
    ffn = layers.Dense(inputs.shape[-1])(ffn)
    ffn = layers.Dropout(dropout)(ffn)
    return layers.LayerNormalization(epsilon=1e-6)(add_attention + ffn)


def build_transformer_model(time_steps=60, features=17, num_blocks=2):
    """
    Builds the full Transformer model by stacking the encoder blocks.
    """
    inputs = layers.Input(shape=(time_steps, features))
    x = inputs

    # I stacked two blocks. This allows the model to build up a more
    # sophisticated understanding of the data's long-term relationships.
    for _ in range(num_blocks):
        x = transformer_encoder_block(x)

    # Condense the full 60-day output into a single representative vector
    # that captures the model's overall "holistic" analysis.
    x = layers.GlobalAveragePooling1D(data_format="channels_last")(x)

    # A couple of final layers to make the actual price prediction based on
    # the high-level context it has learned.
    x = layers.Dense(64, activation="relu")(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(1)(x)

    return Model(inputs=inputs, outputs=outputs)

# As always, leaving the model uncompiled. This file is all about the
# "blueprint" of the model, not the training setup.

