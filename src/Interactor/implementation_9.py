import typing as tp

from .. import Entities as Et
from .. import RequestModel
from .. import Utilities
from ..EntityGateway import GateWayABC
from ..Utilities.Graphs.graph_theory_dfs import Graph

cns_x = 'x'
cns_y = 'y'
cns_coordinates = 'coordinates'
cns_method = 'method'
cns_button = 'button'
cns_gesture = 'gesture'

temporary_save_state_name = 'temporary'


def create_save_name(notification: dict, request: dict) -> str:
    if request is not None:
        print_str = f'Mouse button:{request[cns_button]} {request[cns_gesture]}'
    elif notification is None:
        print_str = 'None'
    else:
        print_str = notification[cns_method]
    return print_str


def unselect_shape_at_x_y(request, selection: Et.Selection, shapes: Et.Shapes, search_from: tuple = None):
    x, y = request[cns_x], request[cns_y]
    shape_id_under_mouse = shapes.get_shape_id_at_the_coordinate(x, y, search_from)
    if shape_id_under_mouse is not None:
        selection.unselect_shape(shape_id_under_mouse)


def get_shape_ids_within_rectangle(request, shapes, search_from: tuple = None) -> tuple:
    coordinates = get_rectangle_coordinates_from_request(request)
    shape_ids = shapes.get_shape_ids_in_a_range(coordinates, search_from)
    return tuple(shape_ids)


def get_rectangle_coordinates_from_request(request) -> tp.Tuple[float, float, float, float]:
    (x1, y1), (x2, y2) = request[cns_coordinates]
    coordinates = x1, y1, x2, y2
    return coordinates


def add_new_shapes_per_request_models(request_models, shapes: Et.Shapes):
    shapes.add_new_shapes(request_models)


def interactor_is_responsible_for_setting_default_sizes_and_positions(new_shape_ids, shapes: Et.Shapes,
                                                                      whs: tuple = None):
    for shape_id, (w, h) in zip(new_shape_ids, whs):
        x_current = shapes.get_x(shape_id)
        y_current = shapes.get_y(shape_id)
        width_current = shapes.get_width(shape_id)
        height_current = shapes.get_height(shape_id)

        x = 10 if x_current is None else x_current
        y = 0 if y_current is None else y_current
        width = w if width_current is None else width_current
        height = h if height_current is None else height_current

        shapes.set_x(shape_id, x)
        shapes.set_y(shape_id, y)
        shapes.set_width(shape_id, width)
        shapes.set_height(shape_id, height)


def prevent_shape_overlaps(increment_x_y, new_shape_ids, shapes: Et.Shapes, search_from: tuple = None):
    for shape_id in new_shape_ids:
        search_from = search_from if (search_from is not None) else ()

        x = shapes.get_x(shape_id)
        y = shapes.get_y(shape_id)
        width = shapes.get_width(shape_id)
        height = shapes.get_height(shape_id)

        data = {'x': x, 'y': y, 'width': width, 'height': height}
        shapes.adjust_shape_position_to_avoid_overlapping(data, increment_x_y, search_from)

        shapes.set_x(shape_id, data['x'])
        shapes.set_y(shape_id, data['y'])
        shapes.set_width(shape_id, data['width'])
        shapes.set_height(shape_id, data['height'])


