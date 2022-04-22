import unittest


class MyTestCase(unittest.TestCase):
    def test_main(self):
        from ...ExternalSystems.Configurations import ConfigurationTest
        from view_tkinter import View
        from ...EntityGateway import GateWays
        from ...Main import Main

        """
        This is where you select 
            1) Configuration
            2) View
            3) GateWays
        then plug them into Main.
        """

        config = ConfigurationTest()
        view = View()
        cls_gateways = GateWays
        app = Main(config, view, cls_gateways)
        # app.run()

    def test_gui(self):
        import new_gui
        from stacker import Stacker
        from stacker import widgets as w
        from view_tkinter import View

        view = View(width=500, height=600)
        view.set_title('Financial Model Constructor')

        stacker = Stacker()

        names = 'Banks', 'SG&A', 'Other Expense', 'Other Income', 'Product'
        switchable_frames = []

        frame_number = 0

        def switch_frame(increment: int):
            nonlocal frame_number
            if increment > 0:
                frame_number = min(len(switchable_frames) - 1, frame_number + 1)
            else:
                frame_number = max(0, frame_number - 1)

            next_frame = switchable_frames[frame_number]

            if increment > 0:  # Keep user inputs if Back< button is pushed
                local_view_model = None
                if frame_number == 1:
                    local_view_model = new_gui.create_frame_1_view_model(names, frame_number, next_frame, view)
                elif frame_number == 2:
                    local_view_model = new_gui.create_frame_2_view_model(names, frame_number, next_frame, view)
                elif frame_number == 3:
                    local_view_model = new_gui.create_frame_3_view_model(names, frame_number, next_frame, view)
                elif frame_number == 4:
                    data_structure = new_gui.create_data_structure(names, view)
                    print(data_structure)

                if local_view_model is not None:
                    view.add_widgets(local_view_model)

            view.switch_frame(next_frame)

        stacker.vstack(
            w.FrameSwitcher('frame_switcher', stacker, switchable_frames).stackers(
                stacker.vstack(
                    w.Label('label_frame0').text('Frame00'),
                    new_gui.number_of(names[0], stacker, view),
                    new_gui.number_of(names[1], stacker, view),
                    new_gui.number_of(names[2], stacker, view),
                    new_gui.number_of(names[3], stacker, view),
                    new_gui.number_of(names[4], stacker, view),
                    stacker.hstack(
                        w.Button('button_clear').text('Clear').command(
                            lambda: new_gui.clear_entries(names, view, )).width(15),
                        w.Spacer(),
                    ),
                    w.Spacer(),
                ),
                stacker.vstack(),
                stacker.vstack(),
                stacker.vstack(),
                stacker.vstack(),
            ),
            stacker.hstack(
                w.Button('Back').text('Back<').command(lambda: switch_frame(-1)),
                w.Spacer(),
                w.Button('Next').text('>Next').command(lambda: switch_frame(1)),
            ),
        )

        view_model = stacker.view_model
        view.add_widgets(view_model)
        view.switch_frame(switchable_frames[frame_number])
        view.launch_app()


if __name__ == '__main__':
    unittest.main()
