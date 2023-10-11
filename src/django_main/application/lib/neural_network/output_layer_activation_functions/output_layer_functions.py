"""Hidden layer activation functions"""
import numpy as np

from application.lib.neural_network.output_layer_activation_functions.output_layer_functions_factory import (
    OutputLayerActvaitionFactory,
)


@OutputLayerActvaitionFactory.register("argmax_activation")
def argmax_activation(vector: np.array) -> int:
    """ArgMax output layer activation function"""
    return np.argmax(vector)


@OutputLayerActvaitionFactory.register("soft_argmax_activation")
def soft_argmax_activation(vector: np.array) -> int:
    """soft argmax oultput layer activation fucntion"""
    vector_exp = np.exp(vector)
    vector_sum = vector_exp / vector_exp.sum()
    return np.argmax(vector_sum)
