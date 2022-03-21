import os_identifier
from interface_fm import BoundaryInABC
from interface_keymaps import KeyMapABC
from interface_mouse import MouseControllerABC
from interface_view import ViewABC
from src.BoundaryOutput import PresentersABC

from . import constants
from . import control_commands as c
from . import view_commands as vc
from . import view_model as vm


def get_all_key_combos(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                       mouse: MouseControllerABC) -> dict:
    return {
        constants.keymap_design: create_design_key_combos(interactor, view, presenters, mouse),
        constants.keymap_template: create_template_key_combos(interactor, view, presenters, mouse),
        constants.keymap_state: create_state_key_combos(interactor, view, presenters, mouse),
        constants.keymap_macro: create_macro_key_combos(interactor, view, presenters, mouse),
        constants.keymap_setting: create_setting_key_combos(interactor, view, presenters, mouse),
        constants.keymap_export: create_export_window_key_combos(interactor, view, presenters, mouse),
        constants.keymap_search: create_search_window_key_combos(interactor, view, presenters, mouse),
    }


def create_global_key_combos(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                             mouse: MouseControllerABC) -> dict:
    k = KeyMapABC
    i = interactor
    v = view
    p = presenters
    m = mouse

    main_modifier = k.command if os_identifier.is_mac else k.control
    sub_modifier = k.control if os_identifier.is_mac else k.alt_option
    shift_main = k.shift + main_modifier
    shift_sub = k.shift + sub_modifier
    main_sub = main_modifier + sub_modifier

    cmd_undo = (lambda: i.undo(), 'Undo')
    cmd_redo = (lambda: i.redo(), 'Redo')
    cmd_open_search_window = (lambda: c.popup_search_window(v, i, p, m), 'Search Window')
    dont_wrap_these_commands_with_auto_save = (
        cmd_undo,
        cmd_redo,
    )

    def add_shape():  # to save line space
        c.main_specific_add_shape(interactor, v, v.get_value(vm.entry_id))

    key_combos = {
        # (modifier:int, key:str) : (command:Callables, feedback:str)
        (): (lambda key_: i.feedback_user(key_), ''),

        # No modifier [single Key]
        (main_modifier, k.d): (lambda: c.upon_menu_button1(v, i, p, m), 'Selected Design'),
        (main_modifier, k.t): (lambda: c.upon_menu_button2(v, i, p, m, constants.negative_list), 'Selected Template'),
        (main_modifier, k.s): (lambda: c.upon_menu_button3(v, i, p, m), 'Selected Status'),
        (main_modifier, k.m): (lambda: c.upon_menu_button4(v, i, p, m), 'Selected Macro'),
        (main_modifier, k.g): (lambda: c.upon_menu_button5(v, i, p, m), 'Selected Setting'),

        (main_modifier, k.w): (lambda: c.properly_close_app(i, v), 'Quit'),
        (main_modifier, k.z): cmd_undo,
        (main_modifier + k.shift, k.z): cmd_redo,
        (main_modifier, k.y): cmd_redo,
        (main_modifier, k.e): (lambda: c.popup_excel_export_entry(v, i, p, m), 'Export Window'),
        (shift_main, k.s): cmd_open_search_window,
    }
    wrap_auto_save_functionality(dont_wrap_these_commands_with_auto_save, interactor, key_combos)
    return key_combos


