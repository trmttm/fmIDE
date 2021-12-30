class StatesAndFlags:
    def __init__(self):
        self._entry_by = []
        self._copied_accounts = tuple()
        self._initial_shape_position = None
        self._manually_highlighted = False
        self._input_being_modified = None
        self._cache_circular_connections = None
        self._prevent_auto_highlight = False
        self._previous_previous_commands = ()
        self._previous_commands = []

    @property
    def entry_by(self):
        return self._entry_by

    @property
    def entry_by_template_tree(self) -> bool:
        # TODO this is undesirable logical coupling with App Configuration
        return self._entry_by != [] and self._entry_by[0] == 'tree_pickle_files'

    @property
    def entry_by_mouse(self) -> bool:
        # TODO this is undesirable logical coupling with App Configuration
        try:
            return self._entry_by[0] == 'mouse'
        except IndexError:
            return False

    @property
    def is_more_than_second_entry(self) -> bool:
        return len(self._entry_by) > 0

    def remove_entry_by(self, exit_by):
        index_ = self._entry_by.index(exit_by)
        del self._entry_by[index_]

    def clear_entry_by(self):
        self._entry_by = []

    def set_entry_by(self, entry_by):
        self._entry_by.append(entry_by)

    @property
    def copied_accounts(self):
        return self._copied_accounts

    def set_copied_accounts(self, accounts):
        self._copied_accounts = accounts

    def clear_copied_accounts(self):
        self._copied_accounts = tuple()

    @property
    def initial_shape_position(self):
        return self._initial_shape_position

    @property
    def initial_shape_position_is_not_set(self) -> bool:
        return self._initial_shape_position is None

    def clear_initial_shape_position(self):
        self._initial_shape_position = None

    def set_initial_shape_position(self, shape_id, shape_x, shape_y):
        self._initial_shape_position = shape_id, shape_x, shape_y

    @property
    def manually_highlighted(self):
        return self._manually_highlighted

    def set_manually_highlighted(self, value):
        self._manually_highlighted = value

    @property
    def input_being_modified(self):
        return self._input_being_modified

    def set_input_being_modified(self, input_account):
        self._input_being_modified = input_account

    def clear_input_being_modified(self):
        self._input_being_modified = None

    @property
    def cache_circular_connections(self):
        return self._cache_circular_connections

    @property
    def circular_connections_is_not_cached(self) -> bool:
        return self._cache_circular_connections is None

    def set_cache_circular_connections(self, circular_connections):
        self._cache_circular_connections = circular_connections

    def clear_cache_circular_connections(self):
        self._cache_circular_connections = None

    @property
    def prevent_auto_highlight(self):
        return self._prevent_auto_highlight

    def set_prevent_auto_highlight(self, value):
        self._prevent_auto_highlight = value

    @property
    def previous_previous_commands(self):
        return self._previous_previous_commands

    def set_previous_previous_commands(self, previous_commands):
        self._previous_commands = tuple(previous_commands)

    @property
    def previous_commands(self):
        return self._previous_commands
