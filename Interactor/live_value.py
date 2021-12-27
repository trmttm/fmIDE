from typing import Callable

from .. import Utilities
from ..Entities import Connections
from ..Entities import InputDecimals
from ..Entities import Shapes

tag_live_value = 'live_value'


def add_new_live_value(shape_id, period: int, add_new_shape: Callable, connections: Connections, shapes: Shapes):
    live_value_id = add_new_shape('', tag_live_value)
    period_id = add_new_shape(str(period), 'constant')

    account_id, position_id = if_relay_connect_to_original_but_position_live_value_near_relay(shape_id, shapes)

    connections.add_connection(period_id, live_value_id)
    connections.add_connection(account_id, live_value_id)

    increment_x = 80
    increment_period_x = 60
    increment_y = 25
    x = shapes.get_x(position_id) + increment_x
    y = shapes.get_y(position_id) + increment_y
    shapes.set_x(live_value_id, x)
    shapes.set_y(live_value_id, y)
    shapes.set_x(period_id, x - increment_period_x)
    shapes.set_y(period_id, y)
    return live_value_id


def if_relay_connect_to_original_but_position_live_value_near_relay(shape_id, shapes):
    original_shape_id = shapes.get_shape_it_represents_or_self(shape_id)
    if original_shape_id != shape_id:
        position_id = shape_id
        account_id = original_shape_id
    else:
        position_id = shape_id
        account_id = shape_id
    return account_id, position_id


def update_live_value(live_value_ids: tuple, data_table: dict, shapes: Shapes, connections: Connections,
                      decimals: InputDecimals):
    for live_value_id in live_value_ids:
        account_id, period = get_account_id_and_period_from_live_id(live_value_id, connections, shapes)
        if None not in (account_id, period):
            string_value = get_value_str_for_live_value(account_id, data_table, period, decimals)
            shapes.set_text(live_value_id, string_value)


def get_value_str_for_live_value(account_id, data_table: dict, period: int, decimals: InputDecimals) -> str:
    decimal = decimals.get_decimals(account_id)
    try:
        value = data_table[account_id][period]
    except KeyError:
        value = 0
    string_value = format(value, f',.{decimal}f')
    return string_value


def get_account_id_and_period_from_live_id(live_value_id, connections: Connections, shapes: Shapes):
    f = shapes.get_shape_it_represents_or_self
    ac_or_relay = ('account', 'relay')
    a = tuple(f(i) for i in connections.get_connections_into(live_value_id) if shapes.get_tag_type(i) in ac_or_relay)
    p = tuple(i for i in connections.get_connections_into(live_value_id) if shapes.get_tag_type(i) == 'constant')
    shape_id = a[0] if a != () else None
    period_id = p[0] if p != () else None
    period = int(shapes.get_text(period_id)) if period_id is not None else None
    return shape_id, period
