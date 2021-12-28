import os_identifier
from view_tkinter import ViewModels as Vm
from view_tkinter import tk_interface as intf

grid_length = 5
button_width = 1.1 if os_identifier.is_mac else 9
ew = 5
pad_xy = (1, 1)
format_values = ('None', 'total', 'heading')
number_format_values = ('whole number', '1-digit', '2-digit', '%')

root = 'root'

canvas_id = 'canvas'
canvas_template = 'canvas_template'

entry_id = 'entry_to_focus'
entry_template = 'entry_template_name'
entry_text = 'entry text'
entry_x = 'entry x'
entry_y = 'entry y'
entry_width = 'entry width'
entry_height = 'entry height'
entry_sheet = 'entry property worksheet sheet'
entry_delta_x = 'entry_delta_x'
entry_delta_y = 'entry_delta_y'
entry_shape_id = 'entry_shape_id'
entry_sheet_name = 'entry_sheet_name'
entry_conn_id = 'entry_conn_id'
entry_vertical_reference = 'entry_vertical_reference'
entry_macro_name = 'entry_macro_name'
entry_project = 'entry_project'
entry_nop = 'entry_nop'

status_bar_id = 'status_bar'

tree_pickle_files_id = 'tree_pickle_files'
tree_account_order = 'tree_account_list'
tree_worksheets = 'tree_worksheets'
tree_connections = 'tree_connections'
tree_commands = 'tree_commands'
tree_macros = 'tree_macros'

textbox_rpe = 'textbox_rpe'

radio_btn_conn = 'connections_radio_buttons'
int_var_conn = 'connection_radio_button_int_var'

cb_format = 'format'
cb_num_format = 'num_format'
check_btn_macro_mode = 'check_btn_macro_mode'
check_btn = 'check button vertical'
check_btn_cleaner = 'check_btn_cleaner'
check_btn_live_calculation = 'check_btn_live_calc'

btn_undo = 'undo'
btn_redo = 'redo'
button_1 = 'btn_1'
btn_erase_shape = 'btn_2'
button_3 = 'btn_3'
button_4 = 'btn_4'
btn_tree_ac_up = 'btn_6'
btn_tree_ac_down = 'btn_7'
button_8 = 'btn_8'
button_9 = 'btn_9'
button_10 = 'btn_10'
button_11 = 'btn_11'
btn_excel = 'btn_12'
button_13 = 'btn_13'
button_14 = 'btn_14'
button_15 = 'btn_15'
button_16 = 'btn_16'
button_17 = 'btn_17'
button_18 = 'btn_18'
button_19 = 'btn_19'
button_20 = 'btn_20'
btn_reset = 'btn_21'
button_22 = 'btn_22'
button_23 = 'btn_23'
button_24 = 'btn_24'
button_25 = 'btn_25'
btn_swtch_ac = 'btn_26'
btn_swtch_property = 'btn_27'
btn_op_bb = 'btn_28'
btn_op_max = 'btn_29'
btn_op_min = 'btn_30'
btn_op_ave = 'btn_31'
btn_op_le = 'btn_op_le'
btn_op_lt = 'btn_op_lt'
btn_op_ge = 'btn_op_ge'
btn_op_gt = 'btn_op_gt'
btn_op_eq = 'btn_op_eq'
btn_op_pw = 'btn_op_pw'
btn_op_abs = 'btn_op_abs'
btn_analyze = 'btn_analyze'
btn_switch_sheet = 'btn_32'
btn_export_accounts = 'btn_33'
btn_del_sheet = 'btn_34'
btn_add_sheet = 'btn_35'
btn_import_accounts = 'btn_36'
btn_sheet_name = 'btn_37'
btn_ie = 'btn_38'
btn_save_module = 'btn_39'
btn_switch_conn = 'btn_40'
btn_add_conn = 'btn_41'
btn_del_conn = 'btn_42'
btn_add_vref = 'btn_add_v_ref'
btn_remove_v_ref = 'btn_remove_v_ref'
btn_del_macro = 'btn_del_macro'
btn_merge_macro = 'btn_merge_macro'
btn_save_macro = 'btn_save_macro'
btn_run_commands = 'btn_run_commands'
btn_clear_commands = 'btn_clear_commands'
btn_del_commands = 'btn_del_commands'
btn_copy_commands = 'btn_copy_commands'
btn_down_command = 'btn_down_command'
btn_up_command = 'btn_up_command'
btn_set_command_name = 'btn_set_command_name'
btn_set_args = 'btn_set_args'
btn_set_kwargs = 'btn_set_kwargs'
btn_project = 'btn_project'
btn_setting_ok = 'btn_setting_ok'
kw_macro_buttons = {'btn_del_macro': btn_del_macro,
                    'btn_merge_macro': btn_merge_macro,
                    'btn_save_macro': btn_save_macro,
                    'btn_run_commands': btn_run_commands,
                    'btn_clear_commands': btn_clear_commands,
                    'btn_del_commands': btn_del_commands,
                    'btn_copy_commands': btn_copy_commands,
                    'btn_down_command': btn_down_command,
                    'btn_up_command': btn_up_command,
                    'btn_set_command_name': btn_set_command_name,
                    'btn_set_args': btn_set_args,
                    'btn_set_kwargs': btn_set_kwargs,
                    'tree_commands': tree_commands,
                    'tree_macros': tree_macros,
                    'check_btn_macro_mode': check_btn_macro_mode,
                    'entry_macro_name': entry_macro_name,
                    'btn_width': button_width,
                    }
