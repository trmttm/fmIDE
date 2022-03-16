from ..Observable import Observable
from ..Observable import notify


class BreakdownAccounts(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._data: set = set()

    @property
    def breakdown_accounts(self) -> tuple:
        return tuple(self._data)

    @notify
    def add_breakdown_accounts(self, account_id):
        self._data.add(account_id)

    def remove_breakdown_accounts(self, account_ids):
        for account_id in account_ids:
            self.remove_breakdown_account(account_id)

    @notify
    def remove_breakdown_account(self, account_id):
        if account_id in self._data:
            self._data.remove(account_id)

    @notify
    def change_shape_id(self, old_shape_id, new_shape_id):
        if old_shape_id in self._data:
            self.remove_breakdown_account(old_shape_id)
            self.add_breakdown_accounts(new_shape_id)

    @notify
    def copy(self, from_id, to_id):
        if from_id in self._data:
            self.add_breakdown_accounts(to_id)

    @notify
    def merge_data(self, data: set, shape_id_converter: dict):
        for shape_id in data:
            shape_id_to_add = shape_id_converter.get(shape_id, shape_id)
            self.add_breakdown_accounts(shape_id_to_add)
