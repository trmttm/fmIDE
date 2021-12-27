from .Observable import Observable
from .Observable import notify


class CopiedCommands(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._data = ()

    @property
    def data(self) -> tuple:
        return self._data

    @notify
    def set(self, commands: tuple):
        self._data = commands
