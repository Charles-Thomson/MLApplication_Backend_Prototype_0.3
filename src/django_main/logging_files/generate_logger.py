"""
Function to generate a new logger 
"""
import logging

# Basic logging config
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

DEFAULT_FORMAT = "%(levelname)s :: %(funcName)s :: %(message)s"


def generate_logger(logger_name: str, file_path: str, formatting: str = DEFAULT_FORMAT):
    """Generat a custom logger"""
    new_logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(filename=file_path, mode="w")
    formatter = logging.Formatter(formatting)
    handler.setFormatter(formatter)
    new_logger.addHandler(handler)
    new_logger.propagate = False
