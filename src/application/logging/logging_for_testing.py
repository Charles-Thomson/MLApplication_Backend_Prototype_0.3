"""Basic logging imports"""
import logging.handlers
import os
import numpy as np
from math import sqrt
from functools import wraps
from typing import Any, Callable
import logging

# Basic logging config
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(
    level=logging.NOTSET,
)

DEFAULT_FORMAT = "%(levelname)s :: %(funcName)s :: %(message)s"

new_logger = logging.getLogger()
filename = "src/application/tests/test_logging_files/brain_logging.log"


should_roll_over = os.path.isfile(filename)

handler = logging.handlers.RotatingFileHandler(filename=filename, backupCount=3)
if should_roll_over:
    handler.doRollover()
formatter = logging.Formatter(DEFAULT_FORMAT)
handler.setFormatter(formatter)
new_logger.addHandler(handler)
new_logger.propagate = False


def logger_test_brains_logging(func: Callable[..., Any]) -> Any:
    """Testing the logging for test brains"""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        brains, this_maze = func(*args)
        formatted_maze = np.fromstring(this_maze, dtype=int, sep=",")
        resize_value = int(sqrt(len(formatted_maze)))
        formatted_maze = formatted_maze.reshape(resize_value, -1)
        new_logger.info(f"Maze:  \n {formatted_maze}")

        for brain in brains:
            new_logger.info(
                f"Brain: {brain.brain_id} - Generation: {brain.current_generation_number} Fitness: {brain.fitness} Path: {brain.traversed_path}"
            )
            # Path: {brain.traversed_path}

    return wrapper


with_test_brian_logging = logger_test_brains_logging
