from ...BoundaryOutput import PresenterABC
from ...ViewModel import create_view_model_update_accounts


class PresenterAccountsList(PresenterABC):

    def create_view_model(self, response_model: dict):
        view_model = create_view_model_update_accounts(response_model)
        return view_model
