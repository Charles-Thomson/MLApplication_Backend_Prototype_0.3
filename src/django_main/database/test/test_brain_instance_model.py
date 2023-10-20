"""Test relating to the BrainInstance model and object"""
from django.test import TestCase
import numpy as np

from database.internal_use_db_functions.brain_instance_functions import (
    save_brain_instance,
    get_brain_instance_by_id,
    get_brain_instance_by_forign_key,
    get_brain_model_by_id,
    get_brain_model_by_forign_key,
)


from database.models import (
    LearningInstanceModel,
    GenerationInstanceModel,
    BrainInstanceModel,
)

from database.internal_use_db_functions.learning_instance_functions import (
    save_learning_instance,
    get_learning_instance,
    get_learning_model,
)


from database.data_modeling.brain_instance_modeling import (
    brain_instance_to_model,
)

from database.internal_use_db_functions.generation_instance_functions import (
    save_generation_instance,
    get_generation_model_with_id,
)

from application.lib.storage_objects.generation_object import (
    GenerationObject,
)

from application.lib.agent_brain.brain_factory import BrainFactory
from application.lib.agent_brain.static_state_brain import BrainInstance
from application.lib.instance_generation.instance_generation_main import (
    format_brain_config,
)


class BrainInstanceModelTestCase(TestCase):
    """Testing the saving and getting of a Brain instance to and from the DB"""

    def setUp(self) -> None:
        self.instance_id = "test_learning_instance_ref"
        self.learning_instance_db_referance = save_learning_instance(self.instance_id)

        self.generation_instance_id = "test_generation_instance_ref"

        self.test_generation_object_config: GenerationObject = GenerationObject(
            generation_instance_id=self.generation_instance_id,
            generation_number=1,
            average_fitnees=1.0,
            fitness_threshold=2.0,
            generation_alpha_brain="holder",
            parents_of_generation=[],
            generaiton_size=2,
            learning_instance_ref=self.learning_instance_db_referance,
        )

        self.generation_instance_db_referance = save_generation_instance(
            this_generation_object=self.test_generation_object_config,
            learning_instance_referance=self.learning_instance_db_referance,
        )

        test_brain_config: dict = {
            "weight_init_huristic": "he_weight",
            "hidden_activation_func": "linear_activation_function",
            "output_activation_func": "argmax_activation",
            "new_generation_func": "crossover_weights_average",
            "input_to_hidden_connections": "[24,9]",
            "hidden_to_output_connections": "[9,9]",
        }

        self.foramtted_test_config: dict = format_brain_config(
            brain_config=test_brain_config
        )
        self.test_brain_type: str = "random_weighted_brain"

        self.test_brain = BrainFactory.make_brain(
            brain_id="test_brain",
            brain_type=self.test_brain_type,
            brain_config=self.foramtted_test_config,
        )

    def test_brain_instance_model_creation(self) -> None:
        """Test teh creation of a brain instance model from a BrainInstance"""

        brain_instance_as_model = brain_instance_to_model(
            brain_instance=self.test_brain,
            generation_instance_ref=self.generation_instance_db_referance,
        )
        self.assertIsInstance(brain_instance_as_model, BrainInstanceModel)

    def test_saving_and_getting_of_brain_instance(self) -> None:
        """
        Test the conversion of an instance to a model, saving,
        getting and converting back to an instance

        """

        save_brain_instance(
            brain_instance=self.test_brain,
            generation_instance_ref=self.generation_instance_db_referance,
        )

        brain_instance: BrainInstance = get_brain_instance_by_id(brain_id="test_brain")

        self.assertIsInstance(brain_instance, BrainInstance)
        assert callable(brain_instance.hidden_layer_activation_func)
        assert callable(brain_instance.output_layer_activation_func)
        self.assertIsInstance(brain_instance.hidden_weights, np.ndarray)
        self.assertIsInstance(brain_instance.output_weights, np.ndarray)

    def test_saving_two_brains_and_getting_by_forign_key(self) -> None:
        """
        Save two brain instances and recover bot from the database useing the fk attribute
        """

        test_brain_instance_1 = BrainFactory.make_brain(
            brain_id="test_brain_instance_1",
            brain_type=self.test_brain_type,
            brain_config=self.foramtted_test_config,
        )

        test_brain_instance_2 = BrainFactory.make_brain(
            brain_id="test_brain_instance_2",
            brain_type=self.test_brain_type,
            brain_config=self.foramtted_test_config,
        )

        save_brain_instance(
            brain_instance=test_brain_instance_1,
            generation_instance_ref=self.generation_instance_db_referance,
        )

        save_brain_instance(
            brain_instance=test_brain_instance_2,
            generation_instance_ref=self.generation_instance_db_referance,
        )

        generation_model = get_generation_model_with_id(
            generation_instance_id=self.generation_instance_id
        )

        brain_instances = generation_model.fk_ref.all()

        for x in brain_instances:
            print(x)
