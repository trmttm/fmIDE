from typing import Any
from typing import Dict

from ..Observable import Observable
from ..Observable import notify


class InputDecimals(Observable):
    __account_id = 'account_ids'
    __default = 1

    def __init__(self):
        Observable.__init__(self)
        self._data: Dict[Any, int] = {}

    @property
    def data(self) -> dict:
        return self._data

    @notify
    def set_decimals(self, account_id, decimals: int):
        self._data[account_id] = decimals

    def remove_decimals(self, account_ids):
        for account_id in account_ids:
            self.remove_decimal(account_id)

    @notify
    def remove_decimal(self, account_id):
        try:
            del self._data[account_id]
        except KeyError:
            pass

    def get_decimals(self, account_id) -> int:
        return self._data[account_id] if account_id in self._data else self.__default

    @notify
    def copy(self, from_id, to_id):
        if from_id in self._data:
            self._data[to_id] = self._data[from_id]

    @notify
    def merge_data(self, data, shape_id_converter: dict):
        for account_id, decimals in data.items():
            if account_id in shape_id_converter:
                self.set_decimals(shape_id_converter[account_id], decimals)

    def change_shape_id(self, old_shape_id, new_shape_id):
        self.set_decimals(new_shape_id, self.get_decimals(old_shape_id))
        self.remove_decimal(old_shape_id)

    def __repr__(self):
        return str(self._data)

    def __contains__(self, item) -> bool:
        return item in self._data
