from ...BoundaryOutput import PresenterABC


class PresenterScaleCanvas(PresenterABC):

    def create_view_model(self, response_model: dict):
        view_model = response_model['x_times'], response_model['y_times']
        return view_model