def validate_connection(id_from, id_to, connections: Et.Connections, shapes: Et.Shapes) -> str:
    more_than_one_sources = len(connections.get_connections_into(id_to)) > 0
    accounts = shapes.get_shapes('account')
    args = shapes.get_shapes('args')
    kwargs = shapes.get_shapes('kwargs')
    core_accounts = shapes.get_shapes('core_account')
    bb = shapes.get_shapes('bb')
    constants = shapes.get_shapes('constant')
    operators = shapes.get_shapes('operator')
    relays = shapes.get_shapes('relay')
    a_and_relay = accounts + relays
    only_accepts_one_arrow = accounts + args + kwargs + relays + bb

    shape_not_selected = id_from is None
    line_not_pointing_to_anything = id_to is None
    you_cannot_connect_to_yourself = id_to == id_from
    can_accept_only_one_arrow = more_than_one_sources and (id_to in only_accepts_one_arrow)
    core_account_only_accepts_account = (id_to in core_accounts) and (id_from not in a_and_relay)
    only_accepts_account = (id_to in relays + bb) and (id_from not in a_and_relay)
    two_cannot_point_at_each_other = id_from in connections.get_connections_out_of(id_to)
    constant_accepts_nothing = id_to in constants
    constant_must_point_to_op = (id_from in constants) and (id_to in (accounts + core_accounts))
    args_and_kwargs_reject_operators = (id_to in (args + kwargs)) and (id_from in operators)
    the_connection_already_exists = (id_from, id_to) in connections.data
    bb_only_points_to_accounts = (id_from in bb) and (id_to not in accounts)

    if line_not_pointing_to_anything:
        validation = 'Line not pointing to anything.'
    elif shape_not_selected:
        validation = 'Connection source not selected.'
    elif you_cannot_connect_to_yourself:
        validation = 'Cannot connect to itself.'
    elif can_accept_only_one_arrow:
        validation = 'Account, Args, Kwargs and Relay can have only one arrow pointing to itself.'
    elif core_account_only_accepts_account:
        validation = 'Only Account and Relay can point to core accounts.'
    elif only_accepts_account:
        validation = 'Only Account and Relay can point to Intermediaries.'
    elif two_cannot_point_at_each_other:
        validation = 'Two things cannot point at each other.'
    elif constant_accepts_nothing:
        validation = 'Nothing can point to constants.'
    elif constant_must_point_to_op:
        validation = 'Constants must point to operators.'
    elif args_and_kwargs_reject_operators:
        validation = 'Operators cannot point to args and kwargs.'
    elif the_connection_already_exists:
        validation = 'The connection already exists.'
    elif bb_only_points_to_accounts:
        validation = 'BB must point to Accounts.'
    else:
        validation = 'valid'
    return validation


def validate_connection_by_coords(coordinate_from, coordinate_to, connections: Et.Connections, shapes: Et.Shapes,
                                  search_from: tuple = None):
    id_from = shapes.get_shape_id_at_the_coordinate(*coordinate_from, search_from)
    id_to = shapes.get_shape_id_at_the_coordinate(*coordinate_to, search_from)
    validation = validate_connection(id_from, id_to, connections, shapes)
    return validation


def connect_shapes_and_feedback(add_connections: tp.Callable, coordinate_from: tuple, coordinate_to: tuple,
                                set_status_bar: tp.Callable, shapes: Et.Shapes, search_from: tuple = None):
    id_from = shapes.get_shape_id_at_the_coordinate(*coordinate_from, search_from)
    id_to = shapes.get_shape_id_at_the_coordinate(*coordinate_to, search_from)
    request_model = RequestModel.request_model_add_connection
    add_connections([request_model(id_from, id_to)])
    set_status_bar(f'Connection made from {id_from} to {id_to}.')


def clear_connector_line_and_status_bar(delete_shape_connector_line: tp.Callable, set_status_bar: tp.Callable):
    delete_shape_connector_line()
    set_status_bar('')


def move_shapes(delta_x, delta_y, shape_ids: tp.Iterable, shapes: Et.Shapes):
    for shape_id in shape_ids:
        x, y = shapes.get_x(shape_id), shapes.get_y(shape_id)
        shapes.set_x(shape_id, x + delta_x)
        shapes.set_y(shape_id, y + delta_y)


def show_connectable_shapes(id_from, shapes: Et.Shapes, search_from: tuple, connections: Et.Connections,
                            highlight_manually: tp.Callable):
    for shape_id in search_from:
        validation = validate_connection(id_from, shape_id, connections, shapes)
        if validation == 'valid':
            shapes.set_border_color(shape_id, 'blue')
            shapes.set_border_width(shape_id, 3)
        else:
            shapes.set_border_color(shape_id, 'red')
            shapes.set_border_width(shape_id, 3)

    highlight_manually()


def set_account_order(account_order: Et.AccountOrder, new_shape_ids, shapes: Et.Shapes):
    for shape_id in new_shape_ids:
        if shapes.get_tag_type(shape_id) == 'account':
            account_order.add_element_to_last(shape_id)


def get_account_names_by_order(account_order: Et.AccountOrder, shapes: Et.Shapes) -> tuple:
    account_names_by_order = []
    for shape_id in account_order.data:
        account_name = '' if account_order.is_blank(shape_id) else shapes.get_text(shape_id)
        account_names_by_order.append(account_name)
    return tuple(account_names_by_order)


def get_select_flags(account_order: Et.AccountOrder, selection: Et.Selection) -> tuple:
    select_flags = []
    for shape_id in account_order.data:
        select_flags.append(selection.is_selected(shape_id))
    return tuple(select_flags)


