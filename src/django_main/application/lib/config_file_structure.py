test_config = {
    "env_type": "",
    "agent_type": "",
    "env_config": {
        "env_map": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
        "map_dimensions": "4",
        "start_location": "1,1",
        "max_number_of_genrations": "2",
        "max_generation_size": "2",
        "fitness_threshold": "2",
        "new_generation_threshold": "2",
    },
    "instance_config": {
        "max_number_of_genrations": "2",
        "max_generation_size": "2",
        "fitness_threshold": "2",
        "new_generation_threshold": "2",
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
