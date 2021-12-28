from ...BoundaryOutput import PresenterABC
from ...ViewModel import create_view_model_update_accounts_with_deltas


class PresenterAccountsListWithDeltas(PresenterABC):

    def create_view_model(self, response_model: dict):
        view_model = create_view_model_update_accounts_with_deltas(response_model)
        return view_model
