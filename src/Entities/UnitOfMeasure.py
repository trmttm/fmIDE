from typing import Any
from typing import Dict

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
