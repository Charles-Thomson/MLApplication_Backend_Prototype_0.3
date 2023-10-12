"""Testing the configuation of an enviroment once it hs been created"""

import numpy as np


from application.lib.environment.environment_factory import (
    StaticStateEnvironemnt,
)

from application.lib.environment.environment_factory import (
    EnvironmentFactory,
)

from application.lib.instance_generation.instance_generation_main import (
    format_env_config,
)


test_config = {
    "env_map": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
    "map_dimensions": "4",
    "start_location": "1,1",
    "max_number_of_genrations": "2",
    "max_generation_size": "2",
    "fitness_threshold": "2",
    "new_generation_threshold": "2",
}

test_env_type: str = "Static_State"


def test_environemnt_configuration() -> None:
    """Test the configuration of an environment post generation"""

    env_config: dict = format_env_config(test_config)
    static_state_test_env: StaticStateEnvironemnt = EnvironmentFactory.make_env(
        test_env_type, config=env_config
    )

    assert static_state_test_env.start_coords == (1, 1)
    assert static_state_test_env.current_coords == (1, 1)
    assert static_state_test_env.current_step == 0
    assert static_state_test_env.path == []

    assert isinstance(static_state_test_env.environment_map, np.ndarray)
    assert static_state_test_env.environment_map.shape == (
        env_config["map_dimensions"],
        env_config["map_dimensions"],
    )
