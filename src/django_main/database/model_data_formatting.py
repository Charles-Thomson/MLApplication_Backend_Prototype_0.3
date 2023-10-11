from database.models import get_model
from application.lib.agent_brain.static_state_brain import BrainInstance

from application.lib.agent_brain.brain_factory import BrainFactory


def brain_instance_to_model(brain_instance: object, model_type: str) -> BrainInstance:
    """Save the brain instance as a fit instance"""

    model = get_model(model_type=model_type)

    brain_instance.set_attributes_to_bytes()

    new_db_brain_model = model(
        brain_id=brain_instance.brain_id,
        brain_type=brain_instance.brain_type,  # May rename to Model type ?
        current_generation_number=brain_instance.current_generation_number,
        hidden_weights=brain_instance.hidden_weights,
        output_weights=brain_instance.output_weights,
        fitness=brain_instance.fitness,
        traversed_path=brain_instance.traversed_path,
        fitness_by_step=brain_instance.fitness_by_step,
        # svg_path=brain_instance.svg_path,
        # svg_start=brain_instance.svg_start,
        # svg_end=brain_instance.svg_end,
    )

    return new_db_brain_model


def model_to_brain_instance(brain_model) -> BrainInstance:
    """Convert a brain_model used by the DB to a Brain Instance"""

    brain_config: dict = {
        "brain_id": brain_model.brain_id,
        "brain_type": brain_model.brain_type,
        "current_generation_number": brain_model.current_generation_number,
        "hidden_weights": brain_model.hidden_weights,
        "output_weights": brain_model.output_weights,
        "fitness": brain_model.fitness,
        "traversed_path": brain_model.traversed_path,
        "fitness_by_step": brain_model.fitness_by_step,
    }

    new_brain_instance: BrainInstance = BrainFactory.make_brain(
        current_generation_number=0,
        brain_type="generational_weighted_brain",
        ann_config=brain_config,
        parents=[],
    )

    return new_brain_instance
