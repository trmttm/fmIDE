from typing import Iterable


def test_cases_add_new_shape(create_shape_kwargs: Iterable[dict] = None):
    from ..RequestModel import request_model_add_new_shape
    from ..Entities.Shape.implementation import create_shape_data
    import copy
    request_models = (
        request_model_add_new_shape('Account0'),
        request_model_add_new_shape('Account1'),
        request_model_add_new_shape('Account2'),
        request_model_add_new_shape('+'),
        request_model_add_new_shape('-'),
        request_model_add_new_shape('/'),
        request_model_add_new_shape('x'),
        request_model_add_new_shape('*'),
        request_model_add_new_shape('**'),
        request_model_add_new_shape('^'),
        request_model_add_new_shape('150'),
        request_model_add_new_shape('-10'),
        request_model_add_new_shape('-10.2'),
    )
    kw = create_shape_kwargs or tuple({} for _ in range(len(request_models)))
    shape_datas = (
        {0: create_shape_data(text='Account0', tags=('TagTextBox_0', 'account',), **kw[0])},
        {1: create_shape_data(text='Account1', tags=('TagTextBox_1', 'account',), **kw[1])},
        {2: create_shape_data(text='Account2', tags=('TagTextBox_2', 'account',), **kw[2])},
        {3: create_shape_data(text='+', tags=('TagTextBox_3', 'operator',), **kw[3])},
        {4: create_shape_data(text='-', tags=('TagTextBox_4', 'operator',), **kw[4])},
        {5: create_shape_data(text='/', tags=('TagTextBox_5', 'operator',), **kw[5])},
        {6: create_shape_data(text='x', tags=('TagTextBox_6', 'operator',), **kw[6])},
        {7: create_shape_data(text='*', tags=('TagTextBox_7', 'operator',), **kw[7])},
        {8: create_shape_data(text='**', tags=('TagTextBox_8', 'operator',), **kw[8])},
        {9: create_shape_data(text='^', tags=('TagTextBox_9', 'operator',), **kw[9])},
        {10: create_shape_data(text='150', tags=('TagTextBox_10', 'constant',), **kw[10])},
        {11: create_shape_data(text='-10', tags=('TagTextBox_11', 'constant',), **kw[11])},
        {12: create_shape_data(text='-10.2', tags=('TagTextBox_12', 'constant',), **kw[12])},)

    data = {}
    expected_shapes_datas = []
    for shape_data in shape_datas:
        data.update(shape_data)
        expected_shapes_datas.append(copy.deepcopy(data))

    return expected_shapes_datas, request_models


def test_cases_add_new_shape_interactor():
    adjusted_y = [25 * (n + 1) for n in range(33)]
    shape_kwargs = [
        {'x': 10, 'y': adjusted_y[0], 'height': 20, 'width': 50},
        {'x': 10, 'y': adjusted_y[1], 'height': 20, 'width': 50},
        {'x': 10, 'y': adjusted_y[2], 'height': 20, 'width': 50},
        {'x': 10, 'y': adjusted_y[3], 'height': 20, 'width': 50},
        {'x': 10, 'y': adjusted_y[4], 'height': 20, 'width': 50},
        {'x': 10, 'y': adjusted_y[5], 'height': 20, 'width': 50},
        {'x': 10, 'y': adjusted_y[6], 'height': 20, 'width': 50},
        {'x': 10, 'y': adjusted_y[7], 'height': 20, 'width': 50},
        {'x': 10, 'y': adjusted_y[8], 'height': 20, 'width': 50},
        {'x': 10, 'y': adjusted_y[9], 'height': 20, 'width': 50},
        {'x': 10, 'y': adjusted_y[10], 'height': 20, 'width': 50},
        {'x': 10, 'y': adjusted_y[11], 'height': 20, 'width': 50},
        {'x': 10, 'y': adjusted_y[12], 'height': 20, 'width': 50},
    ]
    expected_shapes_datas, request_models = test_cases_add_new_shape(shape_kwargs)
    nth_shape_data = [shape_data[n] for (n, shape_data) in enumerate(expected_shapes_datas)]
    return nth_shape_data, request_models


def test_cases_add_new_shape_expected_response_model(shapes_data):
    from ..ResponseModel import response_model_to_presenter_add_shape
    j = len(test_cases_add_new_shape()[1])
    expected_response_model = response_model_to_presenter_add_shape(shapes_data, range(j))
    return expected_response_model


def test_cases_add_selection():
    from ..RequestModel import request_model_add_to_selection
    request_models = (
        request_model_add_to_selection(0),
        request_model_add_to_selection(1),
        request_model_add_to_selection(2),
        request_model_add_to_selection(3),
        request_model_add_to_selection(4),
        request_model_add_to_selection(5),
        request_model_add_to_selection(6),
        request_model_add_to_selection(7),
        request_model_add_to_selection(8),
        request_model_add_to_selection(9),
        request_model_add_to_selection(10),
        request_model_add_to_selection(11),
        request_model_add_to_selection(12),
    )
    expected_selections = (
        {i for i in range(0 + 1)},
        {i for i in range(1 + 1)},
        {i for i in range(2 + 1)},
        {i for i in range(3 + 1)},
        {i for i in range(4 + 1)},
        {i for i in range(5 + 1)},
        {i for i in range(6 + 1)},
        {i for i in range(7 + 1)},
        {i for i in range(8 + 1)},
        {i for i in range(9 + 1)},
        {i for i in range(10 + 1)},
        {i for i in range(11 + 1)},
        {i for i in range(12 + 1)},
    )
    return expected_selections, request_models


