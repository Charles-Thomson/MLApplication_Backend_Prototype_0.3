"""
Functions used internally by the back end 
Not used by the API of database.views
"""
from application.lib.agent_brain.static_state_brain import BrainInstance
from django.db import models
from database.models import (
    BrainInstanceModel,
    GenerationInstanceModel,
    LearningInstanceModel,
)
from database.model_data_formatting import (
    brain_instance_to_model,
    model_to_brain_instance,
    generation_model_to_object,
    generation_object_to_model,
    learning_instance_data_to_model,
    learning_instance_model_to_object,
)

from application.lib.storage_objects.learning_instance_object import (
    LearningInstanceObject,
)
from application.lib.storage_objects.generation_object import (
    GenerationObject,
)

from logging_files.logging_decos import with_save_generation_logging


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

    model = learning_instance_data_to_model(learning_instance_data)

    model.save()

    return model


def get_learning_instance(learning_instance_id: int) -> None:
    """Get a brain Instance back from the model"""

    learing_instance_model: LearningInstanceModel = LearningInstanceModel.objects.get(
        learning_instance_id=learning_instance_id
    )

    rtn_data = learning_instance_model_to_object(learing_instance_model)

    return rtn_data


def save_generation_object(
    this_generation_object: GenerationObject, learning_instance_referance: str
) -> GenerationInstanceModel:
    """
    Save a generation_instace_object to the database
    """

    new_generation_model_ref: GenerationInstanceModel = generation_object_to_model(
        this_generation_object, learning_instance_referance
    )

    new_generation_model_ref.save()

    return new_generation_model_ref


def get_generation_model(this_learning_instance_ref: str) -> GenerationObject:
    """
    Get a generation model and return it as a genertion_object
    """

    generation_instance_model: GenerationInstanceModel = (
        GenerationInstanceModel.objects.get(
            learning_instance_ref=this_learning_instance_ref
        )
    )

    rtn_data = generation_model_to_object(generation_instance_model)

    return rtn_data


def save_brain_instance(brain_instance: BrainInstance, model_type: str) -> None:
    """Save the given Brain Instance to the Django DB"""

    new_brain_instance_as_model: models.Model = brain_instance_to_model(
        brain_instance, model_type=model_type
    )

    new_brain_instance_as_model.save()


def get_generation_instance(generation_id: int) -> None:
    """Get a brain Instance back from the model"""

    generation_model: GenerationInstanceModel = GenerationInstanceModel.objects.get(
        generation_id=generation_id
    )

    rtn_data = generation_model_to_data(generation_model)

    return rtn_data


def get_brain_instance(brain_id: int) -> None:
    """Get a brain Instance back from the model"""

    brain_model: BrainInstanceModel = BrainInstanceModel.objects.get(id=brain_id)

    rtn_brain_instance = model_to_brain_instance(brain_model)

    return rtn_brain_instance


def clear_all_models_for_database() -> None:
    """
    Delete all models from the database
    """
    BrainInstanceModel.objects.all().delete()
    GenerationInstanceModel.objects.all().delete()
