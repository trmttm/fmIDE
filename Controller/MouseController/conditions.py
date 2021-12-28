from . import constants as mouse


def _user_action_is(action: str, request: dict) -> bool:
    return request[mouse.GESTURE] == action


def _button_is(button: str, request: dict) -> bool:
    return request[mouse.BUTTON] == button


def _with_modifier(modifier: str, request: dict) -> bool:
    return request[mouse.MODIFIER] == modifier


def _no_modifier(request: dict) -> bool:
    return request[mouse.MODIFIER] is None


"""
Clicks
"""


def _is_left_click(request):
    return _user_action_is(mouse.CLICK, request) and _button_is(mouse.LEFT, request)


def _is_right_click(request):
    return _user_action_is(mouse.CLICK, request) and _button_is(mouse.RIGHT, request)


def _is_middle_click(request):
    return _user_action_is(mouse.CLICK, request) and _button_is(mouse.MIDDLE, request)


def is_left_click(request: dict) -> bool:
    return _is_left_click(request) and _no_modifier(request)


def is_right_click(request: dict) -> bool:
    return _is_right_click(request) and _no_modifier(request)


def is_middle_click(request: dict) -> bool:
    return _is_middle_click(request) and _no_modifier(request)


def is_shift_left_click(request: dict) -> bool:
    return _is_left_click(request) and _with_modifier(mouse.SHIFT, request)


def is_shift_right_click(request: dict) -> bool:
    return _is_right_click(request) and _with_modifier(mouse.SHIFT, request)


def is_shift_middle_click(request: dict) -> bool:
    return _is_middle_click(request) and _with_modifier(mouse.SHIFT, request)


def is_alt_option_left_click(request: dict) -> bool:
    return _is_left_click(request) and _with_modifier(mouse.ALT_OPTION, request)


def is_alt_option_right_click(request: dict) -> bool:
    return _is_right_click(request) and _with_modifier(mouse.ALT_OPTION, request)


def is_alt_option_middle_click(request: dict) -> bool:
    return _is_middle_click(request) and _with_modifier(mouse.ALT_OPTION, request)


def is_control_left_click(request: dict) -> bool:
    return _is_left_click(request) and _with_modifier(mouse.CONTROL, request)


def is_control_right_click(request: dict) -> bool:
    return _is_right_click(request) and _with_modifier(mouse.CONTROL, request)


def is_control_middle_click(request: dict) -> bool:
    return _is_middle_click(request) and _with_modifier(mouse.CONTROL, request)


def is_command_left_click(request: dict) -> bool:
    return _is_left_click(request) and _with_modifier(mouse.COMMAND, request)


def is_command_right_click(request: dict) -> bool:
    return _is_right_click(request) and _with_modifier(mouse.COMMAND, request)


def is_command_middle_click(request: dict) -> bool:
    return _is_middle_click(request) and _with_modifier(mouse.COMMAND, request)


"""
Drags
"""


def _is_left_drag(request) -> bool:
    return _user_action_is(mouse.CLICK_MOTION, request) and _button_is(mouse.LEFT, request)


def _is_right_drag(request) -> bool:
    return _user_action_is(mouse.CLICK_MOTION, request) and _button_is(mouse.RIGHT, request)


def _is_middle_drag(request):
    return _user_action_is(mouse.CLICK_MOTION, request) and _button_is(mouse.MIDDLE, request)


def is_left_drag(request: dict) -> bool:
    return _is_left_drag(request) and _no_modifier(request)


def is_right_drag(request: dict) -> bool:
    return _is_right_drag(request) and _no_modifier(request)


def is_middle_drag(request: dict) -> bool:
    return _is_middle_drag(request) and _no_modifier(request)


def is_shift_left_drag(request: dict) -> bool:
    return _is_left_drag(request) and _with_modifier(mouse.SHIFT, request)


def is_shift_right_drag(request: dict) -> bool:
    return _is_right_drag(request) and _with_modifier(mouse.SHIFT, request)


def is_shift_middle_drag(request: dict) -> bool:
    return _is_middle_drag(request) and _with_modifier(mouse.SHIFT, request)


def is_alt_option_left_drag(request: dict) -> bool:
    return _is_left_drag(request) and _with_modifier(mouse.ALT_OPTION, request)


def is_alt_option_right_drag(request: dict) -> bool:
    return _is_right_drag(request) and _with_modifier(mouse.ALT_OPTION, request)


def is_alt_option_middle_drag(request: dict) -> bool:
    return _is_middle_drag(request) and _with_modifier(mouse.ALT_OPTION, request)


