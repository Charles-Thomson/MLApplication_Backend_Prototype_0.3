import json
import numpy as np
import jsonpickle

from application.lib.agent_brain.static_state_brain import BrainInstance

from application.lib.agent_brain.brain_factory import BrainFactory

from database.models import DatabaseModelsFactory
from rest_framework import serializers
from database.models import BrainInstanceModel


class ModelToBrainInstanceSerializer(serializers.ModelSerializer):
    """
    Serialize the model for model to instance

    """

    class Meta:
        model = BrainInstanceModel
        fields = "__all__"


def brain_instance_to_model(brain_instance: object, model_type: str) -> BrainInstance:
    """Save the brain instance as a fit instance"""

    model = DatabaseModelsFactory.get_model(model_type="general")

    weights_dict: dict = {
        "hidden_weights": brain_instance.hidden_weights.tolist(),
        "output_weights": brain_instance.output_weights.tolist(),
    }

    functions_callable_jsonpickle: json = jsonpickle.encode(
        brain_instance.functions_callable
    )
    weights_json = json.dumps(weights_dict)

    traversed_path: str = ",".join(str(val) for val in brain_instance.traversed_path)
    fitness_by_step: str = ",".join(str(val) for val in brain_instance.fitness_by_step)

    new_db_brain_model = model(
        brain_id=brain_instance.brain_id,
        brain_type=brain_instance.brain_type,  # May rename to Model type ?
        current_generation_number=brain_instance.current_generation_number,
        fitness=brain_instance.fitness,
        weights=weights_json,
        traversed_path=traversed_path,
        fitness_by_step=fitness_by_step,
        functions_callable=functions_callable_jsonpickle
        # svg_path=brain_instance.svg_path,
        # svg_start=brain_instance.svg_start,
        # svg_end=brain_instance.svg_end,
    )

    return new_db_brain_model


def model_to_brain_instance(brain_model) -> BrainInstance:
    """Convert a brain_model used by the DB to a Brain Instance"""

    brain_config: dict = ModelToBrainInstanceSerializer(brain_model).data

    brain_config: dict = set_config_attributes_format(brain_config=brain_config)

    new_brain_instance: BrainInstance = BrainFactory.make_brain(
        brain_type=brain_config["brain_type"],
        ann_config=brain_config,
    )

    print(new_brain_instance.functions_callable)

    return new_brain_instance


def set_config_attributes_format(brain_config: dict) -> dict:
    """
    Convert the attributes back to the origional fromat from bytes
    var: brain_config - config with some attributes in byte format
    rtn: brain_config - config with all attributes in origional format
    """

    brain_config["brain_type"] = "base_brain_instance"

    brain_config["weights"] = json.loads(brain_config["weights"])
    brain_config["functions_callable"] = jsonpickle.decode(
        brain_config["functions_callable"]
    )

    brain_config["weights"]["hidden_weights"] = np.array(
        brain_config["weights"]["hidden_weights"]
    )
    brain_config["weights"]["output_weights"] = np.array(
        brain_config["weights"]["output_weights"]
    )
    brain_config["traversed_path"] = brain_config["traversed_path"].split(",")
    brain_config["fitness_by_step"] = brain_config["fitness_by_step"].split(",")

    return brain_config


def gernation_to_model(generation_data: dict) -> json:
    """
    Set convert a given geenration i.e set of parents to a db model
    var: generation_data - The given data for the generation
    rtn: new_generation_model - generation data in a db model format
    """

    model = DatabaseModelsFactory.get_model(model_type="generation_storeage_model")

    generations_parents_pickle: json = jsonpickle.encode(generation_data.parents)

    new_generation_model = model(
        generation_id=generate_generation_id(),
        generation_number=generation_data["generation_number"],
        average_fitness=generation_data["average_fitness"],
        BrainInstance=generations_parents_pickle,
    )

    return new_generation_model


def generate_generation_id() -> str:
    """
    Generate a generation models id
    """
    return "test-id"