def create_design_key_combos(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                             mouse: MouseControllerABC) -> dict:
    k = KeyMapABC
    i = interactor
    v = view
    p = presenters
    m = mouse
    dec_show_btns = vc.decorator_show_design_buttons

    main_modifier = k.command if os_identifier.is_mac else k.control
    sub_modifier = k.control if os_identifier.is_mac else k.alt_option
    shift_main = k.shift + main_modifier
    shift_sub = k.shift + sub_modifier
    main_sub = main_modifier + sub_modifier

    cmd_repeat = (lambda: i.execute_previous_command(), 'Repeated previous command')
    dont_wrap_these_commands_with_auto_save = (cmd_repeat,)

    def add_shape():  # to save line space
        c.main_specific_add_shape(interactor, v, v.get_value(vm.entry_id))

    def prevent_widget_interference(f):
        def wrapper(*args, **kwargs):
            focused_widget_id = v.focused_widget
            tree_that_interfere_with_keyboard = [vm.tree_account_order, vm.tree_connections, vm.tree_worksheets]
            if 'entry' not in focused_widget_id and focused_widget_id not in tree_that_interfere_with_keyboard:
                f(*args, **kwargs)

        return wrapper

    dx, dy = i.move_shape_increment

    mouse_position = v.get_mouse_canvas_coordinate
    key_combos = {
        # (modifier:int, key:str) : (command:Callables, feedback:str)
        (): (lambda key_: i.feedback_user(key_), ''),

        # No modifier [single Key]
        (k.none, k.delete): (prevent_widget_interference(interactor.erase_selected_shapes), 'Deleted shapes.'),
        (k.none, k.back_space): (prevent_widget_interference(interactor.erase_selected_shapes), 'Deleted shapes.'),

        (sub_modifier, k.enter): (add_shape, f'New shape Added'),
        (shift_sub, k.equal): (lambda: c.main_specific_add_shape(i, v, '+'), '+ Added'),
        (sub_modifier, k.minus): (lambda: c.main_specific_add_shape(i, v, '-'), '- Added'),
        (sub_modifier, k.x): (lambda: c.main_specific_add_shape(i, v, 'x'), 'x Added'),
        (sub_modifier, k.slash): (lambda: c.main_specific_add_shape(i, v, '/'), '/ Added'),
        (sub_modifier, k.b): (lambda: c.main_specific_add_shape(i, v, 'BB'), 'BB Added'),
        (sub_modifier, k.m): (lambda: c.main_specific_add_shape(i, v, 'max'), 'max Added'),
        (shift_sub, k.m): (lambda: c.main_specific_add_shape(i, v, 'min'), 'min Added'),
        (sub_modifier, k.a): (lambda: c.main_specific_add_shape(i, v, 'ave'), 'ave Added'),
        (shift_sub, k.l): (lambda: c.main_specific_add_shape(i, v, '<='), '<= Added'),
        (sub_modifier, k.l): (lambda: c.main_specific_add_shape(i, v, '<'), '< Added'),
        (shift_sub, k.g): (lambda: c.main_specific_add_shape(i, v, '>='), '>= Added'),
        (sub_modifier, k.g): (lambda: c.main_specific_add_shape(i, v, '>'), '> Added'),
        (sub_modifier, k.equal): (lambda: c.main_specific_add_shape(i, v, '='), '= Added'),
        (sub_modifier, k.p): (lambda: c.main_specific_add_shape(i, v, '^'), '^ Added'),
        (shift_sub, k.a): (lambda: c.main_specific_add_shape(i, v, 'abs'), 'abs Added'),
        (sub_modifier, k.r): (lambda: i.add_relay(), 'Relays added.'),
        (main_modifier, k.r): (lambda: i.tear_down_setup(), 'Removed caretaker states'),

        (sub_modifier, k.s): (lambda: i.add_slider_of_selected_input_accounts(), 'Slider added.'),
        (main_sub, k.g): (lambda: i.add_a_y_axis_of_selected_accounts(mouse_position(), (0, 100)), 'Graph added.'),
        (main_sub, k.b): (lambda: i.add_bar_of_selected_accounts(), 'Bar added.'),
        (main_sub, k.v): (lambda: i.add_live_values_of_selected_accounts(), 'Live Values Added'),
        (sub_modifier, k.four): cmd_repeat,

        (sub_modifier, k.d): (lambda: i.copy_selection(), 'Selection Copied'),
        (sub_modifier, k.c): (lambda: interactor.set_fill_to_selection(view.ask_color()), 'Select Color'),

        (main_modifier, k.i): (lambda: c.popup_input_entry(v, i, m.__class__), 'Pupup Input Entry'),
        (sub_modifier, k.v): (lambda: vc.toggle_design_buttons_show_hide(v), 'Toggled Buttons Show / Hide'),
        (main_modifier, k.a): (prevent_widget_interference(i.select_all_in_the_sheet), 'Select All'),

        (main_modifier, k.f): (lambda: i.toggle_format(), 'Updated Format'),
        (shift_main, k.f): (lambda: i.toggle_number_format(), 'Update Number Format'),

        (k.none, k.up): (lambda: prevent_widget_interference(i.move_selections)(0, -dy), 'Move Shape Up'),
        (k.none, k.down): (lambda: prevent_widget_interference(i.move_selections)(0, dy), 'Move Shape Down'),
        (k.none, k.left): (lambda: prevent_widget_interference(i.move_selections)(-dx, 0), 'Move Shape Left'),
        (k.none, k.right): (lambda: prevent_widget_interference(i.move_selections)(dx, 0), 'Move Shape Right'),

        (shift_sub, k.up): (lambda: i.align_top(), 'Aligned Up'),
        (shift_sub, k.down): (lambda: i.align_bottom(), 'Aligned Down'),
        (shift_sub, k.left): (lambda: i.align_left(), 'Aligned Left'),
        (shift_sub, k.right): (lambda: i.align_right(), 'Aligned Right'),

        (shift_main, k.up): (lambda: prevent_widget_interference(i.match_selected_shapes_width)(), 'Match width'),
        (shift_main, k.down): (lambda: prevent_widget_interference(i.fit_selected_shapes_width)(), 'Fit Width'),
        (shift_main, k.left): (
            lambda: prevent_widget_interference(i.decrease_width_of_selected_shapes)(), 'Reduce Width'),
        (shift_main, k.right): (
            lambda: prevent_widget_interference(i.increase_width_of_selected_shapes)(), 'Increase Width'),

        (main_modifier, k.up): (lambda: i.evenly_distribute_vertically(), 'Evenly distribute Vertically'),
        (main_modifier, k.down): (lambda: i.align_middle_vertical(), 'Align Middle Vertical'),
        (main_modifier, k.left): (lambda: i.evenly_distribute_horizontally(), 'Evenly distribute Horizontally'),
        (main_modifier, k.right): (lambda: i.align_middle_horizontal(), 'Aligned Middle Horizontal'),

        (main_modifier, k.one): (lambda: dec_show_btns(c.upon_fmd_switcher_accounts, v)(v), 'Account Order'),
        (main_modifier, k.two): (lambda: dec_show_btns(c.upon_fmd_switcher_properties, v)(v), 'Properties'),
        (main_modifier, k.three): (lambda: dec_show_btns(c.upon_fmd_switcher_worksheets, v)(v), 'Worksheets'),
        (main_modifier, k.four): (lambda: dec_show_btns(c.upon_fmd_switcher_connections, v)(v), 'Connection IDs'),

        (k.none, k.f9): (lambda: i.calculate(), 'Calculated'),
        (k.none, k.f12): (lambda: c.popup_template_save(v, i, p, m), 'Template Save Popup'),
        (shift_sub, k.s): (lambda: c.popup_canvas_save(v, i, p, m), 'Canvas Save'),

        (shift_sub, k.i): (lambda: i.scale_canvas(2, 2), 'Canvas Scaled'),
        (shift_sub, k.o): (lambda: i.scale_canvas(0.5, 0.5), 'Canvas Scaled'),

        (k.none, k.f2): (lambda: c.popup_f2_entry(v, i, p, m), 'Text Focus'),
        (main_modifier, k.l): (lambda: dec_show_btns(c.focus_on_account_entry, v)(v), 'New Focus'),

        (main_modifier, k.n): (lambda: i.reset(), 'Reset'),
    }
    wrap_auto_save_functionality(dont_wrap_these_commands_with_auto_save, interactor, key_combos)
    key_combos.update(create_global_key_combos(i, v, p, m))
    return key_combos


