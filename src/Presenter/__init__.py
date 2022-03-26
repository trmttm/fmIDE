from typing import Callable

from .AddShape import PresenterAddShape
from .AddWorksheet import PresenterAddWorksheet
from .ClearCanvas import PresenterClearCanvas
from .Commands import PresenterCommands
from .ConnectShape import PresenterConnectShape
from .DeleteWorksheet import PresenterDeleteWorksheet
from .DrawLine import PresenterDrawLine
from .DrawRectangle import PresenterDrawRectangle
from .FeedbackUser import PresenterFeedbackUser
from .HighlightShape import PresenterHighlightShape
from .InputEntry import PresenterInputEntry
from .LoadPickleFilesList import PresenterLoadPickleFilesList
from .Macros import PresenterMacros
from .MoveShape import PresenterMoveShape
from .PresenterPassThrough import PresenterPassThrough
from .RemoveShape import PresenterRemoveShape
from .SelectWorksheet import PresenterSelectWorksheet
from .States import PresenterStates
from .Template import PresenterTemplate
from .UpdateAccountOrder import PresenterUpdateAccountOrder
from .UpdateAccountsList import PresenterAccountsList
from .UpdateAccountsListWithDeltas import PresenterAccountsListWithDeltas
from .UpdateConnectionIDs import PresenterUpdateConnectionIDs
from .UpdateShapeProperties import PresenterUpdateShapeProperties
from .Worksheets import PresenterWorksheets
from ..BoundaryOutput import PresentersABC