def get_line_color_and_user_feedback_based_on_validation(id_from, id_to, color, validation) -> tuple:
    is_valid = validation == 'valid'
    color = 'red' if not is_valid else color
    feed_back = f'Valid connection from {id_from} to {id_to}' if is_valid else validation
    return color, feed_back


def sort_accounts(shapes_to_be_moved: tp.Iterable, sign, by: int, account_order: Et.AccountOrder,
                  change_account_order: tp.Callable) -> bool:
    shape_ids = shapes_to_be_moved
    current_shape_orders = get_current_account_orders(account_order, shape_ids)
    destinations = [order + sign * by for order in current_shape_orders]
    shape_id_to_destination = dict(zip(shape_ids, destinations))
    counter = 0
    while not sorting_is_complete(current_shape_orders, shape_id_to_destination, len(account_order.data)):
        counter += 1
        if counter > 100:
            return False
        for shape_id, destination in shape_id_to_destination.items():
            index_ = account_order.get_order(shape_id)
            if index_ != destination:
                change_account_order(index_, destination)
        current_shape_orders = get_current_account_orders(account_order, shape_ids)

    return True


def sorting_is_complete(current_account_orders: list, shape_id_to_destination: dict, total_number: int) -> bool:
    destinations = []
    for destination in shape_id_to_destination.values():
        if destination < 0:
            destination += total_number
        elif destination >= total_number:
            destination -= total_number
        destinations.append(destination)
    return current_account_orders == destinations


def get_current_account_orders(account_order: Et.AccountOrder, shape_ids: tp.Iterable) -> list:
    return [account_order.get_order(shape_id) for shape_id in shape_ids]


def save_state_without_using_memento(cls_gateway: tp.Type[GateWayABC], entities: Et.Entities, ) -> GateWayABC:
    temporary_gateway = cls_gateway(entities)
    temporary_gateway.save_state(temporary_save_state_name)
    return temporary_gateway


def restore_state_without_using_memento(gateway: GateWayABC):
    gateway.undo()


def decide_what_to_select_next(account_order: Et.AccountOrder, selection: Et.Selection):
    try:
        last_position = max(get_account_order_none_removed(account_order, selection.data)) + 1
    except ValueError:
        last_position = -1
    next_element = account_order.get_element(last_position)
    return next_element


def get_account_order_none_removed(account_order: Et.AccountOrder, account_ids) -> set:
    orders = set(get_current_account_orders(account_order, account_ids))
    if None in orders:
        orders.remove(None)
    return orders


def get_shape_id_at_mouse_point(shapes: Et.Shapes, request: dict, search_from: tuple = None):
    x, y = request['x'], request['y']
    shape_at_the_coordinate = shapes.get_shape_id_at_the_coordinate(x, y, search_from)
    return shape_at_the_coordinate


def get_common_properties(shape_ids: tuple, shapes: Et.Shapes, worksheets: Et.Worksheets, format_: Et.Format,
                          number_format: Et.NumberFormat, vertical_accounts: Et.VerticalAccounts,
                          uom: Et.UnitOfMeasure) -> tuple:
    texts = set()
    xs = set()
    ys = set()
    widths = set()
    heights = set()
    sheets = set()
    formats = set()
    number_formats = set()
    vertical_acs = set()
    uoms_set = set()

    for shape_id in shape_ids:
        if shape_id_is_not_blank(shape_id, shapes):
            texts.add(shapes.get_text(shape_id))
            xs.add(shapes.get_x(shape_id))
            ys.add(shapes.get_y(shape_id))
            widths.add(shapes.get_width(shape_id))
            heights.add(shapes.get_height(shape_id))
            sheets.add(worksheets.get_worksheet_of_an_account(shape_id))
            f = format_.get_format(shape_id)
            if f is not None:
                formats.add(f)
            f = number_format.get_format(shape_id)
            if f is not None:
                number_formats.add(f)
            vertical_acs.add(vertical_accounts.is_a_vertical_account(shape_id))
            uoms_set.add(uom.get_unit_of_measure(shape_id))

    text = texts.pop() if len(texts) == 1 else ''
    x = xs.pop() if len(xs) == 1 else ''
    y = ys.pop() if len(ys) == 1 else ''
    width = widths.pop() if len(widths) == 1 else ''
    height = heights.pop() if len(heights) == 1 else ''
    worksheet = sheets.pop() if len(sheets) == 1 else ''
    shape_id = tuple(shape_ids)[0] if len(shape_ids) == 1 else ''
    cell_format = formats.pop() if len(formats) == 1 else 'None'
    cell_number_format = number_formats.pop() if len(number_formats) == 1 else ''
    vertical_references = vertical_acs.pop() if len(vertical_acs) == 1 else False
    uoms = uoms_set.pop() if len(uoms_set) == 1 else ''

    return text, x, y, width, height, worksheet, shape_id, cell_format, cell_number_format, vertical_references, uoms


