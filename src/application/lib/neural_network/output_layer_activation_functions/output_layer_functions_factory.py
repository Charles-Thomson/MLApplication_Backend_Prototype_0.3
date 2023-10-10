"""Output layer functions factory"""
import numpy as np


class OutputLayerActvaitionFactory:
    """Factory for output layer activaition functions"""

    output_layer_activation_functions = {}

    @classmethod
    def get_output_activation_func(cls, activation_function):
        """Generate the brain based of given type"""
        try:
            retreval = cls.output_layer_activation_functions[activation_function]

        except KeyError as err:
            raise NotImplementedError(f"{activation_function} Not implemented") from err

        return retreval

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.output_layer_activation_functions[type_name] = deco_cls
            return deco_cls

        return deco


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
