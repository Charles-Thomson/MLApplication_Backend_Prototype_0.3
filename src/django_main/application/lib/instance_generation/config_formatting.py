"""Formatting of the json config file to the appropriate format"""
import numpy as np


from src.django_main.application.lib.neural_network.generational_functions.generational_functions_factory import (
    GenerationalFunctionsFactory,
)
from src.django_main.application.lib.neural_network.hidden_layer_activation_functions.hidden_layer_functions_factory import (
    HiddenLayerActvaitionFactory,
)
from src.django_main.application.lib.neural_network.output_layer_activation_functions.output_layer_functions_factory import (
    OutputLayerActvaitionFactory,
)
from src.django_main.application.lib.neural_network.weight_huristics.weight_huristics_factory import (
    WeightHuristicsFactory,
)


def format_instance_config(config: dict) -> dict:
    """Format the json config to the appropriate types"""
    this_instance_config = {
        "max_number_of_genrations": "",
        "max_generation_size": "",
        "fitness_threshold": "",
        "new_generation_threshold": "",
    }

    this_instance_config["max_number_of_genrations"] = int(
        config["max_number_of_genrations"]
    )
    this_instance_config["max_generation_size"] = int(config["max_generation_size"])
    this_instance_config["fitness_threshold"] = float(config["fitness_threshold"])
    this_instance_config["new_generation_threshold"] = int(
        config["new_generation_threshold"]
    )

    return this_instance_config


# TODO: Rename the ann_config to barin config ??
# Move the setting of the functions into the Brain_Factoy ?
def format_ann_config(ann_config: dict) -> dict:
    """Format the ann config from dict[str:str] to dict[str:type]"""

    formatted_ann_config: dict = {
        "input_to_hidden_connections": "",
        "hidden_to_output_connections": "",
        "brain_type": "",
        "brain_id": "",
        "fitness": 0.0,
        "traversed_path": [],
        "fitness_by_step": [],
        "current_generation_number": 0,
        "functions_ref": {
            "weight_init_huristic": "",
            "hidden_activation_func": "",
            "output_activation_func": "",
            "new_generation_func": "",
        },
        "funcations_callable": {
            "weight_init_huristic": "",
            "hidden_activation_func": "",
            "output_activation_func": "",
            "new_generation_func": "",
        },
    }

    formatted_ann_config["brain_id"] = ""

    formatted_ann_config["funcations_callable"]["weight_init_huristic"] = ann_config[
        "weight_init_huristic"
    ]
    formatted_ann_config["funcations_callable"]["hidden_activation_func"] = ann_config[
        "hidden_activation_func"
    ]
    formatted_ann_config["funcations_callable"]["output_activation_func"] = ann_config[
        "output_activation_func"
    ]
    formatted_ann_config["funcations_callable"]["new_generation_func"] = ann_config[
        "new_generation_func"
    ]

    # TODO: Refactor out the use of eval
    formatted_ann_config["input_to_hidden_connections"]: tuple[int, int] = eval(
        ann_config["input_to_hidden_connections"]
    )
    formatted_ann_config["hidden_to_output_connections"]: tuple[int, int] = eval(
        ann_config["hidden_to_output_connections"]
    )

    return formatted_ann_config


def format_env_config(config: dict) -> dict:
    """Format the Json data to a dict to be passed to the environment factory
    var: config - Recived json file
    rtn: env_config - Json file in dict format
    """

    env_config = {
        "env_map": "",
        "map_dimensions": "",
        "start_location": "",
        "fitness_threshold": "",
    }

    env_map_string: str = config["env_map"]
    env_map_unshaped: np.array = np.fromstring(env_map_string, dtype=int, sep=",")
    reshape_val: int = int(config["map_dimensions"])

    env_map_shaped: np.array = env_map_unshaped.reshape(reshape_val, -1)
    env_config["env_map"] = env_map_shaped

    env_config["map_dimensions"] = int(config["map_dimensions"])

    start_x, start_y = config["start_location"].split(",")
    env_config["start_location"] = (int(start_x), int(start_y))

    return env_config
