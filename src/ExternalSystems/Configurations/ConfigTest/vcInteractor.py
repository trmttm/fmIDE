from typing import Callable

from interface_view import ViewABC


class ViewControllerInteractor:
    _clicked_canvas_item = '_clicked_canvas_item'
    _canvas_min_y = '_canvas_min_y'
    _canvas_max_y = '_canvas_min_x'
    _input_entry_observers = '_input_entry_observers'
    _input_entry_close_observers = '_input_entry_close_observers'
    _widget_id_min = '_widget_id_min'
    _widget_id_max = '_widget_id_max'
    _widget_id_digit = '_widget_id_digit'
    _number_of_periods = '_number_of_periods'
    _margin_rate = '_margin_rate'

    def __init__(self, view: ViewABC):
        self._view = view
        self._view_state = {}

        # cache
        self._previous_position = None

    def input_entry_control_by_graph(self):
        positions, y_range = self._create_request_model_to_controller()
        if positions != self._previous_position:
            self._previous_position = positions
            self.notify_input_entry_controller(positions, y_range)

    def input_entry_control_by_slider(self):
        positions_, y_range = self._create_request_model_to_controller()
        nop = self.get_number_of_periods()
        positions = tuple(positions_[0] for _ in range(nop))
        self.notify_input_entry_controller(positions, y_range)

    def attach_to_input_entry(self, observer: Callable):
        if self._input_entry_observers not in self._view_state:
            self._view_state[self._input_entry_observers] = [observer]
        else:
            self._view_state[self._input_entry_observers].append(observer)

    def attach_to_ie_close(self, observer: Callable):
        if self._input_entry_close_observers not in self._view_state:
            self._view_state[self._input_entry_close_observers] = [observer]
        else:
            self._view_state[self._input_entry_close_observers].append(observer)

    def notify_input_entry_controller(self, positions, y_range):
        for observer in self._view_state[self._input_entry_observers]:
            observer(y_range, positions)

    def set_view_state(self, key, value):
        self._view_state[key] = value

    def clear_input_entry_state(self):
        self._view_state = {}

    def _set_clicked_canvas_item(self, canvas_item):
        self.set_view_state(self._clicked_canvas_item, canvas_item)

    def get_clicked_canvas_item(self):
        return self._view_state[self._clicked_canvas_item]

    def set_widget_id_min(self, widget_id):
        self._view_state[self._widget_id_min] = widget_id

    def _get_widget_id_min(self):
        return self._view_state[self._widget_id_min]

    def set_widget_id_digit(self, widget_id):
        self._view_state[self._widget_id_digit] = widget_id

    def _get_widget_id_digit(self):
        return self._view_state[self._widget_id_digit]

    def set_widget_id_max(self, widget_id):
        self._view_state[self._widget_id_max] = widget_id

    def _get_widget_id_max(self):
        return self._view_state[self._widget_id_max]

    def set_canvas_min_y(self, min_y):
        self.set_view_state(self._canvas_min_y, min_y)

    def _get_canvas_min_y(self):
        return self._view_state[self._canvas_min_y]

    def set_canvas_max_y(self, max_y):
        self.set_view_state(self._canvas_max_y, max_y)

    def _get_canvas_max_y(self):
        return self._view_state[self._canvas_max_y]

    def set_number_of_periods(self, number_of_periods: int):
        self._view_state[self._number_of_periods] = number_of_periods

    def get_number_of_periods(self) -> int:
        return self._view_state[self._number_of_periods]

    def graph_click_shape(self, request: dict):
        clicked_item = self._view.get_clicked_rectangle()
        self._set_clicked_canvas_item(clicked_item)

    def graph_move_shape(self, request: dict, by_slider: bool):
        delta_x, delta_y = 0, request['delta_y']
        y_range = (self._get_canvas_min_y(), self._get_canvas_max_y())
        self._view.move_item_vertically_within_range(self.get_clicked_canvas_item(), delta_x, delta_y, y_range)

        if by_slider:
            self.input_entry_control_by_slider()
        else:
            self.input_entry_control_by_graph()

    def set_margin_rate(self, margin_rate: float):
        self.set_view_state(self._margin_rate, margin_rate)

    @property
    def margin_rate(self) -> float:
        return self._view_state[self._margin_rate]

    def _create_request_model_to_controller(self):
        if self._input_entry_observers not in self._view_state:
            self._view_state[self._input_entry_observers] = []
        min_ = self._view.get_value(self._get_widget_id_min())
        max_ = self._view.get_value(self._get_widget_id_max())
        y_range = float(min_), float(max_)
        y_coordinates = self._view.get_mid_y_coordinates_of_all_rectangles_on_canvas()
        canvas_min = margin = self._get_canvas_min_y()
        canvas_max = self._get_canvas_max_y()
        lengths = tuple(y - margin for y in y_coordinates)
        positions = tuple(length / (canvas_max - canvas_min) for length in lengths)
        return positions, y_range

    def close(self, widget_id):
        self._view.close(widget_id)
        for observer in self._view_state[self._input_entry_close_observers]:
            observer()
        self.clear_input_entry_state()
