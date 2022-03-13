from ..Entities import Configurations
from ..Entities import Shapes
from ..Entities import Worksheets


def figure_out_x_where_to_place_new_relay(connection_to, sheet_to, sheet_to_right_most_x: dict, worksheets: Worksheets,
                                          shapes: Shapes, configurations: Configurations, margin=25) -> int:
    if configurations.relay_to_be_placed_at_right_end:
        x = get_right_most_x(sheet_to, sheet_to_right_most_x, shapes, worksheets, margin)
    else:
        x = shapes.get_x(connection_to) + shapes.get_width(connection_to) + margin
    return x


def get_right_most_x(sheet_to, sheet_to_right_most_x: dict, shapes: Shapes, worksheets: Worksheets, margin=25):
    external_relay_x = sheet_to_right_most_x.get(sheet_to, None)
    if external_relay_x is None:
        sheet_contents = worksheets.get_sheet_contents(sheet_to)
        contents_except_relays = tuple(c for c in sheet_contents if shapes.get_tag_type(c) != 'relay')
        right_most_shape_id = shapes.get_right_most_shape_id(contents_except_relays)

        right_most_x = shapes.get_x(right_most_shape_id)
        right_most_width = shapes.get_width(right_most_shape_id) + margin
        external_relay_x = right_most_x + right_most_width
    sheet_to_right_most_x[sheet_to] = external_relay_x
    return external_relay_x
