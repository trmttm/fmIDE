from ... import ViewModel
from ...BoundaryOutput import PresenterABC


class PresenterStates(PresenterABC):

    def create_view_model(self, response_model: dict) -> str:
        view_model = ViewModel.create_view_model_display_states(response_model)
        return view_model
