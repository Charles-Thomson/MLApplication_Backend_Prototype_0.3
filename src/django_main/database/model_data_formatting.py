import json
import numpy as np
import jsonpickle

from application.lib.agent_brain.static_state_brain import BrainInstance

from application.lib.agent_brain.brain_factory import BrainFactory

from application.lib.storage_objects.generation_object import GenerationObject
from application.lib.storage_objects.learning_instance_object import (
    LearningInstanceObject,
)

from database.models import (
    DatabaseModelsFactory,
    GenerationInstanceModel,
    LearningInstanceModel,
)

from database.serializers import (
    ModelToBrainInstanceSerializer,
    ModelToGenerationDataSerializer,
    ModelToLearningInstanceSerializer,
)


from database.models import BrainInstanceModel


def brain_instance_to_model(brain_instance: object) -> BrainInstanceModel:
    """Save the brain instance as a fit instance"""

    model = DatabaseModelsFactory.get_model(model_type="brain_instance_model")

    weights_dict: dict = {
        "hidden_weights": brain_instance.hidden_weights.tolist(),
        "output_weights": brain_instance.output_weights.tolist(),
    }

    new_db_brain_model = model(
        brain_id=brain_instance.brain_id,
        brain_type=brain_instance.brain_type,  # May rename to Model type ?
        current_generation_number=brain_instance.current_generation_number,
        fitness=brain_instance.fitness,
        weights=json.dumps(weights_dict),
        traversed_path=json.dumps(brain_instance.traversed_path),
        fitness_by_step=json.dumps(brain_instance.fitness_by_step),
        functions_callable=jsonpickle.encode(brain_instance.functions_callable)
        # svg_path=brain_instance.svg_path,
        # svg_start=brain_instance.svg_start,
        # svg_end=brain_instance.svg_end,
    )

    return new_db_brain_model


def model_to_brain_instance(brain_model) -> BrainInstance:
    """Convert a brain_model used by the DB to a Brain Instance"""

    brain_config: dict = ModelToBrainInstanceSerializer(brain_model).data

    brain_config["brain_type"] = "base_brain_instance"

    brain_config["functions_callable"] = jsonpickle.decode(
        brain_config["functions_callable"]
    )

    un_formatted_weights: dict = json.loads(brain_config["weights"])

    brain_config["weights"] = {
        "hidden_weights": np.array(un_formatted_weights["hidden_weights"]),
        "output_weights": np.array(un_formatted_weights["output_weights"]),
    }

    brain_config["traversed_path"] = json.loads(brain_config["traversed_path"])
    brain_config["fitness_by_step"] = json.loads(brain_config["fitness_by_step"])

    new_brain_instance: BrainInstance = BrainFactory.make_brain(
        brain_id=brain_config["brain_id"],
        brain_type=brain_config["brain_type"],
        brain_config=brain_config,
    )

    return new_brain_instance


def generation_object_to_model(
    generation_data: GenerationObject, learning_instance_referace: str
) -> json:
    """
    Set convert a given geenration i.e set of parents to a db model
    var: generation_data - The given data for the generation
    rtn: new_generation_model - generation data in a db model format
    """

    model = DatabaseModelsFactory.get_model(model_type="generation_instance_model")

    new_generation_model = model(
        generation_id=generation_data.generation_id,
        generation_number=generation_data.generation_number,
        average_fitness=generation_data.average_fitnees,
        fitness_threshold=generation_data.fitness_threshold,
        parents_of_generation=jsonpickle.encode(generation_data.parents_of_generation),
        generation_alpha_brain=jsonpickle.encode(
            generation_data.generation_alpha_brain
        ),
        learning_instance_ref=learning_instance_referace,
    )

    return new_generation_model


def generation_model_to_object(
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


def learning_instance_data_to_model(
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


def learning_instance_model_to_object(
    this_model: LearningInstanceModel,
) -> LearningInstanceObject:
    """
    Convert a learning instance model to a learning instance Object
    """

    model_data: dict = ModelToLearningInstanceSerializer(this_model).data

    new_object: LearningInstanceObject = LearningInstanceObject(*model_data)

    return new_object


def generate_generation_id() -> str:
    """
    Generate a generation models id
    """
    return "test-id"
