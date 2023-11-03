# """Testing the configuation of an enviroment once it hs been created"""

# from application.lib.environment.environment_factory import (
#     StaticStateEnvironemnt,
# )

# from application.lib.environment.environment_factory import (
#     EnvironmentFactory,
# )

# from application.lib.instance_generation.instance_generation_main import (
#     format_env_config,
# )

# # 1,1,1,1
# # 1,1,3,1
# # 1,1,1,1
# # 1,1,1,1


# test_config = {
#     "env_map": "1,1,1,1,1,1,3,2,1,1,1,1,1,1,1,1",
#     "map_dimensions": "4",
#     "start_location": "1,1",
#     "max_number_of_genrations": "2",
#     "max_generation_size": "2",
#     "fitness_threshold": "2",
#     "new_generation_threshold": "2",
# }

# test_env_type: str = "Static_State"


# def test_environment_step_by_step():
#     """
#     Testing a small pth in the enviroment.
#     This covers a goal and termination node.
#     """

#     env_config: dict = format_env_config(test_config)
#     static_state_test_env: StaticStateEnvironemnt = EnvironmentFactory.make_env(
#         test_env_type, config=env_config
#     )

#     assert static_state_test_env.start_coords == (1, 1)
#     assert static_state_test_env.current_coords == (1, 1)
#     assert static_state_test_env.current_step == 0

#     test_action = 5  # move left
#     new_coords_a, termination_a, reward_a = static_state_test_env.step(test_action)

#     assert new_coords_a == (1, 2)
#     assert termination_a == False
#     assert reward_a == 0.15

#     new_coords_b, termination_b, reward_b = static_state_test_env.step(test_action)

#     assert new_coords_b == (1, 3)
#     assert termination_b == True
#     assert reward_b == 3.0
