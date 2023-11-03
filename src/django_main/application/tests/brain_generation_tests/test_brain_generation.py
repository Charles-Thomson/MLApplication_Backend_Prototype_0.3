"""Testing the generation of different types of brain"""
import pytest
import json
import numpy as np
from application.lib.agent_brain.brain_factory import BrainFactory
from application.lib.agent_brain.static_state_brain import BrainInstance

from application.lib.config_generation.config_file_structure import (
    generate_test_input_config_as_json,
)

from application.lib.config_generation.generate_config_data import (
    generate_instance_configuration_data,
)


@pytest.fixture(name="test_instance_config")
def setup_instance_config() -> dict:
    """
    Set up an instance config file for testing
    """
    test_config_instance_id: str = "test_instance"

    input_config_json: json = generate_test_input_config_as_json(
        test_instance_id=test_config_instance_id
    )
    test_insance_config_data: dict = generate_instance_configuration_data(
        input_config=input_config_json
    )

    return test_insance_config_data


@pytest.fixture(name="dummy_test_parets")
def setup_ten_dummy_test_parents(test_instance_config: dict) -> list[BrainInstance]:
    """
    Generate a list of dummy test parents
    """
    brain_data = test_instance_config["brain_config"]
    brain_data["brain_id"] = "brain_test_id_parent"
    brain_data["brain_type"] = "random_weighted_brain"
    dummy_parents: list[BrainInstance] = [
        BrainFactory.make_brain(
            brain_config=brain_data,
        )
        for _ in range(10)
    ]

    return dummy_parents


def test_generate_generational_weighted_brain_instance(
    test_instance_config: dict, dummy_test_parets: list[BrainInstance]
) -> None:
    """
    Test generating a generational brain from a set of test parents
    """

    brain_data = test_instance_config["brain_config"]
    brain_data["brain_id"] = "brain_test_id"
    brain_data["brain_type"] = "generational_weighted_brain"

    test_generational_brain: BrainInstance = BrainFactory.make_brain(
        brain_config=brain_data,
        parents=dummy_test_parets,
    )

    assert isinstance(test_generational_brain, BrainInstance)
    assert isinstance(test_generational_brain.hidden_weights, np.ndarray)
    assert isinstance(test_generational_brain.output_weights, np.ndarray)
    assert test_generational_brain.hidden_weights.shape == (24, 9)
    assert test_generational_brain.output_weights.shape == (9, 9)

    assert callable(test_generational_brain.hidden_layer_activation_func) is True
    assert callable(test_generational_brain.output_layer_activation_func) is True


def test_generate_random_weighted_brain_instance(test_instance_config: dict) -> None:
    """
    Test the gernatrion of a brain instance with random weights
    """

    brain_data = test_instance_config["brain_config"]
    brain_data["brain_id"] = "brain_test_id"
    brain_data["brain_type"] = "random_weighted_brain"

    test_random_weighted_brain: BrainInstance = BrainFactory.make_brain(
        brain_config=brain_data,
    )

    assert isinstance(test_random_weighted_brain, BrainInstance)
    assert isinstance(test_random_weighted_brain.hidden_weights, np.ndarray)
    assert isinstance(test_random_weighted_brain.output_weights, np.ndarray)
    assert test_random_weighted_brain.hidden_weights.shape == (24, 9)
    assert test_random_weighted_brain.output_weights.shape == (9, 9)

    assert callable(test_random_weighted_brain.hidden_layer_activation_func) is True
    assert callable(test_random_weighted_brain.output_layer_activation_func) is True
