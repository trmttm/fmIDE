from abc import ABC
from abc import abstractmethod
from typing import Callable


class PresenterABC(ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer: Callable):
        self._observers.append(observer)

    @abstractmethod
    def create_view_model(self, response_model):
        pass

    def present(self, response_model=None):
        if self._observers:
            view_model = self.create_view_model(response_model)
            for observer in self._observers:
                observer(view_model)
