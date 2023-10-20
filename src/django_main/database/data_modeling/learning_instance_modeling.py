""" Data modeling for the learning instance modesl/objects"""
from database.serializers import ModelToLearningInstanceSerializer
from database.models import DatabaseModelsFactory, LearningInstanceModel

from application.lib.storage_objects.learning_instance_object import (
    LearningInstanceObject,
)


def learning_instance_to_model(
    learning_instance_data: dict,
) -> LearningInstanceModel:
    """
    Convert learning instance data to a learning instance model
    """

    model = DatabaseModelsFactory.get_model(model_type="learning_instance_model")

    new_model: LearningInstanceModel = model(
        id=0,
        learning_instance_id=learning_instance_data["learning_instance_id"],
        alpha_brain="{}",
        number_of_generations="0",
    )

    return new_model


def learning_model_to_instance(
    this_model: LearningInstanceModel,
) -> LearningInstanceObject:
    """
    Convert a learning instance model to a learning instance Object
    """

    model_data: dict = ModelToLearningInstanceSerializer(this_model).data

    new_object: LearningInstanceObject = LearningInstanceObject(*model_data)

    return new_object
