"""generate the intances for trainning of the brain"""
import json
from typing import Generator
import uuid

from functools import partial


from logging_files.run_time_logging.function_call_time_logging import (
    with_run_time_logging,
)

from logging_files.logging_for_application.generation_function_logging import (
    with_brain_logging,
)

from logging_files.logging_for_application.fitness_threshold_logging import (
    with_fitness_threshold_logging,
)

from logging_files.logging_for_testing.logging_for_testing import (
    debug_logger,
)

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

from database.internal_use_db_functions.learning_instance_functions import (
    new_learning_instance_model,
    update_learning_instance_model_by_id,
)

from database.internal_use_db_functions.generation_instance_functions import (
    new_generation_instance_model,
    update_generation_model_by_id,
)

from database.internal_use_db_functions.brain_instance_functions import (
    save_brain_instance,
)


class LearningInstance:
    """
    The generated instance class
    The running of this instance will result in a "Trained" Brain that can
    then be used on a new environment
    """

    def __init__(
        self, instance_id, agent_generater_partial: object, instance_config: dict
    ):
        self.instance_id: str = f"L:{instance_id}"

        self.current_generation_failure_threshold = 10

        self.agent_generater_partial: callable = agent_generater_partial

        self.max_generation_size: int = instance_config["max_generation_size"]
        self.current_fitness_threshold: float = instance_config["fitness_threshold"]
        self.new_generation_threshold: int = instance_config["new_generation_threshold"]
        self.max_number_of_generations: int = instance_config[
            "max_number_of_genrations"
        ]

        self.learning_instance_db_ref = new_learning_instance_model(
            learning_instance_id=self.instance_id
        )

    @with_run_time_logging
    def run_instance(self) -> None:
        """
        Run the Lenarning instance
        """
        new_parents: list[BrainInstance] = []
        current_alpha_brain: BrainInstance = None
        fitness_threshold: float = self.current_fitness_threshold

        for current_generation_number in range(self.max_number_of_generations):
            new_generation_id: str = (
                f"L:{self.learning_instance_db_ref}-G:{current_generation_number}"
            )

            this_generation_db_ref = new_generation_instance_model(
                generation_instance_id=new_generation_id,
                learning_instance_referance=self.learning_instance_db_ref,
                generation_number=current_generation_number,
                parents_of_generation=new_parents,  # Need to add in on other side
            )

            agent_generator: object = self.agent_generater_partial(
                parents=new_parents,
                max_generation_size=self.max_generation_size,
                current_generation_number=current_generation_number,
                instance_id=self.instance_id,
            )

            generation_viability, alpha_brains_from_generation, _ = self.run_generation(
                agent_generator=agent_generator,
                fitness_threshold=fitness_threshold,
                generation_db_ref=this_generation_db_ref,
                generation_id=new_generation_id,
            )

            potential_new_alpha = alpha_brains_from_generation[0]

            if not current_alpha_brain:
                current_alpha_brain = potential_new_alpha

            elif potential_new_alpha.fitness > current_alpha_brain.fitness:
                current_alpha_brain = potential_new_alpha

            if generation_viability is False:
                debug_logger.info(
                    "BREAK - The generation is not viable due to an inificent number of brains passing the fitness threshold"
                )
                break

            new_parents = alpha_brains_from_generation

            fitness_threshold = self.generate_new_fitness_threshold(
                parents=new_parents, generation_number=current_generation_number
            )

            for brain in alpha_brains_from_generation:
                debug_logger.info(
                    f"Generation number: {brain.current_generation_number} - ID : {brain.brain_id} - Fitness: {brain.fitness} Threshold: {fitness_threshold}"
                )

        update_learning_instance_model_by_id(
            learning_instance_id=self.instance_id,
            new_alpha_brain=current_alpha_brain,
            total_generations=current_generation_number,
        )

        debug_logger.info(
            f"END OF INSTANCE - Generations created: {current_generation_number}"
        )

        debug_logger.info(f"Alpha_brain_fitness =  {current_alpha_brain.fitness}")

    @with_run_time_logging
    @with_brain_logging
    def run_generation(
        self,
        agent_generator: Generator,
        fitness_threshold: float,
        generation_db_ref: str,
        generation_id: str,
    ) -> list[BrainInstance]:
        """
        Run a new generation
        var: agent_generator
        rtn: new_parents - A list of brain instances tha pass the fitnees threshold
        """
        all_brains: list = []
        generation_alphas_brains: list[BrainInstance] = []
        generation_passed_viability: bool = False

        for agent in agent_generator:
            post_run_agent_brain: object = agent.run_agent()

            if post_run_agent_brain.fitness >= fitness_threshold:
                generation_alphas_brains.append(post_run_agent_brain)

            save_brain_instance(
                post_run_agent_brain, generation_instance_db_ref=generation_db_ref
            )

            all_brains.append(post_run_agent_brain)

            if len(generation_alphas_brains) >= self.new_generation_threshold:
                generation_alphas_brains = sorted(
                    generation_alphas_brains, key=lambda x: x.fitness, reverse=True
                )
                generation_passed_viability = True
                return generation_passed_viability, generation_alphas_brains, all_brains

        generation_alphas_brains = sorted(
            all_brains, key=lambda x: x.fitness, reverse=True
        )[:10]

        alpha_brain: BrainInstance = generation_alphas_brains[0]
        update_data: dict = {
            "average_fitness": self.get_generation_fitness_average(parents=all_brains),
            "fitness_threshold": fitness_threshold,
            "generation_alpha_brain": alpha_brain,
            "generation_size": len(all_brains),
        }

        update_generation_model_by_id(
            generation_instance_id=generation_id, update_data=update_data
        )

        return generation_passed_viability, generation_alphas_brains, all_brains

    @with_fitness_threshold_logging
    def generate_new_fitness_threshold(
        self, parents: list[BrainInstance], generation_number: int
    ) -> float:
        """
        Generate a new fitness threshold based on the average fitness of the previous generation plus a percentage
        var: parents - List of brain inatnces from previous generation
        var: generation_number - The current generation
        rtn: new_fitness_threshold - average of perents fitness  plus 10%
        """

        average_fitness: float = self.get_generation_fitness_average(parents=parents)

        return average_fitness + (average_fitness / 100) * 10

    def get_generation_fitness_average(self, parents: list[BrainInstance]) -> float:
        """
        Get the average fitness from a given set of brain instances
        var: parents - the set of instances to find the average fitness from
        rtn: The average fitness of the given "parents"

        """

        if not parents:
            return 0.0

        return sum(instance.fitness for instance in parents) / len(parents)


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

    instance_id: str = generate_instance_id()

    this_instance = LearningInstance(
        instance_id=instance_id,
        agent_generater_partial=agent_generater_partial,
        instance_config=instance_config_formatted,
    )

    return this_instance


def generate_instance_id() -> str:
    """Generate a random brain_ID"""
    brain_id = uuid.uuid4()
    brain_id = str(brain_id)[:10]
    return brain_id
