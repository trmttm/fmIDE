from abc import ABC
from abc import abstractmethod

from .memento_ABC import MementoABC


class OriginatorABC(ABC):
    @abstractmethod
    def save(self, name: str = '') -> MementoABC:
        pass

    @abstractmethod
    def restore(self, memento: MementoABC) -> None:
        pass

    @abstractmethod
    def restore_merge(self, memento: MementoABC, *args, **kwargs):
        pass
