from src.Interactor import Interactor


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
