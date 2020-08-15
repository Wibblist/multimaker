from math import sqrt
from classes import *


def get_closest_segment(segments_list, current_point):
    return segments_list.index(
        min(
            segments_list,
            key=lambda Segment: sqrt(
                (Segment.points[0].X_value - current_point.X_value) ** 2
                + (Segment.points[0].Y_value - current_point.Y_value) ** 2
            ),
        )
    )


unvisited_segments = seglist
visited_segments = []

a1 = []  # path of arm
current_point = Point(0, 3600, 0, 0, 0, 0)  # start

while len(unvisited_segments) > 0:
    i = get_closest_segment(unvisited_segments, current_point)

    for point in unvisited_segments[i].points:
        a1.append(point)
    current_point = unvisited_segments[i].points[-1]
    visited_segments.append(unvisited_segments[i])
    del unvisited_segments[i]
