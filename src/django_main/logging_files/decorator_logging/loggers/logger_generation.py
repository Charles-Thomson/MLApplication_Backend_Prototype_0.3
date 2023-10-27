"""Generating the loggers used in the decorator based logging system"""
import logging.handlers
import logging
import os
from logging_files.generate_logger import generate_logger


# Basic logging config
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(
    level=logging.NOTSET,
)


def new_generation_instance_logger(
    instance_file_path: str, generation_number: int, instance_id: str
) -> None:
    """
    Generate a logger for a new generation in the learning insatnce
    Logger created using referance to the base learning instance & generation number

    var: instance_file_path - file path to root logging folder for instance
    var: generation_number - the generation number of the new generation
    var: instance_id - The id of the learning instance the generation belongs to

    """

    new_generation_file_path = (
        instance_file_path + "/generation_data/generation_" + str(generation_number)
    )

    if not os.path.exists(new_generation_file_path):
        os.makedirs(new_generation_file_path)

    ref_names: str = ["alpha_brain", "all_brain"]

    for name in ref_names:
        logger_name: str = instance_id + name + "_logger" + str(generation_number)
        file_path: str = new_generation_file_path + "/" + name + "_log"
        generate_logger(logger_name=logger_name, file_path=file_path)


def new_fitness_threshold_logger(instance_file_path: str, instance_id: str) -> None:
    """
    Generate a logger for fitness_threshold logging in the learning insatance
    Logger created using referance to the base learning instance

    var: instance_file_path - the file path to the root logging folder
    var: instance_id - The id of the learning instance
    """

    logger_name: str = instance_id + "fitness_threshold_logger"
    file_path: str = (
        instance_file_path + "/fitness_thresholds/fitness_thresholds_log.log"
    )
    generate_logger(logger_name=logger_name, file_path=file_path)


def new_run_time_logger(instance_file_path: str, instance_id: str) -> None:
    """
    Generate a logger for function run time logging in the learning insatance
    Logger created using referance to the base learning instance

    var: instance_file_path - the file path to the root logging folder
    var: instance_id - The id of the learning instance
    """

    logger_name: str = instance_id + "run_time_logger"
    file_path: str = instance_file_path + "/run_time/run_time_log.log"
    generate_logger(logger_name=logger_name, file_path=file_path)
