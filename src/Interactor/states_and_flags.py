class StatesAndFlags:
    def __init__(self):
        self._entry_by = []
        self._initial_shape_position = None
        self._manually_highlighted = False
        self._input_being_modified = None
        self._cache_circular_connections = None
        self._prevent_auto_highlight = False
        self._prevent_refresh_canvas = False
        self._prevent_recording_previous_command = False
        self._previous_previous_commands = []
        self._previous_commands = []
        self._sheet_name_dictionary = {}
        self._sheet_id = 0

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
    def prevent_refresh_canvas(self):
        return self._prevent_refresh_canvas

    def set_prevent_refresh_canvas(self, value):
        self._prevent_refresh_canvas = value

    def set_prevent_recording_previous_command(self, value: bool):
        self._prevent_recording_previous_command = value

    def prevent_recording_previous_command(self) -> bool:
        return self._prevent_recording_previous_command

    @property
    def previous_previous_commands(self):
        return self._previous_previous_commands

    def set_previous_previous_commands(self, previous_commands):
        self._previous_commands = tuple(previous_commands)

    @property
    def previous_commands(self):
        return self._previous_commands

    def clear_previous_commands(self):
        self._previous_commands = []

    def set_previous_commands(self, previous_commands):
        self._previous_commands = list(previous_commands)

    @property
    def previous_commands_are_not_set(self) -> bool:
        return not self._previous_commands

    def append_previous_commands(self, new_command):
        self._previous_commands.append(new_command)

    def set_previous_commands_to_previous_previous_commands(self):
        """
        If the actions following set_entry_point has no impacts on the state, then restore previous_previous commands
        as the previous command. For example, changing frames from Design -> Macro -> Design has no impacts on the
        state and therefore previous command should not be impacted either
        """
        self.set_previous_previous_commands(self.previous_commands)
        self.clear_previous_commands()

    @property
    def registered_worksheets(self) -> set:
        return set(self._sheet_name_dictionary.keys())

    def add_worksheet(self, new_sheet_name):
        self._add_work_sheet(new_sheet_name, new_sheet_name)

    def remove_worksheet(self, sheet_name):
        if sheet_name in self._sheet_name_dictionary:
            del self._sheet_name_dictionary[sheet_name]

    def change_worksheet(self, old_sheet_name, new_sheet_name):
        self._add_work_sheet(old_sheet_name, new_sheet_name)
        self.remove_worksheet(old_sheet_name)

    def get_sheet_name_to_pass_to_presenter(self, sheet_name) -> str:
        return self._sheet_name_dictionary.get(sheet_name, None)

    def _add_work_sheet(self, old_sheet_name, new_sheet_name):
        # IF new_sheet_name == someone else's old sheet name, then someone else will unintendedly point to the new sheet
        # Below block of codes prevents this error by creating oldest_sheet_name with id for the new_sheet_name.
        someone_elses_old_sheet_names = []
        for some_one_else_sheet_name, some_one_else_old_sheet_name in self._sheet_name_dictionary.items():
            has_old_sheet_name = (some_one_else_sheet_name != some_one_else_old_sheet_name)
            is_someone_else = (some_one_else_sheet_name != old_sheet_name)
            if has_old_sheet_name and is_someone_else:
                someone_elses_old_sheet_names.append(some_one_else_old_sheet_name)
        if new_sheet_name in someone_elses_old_sheet_names:
            oldest_sheet_name = f'{new_sheet_name}_{self._sheet_id}'
            self._sheet_id += 1
        else:
            oldest_sheet_name = self.get_sheet_name_to_pass_to_presenter(old_sheet_name)

        if oldest_sheet_name is None:
            self._sheet_name_dictionary[new_sheet_name] = new_sheet_name
        else:
            self._sheet_name_dictionary[new_sheet_name] = oldest_sheet_name
