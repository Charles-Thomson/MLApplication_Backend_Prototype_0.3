"""Warapper and logging for the generate new threshold function in learning instance"""

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

fitness_threshold_logger = logging.getLogger("fitness_threshold_logger")
filename = "logs/fitness_threshold_logs/fitness_threshold_log.log"

should_roll_over = os.path.isfile(filename)

handler_all = logging.handlers.RotatingFileHandler(filename=filename, backupCount=3)
if should_roll_over:
    handler_all.doRollover()
formatter = logging.Formatter(DEFAULT_FORMAT)
handler_all.setFormatter(formatter)
fitness_threshold_logger.addHandler(handler_all)
fitness_threshold_logger.propagate = False


def fitness_threshold_generation_function_wrapper(func: [..., Any]) -> callable:
    """Decorator"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> None:
        parents, generation_number = kwargs
        new_fitness_threshold = func(*args, **kwargs)

        fitness_threshold_logger.info(
            f"Generation Number: {generation_number} - Fitness Threshold: {new_fitness_threshold}"
        )

        return new_fitness_threshold

    return wrapper


with_fitness_threshold_logging = fitness_threshold_generation_function_wrapper