def create_template_key_combos(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                               mouse: MouseControllerABC) -> dict:
    k = KeyMapABC
    i = interactor
    v = view
    p = presenters
    m = mouse

    main_modifier = k.command if os_identifier.is_mac else k.control
    sub_modifier = k.control if os_identifier.is_mac else k.alt_option
    shift_main = k.shift + main_modifier
    shift_sub = k.shift + sub_modifier
    main_sub = main_modifier + sub_modifier

    dont_wrap_these_commands_with_auto_save = ()

    key_combos = {
    }
    wrap_auto_save_functionality(dont_wrap_these_commands_with_auto_save, interactor, key_combos)
    key_combos.update(create_global_key_combos(i, v, p, m))
    return key_combos


def create_state_key_combos(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                            mouse: MouseControllerABC) -> dict:
    k = KeyMapABC
    i = interactor
    v = view
    p = presenters
    m = mouse

    main_modifier = k.command if os_identifier.is_mac else k.control
    sub_modifier = k.control if os_identifier.is_mac else k.alt_option
    shift_main = k.shift + main_modifier
    shift_sub = k.shift + sub_modifier
    main_sub = main_modifier + sub_modifier

    dont_wrap_these_commands_with_auto_save = ()

    key_combos = {
    }
    wrap_auto_save_functionality(dont_wrap_these_commands_with_auto_save, interactor, key_combos)
    key_combos.update(create_global_key_combos(i, v, p, m))
    return key_combos


