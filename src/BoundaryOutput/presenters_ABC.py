from abc import ABC
from abc import abstractmethod
from typing import Callable


class PresentersABC(ABC):
    @abstractmethod
    def attach_to_response_model_receiver(self, observer: Callable):
        pass

    @abstractmethod
    def attach_to_add_shape(self, observer):
        pass

    @abstractmethod
    def attach_to_connect_shapes(self, observer):
        pass

    @abstractmethod
    def attach_to_highlight_shape(self, observer):
        pass

    @abstractmethod
    def attach_to_move_shapes(self, observer):
        pass

    @abstractmethod
    def attach_to_draw_rectangle(self, observer):
        pass

    @abstractmethod
    def attach_to_remove_shape(self, observer):
        pass

    @abstractmethod
    def attach_to_draw_line(self, observer):
        pass

    @abstractmethod
    def attach_to_update_status_bar(self, observer):
        pass

    @abstractmethod
    def attach_to_clear_canvas(self, observer):
        pass

    @abstractmethod
    def attach_to_load_pickle_files_list(self, observer):
        pass

    @abstractmethod
    def attach_to_update_account_order(self, observer):
        pass

    @abstractmethod
    def attach_to_update_shape_properties(self, observer):
        pass

    @abstractmethod
    def attach_to_present_states(self, observer):
        pass

    @abstractmethod
    def attach_to_present_worksheets(self, observer):
        pass

    @abstractmethod
    def attach_to_present_show_input_entry(self, observer):
        pass

    @abstractmethod
    def attach_to_present_update_connection_ids(self, observer):
        pass

    @abstractmethod
    def attach_to_present_update_commands(self, observer):
        pass

    @abstractmethod
    def attach_to_present_update_macros(self, observer):
        pass

    @abstractmethod
    def attach_to_present_update_sensitivity_input_accounts(self, observer):
        pass

    @abstractmethod
    def attach_to_present_update_sensitivity_accounts(self, observer):
        pass

    @abstractmethod
    def attach_to_present_update_sensitivity_target_accounts(self, observer):
        pass

    @abstractmethod
    def attach_to_present_update_data_table_accounts(self, observer):
        pass

    @abstractmethod
    def attach_to_present_update_data_table_target_accounts(self, observer):
        pass

    @abstractmethod
    def attach_to_present_update_sensitivity_variable_accounts(self, observer):
        pass

    @abstractmethod
    def attach_to_present_update_data_table_variable_accounts(self, observer):
        pass

    @abstractmethod
    def attach_to_present_insert_sheet_name_in_input_sheet(self, observer):
        pass

    @abstractmethod
    def attach_to_present_add_worksheet(self, observer):
        pass

    @abstractmethod
    def attach_to_present_select_worksheet(self, observer):
        pass

    @abstractmethod
    def attach_to_present_delete_worksheet(self, observer):
        pass

    @abstractmethod
    def add_shape(self, response_model):
        pass

    @abstractmethod
    def connect_shapes(self, response_model):
        pass

    @abstractmethod
    def highlight_shape(self, response_model):
        pass

    @abstractmethod
    def move_shapes(self, response_model):
        pass

    @abstractmethod
    def draw_rectangle(self, response_model):
        pass

    @abstractmethod
    def remove_shape(self, response_model):
        pass

    @abstractmethod
    def draw_line(self, response_model):
        pass

    @abstractmethod
    def feedback_user(self, response_model):
        pass

    @abstractmethod
    def clear_canvas(self, response_model=None):
        pass

    @abstractmethod
    def load_pickle_files_list(self, response_model):
        pass

    @abstractmethod
    def update_account_order(self, response_model):
        pass

    @abstractmethod
    def update_shape_properties(self, response_model):
        pass

    @abstractmethod
    def present_states(self, response_model):
        pass

    @abstractmethod
    def update_worksheets(self, response_model):
        pass

    @abstractmethod
    def show_input_entry(self, response_model):
        pass

    @abstractmethod
    def update_connection_ids(self, response_model):
        pass

    @abstractmethod
    def update_commands(self, response_model):
        pass

    @abstractmethod
    def update_macros(self, response_model):
        pass

    @abstractmethod
    def update_sensitivity_input_list(self, response_model):
        pass

    @abstractmethod
    def update_sensitivity_account_list(self, response_model):
        pass

    @abstractmethod
    def update_data_table_account_list(self, response_model):
        pass

    @abstractmethod
    def update_sensitivity_target_accounts(self, response_model):
        pass

    @abstractmethod
    def update_data_table_target_accounts(self, response_model):
        pass

    @abstractmethod
    def update_sensitivity_variable_accounts(self, response_model):
        pass

    @abstractmethod
    def update_data_table_variable_accounts(self, response_model):
        pass

    @abstractmethod
    def insert_sheet_name_in_input_sheet(self, response_model):
        pass

    @abstractmethod
    def add_worksheet(self, response_model):
        pass

    @abstractmethod
    def select_worksheet(self, response_model):
        pass

    @abstractmethod
    def delete_work_sheet(self, response_model):
        pass
