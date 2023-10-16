import json
import numpy as np

from application.lib.agent_brain.static_state_brain import BrainInstance

from application.lib.agent_brain.brain_factory import BrainFactory

from database.models import DatabaseModelsFactory


def brain_instance_to_model(brain_instance: object, model_type: str) -> BrainInstance:
    """Save the brain instance as a fit instance"""

    # TODO: Move away from hard coded model_type
    model = DatabaseModelsFactory.get_model(model_type="general")

    hidden_weights: bytes = brain_instance.hidden_weights.tolist()
    output_weights: bytes = brain_instance.output_weights.tolist()

    weights_dict: dict = {
        "hidden_weights": hidden_weights,
        "output_weights": output_weights,
    }

    functions_callable_dict: dict = {
        "functions_callable": {
            "weight_init_huristic": "",
            "hidden_activation_func": "",
            "output_activation_func": "",
            "new_generation_func": "",
        }
    }

    weights_json = json.dumps(weights_dict)
    functions_callable_json: json = json.dumps(functions_callable_dict)
    functions_ref_json: json = json.dumps(brain_instance.functions_ref)

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
        functions_ref=functions_ref_json,
        functions_callable=functions_callable_json
        # svg_path=brain_instance.svg_path,
        # svg_start=brain_instance.svg_start,
        # svg_end=brain_instance.svg_end,
    )

    return new_db_brain_model


def model_to_brain_instance(brain_model) -> BrainInstance:
    """Convert a brain_model used by the DB to a Brain Instance"""

    brain_config: dict = {
        "brain_type": "base_brain_instance",
        "brain_id": brain_model.brain_id,
        "fitness": brain_model.fitness,
        "traversed_path": brain_model.traversed_path,
        "fitness_by_step": brain_model.fitness_by_step,
        "current_generation_number": brain_model.current_generation_number,
        "functions_ref": brain_model.functions_ref,
        "functions_callable": brain_model.functions_callable,
        "weights": brain_model.weights,
    }

    brain_config: dict = get_instance_attributes_from_bytes(brain_config=brain_config)

    new_brain_instance: BrainInstance = BrainFactory.make_brain(
        brain_type=brain_config["brain_type"],
        ann_config=brain_config,
    )

    print(new_brain_instance.hidden_layer_activation_func)

    return new_brain_instance


def get_instance_attributes_from_bytes(brain_config: dict) -> dict:
    """
    Convert the attributes back to the origional fromat from bytes
    var: brain_config - config with some attributes in byte format
    rtn: brain_config - config with all attributes in origional format
    """

    brain_config["weights"] = json.loads(brain_config["weights"])
    brain_config["functions_ref"] = json.loads(brain_config["functions_ref"])
    brain_config["functions_callable"] = json.loads(brain_config["functions_callable"])

    print(brain_config["functions_callable"])
    print(type(brain_config["functions_callable"]))
    brain_config["weights"]["hidden_weights"] = np.array(
        brain_config["weights"]["hidden_weights"]
    )
    brain_config["weights"]["output_weights"] = np.array(
        brain_config["weights"]["output_weights"]
    )

    # brain_config["weights"]["hidden_weights"] = np.frombuffer(
    #     brain_config["weights"]["hidden_weights"]
    # ).reshape(24, -1)
    # brain_config["weights"]["output_weights"] = np.frombuffer(
    #     brain_config["weights"]["output_weights"]
    # ).reshape(9, -1)
    brain_config["traversed_path"] = brain_config["traversed_path"].split(",")
    brain_config["fitness_by_step"] = brain_config["fitness_by_step"].split(",")

    return brain_config
