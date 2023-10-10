"""generational functions factory"""
import numpy as np
import random


class GenerationalFunctionsFactory:
    """Factory for geerational functions"""

    generational_functions = {}

    @classmethod
    def get_generation_func(cls, generational_funcation):
        """Generate the brain based of given type"""
        try:
            retreval = cls.generational_functions[generational_funcation]

        except KeyError as err:
            raise NotImplementedError(
                f"{generational_funcation} Not implemented"
            ) from err

        return retreval

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.generational_functions[type_name] = deco_cls
            return deco_cls

        return deco


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
