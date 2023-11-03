# """Testing elements of the static state environement"""
# import pytest

# from application.lib.environment.environment_factory import (
#     EnvironmentFactory,
# )

# from application.lib.instance_generation.instance_generation_main import (
#     format_env_config,
# )

# from application.lib.environment.environment_factory import (
#     StaticStateEnvironemnt,
# )

# test_env_type: str = "Static_State"

# test_config = {
#     "env_map": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
#     "map_dimensions": "4",
#     "start_location": "1,1",
#     "max_number_of_genrations": "2",
#     "max_generation_size": "2",
#     "fitness_threshold": "2",
#     "new_generation_threshold": "2",
# }


# env_config: dict = format_env_config(test_config)
# pytest.static_state_test_env: StaticStateEnvironemnt = EnvironmentFactory.make_env(
#     env_type=test_env_type, config=env_config
# )


# def test_get_env_type() -> None:
#     """Test the reurned env type"""

#     assert pytest.static_state_test_env.get_env_type() == test_env_type


# def test_environment_observation() -> None:
#     """Test the collection of observation data from the environement"""

#     observation_data = pytest.static_state_test_env.get_environment_observation()

#     assert len(observation_data) == 24
#     assert (x == type(float) for x in observation_data)


# @pytest.mark.parametrize(
#     "action,location,new_location,termination_state",
#     [
#         (0, (1, 1), (0, 0), False),
#         (1, (1, 1), (0, 1), False),
#         (2, (1, 1), (0, 2), False),
#         (3, (1, 1), (1, 0), False),
#         (4, (1, 1), (1, 1), False),
#         (5, (1, 1), (1, 2), False),
#         (6, (1, 1), (2, 0), False),
#         (7, (1, 1), (2, 1), False),
#         (8, (1, 1), (2, 2), False),
#     ],
# )
# def test_step_by_direction(action, location, new_location, termination_state) -> None:
#     """Test a single step in the enviornment"""
#     test_env: StaticStateEnvironemnt = EnvironmentFactory.make_env(
#         env_type=test_env_type, config=env_config
#     )

#     new_coords, termination, reward = test_env.step(action)

#     assert new_coords == new_location
#     assert termination == termination_state


# bounds = env_config["map_dimensions"]
# total_states: int = env_config["map_dimensions"] * env_config["map_dimensions"] - 1


# # Param termination testing data
# @pytest.mark.parametrize(
#     "location,action,termination",
#     [
#         ((0, 0), 0, True),
#         ((0, 0), 1, True),
#         ((0, 0), 2, True),
#         ((0, 0), 3, True),
#         ((0, 0), 6, True),
#         ((0, bounds), 0, True),
#         ((0, bounds), 1, True),
#         ((0, bounds), 2, True),
#         ((0, bounds), 5, True),
#         ((0, bounds), 8, True),
#         ((bounds, 0), 0, True),
#         ((bounds, 0), 3, True),
#         ((bounds, 0), 6, True),
#         ((bounds, 0), 7, True),
#         ((bounds, 0), 8, True),
#         ((bounds, bounds), 2, True),
#         ((bounds, bounds), 5, True),
#         ((bounds, bounds), 6, True),
#         ((bounds, bounds), 7, True),
#         ((bounds, bounds), 8, True),
#     ],
# )
# def test_boundry_termination(location, action, termination):
#     """holder"""
#     pytest.static_state_test_env.current_coords = location
#     new_state, this_termination, reward = pytest.static_state_test_env.step(action)

#     assert this_termination == termination
