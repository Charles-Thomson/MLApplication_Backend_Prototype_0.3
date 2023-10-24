"""The internal functions relating to the brain_instance DB operations"""
from django.db import models

from database.models import BrainInstanceModel
from database.data_modeling.brain_instance_modeling import (
    brain_instance_to_model,
    brain_model_to_instance,
)

from application.lib.agent_brain.static_state_brain import BrainInstance


def save_brain_instance(
    brain_instance: BrainInstance, generation_instance_db_ref: str
) -> None:
    """Save the given Brain Instance to the Django DB"""

    new_brain_instance_as_model: models.Model = brain_instance_to_model(
        brain_instance, generation_instance_db_ref
    )

    new_brain_instance_as_model.save()


def get_brain_instance_by_id(brain_id: str) -> None:
    """Get a brain Instance by brain instance id"""

    brain_model: BrainInstanceModel = BrainInstanceModel.objects.get(brain_id=brain_id)

    rtn_brain_instance = brain_model_to_instance(brain_model)

    return rtn_brain_instance


def get_brain_instance_by_forign_key(this_generation_instance_ref: str) -> None:
    """Get a brain Instance by generation ref - FK"""

    brain_model: BrainInstanceModel = BrainInstanceModel.objects.get(
        generation_instance_ref=this_generation_instance_ref
    )

    rtn_brain_instance = brain_model_to_instance(brain_model)

    return rtn_brain_instance


def get_brain_model_by_id(brain_instance_id: str) -> None:
    """Get a brain model by brain instance id"""

    brain_model: BrainInstanceModel = BrainInstanceModel.objects.get(
        brain_instance_id=brain_instance_id
    )

    rtn_brain_instance = brain_model_to_instance(brain_model)

    return rtn_brain_instance


def get_brain_model_by_forign_key(this_generation_instance_ref: str) -> None:
    """Get a brain model by generation reference - FK"""

    brain_model: BrainInstanceModel = BrainInstanceModel.objects.get(
        generation_instance_ref=this_generation_instance_ref
    )

    return brain_model
