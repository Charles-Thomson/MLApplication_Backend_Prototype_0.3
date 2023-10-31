"""Decorators for the purpose of logging

This file can be refactored down using factories
Protocols can also be implemented for the wrapper functions ?
"""
from datetime import datetime
from functools import wraps
import logging
from typing import Any, Callable
from logging_files.decorator_logging.loggers.logger_generation import (
    new_generation_instance_logger,
)
from logging_files.decorator_logging.loggers.logger_generation import (
    new_run_time_logger,
)
from logging_files.decorator_logging.loggers.logger_generation import (
    new_fitness_threshold_logger,
)

from logging_files.decorator_logging.directory_generation import (
    generate_new_logging_file,
)


def run_time_logging_pre_call_function(func: Callable, instance_id: str) -> None:
    """
    Pre call function
    Used to log the run time of a function
    """

    run_time_logger = logging.getLogger(instance_id + "run_time_logger")

    time = datetime.now().time().strftime("%H:%M:%S")
    run_time_logger.info(f"{func.__name__} called at - {time}")


def run_time_loging_post_call_function(func: callable, instance_id: str):
    """
    Post call function
    Used to log the run time of a function
    """
    run_time_logger = logging.getLogger(instance_id + "run_time_logger")

    time = datetime.now().time().strftime("%H:%M:%S")
    run_time_logger.info(f"{func.__name__} completed at - {time}")


def run_instance_function_wrapper(
    pre_run_function: Callable, post_run_function: Callable
) -> Callable:
    """
    Logging wrapper for the run_instace_function
    This will set up the logging folders if needed
    """

    def deco(func: [..., Any]) -> Callable:
        """Decorator"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            instance = args[0]

            if not instance.with_logging:
                func(*args, logging_root_file_path="", **kwargs)
            else:
                logging_root_file_path: str = generate_new_logging_file(
                    new_instance_id=instance.instance_id
                )

                # TODO: This generation approach can be refactored down ?
                new_run_time_logger(
                    instance_file_path=logging_root_file_path,
                    instance_id=instance.instance_id,
                )
                new_fitness_threshold_logger(
                    logging_root_file_path, instance.instance_id
                )
                pre_run_function(func, instance.instance_id)

                func(*args, logging_root_file_path, **kwargs)

                post_run_function(func, instance.instance_id)

        return wrapper

    return deco


def run_generation_function_wrapper(
    pre_run_function: Callable,
    post_run_function: Callable,
) -> Callable:
    """
    Logging wrapper for the run_generation
    This will set up the logging folders if needed
    """

    def deco(func: Callable) -> Callable:
        """Decorator"""

        @wraps(func)
        def wrapper(
            *args,
            logging_root_file_path,
            instance_id,
            with_logging,
            generation_number,
            **kwargs,
        ):
            if not with_logging:
                return func(*args, **kwargs)

            pre_run_function(func, instance_id)
            new_generation_instance_logger(
                instance_file_path=logging_root_file_path,
                generation_number=generation_number,
                instance_id=instance_id,
            )

            all_brains_logger = logging.getLogger(
                instance_id + "all_brain_logger" + str(generation_number)
            )
            fit_brains_logger = logging.getLogger(
                instance_id + "alpha_brain_logger" + str(generation_number)
            )

            # log these in a second
            generation_passed_viability, generation_alphas_brains, all_brains = func(
                *args, **kwargs
            )

            for brain in generation_alphas_brains:
                fit_brains_logger.info(
                    f"generation number: {brain.current_generation_number} - Brain id {brain.brain_id} - Brain fitness {brain.fitness} - Path: {brain.traversed_path}"
                )

            for this_brain in all_brains:
                all_brains_logger.info(
                    f"generation number: {this_brain.current_generation_number} - Brain id {this_brain.brain_id} - Brain fitness {this_brain.fitness} - Path: {this_brain.traversed_path}"
                )

            post_run_function(func, instance_id)

            return generation_passed_viability, generation_alphas_brains, all_brains

        return wrapper

    return deco


def fitness_threshold_function_wrapper(
    pre_run_function: Callable, post_run_function: Callable
) -> Callable:
    """
    Logging wrapper for the generate new fitness threshold
    This will set up the logging folders if needed
    """

    def deco(func: [..., Any]) -> Callable:
        """Decorator"""

        @wraps(func)
        def wrapper(
            *args,
            logging_root_file_path,
            instance_id,
            with_logging,
            generation_number,
            **kwargs,
        ):
            if not with_logging:
                new_fitness_threshold = func(*args, **kwargs)
                return new_fitness_threshold

            pre_run_function(func, instance_id)
            new_fitness_threshold = func(*args, **kwargs)

            fitness_threshold_logger = logging.getLogger(
                instance_id + "fitness_threshold_logger"
            )
            fitness_threshold_logger.info(
                f"Generation Number: {generation_number} - Fitness Threshold: {new_fitness_threshold}"
            )
            post_run_function(func, instance_id)

            return new_fitness_threshold

        return wrapper

    return deco


run_instance_with_logging = run_instance_function_wrapper(
    pre_run_function=run_time_logging_pre_call_function,
    post_run_function=run_time_loging_post_call_function,
)

run_generation_with_logging = run_generation_function_wrapper(
    pre_run_function=run_time_logging_pre_call_function,
    post_run_function=run_time_loging_post_call_function,
)

generate_fitness_threshold_with_logging = fitness_threshold_function_wrapper(
    pre_run_function=run_time_logging_pre_call_function,
    post_run_function=run_time_loging_post_call_function,
)
