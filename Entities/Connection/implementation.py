import copy
from typing import Set


def get_all_connections_with_a_shape(connections_data: Set[tuple], shape_id) -> tuple:
    all_connections_with_a_shape = []
    for connection in copy.deepcopy(connections_data):
        if shape_id in connection:
            all_connections_with_a_shape.append(connection)
    return tuple(all_connections_with_a_shape)


def get_connections_into_shape_id(connections_data: Set[tuple], shape_id) -> set:
    connections_into_shape_id = set()
    for connection_from, connection_to in connections_data:
        if connection_to == shape_id:
            connections_into_shape_id.add(connection_from)
    return connections_into_shape_id


def get_connections_out_of_shape_id(connections_data: Set[tuple], shape_id) -> set:
    connections_out_of_shape_id = set()
    for connection_from, connection_to in connections_data:
        if connection_from == shape_id:
            connections_out_of_shape_id.add(connection_to)
    return connections_out_of_shape_id


def merge_connections_data(connections, connections_data, shape_id_converter):
    for shape_id_from, shape_id_to in connections_data:
        converted_shape_id_from = convert_shape_id(shape_id_from, shape_id_converter)
        converted_shape_id_to = convert_shape_id(shape_id_to, shape_id_converter)

        connections.add_connection(converted_shape_id_from, converted_shape_id_to)
        connections.add_new_merged_connections(converted_shape_id_from, converted_shape_id_to)


def convert_shape_id(shape_id, shape_id_converter: dict):
    try:
        converted_shape_id_from = shape_id_converter[shape_id]
    except KeyError:  # Socket
        converted_shape_id_from = shape_id
    return converted_shape_id_from


def change_shape_id(connection, new_shape_id, old_shape_id):
    for connection_from, connection_to in connection.data:
        if connection_from == old_shape_id:
            connection.add_connection(new_shape_id, connection_to)
            connection.remove_connection(connection_from, connection_to)
        elif connection_to == old_shape_id:
            connection.add_connection(connection_from, new_shape_id)
            connection.remove_connection(connection_from, connection_to)
