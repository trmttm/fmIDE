from Utilities.Memento import Memento

from fmIDE import instantiate_app
from src.Entities.AccountOrder import AccountOrder
from src.Entities.AccountOrder import Blank
from src.Entities.Selection import Selection

account_orders = [AccountOrder(),
                  AccountOrder(), ]
account_orders[1].set_data((1, 2, 3, 4, Blank()))
account_orders[0].set_data((0,))

selections = [
    Selection(),
    Selection(),
]
state = [
    {(6, 1), (5, 4), (0, 6), (2, 5), (3, 5)},
    {2},
    {

        0: {'x': 10, 'y': 25, 'width': 50, 'height': 20, 'border_color': None, 'border_width': None, 'fill': None,
            'text': 'Period', 'text_color': None, 'text_rotation': None, 'font': None,
            'tags': ('TagTextBox_0', 'account'), 'font_size': 13},
        1: {'x': 0, 'y': 0, 'width': 200, 'height': 20, 'border_color': 'blue', 'border_width': 3, 'fill': None,
            'text': 'Revenue Name', 'text_color': None, 'text_rotation': None, 'font': None,
            'tags': ('TagTextBox_1', 'account'), 'font_size': 13},
        2: {'x': 110, 'y': 25, 'width': 90, 'height': 20, 'border_color': 'black', 'border_width': None, 'fill': None,
            'text': 'Volume', 'text_color': None, 'text_rotation': None, 'font': None,
            'tags': ('TagTextBox_2', 'account'), 'font_size': 13},
        3: {'x': 110, 'y': 50, 'width': 90, 'height': 20, 'border_color': 'blue', 'border_width': 3, 'fill': None,
            'text': 'Price', 'text_color': None, 'text_rotation': None, 'font': None,
            'tags': ('TagTextBox_3', 'account'), 'font_size': 13},
        4: {'x': 0, 'y': 75, 'width': 100, 'height': 20, 'border_color': 'black', 'border_width': None, 'fill': None,
            'text': 'Revenue', 'text_color': None, 'text_rotation': None, 'font': None,
            'tags': ('TagTextBox_4', 'account'), 'font_size': 13},
        5: {'x': 25, 'y': 37, 'width': 50, 'height': 20, 'border_color': 'black', 'border_width': None, 'fill': None,
            'text': 'x', 'text_color': None, 'text_rotation': None, 'font': None,
            'tags': ('TagTextBox_5', 'operator'), 'font_size': 13},
        6: {'x': 225, 'y': 0, 'width': 48, 'height': 20, 'border_color': None, 'border_width': None, 'fill': None,
            'text': 'Period', 'text_color': None, 'text_rotation': None, 'font': None,
            'tags': ('TagTextBox_6', 'relay'), 'font_size': 13, 'shape_it_represents': 0}},
    {},
    {},
    (1, 2, 3, 4, Blank()),
    {
        'Sheet1': account_orders[0],
        'Revenue': account_orders[1],
    },
    {
        'Sheet1': selections[0],
        'Revenue': selections[1],
    },
    {'selected': 'Revenue', '_sheet_data': {'Sheet1': {0}, 'Revenue': {1, 2, 3, 4, 5, 6}}},
    {'nop': 10, 'bb_shift': -1, 'default_increment': (0, 5), 'move_shape_increment': (25, 25),
     '_save_file_name': 'Excel', '_target_accounts_sensitivity': (), '_variable_accounts_sensitivity': (),
     '_sensitivity_deltas': {}, '_insert_sheet_name_in_input_sheet': False, '_prevent_refresh_canvas': False,
     'clean_up_state_before_pickling_though_expensive': True, 'live_calculation': True, 'account width': 50,
     'account height': 20, 'account font size': 13, 'operator width': 50, 'operator height': 20,
     'operator font size': 13, 'bb width': 50, 'bb height': 20, 'bb font size': 13, 'constant width': 50,
     'constant height': 20, 'constant font size': 13, 'all other font size': 13, '_auto_fit_width_per_letter': 8,
     '_slider_w': 25, '_slider_h': 200, '_slider_range_w': 40, '_slider_range_h': 20, '_slider_decimal_w': 40,
     '_slider_decimal_h': 20, '_slider_handle_h': 25, '_slider_range_dx': -60, '_graph_y_ax_w': 1,
     '_graph_y_ax_height': 200, '_graph_range_w': 40, '_graph_range_h': 20, '_graph_period_w': 40,
     '_graph_period_h': 20, '_graph_range_dx': -60, '_scale_x': 1, '_scale_y': 1, '_relay_x': '_relay_x_to_right',
     '_copied_accounts': ()},
    {
        0: {0: 0.0, 1: 1.0, 2: 2.0, 3: 3.0, 4: 4.0, 5: 5.0, 6: 6.0, 7: 7.0, 8: 8.0, 9: 9.0},
        1: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},
        2: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},
        3: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},
        4: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},
        5: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}},
    {0: (0.0, 10.0), 1: None, 2: None, 3: None, 4: None, 5: None},
    {
        '_key_connection_ids': {0: ('period',), 2: ('Tr_Volume_Sales',), 4: ('Tr_Revenue',)},
        '_key_partner_plugs': {1: ('period',)},
        '_key_partner_sockets': {4: ('to_IS_Total_Revenue',)}
    },
    {None: (0, 2, 3, 5), 'heading': (1,), 'total': (4,)},
    {'whole number': (0,), None: (1, 2, 3, 4, 5)},
    {},
    (),
    (),
    {0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1},
    {'fill': {}},
    {0: '', 2: 'kt', 3: '$/ton', 4: '$k'},
    {},
    set()
]

app = instantiate_app()
memento = Memento(state)
app.interactor.load_memento(memento)
app.interactor.export_excel('spreadsheet from JS.xlsx', "/Users/yamaka/Desktop/")
print("\nFile saved!")
