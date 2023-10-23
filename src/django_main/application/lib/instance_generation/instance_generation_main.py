"""generate the intances for trainning of the brain"""
import json
from typing import Generator
import uuid

from functools import partial

from application.lib.environment.environment_factory import (
    EnvironmentFactory,
)
from application.lib.agent_brain.static_state_brain import BrainInstance

from application.lib.storage_objects.generation_object import GenerationObject

from application.lib.agent.agent_generator import new_agent_generator

from application.lib.instance_generation.config_formatting import (
    format_instance_config,
    format_brain_config,
    format_env_config,
)

from database.internal_use_db_functions.learning_instance_functions import (
    save_learning_instance,
    update_learning_instance_model_by_id,
)

from database.internal_use_db_functions.generation_instance_functions import (
    save_generation_instance,
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

        self.learning_instance_db_ref = save_learning_instance(self.instance_id)

        self.number_of_generations: int = 0
        self.alpha_brains: list[BrainInstance] = []

    def run_instance(self):
        """run the instance"""
        current_generation_number: int = 0
        # new_fitness_threshold = self.current_fitness_threshold
        new_parents: list[BrainInstance] = []
        current_alpha_brain: BrainInstance = None

        for current_generation_number in range(self.max_number_of_generations):
            new_generation_id: str = (
                f"{self.learning_instance_db_ref}-G{current_generation_number}"
            )
            this_generation_object: GenerationObject = self.new_generation_object(
                current_generation_number=current_generation_number,
                generation_instance_id=new_generation_id,
            )

            this_generation_db_ref = save_generation_instance(
                this_generation_object=this_generation_object,
                learning_instance_referance=self.learning_instance_db_ref,
            )

            new_fitness_threshold = self.generate_new_fitness_threshold(new_parents)

            agent_generator: object = self.get_new_agent_generator(
                new_parents=new_parents,
                current_generation_number=current_generation_number,
                instance_id=self.instance_id,
            )

            new_parents, alpah_brain = self.run_generation(
                agent_generator=agent_generator,
                fitness_threshold=new_fitness_threshold,
                generation_db_ref=this_generation_db_ref,
                current_parents=new_parents,  # naming not good - add current_parents and handle ?
                generation_id=new_generation_id,
            )

            self.alpha_brains.append(alpah_brain)
            self.number_of_generations += 1

            if len(new_parents) <= self.current_generation_failure_threshold:
                break

        # Getting the final from the alpha_brains list is lazy and shit work
        update_learning_instance_model_by_id(self.instance_id, self.alpha_brains[:-1])

        # For logging deco
        return self.brains

    # This will be refactored out
    def new_generation_object(
        self,
        generation_instance_id: str,
        current_generation_number: int,
        new_parents: list[BrainInstance],
    ) -> GenerationObject:
        """
        Create a new generation object with the relervervent data
        """
        return GenerationObject(
            generation_instance_id=generation_instance_id,
            generation_number=current_generation_number,
            average_fitnees=0.0,
            fitness_threshold=self.current_fitness_threshold,
            generation_alpha_brain=None,
            generaiton_size=0,
            parents_of_generation=new_parents,
            learning_instance_ref=self.learning_instance_db_ref,
        )

    def run_generation(
        self,
        agent_generator: Generator,
        fitness_threshold: float,
        generation_db_ref: str,
        generation_id: str,
        current_parents: list[BrainInstance],
    ) -> None:
        """
        Run a new generation
        var: agent_generator
        rtn: new_parents - A list of brain instances tha pass the fitnees threshold
        """
        new_parents: list = []
        all_brains: list[BrainInstance] = []
        alpha_brain: BrainInstance = None

        for agent in agent_generator:
            post_run_agent_brain: object = agent.run_agent()

            # needs to be reworked
            if not alpha_brain:
                alpha_brain = post_run_agent_brain

            self.brains.append(post_run_agent_brain)  # for logging

            if post_run_agent_brain.fitness >= fitness_threshold:
                new_parents.append(post_run_agent_brain)

            # is this faster then a list comp approach ?
            if post_run_agent_brain.fitness >= alpha_brain.fitness:
                alpha_brain = post_run_agent_brain

            save_brain_instance(
                post_run_agent_brain, generation_instance_ref=generation_db_ref
            )

            all_brains.append(post_run_agent_brain)

            if len(new_parents) >= self.new_generation_threshold:
                break

        # can call this in update_generaiton_model_data() ?
        average_fitness: float = self.get_generation_fitness_average(parents=all_brains)

        update_data: dict = {
            "average_fitness": average_fitness,
            "fitness_threshold": fitness_threshold,
            "generation_alpha_brain": alpha_brain,
            "generation_size": len(all_brains),
            "parents_of_generation": current_parents,
        }

        update_generation_model_by_id(
            generation_instace_id=generation_id, update_data=update_data
        )

        return new_parents, alpha_brain

    def update_generaiton_model_data(
        self,
        average_fitness: float,
        fitness_threshold: float,
        generation_alpha_brain: BrainInstance,
        generation_size: int,
        parents_of_generation: list[BrainInstance],
    ) -> None:
        """
        Update the generation models data after the gernation is complete
        """

    # def save_brain_instances() -> None:
    #     """
    #     Save all the brain instances
    #     """

    #     save_brain_instance(
    #             brain_instance=post_run_agent_brain,
    #             generation_instance_ref=generation_db_ref,
    #         )

    # def update_learning_model_data() -> None:
    #     """
    #     Update the learning model data post generation completion
    #     """

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

    def get_generation_fitness_average(self, parents: list[BrainInstance]) -> float:
        """
        Get the average fitness from a given set of brain instances
        var: parents - the set of instances to find the average fitness from
        rtn: The average fitness of the given "parents"

        """

        if not parents:
            return 0.0

        return sum(instance.fitness for instance in parents) / len(parents)

    # This can be refactored down
    def generate_new_fitness_threshold(self, parents: list[object]) -> float:
        """
        Calculate a new fitness threshold based on the average fitness + 10%
        of the given parents fitness
        """

        fitness_average: float = self.get_generation_fitness_average(parents=parents)

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
