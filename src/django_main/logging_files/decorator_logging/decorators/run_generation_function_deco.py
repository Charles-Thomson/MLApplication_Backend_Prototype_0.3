"""Functions related to the decorator for the run_generation function in a Learning instance"""
from datetime import datetime
from functools import wraps
from typing import Any, Callable
import logging

from functools import partial


from logging_files.decorator_logging.loggers.logger_generation import (
    new_generation_instance_logger,
)


# this approach can work
def non_deco_logging(
    func, logging_root_file_path, instance_id, generation_number, **kwargs
):
    """Testing a none deco version of logging"""

    print("in the deco")
    a, b, c = func(**kwargs)

    print(b)

    return a


def run_generation_function_pre_call(
    func, instance_id: str, with_logging: bool
) -> None:
    """
    Pre call function in for the run_instance wrapper
    This will set up the logging if needed
    """
    if with_logging:
        run_time_logger = logging.getLogger(instance_id + "run_time_logger")

        time = datetime.now().time().strftime("%H:%M:%S")
        run_time_logger.info(f"{func.__name__} called at - {time}")


def run_generation_function_post_call(func, instance_id):
    run_time_logger = logging.getLogger(instance_id + "run_time_logger")

    time = datetime.now().time().strftime("%H:%M:%S")
    run_time_logger.info(f"{func.__name__} called at - {time} - 2nd gen")


# Make the deco take functions which are in the instance ?
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
            pre_run_function(func, instance_id, with_logging)
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


with_generation_data_logging = run_generation_function_wrapper(
    pre_run_function=run_generation_function_pre_call,
    post_run_function=run_generation_function_post_call,
)
