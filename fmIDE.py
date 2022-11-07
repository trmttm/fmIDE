from typing import Callable
from typing import Tuple
from typing import Union

from fm_calculator import Calculator
from interface_view import ViewABC
from keyboard_shortcut import KeyMaps
from spreadsheet import Spreadsheet
from src.EntityGateway import GateWays
from src.ExternalSystems.Configurations import ConfigurationTest
from src.ExternalSystems.UserDefinedFunction import UDFBuilder
from src.Main import Main
from view_tkinter import View


def instantiate_app():
    config = ConfigurationTest()
    view = View()
    app = Main(config, view, GateWays)
    app.interactor.plug_in_gateway_spreadsheet(Spreadsheet)
    app.interactor.plug_in_vba_user_defined_function_builder(UDFBuilder)
    app.interactor.plug_in_calculator(Calculator)
    app.interactor.plug_in_canvas_image_saver(view.save_canvas_as_an_image)

    app.interactor.plug_in_keymaps(KeyMaps)
    app.interactor.register_all_keyboard_shortcuts(app.default_keyboard_shortcuts)
    app.view.set_keyboard_shortcut_handler_to_root(app.interactor.keyboard_shortcut_handler)
    app.interactor.change_active_keymap('Design')
    return app


def clean_command_pickles():
    app = instantiate_app()
    files = app.interactor.pickle_commands_file_names
    for file in files:
        try:
            app.interactor.clear_commands()
            app.interactor.merge_macro(file)
            app.interactor.save_macro(file)
            print(file)
        except:
            print(f'Error!! {file}')
    app.quit()


def clean_template_pickles():
    app = instantiate_app()
    files = app.interactor.get_pickle_file_names([])
    for file in files:
        try:
            app.interactor.reset()
            app.interactor.merge_file(file)
            app.interactor.save_state_to_file(file)
            print(file)
        except:
            print(f'Error!! {file}')
    app.quit()


