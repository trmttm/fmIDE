from interface_view import ViewABC

from ..BoundaryOutput import PresentersABC


def plug_views_to_presenters(presenters: PresentersABC, view: ViewABC):
    presenters.attach_to_add_shape(lambda view_model_: view.add_text_box(view_model_))
    presenters.attach_to_remove_shape(lambda view_model_: view.remove_text_box(view_model_))
    presenters.attach_to_move_shapes(lambda view_model_: view.move_shapes(view_model_))
    presenters.attach_to_connect_shapes(lambda view_model_: view.connect_shapes(view_model_))
    presenters.attach_to_highlight_shape(lambda view_model_: view.highlight_shapes(view_model_))
    presenters.attach_to_draw_rectangle(lambda view_model_: view.draw_rectangle(view_model_))
    presenters.attach_to_draw_line(lambda view_model_: view.draw_line(view_model_))
    presenters.attach_to_update_status_bar(lambda view_model_: view.update_status_bar(view_model_))
    presenters.attach_to_clear_canvas(lambda view_model_: view.clear_canvas(view_model_))
    presenters.attach_to_load_pickle_files_list(lambda view_model_: view.update_tree(view_model_))
