from typing import Callable

from . import slider
from ..Entities import Connections
from ..Entities import Shapes


def get_data_table_from_cache(key, cache_data_table: dict, feedback_user: Callable) -> dict:
    data_table = None
    if cache_data_table != {}:
        if key is not None:
            data_table = cache_data_table.get(key, None)
            if data_table is not None:
                feedback_user(f'Cache {key}', 'success')
    return data_table


def get_data_table_cache_key_from_inputs_and_values(input_ids: tuple, input_values: tuple):
    if input_ids:
        input_id = input_ids[0]
        input_value = input_values[0]
        key = input_id, input_value
        return key


def get_data_table_cache_key_from_handle_ids(handle_ids: tuple, connections: Connections, shapes: Shapes):
    handle_id = handle_ids[0]
    slider_id = slider.get_slider_id_from_handle_id(handle_id, connections)
    input_ids = slider.get_input_ids_from_slider_id(slider_id, connections, shapes)
    input_values = slider.get_values_from_handle_ids(connections, handle_ids, shapes)
    key = get_data_table_cache_key_from_inputs_and_values(input_ids, input_values)
    return key