class EmptyView(ViewABC):

    def attach_to_event_upon_closing(self, observer):
        pass

    def add_text_box(self, view_model: list):
        pass

    def add_rectangle(self, view_model: dict):
        pass

    def add_text(self, view_model: dict):
        pass

    def remove_shape(self, view_model: list):
        pass

    def connect_shapes(self, view_model: dict):
        pass

    def move_shapes(self, view_model: dict):
        pass

    def move_lines(self, view_model: dict):
        pass

    def add_widgets(self, view_model: Union[list, tuple]):
        pass

    def highlight_shapes(self, view_model: dict):
        pass

    def draw_rectangle(self, view_model: dict):
        pass

    def set_border_color(self, view_model: dict):
        pass

    def set_text_value(self, view_model: dict):
        pass

    def set_text_color(self, view_model: dict):
        pass

    def set_font_size(self, view_model: dict):
        pass

    def set_border_width(self, view_model: dict):
        pass

    def set_line_width(self, view_model: dict):
        pass

    def set_line_arrow(self, view_model: dict):
        pass

    def set_fill_color(self, view_model: dict):
        pass

    def add_line(self, view_model: dict):
        pass

    def draw_line(self, view_model: dict):
        pass

    def get_value(self, widget_id):
        pass

    def set_combobox_values(self, widget_id, values: tuple):
        pass

    def set_values(self, widget_ids: tuple, values: tuple):
        pass

    def set_value(self, widget_id, value):
        pass

    def get_mouse_coordinates_captured(self, event) -> Tuple[int, int]:
        return (0, 0)

    def widget_exists(self, widget_id) -> bool:
        return True

    def remove_widget(self, widget_id):
        pass

    def clear_frame(self, frame_id):
        pass

    def get_mouse_canvas_coordinate(self) -> tuple:
        return (0, 0)

    def set_text(self, widget_id, text: str):
        pass

    def update(self):
        pass

    @property
    def focused_widget(self) -> str:
        return ''

    def focus(self, widget_id, **kwargs):
        pass

    def launch_app(self):
        pass

    def bind_command_to_widget(self, widget_id, command):
        pass

    def unbind_command_from_widget(self, widget_id):
        pass

    def bind_entry_update(self, entry_id, command):
        pass

    def switch_status_bar(self, status_bar_id):
        pass

    def update_status_bar(self, view_model: dict):
        pass

    def clear_canvas(self, view_model: dict = None):
        pass

    def switch_frame(self, widget_id):
        pass

    def switch_canvas(self, canvas_id):
        pass

    @property
    def current_tree(self):
        pass

    def set_tree_headings(self, tree_id: str, headings: Tuple[str, ...]):
        pass

    def get_all_tree_values(self, tree_id=None):
        pass

    def switch_tree(self, tree_id):
        pass

    def update_tree(self, view_model):
        pass

    def tree_focused_values(self, tree_id) -> tuple:
        return (0, 1)

    def tree_selected_values(self, tree_id=None) -> tuple:
        return ()

    def get_selected_tree_item_indexes(self, tree_id) -> tuple:
        return ()

    def select_multiple_tree_items(self, tree_id=None, indexes=()):
        pass

    def tree_number_of_items(self, tree_id=None) -> int:
        return 0

    def select_tree_top_items_after_deleting_items(self, indexes: tuple, tree_id=None):
        pass

    def set_title(self, title: str):
        pass

    def change_window_size(self, width=600, height=900):
        pass

    def set_exception_catcher(self, callback: Callable):
        pass

    @property
    def current_canvas(self):
        pass

    def scroll_canvas(self, x, y):
        pass

    def save_canvas_as_an_image(self, file_name):
        pass

    def get_canvas_width(self) -> float:
        return 0

    def get_canvas_height(self) -> float:
        return 0

    def bind_change_canvas_size(self, call_back: Callable, canvas_id=None):
        pass

    def clear_canvas_shapes_by_tag(self, tag):
        pass

    def get_widget(self, widget_id):
        pass

    @staticmethod
    def close(widget_id):
        pass

    def quit(self):
        pass

    def get_mid_y_coordinates_of_all_rectangles_on_canvas(self):
        pass

    def move_item_vertically_within_range(self, item, delta_x, delta_y, y_range: tuple):
        pass

    def get_clicked_rectangle(self):
        pass

    @staticmethod
    def ask_color(title='Choose color') -> str:
        return 'red'

    def bind_tree_left_click(self, command: Callable, tree_id=None):
        pass

    def bind_tree_right_click(self, command: Callable, tree_id=None):
        pass

    def bind_tree_middle_click(self, command: Callable, tree_id=None):
        pass

    def bind_tree_left_click_release(self, command: Callable, tree_id=None):
        pass

    def bind_tree_right_click_release(self, command: Callable, tree_id=None):
        pass

    def bind_tree_middle_click_release(self, command: Callable, tree_id=None):
        pass

    def deselect_tree_items(self, tree_id=None):
        pass

    def select_folder(self, initialdir=None):
        pass

    def ask_yes_no(self, title, message) -> bool:
        return False

    def select_save_file(self, initialdir=None, initialfile=''):
        pass

    def select_open_file(self, initialdir=None):
        pass

    def update_menu_bar(self, menu_bar_model: dict, toplevel_id=None):
        pass

    def set_keyboard_shortcut_handler_to_root(self, keyboard_shortcut_handler: Callable):
        pass

    def set_keyboard_shortcut_handler(self, widget_id, keyboard_shortcut_handler: Callable):
        pass

    def set_paned_window_sash_position(self, paned_window_id, new_position: int):
        pass

    def get_paned_window_sash_position(self, paned_window_id) -> int:
        return 0

    def set_foreground_color(self, widget_id, color: str):
        pass


def main():
    app = instantiate_app()
    app.run()


if __name__ == '__main__':
    main()
