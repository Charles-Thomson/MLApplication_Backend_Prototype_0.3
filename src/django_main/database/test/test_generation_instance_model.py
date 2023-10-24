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
        self.instance_id = "test_instance"
        self.learning_instance_db_referance = new_learning_instance_model(
            self.instance_id
        )

    def test_create_update_retrive_generation_model(self) -> GenerationInstanceModel:
        """
        test the creation of a generation instance model
        """
        current_generation_number_1 = 1
        generation_instance_id_1 = f"L{self.instance_id}-G{current_generation_number_1}"

        test_generation_model_ref: json = new_generation_instance_model(
            generation_instance_id=generation_instance_id_1,
            generation_number=current_generation_number_1,
            learning_instance_referance=self.learning_instance_db_referance,
        )

        update_test_data: dict = {
            "average_fitness": 3.5,
            "fitness_threshold": 4.0,
            "generation_alpha_brain": "Brain_2",
            "generation_size": 2,
            "parents_of_generation": ["Brain_1", "brain_2"],
        }

        update_generation_model_by_id(
            generation_instance_id=generation_instance_id_1,
            update_data=update_test_data,
        )

        returned_generation_data: dict = get_generation_data_with_id(
            generation_instance_id=generation_instance_id_1
        )

        print(returned_generation_data)

    def test_multiple_generation_model_retrival_with_fk(self) -> None:
        """Test saving and returning two gneration_instance using the FK - aka learning instance ref"""

        current_generation_number_1 = 1
        generation_instance_id_1 = f"L{self.instance_id}-G{current_generation_number_1}"

        current_generation_number_2 = 2
        generation_instance_id_2 = f"L{self.instance_id}-G{current_generation_number_2}"

        test_generation_model_ref_1: json = new_generation_instance_model(
            generation_instance_id=generation_instance_id_1,
            generation_number=current_generation_number_1,
            learning_instance_referance=self.learning_instance_db_referance,
        )

        test_generation_model_ref_2: json = new_generation_instance_model(
            generation_instance_id=generation_instance_id_2,
            generation_number=current_generation_number_2,
            learning_instance_referance=self.learning_instance_db_referance,
        )

        update_test_data: dict = {
            "average_fitness": 3.5,
            "fitness_threshold": 4.0,
            "generation_alpha_brain": "Brain_2",
            "generation_size": 2,
            "parents_of_generation": ["Brain_1", "brain_2"],
        }

        update_generation_model_by_id(
            generation_instance_id=generation_instance_id_1,
            update_data=update_test_data,
        )

        update_generation_model_by_id(
            generation_instance_id=generation_instance_id_2,
            update_data=update_test_data,
        )

        learning_instance_model = get_learning_model_by_id(self.instance_id)

        generation_objects = learning_instance_model.fk_ref.all()

        for instance in generation_objects:
            self.assertIsInstance(instance, GenerationInstanceModel)
            print(f"FK-Return: {instance}")
