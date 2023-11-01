"""Test the formatting of the input_config_data to the instance_config_data"""
import json
import numpy as np
from application.lib.config_generation.generate_config_data import (
    generate_instance_configuration_data,
)
from application.lib.config_file_structure import generate_test_input_config_as_json


def test_input_config_to_system_config() -> None:
    """
    Test the cration of a insatce_config from the given input_config
    """

    test_id: str = "test_configuration_id"

    test_input_config: json = generate_test_input_config_as_json(
        test_instance_id=test_id
    )

    test_instance_config: dict = generate_instance_configuration_data(
        input_config=test_input_config
    )

    hyper_perameters = test_instance_config["hyper_perameters"]
    map_data = test_instance_config["map_data"]
    brain_config = test_instance_config["brain_config"]
    weights = test_instance_config["weights"]

    assert type(test_input_config) is type(dict)

    assert type(hyper_perameters) is type(dict)
    assert type(map_data) is type(dict)
    assert type(brain_config) is type(dict)
    assert type(weights) is type(dict)

    assert test_input_config["instance_id"] == test_id

    assert type(hyper_perameters["max_number_of_genrations"]) is type(int)
    assert type(hyper_perameters["max_generation_size"]) is type(int)
    assert type(hyper_perameters["fitness_threshold"]) is type(float)
    assert type(hyper_perameters["max_number_of_genrations"]) is type(int)

    assert type(map_data["env_map"]) is type(np.ndarray)
    assert type(map_data["start_location"]) is type(tuple)

    assert type(brain_config["input_to_hidden_connections"]) is type(tuple)
    assert type(brain_config["hidden_to_output_connections"]) is type(tuple)

    brain_functions_callable = brain_config["functions_callable"]

    assert type(brain_functions_callable) is type(dict)

    assert type(brain_functions_callable["weight_init_huristic"]) is type(callable)
    assert type(brain_functions_callable["hidden_activation_func"]) is type(callable)
    assert type(brain_functions_callable["output_activation_func"]) is type(callable)
    assert type(brain_functions_callable["new_generation_func"]) is type(callable)
