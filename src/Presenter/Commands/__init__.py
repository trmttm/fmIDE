from src.BoundaryOutput import PresenterABC

from src import ViewModel


class PresenterCommands(PresenterABC):

    def create_view_model(self, response_model: dict) -> str:
        view_model = ViewModel.create_view_model_update_commands(response_model)
        return view_model
