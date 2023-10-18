"""Generator for agent"""
from copy import deepcopy
from typing import Generator


from application.lib.agent_brain.brain_factory import BrainFactory

from application.lib.agent.agent_factory import AgentFactory


def new_agent_generator(
    brain_config: dict,
    agent_type: str,
    parents: list,
    max_generation_size: int,
    current_generation_number: int,
    instance_id: str,
    environment: object,
) -> Generator:
    """Test"""
    for instance_in_gen in range(max_generation_size):
        brain_config["current_generation_number"] = current_generation_number

        this_brain_type = "generational_weighted_brain"

        if current_generation_number == 0:
            this_brain_type = "random_weighted_brain"

        brain_id: str = f"B-{instance_id}-{current_generation_number}-{instance_in_gen}"

        agent_brain: object = BrainFactory.make_brain(
            brain_type=this_brain_type,
            brain_config=brain_config,
            parents=parents,
            brain_id=brain_id,
        )

        new_env = deepcopy(environment)

        agent: object = AgentFactory.make_agent(
            agent_type=agent_type, brain=agent_brain, environment=new_env
        )

        yield agent