def test_cases_add_selection_expected_response_model():
    from ..ResponseModel import response_model_to_presenter_highlight_auto
    from ..ResponseModel import audit_shape
    from ..Entities.Shape.implementation import create_canvas_tag_from_shape_id as c_tag
    audit_results = [
        audit_shape(0, True, 'account', c_tag(0), set(), False, False),
        audit_shape(1, True, 'account', c_tag(1), set(), False, False),
        audit_shape(2, True, 'account', c_tag(2), set(), False, False),
        audit_shape(3, True, 'operator', c_tag(3), set(), False, False),
        audit_shape(4, True, 'operator', c_tag(4), set(), False, False),
        audit_shape(5, True, 'operator', c_tag(5), set(), False, False),
        audit_shape(6, True, 'operator', c_tag(6), set(), False, False),
        audit_shape(7, True, 'operator', c_tag(7), set(), False, False),
        audit_shape(8, True, 'operator', c_tag(8), set(), False, False),
        audit_shape(9, True, 'operator', c_tag(9), set(), False, False),
        audit_shape(10, True, 'constant', c_tag(10), set(), False, False),
        audit_shape(11, True, 'constant', c_tag(11), set(), False, False),
        audit_shape(12, True, 'constant', c_tag(12), set(), False, False),
    ]

    d = {0: 'Sheet1',
         1: 'Sheet1',
         2: 'Sheet1',
         3: 'Sheet1',
         4: 'Sheet1',
         5: 'Sheet1',
         6: 'Sheet1',
         7: 'Sheet1',
         8: 'Sheet1',
         9: 'Sheet1',
         10: 'Sheet1',
         11: 'Sheet1',
         12: 'Sheet1'}

    expected_response_model = response_model_to_presenter_highlight_auto(audit_results)
    return expected_response_model


def test_cases_newly_select():
    from ..RequestModel import request_model_select_shape
    request_models = (
        request_model_select_shape(0),
        request_model_select_shape(1),
        request_model_select_shape(2),
        request_model_select_shape(3),
        request_model_select_shape(4),
        request_model_select_shape(5),
        request_model_select_shape(6),
        request_model_select_shape(7),
        request_model_select_shape(8),
        request_model_select_shape(9),
        request_model_select_shape(10),
        request_model_select_shape(11),
        request_model_select_shape(12),
    )
    expected_selections = (
        {0},
        {1},
        {2},
        {3},
        {4},
        {5},
        {6},
        {7},
        {8},
        {9},
        {10},
        {11},
        {12},
    )
    return expected_selections, request_models


def test_cases_newly_select_response_model():
    from ..ResponseModel import response_model_to_presenter_highlight_auto
    from ..ResponseModel import audit_shape
    from ..Entities.Shape.implementation import create_canvas_tag_from_shape_id as c_tag
    audit_results = [
        audit_shape(0, False, 'account', c_tag(0), set(), False, False),
        audit_shape(1, False, 'account', c_tag(1), set(), False, False),
        audit_shape(2, False, 'account', c_tag(2), set(), False, False),
        audit_shape(3, False, 'operator', c_tag(3), set(), False, False),
        audit_shape(4, False, 'operator', c_tag(4), set(), False, False),
        audit_shape(5, False, 'operator', c_tag(5), set(), False, False),
        audit_shape(6, False, 'operator', c_tag(6), set(), False, False),
        audit_shape(7, False, 'operator', c_tag(7), set(), False, False),
        audit_shape(8, False, 'operator', c_tag(8), set(), False, False),
        audit_shape(9, False, 'operator', c_tag(9), set(), False, False),
        audit_shape(10, False, 'constant', c_tag(10), set(), False, False),
        audit_shape(11, False, 'constant', c_tag(11), set(), False, False),
        audit_shape(12, True, 'constant', c_tag(12), set(), False, False),
    ]

    d = {0: 'Sheet1',
         1: 'Sheet1',
         2: 'Sheet1',
         3: 'Sheet1',
         4: 'Sheet1',
         5: 'Sheet1',
         6: 'Sheet1',
         7: 'Sheet1',
         8: 'Sheet1',
         9: 'Sheet1',
         10: 'Sheet1',
         11: 'Sheet1',
         12: 'Sheet1'}

    expected_response_model = response_model_to_presenter_highlight_auto(audit_results)
    return expected_response_model


