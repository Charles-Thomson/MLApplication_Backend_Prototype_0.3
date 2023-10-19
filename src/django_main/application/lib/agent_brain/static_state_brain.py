"""Instance of a brain used by a agent"""
import json
import numpy as np


class BrainInstance:
    """Instance of agent brian"""

    def __init__(self, brain_config: dict) -> None:
        """Setup the core elements of the brain"""

        self.brain_id: str = brain_config["brain_id"]

        self.brain_config: dict = brain_config
        self.brain_type: str = brain_config["brain_type"]
        self.fitness: float = brain_config["fitness"]
        self.traversed_path: list[tuple] = brain_config["traversed_path"]
        self.fitness_by_step: list[float] = brain_config["fitness_by_step"]
        self.current_generation_number: int = brain_config["current_generation_number"]
        self.hidden_weights: np.array = brain_config["weights"]["hidden_weights"]
        self.output_weights: np.array = brain_config["weights"]["output_weights"]
        self.functions_callable: dict = brain_config["functions_callable"]

        self.hidden_layer_activation_func: callable = self.functions_callable[
            "hidden_activation_func"
        ]
        self.output_layer_activation_func: callable = self.functions_callable[
            "output_activation_func"
        ]

        # self.svg_path: str = ""
        # self.svg_start: str = ""
        # self.svg_end: str = ""

    # TODO: See if the approach of setting the ann after use and returing it is better ?
    def update_and_return_config(self):
        """
        Update and return the brains config file
        """

    def determin_action(self, sight_data: np.array) -> int:
        """Determin best action based on given data/activation"""

        hidden_layer_dot_product = np.dot(sight_data, self.hidden_weights)

        vectorize_func = np.vectorize(self.hidden_layer_activation_func)
        hidden_layer_activation = vectorize_func(hidden_layer_dot_product)

        output_layer_dot_product = np.dot(hidden_layer_activation, self.output_weights)

        return self.output_layer_activation_func(output_layer_dot_product)
