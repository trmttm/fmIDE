from typing import Any
from typing import Dict

from ..Observable import Observable
from ..Observable import notify


class ShapeFormat(Observable):
    _fill = 'fill'

    def __init__(self):
        Observable.__init__(self)

        self._data: Dict[str, Dict[Any, tuple]] = {
            self._fill: {},
        }

    @property
    def _fill_dictionary(self) -> dict:
        return self._data[self._fill]

    @notify
    def set_fill(self, shape_id, color):
        self.remove_fill(shape_id)
        if color in self._fill_dictionary:
            if shape_id not in self._fill_dictionary[color]:
                self._fill_dictionary[color] += (shape_id,)
        else:
            self._fill_dictionary[color] = (shape_id,)

    def remove_fills(self, shape_ids):
        for shape_ids in shape_ids:
            self.remove_fill(shape_ids)

    @notify
    def remove_fill(self, shape_id):
        for color in tuple(self._fill_dictionary.keys()):
            shape_ids = self._fill_dictionary[color]
            self._fill_dictionary[color] = tuple(i for i in shape_ids if i != shape_id)

    @notify
    def clean_data(self, all_shape_ids: tuple):
        for category in tuple(self._data.keys()):
            data_dict = self._data[category]
            for key in tuple(data_dict.keys()):
                values = data_dict[key]
                if values == ():
                    del data_dict[key]
                else:
                    filtered_values = tuple(i for i in values if i in all_shape_ids)
                    data_dict[key] = filtered_values

    def get_specified_fill(self, shape_id):
        for color, shape_ids in self._fill_dictionary.items():
            if shape_id in shape_ids:
                return color
        return None

    def merge_data(self, data: Dict[str, Dict[Any, tuple]], shape_id_converter: dict):
        for category, data_dict in data.items():
            if category not in self._data:
                self._data[category] = {}
            for key, value in data_dict.items():
                converted_values = tuple(shape_id_converter[v] if v in shape_id_converter else v for v in value)
                if key in self._data[category]:
                    self._data[category][key] += converted_values
                else:
                    self._data[category][key] = converted_values

    @notify
    def change_shape_id(self, old_shape_id, new_shape_id):
        for category in tuple(self._data.keys()):
            data_dict = self._data[category]
            for key in tuple(data_dict.keys()):
                shape_ids = data_dict[key]
                if old_shape_id in shape_ids:
                    new_shape_ids = tuple(i for i in shape_ids if i != old_shape_id) + (new_shape_id,)
                    self._data[category][key] = new_shape_ids
