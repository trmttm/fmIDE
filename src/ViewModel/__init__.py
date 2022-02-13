from typing import Any
from typing import Dict
from typing import Iterable
from typing import List

from src import Utilities


def create_view_model_add_shape(response_model: dict) -> List[dict]:
    return list(response_model.values())


def create_tree_data(parent: str, index: str, text: str, values: tuple, tags: tuple, select: bool, id_=None) -> dict:
    tree_data = {
        'parent': parent,
        'index': index,
        'text': text,
        'values': values,
        'tags': tags,
        'select_this_item': select
    }
    if id_ is not None:
        tree_data['id'] = id_
    return tree_data


def create_view_model_tree(headings: tuple, widths: tuple, tree_datas: Iterable, stretches: tuple, scroll_v: bool,
                           scroll_h: bool) -> dict:
    return {'tree_datas': tree_datas, 'headings': headings, 'widths': widths, 'stretches': stretches,
            'scroll_v': scroll_v, 'scroll_h': scroll_h, }


def create_view_model_pickle_loader_list(response_model: dict) -> dict:
    headings = ('No', 'Name')
    widths = (50, 200)
    stretches = (False, True)
    scroll_v, scroll_h = False, False
    file_names = response_model['file_names']
    always_false = False
    tree_datas = [create_tree_data('', f'{n}', '', (n, name), (), always_false) for (n, name) in enumerate(file_names)]
    view_model = create_view_model_tree(headings, widths, tree_datas, stretches, scroll_v, scroll_h)
    return view_model


def create_view_model_update_account_order(response_model: dict):
    headings = ('No', 'Name')
    widths = (30, 100)
    stretches = (False, True)
    scroll_v, scroll_h = False, False
    account_names = response_model['account_names']
    select = response_model['select_flags']
    tree_datas = [create_tree_data('', f'{n}', '', (n, name), (), select[n]) for (n, name) in enumerate(account_names)]
    view_model = create_view_model_tree(headings, widths, tree_datas, stretches, scroll_v, scroll_h)
    return view_model


def create_view_model_update_accounts(response_model: dict) -> dict:
    headings = ('No', 'ID', 'Account Name', 'Sheet')
    widths = (50, 50, 100, 100)
    stretches = (False, False, True, False)
    scroll_v, scroll_h = False, False

    input_accounts = response_model['accounts']
    texts = response_model['texts']
    worksheets = response_model['worksheets']
    data = zip(input_accounts, texts, worksheets)
    f = create_tree_data
    tree_datas = [f('', f'{n}', '', (n, id_, name, sh), (), False) for (n, (id_, name, sh)) in enumerate(data)]

    view_model = create_view_model_tree(headings, widths, tree_datas, stretches, scroll_v, scroll_h)
    return view_model


def create_view_model_update_accounts_with_deltas(response_model: dict) -> dict:
    headings = ('No', 'ID', 'Deltas', 'Account Name', 'Sheet')
    widths = (50, 50, 50, 100, 100)
    stretches = (False, False, False, True, False)
    scroll_v, scroll_h = False, False

    input_accounts = response_model['accounts']
    deltas = response_model['deltas']
    texts = response_model['texts']
    worksheets = response_model['worksheets']
    data = zip(input_accounts, deltas, texts, worksheets)
    f = create_tree_data
    tree_datas = [f('', f'{n}', '', (n, id_, d, name, sh), (), False) for (n, (id_, d, name, sh)) in enumerate(data)]

    view_model = create_view_model_tree(headings, widths, tree_datas, stretches, scroll_v, scroll_h)
    return view_model


def create_view_model_worksheets(response_model):
    def get_parent_id(sheet_name):
        return sheet_name_to_parent.get(sheet_name, None) or ''

    gp = get_parent_id
    headings = ('No', 'Worksheets Name')
    widths = (30, 100)
    stretches = (False, True)
    scroll_v, scroll_h = False, False
    ws_names: tuple = response_model['sheet_names']
    select: tuple = response_model['select_flags']
    sheet_name_to_parent = response_model.get('sheet_name_to_parent', {})
    f = create_tree_data
    tree_datas = [f(gp(name), f'{n}', name, (n, name), (), select[n], name) for (n, name) in enumerate(ws_names)]
    view_model = create_view_model_tree(headings, widths, tree_datas, stretches, scroll_v, scroll_h)
    view_model.update({'text_width': 130})
    return view_model


def create_view_model_connection_ids(response_model):
    headings = ('No', 'Type', 'Connection_IDs')
    widths = (30, 50, 100)
    stretches = (False, False, True)
    scroll_v, scroll_h = False, False
    types_names: tuple = response_model['type_and_names']
    select: tuple = response_model['select_flags']
    tree_datas = []
    for n, (id_type, id_name) in enumerate(types_names):
        data = create_tree_data('', f'{n}', '', (n, id_type, id_name), (), select[n])
        tree_datas.append(data)
    view_model = create_view_model_tree(headings, widths, tree_datas, stretches, scroll_v, scroll_h)
    return view_model


def create_view_model_user_feedback(response_model: dict) -> dict:
    text = response_model['text']
    feedback_type = response_model.get('feedback_type', 'normal')

    if 'incremental_progress' in response_model:
        update = response_model['incremental_progress']
    else:
        update = False

    color = {'normal': 'black', 'error': 'red', 'success': 'green'}
    return {'text': text, 'text_color': color[feedback_type], 'update': update}


