import json
from functools import partial


# This is all working of the old state vale system - need to rework to use the x,y system
def build_svg_data(brain_instance_models: list) -> list:
    """Build the svg path strings based on the Brain instance path"""

    # Hard coding sizes to start
    board_size_x = 200
    states_x = 10

    step_size = board_size_x / states_x
    state_center_point = step_size / 2

    to_coords_partial: callable = partial(
        state_to_coords,
        states_x=states_x,
        step_size=step_size,
        state_center_point=state_center_point,
    )

    for instance in brain_instance_models:
        svg_commands: list[str] = []

        path: str = instance.traversed_path
        print(path)
        path_list: list[int] = instance.traversed_path

        start_location_state: int = int(instance.svg_start)
        end_location_state: int = int(instance.svg_end)

        # can be refactored down
        start_svg_coords_x, start_svg_coords_y = to_coords_partial(start_location_state)

        end_svg_coords_x, end_svg_coords_y = to_coords_partial(end_location_state)

        svg_commands.append(
            f"M{start_svg_coords_x},{start_svg_coords_y}"
        )  # depending on how its handled may need this

        for element in path_list:
            svg_coords_x, svg_coords_y = to_coords_partial(element)
            svg_commands.append(f"L{svg_coords_x},{svg_coords_y}")

        instance.svg_start = build_svg_start_commands(
            start_svg_coords_x, start_svg_coords_y
        )
        instance.svg_end = build_end_point_commands(end_svg_coords_x, end_svg_coords_y)

        instance.svg_path = ",".join(svg_commands)

    return brain_instance_models


def build_end_point_commands(
    end_svg_coords_x: float, end_svg_coords_y: float
) -> list[str]:
    """Build the command needed to draw a cross at the end of the drawn svg_path"""

    line_1_x1: str = str(end_svg_coords_x - 5)
    line_1_y1: str = str(end_svg_coords_y - 5)

    line_1_x2: str = str(end_svg_coords_x + 5)
    line_1_y2: str = str(end_svg_coords_y + 5)

    line_2_x1: str = str(end_svg_coords_x - 5)
    line_2_y1: str = str(end_svg_coords_y + 5)

    line_2_x2: str = str(end_svg_coords_x + 5)
    line_2_y2: str = str(end_svg_coords_y - 5)

    commands: list[str] = [
        line_1_x1,
        line_1_y1,
        line_1_x2,
        line_1_y2,
        line_2_x1,
        line_2_y1,
        line_2_x2,
        line_2_y2,
    ]
    return commands


def build_svg_start_commands(
    start_svg_coords_x: float, start_svg_coords_y: float
) -> list[str]:
    """Build the command needed to draw a circle at the start of the drawn  svg_path"""

    circle_x1: str = str(start_svg_coords_x)
    circle_y1: str = str(start_svg_coords_y)
    commands: list[str] = [circle_x1, circle_y1]

    return commands


def state_to_coords(
    state: int, states_x: int, step_size: float, state_center_point: float
) -> str:
    """Convert a given state to coords representation

    Gives the coords of the ceter point of the give state
    """

    base_coords = divmod(state, states_x)
    y_state = base_coords[0]
    x_state = base_coords[1]
    svg_coords_x = (x_state * step_size) + state_center_point
    svg_coords_y = (y_state * step_size) + state_center_point

    return svg_coords_x, svg_coords_y
