from typing import Any
from typing import Dict

from ..Observable import Observable
from ..Observable import notify


class VerticalAccounts(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._data: Dict[Any, tuple] = {}

    @notify
    def add_vertical_account(self, account_id):
        self._data[account_id] = tuple()

    @notify
    def add_vertical_reference(self, vertical_account_id, vertical_reference_id):
        self.add_vertical_references(vertical_account_id, (vertical_reference_id,))

    @notify
    def add_vertical_references(self, vertical_account_id, vertical_reference_ids: tuple):
        if not self.is_a_vertical_account(vertical_account_id):
            self.add_vertical_account(vertical_account_id)
        self._data[vertical_account_id] += vertical_reference_ids

    def remove_vertical_accounts(self, account_ids):
        for account_id in account_ids:
            self.remove_vertical_account(account_id)

    @notify
    def remove_vertical_account(self, account_id):
        try:
            del self._data[account_id]
        except KeyError:
            pass

    @notify
    def replace_vertical_account_reference(self, vertical_account_id, new_vertical_reference: tuple):
        self._data[vertical_account_id] = new_vertical_reference

    @notify
    def remove_vertical_reference(self, vertical_account_id, vertical_reference_id):
        if vertical_account_id in self._data:
            if vertical_reference_id in self._data[vertical_account_id]:
                reference_accounts_mutable = list(self._data[vertical_account_id])
                reference_accounts_mutable.remove(vertical_reference_id)
                self._data[vertical_account_id] = tuple(reference_accounts_mutable)

    def remove_vertical_reference_from_all_vertical_accounts(self, vertical_reference_id):
        for vertical_account_id in self._data.keys():
            self.remove_vertical_reference(vertical_account_id, vertical_reference_id)

    def get_vertical_reference(self, vertical_account_id) -> tuple:
        return self._data[vertical_account_id] if vertical_account_id in self._data else ()

    def is_a_vertical_account(self, account_id) -> bool:
        return account_id in self._data

    def change_shape_id(self, old_shape_id, new_shape_id):
        if old_shape_id in self._data:
            old_vertical_references = self.get_vertical_reference(old_shape_id)
            self.add_vertical_references(new_shape_id, old_vertical_references)
            self.remove_vertical_account(old_shape_id)

        for account_id, old_vertical_references in self._data.items():
            new_reference = tuple(new_shape_id if (item == old_shape_id) else item for item in old_vertical_references)
            self.replace_vertical_account_reference(account_id, new_reference)

    @notify
    def copy(self, from_id, to_id):
        if self.is_a_vertical_account(from_id):
            self.add_vertical_account(to_id)
            self.add_vertical_references(to_id, self.get_vertical_reference(from_id))

    @notify
    def merge_data(self, data: Dict[Any, tuple], shape_id_converter: dict):
        for vertical_account, vertical_references in data.items():
            if vertical_account in shape_id_converter:
                key = shape_id_converter[vertical_account]
            else:
                key = vertical_account

            new_values = []
            for vertical_reference in vertical_references:
                if vertical_reference in shape_id_converter:
                    value = shape_id_converter[vertical_reference]
                else:
                    value = vertical_reference
                new_values.append(value)

            self._data[key] = tuple(new_values)
