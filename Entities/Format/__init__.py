from typing import Any
from typing import Dict

from ..Observable import Observable
from ..Observable import notify


class Format(Observable):
    _heading = 'heading'
    _total = 'total'
    _all_format_keys = _heading, _total

    def __init__(self):
        Observable.__init__(self)
        self._data: Dict[Any, tuple] = {}

    @notify
    def set_format(self, shape_id, format_id: Any):
        self.delete_format(shape_id)
        if format_id in self._data:
            self._data[format_id] += (shape_id,)
        else:
            self._data[format_id] = (shape_id,)

    @notify
    def copy(self, from_id, to_id):
        for format_id, shape_ids in self._data.items():
            if from_id in shape_ids:
                self.set_format(to_id, format_id)

    def delete_format(self, shape_id):
        for format_key, shape_ids in self._data.items():
            if shape_id in shape_ids:
                self._data[format_key] = tuple(i for i in shape_ids if i != shape_id)

    def get_accounts(self, format_key) -> tuple:
        if format_key not in self._data:
            return ()
        else:
            return self._data[format_key]

    def get_format(self, account_id) -> str:
        for format_key, accounts in self._data.items():
            if account_id in accounts:
                return format_key

    def mark_as_heading(self, shape_id):
        self.set_format(shape_id, self._heading)

    def mark_as_total(self, shape_id):
        self.set_format(shape_id, self._total)

    @property
    def all_format_keys(self) -> tuple:
        return self._all_format_keys

    @property
    def headings(self) -> tuple:
        return self.get_accounts(self._heading)

    @property
    def total(self) -> tuple:
        return self.get_accounts(self._total)

    def change_shape_id(self, old_shape_id, new_shape_id):
        self.set_format(new_shape_id, self.get_format(old_shape_id))
        self.delete_format(old_shape_id)

    def merge_data(self, data: Dict[Any, tuple], shape_id_converter: dict):
        for key, shape_ids in data.items():
            converted_shape_ids = tuple(shape_id_converter[shape_id] for shape_id in shape_ids)
            if key in self._data:
                self._data[key] += converted_shape_ids
            else:
                self._data[key] = converted_shape_ids
