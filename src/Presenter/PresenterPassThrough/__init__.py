from ...BoundaryOutput import PresenterABC


class PresenterPassThrough(PresenterABC):

    def create_view_model(self, response_model):
        return response_model
