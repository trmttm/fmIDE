from typing import Any
from typing import Callable
from typing import Iterable

from ..Entities import Configurations
from ..Entities import Connections
from ..Entities import InputDecimals
from ..Entities import InputRanges
from ..Entities import Shapes

slider_range = 'slider_range'
slider_handle = 'slider_handle'
slider_min = 'slider_min'
slider_max = 'slider_max'
slider_gauge = 'slider_gauge'
slider_decimal = 'slider_decimal'
slider_non_handle_items = (slider_range, slider_min, slider_max, slider_gauge, slider_decimal)


def add_slider(coordinate, min_max, add_new_shape, connections: Connections, shapes: Shapes,
               configurations: Configurations, decimal: int = 1) -> Any:
    x, y = coordinate
    min_, max_ = min_max if min_max is not None else (0, 100)
    slider_w = configurations.slider_w
    slider_h = configurations.slider_h
    range_w = configurations.slider_range_w
    range_h = configurations.slider_range_h
    decimal_w = configurations.slider_decimal_w
    decimal_h = configurations.slider_decimal_h
    handle_h = configurations.slider_handle_h
    handle_y = y + slider_h - handle_h / 2
    range_dx = configurations.slider_range_dx

    slider_id = add_new_shape('', slider_range)
    handle_id = add_new_shape('', slider_handle)
    min_id = add_new_shape(min_, slider_min)
    max_id = add_new_shape(max_, slider_max)
    gauge_id = add_new_shape(min_, slider_gauge)
    decimal_id = add_new_shape(decimal, slider_decimal)

    connections.add_connection(min_id, slider_id)
    connections.add_connection(max_id, slider_id)
    connections.add_connection(handle_id, slider_id)
    connections.add_connection(decimal_id, slider_id)
    connections.add_connection(gauge_id, handle_id)

    shapes.set_x(slider_id, x)
    shapes.set_y(slider_id, y)
    shapes.set_width(slider_id, slider_w)
    shapes.set_height(slider_id, slider_h)

    shapes.set_x(handle_id, x)
    shapes.set_y(handle_id, handle_y)
    shapes.set_width(handle_id, slider_w)
    shapes.set_height(handle_id, handle_h)

    shapes.set_x(max_id, x + range_dx)
    shapes.set_y(max_id, y - range_h / 2)
    shapes.set_width(max_id, range_w)
    shapes.set_height(max_id, range_h)

    shapes.set_x(min_id, x + range_dx)
    shapes.set_y(min_id, y + slider_h - range_h / 2)
    shapes.set_width(min_id, range_w)
    shapes.set_height(min_id, range_h)

    shapes.set_x(gauge_id, x + range_dx)
    shapes.set_y(gauge_id, _get_gauge_y(handle_y, handle_h, range_h))
    shapes.set_width(gauge_id, range_w)
    shapes.set_height(gauge_id, range_h)

    shapes.set_x(decimal_id, x - (decimal_w - slider_w) / 2)
    shapes.set_y(decimal_id, y + slider_h + 20)
    shapes.set_width(decimal_id, decimal_w)
    shapes.set_height(decimal_id, decimal_h)

    shapes.get_y = _decorator(shapes.get_y, shapes, gauge_id, handle_id)

    return slider_id


def restrict_handle_move_range(handle_ids, delta_x, delta_y, shapes: Shapes, connections: Connections):
    if handle_ids:
        delta_x = 0

        new_delta_y = delta_y
        for handle_id in handle_ids:
            max_y, min_y = _get_min_max_from_slider_handle_id(handle_id, connections, shapes)
            handle_y, handle_h = shapes.get_y(handle_id), shapes.get_height(handle_id)
            if delta_y > 0:
                new_delta_y = min(new_delta_y, max_y - handle_y - handle_h / 2)
            else:
                new_delta_y = max(new_delta_y, min_y - handle_y - handle_h / 2)
        delta_y = new_delta_y
    return delta_x, delta_y


def drag_gauges_with_handles(handle_ids, shape_ids, connections: Connections):
    if handle_ids:
        gauges = tuple(connections.get_connections_into(i).pop() for i in handle_ids)
        shape_ids += gauges
    return shape_ids


