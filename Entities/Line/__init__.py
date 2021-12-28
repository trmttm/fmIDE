from typing import Union

from . import constants as cns
from . import implementation as impl
from ..Observable import Observable
from ..Observable import notify


class Lines(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._data = {}
        self._id = 0

    @notify
    def draw_line(self, coordinate_from, coordinate_to, width, color):
        args = coordinate_from, coordinate_to, width, color
        self._prevent_collision_with_loaded_data()
        self._data.update(impl.draw_line(self._id, *args))
        self._id += 1

    def draw_lines(self, request_models):
        for request_model in request_models:
            self.draw_line(**request_model)

    def _prevent_collision_with_loaded_data(self):
        while self._id in self._data:
            self._id += 1

    @property
    def data(self) -> dict:
        return self._data

    @notify
    def erase_line(self, line_id):
        del self._data[line_id]

    def erase_lines(self, request_models):
        for request_model in request_models:
            self.erase_line(**request_model)

    @notify
    def clear_lines(self):
        self._data = {}


def get_args(request_model: dict) -> Union[None, tuple]:
    try:
        coords1 = request_model[cns.coordinate_from]
        coords2 = request_model[cns.coordinate_to]
        width = request_model[cns.line_width]
        color = request_model[cns.line_color]
        args = (coords1, coords2, width, color)
    except KeyError:
        args = None
    return args
