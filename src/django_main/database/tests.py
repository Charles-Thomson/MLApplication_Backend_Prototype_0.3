"""Testing of BrainInstance model generation and DB elements"""

import numpy as np
from application.lib.instance_generation.instance_generation_main import (
    format_ann_config,
)
from application.lib.agent_brain.brain_factory import BrainFactory

from database.model_data_formatting import (
    brain_instance_to_model,
    model_to_brain_instance,
)

from application.lib.agent_brain.static_state_brain import BrainInstance

from django.test import TestCase
from database.models import BrainInstanceModel


# Create your tests here.


test_ann_config: dict = {
    "weight_init_huristic": "he_weight",
    "hidden_activation_func": "linear_activation_function",
    "output_activation_func": "argmax_activation",
    "new_generation_func": "crossover_weights_average",
    "input_to_hidden_connections": "[24,9]",
    "hidden_to_output_connections": "[9,9]",
}


class BrainInstanceModelTestCase(TestCase):
    """Testing the saving and getting of a Brain instance to and from the DB"""

    def setUp(self) -> None:
        foramtted_test_config: dict = format_ann_config(ann_config=test_ann_config)
        test_brain_type: str = "random_weighted_brain"

        self.test_brain = BrainFactory.make_brain(
            brain_type=test_brain_type,
            ann_config=foramtted_test_config,
        )

    def test_brain_instance_model_creation(self) -> None:
        """Test teh creation of a brain instance model from a BrainInstance"""

        brain_instance_as_model = brain_instance_to_model(
            brain_instance=self.test_brain, model_type="general"
        )
        self.assertIsInstance(brain_instance_as_model, BrainInstanceModel)

    def test_brain_instance_model_to_brain_instance(self) -> None:
        """
        The conversion of a model insance to a Brain Instance
        """

        brain_instance_as_model = brain_instance_to_model(
            brain_instance=self.test_brain, model_type="general"
        )

        brain_model_as_instance = model_to_brain_instance(
            brain_model=brain_instance_as_model
        )

        self.assertIsInstance(brain_model_as_instance, BrainInstance)
        assert callable(brain_model_as_instance.hidden_layer_activation_func)
        assert callable(brain_model_as_instance.output_layer_activation_func)
        self.assertIsInstance(brain_model_as_instance.hidden_weights, np.ndarray)
        self.assertIsInstance(brain_model_as_instance.output_weights, np.ndarray)