def shape_id_is_not_blank(shape_id, shapes):
    return shape_id in shapes.data


def move_shapes_to_one_direction_algorithm(initial_x, initial_y, request, shape_x, shape_y):
    mouse_x, mouse_y = request['x'], request['y']
    clicked_x, clicked_y = request['coordinates'][0]
    delta_x, delta_y = request['delta_x'], request['delta_y']
    distance_x = mouse_x - clicked_x
    distance_y = mouse_y - clicked_y
    if abs(distance_x) >= abs(distance_y):
        delta_y = initial_y - shape_y
    else:
        delta_x = initial_x - shape_x
    return delta_x, delta_y


def selections_are_the_same(selection1: set, selection2: set) -> bool:
    # Blank objects within sets are not 'equal'
    return set(str(element) for element in selection1) == set(str(element) for element in selection2)


def prevent_any_shapes_from_entering_negative_x_y_area(delta_x: float, delta_y: float, shape_ids: tp.Iterable,
                                                       shapes: Et.Shapes) -> tp.Tuple[float, float]:
    left_most_shape = shapes.get_left_most_shape_id(shape_ids)
    top_most_shape = shapes.get_top_shape_id(shape_ids)

    left_most_x = shapes.get_x(left_most_shape)
    top_y = shapes.get_y(top_most_shape)

    delta_x -= min(0, left_most_x + delta_x)
    delta_y -= min(0, top_y + delta_y)

    return delta_x, delta_y


def get_input_accounts(connections: Et.Connections, shapes: Et.Shapes, negative_list: tp.Iterable = ()) -> tuple:
    c, s = connections, shapes
    return tuple(i for i in s.shapes_ids
                 if s.get_tag_type(i) == 'account'
                 and len(c.get_connections_into(i)) == 0
                 and i not in negative_list)


def get_circular_reference_free_accounts(connections: Et.Connections, shapes: Et.Shapes) -> set:
    safe_accounts = set()

    for shape_id in shapes.shapes_ids:
        tag_type = shapes.get_tag_type(shape_id)
        if tag_type in ('bb', 'constant'):
            safe_accounts.add(shape_id)
        elif tag_type in ('account', 'operator'):
            dependencies = connections.get_connections_into(shape_id)
            if len(dependencies) == 0:
                safe_accounts.add(shape_id)  # Either 1)Input Account, or 2) Operator to Core Account

    for safe_account in tuple(safe_accounts):
        add_shapes_that_depend_only_on_safe_accounts(safe_account, safe_accounts, shapes, connections, set())

    return safe_accounts


def add_shapes_that_depend_only_on_safe_accounts(safe_account, safe_accounts: set, shapes: Et.Shapes,
                                                 connections: Et.Connections, already_searched: set = None):
    already_searched = set() if already_searched is None else already_searched
    already_searched.add(safe_account)
    for dependant in connections.get_connections_out_of(safe_account):
        dependant_type = shapes.get_tag_type(dependant)
        if dependant_type == 'account':
            account_is_safe = check_if_an_account_is_safe(dependant, already_searched, safe_accounts, connections)
            if not account_is_safe:
                return
            new_safe_account = dependant
            safe_accounts.add(new_safe_account)
            for new_safe_account_relay in shapes.get_relays(new_safe_account):
                safe_accounts.add(new_safe_account_relay)
                already_searched.add(new_safe_account_relay)
            add_shapes_that_depend_only_on_safe_accounts(new_safe_account, safe_accounts, shapes, connections,
                                                         already_searched)
        elif dependant_type == 'operator':
            operator = dependant
            operator_is_safe = True
            for account in connections.get_connections_into(operator):
                account = account
                if account not in safe_accounts:
                    operator_is_safe = False
                    break

            if operator_is_safe:
                recursively_check_dependants(operator, already_searched, connections, safe_accounts, shapes)
        elif dependant_type == 'relay':
            relay = dependant
            recursively_check_dependants(relay, already_searched, connections, safe_accounts, shapes)


