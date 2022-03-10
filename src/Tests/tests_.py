import unittest

from . import test_cases as tc


def no_need_to_test_vba_file(gateway_model):
    if 'vba_file' in gateway_model:
        del gateway_model['vba_file']


class TestInteractorAndEntity(unittest.TestCase):
    def setUp(self) -> None:
        import os
        from src.Entities import Entities
        from src.Presenter import Presenters
        from src.Interactor.Interactor import Interactor
        from src.EntityGateway import GateWays
        from .catchers import NotificationCatcher, ResponseModelCatcher, ViewResponseModelCatcher

        cwd = os.getcwd().replace('fmide/src', 'fmide')
        self._path_test_pickles = f'{cwd}/{"src/Tests"}/{"pickles"}'

        entities = Entities()
        presenters = Presenters()
        interactor = Interactor(entities, presenters, GateWays(entities))
        interactor.add_new_worksheet('Sheet1')
        shapes = entities.shapes
        selection = entities.selection
        rectangle = entities.rectangle_selector
        connections = entities.connections
        lines = entities.lines
        account_order = entities.account_order
        account_orders = entities.account_orders
        worksheets = entities.worksheets
        connection_ids = entities.connection_ids

        notification_catcher = NotificationCatcher()
        shapes.attach(notification_catcher.observer)
        selection.attach(notification_catcher.observer)
        rectangle.attach(notification_catcher.observer)
        connections.attach(notification_catcher.observer)
        lines.attach(notification_catcher.observer)
        account_order.attach(notification_catcher.observer)
        account_orders.attach(notification_catcher.observer)
        worksheets.attach(notification_catcher.observer)
        connection_ids.attach(notification_catcher.observer)

        response_model_catcher = ResponseModelCatcher()
        view_model_catcher = ViewResponseModelCatcher()
        presenters.attach_to_response_model_receiver(response_model_catcher.presenter_method)
        presenters.attach_to_add_shape(view_model_catcher.view_method)

        self._shapes = shapes
        self._selection = selection
        self._interactor = interactor
        self._rectangle = rectangle
        self._connections = connections
        self._lines = lines
        self._account_order = account_order
        self._account_orders = account_orders
        self._worksheets = worksheets
        self._connection_ids = connection_ids
        self._notification_catcher = notification_catcher
        self._response_model_catcher = response_model_catcher
        self._view_model_catcher = view_model_catcher

        self._test_setting()

    def tearDown(self) -> None:
        from src.Entities import Observable
        Observable.is_debug_mode = True

    def _test_setting(self):
        self._shapes_to_delete = (1, 2, 3)
        self._shapes_to_unselect = [1, 3, 5, 7]
        self._get_data_from_notification = self._get_recent

    def test_add_new_shape(self):
        self._run_tests(self._shapes.add_new_shapes, tc.test_cases_add_new_shape)

    def test_interactor_add_new_shape(self):
        self._get_data_from_notification = self._get_interactor_add_shape
        self._run_tests(self._interactor.add_new_shapes, tc.test_cases_add_new_shape_interactor)

        response_model_caught = self._response_model_catcher.response_models_caught[-2]
        expectation = tc.test_cases_add_new_shape_expected_response_model(self._shapes.data)
        self.assertEqual(response_model_caught, expectation)

    def test_erase_shape(self):
        import copy
        add_shapes(self._shapes)
        data_copy = copy.deepcopy(self._shapes.data)
        for shape_id in self._shapes_to_delete:
            del data_copy[shape_id]
        self._shapes.erase_shapes(tuple({'shape_id': shape_id} for shape_id in self._shapes_to_delete))
        self.assertEqual(self._shapes.data, data_copy)

    def test_interactor_erase_shape(self):
        add_shapes(self._interactor)

        self._interactor.erase_shapes(tuple({'shape_id': shape_id} for shape_id in self._shapes_to_delete))

        response_model_caught = self._response_model_catcher.response_models_caught[-3]
        expectation = tc.test_cases_erase_shapes_expected_response_model(self._shapes, self._shapes_to_delete)
        self.assertEqual(response_model_caught, expectation)

    def test_erase_all_shape(self):
        add_shapes(self._shapes)
        self._shapes.erase_all_shapes()
        self.assertEqual(self._shapes.data, {})

    def test_interactor_erase_all_shapes(self):
        add_shapes(self._interactor)
        self._interactor.erase_all_shapes()
        self.assertEqual(self._shapes.data, {})

        response_model_caught = self._response_model_catcher.response_models_caught[-1]
        expectation = None
        self.assertEqual(response_model_caught, expectation)

    def test_add_selection(self):
        add_shapes(self._shapes)
        self._run_tests(self._selection.add_selections, tc.test_cases_add_selection)

    def test_newly_select(self):
        add_shapes(self._shapes)
        self._run_tests(self._selection.select_shapes, tc.test_cases_newly_select)

    def test_unselect(self):
        add_shapes(self._shapes)
        self._selection.add_selections_by_shape_ids(tuple(i['shape_id'] for i in tc.test_cases_add_selection()[1]))
        self._run_tests(self._selection.unselect_shapes, lambda: tc.test_cases_unselect(self._shapes_to_unselect))

    def test_interactor_unselect(self):
        add_shapes(self._interactor)
        self._selection.add_selections_by_shape_ids(tuple(i['shape_id'] for i in tc.test_cases_add_selection()[1]))
        self._run_tests(self._interactor.unselect_shapes, lambda: tc.test_cases_unselect(self._shapes_to_unselect))

        # highlight for the sake of producing response model expected by test case
        self._interactor._present_highlight_automatic()
        response_model_caught = self._response_model_catcher.response_models_caught[-1]
        expectation = tc.test_cases_unselect_response_model(self._shapes_to_unselect)
        self.assertEqual(response_model_caught, expectation)

    def test_clear_selection(self):
        add_shapes(self._shapes)
        self._selection.add_selections(tc.test_cases_add_selection()[1])
        self._selection.clear_selection()
        self.assertEqual(self._selection.data, set())

    def test_interactor_clear_selection(self):
        add_shapes(self._interactor)
        self._selection.add_selections_by_shape_ids(tuple(i['shape_id'] for i in tc.test_cases_add_selection()[1]))
        self._interactor.clear_selection()
        self.assertEqual(self._selection.data, set())

        response_model_caught = self._response_model_catcher.response_models_caught[-6]
        expectation = tc.test_cases_unselect_response_model(self._shapes.shapes_ids)
        self.assertEqual(response_model_caught, expectation)

    def test_draw_rectangle(self):
        self._run_tests(self._rectangle.draw_rectangles, tc.test_cases_draw_rectangle)

    def test_interactor_draw_rectangle(self):
        self._run_tests(self._interactor.draw_rectangles, tc.test_cases_draw_rectangle)

        response_model_caught = self._response_model_catcher.response_models_caught[-1]
        expectation = tc.test_cases_draw_rectangle_response_model(self._rectangle.data)
        self.assertEqual(response_model_caught, expectation)

    def test_erase_rectangle(self):
        self._rectangle.draw_rectangles(tc.test_cases_draw_rectangle()[1])
        self._run_tests(self._rectangle.erase_rectangles, tc.test_cases_erase_rectangle)

    def test_interactor_erase_rectangle(self):
        self._interactor.draw_rectangles(tc.test_cases_draw_rectangle()[1])
        self._run_tests(self._interactor.erase_rectangles, lambda: tc.test_cases_erase_rectangle(True))

        response_model_caught = self._response_model_catcher.response_models_caught[-1]
        expectation = tc.test_cases_draw_rectangle_response_model(self._rectangle.data)
        self.assertEqual(response_model_caught, expectation)

    def test_clear_rectangle(self):
        self._rectangle.draw_rectangles(tc.test_cases_draw_rectangle()[1])
        self._rectangle.clear_rectangle()
        self.assertEqual(self._rectangle.data, {})

    def test_interactor_clear_rectangle(self):
        self._interactor.draw_rectangles(tc.test_cases_draw_rectangle()[1])
        self._interactor.clear_rectangles()
        self.assertEqual(self._rectangle.data, {})

        response_model_caught = self._response_model_catcher.response_models_caught[-1]
        expectation = tc.test_cases_draw_rectangle_response_model(self._rectangle.data)
        self.assertEqual(response_model_caught, expectation)

    def test_add_connection(self):
        self._run_tests(self._connections.add_connections, tc.test_cases_add_connection)

    def test_interactor_add_connection(self):
        add_shapes(self._interactor)
        self._run_tests(self._interactor.add_connections, tc.test_cases_add_connection_interactor)

        response_model_caught = self._response_model_catcher.response_models_caught[-1]
        args = self._connections.data, self._shapes.get_coords_from_shape_id
        expectation = tc.test_cases_change_connection_response_model(*args)
        for each_connection_response_model, each_expectation in zip(response_model_caught, expectation):
            self.assertEqual(each_connection_response_model['coordinates'], each_expectation['coordinates'])

    def test_remove_connection(self):
        self._connections.add_connections(tc.test_cases_add_connection()[1])
        self._run_tests(self._connections.remove_connections, tc.test_cases_remove_connection)

    def test_interactor_remove_connection(self):
        add_shapes(self._interactor)
        self._interactor.add_connections(tc.test_cases_add_connection()[1])
        self._run_tests(self._interactor.remove_connections, tc.test_cases_remove_connection)

        response_model_caught = self._response_model_catcher.response_models_caught[-1]
        args = self._connections.data, self._shapes.get_coords_from_shape_id
        expectation = tc.test_cases_change_connection_response_model(*args)
        self.assertEqual(response_model_caught, expectation)

    def test_remove_all_connections_of_a_shape(self):
        self._connections.add_connections(tc.test_cases_add_connection()[1])
        self._run_tests(self._connections.remove_all_connections_of_shapes, tc.test_cases_remove_connection_of_a_shape)

    def test_draw_lines(self):
        self._run_tests(self._lines.draw_lines, tc.test_cases_draw_lines)

    def test_interactor_draw_lines(self):
        self._run_tests(self._interactor.draw_lines, tc.test_cases_draw_lines)

        response_model_caught = self._response_model_catcher.response_models_caught[-1]
        expectation = tc.test_cases_draw_lines_response_model(self._lines.data)
        self.assertEqual(response_model_caught, expectation)

    def test_erase_lines(self):
        self._lines.draw_lines(tc.test_cases_draw_lines()[1])
        self._run_tests(self._lines.erase_lines, tc.test_cases_erase_lines)

    def test_interactor_erase_lines(self):
        self._interactor.draw_lines(tc.test_cases_draw_lines()[1])
        self._run_tests(self._interactor.erase_lines, tc.test_cases_erase_lines)

        response_model_caught = self._response_model_catcher.response_models_caught[-1]
        expectation = tc.test_cases_draw_lines_response_model(self._lines.data)
        self.assertEqual(response_model_caught, expectation)

    def test_clear_lines(self):
        self._lines.draw_lines(tc.test_cases_draw_lines()[1])
        self._lines.clear_lines()
        self.assertEqual(self._lines.data, {})

    def test_interactor_clear_lines(self):
        self._interactor.draw_lines(tc.test_cases_draw_lines()[1])
        self._interactor.erase_all_lines()
        self.assertEqual(self._lines.data, {})

        response_model_caught = self._response_model_catcher.response_models_caught[-1]
        expectation = tc.test_cases_draw_lines_response_model(self._lines.data)
        self.assertEqual(response_model_caught, expectation)

    def test_get_shape_id_at_the_coordinate(self):
        add_shapes(self._interactor)
        expected_shape_ids, coordinates = tc.test_case_shape_id_at_xy()
        for coordinate, expected_shape_id in zip(coordinates, expected_shape_ids):
            self.assertEqual(self._shapes.get_shape_id_at_the_coordinate(*coordinate), expected_shape_id)

    def test_get_shapes_by_tag_type(self):
        add_shapes(self._shapes)
        expectations, tag_types = tc.test_cases_get_shapes_by_tag_types()
        for tag_type, expected_shapes in zip(tag_types, expectations):
            self.assertEqual(self._shapes.get_shapes(tag_type), expected_shapes)

    def test_interactor_load_pickle(self):
        from src.EntityGateway.FilesSystemIO import get_file_names_in_a_folder
        negative_list = ('.DS_Store', 'pickle_for_unit_test', '__init__.py')
        self._interactor.load_pickle_files_list()

        response_model_caught = self._response_model_catcher.response_models_caught[-1]
        file_names = get_file_names_in_a_folder('src/Pickles', negative_list)
        file_names.sort()
        expectation = {'file_names': file_names}
        self.assertEqual(response_model_caught, expectation)

    def test_interactor_update_account_list(self):
        add_shapes(self._interactor)
        account_order = self._interactor.account_order
        self.assertEqual(account_order.data, (0, 1, 2))
        response_model_caught = self._response_model_catcher.response_models_caught[-3]
        expectation = {'account_names': ('Account0', 'Account1', 'Account2'), 'select_flags': (False, False, False)}
        self.assertEqual(response_model_caught, expectation)

    def test_change_account_order(self):
        add_shapes(self._interactor)
        account_order = self._interactor.account_order
        selection = self._interactor.selection

        self.assertEqual(account_order.data, (0, 1, 2))

        self._interactor.change_account_order(2, 1)
        self.assertEqual(account_order.data, (0, 2, 1))

        selection.select_shape(1)
        self._interactor.selection.select_shape(1)
        self._interactor.move_selection_up()
        self.assertEqual(account_order.data, (0, 1, 2))

        self._interactor.move_selection_up()
        self.assertEqual(account_order.data, (1, 0, 2))

        selection.select_shape(2)
        self.assertEqual(selection.data, {2})
        self._interactor.move_selection_up(2)
        self.assertEqual(account_order.data, (2, 1, 0))

        self._interactor.move_selection_down()
        self.assertEqual(account_order.data, (1, 2, 0))

        selection.add_selection(1)
        self.assertEqual(selection.data, {1, 2})
        self._interactor.move_selection_up()
        self.assertEqual(account_order.data, (2, 0, 1))

        self._interactor.move_selection_up(2)
        self.assertEqual(account_order.data, (1, 2, 0))

        self._interactor.move_selection_down()
        self.assertEqual(account_order.data, (0, 1, 2))

        selection.select_shape(2)
        self._interactor.move_selection_down()
        self.assertEqual(account_order.data, (2, 0, 1))

    def test_interactor_add_blank_row(self):
        add_shapes(self._interactor)
        account_order = self._interactor.account_order
        selection = self._interactor.selection
        self.assertEqual(account_order.data, (0, 1, 2))

        index_ = 1
        self._interactor.add_blank_row(index_)
        blank1 = account_order.data[index_]
        self.assertEqual(account_order.data, (0, blank1, 1, 2))

        selection.add_selection(2)
        self._interactor.add_blank_above_selection()
        blank2 = account_order.data[3]
        self.assertEqual(account_order.data, (0, blank1, 1, blank2, 2))

        selection.select_shape(0)
        self._interactor.add_blank_above_selection()
        blank3 = account_order.data[0]
        self.assertEqual(account_order.data, (blank3, 0, blank1, 1, blank2, 2))

    def test_align_shapes(self):
        with_ = 0
        aligning = 1
        coords_with = (10, 10, 60, 30)
        coords_aligning = (100, 15, 150, 45)

        self._shapes.add_new_shape('Shape0')
        self._shapes.add_new_shape('Shape1')

        self._shapes.set_coordinate(with_, coords_with)
        self._shapes.set_coordinate(aligning, coords_aligning)
        self._shapes.align_shape(aligning, with_, 'left')
        self.assertEqual(self._shapes.get_x(with_), self._shapes.get_x(aligning))
        self.assertEqual(self._shapes.get_x(with_), 10)

        self._shapes.erase_all_shapes()

    def test_evenly_distribute_horizontally(self):
        add_shapes(self._interactor)
        shapes = self._shapes
        shape_ids = shapes.shapes_ids

        x_end = 1500
        shapes.set_x(shape_ids[-1], x_end)
        x_before_distribution = [shapes.get_x(shape_id) for shape_id in shape_ids]
        expectation = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, x_end]
        self.assertEqual(x_before_distribution, expectation)

        shapes.evenly_distribute_horizontally(shape_ids)

        x_after_distribution = [shapes.get_x(shape_id) for shape_id in shape_ids]
        expectation = [10,
                       135.46000000000004,
                       260.9200000000001,
                       386.3800000000001,
                       511.84000000000015,
                       637.3000000000002,
                       762.7600000000002,
                       888.2200000000003,
                       1013.6800000000003,
                       1139.1400000000003,
                       1264.6000000000004,
                       1390.0600000000004,
                       1500]
        self.assertEqual(x_after_distribution, expectation)

    def test_evenly_distribute_vertically(self):
        add_shapes(self._interactor)
        shapes = self._shapes
        shape_ids = shapes.shapes_ids

        y_end = 600
        self._shapes.set_y(shape_ids[-1], y_end)
        y_before_distribution = [shapes.get_y(shape_id) for shape_id in shape_ids]
        expectation = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, y_end]
        self.assertEqual(y_before_distribution, expectation)

        shapes.evenly_distribute_vertically(shape_ids)
        y_after_distribution = [shapes.get_y(shape_id) for shape_id in shape_ids]
        expectation = [25,
                       72.96499999999997,
                       120.92999999999995,
                       168.89499999999992,
                       216.8599999999999,
                       264.8249999999999,
                       312.78999999999985,
                       360.7549999999998,
                       408.7199999999998,
                       456.6849999999998,
                       504.64999999999975,
                       552.6149999999998,
                       600]
        self.assertEqual(y_after_distribution, expectation)

    def test_fit_width(self):
        add_shapes(self._interactor)
        expectation = ((0, 50),
                       (1, 50),
                       (2, 50),
                       (3, 50),
                       (4, 50),
                       (5, 50),
                       (6, 50),
                       (7, 50),
                       (8, 50),
                       (9, 50),
                       (10, 50),
                       (11, 50),
                       (12, 50))
        shape_id_to_width = tuple((shape_id, self._shapes.get_width(shape_id)) for shape_id in self._shapes.shapes_ids)
        self.assertEqual(shape_id_to_width, expectation)

        self._interactor.fit_all_shapes_width()
        expectation = ((0, 64),
                       (1, 64),
                       (2, 64),
                       (3, 8),
                       (4, 8),
                       (5, 8),
                       (6, 8),
                       (7, 8),
                       (8, 16),
                       (9, 8),
                       (10, 24),
                       (11, 24),
                       (12, 40))
        shape_id_to_width = tuple((shape_id, self._shapes.get_width(shape_id)) for shape_id in self._shapes.shapes_ids)
        self.assertEqual(shape_id_to_width, expectation)

    def test_worksheet_operations(self):
        # Add worksheets
        self._interactor.add_new_worksheet()
        self._interactor.add_new_worksheet()
        response_model_caught = self._response_model_catcher.response_models_caught[-3]
        expectation = {'select_flags': (False, False, True), 'sheet_names': ('Sheet1', 'Sheet2', 'Sheet3'),
                       'sheet_name_to_parent': {}, }
        self.assertEqual(response_model_caught, expectation)

        # Select worksheet
        self._interactor.select_worksheet('Sheet1')
        response_model_caught = self._response_model_catcher.response_models_caught[-2]
        expectation = {'select_flags': (True, False, False), 'sheet_names': ('Sheet1', 'Sheet2', 'Sheet3'),
                       'sheet_name_to_parent': {}}
        self.assertEqual(response_model_caught, expectation)

        # Delete worksheets
        self._interactor.delete_selected_worksheet()
        response_model_caught = self._response_model_catcher.response_models_caught[-2]
        expectation = {'select_flags': (False, True), 'sheet_names': ('Sheet2', 'Sheet3'),
                       'sheet_name_to_parent': {}}
        self.assertEqual(response_model_caught, expectation)

        # change sheet name
        self._interactor.change_selected_sheet_name('Model')
        response_model_caught = self._response_model_catcher.response_models_caught[-2]
        expectation = {'select_flags': (False, True), 'sheet_names': ('Sheet2', 'Model'),
                       'sheet_name_to_parent': {}}
        self.assertEqual(response_model_caught, expectation)

    def test_output_worksheet_data(self):
        self._interactor.add_new_shape('AA', 'account')
        self._interactor.add_new_shape('BB', 'account')
        # self._interactor.select_shape_by_shape_id(1)
        self._interactor._selection.select_shape(1)
        self._interactor.add_blank_above_selection()
        blank = self._interactor.account_order.data[-2]

        self._interactor.add_new_worksheet()
        self._interactor.add_new_shape('CC', 'account')
        self._interactor.add_new_shape('DD', 'account')
        self._interactor._selection.select_shape(1)

        expectation = {'Sheet1': (0, blank, 1), 'Sheet2': (2, 3)}
        self.assertEqual(self._interactor.output_worksheet_information, expectation)

    def test_change_worksheet_of_selected_shapes(self):
        path_test_pickles = self._path_test_pickles
        from src.Entities.AccountOrder import Blank
        from spreadsheet import Spreadsheet
        from src import Utilities
        import os_identifier
        blank = Blank()
        interactor = self._interactor

        pickle_name = 'change_worksheet'
        file_name = f'{pickle_name}_output.xlsx'
        interactor.plug_in_gateway_spreadsheet(Spreadsheet)
        interactor.change_path_pickles(path_test_pickles)
        interactor.load_file(pickle_name)
        sheet_name_from = 'Income Statement'
        sheet_name_to = 'Balance Sheet'

        interactor.select_worksheet(sheet_name_from)
        interactor.add_shapes_to_selection(interactor.sheet_contents)
        interactor.set_worksheet_to_selected_shapes_properties(sheet_name_to)

        if os_identifier.is_mac:
            path = f'{Utilities.cwd.replace(".", "")}Tests/pickles/change_worksheet_output.xlsx'
        else:
            path = 'C:\\Users\\Yamaka\\Documents\\FMDesigner/Tests/pickles/change_worksheet_output.xlsx'
        expected_request_model = {
            'workbook_name': path,
            'shape_id_to_address': {0: 'max',
                                    1: '0',
                                    2: '+',
                                    3: '+',
                                    4: '-',
                                    5: 'Net Cash',
                                    6: '0',
                                    7: 'min',
                                    8: '-1',
                                    9: 'x',
                                    10: 'Non Plug CL',
                                    11: 'Total Assets',
                                    12: 'Non Current Assets',
                                    13: 'Current Assets',
                                    14: 'Cash',
                                    15: 'Non Cash',
                                    16: '+',
                                    17: '+',
                                    18: 'Total Liabilities',
                                    19: 'Excess Cash',
                                    20: 'Excess Deficit',
                                    21: 'Plug',
                                    22: 'Cash',
                                    23: 'Non Current Liabilities',
                                    24: 'Non cash assets',
                                    25: 'Liabilities NC',
                                    26: 'Total Equity',
                                    27: 'Non Cash CA',
                                    28: 'Non Current Assets',
                                    29: 'Current Liabilities',
                                    30: 'Non Plug CL',
                                    31: 'Plug - Revolver',
                                    32: '+',
                                    33: '+',
                                    34: 'Total Equity',
                                    35: 'Other Equity',
                                    36: 'Retained Earnings',
                                    37: 'Paid in Capital',
                                    38: '+',
                                    39: 'Non Cash',
                                    40: 'Non Current Assets',
                                    41: 'Total Equity',
                                    42: 'Non Plug CL',
                                    43: 'Non Current Liabilities',
                                    44: 'Cash',
                                    45: 'Plug',
                                    46: 'Total Assets',
                                    47: 'Total Liabilities',
                                    48: 'Total Equity',
                                    49: 'Dr Cr match',
                                    50: '+',
                                    51: '-',
                                    52: 'Total Liabilities',
                                    53: 'Total Equity',
                                    54: 'Total Assets',
                                    55: 'Revenue',
                                    56: 'Cost of Goods',
                                    57: 'Gross Profit',
                                    58: 'SG&A',
                                    59: 'Other costs',
                                    60: 'Other incomes',
                                    61: 'EBITDA',
                                    62: 'Depreciation',
                                    63: 'Amortization',
                                    64: 'EBIT',
                                    65: 'Interest Income',
                                    66: 'Interest Expense',
                                    67: 'EBT',
                                    68: 'Tax',
                                    69: 'Net Income',
                                    70: '-',
                                    71: '-',
                                    72: '+',
                                    73: '+',
                                    74: '-',
                                    75: '+',
                                    76: '+',
                                    77: '-',
                                    78: '-',
                                    79: 'Net Income',
                                    80: 'Retained Earnings',
                                    99: 'Retained Earnings',
                                    100: 'Retained Earnings BB',
                                    101: 'Net Income',
                                    102: 'Dividend Payout',
                                    103: '+'},
            'inputs': (12, 15, 23, 30, 35, 37, 55, 56, 58, 59, 60, 62, 63, 65, 66, 68, 100, 102),
            'input_values': ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
            'operators': (2,
                          3,
                          4,
                          0,
                          7,
                          9,
                          16,
                          17,
                          32,
                          33,
                          38,
                          50,
                          51,
                          70,
                          71,
                          72,
                          73,
                          74,
                          75,
                          76,
                          77,
                          78,
                          103),
            'constants': (1, 6, 8),
            'sheets_data': {'Balance Sheet': (14,
                                              15,
                                              13,
                                              12,
                                              11,
                                              blank,
                                              30,
                                              31,
                                              29,
                                              23,
                                              18,
                                              blank,
                                              37,
                                              36,
                                              35,
                                              34,
                                              blank,
                                              26,
                                              10,
                                              25,
                                              blank,
                                              27,
                                              28,
                                              24,
                                              blank,
                                              5,
                                              blank,
                                              19,
                                              22,
                                              20,
                                              21,
                                              blank,
                                              46,
                                              47,
                                              48,
                                              49,
                                              blank,
                                              55,
                                              56,
                                              57,
                                              blank,
                                              58,
                                              59,
                                              60,
                                              61,
                                              blank,
                                              62,
                                              63,
                                              64,
                                              blank,
                                              66,
                                              65,
                                              67,
                                              blank,
                                              68,
                                              69,
                                              blank),
                            'Corkscrew': (100, 101, 102, 99, blank),
                            'Income Statement': (blank, blank, blank, blank, blank)},
            'rpes': ((24, (27, 28, 2)),
                     (5, (26, 10, 3, 25, 3, 24, 4)),
                     (19, (1, 5, 0)),
                     (20, (5, 6, 7)),
                     (21, (8, 20, 9)),
                     (13, (14, 15, 16)),
                     (11, (12, 13, 17)),
                     (29, (30, 31, 32)),
                     (18, (23, 29, 33)),
                     (34, (35, 36, 38, 37, 38)),
                     (49, (46, 47, 48, 50, 51)),
                     (57, (55, 56, 70)),
                     (61, (57, 58, 59, 72, 71, 60, 73)),
                     (64, (61, 62, 63, 75, 74)),
                     (67, (64, 66, 77, 65, 76)),
                     (69, (67, 68, 78)),
                     (99, (100, 101, 103, 102, 103))),
            'nop': 10,
            'direct_links_mutable': ((30, 10, 0),
                                     (23, 25, 0),
                                     (22, 14, 0),
                                     (15, 27, 0),
                                     (18, 47, 0),
                                     (21, 31, 0),
                                     (11, 46, 0),
                                     (69, 101, 0),
                                     (19, 22, 0),
                                     (34, 48, 0),
                                     (34, 26, 0),
                                     (99, 36, 0),
                                     (12, 28, 0)),
            'format_data': {},
            'number_format_data': {},
            'vertical_acs': {},
            'shape_id_to_uom': {},

        }
        self._test_change_worksheet(expected_request_model, file_name, interactor)

    def test_change_worksheet_of_selected_shapes2(self):
        path_test_pickles = self._path_test_pickles
        from src.Entities.AccountOrder import Blank
        from spreadsheet import Spreadsheet
        from src import Utilities
        import os_identifier
        blank = Blank()
        interactor = self._interactor

        pickle_name = 'change_worksheet2'
        file_name = f'{pickle_name}_output.xlsx'
        interactor.plug_in_gateway_spreadsheet(Spreadsheet)
        interactor.change_path_pickles(path_test_pickles)
        interactor.load_file(pickle_name)
        sheet_name_from = 'Model'
        sheet_name_to = 'Core Accounts'

        interactor.add_new_worksheet(sheet_name_to)
        interactor.select_worksheet(sheet_name_from)
        interactor.add_shapes_to_selection((86, 82, 93, 94))  # Total Revenue, Total COGS, relay, relay
        interactor.set_worksheet_to_selected_shapes_properties(sheet_name_to)

        if os_identifier.is_mac:
            path = f'{Utilities.cwd.replace(".", "")}Tests/pickles/change_worksheet2_output.xlsx'
        else:
            path = 'C:\\Users\\Yamaka\\Documents\\FMDesigner/Tests/pickles/change_worksheet2_output.xlsx'
        expected_request_model = {
            'workbook_name': path,
            'shape_id_to_address': {19: 'Excess Cash', 20: 'Excess Deficit', 21: 'Plug', 22: 'Cash',
                                    24: 'Non cash assets', 25: 'Liabilities NC', 26: 'Total Equity', 27: 'Non Cash CA',
                                    28: 'Non Current Assets', 2: '+', 3: '+', 4: '-', 5: 'Net Cash', 0: 'max', 1: '0',
                                    6: '0', 7: 'min', 8: '-1', 9: 'x', 10: 'Non Plug CL', 11: 'Total Assets',
                                    12: 'Non Current Assets', 13: 'Current Assets', 14: 'Cash', 15: 'Non Cash', 16: '+',
                                    17: '+', 18: 'Total Liabilities', 23: 'Non Current Liabilities',
                                    29: 'Current Liabilities', 30: 'Non Plug CL', 31: 'Plug - Revolver', 32: '+',
                                    33: '+', 34: 'Total Equity', 35: 'Other Equity', 36: 'Retained Earnings',
                                    37: 'Paid in Capital', 38: '+', 39: 'Non Cash', 40: 'Non Current Assets',
                                    41: 'Total Equity', 42: 'Non Plug CL', 43: 'Non Current Liabilities', 44: 'Cash',
                                    45: 'Plug', 46: 'Total Assets', 47: 'Total Liabilities', 48: 'Total Equity',
                                    49: 'Dr Cr match', 50: '+', 51: '-', 52: 'Total Liabilities', 53: 'Total Equity',
                                    54: 'Total Assets', 55: 'Revenue', 56: 'Cost of Goods', 57: 'Gross Profit',
                                    58: 'SG&A', 59: 'Other costs', 60: 'Other incomes', 61: 'EBITDA',
                                    62: 'Depreciation',
                                    63: 'Amortization', 64: 'EBIT', 65: 'Interest Income', 66: 'Interest Expense',
                                    67: 'EBT', 68: 'Tax', 69: 'Net Income', 70: '-', 71: '-', 72: '+', 73: '+', 74: '-',
                                    75: '+', 76: '+', 77: '-', 78: '-', 99: 'Retained Earnings',
                                    100: 'Retained Earnings BB', 101: 'Net Income', 102: 'Dividend Payout', 103: '+',
                                    79: 'Net Income', 80: 'Retained Earnings', 81: 'Revenue', 83: 'Volume', 84: 'Price',
                                    85: 'x', 86: 'Total Revenue', 87: 'Total Revenue', 82: 'Total Cogs',
                                    89: 'Unit Cost',
                                    90: 'x', 91: 'Cogs', 92: 'Total Cogs', 88: 'Volume', 93: 'Revenue', 94: 'Cogs'},
            'inputs': (12, 15, 23, 30, 35, 37, 58, 59, 60, 62, 63, 65, 66, 68, 100, 102, 83, 84, 89),
            'input_values': ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
            'operators': (2, 3, 4, 0, 7, 9, 16, 17, 32, 33, 38, 50, 51, 70, 71, 72, 73, 74, 75, 76, 77, 78, 103, 85,
                          90),
            'constants': (1, 6, 8),
            'sheets_data': {'Balance Sheet': (
                14, 15, 13, 12, 11, blank, 30, 31, 29, 23, 18, blank, 37, 36, 35, 34, blank, 26, 10, 25, blank, 27, 28,
                24,
                blank, 5, blank, 19, 22, 20, 21, blank, 46, 47, 48, 49, blank, 55, 56, 57, blank, 58, 59, 60, 61, blank,
                62, 63,
                64, blank, 66, 65, 67, blank, 68, 69, blank), 'Model': (
                100, 101, 102, 99, blank, 83, 84, 81, blank, 89, 88, 91, blank, blank, blank), 'a': (),
                'Core Accounts': (86, blank, 82, blank)},
            'rpes': ((24, (27, 28, 2)), (5, (26, 10, 3, 25, 3, 24, 4)), (19, (1, 5, 0)), (20, (5, 6, 7)),
                     (21, (8, 20, 9)), (13, (14, 15, 16)), (11, (12, 13, 17)), (29, (30, 31, 32)),
                     (18, (23, 29, 33)), (34, (35, 36, 38, 37, 38)), (49, (46, 47, 48, 50, 51)),
                     (57, (55, 56, 70)), (61, (57, 58, 59, 72, 71, 60, 73)), (64, (61, 62, 63, 75, 74)),
                     (67, (64, 66, 77, 65, 76)), (69, (67, 68, 78)), (99, (100, 101, 103, 102, 103)),
                     (81, (84, 83, 85)), (91, (88, 89, 90))),
            'nop': 10,
            'direct_links_mutable': ((30, 10, 0), (23, 25, 0), (91, 82, 0), (22, 14, 0), (15, 27, 0), (18, 47, 0),
                                     (21, 31, 0), (11, 46, 0), (81, 86, 0), (69, 101, 0), (19, 22, 0), (34, 48, 0),
                                     (34, 26, 0), (83, 88, 0), (99, 36, 0), (82, 56, 0), (12, 28, 0), (86, 55, 0)),
            'format_data': {},
            'number_format_data': {},
            'vertical_acs': {},
            'shape_id_to_uom': {},
        }
        self._test_change_worksheet(expected_request_model, file_name, interactor)

    def _test_change_worksheet(self, expected_request_model, file_name, interactor):
        gateway_model_created = interactor.create_gateway_model_to_spreadsheet(file_name)
        no_need_to_test_vba_file(gateway_model_created)
        self.assertEqual(len(gateway_model_created), len(expected_request_model))
        for n, (element, expectation) in enumerate(zip(gateway_model_created, expected_request_model)):
            if n == 9:
                self.assertEqual(set(element), set(expectation))
            else:
                self.assertEqual(element, expectation)

        interactor.export_excel(file_name)

    def test_bb(self):
        path_test_pickles = self._path_test_pickles
        from src.Entities.AccountOrder import Blank
        from spreadsheet import Spreadsheet
        from src import Utilities
        import os_identifier
        blank = Blank()
        interactor = self._interactor

        pickle_name = 'bb'
        file_name = f'{pickle_name}_output.xlsx'
        interactor.plug_in_gateway_spreadsheet(Spreadsheet)
        interactor.change_path_pickles(path_test_pickles)
        interactor.load_file(pickle_name)

        if os_identifier.is_mac:
            path = f'{Utilities.cwd.replace(".", "")}/Tests/pickles/bb_output.xlsx'
        else:
            path = 'C:\\Users\\Yamaka\\Documents\\FM/src/Tests/pickles/bb_output.xlsx'
        expected_request_model = {
            'workbook_name': path,
            'shape_id_to_address': {0: 'AA', 1: 'AA BB', 2: 'increase', 3: 'decrease', 4: '+', 5: '-', 6: 'BB'},
            'inputs': (2, 3),
            'input_values': ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
            'operators': (4, 5),
            'constants': (),
            'sheets_data': {'Sheet1': (1, 2, 3, 0, blank)},
            'rpes': ((0, (1, 2, 4, 3, 5)),),
            'nop': 10,
            'direct_links_mutable': ((0, 1, -1),),
            'format_data': {},
            'number_format_data': {},
            'vertical_acs': {},
            'shape_id_to_uom': {},
        }
        request_model = interactor.create_gateway_model_to_spreadsheet(file_name)
        no_need_to_test_vba_file(request_model)
        keys1 = tuple(request_model.keys())
        keys2 = tuple(expected_request_model.keys())
        self.assertEqual(keys1, keys2)
        if keys1 == keys2:
            for key in keys1:
                self.assertEqual(request_model[key], expected_request_model[key])

    def test_excel_request_model_from_pickle(self):
        path_test_pickles = self._path_test_pickles
        from src.Entities.AccountOrder import Blank
        blank = Blank()

        pickle_names = (
            'test_ave_operation',
            'test_equal_operation',
            'test_ge_operation',
            'test_min_operation',
            'test_abs_operation',
        )
        expected_gateway_models = (
            {
                'workbook_name': f'{path_test_pickles}/Excel.xlsx',
                'shape_id_to_address': {0: 'A', 1: 'B', 2: 'C', 3: 'ave', 4: 'D', 5: 'E'},
                'inputs': (0, 1, 4, 5),
                'input_values': ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                 (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                 (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                 (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
                'operators': (3,),
                'constants': (),
                'sheets_data': {'Sheet1': (0, 1, 4, 5, 2, blank)},
                'rpes': ((2, (0, 1, 3, 4, 3, 5, 3)),),
                'nop': 10,
                'direct_links_mutable': (),
                'format_data': {},
                'number_format_data': {},
                'vertical_acs': {},
                'shape_id_to_uom': {},
            },

            {
                'workbook_name': f'{path_test_pickles}/Excel.xlsx',
                'shape_id_to_address': {0: 'A', 1: 'B', 2: 'C', 3: '='},
                'inputs': (0, 1),
                'input_values': ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
                'operators': (3,),
                'constants': (),
                'sheets_data': {'Sheet1': (0, 1, 2)},
                'rpes': ((2, (0, 1, 3)),),
                'nop': 10,
                'direct_links_mutable': (),
                'format_data': {},
                'number_format_data': {},
                'vertical_acs': {},
                'shape_id_to_uom': {},
            },

            {

                'workbook_name': f'{path_test_pickles}/Excel.xlsx',
                'shape_id_to_address': {0: 'A', 1: 'B', 2: 'C', 3: '>='},
                'inputs': (0, 1),
                'input_values': ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
                'operators': (3,),
                'constants': (),
                'sheets_data': {'Sheet1': (0, 1, 2)},
                'rpes': ((2, (0, 1, 3)),),
                'nop': 10,
                'direct_links_mutable': (),
                'format_data': {},
                'number_format_data': {},
                'vertical_acs': {},
                'shape_id_to_uom': {},
            },

            {
                'workbook_name': f'{path_test_pickles}/Excel.xlsx',
                'shape_id_to_address': {0: 'A', 1: 'B', 2: 'C', 3: 'min', 4: 'D', 5: 'E'},
                'inputs': (0, 1, 4, 5),
                'input_values': ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                 (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                 (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                 (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
                'operators': (3,),
                'constants': (),
                'sheets_data': {'Sheet1': (0, 1, 4, 5, 2, blank)},
                'rpes': ((2, (0, 1, 3, 4, 3, 5, 3)),),
                'nop': 10,
                'direct_links_mutable': (),
                'format_data': {},
                'number_format_data': {},
                'vertical_acs': {},
                'shape_id_to_uom': {},
            },

            {
                'workbook_name': f'{path_test_pickles}/Excel.xlsx',
                'shape_id_to_address': {0: 'Cash from BS',
                                        1: 'Cash from CFWF',
                                        3: 'Difference - absolute',
                                        4: '-',
                                        6: 'abs'},
                'inputs': (0, 1),
                'input_values': ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
                'operators': (4, 6),
                'constants': (),
                'sheets_data': {'Sheet1': (0, 1, 3, blank)},
                'rpes': ((3, (0, 1, 4, 6)),),
                'nop': 10,
                'direct_links_mutable': (),
                'format_data': {},
                'number_format_data': {},
                'vertical_acs': {},
                'shape_id_to_uom': {},
            },
        )

        self._interactor.change_path_pickles(path_test_pickles)
        for n, (pickle_name, expected_gateway_model) in enumerate(zip(pickle_names, expected_gateway_models)):
            self._interactor.load_file(pickle_name)
            gateway_model = self._interactor.create_gateway_model_to_spreadsheet()
            no_need_to_test_vba_file(gateway_model)
            self.assertEqual(gateway_model, expected_gateway_model)

    def test_change_shape_id(self):
        path_test_pickles = self._path_test_pickles
        pickle_names = ('test_dynamic_connector',)
        expectation1 = {'shape_ids': (1, 2, 3, 4, 5, 6, 7, 'new_shape_id'),
                        'selections': {1, 2, 'new_shape_id'},
                        'account_orders': (('new_shape_id', 1, 2), (3, 7)),
                        'worksheets': {'Sheet From': {1, 2, 5, 'new_shape_id'}, 'Sheet To': {3, 4, 6, 7}},
                        }
        expectations = (expectation1,)
        self._interactor.change_path_pickles(path_test_pickles)

        for n, (pickle_name, expectation) in enumerate(zip(pickle_names, expectations)):
            self._interactor.load_file(pickle_name)
            for i in (0, 1, 2):
                self._interactor._selection.add_selection(i)
            self._interactor.change_shape_id(0, 'new_shape_id')
            self.assertEqual(self._shapes.shapes_ids, expectation['shape_ids'])
            self.assertEqual(self._interactor._selection.data, expectation['selections'])

            d = tuple(account_order.data for account_order in self._account_orders._data.values())
            self.assertEqual(d, expectation['account_orders'])

            self.assertEqual(self._worksheets.data['_sheet_data'], expectation['worksheets'])

    def test_socket(self):
        path_test_pickles = self._path_test_pickles
        pickle_name = 'test_dynamic_connector'
        socket_name = 'test_socket_name'
        expectation = {
            'shape_ids': (0, 1, 2, 3, 4, 5, 6, 7),
            'sockets': {'_key_connection_ids': {4: ('test_socket_name',)},
                        '_key_partner_plugs': {},
                        '_key_partner_sockets': {}},
        }
        self._interactor.change_path_pickles(path_test_pickles)

        self._interactor.load_file(pickle_name)
        self._interactor.connect_shapes_by_shape_ids(3, 4)
        self._interactor.add_connection_id(4, socket_name)
        self.assertEqual(self._shapes.shapes_ids, expectation['shape_ids'])
        self.assertEqual(self._connection_ids.data, expectation['sockets'])

        expectation = {
            'shape_ids': (0, 1, 2, 3, 4, 5, 6, 7),
            'sockets': {'_key_connection_ids': {4: ()},
                        '_key_partner_plugs': {},
                        '_key_partner_sockets': {}},
        }
        self._interactor.remove_connection_id(4, 'test_socket_name')
        self.assertEqual(self._shapes.shapes_ids, expectation['shape_ids'])
        self.assertEqual(self._connection_ids.data, expectation['sockets'])

    def test_save_as_module(self):
        path_test_pickles = self._path_test_pickles
        pickle_name = 'test_module'
        module_name = f'{pickle_name}_saved_as_a_module'

        self._interactor.change_path_pickles(path_test_pickles)

        self._interactor.load_file(pickle_name)
        self._interactor.save_current_sheet_as_module(module_name)
        self._interactor.merge_file(module_name)
        expectation = {'_key_connection_ids': {'Socket_IS_Net_Income': ('IS_Net_Income',),
                                               'Socket_to_CF_Total_delta_Working_Capital': (
                                                   'to_CF_Total_delta_Working_Capital',)},
                       '_key_partner_plugs': {59: ('IS_Net_Income',)},
                       '_key_partner_sockets': {61: ('to_CF_Total_delta_Working_Capital',)}}
        self.assertEqual(self._connection_ids._data, expectation)

    def test_clean_pickles(self):
        from ..EntityGateway import GateWays
        negative_list = GateWays.negative_list
        file_names = self._interactor.get_pickle_file_names(negative_list)
        for folder_name in file_names:
            # try:
            #     self._interactor.load_file(folder_name)
            #
            #     for connection_from, connection_to in tuple(self._interactor._connections.data):
            #         if connection_from not in self._shapes.data or connection_to not in self._shapes.data:
            #             self._interactor._connections.remove_connection(connection_from, connection_to)
            # except:
            #     pass
            # try:
            #     if type(self._interactor._connection_ids._data) == set:
            #         self._interactor._connection_ids.__init__()
            # except:
            #     pass
            # try:
            #     for data_dictionary in self._interactor._connection_ids._data.values():
            #         for format_key in tuple(data_dictionary.keys()):
            #             if 'S' in str(format_key) or data_dictionary[format_key] == () or format_key not in self._interactor._shapes.data:
            #                 del data_dictionary[format_key]
            # except:
            #     pass
            # try:
            #     for sheet_name in tuple(self._account_orders.data.keys()):
            #         if sheet_name not in self._worksheets.sheet_names:
            #             self._account_orders.delete_account_order(sheet_name)
            # except:
            #     pass
            #
            # in_a_sheet = self._interactor._worksheets.get_worksheet_of_an_account
            # shapes_to_erase = tuple(i for i in self._shapes.shapes_ids if in_a_sheet(i) is None)
            # try:
            #     self._interactor.erase_shapes_by_shape_ids(shapes_to_erase)
            # except:
            #     pass

            self._interactor.save_state_to_file(folder_name)

    def test_dependencies(self):
        path_test_pickles = self._path_test_pickles
        pickle_name = 'test_circular_reference'

        self._interactor.change_path_pickles(path_test_pickles)
        self._interactor.load_file(pickle_name)

        dependencies = self._interactor.get_dependencies('cash_eb')
        expectation = {'+_1', '+_2', '/', 'base', 'bb', 'cash_bb', 'cash_eb', 'interest_income', 'interest_rate', 'two',
                       'x'}
        self.assertEqual(dependencies, expectation)
        self.assertEqual(self._interactor.is_circular('cash_eb'), True)
        expectation = {'+_2', 'cash_eb', 'base', '+_1', 'x', 'interest_income', '/'}
        circular_dependencies = self._interactor.get_minimum_circular_dependencies('cash_eb')
        self.assertEqual(set(circular_dependencies), expectation)

    def test_circular_reference(self):
        path_test_pickles = self._path_test_pickles

        # Circular reference
        pickle_name = 'test_circular_reference'
        self._interactor.change_path_pickles(path_test_pickles)
        self._interactor.load_file(pickle_name)
        expectation = (('+_2', '/'),
                       ('x', 'interest_income'),
                       ('cash_eb', '+_2'),
                       ('+_1', 'cash_eb'),
                       ('/', 'base'),
                       ('base', 'x'),
                       ('interest_income', '+_1'))
        for un_ordered_data in self._interactor.get_circular_connections():
            self.assertIn(un_ordered_data, expectation)

        # No circular reference
        pickle_name = 'test_inventory_model'
        self._interactor.load_file(pickle_name)
        self.assertEqual(self._interactor.get_circular_connections(), ())

    def test_vba_user_defined_function(self):
        path_test_pickles = self._path_test_pickles
        pickle_name = 'test_circular_reference'
        self._interactor.change_path_pickles(path_test_pickles)

        self._interactor.load_file(pickle_name)
        gateway_model = self._interactor.create_gateway_model_for_vba_uda('cash_eb')
        expectation = {'arguments': ('var_cash_bb_cash_bb', 'var_interest_rate_rate'),
                       'direct_links_mutable': (),
                       'folder_name': None,
                       'formulas': ('var_base_base = (var_cash_bb_cash_bb+var_cash_eb_cash_eb)/2',
                                    'var_cash_eb_cash_eb = var_cash_bb_cash_bb+var_interest_income_interest',
                                    'var_interest_income_interest = var_base_base*var_interest_rate_rate'),
                       'name': 'user_defined_function',
                       'max_loop': 10000,
                       'target_value': 'var_cash_eb_cash_eb',
                       'tolerance': 0.0001,
                       'variables': ('var_base_base',
                                     'var_cash_bb_cash_bb',
                                     'var_cash_eb_cash_eb',
                                     'var_interest_income_interest',
                                     'var_interest_rate_rate'),
                       'minimum_iteration': 10, }
        for key, value in gateway_model.items():
            self.assertEqual(value, expectation[key])

        pickle_name = 'test_excel_with_udf'
        self._interactor.load_file(pickle_name)
        gateway_model = self._interactor.create_gateway_model_for_vba_uda(156)
        expectation = {'arguments': ('var_65_ebit',
                                     'var_67_delta_working_capital',
                                     'var_68_depreciation',
                                     'var_69_amortization',
                                     'var_116_ebit',
                                     'var_158_draw_down',
                                     'var_164_interest_payment',
                                     'var_166_avaialble_cash',
                                     'var_168_cfi',
                                     'var_171_cash_bb',
                                     'var_172_plug_interest_rate',
                                     'var_240_revolver_bb',
                                     'var_247_plug_interest_rate',
                                     'var_257_interest_expense',
                                     'var_269_repayment',
                                     'var_308_income_tax_rate'),
                       'direct_links_mutable': (('var_70_total_cfo', 'var_98_cash_flow_from_operation'),
                                                ('var_139_total_interest_income', 'var_117_interest_income'),
                                                ('var_138_total_interest_expense', 'var_118_interest_expense'),
                                                ('var_165_remaining_cash', 'var_157_available_cash'),
                                                ('var_98_cash_flow_from_operation', 'var_167_cfo'),
                                                ('var_228_remaining_cash', 'var_219_cash_eb'),
                                                ('var_156_remaining_cash', 'var_229_available_cash'),
                                                ('var_230_revolver_dd', 'var_241_draw_down'),
                                                ('var_231_revolver_repayment', 'var_242_repayment'),
                                                ('var_323_cf_revolver_interest', 'var_290_revolver_interest'),
                                                ('var_327_cf_interest_on_cash', 'var_292_cash_interest'),
                                                ('var_119_ebt', 'var_309_taxable_income')),
                       'folder_name': None,
                       'formulas': ('var_66_tax_payment = var_215_cf_tax_payment+0',
                                    'var_70_total_cfo = '
                                    'var_65_ebit+var_66_tax_payment+var_67_delta_working_capital+var_69_amortization+var_68_depreciation',
                                    'var_119_ebt = var_116_ebit-var_118_interest_expense+var_117_interest_income',
                                    'var_138_total_interest_expense = '
                                    'var_257_interest_expense+var_253_revolver_interest',
                                    'var_139_total_interest_income = var_173_interest_on_cash+0',
                                    'var_156_remaining_cash = '
                                    'var_157_available_cash+var_158_draw_down+var_159_repayment+var_164_interest_payment+var_290_revolver_interest+var_292_cash_interest',
                                    'var_159_repayment = min(max(var_157_available_cash+var_158_draw_down, 0), '
                                    'var_269_repayment)*-1',
                                    'var_165_remaining_cash = var_166_avaialble_cash+var_167_cfo+var_168_cfi',
                                    'var_173_interest_on_cash = var_172_plug_interest_rate*var_218_base',
                                    'var_215_cf_tax_payment = -1*var_310_income_tax_expense',
                                    'var_218_base = (var_219_cash_eb+var_171_cash_bb)/2',
                                    'var_228_remaining_cash = '
                                    'var_229_available_cash+var_230_revolver_dd+var_231_revolver_repayment',
                                    'var_230_revolver_dd = -1*min(0, var_229_available_cash)',
                                    'var_231_revolver_repayment = -1*min(max(var_240_revolver_bb, 0), '
                                    'max(var_229_available_cash, 0))',
                                    'var_239_revolver = var_240_revolver_bb+var_241_draw_down+var_242_repayment',
                                    'var_253_revolver_interest = var_259_base*var_247_plug_interest_rate',
                                    'var_259_base = (var_240_revolver_bb+var_239_revolver)/2',
                                    'var_310_income_tax_expense = var_308_income_tax_rate*var_309_taxable_income',
                                    'var_323_cf_revolver_interest = var_253_revolver_interest*-1',
                                    'var_327_cf_interest_on_cash = var_173_interest_on_cash+0'),
                       'name': 'user_defined_function',
                       'max_loop': 10000,
                       'target_value': 'var_156_remaining_cash',
                       'tolerance': 0.0001,
                       'variables': ('var_100_cash_flow_from_financing',
                                     'var_101_cash_bb',
                                     'var_107_revenue',
                                     'var_108_cost_of_goods',
                                     'var_10_other_cl',
                                     'var_110_sga',
                                     'var_111_other_expenses',
                                     'var_112_other_incomes',
                                     'var_114_depreciation',
                                     'var_115_amortization',
                                     'var_116_ebit',
                                     'var_117_interest_income',
                                     'var_118_interest_expense',
                                     'var_119_ebt',
                                     'var_11_plug__revolver',
                                     'var_120_tax',
                                     'var_138_total_interest_expense',
                                     'var_139_total_interest_income',
                                     'var_156_remaining_cash',
                                     'var_157_available_cash',
                                     'var_158_draw_down',
                                     'var_159_repayment',
                                     'var_15_other',
                                     'var_164_interest_payment',
                                     'var_165_remaining_cash',
                                     'var_166_avaialble_cash',
                                     'var_167_cfo',
                                     'var_168_cfi',
                                     'var_16_retained_earnings',
                                     'var_171_cash_bb',
                                     'var_172_plug_interest_rate',
                                     'var_173_interest_on_cash',
                                     'var_17_paid_in_capital',
                                     'var_183_cash_from_bs',
                                     'var_190_net_cash_balance',
                                     'var_195_cash_from_bs',
                                     'var_198_tolerance',
                                     'var_1_non_current_assets',
                                     'var_200_remaining_cash',
                                     'var_215_cf_tax_payment',
                                     'var_218_base',
                                     'var_219_cash_eb',
                                     'var_226_loan_bb',
                                     'var_227_draw_down',
                                     'var_228_remaining_cash',
                                     'var_229_available_cash',
                                     'var_230_revolver_dd',
                                     'var_231_revolver_repayment',
                                     'var_236_cash_bb',
                                     'var_239_revolver',
                                     'var_240_revolver_bb',
                                     'var_241_draw_down',
                                     'var_242_repayment',
                                     'var_247_plug_interest_rate',
                                     'var_253_revolver_interest',
                                     'var_257_interest_expense',
                                     'var_259_base',
                                     'var_266_base',
                                     'var_269_repayment',
                                     'var_290_revolver_interest',
                                     'var_292_cash_interest',
                                     'var_308_income_tax_rate',
                                     'var_309_taxable_income',
                                     'var_310_income_tax_expense',
                                     'var_323_cf_revolver_interest',
                                     'var_327_cf_interest_on_cash',
                                     'var_357_total_assets',
                                     'var_358_total_liabilities',
                                     'var_359_total_equity',
                                     'var_365_tolerance',
                                     'var_375_cash_from_cf',
                                     'var_378_tolerance',
                                     'var_380_remaining_cash',
                                     'var_4_cash',
                                     'var_58_retained_earnings_bb',
                                     'var_59_net_income',
                                     'var_5_non_current_liabilities',
                                     'var_65_ebit',
                                     'var_66_tax_payment',
                                     'var_67_delta_working_capital',
                                     'var_68_depreciation',
                                     'var_69_amortization',
                                     'var_6_non_cash',
                                     'var_70_total_cfo',
                                     'var_98_cash_flow_from_operation',
                                     'var_99_cash_flow_from_investing'),
                       'minimum_iteration': 10, }
        for key, value in gateway_model.items():
            self.assertEqual(value, expectation[key])

    def test_spreadsheet_with_udf(self):
        path_test_pickles = self._path_test_pickles
        from src.Entities.AccountOrder import Blank
        blank = Blank()
        self._interactor.change_path_pickles(path_test_pickles)
        self._interactor.load_file('test_excel_with_udf')
        self._interactor.selection.select_shape(156)
        expectations = {
            'workbook_name': '/Users/yamaka/Desktop/Excel.xlsx',
            'shape_id_to_address': {0: 'Total Assets',
                                    1: 'Non Current Assets',
                                    2: 'Current Assets',
                                    3: 'Total Liabilities',
                                    4: 'Cash',
                                    5: 'Non Current Liabilities',
                                    6: 'Non Cash',
                                    7: '+',
                                    8: '+',
                                    9: 'Current Liabilities',
                                    10: 'Other CL',
                                    11: 'Plug - Revolver',
                                    12: '+',
                                    13: '+',
                                    14: 'Total Equity',
                                    15: 'Other',
                                    16: 'Retained Earnings',
                                    17: 'Paid in Capital',
                                    18: '+',
                                    19: 'Total Account Receivable',
                                    20: 'Total Inventory',
                                    21: 'Total Non Cash Current Assets',
                                    22: 'Total PPE Cost',
                                    23: 'Total Acc Depreciation',
                                    24: 'Total Non Current Assets',
                                    25: 'Account Payable',
                                    26: 'Interest Payable',
                                    27: 'Dividend Payable',
                                    28: 'Tax Payable',
                                    29: 'Other CL',
                                    30: 'Total Non Plug Current Liabilities',
                                    31: 'Loan',
                                    32: 'Other NC Liabilities',
                                    33: 'Total Non Current Liabilities',
                                    34: 'Total Paid in Capital',
                                    35: 'Total Other Equity',
                                    36: '+',
                                    37: '+',
                                    38: '+',
                                    39: '+',
                                    40: '+',
                                    41: '+',
                                    42: '+',
                                    43: '+',
                                    44: '+',
                                    45: '+',
                                    46: '+',
                                    47: '+',
                                    48: '+',
                                    49: '+',
                                    50: '+',
                                    51: '+',
                                    52: '+',
                                    53: 'Total Non Plug Current Liabilities',
                                    54: 'Total Non Current Liabilities',
                                    55: 'Total Paid in Capital',
                                    56: 'Total Other Equity',
                                    57: 'Retained Earnings',
                                    58: 'Retained Earnings BB',
                                    59: 'Net Income',
                                    60: 'Dividend Payout',
                                    61: '+',
                                    62: 'BB',
                                    63: '+',
                                    64: 'Retained Earnings',
                                    65: 'EBIT',
                                    66: 'Tax Payment',
                                    67: 'Delta Working Capital',
                                    68: 'Depreciation',
                                    69: 'Amortization',
                                    70: 'Total CFO',
                                    71: 'Capex',
                                    72: 'Proceeds from asset sales',
                                    73: 'Total CFI',
                                    74: 'Stock Issuance',
                                    75: 'Dividend Payout',
                                    76: 'Stock Repurchase',
                                    77: 'Debt Issuance',
                                    78: 'Interest Payment',
                                    79: 'Debt Repayment',
                                    80: 'Other',
                                    81: 'Total CFF',
                                    82: '+',
                                    83: '+',
                                    84: '+',
                                    85: '+',
                                    86: '+',
                                    87: '+',
                                    88: '+',
                                    89: '+',
                                    90: '+',
                                    91: '+',
                                    92: '+',
                                    93: '+',
                                    94: '+',
                                    95: '+',
                                    96: '+',
                                    97: 'Total Cash Flow',
                                    98: 'Cash Flow from Operation',
                                    99: 'Cash Flow from Investing',
                                    100: 'Cash Flow from Financing',
                                    101: 'Cash BB',
                                    102: 'Cash',
                                    103: '+',
                                    104: '+',
                                    105: 'BB',
                                    106: '+',
                                    107: 'Revenue',
                                    108: 'Cost of Goods',
                                    109: 'Gross Profit',
                                    110: 'SG&A',
                                    111: 'Other expenses',
                                    112: 'Other incomes',
                                    113: 'EBITDA',
                                    114: 'Depreciation',
                                    115: 'Amortization',
                                    116: 'EBIT',
                                    117: 'Interest Income',
                                    118: 'Interest Expense',
                                    119: 'EBT',
                                    120: 'Tax',
                                    121: 'Net Income',
                                    122: '-',
                                    123: '-',
                                    124: '+',
                                    125: '+',
                                    126: '-',
                                    127: '+',
                                    128: '+',
                                    129: '-',
                                    130: '-',
                                    131: 'Total Revenue',
                                    132: 'Total COGS',
                                    133: 'Total SGA',
                                    134: 'Total Other Expense',
                                    135: 'Total Other Income',
                                    136: 'Total Depreciation',
                                    137: 'Total Amortization',
                                    138: 'Total Interest Expense',
                                    139: 'Total Interest Income',
                                    140: 'Total Tax Expense',
                                    141: '+',
                                    142: '+',
                                    143: '+',
                                    144: '+',
                                    145: '+',
                                    146: '+',
                                    147: '+',
                                    148: '+',
                                    149: '+',
                                    150: '+',
                                    151: 'Net Income',
                                    152: 'EBIT',
                                    153: 'Cash',
                                    154: 'Cash Flow from Operation',
                                    155: 'Cash Flow from Investing',
                                    156: 'Remaining Cash',
                                    157: 'Available Cash',
                                    158: 'Draw Down',
                                    159: 'Repayment',
                                    160: '+',
                                    161: '+',
                                    162: 'x',
                                    163: '-1',
                                    164: 'Interest Payment',
                                    165: 'Remaining Cash',
                                    166: 'Avaialble Cash',
                                    167: 'CFO',
                                    168: 'CFI',
                                    169: '+',
                                    170: 'Cash BB',
                                    171: 'Cash BB',
                                    172: 'Plug Interest Rate',
                                    173: 'Interest on Cash',
                                    174: 'Plug Interest Rate',
                                    175: 'CF Revolver Interest',
                                    176: 'Revolver Interest',
                                    177: 'Revolver',
                                    178: 'Draw Down',
                                    179: '+',
                                    180: 'CF Interest on Cash',
                                    181: 'Repayment',
                                    182: 'Interest on Cash',
                                    183: 'Cash from BS',
                                    184: 'Cash from CF',
                                    185: 'Difference',
                                    186: 'abs',
                                    187: 'Results',
                                    188: 'max',
                                    189: '0',
                                    190: 'Net Cash Balance',
                                    191: '-',
                                    192: 'Tolerance',
                                    193: 'Cash',
                                    194: 'Cash',
                                    195: 'Cash from BS',
                                    196: 'Cash from CFWF',
                                    197: 'Difference',
                                    198: 'Tolerance',
                                    199: 'Results',
                                    200: 'Remaining Cash',
                                    201: 'max',
                                    202: '0',
                                    203: '-',
                                    204: 'abs',
                                    205: '<',
                                    206: 'Remaining Cash',
                                    207: 'Cash',
                                    208: 'Remaining Cash',
                                    209: 'Cash',
                                    210: 'Tolerance',
                                    211: 'Remaining Cash',
                                    212: '/',
                                    213: '2',
                                    214: 'Remaining Cash',
                                    215: 'CF Tax Payment',
                                    216: 'BB',
                                    217: '-1',
                                    218: 'Base',
                                    219: 'Cash EB',
                                    220: 'Price',
                                    221: 'Volume',
                                    222: 'Revenue',
                                    223: 'x',
                                    224: 'Revenue',
                                    225: 'Loan',
                                    226: 'Loan BB',
                                    227: 'Draw Down',
                                    228: 'Remaining Cash',
                                    229: 'Available Cash',
                                    230: 'Revolver DD',
                                    231: 'Revolver Repayment',
                                    232: '+',
                                    233: '0',
                                    234: 'max',
                                    235: 'Repayment',
                                    236: 'Cash BB',
                                    237: '+',
                                    238: 'min',
                                    239: 'Revolver',
                                    240: 'Revolver BB',
                                    241: 'Draw Down',
                                    242: 'Repayment',
                                    243: '+',
                                    244: 'BB',
                                    245: 'BB',
                                    246: 'Draw Down',
                                    247: 'Plug Interest Rate',
                                    248: 'Interest Rate',
                                    249: 'Revolver DD',
                                    250: 'x',
                                    251: 'BB weight',
                                    252: '1',
                                    253: 'Revolver Interest',
                                    254: 'x',
                                    255: 'EB weight',
                                    256: '-',
                                    257: 'Interest Expense',
                                    258: '<',
                                    259: 'Base',
                                    260: 'Base',
                                    261: 'Loan BB',
                                    262: 'x',
                                    263: 'Available Cash',
                                    264: '+',
                                    265: 'x',
                                    266: 'Base',
                                    267: 'Loan',
                                    268: 'Draw Down',
                                    269: 'Repayment',
                                    270: 'Repayment',
                                    271: '-1',
                                    272: 'x',
                                    273: 'CF Interest',
                                    274: '-1',
                                    275: 'x',
                                    276: '0',
                                    277: 'max',
                                    278: 'Loan',
                                    279: '-1',
                                    280: 'x',
                                    281: 'Revolver Repayment',
                                    282: '0',
                                    283: 'min',
                                    284: '-1',
                                    285: 'x',
                                    286: 'Draw Down',
                                    287: 'Interest Expense',
                                    288: 'Repayment',
                                    289: 'CF Interest',
                                    290: 'Revolver Interest',
                                    291: 'Repayment',
                                    292: 'Cash Interest',
                                    293: 'Draw Down',
                                    294: 'x',
                                    295: 'CF Interest',
                                    296: 'Revolver BB',
                                    297: 'x',
                                    298: 'CF Tax Payment',
                                    299: 'Income Tax Expense',
                                    300: 'EBT',
                                    308: 'Income Tax Rate',
                                    309: 'Taxable Income',
                                    310: 'Income Tax Expense',
                                    311: 'x',
                                    320: '0',
                                    321: 'max',
                                    322: 'min',
                                    323: 'CF Revolver Interest',
                                    324: '-1',
                                    325: 'x',
                                    326: '+',
                                    327: 'CF Interest on Cash',
                                    328: 'CF Revolver Interest',
                                    329: 'CF Interest on Cash',
                                    346: '+',
                                    347: '/',
                                    348: '2',
                                    349: 'Revolver BB',
                                    350: 'Revolver',
                                    357: 'Total Assets',
                                    358: 'Total Liabilities',
                                    359: 'Total Equity',
                                    360: 'Dr Cr match',
                                    361: '+',
                                    362: '-',
                                    363: 'abs',
                                    364: '<=',
                                    365: 'Tolerance',
                                    366: 'Results',
                                    367: 'Total Assets',
                                    368: 'Total Liabilities',
                                    369: 'Total Equity',
                                    375: 'Cash from CF',
                                    376: 'Cash from CFWF',
                                    377: 'Difference',
                                    378: 'Tolerance',
                                    379: 'Results',
                                    380: 'Remaining Cash',
                                    381: 'max',
                                    382: '0',
                                    383: '-',
                                    384: 'abs',
                                    385: '<'},
            'inputs': (247, 192, 220, 221, 246, 248, 251, 269, 308),
            'input_values': ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                             (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
            'operators': (7,
                          8,
                          12,
                          13,
                          18,
                          36,
                          37,
                          38,
                          39,
                          40,
                          41,
                          42,
                          43,
                          44,
                          45,
                          46,
                          47,
                          48,
                          49,
                          50,
                          51,
                          52,
                          61,
                          63,
                          82,
                          83,
                          84,
                          85,
                          86,
                          87,
                          88,
                          89,
                          90,
                          91,
                          92,
                          93,
                          94,
                          95,
                          96,
                          103,
                          104,
                          106,
                          122,
                          123,
                          124,
                          125,
                          126,
                          127,
                          128,
                          129,
                          130,
                          141,
                          142,
                          143,
                          144,
                          145,
                          146,
                          147,
                          148,
                          149,
                          150,
                          169,
                          160,
                          161,
                          162,
                          232,
                          243,
                          250,
                          277,
                          280,
                          283,
                          285,
                          238,
                          234,
                          294,
                          321,
                          322,
                          325,
                          326,
                          186,
                          188,
                          191,
                          258,
                          201,
                          203,
                          204,
                          205,
                          381,
                          383,
                          384,
                          385,
                          361,
                          362,
                          363,
                          364,
                          346,
                          347,
                          179,
                          212,
                          223,
                          237,
                          254,
                          256,
                          262,
                          264,
                          265,
                          272,
                          275,
                          311,
                          297),
            'constants': (163,
                          276,
                          279,
                          282,
                          284,
                          233,
                          320,
                          324,
                          189,
                          202,
                          382,
                          348,
                          213,
                          252,
                          271,
                          274,
                          217),
            'sheets_data': {'Audit': (190,
                                      183,
                                      184,
                                      185,
                                      192,
                                      187,
                                      blank,
                                      200,
                                      195,
                                      196,
                                      197,
                                      198,
                                      199,
                                      blank,
                                      380,
                                      375,
                                      376,
                                      377,
                                      378,
                                      379,
                                      blank,
                                      365,
                                      357,
                                      358,
                                      359,
                                      360,
                                      366,
                                      blank),
                            'BS': (4,
                                   6,
                                   2,
                                   1,
                                   0,
                                   blank,
                                   10,
                                   11,
                                   9,
                                   5,
                                   3,
                                   blank,
                                   17,
                                   16,
                                   15,
                                   14,
                                   blank,
                                   19,
                                   20,
                                   21,
                                   blank,
                                   22,
                                   23,
                                   24,
                                   blank,
                                   25,
                                   26,
                                   27,
                                   28,
                                   29,
                                   30,
                                   blank,
                                   31,
                                   32,
                                   33,
                                   blank,
                                   34,
                                   blank,
                                   35,
                                   blank,
                                   58,
                                   59,
                                   60,
                                   57),
                            'CF': (65,
                                   66,
                                   67,
                                   68,
                                   69,
                                   70,
                                   blank,
                                   71,
                                   72,
                                   73,
                                   blank,
                                   74,
                                   75,
                                   76,
                                   77,
                                   78,
                                   79,
                                   80,
                                   81,
                                   blank,
                                   101,
                                   blank,
                                   98,
                                   99,
                                   100,
                                   97,
                                   blank,
                                   102,
                                   blank),
                            'CFWF': (236,
                                     blank,
                                     166,
                                     167,
                                     168,
                                     165,
                                     blank,
                                     157,
                                     158,
                                     159,
                                     164,
                                     290,
                                     292,
                                     156,
                                     blank,
                                     229,
                                     230,
                                     231,
                                     228,
                                     blank,
                                     240,
                                     241,
                                     242,
                                     239,
                                     blank,
                                     259,
                                     247,
                                     253,
                                     blank,
                                     323,
                                     blank,
                                     171,
                                     219,
                                     blank,
                                     218,
                                     172,
                                     173,
                                     blank,
                                     327,
                                     blank),
                            'IS': (107,
                                   108,
                                   109,
                                   blank,
                                   110,
                                   111,
                                   112,
                                   113,
                                   blank,
                                   114,
                                   115,
                                   116,
                                   blank,
                                   118,
                                   117,
                                   119,
                                   blank,
                                   120,
                                   121,
                                   blank,
                                   131,
                                   blank,
                                   132,
                                   blank,
                                   133,
                                   blank,
                                   134,
                                   blank,
                                   135,
                                   blank,
                                   136,
                                   blank,
                                   137,
                                   blank,
                                   138,
                                   blank,
                                   139,
                                   blank,
                                   140,
                                   blank),
                            'Sheet1': (blank,
                                       blank,
                                       blank,
                                       221,
                                       220,
                                       222,
                                       blank,
                                       246,
                                       269,
                                       blank,
                                       226,
                                       227,
                                       235,
                                       225,
                                       blank,
                                       251,
                                       255,
                                       260,
                                       blank,
                                       266,
                                       248,
                                       257,
                                       blank,
                                       273,
                                       blank,
                                       308,
                                       309,
                                       310,
                                       blank,
                                       215,
                                       blank)},
            'rpes': ((2, (4, 6, 7)),
                     (0, (1, 2, 8)),
                     (9, (10, 11, 12)),
                     (3, (5, 9, 13)),
                     (14, (15, 16, 18, 17, 18)),
                     (21, (19, 20, 36)),
                     (24, (22, 23, 37)),
                     (30, (28, 29, 38, 25, 38, 26, 38, 27, 38)),
                     (33, (31, 32, 39)),
                     (19, (40,)),
                     (20, (41,)),
                     (22, (42,)),
                     (23, (43,)),
                     (25, (44,)),
                     (26, (45,)),
                     (27, (46,)),
                     (28, (47,)),
                     (29, (48,)),
                     (31, (225, 49)),
                     (32, (50,)),
                     (34, (51,)),
                     (35, (52,)),
                     (57, (58, 59, 61, 60, 61)),
                     (60, (63,)),
                     (67, (82,)),
                     (68, (83,)),
                     (69, (84,)),
                     (71, (85,)),
                     (72, (86,)),
                     (74, (87,)),
                     (75, (88,)),
                     (76, (89,)),
                     (77, (227, 241, 90)),
                     (78, (273, 323, 91, 327, 91)),
                     (79, (235, 242, 92)),
                     (80, (93,)),
                     (70, (65, 66, 94, 67, 94, 69, 94, 68, 94)),
                     (73, (71, 72, 95)),
                     (81, (74, 75, 96, 76, 96, 77, 96, 78, 96, 79, 96, 80, 96)),
                     (97, (98, 99, 103, 100, 103)),
                     (102, (97, 101, 104)),
                     (66, (215, 106)),
                     (109, (107, 108, 122)),
                     (113, (109, 110, 111, 124, 123, 112, 125)),
                     (116, (113, 114, 115, 127, 126)),
                     (119, (116, 118, 129, 117, 128)),
                     (121, (119, 120, 130)),
                     (131, (222, 141)),
                     (132, (142,)),
                     (133, (143,)),
                     (134, (144,)),
                     (135, (145,)),
                     (136, (146,)),
                     (137, (147,)),
                     (138, (257, 253, 148)),
                     (139, (173, 149)),
                     (140, (310, 150)),
                     (165, (166, 167, 169, 168, 169)),
                     (156, (157, 158, 160, 159, 160, 164, 160, 290, 160, 292, 160)),
                     (159, (157, 158, 161, 320, 321, 269, 322, 163, 162)),
                     (228, (229, 230, 232, 231, 232)),
                     (239, (240, 241, 243, 242, 243)),
                     (253, (259, 247, 250)),
                     (231, (279, 240, 276, 277, 229, 233, 234, 238, 280)),
                     (230, (284, 282, 229, 283, 285)),
                     (173, (172, 218, 294)),
                     (323, (253, 324, 325)),
                     (327, (173, 326)),
                     (184, (189, 190, 188)),
                     (185, (183, 184, 191)),
                     (187, (185, 186, 192, 258)),
                     (196, (202, 200, 201)),
                     (197, (195, 196, 203)),
                     (199, (197, 204, 198, 205)),
                     (376, (382, 380, 381)),
                     (377, (375, 376, 383)),
                     (379, (377, 384, 378, 385)),
                     (360, (357, 358, 359, 361, 362)),
                     (366, (360, 363, 365, 364)),
                     (259, (240, 239, 346, 348, 347)),
                     (218, (219, 171, 179, 213, 212)),
                     (222, (220, 221, 223)),
                     (225, (226, 227, 237, 235, 237)),
                     (257, (266, 248, 254)),
                     (255, (252, 251, 256)),
                     (260, (226, 251, 262, 225, 255, 265, 264)),
                     (235, (271, 269, 272)),
                     (273, (257, 274, 275)),
                     (310, (308, 309, 311)),
                     (215, (217, 310, 297))),
            'nop': 10,
            'direct_links_mutable': ((21, 6, 0),
                                     (3, 358, 0),
                                     (136, 114, 0),
                                     (102, 375, 0),
                                     (135, 112, 0),
                                     (139, 117, 0),
                                     (73, 99, 0),
                                     (70, 98, 0),
                                     (132, 108, 0),
                                     (138, 118, 0),
                                     (228, 219, 0),
                                     (14, 359, 0),
                                     (231, 242, 0),
                                     (35, 15, 0),
                                     (228, 380, 0),
                                     (323, 290, 0),
                                     (273, 164, 0),
                                     (327, 292, 0),
                                     (121, 59, 0),
                                     (119, 309, 0),
                                     (165, 157, 0),
                                     (192, 365, 0),
                                     (24, 1, 0),
                                     (34, 17, 0),
                                     (30, 10, 0),
                                     (230, 241, 0),
                                     (102, 190, 0),
                                     (236, 166, 0),
                                     (98, 167, 0),
                                     (246, 227, 0),
                                     (239, 11, 0),
                                     (133, 110, 0),
                                     (247, 172, 0),
                                     (228, 4, 0),
                                     (57, 16, 0),
                                     (134, 111, 0),
                                     (236, 171, 0),
                                     (260, 266, 0),
                                     (99, 168, 0),
                                     (192, 378, 0),
                                     (140, 120, 0),
                                     (156, 229, 0),
                                     (137, 115, 0),
                                     (116, 65, 0),
                                     (228, 200, 0),
                                     (33, 5, 0),
                                     (246, 158, 0),
                                     (4, 195, 0),
                                     (131, 107, 0),
                                     (81, 100, 0),
                                     (192, 198, 0),
                                     (0, 357, 0),
                                     (4, 183, 0),
                                     (57, 58, -1),
                                     (102, 101, -1),
                                     (4, 236, -1),
                                     (239, 240, -1),
                                     (225, 226, -1)),
        }
        gateway_model = self._interactor.create_gateway_model_to_spreadsheet()
        for actual, expectation in zip(gateway_model, expectations):
            self.assertEqual(actual, expectation)

    def test_vertical_account(self):
        path_test_pickles = self._path_test_pickles
        pickle_name = 'test_vertical_account'
        interactor = self._interactor
        interactor.change_path_pickles(path_test_pickles)
        interactor.load_file(pickle_name)

        interactor.add_vertical_account(4)
        self.assertEqual(interactor._entities._vertical_accounts.data, {4: ()})

        interactor.add_vertical_account(6)
        self.assertEqual(interactor._entities._vertical_accounts.data, {4: ()})

        interactor.add_vertical_reference(4, 3)
        self.assertEqual(interactor._entities._vertical_accounts.data, {4: (3,)})

        interactor.remove_vertical_account(6)
        self.assertEqual(interactor._entities._vertical_accounts.data, {4: (3,)})

        interactor.remove_vertical_reference(4, 3)
        interactor.remove_vertical_reference(4, 5)
        self.assertEqual(interactor._entities._vertical_accounts.data, {4: ()})

        interactor.remove_vertical_account(4)
        self.assertEqual(interactor._entities._vertical_accounts.data, {})

        interactor.add_vertical_account(4)
        interactor.add_vertical_reference(4, 0)
        interactor.add_vertical_reference(4, 1)
        interactor.add_vertical_account(3)
        interactor.add_vertical_reference(3, 1)
        interactor.add_vertical_reference(3, 2)
        self.assertEqual(interactor._entities._vertical_accounts.data, {3: (1, 2), 4: (0, 1)})
        interactor.remove_vertical_reference_from_all_vertical_accounts(1)
        self.assertEqual(interactor._entities._vertical_accounts.data, {3: (2,), 4: (0,)})

    def test_select_shape_by_name(self):
        interactor = self._interactor
        interactor.add_new_shape('Account1', 'account')  # 0
        interactor.add_new_shape('Account1', 'account')  # 1
        interactor.add_new_shape('Account2', 'account')  # 2
        interactor.add_new_shape('Account3', 'account')  # 3
        interactor.add_new_shape('Account1', 'account')  # 4

        interactor.select_account_by_name('Account1', nth=2)
        self.assertEqual(interactor._selection.data, {4})

        interactor.select_account_by_name('Account1', nth=1)
        self.assertEqual(interactor._selection.data, {1})

        interactor.add_new_worksheet('Sheet_X')
        interactor.add_new_shape('Account1', 'account')  # 5
        interactor.add_new_shape('Account1', 'account')  # 6
        interactor.add_new_shape('Account2', 'account')  # 7
        interactor.add_new_shape('Account3', 'account')  # 8
        interactor.add_new_shape('Account1', 'account')  # 9

        interactor.select_account_by_name('Account1', 'Sheet1', 1)
        self.assertEqual(interactor._selection.data, {1})

        interactor.select_account_by_name(*('Account1', 'Sheet_X', 1))
        self.assertEqual(interactor._selection.data, {6})

    def test_macros(self):
        from src.Entities import Observable, Blank
        path_test_pickles = self._path_test_pickles
        blank = Blank()
        Observable.is_debug_mode = False
        interactor = self._interactor
        interactor.change_path_command_pickles(path_test_pickles)
        interactor.merge_macro('Test_Commands')
        interactor.run_macro()

        gateway_model = interactor.create_gateway_model_to_spreadsheet()
        no_need_to_test_vba_file(gateway_model)
        expected_gateway_model = {'workbook_name': '/Users/yamaka/Desktop/Excel.xlsx',
                                  'shape_id_to_address': {0: 'Period', 1: 'Income Statement', 2: 'Revenue',
                                                          3: 'Cost of Goods', 4: 'Gross Profit', 5: 'SG&A',
                                                          6: 'Other expenses', 7: 'Other incomes', 8: 'EBITDA',
                                                          9: 'Depreciation', 10: 'Amortization', 11: 'EBIT',
                                                          12: 'Interest Expense', 13: 'Interest Income', 14: 'EBT',
                                                          15: 'Income Tax Current', 16: 'Income Tax Deferred',
                                                          17: 'Net Income', 18: '-', 19: '-', 20: '+', 21: '+', 22: '-',
                                                          23: '+', 24: '+', 25: '-', 26: '-', 27: 'Balance Sheet',
                                                          28: 'Cash', 29: 'Non Cash', 30: 'Current Assets',
                                                          31: 'Non Current Assets', 32: 'Total Assets', 33: 'Other CL',
                                                          34: 'Plug - Revolver', 35: 'Current Liabilities',
                                                          36: 'Non Current Liabilities', 37: 'Total Liabilities',
                                                          38: 'Paid in Capital', 39: 'Retained Earnings', 40: 'Other',
                                                          41: 'Total Equity', 42: '+', 43: '+', 44: '+', 45: '+',
                                                          46: '+', 47: 'Cash Flow Statement', 48: 'Cash BB',
                                                          49: 'Cash Flow from Operation',
                                                          50: 'Cash Flow from Investing',
                                                          51: 'Cash Flow from Financing', 52: 'Total Cash Flow',
                                                          53: 'Cash', 54: '+', 55: '+', 56: 'BB', 57: 'Ratios',
                                                          58: 'Current Assets', 59: 'Current Liabilities', 60: 'Cash',
                                                          61: 'Marketable Securities', 62: 'Net Receivables',
                                                          63: 'Net Credit Sales', 64: 'BB Net AR', 65: 'Net AR',
                                                          66: 'Average net Receivables', 67: 'COGS', 68: 'Inventory',
                                                          69: 'BB Inventory', 70: 'Average Inventory', 71: 'BB WC',
                                                          72: 'Average Working Capital', 73: 'BB Total Assets',
                                                          74: 'Average Total Assets', 75: 'Net Income',
                                                          76: 'Gross Profit', 77: 'EBITDA', 78: 'Tax Rate',
                                                          79: 'Interest Expense', 80: 'Interest Expense after Tax',
                                                          81: 'BB Total LT Liabilities', 82: 'Average LT Liabilities',
                                                          83: 'BB Total Equity', 84: 'Average Equity',
                                                          85: 'Total Liabilities', 86: 'Total Assets', 87: 'EBIT',
                                                          88: 'CFO', 89: 'Total Equity', 90: 'Working Capital',
                                                          91: 'Current Ratio', 92: 'Acid Test Ratio', 93: 'Cash Ratio',
                                                          94: 'AR Turnover in X times', 95: 'AR Turnover in X days',
                                                          96: 'Inventory Turnoverin X times',
                                                          97: 'Inventory Turnoverin X days', 98: 'Operating Cycle',
                                                          99: 'Working Capital Turnover', 100: 'Asset Turnover',
                                                          101: 'Net Income Margin', 102: 'Gross Profit Margin',
                                                          103: 'EBITDA Margin', 104: 'Return on Asset',
                                                          105: 'Return on Investment', 106: 'Debt to Equity Ratio',
                                                          107: 'Debt Ratio', 108: 'Times Interest Earned',
                                                          109: 'CFO to Total Debt', 110: 'Current Assets',
                                                          111: 'Current Liabilities', 112: '-', 113: '/',
                                                          114: 'Current Liabilities', 115: 'Marketable Securities',
                                                          116: 'Net Receivables', 117: '+', 118: '/', 119: '+',
                                                          120: 'Cash', 121: '/', 122: 'Net Credit Sales',
                                                          123: 'Average net Receivables', 124: '/', 125: '365',
                                                          126: '/', 127: 'COGS', 128: 'Average Inventory', 129: '/',
                                                          130: '/', 131: '+', 132: 'Average Working Capital',
                                                          133: 'Net Credit Sales', 134: '/', 135: '/',
                                                          136: 'Average Total Assets', 137: 'Net Income', 138: '/',
                                                          139: 'Gross Profit', 140: 'EBITDA', 141: '/', 142: '/',
                                                          143: 'Average Total Assets', 144: 'Net Income', 145: '/',
                                                          146: 'Average LT Liabilities', 147: 'Net Income',
                                                          148: 'Average Equity', 149: 'Interest Expense after Tax',
                                                          150: '+', 151: '-', 152: '/', 153: 'Total Equity',
                                                          154: 'Total Liabilities', 155: '/', 156: 'Total Assets',
                                                          157: 'Total Liabilities', 158: '/', 159: '/', 160: 'EBIT',
                                                          161: 'Interest Expense', 162: 'CFO', 163: 'Total Liabilities',
                                                          164: '/', 165: 'Total Assets', 166: 'BB', 167: '+', 168: '/',
                                                          169: '2', 170: '+', 171: '/', 172: 'BB', 173: '2',
                                                          174: 'Total Equity', 175: '+', 176: '/', 177: 'BB', 178: '2',
                                                          179: 'Total Liabilities', 180: '+', 181: '/', 182: '2',
                                                          183: 'BB', 184: '+', 185: '/', 186: '2', 187: 'BB',
                                                          188: 'Working Capital', 189: '1', 190: '-', 191: 'x',
                                                          192: '+', 193: '/', 194: '2', 195: 'BB', 196: 'EBIT',
                                                          197: 'Cash', 198: 'Period', 199: 'Total Liabilities',
                                                          200: 'Cost of Goods', 201: 'Interest Expense',
                                                          202: 'Net Income', 203: 'EBITDA', 204: 'Total Equity',
                                                          205: 'Current Assets', 206: 'Revenue',
                                                          207: 'Current Liabilities', 208: 'Cash Flow from Operation',
                                                          209: 'Total Assets', 210: 'Gross Profit', 211: 'IS Accounts',
                                                          212: 'Total Revenue', 213: 'Total COGS', 214: 'Total SGA',
                                                          215: 'Total Other Expense', 216: 'Total Other Income',
                                                          217: 'Total Depreciation', 218: 'Total Amortization',
                                                          219: 'Total Interest Expense', 220: 'Total Interest Income',
                                                          221: 'Total Income Tax Current',
                                                          222: 'Total Income Tax Deferred', 223: '+', 224: '+',
                                                          225: '+', 226: '+', 227: '+', 228: '+', 229: '+', 230: '+',
                                                          231: '+', 232: '+', 233: '+', 234: 'Total COGS',
                                                          235: 'Total Other Expense', 236: 'Total Interest Expense',
                                                          237: 'Total Other Income', 238: 'Total Depreciation',
                                                          239: 'Total Amortization', 240: 'Total Income Tax Current',
                                                          241: 'Total Interest Income', 242: 'Period',
                                                          243: 'Total Income Tax Deferred', 244: 'Total Revenue',
                                                          245: 'Total SGA', 246: 'BS Accounts',
                                                          247: 'Total Account Receivable', 248: 'Total Inventory',
                                                          249: 'Total Non Cash Current Assets',
                                                          250: 'Deferred Tax Asset', 251: 'Total PPE Cost',
                                                          252: 'Total Acc Depreciation',
                                                          253: 'Total Non Current Assets', 254: 'Account Payable',
                                                          255: 'Interest Payable', 256: 'Dividend Payable',
                                                          257: 'Tax Payable', 258: 'Other CL',
                                                          259: 'Total Non Plug Current Liabilities',
                                                          260: 'Deferred Tax Liability', 261: 'Loan',
                                                          262: 'Other NC Liabilities',
                                                          263: 'Total Non Current Liabilities',
                                                          264: 'Total Paid in Capital', 265: 'Total Other Equity',
                                                          266: '+', 267: '+', 268: '+', 269: '+', 270: '+', 271: '+',
                                                          272: '+', 273: '+', 274: '+', 275: '+', 276: '+', 277: '+',
                                                          278: '+', 279: '+', 280: '+', 281: '+', 282: '+', 283: '+',
                                                          284: '+', 285: 'Total Non Cash Current Assets', 286: 'Period',
                                                          287: 'Total Other Equity', 288: 'Total Paid in Capital',
                                                          289: 'Total Account Receivable',
                                                          290: 'Total Non Plug Current Liabilities',
                                                          291: 'Total Account Receivable',
                                                          292: 'Total Non Current Liabilities',
                                                          293: 'Total Non Current Assets', 294: 'Total Inventory',
                                                          295: 'Retained Earnings BB', 296: 'Net Income',
                                                          297: 'Dividend Payout', 298: 'Retained Earnings', 299: '+',
                                                          300: 'BB', 301: '+', 302: 'Net Income',
                                                          303: 'Retained Earnings', 304: 'CF Accounts', 305: 'EBIT',
                                                          306: 'Tax Payment', 307: 'Delta Working Capital',
                                                          308: 'Depreciation', 309: 'Amortization', 310: 'Total CFO',
                                                          311: 'Capex', 312: 'Proceeds from asset sales',
                                                          313: 'Total CFI', 314: 'Stock Issuance',
                                                          315: 'Dividend Payout', 316: 'Stock Repurchase',
                                                          317: 'Debt Issuance', 318: 'Interest Payment',
                                                          319: 'Debt Repayment', 320: 'Other', 321: 'Total CFF',
                                                          322: '+', 323: '+', 324: '+', 325: '+', 326: '+', 327: '+',
                                                          328: '+', 329: '+', 330: '+', 331: '+', 332: '+', 333: '+',
                                                          334: '+', 335: '+', 336: '+', 337: '+', 338: 'Total CFF',
                                                          339: 'Period', 340: 'Total CFI', 341: 'Total CFO',
                                                          342: 'EBIT', 343: 'Plug', 344: 'Non Cash CA',
                                                          345: 'Non Current Assets', 346: 'Total Equity',
                                                          347: 'Non Plug CL', 348: 'Liabilities NC',
                                                          349: 'Non cash assets', 350: 'Net Cash', 351: 'Excess Cash',
                                                          352: 'Cash', 353: 'Cash Deficit', 354: 'Plug', 355: 'Plug BB',
                                                          356: 'Plug', 357: 'delta Revolver', 358: 'Draw Down Revolver',
                                                          359: 'Repayment Revolver', 360: '+', 361: '+', 362: '-',
                                                          363: 'max', 364: '0', 365: '0', 366: 'min', 367: '-1',
                                                          368: 'x', 369: 'BB', 370: '-', 371: 'max', 372: 'min',
                                                          373: '0', 374: '0', 375: 'Other CL',
                                                          376: 'Non Current Liabilities', 377: 'Period',
                                                          378: 'Non Current Assets', 379: 'Cash', 380: 'Total Equity',
                                                          381: 'Plug', 382: 'Non Cash', 383: 'Plug Interest',
                                                          384: 'Plug Interest Rate', 385: 'Cash Deficit',
                                                          386: 'Excess Cash BB', 387: 'Interest Rate',
                                                          388: 'Plug Interest Income', 389: 'Cash Deficit BB',
                                                          390: 'Interest Rate', 391: 'Plug Interest Expense',
                                                          392: 'CF Plug Interest', 393: 'BB', 394: 'BB', 395: 'x',
                                                          396: 'x', 397: 'Plug Interest Expense', 398: '+', 399: '-1',
                                                          400: 'x', 401: '-1', 402: 'x', 403: 'Period',
                                                          404: 'Tolerance', 405: 'Audit BS', 406: 'Tolerance',
                                                          407: 'Total Assets', 408: 'Total Liabilities',
                                                          409: 'Total Equity', 410: 'Dr Cr match', 411: 'Results',
                                                          412: '+', 413: '-', 414: 'abs', 415: '<=',
                                                          416: 'Total Equity', 417: 'Period', 418: 'Total Liabilities',
                                                          419: 'Total Assets', 420: 'Audit Cash - BS vs CF',
                                                          421: 'Net Cash Balance', 422: 'Cash from BS',
                                                          423: 'Cash from CF', 424: 'Difference', 425: 'Tolerance',
                                                          426: 'Results', 427: 'abs', 428: 'max', 429: '0', 430: '-',
                                                          431: '<', 432: 'Cash', 433: 'Cash', 434: 'Period',
                                                          435: 'Revenue Name', 436: 'Volume', 437: 'Price',
                                                          438: 'Revenue', 439: 'x', 440: 'Period', 441: 'Revenue',
                                                          442: 'Cost of Goods Sold', 443: 'Volume', 444: 'Unit Cost',
                                                          445: 'COGS', 446: 'x', 447: 'COGS', 448: 'Period',
                                                          449: 'Account Receivable', 450: 'Base',
                                                          451: 'Receivable Outstanding Rate', 452: 'Receivable BB',
                                                          453: 'increase', 454: 'decrease', 455: 'Receivable',
                                                          456: 'CF AR movement', 457: '+', 458: 'BB', 459: 'x',
                                                          460: '-1', 461: 'x', 462: 'decrease', 463: 'increase',
                                                          464: '+', 465: '-1', 466: 'x', 467: 'Receivable',
                                                          468: 'Period', 469: 'CF AR movement', 470: 'Accounts Payable',
                                                          471: 'Base', 472: 'Payable Outstanding Rate',
                                                          473: 'Payable BB', 474: 'increase', 475: 'decrease',
                                                          476: 'Payable', 477: 'CF AP movement', 478: 'decrease',
                                                          479: 'increase', 480: 'x', 481: 'x', 482: '+', 483: '+',
                                                          484: 'BB', 485: '-1', 486: 'CF AP movement', 487: 'Payable',
                                                          488: 'Period', 489: 'Inventory', 490: 'Volume Out',
                                                          491: 'Inventory Volume BB', 492: 'Volume Increase',
                                                          493: 'Volume Decrease', 494: 'Inventory Volume',
                                                          495: 'Inventory Unit Cost BB', 496: 'Unit Cost In',
                                                          497: 'Unit Cost Out', 498: 'Inventory Unit Cost',
                                                          499: 'Inventory Value BB', 500: 'Value increase',
                                                          501: 'Value decrease', 502: 'Inventory Value',
                                                          503: 'CF Inventory movement', 504: '+', 505: 'BB', 506: 'BB',
                                                          507: '+', 508: 'BB', 509: 'Unit Cost In',
                                                          510: 'Volume Increase', 511: 'x', 512: 'Unit Cost Out',
                                                          513: 'Volume decrease', 514: 'x', 515: 'Inventory Value BB',
                                                          516: 'Value increase', 517: 'Inventory Volume BB',
                                                          518: 'Volume Increase', 519: '+', 520: '+', 521: '/',
                                                          522: '-1', 523: 'x', 524: '-1', 525: 'Value increase',
                                                          526: 'Value decrease', 527: '+', 528: 'x', 529: 'Period',
                                                          530: 'CF Inventory movement', 531: 'Inventory Value',
                                                          532: 'Capex & Depreciation - Straight Line', 533: 'Period',
                                                          534: 'Capex', 535: 'Life - Straight Line', 536: 'After',
                                                          537: 'Depreciation Start', 538: 'Cost BB', 539: 'increase',
                                                          540: 'decrease', 541: 'Cost EB', 542: 'AD BB',
                                                          543: 'increase', 544: 'decrease',
                                                          545: 'Accumulated Depreciation', 546: 'Depreciation',
                                                          547: 'CF Capex', 548: 'Depreciation',
                                                          549: 'Accumulated Depreciation', 550: '+', 551: 'BB',
                                                          552: '+', 553: 'BB', 554: '+', 555: '+', 556: 'Capex',
                                                          557: '-1', 558: 'x', 559: '+', 560: '<=',
                                                          561: 'Depreciation Start', 562: 'Period', 563: '+',
                                                          564: 'Depreciation Start', 565: 'Period', 566: '<',
                                                          567: 'Capex', 568: '/', 569: 'Life - Straight Line', 570: 'x',
                                                          571: 'Depreciation', 572: 'Accumulated Depreciation',
                                                          573: 'x', 574: '-1', 575: 'Period', 576: 'Cost EB',
                                                          577: 'CF Capex', 578: 'Depreciation',
                                                          579: 'Accumulated Depreciation', 580: 'Depreciation',
                                                          581: 'Taxable Income', 582: 'Earning Before Tax',
                                                          583: 'Permanent difference for IPTA',
                                                          584: 'Temporary difference for IPTA',
                                                          585: 'Taxable Income Before LCF', 586: 'Tax Losses',
                                                          587: 'NOL Used', 588: 'NOL Expired',
                                                          589: 'Taxable Income after LCF', 590: 'Income Tax Rate',
                                                          591: 'Income Tax Current', 592: 'NOL Expiry schedule',
                                                          593: 'NOL life', 594: 'Expire Period', 595: 'Tax Losses',
                                                          596: 'NOL Expiry per Schedule', 597: 'Expiry vs Sheild',
                                                          598: 'NOL Expiry per Shedule', 599: 'NOL Shield Used',
                                                          600: 'NOL Expired', 601: 'NOL Calculation', 602: 'BB NOL',
                                                          603: 'NOL Expired', 604: 'Tax Losses', 605: 'NOL Used',
                                                          606: 'Net Operating Loss', 607: 'NOL Shield',
                                                          608: 'BB NOL Shield', 609: 'NOL Used', 610: 'NOL Shield Used',
                                                          611: 'NOL Shield', 612: 'Deferred Tax',
                                                          613: 'Net Operating Loss', 614: 'Income Tax Rate',
                                                          615: 'Deferred Tax Asset LCF',
                                                          616: 'Acc Temporary difference', 617: 'Income Tax Rate',
                                                          618: 'Deferred Tax Asset IPTA', 619: 'Deferred Tax Asset',
                                                          620: 'Deferred Tax Liability', 621: 'BB DTA', 622: 'BB DTL',
                                                          623: 'delta DTA', 624: 'delta DTL',
                                                          625: 'Income Tax Deferred', 626: 'Cash Flow Impact',
                                                          627: 'Tax Payament', 628: 'Temporary Difference BB',
                                                          629: 'increase', 630: 'Acc Temporary Difference', 631: '+',
                                                          632: '-1', 633: 'max', 634: '0', 635: 'x',
                                                          636: 'Taxable Income Before LCF', 637: 'NOL Used', 638: '+',
                                                          639: 'x', 640: 'Tax Losses', 641: 'NOL Expiry per Schedule',
                                                          642: 'NOL Shield Used', 643: '+', 644: 'BB', 645: '-1',
                                                          646: 'x', 647: 'NOL Expired', 648: 'Tax Losses', 649: '-1',
                                                          650: 'max', 651: 'min', 652: '0', 653: '+', 654: 'x',
                                                          655: 'Taxable Income Before LCF', 656: 'BB NOL',
                                                          657: 'NOL Expired', 658: '+', 659: 'BB', 660: '+', 661: '-1',
                                                          662: 'x', 663: 'NOL Used', 664: '-1', 665: 'min',
                                                          666: 'BB NOL Shield', 667: 'NOL Expiry per Schedule',
                                                          668: 'x', 669: 'x', 670: 'Income Tax Rate',
                                                          671: 'Net Operating Loss', 672: '+', 673: 'BB',
                                                          674: 'Temporary difference for IPTA',
                                                          675: 'Acc Temporary Difference', 676: 'Income Tax Rate',
                                                          677: 'max', 678: 'x', 679: '0', 680: 'min', 681: '0',
                                                          682: 'x', 683: '-1', 684: '+', 685: 'x', 686: '=', 687: 'x',
                                                          688: '-1', 689: 'Income Tax Current', 690: 'NOL Expired',
                                                          691: '+', 692: 'BB', 693: '-', 694: 'BB',
                                                          695: 'Deferred Tax Asset', 696: 'Deferred Tax Liability',
                                                          697: 'x', 698: '-1', 699: '-', 700: '+', 701: 'Period',
                                                          702: 'Period', 703: 'Income Tax Deferred',
                                                          704: 'Deferred Tax Asset', 705: 'Period', 706: 'Period',
                                                          707: 'Deferred Tax Liability', 708: 'Income Tax Rate',
                                                          709: 'Period', 710: 'Income Tax Current', 711: 'Period',
                                                          712: 'Tax Payament', 713: 'Period', 714: 'EBT'},
                                  'inputs': (
                                      0, 61, 384, 404, 436, 437, 451, 472, 492, 496, 534, 535, 536, 583, 584, 590, 593),
                                  'input_values': (
                                      (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0),
                                      (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                      (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (
                                          0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001,
                                          0.001,
                                          0.001, 0.001, 0.001), (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                      (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                      (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                      (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                      (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                      (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                      (10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                                      (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                      (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                      (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                      (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                      (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                      (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
                                  'operators': (
                                      18, 19, 20, 21, 22, 23, 24, 25, 26, 42, 43, 44, 45, 46, 54, 55, 112, 113, 117,
                                      118,
                                      119, 121, 124, 126, 129, 130, 131, 134, 135, 138, 141, 142, 145, 150, 151, 152,
                                      155,
                                      158, 159, 164, 167, 168, 170, 171, 175, 176, 180, 181, 184, 185, 190, 191, 192,
                                      193,
                                      223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 266, 267, 268, 269, 270,
                                      271,
                                      272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 299, 301, 322,
                                      323,
                                      324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 360, 361,
                                      362,
                                      363, 366, 368, 370, 371, 372, 395, 396, 398, 400, 402, 412, 413, 414, 415, 427,
                                      428,
                                      430, 431, 439, 446, 457, 459, 461, 464, 466, 480, 481, 482, 483, 504, 507, 511,
                                      514,
                                      519, 520, 521, 523, 527, 528, 550, 552, 554, 555, 558, 559, 560, 563, 566, 568,
                                      570,
                                      573, 631, 633, 635, 638, 639, 643, 646, 650, 651, 653, 654, 658, 660, 662, 665,
                                      668,
                                      669, 672, 677, 678, 680, 682, 684, 685, 686, 687, 691, 693, 697, 699, 700),
                                  'constants': (
                                      125, 169, 173, 178, 182, 186, 189, 194, 364, 365, 367, 373, 374, 399, 401, 429,
                                      460,
                                      465, 485, 522, 524, 557, 574, 632, 634, 645, 649, 652, 661, 664, 679, 681, 683,
                                      688,
                                      698),
                                  'sheets_data':
                                      {'FS': (
                                          0, blank, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, blank,
                                          27,
                                          28, 29, 30, 31, 32, blank, 33, 34, 35, 36, 37, blank, 38, 39, 40, 41, blank,
                                          47,
                                          48, blank, 49, 50, 51, 52, blank, 53, blank),
                                          'Ratios': (
                                              57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
                                              75, 76,
                                              77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, blank, 90, 91, 92, 93,
                                              94,
                                              95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                                              blank,
                                              blank),
                                          'Model': (
                                              211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, blank, 246,
                                              247, 248,
                                              249, blank, 250, 251, 252, 253, blank, 254, 255, 256, 257, 258, 259,
                                              blank, 260,
                                              261, 262, 263, blank, 264, blank, 265, blank, 295, 296, 297, 298, blank,
                                              304,
                                              305, 306, 307, 308, 309, 310, blank, 311, 312, 313, blank, 314, 315, 316,
                                              317,
                                              318, 319, 320, 321, blank, 343, 344, 345, blank, 346, 347, 348, 349, 350,
                                              blank,
                                              351, 352, blank, 353, 354, blank, 355, 356, 357, blank, 358, 359, blank,
                                              383,
                                              384, 385, blank, 386, 387, 388, blank, 389, 390, 391, blank, 392, blank),
                                          'Audit': (
                                              404, blank, 405, 406, blank, 407, 408, 409, 410, blank, 411, blank, 420,
                                              421,
                                              blank, 422, 423, 424, blank, 425, 426, blank),
                                          'GP': (
                                              435, 436, 437, 438, blank, 442, 443, 444, 445, blank, 449, 450, 451,
                                              blank, 452,
                                              453, 454, 455, blank, 456, blank, 470, 471, 472, blank, 473, 474, 475,
                                              476,
                                              blank, 477, blank),
                                          'Inventory': (
                                              489, 490, blank, 491, 492, 493, 494, blank, 495, 496, 497, 498, blank,
                                              499, 500,
                                              501, 502, blank, 503, blank),
                                          'CAPEX': (
                                              532, 533, 534, 535, 536, 537, blank, 538, 539, 540, 541, blank, 542, 543,
                                              544,
                                              545, blank, 546, blank, 547, 548, 549, blank),
                                          'Tax': (
                                              581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, blank, 592, 593,
                                              594, 595,
                                              596, blank, 597, 598, 599, 600, blank, 601, 602, 603, 604, 605, 606,
                                              blank, 607,
                                              608, 609, 610, 611, blank, 612, 613, 614, 615, blank, 616, 617, 618,
                                              blank, 619,
                                              620, blank, 621, 622, blank, 623, 624, 625, blank, 626, 627, blank, 628,
                                              629,
                                              630, blank)},
                                  'rpes': ((4, (2, 3, 18)), (8, (4, 5, 6, 20, 19, 7, 21)), (11, (8, 9, 10, 23, 22)),
                                           (14, (11, 12, 25, 13, 24)), (17, (14, 15, 26, 16, 26)), (30, (28, 29, 42)),
                                           (32, (30, 31, 43)), (35, (33, 34, 44)), (37, (35, 36, 45)),
                                           (41, (38, 39, 46, 40, 46)), (52, (49, 50, 54, 51, 54)), (53, (48, 52, 55)),
                                           (90, (58, 59, 112)), (91, (58, 59, 113)),
                                           (92, (61, 62, 117, 60, 117, 59, 118)), (93, (61, 60, 119, 59, 121)),
                                           (94, (63, 66, 124)), (95, (125, 94, 126)), (96, (67, 70, 129)),
                                           (97, (125, 96, 130)), (98, (95, 97, 131)), (99, (63, 72, 134)),
                                           (100, (63, 74, 135)), (101, (63, 75, 138)), (102, (63, 76, 141)),
                                           (103, (63, 77, 142)), (104, (75, 74, 145)),
                                           (105, (75, 80, 151, 84, 82, 150, 152)), (106, (85, 89, 155)),
                                           (107, (85, 86, 158)), (108, (79, 87, 159)), (109, (88, 85, 164)),
                                           (74, (86, 73, 167, 169, 168)), (84, (89, 83, 170, 173, 171)),
                                           (82, (85, 81, 175, 178, 176)), (66, (65, 64, 180, 182, 181)),
                                           (72, (90, 71, 184, 186, 185)), (80, (189, 78, 190, 79, 191)),
                                           (70, (68, 69, 192, 194, 193)), (212, (438, 223)), (213, (445, 224)),
                                           (214, (225,)), (215, (226,)), (216, (227,)), (217, (548, 228)),
                                           (218, (229,)), (219, (391, 230)), (220, (388, 231)), (221, (591, 232)),
                                           (222, (625, 233)), (249, (247, 248, 266)), (253, (250, 251, 267, 252, 267)),
                                           (259, (257, 258, 268, 254, 268, 255, 268, 256, 268)),
                                           (263, (260, 261, 269, 262, 269)), (247, (455, 270)), (248, (502, 271)),
                                           (251, (541, 272)), (252, (549, 273)), (254, (476, 274)), (255, (275,)),
                                           (256, (276,)), (257, (277,)), (258, (278,)), (261, (279,)), (262, (280,)),
                                           (264, (281,)), (265, (282,)), (250, (619, 283)), (260, (620, 284)),
                                           (298, (295, 296, 299, 297, 299)), (297, (301,)),
                                           (307, (456, 477, 322, 503, 322)), (308, (548, 323)), (309, (324,)),
                                           (311, (547, 325)), (312, (326,)), (314, (327,)), (315, (328,)),
                                           (316, (329,)), (317, (358, 330)), (318, (392, 331)), (319, (359, 332)),
                                           (320, (333,)), (310, (305, 306, 334, 307, 334, 309, 334, 308, 334)),
                                           (313, (311, 312, 335)),
                                           (321, (314, 315, 336, 316, 336, 317, 336, 318, 336, 319, 336, 320, 336)),
                                           (306, (627, 337)), (349, (344, 345, 360)),
                                           (350, (346, 347, 361, 348, 361, 349, 362)), (351, (364, 350, 363)),
                                           (353, (350, 365, 366)), (354, (367, 353, 368)), (357, (356, 355, 370)),
                                           (358, (357, 373, 371)), (359, (374, 357, 372)), (388, (387, 386, 395)),
                                           (391, (390, 389, 396)), (392, (388, 391, 401, 402, 398)),
                                           (389, (399, 385, 400)), (410, (407, 408, 409, 412, 413)),
                                           (411, (410, 414, 406, 415)), (423, (421, 429, 428)), (424, (422, 423, 430)),
                                           (426, (424, 427, 425, 431)), (438, (437, 436, 439)), (445, (443, 444, 446)),
                                           (455, (452, 453, 457, 454, 457)), (453, (450, 451, 459)),
                                           (454, (452, 460, 461)), (456, (465, 454, 453, 464, 466)),
                                           (474, (471, 472, 480)), (475, (473, 485, 481)),
                                           (476, (473, 474, 482, 475, 482)), (477, (475, 474, 483)),
                                           (494, (491, 492, 504, 493, 504)), (502, (499, 500, 507, 501, 507)),
                                           (500, (496, 492, 511)), (501, (497, 493, 514)),
                                           (497, (499, 500, 519, 491, 492, 520, 521)), (493, (522, 490, 523)),
                                           (503, (501, 500, 527, 524, 528)), (541, (538, 539, 550, 540, 550)),
                                           (545, (542, 543, 552, 544, 552)), (540, (554,)), (544, (555,)),
                                           (547, (557, 534, 558)), (537, (533, 536, 559)),
                                           (546, (537, 533, 560, 533, 535, 537, 563, 566, 570, 534, 535, 568, 570)),
                                           (549, (545, 574, 573)), (585, (582, 583, 631, 584, 631)),
                                           (586, (585, 632, 635, 634, 633)), (589, (587, 585, 638, 586, 638, 588, 638)),
                                           (591, (589, 590, 639)), (600, (598, 599, 643)), (603, (600, 645, 646)),
                                           (605, (585, 602, 603, 653, 651, 652, 650, 649, 654)),
                                           (606, (605, 602, 658, 603, 658, 604, 658)), (611, (608, 609, 660, 610, 660)),
                                           (609, (605, 661, 662)), (610, (664, 608, 596, 665, 668)),
                                           (615, (613, 614, 669)), (630, (628, 629, 672)),
                                           (618, (616, 617, 678, 679, 677)), (620, (683, 616, 617, 678, 681, 680, 682)),
                                           (594, (592, 593, 684)), (596, (595, 592, 594, 686, 685)),
                                           (627, (688, 591, 687)), (619, (615, 618, 691)),
                                           (623, (698, 621, 619, 693, 697)), (624, (622, 620, 699)),
                                           (625, (623, 624, 700))),
                                  'nop': 15,
                                  'direct_links_mutable': (
                                      (0, 470, 0), (0, 489, 0), (29, 344, 0), (352, 28, 0), (384, 390, 0), (0, 405, 0),
                                      (351, 352, 0), (445, 471, 0), (438, 450, 0), (17, 75, 0), (2, 63, 0),
                                      (248, 68, 0),
                                      (0, 612, 0), (35, 59, 0), (17, 296, 0), (534, 539, 0), (41, 346, 0), (36, 348, 0),
                                      (0, 449, 0), (354, 356, 0), (213, 3, 0), (321, 51, 0), (32, 86, 0), (497, 498, 0),
                                      (32, 407, 0), (259, 33, 0), (0, 57, 0), (630, 616, 0), (590, 617, 0),
                                      (354, 34, 0),
                                      (217, 9, 0), (0, 442, 0), (11, 87, 0), (49, 88, 0), (28, 60, 0), (249, 29, 0),
                                      (216, 7, 0), (606, 613, 0), (0, 27, 0), (53, 421, 0), (0, 626, 0), (0, 592, 0),
                                      (596, 598, 0), (0, 211, 0), (605, 587, 0), (31, 345, 0), (263, 36, 0),
                                      (532, 533, 0),
                                      (264, 38, 0), (310, 49, 0), (218, 10, 0), (222, 16, 0), (0, 383, 0), (0, 581, 0),
                                      (436, 443, 0), (603, 588, 0), (0, 343, 0), (546, 548, 0), (37, 408, 0),
                                      (4, 76, 0),
                                      (384, 387, 0), (28, 422, 0), (265, 40, 0), (41, 409, 0), (436, 490, 0),
                                      (220, 13, 0),
                                      (247, 62, 0), (0, 532, 0), (610, 599, 0), (404, 425, 0), (546, 543, 0),
                                      (253, 31, 0),
                                      (12, 79, 0), (30, 58, 0), (214, 5, 0), (41, 89, 0), (0, 304, 0), (0, 601, 0),
                                      (404, 406, 0), (586, 604, 0), (14, 582, 0), (221, 15, 0), (0, 420, 0),
                                      (590, 614, 0),
                                      (0, 435, 0), (247, 65, 0), (298, 39, 0), (584, 629, 0), (11, 305, 0), (0, 47, 0),
                                      (497, 444, 0), (37, 85, 0), (33, 347, 0), (219, 12, 0), (0, 597, 0), (0, 607, 0),
                                      (586, 595, 0), (0, 246, 0), (212, 2, 0), (8, 77, 0), (0, 1, 0), (590, 78, 0),
                                      (3, 67, 0), (313, 50, 0), (215, 6, 0), (53, 48, -1), (86, 73, -1), (89, 83, -1),
                                      (85, 81, -1), (65, 64, -1), (90, 71, -1), (68, 69, -1), (298, 295, -1),
                                      (356, 355, -1), (351, 386, -1), (353, 385, -1), (455, 452, -1), (476, 473, -1),
                                      (494, 491, -1), (498, 495, -1), (502, 499, -1), (541, 538, -1), (545, 542, -1),
                                      (606, 602, -1), (611, 608, -1), (630, 628, -1), (620, 622, -1), (619, 621, -1)),
                                  'format_data': {None: (
                                      0, 2, 3, 5, 6, 7, 9, 10, 12, 13, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28,
                                      29,
                                      30, 31, 33, 34, 35, 36, 38, 39, 40, 42, 43, 44, 45, 46, 49, 50, 51, 54, 55, 56,
                                      58,
                                      59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78,
                                      79,
                                      80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
                                      100,
                                      101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
                                      117,
                                      118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133,
                                      134,
                                      135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150,
                                      151,
                                      152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167,
                                      168,
                                      169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184,
                                      185,
                                      186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 212, 213, 214, 215, 216, 217,
                                      218,
                                      219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 247,
                                      248,
                                      250, 251, 252, 254, 255, 256, 257, 258, 260, 261, 262, 264, 265, 266, 267, 268,
                                      269,
                                      270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 295,
                                      296,
                                      297, 299, 300, 301, 305, 306, 307, 308, 309, 311, 312, 314, 315, 316, 317, 318,
                                      319,
                                      320, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336,
                                      337,
                                      344, 345, 346, 347, 348, 349, 351, 353, 355, 357, 360, 361, 362, 363, 364, 365,
                                      366,
                                      367, 368, 369, 370, 371, 372, 373, 374, 384, 386, 387, 389, 390, 393, 394, 395,
                                      396,
                                      397, 398, 399, 400, 401, 402, 404, 406, 407, 408, 409, 410, 412, 413, 414, 415,
                                      421,
                                      422, 423, 424, 425, 427, 428, 429, 430, 431, 436, 437, 439, 443, 444, 446, 450,
                                      451,
                                      452, 453, 454, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 471, 472, 473,
                                      474,
                                      475, 478, 479, 480, 481, 482, 483, 484, 485, 490, 491, 492, 493, 495, 496, 497,
                                      499,
                                      500, 501, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517,
                                      518,
                                      519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 533, 534, 535, 536, 537, 538,
                                      539,
                                      540, 542, 543, 544, 546, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560,
                                      561,
                                      562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 582, 583, 584,
                                      586,
                                      587, 588, 590, 593, 594, 595, 598, 599, 602, 603, 604, 605, 608, 609, 610, 613,
                                      614,
                                      616, 617, 621, 622, 623, 624, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636,
                                      637,
                                      638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653,
                                      654,
                                      655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670,
                                      671,
                                      672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687,
                                      688,
                                      689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700),
                                      'heading': (
                                          1, 27, 47, 57, 211, 246, 304, 343, 383, 405, 420, 435, 442, 449, 470,
                                          489, 532, 581, 592, 597, 601, 607, 612, 626),
                                      'total': (
                                          4, 8, 11, 14, 17, 32, 37, 41, 48, 52, 53, 249, 253, 259, 263, 298,
                                          310, 313, 321, 350, 352, 354, 356, 358, 359, 385, 388, 391, 392, 411,
                                          426, 438, 445, 455, 456, 476, 477, 494, 498, 502, 503, 541, 545, 547,
                                          548, 549, 585, 589, 591, 596, 600, 606, 611, 615, 618, 619, 620,
                                          625)},
                                  'number_format_data': {''
                                                         'whole number': (0, 1, 27, 47), None: (
                                      2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                      24,
                                      25, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
                                      46,
                                      48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67,
                                      68,
                                      69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88,
                                      89,
                                      90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107,
                                      108,
                                      109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124,
                                      125,
                                      126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141,
                                      142,
                                      143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158,
                                      159,
                                      160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175,
                                      176,
                                      177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192,
                                      193,
                                      194, 195, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224,
                                      225,
                                      226, 227, 228, 229, 230, 231, 232, 233, 246, 247, 248, 249, 250, 251, 252, 253,
                                      254,
                                      255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270,
                                      271,
                                      272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 295, 296, 297,
                                      298,
                                      299, 300, 301, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316,
                                      317,
                                      318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333,
                                      334,
                                      335, 336, 337, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355,
                                      356,
                                      357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372,
                                      373,
                                      374, 383, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398,
                                      399,
                                      400, 401, 402, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 420,
                                      421,
                                      422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 435, 436, 437, 438, 439, 442,
                                      443,
                                      444, 445, 446, 449, 450, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462,
                                      463,
                                      464, 465, 466, 470, 471, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483,
                                      484,
                                      485, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503,
                                      504,
                                      505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520,
                                      521,
                                      522, 523, 524, 525, 526, 527, 528, 532, 533, 534, 535, 536, 537, 538, 539, 540,
                                      541,
                                      542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557,
                                      558,
                                      559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574,
                                      581,
                                      582, 583, 584, 585, 586, 587, 588, 589, 591, 592, 593, 594, 595, 596, 597, 598,
                                      599,
                                      600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615,
                                      616,
                                      617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632,
                                      633,
                                      634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649,
                                      650,
                                      651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666,
                                      667,
                                      668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683,
                                      684,
                                      685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700),
                                                         '%': (384, 451, 472, 590), ''
                                                                                    '2-digit': ()},
                                  'vertical_acs': {546: (535, 537, 534), 596: (595, 594)},
                                  'shape_id_to_uom': {}}

        for key in gateway_model.keys():
            g = gateway_model[key]
            expectation = expected_gateway_model[key]
            if key in ('shape_id_to_address',):
                # For some reason, Win and Mac produces different order. Below does not test order. Just contents [set]
                self.assertEqual(tuple(g.keys()), tuple(expectation.keys()))
                self.assertEqual(set(tuple(g.values())), set(tuple(expectation.values())))
            elif key in ('direct_links_mutable',):
                # For some reason, Win and Mac produces different order. Below does not test order. Just contents [set]
                self.assertEqual(set(g), set(expectation))
            else:
                self.assertEqual(g, expectation)
        Observable.is_debug_mode = True

    def test_import_lib(self):
        import importlib.resources
        import pickle
        with importlib.resources.open_binary('src.Pickles', 'Tr AR') as f:
            memento = pickle.load(f)
        self.assertEqual(hasattr(memento, '_state'), True)

    def _run_tests(self, command, test_cases):
        expectations, request_models = test_cases()
        command(request_models)
        self._test(expectations)

    def _test(self, expectations):
        for n, expectation in enumerate(expectations):
            data = self._get_data_from_notification(n, expectations)
            self.assertEqual(data, expectation)

    def _get_recent(self, n: int, expectations) -> int:
        return self._notification_catcher.kwargs[-len(expectations) + n]['data']

    def _get_interactor_add_shape(self, n: int, _) -> int:
        target_notifications = []
        flag = False
        for notification in self._notification_catcher.kwargs:
            if notification['method'] != 'set_y':
                flag = True
            else:
                if flag:
                    # Append the last 'set_y' notifications.
                    target_notifications = []
                    flag = False
                target_notifications.append(notification)
        return target_notifications[n]['data'][n]


class TestPresenter(unittest.TestCase):
    def setUp(self) -> None:
        from .catchers import ViewResponseModelCatcher
        self._view = ViewResponseModelCatcher()

    def _test_presenter(self, presenter, test_cases):
        presenter.attach(self._view.view_method)
        expected_view_models, response_models = test_cases()
        for response_model, expected_view_model in zip(response_models, expected_view_models):
            presenter.present(response_model)
            self.assertEqual(self._view.view_model_passed[-1], expected_view_model)

    def test_presenter_add_shape(self):
        from src.Presenter import PresenterAddShape
        self._test_presenter(PresenterAddShape(), tc.test_cases_presenter_add_shape)

    def test_presenter_clear_canvas(self):
        from src.Presenter import PresenterClearCanvas
        self._test_presenter(PresenterClearCanvas(), tc.test_cases_presenter_clear_canvas)

    def test_presenter_connect_shape(self):
        from src.Presenter import PresenterConnectShape
        self._test_presenter(PresenterConnectShape(), tc.test_cases_presenter_connect_shape)

    def test_presenter_draw_line(self):
        from src.Presenter import PresenterDrawLine
        self._test_presenter(PresenterDrawLine(), tc.test_cases_presenter_draw_line)

    def test_presenter_draw_rectangle(self):
        from src.Presenter import PresenterDrawRectangle
        self._test_presenter(PresenterDrawRectangle(), tc.test_cases_presenter_draw_rectangle)

    def test_presenter_highlight_shape(self):
        from src.Presenter import PresenterHighlightShape
        self._test_presenter(PresenterHighlightShape(), tc.test_cases_presenter_highlight_shape_auto)

    def test_presenter_move_shape(self):
        from src.Presenter import PresenterMoveShape
        self._test_presenter(PresenterMoveShape(), tc.test_cases_presenter_move_shape)

    def test_presenter_remove_shape(self):
        from src.Presenter import PresenterRemoveShape
        self._test_presenter(PresenterRemoveShape(), tc.test_cases_presenter_remove_shape)

    def test_presenter_update_status_bar(self):
        from src.Presenter import PresenterFeedbackUser
        self._test_presenter(PresenterFeedbackUser(), tc.test_cases_presenter_update_status_bar)

    def test_presenter_load_pickle_files_list(self):
        from src.Presenter import PresenterLoadPickleFilesList
        self._test_presenter(PresenterLoadPickleFilesList(), tc.test_cases_presenter_load_pickle_files_list)


def add_shapes(object_to_test):
    request_models = tc.test_cases_add_new_shape()[1]
    object_to_test.add_new_shapes(request_models)


if __name__ == '__main__':
    unittest.main()
