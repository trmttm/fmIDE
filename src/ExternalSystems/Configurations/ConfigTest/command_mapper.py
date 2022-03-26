from interface_fm import BoundaryInABC
from interface_mouse import MouseControllerABC
from interface_view import ViewABC
from src.BoundaryOutput import PresentersABC

from . import constants as cns
from . import control_commands as c
from . import view_model as w


def widget_command_map_factory(view: ViewABC, interactor: BoundaryInABC, mouse: MouseControllerABC,
                               presenters: PresentersABC) -> dict:
    entry_exits_are_managed_separately = [mouse.handle]
    do_not_save_states = []
    negative_command_list = entry_exits_are_managed_separately + do_not_save_states

    # Virtual events. Prevent saving.
    virtual_events_key = [w.tree_pickle_files_id, w.tree_account_order, w.tree_worksheets, w.entry_sheet]
    undo_redo_needs_no_auto_save = [w.btn_undo, w.btn_redo]
    negative_key_list = virtual_events_key + undo_redo_needs_no_auto_save

    sc = c.set_configuration_value
    command_dictionary = {
        # w.root: lambda *args: interactor.feedback_user(f'Mouse wheel {args}'),
        w.button_1: lambda: c.main_specific_add_shape(interactor, view, ),
        w.btn_erase_shape: interactor.erase_selected_shapes,
        w.btn_tree_ac_up: interactor.move_selection_up,
        w.btn_tree_ac_down: interactor.move_selection_down,
        w.button_8: interactor.add_blank_above_selection,
        w.button_9: interactor.add_relay,
        # w.button_11: lambda: interactor.export_vba_user_defined_function('UDF.text'),
        w.btn_ie: lambda: c.popup_input_entry(view, interactor, mouse.__class__),
        w.button_13: interactor.align_left,
        w.button_14: interactor.align_top,
        w.button_15: interactor.align_bottom,
        w.button_16: interactor.align_right,
        w.button_17: interactor.align_middle_vertical,
        w.button_18: interactor.align_middle_horizontal,
        w.button_19: interactor.evenly_distribute_vertically,
        w.button_20: interactor.evenly_distribute_horizontally,
        w.btn_reset: interactor.reset,
        w.button_22: interactor.fit_selected_shapes_width,
        w.button_23: interactor.match_selected_shapes_width,
        w.button_24: interactor.decrease_width_of_selected_shapes,
        w.button_25: interactor.increase_width_of_selected_shapes,
        w.btn_swtch_ac: lambda: c.upon_fmd_switcher_accounts(view),
        w.btn_swtch_property: lambda: c.upon_fmd_switcher_properties(view),
        w.btn_op_bb: lambda: c.main_specific_add_shape(interactor, view, 'BB'),
        w.btn_op_max: lambda: c.main_specific_add_shape(interactor, view, 'max'),
        w.btn_op_min: lambda: c.main_specific_add_shape(interactor, view, 'min'),
        w.btn_op_ave: lambda: c.main_specific_add_shape(interactor, view, 'ave'),
        w.btn_op_le: lambda: c.main_specific_add_shape(interactor, view, '<='),
        w.btn_op_lt: lambda: c.main_specific_add_shape(interactor, view, '<'),
        w.btn_op_ge: lambda: c.main_specific_add_shape(interactor, view, '>='),
        w.btn_op_gt: lambda: c.main_specific_add_shape(interactor, view, '>'),
        w.btn_op_eq: lambda: c.main_specific_add_shape(interactor, view, '='),
        w.btn_op_pw: lambda: c.main_specific_add_shape(interactor, view, '^'),
        w.btn_op_abs: lambda: c.main_specific_add_shape(interactor, view, 'abs'),
        w.btn_analyze: interactor.analyze_circular_reference,
        w.btn_switch_sheet: lambda: c.upon_fmd_switcher_worksheets(view),
        w.btn_export_accounts: lambda: c.paste_selected_accounts(interactor),
        w.btn_del_sheet: interactor.delete_selected_worksheet,
        w.btn_add_sheet: interactor.add_new_worksheet,
        w.btn_import_accounts: lambda: c.copy_selected_accounts(interactor),
        w.btn_sheet_name: lambda: c.change_selected_sheet_name(interactor, view),
        # w.btn_save_module: lambda: c.upon_save_as_module(view, interactor, w.entry_template),
        w.btn_save_module: lambda: c.popup_module_save(view, interactor, presenters, mouse),
        w.btn_undo: interactor.undo,
        w.btn_redo: interactor.redo,
        w.btn_sheet_up: lambda: c.move_selected_worksheets(interactor, view, -1),
        w.btn_sheet_down: lambda: c.move_selected_worksheets(interactor, view, 1),
        w.btn_sheet_left: lambda: c.move_selected_worksheets_left(interactor, view),
        w.btn_sheet_right: lambda: c.move_selected_worksheets_right(interactor, view),
        'op1': lambda: c.main_specific_add_shape(interactor, view, '+'),
        'op2': lambda: c.main_specific_add_shape(interactor, view, '-'),
        'op3': lambda: c.main_specific_add_shape(interactor, view, 'x'),
        'op4': lambda: c.main_specific_add_shape(interactor, view, '/'),
        'm1': lambda: c.upon_menu_button1(view, interactor, presenters, mouse),
        'm2': lambda: c.upon_menu_button2(view, interactor, presenters, mouse, cns.negative_list),
        'm3': lambda: c.upon_menu_button3(view, interactor, presenters, mouse),
        'm4': lambda: c.upon_menu_button4(view, interactor, presenters, mouse),
        'm5': lambda: c.upon_menu_button5(view, interactor, presenters, mouse),
        'button_delete_template': lambda: c.upon_delete_template(view, interactor, cns.negative_list),
        'button_load_pickle': lambda: c.upon_load_pickle(view, interactor, presenters, mouse),
        'button_merge_pickle': lambda: c.upon_merge_pickle(view, interactor, presenters, mouse, cns.negative_list, ),

        w.btn_switch_conn: lambda: c.upon_fmd_switcher_connections(view),
        w.btn_add_conn: lambda: c.add_connection_id(view, interactor),
        w.btn_del_conn: lambda: c.delete_connection_id(view, interactor),

        # Command and Macro
        w.btn_del_macro: lambda: c.btn_del_macro(view, interactor),
        w.btn_merge_macro: lambda: c.btn_merge_macro(view, interactor),
        w.btn_save_macro: lambda: c.btn_save_macro(view, interactor),
        w.btn_run_commands: lambda: c.btn_run_commands(view, interactor),
        w.btn_run_commands_fast: lambda: c.btn_run_commands_fast(interactor),
        w.btn_clear_commands: lambda: c.btn_clear_commands(interactor),
        w.btn_del_commands: lambda: c.btn_del_commands(view, interactor),
        w.btn_copy_commands: lambda: c.btn_copy_commands(view, interactor),
        w.btn_down_command: lambda: c.btn_down_command(view, interactor),
        w.btn_up_command: lambda: c.btn_up_command(view, interactor),
        w.btn_set_command_name: lambda: c.btn_set_command_name(view, interactor),
        w.btn_set_args: lambda: c.btn_set_args(view, interactor),
        w.btn_set_kwargs: lambda: c.btn_set_kwargs(view, interactor),
        w.check_btn_macro_mode: lambda: c.upon_check_box_macro_mode(view, interactor),

        w.tree_pickle_files_id: lambda: c.upon_tree_pickles_list_click(interactor, view),
        w.tree_account_order: lambda: c.upon_tree_account_order_click(interactor, view),
        w.tree_worksheets: lambda: c.upon_tree_worksheets_click(interactor, view),

        # Property
        w.entry_text: lambda *_: c.upon_leaving_entry(view, interactor, w.entry_text, 'text'),
        w.entry_x: lambda *_: c.upon_leaving_entry(view, interactor, w.entry_x, 'x'),
        w.entry_y: lambda *_: c.upon_leaving_entry(view, interactor, w.entry_y, 'y'),
        w.entry_width: lambda *_: c.upon_leaving_entry(view, interactor, w.entry_width, 'width'),
        w.entry_height: lambda *_: c.upon_leaving_entry(view, interactor, w.entry_height, 'height'),
        w.entry_sheet: lambda *_: c.upon_leaving_entry(view, interactor, w.entry_sheet, 'worksheet'),
        w.entry_delta_x: lambda *_: c.upon_leaving_entry_delta(view, interactor),
        w.entry_delta_y: lambda *_: c.upon_leaving_entry_delta(view, interactor),
        w.entry_shape_id: lambda *_: c.upon_leaving_entry(view, interactor, w.entry_shape_id, 'shape_id'),
        w.entry_uom: lambda *_: c.upon_leaving_entry(view, interactor, w.entry_uom, 'uom'),
        w.check_btn_breakdown_account: lambda *_: c.set_breakdown_account(view, interactor),

        w.cb_format: lambda value: c.upon_format_selection(view, interactor),
        w.cb_num_format: lambda value: c.upon_number_format_selection(view, interactor),

        # Vertical Reference
        w.check_btn: lambda: c.upon_check_box_vertical_account(view, interactor),
        w.btn_add_vref: lambda: c.add_vertical_reference(view, interactor),
        w.btn_remove_v_ref: lambda: c.remove_vertical_reference(view, interactor),

        # Configuration setting
        w.entry_nop: lambda *_: c.check_nop_valid_entry(view, interactor),
        w.btn_setting_ok: lambda: c.apply_configuration_setting(view, interactor),
        w.check_btn_cleaner: lambda: c.upon_state_cleaner_check_button(view, interactor),
        w.check_btn_live_calculation: lambda: c.upon_live_calculation_check_button(view, interactor),
        w.btn_project: lambda: c.create_project_folder(view, interactor, presenters, mouse),
        w.entry_project: lambda *_: c.set_project_folder(view, interactor, presenters, mouse),
        w.entry_account_w: lambda *_: sc(view, interactor.set_account_width, w.entry_account_w),
        w.entry_account_h: lambda *_: sc(view, interactor.set_account_height, w.entry_account_h),
        w.entry_account_font_size: lambda *_: sc(view, interactor.set_account_font_size, w.entry_account_font_size),
        w.entry_operator_w: lambda *_: sc(view, interactor.set_operator_width, w.entry_operator_w),
        w.entry_operator_h: lambda *_: sc(view, interactor.set_operator_height, w.entry_operator_h),
        w.entry_operator_font_size: lambda *_: sc(view, interactor.set_operator_font_size, w.entry_operator_font_size),
        w.entry_constant_w: lambda *_: sc(view, interactor.set_constant_width, w.entry_constant_w),
        w.entry_constant_h: lambda *_: sc(view, interactor.set_constant_height, w.entry_constant_h),
        w.entry_constant_font_size: lambda *_: sc(view, interactor.set_constant_font_size, w.entry_constant_font_size),
        w.entry_bb_w: lambda *_: sc(view, interactor.set_bb_width, w.entry_bb_w),
        w.entry_bb_h: lambda *_: sc(view, interactor.set_bb_height, w.entry_bb_h),
        w.entry_bb_font_size: lambda *_: sc(view, interactor.set_bb_font_size, w.entry_bb_font_size),
        w.check_btn_relay_right_end: lambda: c.toggle_relay_x_position(view, interactor),

        # Excel Export
        w.btn_excel: lambda: c.popup_excel_export_entry(view, interactor, presenters, mouse),
    }
    for key, command in command_dictionary.items():
        if (command not in negative_command_list) and (key not in negative_key_list):
            command_dictionary[key] = c.decorator_entry_and_exit_point(command, interactor, key)
    return command_dictionary
