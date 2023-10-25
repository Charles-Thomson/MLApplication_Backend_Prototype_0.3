"""Test a long run of the overall system """

from application.lib.instance_generation.instance_generation_main import new_instance

import pytest


@pytest.mark.django_db
def test_long_duration_instance() -> None:
    """
    Testing a full run of an instance
    """
    test_config = {
        "env_type": "Static_State",
        "agent_type": "Static_State",
        "env_config": {
            "env_map": "1,1,1,1,1,1,1,1,3,1,1,1,2,1,1,1,1,2,3,1,1,3,1,3,1",
            "map_dimensions": "5",
            "start_location": "1,1",
        },
        "instance_config": {
            "max_number_of_genrations": "40",
            "max_generation_size": "200",
            "fitness_threshold": "3",
            "new_generation_threshold": "10",
        },
        "brain_config": {
            "weight_init_huristic": "he_weight",
            "hidden_activation_func": "linear_activation_function",
            "output_activation_func": "argmax_activation",
            "new_generation_func": "crossover_weights_average",
            "input_to_hidden_connections": "[24,9]",
            "hidden_to_output_connections": "[9,9]",
        },
    }
    test_instance = new_instance(config=test_config)

    test_instance.run_instance()


# test_map
# 1, 1, 1, 1, 1,
# 1, 1, 1, 3, 1,
# 1, 1, 2, 1, 1,
# 1, 1, 2, 1, 1,
# 1, 3, 1, 3, 1
