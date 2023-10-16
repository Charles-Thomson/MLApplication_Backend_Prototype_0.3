"""
Functions used internally by the back end 
Not used by the API of database.views
"""
from application.lib.agent_brain.static_state_brain import BrainInstance
from django.db import models
from database.models import BrainInstanceModel
from database.model_data_formatting import (
    brain_instance_to_model,
    model_to_brain_instance,
    gernation_to_model,
)


def save_brain_instance(brain_instance: BrainInstance, model_type: str) -> None:
    """Save the given Brain Instance to the Django DB"""

    new_brain_instance_as_model: models.Model = brain_instance_to_model(
        brain_instance, model_type=model_type
    )

    new_brain_instance_as_model.save()


def save_full_generation(generation_data: dict) -> None:
    """
    Save a full generation to the db
    """

    new_generation_model: models.Model = gernation_to_model(
        generation_data=generation_data
    )

    new_generation_model.save()


def clear_all_models_for_database() -> None:
    """
    Delete all models from the database
    """
    BrainInstanceModel.objects.all().delete()