kw_setting = {
    'btn_project': btn_project,
    'btn_setting_ok': btn_setting_ok,
    'entry_project': entry_project,
    'entry_nop': entry_nop,
    'check_btn_cleaner': check_btn_cleaner,
    'check_btn_live_calculation': check_btn_live_calculation,
}

paned_window_btn = 'paned_window_design_button'
fr_paned_window_btn_left = 'fr_pwl'
fr_paned_window_btn_right = 'fr_pwr'

fr_root = 'frame_root'
fr_switch = 'frame_switch'
fr_fmd = 'frame_FMD'
fr_state = 'frame_state'
fr_macro = 'frame_macro'
fr_setting = 'frame_setting'
fr_template = 'frame_pickle_loader'
fr_all_save = 'frame_all_save'
fr_align = 'frame_align'
fr_align2 = 'frame_align2'
fr_width = 'frame_shape_width'
fr_switch2 = 'frame_switch2'
fr_btn_swithcer2 = 'fr_btn_swithcer2'

fr_menu = 'frame_menu'
fr_entry = 'frame_entry'
fr_button = 'frame_button'
fr_canvas = 'frame_canvas'
fr_operators = 'frame_operators'
fr_del_load_save = 'frame_delete_load_save'
fr_unredo = 'frame_undo_redo'
fr_tobenamed = 'frame_to_be_named'
fr_account_order = 'frame_account_order'
fr_tree_btn = 'frame_account_order_buttons'
fr_sh_name = 'frame_worksheets_name'
fr_connection_name = 'frame_connection_name'
fr_tree_btn2 = 'frame_worksheets_buttons'
fr_conn_btn = 'frame_connection_buttons'
fr_conn_radio_btn = 'frame_connection_radio_buttons'
fr_property = 'frame_property'
fr_vertical_ref = 'frame_vertical_ref'
fr_worksheets = 'frame_worksheets'
fr_connection = 'frame_connection'
fr_radio_btn_conn = 'fr_radio_button_connection'

fr_toplevel = 'frame_toplevel'
fr_tree_ac_import = 'frame_toplevel_left'
fr_tree_canvas = 'frame_toplevel_canvas'

f_root_rc = ((1,), (1,)), ((0,), (1,))
f_menu_rc = ((0,), (1,)), ((0, 2,), (1, 1,))
f_0 = ((0,), (1,)), ((0,), (1,))
f_1 = ((0,), (1,)), ((1,), (1,))
f_0_0 = ((0,), (1,)), ((0,), (1,))
f_2_1 = ((2,), (1,)), ((1,), (1,))
f_0_1 = ((0,), (1,)), ((1,), (1,))
f_100_0 = ((100,), (1,)), ((0,), (1,))

f_btn_rc = ((10,), (1,)), ((0,), (1,))

f_op_rc = ((0,), (1,)), ((0, 1, 2, 3), (1, 1, 1, 1))
f_0123 = ((0,), (1,)), ((0, 1, 2, 3), (1, 1, 1, 1))
f_012 = ((0,), (1,)), ((0, 1, 2,), (1, 1, 1,))
f_urdo_rc = ((0,), (1,)), ((0, 1,), (1, 1,))
f_base_rc = ((0,), (1,)), ((0,), (1,))
f_property_rc = ((20,), (1,)), ((0,), (1,))


