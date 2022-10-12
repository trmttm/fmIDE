import interface_tk as intf

from ...BoundaryOutput import PresenterABC


class PresenterAddWorksheet(PresenterABC):

    def create_view_model(self, response_model: dict) -> dict:
        f = intf.widget_model
        f_0 = ((0,), (1,)), ((0,), (1,))
        sheet_name = response_model.get('sheet_name')
        color = response_model.get('color')
        frame_canvas = f'frame_canvas_{sheet_name}'
        canvas_id = f'canvas_{sheet_name}'
        view_model = [
            f('fr_pwr', frame_canvas, 'frame', 0, 0, 0, 0, 'nsew', **intf.frame_options(*f_0)),
            f(frame_canvas, canvas_id, 'canvas', 0, 0, 0, 0, 'nsew', bg=color),
        ]
        return {'view_model': view_model, 'frame_canvas': frame_canvas, 'canvas_id': canvas_id}
