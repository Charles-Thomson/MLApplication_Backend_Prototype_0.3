"""Testing of BrainInstance model generation and DB elements"""

from application.lib.instance_generation.instance_generation_main import (
    format_ann_config,
)
from application.lib.agent_brain.brain_factory import BrainFactory

from database.model_data_formatting import (
    brain_instance_to_model,
    model_to_brain_instance,
)

from django.test import TestCase
from database.models import BrainInstanceModel


# Create your tests here.


test_ann_config: dict = {
    "weight_init_huristic": "he_weight",
    "hidden_activation_func": "linear_activation_function",
    "output_activation_func": "argmax_activation",
    "new_generation_func": "crossover_weights_average",
    "input_to_hidden_connections": "(24,9)",
    "hidden_to_output_connections": "(9,9)",
}


class BrainInstanceModelTestCase(TestCase):
    """Testing the saving and getting of a Brain instance to and from the DB"""

    def setUp(self) -> None:
        self.foramtted_test_config = format_ann_config(ann_config=test_ann_config)

    def test_brain_instance_model_creation(self) -> None:
        """Test teh creation of a brain instance model from a BrainInstance"""
        test_brain_type: str = "random_weighted_brain"

        test_brain = BrainFactory.make_brain(
            brain_type=test_brain_type,
            ann_config=self.foramtted_test_config,
        )

        brain_instance_as_model = brain_instance_to_model(
            brain_instance=test_brain, model_type="general"
        )
        self.assertIsInstance(brain_instance_as_model, BrainInstanceModel)