def start_view_model_factory() -> list:
    f = intf.widget_model

    # view model
    view_model = [f(root, fr_root, 'frame', 0, 0, 0, 0, 'nsew', **intf.frame_options(*f_root_rc)), ]
    root_frame = [
        f(fr_root, fr_menu, 'frame', 0, 0, 0, 0, 'nsew', **intf.frame_options(*f_menu_rc)),
        f(fr_root, fr_switch, 'frame', 1, 1, 0, 0, 'nsew', **intf.frame_options(*f_0)),
        f(fr_root, status_bar_id, 'label', 2, 2, 0, 0, 'nsew', **{'text': 'status tag_bar:'}),
    ]

    # Menu
    menu = Vm.main_menu_contents(fr_menu, button_width)
    common_padding = (10, 0)
    op_paned_window_button = intf.paned_window_options(False, (fr_paned_window_btn_left, fr_paned_window_btn_right))
    switchable1 = [
        f(fr_switch, fr_setting, 'frame', 0, 0, 0, 0, 'nsew', common_padding, **intf.frame_options(*f_100_0)),
        f(fr_switch, fr_macro, 'frame', 0, 0, 0, 0, 'nsew', common_padding, **intf.frame_options(*f_0_0)),
        f(fr_switch, fr_template, 'frame', 0, 0, 0, 0, 'nsew', common_padding, **intf.frame_options(*f_0_0)),
        f(fr_switch, fr_state, 'frame', 0, 0, 0, 0, 'nsew', common_padding, **intf.frame_options(*f_1)),
        f(fr_switch, fr_fmd, 'frame', 0, 0, 0, 0, 'nsew', common_padding, **intf.frame_options(*f_0)),
        f(fr_fmd, paned_window_btn, 'paned_window', 0, 0, 0, 0, 'nsew', common_padding, **op_paned_window_button),
    ]

    fmd_root = [
        f(fr_paned_window_btn_left, fr_button, 'frame', 0, 0, 0, 0, 'nsew', **intf.frame_options(*f_btn_rc)),
        f(fr_paned_window_btn_right, fr_canvas, 'frame', 0, 0, 0, 0, 'nsew', **intf.frame_options(*f_0)),
    ]
    fmd_button = [
        f(fr_button, fr_entry, 'frame', 0, 0, 0, 0, 'nsew', **intf.frame_options(*f_base_rc)),
        f(fr_button, fr_operators, 'frame', 1, 1, 0, 0, 'nsew', **intf.frame_options(*f_op_rc)),
        f(fr_button, fr_del_load_save, 'frame', 2, 2, 0, 0, 'nsew', **intf.frame_options(*f_0123)),
        f(fr_button, fr_unredo, 'frame', 3, 3, 0, 0, 'nsew', **intf.frame_options(*f_0123)),

        f(fr_button, fr_tobenamed, 'frame', 5, 5, 0, 0, 'nsew', **intf.frame_options(*f_0123)),
        f(fr_button, fr_align, 'frame', 7, 7, 0, 0, 'nsew', **intf.frame_options(*f_0123)),
        f(fr_button, fr_align2, 'frame', 8, 8, 0, 0, 'nsew', **intf.frame_options(*f_0123)),
        f(fr_button, fr_width, 'frame', 9, 9, 0, 0, 'nsew', **intf.frame_options(*f_0123)),
        f(fr_button, fr_switch2, 'frame', 10, 10, 0, 0, 'nsew', (3, 3), **intf.frame_options(*f_base_rc)),
        f(fr_button, fr_btn_swithcer2, 'frame', 11, 11, 0, 0, 'nsew', **intf.frame_options(*f_012)),
    ]
    fmd_entry_shape_name = Vm.entry_and_button(fr_entry, entry_id, ew, button_1, 'Add', button_width, 'Account Name')
    operator_buttons = Vm.operator_buttons(fr_operators, button_width)
    fmd_button_del_load_save = [
        f(fr_del_load_save, btn_op_bb, 'button', 0, 0, 0, 0, 'nsew', **{'text': 'BB', 'width': button_width}),
        f(fr_del_load_save, btn_op_max, 'button', 0, 0, 1, 1, 'nsew', **{'text': 'max', 'width': button_width}),
        f(fr_del_load_save, btn_op_min, 'button', 0, 0, 2, 2, 'nsew', **{'text': 'min', 'width': button_width}),
        f(fr_del_load_save, btn_op_ave, 'button', 0, 0, 3, 3, 'nsew', **{'text': 'ave', 'width': button_width}),
        f(fr_del_load_save, btn_op_le, 'button', 1, 1, 0, 0, 'nsew', **{'text': '<=', 'width': button_width}),
        f(fr_del_load_save, btn_op_lt, 'button', 1, 1, 1, 1, 'nsew', **{'text': '<', 'width': button_width}),
        f(fr_del_load_save, btn_op_ge, 'button', 1, 1, 2, 2, 'nsew', **{'text': '>=', 'width': button_width}),
        f(fr_del_load_save, btn_op_gt, 'button', 1, 1, 3, 3, 'nsew', **{'text': '>', 'width': button_width}),
        f(fr_del_load_save, btn_op_eq, 'button', 2, 2, 0, 0, 'nsew', **{'text': '=', 'width': button_width}),
        f(fr_del_load_save, btn_op_pw, 'button', 2, 2, 1, 1, 'nsew', **{'text': '^', 'width': button_width}),
        f(fr_del_load_save, btn_op_abs, 'button', 2, 2, 2, 2, 'nsew', **{'text': 'abs', 'width': button_width}),
        f(fr_del_load_save, btn_analyze, 'button', 2, 2, 3, 3, 'nsew', **{'text': 'ana', 'width': button_width}),
    ]

    undo_redo_buttons = [
        f(fr_unredo, btn_undo, 'button', 0, 0, 0, 0, 'nsew', **{'text': '↩️', 'width': button_width}),
        f(fr_unredo, btn_redo, 'button', 0, 0, 1, 1, 'nsew', **{'text': '↪️', 'width': button_width}),
        f(fr_unredo, btn_reset, 'button', 0, 0, 2, 2, 'nsew', **{'text': 'New', 'width': button_width}),
        f(fr_unredo, button_9, 'button', 0, 0, 3, 3, 'nsew', **{'text': 'Rel', 'width': button_width}),
    ]
    tbn = [
        f(fr_tobenamed, btn_erase_shape, 'button', 0, 0, 0, 0, 'nsew', **{'text': '❌', 'width': button_width}),
        f(fr_tobenamed, btn_excel, 'button', 0, 0, 1, 1, 'nsew', **{'text': 'XL', 'width': button_width}),
        f(fr_tobenamed, btn_ie, 'button', 0, 0, 2, 2, 'nsew', **{'text': 'IE', 'width': button_width}),
        f(fr_tobenamed, btn_save_module, 'button', 0, 0, 3, 3, 'nsew', **{'text': 'Mod', 'width': button_width}),
    ]
    groups_of_buttons = fmd_entry_shape_name + fmd_button_del_load_save + operator_buttons + undo_redo_buttons + tbn

    switchable2 = [
        f(fr_switch2, fr_property, 'frame', 0, 0, 0, 0, 'nsew', **intf.frame_options(*f_property_rc)),
        f(fr_switch2, fr_account_order, 'frame', 0, 0, 0, 0, 'nsew', **intf.frame_options(*f_base_rc)),
        f(fr_switch2, fr_worksheets, 'frame', 0, 0, 0, 0, 'nsew', **intf.frame_options(*f_base_rc)),
        f(fr_switch2, fr_connection, 'frame', 0, 0, 0, 0, 'nsew', **intf.frame_options(*f_base_rc, propagate=False)),
    ]

    # Worksheets
    tree_sheets = Vm.tree_view(fr_worksheets, tree_worksheets)
    tree_sheets.append(
        f(fr_worksheets, fr_sh_name, 'frame', 1, 1, 0, 0, 'nsew', **intf.frame_options(*f_0)),
    )
    tree_sheets.append(
        f(fr_worksheets, fr_tree_btn2, 'frame', 2, 2, 0, 0, 'nsew', **intf.frame_options(*f_0123)),
    )
    sheet_entry = Vm.entry_and_button(fr_sh_name, entry_sheet_name, ew, btn_sheet_name, 'OK', button_width)
    tree_ws_btns = [
        f(fr_tree_btn2, btn_del_sheet, 'button', 0, 0, 0, 0, 'nsew', **{'text': '❌', 'width': button_width}),
        f(fr_tree_btn2, btn_add_sheet, 'button', 0, 0, 1, 1, 'nsew', **{'text': '➕', 'width': button_width}),
        f(fr_tree_btn2, btn_export_accounts, 'button', 0, 0, 2, 2, 'nsew', **{'text': 'paste', 'width': button_width}),
        f(fr_tree_btn2, btn_import_accounts, 'button', 0, 0, 3, 3, 'nsew', **{'text': 'copy️', 'width': button_width}),
    ]

    # ConnectionIDs
    tree_connection = Vm.tree_view(fr_connection, tree_connections)
    rb_options = intf.radio_button_options(fr_radio_btn_conn, int_var_conn, ('ID', 'Socket', 'Plug'))
    tree_radio_buttons = [
        f(fr_connection, radio_btn_conn, 'radio_button', 1, 1, 0, 0, 'nsew', **rb_options)
    ]
    tree_connection.append(
        f(fr_connection, fr_connection_name, 'frame', 2, 2, 0, 0, 'nsew', **intf.frame_options(*f_0)),
    )

    tree_connection.append(
        f(fr_connection, fr_conn_radio_btn, 'frame', 3, 3, 0, 0, 'nsew', **intf.frame_options(*f_0123)),
    )
    tree_connection.append(
        f(fr_connection, fr_conn_btn, 'frame', 4, 4, 0, 0, 'nsew', **intf.frame_options(*f_0123)),
    )

    connection_entry = Vm.entry_and_button(fr_connection_name, entry_conn_id, ew, btn_add_conn, '➕', button_width)
    tree_connection_btns = [
        f(fr_conn_btn, btn_del_conn, 'button', 0, 0, 0, 0, 'nsew', **{'text': '❌', 'width': button_width}),
    ]

    # Accounts
    tree_accounts = Vm.tree_view(fr_account_order, tree_account_order)
    tree_accounts.append(
        f(fr_account_order, fr_tree_btn, 'frame', 1, 1, 0, 0, 'nsew', **intf.frame_options(*f_012))
    )
    tree_btns = [
        f(fr_tree_btn, btn_tree_ac_up, 'button', 0, 0, 0, 0, 'nsew', **{'text': '⬆️', 'width': button_width}),
        f(fr_tree_btn, btn_tree_ac_down, 'button', 0, 0, 1, 1, 'nsew', **{'text': '⬇️', 'width': button_width}),
        f(fr_tree_btn, button_8, 'button', 0, 0, 2, 2, 'nsew', **{'text': '[_]', 'width': button_width}),
    ]

    # Properties
    property_setter = [
        f(fr_property, 'label text', 'label', 3, 3, 0, 0, 'nse', **{'text': 'Text:'}),
        f(fr_property, 'label x', 'label', 4, 4, 0, 0, 'nse', **{'text': 'x:'}),
        f(fr_property, 'label y', 'label', 5, 5, 0, 0, 'nse', **{'text': 'y:'}),
        f(fr_property, 'label width', 'label', 6, 6, 0, 0, 'nse', **{'text': 'width:'}),
        f(fr_property, 'label height', 'label', 7, 7, 0, 0, 'nse', **{'text': 'height:'}),
        f(fr_property, 'label sheet', 'label', 8, 8, 0, 0, 'nse', **{'text': 'Sheet:'}),
        f(fr_property, 'label delta_x', 'label', 9, 9, 0, 0, 'nse', **{'text': 'Δx:'}),
        f(fr_property, 'label delta_y', 'label', 10, 10, 0, 0, 'nse', **{'text': 'Δy:'}),
        f(fr_property, 'label shape_id', 'label', 11, 11, 0, 0, 'nse', **{'text': 'id:'}),
        f(fr_property, 'label format', 'label', 12, 12, 0, 0, 'nse', **{'text': 'Format'}),
        f(fr_property, 'label num_format', 'label', 13, 13, 0, 0, 'nse', **{'text': '#'}),
        f(fr_property, 'label vertical', 'label', 14, 14, 0, 0, 'nse', **{'text': 'Vertical:'}),

        f(fr_property, entry_text, 'entry', 3, 3, 1, 1, 'nswe'),
        f(fr_property, entry_x, 'entry', 4, 4, 1, 1, 'nswe'),
        f(fr_property, entry_y, 'entry', 5, 5, 1, 1, 'nswe'),
        f(fr_property, entry_width, 'entry', 6, 6, 1, 1, 'nswe'),
        f(fr_property, entry_height, 'entry', 7, 7, 1, 1, 'nswe'),
        f(fr_property, entry_sheet, 'entry', 8, 8, 1, 1, 'nswe'),

        f(fr_property, entry_delta_x, 'entry', 9, 9, 1, 1, 'nswe'),
        f(fr_property, entry_delta_y, 'entry', 10, 10, 1, 1, 'nswe'),
        f(fr_property, entry_shape_id, 'entry', 11, 11, 1, 1, 'nswe'),

        f(fr_property, cb_format, 'combo_box', 12, 12, 1, 1, 'nswe', **{'values': format_values}),
        f(fr_property, cb_num_format, 'combo_box', 13, 13, 1, 1, 'nswe', **{'values': number_format_values}),

        f(fr_property, fr_vertical_ref, 'frame', 14, 14, 1, 1, 'nswe', **intf.frame_options(*f_0)),
        f(fr_vertical_ref, check_btn, 'check_button', 0, 0, 0, 0, 'nswe'),
        f(fr_vertical_ref, entry_vertical_reference, 'entry', 0, 0, 1, 1, 'nswe', **{'width': 5}),
        f(fr_vertical_ref, btn_add_vref, 'button', 0, 0, 2, 2, 'nswe', **{'text': 'Add', 'width': button_width}),
        f(fr_vertical_ref, btn_remove_v_ref, 'button', 0, 0, 3, 3, 'nswe', **{'text': 'Rem', 'width': button_width}),

    ]
    align_btns = Vm.create_d_pad_model(fr_align, (button_13, button_14, button_15, button_16), button_width)
    switcher2_buttons = [
        f(fr_btn_swithcer2, btn_swtch_ac, 'button', 0, 0, 0, 0, 'nsew', **{'text': 'Ac', 'width': button_width}),
        f(fr_btn_swithcer2, btn_swtch_property, 'button', 0, 0, 1, 1, 'nsew', **{'text': 'Pr', 'width': button_width}),
        f(fr_btn_swithcer2, btn_switch_sheet, 'button', 0, 0, 2, 2, 'nsew', **{'text': 'WS', 'width': button_width}),
        f(fr_btn_swithcer2, btn_switch_conn, 'button', 0, 0, 3, 3, 'nsew', **{'text': 'CN', 'width': button_width}),
    ]

    align_btns2 = [
        f(fr_align2, button_17, 'button', 0, 0, 0, 0, 'nsew', **{'text': '一', 'width': button_width}),
        f(fr_align2, button_19, 'button', 0, 0, 1, 1, 'nsew', **{'text': '二', 'width': button_width}),
        f(fr_align2, button_18, 'button', 0, 0, 2, 2, 'nsew', **{'text': '|', 'width': button_width}),
        f(fr_align2, button_20, 'button', 0, 0, 3, 3, 'nsew', **{'text': '||', 'width': button_width}),
    ]
    size_btns = [
        f(fr_width, button_22, 'button', 0, 0, 0, 0, 'nsew', **{'text': '>w<', 'width': button_width}),
        f(fr_width, button_23, 'button', 0, 0, 1, 1, 'nsew', **{'text': '<W>', 'width': button_width}),
        f(fr_width, button_24, 'button', 0, 0, 2, 2, 'nsew', **{'text': '-w', 'width': button_width}),
        f(fr_width, button_25, 'button', 0, 0, 3, 3, 'nsew', **{'text': '+W', 'width': button_width}),
    ]
    fmd_canvas = [
        f(fr_canvas, canvas_id, 'canvas', 0, 0, 0, 0, 'nsew', bg='white'),
    ]

    fmd = fmd_root
    fmd += fmd_button + groups_of_buttons
    fmd += fmd_canvas
    fmd += switchable2
    fmd += tree_sheets + sheet_entry + tree_ws_btns
    fmd += tree_connection + connection_entry + tree_radio_buttons + tree_connection_btns
    fmd += tree_accounts + tree_btns
    fmd += property_setter + align_btns + align_btns2 + size_btns
    fmd += switcher2_buttons

    state = [
        f(fr_state, textbox_rpe, 'text', 0, 0, 0, 1, 'nsew', (5, 5)),
    ]
    template = Vm.pickle_loader(fr_template, tree_pickle_files_id, canvas_template, button_width)
    macro = Vm.create_macro_manager_view_model(fr_macro, **kw_macro_buttons)
    setting = Vm.create_configuration_setting(fr_setting, **kw_setting)

    view_model += root_frame
    view_model += (menu + switchable1) + (fmd + state + template + macro + setting)

    return view_model


