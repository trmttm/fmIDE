from ...BoundaryOutput import PresenterABC
from ...ViewModel import create_view_model_pickle_loader_list


class PresenterLoadPickleFilesList(PresenterABC):

    def create_view_model(self, response_model: dict):
        view_model = create_view_model_pickle_loader_list(response_model)
        return view_model
