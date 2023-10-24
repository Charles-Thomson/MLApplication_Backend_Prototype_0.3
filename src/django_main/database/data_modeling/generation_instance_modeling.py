"""Data modeling for the generation instance models/objects"""
import json
import jsonpickle

from database.serializers import ModelToGenerationDataSerializer
from database.models import DatabaseModelsFactory, GenerationInstanceModel


def generation_data_to_model(generation_data: dict) -> json:
    """
    Set convert a given geenration i.e set of parents to a db model
    var: generation_data - The given data for the generation
    rtn: new_generation_model - generation data in a db model format
    """

    model = DatabaseModelsFactory.get_model(model_type="generation_instance_model")

    new_generation_model = model(
        generation_instance_id=generation_data["generation_instance_id"],
        generation_number=generation_data["generation_number"],
        average_fitness=generation_data["average_fitness"],
        fitness_threshold=generation_data["fitness_threshold"],
        parents_of_generation=jsonpickle.encode(
            generation_data["parents_of_generation"]
        ),
        generation_size=generation_data["generation_size"],
        generation_alpha_brain=jsonpickle.encode(
            generation_data["generation_alpha_brain"]
        ),
        learning_instance_ref=generation_data["learning_instance_ref"],
    )

    return new_generation_model


def generation_model_to_data(
    generational_model: GenerationInstanceModel,
) -> json:
    """
    Convert a generation_model to a usable data form
    var: generational_model - Generational data in model form
    rtn: generation data - generation data of given model in usable format
    """

    return ModelToGenerationDataSerializer(generational_model).data