ie_toplevel = 'ie_toplevel'
ie_label = 'ie_label'
ie_check_btn = 'ie_check_btn'
ie_canvas_slider = 'ie_canvas_slider'
ie_canvas_graph = 'ie_canvas_graph'
ie_entry = 'ie_entry'
ie_btn_apply = 'ie_btn_apply'
ie_btn_ok = 'ie_btn_ok'
ie_entry_min = 'ie_entry_min'
ie_entry_max = 'ie_entry_max'
ie_entry_digits = 'ie_entry_digits'
ie_combo_box = 'ie_combo_box'
ie_btn_next = 'ie_btn_next'
ie_btn_previous = 'ie_btn_previous'


def input_entry() -> list:
    options = intf.top_level_options('Input Setting')
    view_model = [intf.widget_model(root, ie_toplevel, 'toplevel', 0, 0, 0, 0, 'nsew', pad_xy, **options)]
    view_model += Vm.input_entry(ie_toplevel, ie_label, ie_check_btn, ie_canvas_slider, ie_canvas_graph, ie_entry,
                                 ie_btn_apply, ie_btn_ok, ie_entry_min, ie_entry_max, ie_entry_digits, ie_combo_box,
                                 ie_btn_next, ie_btn_previous, pad_xy)
    return view_model


