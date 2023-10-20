"""
The generation storage object
"""
from dataclasses import dataclass
from application.lib.agent_brain.brain_factory import BrainInstance


@dataclass
class GenerationObject:
    """
    The gernation object uesed to store the data from each generation
    """

    generation_instance_id: str
    generation_number: int
    average_fitnees: float
    fitness_threshold: float
    generation_alpha_brain: BrainInstance
    generaiton_size: int
    parents_of_generation: list
    learning_instance_ref: str
