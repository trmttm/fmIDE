import copy

from .caretaker_ABC import CaretakerABC
from .memento import Memento
from .memento_ABC import MementoABC
from .originator_ABC import OriginatorABC


class Caretaker(CaretakerABC):
    """
    The Caretaker doesn't depend on the Concrete MementoABC class. Therefore, it
    doesn't have access to the originator's states, stored inside the Mm. It
    works with all mementos via the base MementoABC interface.
    """

    def __init__(self, originator: OriginatorABC) -> None:
        self._mementos_past_states = []
        self._mementos_future_states = []
        self._memento_current_state = []
        self._originator = originator

    def backup(self, event: str = '') -> None:
        if self._mementos_future_states:
            # Overwrite current and future states.
            self._mementos_future_states = []
            self._memento_current_state = []

        if not self._memento_current_state:
            memento_current = self._originator.save(event)

            if there_are_changes_in_new_state(memento_current, self._mementos_past_states):
                self._mementos_past_states.append(memento_current)
        else:
            # Current state is already backed up. This time no need to back up.
            self._mementos_past_states.append(self._memento_current_state.pop())

    def undo(self) -> None:
        if not len(self._mementos_past_states):
            return

        memento_from_past = self._mementos_past_states.pop()
        if not self._memento_current_state:
            memento_current = self._originator.save('Last state')
            self._mementos_future_states.append(memento_current)
        else:
            self._mementos_future_states.append(self._memento_current_state.pop())

        self._memento_current_state.append(memento_from_past)

        try:
            self.restore(memento_from_past)
        except Exception:
            self.undo()

    def redo(self):
        if not len(self._mementos_future_states):
            return

        self._mementos_past_states.append(self._memento_current_state.pop())
        memento_from_future = self._mementos_future_states.pop()
        self._memento_current_state.append(memento_from_future)

        try:
            self.restore(memento_from_future)
        except Exception:
            self.redo()

    def show_history(self) -> None:
        print("Caretaker: Here'shapes the list of mementos:")
        for memento in self._mementos_past_states:
            print(memento.get_name())

    @property
    def mementos(self) -> list:
        return self._mementos_past_states

    def restore(self, memento: MementoABC):
        self._originator.restore(copy.deepcopy(memento))

    def restore_merge(self, memento: MementoABC, *args, **kwargs):
        self._originator.restore_merge(copy.deepcopy(memento), *args, **kwargs)

    @property
    def name(self) -> str:
        return self._originator.__class__.__name__

    def __repr__(self) -> str:
        n_past = len(self._mementos_past_states)
        past_states = str([m for m in range(n_past)]).replace(']', '')
        current_state = str(n_past) if self._memento_current_state != [] else None
        future_states = str([m + n_past + 1 for m in range(len(self._mementos_future_states))]).replace('[', '')
        past_states_recent10 = past_states[-10] if len(past_states) >= 10 else past_states
        r = f'Mementos {past_states_recent10} |{current_state or " "}| {future_states}'
        return r

    @property
    def all_states(self) -> MementoABC:
        state = copy.deepcopy(self._mementos_past_states),
        return Memento(state)

    def restore_all_states(self, memento: MementoABC):
        state = memento.get_state()
        self._mementos_past_states = copy.deepcopy(state[0])
        self.undo()

    @property
    def state_to_save(self) -> MementoABC:
        return copy.deepcopy(self._originator.save())


def there_are_changes_in_new_state(memento_current, past_mementos: list):
    try:
        memento_previous = past_mementos[-1]
    except IndexError:
        memento_previous = None
    flag = (memento_previous is None) or (memento_previous.get_state() != memento_current.get_state())
    return flag
