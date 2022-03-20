import copy

from Utilities import Memento as Mm

from ..Entities import Entities


class SystemState(Mm.OriginatorABC):
    def __init__(self, entities: Entities):
        self._entities = entities
        self._last_state = None

    @property
    def state(self) -> list:
        entities = self._entities
        state = copy.deepcopy([entities.connections.data,  # 0
                               entities.selection.data,  # 1
                               entities.shapes.data,  # 2
                               entities.rectangle_selector.data,  # 3
                               entities.lines.data,  # 4
                               entities.account_order.data,  # 5
                               entities.account_orders.data,  # 6
                               entities.selections.data,  # 7
                               entities.worksheets.data,  # 8
                               entities.configurations.data,  # 9
                               entities.input_values.data,  # 10
                               entities.input_ranges.data,  # 11
                               entities.connection_ids.data,  # 12
                               entities.format.data,  # 13
                               entities.number_format.data,  # 14
                               entities.vertical_accounts.data,  # 15
                               entities.commands.data,  # 16
                               entities.copied_commands.data,  # 17
                               entities.input_decimals.data,  # 18
                               entities.shape_format.data,  # 19
                               entities.unit_of_measure.data,  # 20
                               entities.worksheet_relationship.data,  # 21
                               entities.breakdown_accounts.data,  # 22
                               ])
        return state

    def save(self, name: str = '') -> Mm.MementoABC:
        state = self.state
        self.set_last_state(state)
        return Mm.Memento(state)

    def restore(self, memento: Mm.MementoABC) -> None:
        entities = self._entities
        state = memento.get_state()

        entities.connections.set_data(state[0])
        entities.shapes.set_data(state[2])
        entities.rectangle_selector.set_data(state[3])
        entities.lines.set_data(state[4])
        entities.account_orders.set_data(state[6])
        entities.selections.set_data(state[7])
        entities.worksheets.set_data(state[8])

        # 9 configuration should not be loaded. => WHY? => because NOP should be consistent across templates.
        # restore_if_state_exists_otherwise_initialize(entities.configurations, 9, state)
        restore_if_state_exists_otherwise_initialize(entities.input_values, 10, state)
        restore_if_state_exists_otherwise_initialize(entities.input_ranges, 11, state)
        restore_if_state_exists_otherwise_initialize(entities.connection_ids, 12, state)
        restore_if_state_exists_otherwise_initialize(entities.format, 13, state)
        restore_if_state_exists_otherwise_initialize(entities.number_format, 14, state)
        restore_if_state_exists_otherwise_initialize(entities.vertical_accounts, 15, state)
        # No need to load commands / macro, because loading pickle is part of macro sequence.
        restore_if_state_exists_otherwise_initialize(entities.input_decimals, 18, state)
        restore_if_state_exists_otherwise_initialize(entities.shape_format, 19, state)
        restore_if_state_exists_otherwise_initialize(entities.unit_of_measure, 20, state)
        restore_if_state_exists_otherwise_initialize(entities.worksheet_relationship, 21, state)
        restore_if_state_exists_otherwise_initialize(entities.breakdown_accounts, 22, state)

    def restore_merge(self, memento: Mm.MementoABC, *args, **kwargs):
        entities = self._entities
        state = memento.get_state()

        shape_id_converter = entities.shapes.merge_data(state[2])

        entities.connections.merge_data(state[0], shape_id_converter)
        entities.selections.merge_data(state[7], shape_id_converter)
        entities.account_orders.merge_data(state[6], shape_id_converter)
        entities.worksheets.merge_data(state[8], shape_id_converter)

        merge_state_if_available(entities.input_values, 10, shape_id_converter, state)
        merge_state_if_available(entities.input_ranges, 11, shape_id_converter, state)
        merge_state_if_available(entities.connection_ids, 12, shape_id_converter, state)
        merge_state_if_available(entities.format, 13, shape_id_converter, state)
        merge_state_if_available(entities.number_format, 14, shape_id_converter, state)
        merge_state_if_available(entities.vertical_accounts, 15, shape_id_converter, state)
        merge_state_if_available(entities.input_decimals, 18, shape_id_converter, state)
        merge_state_if_available(entities.shape_format, 19, shape_id_converter, state)
        merge_state_if_available(entities.unit_of_measure, 20, shape_id_converter, state)
        merge_state_if_available(entities.worksheet_relationship, 21, shape_id_converter, state)
        merge_state_if_available(entities.breakdown_accounts, 22, shape_id_converter, state)

    def set_last_state(self, state):
        self._last_state = state

    def get_last_state(self):
        return self._last_state

    def state_changed(self) -> bool:
        return self.states_are_different(self._last_state, self.state)

    @staticmethod
    def states_are_different(state_one, state_two) -> bool:
        if state_one is None:
            return True
        for n, (state_previous, state_current) in enumerate(zip(state_one, state_two)):
            if n <= 5 or 9 <= n:
                # Immutable data
                if state_previous != state_current:
                    return True
            elif n in (6, 7):
                # AccountOrders, Selections
                if set(state_previous.keys()) != set(state_current.keys()):
                    return True
                else:
                    for sheet_name in state_previous.keys():
                        if state_previous[sheet_name].data != state_current[sheet_name].data:
                            return True
            elif n == 8:
                # Worksheets
                for key in state_previous.keys():
                    if state_previous[key] != state_current[key]:
                        return True
        return False


def restore_if_state_exists_otherwise_initialize(entity, number, state):
    if len(state) > number:
        entity.set_data(state[number])
    else:
        entity.__init__()


def restore_if_state_exists(entity, number, state):
    if len(state) > number:
        entity.set_data(state[number])


def merge_state_if_available(entity, number, shape_id_converter, state):
    if len(state) > number:
        entity.merge_data(state[number], shape_id_converter)