def test_cases_unselect(shapes_to_unselect: Iterable):
    from ..RequestModel import request_model_select_shape
    request_models = tuple(request_model_select_shape(i) for i in shapes_to_unselect)

    selections = []
    negative_list = set()
    for shape in shapes_to_unselect:
        negative_list.add(shape)
        selection = set(n for n in range(13) if n not in negative_list)
        selections.append(selection)
    expected_selections = tuple(selections)
    return expected_selections, request_models


def test_cases_unselect_response_model(shapes_to_unselect: Iterable):
    from ..ResponseModel import response_model_to_presenter_highlight_auto
    from ..ResponseModel import audit_shape
    from ..Entities.Shape.implementation import create_canvas_tag_from_shape_id as c_tag
    audit_results = [
        audit_shape(0, 0 not in shapes_to_unselect, 'account', c_tag(0), set(), False, False),
        audit_shape(1, 1 not in shapes_to_unselect, 'account', c_tag(1), set(), False, False),
        audit_shape(2, 2 not in shapes_to_unselect, 'account', c_tag(2), set(), False, False),
        audit_shape(3, 3 not in shapes_to_unselect, 'operator', c_tag(3), set(), False, False),
        audit_shape(4, 4 not in shapes_to_unselect, 'operator', c_tag(4), set(), False, False),
        audit_shape(5, 5 not in shapes_to_unselect, 'operator', c_tag(5), set(), False, False),
        audit_shape(6, 6 not in shapes_to_unselect, 'operator', c_tag(6), set(), False, False),
        audit_shape(7, 7 not in shapes_to_unselect, 'operator', c_tag(7), set(), False, False),
        audit_shape(8, 8 not in shapes_to_unselect, 'operator', c_tag(8), set(), False, False),
        audit_shape(9, 9 not in shapes_to_unselect, 'operator', c_tag(9), set(), False, False),
        audit_shape(10, 10 not in shapes_to_unselect, 'constant', c_tag(10), set(), False, False),
        audit_shape(11, 11 not in shapes_to_unselect, 'constant', c_tag(11), set(), False, False),
        audit_shape(12, 12 not in shapes_to_unselect, 'constant', c_tag(12), set(), False, False),
    ]

    d = {0: 'Sheet1',
         1: 'Sheet1',
         2: 'Sheet1',
         3: 'Sheet1',
         4: 'Sheet1',
         5: 'Sheet1',
         6: 'Sheet1',
         7: 'Sheet1',
         8: 'Sheet1',
         9: 'Sheet1',
         10: 'Sheet1',
         11: 'Sheet1',
         12: 'Sheet1'}

    expected_response_model = response_model_to_presenter_highlight_auto(audit_results)
    return expected_response_model


def test_cases_erase_shapes(shapes_to_delete):
    from ..RequestModel import request_model_erase_shape

    request_models = tuple(request_model_erase_shape(shape_id) for shape_id in shapes_to_delete)
    expected_remaining_selections = tuple(
        tuple([i for i in range(13) if i not in shapes_to_delete[0:n + 1]]) for n in range(len(shapes_to_delete))
    )
    return expected_remaining_selections, request_models


def test_cases_erase_shapes_expected_response_model(shapes, shape_ids_to_delete):
    expected_response_model = tuple(shapes.get_canvas_tag_from_shape_id(i) for i in shape_ids_to_delete)
    return expected_response_model


def test_cases_draw_rectangle():
    from ..RequestModel import request_model_draw_rectangle
    request_models = (
        request_model_draw_rectangle((10, 10), (15, 15), 1, 'black'),
        request_model_draw_rectangle((20, 20), (25, 25), 2, 'red'),
    )
    expected_rectangle_data = (
        {0: {'coordinate_from': (10, 10),
             'coordinate_to': (15, 15),
             'line_color': 'black',
             'line_width': 1}},
        {0: {'coordinate_from': (10, 10),
             'coordinate_to': (15, 15),
             'line_color': 'black',
             'line_width': 1},
         1: {'coordinate_from': (20, 20),
             'coordinate_to': (25, 25),
             'line_color': 'red',
             'line_width': 2}
         },

    )
    return expected_rectangle_data, request_models


def test_cases_draw_rectangle_response_model(rectangle_selector_data):
    from ..ResponseModel import response_model_to_presenter_draw_rectangle
    expected_response_model = response_model_to_presenter_draw_rectangle(rectangle_selector_data)
    return expected_response_model


def test_cases_erase_rectangle(by_interactor=False):
    from ..RequestModel import request_model_erase_rectangle
    request_models = (
        request_model_erase_rectangle(0),
        request_model_erase_rectangle(1),
    )
    data = {1: {'coordinate_from': (20, 20),
                'coordinate_to': (25, 25),
                'line_color': 'red',
                'line_width': 2, }, }
    if by_interactor:
        data[1].update({'tags': ('rectangle_selector',)})
    expected_rectangle_data = (
        data,
        {},

    )
    return expected_rectangle_data, request_models


