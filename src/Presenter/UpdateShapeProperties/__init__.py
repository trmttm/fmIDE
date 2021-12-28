from ... import ViewModel
from ...BoundaryOutput import PresenterABC


class PresenterUpdateShapeProperties(PresenterABC):

    def create_view_model(self, response_model: dict):
        view_model = ViewModel.create_view_model_update_properties(response_model)
        return view_model
