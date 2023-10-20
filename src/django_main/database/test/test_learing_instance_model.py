"""Test covering the learing instance model"""
from django.test import TestCase

from database.internal_use_db_functions.learning_instance_functions import (
    save_learning_instance,
    get_learning_instance,
    get_learning_model,
)

from application.lib.storage_objects.learning_instance_object import (
    LearningInstanceObject,
)


class LearningInsanceModelTests(TestCase):
    """
    Testing the creation and saving/get of a learning instance mode
    """

    def setUp(self) -> None:
        self.instance_id = "test_intance_id"

    def test_saving_learning_instance(self):
        """
        Test the process of saving a learning instance model
        """

        instance_ref = save_learning_instance(self.instance_id)

        learning_instance_object = get_learning_instance(self.instance_id)

        self.assertIsInstance(learning_instance_object, LearningInstanceObject)
