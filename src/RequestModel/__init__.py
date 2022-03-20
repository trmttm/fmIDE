import Utilities


def request_model_add_new_shape(text: str, tag: str = None) -> dict:
    if tag is None:
        if Utilities.is_number(text):
            tag = 'constant'
        elif text in ['+', '-', '*', '/', 'x', '**', '^']:
            tag = 'operator'
        else:
            tag = 'account'
    return {'text': text, 'tags': (tag,)}


def request_model_place(shape_id, x, y) -> dict:
    return {'shape_id': shape_id, 'x': x, 'y': y}


def request_model_move(shape_id, delta_x, delta_y) -> dict:
    return {'shape_id': shape_id, 'delta_x': delta_x, 'delta_y': delta_y}


def request_model_add_to_selection(shape_id) -> dict:
    return {'shape_id': shape_id}


def request_model_select_shape(shape_id) -> dict:
    return {'shape_id': shape_id}


def request_model_erase_shape(shape_id) -> dict:
    return {'shape_id': shape_id}


def request_model_draw_rectangle(coords1: tuple, coords2: tuple, width: float, color: str) -> dict:
    return {'coords1': coords1, 'coords2': coords2, 'width': width, 'color': color}


def request_model_erase_rectangle(rectangle_id) -> dict:
    return {'rectangle_id': rectangle_id}


def request_model_add_connection(id_from, id_to) -> dict:
    return {'id_from': id_from, 'id_to': id_to}


def request_model_remove_connection(id_from, id_to) -> dict:
    return {'id_from': id_from, 'id_to': id_to}


def request_model_remove_connection_of_a_shape(shape_id) -> dict:
    return {'shape_id': shape_id}


def request_model_draw_line(coordinate_from, coordinate_to, width, color) -> dict:
    return {'coordinate_from': coordinate_from, 'coordinate_to': coordinate_to, 'width': width, 'color': color, }


def request_model_erase_line(line_id) -> dict:
    return {'line_id': line_id, }
