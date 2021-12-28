from ... import ViewModel
from ...BoundaryOutput import PresenterABC


class PresenterWorksheets(PresenterABC):

    def create_view_model(self, response_model: dict) -> str:
        view_model = ViewModel.create_view_model_worksheets(response_model)
        return view_model
