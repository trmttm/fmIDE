from typing import List

from ... import ViewModel
from ...BoundaryOutput import PresenterABC


class PresenterAddShape(PresenterABC):

    def create_view_model(self, response_model: dict) -> List[dict]:
        return ViewModel.create_view_model_add_shape(response_model)
