"""Test relating to the BrainInstance model and object"""
import json
from django.test import TestCase
import numpy as np

from application.lib.config_generation.generate_config_data import (
    generate_instance_configuration_data,
)
from application.lib.config_generation.config_file_structure import (
    generate_test_input_config_as_json,
)

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
    new_learning_instance_model,
    get_learning_data_by_id,
    get_learning_model_by_id,
    update_learning_instance_model_by_id,
)


from database.data_modeling.brain_instance_modeling import (
    brain_instance_to_model,
)

from database.internal_use_db_functions.generation_instance_functions import (
    new_generation_instance_model,
    update_generation_model_by_id,
    get_generation_data_with_id,
    get_generation_model_with_forign_key,
    get_generation_model_with_id,
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
        self.learning_instance_db_referance = new_learning_instance_model(
            self.instance_id
        )

        current_generation_number: int = 1
        self.generation_instance_id = f"{self.instance_id}-{current_generation_number}"

        self.test_generation_model_db_ref: json = new_generation_instance_model(
            generation_instance_id=self.generation_instance_id,
            generation_number=current_generation_number,
            learning_instance_referance=self.learning_instance_db_referance,
            parents_of_generation=[],
        )

        update_test_data: dict = {
            "average_fitness": 3.5,
            "fitness_threshold": 4.0,
            "generation_alpha_brain": "Brain_2",
            "generation_size": 2,
            "parents_of_generation": ["Brain_1", "brain_2"],
        }

        update_generation_model_by_id(
            generation_instance_id=self.generation_instance_id,
            update_data=update_test_data,
        )

    def generate_brain_helper(self, instance_id: str, brain_id: int) -> BrainInstance:
        """Helper function for generating brain instances"""

        input_config_json: json = generate_test_input_config_as_json(
            test_instance_id=instance_id
        )
        test_insance_config_data: dict = generate_instance_configuration_data(
            input_config=input_config_json
        )

        brain_data: dict = test_insance_config_data["brain_config"]
        brain_data["brain_id"] = brain_id
        brain_data["brain_type"] = "random_weighted_brain"

        test_brain_instance: BrainInstance = BrainFactory.make_brain(
            brain_config=brain_data,
        )

        return test_brain_instance

    def test_brain_model_creation_and_retrival(self) -> None:
        """
        Test the creation, updating and retrival of a BrainInstanceModel
        """

        test_brain_instance_id = f"{self.instance_id}-{self.generation_instance_id}-0"

        test_brain_instance_1 = self.generate_brain_helper(
            instance_id=self.instance_id, brain_id=test_brain_instance_id
        )

        save_brain_instance(
            brain_instance=test_brain_instance_1,
            generation_instance_db_ref=self.test_generation_model_db_ref,
        )

        returned_brain_instance: BrainInstance = get_brain_instance_by_id(
            brain_id=test_brain_instance_id
        )

        self.assertIsInstance(returned_brain_instance, BrainInstance)

        self.assertIsInstance(returned_brain_instance, BrainInstance)
        assert callable(returned_brain_instance.hidden_layer_activation_func)
        assert callable(returned_brain_instance.output_layer_activation_func)
        self.assertIsInstance(returned_brain_instance.hidden_weights, np.ndarray)
        self.assertIsInstance(returned_brain_instance.output_weights, np.ndarray)

    def test_saving_two_brains_and_getting_by_forign_key(self) -> None:
        """
        Save two brain instances and recover bot from the database useing the fk attribute
        """

        test_brain_instance_1_id: str = (
            f"{self.instance_id}-{self.generation_instance_id}-1"
        )
        test_brain_1: BrainInstance = self.generate_brain_helper(
            instance_id=self.instance_id, brain_id=test_brain_instance_1_id
        )

        test_brain_instance_2_id: str = (
            f"{self.instance_id}-{self.generation_instance_id}-2"
        )
        test_brain_2: BrainInstance = self.generate_brain_helper(
            instance_id=self.instance_id, brain_id=test_brain_instance_2_id
        )

        save_brain_instance(
            brain_instance=test_brain_1,
            generation_instance_db_ref=self.test_generation_model_db_ref,
        )

        save_brain_instance(
            brain_instance=test_brain_2,
            generation_instance_db_ref=self.test_generation_model_db_ref,
        )

        generation_model = get_generation_model_with_id(
            generation_instance_id=self.generation_instance_id
        )

        brain_instances = generation_model.fk_ref.all()

        for x in brain_instances:
            self.assertIsInstance(x, BrainInstanceModel)
