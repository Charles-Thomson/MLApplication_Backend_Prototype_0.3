"""The internal functions relating to the learning_instance DB operations"""

from database.models import LearningInstanceModel
from django.db.models import F

from database.data_modeling.learning_instance_modeling import (
    learning_instance_to_model,
    learning_model_to_instance,
)

from application.lib.storage_objects.learning_instance_object import (
    LearningInstanceObject,
)


# this is building the instance here via an id - not sure if correct approach
def save_learning_instance(
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

    model = learning_instance_to_model(learning_instance_data)

    model.save()

    return model


def get_learning_instance(learning_instance_id: int) -> LearningInstanceObject:
    """Get a brain Instance back from the model"""

    learing_instance_model: LearningInstanceModel = LearningInstanceModel.objects.get(
        learning_instance_id=learning_instance_id
    )

    rtn_data = learning_model_to_instance(learing_instance_model)

    return rtn_data


def get_learning_model(learning_instance_id: str) -> LearningInstanceModel:
    """
    Get a learning instance model based on a given id
    """

    learing_instance_model: LearningInstanceModel = LearningInstanceModel.objects.get(
        learning_instance_id=learning_instance_id
    )

    print(learing_instance_model)

    return learing_instance_model


def update_learning_instance_model_by_id(
    learning_instance_id: str, new_alpha_brain: object
) -> None:
    """
    Update a learning instance - selected by learning instance id
    """

    learning_instance: LearningInstanceModel = LearningInstanceModel.objects.get(
        learning_instance_id=learning_instance_id
    )

    learning_instance_id.alpha_brain = new_alpha_brain
    learning_instance.number_of_generations = F("number_of_generations") + 1

    learning_instance.save(update_fields=["alpha_brain", "number_of_generations"])
