from typing import Iterable
from typing import Tuple

from src import Utilities

from ..Shape import constants as cns


def create_shape_dict_data(shape_id, x=None, y=None, width=None, height=None, border_color=None, border_width=None,
                           fill=None, text=None, text_color=None, text_rotation=None, font=None,
                           tags: tuple = None) -> dict:
    tags = (create_canvas_tag_from_shape_id(shape_id),) + (tags or ())
    args = x, y, width, height, border_color, border_width, fill, text, text_color, text_rotation, font, tags
    shape_data = {shape_id: create_shape_data(*args)}
    return shape_data


def create_canvas_tag_from_shape_id(shape_id) -> str:
    tag = f'{cns.tag_prefix}_{shape_id}'
    return tag


def create_shape_data(x=None, y=None, width=None, height=None, border_color=None, border_width=None,
                      fill=None, text=None, text_color=None, text_rotation=None, font=None, tags: tuple = None) -> dict:
    shape_data = {
        cns.x: x,
        cns.y: y,
        cns.width: width,
        cns.height: height,
        cns.border_color: border_color,
        cns.border_width: border_width,
        cns.fill: fill,
        cns.text: text,
        cns.text_color: text_color,
        cns.text_rotation: text_rotation,
        cns.font: font,
        cns.tags: tags,
    }
    return shape_data


def get_coordinates_from_shape_id(shapes_data: dict, shape_id) -> Tuple[int, int, int, int]:
    return get_coordinates_from_shape_data(shapes_data[shape_id])


def get_coordinates_from_shape_data(shape_data: dict) -> Tuple[int, int, int, int]:
    x1, y1 = shape_data[cns.x], shape_data[cns.y]
    x2, y2 = x1 + shape_data[cns.width], y1 + shape_data[cns.height]
    return x1, y1, x2, y2


def coords_overlaps_with_existing_shapes(coords, shapes_data: dict, search_from: tuple = None) -> bool:
    list_of_x, list_of_y = get_argument_combination(coords)
    search_from = shapes_data.keys() if search_from is None else search_from
    for shape_id in search_from:
        shape_coordinates = get_coordinates_from_shape_id(shapes_data, shape_id)
        if True in map(lambda *args: coordinate_in_range(*args, *shape_coordinates), list_of_x, list_of_y):
            return True
    return False


def coordinate_in_range(x, y, x1, y1, x2, y2) -> bool:
    x_is_between_the_range = (x1 <= x <= x2) or (x2 <= x <= x1)
    y_is_between_the_range = (y1 <= y <= y2) or (y2 <= y <= y1)
    return x_is_between_the_range and y_is_between_the_range


def get_argument_combination(coords):
    x1, y1, x2, y2 = coords
    list_of_x = (x1, x2, x1, x2)
    list_of_y = (y1, y1, y2, y2)
    return list_of_x, list_of_y


def get_shape_id_at_the_coordinate(x, y, shapes_data, search_from: tuple = None):
    shape_id_under_mouse = None
    search_from = shapes_data.keys() if search_from is None else search_from
    for shape_id in reversed(tuple(search_from)):
        shape_coordinates = get_coordinates_from_shape_id(shapes_data, shape_id)
        if coordinate_in_range(x, y, *shape_coordinates):
            shape_id_under_mouse = shape_id
            break
    return shape_id_under_mouse


def get_shape_ids_in_a_range(coordinates, shapes_data, search_from: tuple = None) -> list:
    shape_ids = []
    range_coordinates = coordinates
    if search_from is None:
        search_from = reversed(list(shapes_data.keys()))

    for shape_id in search_from:
        shape_coorinates = get_coordinates_from_shape_id(shapes_data, shape_id)
        if coordinates_overlap(range_coordinates, shape_coorinates):
            shape_ids.append(shape_id)
    return shape_ids


def coordinates_overlap(coords1, coords2) -> bool:
    x11, x12 = min(coords1[0], coords1[2]), max(coords1[0], coords1[2]),
    y11, y12 = min(coords1[1], coords1[3]), max(coords1[1], coords1[3]),
    x21, x22 = min(coords2[0], coords2[2]), max(coords2[0], coords2[2]),
    y21, y22 = min(coords2[1], coords2[3]), max(coords2[1], coords2[3]),

    # If one rectangle is on left side of other
    if x11 >= x22 or x21 >= x12:
        return False

    # If one rectangle is above other
    if y12 <= y21 or y22 <= y11:
        return False

    return True


