from Utilities.Memento import CaretakerABC

from .SaveState import SaveStateABC


class StatesIOMemory(SaveStateABC):

    def __init__(self, caretaker: CaretakerABC):
        self._caretaker = caretaker

    def save_state(self, name=''):
        self._caretaker.backup(name)

    def load_state_from_package(self, memento):
        self._caretaker.restore(memento)

    @property
    def save_result(self) -> str:
        return self._caretaker.__repr__()

    def undo(self):
        self._caretaker.undo()

    def redo(self):
        self._caretaker.redo()

    def set_state_name(self):
        pass
