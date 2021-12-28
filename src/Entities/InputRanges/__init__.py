from typing import Any
from typing import Dict
from typing import Tuple

from ..Observable import Observable
from ..Observable import notify


class InputRanges(Observable):
    __account_id = 'account_ids'

    def __init__(self):
        Observable.__init__(self)
        self._data: Dict[Any, Tuple[float, float]] = {}

    @property
    def data(self) -> dict:
        return self._data

    @notify
    def set_range(self, account_id, y_range: tuple):
        self._data[account_id] = y_range

    def remove_ranges(self, account_ids):
        for account_id in account_ids:
            self.remove_range(account_id)

    @notify
    def remove_range(self, account_id):
        try:
            del self._data[account_id]
        except KeyError:
            pass

    def get_ranges(self, account_id) -> tuple:
        return self._data[account_id] if account_id in self._data else None

    @notify
    def copy(self, from_id, to_id):
        if from_id in self._data:
            self._data[to_id] = self._data[from_id]

    @notify
    def merge_data(self, data, shape_id_converter: dict):
        for account_id, y_range in data.items():
            if account_id in shape_id_converter:
                self.set_range(shape_id_converter[account_id], y_range)

    def change_shape_id(self, old_shape_id, new_shape_id):
        self.set_range(new_shape_id, self.get_ranges(old_shape_id))
        self.remove_range(old_shape_id)

    def __repr__(self):
        return str(self._data)

    def __contains__(self, item) -> bool:
        return item in self._data
