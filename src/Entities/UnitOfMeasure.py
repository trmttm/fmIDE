from typing import Any
from typing import Dict
from typing import Iterable

from .Observable import Observable
from .Observable import notify


class UnitOfMeasure(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._data: Dict[Any, str] = {}

    @notify
    def add_unit_of_measure(self, shape_id, unit_of_measure: str):
        self._data[shape_id] = unit_of_measure

    def get_unit_of_measure(self, shape_id) -> str:
        return self._data.get(shape_id, '')

    @notify
    def set_data(self, data: Dict[Any, str]):
        self._data = data

    @notify
    def merge_data(self, data: Dict[Any, str], shape_id_converter: dict):
        new_data = {}
        for shape_id, unit_of_measure in data.items():
            converted_shape_id = shape_id_converter.get(shape_id, shape_id)
            new_data[converted_shape_id] = unit_of_measure
        self._data.update(new_data)

    def remove_uoms(self, shape_ids: Iterable):
        for shape_id in shape_ids:
            if shape_id in self._data:
                del self._data[shape_id]

    @notify
    def copy(self, from_id, to_id):
        self.add_unit_of_measure(to_id, self.get_unit_of_measure(from_id))