def recursively_check_dependants(account, already_searched, connections, safe_accounts, shapes):
    safe_accounts.add(account)
    args = account, safe_accounts, shapes, connections, already_searched
    add_shapes_that_depend_only_on_safe_accounts(*args)


def check_if_an_account_is_safe(account, already_searched: set, safe_accounts: set,
                                connections: Et.Connections) -> bool:
    if account in already_searched:
        return False
    else:
        already_searched.add(account)
    for dependency in connections.get_connections_into(account):
        if dependency not in safe_accounts:
            return False
    return True


def identify_shape_ids_to_update(key, shape_ids, shapes) -> tuple:
    if key == 'text':
        shape_ids_with_origin = set(shape_ids)
        for shape_id in shape_ids:
            origin = shapes.get_shape_it_represents(shape_id)
            if origin is not None:
                shape_ids_with_origin.add(origin)

        shape_ids_to_update = set()
        for shape_id in shape_ids_with_origin:
            shape_ids_to_update.add(shape_id)
            for s in shapes.get_relays(shape_id):
                shape_ids_to_update.add(s)
    else:
        shape_ids_to_update = shape_ids
    return shape_ids_to_update


def get_filtered_connection(all_connections: tuple, positive_list: tuple):
    connections_withing_the_sheet = []
    for connection_from, connection_to in all_connections:
        if connection_from in positive_list and connection_to in positive_list:
            connections_withing_the_sheet.append((connection_from, connection_to))
    connections = tuple(connections_withing_the_sheet)
    return connections


def sort_by_account_order(accounts_to_sort: tuple,
                          account_orders: Et.AccountOrders,
                          worksheets: Et.Worksheets) -> tuple:
    sorted_accounts_list = []
    for sheet_name in worksheets.sheet_names:
        account_order = account_orders.get_account_order(sheet_name)
        for element in account_order.data:
            if element in accounts_to_sort:
                sorted_accounts_list.append(element)
    sorted_accounts = tuple(sorted_accounts_list)
    return sorted_accounts


def connection_filter(connection: tuple, sheet_contents: tuple, selection: set, relays: tuple, y_axes=(), bars=(),
                      sliders=(), accounts=(), live_values=()) -> bool:
    from_, to_ = connection
    if from_ not in sheet_contents:
        return False
    if to_ not in sheet_contents:
        return False
    if to_ in relays + y_axes + bars + live_values:
        if from_ not in selection and to_ not in selection:
            return False
    if to_ in sliders:
        if to_ not in selection and (from_ not in accounts):
            return False
    return True


def select_input_account_to_edit(inputs, selections_data):
    selected_accounts = tuple(selections_data)
    if len(inputs) == 0:
        input_account = None
    elif len(selected_accounts) == 1:
        selected_account = selected_accounts[0]
        if selected_account in inputs:
            input_account = selected_account
        else:
            input_account = None
    else:
        input_account = inputs[0]
    return input_account


def get_next_input_to_edit(current_input, shift, sorted_input_accounts):
    position = sorted_input_accounts.index(current_input) if current_input in sorted_input_accounts else -1
    try:
        next_input = sorted_input_accounts[position + shift]
    except IndexError:
        next_input = sorted_input_accounts[0]
    return next_input


def get_external_dependents(connections_out, sheet_name, shape_id_to_sheet_name: dict):
    external_dependents = []
    for shape_id_dependent in connections_out:
        try:
            external_sheet = shape_id_to_sheet_name[shape_id_dependent]
        except KeyError:
            continue
        if external_sheet != sheet_name:
            external_dependents.append(external_sheet)
    return external_dependents


def get_y_shift_to_prevent_overlap(shape_ids: tp.Iterable, sheet_to_contents: dict, increment_y, shapes: Et.Shapes):
    bottom_shape = shapes.get_bottom_shape_id(shape_ids)
    bottom_shape_sheet_to = shapes.get_bottom_shape_id(sheet_to_contents)
    largest_y_in_sheet_from = shapes.get_y(bottom_shape)
    if bottom_shape_sheet_to is not None:
        largest_y_in_sheet_to = shapes.get_y(bottom_shape_sheet_to)
    else:
        largest_y_in_sheet_to = 0

    if len(sheet_to_contents) > 0:
        top_shape = shapes.get_top_shape_id(sheet_to_contents)
        smallest_y_in_sheet_to = shapes.get_y(top_shape)
    else:
        return 0

    if largest_y_in_sheet_from + increment_y < smallest_y_in_sheet_to:
        return 0
    else:
        return largest_y_in_sheet_to + increment_y


