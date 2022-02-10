import copy
import os
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Type
from typing import Union

from interface_fm import BoundaryInABC
from interface_fm_calculator import CalculatorABC
from interface_keymaps import KeyMapABC
from interface_keymaps import KeyMapsABC
from interface_spreadsheet import SpreadsheetABC
from interface_udf_builder import UDFBuilderABC

from . import caching
from . import graph
from . import implementation_5 as imp5
from . import implementation_9 as imp9
from . import live_value
from . import rpe
from . import selection as sel
from . import slider
from . import spotlight
from . import vba_udf
from .cache import Cache
from .load_config import LoadConfiguration
from .states_and_flags import StatesAndFlags
from .. import RequestModel
from .. import ResponseModel
from .. import Utilities
from ..Entities import Entities
from ..Entities import Observable
from ..EntityGateway import GateWayABC
from ..Presenter import PresentersABC
from ..Utilities.Memento import Memento


class Interactor(BoundaryInABC):

    def __init__(self, entities: Entities, presenters: PresentersABC, gateways: GateWayABC = None):
        self._set_entities(entities)
        self._gateways = gateways
        self._presenters = presenters

        gateways.attach_to_notification(self._present_feedback_user)

        self._sf = StatesAndFlags()
        self._load_config = LoadConfiguration()
        self._cache = Cache()

        # Plug-ins
        self._spreadsheet: Union[None, SpreadsheetABC] = None
        self._vba_udf_builder: Union[None, UDFBuilderABC] = None
        self._calculator: Union[None, CalculatorABC] = None
        self._keymaps: Union[None, KeyMapsABC] = None
        self._canvas_image_saver: Union[None, Callable] = None

    def setup(self):
        self.add_new_worksheet('Sheet1')
        self._present_connection_ids()

        last_load_config_data = self.get_pickle_from_file_system(self._load_config.config_file_path)
        if last_load_config_data is None:
            self._gateways.create_load_config_folder(self._load_config.folder_name, 'Documents')
        else:
            self._load_config.restore(last_load_config_data)
            path = self._load_config.last_project_path
            if path is not None:
                data = self.get_pickle_from_file_system(self._load_config.config_file_path)
                self._load_config.restore(data)
                self.set_project_folder_path(path)

        self.save_state_to_memory()

    def tear_down(self):
        self._load_config.save_last_state(self.current_state)
        data = self._load_config.load_config_data
        self.save_any_data_as_pickle(self._load_config.config_file_path, data)

    def tear_down_setup(self):
        # Remove chain of undo / redo states to make the system run fast.
        self.tear_down()
        self.reset()
        self.setup()

    @property
    def account_width(self):
        return self._configurations.account_width

    def set_account_width(self, value: int):
        self._configurations.set_account_width(value)

    @property
    def account_height(self):
        return self._configurations.account_height

    def set_account_height(self, value: int):
        self._configurations.set_account_height(value)

    @property
    def account_font_size(self):
        return self._configurations.account_font_size

    def set_account_font_size(self, value: int):
        self._configurations.set_account_font_size(value)

    @property
    def operator_width(self):
        return self._configurations.operator_width

    def set_operator_width(self, value: int):
        self._configurations.set_operator_width(value)

    @property
    def operator_height(self):
        return self._configurations.operator_height

    def set_operator_height(self, value: int):
        self._configurations.set_operator_height(value)

    @property
    def operator_font_size(self):
        return self._configurations.operator_font_size

    def set_operator_font_size(self, value: int):
        self._configurations.set_operator_font_size(value)

    @property
    def constant_width(self):
        return self._configurations.constant_width

    def set_constant_width(self, value: int):
        self._configurations.set_constant_width(value)

    @property
    def constant_height(self):
        return self._configurations.constant_height

    def set_constant_height(self, value: int):
        self._configurations.set_constant_height(value)

    @property
    def constant_font_size(self):
        return self._configurations.constant_font_size

    def set_constant_font_size(self, value: int):
        self._configurations.set_constant_font_size(value)

    @property
    def bb_width(self):
        return self._configurations.bb_width

    def set_bb_width(self, value: int):
        self._configurations.set_bb_width(value)

    @property
    def bb_height(self):
        return self._configurations.bb_height

    def set_bb_height(self, value: int):
        self._configurations.set_bb_height(value)

    @property
    def bb_font_size(self):
        return self._configurations.bb_font_size

    def set_bb_font_size(self, value: int):
        self._configurations.set_bb_font_size(value)

    @property
    def recent_project_paths(self) -> tuple:
        return tuple(self._load_config.recent_project_paths)

    @property
    def entities(self) -> Entities:
        return self._entities

    @property
    def _selection(self):
        return self._entities.selection

    @property
    def _account_order(self):
        return self._entities.account_order

    @property
    def selection(self):
        return self._selection

    @property
    def account_order(self):
        return self._account_order

    @property
    def sheet_contents(self) -> tuple:
        return self._worksheets.selected_sheet_contents

    @property
    def selected_account_names(self) -> tuple:
        return self._get_texts_of_shapes(self.selected_accounts)

    @property
    def first_selected_text(self) -> str:
        selection = tuple(self.selection.data)
        return self._shapes.get_text(selection[0]) if len(selection) > 0 else ''

    @property
    def copied_account_names(self) -> tuple:
        return self._get_texts_of_shapes(self._sf.copied_accounts)

    @property
    def input_accounts(self) -> tuple:
        return imp9.get_input_accounts(self._connections, self._shapes)

    def _get_texts_of_shapes(self, shape_ids: Iterable) -> tuple:
        return tuple(self._shapes.get_text(shape_id) for shape_id in shape_ids)

    @property
    def input_names(self) -> tuple:
        return self._get_texts_of_shapes(self.input_accounts)

    def display_pickle(self, pickle_name: str):
        original_entities = self._entities
        temporary_entities = Entities()
        self._gateways.restore_state(temporary_entities, pickle_name)
        self._set_entities(temporary_entities)

        # Part of refresh canvas
        self._present_clear_canvas()
        self._present_add_shape(self.sheet_contents)
        self._present_connect_shapes()
        self._present_highlight_automatic()

        self._set_entities(original_entities)

    # Configuration
    def set_project_folder_path(self, path):
        if Utilities.is_directory(path):
            self._load_config.set_opening_project(path)
            self._gateways.set_project_folder(path)
            self.set_save_path(path)

            last_state = self._load_config.last_state
            if last_state is not None:
                memento = Memento(last_state)
                self.load_memento(memento)
            self._present_feedback_user(f'Project folder set to {path}.', 'success')
        else:
            self._present_feedback_user(f'Invalid path! {path}.', 'error')

    def create_project_folder(self, path):
        feedback = self._gateways.create_project_folder(path)
        if feedback == 'success':
            self._gateways.embed_resources_to_project_folder(path)
            self.set_project_folder_path(path)

    def clear_project_history(self):
        self._load_config.clear()
        self._present_feedback_user('Project history cleared.', 'success')

    @property
    def project_folder(self):
        return self._load_config.opening_project

    @property
    def clean_state_prior_to_save(self) -> bool:
        return self._configurations.state_cleaner_is_activated

    def activate_state_cleaner(self):
        self._configurations.activate_state_cleaner()
        self._present_feedback_user('State Cleaner activated. State will be cleaned upon save.', 'success')

    def deactivate_state_cleaner(self):
        self._configurations.deactivate_state_cleaner()
        self._present_feedback_user('State Cleaner deactivated.', 'success')

    def activate_live_calculation(self):
        self._configurations.activate_live_calculation()
        self._update_graph_bars_and_live_values()
        self._present_feedback_user('Live Calculation activated. Calculation will be done upon slider.', 'success')

    def deactivate_live_calculation(self):
        self._configurations.deactivate_live_calculation()
        self._present_feedback_user('Live Calculation deactivated.', 'success')

    @property
    def is_live_calculation_mode(self) -> bool:
        return self._configurations.live_calculation_is_activated

    @staticmethod
    def is_debug_mode() -> bool:
        return Observable.is_debug_mode

    def stop_canvas_refreshing(self):
        self._sf.set_prevent_refresh_canvas(True)

    def start_canvas_refreshing(self):
        self._sf.set_prevent_refresh_canvas(False)

    @property
    def prevent_refresh_canvas(self) -> bool:
        return self._sf.prevent_refresh_canvas

    @property
    def _increment_x_y(self) -> tuple:
        return self._configurations.default_shape_position_increment

    @property
    def move_shape_increment(self) -> tuple:
        return self._configurations.move_shape_increment

    @property
    def _bb_shift(self) -> int:
        return self._configurations.bb_shift

    @property
    def number_of_periods(self) -> int:
        return self._configurations.number_of_periods

    def set_default_increment(self, x, y):
        self._configurations.set_default_shape_position_increment(x, y)

    def set_move_shape_increment(self, x: int, y: int):
        self._configurations.set_move_shape_increment(x, y)

    def set_bb_shift(self, shift):
        self._configurations.set_bb_shift(shift)

    def set_number_of_periods(self, number_of_periods: int):
        self._configurations.set_number_of_periods(number_of_periods)
        self._input_values.change_number_of_periods(number_of_periods)
        for input_account in self.input_accounts:
            if 'period' in self._connection_ids.get_connection_ids(input_account):
                period_account = input_account
                self.set_input_values(period_account, tuple(range(number_of_periods)))
        self._present_feedback_user(f'Number of periods set to {number_of_periods}')

    def set_save_file_name(self, file_name):
        self._entities.configurations.set_save_file_name(file_name)

    @property
    def save_file_name(self):
        return self._entities.configurations.save_file_name

    def set_save_path(self, folder_path):
        self._load_config.set_opening_project(folder_path)

    # Configuration - Export Excel Setting
    def turn_on_insert_sheet_names_in_input_sheet(self):
        self._configurations.turn_on_insert_sheet_names_in_input_sheet()
        self.present_insert_worksheet_in_input_sheet_mode()

    def turn_off_insert_sheet_names_in_input_sheet(self):
        self._configurations.turn_off_insert_sheet_names_in_input_sheet()
        self.present_insert_worksheet_in_input_sheet_mode()

    def add_sensitivity_target_account(self, account_id):
        # For macro (easier to set account_id as argument than tuple account_ids)
        self.add_sensitivity_target_accounts((account_id,))

    def add_sensitivity_target_accounts(self, account_ids: tuple):
        self._configurations.add_sensitivity_target_accounts(account_ids)

    def remove_sensitivity_target_accounts(self, account_ids: tuple):
        self._configurations.remove_sensitivity_target_accounts(account_ids)

    def shift_multiple_sensitivity_target_account(self, indexes, shift: int) -> tuple:
        destinations = self._configurations.shift_multiple_sensitivity_target_accounts(indexes, shift)
        return destinations

    def add_sensitivity_variable_account(self, account_id):
        # For macro (easier to set account_id as argument than tuple account_ids)
        self.add_sensitivity_variable_accounts((account_id,))

    def add_sensitivity_variable_accounts(self, account_ids: tuple):
        self._configurations.add_sensitivity_variable_accounts(account_ids)

    def remove_sensitivity_variable_accounts(self, account_ids: tuple):
        self._configurations.remove_sensitivity_variable_accounts(account_ids)

    def set_sensitivity_delta(self, account_id, delta: float):
        # For macro (easier to set account_id as argument than tuple account_ids)
        self.set_sensitivity_deltas((account_id,), delta)

    def set_sensitivity_deltas(self, account_ids: tuple, delta: float):
        self._configurations.set_sensitivity_deltas(account_ids, delta)

    @property
    def save_path(self):
        return self._load_config.opening_project or Utilities.desktop

    @property
    def pickle_path(self):
        return self._gateways.path_pickles

    def do_nothing(self, *_, **__):
        pass

    @property
    def sensitivity_sheet_added(self) -> bool:
        return len(self._configurations.sensitivity_target_accounts) > 0

    # Entry / Exit points
    def set_entry_point(self, entry_by: str = None, request: dict = None, ):
        self.save_state_to_memory()
        if request is not None:
            entry_by = request['entry_by']
            if entry_by == 'mouse':
                self._cache.set_connections_filtered(self.connections_filtered)
        self._sf.set_entry_by(entry_by)
        self._sf.set_previous_commands_to_previous_previous_commands()

    def exit_point(self, exit_by: str = None, request: dict = None):
        if request is not None:
            exit_by = request['exit_by']
        if exit_by in self._sf.entry_by:
            self._sf.remove_entry_by(exit_by)
        self._sf.clear_initial_shape_position()

        if self._sf.previous_commands_are_not_set:
            self._sf.set_previous_commands(self._sf.previous_previous_commands)
        if exit_by == 'mouse':
            self._cache.clear_connections_filtered()
            self._upon_selection(self._selection.data)

    def set_previous_command(self, f: Callable, args: tuple, kwargs: dict):
        self._sf.append_previous_commands((f, args, kwargs))

    def execute_previous_command(self):
        feedback = ''
        for f, args, kwargs in self._sf.previous_commands:
            f(*args, **kwargs)
            feedback += f'{f.__name__}({args},{kwargs}), '
        self.feedback_user(f'Invoked previous actions {feedback}')

    def upon_exception(self, *args, **kwargs):
        exception = args[1]
        self._present_feedback_user(exception.__repr__(), 'error')

        if self._sf.entry_by_template_tree:
            self._present_clear_canvas()
        self._sf.clear_entry_by()
        # raise exception

    @property
    def entry_by_mouse(self) -> bool:
        return self._sf.entry_by_mouse

    # Input Entry
    def set_input_y_range(self, y_range: tuple):
        self._set_input_y_range(self._sf.input_being_modified, y_range)

    def _set_input_y_range(self, input_account, y_range):
        self._input_ranges.set_range(input_account, y_range)

    def get_input_y_range(self, input_account) -> tuple:
        y_range = self._input_ranges.get_ranges(input_account)
        if y_range is None:
            values = self._input_values.get_values(input_account)
            y_range = min(values), max(values)
        return y_range

    def get_input_decimals(self, input_account) -> int:
        return self._input_decimals.get_decimals(input_account)

    def _set_input_being_modified(self, input_account):
        self._sf.set_input_being_modified(input_account)

    def clear_input_being_modified(self):
        self._sf.clear_input_being_modified()

    @property
    def input_being_modified(self):
        return self._sf.input_being_modified

    def set_default_input_values_if_values_not_set(self):
        input_accounts = self.input_accounts
        for input_account in input_accounts:
            if self._input_values.values_are_not_set(input_account):
                self._input_values.set_default_values(input_account, self.number_of_periods)

    def update_input_entry(self):
        input_account = self._sf.input_being_modified
        if input_account is not None:
            self._update_input_entry(input_account)
        else:
            self.update_input_entry_upon_launch()

    def update_input_entry_upon_launch(self):
        self.set_default_input_values_if_values_not_set()
        input_accounts = self._get_sorted_input_accounts()
        input_account = imp9.select_input_account_to_edit(input_accounts, self._selection.data)

        if input_account is not None:
            self._update_input_entry(input_account)

    def show_next_input(self):
        self._change_input_to_modify(1)

    def show_previous_input(self):
        self._change_input_to_modify(-1)

    def show_specified_input(self, input_id):
        self._change_input_to_modify_by_input_id(input_id)

    def _change_input_to_modify(self, shift: int):
        args = self._sf.input_being_modified, shift, self._get_sorted_input_accounts()
        next_input = imp9.get_next_input_to_edit(*args)
        self._change_input_to_modify_by_input_id(next_input)

    def _change_input_to_modify_by_input_id(self, input_id):
        self._update_input_entry(input_id)
        self._set_input_being_modified(input_id)

    def _get_sorted_input_accounts(self):
        input_accounts_unsorted = self.input_accounts
        input_accounts = imp9.sort_by_account_order(input_accounts_unsorted, self._account_orders, self._worksheets)
        return input_accounts

    def set_values_to_input_being_modified(self, values: tuple):
        input_account = self._sf.input_being_modified
        if input_account is not None:
            self.set_input_values(input_account, values)

    def set_decimals_to_input_being_modified(self, decimals: int):
        input_account = self._sf.input_being_modified
        if input_account is not None:
            self.set_input_decimals(input_account, decimals)

    def set_input_values(self, input_account, values: tuple):
        self._input_values.set_values(input_account, values)

    def set_input_decimals(self, input_account, decimals: int):
        self._input_decimals.set_decimals(input_account, decimals)

    def set_same_input_values(self, input_account, value: float):
        values = tuple(value for _ in range(self.number_of_periods))
        self._input_values.set_values(input_account, values)

    def _update_input_entry(self, input_account):
        input_text = self._shapes.get_text(input_account)
        input_values = self._input_values.get_values(input_account)
        y_range = self.get_input_y_range(input_account)
        decimals = self.get_input_decimals(input_account)
        uom = self._unit_of_measure.get_unit_of_measure(input_account)

        response_model = ResponseModel.response_model_to_presenter_show_input_entry
        args = input_text, input_values, self.number_of_periods, y_range, decimals, input_account, uom
        self._presenters.show_input_entry(response_model(*args))
        self._set_input_being_modified(input_account)

    # Size
    def decrease_width_of_selected_shapes(self):
        self.change_widths(-10, self.selection_except_blanks)

    def increase_width_of_selected_shapes(self):
        self.change_widths(10, self.selection_except_blanks)

    def change_widths(self, delta, shape_ids: Iterable):
        for shape_id in shape_ids:
            self._shapes.set_width(shape_id, self._shapes.get_width(shape_id) + delta)
        self.present_refresh_canvas()

    def match_selected_shapes_width(self):
        self.match_shapes_width(self.selection_except_blanks)

    def match_shapes_width(self, shape_ids: Iterable):
        if shape_ids:
            max_width = max(tuple(self._shapes.get_width(shape_id) for shape_id in shape_ids))
            for shape_id in shape_ids:
                self._shapes.set_width(shape_id, max_width)
            self.present_refresh_canvas()

    def fit_selected_shapes_width(self):
        self.fit_shapes_width(self.selection_except_blanks)

    def fit_all_shapes_width(self):
        self.fit_shapes_width(self._shapes.shapes_ids)

    def fit_shapes_width(self, shape_ids: Iterable):
        for shape_id in shape_ids:
            text = self._shapes.get_text(shape_id)
            try:
                self._shapes.set_width(shape_id, len(text) * 8)
            except TypeError:
                pass  # if shape_id is constant
        self.present_refresh_canvas()

    # Worksheets
    def add_new_worksheet(self, sheet_name: str = None):
        previous_sheet_state = copy.deepcopy((self._worksheets.sheet_names, self._worksheets.selected_sheet))
        self._entities.add_new_worksheet(sheet_name)
        self.upon_updating_worksheets(previous_sheet_state)

    def select_worksheet(self, sheet_name: str):
        previous_sheet_state = copy.deepcopy((self._worksheets.sheet_names, self._worksheets.selected_sheet))
        self._worksheets.select_sheet(sheet_name)
        self.upon_updating_worksheets(previous_sheet_state)

    def delete_selected_worksheet(self):
        if len(self._worksheets.sheet_names) == 1:
            self._present_feedback_user('There has to be at lease one worksheet.', 'error')
            return

        previous_sheet_state = copy.deepcopy((self._worksheets.sheet_names, self._worksheets.selected_sheet))
        self.erase_shapes_by_shape_ids(self.sheet_contents)
        self._entities.delete_selected_sheet()
        self.upon_updating_worksheets(previous_sheet_state)

    def delete_empty_worksheets(self):
        for sheet_name in self._worksheets.sheet_names:
            if self._worksheets.is_empty(sheet_name):
                self._worksheets.select_sheet(sheet_name)
                self.delete_selected_worksheet()

    def change_selected_sheet_name(self, sheet_name: str):
        new_sheet_name = sheet_name
        if sheet_name in self._worksheets.sheet_names:
            self.add_shapes_to_selection(self.sheet_contents)
            self.set_worksheet_to_selected_shapes_properties(new_sheet_name)
            self.delete_selected_worksheet()
        else:
            self._entities.change_selected_sheet_name(new_sheet_name)
            self.select_worksheet(new_sheet_name)

    def upon_updating_worksheets(self, previous_sheet_state: tuple):
        current_state = (self._worksheets.sheet_names, self._worksheets.selected_sheet)
        if previous_sheet_state != current_state:
            self._present_update_account_order()
            self.present_refresh_canvas()

    def present_update_worksheets(self):
        ws = self._worksheets
        response_model = ResponseModel.response_model_to_presenter_worksheets
        self._presenters.update_worksheets(response_model(tuple(ws.sheet_names), ws.selected_sheet))

    # Copy / Paste Accounts
    def copy_accounts(self):
        self._sf.set_copied_accounts(self.selected_accounts)

    def paste_accounts(self):
        self.add_relay_by_shape_ids(self._sf.copied_accounts)
        self._sf.clear_copied_accounts()

    # Selecting
    @property
    def selected_accounts(self) -> tuple:
        return sel.get_selected_accounts(self._selection.data, self._shapes)

    def select_all_in_the_sheet(self):
        self.add_shapes_to_selection(self.sheet_contents)

    def select_account_by_name(self, account_name, sheet_name: str = None, nth: int = 0):
        initial_selections = tuple(self.selection.data)
        shape_id_to_select = self.get_shape_id_by_name(account_name, sheet_name, nth)
        if shape_id_to_select is not None:
            self._selection.select_shape(shape_id_to_select)
            self._upon_selection((shape_id_to_select,) + initial_selections)

    def get_shape_id_by_name(self, account_name, sheet_name, nth):
        args = account_name, sheet_name, self.sheet_contents, self._shapes, self._worksheets
        candidates = imp9.get_accounts_that_match_name(*args)
        if len(candidates) == 0:
            self._present_feedback_user(f'{account_name} does not exist in sheet:{sheet_name}.')
            return None
        try:
            shape_id_to_select = candidates[nth]
        except IndexError:
            shape_id_to_select = candidates[0]
        return shape_id_to_select

    @property
    def selection_except_blanks(self) -> tuple:
        return tuple(s for s in self._selection.data if str(s) != 'blank')

    def get_shape_at_coordinate(self, x, y):
        return imp9.get_shape_id_at_mouse_point(self._shapes, {'x': x, 'y': y}, self.sheet_contents)

    def select_shape_at_x_y(self, request: dict):
        initial_selections = tuple(self._selection.data)
        shape_at_the_coordinate = imp9.get_shape_id_at_mouse_point(self._shapes, request, self.sheet_contents)
        shape_is_selected = self._selection.is_selected(shape_at_the_coordinate)
        if shape_at_the_coordinate is None:
            self._selection.clear_selection()
            self._upon_selection(initial_selections)
        elif not shape_is_selected:
            self._selection.select_shape(shape_at_the_coordinate)
            self._upon_selection((shape_at_the_coordinate,) + initial_selections)
        else:
            self._selection.add_selection(shape_at_the_coordinate)
            self._upon_selection((shape_at_the_coordinate,))

    def add_shape_at_x_y_to_selection(self, request: dict):
        shape_at_the_coordinate = imp9.get_shape_id_at_mouse_point(self._shapes, request, self.sheet_contents)
        if shape_at_the_coordinate is not None:
            self._selection.add_selection(shape_at_the_coordinate)
            self._upon_selection((shape_at_the_coordinate,))

    def select_shape_by_account_orders(self, account_orders, prevent_circularity=False):
        initial_selections = tuple(self.selection.data)
        shape_ids_with_blank = tuple(self._account_order.get_element(account_order) for account_order in account_orders)
        self.add_shapes_to_selection(shape_ids_with_blank)
        self._upon_selection(shape_ids_with_blank + initial_selections)

    def select_shape_by_account_order(self, account_order):
        initial_selections = tuple(self._selection.data)
        shape_id = self._account_order.get_element(account_order)
        if str(shape_id) == 'blank':
            self.clear_selection()
        self._selection.select_shape(shape_id)
        self._upon_selection((shape_id,) + initial_selections)

    def select_shape_by_shape_id(self, shape_id=None):
        if shape_id is not None:
            self._selection.select_shape(shape_id)
            self._upon_selection((shape_id,))

    def _select_shape_by_shape_id(self, shape_id):
        if shape_id is None:
            return
        self._selection.select_shape(shape_id)
        self._upon_selection((shape_id,))

    def _upon_selection(self, shape_ids: Iterable = None):
        self._present_highlight_automatic(shape_ids)
        if not self.entry_by_mouse:
            # Do there just one at the end when click is released
            self._present_update_account_order()
            self._present_shape_properties()
            self._present_connection_ids()
            self.feedback_selection()
            self._present_connect_shapes()

    def remove_selections_by_shape_ids(self, shape_ids):
        request_model = RequestModel.request_model_select_shape
        self.unselect_shapes([request_model(shape_id) for shape_id in shape_ids])
        self.feedback_selection()

    def add_shapes_in_range_to_selection(self, request: dict):
        shapes_in_rectangle = imp9.get_shape_ids_within_rectangle(request, self._shapes, self.sheet_contents)
        shapes_to_select = set(shapes_in_rectangle) - self._selection.data
        if len(shapes_to_select) == 0:
            return
        self.add_shapes_to_selection(shapes_to_select)

    def select_shapes_in_range(self, request: dict):
        initial_selections = tuple(self._selection.data)
        shapes_to_select = imp9.get_shape_ids_within_rectangle(request, self._shapes, self.sheet_contents)
        self._selection.select_shapes_by_shape_ids(shapes_to_select)
        self._upon_selection(initial_selections + shapes_to_select)

    def unselect_shape_in_range(self, request: dict):
        current_selections: set = self._selection.data
        shapes_in_range = imp9.get_shape_ids_within_rectangle(request, self._shapes, self.sheet_contents)
        shape_ids = current_selections - set(shapes_in_range)
        self.add_shapes_to_selection(shape_ids)

    def add_shapes_to_selection(self, shape_ids: Iterable):
        self._selection.add_selections_by_shape_ids(shape_ids)
        self._upon_selection(shape_ids)

    def unselect_shape_at_x_y(self, request: dict):
        x, y = request['x'], request['y']
        shape_id_under_mouse = self._shapes.get_shape_id_at_the_coordinate(x, y, self.sheet_contents)
        if shape_id_under_mouse is not None:
            self._selection.unselect_shape(shape_id_under_mouse)
        self._upon_selection((shape_id_under_mouse,))

    def unselect_shapes(self, request_models: Iterable):
        self._selection.unselect_shapes(request_models)

    def clear_selection(self):
        self._selection.clear_selection()
        self._upon_selection()

    def feedback_selection(self):
        shapes = self._shapes
        worksheets = self._worksheets
        connections = self._connections
        selected_set = set(d for d in self._selection.data if d in self.sheet_contents)
        feedback = f'Selection = {selected_set}.'
        if len(selected_set) == 1:
            shape_id = tuple(selected_set)[0]
            if shapes.get_tag_type(shape_id) == 'relay':
                feedback = imp9.get_original_account_of_relay_str(feedback, shape_id, shapes, worksheets)
            elif self.shape_is_depended_by_external_sheet(shape_id):
                feedback = imp9.get_dependants_str(shape_id, connections, shapes, worksheets)
        self.feedback_user(feedback)

    # Moving
    def move_selections_one_direction(self, request: dict):
        if len(self._selection.data) == 0:
            return
        if self._sf.initial_shape_position_is_not_set:
            self._set_initial_positions(request)

        initial_x, initial_y, shape_x, shape_y = self._get_initial_positions()
        if initial_x is None:
            return

        delta_x, delta_y = imp9.move_shapes_to_one_direction_algorithm(initial_x, initial_y, request, shape_x, shape_y)
        self.move_selections(delta_x, delta_y)

    def move_selections_one_direction_and_evenly_distribute(self, request: dict):
        if len(self._selection.data) == 0:
            return
        if self._sf.initial_shape_position_is_not_set:
            self._set_initial_positions(request)

        initial_x, initial_y, shape_x, shape_y = self._get_initial_positions()
        if initial_x is None:
            return

        delta_x, delta_y = imp9.move_shapes_to_one_direction_algorithm(initial_x, initial_y, request, shape_x, shape_y)
        shape_id = self._shapes.get_shape_id_at_the_coordinate(request['x'], request['y'], tuple(self._selection.data))
        if shape_id is not None:
            self._move_shapes_by_delta_xy(delta_x, delta_y, (shape_id,))
        if delta_x not in (0, None):
            self.evenly_distribute_horizontally()
        if delta_y not in (0, None):
            self.evenly_distribute_vertically()

    def _set_initial_positions(self, request):
        shape_id = imp9.get_shape_id_at_mouse_point(self._shapes, request, self.sheet_contents)
        if shape_id is None:
            self._sf.clear_initial_shape_position()
            return

        shape_x, shape_y = self._shapes.get_x(shape_id), self._shapes.get_y(shape_id)
        self._sf.set_initial_shape_position(shape_id, shape_x, shape_y)

    def _get_initial_positions(self) -> tuple:
        if self._sf.initial_shape_position_is_not_set:
            return None, None, None, None
        shape_id, initial_x, initial_y = self._sf.initial_shape_position
        shape_x, shape_y = self._shapes.get_x(shape_id), self._shapes.get_y(shape_id)
        return initial_x, initial_y, shape_x, shape_y

    def move_selections(self, delta_x=None, delta_y=None, request: dict = None):
        shapes = self._shapes
        shape_ids = self.selection_except_blanks
        if len(shape_ids) == 0:
            return
        if request:
            delta_x, delta_y = request['delta_x'], request['delta_y']
        delta_x, delta_y = imp9.prevent_any_shapes_from_entering_negative_x_y_area(delta_x, delta_y, shape_ids, shapes)
        if delta_x == 0 and delta_y == 0:
            return

        graph_items, handle_ids, slider_items = imp5.get_special_shapes_when_moving(shape_ids, shapes)
        if handle_ids:
            self.slide_handle_ids(handle_ids, delta_x, delta_y)
        else:
            shape_ids = slider.drag_slider_items(slider_items, shape_ids, shapes, self._connections)
            shape_ids = graph.drag_graph_items(graph_items, shape_ids, shapes, self._connections)
            self._move_shapes_by_delta_xy(delta_x, delta_y, shape_ids)

    def slide_handle_ids(self, handle_ids: tuple, dx, dy):
        slider.update_gauges_values(handle_ids, self._shapes, self._connections, self._input_decimals)

        args = self._shapes, self._connections, self._input_ranges, self._input_decimals, self.set_same_input_values
        slider.update_inputs_values(handle_ids, *args)

        self.update_data_table_upon_slider_action(handle_ids)

        dx, dy = slider.restrict_handle_move_range(handle_ids, dx, dy, self._shapes, self._connections)
        shape_ids = slider.drag_gauges_with_handles(handle_ids, handle_ids, self._connections)
        imp9.move_shapes(dx, dy, shape_ids, self._shapes)

        self._present_move_shapes(shape_ids, dx, dy)

    def _move_shapes_by_delta_xy(self, delta_x, delta_y, shape_ids: tuple):
        imp9.move_shapes(delta_x, delta_y, shape_ids, self._shapes)
        self._present_move_shapes(shape_ids, delta_x, delta_y)
        self._present_shape_properties()
        self._present_connection_ids()
        self._present_connect_shapes()

    def move_selections_to(self, x: int, y: int):
        accounts = self.selection.data

        left_shape_id = self._shapes.get_left_most_shape_id(accounts)
        top_shape_id = self._shapes.get_top_shape_id(accounts)
        x_current = self._shapes.get_x(left_shape_id)
        y_current = self._shapes.get_y(top_shape_id)
        delta_x = x - x_current
        delta_y = y - y_current

        self.move_selections(delta_x, delta_y)

    def _present_move_shapes(self, shape_ids: Iterable, delta_x, delta_y):
        response_model = ResponseModel.response_model_to_presenter_move_shapes
        self._presenters.move_shapes(response_model(shape_ids, delta_x, delta_y, self._shapes.data))

    def align_left(self):
        self._shapes.align_shapes_to_left(self.selection_except_blanks)
        self.present_refresh_canvas()

    def align_right(self):
        self._shapes.align_shapes_to_right(self.selection_except_blanks)
        self.present_refresh_canvas()

    def align_top(self):
        self._shapes.align_shapes_to_top(self.selection_except_blanks)
        self.present_refresh_canvas()

    def align_bottom(self):
        self._shapes.align_shapes_to_bottom(self.selection_except_blanks)
        self.present_refresh_canvas()

    def align_middle_horizontal(self):
        self._shapes.align_middle_horizontal(self.selection_except_blanks)
        self.present_refresh_canvas()

    def align_middle_vertical(self):
        self._shapes.align_middle_vertical(self.selection_except_blanks)
        self.present_refresh_canvas()

    def evenly_distribute_horizontally(self):
        self._shapes.evenly_distribute_horizontally(self.selection_except_blanks)
        self.present_refresh_canvas()

    def evenly_distribute_vertically(self):
        self._shapes.evenly_distribute_vertically(self.selection_except_blanks)
        self.present_refresh_canvas()

    # Adding
    def add_new_shape(self, text: str = 'Text', tag: str = None):
        request_model = RequestModel.request_model_add_new_shape
        new_shape_ids = self.add_new_shapes([request_model(text, tag)])
        self.add_shapes_to_selection(new_shape_ids)
        new_shape_id = new_shape_ids.pop()
        return new_shape_id

    def copy_shapes(self, shape_ids):
        canvas_refresh_was_prevented_at_the_beginning = self.prevent_refresh_canvas
        self.stop_canvas_refreshing()

        original_to_copies = {}
        for shape_id in tuple(shape_ids):
            text = self._shapes.get_text(shape_id)
            tag = self._shapes.get_tag_type(shape_id)
            copy_id = self.add_new_shape(text, tag)
            original_to_copies[shape_id] = copy_id

            self._shapes.copy(shape_id, copy_id, *self._configurations.move_shape_increment)
            self._connection_ids.copy(shape_id, copy_id)
            self._input_values.copy(shape_id, copy_id)
            self._input_ranges.copy(shape_id, copy_id)
            self._input_decimals.copy(shape_id, copy_id)
            self._format.copy(shape_id, copy_id)
            self._number_format.copy(shape_id, copy_id)
            self._vertical_accounts.copy(shape_id, copy_id)
            self._unit_of_measure.copy(shape_id, copy_id)

        self._connections.copy(original_to_copies)

        self.clear_selection()
        self.add_shapes_to_selection(tuple(original_to_copies.values()))

        if not canvas_refresh_was_prevented_at_the_beginning:
            self.start_canvas_refreshing()
            self.present_refresh_canvas()

    def copy_selection(self):
        self.copy_shapes(self._selection.data)

    def add_relay(self):
        self.add_relay_by_shape_ids(self._selection.data)
        self.present_refresh_canvas()

    def add_relay_by_shape_ids(self, shape_ids: Iterable) -> tuple:
        shapes = self._shapes
        accounts_or_relay = self._extract_account_or_relays_from_shape_ids(shape_ids)
        sorted_accounts_or_relay = sorted(accounts_or_relay)
        texts = [shapes.get_text(id_) for id_ in sorted_accounts_or_relay]
        request_models = [RequestModel.request_model_add_new_shape(text, 'relay') for text in texts]
        new_shape_ids = self.add_new_shapes(request_models)
        sorted_new_shape_ids = tuple(sorted(new_shape_ids))
        for new_shape_id, account_or_relay in zip(sorted_new_shape_ids, sorted_accounts_or_relay):
            shape_id_original = shapes.get_shape_it_represents_or_self(account_or_relay)
            shapes.set_shape_it_represents(new_shape_id, shape_id_original)
            self._connections.add_connection(shape_id_original, new_shape_id)
            shapes.set_x(new_shape_id, shapes.get_x(account_or_relay) + shapes.get_width(account_or_relay) + 30)
            shapes.set_y(new_shape_id, shapes.get_y(account_or_relay) + 30)

        self.upon_adding_new_shapes(sorted_new_shape_ids)
        return sorted_new_shape_ids

    def upon_adding_new_shapes(self, new_shape_ids):
        self.clear_selection()
        self.add_shapes_to_selection(new_shape_ids)
        self.fit_selected_shapes_width()
        self.present_refresh_canvas()

    def add_inter_sheets_relays(self, connections_passed: set = None):
        relays = self._shapes.get_shapes('relay')
        connections_to_evaluation = set(self._connections.data) if connections_passed is None else connections_passed
        for connection_from, connection_to in connections_to_evaluation:
            sheet_from = self._worksheets.get_worksheet_of_an_account(connection_from)
            sheet_to = self._worksheets.get_worksheet_of_an_account(connection_to)

            if sheet_from == sheet_to:
                continue
            if connection_to in relays:
                continue
            if sheet_to is None:
                continue
            if sheet_from is None:
                continue
            if self._shapes.get_tag_type(connection_from) != 'account':
                continue

            connection_from = self._shapes.get_shape_it_represents_or_self(connection_from)
            a = set(self._shapes.shapes_ids)
            self.add_relay_by_shape_ids((connection_from,))
            new_relay_id = (set(self._shapes.shapes_ids) - a).pop()

            initial_relay_x = self._shapes.get_x(connection_to) + self._shapes.get_width(connection_to) + 30
            initial_relay_y = self._shapes.get_y(connection_to)
            self.fit_shapes_width((new_relay_id,))

            self.move_contents_to_different_sheet((new_relay_id,), sheet_to)
            self._shapes.set_x(new_relay_id, initial_relay_x)
            self._shapes.set_y(new_relay_id, initial_relay_y)
            self._connections.remove_connection(connection_from, connection_to)
            self._connections.add_connection(new_relay_id, connection_to)

    def add_new_shapes(self, request_models: Iterable) -> set:
        all_shape_ids_before = set(self._shapes.shapes_ids)
        self._shapes.add_new_shapes(request_models)
        all_shape_ids_after = set(self._shapes.shapes_ids)
        new_shape_ids = all_shape_ids_after - all_shape_ids_before

        self._worksheets.add_contents_to_selected_sheet(new_shape_ids)

        tags = [rm['tags'][0] for rm in request_models]
        tag_to_wh = {
            'account': (self.account_width, self.account_height),
            'relay': (self.account_width, self.account_height),  # relay wh= account wh
            'bb': (self.bb_width, self.bb_height),
            'constant': (self.constant_width, self.constant_height),
            'operator': (self.operator_width, self.operator_height),
        }
        try:
            whs = tuple(tag_to_wh[tag] for tag in tags)
        except KeyError:
            """
            All other tags will use operator's width height value.
                Expects tags like slider, graph, and their supporting tags.
                These tags' width height will be set later in the process.
            """
            whs = tuple(tag_to_wh['operator'] for _ in request_models)
        imp9.interactor_is_responsible_for_setting_default_sizes_and_positions(new_shape_ids, self._shapes, whs)
        imp9.prevent_shape_overlaps(self._increment_x_y, new_shape_ids, self._shapes, self.sheet_contents)
        self._add_account_order_by_shape_ids(new_shape_ids)

        self._present_update_account_order()
        self._present_add_shape(new_shape_ids)
        self._present_highlight_automatic(new_shape_ids)

        return new_shape_ids

    def erase_shapes_in_rectangle(self, request: dict):
        shape_ids = imp9.get_shape_ids_within_rectangle(request, self._shapes, self.sheet_contents)
        self.erase_shapes_by_shape_ids(shape_ids)

    def erase_selected_shapes(self, **_):
        shapes_to_erase = set(self._selection.data)
        if len(shapes_to_erase) == 0:
            return

        next_element = imp9.decide_what_to_select_next(self._account_order, self._selection)
        self.erase_shapes_by_shape_ids(shapes_to_erase)
        self._selection.select_shape(next_element)
        self._upon_selection((next_element,))

    def erase_shapes_by_shape_ids(self, shape_ids: Iterable):
        request_model = RequestModel.request_model_erase_shape
        self.erase_shapes([request_model(shape_id) for shape_id in shape_ids])

    def erase_shapes(self, request_models: Iterable):
        shape_ids_deleted = tuple(request_model['shape_id'] for request_model in request_models)
        relays = []
        for shape_id in shape_ids_deleted:
            for relay in self._shapes.get_relays(shape_id):
                relays.append(relay)
        all_shapes_ids_to_be_deleted = shape_ids_deleted + tuple(relays)

        new_request_models = tuple({'shape_id': shape_id} for shape_id in all_shapes_ids_to_be_deleted)
        self._shapes.erase_shapes(new_request_models)

        self._worksheets.remove_contents_from_respective_sheets(all_shapes_ids_to_be_deleted)
        self.remove_selections_by_shape_ids(all_shapes_ids_to_be_deleted)
        self._connections.remove_all_connections_by_shape_ids(all_shapes_ids_to_be_deleted)
        self._remove_account_orders_by_shape_ids(all_shapes_ids_to_be_deleted)
        self._connection_ids.remove_shape_ids(all_shapes_ids_to_be_deleted)
        self._input_values.remove_accounts(all_shapes_ids_to_be_deleted)
        self._input_ranges.remove_ranges(all_shapes_ids_to_be_deleted)
        self._input_decimals.remove_decimals(all_shapes_ids_to_be_deleted)
        self._vertical_accounts.remove_vertical_accounts(all_shapes_ids_to_be_deleted)
        self.remove_format(all_shapes_ids_to_be_deleted)
        self.remove_number_format(all_shapes_ids_to_be_deleted)
        self.remove_fills(all_shapes_ids_to_be_deleted)
        self._unit_of_measure.remove_uoms(all_shapes_ids_to_be_deleted)

        self._present_update_account_order()
        self._present_remove_shape(all_shapes_ids_to_be_deleted)

    def erase_all_shapes(self):
        self._shapes.erase_all_shapes()
        self._selection.clear_selection()
        self._present_clear_canvas()

    def _present_add_shape(self, shape_ids: Iterable):
        response_model = ResponseModel.response_model_to_presenter_add_shape
        tag_type_to_font_size = {
            'account': self.account_font_size,
            'relay': self.account_font_size,
            'constant': self.constant_font_size,
            'bb': self.bb_font_size,
            'operator': self.operator_font_size,
        }
        shape_id_to_font_size = dict(zip(
            shape_ids,
            tuple(tag_type_to_font_size.get(self._shapes.get_tag_type(i), 13) for i in shape_ids)))
        self._presenters.add_shape(response_model(self._shapes.data, shape_ids, shape_id_to_font_size))

    def _present_remove_shape(self, shape_ids_to_delete: Iterable):
        canvas_tags = tuple(self._shapes.get_canvas_tag_from_shape_id(i) for i in shape_ids_to_delete)
        self._presenters.remove_shape(canvas_tags)

    # Rectangle
    def draw_rectangle(self, coordinate_from=None, coordinate_to=None, line_width=None, line_color=None, request=None):
        if request:
            coordinate_from, coordinate_to = request['coordinates']
            line_width = request['line_width']
            line_color = request['line_color']

        self._rectangle.clear_rectangle()
        request_model = RequestModel.request_model_draw_rectangle
        self.draw_rectangles([request_model(coordinate_from, coordinate_to, line_width, line_color)])

    def draw_rectangles(self, request_models: Iterable):
        self._rectangle.draw_rectangles(request_models)
        self._present_draw_rectangle()

    def erase_rectangles(self, request_models: Iterable):
        self._rectangle.erase_rectangles(request_models)
        self._present_draw_rectangle()

    def clear_rectangles(self, **__):
        self._rectangle.clear_rectangle()
        self._present_draw_rectangle()

    def _present_draw_rectangle(self):
        response_model = ResponseModel.response_model_to_presenter_draw_rectangle
        self._presenters.draw_rectangle(response_model(self._rectangle.data))

    # Connection
    def connect_shapes_by_names(self, name_from, sheet_from, nth_from, name_to, sheet_to, nth_to):
        shape_id_from = self.get_shape_id_by_name(name_from, sheet_from, nth_from)
        shape_id_to = self.get_shape_id_by_name(name_to, sheet_to, nth_to)
        if (shape_id_from is not None) and (shape_id_to is not None):
            self.connect_shapes_by_shape_ids(shape_id_from, shape_id_to)
        elif shape_id_from is None:
            self._present_feedback_user(f'{name_from} does not exist.')
        elif shape_id_to is None:
            self._present_feedback_user(f'{name_to} does not exist.')

    def connect_shapes_by_coordinates(self, coordinate_from=None, coordinate_to=None, request: dict = None):
        if request:
            coordinate_from, coordinate_to = request['coordinates']

        connections = self._connections
        shapes = self._shapes
        contents = self.sheet_contents

        validation = imp9.validate_connection_by_coords(coordinate_from, coordinate_to, connections, shapes, contents)
        if validation == 'valid':
            args = self.add_connections, coordinate_from, coordinate_to, self._present_feedback_user, shapes, contents
            imp9.connect_shapes_and_feedback(*args)
        else:
            imp9.clear_connector_line_and_status_bar(self._present_connect_shapes, self._present_feedback_user)
        self._present_highlight_automatic()

    def erase_connections_in_range(self, request: dict):
        all_connections_in_the_range = self._get_connections_in_range(request)
        connections = imp9.get_filtered_connection(all_connections_in_the_range, self.sheet_contents)
        for connection in connections:
            self.disconnect_shapes_by_shape_ids(*connection)

    def connect_shapes_by_shape_ids(self, shape_id_from, shape_id_to):
        request_model = RequestModel.request_model_add_connection
        self.add_connections([request_model(shape_id_from, shape_id_to)])

    def disconnect_shapes_by_shape_ids(self, shape_id_from, shape_id_to):
        request_model = RequestModel.request_model_remove_connection
        self.remove_connections([request_model(shape_id_from, shape_id_to)])

    def show_connectable_shapes(self, id_from=None, request: dict = None):
        if request is not None:
            id_from = self._shapes.get_shape_id_at_the_coordinate(request['x'], request['y'], self.sheet_contents)
        if id_from is not None:
            if not self._sf.manually_highlighted:
                args = id_from, self._shapes, self.sheet_contents, self._connections, self._present_highlight_manual
                imp9.show_connectable_shapes(*args)

    def remove_connections(self, request_models: Iterable):
        self._connections.remove_connections(request_models)
        self._present_connect_shapes()

    def add_connections(self, request_models: Iterable):
        self._connections.add_connections(request_models)
        self._present_connect_shapes()

    def connect_relay_of_shape_at_x_y(self, request: dict):
        shape_id = imp9.get_shape_id_at_mouse_point(self._shapes, request, self.sheet_contents)
        original_shape_id = self._shapes.get_shape_it_represents(shape_id)
        if shape_id is None:
            return
        if original_shape_id is not None:
            self.connect_shapes_by_shape_ids(original_shape_id, shape_id)
        for relay in self._shapes.get_relays(shape_id):
            self.connect_shapes_by_shape_ids(shape_id, relay)

    def are_connected(self, from_, to_) -> bool:
        if self.directly_connected(from_, to_) or self.indirectly_connected(from_, to_):
            return True
        return False

    def directly_connected(self, from_, to_) -> bool:
        return (from_, to_) in self._connections.data

    def indirectly_connected(self, from_, to_) -> bool:
        connection_tos = self._connections.get_connections_out_of(from_)
        relays = tuple(c for c in connection_tos if self._shapes.get_tag_type(c) == 'relay')
        for relay in relays:
            if self.directly_connected(relay, to_):
                return True
        return False

    def get_dependencies(self, shape_id) -> set:
        return imp9.get_dependencies(shape_id, self._shapes, self._connections)

    def get_minimum_circular_dependencies(self, shape_id) -> tuple:
        return imp9.get_minimum_circular_dependencies(shape_id, self._connections, self._shapes)

    def get_circular_connections(self) -> tuple:
        return tuple(imp9.get_all_circular_connections(self._connections, self._shapes))

    def is_circular(self, shape_id) -> bool:
        return imp9.is_cyclic(shape_id, self._connections, self._shapes)

    def analyze_circular_reference(self):
        circular_connections = self.get_circular_connections()
        if circular_connections == ():
            self._present_feedback_user('No circular reference.', 'success')
            return
        else:
            self._sf.set_cache_circular_connections(circular_connections)

        cycle_breakers = imp9.get_cycle_breakers(self._connections, self._shapes)
        self._present_feedback_user(f'Cycle breakers = {cycle_breakers}')
        self._present_connect_shapes_and_show_circular_reference()

    def _present_connect_shapes(self, connections_selected: Iterable = None):
        if self._sf.circular_connections_is_not_cached:
            self._sf.set_cache_circular_connections(())
        self._present_connections(connections_selected)

    def _present_connect_shapes_and_show_circular_reference(self, connections_selected: Iterable = None):
        if self._sf.circular_connections_is_not_cached:
            self._sf.set_cache_circular_connections(self.get_circular_connections())
        self._present_connections(connections_selected)

    def _clear_circular_reference_cache(self):
        self._sf.clear_cache_circular_connections()

    def _present_connections(self, connections_selected):
        if not self._cache.connection_model_is_cached:
            response_model = self._create_response_model_for_presenter_connection(connections_selected)
        else:
            response_model = self._cache.cache_response_model_for_presenter_connection
        self._presenters.connect_shapes(response_model)

    def _create_response_model_for_presenter_connection(self, connections_selected=None):
        sht_contents = self.sheet_contents
        g, s = graph, slider
        tag_types = 'relay', g.tag_y_axis, g.tag_bar, s.slider_range, 'account', 'relay', live_value.tag_live_value
        tag_types_to_shape_ids = self._shapes.create_tag_type_to_shape_ids_dictionary(tag_types, sht_contents)
        no_arrows = tag_types_to_shape_ids[s.slider_range]

        rm = ResponseModel.response_model_to_presenter_connect
        f = self._shapes.get_coords_from_shape_id
        circular = self._sf.cache_circular_connections
        response_model = rm(self.connections_filtered, f, connections_selected, circular, no_arrows)
        return response_model

    @property
    def connections_filtered(self) -> set:
        if not self._cache.connections_filetered_are_cached:
            connections = self._connections.data
            sht_contents = self.sheet_contents
            selected = self._selection.data
            tt = 'relay', graph.tag_y_axis, graph.tag_bar, slider.slider_range, 'account', 'relay', live_value.tag_live_value
            tag_types_to_shape_ids = self._shapes.create_tag_type_to_shape_ids_dictionary(tt, sht_contents)

            relays = tag_types_to_shape_ids['relay']
            y_axes = tag_types_to_shape_ids[graph.tag_y_axis]
            bars = tag_types_to_shape_ids[graph.tag_bar]
            na = no_arrows = tag_types_to_shape_ids[slider.slider_range]
            accounts = tag_types_to_shape_ids['account'] + tag_types_to_shape_ids['relay']
            live_values = tag_types_to_shape_ids[live_value.tag_live_value]
            args = sht_contents, selected, relays, y_axes, bars, na, accounts, live_values
            connections_filtered = set(c for c in connections if imp9.connection_filter(c, *args))
        else:
            connections_filtered = self._cache.connections_filtered
        return connections_filtered

    # Line
    def draw_line_shape_connector(self, coordinate_from: tuple = None, coordinate_to: tuple = None, width=None,
                                  color=None, request: dict = None):
        if request:
            coordinate_from, coordinate_to = request['coordinates']
            width = request['line_width']
            color = request['line_color']
        id_from = self._shapes.get_shape_id_at_the_coordinate(*coordinate_from, self.sheet_contents)
        id_to = self._shapes.get_shape_id_at_the_coordinate(*coordinate_to, self.sheet_contents)
        if id_from is None:
            return

        args = coordinate_from, coordinate_to, self._connections, self._shapes, self.sheet_contents
        validation = imp9.validate_connection_by_coords(*args)
        color, feed_back = imp9.get_line_color_and_user_feedback_based_on_validation(id_from, id_to, color, validation)

        self.show_connectable_shapes(id_from)
        self.erase_all_lines()
        self._present_feedback_user(feed_back)
        request_model = RequestModel.request_model_draw_line
        self.draw_lines([request_model(coordinate_from, coordinate_to, width, color)])

    def draw_lines(self, request_models: Iterable):
        self._lines.draw_lines(request_models)
        self._present_draw_line()

    def erase_all_lines(self, request: dict = None):
        self._lines.clear_lines()
        self._present_draw_line()

    def erase_lines(self, request_models: Iterable):
        self._lines.erase_lines(request_models)
        self._present_draw_line()

    def _present_draw_line(self):
        response_model = ResponseModel.response_model_to_presenter_draw_line
        self._presenters.draw_line(response_model(self._lines.data))

    # State
    @property
    def current_state(self):
        return self._gateways.current_state

    def states_are_different(self, state_one, state_two) -> bool:
        return self._gateways.states_are_different(state_one, state_two)

    def save_state_to_file(self, file_name: str):
        self._selection.clear_selection()
        feedback = self._clean_data_and_save_as_template_file(file_name)
        if feedback == 'success':
            self.feedback_user(f'{file_name} saved.', 'success')
        else:
            self.feedback_user(feedback, 'error')

    def save_current_sheet_as_module(self, file_name: str):
        temporary_gateways = imp9.save_state_without_using_memento(self._gateways.__class__, self._entities)

        self._memorize_who_to_dynamically_connect_with()
        self._erase_all_shapes_except_current_sheet()
        self.save_state_to_file(file_name)

        imp9.restore_state_without_using_memento(temporary_gateways)
        self._upon_loading_state()

    def _memorize_who_to_dynamically_connect_with(self):
        for from_, to_ in self._connections.data:
            self.grab_all_connection_ids_of_sockets_outside_of_current_sheet(from_, to_)
            self.grab_all_connection_ids_of_plugs_outside_of_current_sheet(from_, to_)

    def grab_all_connection_ids_of_sockets_outside_of_current_sheet(self, from_, to_):
        from_, to_ = self._remove_relays(from_, to_)
        if imp9.is_a_connection_out_of_current_sheet(self.sheet_contents, from_, to_):
            if self._connection_ids.has_connection_id(to_):
                connection_ids = self._connection_ids.get_connection_ids(to_)
                for connection_id in connection_ids:
                    self._connection_ids.add_socket_to_dynamically_search_for(from_, connection_id)

    def grab_all_connection_ids_of_plugs_outside_of_current_sheet(self, from_, to_):
        from_, to_ = self._remove_relays(from_, to_)
        if imp9.is_connection_into_current_sheet(self.sheet_contents, from_, to_):
            if self._connection_ids.has_connection_id(from_):
                connection_ids = self._connection_ids.get_connection_ids(from_)
                for connection_id in connection_ids:
                    self._connection_ids.add_plug_to_dynamically_accept(to_, connection_id)

    def _remove_relays(self, from_, to_):
        from_ = self._shapes.get_shape_it_represents_or_self(from_)
        to_ = self._shapes.get_shape_it_represents_or_self(to_)
        return from_, to_

    def _erase_all_shapes_except_current_sheet(self):
        current_sheet = self._worksheets.selected_sheet
        previous_sheet_state = copy.deepcopy((self._worksheets.sheet_names, self._worksheets.selected_sheet))
        for sheet_name in self._worksheets.sheet_names:
            if sheet_name != current_sheet:
                self.erase_shapes_by_shape_ids(self._worksheets.get_sheet_contents(sheet_name))
                self._entities.delete_a_sheet(sheet_name)
        self.upon_updating_worksheets(previous_sheet_state)

    def load_memento(self, memento):
        self._gateways.load_state_from_memento(memento)
        self._upon_loading_state()
        self._input_values.change_number_of_periods(self.number_of_periods)
        self._present_feedback_user(f'Loaded state', 'success')

    def load_file(self, file_name: str):
        self._gateways.load_state_from_file(file_name)
        self._upon_loading_state()
        self._input_values.change_number_of_periods(self.number_of_periods)
        self._present_feedback_user(f'Loaded file: {file_name}', 'success')

    def merge_file(self, file_name: str):
        initial_shapes = set(self._shapes.shapes_ids)
        self._gateways.merge_state_from_file(file_name)

        current_sheet = self._worksheets.selected_sheet
        get_sheet = self._worksheets.get_worksheet_of_an_account
        existing_shapes = tuple(shape_id for shape_id in initial_shapes if get_sheet(shape_id) == current_sheet)
        y_shift = self.get_y_shift_to_prevent_overlap(existing_shapes, self._worksheets.selected_sheet)
        shapes_added = set(self._shapes.shapes_ids) - initial_shapes
        for shape_id in shapes_added:
            self._shapes.set_y(shape_id, self._shapes.get_y(shape_id) + y_shift)

        self._upon_loading_state()
        self._input_values.change_number_of_periods(self.number_of_periods)
        self.auto_connect()
        self.add_inter_sheets_relays(self._connections.new_merged_connections)
        self._present_feedback_user(f'Merged file: {file_name}', 'success')
        self._selection.add_selections_by_shape_ids(shapes_added)
        self.present_refresh_canvas()

    def remove_templates(self, pickle_names: tuple):
        for pickle_name in pickle_names:
            self.remove_template(pickle_name)

    def remove_template(self, pickle_name):
        feedback = self._gateways.remove_template(pickle_name)
        if feedback != 'success':
            self._present_feedback_user(feedback, feedback)

    def clean_up_all_templates(self, negative_list: tuple):
        for file_name in self.get_pickle_file_names(negative_list):
            self.clean_template_pickle(file_name)

    def save_all_to_file(self, file_name: str):
        self._selection.clear_selection()
        self._gateways.save_all_sates_to_file(file_name)
        self._present_feedback_user(f'Saved all stated to {file_name}')

    def load_all_from_file(self, file_name: str):
        self._gateways.restore_all_states_from_file(file_name)
        self._upon_loading_state()
        self._present_feedback_user(f'Loaded all states from file: {file_name}')

    def load_pickle_files_list(self, negative_list: tuple = None):
        file_names = self.get_pickle_file_names(negative_list)
        self._present_load_pickle_files_list(file_names)

    def get_pickle_file_names(self, negative_list):
        file_names = self._gateways.pickle_file_names
        if negative_list is None:
            negative_list = self._gateways.negative_list
        else:
            negative_list += self._gateways.negative_list
        for negative in negative_list:
            try:
                file_names.remove(negative)
            except ValueError:
                pass
        file_names.sort()
        return file_names

    @property
    def pickle_commands_file_names(self) -> list:
        return self._gateways.pickle_macro_file_names

    def reset(self):
        self.clear_all_cache()
        old_entities = self._entities
        commands = old_entities.commands
        copied_commands = old_entities.copied_commands
        new_entities = Entities()
        new_entities._commands = commands
        new_entities._copied_commands = copied_commands

        self._set_entities(new_entities)
        self.add_new_worksheet('Sheet1')
        self._gateways.reset(new_entities)
        self.present_refresh_canvas()
        self._present_update_account_order()

    def save_state_to_memory(self, save_name: str = ''):
        if self._sf.is_more_than_second_entry:
            return

        saved = self._gateways.save_state(save_name)
        if saved:
            self._present_save_slot()

    def undo(self):
        self._gateways.undo()
        self._upon_loading_state()
        self._present_save_slot()

    def redo(self):
        self._gateways.redo()
        self._upon_loading_state()
        self._present_save_slot()

    def change_path_pickles(self, directory: str):
        self._gateways.change_path_pickles(directory)
        self.set_save_path(directory)

    def change_path_command_pickles(self, directory: str):
        self._gateways.change_path_command_pickles(directory)

    def _upon_loading_state(self):
        self.present_refresh_canvas()
        self._present_update_account_order()

        # support for old pickle without connections to relay
        for relay in self._shapes.get_shapes('relay'):
            original_ac = self._shapes.get_shape_it_represents(relay)
            self._connections.add_connection(original_ac, relay)

    def _present_save_slot(self):
        save_result = self._gateways.save_result
        self._present_feedback_user(save_result)

    def _present_load_pickle_files_list(self, file_names):
        response_model = ResponseModel.response_model_to_presenter_load_pickle_files_list
        self._presenters.load_pickle_files_list(response_model(file_names))

    # Account Order
    def add_blank_above_selection(self):
        orders = imp9.get_current_account_orders(self._account_order, self._selection.data)
        index_ = max(0, min(orders)) if orders else 0
        self.add_blank_row(index_)
        self._present_update_account_order()

    def move_selection_up(self, by: int = 1):
        shapes_to_sort = tuple(shape_id for shape_id in self._selection.data if shape_id in self._account_order.data)
        self._sort_accounts(shapes_to_sort, by, -1)

    def move_selection_down(self, by: int = 1):
        shapes_to_sort = tuple(shape_id for shape_id in self._selection.data if shape_id in self._account_order.data)
        self._sort_accounts(shapes_to_sort, by, 1)

    def _sort_accounts(self, shapes_to_be_moved: Iterable, by, sign):
        self._present_feedback_user('')
        success = imp9.sort_accounts(shapes_to_be_moved, sign, by, self._account_order, self.change_account_order)
        self._present_update_account_order()
        if not success:
            self._present_feedback_user('Could not sort accounts. Check sorting algorithms.')

    def change_account_order(self, index_: int, destination: int):
        self._account_order.change_account_order(index_, destination)

    def add_blank_row(self, index_: int):
        self._account_order.add_blank(index_)

    def is_blank(self, value) -> bool:
        return value.__class__ == self._entities.blank.__class__

    def _add_account_order_by_shape_ids(self, new_shape_ids):
        imp9.set_account_order(self._account_order, new_shape_ids, self._shapes)

    def _remove_account_orders_by_shape_ids(self, shape_ids_deleted):
        self._account_order.remove_accounts(shape_ids_deleted)

    def _get_account_order_negative_list(self):
        shapes = self._shapes
        negative_list = ()
        negative_list += shapes.get_shapes('operator')
        negative_list += shapes.get_shapes('relay')
        negative_list += shapes.get_shapes('bb')
        negative_list += shapes.get_shapes('constant')
        negative_list += shapes.get_shapes(graph.tag_y_axis)
        negative_list += shapes.get_shapes(graph.tag_y_min)
        negative_list += shapes.get_shapes(graph.tag_y_max)
        negative_list += shapes.get_shapes(graph.tag_bar)
        negative_list += shapes.get_shapes(graph.tag_period)
        negative_list += shapes.get_shapes(slider.slider_range)
        negative_list += shapes.get_shapes(slider.slider_handle)
        negative_list += shapes.get_shapes(slider.slider_min)
        negative_list += shapes.get_shapes(slider.slider_max)
        negative_list += shapes.get_shapes(slider.slider_gauge)
        negative_list += shapes.get_shapes(slider.slider_decimal)

        return negative_list

    def _present_update_account_order(self):
        account_names_by_order = imp9.get_account_names_by_order(self._account_order, self._shapes)
        select_flags = imp9.get_select_flags(self._account_order, self._selection)
        response_model = ResponseModel.response_model_to_presenter_update_account_order
        self._presenters.update_account_order(response_model(account_names_by_order, select_flags))

    # User Feedback
    def present_state(self):
        shapes = self._shapes
        response_model = ResponseModel.response_model_to_presenter_states
        shape_ids = shapes.shapes_ids
        x_coords = tuple(shapes.get_x(shape_id) for shape_id in shape_ids)
        texts = dict(zip(shapes.shapes_ids, tuple(shapes.get_text(shape_id) for shape_id in shapes.shapes_ids)))
        connections = self._connections
        operators = shapes.get_shapes('operator')
        rpe_readable = self.output_rpe_readable
        input_accounts = self.input_accounts
        input_texts = tuple(shapes.get_text(shape_id) for shape_id in input_accounts)
        sheet = self.output_worksheet_information
        connection_ids = self._connection_ids.data
        vertical_accounts = self._vertical_accounts.data
        args = shape_ids, x_coords, texts, connections.data, operators, rpe_readable, input_accounts, input_texts, sheet, connection_ids, vertical_accounts
        self._presenters.present_states(response_model(*args))

    def feedback_user(self, text: str, feedback_type='normal', is_incremental_progress=False):
        self._present_feedback_user(text, feedback_type, is_incremental_progress)

    def _present_feedback_user(self, text: str, feedback_type='normal', is_incremental_progress=False):
        response_model = ResponseModel.response_model_to_presenter_update_status_bar
        self._presenters.feedback_user(response_model(text, feedback_type, is_incremental_progress))

    # Vertical Account
    def add_selection_to_vertical_accounts(self):
        self._selected_account_iterator(self.add_vertical_account)

    def remove_selection_from_vertical_accounts(self):
        self._selected_account_iterator(self.add_vertical_account)

    def _selected_account_iterator(self, command: Callable):
        accounts = self._shapes.get_shapes('account')
        for shape_id in self._selection.data:
            if shape_id in accounts:
                command(shape_id)

    def add_vertical_account(self, account_id):
        if self._shapes.get_tag_type(account_id) == 'account':
            self._vertical_accounts.add_vertical_account(account_id)
        else:
            self._present_feedback_user('Only account can be added to Vertical Account', 'error')

    def remove_vertical_account(self, account_id):
        self._vertical_accounts.remove_vertical_account(account_id)

    def add_vertical_reference_to_selection(self, vertical_reference_id):
        all_accounts = self._shapes.get_shapes('account')
        account = vertical_reference_id
        if account not in all_accounts:
            self._present_feedback_user(f'{vertical_reference_id} does not exist!', 'error')
            return
        for shape_id in self._selection.data:
            if self._shapes.get_tag_type(shape_id) == 'account':
                self.add_vertical_reference(shape_id, vertical_reference_id)

    def remove_vertical_reference_to_selection(self, vertical_reference_id):
        all_accounts = self._shapes.get_shapes('account')
        account = vertical_reference_id
        if account not in all_accounts:
            self._present_feedback_user(f'{vertical_reference_id} does not exist!', 'error')
            return
        for shape_id in self._selection.data:
            if self._shapes.get_tag_type(shape_id) == 'account':
                self.remove_vertical_reference(shape_id, vertical_reference_id)

    def add_vertical_reference(self, vertical_account_id, vertical_reference_id):
        all_accounts = self._shapes.get_shapes('account')
        account = vertical_account_id
        if account not in all_accounts:
            self._present_feedback_user(f'{account} does not exist!', 'error')
            return
        account = vertical_reference_id
        if account not in all_accounts:
            self._present_feedback_user(f'{account} does not exist!', 'error')
            return

        self._vertical_accounts.add_vertical_reference(vertical_account_id, vertical_reference_id)

    def remove_vertical_reference(self, vertical_account_id, vertical_reference_id):
        all_accounts = self._shapes.get_shapes('account')
        account = vertical_account_id
        if account not in all_accounts:
            self._present_feedback_user(f'{account} does not exist!', 'error')
            return
        account = vertical_reference_id
        if account not in all_accounts:
            self._present_feedback_user(f'{account} does not exist!', 'error')
            return
        self._vertical_accounts.remove_vertical_reference(vertical_account_id, vertical_reference_id)

    def remove_vertical_reference_from_all_vertical_accounts(self, vertical_reference_id):
        self._vertical_accounts.remove_vertical_reference_from_all_vertical_accounts(vertical_reference_id)

    # UOM
    def add_unit_of_measure(self, shape_id, unit_of_measure: str):
        tag = self._shapes.get_tag_type(shape_id)
        if tag == 'account':
            self._unit_of_measure.add_unit_of_measure(shape_id, unit_of_measure)
        else:
            self.feedback_user(f'Unit of measure can only be set to Accounts, not {tag}','error')

    def add_unit_of_measure_to_selection(self, unit_of_measure: str):
        for shape_id in self.selected_accounts:
            self.add_unit_of_measure(shape_id, unit_of_measure)

    # Properties
    @property
    def selection_contains_constant(self) -> bool:
        return True in tuple(self._shapes.get_tag_type(i) == 'constant' for i in self._selection.data)

    @property
    def number_of_selected_shapes(self) -> int:
        return len(self._selection.data)

    def refresh_properties(self):
        self._present_shape_properties()

    def _present_shape_properties(self):
        args1 = (self._selection.data,
                 self._shapes,
                 self._worksheets,
                 self._format,
                 self._number_format,
                 self._vertical_accounts,
                 self._unit_of_measure,
                 )

        response_model = ResponseModel.response_model_to_presenter_shape_properties
        self._presenters.update_shape_properties(response_model(*imp9.get_common_properties(*args1)))

    def set_property_to_selection(self, key: str, value):
        self.set_properties(key, self._selection.data, value)
        self.present_refresh_canvas()

    def worksheet_exists(self, sheet_name: str) -> bool:
        existing_worksheet_names = self._worksheets.sheet_names
        return sheet_name in existing_worksheet_names

    def set_worksheet_to_selected_shapes_properties(self, sheet_to):
        if not self.worksheet_exists(sheet_to):
            self.feedback_user(f'Worksheet {sheet_to} does not exist.', 'error')
            return

        shape_ids = self.get_selection_sorted_by_account_order()
        self.move_contents_to_different_sheet(shape_ids, sheet_to)
        self.add_inter_sheets_relays()

    def move_contents_to_different_sheet(self, shape_ids: tuple, sheet_to):
        y_shift_to_prevent_overlap = self.get_y_shift_to_prevent_overlap(shape_ids, sheet_to)
        account_order_of_sheet_to = self._account_orders.get_account_order(sheet_to)
        accounts_before_blank = self.get_shape_ids_followed_by_blank_in_account_order()
        sheet_froms = tuple(self._worksheets.get_worksheet_of_an_account(s) for s in shape_ids)

        for shape_id, sheet_from in zip(shape_ids, sheet_froms):
            if sheet_from == sheet_to:
                continue
            self._entities.remove_sheet_content(sheet_from, shape_id)
            self._entities.add_sheet_content(sheet_to, shape_id, self._get_account_order_negative_list())
            self._shapes.set_y(shape_id, self._shapes.get_y(shape_id) + y_shift_to_prevent_overlap)
            if shape_id in accounts_before_blank:
                account_order_of_sheet_to.add_blank_to_last()

        self.present_refresh_canvas()

        texts = self._get_texts_of_shapes(shape_ids)
        self.feedback_user(f'Items moved to {sheet_to}: {texts}', 'success')

    def get_y_shift_to_prevent_overlap(self, shape_ids: tuple, sheet_to) -> float:
        if len(shape_ids) == 0:
            return 0
        args = shape_ids, self._worksheets.get_sheet_contents(sheet_to), 40, self._shapes
        return imp9.get_y_shift_to_prevent_overlap(*args)

    def get_shape_ids_followed_by_blank_in_account_order(self) -> tuple:
        data = self._account_order.data
        return tuple(data[n - 1] for (n, d) in enumerate(data) if (n > 0) and self.is_blank(d))

    def get_selection_sorted_by_account_order(self) -> tuple:
        shape_ids_list = []
        for shape_id in self._account_order.data:
            if not self.is_blank(shape_id) and shape_id in self._selection.data:
                self._selection.data.remove(shape_id)
                shape_ids_list.append(shape_id)
        shape_ids_list += list(self._selection.data)
        shape_ids = tuple(shape_ids_list)
        return shape_ids

    def set_properties(self, key, shape_ids, value):
        for shape_id in imp9.identify_shape_ids_to_update(key, shape_ids, self._shapes):
            self._shapes.set_value(key, shape_id, value)
        self.feedback_user(f'Set {key} = {value}')

    def change_shape_id(self, old_shape_id, new_shape_id):
        if str(old_shape_id) != str(new_shape_id):
            self._change_shape_id(old_shape_id, new_shape_id)

    def clean_template_pickle(self, file_name: str):
        self.load_file(file_name)
        self._clean_data_and_save_as_template_file(file_name)

    def _clean_data_and_save_as_template_file(self, file_name):
        if self.clean_state_prior_to_save:
            all_shape_ids = self._shapes.shapes_ids
            self._present_feedback_user('Cleaning up state...')
            new_shape_id = 0
            for shape_id in self._shapes.shapes_ids:
                self.change_shape_id(shape_id, shape_id + 10000)
            # Change shape id sorted by account_order
            for sheet_name in self._worksheets.sheet_names:
                account_order = self._account_orders.get_account_order(sheet_name)
                for item in account_order.data:
                    if not self.is_blank(item):
                        self.change_shape_id(item, new_shape_id)
                        new_shape_id += 1
            # Change shape id of non-account shapes
            for shape_id in self._shapes.shapes_ids:
                if shape_id >= 10000:
                    self.change_shape_id(shape_id, new_shape_id)
                    new_shape_id += 1
            # Remove redundant connection_ids
            self._connection_ids.clean_data()
            self._shape_format.clean_data(all_shape_ids)
            all_accounts = self._shapes.get_shapes('account')
            self._unit_of_measure.clean_data(all_accounts)
        feedback = self._gateways.save_file(file_name)
        return feedback

    def _change_shape_id(self, old_shape_id, new_shape_id):
        shape_ids_str = tuple(str(shape_id) for shape_id in self._shapes.shapes_ids)
        if str(new_shape_id) not in shape_ids_str:
            self._shapes.change_shape_id(old_shape_id, new_shape_id)
            self._connections.change_shape_id(old_shape_id, new_shape_id)
            self._selections.change_shape_id(old_shape_id, new_shape_id)
            self._account_orders.change_shape_id(old_shape_id, new_shape_id)
            self._worksheets.change_shape_id(old_shape_id, new_shape_id)
            self._input_ranges.change_shape_id(old_shape_id, new_shape_id)
            self._input_values.change_shape_id(old_shape_id, new_shape_id)
            self._input_decimals.change_shape_id(old_shape_id, new_shape_id)
            self._connection_ids.change_shape_id(old_shape_id, new_shape_id)
            self._format.change_shape_id(old_shape_id, new_shape_id)
            self._number_format.change_shape_id(old_shape_id, new_shape_id)
            self._vertical_accounts.change_shape_id(old_shape_id, new_shape_id)
            self._shape_format.change_shape_id(old_shape_id, new_shape_id)
            self._unit_of_measure.change_shape_id(old_shape_id, new_shape_id)

        else:
            self.feedback_user(f'{new_shape_id} already exists!', 'error')
        self.refresh_properties()

    # Presenters
    def present_insert_worksheet_in_input_sheet_mode(self):
        response_model = self._configurations.insert_sheet_name_in_input_sheet
        self._presenters.insert_sheet_name_in_input_sheet(response_model)

    def present_sensitivity_input_accounts(self):
        negative_list = self._configurations.sensitivity_variable_accounts
        self._present_input_accounts(negative_list)

    def _present_input_accounts(self, negative_list):
        accounts = tuple(ac for ac in self.input_accounts if ac not in negative_list)
        response_model = self._create_response_model_for_presenter_account(accounts)
        self._presenters.update_sensitivity_input_list(response_model)

    def present_sensitivity_accounts(self):
        present_method = self._presenters.update_sensitivity_account_list
        negative_list = self._configurations.sensitivity_target_accounts
        self._present_target_candidate_accounts(present_method, negative_list)

    def _present_target_candidate_accounts(self, present_method, negative_list: tuple = ()):
        formula_owners = self._rpe.get_all_formula_owners(self._connections.data, self._shapes.get_shapes('operator'))

        def filtered(account_) -> bool:
            is_and_account = (self._shapes.get_tag_type(account_) == 'account')
            not_added_yet = (account_ not in negative_list)
            return is_and_account and not_added_yet

        accounts = tuple(ac for ac in formula_owners if filtered(ac))
        response_model = self._create_response_model_for_presenter_account(accounts)
        present_method(response_model)

    def present_sensitivity_target_accounts(self):
        accounts = self._configurations.sensitivity_target_accounts
        response_model = self._create_response_model_for_presenter_selected_account(accounts)
        self._presenters.update_sensitivity_target_accounts(response_model)

    def present_sensitivity_variable_accounts(self):
        accounts = self._configurations.sensitivity_variable_accounts
        response_model = self._create_response_model_for_presenter_selected_account_with_deltas(accounts)
        self._presenters.update_sensitivity_variable_accounts(response_model)

    def _create_response_model_for_presenter_account(self, accounts: tuple):
        worksheets = tuple(self._worksheets.get_worksheet_of_an_account(account_id) for account_id in accounts)
        sh_sorted, ac_sorted = Utilities.sort_lists(worksheets, accounts)
        texts = self._get_texts_of_shapes(ac_sorted)
        response_model = ResponseModel.response_model_to_presenter_accounts(tuple(ac_sorted), texts, tuple(sh_sorted))
        return response_model

    def _create_response_model_for_presenter_selected_account(self, accounts: tuple):
        worksheets = tuple(self._worksheets.get_worksheet_of_an_account(account_id) for account_id in accounts)
        texts = self._get_texts_of_shapes(accounts)
        response_model = ResponseModel.response_model_to_presenter_accounts(tuple(accounts), texts, tuple(worksheets))
        return response_model

    def _create_response_model_for_presenter_selected_account_with_deltas(self, accounts: tuple):
        worksheets = tuple(self._worksheets.get_worksheet_of_an_account(account_id) for account_id in accounts)
        texts = self._get_texts_of_shapes(accounts)
        deltas = self._configurations.get_sensitivity_deltas(accounts)
        args = tuple(accounts), texts, tuple(worksheets), deltas
        response_model = ResponseModel.response_model_to_presenter_accounts_with_deltas(*args)
        return response_model

    def present_refresh_canvas(self):
        if not self.prevent_refresh_canvas:
            self._clear_circular_reference_cache()
            self._present_clear_canvas()
            self._present_add_shape(self.sheet_contents)
            self._present_connect_shapes()
            self.present_update_worksheets()
            self._present_shape_properties()
            self._present_connection_ids()
            self._present_highlight_automatic()

    def present_refresh_canvas_minimum(self):
        minimum_shapes_to_update = self._get_minimum_shape_ids_to_update()
        self._present_remove_shape(minimum_shapes_to_update)
        self._present_add_shape(minimum_shapes_to_update)
        self._present_connect_shapes()
        self._present_highlight_automatic(minimum_shapes_to_update)  # Comment out this to achieve super fast slider

    def _get_minimum_shape_ids_to_update(self) -> tuple:
        s, g, v = slider, graph, live_value
        tag_types = s.slider_handle, g.tag_bar, s.slider_gauge, v.tag_live_value
        shape_ids_to_update = self._shapes.filter_shapes_by_tag_and_intercept(tag_types, self.sheet_contents)
        return shape_ids_to_update

    def _present_clear_canvas(self):
        self._presenters.clear_canvas()

    def highlight_automatic(self, **_):
        self._present_highlight_automatic()

    def _present_highlight_automatic(self, shapes_to_highlight: Iterable = None):
        if shapes_to_highlight is None:
            shapes_to_highlight = self.sheet_contents
        if self._auto_highlight_is_disabled:
            return
        audit_results = self._get_audit_results(shapes_to_highlight)
        response_model = ResponseModel.response_model_to_presenter_highlight_auto
        self._presenters.highlight_shape(response_model(audit_results))
        self._sf.set_manually_highlighted(False)

    def stop_highlighting(self):
        self._sf.set_prevent_auto_highlight(True)

    def start_highlighting(self):
        self._sf.set_prevent_auto_highlight(False)

    @property
    def _auto_highlight_is_disabled(self) -> bool:
        return self._sf.prevent_auto_highlight

    def _present_highlight_manual(self):
        args = self._shapes.data, self._shapes.get_canvas_tag_from_shape_id, self._shapes.shapes_ids

        response_model = ResponseModel.response_model_to_presenter_highlight_manual
        self._presenters.highlight_shape(response_model(*args))
        self._sf.set_manually_highlighted(True)

    def _get_audit_results(self, shape_ids: Iterable) -> list:
        if self._cache.audit_results_are_cached:
            audit_results = self._cache.cache_audit_results
        else:
            audit_results = [self._get_audit_result(shape_id) for shape_id in shape_ids]
        return audit_results

    def _get_audit_result(self, shape_id) -> dict:
        is_selected = self._selection.is_selected(shape_id)
        tag_type = self._shapes.get_tag_type(shape_id)
        canvas_tag = self._shapes.get_canvas_tag_from_shape_id(shape_id)

        connections_in = self._connections.get_connections_into(shape_id)
        sheet_name = self._worksheets.get_worksheet_of_an_account(shape_id)
        id_to_sheet = self._worksheets.shape_id_to_sheet_name_dict
        external_dependencies = imp9.get_external_dependencies_sheets(connections_in, id_to_sheet, sheet_name)

        depending_on_external_sheet = len(external_dependencies) > 0
        depended_by_external_sheet = self.shape_is_depended_by_external_sheet(shape_id)
        format_data = self._format.data
        height = self._shapes.get_height(shape_id) if tag_type == graph.tag_bar else None  # to please unit tests...
        specified_fill = self._shape_format.get_specified_fill(shape_id)

        return ResponseModel.audit_shape(shape_id, is_selected, tag_type, canvas_tag, connections_in,
                                         depending_on_external_sheet, depended_by_external_sheet, format_data, height,
                                         specified_fill)

    def shape_is_depended_by_external_sheet(self, shape_id) -> bool:
        ws = self._worksheets
        sheet_name = ws.get_worksheet_of_an_account(shape_id)
        connections_out = self._connections.get_connections_out_of(shape_id)

        external_dependents = imp9.get_external_dependents(connections_out, sheet_name, ws.shape_id_to_sheet_name_dict)
        depended_by_external_sheet = len(external_dependents) > 0
        return depended_by_external_sheet

    def _get_connections_in_range(self, request: dict) -> tuple:
        x1, y1, x2, y2 = imp9.get_rectangle_coordinates_from_request(request)
        bottom_left, top_right = Utilities.get_rectangle_edges(x1, x2, y1, y2)

        current_sheet_contents = self.sheet_contents
        connections_intersecting_rectangle = []
        for connection in self._connections.data:
            if (connection[0] not in current_sheet_contents) or (connection[1] not in current_sheet_contents):
                continue
            p1, p2 = self._shapes.get_nearest_points_of_two_shape_ids(*connection)
            if Utilities.line_intersect_rectangle(p1, p2, bottom_left, top_right):
                connections_intersecting_rectangle.append(connection)
        return tuple(connections_intersecting_rectangle)

    # ConnectionID
    def add_connection_id(self, shape_id, socket_name: str):
        self._connection_ids.add_connection_id(shape_id, socket_name)

    def add_the_same_connection_ids_to_selection(self, connection_id: str):
        connection_ids = tuple(connection_id for _ in self._selection.data)
        self._connection_ids.add_connection_ids(self._selection.data, connection_ids)
        self._present_connection_ids()

    def add_the_same_plug_to_selection(self, plug_id: str):
        self._connection_ids.add_plugs_to_dynamically_accept(self._selection.data, plug_id)
        self._present_connection_ids()

    def add_the_same_socket_to_selection(self, socket_id: str):
        self._connection_ids.add_sockets_to_dynamically_search_for(self._selection.data, socket_id)
        self._present_connection_ids()

    def remove_connection_id_from_selection(self, connection_id):
        for shape_id in self._selection.data:
            self.remove_connection_id(shape_id, connection_id)
        self._present_connection_ids()

    def remove_connection_id(self, shape_id, connection_id):
        self._connection_ids.remove_connection_id(shape_id, connection_id)

    def remove_plug_id_from_selection(self, plug_id):
        for shape_id in self._selection.data:
            self._connection_ids.remove_plug_id(shape_id, plug_id)
        self._present_connection_ids()

    def remove_socket_id_from_selection(self, socket_id):
        for shape_id in self._selection.data:
            self._connection_ids.remove_socket_id(shape_id, socket_id)
        self._present_connection_ids()

    def auto_connect(self, shape_ids_to_search_from: Iterable = None):
        shape_ids = shape_ids_to_search_from or self._shapes.shapes_ids
        for shape_id in shape_ids:
            plugs_that_i_want = self._connection_ids.get_plugs_that_i_want(shape_id)
            self.accept_plugs(plugs_that_i_want, shape_id)
            sockets_that_i_want = self._connection_ids.get_sockets_that_i_want(shape_id)
            self.plug_into_sockets(sockets_that_i_want, shape_id)

    def accept_plugs(self, connection_ids: tuple, shape_id):
        candidates = self._get_candidates(connection_ids)
        if self._shapes.get_tag_type(shape_id) in ('account', 'bb'):
            if len(self._connections.get_connections_into(shape_id)) > 0:
                pass
            else:
                if len(candidates) == 1:
                    shape_id_decided = candidates[0]
                    self._connections.add_connection(shape_id_decided, shape_id)
                    self._connections.add_new_merged_connections(shape_id_decided, shape_id)
                elif len(candidates) > 1:
                    shape_id_decided = max(candidates)  # This line decides priority.
                    self._connections.add_connection(shape_id_decided, shape_id)
                    self._connections.add_new_merged_connections(shape_id_decided, shape_id)

        elif self._shapes.get_tag_type(shape_id) == 'operator':
            for candidate in candidates:
                if not self.are_connected(candidate, shape_id):
                    self._connections.add_connection(candidate, shape_id)

    def plug_into_sockets(self, connection_ids: tuple, shape_id):
        for candidate in self._get_candidates(connection_ids):
            if self._shapes.get_tag_type(candidate) in ('account', 'bb'):
                if len(self._connections.get_connections_into(candidate)) == 0:
                    self._connections.add_connection(shape_id, candidate)
                    self._connections.add_new_merged_connections(shape_id, candidate)
            elif not self.are_connected(shape_id, candidate):
                self._connections.add_connection(shape_id, candidate)
                self._connections.add_new_merged_connections(shape_id, candidate)

    def _get_candidates(self, connection_ids) -> list:
        candidates = []
        for connection_id in connection_ids:
            shape_ids_with_target_connection_id = self._connection_ids.get_shape_ids_connection_id(connection_id)
            candidates += list(shape_ids_with_target_connection_id)
        candidates = list(set(candidates))  # remove duplicate
        return candidates

    def _present_connection_ids(self, select_index=0):
        if len(self._selection.data) == 0:
            types_and_names = ()
            select_flags = ()
        elif len(self._selection.data) == 1:
            account_id = tuple(self._selection.data)[0]
            connection_ids = self._connection_ids.get_connection_ids(account_id)
            sockets = self._connection_ids.get_sockets_that_i_want(account_id)
            plugs = self._connection_ids.get_plugs_that_i_want(account_id)

            names = connection_ids + sockets + plugs
            type_id = tuple('id' for _ in connection_ids)
            type_socket = tuple('socket' for _ in sockets)
            type_plug = tuple('plug' for _ in plugs)
            id_types = type_id + type_socket + type_plug
            types_and_names = tuple(zip(id_types, names))
            select_flags = tuple(n == select_index for (n, _) in enumerate(types_and_names))
        else:
            return

        response_model = ResponseModel.response_model_to_presenter_update_connection_ids
        self._presenters.update_connection_ids(response_model(types_and_names, select_flags))

    # Format
    def toggle_format(self):
        selected = tuple(self._selection.data)
        if len(selected) == 0:
            return

        format_key = self._format.get_format(selected[0])
        index_ = -1
        try:
            index_ = self._format.all_format_keys.index(format_key)
        except ValueError:
            pass

        if index_ == -1:
            self.set_selection_as_heading()
        elif index_ == 0:
            self.set_selection_as_sub_total()
        elif index_ == 1:
            self.remove_format_from_selections()
        self._present_shape_properties()

    def set_selection_as_heading(self):
        self.set_format_heading(self.selected_accounts)

    def set_selection_as_sub_total(self):
        self.set_format_sub_total(self.selected_accounts)

    def toggle_number_format(self):
        selected_ = tuple(self._selection.data)
        if len(selected_) == 0:
            return

        number_format_key = self._number_format.get_format(selected_[0])
        index_ = -1
        try:
            index_ = self._number_format.all_number_format_keys.index(number_format_key)
        except ValueError:
            pass

        if index_ == -1:
            self.set_number_format_whole_number_to_selection()
        elif index_ == 0:
            self.set_number_format_one_digit_to_selection()
        elif index_ == 1:
            self.set_number_format_two_digit_to_selection()
        elif index_ == 2:
            self.set_number_format_percent_to_selection()
        elif index_ == 3:
            self.remove_number_format_from_selections()
        self._present_shape_properties()

    def set_number_format_whole_number_to_selection(self):
        self.set_whole_number(self.selected_accounts)

    def set_number_format_one_digit_to_selection(self):
        self.set_one_digit(self.selected_accounts)

    def set_number_format_two_digit_to_selection(self):
        self.set_two_digit(self.selected_accounts)

    def set_number_format_percent_to_selection(self):
        self.set_percent(self.selected_accounts)

    def remove_format_from_selections(self):
        self.remove_format(self.selected_accounts)

    def remove_number_format_from_selections(self):
        self.remove_number_format(self.selected_accounts)

    def set_format_heading(self, shape_ids: Iterable):
        for shape_id in shape_ids:
            self._format.mark_as_heading(shape_id)
        self._present_highlight_automatic(shape_ids)

    def set_format_sub_total(self, shape_ids: Iterable):
        for shape_id in shape_ids:
            self._format.mark_as_total(shape_id)
        self._present_highlight_automatic(shape_ids)

    def remove_format(self, shape_ids: Iterable):
        for shape_id in shape_ids:
            self._format.delete_format(shape_id)
        self._present_highlight_automatic(shape_ids)

    def set_whole_number(self, shape_ids: Iterable):
        for shape_id in shape_ids:
            self._number_format.mark_as_whole_number(shape_id)

    def set_one_digit(self, shape_ids: Iterable):
        for shape_id in shape_ids:
            self._number_format.mark_as_1_digit(shape_id)

    def set_two_digit(self, shape_ids: Iterable):
        for shape_id in shape_ids:
            self._number_format.mark_as_2_digit(shape_id)

    def set_percent(self, shape_ids: Iterable):
        for shape_id in shape_ids:
            self._number_format.mark_as_percent(shape_id)

    def remove_number_format(self, shape_ids: Iterable):
        for shape_id in shape_ids:
            self._number_format.delete_format(shape_id)

    # Macro
    def set_command_name(self, index_: int, command_name: str, selected_: tuple = ()):
        self.save_state_to_memory()
        if hasattr(self, command_name):
            self._commands.change_command_name(index_, command_name)
            self.present_commands(selected_)
        else:
            self._present_feedback_user(f'Method {command_name} does not exist.', 'error')

    def set_macro_args(self, index_: int, args_str: str, selected_: tuple = ()):
        args = imp9.parse_arg_str(args_str)
        self._commands.change_args(index_, args)
        self.present_commands(selected_)

    def set_macro_kwargs(self, index_: int, kwargs_str: str, selected_: tuple = ()):
        self._present_feedback_user('Not defined yet.')

    def merge_macro(self, file_name: str):
        self._gateways.merge_macro_file(file_name)
        self.present_commands()

    def save_macro(self, file_name: str):
        feedback = self._gateways.save_commands_to_file(file_name)
        self.clear_commands()
        self.present_macros()
        return feedback

    def present_macros(self, next_position: int = None):
        file_names = self.pickle_commands_file_names
        position = next_position or 0

        response_model = ResponseModel.response_model_to_presenter_update_macros
        if position >= len(file_names):
            position = len(file_names) - 1
        select_flags = tuple(position == i for i in range(len(file_names)))
        self._presenters.update_macros(response_model(file_names, select_flags))

    def start_macro_recording(self):
        self._commands.start_macro_recording()
        self.present_commands()

    def stop_macro_recording(self):
        self._commands.stop_macro_recording()
        self.present_commands()

    def add_command(self, key, args: tuple, kwargs: dict):
        self._commands.add_command(key, args, kwargs)
        self.present_commands()

    @property
    def commands(self) -> tuple:
        return self._commands.data

    def set_commands(self, data: tuple):
        self._commands.set_data(data)
        self.present_commands()

    @property
    def copied_commands(self) -> tuple:
        return self._copied_commands.data

    def copy_commands(self, indexes: tuple):
        commands = tuple(c for (n, c) in enumerate(self._commands.data) if n in indexes)
        self._copied_commands.set(commands)

    def paste_command(self, index_: int):
        commands = self._copied_commands.data
        self._commands.insert_commands(index_, commands)
        select = (index_,)
        self.present_commands(select)

    def delete_commands(self, indexes: tuple):
        self._commands.delete_commands(indexes)
        select = indexes
        number_of_commands = len(self.commands)
        if len(select) > 0:
            if number_of_commands <= max(select):
                select = (number_of_commands - 1,)
        self.present_commands(select)

    def clear_commands(self):
        original_macro_mode = self._commands.is_macro_recording_mode
        self._commands.clear_commands()
        self.stop_macro_recording()
        self.toggle_macro_mode(original_macro_mode)

    def toggle_macro_mode(self, value):
        if value:
            self.start_macro_recording()
        else:
            self.stop_macro_recording()

    def delete_macros(self, file_names: tuple, next_position=None):
        for file_name in file_names:
            self._gateways.remove_macro(file_name)
        self.present_macros(next_position)

    def delete_macro(self, file_name: str, next_position=None):
        feedback = self._gateways.remove_macro(file_name)
        if feedback != 'success':
            self._present_feedback_user(feedback, feedback)
            self.present_macros(next_position)

    def run_macro(self, observer_passed: Callable = None) -> tuple:
        self.stop_canvas_refreshing()
        self.stop_highlighting()

        def observer(no: int, total_n: int, command_name: str):
            self._present_feedback_user(f'{no}/{total_n} running {command_name}...', is_incremental_progress=True)

        observers = (observer, observer_passed) if observer_passed is not None else (observer,)
        succeeded, return_values_or_error = self._commands.run_macro(self, observers)

        self.start_canvas_refreshing()
        self.start_highlighting()
        self.present_refresh_canvas()
        if succeeded:
            return_values = return_values_or_error
            self._present_feedback_user('Macro completed!', 'success')
            return return_values
        else:
            n, key, args, kwargs, e = return_values_or_error
            message = f'Macro stopped due to error. No.:{n}, command:{key}, args:{args}, kwargs:{kwargs}, exception{e}'
            self._present_feedback_user(message, 'error')
            return ()

    @property
    def cleared_commands(self) -> bool:
        return self._commands.cleared_commands

    @property
    def is_macro_recording_mode(self) -> bool:
        return self._commands.is_macro_recording_mode

    @property
    def turned_off_macro_recording(self) -> bool:
        return self._commands.turned_off_macro_recording

    @property
    def turned_on_macro_recording(self) -> bool:
        return self._commands.turned_on_macro_recording

    def shift_multiple_commands(self, indexes: tuple, shift: int) -> tuple:
        destinations = self._commands.shift_multiple_commands(indexes, shift)
        self.present_commands()
        return destinations

    def present_commands(self, select: tuple = ()):
        select_flags = None
        if select != ():
            select_flags = tuple(i in select for i in range(len(self.commands)))
        response_model = ResponseModel.response_model_to_presenter_update_commands
        self._presenters.update_commands(response_model(self._commands.data, select_flags))

    # Spotlight
    @property
    def get_all_group_and_names(self) -> tuple:
        return spotlight.get_all_group_and_names_(self.pickle_commands_file_names, self._gateways.pickle_file_names)

    @property
    def get_list_of_templates(self) -> tuple:
        return tuple(d[1] for d in spotlight.get_templates(self._gateways.pickle_file_names))

    @property
    def gateway_out_methods(self) -> tuple:
        gateway_out_methods = (
            self.export_excel,
            self.save_data_table,
            self.save_all_to_file,
            self.save_state_to_file,
            self.save_macro
        )
        return gateway_out_methods

    def _set_entities(self, entities: Entities):
        """
        when adding new entity, make sure to update
        1) SystemState
        2) Erasing shapes
        3) Copying shapes
        4) AccountOrder negative list
        5) change_shape_id
        6) Clean Pickle
        """
        self._entities = entities
        self._shapes = entities.shapes
        self._rectangle = entities.rectangle_selector
        self._connections = entities.connections
        self._lines = entities.lines
        self._selections = entities.selections
        self._account_orders = entities.account_orders
        self._worksheets = entities.worksheets
        self._configurations = entities.configurations
        self._input_values = entities.input_values
        self._input_ranges = entities.input_ranges
        self._input_decimals = entities.input_decimals
        self._connection_ids = entities.connection_ids
        self._format = entities.format
        self._number_format = entities.number_format
        self._rpe = entities.rpe
        self._vertical_accounts = entities.vertical_accounts
        self._commands = entities.commands
        self._copied_commands = entities.copied_commands
        self._shape_format = entities.shape_format
        self._unit_of_measure = entities.unit_of_measure

    # Graph & Slider
    def _extract_account_or_relays_from_selection(self) -> tuple:
        shape_ids = self._selection.data
        return self._extract_account_or_relays_from_shape_ids(shape_ids)

    def _extract_account_or_relays_from_shape_ids(self, shape_ids) -> tuple:
        return tuple(i for i in shape_ids if self._shapes.get_tag_type(i) in ('account', 'relay'))

    def _update_graph_bars_and_live_values(self, data_table=None):
        if self.is_live_calculation_mode:
            if data_table is None:
                data_table = self.create_data_table()
            graph.update_bars(data_table, self._shapes, self._connections)
            self.update_live_values(data_table)

    # Slider
    def add_slider_of_selected_input_accounts(self):
        selected_inputs = tuple(sorted(self._get_selected_inputs_or_their_relays()))
        self.clear_selection()
        if selected_inputs == ():
            self._add_empty_slider()
        else:
            self._add_slider_of_selected_input_accounts(selected_inputs)
        self.present_refresh_canvas()

    def _get_selected_inputs_or_their_relays(self) -> tuple:
        input_accounts = self.input_accounts
        input_relays = ()
        for input_id in input_accounts:
            input_relays += tuple(self._shapes.get_relays(input_id))
        selected_inputs = tuple(i for i in self._selection.data if i in input_accounts + input_relays)
        return selected_inputs

    def _add_empty_slider(self, coordinate: tuple = (100, 100), min_max: tuple = (0, 100)) -> Any:
        slider_id = slider.add_slider(coordinate, min_max, self.add_new_shape, self._connections, self._shapes)
        self.present_refresh_canvas()
        return slider_id

    def _add_slider_of_selected_input_accounts(self, inputs_or_their_relays: tuple):
        shapes = self._shapes
        ir = self._input_ranges
        id_ = self._input_decimals
        connections = self._connections
        add_new_shape = self.add_new_shape
        i_or_r = inputs_or_their_relays

        slider_ids = slider.add_sliders_for_selected_inputs(i_or_r, add_new_shape, connections, ir, id_, shapes)
        new_relay_ids = self.add_relay_by_shape_ids(i_or_r)
        self.fit_shapes_width(new_relay_ids)
        for slider_id, relay_id in zip(slider_ids, new_relay_ids):
            imp9.place_a_shape_above_another(relay_id, slider_id, 30, shapes, connections)
            self._selection.add_selection(slider_id)

    # Graph
    def add_a_y_axis_of_selected_accounts(self, coordinate: tuple = (), min_max: tuple = None):
        account_ids = self._extract_account_or_relays_from_selection()
        self.clear_selection()
        graph_id = graph.add_y_axis(coordinate, min_max, self.add_new_shape, self._connections, self._shapes)
        self._selection.select_shape(graph_id)
        if account_ids != ():
            self.add_bars_of_selected_accounts(account_ids)
        else:
            self._add_an_empty_bar(graph_id)
        self._update_graph_bars_and_live_values()
        self.present_refresh_canvas()

    def _add_an_empty_bar(self, graph_id) -> Any:
        bar_id = graph.add_bar(graph_id, self.add_new_shape, self._shapes, self._connections)
        self._selection.add_selection(graph_id)
        return bar_id

    def add_bar_of_selected_accounts(self):
        account_ids = self._extract_account_or_relays_from_selection()
        self.add_bars_of_selected_accounts(account_ids)

    def add_bars_of_selected_accounts(self, account_or_relays: tuple):
        bar_ids_dict = {}
        new_bar_ids = []
        selected_y_axis = graph.get_selected_y_axis(self._selection.data, self._shapes, self._connections)
        for y_axis_id in selected_y_axis:
            bar_ids_dict[y_axis_id] = ()
            if account_or_relays != ():
                for _ in account_or_relays:
                    new_bar_id = graph.add_bar(y_axis_id, self.add_new_shape, self._shapes, self._connections)
                    bar_ids_dict[y_axis_id] += (new_bar_id,)
                    new_bar_ids.append(new_bar_id)
            else:
                new_bar_id = self._add_an_empty_bar(y_axis_id)
                bar_ids_dict[y_axis_id] += (new_bar_id,)
                new_bar_ids.append(new_bar_id)

        if not new_bar_ids:
            self._present_feedback_user('Select at least one graph', 'error')
            return

        all_new_relays = ()
        for y_axis_id in selected_y_axis:
            bar_ids = bar_ids_dict[y_axis_id]
            new_relay_ids = self.add_relay_by_shape_ids(account_or_relays)
            all_new_relays += new_relay_ids
            for bar_id, relay_id in zip(bar_ids, new_relay_ids):
                imp9.place_a_shape_above_another(relay_id, bar_id, 30, self._shapes, self._connections)
        self.add_shapes_to_selection(selected_y_axis + all_new_relays)
        self.fit_shapes_width(all_new_relays)

    # Live Value
    def add_live_values_of_selected_accounts(self, period=0):
        accounts = self._extract_account_or_relays_from_selection()
        self.clear_selection()
        for account_id in accounts:
            self.add_new_live_value(account_id, period)
        data_table = self.create_data_table()
        self.update_live_values(data_table)
        if len(accounts) == 0:
            self.feedback_user('Select at least one Account or its Relay', 'error')

    def add_new_live_value(self, shape_id, period: int = 0):
        lv_id = live_value.add_new_live_value(shape_id, period, self.add_new_shape, self._connections, self._shapes)
        data_table = self.create_data_table()
        shape_id = self._shapes.get_shape_it_represents_or_self(shape_id)
        string_value = live_value.get_value_str_for_live_value(shape_id, data_table, period, self._input_decimals)
        self._shapes.set_text(lv_id, string_value)
        self.present_refresh_canvas()

    def update_live_values(self, data_table: dict = None):
        if data_table is None:
            data_table = self.create_data_table()
        live_value_ids = self._shapes.get_shapes(live_value.tag_live_value)
        live_value.update_live_value(live_value_ids, data_table, self._shapes, self._connections, self._input_decimals)
        self.present_refresh_canvas_minimum()

    # Shape Format
    def set_fill_to_selection(self, color):
        for shape_id in self._selection.data:
            self.set_fill(shape_id, color)
        self.present_refresh_canvas()

    def remove_fill_of_selection(self):
        self.remove_fills(self._selection.data)
        self.present_refresh_canvas()

    def set_fill(self, shape_id, color):
        self._shape_format.set_fill(shape_id, color)

    def remove_fills(self, shape_ids):
        self._shape_format.remove_fills(shape_ids)

    # Output
    @property
    def output_rpe_raw(self) -> tuple:
        shapes = self._shapes
        positions = dict(zip(shapes.shapes_ids, (shapes.get_x(shape_id) for shape_id in shapes.shapes_ids)))
        operators = shapes.get_shapes('operator')
        rpes = self._rpe.get_rpes(self._connections.data, positions, operators)
        rpes = self._rpe.replace_rpe_element(rpes, self._relay_to_original_mapper)
        return rpes

    @property
    def rpe_raw_sorted(self) -> tuple:
        rpe_raw = self.output_rpe_raw
        formula_owners = tuple(rpe_[0] for rpe_ in rpe_raw)
        _, rpe_raw_sorted = Utilities.sort_lists(formula_owners, rpe_raw)
        return tuple(rpe_raw_sorted)

    @property
    def rpe_dictionary(self) -> dict:
        args = self.bb_rpes, self.output_rpe_raw, self._shapes.get_text, self._shapes.get_shapes('operator')
        return rpe.get_rpe_dictionary(*args)

    @property
    def _direct_links(self) -> tuple:
        return imp9.get_direct_links(self._connections, self._relay_to_original_mapper, self._shapes, self._bb_shift)

    @property
    def _relay_to_original_mapper(self) -> dict:
        relays = self._shapes.get_shapes('relay')
        originals = tuple(self._shapes.get_shape_it_represents(shape_id) for shape_id in relays)
        mapper = dict(zip(relays, originals))
        return mapper

    @property
    def output_rpe_readable(self) -> tuple:
        s = self._shapes
        texts = dict(zip(s.shapes_ids, tuple(s.get_text(shape_id) for shape_id in s.shapes_ids)))
        return self._rpe.get_rpe_readable(self.output_rpe_raw, texts)

    @property
    def output_worksheet_information(self) -> dict:
        worksheet_information = {}
        for sheet_name in self._worksheets.sheet_names:
            account_order = self._account_orders.get_account_order(sheet_name)
            worksheet_information[sheet_name] = account_order.data
        return worksheet_information

    # Gateway Spreadsheet
    def plug_in_gateway_spreadsheet(self, cls_spreadsheet_gateway: Type[SpreadsheetABC]):
        self._spreadsheet = cls_spreadsheet_gateway()

    def _clear_spreadsheet_state(self):
        self.plug_in_gateway_spreadsheet(self._spreadsheet.__class__)

    def export_excel(self, file_name: str = None, path: str = None):
        gateway_model = self.create_gateway_model_to_spreadsheet(file_name, path)
        feedback = self._spreadsheet.export(**gateway_model)
        self._clear_spreadsheet_state()
        if feedback == ():
            self._present_feedback_user('Excel successfully saved', 'success')

            if self.sensitivity_sheet_added:
                file_path = os.path.join(self.save_path, self._configurations.command_file_name)
                self.open_file(file_path)
        else:
            self._present_feedback_user(str(feedback), 'error')

    def open_file(self, file_path: str):
        self._gateways.open_file(file_path)

    def _get_arguments_to_spreadsheet_udf(self, dependencies: set) -> tuple:
        circular_safe_accounts = imp9.get_circular_reference_free_accounts(self._connections, self._shapes)
        arguments = []
        for arg in circular_safe_accounts:
            if self._shapes.get_tag_type(arg) in ('account',):
                if arg in dependencies:
                    arguments.append(vba_udf.shape_id_to_vba_variable_name(arg, self._shapes))
        return tuple(sorted(arguments))

    def create_gateway_model_to_spreadsheet(self, file_name: str = None, path: str = None) -> dict:
        # FMDesigner's gateway model to FMSpreadsheet = FMSpreadsheet's request_model
        if self._spreadsheet is None:
            self.feedback_user('Spreadsheet gateway is not plugged in.', 'error')
        shape_ids = self._shapes.shapes_ids
        path = self.save_path if path is None else path
        workbook_name = f'{path}/{file_name if file_name is not None else "Excel.xlsx"}'.replace('//', '/')
        shape_id_to_text = dict(zip(shape_ids, self._get_texts_of_shapes(shape_ids)))

        input_accounts = self.input_accounts
        number_of_periods = nop = self.number_of_periods
        self.set_default_input_values_if_values_not_set()
        input_values = tuple(self._input_values.get_values(input_account)[:nop] for input_account in input_accounts)
        operator_ids = self._shapes.get_shapes('operator')
        constant_ids = self._shapes.get_shapes('constant')
        worksheets_data = self.output_worksheet_information
        rpes = self.output_rpe_raw
        direct_links = self._direct_links

        gateway_model = {
            'workbook_name': workbook_name,
            'shape_id_to_address': shape_id_to_text,
            'inputs': input_accounts,
            'input_values': input_values,
            'operators': operator_ids,
            'constants': constant_ids,
            'sheets_data': worksheets_data,
            'rpes': rpes,
            'nop': number_of_periods,
            'direct_links_mutable': direct_links,
            'format_data': self._format.data,
            'number_format_data': self._number_format.data,
            'vertical_acs': self._vertical_accounts.data,
            'vba_file': self._gateways.get_vba_binary(),
            'shape_id_to_uom': self._unit_of_measure.data,
        }

        if self.sensitivity_sheet_added:
            gateway_model.update({
                'add_sensitivity_sheet': True,
                'target_accounts': self._configurations.sensitivity_target_accounts,
                'selected_variables': self._configurations.sensitivity_variable_accounts,
                'shape_id_to_delta': self._configurations.get_account_ids_to_deltas(input_accounts),
                'command_file_name': self._configurations.command_file_name,
            })

        if self._configurations.insert_sheet_name_in_input_sheet:
            gateway_model.update({'insert_sheet_name': True})

        selection_data = self._selection.data
        if len(selection_data) == 1:
            account_id = tuple(selection_data)[0]
            if self.is_circular(account_id):
                minimum_circular_dependencies = self.get_minimum_circular_dependencies(account_id)
                account_used_in_udf = self._get_accounts_used_in_user_defined_function(minimum_circular_dependencies)
                user_defined_function = {
                    'name': 'user_defined_function',
                    'account_ids': account_id,
                    'arguments': self._get_arguments_to_vba_udf(account_used_in_udf),
                }
                gateway_model['user_defined_function'] = user_defined_function

        return gateway_model

    # Calculation
    def plug_in_calculator(self, cls_calculator: Type[CalculatorABC]):
        self._calculator = cls_calculator()

    def create_calculation_gateway_model(self):
        inputs = self.input_accounts
        constants = self._shapes.get_shapes('constant')
        input_values = tuple(self._input_values.get_values(input_id) for input_id in inputs)
        input_values_dictionary = dict(zip(inputs, input_values))
        constant_values = tuple(float(self._shapes.get_text(c).replace(',', '')) for c in constants)
        gateway_model = {
            'account_ids': self._shapes.get_shapes('account'),
            'input_values': input_values_dictionary,
            'rpes': self.rpe_dictionary,
            'calculation_order': self.get_calculation_order(),
            'constants_to_values': dict(zip(constants, constant_values)),
            'direct_links': self._direct_links,
            'vertical_accounts': self._vertical_accounts.data,
            'number_of_periods': self.number_of_periods,
        }
        return gateway_model

    def get_calculation_order(self) -> tuple:
        topological_order = imp9.get_topological_order(self._shapes, self._connections)
        lower_level_accounts = []
        for shape_id in topological_order:
            if self._shapes.get_tag_type(shape_id) == 'account':
                account_id = shape_id
                if account_id not in lower_level_accounts:
                    lower_level_accounts.append(account_id)
        return tuple(lower_level_accounts)

    def save_data_table(self, file_name):
        file_path = os.path.join(self.save_path, file_name)
        data_table = self.create_data_table()

        def get_key(id_) -> tuple:
            return id_, self._shapes.get_text(id_), self._worksheets.get_worksheet_of_an_account(id_)

        keys = tuple(get_key(i) for i in data_table.keys())
        values = tuple(tuple(d.values()) for d in data_table.values())
        self._spreadsheet.save_dictionary_as_spreadsheet(file_path, dict(zip(keys, values)))
        self._present_feedback_user(f'Saved Calculation DataTable to {file_path}')

    def calculate(self):
        data_table = self.create_data_table()
        self._update_graph_bars_and_live_values(data_table)

    def create_data_table(self):
        gateway_model = self.create_calculation_gateway_model()
        data_table = self._calculator.create_data_table(gateway_model)

        self.__clear_calculator()
        return data_table

    def __clear_calculator(self):
        self.plug_in_calculator(self._calculator.__class__)

    @property
    def bb_rpes(self) -> dict:
        return rpe.get_bb_rpes(self._connections, self._relay_to_original_mapper, self._shapes, self._bb_shift)

    # Gateway VBA user defined function
    def plug_in_vba_user_defined_function_builder(self, cls_vba_udf_gateway: Type[UDFBuilderABC]):
        self._vba_udf_builder = cls_vba_udf_gateway()

    def _clear_vba_udf_builder(self):
        self.plug_in_vba_user_defined_function_builder(self._vba_udf_builder.__class__)

    def _get_arguments_to_vba_udf(self, accounts_in_udf: Iterable, argument_converter: Callable = None) -> tuple:
        return vba_udf.get_arguments_to_vba_udf(accounts_in_udf, argument_converter, self._connections, self._shapes)

    def _get_accounts_used_in_user_defined_function(self, dependencies: Iterable) -> set:
        return vba_udf.get_accounts_used_in_user_defined_function(dependencies, self.rpe_raw_sorted, self._shapes)

    def create_gateway_model_for_vba_uda(self, shape_id, file_name: str = None):
        return vba_udf.create_gateway_model(self._connections, self._direct_links, file_name,
                                            self.get_minimum_circular_dependencies(shape_id),
                                            self.rpe_raw_sorted, shape_id, self._shapes)

    def export_vba_user_defined_function(self, file_name: str):
        if self._vba_udf_builder is None:
            self.feedback_user('VBA UDF builder gateway is not plugged in.', 'error')
            return

        selected_data = tuple(self._selection.data)
        if len(selected_data) != 1:
            self._present_feedback_user('Only select one account within circular reference.', 'error')
            return

        shape_id = selected_data[0]
        if len(self.get_minimum_circular_dependencies(shape_id)) == 0:
            message = f'{shape_id}/{self._shapes.get_text(shape_id)} is not in circular reference.'
            self._present_feedback_user(message, 'error')
            return

        gateway_model = self.create_gateway_model_for_vba_uda(shape_id, file_name)
        self._vba_udf_builder.export(**gateway_model)
        self._clear_vba_udf_builder()
        self._present_feedback_user('VBA User Defined Function copied to clipboard.', 'success')

    # KeyMap
    def plug_in_keymaps(self, keymaps: Type[KeyMapsABC]):
        self._keymaps = keymaps()

    def register_all_keyboard_shortcuts(self, key_combos_dictionary: dict):
        for name, key_combos in key_combos_dictionary.items():
            self.load_keyboard_shortcut(name, key_combos)

    def load_keyboard_shortcut(self, name: str, key_combos: dict):
        self.change_active_keymap(name)
        self.set_keyboard_shortcuts(key_combos)

    def set_keyboard_shortcuts(self, key_combos):
        for key_combo, command in key_combos.items():
            self.add_new_keyboard_shortcut(key_combo, command)

    def change_active_keymap(self, keymap_name):
        if self._keymaps is not None:
            self._keymaps.set_active_keymap(keymap_name)

    @property
    def active_keymap(self) -> KeyMapABC:
        return self._keymaps.active_keymap

    def add_new_keyboard_shortcut(self, key_combo, command):
        self.active_keymap.add_new_keyboard_shortcut(key_combo, command)

    def keyboard_shortcut_handler(self, modifiers: int, key: str):
        command, feedback = self.active_keymap.get_command_and_feedback((modifiers, key))
        if command is not None:
            self.feedback_user(f'[{modifiers}-{key}]: {feedback}')
            command()
        else:
            self.feedback_user(f'[{modifiers}-{key}]: {feedback}')

    def keyboard_shortcut_handler_silent(self, modifiers: int, key: str):
        # For Popups that has own status_bar / user_feed_back, handler is expected to be silent (don't feedback user)
        command, feedback = self.active_keymap.get_command_and_feedback((modifiers, key))
        if command is not None:
            self.feedback_user(f'[{modifiers}-{key}]: {feedback}')
            command()

    # Save as Pickle
    def save_any_data_as_pickle(self, file_name_abs_path, data):
        self._gateways.save_object_as_pickle(file_name_abs_path, data)

    def get_pickle_from_file_system(self, abs_path):
        return self._gateways.get_pickle_from_file_system(abs_path)

    # Save Canvas
    def plug_in_canvas_image_saver(self, image_saver: Callable):
        self._canvas_image_saver = image_saver

    def save_slider_images(self, number_of_images, travel_range, direction):
        y_range = travel_range
        delta = direction * y_range / (number_of_images - 1)
        for i in range(number_of_images):
            self.move_selections(0, delta)
            self.present_refresh_canvas()
            self._present_feedback_user(f'Canvas saving {i + 1}/{number_of_images}', is_incremental_progress=True)
            self.save_canvas_as_image(f'canvas_images/canvas_{i}.ps')
        self._present_feedback_user(f'Canvas saved!', 'success')

    def save_canvas_as_image(self, file_name):
        path = self.save_path
        try:
            self._canvas_image_saver(f'{path}/{file_name}')
        except TypeError:
            pass

    # Caching
    def clear_all_cache(self):
        self.clear_cache_audit_results()
        self.clear_cache_slider()

    def cache_audit_results(self):
        self._cache.set_cache_audit_results(self._get_audit_results(self._get_minimum_shape_ids_to_update()))
        self._cache.set_connection_model(self._create_response_model_for_presenter_connection())
        self.feedback_user('Cached.', 'success')

    def clear_cache_audit_results(self):
        self._cache.clear_audit_results()
        self._cache.clear_connection_model()

    def cache_slider(self):
        selected_shapes = self._selection.data
        if selected_shapes != set():
            args = slider.create_args_to_cache_data_table(selected_shapes, self._connections, self._shapes)
            self.cache_data_table(*args)
        else:
            self.feedback_user('Select a slider', 'error')

    def update_data_table_upon_slider_action(self, handle_ids: tuple):
        key = caching.get_data_table_cache_key_from_handle_ids(handle_ids, self._connections, self._shapes)
        dt = caching.get_data_table_from_cache(key, self._cache.cache_data_table, self.feedback_user)
        self._update_graph_bars_and_live_values(dt)

    def cache_data_table(self, input_ids: tuple, input_values: tuple):
        cache = {}
        total_steps = len(input_values)
        input_id = input_ids[0]
        for n, input_value in enumerate(input_values):
            key = input_id, input_value
            self.set_same_input_values(input_id, input_value)
            data_table = self.create_data_table()
            cache[key] = data_table
            self._present_feedback_user(f'Caching {n}/{total_steps}', is_incremental_progress=True)
        self._present_feedback_user(f'Caching complete!', 'success')
        self._cache.set_cache_data_table(cache)

    def clear_cache_slider(self):
        self._cache.clear_cache_data_table()