export_top_level = 'export_top_level'
entry_export_file_name = 'entry_export_file_name'
entry_path = 'entry_path'
entry_tornado_delta = 'entry_tornado_delta'
entry_sensitivity_min = 'entry_sensitivity_min'
entry_sensitivity_increment = 'entry_sensitivity_increment'
entry_sensitivity_max = 'entry_sensitivity_max'
entry_sensitivity_delta = 'entry_sensitivity_delta'

entry_scenario_name = 'entry_scenario_name'
tree_sensitivity_account_list = 'tree_sensitivity_account_list'
tree_sensitivity_target_list = 'tree_sensitivity_target_list'
tree_sensitivity_input_list = 'tree_sensitivity_input_list'
tree_sensitivity_variable_list = 'tree_sensitivity_variable_list'
tree_dash_board = 'tree_dash_board'
tree_scenario = 'tree_scenario'
tree_graph = 'tree_graph'

btn_path = 'btn_path'
btn_sensitivity_target_add = 'btn_sensitivity_target_add'
btn_sensitivity_target_remove = 'btn_sensitivity_target_remove'
btn_sensitivity_target_up = 'btn_sensitivity_target_up'
btn_sensitivity_target_down = 'btn_sensitivity_target_down'
btn_sensitivity_variable_add = 'btn_sensitivity_variable_add'
btn_sensitivity_variable_remove = 'btn_sensitivity_variable_remove'
btn_sensitivity_variable_up = 'btn_sensitivity_variable_up'
btn_sensitivity_variable_down = 'btn_sensitivity_variable_down'
btn_sensitivity_delta = 'btn_sensitivity_delta'
btn_scenario_name = 'btn_scenario_name'
btn_fr_scenario_up = 'btn_fr_scenario_up'
btn_fr_scenario_down = 'btn_fr_scenario_down'
btn_fr_scenario_delete = 'btn_fr_scenario_delete'
btn_graph_name = 'btn_graph_name'
btn_fr_graph_up = 'btn_fr_graph_up'
btn_fr_graph_down = 'btn_fr_graph_down'
btn_fr_graph_delete = 'btn_fr_graph_delete'
btn_dash_board_name = 'btn_dash_board_name'
btn_fr_dash_board_up = 'btn_fr_dash_board_up'
btn_fr_dash_board_down = 'btn_fr_dash_board_down'
btn_fr_dash_board_delete = 'btn_fr_dash_board_delete'
btn_export = 'btn_export'

