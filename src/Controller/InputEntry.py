from typing import Callable
from typing import List
from typing import Tuple


class InputEntryController:

    def __init__(self):
        self._observers: List[Callable] = []

    def attach(self, observer: Callable):
        self._observers.append(observer)

    def handle(self, y_range: Tuple[float, float], positions: tuple):
        y_min, y_max = y_range
        values = tuple(y_min + (y_max - y_min) * (1 - position) for position in positions)
        for observer in self._observers:
            observer(values)
