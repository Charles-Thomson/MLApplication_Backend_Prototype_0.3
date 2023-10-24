"""Test covering the learing instance model"""
from django.test import TestCase

from database.internal_use_db_functions.learning_instance_functions import (
    new_learning_instance_model,
    get_learning_data_by_id,
    get_learning_model_by_id,
    update_learning_instance_model_by_id,
)


class LearningInsanceModelTests(TestCase):
    """
    Testing the creation and saving/get of a learning instance mode
    """

    def setUp(self) -> None:
        self.learning_instance_id = "test_intance_id"

    def test_create_update_retrive_learning_model(self) -> None:
        """
        Test the process of saving a learning instance model
        """

        instance_ref = new_learning_instance_model(self.learning_instance_id)

        update_learning_instance_model_by_id(
            learning_instance_id=self.learning_instance_id,
            new_alpha_brain="alpha_brain",
            total_generations=1,
        )

        learning_instance_data = get_learning_data_by_id(self.learning_instance_id)

        print(f"Learning Instance data after update: {learning_instance_data} ")