check_btn_input_sheet = 'check_btn_input_sheet'

kwargs_xl_export = {
    'entry_export_file_name': entry_export_file_name,
    'entry_path': entry_path,
    'entry_sensitivity_min': entry_sensitivity_min,
    'entry_sensitivity_increment': entry_sensitivity_increment,
    'entry_sensitivity_max': entry_sensitivity_max,
    'entry_sensitivity_delta': entry_sensitivity_delta,
    'entry_scenario_name': entry_scenario_name,

    'tree_sensitivity_account_list': tree_sensitivity_account_list,
    'tree_sensitivity_target_list': tree_sensitivity_target_list,
    'tree_sensitivity_input_list': tree_sensitivity_input_list,
    'tree_sensitivity_variable_list': tree_sensitivity_variable_list,
    'tree_dash_board': tree_dash_board,
    'tree_scenario': tree_scenario,
    'tree_graph': tree_graph,

    'btn_path': btn_path,
    'btn_sensitivity_target_add': btn_sensitivity_target_add,
    'btn_sensitivity_target_remove': btn_sensitivity_target_remove,
    'btn_sensitivity_target_up': btn_sensitivity_target_up,
    'btn_sensitivity_target_down': btn_sensitivity_target_down,
    'btn_sensitivity_variable_add': btn_sensitivity_variable_add,
    'btn_sensitivity_variable_remove': btn_sensitivity_variable_remove,
    'btn_sensitivity_delta': btn_sensitivity_delta,
    'btn_scenario_name': btn_scenario_name,
    'btn_fr_scenario_up': btn_fr_scenario_up,
    'btn_fr_scenario_down': btn_fr_scenario_down,
    'btn_fr_scenario_delete': btn_fr_scenario_delete,
    'btn_graph_name': btn_graph_name,
    'btn_fr_graph_up': btn_fr_graph_up,
    'btn_fr_graph_down': btn_fr_graph_down,
    'btn_fr_graph_delete': btn_fr_graph_delete,
    'btn_dash_board_name': btn_dash_board_name,
    'btn_fr_dash_board_up': btn_fr_dash_board_up,
    'btn_fr_dash_board_down': btn_fr_dash_board_down,
    'btn_fr_dash_board_delete': btn_fr_dash_board_delete,
    'btn_export': btn_export,

    'check_btn_input_sheet': check_btn_input_sheet,
}


