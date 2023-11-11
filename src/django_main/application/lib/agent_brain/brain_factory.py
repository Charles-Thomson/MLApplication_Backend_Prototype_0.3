"""Brain generation in the form of a factory"""
from __future__ import annotations
from copy import deepcopy
import random
import numpy as np

from application.lib.agent_brain.static_state_brain import BrainInstance


class BrainFactory:
    """
    Brain generation factory
    rtn: retreval - the brain of the given type/ var brain_type
    """

    brain_types = {}

    @classmethod
    def make_brain(
        cls,
        brain_config: dict,
        parents: list[BrainInstance] = None,
    ):
        """Generate the brain based of given type"""

        brain_type = brain_config["brain_type"]
        try:
            retreval = cls.brain_types[brain_type]

        except KeyError as err:
            raise NotImplementedError(f"{brain_type} Not implemented") from err

        return retreval(brain_config=brain_config, parents=parents)

    @classmethod
    def register(cls, type_name):
        """Register an brain enerator to the factory"""

        def deco(deco_cls):
            cls.brain_types[type_name] = deco_cls
            return deco_cls

        return deco


@BrainFactory.register("base_brain_instance")
def base_brain_instance(brain_config: dict, parents=None) -> BrainInstance:
    """
    Return a generic brain instance
    usage - Converting a models.Model back to a brain instance
    var: brain_config - the config file of the brain instance
    var: parents - not used
    rnt: A new Brain Instance
    """
    return BrainInstance(
        brain_config=brain_config,
    )


@BrainFactory.register("generational_weighted_brain")
def new_generational_weighted_brain(
    brain_config: dict, parents: list[BrainInstance]
) -> BrainInstance:
    """
    Generate a new generationally weighted brain
    var: brain_config - the config file of the brain instance
    var: parents - parent brain instances used to generate new instance
    """

    mutation_threshold: int = 50

    new_generation_function: callable = brain_config["functions_callable"][
        "new_generation_func"
    ]

    val: int = len(parents)
    weightings: list[float] = tuple(val / i for i in range(1, val + 1))

    parent_a, parent_b = random.choices(parents, weights=weightings, k=2)

    parent_a: BrainInstance = deepcopy(parent_a)
    parent_b: BrainInstance = deepcopy(parent_b)

    new_input_to_hidden_weight: np.array = new_generation_function(
        parent_a.hidden_weights, parent_b.hidden_weights
    )

    new_hidden_to_output_weights: np.array = new_generation_function(
        parent_a.output_weights, parent_b.output_weights
    )

    if random.randint(0, 100) > mutation_threshold:
        random_selection = random.randint(0, 1)
        if random_selection == 0:
            new_input_to_hidden_weight = apply_mutation(new_input_to_hidden_weight)

        if random_selection == 1:
            new_hidden_to_output_weights = apply_mutation(new_hidden_to_output_weights)

    brain_config["weights"]["hidden_weights"] = new_input_to_hidden_weight
    brain_config["weights"]["output_weights"] = new_hidden_to_output_weights

    return BrainInstance(
        brain_config=brain_config,
    )


def apply_mutation(weight_set: np.array) -> np.array:
    """
    Apply a +/- 1-10% mutation to the weights to give variance
    var: weight_set - set of given weights to be mutated
    rtn: weight_set - weight_set post mtation
    """

    weight_set_shape: tuple = weight_set.shape

    # select random weight from set

    x_loc: int = random.randrange(weight_set_shape[0])
    y_loc: int = random.randrange(weight_set_shape[1])

    weight_to_mutate: float = weight_set[x_loc][y_loc]

    mutation_amount: int = random.randint(1, 10)
    positive_mutation: float = weight_to_mutate - (weight_to_mutate / mutation_amount)
    negitive_mutation: float = weight_to_mutate + (weight_to_mutate / mutation_amount)

    mutation: float = random.choice((positive_mutation, negitive_mutation))

    weight_set[x_loc][y_loc] = mutation

    return weight_set


@BrainFactory.register("random_weighted_brain")
def new_random_weighted_brain(brain_config: dict, parents: list) -> BrainInstance:
    """
    Generate a randomly weighted brain
    var: brain_config - the config file of the brain instance
    var: parents - unused
    rtn: BrainInstance - A randomly weight brain instance
    """

    hidden_weights: np.array = initialize_weights(
        layer_connections=brain_config["input_to_hidden_connections"],
        weight_heuristic_func=brain_config["functions_callable"][
            "weight_init_huristic"
        ],
    )

    output_weights: np.array = initialize_weights(
        layer_connections=brain_config["hidden_to_output_connections"],
        weight_heuristic_func=brain_config["functions_callable"][
            "weight_init_huristic"
        ],
    )

    brain_config["weights"]["hidden_weights"] = hidden_weights
    brain_config["weights"]["output_weights"] = output_weights

    return BrainInstance(
        brain_config=brain_config,
    )


def initialize_weights(
    layer_connections: tuple[int, int], weight_heuristic_func: callable
) -> np.array:
    """
    Generate random weigths between to layers of a specified sizes
    var: layer_connections - number of connections between two layers
    var: weight_heuristic_func - the init huristic of the weights
    rtn: rand_weights - Generated weights
    """
    get_weight = weight_heuristic_func(layer_connections)

    sending_layer, reciving_layer = layer_connections
    rand_weights: np.array = np.array(
        [
            [next(get_weight) for i in range(reciving_layer)]
            for i in range(sending_layer)
        ]
    )

    return rand_weights
