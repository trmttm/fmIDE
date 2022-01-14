import copy
from typing import Any
from typing import Callable
from typing import Dict
from typing import List

from interface_mouse import MouseControllerABC

from . import conditions as mouse_condition
from . import constants as cns
from . import implementations as impl


class MouseController(MouseControllerABC):
    def __init__(self):
        self._clicked_coordinate = (0, 0)
        self._previous_coordinate = (0, 0)

        self._commands: Dict[Any, List[Callable]] = {}
        self._conditions: Dict[Any, Callable[[dict], bool]] = {}
        self._command_specific_arguments_dict: Dict[Any, dict] = {}

        # Flags
        self._is_moving_shapes = False

    def set_mode_to_moving_shapes(self):
        self._is_moving_shapes = True

    def set_mode_to_adding_shapes(self):
        self._is_moving_shapes = False

    @property
    def is_moving_shape_mode(self) -> bool:
        return self._is_moving_shapes

    @property
    def is_adding_shapes_mode(self) -> bool:
        return not self._is_moving_shapes

    @property
    def clicked_coordinate(self) -> tuple:
        return self._clicked_coordinate

    def configure(self, key, command, condition: Callable[[dict], bool], command_specific_arguments_dict: dict):
        commands = self._commands
        if key in commands:
            commands[key].append(command)
        else:
            commands[key] = [command]

        self._conditions[key] = condition
        self._command_specific_arguments_dict[key] = command_specific_arguments_dict or {}

    def handle(self, x, y, button, modifier, gesture, **kwargs):
        common_args = impl.create_common_arguments(button, gesture, x, y, modifier)
        impl.add_live_mouse_information_to_argument(self._previous_coordinate, self._clicked_coordinate, common_args)

        for key, identify_mouse_action in self._conditions.items():
            if identify_mouse_action(common_args):
                common_arguments_copy = copy.deepcopy(common_args)
                unique_kwargs = copy.deepcopy(self._command_specific_arguments_dict)
                unique_kwargs[key].update(kwargs)
                impl.handle_request(self._commands, key, common_arguments_copy, unique_kwargs)

                self._save_mouse_position(common_arguments_copy)
                self._save_clicked_position(common_arguments_copy)

    def _save_mouse_position(self, request: dict):
        self._previous_coordinate = request['x'], request['y']

    def _save_clicked_position(self, request: dict):
        save_clicked_position = request.get(cns.save_click_coordinate, None)
        if save_clicked_position:
            self._clicked_coordinate = request['x'], request['y']

    @staticmethod
    def is_left_click(request: dict) -> bool:
        return mouse_condition.is_left_click(request)

    @staticmethod
    def is_right_click(request: dict) -> bool:
        return mouse_condition.is_right_click(request)

    @staticmethod
    def is_middle_click(request: dict) -> bool:
        return mouse_condition.is_middle_click(request)

    @staticmethod
    def is_shift_left_click(request: dict) -> bool:
        return mouse_condition.is_shift_left_click(request)

    @staticmethod
    def is_shift_right_click(request: dict) -> bool:
        return mouse_condition.is_shift_right_click(request)

    @staticmethod
    def is_shift_middle_click(request: dict) -> bool:
        return mouse_condition.is_shift_middle_click(request)

    @staticmethod
    def is_alt_option_left_click(request: dict) -> bool:
        return mouse_condition.is_alt_option_left_click(request)

    @staticmethod
    def is_alt_option_right_click(request: dict) -> bool:
        return mouse_condition.is_alt_option_right_click(request)

    @staticmethod
    def is_alt_option_middle_click(request: dict) -> bool:
        return mouse_condition.is_alt_option_middle_click(request)

    @staticmethod
    def is_control_left_click(request: dict) -> bool:
        return mouse_condition.is_control_left_click(request)

    @staticmethod
    def is_control_right_click(request: dict) -> bool:
        return mouse_condition.is_control_right_click(request)

    @staticmethod
    def is_control_middle_click(request: dict) -> bool:
        return mouse_condition.is_control_middle_click(request)

    @staticmethod
    def is_command_left_click(request: dict) -> bool:
        return mouse_condition.is_command_left_click(request)

    @staticmethod
    def is_command_right_click(request: dict) -> bool:
        return mouse_condition.is_command_right_click(request)

    @staticmethod
    def is_command_middle_click(request: dict) -> bool:
        return mouse_condition.is_command_middle_click(request)

    @staticmethod
    def is_left_drag(request: dict) -> bool:
        return mouse_condition.is_left_drag(request)

    @staticmethod
    def is_right_drag(request: dict) -> bool:
        return mouse_condition.is_right_drag(request)

    @staticmethod
    def is_middle_drag(request: dict) -> bool:
        return mouse_condition.is_middle_drag(request)

    @staticmethod
    def is_shift_left_drag(request: dict) -> bool:
        return mouse_condition.is_shift_left_drag(request)

    @staticmethod
    def is_shift_right_drag(request: dict) -> bool:
        return mouse_condition.is_shift_right_drag(request)

    @staticmethod
    def is_shift_middle_drag(request: dict) -> bool:
        return mouse_condition.is_shift_middle_drag(request)

    @staticmethod
    def is_alt_option_left_drag(request: dict) -> bool:
        return mouse_condition.is_alt_option_left_drag(request)

    @staticmethod
    def is_alt_option_right_drag(request: dict) -> bool:
        return mouse_condition.is_alt_option_right_drag(request)

    @staticmethod
    def is_alt_option_middle_drag(request: dict) -> bool:
        return mouse_condition.is_alt_option_middle_drag(request)

    @staticmethod
    def is_control_left_drag(request: dict) -> bool:
        return mouse_condition.is_control_left_drag(request)

    @staticmethod
    def is_control_right_drag(request: dict) -> bool:
        return mouse_condition.is_control_right_drag(request)

    @staticmethod
    def is_control_middle_drag(request: dict) -> bool:
        return mouse_condition.is_control_middle_drag(request)

    @staticmethod
    def is_command_left_drag(request: dict) -> bool:
        return mouse_condition.is_command_left_drag(request)

    @staticmethod
    def is_command_right_drag(request: dict) -> bool:
        return mouse_condition.is_command_right_drag(request)

    @staticmethod
    def is_command_middle_drag(request: dict) -> bool:
        return mouse_condition.is_command_middle_drag(request)

    @staticmethod
    def is_left_release(request: dict) -> bool:
        return mouse_condition.is_left_release(request)

    @staticmethod
    def is_right_release(request: dict) -> bool:
        return mouse_condition.is_right_release(request)

    @staticmethod
    def is_middle_release(request: dict) -> bool:
        return mouse_condition.is_middle_release(request)

    @staticmethod
    def is_shift_left_release(request: dict) -> bool:
        return mouse_condition.is_shift_left_release(request)

    @staticmethod
    def is_shift_right_release(request: dict) -> bool:
        return mouse_condition.is_shift_right_release(request)

    @staticmethod
    def is_shift_middle_release(request: dict) -> bool:
        return mouse_condition.is_shift_middle_release(request)

    @staticmethod
    def is_alt_option_left_release(request: dict) -> bool:
        return mouse_condition.is_alt_option_left_release(request)

    @staticmethod
    def is_alt_option_right_release(request: dict) -> bool:
        return mouse_condition.is_alt_option_right_release(request)

    @staticmethod
    def is_alt_option_middle_release(request: dict) -> bool:
        return mouse_condition.is_alt_option_middle_release(request)

    @staticmethod
    def is_control_left_release(request: dict) -> bool:
        return mouse_condition.is_control_left_release(request)

    @staticmethod
    def is_control_right_release(request: dict) -> bool:
        return mouse_condition.is_control_right_release(request)

    @staticmethod
    def is_control_middle_release(request: dict) -> bool:
        return mouse_condition.is_control_middle_release(request)

    @staticmethod
    def is_command_left_release(request: dict) -> bool:
        return mouse_condition.is_command_left_release(request)

    @staticmethod
    def is_command_right_release(request: dict) -> bool:
        return mouse_condition.is_command_right_release(request)

    @staticmethod
    def is_command_middle_release(request: dict) -> bool:
        return mouse_condition.is_command_middle_release(request)

    @staticmethod
    def is_mouse_in(request: dict) -> bool:
        return mouse_condition.is_mouse_in(request)

    @staticmethod
    def is_mouse_out(request: dict) -> bool:
        return mouse_condition.is_mouse_out(request)

    @staticmethod
    def is_mouse_wheel(request: dict) -> bool:
        return mouse_condition.is_mouse_wheel(request)

    @staticmethod
    def is_shift_mouse_wheel(request: dict) -> bool:
        return mouse_condition.is_shift_mouse_wheel(request)

    @staticmethod
    def is_alt_option_mouse_wheel(request: dict) -> bool:
        return mouse_condition.is_alt_option_mouse_wheel(request)

    @staticmethod
    def is_control_mouse_wheel(request: dict) -> bool:
        return mouse_condition.is_control_mouse_wheel(request)

    @staticmethod
    def is_command_mouse_wheel(request: dict) -> bool:
        return mouse_condition.is_command_mouse_wheel(request)