def excel_export_window() -> list:
    options = intf.top_level_options('Export Setting')
    view_model = [intf.widget_model(root, export_top_level, 'toplevel', 0, 0, 0, 0, 'nsew', pad_xy, **options)]
    view_model += Vm.export_window(export_top_level, **kwargs_xl_export)
    return view_model


toplevel_search = 'toplevel_search'
entry_search = 'entry_search'
tree_search = 'tree_search'


def search_window() -> list:
    view_model = Vm.create_view_model_search_popup(toplevel_search, entry_search, tree_search)
    return view_model


toplevel_f2 = 'toplevel_f2'
entry_f2 = 'entry_f2'
button_f2_ok = 'button_f2_ok'
f2_feedback = 'f2_feedback'


def f2_entry(title_str) -> list:
    f = intf.widget_model
    options = intf.top_level_options(title_str)
    rc = ((1,), (1,)), ((0,), (1,))
    view_model = [
        intf.widget_model(root, toplevel_f2, 'toplevel', 0, 0, 0, 0, 'nsew', pad_xy, **options),
        intf.widget_model(toplevel_f2, 'frame_f2', 'frame', 0, 0, 0, 0, 'nsew', pad_xy, **intf.frame_options(*rc)),
    ]
    view_model += Vm.entry_and_button('frame_f2', entry_f2, 30, button_f2_ok, 'OK', button_width, '')
    view_model += [f('frame_f2', f2_feedback, 'label', 1, 1, 0, 1, 'nsew', **{'text': ''})]
    return view_model


