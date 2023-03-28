from typing import Callable

from .. import Entities


def add_command_select_accounts(e: Entities, sheet: str, add_command_always: Callable):
    command = 'select_account_by_name'
    common_looping_method(command, e, sheet, add_command_always, get_args_pattern_1)


def set_sensitivity_account_by_name(e: Entities, sheet: str, add_command_always: Callable):
    command = 'set_sensitivity_variable_account_by_name'
    common_looping_method(command, e, sheet, add_command_always, get_args_pattern_1)


def set_sensitivity_delta_by_name(e: Entities, sheet: str, add_command_always: Callable):
    command = 'set_sensitivity_delta_by_name'
    common_looping_method(command, e, sheet, add_command_always, get_args_pattern_2)


def common_looping_method(command, e, sheet, add_command_always, get_args):
    for shape_id in e.selection.data:
        text = e.shapes.get_text(shape_id)
        n = 0
        for shape in e.worksheets.selected_sheet_contents:
            if shape_id == shape:
                kw = {'text': text, 'sheet': sheet, 'n': n}
                add_command_always(command, get_args(**kw))
                break
            elif e.shapes.get_text(shape) == text:
                n += 1


def get_args_pattern_1(**kw):
    return kw.get('text'), kw.get('sheet'), kw.get('n')


def get_args_pattern_2(**kw):
    return kw.get('text'), kw.get('sheet'), kw.get('n'), 10
