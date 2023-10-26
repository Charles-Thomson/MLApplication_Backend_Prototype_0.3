"""Testing he new folder creation for logging"""

from datetime import datetime
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

# Issues:
# May have to add the instance ID into each of the logging names to avoid issues with multiple accesses
# Make the loggers Instance_ID plus name and geenration no* if needed
# Make accessing them easier

# Next:
# Add the functunality int a wrapper to be placed on run_instance
# Will need a with_logging var from instance generation
# Instance ID


def new_generation_instance_logger(
    instance_file_path: str, generation_number: int, instance_id: str
) -> logging.Logger:
    """
    Generate a new generation_instance_logger
    var: file path - the file path to the root  logging folder
    """

    new_generation_folder = (
        instance_file_path + "/generation_data/generation_" + str(generation_number)
    )

    if not os.path.exists(new_generation_folder):
        os.makedirs(new_generation_folder)

    new_generation_logger_all_brain_logger = logging.getLogger(
        instance_id + "all_brain_logger" + str(generation_number)
    )
    filename_all_brain = new_generation_folder + "/all_brain_log.log"

    handler_all_brain = logging.FileHandler(filename=filename_all_brain, mode="w")
    formatter = logging.Formatter(DEFAULT_FORMAT)
    handler_all_brain.setFormatter(formatter)
    new_generation_logger_all_brain_logger.addHandler(handler_all_brain)
    new_generation_logger_all_brain_logger.propagate = False

    new_generation_logger_fit_brain_logger = logging.getLogger(
        instance_id + "fit_brain_logger" + str(generation_number)
    )
    filename_fit_brain = new_generation_folder + "/fit_brain_log.log"

    handler_fit_brain = logging.FileHandler(filename=filename_fit_brain, mode="w")
    formatter = logging.Formatter(DEFAULT_FORMAT)
    handler_fit_brain.setFormatter(formatter)
    new_generation_logger_fit_brain_logger.addHandler(handler_fit_brain)
    new_generation_logger_fit_brain_logger.propagate = False


def new_fitness_threshold_logger(
    instance_file_path: str, instance_id: str
) -> logging.Logger:
    """
    Generate a new fitness threshold logger
    var: file path - the file path to the root  logging folder
    """

    fitness_threshold_logger = logging.getLogger(
        instance_id + "fitness_threshold_logger"
    )
    filename_fitness_threshold = (
        instance_file_path + "/fitness_thresholds/fitness_thresholds_log.log"
    )

    handler_all_brain = logging.FileHandler(
        filename=filename_fitness_threshold, mode="w"
    )
    formatter = logging.Formatter(DEFAULT_FORMAT)
    handler_all_brain.setFormatter(formatter)
    fitness_threshold_logger.addHandler(handler_all_brain)
    fitness_threshold_logger.propagate = False


def new_run_time_logger(instance_file_path: str, instance_id: str) -> logging.Logger:
    """
    Generate a new run time logger
    var: file path - the file path to the root  logging folder
    """

    run_time_logger = logging.getLogger(instance_id + "run_time_logger")
    filename_run_time = instance_file_path + "/run_time/run_time_log.log"

    handler_run_time = logging.FileHandler(filename=filename_run_time, mode="w")
    formatter = logging.Formatter(DEFAULT_FORMAT)
    handler_run_time.setFormatter(formatter)
    run_time_logger.addHandler(handler_run_time)
    run_time_logger.propagate = False


def generate_new_logging_file(new_instance_id: str) -> str:
    """
    Generate a new logging file based of the instance ID
    This will return the file name to be passed and used by other loggers
    Or - use get logger ?

    # returning the file path to the insance loging base
    """
    logging_path_root = "src/django_main/logs/instance_data/" + new_instance_id

    if not os.path.exists(logging_path_root):
        os.makedirs(logging_path_root)

    directroys: list[str] = ["/generation_data", "/fitness_thresholds", "/run_time"]

    for directroy in directroys:
        full_file_path: str = logging_path_root + directroy
        if not os.path.exists(full_file_path):
            os.makedirs(full_file_path)

    return logging_path_root


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
    print("In post call")

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
                this_logging_root_file_path,
                instance.with_logging,
                instance.instance_id,
            )
            post_run_function(func, instance.instance_id)

        return wrapper

    return deco


def run_generation_function_pre_call(func, *args, **kwargs) -> None:
    """
    Pre call function in for the run_instance wrapper
    This will set up the logging if needed
    """

    instance_id = kwargs["instance_id"]

    if kwargs["with_logging"]:
        run_time_logger = logging.getLogger(instance_id + "run_time_logger")

        time = datetime.now().time().strftime("%H:%M:%S")
        run_time_logger.info(f"{func.__name__} called at - {time}")


def post_generation_call(func, instance_id):
    print("In post call")

    run_time_logger = logging.getLogger(instance_id + "run_time_logger")

    time = datetime.now().time().strftime("%H:%M:%S")
    run_time_logger.info(f"{func.__name__} called at - {time} - 2nd gen")


def run_generation_function_wrapper(
    pre_run_function: Callable, post_run_function: Callable
) -> Callable:
    """
    Logging wrapper for the run_generation
    This will set up the logging folders if needed
    """

    def deco(func: [..., Any]) -> Callable:
        """Decorator"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            pre_run_function(func, *args, **kwargs)
            # need a new generation logger here
            print(args)
            print(kwargs)

            new_generation_instance_logger(
                kwargs["instance_file_path"],
                kwargs["generation_number"],
                kwargs["instance_id"],
            )

            all_brains_logger = logging.getLogger(
                kwargs["instance_id"] + "all_brain_logger" + kwargs["generation_number"]
            )
            fit_brains_logger = logging.getLogger(
                kwargs["instance_id"] + "fit_brain_logger" + kwargs["generation_number"]
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

            post_run_function(func, kwargs["instance_id"])

        return wrapper

    return deco


def fitness_threshold_function_pre_call() -> None:
    """
    Pre call function in for the run_instance wrapper
    This will set up the logging if needed
    """

    print("fintess threshold pre run func")


def post_fitness_logging_call():
    print("In post call")

    print("post call fitness threhsold logging")


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
        def wrapper(*args, **kwargs):
            pre_run_function()
            new_fitness_threshold = func(*args, **kwargs)

            if kwargs["with_logging"]:
                new_fitness_threshold_logger(
                    kwargs["instance_file_path"], kwargs["instance_id"]
                )
                fitness_threshold_logger = logging.getLogger(
                    kwargs["instance_id"] + "fitness_threshold_logger"
                )
                fitness_threshold_logger.info(
                    f"Generation Number: {kwargs['generation_number']} - Fitness Threshold: {new_fitness_threshold}"
                )
            post_run_function()

        return wrapper

    return deco


with_logging_test_run_instance = run_instance_function_wrapper(
    pre_run_function=run_instance_function_pre_call, post_run_function=post_call
)

with_logging_test_run_generation = run_generation_function_wrapper(
    pre_run_function=run_generation_function_pre_call,
    post_run_function=post_generation_call,
)

with_logging_test_generate_new_fitness_threshold = fitness_threshold_function_wrapper(
    pre_run_function=fitness_threshold_function_pre_call,
    post_run_function=post_fitness_logging_call,
)


# @with_logging
# def test_wrapped_function(
#     logging_root_file_path: str,
#     with_logging,
#     instance_id,
# ):
#     """test wrapped function"""
#     print("In the wrapped function")

#     if logging_root_file_path:
#         print(logging_root_file_path)


# test_wrapped_function(
#     logging_root_file_path="", with_logging=True, instance_id="test_id_wrapper_3"
# )
