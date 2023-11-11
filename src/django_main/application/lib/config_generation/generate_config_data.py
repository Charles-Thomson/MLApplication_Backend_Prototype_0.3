"""
Generate a config object(dict) for the system based on the given input data(json)
"""
import json
import numpy as np


from application.lib.neural_network.generational_functions.generational_functions_factory import (
    GenerationalFunctionsFactory as GF_factory,
)
from application.lib.neural_network.hidden_layer_activation_functions.hidden_layer_functions_factory import (
    HiddenLayerActvaitionFactory as HLA_factory,
)
from application.lib.neural_network.output_layer_activation_functions.output_layer_functions_factory import (
    OutputLayerActvaitionFactory as OLA_factory,
)
from application.lib.neural_network.weight_huristics.weight_huristics_factory import (
    WeightHuristicsFactory as WH_Factory,
)


def generate_instance_configuration_data(input_config: json) -> dict:
    """
    Generate the configuation data from a given input_config
    var: input_config - json file from API containing config data]
    rtn: instance_config_data - internal config based on given input_config
    """

    input_config_loaded: dict = json.loads(input_config)
    map_config: dict = input_config_loaded["map_config"]
    brain_config: dict = input_config_loaded["brain_config"]

    instance_config_data: dict = {
        "env_type": input_config_loaded["env_type"],
        "agent_type": input_config_loaded["agent_type"],
        "instance_id": input_config_loaded["instance_id"],
        "hyper_perameters": input_config_loaded["hyper_perameters"],
        "map_data": {
            "env_map": np.fromstring(map_config["env_map"], dtype=int, sep=",").reshape(
                map_config["map_dimensions"], -1
            ),
            "start_location": map_config["start_location"],
            "max_step_count": map_config["max_step_count"],
        },
        "brain_config": {
            "input_to_hidden_connections": brain_config["input_to_hidden_connections"],
            "hidden_to_output_connections": brain_config[
                "hidden_to_output_connections"
            ],
            "brain_type": "",
            "brain_id": "",
            "fitness": 0.0,
            "traversed_path": [],
            "fitness_by_step": [],
            "current_generation_number": 0,
            "functions_callable": {
                "weight_init_huristic": WH_Factory.get_huristic(
                    brain_config["weight_init_huristic"]
                ),
                "hidden_activation_func": HLA_factory.get_hidden_activation_func(
                    brain_config["hidden_activation_func"]
                ),
                "output_activation_func": OLA_factory.get_output_activation_func(
                    brain_config["output_activation_func"]
                ),
                "new_generation_func": GF_factory.get_generation_func(
                    brain_config["new_generation_func"]
                ),
            },
            "weights": {"hidden_weights": "", "output_weights": ""},
        },
    }
    return instance_config_data
