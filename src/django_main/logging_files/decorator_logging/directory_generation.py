"""The functions to geenrate the directory structure for the decorator based logging system"""
import os


def generate_new_logging_file(new_instance_id: str) -> str:
    """
    Generate the needed directory structure for logging using the
    instance_id as a referance
    var : new_instance_id - id of the given instance
    rtn : logging_path_root - the root file path to the new logging folder
    """
    logging_path_root = "logs/instance_data/" + new_instance_id

    if not os.path.exists(logging_path_root):
        os.makedirs(logging_path_root)

    directroys: list[str] = ["/generation_data", "/fitness_thresholds", "/run_time"]

    for directroy in directroys:
        full_file_path: str = logging_path_root + directroy
        if not os.path.exists(full_file_path):
            os.makedirs(full_file_path)

    return logging_path_root
