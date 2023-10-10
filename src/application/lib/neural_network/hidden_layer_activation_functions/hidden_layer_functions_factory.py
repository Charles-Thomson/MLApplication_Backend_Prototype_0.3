"""Hidden layer functions factory"""
import numpy as np


class HiddenLayerActvaitionFactory:
    """Factory for hidden layer activaition functions"""

    hidden_layer_activation_functions = {}

    @classmethod
    def get_hidden_activation_func(cls, activation_function):
        """Generate the brain based of given type"""
        try:
            retreval = cls.hidden_layer_activation_functions[activation_function]

        except KeyError as err:
            raise NotImplementedError(f"{activation_function} Not implemented") from err

        return retreval

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.hidden_layer_activation_functions[type_name] = deco_cls
            return deco_cls

        return deco


@HiddenLayerActvaitionFactory.register("linear_activation_function")
def linear_activation_function(value: float) -> float:
    """Returns given value - gives linear result"""
    return value


@HiddenLayerActvaitionFactory.register("rectified_linear_activation_function")
def rectified_linear_activation_function(value: float) -> float:
    """ReL activation function - x is 0 or x"""
    return np.round(max(0.0, value), decimals=3)


@HiddenLayerActvaitionFactory.register("leaky_rectified_linear_function")
def leaky_rectified_linear_function(value: float) -> float:
    """Leaky ReL activation function - x is 0.01*x or x"""
    if value > 0:
        return value
    else:
        return 0.01 * value


@HiddenLayerActvaitionFactory.register("sigmoid_activation_fucntion")
def sigmoid_activation_fucntion(value: float) -> float:
    """Sigmoidal activation function - x is between 0 -> 1"""
    return 1 / (1 + np.exp(value))


@HiddenLayerActvaitionFactory.register("hyperbolic_tangent_activation_function")
def hyperbolic_tangent_activation_function(value: float) -> float:
    """tanh activation funtion - gives x is between -1.0 and 1.0"""
    return (np.exp(value) - np.exp(-value)) / (np.exp(value) + np.exp(-value))
