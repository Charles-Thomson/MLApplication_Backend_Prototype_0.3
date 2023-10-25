"""Wrapper for the run_generation function in learning instance"""

from functools import wraps
from typing import Callable, Any
import logging.handlers
import logging
import os

# Basic logging config
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(
    level=logging.NOTSET,
)

DEFAULT_FORMAT = "%(levelname)s :: %(funcName)s :: %(message)s"

all_brains_logger = logging.getLogger("all_brain_logger")
filename_all = "logs/generation_logs/all_generation_brains_log.log"

should_roll_over = os.path.isfile(filename_all)

handler_all = logging.handlers.RotatingFileHandler(filename=filename_all, backupCount=3)
if should_roll_over:
    handler_all.doRollover()
formatter = logging.Formatter(DEFAULT_FORMAT)
handler_all.setFormatter(formatter)
all_brains_logger.addHandler(handler_all)
all_brains_logger.propagate = False

fit_brains_logger = logging.getLogger("fit_brain_logger")
filename_fit = "logs/generation_logs/fit_generation_brains_log.log"

should_roll_over = os.path.isfile(filename_fit)

handler_fit = logging.handlers.RotatingFileHandler(filename=filename_fit, backupCount=3)
if should_roll_over:
    handler_fit.doRollover()
formatter = logging.Formatter(DEFAULT_FORMAT)
handler_fit.setFormatter(formatter)
fit_brains_logger.addHandler(handler_fit)
fit_brains_logger.propagate = False


def pre_call(func) -> None:
    """The pre call function in the wrapper"""
    fit_brains_logger.info("New fit generation brains")
    all_brains_logger.info("New Genreation started")


def post_call(func) -> None:
    """The post call function in the wrapper"""
    fit_brains_logger.info("Generation eneded")
    all_brains_logger.info("Generation eneded")


def run_generation_function_wrapper(
    pre_call_function: callable, post_call_function: Callable
) -> callable:
    """Wrapper for the run_generation_function
    Logs the start time and end time of the function
    Logs all the barins from a generation
    Logs the "fit" or "new_parents" from the generation
    """

    def deco(func: [..., Any]) -> callable:
        """Decorator"""

        @wraps(func)
        def wrapper(*args, **kwargs) -> None:
            pre_call_function(func)
            viability, new_parents, all_brains = func(*args, **kwargs)
            for brain in new_parents:
                fit_brains_logger.info(
                    f"generation number: {brain.current_generation_number} - Brain id {brain.brain_id} - Brain fitness {brain.fitness} - Path: {brain.traversed_path}"
                )

            for this_brain in all_brains:
                all_brains_logger.info(
                    f"generation number: {this_brain.current_generation_number} - Brain id {this_brain.brain_id} - Brain fitness {this_brain.fitness} - Path: {this_brain.traversed_path}"
                )

            post_call_function(func)

            return viability, new_parents, all_brains

        return wrapper

    return deco


with_brain_logging = run_generation_function_wrapper(
    pre_call_function=pre_call, post_call_function=post_call
)
