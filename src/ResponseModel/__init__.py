from typing import Callable
from typing import Iterable

from src import Utilities
from src.Presenter.HighlightShape import highlight as h


def response_model_to_presenter_highlight_auto(audit_results: Iterable) -> dict:
    response_model = {h.key_method: h.key_auto,
                      h.key_highlight_datas: audit_results,
                      }
    return response_model


def response_model_to_presenter_highlight_manual(shapes_data: dict, get_canvas_tag: Callable,
                                                 shape_ids: Iterable) -> dict:
    highlight_datas = []
    for shape_id in shape_ids:
        shape_data = shapes_data[shape_id]
        canvas_tag = get_canvas_tag(shape_id)
        highlight_datas.append({h.key_canvas_tag: canvas_tag, h.key_shape_id: shape_id, h.key_shape_data: shape_data})

    response_model = {h.key_method: h.key_manual, h.key_highlight_datas: highlight_datas, }
    return response_model


def response_model_to_presenter_connect(connections_data, get_coords: Callable, selected: Iterable = None,
                                        circular_connections: tuple = None, no_arrows: Iterable = None) -> list:
    f = connection_response_model
    cc = circular_connections
    s = selected
    na = no_arrows
    response_model = [f(get_coords, from_id, to_id, s, cc, na) for (from_id, to_id) in connections_data]
    return response_model


def connection_response_model(get_coords, from_id, to_id, selected: Iterable = None, circular_connections: tuple = None,
                              no_arrows: Iterable = None) -> dict:
    selected = selected or ()
    circular_connections = circular_connections or ()
    response_model_element = {
        'coordinates': Utilities.get_nearest_points(get_coords(from_id), get_coords(to_id)),
        'selected': (from_id, to_id) in selected,
        'circular': (from_id, to_id) in circular_connections,
    }
    if no_arrows not in (None, ()):
        if to_id in no_arrows:
            response_model_element.update({'arrow': None})
    return response_model_element


def response_model_to_presenter_move_shapes(shape_ids, delta_x, delta_y, shapes_data: dict) -> dict:
    response_model = {}
    for shape_id in shape_ids:
        tag = shapes_data[shape_id]['tags'][0]
        response_model[tag] = (delta_x, delta_y)
    return response_model


def response_model_to_presenter_update_status_bar(text, feedback_type: str = 'normal', is_incremental_progress=False):
    response_model = {'text': text, 'feedback_type': feedback_type, 'incremental_progress': is_incremental_progress}
    return response_model


def response_model_to_presenter_add_shape(shapes_data: dict, new_shape_ids: Iterable,
                                          shape_id_to_font_size: dict = None) -> dict:
    list_of_shape_datas = []
    if shape_id_to_font_size is None:
        shape_id_to_font_size = {}
    for shape_id in new_shape_ids:
        each_shape_data = shapes_data[shape_id]
        if 'live_value' in each_shape_data['tags']:
            each_shape_data.update({'text_align': 'right'})
        font_size = shape_id_to_font_size.get(shape_id, None)
        if font_size is not None:
            shapes_data[shape_id]['font_size'] = font_size
        list_of_shape_datas.append(each_shape_data)
    return dict(zip(new_shape_ids, list_of_shape_datas))


def response_model_to_presenter_draw_rectangle(rectangle_selector_data: dict):
    response_model = rectangle_selector_data
    for id_, data in rectangle_selector_data.items():
        data.update({'tags': ('rectangle_selector',)})

    return response_model


def response_model_to_presenter_draw_line(lines_data):
    response_model = lines_data
    return response_model


def response_model_to_presenter_load_pickle_files_list(file_names: Iterable):
    response_model = {'file_names': file_names}
    return response_model


def response_model_to_presenter_update_account_order(account_names: Iterable, select_flags: Iterable[bool]):
    response_model = {'account_names': account_names, 'select_flags': select_flags}
    return response_model


def response_model_to_presenter_update_commands(commands: Iterable, select_flags: Iterable[bool] = None) -> dict:
    select_flags = select_flags or tuple(False for _ in commands)
    response_model = {'commands': commands, 'select_flags': select_flags}
    return response_model


