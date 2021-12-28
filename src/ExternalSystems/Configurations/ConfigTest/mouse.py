from interface_fm import BoundaryInABC
from interface_mouse import MouseControllerABC
from interface_view import ViewABC

request_save_click = {'save click coordinate': True}
request_draw_rectangle = rdr = {'line_width': 3, 'line_color': 'black'}
request_draw_rectangle2 = {'line_width': 3, 'line_color': 'red'}
request_draw_line = {'line_width': 3, 'line_color': 'blue'}
entry_by = {'entry_by': 'mouse'}
exit_by = {'exit_by': 'mouse'}


def create_mouse_configuration(interactor: BoundaryInABC, view: ViewABC, mouse: MouseControllerABC) -> list:
    mouse_configuration = [

        # Left
        [0, interactor.do_nothing, mouse.is_left_click, request_save_click],
        [1, interactor.set_entry_point, mouse.is_left_click, entry_by],
        [2, interactor.select_shape_at_x_y, mouse.is_left_click, {}],
        [3, interactor.connect_relay_of_shape_at_x_y, mouse.is_left_click, {}],
        [4, lambda request: set_controller_mode(interactor, mouse, request), mouse.is_left_click, {}],

        [5, lambda request: move_or_select(interactor, mouse, request), mouse.is_left_drag, rdr],

        [7, interactor.clear_rectangles, mouse.is_left_release, {}],
        [8, interactor.erase_all_lines, mouse.is_left_release, {}],
        [9, interactor.exit_point, mouse.is_left_release, exit_by],

        # Ctrl Left
        [20, interactor.do_nothing, mouse.is_control_left_click, request_save_click],
        [21, interactor.set_entry_point, mouse.is_control_left_click, entry_by],
        [22, interactor.add_shape_at_x_y_to_selection, mouse.is_control_left_click, {}],

        [23, interactor.draw_rectangle, mouse.is_control_left_drag, request_draw_rectangle],
        [24, interactor.add_shapes_in_range_to_selection, mouse.is_control_left_drag, {}],

        [25, interactor.clear_rectangles, mouse.is_control_left_release, {}],
        [26, interactor.exit_point, mouse.is_control_left_release, exit_by],

        # Opt Left
        [30, interactor.do_nothing, mouse.is_alt_option_left_click, request_save_click],
        [31, interactor.set_entry_point, mouse.is_alt_option_left_click, entry_by],
        [32, interactor.add_shape_at_x_y_to_selection, mouse.is_alt_option_left_click, {}],

        [33, interactor.draw_rectangle, mouse.is_alt_option_left_drag, request_draw_rectangle2],
        [34, interactor.select_shapes_in_range, mouse.is_alt_option_left_drag, {}],

        [35, interactor.clear_rectangles, mouse.is_alt_option_left_release, {}],
        [36, interactor.erase_connections_in_range, mouse.is_alt_option_left_release, {}],
        [37, interactor.erase_shapes_in_rectangle, mouse.is_alt_option_left_release, {}],
        [38, interactor.exit_point, mouse.is_alt_option_left_release, exit_by],

        # Shift Left
        [50, interactor.do_nothing, mouse.is_shift_left_click, request_save_click],
        [51, interactor.set_entry_point, mouse.is_shift_left_click, entry_by],
        [53, interactor.select_shape_at_x_y, mouse.is_shift_left_click, {}],

        [54, interactor.move_selections_one_direction, mouse.is_shift_left_drag, {}],
        [55, interactor.clear_rectangles, mouse.is_shift_left_release, {}],
        [57, interactor.exit_point, mouse.is_shift_left_release, exit_by],

        # Shift Right
        [60, interactor.do_nothing, mouse.is_shift_right_click, request_save_click],
        [61, interactor.set_entry_point, mouse.is_shift_right_click, entry_by],
        [63, interactor.select_shape_at_x_y, mouse.is_shift_right_click, {}],

        [64, interactor.move_selections_one_direction_and_evenly_distribute, mouse.is_shift_right_drag, {}],
        [65, interactor.clear_rectangles, mouse.is_shift_right_release, {}],
        [66, interactor.exit_point, mouse.is_shift_right_release, exit_by],

        # Command Left
        [10, interactor.do_nothing, mouse.is_command_left_click, request_save_click],
        [11, interactor.set_entry_point, mouse.is_command_left_click, entry_by],
        [12, interactor.select_shape_at_x_y, mouse.is_command_left_click, {}],
        [13, interactor.show_connectable_shapes, mouse.is_command_left_click, {}],
        [14, interactor.draw_line_shape_connector, mouse.is_command_left_drag, request_draw_line],
        [15, interactor.connect_shapes_by_coordinates, mouse.is_command_left_release, {}],
        [16, interactor.exit_point, mouse.is_command_left_release, exit_by],

        # Right
        [40, interactor.do_nothing, mouse.is_right_click, request_save_click],
        [41, interactor.set_entry_point, mouse.is_right_click, entry_by],
        [42, interactor.select_shape_at_x_y, mouse.is_right_click, {}],
        [43, interactor.show_connectable_shapes, mouse.is_right_click, {}],
        [44, interactor.draw_line_shape_connector, mouse.is_right_drag, request_draw_line],
        [45, interactor.connect_shapes_by_coordinates, mouse.is_right_release, {}],
        [46, interactor.exit_point, mouse.is_right_release, exit_by],

        # Mouse Wheel
        [70, lambda request: view.scroll_canvas(request['scroll_x'], request['scroll_y']),
         mouse.is_mouse_wheel, {}],
        # [71, lambda request: interactor.feedback_user(f'{request}'), mouse.is_shift_mouse_wheel, {}],
        # [72, lambda request: interactor.feedback_user(f'{request}'), mouse.is_alt_option_mouse_wheel, {}],
        # [73, lambda request: interactor.feedback_user(f'{request}'), mouse.is_control_mouse_wheel, {}],
        # [74, lambda request: interactor.feedback_user(f'{request}'), mouse.is_command_mouse_wheel, {}],
    ]
    return mouse_configuration


def set_controller_mode(interactor: BoundaryInABC, mouse: MouseControllerABC, request):
    if interactor.get_shape_at_coordinate(request['x'], request['y']) is None:
        mouse.set_mode_to_adding_shapes()
    else:
        mouse.set_mode_to_moving_shapes()


def move_or_select(interactor: BoundaryInABC, mouse: MouseControllerABC, request):
    if mouse.is_adding_shapes_mode:
        interactor.draw_rectangle(request=request)
        interactor.select_shapes_in_range(request=request)
    elif mouse.is_moving_shape_mode:
        interactor.move_selections(request=request)

