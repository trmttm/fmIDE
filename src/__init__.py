from fm_calculator import Calculator
from keyboard_shortcut import KeyMaps
from spreadsheet import Spreadsheet
from src.EntityGateway import GateWays
from src.ExternalSystems.Configurations import ConfigurationTest
from src.ExternalSystems.UserDefinedFunction import UDFBuilder
from src.Main import Main
from view_tkinter import View

"""
1) At Spreadsheet export time, be able to rearrange / combine / sort worksheets.
2) External worksheet dependencies should be displayed in different color in FMDesigner.
3) External worksheet dependencies should be displayed in different cell format.
"""


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


if __name__ == '__main__':
    is_profiling = True
    if is_profiling:
        import cProfile


        def start_macro():
            from src.Entities import Observable
            Observable.is_debug_mode = False
            app = instantiate_app()
            # Profiling
            app.view.switch_frame('frame_macro')
            app.interactor.merge_macro('00_Base_Model_Plug_Vertical')
            app.interactor.run_macro()
            app.quit()
            # Profiling end


        def start_calculation():
            from src.Entities import Observable
            Observable.is_debug_mode = False
            app = instantiate_app()
            for i in range(1):
                app.interactor.create_data_table()
            app.quit()


        def start_merge_file():
            from src.Entities import Observable
            Observable.is_debug_mode = False
            app = instantiate_app()
            app.interactor.merge_file('Graph BS IS')


        def slider():
            from src.Entities import Observable
            Observable.is_debug_mode = False
            app = instantiate_app()
            app.interactor.select_shape_by_shape_id(528)
            app.interactor.cache_audit_results()
            steps = 100
            for i in range(0, steps):
                app.interactor.move_selections(0, i * 200 / steps)
            app.interactor.clear_cache_audit_results()
            app.quit()


        def select_shape():
            from src.Entities import Observable
            Observable.is_debug_mode = False
            app = instantiate_app()
            for i in range(100):
                app.interactor.select_shape_at_x_y({'x': 1, 'y': 1})
                app.interactor.select_shape_at_x_y({'x': 72, 'y': 30})


        def mouse_selection():
            # Mouse click and drag mouse and see whats making mouse to move slowly
            from src.Entities import Observable
            Observable.is_debug_mode = False
            app = instantiate_app()
            for i in range(10000):
                request = {
                    'entry_by': 'mouse',
                    'exit_by': 'mouse',
                    'x': 200 + 10 * i,
                    'y': 234.0 + 10 * i,
                    'button': 'Left',
                    'gesture': 'CLICK_MOTION',
                    'modifier': None,
                    'coordinates': ((142.0 + i, 269.0), (205.0, 234.0)),
                    'delta_x': 63.0 + 2 * i,
                    'delta_y': 35.0 + 2 * i,
                    'handler': 5,
                    'line_width': 3,
                    'line_color': 'black'
                }
                if i == 0:
                    app.interactor.set_entry_point(entry_by='mouse', request=request)
                    app.interactor.select_shape_at_x_y(request=request)
                    app.interactor.connect_relay_of_shape_at_x_y(request=request)
                    app.mouse.set_mode_to_adding_shapes()
                app.interactor.draw_rectangle(request=request)
                app.interactor.add_shapes_in_range_to_selection(request=request)
                if i == 99:
                    app.interactor.clear_rectangles(request=request)
                    app.interactor.erase_all_lines(request=request)
                    app.interactor.exit_point(request=request)


        def clean_state_and_save_template():
            from src.Entities import Observable
            Observable.is_debug_mode = False
            app = instantiate_app()
            app.interactor.save_state_to_file('zz_Profiling')

        def sand_box():
            from src.Entities import Observable
            Observable.is_debug_mode = False
            app = instantiate_app()
            app.interactor.merge_macro('test2')
            app.interactor.run_macro()

            app.quit()


        cProfile.run('sand_box()')
        # cProfile.run('slider()')
        # cProfile.run('select_shape()')
        # cProfile.run('mouse_selection()')
        # cProfile.run('clean_state_and_save_template()')
    else:
        app = instantiate_app()
        app.run()
