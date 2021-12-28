from typing import Any
from typing import Dict

from ..Observable import Observable
from ..Observable import notify


class NumberFormat(Observable):
    _whole_number = 'whole number'
    _1_digit = '1-digit'
    _2_digit = '2-digit'
    _percent = '%'
    _all_number_format_keys = (_whole_number, _1_digit, _2_digit, _percent,)

    def __init__(self):
        Observable.__init__(self)
        self._data: Dict[Any, tuple] = {}

    @notify
    def set_number_format(self, shape_id, format_id: Any):
        self.delete_format(shape_id)
        if format_id in self._data:
            self._data[format_id] += (shape_id,)
        else:
            self._data[format_id] = (shape_id,)

    @notify
    def copy(self, from_id, to_id):
        for format_id, shape_ids in self._data.items():
            if from_id in shape_ids:
                self.set_number_format(to_id, format_id)

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

    def mark_as_whole_number(self, shape_id):
        self.set_number_format(shape_id, self._whole_number)

    def mark_as_1_digit(self, shape_id):
        self.set_number_format(shape_id, self._1_digit)

    def mark_as_2_digit(self, shape_id):
        self.set_number_format(shape_id, self._2_digit)

    def mark_as_percent(self, shape_id):
        self.set_number_format(shape_id, self._percent)

    @property
    def all_number_format_keys(self) -> tuple:
        return self._all_number_format_keys

    @property
    def whole_number(self) -> tuple:
        return self.get_accounts(self._whole_number)

    @property
    def one_digit(self) -> tuple:
        return self.get_accounts(self._1_digit)

    @property
    def two_digit(self) -> tuple:
        return self.get_accounts(self._2_digit)

    @property
    def percent(self) -> tuple:
        return self.get_accounts(self._percent)

    def change_shape_id(self, old_shape_id, new_shape_id):
        self.set_number_format(new_shape_id, self.get_format(old_shape_id))
        self.delete_format(old_shape_id)

    def merge_data(self, data: Dict[Any, tuple], shape_id_converter: dict):
        for key, shape_ids in data.items():
            converted_shape_ids = tuple(shape_id_converter[shape_id] for shape_id in shape_ids)
            if key in self._data:
                self._data[key] += converted_shape_ids
            else:
                self._data[key] = converted_shape_ids
