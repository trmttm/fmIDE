from ..Observable import Observable
from ..Observable import notify


class Selection(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._data = set()

    @notify
    def add_selection(self, shape_id):
        self._data.add(shape_id)

    @notify
    def add_selections_by_shape_ids(self, shape_ids):
        self._data = self._data.union(set(shape_ids))

    def select_shapes_by_shape_ids(self, shape_ids):
        self._data = set(shape_ids)

    def add_selections(self, request_models):
        for request_model in request_models:
            self.add_selection(**request_model)

    @notify
    def select_shape(self, shape_id):
        self._data = {shape_id}

    def select_shapes(self, request_models):
        for request_model in request_models:
            self.select_shape(**request_model)

    @notify
    def unselect_shape(self, shape_id):
        try:
            self._data.remove(shape_id)
        except KeyError:
            pass

    def unselect_shapes(self, request_models):
        for request_model in request_models:
            self.unselect_shape(**request_model)

    @notify
    def clear_selection(self):
        self._data = set()

    def is_selected(self, shape_id) -> bool:
        return shape_id in self._data

    @property
    def data(self) -> set:
        return self._data

    @notify
    def convert_data(self, shape_id_converter: dict):
        self._data = set(shape_id_converter[shape_id] for shape_id in self._data if shape_id in shape_id_converter)

    @notify
    def change_shape_id(self, old_shape_id, new_shape_id):
        self._data = set(new_shape_id if data == old_shape_id else data for data in self._data)
