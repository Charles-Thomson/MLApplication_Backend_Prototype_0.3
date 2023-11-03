"""Testing the environment"""
import pytest
import json
import numpy as np
from application.lib.agent_brain.brain_factory import BrainFactory
from application.lib.agent_brain.static_state_brain import BrainInstance


from application.lib.config_generation.generate_config_data import (
    generate_instance_configuration_data,
)

from application.lib.environment.environment_factory import (
    StaticStateEnvironemnt,
)

from application.lib.environment.environment_factory import (
    EnvironmentFactory,
)

test_input_config: dict = {
    "env_type": "Static_State",
    "agent_type": "",
    "instance_id": "test_instance",
    "map_config": {
        "env_map": "1,1,1,1,1,1,3,2,1,1,1,1,1,1,1,1",
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


@pytest.fixture(name="test_instance_config")
def setup_instance_config() -> dict:
    """
    Set up an instance config file for testing
    """
    input_config_json: json = json.dumps(test_input_config)
    test_insance_config_data: dict = generate_instance_configuration_data(
        input_config=input_config_json
    )

    return test_insance_config_data


@pytest.fixture(name="test_env")
def setup_test_environment(test_instance_config: dict) -> StaticStateEnvironemnt:
    """
    Set up an environment instance for testing
    """

    test_env: StaticStateEnvironemnt = EnvironmentFactory.make_env(
        env_type=test_instance_config["env_type"],
        map_data=test_instance_config["map_data"],
    )

    return test_env


def test_environment_multiple_steps(test_env: StaticStateEnvironemnt) -> None:
    """
    Test multiple steps in an environment
    """

    test_environment: StaticStateEnvironemnt = test_env

    assert test_environment.start_coords == [1, 1]
    assert test_environment.current_coords == [1, 1]
    assert test_environment.current_step == 0

    test_action = 5  # move left
    new_coords_a, termination_a, reward_a = test_environment.step(test_action)

    assert new_coords_a == (1, 2)
    assert termination_a is False
    assert reward_a == 0.15

    new_coords_b, termination_b, reward_b = test_environment.step(test_action)

    assert new_coords_b == (1, 3)
    assert termination_b is True
    assert reward_b == 3.0


def test_environment_observation(test_env: StaticStateEnvironemnt) -> None:
    """Test the collection of observation data from the environement"""

    observation_data = test_env.get_environment_observation()

    assert len(observation_data) == 24
    assert (x == type(float) for x in observation_data)


@pytest.mark.parametrize(
    "action,location,new_location,termination_state",
    [
        (0, (1, 1), (0, 0), False),
        (1, (1, 1), (0, 1), False),
        (2, (1, 1), (0, 2), False),
        (3, (1, 1), (1, 0), False),
        (4, (1, 1), (1, 1), False),
        (5, (1, 1), (1, 2), False),
        (6, (1, 1), (2, 0), False),
        (7, (1, 1), (2, 1), False),
        (8, (1, 1), (2, 2), False),
    ],
)
def test_step_by_direction(
    test_env: StaticStateEnvironemnt,
    action: int,
    location: tuple,
    new_location: tuple,
    termination_state: bool,
) -> None:
    """Test a single step in the enviornment"""
    test_env.current_coords = location

    new_coords, termination, reward = test_env.step(action)

    assert new_coords == new_location
    assert termination == termination_state


bounds = 4  # map_shape


@pytest.mark.parametrize(
    "location,action,termination",
    [
        ((0, 0), 0, True),
        ((0, 0), 1, True),
        ((0, 0), 2, True),
        ((0, 0), 3, True),
        ((0, 0), 6, True),
        ((0, bounds), 0, True),
        ((0, bounds), 1, True),
        ((0, bounds), 2, True),
        ((0, bounds), 5, True),
        ((0, bounds), 8, True),
        ((bounds, 0), 0, True),
        ((bounds, 0), 3, True),
        ((bounds, 0), 6, True),
        ((bounds, 0), 7, True),
        ((bounds, 0), 8, True),
        ((bounds, bounds), 2, True),
        ((bounds, bounds), 5, True),
        ((bounds, bounds), 6, True),
        ((bounds, bounds), 7, True),
        ((bounds, bounds), 8, True),
    ],
)
def test_boundry_termination(
    test_env: StaticStateEnvironemnt, location: tuple, action: int, termination: bool
):
    """
    Testing the termination on the boundries of the environment_map

    """
    test_env.current_coords = location
    _, this_termination, _ = test_env.step(action)

    assert this_termination == termination
