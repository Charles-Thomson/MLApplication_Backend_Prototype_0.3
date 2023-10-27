"""Functions related to the decorator for the run_instance function in a Learning instance"""
from datetime import datetime
from functools import wraps
from typing import Any, Callable
import logging

from logging_files.decorator_logging.loggers.logger_generation import (
    new_run_time_logger,
)

from logging_files.decorator_logging.directory_generation import (
    generate_new_logging_file,
)


def run_instance_function_pre_call(func, *args, **kwargs) -> None:
    """
    Pre call function in for the run_instance wrapper
    This will set up the logging if needed
    """
    instance = args[0]

    if instance.with_logging:
        logging_root_file_path: str = generate_new_logging_file(
            new_instance_id=instance.instance_id
        )
        new_run_time_logger(
            instance_file_path=logging_root_file_path, instance_id=instance.instance_id
        )
        run_time_logger = logging.getLogger(instance.instance_id + "run_time_logger")

        time = datetime.now().time().strftime("%H:%M:%S")
        run_time_logger.info(f"{func.__name__} called at - {time}")

        return logging_root_file_path


def post_call(func, instance_id):
    run_time_logger = logging.getLogger(instance_id + "run_time_logger")

    time = datetime.now().time().strftime("%H:%M:%S")
    run_time_logger.info(f"{func.__name__} called at - {time} - 2nd gen")


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
            this_logging_root_file_path = pre_run_function(func, *args, **kwargs)
            instance = args[0]
            func(
                instance,
                instance.with_logging,
                this_logging_root_file_path,
                instance.instance_id,
            )
            post_run_function(func, instance.instance_id)

        return wrapper

    return deco


with_logging_test_run_instance = run_instance_function_wrapper(
    pre_run_function=run_instance_function_pre_call, post_run_function=post_call
)
