from abc import ABC
from abc import abstractmethod


class SaveStateABC(ABC):
    @abstractmethod
    def save_state(self, name=''):
        pass

    @abstractmethod
    def load_state(self, file_name, package):
        pass

    @abstractmethod
    def set_state_name(self):
        pass

    @property
    @abstractmethod
    def save_result(self):
        pass
