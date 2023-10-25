"""Basic logging imports"""
import logging.handlers
import logging
from logging_files.generate_logger import generate_logger

# Basic logging config
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(
    level=logging.NOTSET,
)

DEFAULT_FORMAT = "%(levelname)s :: %(funcName)s :: %(message)s"

# new_parents_logger = generate_logger(
#     __name__ + "new_parents_logger", "new_parents_logger.log"
# )

debug_logger = generate_logger(__name__ + "debug_logger", "debug_logger.log")
