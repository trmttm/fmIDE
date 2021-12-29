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
        memento = self.get_memento_from_package(package, file_name)
        self._caretaker.restore(memento)

    def load_state_from_file_system(self, file_path):
        memento = self.get_memento_from_file_system(file_path)
        self._caretaker.restore(memento)

    def merge_state_from_package(self, file_name, package):
        memento = self.get_memento(file_name, package)
        self._caretaker.restore_merge(memento)

    def merge_state_from_file_system(self, file_path):
        memento = self.get_memento_from_file_system(file_path)
        self._caretaker.restore_merge(memento)

    def get_memento(self, file_name, package):
        memento = self.get_pickle(file_name, package)
        return memento

    def get_pickle(self, file_name, package):
        memento = self.get_memento_from_package(package, file_name)
        return memento

    @staticmethod
    def get_memento_from_file_system(file_path):
        memento = StateIOFile.get_resource_pickle_load_by_file_path(file_path)
        return memento

    def save_all_sates(self, file_path=''):
        with open(file_path, 'wb') as f:
            pickle.dump(self._caretaker.all_states, f)

    def restore_all_states(self, file_name, package):
        memento = self.get_memento_from_package(package, file_name)
        self._caretaker.restore_all_states(memento)

    @staticmethod
    def get_resource(file_name, package):
        with importlib.resources.open_binary(package, file_name) as f:
            resource = io.BytesIO(f.read())
        return resource

    @staticmethod
    def get_memento_from_package(package, file_name):
        try:
            with importlib.resources.open_binary(package, file_name) as f:
                memento = pickle.load(f)
        except FileNotFoundError:
            memento = None
        return memento

    @staticmethod
    def get_resource_pickle_load_by_file_path(file_path):
        try:
            with open(file_path, 'rb') as f:
                memento = pickle.load(f)
        except FileNotFoundError:
            memento = None
        return memento

    @property
    def save_result(self) -> str:
        return ''

    def set_state_name(self):
        pass
