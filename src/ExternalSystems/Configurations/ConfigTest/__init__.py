from interface_fm import BoundaryInABC
from interface_mouse import MouseControllerABC
from interface_view import ViewABC
from src.BoundaryOutput import PresentersABC
from src.Main.configuration_ABC import ConfigurationABC

from . import command_mapper
from . import control_commands as cc
from . import keyboard_shortcuts
from . import mouse as m
from . import view_commands as vc
from . import view_model as vm
from .menu_bar import create_menu_bar_model


class ConfigurationTest(ConfigurationABC):

    @staticmethod
    def start_view_model_factory() -> list:
        return vm.start_view_model_factory()

    @staticmethod
    def widget_command_map_factory(view: ViewABC, interactor: BoundaryInABC, mouse: MouseControllerABC,
                                   presenters: PresentersABC) -> dict:
        return command_mapper.widget_command_map_factory(view, interactor, mouse, presenters)

    @staticmethod
    def set_up(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC, mouse: MouseControllerABC):
        i, v, p = interactor, view, presenters
        w = vm.entry_text, vm.entry_x, vm.entry_y, vm.entry_width, vm.entry_height, vm.entry_sheet, vm.entry_shape_id, vm.cb_format, vm.cb_num_format, vm.check_btn, vm.entry_uom
        p.attach_to_update_shape_properties(lambda view_model: v.set_values(w, tuple(view_model.values())))
        p.attach_to_present_states(lambda view_model: v.set_value(vm.textbox_rpe, view_model))
        p.attach_to_update_account_order(lambda view_model_: vc.update_tree_account(v, view_model_, i))
        p.attach_to_present_worksheets(lambda view_model_: vc.update_tree_worksheets(v, view_model_, i))
        p.attach_to_present_worksheets(lambda view_model_: vc.update_sheet_name_entry(v, view_model_))
        p.attach_to_present_show_input_entry(lambda view_model_: vc.update_input_entry(v, view_model_))
        p.attach_to_present_show_input_entry(lambda view_model_: vc.draw_input_entry(v, view_model_))
        p.attach_to_present_update_connection_ids(lambda view_model_: vc.update_tree_connections(v, view_model_, i))
        p.attach_to_present_update_commands(lambda view_model_: vc.update_tree_commands(v, view_model_))
        p.attach_to_present_update_macros(lambda view_model_: vc.update_tree_macros(v, view_model_))
        p.attach_to_present_add_worksheet(lambda view_model_: cc.upon_add_worksheet(v, view_model_, mouse))
        p.attach_to_present_select_worksheet(lambda view_model_: cc.upon_select_worksheet(v, view_model_))
        p.attach_to_present_delete_worksheet(lambda view_model_: cc.upon_delete_worksheet(v, view_model_))

        cc.upon_menu_button4(v, i, p, mouse)  # Let left tree_id columns stick to frame
        cc.upon_menu_button1(v, i, p, mouse)
        v.switch_status_bar(vm.status_bar_id)
        i.setup()  # Set up should be invoked AFTER view loaded widgets (fix tree_id view column width).
        v.focus(vm.entry_id)

    @staticmethod
    def set_up_again_with_wrapped_interactor(view: ViewABC, interactor: BoundaryInABC, presenters: PresentersABC,
                                             mouse: MouseControllerABC):
        """
        Tricky logic here...
        Initial ConfigurationTest.setup;
            cc.upon_menu_button4(v, i, p, mouse) sticks tree to frame as desired.
            Interactor.setup() must be invoked AFTER view loaded widgets (fix tree_id view column width).
        However, WrappedInteractor should be used to define behaviours of both
            cc.upon_menu_button4(v, i, p, mouse) ---(1)
            cc.upon_menu_button1(v, i, p, mouse) ---(2)
        But Wrapped Interactor cannot be injected to above prior to Interactor.setup() ---(A)
            because;
                by design, WrappedInteractor saves state, which involves state comparison.
                This needs Interactor.setup() in advance.

        As a result, circularity exists.
            WrappedInteractor must be injected to (1), (2), to achieve 'repeat previous action' BUT
            WrappedInteractor cannot be injected to (1), (2) prior to Interactor.setup()
        Solution;
            First do (1), (2) with Interactor (rather than Wrapped Interactor)
            Then Interactor.setup()
            Finally do (1), (2) again (This very method), but this time with WrappedInteractor
        """
        i, v, p = interactor, view, presenters
        cc.upon_menu_button4(v, i, p, mouse)  # Let left tree_id columns stick to frame
        cc.upon_menu_button1(v, i, p, mouse)

    @staticmethod
    def mouse_configurations(interactor: BoundaryInABC, view: ViewABC, mouse: MouseControllerABC) -> list:
        return m.create_mouse_configuration(interactor, view, mouse)

    @staticmethod
    def default_keyboard_shortcuts(interactor: BoundaryInABC, view: ViewABC, presenters: PresentersABC,
                                   mouse: MouseControllerABC) -> dict:
        return keyboard_shortcuts.get_all_key_combos(interactor, view, presenters, mouse)

    def properly_close_app(self, interactor: BoundaryInABC, view: ViewABC):
        cc.properly_close_app(interactor, view)
