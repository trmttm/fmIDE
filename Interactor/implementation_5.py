from typing import Tuple

from . import graph
from . import slider
from ..Entities import Shapes


def get_special_shapes_when_moving(shape_ids, shapes: Shapes) -> Tuple[tuple, tuple, tuple]:
    handle_ids = shape_ids if slider.selections_are_all_slider_handles(shape_ids, shapes) else ()
    slider_items = slider.extract_slider_items_except_handle(shape_ids, shapes)
    graph_items = graph.extract_graph_items(shape_ids, shapes)
    return graph_items, handle_ids, slider_items