def drag_slider_items(slider_items, shape_ids, shapes: Shapes, connections: Connections):
    if slider_items:
        slider_items_to_drag = set()
        for slider_item in slider_items:
            tag_type = shapes.get_tag_type(slider_item)
            slider_id = None
            if tag_type in (slider_max, slider_min, slider_decimal):
                slider_id = connections.get_connections_out_of(slider_item).pop()
            elif tag_type == slider_range:
                slider_id = slider_item
            elif tag_type == slider_gauge:
                handle_id = connections.get_connections_out_of(slider_item).pop()
                slider_id = get_slider_id_from_handle_id(handle_id, connections)

            slider_items_to_drag.add(slider_id)
            handle_min_max_inputs = connections.get_connections_into(slider_id)
            for element in handle_min_max_inputs:
                tag_type = shapes.get_tag_type(element)
                if tag_type == slider_handle:
                    gauge_id = connections.get_connections_into(element).pop()
                    slider_items_to_drag.add(element)
                    slider_items_to_drag.add(gauge_id)
                else:
                    slider_items_to_drag.add(element)
        return tuple(set(shape_ids).union(slider_items_to_drag))
    else:
        return shape_ids


def update_gauges_values(handle_ids, shapes: Shapes, connections: Connections, input_decimals: InputDecimals):
    if handle_ids:
        values = get_values_from_handle_ids(connections, handle_ids, shapes)
        for handle_id, value in zip(handle_ids, values):
            gauge_id = _get_gauge_id_from_slider_handle(handle_id, connections, shapes)
            if value is not None:
                slider_id = get_slider_id_from_handle_id(handle_id, connections)
                input_ids = get_input_ids_from_slider_id(slider_id, connections, shapes)
                if input_ids:
                    decimals = input_decimals.get_decimals(input_ids[0])
                else:
                    decimals = 0
                shapes.set_text(gauge_id, round(value, decimals))
            else:
                shapes.set_text(gauge_id, '??')


def update_inputs_values(handle_ids, shapes: Shapes, connections: Connections, input_ranges: InputRanges,
                         input_decimals: InputDecimals, set_input_values: Callable):
    if handle_ids:
        values = get_values_from_handle_ids(connections, handle_ids, shapes)
        for handle_id, value in zip(handle_ids, values):
            if value is not None:
                slider_id = get_slider_id_from_handle_id(handle_id, connections)
                input_ids = get_input_ids_from_slider_id(slider_id, connections, shapes)
                min_max = get_min_value_max_value_from_slider_id(slider_id, connections, shapes)
                decimals = _get_decimal_value_from_slider_id(slider_id, connections, shapes)
                for input_id in input_ids:
                    input_decimals.set_decimals(input_id, decimals)
                    set_input_values(input_id, round(value, decimals))
                    input_ranges.set_range(input_id, min_max)


def _decorator(f, shapes: Shapes, linker, linked):
    def wrapper(shape_id):
        if shape_id == linked:
            y1 = f(linked)
            handle_h = shapes.get_height(linked)
            gauge_h = shapes.get_height(linker)
            y2 = _get_gauge_y(y1, handle_h, gauge_h)
            shapes.set_y(linker, y2)
            return y1
        else:
            return f(shape_id)

    return wrapper


def _get_gauge_y(handle_y, handle_h, gauge_h) -> int:
    return (handle_y + (handle_y + handle_h)) / 2 - gauge_h / 2


def selections_are_all_slider_handles(shape_ids, shapes: Shapes) -> bool:
    return tuple(shapes.get_tag_type(i) for i in shape_ids) == (slider_handle,) * len(shape_ids)


def extract_slider_items_except_handle(shape_ids, shapes: Shapes) -> tuple:
    slider_items = tuple(i for i in shape_ids if shapes.get_tag_type(i) in slider_non_handle_items)
    return slider_items


def _get_min_max_from_slider_handle_id(handle_id, connections: Connections, shapes: Shapes):
    slider_id = get_slider_id_from_handle_id(handle_id, connections)
    return _get_min_max_from_slider_id(slider_id, shapes)


def get_slider_id_from_handle_id(handle_id, connections: Connections):
    slider_id = connections.get_connections_out_of(handle_id).pop()
    return slider_id


def _get_min_max_from_slider_id(slider_id, shapes: Shapes) -> tuple:
    min_y, max_y = shapes.get_y(slider_id), shapes.get_y(slider_id) + shapes.get_height(slider_id)
    return max_y, min_y


def get_input_ids_from_slider_id(slider_id, connections, shapes) -> tuple:
    ac_or_relay = ('account', 'relay')
    f = shapes.get_shape_it_represents_or_self
    acs = tuple(f(i) for i in connections.get_connections_into(slider_id) if shapes.get_tag_type(i) in ac_or_relay)
    return acs


def _get_gauge_id_from_slider_handle(handle_id, connections: Connections, shapes: Shapes):
    return tuple(i for i in connections.get_connections_into(handle_id) if shapes.get_tag_type(i) == slider_gauge)[0]


