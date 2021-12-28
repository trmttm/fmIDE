from ... import ViewModel
from ...BoundaryOutput import PresenterABC


class PresenterUpdateConnectionIDs(PresenterABC):

    def create_view_model(self, response_model: dict):
        view_model = ViewModel.create_view_model_connection_ids(response_model)
        return view_model
