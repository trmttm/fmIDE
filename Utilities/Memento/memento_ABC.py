from abc import ABC
from abc import abstractmethod


class MementoABC(ABC):
    """
    The MementoABC interface provides a way to retrieve the Mm'shapes metadata,
    such as creation date or relative_path. However, it doesn'rpes expose the Originator'shapes
    states.
    """

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_date(self) -> str:
        pass

    @abstractmethod
    def get_state(self):
        pass
