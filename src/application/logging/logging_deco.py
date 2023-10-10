"""The decorator for logging"""
from functools import wraps
from typing import Any, Callable
import logging

# Basic logging config
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(
    level=logging.NOTSET,
)

DEFAULT_FORMAT = "%(levelname)s :: %(funcName)s :: %(message)s"


def generate_logger(name: __name__, log_file: str, formatting: str = DEFAULT_FORMAT):
    """Generat a custom logger"""

    new_logger = logging.getLogger(name)
    filename = "application/ann/logging_files/" + log_file
    handler = logging.FileHandler(filename=filename, mode="w")
    formatter = logging.Formatter(formatting)
    handler.setFormatter(formatter)
    new_logger.addHandler(handler)
    new_logger.propagate = False

    return new_logger


brains_log = generate_logger(__name__ + "brain_logger", "brain_logger.log")
fitness_log = generate_logger(__name__ + "fitness_logger", "fitness_logger.log")

fitness_threshold_log = generate_logger(
    __name__ + "fitness_threshold_logger", "fitness_threshold_logger.log"
)


def brain_logger(func: Callable[..., Any]):
    """Basic logger deco for logging brain data"""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        brains = func(*args)
        for brain in brains:
            brains_log.info(
                f"Brain: {brain.brain_id} - Generation: {brain.current_generation_number} Path: {brain.traversed_path} Fitness: {brain.fitness}"
            )
            fitness_log.info(
                f"Brain: {brain.brain_id} - Generation: {brain.current_generation_number} Fitness: {brain.fitness}"
            )

    return wrapper


def fitness_threshold_logger(func: Callable[..., Any]):
    """Logging Deco for the fitness threshold"""

    @wraps(func)
    def wrapper(*args: Any) -> Any:
        fitness_threshold = func(*args)
        fitness_threshold_log.info(f"Current Fitness Threshold: {fitness_threshold}")
        return fitness_threshold

    return wrapper


with_brain_logging = brain_logger
with_fitness_threshold_logging = fitness_threshold_logger