def adjust_shape_position_to_avoid_overlapping(increment_x_y: Tuple[int, int], shape_data: dict):
    delta_x, delta_y = increment_x_y[0], increment_x_y[1]
    shape_data[cns.x] += delta_x
    shape_data[cns.y] += delta_y


def set_value(shapes_data: dict, shape_id, key, value):
    if shape_id in shapes_data:
        shapes_data[shape_id][key] = value


def lines_overlap_in_a_direction(min1, max1, min2, max2) -> bool:
    no_overlap = max1 < min2 or max2 < min1
    return not no_overlap


def get_shape_id_to_align_with(getters1, getters2, min_or_max, selection_data, w_or_h):
    d = dict(zip([getters1(s) + w_or_h * getters2(s) for s in selection_data], selection_data))
    try:
        aligning_with = d[min_or_max(d)]
    except ValueError:
        # empty passed to min / max
        aligning_with = None
    return aligning_with


def get_bottom_shape_id(shape_ids: Iterable, shapes):
    min_or_max = max
    w_or_h = 1
    getters1 = shapes.get_y
    getters2 = shapes.get_height
    aligning_with = get_shape_id_to_align_with(getters1, getters2, min_or_max, shape_ids, w_or_h)
    return aligning_with


def get_top_shape_id(shape_ids: Iterable, shapes):
    min_or_max = min
    w_or_h = 0
    getters1 = shapes.get_y
    getters2 = shapes.get_height
    aligning_with = get_shape_id_to_align_with(getters1, getters2, min_or_max, shape_ids, w_or_h)
    return aligning_with


def get_right_most_shape_id(shape_ids: Iterable, shapes):
    min_or_max = max
    w_or_h = 1
    getters1 = shapes.get_x
    getters2 = shapes.get_width
    aligning_with = get_shape_id_to_align_with(getters1, getters2, min_or_max, shape_ids, w_or_h)
    return aligning_with


def get_left_most_shape_id(shape_ids: Iterable, shapes):
    min_or_max = min
    w_or_h = 0
    getters1 = shapes.get_x
    getters2 = shapes.get_width
    aligning_with = get_shape_id_to_align_with(getters1, getters2, min_or_max, shape_ids, w_or_h)
    return aligning_with


def align_shapes_to_bottom(shapes, shapes_to_align):
    aligning_with = shapes.get_bottom_shape_id(shapes_to_align)
    shapes.align_shapes(shapes_to_align, aligning_with, 'bottom')


def align_shapes_to_top(shapes, shapes_to_align):
    aligning_with = shapes.get_top_shape_id(shapes_to_align)
    shapes.align_shapes(shapes_to_align, aligning_with, 'top')


def align_shapes_to_right(shapes, shapes_to_align):
    aligning_with = shapes.get_right_most_shape_id(shapes_to_align)
    shapes.align_shapes(shapes_to_align, aligning_with, 'right')


def align_shapes_to_left(shapes, shapes_to_align):
    aligning_with = shapes.get_left_most_shape_id(shapes_to_align)
    shapes.align_shapes(shapes_to_align, aligning_with, 'left')


def align_middle(getter1, getter2, high_point, low_point, setter, shape_ids):
    if high_point is None or low_point is None:
        return
    middle_point = (getter1(low_point) + getter1(high_point) + getter2(high_point)) / 2
    for shape_id in shape_ids:
        if shape_id not in (low_point, high_point):
            setter(shape_id, middle_point - getter2(shape_id) / 2)


def align_middle_horizontal(shape_ids, shapes):
    low_point = shapes.get_left_most_shape_id(shape_ids)
    high_point = shapes.get_right_most_shape_id(shape_ids)
    getter1 = shapes.get_x
    getter2 = shapes.get_width
    setter = shapes.set_x
    align_middle(getter1, getter2, high_point, low_point, setter, shape_ids)


def align_middle_vertical(shape_ids, shapes):
    low_point = shapes.get_top_shape_id(shape_ids)
    high_point = shapes.get_bottom_shape_id(shape_ids)
    getter1 = shapes.get_y
    getter2 = shapes.get_height
    setter = shapes.set_y
    align_middle(getter1, getter2, high_point, low_point, setter, shape_ids)