toplevel_template = 'toplevel_template'
template_name_feedback = 'template_name_feedback'
entry_template_popup = 'entry_template_popup'
button_template_popup = 'button_template_popup'


def template_name_entry(title: str, default_value: str) -> list:
    f = intf.widget_model
    options = intf.top_level_options(title)
    rc = ((1,), (1,)), ((0,), (1,))
    vm = [
        f(root, toplevel_template, 'toplevel', 0, 0, 0, 0, 'nsew', pad_xy, **options),
        f(toplevel_template, 'frame_template', 'frame', 0, 0, 0, 0, 'nsew', pad_xy, **intf.frame_options(*rc)),
    ]
    args = 'frame_template', entry_template_popup, 30, button_template_popup, 'Ok', button_width, default_value
    vm += Vm.entry_and_button(*args)
    vm += [f('frame_template', template_name_feedback, 'label', 1, 1, 0, 1, 'nsew', **{'text': ''})]
    return vm


toplevel_canvas_save_setting = 'toplevel_canvas_save_setting'
entry_total_frames = 'entry_total_frames'
entry_canvas_save_height = 'entry_canvas_save_height'
btn_canvas_save = 'btn_canvas_save'
canvas_save_feedback = 'canvas_save_feedback'


def canvas_save_setting(title: str) -> list:
    f = intf.widget_model
    options = intf.top_level_options(title)
    rc = ((0,), (1,)), ((0,), (1,))
    vm = [
        f(root, toplevel_canvas_save_setting, 'toplevel', 0, 0, 0, 0, 'nsew', pad_xy, **options),
    ]
    args = toplevel_canvas_save_setting, entry_total_frames, entry_canvas_save_height, btn_canvas_save
    vm += Vm.canvas_save_setting(*args)
    vm += [f(toplevel_canvas_save_setting, canvas_save_feedback, 'label', 1, 1, 0, 1, 'nsew', **{'text': ''})]
    return vm
