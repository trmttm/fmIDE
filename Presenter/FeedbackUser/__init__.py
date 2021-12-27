from ... import ViewModel
from ...BoundaryOutput import PresenterABC


class PresenterFeedbackUser(PresenterABC):

    def create_view_model(self, response_model: dict):
        view_model = ViewModel.create_view_model_user_feedback(response_model)
        return view_model
