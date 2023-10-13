import numpy as np
from database.models import get_model
import json
from application.lib.agent_brain.static_state_brain import BrainInstance

from application.lib.agent_brain.brain_factory import BrainFactory


def brain_instance_to_model(brain_instance: object, model_type: str) -> BrainInstance:
    """Save the brain instance as a fit instance"""

    model = get_model(model_type=model_type)

    # brain_instance.set_attributes_to_bytes()

    # TODO: refactor this into func ? - clean up ect
    hidden_weights: bytes = brain_instance.hidden_weights.tobytes()
    output_weights: bytes = brain_instance.output_weights.tobytes()
    traversed_path: str = ",".join(str(val) for val in brain_instance.traversed_path)
    fitness_by_step: str = ",".join(str(val) for val in brain_instance.fitness_by_step)
    functions_ref: str = json.dumps(brain_instance.functions_ref)

    new_db_brain_model = model(
        brain_id=brain_instance.brain_id,
        brain_type=brain_instance.brain_type,  # May rename to Model type ?
        current_generation_number=brain_instance.current_generation_number,
        fitness=brain_instance.fitness,
        hidden_weights=hidden_weights,
        output_weights=output_weights,
        traversed_path=traversed_path,
        fitness_by_step=fitness_by_step,
        functions_ref=functions_ref
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
        "functions_callable": {
            "weight_init_huristic": "",
            "hidden_activation_func": "",
            "output_activation_func": "",
            "new_generation_func": "",
        },
        "weights": {
            "hidden_weights": brain_model.hidden_weights,
            "output_weights": brain_model.output_weights,
        },
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

    brain_config["weights"]["hidden_weights"] = np.frombuffer(
        brain_config["weights"]["hidden_weights"]
    ).reshape(24, -1)
    brain_config["weights"]["output_weights"] = np.frombuffer(
        brain_config["weights"]["output_weights"]
    ).reshape(9, -1)
    brain_config["traversed_path"] = brain_config["traversed_path"].split(",")
    brain_config["fitness_by_step"] = brain_config["fitness_by_step"].split(",")
    brain_config["functions_ref"] = json.loads(brain_config["functions_ref"])

    return brain_config
