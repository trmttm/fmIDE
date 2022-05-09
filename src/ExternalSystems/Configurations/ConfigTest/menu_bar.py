from interface_fm import BoundaryInABC
from interface_mouse import MouseControllerABC
from interface_view import ViewABC

from . import control_commands as c
from ....BoundaryOutput import PresentersABC


def create_menu_bar_model(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                          mouse: MouseControllerABC) -> dict:
    cmd_undo = interactor.undo
    cmd_redo = interactor.redo
    cmd_repeat = interactor.execute_previous_command

    dont_wrap_these_commands_with_auto_save = (
        cmd_undo,
        cmd_redo,
        cmd_repeat,
    )
    menu_bar_model = {
        'File': {
            'Create New Project': lambda: c.create_project_folder(view, interactor, presenters, mouse),
            'Model with CFWF': lambda: c.popup_wizard(interactor, view, presenters, mouse),
            'Load Project': lambda: c.create_project_folder(view, interactor, presenters, mouse),
            'Load Inputs from Input Setter.csv': lambda: interactor.load_inputs_from_csv(),
            'Recent Projects': {},
            'Clear Project History': lambda: interactor.clear_project_history(),
            'Save as Template': lambda: c.popup_f2_entry(view, interactor, presenters, mouse),
            'Save as Module': lambda: c.popup_module_save(view, interactor, presenters, mouse),
            'Close': lambda: c.properly_close_app(interactor, view),
        },
        'Export': {
            'Export as Excel': lambda: c.popup_excel_export_entry(view, interactor, presenters, mouse),
            'Export as DataTable': lambda: save_data_table(interactor),
            'Save Canvas as PS Image': lambda: interactor.save_canvas_as_image('Canvas Caption.ps'),
            'Save Canvas Images': lambda: c.popup_canvas_save(view, interactor, presenters, mouse),
            'Input Setter.csv': lambda: interactor.export_input_setter_csv(),
        },
        'Caching': {
            'Cache Audit': lambda: interactor.cache_audit_results(),
            'Cache Slider': lambda: interactor.cache_slider(),
            'Clear Cache Audit': lambda: interactor.clear_cache_audit_results(),
            'Clear Cache Slider': lambda: interactor.clear_cache_slider(),
        },
        'Setting': {
            'Configurations': lambda: interactor.feedback_user('Pushed Configurations'),
            'Transactions': {
                'Revenue': lambda: interactor.feedback_user('Revenue'),
                'COGS': lambda: interactor.feedback_user('COGS'),
            },
        },
        'Search': {
            'Commands': lambda: c.popup_search_window(view, interactor, presenters, mouse),
        },
        'Commands': {
            'Undo': cmd_undo,
            'Redo': cmd_redo,
            'Repeat Previous': cmd_repeat,
        },
        'Canvas': {
            'Update All': interactor.update_canvas,
            'Unselect All': lambda: interactor.unselect_all(),
            'Update Current Sheet': interactor.update_canvas_of_current_sheet,
            'Add': {
                'New Shape': lambda: c.main_specific_add_shape(interactor, view, ),
                'Live Value': lambda: interactor.add_live_values_of_selected_accounts(),
                'Slider [sub+s]': lambda: interactor.add_slider_of_selected_input_accounts(),
                'Graph': lambda: interactor.add_a_y_axis_of_selected_accounts((100, 100), (0, 100)),
                'Bar': lambda: interactor.add_bar_of_selected_accounts(),
            },
            'Add Operators': {
                '+': lambda: c.main_specific_add_shape(interactor, view, '+'),
                '-': lambda: c.main_specific_add_shape(interactor, view, '-'),
                'x': lambda: c.main_specific_add_shape(interactor, view, 'x'),
                '/': lambda: c.main_specific_add_shape(interactor, view, '/'),
                'BB': lambda: c.main_specific_add_shape(interactor, view, 'BB'),
                'max': lambda: c.main_specific_add_shape(interactor, view, 'max'),
                'min': lambda: c.main_specific_add_shape(interactor, view, 'min'),
                'ave': lambda: c.main_specific_add_shape(interactor, view, 'ave'),
                '<=': lambda: c.main_specific_add_shape(interactor, view, '<='),
                '<': lambda: c.main_specific_add_shape(interactor, view, '<'),
                '>=': lambda: c.main_specific_add_shape(interactor, view, '>='),
                '>': lambda: c.main_specific_add_shape(interactor, view, '>'),
                '=': lambda: c.main_specific_add_shape(interactor, view, '='),
                '^': lambda: c.main_specific_add_shape(interactor, view, '^'),
                'abs': lambda: c.main_specific_add_shape(interactor, view, 'abs'),
                'iferror': lambda: c.main_specific_add_shape(interactor, view, 'iferror'),
                'int': lambda: c.main_specific_add_shape(interactor, view, 'int'),
            },
            'Align Shapes': {
                '↑ Up': lambda: interactor.align_top(),
                '↓ Down': lambda: interactor.align_bottom(),
                '← Left': lambda: interactor.align_left(),
                '→ Right': lambda: interactor.align_right,
                'Vertical Center': lambda: interactor.align_middle_vertical(),
                'Vertical Even Distribute': lambda: interactor.evenly_distribute_vertically(),
                'Horizontal Center': lambda: interactor.align_middle_horizontal(),
                'Horizontal Evenly Distribute': lambda: interactor.evenly_distribute_horizontally(),
            },
            'Width': {
                'Fit': lambda: interactor.fit_selected_shapes_width(),
                'Max Align': lambda: interactor.match_selected_shapes_width(),
                '->shrink<-': lambda: interactor.decrease_width_of_selected_shapes(),
                '<-WIDEN->': lambda: interactor.increase_width_of_selected_shapes(),
            },
            'Color': {
                'Set Color': lambda: interactor.set_fill_to_selection(view.ask_color()),
                'Remove Color': lambda: interactor.remove_fill_of_selection(),
            },
            'Erase Selected': lambda: interactor.erase_selected_shapes(),
            'Calculate': lambda: interactor.calculate(),
        },
        'Analyze': {
            'Add Graph': {
                'IS': lambda: interactor.feedback_user('to be implemented', ),
                'BS': lambda: interactor.feedback_user('to be implemented', ),
                'CF': lambda: interactor.feedback_user('to be implemented', ),
                'BS IS': lambda: interactor.feedback_user('to be implemented', ),
                'DCF': lambda: interactor.feedback_user('to be implemented', ),
                'Income Tax': lambda: interactor.feedback_user('to be implemented', ),
            },
            'Add Values': {
                'IS': lambda: interactor.feedback_user('to be implemented', ),
                'BS': lambda: interactor.feedback_user('to be implemented', ),
                'CF': lambda: interactor.feedback_user('to be implemented', ),
                'BS IS': lambda: interactor.feedback_user('to be implemented', ),
                'DCF': lambda: interactor.feedback_user('to be implemented', ),

            },
        },
        'Help': {},

    }

    # Auto save
    for key_main, command_dictionary in menu_bar_model.items():
        for key_sub, command_or_dict in command_dictionary.items():
            if type(command_or_dict) == dict:
                menu_bar_model[key_main][key_sub] = {}
                for key_sub_sub, command in command_or_dict.items():
                    entry_by = f'{key_main}-{key_sub}={key_sub_sub}'
                    args = command, interactor, entry_by
                    menu_bar_model[key_main][key_sub][key_sub_sub] = c.decorator_entry_and_exit_point(*args)
            else:
                command = command_or_dict
                if command not in dont_wrap_these_commands_with_auto_save:
                    entry_by = f'{key_main}-{key_sub}'
                    menu_bar_model[key_main][key_sub] = c.decorator_entry_and_exit_point(command, interactor, entry_by)
    return menu_bar_model


def save_data_table(interactor: BoundaryInABC):
    interactor.save_data_table('DataTable.xlsx')
