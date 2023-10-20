"""The internal functions relating to the generation_instance DB operations"""

from database.models import GenerationInstanceModel
from database.data_modeling.generation_instance_modeling import (
    generation_instance_to_model,
    generation_model_to_instance,
)


from application.lib.storage_objects.generation_object import GenerationObject


def save_generation_instance(
    this_generation_object: GenerationObject, learning_instance_referance: str
) -> GenerationInstanceModel:
    """
    Save a generation_instace_object to the database
    """

    new_generation_model_ref: GenerationInstanceModel = generation_instance_to_model(
        this_generation_object, learning_instance_referance
    )

    new_generation_model_ref.save()

    return new_generation_model_ref


def get_generation_instance_with_forign_key(
    this_learning_instance_ref: str,
) -> GenerationObject:
    """
    Get a generation model and return it as a genertion_object
    """

    generation_instance_model: GenerationInstanceModel = (
        GenerationInstanceModel.objects.get(
            learning_instance_ref=this_learning_instance_ref
        )
    )

    rtn_data = generation_model_to_instance(generation_instance_model)

    return rtn_data


def get_generation_model_with_forign_key(
    this_learning_instance_ref: str,
) -> GenerationInstanceModel:
    """
    Get all generation instnce models with a given learning instance ref
    """

    generation_instance_model: GenerationInstanceModel = (
        GenerationInstanceModel.objects.get(
            learning_instance_ref=this_learning_instance_ref
        )
    )

    print(generation_instance_model)

    return generation_instance_model


def get_generation_model_with_id(
    generation_instance_id: str,
) -> GenerationInstanceModel:
    """
    Get a generation model with a given id
    """

    generation_instance_model: GenerationInstanceModel = (
        GenerationInstanceModel.objects.get(
            generation_instance_id=generation_instance_id
        )
    )

    print(generation_instance_model)

    return generation_instance_model