def create_macro_key_combos(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                            mouse: MouseControllerABC) -> dict:
    k = KeyMapABC
    i = interactor
    v = view
    p = presenters
    m = mouse

    main_modifier = k.command if os_identifier.is_mac else k.control
    sub_modifier = k.control if os_identifier.is_mac else k.alt_option
    shift_main = k.shift + main_modifier
    shift_sub = k.shift + sub_modifier
    main_sub = main_modifier + sub_modifier

    dont_wrap_these_commands_with_auto_save = ()

    key_combos = {
    }
    wrap_auto_save_functionality(dont_wrap_these_commands_with_auto_save, interactor, key_combos)
    key_combos.update(create_global_key_combos(i, v, p, m))
    return key_combos


def create_setting_key_combos(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                              mouse: MouseControllerABC) -> dict:
    k = KeyMapABC
    i = interactor
    v = view
    p = presenters
    m = mouse

    main_modifier = k.command if os_identifier.is_mac else k.control
    sub_modifier = k.control if os_identifier.is_mac else k.alt_option
    shift_main = k.shift + main_modifier
    shift_sub = k.shift + sub_modifier
    main_sub = main_modifier + sub_modifier

    dont_wrap_these_commands_with_auto_save = ()

    key_combos = {
    }
    wrap_auto_save_functionality(dont_wrap_these_commands_with_auto_save, interactor, key_combos)
    key_combos.update(create_global_key_combos(i, v, p, m))
    return key_combos


def create_export_window_key_combos(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                                    mouse: MouseControllerABC) -> dict:
    k = KeyMapABC
    i = interactor
    v = view
    p = presenters
    m = mouse

    main_modifier = k.command if os_identifier.is_mac else k.control
    sub_modifier = k.control if os_identifier.is_mac else k.alt_option
    shift_main = k.shift + main_modifier
    shift_sub = k.shift + sub_modifier
    main_sub = main_modifier + sub_modifier
    dont_wrap_these_commands_with_auto_save = ()
    key_combos = {
        # (modifier:int, key:str) : (command:Callables, feedback:str)
        (main_modifier, k.w): (lambda: c.close_export_window_properly(i, v), 'Properly closed export window.'),
        (main_modifier, k.i): (lambda: c.toggle_check_btn_input_sheet(i, v), 'Toggled input check button.'),
        (main_modifier, k.enter): (lambda: c.export_excel(v, i), ''),
    }
    wrap_auto_save_functionality(dont_wrap_these_commands_with_auto_save, interactor, key_combos)
    return key_combos


def create_search_window_key_combos(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                                    mouse: MouseControllerABC) -> dict:
    k = KeyMapABC
    i = interactor
    v = view
    p = presenters
    m = mouse

    main_modifier = k.command if os_identifier.is_mac else k.control
    sub_modifier = k.control if os_identifier.is_mac else k.alt_option
    shift_main = k.shift + main_modifier
    shift_sub = k.shift + sub_modifier
    main_sub = main_modifier + sub_modifier

    default_key_combos = {
        # (modifier:int, key:str) : (command:Callables, feedback:str)
        (k.none, k.up): (lambda: c.search_tree_focus_up(v, vm.tree_search), 'Select tree up'),
        (k.none, k.down): (lambda: c.search_tree_focus_down(v, vm.tree_search), 'Select tree down'),
        (k.none, k.return_): (lambda: c.execute_searched_command(v, i), 'Execute selected command.'),
        (k.shift, k.return_): (lambda: c.execute_searched_command_alternative(v, i), 'Execute command.'),
        (main_modifier, k.return_): (lambda: c.copy_searched_item_to_clip_board(v, i), 'Execute command.'),
        (k.none, k.escape): (lambda: c.close_search_window_properly(i, v), 'Closed Search Window Properly.'),
        (main_modifier, k.w): (lambda: c.close_search_window_properly(i, v), 'Closed Search Window Properly.'),
    }

    '''
    No need to wrap the commands with auto save because saving is done when popping up. 
    '''
    return default_key_combos


