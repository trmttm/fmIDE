from typing import Type

from interface_view import ViewABC
from mouse import MouseController

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
        interactor.present_refresh_canvas()

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


def decorate_with_user_action_catcher(f, wrapped_object: Interactor):
    def wrapper(*args, **kwargs):
        local_f = f

        if not wrapped_object.is_macro_recording_mode:
            return local_f(*args, **kwargs)

        state_before = wrapped_object.current_state
        returned_item = local_f(*args, **kwargs)
        state_after = wrapped_object.current_state

        if local_f in wrapped_object.gateway_out_methods:  # Changes External state such as saving files.
            wrapped_object.add_command(local_f.__name__, args, kwargs)
        elif wrapped_object.states_are_different(state_before, state_after):  # Changed internal state
            wrapped_object.add_command(local_f.__name__, args, kwargs)

        return returned_item

    return wrapper


def decorate_with_set_previous_command_for_repeat(f, wrapped_object: Interactor):
    def wrapper(*args, **kwargs):
        local_f = f

        if wrapped_object.prevent_recording_previous_command:
            return local_f(*args, **kwargs)

        state_before = wrapped_object.current_state
        returned_item = local_f(*args, **kwargs)
        state_after = wrapped_object.current_state

        if wrapped_object.states_are_different(state_before, state_after):
            wrapped_object.set_previous_command(local_f, args, kwargs)
        return returned_item

    return wrapper


class WrappedInteractor:
    # User Action Catcher. Caught commands will be used to record Macros.

    """
    Don't capture Overhead methods as commands as there will be duplications.
        = pure invokers
        = setUp, tearDown
    For example, if Invoker method I invokes A->B->C, then only A,B,C have to be captured and recorded as macros.
    Not I + (A,B,C).
    """
    _dont_record_macro = ['set_entry_point', 'exit_point', 'run_macro', 'keyboard_shortcut_handler',
                          'execute_previous_command']
    _dont_set_repeat_command = ['execute_previous_command']

    def __init__(self, obj: Interactor):
        self._wrapped_obj = obj

    def __getattr__(self, attr):
        # Calls to Wrapper's (not Interactor's) methods
        if attr in self.__dict__:
            return getattr(self, attr)

        # Calls to Interactor's methods
        unwrapped_method = getattr(self._wrapped_obj, attr)
        method_to_invoke = unwrapped_method
        if isinstance(self._wrapped_obj.__class__.__dict__[attr], property):
            # @property and _dont_record_macro do not need user action catcher.
            return unwrapped_method
        if attr not in self._dont_record_macro:
            method_to_invoke = decorate_with_user_action_catcher(unwrapped_method, self._wrapped_obj)
        if attr not in self._dont_set_repeat_command:
            method_to_invoke = decorate_with_set_previous_command_for_repeat(method_to_invoke, self._wrapped_obj)
        return method_to_invoke
