"""The internal functions relating to the generation_instance DB operations"""

import json
import jsonpickle
from database.models import GenerationInstanceModel
from database.data_modeling.generation_instance_modeling import (
    generation_data_to_model,
    generation_model_to_data,
)


def new_generation_instance_model(
    generation_instance_id: str,
    generation_number: int,
    learning_instance_referance: str,
    parents_of_generation: list,
) -> json:
    """
    Create a new gneneration instance model
    var: generation_instance_id - the string used as the id of the generation model
    var: learning_instance_referance - used as the FK in the generation instance model
    rtn: model - used as the FK by BrainInstanceModels
    """

    generation_instance_data: dict = {
        "generation_instance_id": generation_instance_id,
        "generation_number": generation_number,
        "average_fitness": 0.0,
        "fitness_threshold": 0.0,
        "parents_of_generation": parents_of_generation,
        "generation_size": 0,
        "generation_alpha_brain": None,
        "learning_instance_ref": learning_instance_referance,
    }

    model = generation_data_to_model(generation_instance_data)

    model.save()

    return model


def get_generation_data_with_forign_key(
    this_learning_instance_ref: str,
) -> json:
    """
    Get a generation model and return it as a genertion_object
    """

    generation_instance_model: GenerationInstanceModel = (
        GenerationInstanceModel.objects.get(
            learning_instance_ref=this_learning_instance_ref
        )
    )

    return generation_model_to_data(generation_instance_model)


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

    return generation_instance_model


def get_generation_data_with_id(
    generation_instance_id: str,
) -> GenerationInstanceModel:
    """
    Get a generation model data with a given id
    """

    generation_instance_model: GenerationInstanceModel = (
        GenerationInstanceModel.objects.get(
            generation_instance_id=generation_instance_id
        )
    )
    return generation_model_to_data(generation_instance_model)


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
    return generation_instance_model


def update_generation_model_by_id(
    generation_instance_id: str,
    average_fitness: float,
    fitness_threshold: float,
    generation_alpha_brain: object,
    generation_size: int,
) -> None:
    """
    Update a given generation instance - selected by the generation instances id
    var: generation_instance_id - generation instance to be updated
    var: average_fitness- average fitness from a genration
    var: fitness_threshold - fitness threshold from a generation
    var: generation_alpha_brain - the highest fitness brain of the generation
    var: generation_size - the size of the genration(No* BrainInstances)
    """

    generation_instance: GenerationInstanceModel = GenerationInstanceModel.objects.get(
        generation_instance_id=generation_instance_id
    )

    generation_instance.average_fitness = average_fitness
    generation_instance.fitness_threshold = fitness_threshold
    generation_instance.generation_alpha_brain = jsonpickle.encode(
        generation_alpha_brain
    )
    generation_instance.generation_size = generation_size

    generation_instance.save(
        update_fields=[
            "average_fitness",
            "fitness_threshold",
            "generation_alpha_brain",
            "generation_size",
        ]
    )
