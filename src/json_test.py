import json
import numpy as np
from math import sqrt

test_string = '{"names": {"first": "jess", "second": "pls work"}}'

as_dict = json.dumps(test_string)

print(as_dict)
print(type(as_dict))

# inputJsonTest(jsonInput:"{\"env_type\":\"Static_State\",\"agent_type\": \"\",\"instance_id\": \"this_instance_id\", \"map_config\": {\"env_map\": \"1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1\",\"map_dimensions\": 4,\"start_location\": (1, 1),\"max_step_count\": 20,},\"hyper_perameters\": {\"max_number_of_genrations\": 2,\"max_generation_size\": 2,\"fitness_threshold\": 2.0,\"new_generation_threshold\": 2.0,\"generation_failure_threshold\": 10,},\"brain_config\": {\"weight_init_huristic\": \"he_weight\",\"hidden_activation_func\": \"linear_activation_function\",\"output_activation_func\": \"argmax_activation\",\"new_generation_func\": \"crossover_weights_average\",\"input_to_hidden_connections\": (24, 9),\"hidden_to_output_connections\":(9, 9),},}")
