from fm_calculator import Calculator
from keyboard_shortcut import KeyMaps
from spreadsheet import Spreadsheet
from view_tkinter import View

from src.EntityGateway import GateWays
from src.ExternalSystems.Configurations import ConfigurationTest
from src.ExternalSystems.UserDefinedFunction import UDFBuilder
from src.Main import Main


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


def main():
    app = instantiate_app()
    app.run()


if __name__ == '__main__':
    main()