def get_external_dependencies_sheets(connections_in, id_to_sheet, sheet_name):
    external_dependencies = []
    for id_ in connections_in:
        if id_ in id_to_sheet:
            if id_to_sheet[id_] != sheet_name:
                external_dependencies.append(id_to_sheet[id_])
    external_dependencies = tuple(external_dependencies)
    return external_dependencies


def is_a_connection_out_of_current_sheet(current_sheet_contents: tuple, from_, to_) -> bool:
    return (from_ in current_sheet_contents) and (to_ not in current_sheet_contents)


def is_connection_into_current_sheet(current_sheet_contents: tuple, from_, to_) -> bool:
    return (to_ in current_sheet_contents) and (from_ not in current_sheet_contents)


def get_dependencies(shape_id, shapes: Et.Shapes, connections: Et.Connections, dependencies=None, searched=None) -> set:
    dependencies = set() if dependencies is None else dependencies
    searched = set() if searched is None else searched
    for dependency in connections.get_connections_into(shape_id):
        if dependency not in searched:
            searched.add(dependency)
            dependencies.add(dependency)
            get_dependencies(dependency, shapes, connections, dependencies, searched)
    return dependencies


def get_all_circular_connections(connections: Et.Connections, shapes: Et.Shapes) -> set:
    circular_connections = set()
    graph = connections_graph_factory(connections, shapes)

    for cycle in graph.get_simple_cycles():
        for n, element in enumerate(cycle):
            if n != len(cycle) - 1:
                next_element = cycle[n + 1]
                circular_connections.add((element, next_element))
    return circular_connections


def get_topological_order(shapes: Et.Shapes, connections: Et.Connections):
    graph = connections_graph_factory(connections, shapes)
    return graph.get_topological_order()


def connections_graph_factory(connections: Et.Connections, shapes: Et.Shapes) -> Graph:
    graph = Graph()
    for from_, to_ in connections.data:
        from_type = shapes.get_tag_type(from_)
        to_type = shapes.get_tag_type(to_)
        if from_type not in ('bb', 'constant') and to_type not in ('bb', 'constant'):
            graph.add_edge(from_, to_)
    return graph


def get_minimum_circular_dependencies(shape_id, connections: Et.Connections, shapes: Et.Shapes) -> tuple:
    graph = connections_graph_factory(connections, shapes)
    circular_dependencies = set()
    for cycle in graph.get_simple_cycles():
        if shape_id in cycle:
            circular_dependencies = circular_dependencies.union(set(cycle))
    return tuple(circular_dependencies)


def is_cyclic(shape_id, connections: Et.Connections, shapes: Et.Shapes) -> bool:
    graph = connections_graph_factory(connections, shapes)
    return graph.is_circular(shape_id)


def get_cycle_breakers(connections: Et.Connections, shapes: Et.Shapes) -> dict:
    graph = connections_graph_factory(connections, shapes)
    cycle_breakers = tuple(graph.get_cycle_breakers())

    cycle_breakers_account = tuple(i for i in cycle_breakers if shapes.get_tag_type(i) in ('account', 'relay'))
    account_names = tuple(shapes.get_text(i) for i in cycle_breakers_account)
    return dict(zip(cycle_breakers_account, account_names))


def parse_arg_str(args_str: str):
    if ',' in args_str:
        if '(' in args_str and ')' in args_str:
            args_str = args_str.replace('(', '').replace(')', '')
            args_str = comma_separated_string_to_tuple(args_str)
            args = (tuple(Utilities.convert_to_number_if_possible(i) for i in args_str),)
        else:
            args = comma_separated_string_to_tuple(args_str)
            args = tuple(Utilities.convert_to_number_if_possible(a) for a in args)
    else:
        args_str = Utilities.convert_to_number_if_possible(args_str)
        args = (args_str,)
    return args


def comma_separated_string_to_tuple(args_str: str) -> tuple:
    return tuple(string.strip(' ') for string in args_str.split(','))


def if_relay_then_get_the_the_original_account(base_account, relay_mapper: dict):
    if base_account in relay_mapper:
        base_account = relay_mapper[base_account]
    return base_account


def get_original_account(relay, relay_to_original_mapper: dict):
    if relay in relay_to_original_mapper:
        return relay_to_original_mapper[relay]
    else:
        return relay


