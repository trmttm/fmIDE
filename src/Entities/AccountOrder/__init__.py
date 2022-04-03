from typing import Union

import Utilities

from . import implementation as impl
from ..Observable import Observable
from ..Observable import notify


class AccountOrder(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._data = ()

    @notify
    def add_element_to_last(self, shape_id):
        data = list(self._data)
        data.append(shape_id)
        self._data = tuple(data)

    @notify
    def add_elements_to_last(self, shape_ids):
        for shape_id in shape_ids:
            self.add_element_to_last(shape_id)

    @notify
    def remove_element(self, index_):
        data = list(self._data)
        del data[index_]
        self._data = tuple(data)

    @notify
    def remove_account(self, shape_id):
        self._data = tuple([id_ for id_ in self._data if id_ != shape_id])

    @notify
    def remove_accounts(self, shape_ids):
        blank_ids = set(id(element) for element in shape_ids if element.__class__ == Blank)
        element_that_remains = []
        for element in self._data:
            if element.__class__ == Blank:
                if id(element) not in blank_ids:
                    element_that_remains.append(element)
            else:
                if element not in shape_ids:
                    element_that_remains.append(element)
        self._data = tuple(element_that_remains)

    @staticmethod
    def is_blank(element) -> bool:
        return Blank().__class__.__name__ == element.__class__.__name__

    def get_element(self, account_order) -> Union[int, None]:
        try:
            return self._data[account_order]
        except IndexError:
            return None

    @notify
    def change_account_order(self, index_, destination):
        self._data = Utilities.swap_tuple_data(destination, index_, self._data)

    @notify
    def move_account_after(self, moving_account_id, after_this_account_id):
        new_account_order = []
        for account_id in self._data:
            if account_id != moving_account_id:
                new_account_order.append(account_id)
            if account_id == after_this_account_id:
                new_account_order.append(moving_account_id)

        self._data = tuple(new_account_order)

    @property
    def data(self) -> tuple:
        return self._data

    def get_order(self, element) -> int:
        if self.is_blank(element):
            for n, d in enumerate(self._data):
                if id(d) == id(element):
                    return n
        else:
            return self._data.index(element) if element in self._data else None

    @notify
    def add_blank_at_the_end(self):
        self.add_blank(len(self._data))

    @notify
    def add_blank(self, index_: int):
        data = list(self._data)
        data.insert(index_, Blank())
        self._data = tuple(data)

    @notify
    def merge_data(self, account_order_data, shape_id_converter: dict):
        impl.merge_account_order_data(self, account_order_data, shape_id_converter)

    @notify
    def convert_data(self, shape_id_converter: dict):
        shape_ids_converted = []
        for data in self._data:
            if data.__class__ != Blank:
                try:
                    shape_id_converted = shape_id_converter[data]
                except KeyError:
                    continue
                shape_ids_converted.append(shape_id_converted)
            else:
                shape_ids_converted.append(Blank())

        self._data = tuple(shape_ids_converted)

    @notify
    def change_shape_id(self, old_shape_id, new_shape_id):
        self._data = tuple(new_shape_id if data == old_shape_id else data for data in self._data)


class Blank(object):

    def __repr__(self) -> str:
        return 'blank'

    __hash__ = object.__hash__

    def __eq__(self, other) -> bool:
        """
        __eq__ and __hash__ must both be overridden.
        Blank() always equals other Blank() to prevent unnecessary mementos.
        """
        return self.__class__.__name__ == other.__class__.__name__
