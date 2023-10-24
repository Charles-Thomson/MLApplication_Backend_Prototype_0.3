"""Test relating to the BrainInstance model and object"""
import json
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
        self.generation_instance_id = (
            f"L{self.instance_id}-G{current_generation_number}"
        )

        self.test_generation_model_db_ref: json = new_generation_instance_model(
            generation_instance_id=self.generation_instance_id,
            generation_number=current_generation_number,
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
            generation_instance_id=self.generation_instance_id,
            update_data=update_test_data,
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
        self.brain_id = f"L:{self.instance_id}-G:{self.generation_instance_id}-B:1"

        self.test_brain = BrainFactory.make_brain(
            brain_id=self.brain_id,
            brain_type=self.test_brain_type,
            brain_config=self.foramtted_test_config,
        )

    def test_brain_model_creation_and_retrival(self) -> None:
        """
        Test the creation, updating and retrival of a BrainInstanceModel
        """

        save_brain_instance(
            brain_instance=self.test_brain,
            generation_instance_db_ref=self.test_generation_model_db_ref,
        )

        returned_brain_instance: BrainInstance = get_brain_instance_by_id(
            brain_id=self.brain_id
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

        test_brain_instance_1 = BrainFactory.make_brain(
            brain_id=f"L:{self.instance_id}-G:{self.generation_instance_id}-B:1",
            brain_type=self.test_brain_type,
            brain_config=self.foramtted_test_config,
        )

        test_brain_instance_2 = BrainFactory.make_brain(
            brain_id=f"L:{self.instance_id}-G:{self.generation_instance_id}-B:2",
            brain_type=self.test_brain_type,
            brain_config=self.foramtted_test_config,
        )

        save_brain_instance(
            brain_instance=test_brain_instance_1,
            generation_instance_db_ref=self.test_generation_model_db_ref,
        )

        save_brain_instance(
            brain_instance=test_brain_instance_2,
            generation_instance_db_ref=self.test_generation_model_db_ref,
        )

        generation_model = get_generation_model_with_id(
            generation_instance_id=self.generation_instance_id
        )

        brain_instances = generation_model.fk_ref.all()

        for x in brain_instances:
            self.assertIsInstance(x, BrainInstanceModel)