def test_cases_add_connection():
    from ..RequestModel import request_model_add_connection
    request_models = (
        request_model_add_connection(0, 1),
        request_model_add_connection(1, 2),
        request_model_add_connection(2, 3),
        request_model_add_connection(3, 0),
    )
    expected_connections_data = (
        {(0, 1)},
        {(0, 1), (1, 2)},
        {(0, 1), (1, 2), (2, 3)},
        {(0, 1), (1, 2), (2, 3), (3, 0)},
    )
    return expected_connections_data, request_models


def test_cases_add_connection_interactor():
    # interactor filters out invalid connections
    from ..RequestModel import request_model_add_connection
    request_models = (
        request_model_add_connection(0, 1),
        request_model_add_connection(1, 2),
        request_model_add_connection(2, 3),
        request_model_add_connection(3, 0),
    )
    expected_connections_data = (
        {(0, 1)},
        {(0, 1), (1, 2)},
        {(0, 1), (1, 2), (2, 3)},
        {(0, 1), (1, 2), (2, 3), (3, 0)},
    )
    return expected_connections_data, request_models


def test_cases_change_connection_response_model(connections_data, get_coords_from_shape_id):
    from ..ResponseModel import response_model_to_presenter_connect
    expected_response_model = response_model_to_presenter_connect(connections_data, get_coords_from_shape_id)
    return expected_response_model


def test_cases_remove_connection():
    from ..RequestModel import request_model_remove_connection
    request_models = (
        request_model_remove_connection(0, 1),
        request_model_remove_connection(1, 2),
        request_model_remove_connection(2, 3),
        request_model_remove_connection(3, 0),
    )
    expected_rectangle_data = (
        {(1, 2), (2, 3), (3, 0)},
        {(2, 3), (3, 0)},
        {(3, 0)},
        set(),
    )
    return expected_rectangle_data, request_models


def test_cases_remove_connection_of_a_shape():
    from ..RequestModel import request_model_remove_connection_of_a_shape
    request_models = (
        request_model_remove_connection_of_a_shape(1),
        request_model_remove_connection_of_a_shape(0),
    )
    expected_rectangle_data = (
        {(2, 3), (3, 0)},
        {(2, 3)},
    )
    return expected_rectangle_data, request_models


def test_cases_draw_lines():
    from ..RequestModel import request_model_draw_line
    from ..Entities.Line import constants as cns
    request_models = (
        request_model_draw_line((0, 0), (0, 0), 0, 'white'),
        request_model_draw_line((1, 1), (10, 10), 1, 'black'),
        request_model_draw_line((2, 2), (20, 20), 2, 'red'),
        request_model_draw_line((3, 3), (30, 30), 3, 'blue'),
        request_model_draw_line((4, 4), (40, 40), 4, 'yellow'),
        request_model_draw_line((5, 5), (50, 50), 5, 'purple'),
    )
    expected_line_data = (
        {
            0: {
                cns.coordinate_from: (0, 0),
                cns.coordinate_to: (0, 0),
                cns.line_width: 0,
                cns.line_color: 'white',
            },
        },
        {
            0: {
                cns.coordinate_from: (0, 0),
                cns.coordinate_to: (0, 0),
                cns.line_width: 0,
                cns.line_color: 'white',
            },
            1: {
                cns.coordinate_from: (1, 1),
                cns.coordinate_to: (10, 10),
                cns.line_width: 1,
                cns.line_color: 'black',
            },
        },
        {
            0: {
                cns.coordinate_from: (0, 0),
                cns.coordinate_to: (0, 0),
                cns.line_width: 0,
                cns.line_color: 'white',
            },
            1: {
                cns.coordinate_from: (1, 1),
                cns.coordinate_to: (10, 10),
                cns.line_width: 1,
                cns.line_color: 'black',
            },
            2: {
                cns.coordinate_from: (2, 2),
                cns.coordinate_to: (20, 20),
                cns.line_width: 2,
                cns.line_color: 'red',
            },
        },
        {
            0: {
                cns.coordinate_from: (0, 0),
                cns.coordinate_to: (0, 0),
                cns.line_width: 0,
                cns.line_color: 'white',
            },
            1: {
                cns.coordinate_from: (1, 1),
                cns.coordinate_to: (10, 10),
                cns.line_width: 1,
                cns.line_color: 'black',
            },
            2: {
                cns.coordinate_from: (2, 2),
                cns.coordinate_to: (20, 20),
                cns.line_width: 2,
                cns.line_color: 'red',
            },
            3: {
                cns.coordinate_from: (3, 3),
                cns.coordinate_to: (30, 30),
                cns.line_width: 3,
                cns.line_color: 'blue',
            },
        },
        {
            0: {
                cns.coordinate_from: (0, 0),
                cns.coordinate_to: (0, 0),
                cns.line_width: 0,
                cns.line_color: 'white',
            },
            1: {
                cns.coordinate_from: (1, 1),
                cns.coordinate_to: (10, 10),
                cns.line_width: 1,
                cns.line_color: 'black',
            },
            2: {
                cns.coordinate_from: (2, 2),
                cns.coordinate_to: (20, 20),
                cns.line_width: 2,
                cns.line_color: 'red',
            },
            3: {
                cns.coordinate_from: (3, 3),
                cns.coordinate_to: (30, 30),
                cns.line_width: 3,
                cns.line_color: 'blue',
            },
            4: {
                cns.coordinate_from: (4, 4),
                cns.coordinate_to: (40, 40),
                cns.line_width: 4,
                cns.line_color: 'yellow',
            },
        },
        {
            0: {
                cns.coordinate_from: (0, 0),
                cns.coordinate_to: (0, 0),
                cns.line_width: 0,
                cns.line_color: 'white',
            },
            1: {
                cns.coordinate_from: (1, 1),
                cns.coordinate_to: (10, 10),
                cns.line_width: 1,
                cns.line_color: 'black',
            },
            2: {
                cns.coordinate_from: (2, 2),
                cns.coordinate_to: (20, 20),
                cns.line_width: 2,
                cns.line_color: 'red',
            },
            3: {
                cns.coordinate_from: (3, 3),
                cns.coordinate_to: (30, 30),
                cns.line_width: 3,
                cns.line_color: 'blue',
            },
            4: {
                cns.coordinate_from: (4, 4),
                cns.coordinate_to: (40, 40),
                cns.line_width: 4,
                cns.line_color: 'yellow',
            },
            5: {
                cns.coordinate_from: (5, 5),
                cns.coordinate_to: (50, 50),
                cns.line_width: 5,
                cns.line_color: 'purple',
            },
        },
    )
    return expected_line_data, request_models


