"""
Functions used internally by the back end 
Not used by the API of database.views
"""
from application.lib.agent_brain.static_state_brain import BrainInstance
from django.db import models
from database.models import BrainInstanceModel, GenerationInstanceModel
from database.model_data_formatting import (
    brain_instance_to_model,
    model_to_brain_instance,
    generation_model_to_data,
    gernation_data_to_model,
)


def save_brain_instance(brain_instance: BrainInstance, model_type: str) -> None:
    """Save the given Brain Instance to the Django DB"""

    new_brain_instance_as_model: models.Model = brain_instance_to_model(
        brain_instance, model_type=model_type
    )

    new_brain_instance_as_model.save()


def save_full_generation(
    generation_id: str,
    parents: list[BrainInstance],
    fitness_threshold: float,
    generation_number: int,
) -> None:
    """
    Save a full generation to the db
    """

    average_fitness: float = sum(instance.fitness for instance in parents) / len(
        parents
    )
    generation_data: dict = {
        "generation_id": generation_id,
        "brain_instances": parents,
        "fitness_threshold": fitness_threshold,
        "generation_number": generation_number,
        "average_fitness": average_fitness,
    }

    new_generation_model: models.Model = gernation_data_to_model(
        generation_data=generation_data
    )

    new_generation_model.save()


def get_brain_instance(brain_id: int) -> None:
    """Get a brain Instance back from the model"""

    brain_model: BrainInstanceModel = BrainInstanceModel.objects.get(id=brain_id)

    rtn_brain_instance = model_to_brain_instance(brain_model)

    return rtn_brain_instance


def get_generation_instance(generation_id: int) -> None:
    """Get a brain Instance back from the model"""

    generation_model: GenerationInstanceModel = GenerationInstanceModel.objects.get(
        generation_id=generation_id
    )

    rtn_data = generation_model_to_data(generation_model)

    return rtn_data


def clear_all_models_for_database() -> None:
    """
    Delete all models from the database
    """
    BrainInstanceModel.objects.all().delete()
    GenerationInstanceModel.objects.all().delete()
