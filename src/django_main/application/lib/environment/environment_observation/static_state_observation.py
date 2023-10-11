"""The collection of observation data from a static state environemnt"""
from itertools import chain
import numpy as np


def static_state_observation(
    agent_coords: int, env_map: np.array, ncol: int
) -> list[float]:
    """The collection of observation data from a static state based env"""
    loc_row, loc_col = agent_coords

    values_up_right: list = np.diagonal(env_map[loc_row::-1, loc_col:])[1:]

    values_down_right: list = np.diagonal(env_map[loc_row:, loc_col:])[1:]
    values_down: list = env_map[loc_row + 1 :, loc_col]
    values_down_left: list = np.diagonal(env_map[loc_row:, loc_col::-1])[1:]
    values_right = env_map[loc_row, loc_col + 1 :]
    values_up_left: list = np.diagonal(env_map[loc_row::-1, loc_col::-1])[1:]
    values_left: list = env_map[loc_row, loc_col - 1 :: -1]
    values_up: list = env_map[loc_row - 1 :: -1, loc_col]

    # catch fo the 0 error for left and up
    if loc_col == 0:
        values_left: list = []
    if loc_row == 0:
        values_up: list = []

    sight_lines = [
        values_up,
        values_up_right,
        values_right,
        values_down_right,
        values_down,
        values_down_left,
        values_left,
        values_up_left,
    ]

    observation_data = list(map(check_sight_line, sight_lines))
    observation_data = list(chain(*observation_data))
    return observation_data


def check_sight_line(sight_line: list) -> list[float, float, float]:
    """Check along the given sightline and determin activation

    Can not see past Goal or Obstical
    case -> open states to the end of the map
    """
    rtn_data = []
    for distance, value in enumerate(sight_line):
        if value == 1:
            rtn_data = [0.1 * (distance + 1), 0.0, 0.0]
        if value == 2:
            return [round(0.1 * distance, 3), 1 / (distance + 1), 0.0]
        if value == 3:
            return [round(0.1 * distance, 3), 0.0, 1 / (distance + 1)]

    # if no data aka out of bounds
    if not rtn_data:
        return [0.0, 0.0, 0.0]

    return rtn_data


def to_coords(state: int, ncol: int) -> tuple:
    """Convert state to coords"""
    return divmod(state, ncol)
