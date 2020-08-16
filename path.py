from math import sqrt

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



