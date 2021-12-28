from ...BoundaryOutput import PresenterABC


class PresenterMoveShape(PresenterABC):

    def create_view_model(self, response_model: dict):
        return response_model
