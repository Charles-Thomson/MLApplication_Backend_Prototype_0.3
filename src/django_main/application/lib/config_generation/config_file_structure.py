"""
This is the format of the data that is to be passed to the system
This dict will be in the json format and will needed json.loads
It will keep the correct types
Instance_config.instance id will be used to collect the data when completed
- this may need to be stored in the API/GQL call
"""
import json

base_input_config_rework: dict = {
    "env_type": "Static_State",
    "agent_type": "",
    "instance_id": "this_instance_id",
    "map_config": {
        "env_map": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
        "map_dimensions": 4,
        "start_location": (1, 1),
        "max_step_count": 20,
    },
    "hyper_perameters": {
        "max_number_of_genrations": 2,
        "max_generation_size": 2,
        "fitness_threshold": 2.0,
        "new_generation_threshold": 2.0,
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


def generate_test_input_config_as_json(test_instance_id: str) -> json:
    """
    Generate a input config in json format for testing
    """

    test_input_config = base_input_config_rework
    test_input_config["instance_id"] = test_instance_id

    return json.dumps(test_input_config)


def generate_test_input_config_as_dict(test_instance_id: str) -> json:
    """
    Generate a input config in dict format for testing
    """

    test_input_config = base_input_config_rework
    test_input_config["instance_id"] = test_instance_id

    return test_input_config
