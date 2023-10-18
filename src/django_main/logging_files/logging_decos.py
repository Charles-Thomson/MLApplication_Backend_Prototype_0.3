"""The decorator for logging"""
from functools import wraps
from typing import Any, Callable
import logging

# Basic logging config
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

DEFAULT_FORMAT = "%(levelname)s :: %(funcName)s :: %(message)s"


def generate_logger(name: __name__, log_file: str, formatting: str = DEFAULT_FORMAT):
    """Generat a custom logger"""
    new_logger = logging.getLogger(name)
    filename = "logging_files/logs/" + log_file
    handler = logging.FileHandler(filename=filename, mode="w")
    formatter = logging.Formatter(formatting)
    handler.setFormatter(formatter)
    new_logger.addHandler(handler)
    new_logger.propagate = False

    return new_logger


save_generation_log = generate_logger(
    __name__ + "save_generation_logger", "saved_generations.log"
)


def save_generation_logging(func: Callable[..., Any]):
    """
    Logging deco for the saving of generation models
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        generation_data = func(**kwargs)

        save_generation_log.info(
            f"ID: {generation_data['generation_id']} - Gen*No: {generation_data['generation_number']} - Fitness Threshold {generation_data['fitness_threshold']} - Average Fitness: {generation_data['average_fitness']}"
        )

    return wrapper


with_save_generation_logging = save_generation_logging
