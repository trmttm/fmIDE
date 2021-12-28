from ..Observable import Observable
from ..Observable import notify


class AccountValues(Observable):
    # Use this class for both InputValues and BBValues
    key_number_of_periods = 'nop'

    def __init__(self):
        Observable.__init__(self)

        self._data: dict = {self.key_number_of_periods: 0, }

    @notify
    def set_number_of_periods(self, number_of_periods: int):
        self._data[self.key_number_of_periods] = number_of_periods
        for account_id, values in self._data.items():
            n = len(values)
            if account_id == self.key_number_of_periods:
                continue

            if n < number_of_periods:
                extension = tuple(0 for _ in range(number_of_periods - n))
                new_values = values + extension
                self.add_values(account_id, new_values)

    @notify
    def add_values(self, account_id, values: tuple):
        self._data[account_id] = values

    def app_value(self, account_id, value, period):
        if account_id in self._data:
            existing_values = self._data[account_id]
            values = tuple(v if p != period else value for (p, v) in enumerate(existing_values))
        else:
            values = tuple(0 if p != period else value for p in self.nop)
        self.add_values(account_id, values)

    @property
    def data(self) -> dict:
        return self._data

    @property
    def number_of_periods(self):
        return self._data[self.key_number_of_periods]

    @property
    def nop(self):
        return self.number_of_periods
