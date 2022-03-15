from ..Entities import Selections
from ..Entities import Worksheets


def property_select_new_shapes_in_each_worksheet(shapes_added: set, selections: Selections, worksheets: Worksheets):
    for worksheet in worksheets.sheet_names:
        sheet_selection = selections.get_selection(worksheet)
        sheet_contents = set(worksheets.get_sheet_contents(worksheet))

        new_shapes_in_the_worksheet = shapes_added.intersection(sheet_contents)
        if len(new_shapes_in_the_worksheet) > 0:
            sheet_selection.clear_selection()
            for new_shape in new_shapes_in_the_worksheet:
                sheet_selection.add_selection(new_shape)