def get_values_from_handle_ids(connections, handle_ids, shapes) -> tuple:
    values = []
    for handle_id in handle_ids:
        min_y, max_y = _get_min_max_from_slider_handle_id(handle_id, connections, shapes)
        min_value, max_values = _get_min_value_max_value_from_handle_id(handle_id, connections, shapes)
        slider_id = get_slider_id_from_handle_id(handle_id, connections)
        decimal = _get_decimal_value_from_slider_id(slider_id, connections, shapes)
        if None not in (min_value, max_values):
            y = shapes.get_y(handle_id)
            handle_h = shapes.get_height(handle_id)
            relative_position = (y + handle_h / 2 - min_y) / (max_y - min_y)
            value = round(min_value + (max_values - min_value) * relative_position, decimal)
        else:
            value = None
        values.append(value)
    return tuple(values)


def _get_min_value_max_value_from_handle_id(handle_id, connections: Connections, shapes: Shapes):
    slider_id = get_slider_id_from_handle_id(handle_id, connections)
    return get_min_value_max_value_from_slider_id(slider_id, connections, shapes)


def get_min_value_max_value_from_slider_id(slider_id, connections, shapes):
    min_id, max_id = _get_min_id_and_max_id_from_slider_id(slider_id, connections, shapes)
    try:
        min_value = float(shapes.get_text(min_id))
    except ValueError:
        min_value = None
    try:
        max_value = float(shapes.get_text(max_id))
    except ValueError:
        max_value = None
    return min_value, max_value


def _get_decimal_value_from_slider_id(slider_id, connections, shapes):
    connections_into_slider = connections.get_connections_into(slider_id)
    decimal_id = tuple(i for i in connections_into_slider if shapes.get_tag_type(i) == slider_decimal)[0]
    try:
        decimal_value = int(shapes.get_text(decimal_id))
    except ValueError:
        decimal_value = None
    return decimal_value


def _get_min_id_and_max_id_from_slider_id(slider_id, connections: Connections, shapes: Shapes):
    connections_into_slider = connections.get_connections_into(slider_id)
    max_id = tuple(i for i in connections_into_slider if shapes.get_tag_type(i) == slider_max)[0]
    min_id = tuple(i for i in connections_into_slider if shapes.get_tag_type(i) == slider_min)[0]
    return min_id, max_id


def add_sliders_for_selected_inputs(inputs_or_their_relays: tuple, add_new_shape: Callable, connections: Connections,
                                    input_ranges: InputRanges, input_decimals: InputDecimals, shapes: Shapes,
                                    configurations: Configurations) -> tuple:
    slider_ids = []
    relative_position = (150, 0)
    for input_or_its_relay in inputs_or_their_relays:
        input_id = shapes.get_shape_it_represents_or_self(input_or_its_relay)
        decimals = input_decimals.get_decimals(input_id)
        min_max = input_ranges.get_ranges(input_id)
        base_id = input_or_its_relay if input_id != input_or_its_relay else input_id

        coordinate = (shapes.get_x(base_id) + relative_position[0], shapes.get_y(base_id) + relative_position[1])

        slider_id = add_slider(coordinate, min_max, add_new_shape, connections, shapes, configurations, decimals)
        slider_ids.append(slider_id)
    return tuple(slider_ids)


def get_slider_ids(shape_ids, connections: Connections, shapes: Shapes) -> tuple:
    slider_ids = set()
    for shape_id in shape_ids:
        slider_id = None

        tag_type = shapes.get_tag_type(shape_id)
        if tag_type == slider_range:
            slider_id = shape_id
        elif tag_type in (slider_min, slider_max, slider_handle, slider_decimal):
            slider_id = connections.get_connections_out_of(shape_id).pop()
        elif tag_type == slider_gauge:
            handle_id = connections.get_connections_out_of(shape_id).pop()
            slider_id = connections.get_connections_out_of(handle_id).pop()

        if slider_id is not None:
            slider_ids.add(slider_id)

    return tuple(slider_ids)


def create_args_to_cache_data_table(shape_ids: Iterable, connections: Connections, shapes: Shapes):
    slider_ids = get_slider_ids(shape_ids, connections, shapes)
    if slider_ids:
        slider_id = slider_ids[0]
        min_v, max_v = get_min_value_max_value_from_slider_id(slider_id, connections, shapes)
        decimal = _get_decimal_value_from_slider_id(slider_id, connections, shapes)
        increment = 1 / (10 ** decimal)
        total_steps = int((max_v - min_v) / increment)
        input_ids = get_input_ids_from_slider_id(slider_id, connections, shapes)
        input_values = tuple(min_v + n * (max_v - min_v) / total_steps for n in range(total_steps)) + (max_v,)
        return input_ids, input_values