def is_control_left_drag(request: dict) -> bool:
    return _is_left_drag(request) and _with_modifier(mouse.CONTROL, request)


def is_control_right_drag(request: dict) -> bool:
    return _is_right_drag(request) and _with_modifier(mouse.CONTROL, request)


def is_control_middle_drag(request: dict) -> bool:
    return _is_middle_drag(request) and _with_modifier(mouse.CONTROL, request)


def is_command_left_drag(request: dict) -> bool:
    return _is_left_drag(request) and _with_modifier(mouse.COMMAND, request)


def is_command_right_drag(request: dict) -> bool:
    return _is_right_drag(request) and _with_modifier(mouse.COMMAND, request)


def is_command_middle_drag(request: dict) -> bool:
    return _is_middle_drag(request) and _with_modifier(mouse.COMMAND, request)


"""
Released
"""


def _is_left_release(request):
    return _user_action_is(mouse.CLICK_RELEASE, request) and _button_is(mouse.LEFT, request)


def _is_right_release(request):
    return _user_action_is(mouse.CLICK_RELEASE, request) and _button_is(mouse.RIGHT, request)


def _is_middle_release(request):
    return _user_action_is(mouse.CLICK_RELEASE, request) and _button_is(mouse.MIDDLE, request)


def is_left_release(request: dict) -> bool:
    return _is_left_release(request) and _no_modifier(request)


def is_right_release(request: dict) -> bool:
    return _is_right_release(request) and _no_modifier(request)


def is_middle_release(request: dict) -> bool:
    return _is_middle_release(request) and _no_modifier(request)


def is_shift_left_release(request: dict) -> bool:
    return _is_left_release(request) and _with_modifier(mouse.SHIFT, request)


def is_shift_right_release(request: dict) -> bool:
    return _is_right_release(request) and _with_modifier(mouse.SHIFT, request)


def is_shift_middle_release(request: dict) -> bool:
    return _is_middle_release(request) and _with_modifier(mouse.SHIFT, request)


def is_alt_option_left_release(request: dict) -> bool:
    return _is_left_release(request) and _with_modifier(mouse.ALT_OPTION, request)


def is_alt_option_right_release(request: dict) -> bool:
    return _is_right_release(request) and _with_modifier(mouse.ALT_OPTION, request)


def is_alt_option_middle_release(request: dict) -> bool:
    return _is_middle_release(request) and _with_modifier(mouse.ALT_OPTION, request)


def is_control_left_release(request: dict) -> bool:
    return _is_left_release(request) and _with_modifier(mouse.CONTROL, request)


def is_control_right_release(request: dict) -> bool:
    return _is_right_release(request) and _with_modifier(mouse.CONTROL, request)


def is_control_middle_release(request: dict) -> bool:
    return _is_middle_release(request) and _with_modifier(mouse.CONTROL, request)


def is_command_left_release(request: dict) -> bool:
    return _is_left_release(request) and _with_modifier(mouse.COMMAND, request)


def is_command_right_release(request: dict) -> bool:
    return _is_right_release(request) and _with_modifier(mouse.COMMAND, request)


def is_command_middle_release(request: dict) -> bool:
    return _is_middle_release(request) and _with_modifier(mouse.COMMAND, request)


"""
Mouse In Out
"""


def is_mouse_in(request: dict) -> bool:
    return _user_action_is(mouse.MOUSE_IN, request)


def is_mouse_out(request: dict) -> bool:
    return _user_action_is(mouse.MOUSE_OUT, request)


"""
Mouse Wheel
"""


def is_mouse_wheel(request: dict) -> bool:
    return _user_action_is(mouse.MOUSE_WHEEL, request) and _no_modifier(request)


def is_shift_mouse_wheel(request: dict) -> bool:
    return _user_action_is(mouse.MOUSE_WHEEL, request) and _with_modifier(mouse.SHIFT, request)


def is_alt_option_mouse_wheel(request: dict) -> bool:
    return _user_action_is(mouse.MOUSE_WHEEL, request) and _with_modifier(mouse.ALT_OPTION, request)


def is_control_mouse_wheel(request: dict) -> bool:
    return _user_action_is(mouse.MOUSE_WHEEL, request) and _with_modifier(mouse.CONTROL, request)


def is_command_mouse_wheel(request: dict) -> bool:
    return _user_action_is(mouse.MOUSE_WHEEL, request) and _with_modifier(mouse.COMMAND, request)
