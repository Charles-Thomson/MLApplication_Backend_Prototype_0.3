# """Testing the generation of the environments via the environemnt_factory"""

# import pytest

# from application.lib.environment.environment_factory import (
#     EnvironmentFactory,
# )
# from application.lib.environment.environment_factory import (
#     StaticStateEnvironemnt,
# )

# from application.lib.instance_generation.instance_generation_main import (
#     format_env_config,
# )

# env_config = {
#     "env_map": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
#     "map_dimensions": "4",
#     "start_location": "1,1",
#     "max_number_of_genrations": "2",
#     "max_generation_size": "2",
#     "fitness_threshold": "2",
#     "new_generation_threshold": "2",
# }

# formatted_test_config: dict = format_env_config(env_config)


# @pytest.mark.parametrize(
#     "environment_type, test_env_config,expected_type",
#     [("Static_State", formatted_test_config, StaticStateEnvironemnt)],
# )
# def test_environemnt_factory(environment_type, test_env_config, expected_type) -> None:
#     """Test the generation of ebvironmets from the factory"""

#     test_environment: StaticStateEnvironemnt = EnvironmentFactory.make_env(
#         env_type=environment_type, config=test_env_config
#     )

#     assert isinstance(test_environment, expected_type)
