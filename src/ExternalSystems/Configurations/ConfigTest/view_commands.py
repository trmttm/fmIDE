from interface_fm import BoundaryInABC
from interface_view import ViewABC

from . import view_model as vm

__paned_window_btn_previous_sash_position = None
__hide_position = 0


def update_tree_account(view: ViewABC, view_model, interactor: BoundaryInABC):
    view.switch_tree(vm.tree_account_order)
    view.update_tree(view_model)

    keep_focus_away_from_entries_or_trees_so_key_can_manipulate_canvas_only(interactor, view)


def update_tree_worksheets(view: ViewABC, view_model, interactor: BoundaryInABC):
    view.switch_tree(vm.tree_worksheets)
    view.update_tree(view_model)

    keep_focus_away_from_entries_or_trees_so_key_can_manipulate_canvas_only(interactor, view)


def update_tree_connections(view: ViewABC, view_model, interactor: BoundaryInABC):
    view.switch_tree(vm.tree_connections)
    view.update_tree(view_model)

    keep_focus_away_from_entries_or_trees_so_key_can_manipulate_canvas_only(interactor, view)


def get_initial_focused_widget_id(view):
    try:
        initial_focus = view.focused_widget
        return initial_focus
    except KeyError:
        return None


def keep_focus_away_from_entries_or_trees_so_key_can_manipulate_canvas_only(interactor: BoundaryInABC, view: ViewABC):
    if interactor.entry_by_mouse:
        view.focus(vm.btn_op_bb)


def update_tree_commands(view: ViewABC, view_model):
    view.switch_tree(vm.tree_commands)
    view.update_tree(view_model)


def update_tree_macros(view: ViewABC, view_model):
    view.switch_tree(vm.tree_macros)
    view.update_tree(view_model)


def update_tree_inputs(view: ViewABC, view_model):
    view.switch_tree(vm.tree_sensitivity_input_list)
    view.update_tree(view_model)


def update_tree_sensitivity_accounts(view: ViewABC, view_model):
    view.switch_tree(vm.tree_sensitivity_account_list)
    view.update_tree(view_model)


def update_tree_sensitivity_target_accounts(view: ViewABC, view_model):
    view.switch_tree(vm.tree_sensitivity_target_list)
    view.update_tree(view_model)


def update_tree_sensitivity_variable_accounts(view: ViewABC, view_model):
    view.switch_tree(vm.tree_sensitivity_variable_list)
    view.update_tree(view_model)


def update_sheet_name_entry(view: ViewABC, view_model):
    sheet_name = ''
    for tree_data in view_model['tree_datas']:
        if tree_data['select_this_item']:  # only one worksheet is 'selected' at any time.
            sheet_name = tree_data['values'][1]
    if sheet_name:
        view.set_value(vm.entry_sheet_name, sheet_name)


def update_input_entry(view: ViewABC, view_model: dict):
    text = view_model['text']
    values_str = view_model['values_str']
    input_id = view_model['input_id']
    input_name = view_model['input_name']

    view.set_value(vm.ie_label, text)
    view.set_value(vm.ie_entry, values_str)
    view.set_value(vm.ie_combo_box, (input_id, input_name))


def draw_input_entry(view: ViewABC, view_model: dict):
    values = view_model['values']
    nop = view_model['nop']
    y_range = view_model['y_range']
    decimals = view_model['decimals'] if 'decimals' in view_model else None

    draw_input_entry_graph(0.05, values, view, nop, y_range, decimals)

    check_button = view.get_value(vm.ie_check_btn)
    if check_button:
        draw_input_entry_slider(view)


def draw_input_entry_graph(margin_rate, values, view, number_of_periods: int, y_range: tuple, decimals: int = None):
    current_canvas = view.current_canvas
    view.switch_canvas(vm.ie_canvas_graph)

    nop = number_of_periods
    view.clear_canvas()

    draw_grid_line(margin_rate, nop, view)
    draw_rectangle_sliders(margin_rate, nop, values, view, y_range)
    set_min_max_entries(view, y_range)
    set_decimals(view, decimals)

    view.switch_canvas(current_canvas)


def draw_grid_line(margin_rate, nop, view: ViewABC, more_line_data: dict = None):
    canvas_height = view.get_canvas_height()
    canvas_width = view.get_canvas_width()
    trim_rate = 1 - margin_rate
    margin = canvas_height * margin_rate
    canvas_height_trimmed = canvas_height * trim_rate
    line_data = {}
    for n in range(nop):
        line_data[n] = {}
        x = canvas_width / (nop + 1) * (n + 1)
        line_data[n]['coordinate_from'] = (x, margin)
        line_data[n]['coordinate_to'] = (x, canvas_height_trimmed)
        line_data[n]['line_color'] = 'black'
        line_data[n]['line_width'] = '1'
        line_data[n]['arrow'] = None
    if more_line_data is not None:
        line_data.update(more_line_data)
    view.draw_line(line_data)