def response_model_to_presenter_update_macros(macros: Iterable, select_flags: Iterable[bool] = None) -> dict:
    select_flags = select_flags or tuple(False for _ in macros)
    response_model = {'macros': macros, 'select_flags': select_flags}
    return response_model


def audit_shape(shape_id, is_selected: bool, tag_type, canvas_tag, connections_in, depending_on_external_sheet: bool,
                depended_by_external_sheet: bool, format_data: dict = None, height=None, fill=None) -> dict:
    audit_result = {
        h.key_shape_id: shape_id,
        h.key_tag_type: tag_type,
        h.key_canvas_tag: canvas_tag,
        h.key_selected: is_selected,

        h.key_is_input_account: (tag_type == h.key_account) and (len(connections_in) == 0),
        h.key_depending_on_external_sheet: depending_on_external_sheet,
        h.key_is_depended_by_external_sheet: depended_by_external_sheet,
    }
    if format_data is not None:
        if 'heading' in format_data:
            audit_result.update({h.key_is_heading: shape_id in format_data['heading']})
        if 'total' in format_data:
            audit_result.update({h.key_is_total: shape_id in format_data['total']})
    if height is not None:
        audit_result.update({h.key_height: height})
    if fill is not None:
        audit_result.update({h.key_specified_fill: fill})
    return audit_result


def response_model_to_presenter_shape_properties(text, x, y, width, height, worksheet, shape_id, formats,
                                                 number_formats, vertical_references, uoms) -> dict:
    return {'text': text, 'x': x, 'y': y, 'width': width, 'height': height, 'worksheet': worksheet, 'id': shape_id,
            'formats': formats, 'number_formats': number_formats, 'vertical_references': vertical_references,
            'uoms': uoms}


def response_model_to_presenter_states(shape_ids, shapes_positions, texts, connections, operators, rpes,
                                       input_accounts, input_accounts_text, sheet, connection_ids,
                                       vertical_accounts) -> dict:
    response_model = {
        'shape_ids': shape_ids,
        'shapes_positions': shapes_positions,
        'texts': texts,
        'connections': connections,
        'operators': operators,
        'rpes': rpes,
        'inputs': input_accounts,
        'input_accounts_text': input_accounts_text,
        'worksheet_information': sheet,
        'connection_ids': connection_ids,
        'vertical_acs': vertical_accounts,
    }
    return response_model


def response_model_to_presenter_worksheets(sheet_names: tuple, selected=None,
                                           sheet_name_to_parent: dict = None) -> dict:
    if selected is not None:
        select_flags = tuple(sheet_name == selected for sheet_name in sheet_names)
    else:
        select_flags = tuple(sheet_name == sheet_names[-1] for sheet_name in sheet_names)
    response_model = {'sheet_names': sheet_names, 'select_flags': select_flags}
    if sheet_name_to_parent is not None:
        response_model.update({'sheet_name_to_parent': sheet_name_to_parent})
    return response_model


def response_model_to_presenter_show_input_entry(input_text: str, input_values: tuple, number_of_periods: int,
                                                 y_range: tuple, decimals: int = None, input_id='', uom='') -> dict:
    response_model = {'text': input_text, 'values': input_values, 'nop': number_of_periods, 'y_range': y_range,
                      'input_id': input_id, 'uom': uom}
    if decimals is not None:
        response_model.update({'decimals': decimals})
    return response_model


def response_model_to_presenter_update_connection_ids(types_and_names: tuple, select_flags: tuple) -> dict:
    return {'type_and_names': types_and_names, 'select_flags': select_flags}


def response_model_to_presenter_accounts(input_accounts: tuple, texts: tuple, worksheets: tuple) -> dict:
    return {'accounts': input_accounts, 'texts': texts, 'worksheets': worksheets}


def response_model_to_presenter_accounts_with_deltas(input_accounts: tuple, texts: tuple, worksheets: tuple,
                                                     deltas: tuple) -> dict:
    response_model = response_model_to_presenter_accounts(input_accounts, texts, worksheets)
    response_model.update({'deltas': deltas})
    return response_model
