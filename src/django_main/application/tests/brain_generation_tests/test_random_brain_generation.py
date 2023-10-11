"""Testing the gernation of a randomly weighted brain"""
import pytest
import numpy as np
from src.django_main.application.lib.instance_generation.instance_generation_main import (
    format_ann_config,
)

from src.django_main.application.lib.agent_brain.brain_factory import BrainFactory
from src.django_main.application.lib.agent_brain.static_state_brain import BrainInstance

test_ann_config: dict = {
    "weight_init_huristic": "he_weight",
    "hidden_activation_func": "linear_activation_function",
    "output_activation_func": "argmax_activation",
    "new_generation_func": "crossover_weights_average",
    "input_to_hidden_connections": "(24,9)",
    "hidden_to_output_connections": "(9,9)",
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
                "input_to_hidden_connections": "(24,9)",
                "hidden_to_output_connections": "(9,9)",
            }
        ),
        (
            {
                "weight_init_huristic": "xavier_weight",
                "hidden_activation_func": "sigmoid_activation_fucntion",
                "output_activation_func": "soft_argmax_activation",
                "new_generation_func": "crossover_weights_average",
                "input_to_hidden_connections": "(24,9)",
                "hidden_to_output_connections": "(9,9)",
            }
        ),
    ],
)
def test_formatting_ann_config(test_config) -> None:
    """Testing the formatting of the ann config file"""

    foramtted_test_config = format_ann_config(ann_config=test_config)

    assert isinstance(foramtted_test_config, dict)
    assert callable(foramtted_test_config["weight_init_huristic"]) is True
    assert callable(foramtted_test_config["hidden_activation_func"]) is True
    assert callable(foramtted_test_config["output_activation_func"]) is True
    assert callable(foramtted_test_config["new_generation_func"]) is True
    assert foramtted_test_config["input_to_hidden_connections"] == (24, 9)
    assert foramtted_test_config["hidden_to_output_connections"] == (9, 9)


def test_random_brain_generation() -> None:
    """Test the genartaion of a random weighted brain"""

    foramtted_test_config = format_ann_config(ann_config=test_ann_config)
    test_brain_type: str = "random_weighted_brain"
    parents: list = []

    test_brain = BrainFactory.make_brain(
        current_generation_number=0,
        brain_type=test_brain_type,
        ann_config=foramtted_test_config,
        parents=parents,
    )

    assert isinstance(test_brain, BrainInstance)
    assert isinstance(test_brain.hidden_weights, np.ndarray)
    assert isinstance(test_brain.output_weights, np.ndarray)
    assert test_brain.hidden_weights.shape == (24, 9)
    assert test_brain.output_weights.shape == (9, 9)

    assert callable(test_brain.hidden_layer_activation_func) is True
    assert callable(test_brain.output_layer_activation_func) is True
