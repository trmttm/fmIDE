from typing import Any
from typing import Iterable
from typing import Tuple

from ..Entities import Configurations
from ..Entities import Connections
from ..Entities import Shapes

tag_y_axis = 'tag_y_axis'
tag_y_min = 'tag_y_min'
tag_y_max = 'tag_y_max'
tag_bar = 'graph_bar'
tag_period = 'graph_period'
graph_items = (tag_y_axis, tag_y_min, tag_y_max, tag_bar, tag_period)

bar_distance = 20
bar_width = 25


def add_y_axis(coordinate, min_max, add_new_shape, connections: Connections, shapes: Shapes,
               configurations: Configurations):
    x, y = coordinate
    min_, max_ = min_max if min_max is not None else (0, 100)
    period = 0
    y_ax_w = configurations.graph_y_ax_w
    y_ax_height = configurations.graph_y_ax_height
    range_w = configurations.graph_range_w
    range_h = configurations.graph_range_h
    period_w = configurations.graph_period_w
    period_h = configurations.graph_period_h
    range_dx = configurations.graph_range_dx

    graph_id = add_new_shape('', tag_y_axis)
    min_id = add_new_shape(min_, tag_y_min)
    max_id = add_new_shape(max_, tag_y_max)
    period_id = add_new_shape(period, tag_period)

    connections.add_connection(min_id, graph_id)
    connections.add_connection(max_id, graph_id)
    connections.add_connection(period_id, graph_id)

    shapes.set_x(graph_id, x)
    shapes.set_y(graph_id, y)
    shapes.set_width(graph_id, y_ax_w)
    shapes.set_height(graph_id, y_ax_height)

    shapes.set_x(max_id, x + range_dx)
    shapes.set_y(max_id, y - range_h / 2)
    shapes.set_width(max_id, range_w)
    shapes.set_height(max_id, range_h)

    shapes.set_x(min_id, x + range_dx)
    shapes.set_y(min_id, y + y_ax_height - range_h / 2)
    shapes.set_width(min_id, range_w)
    shapes.set_height(min_id, range_h)

    shapes.set_x(period_id, x - (period_w - y_ax_w) / 2)
    shapes.set_y(period_id, y + y_ax_height + 20)
    shapes.set_width(period_id, period_w)
    shapes.set_height(period_id, period_h)
    return graph_id


def extract_graph_items(shape_ids, shapes) -> tuple:
    return tuple(i for i in shape_ids if shapes.get_tag_type(i) in graph_items)


def drag_graph_items(graph_items_, shape_ids, shapes: Shapes, connections: Connections) -> tuple:
    if graph_items_:
        graph_items_to_drag = set()
        for graph_item in graph_items_:
            tag_type = shapes.get_tag_type(graph_item)
            graph_id = None
            if tag_type in (tag_y_max, tag_y_min, tag_bar, tag_period):
                graph_id = _get_graph_id_from_graph_item(graph_item, connections, shapes)
            elif tag_type == tag_y_axis:
                graph_id = graph_item

            graph_items_to_drag.add(graph_id)
            for element in connections.get_connections_into(graph_id):
                graph_items_to_drag.add(element)
        return tuple(set(shape_ids).union(graph_items_to_drag))
    else:
        return shape_ids


def _get_graph_id_from_graph_item(max_min_or_bar, connections: Connections, shapes: Shapes):
    g = tuple(i for i in connections.get_connections_out_of(max_min_or_bar) if shapes.get_tag_type(i) == tag_y_axis)
    return g[0]


def add_bar(y_axis_id, add_new_shape, shapes: Shapes, connections: Connections) -> Any:
    bar_id = add_new_shape('', tag_bar)
    existing_bars = tuple(i for i in connections.get_connections_into(y_axis_id) if shapes.get_tag_type(i) == tag_bar)
    number_of_existing_bars = len(existing_bars)

    shapes.set_x(bar_id, shapes.get_x(y_axis_id) + number_of_existing_bars * (bar_distance + bar_width) + bar_distance)
    shapes.set_y(bar_id, shapes.get_y(y_axis_id))
    shapes.set_width(bar_id, bar_width)
    shapes.set_height(bar_id, shapes.get_height(y_axis_id))

    connections.add_connection(bar_id, y_axis_id)
    return bar_id


