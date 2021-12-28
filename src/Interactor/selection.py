from typing import Iterable

from ..Entities import Shapes


def get_selected_accounts(selection_data: Iterable, shapes: Shapes) -> tuple:
    return tuple(shape_id for shape_id in selection_data if shapes.get_tag_type(shape_id) == 'account')
