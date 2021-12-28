from typing import Iterable
from typing import Tuple
from typing import Union

from . import constants
from . import implementation as impl
from ..Observable import Observable
from ..Observable import notify
from ... import Utilities


class Shapes(Observable):

    def __init__(self):
        Observable.__init__(self)
        self._data = {}
        self._id = 0

    @property
    def data(self) -> dict:
        return self._data

    @notify
    def add_new_shape(self, text: str = 'Text', tags: tuple = None):
        while self._id in self._data:
            self._id += 1
        new_shape_data = impl.create_shape_dict_data(self._id, text=text, tags=tags)
        self._data.update(new_shape_data)
        self._id += 1

    @notify
    def add_new_shape_from_shape_data(self, new_shape_data: dict):
        while self._id in self._data:
            self._id += 1
        self._data.update({self._id: new_shape_data})
        self._id += 1

    @property
    def next_shape_id(self) -> int:
        self._id += 1
        return self._id

    def add_new_shapes(self, request_models):
        for request_model in request_models:
            self.add_new_shape(**request_model)

    @notify
    def erase_shape(self, shape_id):
        try:
            del self._data[shape_id]
        except KeyError:
            pass

    def erase_shapes(self, request_models):
        shape_ids = tuple(r['shape_id'] for r in request_models)
        keys = tuple(key for key in self._data.keys() if key not in shape_ids)
        values = tuple(value for (key, value) in self._data.items() if key not in shape_ids)
        self._data = dict(zip(keys, values))

    @notify
    def erase_all_shapes(self):
        self._data = {}
        self._id = 0

    def set_x_y_without_overlapping(self, x, y):
        self.set_x(x)
        self.set_y(y)

    @notify
    def set_x(self, shape_id, x):
        impl.set_value(self._data, shape_id, 'x', x)

    @notify
    def set_y(self, shape_id, y):
        impl.set_value(self._data, shape_id, 'y', y)

    @notify
    def set_width(self, shape_id, width):
        impl.set_value(self._data, shape_id, 'width', width)

    @notify
    def set_height(self, shape_id, height):
        impl.set_value(self._data, shape_id, 'height', height)

    @notify
    def set_border_color(self, shape_id, border_color):
        impl.set_value(self._data, shape_id, 'border_color', border_color)

    @notify
    def set_border_width(self, shape_id, border_width):
        impl.set_value(self._data, shape_id, 'border_width', border_width)

    @notify
    def set_fill(self, shape_id, fill):
        impl.set_value(self._data, shape_id, 'fill', fill)

    @notify
    def set_text(self, shape_id, text):
        impl.set_value(self._data, shape_id, 'text', text)

    @notify
    def set_text_rotation(self, shape_id, text_rotation):
        impl.set_value(self._data, shape_id, 'text_rotation', text_rotation)

    @notify
    def set_font(self, shape_id, font):
        impl.set_value(self._data, shape_id, 'font', font)

    @notify
    def set_font_color(self, shape_id, font_color):
        impl.set_value(self._data, shape_id, 'font_color', font_color)

    @notify
    def set_tags(self, shape_id, tags):
        impl.set_value(self._data, shape_id, 'tags', tags)

    @notify
    def set_shape_it_represents(self, shape_id, shape_id_it_represents):
        impl.set_value(self._data, shape_id, constants.shape_it_represents, shape_id_it_represents)

    @notify
    def copy(self, from_id, to_id, dx=25, dy=25):
        self._data[to_id] = dict(self._data[from_id])
        self.set_x(to_id, self.get_x(from_id) + dx)
        self.set_y(to_id, self.get_y(from_id) + dy)
        impl.replace_canvas_tag(to_id, self)

    def get_value(self, key, shape_id):
        if shape_id not in self._data:
            return

        if key == 'text':
            return self.get_text(shape_id)
        elif key == 'x':
            return self.get_x(shape_id)
        elif key == 'y':
            return self.get_y(shape_id)
        elif key == 'width':
            return self.get_width(shape_id)
        elif key == 'height':
            return self.get_height(shape_id)

    def set_value(self, key, shape_id, value):
        if key == 'text':
            return self.set_text(shape_id, str(value))

        try:
            v = float(value)
        except ValueError:
            return

        if key == 'x':
            return self.set_x(shape_id, v)
        elif key == 'y':
            return self.set_y(shape_id, v)
        elif key == 'width':
            return self.set_width(shape_id, v)
        elif key == 'height':
            return self.set_height(shape_id, v)

    def get_x(self, shape_id):
        return self._data[shape_id]['x']

    def get_y(self, shape_id):
        return self._data[shape_id]['y']

    def get_width(self, shape_id):
        return self._data[shape_id]['width']

    def get_height(self, shape_id):
        return self._data[shape_id]['height']

    def get_border_color(self, shape_id):
        return self._data[shape_id]['border_color']

    def get_border_width(self, shape_id):
        return self._data[shape_id]['border_width']

    def get_fill(self, shape_id):
        return self._data[shape_id]['fill']

    def get_text(self, shape_id):
        return self._data[shape_id]['text']

    def get_text_rotation(self, shape_id):
        return self._data[shape_id]['text_rotation']

    def get_font(self, shape_id):
        return self._data[shape_id]['font']

    def get_font_color(self, shape_id):
        return self._data[shape_id]['font_color']

    def get_tags(self, shape_id):
        return self._data[shape_id]['tags']

    def get_shape_it_represents(self, shape_id):
        try:
            return self._data[shape_id][constants.shape_it_represents]
        except KeyError:
            return

    def get_shape_it_represents_or_self(self, shape_id):
        shape_relay_represents = self.get_shape_it_represents(shape_id)
        return shape_relay_represents if shape_relay_represents is not None else shape_id

    def get_relays(self, shape_id) -> set:
        relays = set()
        for relay_shape_id in self.shapes_ids:
            if self.get_shape_it_represents(relay_shape_id) == shape_id:
                relays.add(relay_shape_id)
        return relays

    @property
    def shapes_ids(self) -> tuple:
        return tuple(self._data.keys())

    def get_coords_from_shape_id(self, shape_id) -> Tuple[int, int, int, int]:
        return impl.get_coordinates_from_shape_id(self._data, shape_id)

    def coords_overlap_with_existing_shapes(self, coords: Tuple[int, int, int, int], search_from: tuple = None) -> bool:
        return impl.coords_overlaps_with_existing_shapes(coords, self._data, search_from)

    def shape_overlap_with_existing_shapes(self, shape_data: dict, search_from: tuple = None) -> bool:
        return self.coords_overlap_with_existing_shapes(impl.get_coordinates_from_shape_data(shape_data), search_from)

    def adjust_shape_position_to_avoid_overlapping(self, shape_data, increment_x_y, search_from: tuple = None):
        while self.shape_overlap_with_existing_shapes(shape_data, search_from):
            impl.adjust_shape_position_to_avoid_overlapping(increment_x_y, shape_data)

    def get_shape_id_at_the_coordinate(self, x, y, search_from: tuple = None):
        return impl.get_shape_id_at_the_coordinate(x, y, self._data, search_from)

    def get_shape_ids_in_a_range(self, coordinates, search_from: tuple = None) -> list:
        return impl.get_shape_ids_in_a_range(coordinates, self._data, search_from)

    @staticmethod
    def get_canvas_tag_from_shape_id(shape_id):
        return impl.create_canvas_tag_from_shape_id(shape_id)

    def get_shapes(self, tag_type: str = None) -> tuple:
        return tuple(i for i in self._data if self.get_tag_type(i) == tag_type)

    def create_tag_type_to_shape_ids_dictionary(self, tag_types: tuple, intercept=None) -> dict:
        tag_type_to_shapes_dictionary = dict(zip(tag_types, tuple(() for _ in tag_types)))

        shape_ids_to_search = self._data if intercept is None else set(self._data.keys()).intersection(set(intercept))
        for shape_id in shape_ids_to_search:
            tag_type = self.get_tag_type(shape_id)
            if tag_type in tag_types:
                tag_type_to_shapes_dictionary[tag_type] += (shape_id,)
        return tag_type_to_shapes_dictionary

    def filter_shapes_by_tag_and_intercept(self, tag_types: Iterable, intercept: Iterable) -> tuple:
        shape_ids_filtered = set(i for i in self._data if self.get_tag_type(i) in tag_types)
        return tuple(set(intercept).intersection(shape_ids_filtered))

    def get_tag_type(self, shape_id) -> Union[None, str]:
        try:
            return self._data[shape_id][constants.tags][1]
        except KeyError:
            # blank
            return None

    def set_coordinate(self, shape_id, coordinate: tuple):
        self.set_x(shape_id, coordinate[0])
        self.set_y(shape_id, coordinate[1])
        self.set_width(shape_id, coordinate[2])
        self.set_height(shape_id, coordinate[3])

    def align_shapes(self, shape_ids: Iterable, with_, direction):
        for shape_id in shape_ids:
            self.align_shape(shape_id, with_, direction)

    def align_shape(self, shape_id, with_, direction: str):
        self._align_left(shape_id, with_, direction)
        self._align_right(shape_id, with_, direction)
        self._align_top(shape_id, with_, direction)
        self._align_bottom(shape_id, with_, direction)

    def _align_left(self, aligning, with_, direction=constants.left):
        if direction == constants.left:
            self.set_x(aligning, self.get_x(with_))

    def _align_right(self, aligning, with_, direction=constants.right):
        if direction == constants.right:
            self.set_x(aligning, self.get_x(with_) + self.get_width(with_) - self.get_width(aligning))

    def _align_top(self, aligning, with_, direction=constants.top):
        if direction == constants.top:
            self.set_y(aligning, self.get_y(with_))

    def _align_bottom(self, aligning, with_, direction=constants.bottom):
        if direction == constants.bottom:
            self.set_y(aligning, self.get_y(with_) + self.get_height(with_) - self.get_height(aligning))

    def get_bottom_shape_id(self, shape_ids: Iterable):
        return impl.get_bottom_shape_id(shape_ids, self)

    def get_left_most_shape_id(self, shape_ids: Iterable):
        return impl.get_left_most_shape_id(shape_ids, self)

    def get_right_most_shape_id(self, shape_ids: Iterable):
        return impl.get_right_most_shape_id(shape_ids, self)

    def get_top_shape_id(self, shape_ids: Iterable):
        return impl.get_top_shape_id(shape_ids, self)

    def align_shapes_to_bottom(self, shape_ids: Iterable):
        impl.align_shapes_to_bottom(self, shape_ids)

    def align_shapes_to_top(self, shape_ids: Iterable):
        impl.align_shapes_to_top(self, shape_ids)

    def align_shapes_to_right(self, shape_ids: Iterable):
        impl.align_shapes_to_right(self, shape_ids)

    def align_shapes_to_left(self, shape_ids: Iterable):
        impl.align_shapes_to_left(self, shape_ids)

    def align_middle_horizontal(self, shape_ids):
        impl.align_middle_horizontal(shape_ids, self)

    def align_middle_vertical(self, shape_ids):
        impl.align_middle_vertical(shape_ids, self)

    def is_account(self, shape_id) -> bool:
        return self.get_tag_type(shape_id) == 'account'

    def evenly_distribute_horizontally(self, shape_ids: Iterable):
        impl.evenly_distribute_horizontally(shape_ids, self)

    def evenly_distribute_vertically(self, shape_ids: Iterable):
        impl.evenly_distribute_vertically(shape_ids, self)

    def get_nearest_points_of_two_shape_ids(self, shape_id1, shape_id2) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        get_coordinates = self.get_coords_from_shape_id
        return Utilities.get_nearest_points(get_coordinates(shape_id1), get_coordinates(shape_id2))

    def merge_data(self, shapes_data_to_merge: dict) -> dict:
        return impl.merge_shapes_data(self, shapes_data_to_merge)

    @notify
    def change_shape_id(self, old_shape_id, new_shape_id):
        self._data[new_shape_id] = self._data[old_shape_id]
        impl.replace_canvas_tag(new_shape_id, self)
        impl.replace_shape_id_that_relays_represent(old_shape_id, new_shape_id, self)
        self.erase_shape(old_shape_id)

    def __contains__(self, item) -> bool:
        return item in self._data
