"""Test related to the Generation instance model and object"""
from django.test import TestCase

from database.internal_use_db_functions.learning_instance_functions import (
    save_learning_instance,
    get_learning_instance,
    get_learning_model,
)

from database.models import GenerationInstanceModel


from database.internal_use_db_functions.generation_instance_functions import (
    save_generation_instance,
    get_generation_instance_with_forign_key,
    get_generation_model_with_forign_key,
    get_generation_model_with_id,
)

from application.lib.storage_objects.generation_object import (
    GenerationObject,
)


class GenerationInstanceModelTests(TestCase):
    """Testing the saving of generation objects with the FK of a learning instance"""

    def setUp(self) -> None:
        self.instance_id = "test_instance"
        self.learning_instance_db_referance = save_learning_instance(self.instance_id)

    def test_saving_and_getting_generation_instance(self):
        """Test creating and saving two generation objects with the correct FK"""

        test_generation_object_1: GenerationObject = GenerationObject(
            generation_instance_id="generation_object_1",
            generation_number=1,
            average_fitnees=1.0,
            fitness_threshold=2.0,
            generation_alpha_brain="holder",
            parents_of_generation=[],
            generaiton_size=2,
            learning_instance_ref=self.learning_instance_db_referance,
        )

        test_generation_1_ref = save_generation_instance(
            this_generation_object=test_generation_object_1,
            learning_instance_referance=self.learning_instance_db_referance,
        )

        generation_object = get_generation_instance_with_forign_key(
            this_learning_instance_ref=self.learning_instance_db_referance
        )

        self.assertIsInstance(generation_object, GenerationObject)

    def test_saving_and_returning_two_generation_instance_with_fk(self):
        """Test saving and returning two gneration_instance using the FK - aka learning instance ref"""

        test_generation_object_2: GenerationObject = GenerationObject(
            generation_instance_id="generation_object_2",
            generation_number=2,
            average_fitnees=1.0,
            fitness_threshold=2.0,
            generation_alpha_brain="holder",
            parents_of_generation=[],
            generaiton_size=2,
            learning_instance_ref=self.learning_instance_db_referance,
        )

        test_generation_object_3: GenerationObject = GenerationObject(
            generation_instance_id="generation_object_3",
            generation_number=3,
            average_fitnees=1.0,
            fitness_threshold=2.0,
            generation_alpha_brain="holder",
            parents_of_generation=[],
            generaiton_size=2,
            learning_instance_ref=self.learning_instance_db_referance,
        )

        test_generation_2_ref = save_generation_instance(
            this_generation_object=test_generation_object_2,
            learning_instance_referance=self.learning_instance_db_referance,
        )

        test_generation_3_ref = save_generation_instance(
            this_generation_object=test_generation_object_3,
            learning_instance_referance=self.learning_instance_db_referance,
        )

        learning_instance_model = get_learning_model(self.instance_id)

        generation_objects = learning_instance_model.fk_ref.all()

        for instance in generation_objects:
            self.assertIsInstance(instance, GenerationInstanceModel)