def test_cases_draw_lines_response_model(lines_data):
    from ..ResponseModel import response_model_to_presenter_draw_line
    expected_response_model = response_model_to_presenter_draw_line(lines_data)
    return expected_response_model


def test_cases_erase_lines():
    from ..RequestModel import request_model_erase_line
    from ..Entities.Line import constants as cns
    request_models = (
        request_model_erase_line(5),
        request_model_erase_line(4),
        request_model_erase_line(3),
        request_model_erase_line(2),
        request_model_erase_line(1),
        request_model_erase_line(0),
    )
    expected_line_data = (
        {
            0: {
                cns.coordinate_from: (0, 0),
                cns.coordinate_to: (0, 0),
                cns.line_width: 0,
                cns.line_color: 'white',
            },
            1: {
                cns.coordinate_from: (1, 1),
                cns.coordinate_to: (10, 10),
                cns.line_width: 1,
                cns.line_color: 'black',
            },
            2: {
                cns.coordinate_from: (2, 2),
                cns.coordinate_to: (20, 20),
                cns.line_width: 2,
                cns.line_color: 'red',
            },
            3: {
                cns.coordinate_from: (3, 3),
                cns.coordinate_to: (30, 30),
                cns.line_width: 3,
                cns.line_color: 'blue',
            },
            4: {
                cns.coordinate_from: (4, 4),
                cns.coordinate_to: (40, 40),
                cns.line_width: 4,
                cns.line_color: 'yellow',
            },
            5: {
                cns.coordinate_from: (5, 5),
                cns.coordinate_to: (50, 50),
                cns.line_width: 5,
                cns.line_color: 'purple',
            },
        },
        {
            0: {
                cns.coordinate_from: (0, 0),
                cns.coordinate_to: (0, 0),
                cns.line_width: 0,
                cns.line_color: 'white',
            },
            1: {
                cns.coordinate_from: (1, 1),
                cns.coordinate_to: (10, 10),
                cns.line_width: 1,
                cns.line_color: 'black',
            },
            2: {
                cns.coordinate_from: (2, 2),
                cns.coordinate_to: (20, 20),
                cns.line_width: 2,
                cns.line_color: 'red',
            },
            3: {
                cns.coordinate_from: (3, 3),
                cns.coordinate_to: (30, 30),
                cns.line_width: 3,
                cns.line_color: 'blue',
            },
            4: {
                cns.coordinate_from: (4, 4),
                cns.coordinate_to: (40, 40),
                cns.line_width: 4,
                cns.line_color: 'yellow',
            },
        },
        {
            0: {
                cns.coordinate_from: (0, 0),
                cns.coordinate_to: (0, 0),
                cns.line_width: 0,
                cns.line_color: 'white',
            },
            1: {
                cns.coordinate_from: (1, 1),
                cns.coordinate_to: (10, 10),
                cns.line_width: 1,
                cns.line_color: 'black',
            },
            2: {
                cns.coordinate_from: (2, 2),
                cns.coordinate_to: (20, 20),
                cns.line_width: 2,
                cns.line_color: 'red',
            },
            3: {
                cns.coordinate_from: (3, 3),
                cns.coordinate_to: (30, 30),
                cns.line_width: 3,
                cns.line_color: 'blue',
            },
        },
        {
            0: {
                cns.coordinate_from: (0, 0),
                cns.coordinate_to: (0, 0),
                cns.line_width: 0,
                cns.line_color: 'white',
            },
            1: {
                cns.coordinate_from: (1, 1),
                cns.coordinate_to: (10, 10),
                cns.line_width: 1,
                cns.line_color: 'black',
            },
            2: {
                cns.coordinate_from: (2, 2),
                cns.coordinate_to: (20, 20),
                cns.line_width: 2,
                cns.line_color: 'red',
            },
        },

        {
            0: {
                cns.coordinate_from: (0, 0),
                cns.coordinate_to: (0, 0),
                cns.line_width: 0,
                cns.line_color: 'white',
            },
            1: {
                cns.coordinate_from: (1, 1),
                cns.coordinate_to: (10, 10),
                cns.line_width: 1,
                cns.line_color: 'black',
            },
        },

        {
            0: {
                cns.coordinate_from: (0, 0),
                cns.coordinate_to: (0, 0),
                cns.line_width: 0,
                cns.line_color: 'white',
            },
        },
        {},
    )
    return expected_line_data, request_models