def create_view_model_connect_shapes(response_model) -> list:
    view_model = []
    for connection_data in response_model:
        color = 'black'
        if connection_data['selected']:
            color = 'red'
        if ('circular' in connection_data) and connection_data['circular']:
            color = 'red'
        view_model_element = {'coordinates': connection_data['coordinates'], 'color': color}

        if 'arrow' in connection_data:
            view_model_element.update({'arrow': connection_data['arrow']})

        view_model.append(view_model_element)

    return view_model


def create_view_model_update_properties(response_model: dict) -> dict:
    view_model = {
        'text': response_model['text'],
        'x': view_format(response_model["x"]),
        'y': view_format(response_model["y"]),
        'width': view_format(response_model["width"]),
        'height': view_format(response_model["height"]),
        'worksheet': view_format(response_model["worksheet"]),
        'id': response_model["id"],
        'formats': response_model["formats"],
        'number_formats': response_model["number_formats"],
        'vertical_references': response_model["vertical_references"],
        'uoms': response_model["uoms"],
    }
    return view_model


def create_view_model_input_entry(response_model: dict):
    text = response_model['text']
    values = response_model['values']
    nop = response_model['nop']
    values_str = Utilities.values_tuple_to_values_str(values)
    y_range = response_model['y_range']
    input_id = response_model['input_id']
    uom = response_model['uom']
    view_model = {'text': f'Input Account: {text}', 'values': values, 'values_str': values_str, 'nop': nop,
                  'y_range': y_range, 'input_id': input_id, 'input_name': text, 'uom': uom}
    if 'decimals' in response_model:
        view_model.update({'decimals': response_model['decimals']})
    return view_model


def view_format(value) -> str:
    if Utilities.is_number(value):
        return f'{value:.0f}'
    else:
        return value


def create_view_model_display_states(response_model: dict) -> str:
    shape_ids = response_model['shape_ids']
    shape_positions = response_model['shapes_positions']
    texts = response_model['texts']
    connections = response_model['connections']
    operators = response_model['operators']
    input_accounts = response_model['inputs']
    input_accounts_text = response_model['input_accounts_text']
    rpes: tuple = response_model['rpes']
    worksheet_information: dict = response_model['worksheet_information']
    connection_ids: Dict[str, Dict[Any, tuple]] = response_model['connection_ids']
    vertical_accounts: Dict[Any, tuple] = response_model['vertical_acs']

    operator_texts = tuple(texts[operator_id] for operator_id in operators)
    operator_dict = dict(zip(operators, operator_texts))

    rpe_str = ''
    n = 30
    for rpe in rpes:
        formula_owner = rpe[0]
        i = n - len(formula_owner)
        rpe_str += f'{formula_owner}{" " * i}= {rpe[1]}\n'

    states_str = f'==================================================\n'
    str_names = ('shape_ids', 'connections', 'positions', 'operators',)
    values = (texts, connections, dict(zip(shape_ids, shape_positions)), operator_dict,)
    for j, (str_name, value) in enumerate(zip(str_names, values)):
        i = n - len(str_name)
        if j == 1:
            value = str(value).replace('), ', f'),\n{" " * (n + 3)}')
        else:
            value = str(value).replace(', ', f',\n{" " * (n + 3)}')
        states_str += f'{str_name}{" " * i}= {value}\n'

    states_str += f'\nRPE===============================================\n'
    states_str += rpe_str

    states_str += f'\n==================================================\n'
    str_name = 'Input Accounts'
    i = n - len(str_name)
    input_accounts_dict = dict(zip(input_accounts, input_accounts_text))
    input_accounts_dict = str(input_accounts_dict).replace(', ', f',\n{" " * (n + 3)}')
    states_str += f'{str_name}{" " * i}= {input_accounts_dict}\n'

    states_str += f'\n=================================================='
    for sheet_name, sheet_data in worksheet_information.items():
        states_str += f'\n{sheet_name}\n'
        for j, content in enumerate(sheet_data):
            i = 4 - len(str(j))
            states_str += f'{" " * i}{j}\t{content}\n'

    states_str += f'\n=================================================='
    for key, dictionary in connection_ids.items():
        states_str += f'\n{key}\n'
        for shape_id, connection_ids in dictionary.items():
            i = 4 - len(str(shape_id))
            states_str += f'{" " * i}{shape_id}\t{connection_ids}\n'

    states_str += f'\nVertical Accounts=================================\n'
    for vertical_account, vertical_references in vertical_accounts.items():
        i = 4 - len(str(vertical_account))
        states_str += f'{" " * i}{vertical_account}\t{vertical_references}\n'
    return states_str


def create_view_model_update_commands(response_model: dict):
    headings = ('No', 'Command Name', 'args', 'kwargs')
    widths = (40, 100, 130, 130)
    stretches = (False, True, True, True)
    scroll_v, scroll_h = False, False
    c = response_model['commands']
    select = response_model['select_flags']
    tree_datas = [create_tree_data('', f'{n}', '', (n, key, a, k), (), select[n]) for (n, (key, a, k)) in enumerate(c)]
    view_model = create_view_model_tree(headings, widths, tree_datas, stretches, scroll_v, scroll_h)
    return view_model


def create_view_model_update_macros(response_model: dict):
    headings = ('No', 'Macro Name')
    widths = (30, 250)
    stretches = (False, True)
    scroll_v, scroll_h = False, False
    c = response_model['macros']
    select = response_model['select_flags']
    tree_datas = [create_tree_data('', f'{n}', '', (n, file_name), (), select[n]) for (n, (file_name)) in enumerate(c)]
    view_model = create_view_model_tree(headings, widths, tree_datas, stretches, scroll_v, scroll_h)
    return view_model
