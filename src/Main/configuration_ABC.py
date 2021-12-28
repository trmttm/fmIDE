from abc import ABC
from abc import abstractmethod

from interface_fm import BoundaryInABC
from interface_mouse import MouseControllerABC
from interface_view import ViewABC

from ..BoundaryOutput import PresentersABC


class ConfigurationABC(ABC):
    @staticmethod
    @abstractmethod
    def start_view_model_factory() -> list:
        pass

    @staticmethod
    @abstractmethod
    def set_up(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
        pass

    @staticmethod
    def set_up_again_with_wrapped_interactor(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC,
                                             mouse: MouseControllerABC):
        pass

    @staticmethod
    @abstractmethod
    def widget_command_map_factory(view: ViewABC, interactor: BoundaryInABC, mouse: MouseControllerABC,
                                   presenters: PresentersABC) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def mouse_configurations(interactor: BoundaryInABC, view: ViewABC, mouse: MouseControllerABC) -> list:
        pass

    @staticmethod
    @abstractmethod
    def default_keyboard_shortcuts(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                                   mouse: MouseControllerABC) -> dict:
        pass

    @abstractmethod
    def properly_close_app(self, interactor: BoundaryInABC, view: ViewABC):
        pass
