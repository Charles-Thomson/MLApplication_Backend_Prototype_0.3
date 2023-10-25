""" Wrappers for fuctions in the leanring instance class"""

from datetime import datetime
import logging.handlers
import os
from functools import wraps
from typing import Any, Callable

# Basic logging config
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(
    level=logging.NOTSET,
)

DEFAULT_FORMAT = "%(levelname)s :: %(funcName)s :: %(message)s"

current_logger = logging.getLogger()
filename = "logs/run_time_logs/run_time_log.log"

should_roll_over = os.path.isfile(filename)

handler = logging.handlers.RotatingFileHandler(filename=filename, backupCount=3)
if should_roll_over:
    handler.doRollover()
formatter = logging.Formatter(DEFAULT_FORMAT)
handler.setFormatter(formatter)
current_logger.addHandler(handler)
current_logger.propagate = False


# def pre_call(func, *args):
#     current_logger.info(f"{func.__name__} Before function call")
#     current_logger.info("The arguments are  %s and %s" % (args))


# def post_call(func):
#     current_logger.info("After function call")


# def learning_isntance_run_instance_wrapper(
#     pre_call: Callable, post_call: Callable
# ) -> Any:
#     """
#     Wrapper for the learning instance run_instance function
#     """

#     def deco(func: Callable[..., Any]) -> Callable:
#         """Decorator"""

#         @wraps(func)
#         def call(*args, **kwargs) -> None:
#             """Function calls from wrapping"""
#             pre_call(func, *args)
#             result = func(*args, **kwargs)
#             post_call(func)
#             return result

#         return call

#     return deco


# @learning_isntance_run_instance_wrapper(pre_call=pre_call, post_call=post_call)
# def test_wrapper(x: int, y: int):
#     current_logger.info("In call")
#     result = x + y
#     return result


# test_wrapper(2, 3)


def pre_call_function(func):
    """
    Pre call function in the wrapper
    """
    time = datetime.now().time().strftime("%H:%M:%S")
    current_logger.info(f"{func.__name__} called at - {time}")


def post_call_function(func):
    """
    Post call function in the wrapper
    """
    time = datetime.now().time().strftime("%H:%M:%S")
    current_logger.info(f"{func.__name__} completed at - {time}")


def function_call_time_wrapper(pre_call: Callable, post_call: Callable) -> Any:
    """
    Wrapper for the learning instance run_instance function
    """

    def deco(func: Callable[..., Any]) -> Callable:
        """Decorator"""

        @wraps(func)
        def call(*args, **kwargs) -> None:
            """Function calls from wrapping"""
            pre_call(func)
            result = func(*args, **kwargs)
            post_call(func)
            return result

        return call

    return deco


with_run_time_logging = function_call_time_wrapper(
    pre_call=pre_call_function, post_call=post_call_function
)
