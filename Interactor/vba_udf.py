from typing import Iterable
from typing import Tuple

from . import implementation_9 as impl
from .. import Utilities
from ..Entities import Connections
from ..Entities import Shapes
from ..Utilities import rpe_to_normal


def get_arguments_to_vba_udf(account_used_in_udf, argument_converter, connections, shapes):
    circular_safe_accounts = impl.get_circular_reference_free_accounts(connections, shapes)
    arguments = []
    for arg in sorted(tuple(circular_safe_accounts)):
        if shapes.get_tag_type(arg) in ('account',):
            if arg in account_used_in_udf:
                arg_converted = arg if argument_converter is None else argument_converter(arg, shapes)
                arguments.append(arg_converted)
    return tuple(arguments)


def get_accounts_used_in_user_defined_function(dependencies: Iterable, rpe_raw_sorted: Iterable, shapes: Shapes) -> set:
    account_used_in_user_defined_function = set()
    for account, expression_raw in rpe_raw_sorted:
        if account in dependencies:
            for element in expression_raw:

                shape_type = shapes.get_tag_type(element)
                if shape_type == 'account':
                    account_used_in_user_defined_function.add(element)
    return account_used_in_user_defined_function


def get_udf_formulas(dependencies: Iterable, rpe_raw_sorted: Iterable, shapes: Shapes) -> Tuple[tuple, set]:
    formulas_list = []
    variables = set()
    for account, expression_raw in rpe_raw_sorted:
        if account in dependencies:
            rpe_expression = []
            variables.add(shape_id_to_vba_variable_name(account, shapes))
            for element in expression_raw:
                shape_type = shapes.get_tag_type(element)
                text = shapes.get_text(element)
                if shape_type == 'account':
                    rpe_expression.append(shape_id_to_vba_variable_name(element, shapes))
                    variables.add(shape_id_to_vba_variable_name(element, shapes))
                elif shape_type == 'constant':
                    rpe_expression.append(text)
                elif shape_type == 'operator':
                    rpe_expression.append(rpe_to_normal.operator[text])
            formula = rpe_to_normal.post_to_infix(tuple(rpe_expression))
            formulas_list.append(f'{shape_id_to_vba_variable_name(account, shapes)} = {formula}')
    formulas = tuple(formulas_list)
    return formulas, variables


def get_udf_direct_links(dependencies: Iterable, direct_links: Iterable, shapes: Shapes,
                         variables: set) -> Tuple[tuple, set]:
    direct_links_list = []
    converter = shape_id_to_vba_variable_name
    account_tos = tuple(element[1] for element in direct_links)
    _, direct_links_sorted = Utilities.sort_lists(account_tos, direct_links)
    for direct_link in direct_links_sorted:
        ac_from, ac_to, shift = direct_link

        variables.add(shape_id_to_vba_variable_name(ac_to, shapes))
        if ac_to in dependencies and shift == 0:
            direct_links_list.append((converter(ac_from, shapes), converter(ac_to, shapes)))
    return tuple(direct_links_list), variables


def create_gateway_model_for_vba_udf(arguments, direct_links, file_name, formulas, shape_id, shapes, variables) -> dict:
    gateway_model = {
        'folder_name': file_name,
        'max_loop': 10000,
        'tolerance': 0.0001,
        'arguments': arguments,
        'name': 'user_defined_function',
        'formulas': formulas,
        'direct_links_mutable': direct_links,
        'variables': tuple(sorted(list(variables))),
        'target_value': shape_id_to_vba_variable_name(shape_id, shapes),
        'minimum_iteration': 10,
    }
    return gateway_model


def shape_id_to_vba_variable_name(shape_id, shapes) -> str:
    replace = {' ': '_',
               '&': '',
               '-': '',
               }
    variable_name = f'var_{str(shape_id)}_{shapes.get_text(shape_id)}'.lower()
    for key, value in replace.items():
        variable_name = variable_name.replace(key, value)
    return variable_name


def create_gateway_model(connections: Connections, direct_links: Iterable, file_name, dependencies: Iterable,
                         rpe_raw_sorted: Iterable, shape_id, shapes: Shapes) -> dict:
    formulas, variables = get_udf_formulas(dependencies, rpe_raw_sorted, shapes)
    account_used_in_udf = get_accounts_used_in_user_defined_function(dependencies, rpe_raw_sorted, shapes)
    direct_links, variables = get_udf_direct_links(dependencies, direct_links, shapes, variables)
    arguments = get_arguments_to_vba_udf(account_used_in_udf, shape_id_to_vba_variable_name, connections, shapes)
    args = arguments, direct_links, file_name, formulas, shape_id, shapes, variables
    return create_gateway_model_for_vba_udf(*args)
