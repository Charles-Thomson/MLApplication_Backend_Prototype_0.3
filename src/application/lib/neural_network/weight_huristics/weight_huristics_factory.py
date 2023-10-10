"""weight huristics functions factory"""

from math import sqrt
import numpy as np
from numpy.random import randn, rand


class WeightHuristicsFactory:
    """Factory for weight huristics activaition functions"""

    weight_huristics_functions = {}

    @classmethod
    def get_huristic(cls, weight_huristic: str):
        """Get weight huristic of given type"""

        try:
            retreval = cls.weight_huristics_functions[weight_huristic]

        except KeyError as err:
            raise NotImplementedError(f"{weight_huristic} Not implemented") from err

        return retreval

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.weight_huristics_functions[type_name] = deco_cls
            return deco_cls

        return deco


@WeightHuristicsFactory.register("he_weight")
def he_weight_init_generator(layer_connections: tuple[int, int]) -> list[float]:
    """HE weight initalization"""
    input_layer_size, output_layer_size = layer_connections

    std = sqrt(2.0 / input_layer_size)
    n = input_layer_size * output_layer_size
    numbers = randn(n)
    scaled = np.round(numbers * std, decimals=3)
    for element in scaled:
        yield element


@WeightHuristicsFactory.register("xavier_weight")
def xavier_weight_init_generator(layer_connections: tuple[int, int]) -> list[float]:
    """xzavier weight initalizations"""
    input_layer_size, output_layer_size = layer_connections

    upper_bounds, lower_bounds = -(1 / sqrt(input_layer_size)), (
        1 / sqrt(input_layer_size)
    )
    n = input_layer_size * output_layer_size
    numbers = rand(n)

    scaled = np.round(
        lower_bounds + numbers * (upper_bounds - lower_bounds), decimals=3
    )
    for element in scaled:
        yield element


@WeightHuristicsFactory.register("normalized_xavier_weight")
def normalized_xavier_weight_init_generator(
    layer_connections: tuple[int, int]
) -> list[float]:
    """normalized xzavier weight initalizations"""
    input_layer_size, output_layer_size = layer_connections
    n = input_layer_size + output_layer_size
    lower_bounds, upper_bounds = -(sqrt(6.0) / sqrt(n)), (sqrt(6.0) / sqrt(n))

    n_numbers = input_layer_size * output_layer_size

    # Numbers
    numbers = rand(n_numbers)
    # Scale numbers to bounds
    scaled = np.round(
        lower_bounds + numbers * (upper_bounds - lower_bounds), decimals=3
    )
    for element in scaled:
        yield element
