import os_identifier

from .Observable import Observable
from .Observable import notify
from .. import Utilities


class Configurations(Observable):
    _default_nop = 10
    _default_bb_shift = -1
    _default_shape_position_increment_value = (0, 5)
    _default_move_shape_increment = (25, 25)
    _default_save_file_name = 'Excel'
    _default_delta = 10
    _default_font_size = 13 if os_identifier.is_mac else 10
    _default_account_width = 50
    _default_account_height = 20
    _default_operator_width = 50
    _default_operator_height = 20
    _default_slider_w = 25
    _default_slider_h = 200
    _default_slider_range_w = 40
    _default_slider_range_h = 20
    _default_slider_decimal_w = 40
    _default_slider_decimal_h = 20
    _default_slider_handle_h = 25
    _default_slider_range_dx = -60
    _default_graph_y_ax_w = 1
    _default_graph_y_ax_height = 200
    _default_graph_range_w = 40
    _default_graph_range_h = 20
    _default_graph_period_w = 40
    _default_graph_period_h = 20
    _default_graph_range_dx = -60
    _default_scale_x = 1
    _default_scale_y = 1
    _default_bb_width = 50
    _default_bb_height = 20
    _default_constant_width = 50
    _default_constant_height = 20
    _default_auto_fit_width_per_letter = 8
    _relay_x_to_right_end = 'right most'
    _relay_x_to_right = '_relay_x_to_right'

    _number_of_periods = 'nop'
    _bb_shift = 'bb_shift'
    _default_shape_position_increment = 'default_increment'
    _move_shape_increment = 'move_shape_increment'
    _save_file_name = '_save_file_name'
    _target_accounts_sensitivity = '_target_accounts_sensitivity'
    _variable_accounts_sensitivity = '_variable_accounts_sensitivity'
    _sensitivity_deltas = '_sensitivity_deltas'
    _insert_sheet_name_in_input_sheet = '_insert_sheet_name_in_input_sheet'
    _prevent_refresh_canvas = '_prevent_refresh_canvas'
    _default_command_file_name = 'Commands.xlsm'
    _clean_state_prior_to_save = 'clean_up_state_before_pickling_though_expensive'
    _live_calculation = 'live_calculation'
    _account_width = 'account width'
    _account_height = 'account height'
    _account_font_size = 'account font size'
    _operator_width = 'operator width'
    _operator_height = 'operator height'
    _operator_font_size = 'operator font size'
    _bb_width = 'bb width'
    _bb_height = 'bb height'
    _bb_font_size = 'bb font size'
    _constant_width = 'constant width'
    _constant_height = 'constant height'
    _constant_font_size = 'constant font size'
    _all_other_font_size = 'all other font size'
    _auto_fit_width_per_letter = '_auto_fit_width_per_letter'
    _slider_w = '_slider_w'
    _slider_h = '_slider_h'
    _slider_range_w = '_slider_range_w'
    _slider_range_h = '_slider_range_h'
    _slider_decimal_w = '_slider_decimal_w'
    _slider_decimal_h = '_slider_decimal_h'
    _slider_handle_h = '_slider_handle_h'
    _slider_range_dx = '_slider_range_dx'
    _graph_y_ax_w = '_graph_y_ax_w'
    _graph_y_ax_height = '_graph_y_ax_height'
    _graph_range_w = '_graph_range_w'
    _graph_range_h = '_graph_range_h'
    _graph_period_w = '_graph_period_w'
    _graph_period_h = '_graph_period_h'
    _graph_range_dx = '_graph_range_dx'
    _scale_x = '_scale_x'
    _scale_y = '_scale_y'
    _relay_x = '_relay_x'

    _copied_accounts = '_copied_accounts'

    def __init__(self):
        Observable.__init__(self)
        self._data = {self._number_of_periods: self._default_nop,
                      self._bb_shift: self._default_bb_shift,
                      self._default_shape_position_increment: self._default_shape_position_increment_value,
                      self._move_shape_increment: self._default_move_shape_increment,
                      self._save_file_name: self._default_save_file_name,
                      self._target_accounts_sensitivity: (),
                      self._variable_accounts_sensitivity: (),
                      self._sensitivity_deltas: {},
                      self._insert_sheet_name_in_input_sheet: False,
                      self._prevent_refresh_canvas: False,
                      self._clean_state_prior_to_save: True,
                      self._live_calculation: True,
                      self._account_width: self._default_account_width,
                      self._account_height: self._default_account_height,
                      self._account_font_size: self._default_font_size,
                      self._operator_width: self._default_operator_width,
                      self._operator_height: self._default_operator_height,
                      self._operator_font_size: self._default_font_size,
                      self._bb_width: self._default_bb_width,
                      self._bb_height: self._default_bb_height,
                      self._bb_font_size: self._default_font_size,
                      self._constant_width: self._default_constant_width,
                      self._constant_height: self._default_constant_height,
                      self._constant_font_size: self._default_font_size,
                      self._all_other_font_size: self._default_font_size,
                      self._auto_fit_width_per_letter: self._default_auto_fit_width_per_letter,
                      self._slider_w: self._default_slider_w,
                      self._slider_h: self._default_slider_h,
                      self._slider_range_w: self._default_slider_range_w,
                      self._slider_range_h: self._default_slider_range_h,
                      self._slider_decimal_w: self._default_slider_decimal_w,
                      self._slider_decimal_h: self._default_slider_decimal_h,
                      self._slider_handle_h: self._default_slider_handle_h,
                      self._slider_range_dx: self._default_slider_range_dx,
                      self._graph_y_ax_w: self._default_graph_y_ax_w,
                      self._graph_y_ax_height: self._default_graph_y_ax_height,
                      self._graph_range_w: self._default_graph_range_w,
                      self._graph_range_h: self._default_graph_range_h,
                      self._graph_period_w: self._default_graph_period_w,
                      self._graph_period_h: self._default_graph_period_h,
                      self._graph_range_dx: self._default_graph_range_dx,
                      self._scale_x: self._default_scale_x,
                      self._scale_y: self._default_scale_y,
                      self._relay_x: self._relay_x_to_right,

                      self._copied_accounts: tuple(),
                      }

    @property
    def number_of_periods(self) -> int:
        return self._data.get(self._number_of_periods, self._default_nop)

    @notify
    def set_number_of_periods(self, number_of_periods: int):
        self._data[self._number_of_periods] = number_of_periods

    @property
    def bb_shift(self) -> int:
        return self._data.get(self._bb_shift, self._default_bb_shift)

    @notify
    def set_bb_shift(self, bb_shift: int):
        self._data[self._bb_shift] = bb_shift

    @property
    def default_shape_position_increment(self) -> tuple:
        return self._data.get(self._default_shape_position_increment)

    @notify
    def set_default_shape_position_increment(self, x, y):
        self._data[self._default_shape_position_increment] = (x, y)

    @property
    def move_shape_increment(self) -> tuple:
        return self._data.get(self._move_shape_increment, self._default_move_shape_increment)

    @notify
    def set_move_shape_increment(self, x: int, y: int):
        self._data[self._move_shape_increment] = (x, y)

    # Save Setting
    @notify
    def set_save_file_name(self, file_name):
        self._data[self._save_file_name] = file_name

    @property
    def save_file_name(self):
        return self._data.get(self._save_file_name, self._default_save_file_name)

    def turn_on_insert_sheet_names_in_input_sheet(self):
        self._data[self._insert_sheet_name_in_input_sheet] = True

    def turn_off_insert_sheet_names_in_input_sheet(self):
        self._data[self._insert_sheet_name_in_input_sheet] = False

    @property
    def insert_sheet_name_in_input_sheet(self) -> bool:
        return self._data.get(self._insert_sheet_name_in_input_sheet, False)

    # Sensitivity Setting
    @property
    def command_file_name(self) -> str:
        return self._default_command_file_name

    def add_sensitivity_target_accounts(self, account_ids: tuple):
        for account_id in account_ids:
            self.add_sensitivity_target_account(account_id)

    @notify
    def add_sensitivity_target_account(self, account_id):
        if account_id not in self.sensitivity_target_accounts:
            self._data[self._target_accounts_sensitivity] += (account_id,)

    def remove_sensitivity_target_accounts(self, account_ids: tuple):
        for account_id in account_ids:
            self.remove_sensitivity_target_account(account_id)

    @notify
    def remove_sensitivity_target_account(self, account_id):
        existing_data = self.sensitivity_target_accounts
        new_data = Utilities.remove_item_from_tuple(existing_data, account_id)
        self.set_sensitivity_target_accounts(new_data)

    @notify
    def shift_multiple_sensitivity_target_accounts(self, indexes: tuple, shift: int):
        existing_data = self.sensitivity_target_accounts
        args = existing_data, indexes, shift
        destinations, new_data = Utilities.get_tuple_and_destinations_after_shifting_elements(*args)
        self.set_sensitivity_target_accounts(new_data)
        return tuple(destinations)

    @notify
    def set_sensitivity_target_accounts(self, data):
        self._data[self._target_accounts_sensitivity] = data

    @property
    def sensitivity_target_accounts(self) -> tuple:
        return self._data.get(self._target_accounts_sensitivity, ())

    def add_sensitivity_variable_accounts(self, account_ids: tuple):
        for account_id in account_ids:
            self.add_sensitivity_variable_account(account_id)

    @notify
    def add_sensitivity_variable_account(self, account_id, delta: int = None):
        delta = self._default_delta if delta is None else delta
        if account_id not in self.sensitivity_variable_accounts:
            self._data[self._variable_accounts_sensitivity] += (account_id,)
            self._data[self._sensitivity_deltas][account_id] = delta

    def remove_sensitivity_variable_accounts(self, account_ids: tuple):
        for account_id in account_ids:
            self.remove_sensitivity_variable_account(account_id)

    @notify
    def remove_sensitivity_variable_account(self, account_id):
        existing_data = self.sensitivity_variable_accounts
        new_data = Utilities.remove_item_from_tuple(existing_data, account_id)
        self.set_sensitivity_variable_accounts(new_data)
        self.remove_sensitivity_delta(account_id)

    @notify
    def set_sensitivity_variable_accounts(self, data):
        self._data[self._variable_accounts_sensitivity] = data

    @property
    def sensitivity_variable_accounts(self) -> tuple:
        return self._data.get(self._variable_accounts_sensitivity, ())

    def set_sensitivity_deltas(self, account_ids: tuple, delta: float):
        for account_id in account_ids:
            self.set_sensitivity_delta(account_id, delta)

    @notify
    def set_sensitivity_delta(self, account_id, delta: float):
        self._data[self._sensitivity_deltas][account_id] = delta

    def remove_sensitivity_delta(self, account_id):
        if account_id in self._data[self._sensitivity_deltas]:
            del self._data[self._sensitivity_deltas][account_id]

    def get_sensitivity_delta(self, account_id) -> int:
        if account_id in self._data[self._sensitivity_deltas]:
            return self._data[self._sensitivity_deltas][account_id]
        else:
            return self._default_delta

    def get_sensitivity_deltas(self, account_ids) -> tuple:
        return tuple(self.get_sensitivity_delta(ac) for ac in account_ids)

    def get_account_ids_to_deltas(self, account_ids) -> dict:
        return dict(zip(account_ids, self.get_sensitivity_deltas(account_ids)))

    @property
    def state_cleaner_is_activated(self) -> bool:
        return self._data.get(self._clean_state_prior_to_save, True)

    def activate_state_cleaner(self):
        self._data[self._clean_state_prior_to_save] = True

    def deactivate_state_cleaner(self):
        self._data[self._clean_state_prior_to_save] = False

    @property
    def live_calculation_is_activated(self) -> bool:
        return self._data.get(self._live_calculation, True)

    def activate_live_calculation(self):
        self._data[self._live_calculation] = True

    def deactivate_live_calculation(self):
        self._data[self._live_calculation] = False

    @property
    def auto_fit_width_per_letter(self):
        return self._data.get(self._auto_fit_width_per_letter, self._default_auto_fit_width_per_letter)

    def set_auto_fit_width_per_letter(self, value):
        self._data[self._auto_fit_width_per_letter] = value

    @property
    def account_width(self):
        return self._data.get(self._account_width, self._default_account_width)

    def set_account_width(self, value):
        self._data[self._account_width] = value

    @property
    def account_height(self):
        return self._data.get(self._account_height, self._default_account_height)

    def set_account_height(self, value):
        self._data[self._account_height] = value

    @property
    def account_font_size(self):
        return self._data.get(self._account_font_size, self._default_font_size)

    def set_account_font_size(self, value):
        self._data[self._account_font_size] = value

    @property
    def operator_width(self):
        return self._data.get(self._operator_width, self._default_operator_width)

    def set_operator_width(self, value):
        self._data[self._operator_width] = value

    @property
    def operator_height(self):
        return self._data.get(self._operator_height, self._default_operator_height)

    def set_operator_height(self, value):
        self._data[self._operator_height] = value

    @property
    def operator_font_size(self):
        return self._data.get(self._operator_font_size, self._default_font_size)

    def set_operator_font_size(self, value):
        self._data[self._operator_font_size] = value

    @property
    def bb_width(self):
        return self._data.get(self._bb_width, self._default_bb_width)

    def set_bb_width(self, value):
        self._data[self._bb_width] = value

    @property
    def bb_height(self):
        return self._data.get(self._bb_height, self._default_bb_height)

    def set_bb_height(self, value):
        self._data[self._bb_height] = value

    @property
    def bb_font_size(self):
        return self._data.get(self._bb_font_size, self._default_font_size)

    def set_bb_font_size(self, value):
        self._data[self._bb_font_size] = value

    @property
    def constant_width(self):
        return self._data.get(self._constant_width, self._default_constant_width)

    def set_constant_width(self, value):
        self._data[self._constant_width] = value

    @property
    def constant_height(self):
        return self._data.get(self._constant_height, self._default_constant_height)

    def set_constant_height(self, value):
        self._data[self._constant_height] = value

    @property
    def constant_font_size(self):
        return self._data.get(self._constant_font_size, self._default_font_size)

    def set_constant_font_size(self, value):
        self._data[self._constant_font_size] = value

    @property
    def all_other_font_size(self):
        return self._data.get(self._all_other_font_size, self._default_font_size)

    def set_all_other_font_size(self, value):
        self._data[self._all_other_font_size] = value

    @property
    def slider_w(self):
        return self._data.get(self._slider_w, self._default_slider_w)

    def set_slider_w(self, value):
        self._data[self._slider_w] = value

    @property
    def slider_h(self):
        return self._data.get(self._slider_h, self._default_slider_h)

    def set_slider_h(self, value):
        self._data[self._slider_h] = value

    @property
    def slider_range_w(self):
        return self._data.get(self._slider_range_w, self._default_slider_range_w)

    def set_slider_range_w(self, value):
        self._data[self._slider_range_w] = value

    @property
    def slider_range_h(self):
        return self._data.get(self._slider_range_h, self._default_slider_range_h)

    def set_slider_range_h(self, value):
        self._data[self._slider_range_h] = value

    @property
    def slider_decimal_w(self):
        return self._data.get(self._slider_decimal_w, self._default_slider_decimal_w)

    def set_slider_decimal_w(self, value):
        self._data[self._slider_decimal_w] = value

    @property
    def slider_decimal_h(self):
        return self._data.get(self._slider_decimal_h, self._default_slider_decimal_h)

    def set_slider_decimal_h(self, value):
        self._data[self._slider_decimal_h] = value

    @property
    def slider_handle_h(self):
        return self._data.get(self._slider_handle_h, self._default_slider_handle_h)

    def set_slider_handle_h(self, value):
        self._data[self._slider_handle_h] = value

    @property
    def slider_range_dx(self):
        return self._data.get(self._slider_range_dx, self._default_slider_range_dx)

    def set_slider_range_dx(self, value):
        self._data[self._slider_range_dx] = value

    @property
    def graph_y_ax_w(self):
        return self._data.get(self._graph_y_ax_w, self._default_graph_y_ax_w)

    def set_graph_y_ax_w(self, value):
        self._data[self._graph_y_ax_w] = value

    @property
    def graph_y_ax_height(self):
        return self._data.get(self._graph_y_ax_height, self._default_graph_y_ax_height)

    def set_graph_y_ax_height(self, value):
        self._data[self._graph_y_ax_height] = value

    @property
    def graph_range_w(self):
        return self._data.get(self._graph_range_w, self._default_graph_range_w)

    def set_graph_range_w(self, value):
        self._data[self._graph_range_w] = value

    @property
    def graph_range_h(self):
        return self._data.get(self._graph_range_h, self._default_graph_range_h)

    def set_graph_range_h(self, value):
        self._data[self._graph_range_h] = value

    @property
    def graph_period_w(self):
        return self._data.get(self._graph_period_w, self._default_graph_period_w)

    def set_graph_period_w(self, value):
        self._data[self._graph_period_w] = value

    @property
    def graph_period_h(self):
        return self._data.get(self._graph_period_h, self._default_graph_period_h)

    def set_graph_period_h(self, value):
        self._data[self._graph_period_h] = value

    @property
    def graph_range_dx(self):
        return self._data.get(self._graph_range_dx, self._default_graph_range_dx)

    def set_graph_range_dx(self, value):
        self._data[self._graph_range_dx] = value

    @property
    def scale_x(self):
        return self._data.get(self._scale_x, self._default_scale_x)

    def set_scale_x(self, value):
        self._data[self._scale_x] = value

    @property
    def scale_y(self):
        return self._data.get(self._scale_y, self._default_scale_y)

    def set_scale_y(self, value):
        self._data[self._scale_y] = value

    @property
    def relay_x_position(self) -> str:
        return self._data.get(self._relay_x, self._relay_x_to_right_end)

    def set_relay_x_to_right(self):
        value = self._relay_x_to_right
        self._set_relay_x(value)

    def set_relay_x_to_right_end(self):
        value = self._relay_x_to_right_end
        self._set_relay_x(value)

    def _set_relay_x(self, value):
        self._data[self._relay_x] = value

    @property
    def relay_to_be_placed_at_right_end(self) -> bool:
        return self.relay_x_position == self._relay_x_to_right_end

    @property
    def relay_to_be_placed_to_right(self) -> bool:
        return self.relay_x_position == self._relay_x_to_right

    @property
    def copied_accounts(self) -> tuple:
        return self._data.get(self._copied_accounts, ())

    def set_copied_accounts(self, accounts: tuple):
        self._data[self._copied_accounts] = accounts

    def clear_copied_accounts(self):
        self.data[self._copied_accounts] = tuple()
