from ...BoundaryOutput import PresenterABC


class PresenterFormatColor(PresenterABC):

    def create_view_model(self, response_model: dict):
        view_model = response_model
        return view_model
