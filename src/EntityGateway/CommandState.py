import copy

from Utilities import Memento as Mm
from src.Entities import Entities


class CommandState(Mm.OriginatorABC):
    def __init__(self, entities: Entities):
        self._entities = entities
        self._last_state = None

    @property
    def state(self) -> list:
        entities = self._entities
        state = copy.deepcopy([
            entities.commands.data,  # 0
        ])
        return state

    def save(self, name: str = '') -> Mm.MementoABC:
        state = self.state
        self.set_last_state(state)
        return Mm.Memento(state)

    def restore(self, memento: Mm.MementoABC) -> None:
        entities = self._entities
        state = memento.get_state()

        entities.commands.set_data(state[0])

    def restore_merge(self, memento: Mm.MementoABC, *args, **kwargs):
        entities = self._entities
        state = memento.get_state()

        entities.commands.merge_data(state[0])

    def restore_merge_insert(self, memento: Mm.MementoABC, *args, **kwargs):
        entities = self._entities
        state = memento.get_state()

        entities.commands.merge_data_insert(state[0])

    def set_last_state(self, state):
        self._last_state = state

    def get_last_state(self):
        return self._last_state

    def state_changed(self):
        return self._last_state != self.state