def get_direct_links(connections, relay_to_original_mapper, shapes, bb_shift) -> tuple:
    account_ids = shapes.get_shapes('account')
    direct_links_list = []
    mapper = relay_to_original_mapper
    for connection_from, connection_to in connections.data:
        if shapes.get_tag_type(connection_to) == 'relay':
            continue
        shift = 0
        from_ = get_original_account(connection_from, mapper)
        to_ = get_original_account(connection_to, mapper)
        if (from_ in account_ids) and (to_ in account_ids):
            direct_links_list.append((from_, to_, shift))
    for shifter in shapes.get_shapes('bb'):
        shift = bb_shift
        """
        1) Shifters are (must be) guaranteed to have one account pointing to itself.
        2) Shifter can point to many things
        """
        connections_into = connections.get_connections_into(shifter)
        if connections_into:
            connection_from = connections_into.pop()
            connection_from = get_original_account(connection_from, mapper)
            connection_tos = connections.get_connections_out_of(shifter)
            for connection_to in connection_tos:
                direct_links_list.append((connection_from, connection_to, shift))
    direct_links = tuple(direct_links_list)
    return direct_links


def get_accounts_that_match_name(account_name, sheet_name, selected_sheet_contents: tp.Iterable, shapes: Et.Shapes,
                                 worksheets: Et.Worksheets) -> tuple:
    if sheet_name is None:
        sheet_contents = selected_sheet_contents
    else:
        sheet_contents = worksheets.get_sheet_contents(sheet_name)
    candidates = tuple(shape for shape in sheet_contents if shapes.get_text(shape) == account_name)
    return candidates


def get_dependants_str(shape_id, connections: Et.Connections, shapes: Et.Shapes, worksheets: Et.Worksheets) -> str:
    depended_by = connections.get_connections_out_of(shape_id)
    feedback = 'Selection is depended by:'
    for n, depending_account in enumerate(depended_by):
        text = shapes.get_text(depending_account)
        sheet_name = worksheets.get_worksheet_of_an_account(depending_account)
        feedback += f' {n}){sheet_name}!{text},'
    return feedback


def get_original_account_of_relay_str(feedback, shape_id, shapes, worksheets) -> str:
    relay = shape_id
    original_ac = shapes.get_shape_it_represents(relay)
    if worksheets.get_worksheet_of_an_account(original_ac) != worksheets.selected_sheet:
        sheet_name = worksheets.get_worksheet_of_an_account(original_ac)
        relay_text = shapes.get_text(relay)
        feedback = f'Relay of [{relay_text}] in Sheet [{sheet_name}].'
    return feedback


def place_a_shape_above_another(place_this, above_this, gap: int, shapes: Et.Shapes, connections: Et.Connections):
    x = (shapes.get_x(above_this) + shapes.get_width(above_this) / 2) - shapes.get_width(place_this) / 2
    shapes.set_x(place_this, x)
    shapes.set_y(place_this, shapes.get_y(above_this) - gap)
    connections.add_connection(place_this, above_this)


