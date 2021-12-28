from ...BoundaryOutput import PresenterABC
from ...ViewModel import create_view_model_update_account_order


class PresenterUpdateAccountOrder(PresenterABC):

    def create_view_model(self, response_model: dict):
        view_model = create_view_model_update_account_order(response_model)
        return view_model
