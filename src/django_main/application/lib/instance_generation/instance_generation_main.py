"""generate the intances for trainning of the brain"""
import json
from typing import Generator

from functools import partial

from logging_files.decorator_logging.decorators.logging_decorators import (
    run_instance_with_logging,
    alt_run_generation_with_logging,
    generate_fitness_threshold_with_logging,
)

from application.lib.config_generation.generate_config_data import (
    generate_instance_configuration_data,
)

from application.lib.environment.environment_factory import (
    EnvironmentFactory,
)
from application.lib.agent_brain.static_state_brain import BrainInstance

from application.lib.agent.agent_generator import (
    new_agent_generator,
    alt_new_agent_generator,
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
        self,
        instance_id: str,
        agent_generater_partial: object,
        alt_agent_generator: object,
        hyper_perameters: dict,
        with_logging: bool,
    ):
        self.instance_id = instance_id
        self.with_logging = with_logging
        self.agent_generater_partial: callable = agent_generater_partial
        self.alt_agent_generator: callable = alt_agent_generator
        self.max_generation_size: int = hyper_perameters["max_generation_size"]
        self.current_fitness_threshold: float = hyper_perameters["fitness_threshold"]

        self.current_generation_failure_threshold = hyper_perameters[
            "generation_failure_threshold"
        ]
        self.new_generation_threshold: int = hyper_perameters[
            "new_generation_threshold"
        ]
        self.max_number_of_generations: int = hyper_perameters[
            "max_number_of_genrations"
        ]

        self.learning_instance_db_ref = new_learning_instance_model(
            learning_instance_id=self.instance_id
        )

    @run_instance_with_logging
    def run_instance(self, logging_root_file_path=None, **kwargs) -> None:
        """
        Run the Lenarning instance
        """
        alpha_brains_from_generation: list[BrainInstance] = []
        current_alpha_brain: BrainInstance = None
        fitness_threshold: float = self.current_fitness_threshold

        for current_generation_number in range(self.max_number_of_generations):
            new_generation_id: str = f"{self.instance_id}-{current_generation_number}"

            alt_agent_generator = self.alt_agent_generator(
                instance_id=self.instance_id,
                parents=alpha_brains_from_generation,
                max_generation_size=self.max_generation_size,
                current_generation_number=current_generation_number,
            )

            this_generation_db_ref = new_generation_instance_model(
                generation_instance_id=new_generation_id,
                generation_number=current_generation_number,
                parents_of_generation=alpha_brains_from_generation,
                learning_instance_referance=self.learning_instance_db_ref,
            )

            (
                avg_fitness,
                alpha_brains_from_generation,
                sorted_brains,
                generation_viability,
            ) = self.alt_run_generation(
                instance_id=self.instance_id,
                with_logging=self.with_logging,
                agent_generator=alt_agent_generator,
                generation_id=new_generation_id,
                fitness_threshold=fitness_threshold,
                generation_db_ref=this_generation_db_ref,
                generation_number=current_generation_number,
                logging_root_file_path=logging_root_file_path,
            )

            potential_new_alpha = alpha_brains_from_generation[0]

            update_generation_model_by_id(
                generation_size=len(sorted_brains),
                fitness_threshold=fitness_threshold,
                generation_instance_id=new_generation_id,
                generation_alpha_brain=potential_new_alpha,
                average_fitness=avg_fitness,
            )

            if not current_alpha_brain:
                current_alpha_brain = potential_new_alpha

            elif potential_new_alpha.fitness > current_alpha_brain.fitness:
                current_alpha_brain = potential_new_alpha

            if generation_viability is False:
                break

            fitness_threshold = self.generate_new_fitness_threshold(
                instance_id=self.instance_id,
                with_logging=self.with_logging,
                parents=alpha_brains_from_generation,
                generation_number=current_generation_number,
            )

        update_learning_instance_model_by_id(
            new_alpha_brain=current_alpha_brain,
            learning_instance_id=self.instance_id,
            total_generations=current_generation_number,
        )

    @alt_run_generation_with_logging
    def alt_run_generation(
        self,
        agent_generator: Generator,
        fitness_threshold: float,
        generation_db_ref: str,
        **kwargs,
    ) -> list[BrainInstance]:
        """
        Run the generation
        """
        valid_generation = False
        all_brains_post_run = [agent for agent in agent_generator]

        sorted_brains = sorted(
            all_brains_post_run, key=lambda x: x.fitness, reverse=True
        )

        if sorted_brains[10].fitness >= fitness_threshold:
            valid_generation = True

        avg_fitness: float = self.get_generation_fitness_average(
            parents=all_brains_post_run
        )

        partial_save = partial(
            save_brain_instance, generation_instance_db_ref=generation_db_ref
        )
        map(partial_save, all_brains_post_run)
        return avg_fitness, sorted_brains[:10], sorted_brains, valid_generation

    @generate_fitness_threshold_with_logging
    def generate_new_fitness_threshold(
        self,
        parents: list[BrainInstance],
        **kwargs,
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


def new_instance(input_config: json) -> LearningInstance:
    """Generate a new instance based on the given config settings
    var: config - the given config settings as json
    rtn: Callable object
    """

    formatted_config: dict = generate_instance_configuration_data(
        input_config=input_config
    )

    environment: object = EnvironmentFactory.make_env(
        env_type=formatted_config["env_type"],
        map_data=formatted_config["map_data"],
    )

    agent_generater_partial: callable = partial(
        new_agent_generator,
        brain_config=formatted_config["brain_config"],
        agent_type=formatted_config["agent_type"],
        environment=environment,
    )

    alt_generator: callable = partial(
        alt_new_agent_generator,
        brain_config=formatted_config["brain_config"],
        agent_type=formatted_config["agent_type"],
        environment=environment,
    )

    this_instance = LearningInstance(
        instance_id=formatted_config["instance_id"],
        agent_generater_partial=agent_generater_partial,
        alt_agent_generator=alt_generator,
        hyper_perameters=formatted_config["hyper_perameters"],
        with_logging=True,
    )

    return this_instance