def consider_parent_child_level_and_identify_which_sheets_to_shift(indexes: tuple, shift: int,
                                                                   worksheets: Et.Worksheets,
                                                                   ws_relationship: Et.WorksheetRelationship) -> tuple:
    shifting_down = shift > 0
    shifting_up = shift < 0

    all_worksheet_names = worksheets.sheet_names
    all_parents_sheet_name = identify_all_parents(all_worksheet_names, indexes, ws_relationship)
    new_indexes = drag_all_children_of_any_parent(all_parents_sheet_name, indexes, worksheets, ws_relationship)

    for sheet_index in tuple(new_indexes):
        sheet_name = all_worksheet_names[sheet_index]

        other_id = sheet_index + shift
        try:
            other_sheet_name = all_worksheet_names[other_id]
        except IndexError:
            other_sheet_name = None
        is_a_parent = ws_relationship.is_a_parent(other_sheet_name)
        has_a_parent = ws_relationship.has_a_parent(other_sheet_name)
        not_shifting = other_id not in new_indexes
        other_sheet_exists = other_sheet_name is not None
        shifting_into_other_parent_range = other_sheet_exists and (is_a_parent or has_a_parent) and not_shifting

        if ws_relationship.has_a_parent(sheet_name):
            parent_sheet_name = ws_relationship.get_parent_worksheet(sheet_name)
            all_siblings_names = ws_relationship.get_children_sheet_names(parent_sheet_name)
            all_siblings_index = tuple(worksheets.get_sheet_position(name) for name in all_siblings_names)
            parent_index = worksheets.get_sheet_position(parent_sheet_name)
            the_sheet_is_the_child_at_the_bottom_of_siblings = max(all_siblings_index) == sheet_index
            its_parent_is_not_shifting_down = parent_index not in new_indexes

            the_sheet_is_the_child_at_the_top_of_siblings = min(all_siblings_index) == sheet_index
            its_parent_is_not_shifting_up = parent_index not in new_indexes

            if shifting_down:
                if the_sheet_is_the_child_at_the_bottom_of_siblings and its_parent_is_not_shifting_down:
                    prevent_the_child_from_shifting(new_indexes, sheet_index)
            elif shifting_up:
                if the_sheet_is_the_child_at_the_top_of_siblings and its_parent_is_not_shifting_up:
                    prevent_the_child_from_shifting(new_indexes, sheet_index)
        elif shifting_into_other_parent_range:
            if len(ws_relationship.get_children_sheet_names(sheet_name)) == 0:
                if is_a_parent:
                    other_parent_name = other_sheet_name
                else:
                    other_parent_name = ws_relationship.get_parent_worksheet(other_sheet_name)
                add_the_parent_as_the_child_s_parent(other_parent_name, sheet_name, ws_relationship)
                if shifting_up:
                    new_indexes.remove(sheet_index)

    return tuple(sorted(new_indexes))


def drag_all_children_of_any_parent(all_parents_sheet_name: set, indexes: tuple, worksheets: Et.Worksheets,
                                    ws_relationship: Et.WorksheetRelationship) -> set:
    new_indexes = set(indexes)
    for parent_sheet_name in all_parents_sheet_name:
        parent_index = worksheets.get_sheet_position(parent_sheet_name)
        if parent_index in indexes:
            children_names = ws_relationship.get_children_sheet_names(parent_sheet_name)
            for child_name in children_names:
                child_index = worksheets.get_sheet_position(child_name)
                new_indexes.add(child_index)
    return new_indexes


def identify_all_parents(all_worksheet_names: tuple, indexes: tuple, ws_relationship: Et.WorksheetRelationship):
    all_parents_sheet_name = set(ws_relationship.all_parent_sheets)
    for sheet_index in indexes:
        sheet_name = all_worksheet_names[sheet_index]
        if ws_relationship.has_a_parent(sheet_name):
            parent_sheet_name = ws_relationship.get_parent_worksheet(sheet_name)
            all_parents_sheet_name.add(parent_sheet_name)
    return all_parents_sheet_name


def prevent_the_child_from_shifting(new_indexes: set, child_index):
    new_indexes.remove(child_index)


def add_the_parent_as_the_child_s_parent(other_parent_name, child_name, ws_relationship: Et.WorksheetRelationship):
    ws_relationship.add_worksheet_parent_child_relationship(other_parent_name, child_name)


def get_adjusted_shift(adjacent_sheet_name: str, filtered_indexes: tuple, shift: int, worksheets: Et.Worksheets,
                       ws_relationship: Et.WorksheetRelationship) -> int:
    sheet_name_in_question = worksheets.get_sheet_name_by_index(min(filtered_indexes))
    my_parent = ws_relationship.get_parent_worksheet(sheet_name_in_question)
    adjacent_has_a_parent = ws_relationship.has_a_parent(adjacent_sheet_name)
    adjacent_parent = ws_relationship.get_parent_worksheet(adjacent_sheet_name)
    neither_has_parent = (my_parent is None and adjacent_parent is None)
    parents_are_different = (adjacent_has_a_parent and (my_parent != adjacent_parent))
    adjacent_is_my_parent = adjacent_sheet_name == my_parent
    if adjacent_has_a_parent:
        adjacent_sheet_name = ws_relationship.get_parent_worksheet(adjacent_sheet_name)
    if parents_are_different or neither_has_parent:
        n_adjacent_shapes_children = len(ws_relationship.get_children_sheet_names(adjacent_sheet_name))
        sign = shift
        adjusted_shift = sign * (n_adjacent_shapes_children + 1)
    elif adjacent_is_my_parent:
        n_adjacent_shapes_children = len(ws_relationship.get_children_sheet_names(adjacent_sheet_name))
        sign = shift
        adjusted_shift = sign * (n_adjacent_shapes_children)
    else:
        adjusted_shift = shift
    return adjusted_shift
