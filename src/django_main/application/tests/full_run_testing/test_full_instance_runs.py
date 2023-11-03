"""Test run the full system with different run duration instances """

import json
from application.lib.instance_generation.instance_generation_main import new_instance

import pytest


@pytest.mark.django_db
def test_long_duration_instance() -> None:
    """
    Testing a full run of an instance
    """
    test_input_config: dict = {
        "env_type": "Static_State",
        "agent_type": "Static_State",
        "instance_id": "this_instance_id",
        "map_config": {
            "env_map": "1,1,1,1,1,1,1,1,3,1,1,1,2,1,1,1,1,2,3,1,1,3,1,3,1",
            "map_dimensions": 5,
            "start_location": (1, 1),
            "max_step_count": 20,
        },
        "hyper_perameters": {
            "max_number_of_genrations": 40,
            "max_generation_size": 200,
            "fitness_threshold": 3.0,
            "new_generation_threshold": 10,
            "generation_failure_threshold": 10,
        },
        "brain_config": {
            "weight_init_huristic": "he_weight",
            "hidden_activation_func": "linear_activation_function",
            "output_activation_func": "argmax_activation",
            "new_generation_func": "crossover_weights_average",
            "input_to_hidden_connections": (24, 9),
            "hidden_to_output_connections": (9, 9),
        },
    }

    test_input_config_json: json = json.dumps(test_input_config)

    test_instance = new_instance(input_config=test_input_config_json)

    test_instance.run_instance()


@pytest.mark.django_db
def test_short_duration_instance() -> None:
    """
    Testing a full run of an instance
    """
    test_input_config: dict = {
        "env_type": "Static_State",
        "agent_type": "Static_State",
        "instance_id": "this_instance_id",
        "map_config": {
            "env_map": "1,1,1,1,1,1,1,1,3,1,1,1,2,1,1,1,1,2,3,1,1,3,1,3,1",
            "map_dimensions": 5,
            "start_location": (1, 1),
            "max_step_count": 20,
        },
        "hyper_perameters": {
            "max_number_of_genrations": 5,
            "max_generation_size": 100,
            "fitness_threshold": 3.0,
            "new_generation_threshold": 10,
            "generation_failure_threshold": 10,
        },
        "brain_config": {
            "weight_init_huristic": "he_weight",
            "hidden_activation_func": "linear_activation_function",
            "output_activation_func": "argmax_activation",
            "new_generation_func": "crossover_weights_average",
            "input_to_hidden_connections": (24, 9),
            "hidden_to_output_connections": (9, 9),
        },
    }

    test_input_config_json: json = json.dumps(test_input_config)

    test_instance = new_instance(input_config=test_input_config_json)

    test_instance.run_instance()


# test_map
# 1, 1, 1, 1, 1,
# 1, 1, 1, 3, 1,
# 1, 1, 2, 1, 1,
# 1, 1, 2, 1, 1,
# 1, 3, 1, 3, 1