def test_case_shape_id_at_xy():
    coordinates = (
        (10, 25),  # TL
        (60, 25),  # TR
        (10, 45),  # BL
        (60, 45),  # BR
        (10, 24),
        (60, 24),
        (10, 46),
        (60, 46),
        (61, 25),
        (61, 45),
    )
    expected_shape_ids = (
        0,
        0,
        0,
        0,
        None,
        None,
        None,
        None,
        None,
        None,
    )
    return expected_shape_ids, coordinates


def test_cases_presenter_add_shape():
    response_models = [
        {
            0: {
                'x': 10,
                'y': 15,
                'width': 50,
                'height': 10,
                'border_color': 'black',
                'border_width': 2,
                'fill': 'light blue',
                'text': 'Test01',
                'text_rotation': 0,
                'font': None,
                'tags': ('account', 'Tag2'),
            },
            1: {
                'x': 10,
                'y': 15,
                'width': 50,
                'height': 10,
                'border_color': 'black',
                'border_width': 2,
                'fill': 'light blue',
                'text': 'Test01',
                'text_rotation': 0,
                'font': None,
                'tags': ('account', 'Tag2'),
            },
        },
        {
            0: {
                'x': 15,
                'y': 15,
                'width': 50,
                'height': 15,
                'border_color': 'black',
                'border_width': 2,
                'fill': 'light blue',
                'text': 'Test01',
                'text_rotation': 0,
                'font': None,
                'tags': ('account', 'Tag2'),
            },
            1: {
                'x': 15,
                'y': 15,
                'width': 50,
                'height': 10,
                'border_color': 'black',
                'border_width': 2,
                'fill': 'light blue',
                'text': 'Test01',
                'text_rotation': 0,
                'font': None,
                'tags': ('account', 'Tag2'),
            },
        },
    ]
    expected_view_models = [
        [
            {
                'x': 10,
                'y': 15,
                'width': 50,
                'height': 10,
                'border_color': 'black',
                'border_width': 2,
                'fill': 'light blue',
                'text': 'Test01',
                'text_rotation': 0,
                'font': None,
                'tags': ('account', 'Tag2'),
            },
            {
                'x': 10,
                'y': 15,
                'width': 50,
                'height': 10,
                'border_color': 'black',
                'border_width': 2,
                'fill': 'light blue',
                'text': 'Test01',
                'text_rotation': 0,
                'font': None,
                'tags': ('account', 'Tag2'),
            },
        ],
        [
            {
                'x': 15,
                'y': 15,
                'width': 50,
                'height': 15,
                'border_color': 'black',
                'border_width': 2,
                'fill': 'light blue',
                'text': 'Test01',
                'text_rotation': 0,
                'font': None,
                'tags': ('account', 'Tag2'),
            },
            {
                'x': 15,
                'y': 15,
                'width': 50,
                'height': 10,
                'border_color': 'black',
                'border_width': 2,
                'fill': 'light blue',
                'text': 'Test01',
                'text_rotation': 0,
                'font': None,
                'tags': ('account', 'Tag2'),
            },
        ],
    ]
    return expected_view_models, response_models


def test_cases_presenter_clear_canvas():
    response_models = (
        'No matter',
        'what response_models are',
        'view_models',
        'are',
        'None',

    )
    expected_view_models = tuple(None for _ in range(len(response_models)))
    return expected_view_models, response_models


def test_cases_presenter_connect_shape():
    response_models = (
        [{'coordinates': ((1, 2), (3, 4)), 'selected': False}],
        [{'coordinates': ((10, 20), (30, 40)), 'selected': True}],
    )
    expected_view_models = (
        [{'color': 'black', 'coordinates': ((1, 2), (3, 4))}],
        [{'color': 'red', 'coordinates': ((10, 20), (30, 40))}],
    )
    return expected_view_models, response_models


def test_cases_presenter_draw_line():
    response_models = (
        {
            0: {
                'coordinate_from': (0, 0),
                'coordinate_to': (1, 1),
                'line_width': 1,
                'line_color': 'black', },
            1: {
                'coordinate_from': (2, 2),
                'coordinate_to': (3, 3),
                'line_width': 4,
                'line_color': 'red',
            },
        }
    )
    expected_view_models = response_models
    return expected_view_models, response_models


