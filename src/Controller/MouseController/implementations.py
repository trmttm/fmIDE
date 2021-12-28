from typing import Any
from typing import Callable
from typing import Dict
from typing import List

from . import constants as cns


def create_common_arguments(button: int, gesture: int, x: float, y: float, modifier) -> dict:
    return {'x': x, 'y': y, cns.BUTTON: button, cns.GESTURE: gesture, cns.MODIFIER: modifier}


def add_live_mouse_information_to_argument(last_coordinate: tuple, clicked_coordinate: tuple, request: dict):
    x, y = request['x'], request['y']
    last_x, last_y = last_coordinate
    clicked_x, clicked_y = clicked_coordinate
    delta_x = x - last_x
    delta_y = y - last_y

    request.update({'coordinates': ((clicked_x, clicked_y), (x, y))})
    request.update({'delta_x': delta_x, 'delta_y': delta_y})


def handle_request(commands: Dict[Any, List[Callable]], key, common_arguments, command_specific_arguments):
    arguments_dict = create_arguments_dict(key, common_arguments, command_specific_arguments)
    invoke_command(commands, key, arguments_dict)


def create_arguments_dict(key, request_copy, request_extensions):
    request_copy.update({'handler': key})
    request_copy.update(request_extensions[key])
    request_model = request_copy
    return request_model


def invoke_command(commands: Dict[Any, List[Callable]], key, arguments_dict):
    for command in commands[key]:
        command(request=arguments_dict)
