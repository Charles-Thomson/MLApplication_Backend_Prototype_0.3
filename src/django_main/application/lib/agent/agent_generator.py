"""Generator for agent"""
from copy import deepcopy
from typing import Generator


from src.django_main.application.lib.agent_brain.brain_factory import BrainFactory

from src.django_main.application.lib.agent.agent_factory import AgentFactory


def new_agent_generator(
    ann_config: dict,
    agent_type: str,
    parents: list,
    max_generation_size: int,
    current_generation_number: int,
    environment: object,
) -> Generator:
    """Test"""
    for _ in range(max_generation_size):
        this_brain_type = "generational_weighted_brain"

        if current_generation_number == 0:
            this_brain_type = "random_weighted_brain"

        # print(
        #     "in agent generator, gen number: {}, parents: {}".format(
        #         current_generation_number, parents
        #     )
        # )
        agent_brain: object = BrainFactory.make_brain(
            brain_type=this_brain_type,
            ann_config=ann_config,
            parents=parents,
            current_generation_number=current_generation_number,
        )

        new_env = deepcopy(environment)

        agent: object = AgentFactory.make_agent(
            agent_type=agent_type, brain=agent_brain, environment=new_env
        )

        yield agent
