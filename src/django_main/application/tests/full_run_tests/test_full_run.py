from src.django_main.application.lib.instance_generation.instance_generation_main import (
    new_instance,
)

from src.django_main.application.logging.logging_for_testing import (
    with_test_brian_logging,
)


@with_test_brian_logging
def test_full_instance() -> None:
    test_config = {
        "env_type": "Static_State",
        "agent_type": "Static_State",
        "env_config": {
            "env_map": "1,1,1,1,1,1,1,1,3,1,1,1,2,1,1,1,1,2,3,1,1,3,1,3,1",
            "map_dimensions": "5",
            "start_location": "1,1",
        },
        "instance_config": {
            "max_number_of_genrations": "5",
            "max_generation_size": "100",
            "fitness_threshold": "2",
            "new_generation_threshold": "4",
        },
        "ann_config": {
            "weight_init_huristic": "he_weight",
            "hidden_activation_func": "linear_activation_function",
            "output_activation_func": "argmax_activation",
            "new_generation_func": "crossover_weights_average",
            "input_to_hidden_connections": "(24,9)",
            "hidden_to_output_connections": "(9,9)",
        },
    }
    test_instance = new_instance(config=test_config)

    test_brains = test_instance.run_instance()

    return test_brains, test_config["env_config"]["env_map"]
