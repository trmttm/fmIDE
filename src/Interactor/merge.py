def property_select_new_shapes_in_each_worksheet(shapes_added, selections, worksheets):
    for worksheet in worksheets.sheet_names:
        sheet_selection = selections.get_selection(worksheet)
        sheet_selection.clear_selection()
        for shape_id in worksheets.get_sheet_contents(worksheet):
            if shape_id in shapes_added:
                sheet_selection.add_selection(shape_id)
