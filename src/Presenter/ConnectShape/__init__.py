from ... import ViewModel
from ...BoundaryOutput import PresenterABC


class PresenterConnectShape(PresenterABC):

    def create_view_model(self, response_model: list) -> list:
        view_model = ViewModel.create_view_model_connect_shapes(response_model)
        return view_model