def draw_rectangle_sliders(margin_rate, nop, values, view: ViewABC, y_range):
    canvas_height = view.get_canvas_height()
    canvas_width = view.get_canvas_width()
    trim_rate = 1 - margin_rate
    margin = canvas_height * margin_rate
    canvas_height_trimmed = canvas_height * trim_rate
    y_min, y_max = y_range
    rectangle_data = {}
    rectangle_w_h = canvas_height_trimmed / (nop * 3)

    for n, value in enumerate(values):
        tag = create_tag_input_slider(n)
        x = canvas_width / (nop + 1) * (n + 1)
        try:
            y = margin + (canvas_height - margin * 2) * (y_max - value) / (y_max - y_min)
        except ZeroDivisionError:
            y = canvas_height - margin
        x1 = x - rectangle_w_h
        x2 = x + rectangle_w_h
        y1 = y - rectangle_w_h
        y2 = y + rectangle_w_h

        rectangle_data[n] = {}
        rectangle_data[n]['coordinate_from'] = x1, y1
        rectangle_data[n]['coordinate_to'] = x2, y2
        rectangle_data[n]['line_color'] = 'black'
        rectangle_data[n]['fill'] = 'orange'
        rectangle_data[n]['line_width'] = '1'
        rectangle_data[n]['tags'] = ('all', tag)
    view.draw_rectangle(rectangle_data)


def draw_rectangle_sliders_per_mouse_line(margin_rate, nop, view: ViewABC, request: dict):
    (a1, b1), (a2, b2) = request['coordinates']
    x_min = min(a1, a2)
    x_max = max(a1, a2)

    try:
        slope = (b2 - b1) / (a2 - a1)
    except ZeroDivisionError:
        slope = 1

    def get_y_at_x(x_):
        return slope * (x_ - a1) + b1

    canvas_height = view.get_canvas_height()
    canvas_width = view.get_canvas_width()
    trim_rate = 1 - margin_rate
    margin = canvas_height * margin_rate
    canvas_height_trimmed = canvas_height * trim_rate
    rectangle_data = {}
    rectangle_w_h = canvas_height_trimmed / (nop * 3)

    for n in range(nop):
        x = canvas_width / (nop + 1) * (n + 1)
        if x < x_min or x_max < x:
            continue
        tag = create_tag_input_slider(n)
        view.clear_canvas_shapes_by_tag(tag)
        try:
            y = get_y_at_x(x)
        except ZeroDivisionError:
            y = canvas_height - margin
        x1 = x - rectangle_w_h
        x2 = x + rectangle_w_h
        y1 = y - rectangle_w_h
        y2 = y + rectangle_w_h

        rectangle_data[n] = {}
        rectangle_data[n]['coordinate_from'] = x1, y1
        rectangle_data[n]['coordinate_to'] = x2, y2
        rectangle_data[n]['line_color'] = 'black'
        rectangle_data[n]['fill'] = 'orange'
        rectangle_data[n]['line_width'] = '1'
        rectangle_data[n]['tags'] = ('all', tag)
    view.draw_rectangle(rectangle_data)


def create_tag_input_slider(period: int):
    tag = f'input_handle_{period}'
    return tag


def set_min_max_entries(view, y_range):
    y_min, y_max = y_range
    view.set_value(vm.ie_entry_max, y_max)
    view.set_value(vm.ie_entry_min, y_min)


def set_decimals(view: ViewABC, decimals: int):
    view.set_value(vm.ie_entry_digits, decimals)


def draw_input_entry_slider(view):
    current_canvas = view.current_canvas

    view.switch_canvas(vm.ie_canvas_slider)
    view.clear_canvas()
    canvas_height = view.get_canvas_height()
    canvas_width = view.get_canvas_width()

    rectangle_data = {0: {}}
    rectangle_data[0]['coordinate_from'] = 0, canvas_height / 2 - canvas_width / 2
    rectangle_data[0]['coordinate_to'] = canvas_width, canvas_height / 2 + canvas_width / 2
    rectangle_data[0]['line_color'] = 'black'
    rectangle_data[0]['fill'] = 'light blue'
    rectangle_data[0]['line_width'] = '1'
    rectangle_data[0]['tags'] = ('all',)
    view.draw_rectangle(rectangle_data)

    view.switch_canvas(current_canvas)


def toggle_design_buttons_show_hide(view: ViewABC):
    global __paned_window_btn_previous_sash_position
    paned_window_id = vm.paned_window_btn
    if __paned_window_btn_previous_sash_position in (None,):
        _hide_design_buttons(paned_window_id, view)
    elif view.get_paned_window_sash_position(paned_window_id) in (__hide_position,):
        _show_design_buttons(paned_window_id, view)
    else:
        _hide_design_buttons(paned_window_id, view)


def decorator_show_design_buttons(f, view: ViewABC):
    def show_design_buttons(*args, **kwargs):
        paned_window_id = vm.paned_window_btn
        if view.get_paned_window_sash_position(paned_window_id) in (__hide_position,):
            _show_design_buttons(paned_window_id, view)

        f(*args, **kwargs)

    return show_design_buttons


def _show_design_buttons(paned_window_id, view: ViewABC):
    global __paned_window_btn_previous_sash_position
    new_position = __paned_window_btn_previous_sash_position
    __paned_window_btn_previous_sash_position = __hide_position
    view.set_paned_window_sash_position(paned_window_id, new_position)


def _hide_design_buttons(paned_window_id, view: ViewABC):
    global __paned_window_btn_previous_sash_position
    __paned_window_btn_previous_sash_position = view.get_paned_window_sash_position(paned_window_id)
    new_position = __hide_position
    view.set_paned_window_sash_position(paned_window_id, new_position)
