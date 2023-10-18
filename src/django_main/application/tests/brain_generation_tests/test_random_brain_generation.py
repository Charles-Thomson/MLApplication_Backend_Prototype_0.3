"""Testing the gernation of a randomly weighted brain"""
import pytest
import numpy as np
from application.lib.instance_generation.instance_generation_main import (
    format_brain_config,
)

from application.lib.agent_brain.brain_factory import BrainFactory
from application.lib.agent_brain.static_state_brain import BrainInstance


test_brain_config: dict = {
    "weight_init_huristic": "he_weight",
    "hidden_activation_func": "linear_activation_function",
    "output_activation_func": "argmax_activation",
    "new_generation_func": "crossover_weights_average",
    "input_to_hidden_connections": "[24,9]",
    "hidden_to_output_connections": "[9,9]",
}


@pytest.mark.parametrize(
    "test_config",
    [
        (
            {
                "weight_init_huristic": "he_weight",
                "hidden_activation_func": "linear_activation_function",
                "output_activation_func": "argmax_activation",
                "new_generation_func": "crossover_weights_average",
                "input_to_hidden_connections": "[24,9]",
                "hidden_to_output_connections": "[9,9]",
            }
        ),
        (
            {
                "weight_init_huristic": "xavier_weight",
                "hidden_activation_func": "sigmoid_activation_fucntion",
                "output_activation_func": "soft_argmax_activation",
                "new_generation_func": "crossover_weights_average",
                "input_to_hidden_connections": "[24,9]",
                "hidden_to_output_connections": "[9,9]",
            }
        ),
    ],
)
def test_formatting_brain_config(test_config) -> None:
    """Testing the formatting of the brain config file"""

    foramtted_test_config = format_brain_config(brain_config=test_config)

    assert isinstance(foramtted_test_config, dict)

    assert foramtted_test_config["input_to_hidden_connections"] == [24, 9]
    assert foramtted_test_config["hidden_to_output_connections"] == [9, 9]


def test_random_brain_generation() -> None:
    """Test the genartaion of a random weighted brain"""

    foramtted_test_config = format_brain_config(brain_config=test_brain_config)

    test_brain_type: str = "random_weighted_brain"
    parents: list = []

    test_brain = BrainFactory.make_brain(
        brain_id="test_brain",
        brain_type=test_brain_type,
        brain_config=foramtted_test_config,
    )

    assert isinstance(test_brain, BrainInstance)
    assert isinstance(test_brain.hidden_weights, np.ndarray)
    assert isinstance(test_brain.output_weights, np.ndarray)
    assert test_brain.hidden_weights.shape == (24, 9)
    assert test_brain.output_weights.shape == (9, 9)

    assert callable(test_brain.hidden_layer_activation_func) is True
    assert callable(test_brain.output_layer_activation_func) is True
