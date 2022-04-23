import subprocess
from typing import Callable
from typing import Tuple
from typing import Type

import Utilities
from Utilities import auto_complete
from interface_fm import BoundaryInABC
from interface_mouse import MouseControllerABC
from interface_view import ViewABC
from src.BoundaryOutput import PresentersABC
from src.Controller import InputEntryController

from src import ViewModel as VM
from . import constants as cns
from . import keyboard_shortcuts
from . import menu_bar
from . import view_commands as vc
from . import view_model as vm
from .vcInteractor import ViewControllerInteractor as Vci

_default_macro_entry = 'User Input'


def main_specific_add_shape(interactor: BoundaryInABC, view: ViewABC, value: str = None):
    if value is None:
        value = view.get_value(vm.entry_id)
    # ViewModel(hence Main) specific method
    if Utilities.is_number(value):
        tag = 'constant'
        value = Utilities.comma_separate_string_value(value)
    elif value in ['+', '-', 'x', '/', '^', 'max', 'min', 'ave', '<', '<=', '>', '>=', '=', 'abs', 'iferror']:
        tag = 'operator'
    elif value in ['BB']:
        tag = 'bb'
    else:
        tag = 'account'

    interactor.add_new_shape(value, tag)
    focus_on_account_entry(view)


def get_current_design_canvas(interactor: BoundaryInABC):
    return f'canvas_{interactor.sheet_name_to_pass_to_presenter}'


def focus_on_account_entry(view: ViewABC):
    view.focus(vm.entry_id)


