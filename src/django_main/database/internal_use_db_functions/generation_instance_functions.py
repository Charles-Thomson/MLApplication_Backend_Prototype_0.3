"""The internal functions relating to the generation_instance DB operations"""

import jsonpickle
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


def update_generation_model_by_id(
    generation_instace_id: str, update_data: dict
) -> None:
    """
    Update a given generation instance - selected by the generation instances id
    """

    generation_instance: GenerationInstanceModel = GenerationInstanceModel.objects.get(
        generation_instace_id=generation_instace_id
    )
    jsonpickle.encode(update_data["generation_alpha_brain"])
    generation_instance.average_fitness = update_data["averag_fitness"]
    generation_instance.fitness_threshold = update_data["fitness_threshold"]
    generation_instance.generation_alpha_brain = jsonpickle.encode(
        update_data["generation_alpha_brain"]
    )
    generation_instance.generation_size = update_data["generation_size"]
    generation_instance.parents_of_generation = jsonpickle.encode(
        update_data["parents_of_generation"]
    )

    generation_instance.save(
        update_fields=[
            "average_fitness",
            "fitness_threshold",
            "generation_alpha_brain",
            "generation_size",
            "parents_of_generation",
        ]
    )
