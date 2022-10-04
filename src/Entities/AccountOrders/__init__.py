from typing import Dict

from .. import AccountOrder
from .. import Blank
from ..Observable import Observable
from ..Observable import notify


class AccountOrders(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._data: Dict[str, AccountOrder] = {}

    @notify
    def create_new_account_order(self, sheet_name: str, account_order: AccountOrder):
        self._data[sheet_name] = account_order

    @notify
    def delete_account_order(self, sheet_name):
        del self._data[sheet_name]

    @notify
    def change_sheet_name(self, from_, to_):
        self._data[to_] = self._data[from_]
        self.delete_account_order(from_)

    def set_data(self, data: Dict[str, AccountOrder]):
        value = {}
        for sheet_name, account_order_data in data.items():
            # Pickle depends on AccountOrder's name and location within project. Only pickle pure python object.
            account_order = AccountOrder()
            ao_data = tuple(d if str(d) != 'blank' else Blank() for d in account_order_data.data)
            account_order.set_data(ao_data)  # remove data after cleaning
            value[sheet_name] = account_order
        self._data = value

    @notify
    def merge_data(self, data: Dict[str, AccountOrder], shape_id_converter: dict):
        for sheet_name, account_order in data.items():
            if sheet_name not in self._data:
                account_order.convert_data(shape_id_converter)
                self._data[sheet_name] = account_order
            else:
                self._data[sheet_name].merge_data(account_order.data, shape_id_converter)

    @notify
    def change_shape_id(self, old_shape_id, new_shape_id):
        for sheet_name, account_order in self._data.items():
            account_order.change_shape_id(old_shape_id, new_shape_id)

    def get_account_order(self, sheet_name) -> AccountOrder:
        return self._data[sheet_name]

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        else:
            if set(self._data.keys()) != set(other.__data.keys()):
                return False
            else:
                for account_order1, account_order2 in zip(self._data.values(), other._data.values()):
                    if account_order1.data != account_order2.data:
                        return False
        return True
