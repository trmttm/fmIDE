from typing import Tuple

from src import Utilities


def get_rpes(connections: tuple, positions: dict, operators: tuple) -> tuple:
    formula_dictionary, rpes_raw = create_rpes_and_formulas_to_be_inserted(connections, operators, positions)
    rpes_filtered = filter_rpes_to_remove_formula_without_owner(operators, rpes_raw)
    rpe = replace_operator_pointing_to_another_operator_with_formula(formula_dictionary, rpes_filtered)
    return tuple(rpe)


def create_rpes_and_formulas_to_be_inserted(connections, operators, positions) -> Tuple[dict, tuple]:
    formulas_owned_by_operator = {}
    rpes = []
    for operator in operators:
        formula_owners = get_formula_owners(connections, operator)
        formula = create_formula(connections, operator, positions)

        for formula_owner in formula_owners:
            args = formula, formula_owner, operators
            store_formula_if_operator_is_pointing_to_another_operator(*args, formulas_owned_by_operator)
            rpes.append((formula_owner, formula))
    return formulas_owned_by_operator, tuple(rpes)


def filter_rpes_to_remove_formula_without_owner(operators: tuple, rpes: tuple):
    negative_list = (None,) + operators
    rpe_filetered = []
    for rpe in rpes:
        formula_owner, formula = rpe
        if formula_owner not in negative_list:
            rpe_filetered.append(rpe)
    return rpe_filetered


def replace_operator_pointing_to_another_operator_with_formula(formula_dictionary, rpes_filetered):
    correct_rpe = []
    for rpe in rpes_filetered:
        formula_owner, formula = rpe
        new_formula = recursively_replace_operators_with_formula(formula, formula_dictionary)
        correct_rpe.append((formula_owner, new_formula))
    return correct_rpe


def store_formula_if_operator_is_pointing_to_another_operator(formula, formula_owner, operators, formula_dictionary):
    operator_is_pointing_to_another_operator = formula_owner in operators
    if operator_is_pointing_to_another_operator:
        formula_dictionary[formula[-1]] = formula


def get_all_formula_owners(connections, operators) -> tuple:
    formula_owners = ()
    for operator in operators:
        formula_owners_for_the_operator = get_formula_owners(connections, operator)
        formula_owners += formula_owners_for_the_operator
    return formula_owners


def get_formula_owners(connections, operator) -> tuple:
    formula_owners = []
    for connection in connections:
        connection_from, connection_to = connection
        if operator == connection_from:
            formula_owners.append(connection_to)
    return tuple(formula_owners)


def create_formula(connections, operator, positions) -> tuple:
    operands = get_operands(connections, operator)
    operands_positions = [positions[operand] for operand in operands]
    _, operands_sorted = Utilities.sort_lists(operands_positions, list(operands))
    formula = insert_operators_between_operands(operands_sorted, operator)
    formula = handle_operator_without_operands(formula, operator)
    return formula


def handle_operator_without_operands(formula, operator):
    if formula == ():
        formula = (operator,)
    return formula


def insert_operators_between_operands(operands_sorted, operator) -> tuple:
    if len(operands_sorted) == 1:
        # operator takes only one operand: Abs(A1)
        return operands_sorted[0], operator

    formula_list = []
    for n, operand in enumerate(operands_sorted):
        if n > 0:
            formula_list += [operand, operator]
        else:
            formula_list.append(operand)
    formula = tuple(formula_list)
    return formula


def get_operands(connections: tuple, operator) -> tuple:
    operands = []
    for connection in connections:
        connection_from, connection_to = connection
        if operator == connection_to:
            operands.append(connection_from)
    return tuple(operands)


def get_rpe_readable(rpes: tuple, texts) -> tuple:
    rpe_human_readables = []
    for formula_owner, formula in rpes:
        owner_readable = texts[formula_owner]
        formula_readable = ()
        for element in formula:
            formula_readable += (texts[element],)
        rpe_human_readables.append((owner_readable, formula_readable))
    rpe_human_readables = tuple(rpe_human_readables)
    return rpe_human_readables


def recursively_replace_operators_with_formula(formula: tuple, formula_dictionary: dict, job_done: set = None) -> tuple:
    job_done = set() if job_done is None else job_done
    new_formula = ()
    for element in formula:
        if element in formula_dictionary:
            operator = element

            formula_to_insert = get_formula_without_the_last_operator(operator, formula_dictionary)
            current_job = (formula_to_insert, operator)
            if current_job in job_done:
                new_formula += (element,)
                continue

            job_done.add(current_job)
            formula_flattened = recursively_replace_operators_with_formula(formula_to_insert, formula_dictionary,
                                                                           job_done)
            new_formula += formula_flattened + (operator,)
        else:
            new_formula += (element,)
    return new_formula


def get_formula_without_the_last_operator(element, formula_dictionary):
    return formula_dictionary[element][:-1]


def replace_rpe_element(rpes: tuple, mapper: dict) -> tuple:
    replaced_rpe = []
    for owner, rpe in rpes:
        replaced_rpe.append((owner, tuple(replace_element(element, mapper) for element in rpe)))
    return tuple(replaced_rpe)


def replace_element(element, mapper: dict):
    return mapper[element] if element in mapper else element
