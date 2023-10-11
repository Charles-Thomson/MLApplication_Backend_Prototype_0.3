"""Instance of a brain used by a agent"""
import numpy as np


class BrainInstance:
    """Instance of agent brian"""

    def __init__(self, current_generation_number, brain_config: dict) -> None:
        """Setup the core elements of the brain"""

        # TODO: These elements need to be added to the config
        self.fitness: float = brain_config["fitness"]
        self.traversed_path: list[tuple] = brain_config["traversed_path"]
        self.fitness_by_step: list[float] = brain_config["fitness_by_step"]
        self.current_generation_number: int = current_generation_number

        self.brain_type = brain_config["brain_type"]
        self.brain_id: str = brain_config["brain_id"]

        self.hidden_layer_activation_func: callable = brain_config[
            "funcations_callable"
        ]["hidden_activation_func"]
        self.output_layer_activation_func: callable = brain_config[
            "funcations_callable"
        ]["output_activation_func"]

        # working on this
        self.hidden_weights: np.array = brain_config["hidden_weights"]
        self.output_weights: np.array = brain_config["output_weights"]

        self.functions_refs: dict = brain_config["functions_ref"]

        # self.svg_path: str = ""
        # self.svg_start: str = ""
        # self.svg_end: str = ""

    def determin_action(self, sight_data: np.array) -> int:
        """Determin best action based on given data/activation"""

        hidden_layer_dot_product = np.dot(sight_data, self.hidden_weights)

        vectorize_func = np.vectorize(self.hidden_layer_activation_func)
        hidden_layer_activation = vectorize_func(hidden_layer_dot_product)

        output_layer_dot_product = np.dot(hidden_layer_activation, self.output_weights)

        return self.output_layer_activation_func(output_layer_dot_product)

    def set_attributes_to_bytes(self) -> None:
        """Covert the np.arrays to bytes for DB storage"""

        self.hidden_weights = self.hidden_weights.tobytes()
        self.output_weights = self.output_weights.tobytes()
        self.traversed_path = ",".join(str(val) for val in self.traversed_path)
        self.fitness_by_step = ",".join(str(val) for val in self.fitness_by_step)

    def get_attributes_from_bytes(self) -> None:
        """Convert the weights from bytes to np.arrays"""

        self.hidden_weights = np.frombuffer(self.hidden_weights).reshape(24, -1)
        self.output_weights = np.frombuffer(self.output_weights).reshape(9, -1)
        self.traversed_path = self.traversed_path.split(",")
        self.fitness_by_step = self.fitness_by_step.split(",")
