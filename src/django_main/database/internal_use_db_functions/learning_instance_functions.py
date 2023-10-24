"""The internal functions relating to the learning_instance DB operations"""

import json

import jsonpickle
from database.models import LearningInstanceModel
from django.db.models import F

from database.data_modeling.learning_instance_modeling import (
    learning_instance_data_to_model,
    learning_model_to_data,
)


def new_learning_instance_model(
    learning_instance_id: str,
) -> LearningInstanceModel:
    """
    Save a learning instance to the db
    var: learning_instance_data - related data as a dict
    rnt: The model
    """
    learning_instance_data: dict = {
        "learning_instance_id": learning_instance_id,
        "alpha_brain": None,
        "number_of_generations": 0,
    }

    model = learning_instance_data_to_model(learning_instance_data)

    model.save()

    return model


def get_learning_data_by_id(learning_instance_id: int) -> json:
    """Get a brain Instance back from the model"""

    learing_instance_model: LearningInstanceModel = LearningInstanceModel.objects.get(
        learning_instance_id=learning_instance_id
    )

    return learning_model_to_data(learing_instance_model)


def get_learning_model_by_id(learning_instance_id: str) -> LearningInstanceModel:
    """
    Get a learning instance model based on a given id
    """

    learing_instance_model: LearningInstanceModel = LearningInstanceModel.objects.get(
        learning_instance_id=learning_instance_id
    )

    return learing_instance_model


def update_learning_instance_model_by_id(
    learning_instance_id: str, new_alpha_brain: object, total_generations: int
) -> None:
    """
    Update a learning instance - selected by learning instance id
    """

    learning_instance: LearningInstanceModel = LearningInstanceModel.objects.get(
        learning_instance_id=learning_instance_id
    )

    learning_instance.alpha_brain = jsonpickle.encode(new_alpha_brain)

    learning_instance.number_of_generations = total_generations

    learning_instance.save(update_fields=["alpha_brain", "number_of_generations"])