class Presenters(PresentersABC):

    def __init__(self):
        self._is_on = True

        self._add_shape = PresenterAddShape()
        self._connect_shapes = PresenterConnectShape()
        self._highlight_shape = PresenterHighlightShape()
        self._move_shapes = PresenterMoveShape()
        self._draw_rectangle = PresenterDrawRectangle()
        self._remove_shape = PresenterRemoveShape()
        self._draw_line = PresenterDrawLine()
        self._feedback_user = PresenterFeedbackUser()
        self._clear_canvas = PresenterClearCanvas()
        self._load_pickle_files_list = PresenterLoadPickleFilesList()
        self._update_account_order = PresenterUpdateAccountOrder()
        self._update_shape_properties = PresenterUpdateShapeProperties()
        self._present_states = PresenterStates()
        self._present_worksheets = PresenterWorksheets()
        self._present_input_entry = PresenterInputEntry()
        self._present_connection_ids = PresenterUpdateConnectionIDs()
        self._present_commands = PresenterCommands()
        self._present_macros = PresenterMacros()
        self._present_sensitivity_input_accounts = PresenterAccountsList()
        self._present_sensitivity_accounts = PresenterAccountsList()
        self._present_data_table_accounts = PresenterAccountsList()
        self._present_sensitivity_target_accounts = PresenterAccountsList()
        self._present_data_table_target_accounts = PresenterAccountsList()
        self._present_sensitivity_variable_accounts = PresenterAccountsListWithDeltas()
        self._present_data_table_variable_accounts = PresenterAccountsList()
        self._present_insert_sheet_name_in_input_sheet = PresenterPassThrough()
        self._present_add_worksheet = PresenterAddWorksheet()
        self._present_select_worksheet = PresenterSelectWorksheet()
        self._present_delete_worksheet = PresenterDeleteWorksheet()

        self._observers = []

    def attach_to_response_model_receiver(self, observer: Callable):
        self._observers.append(observer)

    def _notify(self, response_model):
        for observer in self._observers:
            observer(response_model)

    def attach_to_add_shape(self, observer):
        return self._add_shape.attach(observer)

    def attach_to_connect_shapes(self, observer):
        return self._connect_shapes.attach(observer)

    def attach_to_highlight_shape(self, observer):
        return self._highlight_shape.attach(observer)

    def attach_to_move_shapes(self, observer):
        return self._move_shapes.attach(observer)

    def attach_to_draw_rectangle(self, observer):
        return self._draw_rectangle.attach(observer)

    def attach_to_remove_shape(self, observer):
        return self._remove_shape.attach(observer)

    def attach_to_draw_line(self, observer):
        return self._draw_line.attach(observer)

    def attach_to_update_status_bar(self, observer):
        return self._feedback_user.attach(observer)

    def attach_to_clear_canvas(self, observer):
        return self._clear_canvas.attach(observer)

    def attach_to_load_pickle_files_list(self, observer):
        self._load_pickle_files_list.attach(observer)

    def attach_to_update_account_order(self, observer):
        self._update_account_order.attach(observer)

    def attach_to_update_shape_properties(self, observer):
        self._update_shape_properties.attach(observer)

    def attach_to_present_states(self, observer):
        self._present_states.attach(observer)

    def attach_to_present_worksheets(self, observer):
        self._present_worksheets.attach(observer)

    def attach_to_present_show_input_entry(self, observer):
        self._present_input_entry.attach(observer)

    def attach_to_present_update_connection_ids(self, observer):
        self._present_connection_ids.attach(observer)

    def attach_to_present_update_commands(self, observer):
        self._present_commands.attach(observer)

    def attach_to_present_update_macros(self, observer):
        self._present_macros.attach(observer)

    def attach_to_present_update_sensitivity_input_accounts(self, observer):
        self._present_sensitivity_input_accounts.attach(observer)

    def attach_to_present_update_sensitivity_accounts(self, observer):
        self._present_sensitivity_accounts.attach(observer)

    def attach_to_present_update_sensitivity_target_accounts(self, observer):
        self._present_sensitivity_target_accounts.attach(observer)

    def attach_to_present_update_data_table_accounts(self, observer):
        self._present_data_table_accounts.attach(observer)

    def attach_to_present_update_data_table_target_accounts(self, observer):
        self._present_data_table_target_accounts.attach(observer)

    def attach_to_present_update_sensitivity_variable_accounts(self, observer):
        self._present_sensitivity_variable_accounts.attach(observer)

    def attach_to_present_update_data_table_variable_accounts(self, observer):
        self._present_data_table_variable_accounts.attach(observer)

    def attach_to_present_insert_sheet_name_in_input_sheet(self, observer):
        self._present_insert_sheet_name_in_input_sheet.attach(observer)

    def attach_to_present_add_worksheet(self, observer):
        self._present_add_worksheet.attach(observer)

    def attach_to_present_select_worksheet(self, observer):
        self._present_select_worksheet.attach(observer)

    def attach_to_present_delete_worksheet(self, observer):
        self._present_delete_worksheet.attach(observer)

    def add_shape(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._add_shape.present(response_model)

    def connect_shapes(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._connect_shapes.present(response_model)

    def highlight_shape(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._highlight_shape.present(response_model)

    def move_shapes(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._move_shapes.present(response_model)

    def draw_rectangle(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._draw_rectangle.present(response_model)

    def remove_shape(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._remove_shape.present(response_model)

    def draw_line(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._draw_line.present(response_model)

    def feedback_user(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._feedback_user.present(response_model)

    def clear_canvas(self, response_model=None):
        if self._is_on:
            self._notify(response_model)
            self._clear_canvas.present()

    def load_pickle_files_list(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._load_pickle_files_list.present(response_model)

    def update_account_order(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._update_account_order.present(response_model)

    def update_shape_properties(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._update_shape_properties.present(response_model)

    def present_states(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_states.present(response_model)

    def update_worksheets(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_worksheets.present(response_model)

    def show_input_entry(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_input_entry.present(response_model)

    def update_connection_ids(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_connection_ids.present(response_model)

    def update_commands(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_commands.present(response_model)

    def update_macros(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_macros.present(response_model)

    def update_sensitivity_input_list(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_sensitivity_input_accounts.present(response_model)

    def update_sensitivity_account_list(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_sensitivity_accounts.present(response_model)

    def update_data_table_account_list(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_data_table_accounts.present(response_model)

    def update_sensitivity_target_accounts(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_sensitivity_target_accounts.present(response_model)

    def update_data_table_target_accounts(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_data_table_target_accounts.present(response_model)

    def update_sensitivity_variable_accounts(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_sensitivity_variable_accounts.present(response_model)

    def update_data_table_variable_accounts(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_data_table_variable_accounts.present(response_model)

    def insert_sheet_name_in_input_sheet(self, response_model):
        if self._is_on:
            self._notify(response_model)
            self._present_insert_sheet_name_in_input_sheet.present(response_model)

    def add_worksheet(self, response_model):
        self._notify(response_model)
        self._present_add_worksheet.present(response_model)

    def select_worksheet(self, response_model):
        self._notify(response_model)
        self._present_select_worksheet.present(response_model)

    def delete_work_sheet(self, response_model):
        self._notify(response_model)
        self._present_delete_worksheet.present(response_model)

    def turn_off(self):
        self._is_on = False

    def turn_on(self):
        self._is_on = True

    @property
    def is_on(self) -> bool:
        return self._is_on
