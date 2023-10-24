# """Testing the Gneration and functions of a learning instance"""
# from typing import Generator
# import pytest

# from application.lib.instance_generation.instance_generation_main import (
#     new_instance,
# )
# from application.lib.agent.agent_factory import StaticStateMazeAgent

# from application.lib.agent_brain.static_state_brain import BrainInstance

# test_config = {
#     "env_type": "Static_State",
#     "agent_type": "Static_State",
#     "env_config": {
#         "env_map": "1,1,1,1,1,1,1,1,3,1,1,1,2,1,1,1,1,2,3,1,1,3,1,3,1",
#         "map_dimensions": "5",
#         "start_location": "1,1",
#     },
#     "instance_config": {
#         "max_number_of_genrations": "5",
#         "max_generation_size": "100",
#         "fitness_threshold": "2",
#         "new_generation_threshold": "4",
#     },
#     "brain_config": {
#         "weight_init_huristic": "he_weight",
#         "hidden_activation_func": "linear_activation_function",
#         "output_activation_func": "argmax_activation",
#         "new_generation_func": "crossover_weights_average",
#         "input_to_hidden_connections": "[24,9]",
#         "hidden_to_output_connections": "[9,9]",
#     },
# }

# # Global var used for the get funcs
# number_of_test_brains: int = 10


# @pytest.fixture(name="learning_instance")
# def setup_instance() -> object:
#     """Testing the setup of an instance"""
#     test_learning_instance: object = new_instance(test_config)
#     return test_learning_instance


# @pytest.fixture(name="agent_generator")
# def get_agent_generator(learning_instance) -> Generator:
#     """
#     Return a new agnet generator for testing
#     """
#     return learning_instance.get_new_agent_generator(
#         instance_id="test_instance", new_parents=[], current_generation_number=0
#     )


# @pytest.fixture(name="parent_data")
# def set_dummy_instance_parent_data(agent_generator) -> list[BrainInstance]:
#     """Set the dummy data for testing"""
#     test_brains: list[BrainInstance] = []

#     for x in range(number_of_test_brains):
#         new_agent: object = next(agent_generator)
#         new_brain: BrainInstance = new_agent.brain

#         new_brain.fitness += 1 * x
#         new_brain.traversed_path = [(1, 1)] * x
#         test_brains.append(new_brain)

#     return test_brains

# @pytest.mark.django_db
# def test_instance_attributes(learning_instance) -> None:
#     """
#     Test the attributes of a new instance
#     """
#     assert isinstance(learning_instance.instance_id, str)
#     assert isinstance(learning_instance.max_number_of_generations, int)
#     assert isinstance(learning_instance.new_generation_threshold, int)
#     assert isinstance(learning_instance.max_generation_size, int)
#     assert callable(learning_instance.agent_generater_partial) is True

#     agent_generator_in_instance: object = learning_instance.get_new_agent_generator(
#         instance_id="test-instance",
#         new_parents=[],
#         current_generation_number=0,
#     )
#     assert isinstance(next(agent_generator_in_instance), StaticStateMazeAgent)


# def test_run_generation(learning_instance, agent_generator) -> None:
#     """
#     Test the running of a full generation
#     """
#     new_parents: list[BrainInstance] = learning_instance.run_generation(
#         agent_generator=agent_generator,
#         fitness_threshold=learning_instance.current_fitness_threshold,
#     )

#     print(new_parents)
