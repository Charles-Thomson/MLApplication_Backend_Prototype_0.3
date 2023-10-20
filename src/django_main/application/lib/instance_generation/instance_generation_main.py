"""generate the intances for trainning of the brain"""
import json
from typing import Generator
import uuid

from functools import partial

from application.lib.environment.environment_factory import (
    EnvironmentFactory,
)
from application.lib.agent_brain.static_state_brain import BrainInstance

from application.lib.agent.agent_generator import new_agent_generator

from application.lib.instance_generation.config_formatting import (
    format_instance_config,
    format_brain_config,
    format_env_config,
)

# from database.db_functions import save_learning_instance

# from django_main.logging_files.logging_decos import with_fitness_threshold_logging


class LearningInstance:
    """
    The generated instance class
    The running of this instance will result in a "Trained" Brain that can
    then be used on a new environment
    """

    def __init__(self, id, agent_generater_partial: object, instance_config: dict):
        self.instance_id: str = id

        self.current_fitness_threshold: float = instance_config["fitness_threshold"]
        self.current_generation_failure_threshold = 2

        self.max_number_of_generations: int = instance_config[
            "max_number_of_genrations"
        ]

        self.max_generation_size: int = instance_config["max_generation_size"]
        self.agent_generater_partial: callable = (
            agent_generater_partial  # add an id peram here ?
        )

        # self.current_parents: list[BrainInstance] = []

        self.new_generation_threshold: int = instance_config["new_generation_threshold"]

        self.brains: list[BrainInstance] = []

        # the highest fitness brain from the whole instance
        self.alpha_brain: BrainInstance = object

        # learning_instance_db_ref = save_learning_instance(self.instance_id)

    def run_instance(self):
        """run the instance"""
        current_generation_number: int = 0
        # new_fitness_threshold = self.current_fitness_threshold
        new_parents: list[BrainInstance] = []

        for current_generation_number in range(self.max_number_of_generations):
            new_fitness_threshold = self.generate_new_fitness_threshold(new_parents)

            agent_generator: object = self.get_new_agent_generator(
                new_parents=new_parents,
                current_generation_number=current_generation_number,
                instance_id=self.instance_id,
            )

            new_parents = self.run_generation(
                agent_generator=agent_generator,
                fitness_threshold=new_fitness_threshold,
            )

            # if new_parents:
            #     save_full_generation(
            #         generation_id=f"G-{self.instance_id}-{current_generation_number}",
            #         generation_brain_instances=new_parents,
            #         fitness_threshold=self.current_fitness_threshold,
            #         generation_number=current_generation_number,
            #     )
            if len(new_parents) <= self.current_generation_failure_threshold:
                break

        # For logging deco
        return self.brains

    def run_generation(
        self, agent_generator: Generator, fitness_threshold: float
    ) -> None:
        """
        Run a new generation
        var: agent_generator
        rtn: new_parents - A list of brain instances tha pass the fitnees threshold
        """
        new_parents: list = []
        brain_storage: list[BrainInstance] = []

        for agent in agent_generator:
            post_run_agent_brain: object = agent.run_agent()

            self.brains.append(post_run_agent_brain)  # for logging

            if post_run_agent_brain.fitness >= fitness_threshold:
                new_parents.append(post_run_agent_brain)

            if post_run_agent_brain.fitness >= self.alpha_brain.fitness:
                self.alpha_brain = post_run_agent_brain

            brain_storage.append(post_run_agent_brain)

            if len(new_parents) >= self.new_generation_threshold:
                break

        return new_parents

    # cuurently pulled ti a func for tests - needed ?
    def get_new_agent_generator(
        self, new_parents: list, current_generation_number: int, instance_id: str
    ) -> Generator:
        """Create a new agenet generator
        var: Parents - Parnets for the new generation
        var: current_generation_number - the current generation
        rtn: Agent generator
        """

        return self.agent_generater_partial(
            parents=new_parents,
            max_generation_size=self.max_generation_size,
            current_generation_number=current_generation_number,
            instance_id=instance_id,
        )

    def generate_new_fitness_threshold(self, parents: list[object]) -> float:
        """
        Calculate a new fitness threshold based on the average fitness + 10%
        of the given parents fitness
        """

        if not parents:
            return 2.0

        fitness_average: float = sum(instance.fitness for instance in parents) / len(
            parents
        )

        # * 10 -> inc threshold by 10%
        return fitness_average + (fitness_average / 100) * 10


def new_instance(config: json) -> LearningInstance:
    """Generate a new instance based on the given config settings
    var: config - the given config settings as json
    rtn: Callable object
    """

    env_config: dict = format_env_config(config["env_config"])

    brain_config_formatted: dict = format_brain_config(config["brain_config"])

    instance_config_formatted: dict = format_instance_config(config["instance_config"])

    environment: object = EnvironmentFactory.make_env(
        env_type=config["env_type"], config=env_config
    )

    agent_generater_partial: callable = partial(
        new_agent_generator,
        brain_config=brain_config_formatted,
        agent_type=config["agent_type"],
        environment=environment,
    )

    id: str = generate_instance_id()

    this_instance = LearningInstance(
        id=id,
        agent_generater_partial=agent_generater_partial,
        instance_config=instance_config_formatted,
    )

    return this_instance


def generate_instance_id() -> str:
    """Generate a random brain_ID"""
    brain_id = uuid.uuid4()
    brain_id = str(brain_id)[:10]
    return brain_id
