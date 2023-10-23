"""Data modeling for the generation instance models/objects"""
import json
import jsonpickle

from database.serializers import ModelToGenerationDataSerializer
from database.models import DatabaseModelsFactory, GenerationInstanceModel

from application.lib.storage_objects.generation_object import GenerationObject


def generation_instance_to_model(
    generation_data: GenerationObject, learning_instance_referace: str
) -> json:
    """
    Set convert a given geenration i.e set of parents to a db model
    var: generation_data - The given data for the generation
    rtn: new_generation_model - generation data in a db model format
    """

    model = DatabaseModelsFactory.get_model(model_type="generation_instance_model")

    new_generation_model = model(
        generation_instance_id=generation_data.generation_instance_id,
        generation_number=generation_data.generation_number,
        average_fitness=generation_data.average_fitnees,
        fitness_threshold=generation_data.fitness_threshold,
        parents_of_generation=jsonpickle.encode(generation_data.parents_of_generation),
        generation_size=generation_data.generaiton_size,
        generation_alpha_brain=jsonpickle.encode(
            generation_data.generation_alpha_brain
        ),
        learning_instance_ref=learning_instance_referace,
    )

    return new_generation_model


def generation_model_to_instance(
    generational_model: GenerationInstanceModel,
) -> GenerationObject:
    """
    Convert a generation_model to a usable data form
    var: generational_model - Generational data in model form
    rtn: this_generation_data - generation data of given model in usable format
    """

    generation_data: dict = ModelToGenerationDataSerializer(generational_model).data

    generation_data_object: GenerationObject = GenerationObject(*generation_data)

    return generation_data_object
