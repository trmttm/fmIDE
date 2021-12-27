from typing import Tuple

from . import constants as cns


def draw_line(line_id, coords1: Tuple[int, int], coords2: Tuple[int, int], width, color):
    return {
        line_id: {
            cns.coordinate_from: coords1,
            cns.coordinate_to: coords2,
            cns.line_width: width,
            cns.line_color: color,
        }
    }
