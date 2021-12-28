from abc import ABC
from abc import abstractmethod

from .memento_ABC import MementoABC


class CaretakerABC(ABC):

    @abstractmethod
    def backup(self, event: str = '') -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    @abstractmethod
    def redo(self):
        pass

    @abstractmethod
    def show_history(self) -> None:
        pass

    @property
    @abstractmethod
    def mementos(self) -> list:
        pass

    @abstractmethod
    def restore(self, memento: MementoABC):
        pass

    @abstractmethod
    def restore_merge(self, memento: MementoABC, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def all_states(self) -> MementoABC:
        pass

    @abstractmethod
    def restore_all_states(self, memento: MementoABC):
        pass

    @property
    @abstractmethod
    def state_to_save(self) -> MementoABC:
        pass