def upon_menu_button1(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
    view.switch_frame(vm.fr_fmd)
    view.switch_canvas(get_current_design_canvas(interactor))
    interactor.present_update_worksheets()
    view.focus(vm.entry_id)
    interactor.change_active_keymap(cns.keymap_design)
    update_menu_bar(view, interactor, presenters, mouse)


def upon_menu_button2(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC,
                      negative_list: tuple = ()):
    tree_item_position = _get_currently_selected_tree_position(view, vm.tree_pickle_files_id)
    load_templates(interactor, negative_list, view, tree_item_position)
    interactor.change_active_keymap(cns.keymap_template)
    hide_canvas_commands_from_menubar(interactor, mouse, presenters, view)


def upon_menu_button3(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
    view.switch_frame(vm.fr_state)
    interactor.present_state()
    view.focus(vm.textbox_rpe)
    interactor.change_active_keymap(cns.keymap_state)
    hide_canvas_commands_from_menubar(interactor, mouse, presenters, view)


def upon_menu_button4(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
    position_before_refresh = _get_currently_selected_tree_position(view, vm.tree_macros)
    view.switch_frame(vm.fr_macro)
    view.bind_tree_right_click(lambda values: upon_commands_right_click(interactor, view, values), vm.tree_commands)
    view.bind_tree_right_click(lambda values: upon_macro_list_right_click(view, values), vm.tree_macros)
    interactor.present_commands()
    interactor.present_macros()
    focus_on_tree(view, vm.tree_macros, (position_before_refresh or 0))
    interactor.change_active_keymap(cns.keymap_macro)
    hide_canvas_commands_from_menubar(interactor, mouse, presenters, view)


def upon_menu_button5(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
    view.switch_frame(vm.fr_setting)
    view.set_value(vm.entry_nop, interactor.number_of_periods)
    view.set_value(vm.entry_project, interactor.project_folder if interactor.project_folder is not None else '')
    view.set_value(vm.check_btn_cleaner, interactor.clean_state_prior_to_save)

    view.set_value(vm.entry_account_w, interactor.account_width)
    view.set_value(vm.entry_account_h, interactor.account_height)
    view.set_value(vm.entry_account_font_size, interactor.account_font_size)
    view.set_value(vm.entry_operator_w, interactor.operator_width)
    view.set_value(vm.entry_operator_h, interactor.operator_height)
    view.set_value(vm.entry_operator_font_size, interactor.operator_font_size)
    view.set_value(vm.entry_constant_w, interactor.constant_width)
    view.set_value(vm.entry_constant_h, interactor.constant_height)
    view.set_value(vm.entry_constant_font_size, interactor.constant_font_size)
    view.set_value(vm.entry_bb_w, interactor.bb_width)
    view.set_value(vm.entry_bb_h, interactor.bb_height)
    view.set_value(vm.entry_bb_font_size, interactor.bb_font_size)

    view.set_value(vm.check_btn_relay_right_end, interactor.relay_to_be_placed_at_right_end)

    interactor.change_active_keymap(cns.keymap_setting)
    hide_canvas_commands_from_menubar(interactor, mouse, presenters, view)


def set_configuration_value(view: ViewABC, method, entry_id):
    try:
        value = int(view.get_value(entry_id))
    except ValueError:
        value = None

    if value is not None:
        method(value)


def upon_fmd_switcher_accounts(view: ViewABC):
    view.switch_frame(vm.fr_account_order)
    view.switch_frame(vm.fr_tree_btn)
    tree_item_position = _get_currently_selected_tree_position(view, vm.tree_account_order)
    view.focus(vm.tree_account_order, tree_item_position=tree_item_position)


def upon_fmd_switcher_properties(view: ViewABC):
    view.switch_frame(vm.fr_property)


def upon_fmd_switcher_worksheets(view: ViewABC):
    view.switch_frame(vm.fr_worksheets)
    tree_item_position = _get_currently_selected_tree_position(view, vm.tree_worksheets)
    view.focus(vm.tree_worksheets, tree_item_position=tree_item_position)


def upon_fmd_switcher_connections(view: ViewABC):
    view.switch_frame(vm.fr_connection)


def add_connection_id(view: ViewABC, interactor: BoundaryInABC):
    entry_value = view.get_value(vm.entry_conn_id)
    selection = view.get_value(vm.int_var_conn)
    if selection == 0:
        interactor.add_the_same_connection_ids_to_selection(entry_value)
    elif selection == 1:
        interactor.add_the_same_socket_to_selection(entry_value)
    elif selection == 2:
        interactor.add_the_same_plug_to_selection(entry_value)
    view.focus(vm.entry_conn_id)


def delete_connection_id(view: ViewABC, interactor: BoundaryInABC):
    try:
        _, id_type, connection_id = view.tree_focused_values(vm.tree_connections)
    except ValueError:
        return
    if id_type == 'id':
        interactor.remove_connection_id_from_selection(connection_id)
    elif id_type == 'plug':
        interactor.remove_plug_id_from_selection(connection_id)
    elif id_type == 'socket':
        interactor.remove_socket_id_from_selection(connection_id)


def _get_currently_selected_tree_position(view: ViewABC, tree_id):
    tree_focused_values: tuple = view.tree_focused_values(tree_id)
    return tree_focused_values[0] if tree_focused_values != '' else None


def upon_tree_pickles_list_click(interactor: BoundaryInABC, view: ViewABC):
    try:
        pickle_name = view.tree_focused_values(vm.tree_pickle_files_id)[1]
    except IndexError:
        pickle_name = None

    if pickle_name:
        interactor.display_pickle(pickle_name)


def upon_tree_account_order_click(interactor: BoundaryInABC, view: ViewABC):
    if _need_to_escape_from_infinity_loop(interactor, view):
        return

    selected_tree_item_numbers = view.get_selected_tree_item_indexes(vm.tree_account_order)
    if len(selected_tree_item_numbers) == 1:
        interactor.select_shape_by_account_order(selected_tree_item_numbers[0])
    else:
        interactor.select_shape_by_account_orders(selected_tree_item_numbers)
    if not interactor.prevent_user_input_by_tree:
        view.focus(vm.tree_account_order, tree_item_position=selected_tree_item_numbers)


def _need_to_escape_from_infinity_loop(interactor: BoundaryInABC, view: ViewABC) -> bool:
    tree_numbers = view.get_selected_tree_item_indexes(vm.tree_account_order)
    current_selection = interactor.selection.data
    shape_ids_selected_by_tree = _get_shape_ids_selected_by_tree(interactor, tree_numbers)
    whether_each_tree_item_is_in_selection = tuple(e in current_selection for e in shape_ids_selected_by_tree)
    return False not in whether_each_tree_item_is_in_selection


def _get_shape_ids_selected_by_tree(interactor: BoundaryInABC, selected_tree_item_numbers: tuple) -> set:
    a = interactor.account_order.data
    try:
        shape_ids_selected_by_tree = set(a[n] for n in selected_tree_item_numbers)
    except IndexError:
        shape_ids_selected_by_tree = set()
    return shape_ids_selected_by_tree


def upon_tree_worksheets_click(interactor: BoundaryInABC, view: ViewABC):
    if len(view.tree_selected_values(vm.tree_worksheets)) != 1:
        return
    try:
        sheet_name = view.tree_focused_values(vm.tree_worksheets)[1]
    except IndexError:
        return
    if not interactor.prevent_user_input_by_tree:
        interactor.select_worksheet(sheet_name, update=True)


def highlight_commands_that_contains_text_box(interactor: BoundaryInABC, view: ViewABC):
    select = view.get_selected_tree_item_indexes(vm.tree_commands)
    interactor.highlight_commands_containing_text_box_input(view.get_value(vm.entry_macro_name), select)


def upon_delete_template(view: ViewABC, interactor: BoundaryInABC, negative_list):
    try:
        pickle_names = tuple(value[1] for value in view.tree_selected_values())
    except IndexError:
        return

    tree_item_position = _get_currently_selected_tree_position(view, vm.tree_pickle_files_id)
    interactor.remove_templates(pickle_names)
    load_templates(interactor, negative_list, view, tree_item_position)


def load_templates(interactor: BoundaryInABC, negative_list, view: ViewABC, n: int = None):
    _load_templates(interactor, negative_list, view)
    focus_on_tree(view, vm.tree_pickle_files_id, n)


def _load_templates(interactor: BoundaryInABC, negative_list, view: ViewABC):
    view.switch_frame(vm.fr_template)
    view.switch_canvas(vm.canvas_template)
    view.switch_tree(vm.tree_pickle_files_id)
    interactor.load_pickle_files_list(negative_list)


def focus_on_tree(view, tree_id: str, n=0):
    tree_item_position = _get_currently_selected_tree_position(view, tree_id)
    if tree_item_position is None:
        position_n = n
    else:
        position_n = tree_item_position + n
    view.focus(tree_id, tree_item_position=position_n)


def search_tree_focus_down(view: ViewABC, tree_id):
    try:
        focus_tree_down(tree_id, view)
    except IndexError:
        return
    view.focus(vm.entry_search)


def search_tree_focus_up(view: ViewABC, tree_id):
    focus_tree_up(tree_id, view)
    view.focus(vm.entry_search)


def focus_tree_down(tree_id, view):
    position = view.get_selected_tree_item_indexes(tree_id)[0]
    view.focus(tree_id, tree_item_position=position + 1)


def focus_tree_up(tree_id, view):
    try:
        position = view.get_selected_tree_item_indexes(tree_id)[0]
    except IndexError:
        return
    view.focus(tree_id, tree_item_position=position - 1)


def upon_load_pickle(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
    pickle_name = view.tree_focused_values(vm.tree_pickle_files_id)[1]
    upon_menu_button1(view, interactor, presenters, mouse)
    interactor.load_file(pickle_name)


def upon_merge_pickle(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC,
                      negative_list):
    pickle_name = view.tree_focused_values(vm.tree_pickle_files_id)[1]
    upon_menu_button1(view, interactor, presenters, mouse)
    interactor.merge_file(pickle_name)

    tree_item_position = _get_currently_selected_tree_position(view, vm.tree_pickle_files_id)
    load_templates(interactor, negative_list, view, tree_item_position)


def upon_leaving_entry(view: ViewABC, interactor: BoundaryInABC, widget_id_passed, key):
    entry_value = view.get_value(widget_id_passed)
    initially_selected = tuple(interactor.selection.data)

    if key == 'worksheet':
        _upon_leaving_worksheet_entry(entry_value, initially_selected, interactor, key)
    elif key == 'shape_id':
        if not Utilities.is_number(entry_value):
            interactor.feedback_user('Shape ID must be an integer.', 'error')
            return
        _upon_leaving_shape_id_entry(int(entry_value), interactor, key)
    elif key == 'socket':
        interactor.add_the_same_connection_ids_to_selection(entry_value)
    elif key == 'uom':
        interactor.add_unit_of_measure_to_selection(entry_value)
    else:
        interactor.set_property_to_selection(key, entry_value)


def _upon_leaving_worksheet_entry(entry_value, initially_selected, interactor: BoundaryInABC, key):
    if key == 'worksheet' and entry_value == '':
        return

    if interactor.worksheet_exists(entry_value):
        interactor.set_worksheet_to_selected_shapes_properties(entry_value)
        interactor.select_worksheet(entry_value)
        interactor.add_shapes_to_selection(initially_selected)
    else:
        interactor.refresh_properties()
        interactor.feedback_user(f'Worksheet {entry_value} does not exist.', 'error')


def _upon_leaving_shape_id_entry(entry_value, interactor: BoundaryInABC, key):
    if key == 'shape_id' and interactor.number_of_selected_shapes != 1:
        interactor.feedback_user('Select only one shape to set id.', 'error')
        return

    if Utilities.is_number(entry_value):
        entry_value = int(entry_value)

    old_shape_id = tuple(interactor.selection.data)[0]
    new_shape_id = entry_value
    interactor.change_shape_id(old_shape_id, new_shape_id)


def upon_leaving_entry_delta(view: ViewABC, interactor: BoundaryInABC):
    delta_x = view.get_value(vm.entry_delta_x)
    delta_y = view.get_value(vm.entry_delta_y)

    if not Utilities.is_number(delta_x):
        delta_x = 0
    if not Utilities.is_number(delta_y):
        delta_y = 0
    interactor.move_selections(float(delta_x), float(delta_y))

    view.set_value(vm.entry_delta_x, 0)
    view.set_value(vm.entry_delta_y, 0)


def change_selected_sheet_name(interactor: BoundaryInABC, view: ViewABC):
    sheet_name = view.get_value(vm.entry_sheet_name)
    interactor.change_selected_sheet_name(sheet_name)


def copy_selected_accounts(interactor: BoundaryInABC):
    interactor.copy_accounts()
    account_names = interactor.selected_account_names
    interactor.feedback_user(f'Copied {account_names}')


def paste_selected_accounts(interactor: BoundaryInABC):
    pasted_accounts = interactor.copied_account_names
    interactor.paste_accounts()
    interactor.feedback_user(f'Pasted {pasted_accounts}')


def popup_excel_export_entry(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC,
                             mouse: MouseControllerABC):
    v, i, p, m = view, interactor, presenters, mouse
    v.add_widgets(vm.excel_export_window())
    p.attach_to_present_update_sensitivity_input_accounts(
        lambda view_model: vc.update_tree_inputs(v, view_model))
    p.attach_to_present_update_sensitivity_accounts(
        lambda view_model: vc.update_tree_sensitivity_accounts(v, view_model))
    p.attach_to_present_update_sensitivity_target_accounts(
        lambda view_model: vc.update_tree_sensitivity_target_accounts(v, view_model))
    p.attach_to_present_update_sensitivity_variable_accounts(
        lambda view_model: vc.update_tree_sensitivity_variable_accounts(v, view_model))
    p.attach_to_present_insert_sheet_name_in_input_sheet(
        lambda view_model: v.set_value(vm.check_btn_input_sheet, view_model))

    v.set_value(vm.entry_export_file_name, i.save_file_name)
    v.set_value(vm.entry_path, i.project_folder or i.save_path)

    v.bind_command_to_widget(vm.entry_export_file_name, lambda *_: upon_leaving_file_name_entry(v, i))
    v.bind_command_to_widget(vm.btn_export, lambda: export_excel(v, i))
    v.bind_command_to_widget(vm.btn_path, lambda: change_path(v, i))

    v.bind_command_to_widget(vm.btn_sensitivity_target_add, lambda: add_sensitivity_target(v, i))
    v.bind_command_to_widget(vm.btn_sensitivity_target_remove, lambda: remove_sensitivity_target(v, i))
    v.bind_command_to_widget(vm.btn_sensitivity_target_up, lambda: sensitivity_target_up(v, i))
    v.bind_command_to_widget(vm.btn_sensitivity_target_down, lambda: sensitivity_target_down(v, i))

    v.bind_command_to_widget(vm.btn_sensitivity_variable_add, lambda: add_sens_variable(v, i))
    v.bind_command_to_widget(vm.btn_sensitivity_variable_remove, lambda: remove_sens_variable(v, i))

    v.bind_command_to_widget(vm.btn_sensitivity_delta, lambda: set_sensitivity_delta(v, i))

    v.bind_command_to_widget(vm.check_btn_input_sheet, lambda: upon_check_btn_input_sheet(v, i))

    v.bind_command_to_widget(vm.export_top_level, lambda: close_export_window_properly(i, v))

    i.present_sensitivity_input_accounts()
    i.present_sensitivity_accounts()
    i.present_sensitivity_target_accounts()
    i.present_sensitivity_variable_accounts()
    i.present_insert_worksheet_in_input_sheet_mode()

    # Keyboard shortcut
    i.load_keyboard_shortcut(cns.keymap_export, keyboard_shortcuts.create_export_window_key_combos(i, v, presenters, m))
    v.set_keyboard_shortcut_handler(vm.export_top_level, i.keyboard_shortcut_handler)


def close_export_window_properly(interactor: BoundaryInABC, view: ViewABC):
    view.close(vm.export_top_level)
    interactor.change_active_keymap(cns.keymap_design)  # closing toplevel is responsible for changing keymap


def toggle_check_btn_input_sheet(interactor: BoundaryInABC, view: ViewABC):
    value = not view.get_value(vm.check_btn_input_sheet)
    view.set_value(vm.check_btn_input_sheet, value)
    upon_check_btn_input_sheet(view, interactor)


def export_excel(view: ViewABC, interactor: BoundaryInABC):
    path = view.get_value(vm.entry_path)
    file_name = f'{view.get_value(vm.entry_export_file_name)}.xlsx'
    interactor.export_excel(file_name, path)
    close_export_window_properly(interactor, view)


def upon_leaving_file_name_entry(view: ViewABC, interactor: BoundaryInABC):
    file_name = view.get_value(vm.entry_export_file_name)
    interactor.set_save_file_name(file_name)


def change_path(view: ViewABC, interactor: BoundaryInABC):
    new_path = view.select_folder(initialdir=interactor.save_path)
    interactor.set_save_path(new_path)
    view.set_value(vm.entry_path, new_path)


def add_sensitivity_target(view: ViewABC, interactor: BoundaryInABC):
    tree = vm.tree_sensitivity_account_list
    add_method = interactor.add_sensitivity_target_accounts
    _add_target_accounts(view, tree, add_method)
    interactor.present_sensitivity_target_accounts()
    interactor.present_sensitivity_accounts()


def add_sens_variable(view: ViewABC, interactor: BoundaryInABC):
    tree = vm.tree_sensitivity_input_list
    add_method = interactor.add_sensitivity_variable_accounts
    _add_target_accounts(view, tree, add_method)
    interactor.present_sensitivity_variable_accounts()
    interactor.present_sensitivity_input_accounts()


def _add_target_accounts(view: ViewABC, tree_id: str, add_method: Callable):
    values: Tuple[dict] = view.tree_selected_values(tree_id)
    if values != ():
        indexes = view.get_selected_tree_item_indexes(tree_id)  # has to be before interactor's action
        shape_ids = tuple(value[1] for value in values)
        add_method(shape_ids)
        view.focus(tree_id)  # focus, then select
        view.select_tree_top_items_after_deleting_items(indexes, tree_id)


def remove_sensitivity_target(view: ViewABC, interactor: BoundaryInABC):
    tree = vm.tree_sensitivity_target_list
    remove_method = interactor.remove_sensitivity_target_accounts
    _remove_target_accounts(view, tree, remove_method)
    interactor.present_sensitivity_target_accounts()
    interactor.present_sensitivity_accounts()


def remove_sens_variable(view: ViewABC, interactor: BoundaryInABC):
    tree = vm.tree_sensitivity_variable_list
    remove_method = interactor.remove_sensitivity_variable_accounts
    _remove_target_accounts(view, tree, remove_method)
    interactor.present_sensitivity_variable_accounts()
    interactor.present_sensitivity_input_accounts()


def set_sensitivity_delta(view: ViewABC, interactor: BoundaryInABC):
    delta = view.get_value(vm.entry_sensitivity_delta)
    values: Tuple[dict] = view.tree_selected_values(vm.tree_sensitivity_variable_list)
    account_ids = tuple(value[1] for value in values)
    if Utilities.is_number(delta):
        interactor.set_sensitivity_deltas(account_ids, float(delta))
    else:
        interactor.feedback_user(f'Delta must be number.', 'error')
    interactor.present_sensitivity_variable_accounts()


def upon_check_btn_input_sheet(view: ViewABC, interactor: BoundaryInABC):
    value = view.get_value(vm.check_btn_input_sheet)
    if value:
        interactor.turn_on_insert_sheet_names_in_input_sheet()
        interactor.feedback_user('Input Sheet will have worksheet names.')
    else:
        interactor.turn_off_insert_sheet_names_in_input_sheet()
        interactor.feedback_user('Input Sheet will NOT have worksheet names.')


def _remove_target_accounts(view: ViewABC, tree_id: str, remove_method: Callable):
    values: Tuple[dict] = view.tree_selected_values(tree_id)
    indexes = view.get_selected_tree_item_indexes(tree_id)  # has to be before interactor's action
    shape_ids = tuple(value[1] for value in values)
    remove_method(shape_ids)
    view.focus(tree_id)  # focus, then select
    view.select_tree_top_items_after_deleting_items(indexes, tree_id)


def sensitivity_target_up(view: ViewABC, interactor: BoundaryInABC):
    _move_sensitivity_targets(interactor, -1, view)


def sensitivity_target_down(view: ViewABC, interactor: BoundaryInABC):
    _move_sensitivity_targets(interactor, 1, view)


def _move_sensitivity_targets(interactor: BoundaryInABC, shift: int, view: ViewABC):
    tree = vm.tree_sensitivity_target_list
    shift_method = interactor.shift_multiple_sensitivity_target_account
    _shift_tree_items(view, tree, shift, shift_method)
    interactor.present_sensitivity_target_accounts()
    interactor.present_sensitivity_accounts()


def _shift_tree_items(view: ViewABC, tree_id: str, shift: int, shift_method: Callable):
    indexes = view.get_selected_tree_item_indexes(tree_id)
    destinations = shift_method(indexes, shift)
    view.select_multiple_tree_items(tree_id, destinations)


def popup_input_entry(view: ViewABC, interactor: BoundaryInABC, mouse_cls: Type[MouseControllerABC]):
    margin_rate = 0.05
    nop = interactor.number_of_periods
    live_calculation = interactor.is_live_calculation_mode

    interactor.set_default_input_values_if_values_not_set()

    combobox_values = tuple(zip(interactor.input_accounts, interactor.input_names))
    view.add_widgets(vm.input_entry(combobox_values))
    view.switch_canvas(vm.ie_canvas_graph)

    vci = Vci(view)
    vci.set_margin_rate(margin_rate)

    view.bind_command_to_widget(vm.ie_btn_apply, lambda: apply_input_entry(view, interactor))
    view.bind_command_to_widget(vm.ie_btn_ok, lambda: ok_input_entry(view, interactor, vci))
    view.bind_command_to_widget(vm.ie_btn_next, lambda: next_input(view, interactor))
    view.bind_command_to_widget(vm.ie_btn_previous, lambda: previous_input(view, interactor))
    view.bind_command_to_widget(vm.ie_toplevel, lambda: vci.close(vm.ie_toplevel))
    view.bind_command_to_widget(vm.ie_check_btn, lambda: toggle_canvases(view))
    view.bind_command_to_widget(vm.ie_entry_min, lambda *_: apply_input_entry(view, interactor))
    view.bind_command_to_widget(vm.ie_entry_max, lambda *_: apply_input_entry(view, interactor))
    view.bind_command_to_widget(vm.ie_entry_uom, lambda *_: apply_input_entry(view, interactor))
    view.bind_command_to_widget(vm.ie_entry_digits, lambda *_: apply_input_entry(view, interactor))
    view.bind_command_to_widget(vm.ie_combo_box, lambda value: upon_ie_combobox_selection(value, interactor))
    view.bind_change_canvas_size(lambda event: upon_canvas_size_change(interactor, view, vci), vm.ie_canvas_graph)

    mouse = mouse_cls()

    mouse.configure(0, vci.graph_click_shape, mouse.is_left_click, {'save click coordinate': True})
    mouse.configure(10, lambda request: upon_mouse_drag(request, view, vci, nop, margin_rate), mouse.is_left_drag, {})
    mouse.configure(11, lambda request: upon_mouse_release(view, nop, margin_rate), mouse.is_left_release, {})
    view.bind_command_to_widget(vm.ie_canvas_graph, mouse.handle)
    view.bind_command_to_widget(vm.ie_canvas_slider, mouse.handle)

    ie = InputEntryController()
    vci.attach_to_input_entry(ie.handle)  # View holds InputEntry controller
    vci.attach_to_ie_close(lambda: upon_popup_close(view, interactor))
    ie.attach(lambda values: upon_input_entry_controller_command(view, interactor, vci, values, live_calculation))
    vci.set_widget_id_max(vm.ie_entry_max)
    vci.set_widget_id_min(vm.ie_entry_min)
    vci.set_widget_id_digit(vm.ie_entry_digits)
    vci.set_number_of_periods(interactor.number_of_periods)


def upon_popup_close(view: ViewABC, interactor: BoundaryInABC):
    view.switch_canvas(get_current_design_canvas(interactor))
    interactor.clear_input_being_modified()
    interactor.refresh_properties()


def upon_input_entry_controller_command(view: ViewABC, interactor: BoundaryInABC, vci: Vci, values: tuple,
                                        live_calculation: bool):
    try:
        digits = int(view.get_value(vm.ie_entry_digits))
    except ValueError:
        digits = None
    view.set_value(vm.ie_entry, Utilities.values_tuple_to_values_str(values, digits))

    by_slider = view.get_value(vm.ie_check_btn)

    if live_calculation:
        rounded_values = tuple(float(round(value, digits)) for value in values)
        original_canvas = vm.ie_canvas_slider if by_slider else vm.ie_canvas_graph

        view.switch_canvas(get_current_design_canvas(interactor))
        apply_to_input_account_being_modified(digits, interactor, rounded_values)
        interactor.calculate()
        view.switch_canvas(original_canvas)

    if by_slider:
        input_id = interactor.input_being_modified
        y_range = interactor.get_input_y_range(input_id)
        decimals = interactor.get_input_decimals(input_id)
        margin_rate = vci.margin_rate
        vc.draw_input_entry_graph(margin_rate, values, view, len(values), y_range, decimals)


def upon_mouse_drag(request, view: ViewABC, vci: Vci, nop: int, margin):
    by_slider = view.get_value(vm.ie_check_btn)
    if vci.get_clicked_canvas_item() is not None:
        vci.graph_move_shape(request, by_slider)
    elif not by_slider:
        line_data = {'mouse_line': {'coordinate_from': request['coordinates'][0],
                                    'coordinate_to': request['coordinates'][1],
                                    'line_color': 'black',
                                    'line_width': '2',
                                    'tags': ('mouse_line',),
                                    }}

        view.clear_canvas_shapes_by_tag('mouse_line')  # Only erase mouse_line, rather than all lines...
        view.add_line(line_data)  # ... and keep the rectangle sliders above grid line (so users can select slider)
        vc.draw_rectangle_sliders_per_mouse_line(margin, nop, view, request)
        vci.input_entry_control_by_graph()


def upon_mouse_release(view: ViewABC, nop, margin):
    by_slider = view.get_value(vm.ie_check_btn)
    if not by_slider:
        view.clear_canvas_shapes_by_tag('mouse_line')
        # vc.draw_grid_line(margin, nop, view)


def toggle_canvases(view: ViewABC):
    check_button = view.get_value(vm.ie_check_btn)
    if check_button:  # Slider on
        view.switch_canvas(vm.ie_canvas_slider)
        vc.draw_input_entry_slider(view)
    else:  # Slider off
        view.clear_canvas()
        view.switch_canvas(vm.ie_canvas_graph)


def upon_canvas_size_change(interactor: BoundaryInABC, view: ViewABC, vci: Vci):
    interactor.update_input_entry()

    canvas_height = view.get_canvas_height()
    margin = canvas_height * vci.margin_rate

    vci.set_canvas_max_y(canvas_height - margin)
    vci.set_canvas_min_y(margin)


def upon_ie_combobox_selection(id_name_sheet: str, interactor: BoundaryInABC):
    input_id = int(id_name_sheet.split(' ')[0])
    interactor.show_specified_input(input_id)


def apply_input_entry(view: ViewABC, interactor: BoundaryInABC):
    # Set Input Y Range
    min_str = view.get_value(vm.ie_entry_min)
    max_str = view.get_value(vm.ie_entry_max)
    min_ = Utilities.str_to_float(min_str, 0.0)
    max_ = Utilities.str_to_float(max_str, 0.0)
    y_range = float(min_), float(max_)
    interactor.set_input_y_range(y_range)

    # Add UOM
    unit_of_measure = view.get_value(vm.ie_entry_uom)
    input_id = int(view.get_value(vm.ie_combo_box).split(' ')[0])
    interactor.add_unit_of_measure(input_id, unit_of_measure)

    # Set Values and Decimals
    values_str = view.get_value(vm.ie_entry)
    digits_str = view.get_value(vm.ie_entry_digits)
    digits = Utilities.str_to_int(digits_str, 2)
    try:
        values = tuple(round(float(v), digits) for v in values_str.split(','))
    except ValueError:
        return
    apply_to_input_account_being_modified(digits, interactor, values)


def apply_to_input_account_being_modified(digits: int, interactor: BoundaryInABC, values: tuple):
    interactor.set_values_to_input_being_modified(values)
    interactor.set_decimals_to_input_being_modified(digits)


def ok_input_entry(view: ViewABC, interactor: BoundaryInABC, vci: Vci):
    apply_input_entry(view, interactor)
    vci.close(vm.ie_toplevel)
    view.switch_canvas(get_current_design_canvas(interactor))


def next_input(view: ViewABC, interactor: BoundaryInABC):
    apply_input_entry(view, interactor)
    interactor.show_next_input()


def previous_input(view: ViewABC, interactor: BoundaryInABC):
    apply_input_entry(view, interactor)
    interactor.show_previous_input()


def upon_format_selection(view: ViewABC, interactor: BoundaryInABC):
    shape_ids = interactor.selection_except_blanks
    format_selected: str = view.get_value(vm.cb_format)

    if format_selected == 'total':
        interactor.set_format_sub_total(shape_ids)
    elif format_selected == 'heading':
        interactor.set_format_heading(shape_ids)
    elif format_selected == 'None':
        interactor.remove_format(shape_ids)
    interactor.feedback_user(format_selected)


def upon_number_format_selection(view: ViewABC, interactor: BoundaryInABC):
    shape_ids = interactor.selection_except_blanks
    number_format_selected: str = view.get_value(vm.cb_num_format)

    if number_format_selected == 'whole number':
        interactor.set_whole_number(shape_ids)
    elif number_format_selected == '1-digit':
        interactor.set_one_digit(shape_ids)
    elif number_format_selected == '2-digit':
        interactor.set_two_digit(shape_ids)
    elif number_format_selected == '%':
        interactor.set_percent(shape_ids)
    interactor.feedback_user(number_format_selected)


def upon_check_box_vertical_account(view: ViewABC, interactor: BoundaryInABC):
    value: bool = view.get_value(vm.check_btn)
    if value:
        interactor.add_selection_to_vertical_accounts()
    else:
        interactor.remove_selection_from_vertical_accounts()


def add_vertical_reference(view: ViewABC, interactor: BoundaryInABC):
    shape_id = get_entry_as_integer(view)
    interactor.add_vertical_reference_to_selection(shape_id)


def remove_vertical_reference(view: ViewABC, interactor: BoundaryInABC):
    shape_id = get_entry_as_integer(view)
    interactor.remove_vertical_reference_to_selection(shape_id)


def get_entry_as_integer(view):
    entry_value = view.get_value(vm.entry_vertical_reference)
    try:
        shape_id = int(entry_value)
    except (TypeError, ValueError):
        shape_id = entry_value
    return shape_id


def btn_del_macro(view: ViewABC, interactor: BoundaryInABC):
    tree = vm.tree_macros
    try:
        pickle_names = tuple(values[1] for values in view.tree_selected_values(tree))
    except IndexError:
        return

    tree_item_position = _get_currently_selected_tree_position(view, tree)
    interactor.delete_macros(pickle_names, tree_item_position)


def upon_check_box_macro_mode(view: ViewABC, interactor: BoundaryInABC):
    value: bool = view.get_value(vm.check_btn_macro_mode)
    interactor.toggle_macro_mode(value)


def btn_merge_macro(view: ViewABC, interactor: BoundaryInABC):
    tree_values = view.tree_focused_values(vm.tree_macros)
    file_name = tree_values[1]
    interactor.merge_macro(file_name)
    interactor.feedback_user(f'Successfully loaded macro {file_name}!', 'success')


def btn_save_macro(view: ViewABC, interactor: BoundaryInABC):
    file_name = view.get_value(vm.entry_macro_name)
    feedback = interactor.save_macro(file_name)
    view.set_value(vm.entry_macro_name, _default_macro_entry)

    if feedback == 'success':
        interactor.feedback_user(f'Successfully saved new macro {file_name}!', 'success')
    else:
        interactor.feedback_user(feedback, 'error')


def btn_run_commands(view: ViewABC, interactor: BoundaryInABC):
    def observer(no: int, *_, **__):
        view.focus(vm.tree_commands, tree_item_position=no)

    interactor.run_macro(observer)
    view.focus(vm.tree_commands, tree_item_position=(0,))


def btn_run_commands_fast(view: ViewABC, interactor: BoundaryInABC):
    interactor.run_macro_fast()
    view.focus(vm.tree_commands, tree_item_position=(0,))


def btn_clear_commands(interactor: BoundaryInABC):
    interactor.clear_commands()


def btn_del_commands(view: ViewABC, interactor: BoundaryInABC):
    tree = vm.tree_commands
    indexes = view.get_selected_tree_item_indexes(tree)
    interactor.delete_commands(indexes)


def btn_copy_commands(view: ViewABC, interactor: BoundaryInABC):
    tree = vm.tree_commands

    indexes = view.get_selected_tree_item_indexes(tree)
    interactor.copy_commands(indexes)
    immediate_after = max(indexes) + 1
    interactor.paste_command(immediate_after)

    copied_items_indexes = tuple(range(immediate_after, immediate_after + len(indexes)))
    view.select_multiple_tree_items(tree, copied_items_indexes)


def btn_down_command(view: ViewABC, interactor: BoundaryInABC):
    selections_after_sort = _sort_commands(interactor, 1, view)
    interactor.present_commands(selections_after_sort)


def btn_up_command(view: ViewABC, interactor: BoundaryInABC):
    selections_after_sort = _sort_commands(interactor, -1, view)
    interactor.present_commands(selections_after_sort)


def btn_set_command_name(view: ViewABC, interactor: BoundaryInABC):
    action = interactor.set_command_name
    _change_command(action, view, interactor)


def btn_set_args(view: ViewABC, interactor: BoundaryInABC):
    action = interactor.set_macro_args
    _change_command(action, view, interactor)


def btn_set_kwargs(view: ViewABC, interactor: BoundaryInABC):
    action = interactor.set_macro_kwargs
    _change_command(action, view, interactor)


def _change_command(action, view: ViewABC, interactor: BoundaryInABC):
    user_input = view.get_value(vm.entry_macro_name)
    tree = vm.tree_commands
    indexes = view.get_selected_tree_item_indexes(tree)
    if len(indexes) == 0:
        interactor.feedback_user('Select Command to apply to.')
        return
    for index_ in indexes:
        action(index_, user_input, indexes)
    view.set_value(vm.entry_macro_name, _default_macro_entry)


def _sort_commands(interactor: BoundaryInABC, shift: int, view: ViewABC) -> tuple:
    tree = vm.tree_commands
    indexes = view.get_selected_tree_item_indexes(tree)
    return interactor.shift_multiple_commands(indexes, shift)


def check_nop_valid_entry(view: ViewABC, interactor: BoundaryInABC):
    entry = view.get_value(vm.entry_nop)
    try:
        int(entry)
    except ValueError:
        interactor.feedback_user(f'Number of period has to be an integer! {entry} is invalid!', 'error')


def apply_configuration_setting(view: ViewABC, interactor: BoundaryInABC):
    try:
        number_of_periods = int(view.get_value(vm.entry_nop))
    except ValueError:
        interactor.feedback_user('Number of period has to be an integer!', 'error')
        view.set_value(vm.entry_nop, 10)
        return
    interactor.set_number_of_periods(number_of_periods)


def upon_state_cleaner_check_button(view: ViewABC, interactor: BoundaryInABC):
    state_cleaner_is_activated = view.get_value(vm.check_btn_cleaner)
    if state_cleaner_is_activated:
        interactor.activate_state_cleaner()
    else:
        interactor.deactivate_state_cleaner()


def upon_live_calculation_check_button(view: ViewABC, interactor: BoundaryInABC):
    live_calculation_is_activated = view.get_value(vm.check_btn_live_calculation)
    if live_calculation_is_activated:
        interactor.activate_live_calculation()
    else:
        interactor.deactivate_live_calculation()


def create_project_folder(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC,
                          mouse: MouseControllerABC):
    folder_path = view.select_folder()
    interactor.create_project_folder(folder_path)
    view.set_value(vm.entry_project, folder_path)
    update_menu_bar(view, interactor, presenters, mouse)


def set_project_folder(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
    folder_path = view.get_value(vm.entry_project)
    interactor.create_project_folder(folder_path)
    update_menu_bar(view, interactor, presenters, mouse)


def decorator_entry_and_exit_point(f: Callable, interactor: BoundaryInABC, entry_by: str) -> Callable:
    def wrapper(*args, **kwargs):
        interactor.set_entry_point(entry_by)
        f(*args, **kwargs)
        interactor.exit_point(entry_by)

    return wrapper


def focus_on_shape_text_property(view: ViewABC):
    upon_fmd_switcher_properties(view)
    view.focus(vm.entry_text)


# Search Window
def popup_search_window(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
    v, i, p, m = view, interactor, presenters, mouse
    v.add_widgets(vm.search_window())
    entry = vm.entry_search
    tree = vm.tree_search

    all_groups_and_names = i.get_all_group_and_names

    v.bind_command_to_widget(vm.toplevel_search, lambda: close_search_window_properly(i, v))

    # Entry operations
    v.focus(entry)
    v.bind_entry_update(entry, lambda *_, **__: upon_search_entry_update(v, entry, all_groups_and_names))

    # Tree operations
    v.switch_tree(tree)
    view_model_tree = create_view_model_tree_search_filter(all_groups_and_names)
    v.update_tree(view_model_tree)  # glue column to frame
    v.update_tree({'tree_datas': {}})  # erase all data

    # Keyboard shortcut
    i.load_keyboard_shortcut(cns.keymap_search, keyboard_shortcuts.create_search_window_key_combos(i, v, p, m))
    v.set_keyboard_shortcut_handler(vm.toplevel_search, i.keyboard_shortcut_handler)


def execute_searched_command(view: ViewABC, interactor: BoundaryInABC):
    merge_method = interactor.merge_file
    merge_macro_method = _merge_macro
    _execute_searched_command(view, interactor, merge_method, merge_macro_method)


def execute_searched_command_alternative(view: ViewABC, interactor: BoundaryInABC):
    merge_method = interactor.merge_file_to_selected_sheet
    merge_macro_method = _execute_macro
    _execute_searched_command(view, interactor, merge_method, merge_macro_method)


def copy_searched_item_to_clip_board(view: ViewABC, interactor: BoundaryInABC):
    group, name = view.tree_selected_values(vm.tree_search)[0]
    try:
        subprocess.run("pbcopy", universal_newlines=True, input=name)
    except FileNotFoundError:
        subprocess.run("pbcopy", universal_newlines=True, input=name, shell=True)
    interactor.feedback_user(f'Clipboard = {name}', 'success')
    close_search_window_properly(interactor, view)


def _execute_searched_command(view: ViewABC, interactor: BoundaryInABC, merge_transaction_method: Callable,
                              merge_macro_method: Callable):
    try:
        group, name = view.tree_selected_values(vm.tree_search)[0]
    except IndexError:
        return
    if group == 'Transaction':
        merge_transaction_method(name)
    elif group == 'Macro':
        merge_macro_method(interactor, name)
    close_search_window_properly(interactor, view)


def _merge_macro(interactor: BoundaryInABC, name: str):
    interactor.merge_macro(name)
    interactor.feedback_user(f'Macro {name} merged.')


def _execute_macro(interactor: BoundaryInABC, name: str):
    i = interactor
    initial_commands = i.commands
    recording_mode = i.turned_on_macro_recording
    if recording_mode:
        i.stop_macro_recording()
    #################################
    # Below Overhead Command(s) not to be recorded
    i.clear_commands()
    i.merge_macro(name)
    #################################
    if recording_mode:
        i.start_macro_recording()
    if i.commands[0][0] == i.run_macro.__name__:
        i.set_commands(initial_commands)
    i.run_macro()
    if i.cleared_commands:
        i.clear_commands()  # Pattern 2 Clear Commands
    elif i.turned_on_macro_recording:
        i.stop_macro_recording()
        #################################
        # Below Overhead Command(s) not to be recorded
        i.clear_commands()
        #################################
        i.start_macro_recording()
    else:
        i.set_commands(initial_commands)  # Pattern 1 (base case, add transaction, etc)


def close_search_window_properly(interactor: BoundaryInABC, view: ViewABC):
    view.close(vm.toplevel_search)
    interactor.change_active_keymap(cns.keymap_design)  # closing toplevel is responsible for changing keymap


def upon_search_entry_update(view, entry, all_groups_and_names: tuple):
    tree_id = vm.tree_search
    view.switch_tree(tree_id)
    search_words = view.get_value(entry)
    if search_words == '':
        view.update_tree({'tree_datas': {}})  # erase all data
    else:
        rank_group = {0: [], 1: [], 2: [], 3: []}
        for group_and_name in all_groups_and_names:
            survived_filter, rank = auto_complete.search_filter(' '.join(group_and_name), search_words)
            if survived_filter:
                rank_group[rank].append(group_and_name)

        candidate_groups_and_names = tuple(rank_group[0] + rank_group[1] + rank_group[2] + rank_group[3])
        view_model_tree_ = create_view_model_tree_search_filter(candidate_groups_and_names)
        view.update_tree(view_model_tree_)


def create_view_model_tree_search_filter(candidate_groups_and_names: tuple) -> dict:
    c = candidate_groups_and_names
    headings = ('Group', 'Name')
    widths = (100, 100)
    tree_datas = [VM.create_tree_data('', f'{n}', '', (group, name), (), n == 0) for (n, (group, name)) in enumerate(c)]
    stretches = (False, True)
    view_model_tree = VM.create_view_model_tree(headings, widths, tree_datas, stretches, True, True)
    return view_model_tree


# F2 Entry
def popup_f2_entry(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
    v, i, p, m = view, interactor, presenters, mouse
    v.add_widgets(vm.f2_entry('Template Name'))
    entry = vm.entry_f2

    view.switch_status_bar(vm.f2_feedback)
    v.bind_command_to_widget(vm.toplevel_f2, lambda: close_f2_entry_properly(i, v))

    # Entry operations
    v.set_value(entry, i.first_selected_text)
    v.focus(entry)
    v.bind_entry_update(entry, lambda *_, **__: upon_f2_entry_update(v, i))
    v.bind_command_to_widget(vm.button_f2_ok, lambda *_, **__: upon_f2_ok(v, i))

    # Keyboard shortcut
    i.load_keyboard_shortcut(cns.keymap_f2_entry, keyboard_shortcuts.create_f2_entry_key_combos(i, v, p, m))
    v.set_keyboard_shortcut_handler(vm.toplevel_f2, i.keyboard_shortcut_handler_silent)


def close_f2_entry_properly(interactor: BoundaryInABC, view: ViewABC):
    view.switch_status_bar(vm.status_bar_id)
    view.close(vm.toplevel_f2)
    interactor.refresh_properties()
    interactor.change_active_keymap(cns.keymap_design)  # closing toplevel is responsible for changing keymap


def upon_f2_entry_update(view: ViewABC, interactor: BoundaryInABC):
    entry_text = view.get_value(vm.entry_f2)
    if interactor.selection_contains_constant:
        if not Utilities.is_number(entry_text):
            interactor.feedback_user(f'Entry must be number!{entry_text}', 'error')
    else:
        interactor.feedback_user(f'Entry = {entry_text}')


def upon_f2_ok(view: ViewABC, interactor: BoundaryInABC):
    entry_text = view.get_value(vm.entry_f2)
    interactor.set_property_to_selection('text', entry_text)
    close_f2_entry_properly(interactor, view)


# Popup Save Template
def popup_template_save(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
    _pop_up_template_name_entry('Set Template Name', 'Template Name', save_template, interactor, mouse, presenters,
                                view)


def popup_module_save(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
    _pop_up_template_name_entry('Set Module Name', 'Module Name', save_module, interactor, mouse, presenters, view)


def _pop_up_template_name_entry(title, default_value, save_method: Callable, interactor, mouse, presenters, view):
    v, i, p, m = view, interactor, presenters, mouse

    v.add_widgets(vm.template_name_entry(title, default_value))
    view.switch_status_bar(vm.template_name_feedback)
    v.bind_command_to_widget(vm.toplevel_template, lambda: close_template_entry_properly(i, v))

    entry = vm.entry_template_popup
    existing_templates = et = i.get_list_of_templates

    # Entry operations
    v.focus(entry)
    v.bind_entry_update(entry, lambda *_, **__: upon_template_entry_update(v, i, existing_templates))
    v.bind_command_to_widget(vm.button_template_popup, lambda *_, **__: upon_template_save_ok(v, i, save_method, et))

    # Keyboard shortcut
    i.load_keyboard_shortcut(cns.keymap_template_save, keyboard_shortcuts.create_template_save_key_combos(i, v, p, m))
    v.set_keyboard_shortcut_handler(vm.toplevel_template, i.keyboard_shortcut_handler_silent)


def close_template_entry_properly(interactor: BoundaryInABC, view: ViewABC):
    view.switch_status_bar(vm.status_bar_id)
    view.close(vm.toplevel_template)
    interactor.change_active_keymap(cns.keymap_design)  # closing toplevel is responsible for changing keymap


def upon_template_entry_update(view: ViewABC, interactor: BoundaryInABC, existing_templates=()):
    entry_text = view.get_value(vm.entry_template_popup)
    if entry_text in existing_templates:
        interactor.feedback_user(f'{entry_text} already exists.', 'error')
    else:
        interactor.feedback_user(f'Entry = {entry_text}')


def upon_template_save_ok(view: ViewABC, interactor: BoundaryInABC, save_method: Callable, existing_templates=()):
    entry_text = view.get_value(vm.entry_template_popup)
    existing_templates = existing_templates or interactor.get_list_of_templates
    if entry_text in existing_templates:
        if view.ask_yes_no(f'{entry_text} already exists.', f'Overwrite {entry_text}?'):
            save_method(entry_text, interactor, view)
            close_template_entry_properly(interactor, view)
        else:
            view.focus(vm.entry_template_popup)
    else:
        save_method(entry_text, interactor, view)
        close_template_entry_properly(interactor, view)


def save_template(entry_text: str, interactor: BoundaryInABC, view: ViewABC):
    view.switch_status_bar(vm.status_bar_id)
    interactor.save_state_to_file(entry_text)


def save_module(entry_text: str, interactor: BoundaryInABC, view: ViewABC):
    view.switch_status_bar(vm.status_bar_id)
    interactor.save_current_sheet_as_module(entry_text)


def upon_save_as_module(view: ViewABC, interactor: BoundaryInABC, entry_id):
    module_name = view.get_value(entry_id)
    interactor.save_current_sheet_as_module(module_name)
    interactor.feedback_user(f'Saved {module_name} as Module.', 'success')


# Popup Canvas Save
def popup_canvas_save(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
    v, i, p, m = view, interactor, presenters, mouse

    v.add_widgets(vm.canvas_save_setting('Canvas Save Setting'))
    view.switch_status_bar(vm.canvas_save_feedback)
    v.bind_command_to_widget(vm.toplevel_canvas_save_setting, lambda: close_canvas_save_setting_properly(i, v))

    # Entry operations
    e1 = vm.entry_total_frames
    e2 = vm.entry_canvas_save_height
    v.focus(e1)
    v.bind_entry_update(e1, lambda *_, **__: upon_canvas_save_setting_entry_update(v, i, e1))
    v.bind_entry_update(e2, lambda *_, **__: upon_canvas_save_setting_entry_update(v, i, e2))
    v.bind_command_to_widget(vm.btn_canvas_save, lambda *_, **__: upon_canvas_save_button(v, i))

    # Keyboard shortcut
    i.load_keyboard_shortcut(cns.keymap_canvas_save, keyboard_shortcuts.create_canvas_save_key_combos(i, v, p, m))
    v.set_keyboard_shortcut_handler(vm.toplevel_canvas_save_setting, i.keyboard_shortcut_handler_silent)


def close_canvas_save_setting_properly(interactor: BoundaryInABC, view: ViewABC):
    view.switch_status_bar(vm.status_bar_id)
    view.close(vm.toplevel_canvas_save_setting)
    interactor.change_active_keymap(cns.keymap_design)  # closing toplevel is responsible for changing keymap


def upon_canvas_save_setting_entry_update(view: ViewABC, interactor: BoundaryInABC, entry):
    entry_text = view.get_value(entry)
    _validate_canvas_save_entry(entry_text, interactor)


def _validate_canvas_save_entry(entry_text, interactor):
    if not Utilities.is_number(entry_text):
        interactor.feedback_user(f'Must be integer. {entry_text} is invalid', 'error')
        return False
    else:
        interactor.feedback_user(f'Entry = {entry_text}')
        return True


def upon_canvas_save_button(view: ViewABC, interactor: BoundaryInABC, ):
    number_of_images = view.get_value(vm.entry_total_frames)
    travel_range = view.get_value(vm.entry_canvas_save_height)
    if not _validate_canvas_save_entry(travel_range, interactor):
        return
    if not _validate_canvas_save_entry(number_of_images, interactor):
        return
    close_canvas_save_setting_properly(interactor, view)
    interactor.save_slider_images(int(number_of_images), int(travel_range), -1)


# Menu bar
def update_menu_bar_recent_projects(menu_bar_model: dict, view: ViewABC, interactor: BoundaryInABC,
                                    presenters: PresentersABC, mouse: MouseControllerABC):
    v, p, i, m = view, presenters, interactor, mouse
    project_paths = interactor.recent_project_paths
    project_names = tuple(path.split('/')[-1] for path in project_paths)
    commands = tuple(lambda p=path: set_project_folder_path(p, v, i, p, m) for path in project_paths)
    commands_to_load_projects = dict(zip(project_names, commands))
    menu_bar_model['File']['Recent Projects'].update(commands_to_load_projects)


def update_menu_bar(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
    v, p, i, m = view, presenters, interactor, mouse
    menu_bar_model = menu_bar.create_menu_bar_model(interactor, view, presenters, mouse)
    update_menu_bar_recent_projects(menu_bar_model, v, i, p, m)
    view.update_menu_bar(menu_bar_model)


def hide_canvas_commands_from_menubar(interactor, mouse, presenters, view):
    menu_bar_model = menu_bar.create_menu_bar_model(interactor, view, presenters, mouse)
    del menu_bar_model['Canvas']
    del menu_bar_model['Analyze']
    update_menu_bar_recent_projects(menu_bar_model, view, interactor, presenters, mouse)
    view.update_menu_bar(menu_bar_model)


def set_project_folder_path(path, view: ViewABC, interactor: BoundaryInABC, presenter: PresentersABC,
                            mouse: MouseControllerABC):
    interactor.set_project_folder_path(path)
    view.set_value(vm.entry_project, path)
    update_menu_bar(view, interactor, presenter, mouse)


def properly_close_app(interactor: BoundaryInABC, view: ViewABC):
    interactor.tear_down()
    view.quit()


def move_selected_worksheets(interactor: BoundaryInABC, view: ViewABC, shift: int):
    indexes = view.get_selected_tree_item_indexes(vm.tree_worksheets)
    new_selections_index = interactor.change_sheet_order(indexes, shift)
    if new_selections_index != ():
        view.select_multiple_tree_items(vm.tree_worksheets, new_selections_index)


def move_selected_worksheets_right(interactor: BoundaryInABC, view: ViewABC):
    tree = vm.tree_worksheets
    worksheet_names = tuple(name for (no, name) in view.get_value(tree)['all_values'])
    children_indexes = view.get_selected_tree_item_indexes(tree)

    above_sheet_names = []
    child_sheet_names = []
    for child_index in children_indexes:
        if child_index > 0:
            above_sheet_names.append(worksheet_names[child_index - 1])
            child_sheet_names.append(worksheet_names[child_index])

    interactor.add_worksheet_parent_child_relationships(above_sheet_names, child_sheet_names)
    interactor.present_update_worksheets()


def move_selected_worksheets_left(interactor: BoundaryInABC, view: ViewABC):
    tree = vm.tree_worksheets
    worksheet_names = tuple(name for (no, name) in view.get_value(tree)['all_values'])
    children_indexes = view.get_selected_tree_item_indexes(tree)
    child_sheet_names = tuple(worksheet_names[child_index] for child_index in children_indexes)
    interactor.remove_worksheet_parent_child_relationships(child_sheet_names)
    interactor.present_update_worksheets()


def upon_add_worksheet(view: ViewABC, view_model_: dict, mouse: MouseControllerABC):
    view_model = view_model_.get('view_model')
    canvas_id = view_model_.get('canvas_id')
    if not view.widget_exists(canvas_id):
        view.add_widgets(view_model)
        view.bind_command_to_widget(canvas_id, mouse.handle)
        upon_select_worksheet(view, view_model_)


def upon_select_worksheet(view: ViewABC, view_model_: dict):
    frame_canvas = view_model_.get('frame_canvas')
    canvas_id = view_model_.get('canvas_id')
    update = view_model_.get('update', False)
    view.switch_frame(frame_canvas)
    view.switch_canvas(canvas_id)
    if update:
        view.update()


def upon_delete_worksheet(view: ViewABC, view_model_: dict):
    frame_canvas = view_model_.get('frame_canvas')
    canvas_id = view_model_.get('canvas_id')
    view.remove_widget(frame_canvas)
    view.remove_widget(canvas_id)


def focus_on_canvas(view: ViewABC):
    view.focus(vm.button_1)


def toggle_relay_x_position(view: ViewABC, interactor: BoundaryInABC):
    value = view.get_value(vm.check_btn_relay_right_end)
    if value:
        interactor.set_relay_x_to_right_end()
    else:
        interactor.set_relay_x_to_right()


def set_breakdown_account(view: ViewABC, interactor: BoundaryInABC):
    value = view.get_value(vm.check_btn_breakdown_account)
    if value:
        interactor.add_selection_to_breakdown_accounts()
    else:
        interactor.remove_selection_from_breakdown_accounts()


def upon_commands_right_click(interactor: BoundaryInABC, view: ViewABC, values):
    row, col, value = values
    if value is None:
        return  # Do nothing
    col_n = col - 1
    if col_n in (0, 2):
        value_str = interactor.macro_commands[row][col_n]
    else:
        arg_str = ''
        for arg in interactor.macro_commands[row][col_n]:
            if arg.__class__ in (tuple, list):
                r = '('
                for a in arg:
                    r += f'{a},'
                arg_str += f'{r[:-1]}),'
            else:
                arg_str += f'{arg},'
        value_str = arg_str

    if (len(value_str) > 0) and (value_str[-1] == ','):
        value_str = value_str[:-1]
    view.set_value(vm.entry_macro_name, value_str)
    view.focus(vm.entry_macro_name)


def upon_macro_list_right_click(view: ViewABC, values):
    row, col, value = values
    if value is None:
        return  # Do nothing
    view.set_value(vm.entry_macro_name, value)
    view.focus(vm.entry_macro_name)


def popup_wizard(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC, mouse: MouseControllerABC):
    from ..gui_model_builder import GUI
    from view_tkinter import tk_interface as intf
    options = intf.top_level_options('Input Setting', (500, 600))
    toplevel_id = 'gui_model_top_level'
    view_model = [intf.widget_model('root', toplevel_id, 'toplevel', 0, 0, 0, 0, 'nsew', **options)]
    view.add_widgets(view_model)

    def upon_closing():
        close_wizard_window_properly(toplevel_id, i, v, p, m)

    gui = GUI(toplevel_id, view, interactor, upon_closing)
    gui.add_initial_widgets()

    i, v, p, m = interactor, view, presenters, mouse

    view.bind_command_to_widget(toplevel_id, upon_closing)

    menu_bar_model = menu_bar.create_menu_bar_model(i, v, p, m)
    menu_bar_model['Wizard'] = {
        'Save State': lambda: save_wizard_state(interactor, view, gui),
        'Load State': lambda: load_wizard_state(interactor, view, gui),
    }
    update_menu_bar_recent_projects(menu_bar_model, v, i, p, m)
    view.update_menu_bar(menu_bar_model)


def close_wizard_window_properly(toplevel_id, interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                                 mouse: MouseControllerABC):
    view.close(toplevel_id)
    update_menu_bar(view, interactor, presenters, mouse)
    interactor.change_active_keymap(cns.keymap_design)  # closing toplevel is responsible for changing keymap


def save_wizard_state(interactor: BoundaryInABC, view: ViewABC, gui):
    path = view.select_save_file({interactor.save_path})
    interactor.save_any_data_as_pickle(path, gui.data_structure)
    interactor.feedback_user(f'{path} saved.', 'success')


def load_wizard_state(interactor: BoundaryInABC, view: ViewABC, gui):
    path = view.select_open_file(interactor.save_path)
    data_structure = interactor.get_pickle_from_file_system(path)
    gui.load_state(data_structure)
