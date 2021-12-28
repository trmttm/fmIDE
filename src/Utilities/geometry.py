from typing import Tuple


def lines_intersect(p1: tuple, p2: tuple, p3: tuple, p4: tuple) -> bool:
    tc1 = (p1[0] - p2[0]) * (p3[1] - p1[1]) + (p1[1] - p2[1]) * (p1[0] - p3[0])
    tc2 = (p1[0] - p2[0]) * (p4[1] - p1[1]) + (p1[1] - p2[1]) * (p1[0] - p4[0])
    td1 = (p3[0] - p4[0]) * (p1[1] - p3[1]) + (p3[1] - p4[1]) * (p3[0] - p1[0])
    td2 = (p3[0] - p4[0]) * (p2[1] - p3[1]) + (p3[1] - p4[1]) * (p3[0] - p2[0])
    return tc1 * tc2 < 0 and td1 * td2 < 0


def point_in_rectangle(bottom_left: tuple, top_right: tuple, point: tuple) -> bool:
    if (bottom_left[0] < point[0] < top_right[0]) and (bottom_left[1] < point[1] < top_right[1]):
        return True
    else:
        return False


def line_intersect_rectangle(p1: tuple, p2: tuple, bottom_left: tuple, top_right: tuple) -> bool:
    bottom_right = top_right[0], bottom_left[1]
    top_left = bottom_left[0], top_right[1]
    results = [
        point_in_rectangle(bottom_left, top_right, p1),
        point_in_rectangle(bottom_left, top_right, p2),
        lines_intersect(p1, p2, bottom_left, bottom_right),
        lines_intersect(p1, p2, top_left, top_right),
        lines_intersect(p1, p2, bottom_left, top_left),
        lines_intersect(p1, p2, bottom_right, top_right),
    ]
    return True in results


def get_nearest_points(coords1: Tuple[int, int, int, int], coords2: Tuple[int, int, int, int]) -> Tuple[
    Tuple[int, int], Tuple[int, int]]:
    x11, y11, x12, y12 = coords1
    x21, y21, x22, y22 = coords2
    midpoint_x1, midpoint_y1 = (x11 + x12) / 2, (y11 + y12) / 2
    midpoint_x2, midpoint_y2 = (x21 + x22) / 2, (y21 + y22) / 2

    n1, s1, w1, e1 = (midpoint_x1, y11), (midpoint_x1, y12), (x11, midpoint_y1), (x12, midpoint_y1)
    n2, s2, w2, e2 = (midpoint_x2, y21), (midpoint_x2, y22), (x21, midpoint_y2), (x22, midpoint_y2)

    distance_to_points = {}
    for point1 in [n1, s1, w1, e1]:
        for point2 in [n2, s2, w2, e2]:
            x1, y1 = point1
            x2, y2 = point2
            distance_squared = (x2 - x1) ** 2 + (y2 - y1) ** 2
            distance_to_points[distance_squared] = point1, point2

    point_from, point_to = distance_to_points[min(distance_to_points)]
    return point_from, point_to


def get_rectangle_edges(x1, x2, y1, y2) -> Tuple[tuple, tuple]:
    if x1 <= x2 and y1 <= y2:
        bottom_left = x1, y1
        top_right = x2, y2
    elif x1 <= x2 and y1 > y2:
        top_left = x1, y1
        bottom_right = x2, y2
        bottom_left = top_left[0], bottom_right[1]
        top_right = bottom_right[0], top_left[1]
    elif x1 > x2 and y1 > y2:
        top_right = x1, y1
        bottom_left = x2, y2
    else:
        bottom_right = x1, y1
        top_left = x2, y2
        bottom_left = top_left[0], bottom_right[1]
        top_right = bottom_right[0], top_left[1]
    return bottom_left, top_right
