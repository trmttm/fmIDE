from typing import Any
from typing import Dict

from ..Observable import Observable
from ..Observable import notify


class InputValues(Observable):
    __account_id = 'account_ids'

    def __init__(self):
        Observable.__init__(self)
        self._data: Dict[Any, Dict[int, float]] = {}

    @property
    def data(self) -> dict:
        return self._data

    def get_values(self, account_id) -> tuple:
        return tuple(self._data[account_id].values()) if account_id in self._data else ()

    def get_value(self, account_id, period: int) -> float:
        return self._data[account_id][period]

    @notify
    def add_new_account(self, account_id, values: tuple = ()):
        nop = len(values)
        self._data[account_id] = dict(zip(range(nop), values))

    def remove_accounts(self, account_ids):
        for account_id in account_ids:
            self.remove_account(account_id)

    @notify
    def remove_account(self, account_id):
        try:
            del self._data[account_id]
        except KeyError:
            pass

    @notify
    def set_values(self, account_id, values: tuple):
        nop = len(values)
        self._data[account_id] = dict(zip(range(nop), values))

    @notify
    def set_value(self, account_id, period: int, value: float):
        if account_id in self._data:
            self._data[account_id][period] = value
        else:
            self._data[account_id] = {period: value}

    @notify
    def set_default_values(self, input_account, number_of_periods: int):
        self.add_new_account(input_account, tuple(0 for _ in range(number_of_periods)))

    @notify
    def copy(self, from_id, to_id):
        if from_id in self._data:
            self._data[to_id] = self._data[from_id]

    def values_are_not_set(self, input_account) -> bool:
        return (input_account not in self._data) or (self._data[input_account] == {})

    def change_number_of_periods(self, number_of_periods: int):
        for account_id, values_dict in self._data.items():
            try:
                max_period = max(values_dict.keys())
            except ValueError:
                max_period = None
            for period in range(number_of_periods):
                if period not in values_dict:
                    values_dict[period] = values_dict[max_period] if max_period is not None else 0

    def change_shape_id(self, old_shape_id, new_shape_id):
        self.set_values(new_shape_id, self.get_values(old_shape_id))
        self.remove_account(old_shape_id)

    @notify
    def merge_data(self, data: dict, shape_id_converter: dict):
        for account_id, values_dict in data.items():
            for period, value in values_dict.items():
                if account_id in shape_id_converter:
                    self.set_value(shape_id_converter[account_id], period, value)

    def __repr__(self):
        return str(self._data)

    def __contains__(self, item) -> bool:
        return item in self._data
