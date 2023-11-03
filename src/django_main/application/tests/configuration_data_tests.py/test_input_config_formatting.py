"""Test the formatting of the input_config_data to the instance_config_data"""
import json
import numpy as np
from application.lib.config_generation.generate_config_data import (
    generate_instance_configuration_data,
)
from application.lib.config_generation.config_file_structure import (
    generate_test_input_config_as_json,
)

from typing import Callable


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
    weights = brain_config["weights"]

    assert isinstance(test_instance_config, dict)

    assert isinstance(hyper_perameters, dict)
    assert isinstance(map_data, dict)
    assert isinstance(brain_config, dict)
    assert isinstance(weights, dict)

    assert test_instance_config["instance_id"] == test_id

    assert isinstance(hyper_perameters["max_number_of_genrations"], int)
    assert isinstance(hyper_perameters["max_generation_size"], int)
    assert isinstance(hyper_perameters["fitness_threshold"], float)
    assert isinstance(hyper_perameters["new_generation_threshold"], float)
    assert isinstance(hyper_perameters["generation_failure_threshold"], int)

    assert isinstance(type(map_data["env_map"]), type(np.ndarray))
    assert isinstance(map_data["start_location"], list)

    assert isinstance(brain_config["input_to_hidden_connections"], list)
    assert isinstance(brain_config["hidden_to_output_connections"], list)

    brain_functions_callable = brain_config["functions_callable"]

    assert isinstance(brain_functions_callable, dict)

    assert isinstance(brain_functions_callable["weight_init_huristic"], Callable)
    assert isinstance(brain_functions_callable["hidden_activation_func"], Callable)
    assert isinstance(brain_functions_callable["output_activation_func"], Callable)
    assert isinstance(brain_functions_callable["new_generation_func"], Callable)
