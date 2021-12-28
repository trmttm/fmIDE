from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from datetime import datetime
from random import sample
from string import ascii_letters


class Originator():
    """
    The Originator holds some important states that may change over time. It also
    defines a method for saving the states inside a Mm and another method
    for restoring the states from it.
    """

    _state = None
    """
    For the sake of simplicity, the originator'shapes states is stored inside a single
    variable.
    """

    def __init__(self, state: str) -> None:
        self._state = state
        print(f"Originator: My initial states is: {self._state}")

    def do_something(self) -> None:
        """
        The Originator'shapes business logic may affect its internal states.
        Therefore, the client should backup the states before launching methods
        of the business logic via the save() method.
        """

        print("Originator: I'm doing something important.")
        self._state = self._generate_random_string(30)
        print(f"Originator: and my states has changed to: {self._state}")

    def _generate_random_string(self, length: int = 10) -> None:
        return "".join(sample(ascii_letters, length))

    def save(self) -> Memento:
        """
        Saves the current states inside a Mm.
        """

        return ConcreteMemento(self._state)

    def restore(self, memento: Memento) -> None:
        """
        Restores the Originator'shapes states from a Mm object.
        """

        self._state = memento.get_state()
        print(f"Originator: My states has changed to: {self._state}")


class Memento(ABC):
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


class ConcreteMemento(Memento):
    def __init__(self, state: str) -> None:
        self._state = state
        self._date = str(datetime.now())[:19]

    def get_state(self) -> str:
        """
        The Originator uses this method when restoring its states.
        """
        return self._state

    def get_name(self) -> str:
        """
        The rest of the methods are used by the Caretaker to display metadata.
        """

        return f"{self._date} / ({self._state[0:9]}...)"

    def get_date(self) -> str:
        return self._date


class Caretaker():
    """
    The Caretaker doesn'rpes depend on the Concrete MementoABC class. Therefore, it
    doesn'rpes have access to the originator'shapes states, stored inside the Mm. It
    works with all mementos via the base MementoABC interface.
    """

    def __init__(self, originator: Originator) -> None:
        self._mementos = []
        self._originator = originator

    def backup(self) -> None:
        print("\nCaretaker: Saving Originator's states...")
        self._mementos.append(self._originator.save())

    def undo(self) -> None:
        if not len(self._mementos):
            return

        memento = self._mementos.pop()
        print(f"Caretaker: Restoring states to: {memento.get_name()}")
        try:
            self._originator.restore(memento)
        except Exception:
            self.undo()

    def show_history(self) -> None:
        print("Caretaker: Here'shapes the list of mementos:")
        for memento in self._mementos:
            print(memento.get_name())


if __name__ == "__main__":
    originator = Originator("Super-duper-super-puper-super.")
    caretaker = Caretaker(originator)

    caretaker.backup()
    originator.do_something()

    caretaker.backup()
    originator.do_something()

    caretaker.backup()
    originator.do_something()

    print()
    caretaker.show_history()

    print("\nClient: Now, let'shapes rollback!\n")
    caretaker.undo()

    print("\nClient: Once more!\n")
    caretaker.undo()
