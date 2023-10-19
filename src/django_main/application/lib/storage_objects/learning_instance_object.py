"""Learning instance object"""

from dataclasses import dataclass
from application.lib.agent_brain.brain_factory import BrainInstance


@dataclass
class LearningInstanceObject:
    """
    The stroge object from the learning instance
    """

    id: int
    learning_instance_id: str
    alpha_brain_from_instance: BrainInstance
    number_of_generaitions: int
