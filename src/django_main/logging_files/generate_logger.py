"""
Function to generate a new logger 
"""
import logging

# Basic logging config
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

DEFAULT_FORMAT = "%(levelname)s :: %(funcName)s :: %(message)s"


def generate_logger(name: __name__, log_file: str, formatting: str = DEFAULT_FORMAT):
    """Generat a custom logger"""
    new_logger = logging.getLogger(name)
    filename = "logs/debug_logs/" + log_file
    handler = logging.FileHandler(filename=filename, mode="w")
    formatter = logging.Formatter(formatting)
    handler.setFormatter(formatter)
    new_logger.addHandler(handler)
    new_logger.propagate = False

    return new_logger
