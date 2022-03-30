from typing import Dict
from typing import Tuple

from .. import Selection
from ..Observable import Observable
from ..Observable import notify


class Selections(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._data: Dict[str, Selection] = {}

    @notify
    def create_new_selection(self, sheet_name: str, selection: Selection):
        self._data[sheet_name] = selection

    @notify
    def delete_selection(self, sheet_name):
        del self._data[sheet_name]

    @notify
    def change_sheet_name(self, from_, to_):
        self._data[to_] = self._data[from_]
        self.delete_selection(from_)

    def get_selection(self, sheet_name) -> Selection:
        return self._data[sheet_name]

    def set_data(self, data: Dict[str, set]):
        # Pickle depends on Selection's name and location within project. Only pickle pure python object.
        value = {}
        for sheet_name, selection_data in data.items():
            selection = Selection()
            selection.set_data(selection_data.data)  # remove data after clearing
            value[sheet_name] = selection
        self._data = value

    @property
    def all_selections(self) -> Tuple[Selection]:
        return tuple(self._data.values())

    @notify
    def merge_data(self, data: Dict[str, Selection], shape_id_converter: dict):
        for sheet_name, selection in data.items():
            if sheet_name not in self._data:
                selection.convert_data(shape_id_converter)
                self._data[sheet_name] = selection
            else:
                selection.convert_data(shape_id_converter)
                converted_selection_data = selection.data
                self._data[sheet_name].set_data(converted_selection_data)

    @notify
    def change_shape_id(self, old_shape_id, new_shape_id):
        for _, selection in self._data.items():
            selection.change_shape_id(old_shape_id, new_shape_id)
