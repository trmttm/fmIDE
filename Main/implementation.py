from interface_mouse import MouseControllerABC
from interface_view import ViewABC


def configure_mouse(mouse: MouseControllerABC, mouse_configuration: list):
    for configuration in mouse_configuration:
        mouse.configure(*configuration)


def bind_commands_to_widgets(command_dictionary: dict, view: ViewABC):
    for widget_id, command in command_dictionary.items():
        view.bind_command_to_widget(widget_id, command)
