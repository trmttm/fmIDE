from . import highlight as h
from .highlight import configure_as_per_each_highlight_data
from ...BoundaryOutput import PresenterABC


class PresenterHighlightShape(PresenterABC):

    def create_view_model(self, response_model: dict) -> dict:
        view_model = configure_as_per_each_highlight_data(response_model)
        return view_model
