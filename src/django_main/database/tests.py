"""Testing of BrainInstance model generation and DB elements"""

import numpy as np
from application.lib.instance_generation.instance_generation_main import (
    format_brain_config,
)
from application.lib.agent_brain.brain_factory import BrainFactory

from database.model_data_formatting import (
    brain_instance_to_model,
    model_to_brain_instance,
    gernation_data_to_model,
    generation_model_to_data,
)

from database.models import GenerationInstanceModel, BrainInstanceModel

from database.db_functions import save_full_generation, get_generation_instance

from application.lib.agent_brain.static_state_brain import BrainInstance

from django.test import TestCase


# Create your tests here.


test_brain_config: dict = {
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
        foramtted_test_config: dict = format_brain_config(
            brain_config=test_brain_config
        )
        test_brain_type: str = "random_weighted_brain"

        self.test_brain = BrainFactory.make_brain(
            brain_id="test_brain",
            brain_type=test_brain_type,
            brain_config=foramtted_test_config,
        )

    def test_brain_instance_model_creation(self) -> None:
        """Test teh creation of a brain instance model from a BrainInstance"""

        brain_instance_as_model = brain_instance_to_model(
            brain_instance=self.test_brain
        )
        self.assertIsInstance(brain_instance_as_model, BrainInstanceModel)

    def test_brain_instance_model_to_brain_instance(self) -> None:
        """
        The conversion of a model insance to a Brain Instance
        """

        brain_instance_as_model = brain_instance_to_model(
            brain_instance=self.test_brain
        )

        brain_model_as_instance = model_to_brain_instance(
            brain_model=brain_instance_as_model
        )

        self.assertIsInstance(brain_model_as_instance, BrainInstance)
        assert callable(brain_model_as_instance.hidden_layer_activation_func)
        assert callable(brain_model_as_instance.output_layer_activation_func)
        self.assertIsInstance(brain_model_as_instance.hidden_weights, np.ndarray)
        self.assertIsInstance(brain_model_as_instance.output_weights, np.ndarray)


class GenerationModelTestCase(TestCase):
    """
    Testing the creation, formatting, saving and getting of a Generational_model
    """

    def setUp(self) -> None:
        self.generation_id = "test_generation_id_1"
        self.generation_brain_instances = self.generate_test_parents()
        self.generation_number: int = 1
        self.average_fitness: float = 5.5
        self.fitness_threshold: float = 6.0

    def test_generation_data_to_model(self) -> None:
        """
        Test converting given generation data to the generation_data_model
        """

        average_fitness: float = sum(
            instance.fitness for instance in self.generation_brain_instances
        ) / len(self.generation_brain_instances)
        generation_data: dict = {
            "generation_id": self.generation_id,
            "generation_brain_instances": self.generation_brain_instances,
            "fitness_threshold": self.fitness_threshold,
            "generation_number": self.generation_number,
            "average_fitness": average_fitness,
        }

        new_generation_model = gernation_data_to_model(generation_data=generation_data)

        self.assertIsInstance(new_generation_model, GenerationInstanceModel)

    def test_generation_model_to_data(self) -> None:
        """
        Test returning the stored data to the desiered format
        """

        average_fitness: float = sum(
            instance.fitness for instance in self.generation_brain_instances
        ) / len(self.generation_brain_instances)

        generation_data: dict = {
            "generation_id": self.generation_id,
            "generation_brain_instances": self.generation_brain_instances,
            "fitness_threshold": self.fitness_threshold,
            "generation_number": self.generation_number,
            "average_fitness": average_fitness,
        }

        test_generation_model = gernation_data_to_model(generation_data=generation_data)
        test_generation_model_data = generation_model_to_data(
            generational_model=test_generation_model
        )

        self.assertEqual(
            test_generation_model_data["generation_id"], self.generation_id
        )

        self.assertEqual(
            len(test_generation_model_data["generation_brain_instances"]),
            len(self.generation_brain_instances),
        )

        self.assertEqual(
            float(test_generation_model_data["fitness_threshold"]),
            self.fitness_threshold,
        )
        self.assertEqual(
            int(test_generation_model_data["generation_number"]), self.generation_number
        )
        self.assertEqual(
            float(test_generation_model_data["average_fitness"]), average_fitness
        )

    def test_none_api_save_and_get_generation_model(self) -> None:
        """
        Test the saving of the model to the DB
        Test the getting of the model from the DB by id
        """
        save_full_generation(
            generation_id=self.generation_id,
            generation_brain_instances=self.generation_brain_instances,
            fitness_threshold=self.fitness_threshold,
            generation_number=self.generation_number,
        )

        test_generation_instance_data: GenerationInstanceModel = (
            get_generation_instance(generation_id=self.generation_id)
        )

    # This can be refactored down
    def generate_test_parents(self) -> list[BrainInstance]:
        """
        Generate test brain insatnces for testing
        """

        foramtted_test_config: dict = format_brain_config(
            brain_config=test_brain_config
        )
        test_brain_type: str = "random_weighted_brain"

        def make_new_brain():
            new_brain: BrainFactory = BrainFactory.make_brain(
                brain_id="test_brain",
                brain_type=test_brain_type,
                brain_config=foramtted_test_config,
            )
            return new_brain

        generation_brain_instances: list[BrainInstance] = [
            make_new_brain() for _ in range(10)
        ]

        assert len(generation_brain_instances) == 10

        return generation_brain_instances
