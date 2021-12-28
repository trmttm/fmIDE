from datetime import datetime

from .memento_ABC import MementoABC


class Memento(MementoABC):
    def __init__(self, state, name: str = '') -> None:
        self._state = state
        self._date = str(datetime.now())[:19]
        self._name = name

    def get_state(self):
        """
        The Originator uses this method when restoring its states.
        """
        return self._state

    def get_name(self) -> str:
        """
        The rest of the methods are used by the Caretaker to display metadata.
        """

        return f"{self._date} {self._name}"

    def get_date(self) -> str:
        return self._date
