"""Fucntions for the modeling of the brain instance data/objetcs"""
import json
import jsonpickle
import numpy as np

from database.serializers import ModelToBrainInstanceSerializer
from database.models import DatabaseModelsFactory, BrainInstanceModel

from application.lib.agent_brain.brain_factory import BrainFactory
from application.lib.agent_brain.static_state_brain import BrainInstance


def brain_instance_to_model(
    brain_instance: object, generation_instance_ref: str
) -> BrainInstanceModel:
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
        functions_callable=jsonpickle.encode(brain_instance.functions_callable),
        generation_instance_ref=generation_instance_ref
        # svg_path=brain_instance.svg_path,
        # svg_start=brain_instance.svg_start,
        # svg_end=brain_instance.svg_end,
    )

    return new_db_brain_model


def brain_model_to_instance(brain_model) -> BrainInstance:
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
