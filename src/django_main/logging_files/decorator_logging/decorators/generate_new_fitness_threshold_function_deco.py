"""Functions related to the decorator for the generate_new_fitness_threshold function in a Learning instance"""
from functools import wraps
from typing import Any, Callable
import logging

from logging_files.decorator_logging.loggers.logger_generation import (
    new_fitness_threshold_logger,
)


def fitness_threshold_function_pre_call() -> None:
    """
    Pre call function in for the run_instance wrapper
    This will set up the logging if needed
    """


def post_fitness_logging_call():
    """Place holder"""


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
            pre_run_function()
            new_fitness_threshold = func(*args, **kwargs)

            if with_logging:
                new_fitness_threshold_logger(logging_root_file_path, instance_id)
                fitness_threshold_logger = logging.getLogger(
                    instance_id + "fitness_threshold_logger"
                )
                fitness_threshold_logger.info(
                    f"Generation Number: {generation_number} - Fitness Threshold: {new_fitness_threshold}"
                )
            post_run_function()

            return new_fitness_threshold

        return wrapper

    return deco


with_logging_test_generate_new_fitness_threshold = fitness_threshold_function_wrapper(
    pre_run_function=fitness_threshold_function_pre_call,
    post_run_function=post_fitness_logging_call,
)