def evenly_distribute_horizontally(shape_ids, shapes):
    get_length = shapes.get_width
    get_coordinate = shapes.get_x
    get_start_shape = shapes.get_left_most_shape_id
    get_end_shape = shapes.get_right_most_shape_id
    setter = shapes.set_x

    evenly_distribute(get_coordinate, get_end_shape, get_length, get_start_shape, shape_ids, setter)


def evenly_distribute_vertically(shape_ids, shapes):
    get_length = shapes.get_height
    get_coordinate = shapes.get_y
    get_start_shape = shapes.get_top_shape_id
    get_end_shape = shapes.get_bottom_shape_id
    setter = shapes.set_y

    evenly_distribute(get_coordinate, get_end_shape, get_length, get_start_shape, shape_ids, setter)


def evenly_distribute(get_coordinate, get_end_shape, get_length, get_start_shape, shape_ids, setter):
    start_shape = get_start_shape(shape_ids)
    end_shape = get_end_shape(shape_ids)

    if start_shape is None or end_shape is None:
        return
    start_point = get_coordinate(start_shape)
    end_point = get_coordinate(end_shape) + get_length(end_shape)
    shape_lengths = tuple(get_length(shape_id) for shape_id in shape_ids)
    total_lengths = end_point - start_point

    space = get_space_between_shapes(shape_lengths, total_lengths)
    distribute_shapes(space, get_coordinate, get_length, shape_ids, setter)


def get_space_between_shapes(shape_lengths, total_lengths):
    space = 0
    increment = total_lengths / 1000
    if current_total_widths(shape_lengths, 0) < total_lengths:
        while current_total_widths(shape_lengths, space) < total_lengths:
            space += increment
    else:
        while current_total_widths(shape_lengths, space) > total_lengths:
            space -= increment
    return space


def current_total_widths(sizes, delta: float) -> float:
    number_of_gaps = (len(sizes) - 1)
    return sum(sizes) + delta * number_of_gaps


def distribute_shapes(delta, get_coordinate, get_length, shape_ids, setter):
    shape_ids_sorted = get_shape_ids_sorted_from_start_to_end(get_coordinate, shape_ids)
    for n, shape_id in enumerate(shape_ids_sorted):
        if n not in [0, len(shape_ids_sorted) - 1]:
            previous_shape_id = shape_ids_sorted[n - 1]
            coordinate = get_next_coordinate(delta, get_coordinate, get_length, previous_shape_id)
            setter(shape_id, coordinate)


def get_next_coordinate(space, get_coordinate, get_length, previous_shape_id):
    coordinate = get_coordinate(previous_shape_id) + get_length(previous_shape_id) + space
    return coordinate


def get_shape_ids_sorted_from_start_to_end(get_coordinate, shape_ids):
    coordinates = [get_coordinate(shape_id) for shape_id in shape_ids]
    _, shapes_to_be_aligned_sorted = Utilities.sort_lists(coordinates, shape_ids)
    return shapes_to_be_aligned_sorted


def merge_shapes_data(shapes, shapes_data_to_merge) -> dict:
    shape_id_converter = {}
    new_shape_ids = []
    for old_shape_id, shape_data in shapes_data_to_merge.items():
        if old_shape_id in shapes.data:
            shapes.add_new_shape_from_shape_data(shape_data)
        else:
            shapes.data[old_shape_id] = shape_data
        new_shape_id = shapes.shapes_ids[-1]
        replace_canvas_tag(new_shape_id, shapes)
        shape_id_converter[old_shape_id] = new_shape_id
        new_shape_ids.append(new_shape_id)

    _replace_shape_id_that_relays_represent(shape_id_converter, shapes, new_shape_ids)

    return shape_id_converter


def replace_canvas_tag(new_shape_id, shapes):
    old_tags = shapes.get_tags(new_shape_id)
    new_tags = tuple([shapes.get_canvas_tag_from_shape_id(new_shape_id)] + list(old_tags[1:]))
    shapes.set_tags(new_shape_id, new_tags)


def _replace_shape_id_that_relays_represent(shape_id_converter, shapes, new_shape_ids: Iterable):
    for new_shape_id in new_shape_ids:
        old_original_account = shapes.get_shape_it_represents(new_shape_id)
        if old_original_account is not None:
            shapes.set_shape_it_represents(new_shape_id, shape_id_converter[old_original_account])


def replace_shape_id_that_relays_represent(old_shape_id, new_shape_id, shapes):
    for relay in shapes.get_relays(old_shape_id):
        shapes.set_shape_it_represents(relay, new_shape_id)
