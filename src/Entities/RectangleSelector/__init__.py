from typing import Union

from . import constants as cns
from . import implementation as impl
from ..Observable import Observable
from ..Observable import notify


class RectangleSelectors(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._data = {}
        self._id = 0

    @notify
    def draw_rectangle(self, coords1, coords2, width, color):
        args = coords1, coords2, width, color
        while self._id in self._data:
            self._id += 1
        self._data.update(impl.create_rectangle_selector(self._id, *args))
        self._id += 1

    def draw_rectangles(self, request_models):
        for request_model in request_models:
            self.draw_rectangle(**request_model)

    @property
    def data(self) -> dict:
        return self._data

    @notify
    def erase_rectangle(self, rectangle_id):
        del self._data[rectangle_id]

    def erase_rectangles(self, request_models):
        for request_model in request_models:
            self.erase_rectangle(**request_model)

    @notify
    def clear_rectangle(self):
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
