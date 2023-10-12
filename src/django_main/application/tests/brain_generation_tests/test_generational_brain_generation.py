import numpy as np
from application.lib.instance_generation.instance_generation_main import (
    format_ann_config,
)

from application.lib.agent_brain.brain_factory import BrainFactory
from application.lib.agent_brain.static_state_brain import BrainInstance

# Test holder


test_random_ann_config: dict = {
    "weight_init_huristic": "he_weight",
    "hidden_activation_func": "linear_activation_function",
    "output_activation_func": "argmax_activation",
    "new_generation_func": "crossover_weights_average",
    "input_to_hidden_connections": "(24,9)",
    "hidden_to_output_connections": "(9,9)",
}

base_brain_config: dict = format_ann_config(ann_config=test_random_ann_config)


def test_generational_brain_generation() -> None:
    """Testing the generational of a generationally weighted brain"""

    test_random_brain_type: str = "random_weighted_brain"
    test_generational_brain_type: str = "generational_weighted_brain"
    parents: list = []

    random_test_brains: list[BrainInstance] = [
        BrainFactory.make_brain(
            brain_type=test_random_brain_type,
            ann_config=base_brain_config,
        )
        for _ in range(10)
    ]

    assert len(random_test_brains) == 10
    for instance in random_test_brains:
        assert isinstance(instance, BrainInstance)

    test_generational_brain: BrainInstance = BrainFactory.make_brain(
        brain_type=test_generational_brain_type,
        ann_config=base_brain_config,
        parents=random_test_brains,
    )

    assert isinstance(test_generational_brain, BrainInstance)
    assert isinstance(test_generational_brain.hidden_weights, np.ndarray)
    assert isinstance(test_generational_brain.output_weights, np.ndarray)
    assert test_generational_brain.hidden_weights.shape == (24, 9)
    assert test_generational_brain.output_weights.shape == (9, 9)

    assert callable(test_generational_brain.hidden_layer_activation_func) is True
    assert callable(test_generational_brain.output_layer_activation_func) is True
