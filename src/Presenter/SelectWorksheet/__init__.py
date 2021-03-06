from ...BoundaryOutput import PresenterABC


class PresenterSelectWorksheet(PresenterABC):

    def create_view_model(self, response_model: dict) -> dict:
        sheet_name = response_model.get('sheet_name')
        update = response_model.get('update')
        frame_canvas = f'frame_canvas_{sheet_name}'
        canvas_id = f'canvas_{sheet_name}'
        return {'frame_canvas': frame_canvas, 'canvas_id': canvas_id, 'update': update}