def get_selected_y_axis(shape_ids: Iterable, shapes: Shapes, connections: Connections) -> tuple:
    selected_y_axis = set()
    for shape_id in shape_ids:
        tag_type = shapes.get_tag_type(shape_id)
        if tag_type in graph_items:
            if tag_type == tag_y_axis:
                y_axis_id = shape_id
                selected_y_axis.add(y_axis_id)
            elif tag_type in (tag_y_max, tag_y_min, tag_bar, tag_period):
                y_axis_id = connections.get_connections_out_of(shape_id).pop()
                selected_y_axis.add(y_axis_id)
    return tuple(selected_y_axis)


def update_bars(data_table: dict, shapes: Shapes, connections: Connections):
    all_y_axis = shapes.get_shapes(tag_y_axis)
    for y_axis_id in all_y_axis:
        y_min_id, y_max_id, bar_ids, period_id = _get_min_max_bars_from_y_axis(y_axis_id, shapes, connections)
        y_max_coord = shapes.get_y(y_axis_id)
        y_min_coord = y_max_coord + shapes.get_height(y_axis_id)
        y_min = float(shapes.get_text(y_min_id))
        y_max = float(shapes.get_text(y_max_id))
        period = int(shapes.get_text(period_id))

        for bar in bar_ids:  # First set y and height of all bars
            connections_into_bar = connections.get_connections_into(bar)
            if len(connections_into_bar) > 0:
                account_id = _get_account_from_bar(bar, connections, shapes)
                if account_id is None:
                    continue
                try:
                    account_value = data_table[account_id][period]
                except KeyError:
                    account_value = 0

                coord, height = _get_bar_coord_and_height(account_value, 0, y_max, y_min, y_max_coord, y_min_coord)
                shapes.set_y(bar, coord)
                shapes.set_height(bar, height)

        for bar in sorted(bar_ids):  # Second, handle waterfall base
            connections_into_bar = connections.get_connections_into(bar)
            if len(connections_into_bar) > 0:
                base_bar = _get_base_bar(bar, connections, shapes)
                if base_bar is None:
                    pass
                elif base_bar < bar:  # Right is higher
                    base = shapes.get_y(base_bar)
                    shapes.set_y(bar, base - shapes.get_height(bar))
        for bar in sorted(bar_ids, reverse=True):  # Second, handle waterfall base
            connections_into_bar = connections.get_connections_into(bar)
            if len(connections_into_bar) > 0:
                base_bar = _get_base_bar(bar, connections, shapes)
                if base_bar is None:
                    pass
                elif base_bar > bar:  # Left is higher
                    base = shapes.get_y(base_bar)
                    shapes.set_y(bar, base - shapes.get_height(bar))


def _get_base_bar(bar_id, connections: Connections, shapes: Shapes):
    bars = tuple(i for i in connections.get_connections_into(bar_id) if shapes.get_tag_type(i) == tag_bar)
    return bars[0] if len(bars) == 1 else None


def _get_account_from_bar(bar_id, connections: Connections, shapes: Shapes):
    f = shapes.get_shape_it_represents_or_self
    ac_or_relay = ('account', 'relay')
    bars = tuple(f(i) for i in connections.get_connections_into(bar_id) if shapes.get_tag_type(i) in ac_or_relay)
    return bars[0] if len(bars) == 1 else None


def _get_bar_coord_and_height(bar_max, bar_min, y_axis_max, y_axis_min, y_max_coord, y_min_coord):
    bar_max_coord = _get_coordinate(bar_max, y_axis_max, y_axis_min, y_min_coord, y_max_coord)
    bar_min_coord = _get_coordinate(bar_min, y_axis_max, y_axis_min, y_min_coord, y_max_coord)
    bar_height = bar_min_coord - bar_max_coord
    return bar_max_coord, bar_height


def _get_coordinate(value, y_axis_max, y_axis_min, y_min_coord, y_max_coord):
    delta_y_axis_coord = y_min_coord - y_max_coord
    delta_y_values = y_axis_max - y_axis_min
    distance_from_y_max_coord = delta_y_axis_coord * (y_axis_max - value) / delta_y_values
    coord = y_max_coord + distance_from_y_max_coord
    return coord


def _get_min_max_bars_from_y_axis(y_axis_id, shapes: Shapes, connections: Connections) -> Tuple[Any, Any, tuple, Any]:
    min_id = None
    max_id = None
    bar_ids = []
    period_id = None
    for i in connections.get_connections_into(y_axis_id):
        tag_type = shapes.get_tag_type(i)
        if tag_type == tag_y_min:
            min_id = i
        elif tag_type == tag_y_max:
            max_id = i
        elif tag_type == tag_bar:
            bar_ids.append(i)
        elif tag_type == tag_period:
            period_id = i
    return min_id, max_id, tuple(bar_ids), period_id
