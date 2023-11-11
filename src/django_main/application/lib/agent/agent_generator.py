"""Generator for agent"""
from copy import deepcopy
from typing import Generator


from application.lib.agent_brain.brain_factory import BrainFactory

from application.lib.agent.agent_factory import AgentFactory


def new_agent_generator(
    parents: list,
    agent_type: str,
    instance_id: str,
    brain_config: dict,
    environment: object,
    max_generation_size: int,
    current_generation_number: int,
) -> Generator:
    """
    Ceate a new agent generator
    var: parents - list of brain instances
    var: agent_type - the type of agent
    var: instance_id - base learning instance ID
    var: brain_config - Configuration of the brain instances
    var: environment - Instance environtment
    var: max_generation_size - Max number of generations
    var: current_generation_number - current generation in the instance
    rtn: generator - Yeilds BrainInstance
    """
    for instance_in_generation in range(max_generation_size):
        brain_config["brain_type"] = "generational_weighted_brain"
        brain_config["current_generation_number"] = current_generation_number

        if current_generation_number == 0:
            brain_config["brain_type"] = "random_weighted_brain"

        brain_config[
            "brain_id"
        ] = f"{instance_id}-{current_generation_number}-{instance_in_generation}"

        agent_brain: object = BrainFactory.make_brain(
            brain_config=brain_config, parents=parents
        )

        agent: object = AgentFactory.make_agent(
            agent_type=agent_type, brain=agent_brain, environment=deepcopy(environment)
        )

        yield agent


def alt_new_agent_generator(
    parents: list,
    agent_type: str,
    instance_id: str,
    brain_config: dict,
    environment: object,
    max_generation_size: int,
    current_generation_number: int,
) -> Generator:
    """
    Ceate a new agent generator
    var: parents - list of brain instances
    var: agent_type - the type of agent
    var: instance_id - base learning instance ID
    var: brain_config - Configuration of the brain instances
    var: environment - Instance environtment
    var: max_generation_size - Max number of generations
    var: current_generation_number - current generation in the instance
    rtn: generator - Yeilds BrainInstance
    """
    for instance_in_generation in range(max_generation_size):
        brain_config["brain_type"] = "generational_weighted_brain"
        brain_config["current_generation_number"] = current_generation_number

        if current_generation_number == 0:
            brain_config["brain_type"] = "random_weighted_brain"

        brain_config[
            "brain_id"
        ] = f"{instance_id}-{current_generation_number}-{instance_in_generation}"

        agent_brain: object = BrainFactory.make_brain(
            brain_config=brain_config, parents=parents
        )

        agent: object = AgentFactory.make_agent(
            agent_type=agent_type, brain=agent_brain, environment=deepcopy(environment)
        )

        post_run_brain = agent.run_agent()

        yield post_run_brain
