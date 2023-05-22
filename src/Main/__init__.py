from typing import Type

from interface_view import ViewABC
from mouse import MouseController
from src.Main.interactor_wrapper import WrappedInteractor

from . import implementation as impl
from . import plug_in_views
from .configuration_ABC import ConfigurationABC
from ..Entities import Entities
from ..Entities import Observable
from ..EntityGateway import GateWayABC
from ..Interactor import Interactor
from ..Presenter import Presenters


class Main:
    def __init__(self, config: ConfigurationABC, view: ViewABC, cls_gateways: Type[GateWayABC], ):
        # Dependencies to abstract interfaces(Dependency Injection).
        """
            1) config
            2) view
            3) cls_gateway
        """

        # Dependencies to concrete implementations
        entities = Entities()
        presenters = Presenters()
        gateways = cls_gateways(entities)
        interactor = Interactor(entities, presenters, gateways)
        interactor.stop_canvas_refreshing()
        mouse = MouseController()  # Mouse connected to Interactor (*not* Views like InputEntry)

        # setups (order matters)
        view.add_widgets(config.start_view_model_factory())
        view.set_exception_catcher(interactor.upon_exception)
        view.set_title('Financial Model Integrated Development Environment')
        view.attach_to_event_upon_closing(self.quit)

        wrapped_interactor = WrappedInteractor(interactor)  # wrapped_interactor captures user actions.

        """
        wrapped_interactor allows mouse actions (such as dragging) to be recorded as macro.
        However, the wrapper is expensive because every actions compares the system state.
        Obtaining system states requires deepcopy, which is expensive.
        
        On the other hand, if interactor is passed to mouse_configurations, then it is much faster.
        But mouse actions are not recorded as macro.
        """
        # impl.configure_mouse(mouse, config.mouse_configurations(wrapped_interactor, view, mouse)) # this makes mouse really slow when there are many shapes
        impl.configure_mouse(mouse, config.mouse_configurations(interactor, view, mouse))

        plug_in_views.plug_views_to_presenters(presenters, view)
        config.set_up(view, interactor, presenters, mouse)
        config.set_up_again_with_wrapped_interactor(view, wrapped_interactor, presenters, mouse)
        command_dictionary = config.widget_command_map_factory(view, wrapped_interactor, mouse, presenters)
        impl.bind_commands_to_widgets(command_dictionary, view)

        interactor.start_canvas_refreshing()
        self.default_keyboard_shortcuts = config.default_keyboard_shortcuts(wrapped_interactor, view, presenters, mouse)
        self._view = view
        self._mouse = mouse
        self._interactor = interactor
        self._config = config

    @property
    def interactor(self) -> Interactor:
        return self._interactor

    @property
    def view(self) -> ViewABC:
        return self._view

    @property
    def mouse(self) -> MouseController:
        return self._mouse

    def run(self):
        Observable.is_debug_mode = False
        self._view.launch_app()

    def quit(self):
        Observable.is_debug_mode = True
        self._config.properly_close_app(self._interactor, self._view)
