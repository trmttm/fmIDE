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
        from view_tkinter import View

        view = View(width=500, height=600)
        view.set_title('Financial Model Constructor')

        parent = 'root'
        new_gui.add_widgets(parent, view)
        view.launch_app()


if __name__ == '__main__':
    unittest.main()
