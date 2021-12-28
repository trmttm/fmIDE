from typing import Dict
from typing import Iterable

from ..Observable import Observable
from ..Observable import notify


class ConnectionIDs(Observable):
    _key_connection_ids = '_key_connection_ids'
    _key_partner_plugs = '_key_partner_plugs'
    _key_partner_sockets = '_key_partner_sockets'

    def __init__(self):
        Observable.__init__(self)
        self._data: Dict[str, Dict[str, tuple]] = {
            self._key_connection_ids: {},
            self._key_partner_plugs: {},
            self._key_partner_sockets: {}
        }

    @notify
    def clean_data(self):
        for _, data_dict in self._data.items():
            for account_id in tuple(data_dict.keys()):
                if data_dict[account_id] == ():
                    del data_dict[account_id]

    def add_connection_ids(self, shape_ids: Iterable, connection_id: Iterable):
        for shape_id, socket_name in zip(shape_ids, connection_id):
            self.add_connection_id(shape_id, socket_name)

    def add_sockets_to_dynamically_search_for(self, shape_ids: Iterable, socket_id):
        for shape_id in shape_ids:
            self.add_socket_to_dynamically_search_for(shape_id, socket_id)

    def add_plugs_to_dynamically_accept(self, shape_ids: Iterable, plug_id):
        for shape_id in shape_ids:
            self.add_plug_to_dynamically_accept(shape_id, plug_id)

    @notify
    def add_connection_id(self, shape_id, connection_id: str):
        self._add_value(shape_id, self._key_connection_ids, connection_id)

    @notify
    def add_socket_to_dynamically_search_for(self, shape_id, connection_id):
        self._add_value(shape_id, self._key_partner_sockets, connection_id)

    @notify
    def add_plug_to_dynamically_accept(self, shape_id, connection_id):
        self._add_value(shape_id, self._key_partner_plugs, connection_id)

    def remove_shape_ids(self, shape_ids: Iterable):
        for shape_id in shape_ids:
            self.remove_shape_id(shape_id)

    @notify
    def remove_shape_id(self, shape_id):
        for data_dictionary in self._data.values():
            if shape_id in data_dictionary:
                del data_dictionary[shape_id]

    @notify
    def remove_connection_id(self, shape_id, connection_id):
        try:
            connection_ids: tuple = self._data[self._key_connection_ids][shape_id]
        except KeyError:
            return
        new_connection_id = tuple(c for c in connection_ids if c != connection_id)
        self._data[self._key_connection_ids][shape_id] = new_connection_id

    @notify
    def remove_socket_id(self, shape_id, socket_id):
        try:
            socket_ids: tuple = self._data[self._key_partner_sockets][shape_id]
        except KeyError:
            return
        new_socket_id = tuple(c for c in socket_ids if c != socket_id)
        self._data[self._key_partner_sockets][shape_id] = new_socket_id

    @notify
    def remove_plug_id(self, shape_id, plug_id):
        try:
            plug_ids: tuple = self._data[self._key_partner_plugs][shape_id]
        except KeyError:
            return
        new_plug_id = tuple(c for c in plug_ids if c != plug_id)
        self._data[self._key_partner_plugs][shape_id] = new_plug_id

    def has_connection_id(self, shape_id) -> bool:
        return shape_id in self._data[self._key_connection_ids]

    def get_connection_ids(self, shape_id) -> tuple:
        if shape_id in self._data[self._key_connection_ids]:
            return self._data[self._key_connection_ids][shape_id]
        else:
            return ()

    def get_plugs_that_i_want(self, shape_id) -> tuple:
        if shape_id in self._data[self._key_partner_plugs]:
            return self._data[self._key_partner_plugs][shape_id]
        else:
            return ()

    def get_sockets_that_i_want(self, shape_id) -> tuple:
        if shape_id in self._data[self._key_partner_sockets]:
            return self._data[self._key_partner_sockets][shape_id]
        else:
            return ()

    def get_plugs_who_wants_me(self, shape_id) -> tuple:
        return self._get_partners_who_wants_me(self._key_partner_sockets, shape_id)

    def get_sockets_who_wants_me(self, shape_id) -> tuple:
        return self._get_partners_who_wants_me(self._key_partner_plugs, shape_id)

    def _get_partners_who_wants_me(self, key, shape_id):
        me = shape_id
        results = []
        for shape_id_who_may_want_me, sockets in self._data[key].items():
            if me in sockets:
                results.append(shape_id_who_may_want_me)
        return tuple(results)

    def get_shape_ids_connection_id(self, plug_id) -> tuple:
        plugs = ()
        for shape_id, connection_ids in self._data[self._key_connection_ids].items():
            if plug_id in connection_ids:
                plugs += (shape_id,)
        return plugs

    def change_shape_id(self, old_shape_id, new_shape_id):
        for dictionary in self._data.values():
            if old_shape_id in dictionary:
                dictionary[new_shape_id] = dictionary[old_shape_id]
                del dictionary[old_shape_id]

    @notify
    def merge_data(self, data: Dict[str, Dict[str, tuple]], shape_id_converter: dict):
        for key, dictionary in data.items():
            for shape_id, values in dictionary.items():
                if shape_id in shape_id_converter:
                    shape_id_converted = shape_id_converter[shape_id]
                    self._data[key][shape_id_converted] = values

    @notify
    def copy(self, from_id, to_id):
        my_connection_ids = self.get_connection_ids(from_id)
        plugs_i_want = self.get_plugs_that_i_want(from_id)
        sockets_i_want = self.get_sockets_that_i_want(from_id)

        for connection_id in my_connection_ids:
            self.add_connection_id(to_id, connection_id)
        for plug in plugs_i_want:
            self.add_plug_to_dynamically_accept(to_id, plug)
        for socket in sockets_i_want:
            self.add_socket_to_dynamically_search_for(to_id, socket)

    def _add_value(self, shape_id, key, value):
        if shape_id in self._data[key]:
            if value not in self._data[key][shape_id]:
                self._data[key][shape_id] += (value,)
        else:
            self._data[key].update({shape_id: (value,)})
