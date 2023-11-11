"""Test related to the Generation instance model and object"""
import json
from django.test import TestCase

from database.internal_use_db_functions.learning_instance_functions import (
    new_learning_instance_model,
    get_learning_model_by_id,
)

from database.models import GenerationInstanceModel


from database.internal_use_db_functions.generation_instance_functions import (
    new_generation_instance_model,
    update_generation_model_by_id,
    get_generation_data_with_id,
    get_generation_model_with_forign_key,
    get_generation_model_with_id,
)


class GenerationInstanceModelTests(TestCase):
    """Testing the saving of generation objects with the FK of a learning instance"""

    def setUp(self) -> None:
        self.instance_id = "test_instance_id"
        self.learning_instance_db_referance = new_learning_instance_model(
            self.instance_id
        )

    def test_create_update_retrive_generation_model(self) -> GenerationInstanceModel:
        """
        test the creation of a generation instance model
        """
        current_generation_number_1 = 1
        generation_instance_id_1 = f"{self.instance_id}-{current_generation_number_1}"

        test_generation_model_ref: json = new_generation_instance_model(
            generation_instance_id=generation_instance_id_1,
            generation_number=current_generation_number_1,
            learning_instance_referance=self.learning_instance_db_referance,
            parents_of_generation=[],
        )

        update_generation_model_by_id(
            generation_instance_id=generation_instance_id_1,
            average_fitness=3.5,
            fitness_threshold=4.0,
            generation_alpha_brain="Brain_2",
            generation_size=2,
        )

        returned_generation_data: dict = get_generation_data_with_id(
            generation_instance_id=generation_instance_id_1
        )

    def test_multiple_generation_model_retrival_with_fk(self) -> None:
        """Test saving and returning two gneration_instance using the FK - aka learning instance ref"""

        generation_instance_id_1 = f"{self.instance_id}-{1}"

        generation_instance_id_2 = f"{self.instance_id}-{2}"

        test_generation_model_ref_1: json = new_generation_instance_model(
            generation_instance_id=generation_instance_id_1,
            generation_number=1,
            learning_instance_referance=self.learning_instance_db_referance,
            parents_of_generation=[],
        )

        test_generation_model_ref_2: json = new_generation_instance_model(
            generation_instance_id=generation_instance_id_2,
            generation_number=2,
            learning_instance_referance=self.learning_instance_db_referance,
            parents_of_generation=[],
        )

        update_generation_model_by_id(
            generation_instance_id=generation_instance_id_1,
            average_fitness=3.5,
            fitness_threshold=4.0,
            generation_alpha_brain="Brain_2",
            generation_size=2,
        )

        update_generation_model_by_id(
            generation_instance_id=generation_instance_id_2,
            average_fitness=3.5,
            fitness_threshold=4.0,
            generation_alpha_brain="Brain_2",
            generation_size=2,
        )

        learning_instance_model = get_learning_model_by_id(self.instance_id)

        generation_objects = learning_instance_model.fk_ref.all()

        for instance in generation_objects:
            self.assertIsInstance(instance, GenerationInstanceModel)
