Running tests should be done from within the Django_main package
 ***** SETUP *****

have to set the DJANGO_SETTINGS_MODULE at the django_main level
cmd -> 
 -> make sure no space at the end !!
set DJANGO_SETTINGS_MODULE=django_main.settings 

***** Logging and testing *****

If multiple tests are run, the logging files may overlap

***** CONFIG *****

The config file passed into the main system is the following format 

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
        "brain_config": {
            "weight_init_huristic": "he_weight",
            "hidden_activation_func": "linear_activation_function",
            "output_activation_func": "argmax_activation",
            "new_generation_func": "crossover_weights_average",
            "input_to_hidden_connections": "[24,9]",
            "hidden_to_output_connections": "[9,9]",
        },
    }
