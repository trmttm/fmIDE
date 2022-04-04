from typing import Set

from . import implementation as i
from ..Observable import Observable
from ..Observable import notify


class Connections(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._data = set()
        self._new_merged_connections = set()

    @notify
    def clean_data(self, all_shape_ids: tuple):
        for shape_from, shape_to in tuple(self._data):
            if (shape_from not in all_shape_ids) or (shape_to not in all_shape_ids):
                self._data.remove((shape_from, shape_to))

    @notify
    def add_connection(self, id_from, id_to):
        if (id_from != id_to) and (id_from is not None) and (id_to is not None):
            self._data.add((id_from, id_to))

    def add_connections(self, request_models):
        for request_model in request_models:
            self.add_connection(**request_model)

    @notify
    def remove_connection(self, id_from, id_to):
        try:
            self._data.remove((id_from, id_to))
        except KeyError:
            pass

    def remove_connections(self, request_models):
        for request_model in request_models:
            self.remove_connection(**request_model)

    def remove_all_connections_of_a_shape(self, shape_id):
        [self.remove_connection(*connection) for connection in i.get_all_connections_with_a_shape(self._data, shape_id)]

    def remove_all_connections_by_shape_ids(self, shape_ids: tuple):
        for shape_id in shape_ids:
            self.remove_all_connections_of_a_shape(shape_id)

    def remove_all_connections_of_shapes(self, request_models):
        for request_model in request_models:
            self.remove_all_connections_of_a_shape(**request_model)

    @notify
    def remove_all_connections_out_of(self, shape_id):
        connections_to = tuple(self.get_connections_out_of(shape_id))
        for connection_to in connections_to:
            self.remove_connection(shape_id, connection_to)

    @notify
    def remove_all_connections_into(self, shape_id):
        connections_into = tuple(self.get_connections_into(shape_id))
        for connection_into in connections_into:
            self.remove_connection(connection_into, shape_id)

    @notify
    def clear_all_connections(self):
        self._data = set()

    @property
    def data(self) -> Set[tuple]:
        return self._data

    def get_connections_into(self, shape_id) -> set:
        return i.get_connections_into_shape_id(self._data, shape_id)

    def get_connections_out_of(self, shape_id) -> set:
        return i.get_connections_out_of_shape_id(self._data, shape_id)

    def get_all_connections_with_the_shape(self, shape_id) -> tuple:
        return i.get_all_connections_with_a_shape(self._data, shape_id)

    def reset_new_merged_connections(self):
        self._new_merged_connections = set()

    def add_new_merged_connections(self, connection_from, connection_to):
        self._new_merged_connections.add((connection_from, connection_to))

    @property
    def new_merged_connections(self) -> set:
        return self._new_merged_connections

    def merge_data(self, connections_data: set, shape_id_converter: dict):
        self.reset_new_merged_connections()
        i.merge_connections_data(self, connections_data, shape_id_converter)

    def copy(self, original_to_copies: dict = None):
        if original_to_copies is None:
            return
        for original_id, copy_id in original_to_copies.items():
            connections_to_original = self.get_connections_into(original_id)
            connections_from_original = self.get_connections_out_of(original_id)

            for connection_to_original in connections_to_original:
                if connection_to_original in original_to_copies:
                    self.add_connection(original_to_copies[connection_to_original], copy_id)

            for connection_from_original in connections_from_original:
                if connection_from_original in original_to_copies:
                    self.add_connection(copy_id, original_to_copies[connection_from_original])

    @notify
    def change_shape_id(self, old_shape_id, new_shape_id):
        i.change_shape_id(self, new_shape_id, old_shape_id)
