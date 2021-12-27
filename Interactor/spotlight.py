from typing import Iterable


def get_all_group_and_names_(pickle_commands_file_names: Iterable, pickle_file_names: Iterable):
    templates = get_templates(pickle_file_names)
    macros = get_macros(pickle_commands_file_names)
    return templates + macros


def get_macros(pickle_commands_file_names) -> tuple:
    macros = tuple(('Macro', file_name) for file_name in pickle_commands_file_names)
    return macros


def get_templates(pickle_file_names) -> tuple:
    templates = tuple(('Transaction', file_name) for file_name in pickle_file_names)
    return templates