def test_cases_presenter_draw_rectangle():
    response_models = (
        'view_model = response_model',
    )
    expected_view_models = (
        'view_model = response_model',
    )
    return expected_view_models, response_models


def test_cases_presenter_highlight_shape_auto():
    shape_id_to_sheet_name1 = dict(zip(range(8), tuple('Sheet1' for _ in range(8))))
    response_models = (
        {'method': 0, 'highlight_datas': [
            {
                'shape_id': 0,
                'tag_type': 'account',
                'canvas_tag': 'TagTextBox_0',
                'selected': False,
                'key_is_input_account': True,
                'key_is_depended_by_external_sheet': False,
                'key_depending_on_external_sheet': False,
            },
            {
                'shape_id': 1,
                'tag_type': 'operator',
                'canvas_tag': 'TagTextBox_1',
                'selected': False,
                'key_is_input_account': False,
                'key_is_depended_by_external_sheet': False,
                'key_depending_on_external_sheet': False,
            },
            {
                'shape_id': 2,
                'tag_type': 'constant',
                'canvas_tag': 'TagTextBox_2',
                'selected': False,
                'key_is_input_account': False,
                'key_is_depended_by_external_sheet': False,
                'key_depending_on_external_sheet': False,
            },
            {
                'shape_id': 3,
                'tag_type': 'core_account',
                'canvas_tag': 'TagTextBox_3',
                'selected': False,
                'key_is_input_account': False,
                'key_is_depended_by_external_sheet': False,
                'key_depending_on_external_sheet': False,
            },
            {
                'shape_id': 4,
                'tag_type': 'account',
                'canvas_tag': 'TagTextBox_4',
                'selected': True,
                'key_is_input_account': False,
                'key_is_depended_by_external_sheet': False,
                'key_depending_on_external_sheet': False,
            },
            {
                'shape_id': 5,
                'tag_type': 'operator',
                'canvas_tag': 'TagTextBox_5',
                'selected': True,
                'key_is_input_account': False,
                'key_is_depended_by_external_sheet': True,
                'key_depending_on_external_sheet': False,
            },
            {
                'shape_id': 6,
                'tag_type': 'constant',
                'canvas_tag': 'TagTextBox_6',
                'selected': True,
                'key_is_input_account': False,
                'key_is_depended_by_external_sheet': False,
                'key_depending_on_external_sheet': True,
            },
            {
                'shape_id': 7,
                'tag_type': 'core_account',
                'canvas_tag': 'TagTextBox_7',
                'selected': True,
                'key_is_input_account': False,
                'key_is_depended_by_external_sheet': True,
                'key_depending_on_external_sheet': True,
            },
        ], 'key_shape_id_to_sheet_name': shape_id_to_sheet_name1, },
    )
    expected_view_models = (
        {'TagTextBox_0': {'border_color': 'black',
                          'border_width': 1,
                          'fill': 'light blue',
                          'shape_id': 0,
                          'text_color': 'black'},
         'TagTextBox_1': {'border_color': 'black',
                          'border_width': 1,
                          'fill': 'pink',
                          'shape_id': 1,
                          'text_color': 'black'},
         'TagTextBox_2': {'border_color': 'black',
                          'border_width': 1,
                          'fill': 'light green',
                          'shape_id': 2,
                          'text_color': 'black'},
         'TagTextBox_3': {'border_color': 'black',
                          'border_width': 1,
                          'fill': 'light grey',
                          'shape_id': 3,
                          'text_color': 'black'},
         'TagTextBox_4': {'border_color': 'black',
                          'border_width': 3,
                          'fill': 'white',
                          'shape_id': 4,
                          'text_color': 'black'},
         'TagTextBox_5': {'border_color': 'black',
                          'border_width': 3,
                          'fill': 'light grey',
                          'shape_id': 5,
                          'text_color': 'black'},
         'TagTextBox_6': {'border_color': 'red',
                          'border_width': 3,
                          'fill': 'light green',
                          'shape_id': 6,
                          'text_color': 'black'},
         'TagTextBox_7': {'border_color': 'red',
                          'border_width': 3,
                          'fill': 'light grey',
                          'shape_id': 7,
                          'text_color': 'black'}},
    )
    return expected_view_models, response_models


def test_cases_presenter_move_shape():
    response_models = (
        {'TagTextBox_0': (5, 5),
         'TagTextBox_1': (5, 5),
         'TagTextBox_2': (5, 5),
         'TagTextBox_3': (5, 5),
         'TagTextBox_4': (5, 5), },

    )
    expected_view_models = response_models
    return expected_view_models, response_models