def create_f2_entry_key_combos(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                               mouse: MouseControllerABC) -> dict:
    k = KeyMapABC
    i = interactor
    v = view
    p = presenters
    m = mouse

    main_modifier = k.command if os_identifier.is_mac else k.control
    sub_modifier = k.control if os_identifier.is_mac else k.alt_option
    shift_main = k.shift + main_modifier
    shift_sub = k.shift + sub_modifier
    main_sub = main_modifier + sub_modifier

    dont_wrap_these_commands_with_auto_save = ()

    key_combos = {
        # (modifier:int, key:str) : (command:Callables, feedback:str)
        (k.none, k.return_): (lambda: c.upon_f2_ok(v, i), 'Confirm F2 Entry'),
        (k.none, k.escape): (lambda: c.close_f2_entry_properly(i, v), 'Closed F2 popup Properly.'),
        (main_modifier, k.w): (lambda: c.close_f2_entry_properly(i, v), 'Closed F2 popup Properly.'),
    }

    wrap_auto_save_functionality(dont_wrap_these_commands_with_auto_save, interactor, key_combos)
    return key_combos


def create_template_save_key_combos(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                                    mouse: MouseControllerABC) -> dict:
    k = KeyMapABC
    i = interactor
    v = view
    p = presenters
    m = mouse

    main_modifier = k.command if os_identifier.is_mac else k.control
    sub_modifier = k.control if os_identifier.is_mac else k.alt_option
    shift_main = k.shift + main_modifier
    shift_sub = k.shift + sub_modifier
    main_sub = main_modifier + sub_modifier

    dont_wrap_these_commands_with_auto_save = ()

    key_combos = {
        # (modifier:int, key:str) : (command:Callables, feedback:str)
        (k.none, k.return_): (lambda: c.upon_template_save_ok(v, i, c.save_template), 'Confirm Template Entry'),
        (k.none, k.escape): (lambda: c.close_template_entry_properly(i, v), 'Closed Template popup Properly.'),
        (main_modifier, k.w): (lambda: c.close_template_entry_properly(i, v), 'Closed Template popup Properly.'),
    }

    wrap_auto_save_functionality(dont_wrap_these_commands_with_auto_save, interactor, key_combos)
    return key_combos


def create_canvas_save_key_combos(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                                  mouse: MouseControllerABC) -> dict:
    k = KeyMapABC
    i = interactor
    v = view
    p = presenters
    m = mouse

    main_modifier = k.command if os_identifier.is_mac else k.control
    sub_modifier = k.control if os_identifier.is_mac else k.alt_option
    shift_main = k.shift + main_modifier
    shift_sub = k.shift + sub_modifier
    main_sub = main_modifier + sub_modifier

    dont_wrap_these_commands_with_auto_save = ()

    key_combos = {
        # (modifier:int, key:str) : (command:Callables, feedback:str)
        (k.none, k.return_): (lambda: c.upon_canvas_save_button(v, i), 'Save Canvas'),
        (k.none, k.escape): (lambda: c.close_canvas_save_setting_properly(i, v), 'Closed Canvas Save popup Properly.'),
        (main_modifier, k.w): (
            lambda: c.close_canvas_save_setting_properly(i, v), 'Closed Canvas Save popup Properly.'),
    }

    wrap_auto_save_functionality(dont_wrap_these_commands_with_auto_save, interactor, key_combos)
    return key_combos


def wrap_auto_save_functionality(dont_wrap_these_commands_with_auto_save, interactor, key_combos):
    for shortcut_key, (command, feedback) in key_combos.items():
        if (command, feedback) not in dont_wrap_these_commands_with_auto_save:
            wrapped_command = c.decorator_entry_and_exit_point(command, interactor, shortcut_key)
            key_combos[shortcut_key] = wrapped_command, feedback
        else:
            key_combos[shortcut_key] = command, feedback
