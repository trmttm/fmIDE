import importlib.resources
import io
import pickle

from .SaveState import SaveStateABC
from ..Utilities.Memento import Caretaker


class StateIOFile(SaveStateABC):

    def __init__(self, caretaker: Caretaker):
        self._caretaker = caretaker

    def save_state(self, file_path=''):
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(self._caretaker.state_to_save, f)
            return 'success'
        except Exception as e:
            return e

    def load_state_from_package(self, file_name, package):
        memento = self.get_pickle_from_package(package, file_name)
        self._caretaker.restore(memento)

    def merge_state_from_package(self, file_name, package):
        memento = self.get_pickle_from_package(package, file_name)
        self._caretaker.restore_merge(memento)

    def load_state_from_file_system(self, file_path):
        memento = self.get_pickle_from_file_system(file_path)
        self._caretaker.restore(memento)

    def merge_state_from_file_system(self, file_path):
        memento = self.get_pickle_from_file_system(file_path)
        self._caretaker.restore_merge(memento)

    @staticmethod
    def get_pickle_from_package(package, file_name):
        try:
            with importlib.resources.open_binary(package, file_name) as f:
                pickle_data = pickle.load(f)
        except FileNotFoundError:
            pickle_data = None
        return pickle_data

    @staticmethod
    def get_pickle_from_file_system(file_path):
        try:
            with open(file_path, 'rb') as f:
                pickle_data = pickle.load(f)
        except FileNotFoundError:
            pickle_data = None
        return pickle_data

    @staticmethod
    def get_resource_from_file_system(file_path):
        try:
            with open(file_path, "rb") as f:
                resource = io.BytesIO(f.read())
        except FileNotFoundError:
            resource = None
        return resource

    @staticmethod
    def get_resource_from_package(file_name, package):
        try:
            with importlib.resources.open_binary(package, file_name) as f:
                resource = io.BytesIO(f.read())
        except FileNotFoundError:
            resource = None
        return resource

    def save_all_sates(self, file_path=''):
        with open(file_path, 'wb') as f:
            pickle.dump(self._caretaker.all_states, f)

    def restore_all_states(self, file_name, package):
        memento = self.get_pickle_from_package(package, file_name)
        self._caretaker.restore_all_states(memento)

    @property
    def save_result(self) -> str:
        return ''

    def set_state_name(self):
        pass