def test_cases_presenter_remove_shape():
    response_models = [
        {
            0: {
                'x': 10,
                'y': 15,
                'width': 50,
                'height': 10,
                'border_color': 'black',
                'border_width': 2,
                'fill': 'light blue',
                'text': 'Test01',
                'text_rotation': 0,
                'font': None,
                'tags': ('account', 'Tag2'),
            },
            1: {
                'x': 10,
                'y': 15,
                'width': 50,
                'height': 10,
                'border_color': 'black',
                'border_width': 2,
                'fill': 'light blue',
                'text': 'Test01',
                'text_rotation': 0,
                'font': None,
                'tags': ('account', 'Tag2'),
            },
        },
        {
            2: {
                'x': 15,
                'y': 15,
                'width': 50,
                'height': 15,
                'border_color': 'black',
                'border_width': 2,
                'fill': 'light blue',
                'text': 'Test01',
                'text_rotation': 0,
                'font': None,
                'tags': ('account', 'Tag2'),
            },
            3: {
                'x': 15,
                'y': 15,
                'width': 50,
                'height': 10,
                'border_color': 'black',
                'border_width': 2,
                'fill': 'light blue',
                'text': 'Test01',
                'text_rotation': 0,
                'font': None,
                'tags': ('account', 'Tag2'),
            },
        },
    ]
    expected_view_models = response_models
    return expected_view_models, response_models


def test_cases_presenter_update_status_bar():
    response_models = (
        {'text': 'Message01', },
        {'text': 'Message02', },
        {'text': 'Message03', 'feedback_type': 'error'},
        {'text': 'Message04', 'feedback_type': 'success'},
        {'text': 'Message05', },
    )
    expected_view_models = (
        {'text': 'Message01', 'text_color': 'black', 'update': False},
        {'text': 'Message02', 'text_color': 'black', 'update': False},
        {'text': 'Message03', 'text_color': 'red', 'update': False},
        {'text': 'Message04', 'text_color': 'green', 'update': False},
        {'text': 'Message05', 'text_color': 'black', 'update': False},
    )
    return expected_view_models, response_models


def test_cases_presenter_load_pickle_files_list():
    response_models = (
        {'file_names': [f'{n}' for n in range(0)]},
        {'file_names': [f'{n}' for n in range(1)]},
        {'file_names': [f'{n}' for n in range(2)]},
        {'file_names': [f'{n}' for n in range(3)]},
        {'file_names': [f'{n}' for n in range(4)]},
    )
    values0 = []
    values1 = [
        {'parent': '',
         'index': '0',
         'select_this_item': False,
         'text': '',
         'values': (0, '0'),
         'tags': (), },
    ]
    values2 = [
        {'index': '0',
         'select_this_item': False,
         'parent': '',
         'tags': (),
         'text': '',
         'values': (0, '0')},
        {'index': '1',
         'select_this_item': False,
         'parent': '',
         'tags': (),
         'text': '',
         'values': (1, '1')}
    ]
    values3 = [
        {'index': '0',
         'select_this_item': False,
         'parent': '',
         'tags': (),
         'text': '',
         'values': (0, '0')},
        {'index': '1',
         'select_this_item': False,
         'parent': '',
         'tags': (),
         'text': '',
         'values': (1, '1')},
        {'index': '2',
         'select_this_item': False,
         'parent': '',
         'tags': (),
         'text': '',
         'values': (2, '2')}
    ]
    values4 = [
        {'parent': '',
         'index': '0',
         'select_this_item': False,
         'text': '',
         'values': (0, '0'),
         'tags': (),
         },
        {'parent': '',
         'index': '1',
         'select_this_item': False,
         'text': '',
         'values': (1, '1'),
         'tags': (),
         },
        {'parent': '',
         'index': '2',
         'select_this_item': False,
         'text': '',
         'values': (2, '2'),
         'tags': (),
         },
        {'parent': '',
         'index': '3',
         'select_this_item': False,
         'text': '',
         'values': (3, '3'),
         'tags': (), },

    ]
    v = (50, 200), False, False
    expected_view_models = (
        {'tree_datas': values0, 'headings': ('No', 'Name'), 'widths': v[0], 'stretches': (False, True),
         'scroll_h': v[1], 'scroll_v': v[2], },
        {'tree_datas': values1, 'headings': ('No', 'Name'), 'widths': v[0], 'stretches': (False, True),
         'scroll_h': v[1], 'scroll_v': v[2], },
        {'tree_datas': values2, 'headings': ('No', 'Name'), 'widths': v[0], 'stretches': (False, True),
         'scroll_h': v[1], 'scroll_v': v[2], },
        {'tree_datas': values3, 'headings': ('No', 'Name'), 'widths': v[0], 'stretches': (False, True),
         'scroll_h': v[1], 'scroll_v': v[2], },
        {'tree_datas': values4, 'headings': ('No', 'Name'), 'widths': v[0], 'stretches': (False, True),
         'scroll_h': v[1], 'scroll_v': v[2], },
    )
    return expected_view_models, response_models


def test_cases_get_shapes_by_tag_types():
    tag_types = ('account', 'operator', 'constant')
    expectations = ((0, 1, 2), (3, 4, 5, 6, 7, 8, 9), (10, 11, 12))
    return expectations, tag_types
