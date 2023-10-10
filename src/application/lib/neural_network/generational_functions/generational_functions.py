"""
Cross over weight functions used to generate new generation weights
"""

import random
import numpy as np

from src.application.lib.neural_network.generational_functions.generational_functions_factory import (
    GenerationalFunctionsFactory,
)


@GenerationalFunctionsFactory.register("crossover_weights_average")
def crossover_weights_average(
    weight_set_a: np.array, weight_set_b: np.array
) -> np.array:
    """Cross over parent weights giving the avergae of each parent weight"""
    new_weight_set_sum: np.array = np.add(weight_set_a, weight_set_b)
    new_weight_set: np.array = np.divide(new_weight_set_sum, 2)
    return new_weight_set


@GenerationalFunctionsFactory.register("crossover_weights_mergining")
def crossover_weights_mergining(
    weight_set_a: np.array, weight_set_b: np.array
) -> np.array:
    """Cross over parents weight by randomly selecting from each parent"""

    new_weights = weight_set_a
    for index_x, weights in enumerate(weight_set_a):
        for index_y, _ in enumerate(weights):
            selection_chance = random.randrange(1, 100)
            if selection_chance > 50:
                new_weights[index_x][index_y] = weight_set_b[index_x][index_y]

    new_weights = np.array(new_weights)

    return new_weights
