from typing import Iterable

import Utilities

from .Observable import Observable
from .Observable import notify


class Commands(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._data: tuple = ()
        self._macro_recording_mode = False

        # flags
        self._cleared_commands = False
        self._turned_on_macro_recording = False
        self._turned_off_macro_recording = False

        self._magic_args = {}

    @property
    def data(self) -> tuple:
        return self._data

    @property
    def cleared_commands(self) -> bool:
        return self._cleared_commands

    @property
    def turned_off_macro_recording(self) -> bool:
        return self._turned_off_macro_recording

    @property
    def turned_on_macro_recording(self) -> bool:
        return self._turned_on_macro_recording

    @notify
    def add_command(self, key, args: tuple, kwargs: dict):
        if self._macro_recording_mode:
            self._data += ((key, args, kwargs),)

    @notify
    def insert_commands(self, index_: int, commands: tuple):
        new_data = []
        for n, command in enumerate(self._data):
            if n == index_:
                new_data += list(cmd for cmd in commands)
            new_data.append(command)
        if len(new_data) <= index_:
            new_data += list(cmd for cmd in commands)
        self._data = tuple(new_data)

    @notify
    def delete_commands(self, indexes: tuple):
        existing_data = self._data
        new_data = Utilities.remove_item_from_tuple_by_index(existing_data, indexes)
        self._data = new_data

    @notify
    def shift_multiple_commands(self, indexes: tuple, shift: int) -> tuple:
        existing_data = self._data
        args = existing_data, indexes, shift
        destinations, new_data = Utilities.get_tuple_and_destinations_after_shifting_elements(*args)
        self._data = new_data
        return destinations

    @notify
    def change_command_name(self, index_: int, command_name: str):
        new_data = []
        for n, command in enumerate(self._data):
            if n == index_:
                _, args, kwargs = command
                new_data.append((command_name, args, kwargs))
            else:
                new_data.append(command)
        self._data = tuple(new_data)

    @notify
    def change_args(self, index_: int, args: tuple):
        new_data = []
        for n, command in enumerate(self._data):
            if n == index_:
                key, _, kwargs = command
                new_data.append((key, args, kwargs))
            else:
                new_data.append(command)
        self._data = tuple(new_data)

    @notify
    def change_kwargs(self, index_: int, kwargs: dict):
        new_data = []
        for n, command in enumerate(self._data):
            if n == index_:
                key, args, _ = command
                new_data.append((key, args, kwargs))
            else:
                new_data.append(command)
        self._data = tuple(new_data)

    @notify
    def merge_data(self, data: tuple, *_, **__):
        self._data += data

    @notify
    def clear_commands(self):
        self.__init__()
        self._cleared_commands = True

    def get_command_name(self, index_: int):
        return self._get_data(index_, 0)

    def get_args(self, index_: int):
        return self._get_data(index_, 1)

    def get_kwargs(self, index_: int):
        return self._get_data(index_, 2)

    def _get_data(self, index_, data_index):
        if index_ <= len(self._data) - 1:
            return self._data[index_][data_index]
        else:
            return None

    def start_macro_recording(self):
        self._macro_recording_mode = True
        self._turned_on_macro_recording = True

    def stop_macro_recording(self):
        self._macro_recording_mode = False
        self._turned_off_macro_recording = True

    @property
    def is_macro_recording_mode(self) -> bool:
        return self._macro_recording_mode

    def run_macro(self, obj, observers: Iterable = ()) -> tuple:
        self._cleared_commands = False
        self._turned_on_macro_recording = False
        self._turned_off_macro_recording = False

        initial_number_of_commands = len(self._data)
        return_values = []
        total_n = len(self._data)
        for n, (key, args, kwargs) in enumerate(self._data):
            for observer in observers:
                observer(n, total_n, key)
            try:
                command = getattr(obj, key)
            except Exception as e:
                return False, (n, key, args, kwargs, e)
            if command.__name__ not in ('set_magic_arg', 'set_multiple_magic_args'):
                args = self._apply_magic_arg(args)
            if command.__name__ == 'delete_commands_up_to':
                args = (initial_number_of_commands - 1,)
            try:
                return_value = command(*args, **kwargs)
            except Exception as e:
                return False, (n, key, args, kwargs, e)
            return_values.append(return_value)
        return True, tuple(return_values)

    def set_magic_arg_with_magic_arg(self, arg, replace_with):
        self.set_magic_arg(arg, replace_with)

    def set_magic_arg(self, arg, replace_with):
        self._magic_args[arg] = replace_with

    def _apply_magic_arg(self, args: tuple):
        new_args = []
        for arg in args:
            if arg.__class__ == str:
                text = arg
                self._replace_text_with_magic_arg(new_args, text)
            elif arg.__class__ == tuple:
                tuple_arg_replaced = []
                for each_arg in arg:
                    text = each_arg
                    self._replace_text_with_magic_arg(tuple_arg_replaced, text)
                new_args.append(tuple(tuple_arg_replaced))
            else:
                new_args.append(arg)
        return tuple(new_args)

    def _replace_text_with_magic_arg(self, new_args, text):
        for key, value in self._magic_args.items():
            try:
                text = str(text).replace(key, value)
            except TypeError:  # value is not string, input_values, for example
                if text == key:
                    text = value
        new_args.append(text)
