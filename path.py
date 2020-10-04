from math import sqrt
from classes import *


def segment_sorting(layers, clearance):
    flip = False

    # iterate over all segments

    for layer in layers:

        for segment in layer.segments_in_layer:

            # this list tracks the location of each point:
            # "a1", "a2", or "limbo"

            point_locations = []

            for point in segment.points:

                if flip == False:
                    # if point is below a1 clearance line

                    if (200 - point.Y_value) < point.X_value + clearance:

                        # if point is below a1 clearance line
                        # AND above a2 clearance line

                        if point.X_value < (200 - point.Y_value + clearance):

                            point_locations.append("limbo")

                        # if point is below a1 clearance line
                        # AND below a2 clearance line

                        else:

                            point_locations.append("a2")

                    # if point is above a1 clearance line

                    else:

                        point_locations.append("a1")
                else:
                    if (point.Y_value) < point.X_value + clearance:

                        # if point is below a1 clearance line
                        # AND above a2 clearance line

                        if point.X_value < (point.Y_value + clearance):

                            point_locations.append("limbo")

                        # if point is below a1 clearance line
                        # AND below a2 clearance line

                        else:

                            point_locations.append("a2")

                    # if point is above a1 clearance line

                    else:

                        point_locations.append("a1")

            # now check the point_locations list to see
            # if any of the points themselves are in limbo

            if "limbo" in point_locations:

                layer.limbo_segments.append(segment)

            # if not, check if a1 occurs in point_locations

            elif "a1" in point_locations:

                # if a2 occurs in point_locations as well as a1

                if "a2" in point_locations:

                    layer.limbo_segments.append(segment)

                # if a2 does not occur in addition to a1

                else:

                    layer.a1_segments.append(segment)

            # if a1 does not occur in the list, and neither does limbo

            else:

                layer.a2_segments.append(segment)

            # add limbo segments to the shorter of the two between a1 and a2

        flip = not (flip)


##        if len(layer.a1_segments) > len(layer.a2_segments):
##            layer.a1_segments = layer.a1_segments + layer.limbo_segments
##        else:
##            layer.a2_segments = layer.a2_segments + layer.limbo_segments


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


# def order_segments(unvisited_segments, home):

#     current_point = home
#     arm_path = [home]

#     while len(unvisited_segments) > 0:
#         i = get_closest_segment(unvisited_segments, current_point)

#         for point in unvisited_segments[i].points:
#             arm_path.append(point)
#         current_point = unvisited_segments[i].points[-1]
#         del unvisited_segments[i]

#     return current_point, arm_path


# def path_gen(layers, home1, home2):

#     a1_path = []
#     a2_path = []
#     a1_last = home1
#     a2_last = home2

#     for layer in layers:

#         a1_segments = layer.a1_segments.copy()
#         a2_segments = layer.a2_segments.copy()
#         limbo_segments = layer.limbo_segments.copy()

#         a1_last, ordered_a1_path = order_segments(a1_segments, a1_last)
#         a2_last, ordered_a2_path = order_segments(a2_segments, a2_last)

#         a1_path += ordered_a1_path
#         a2_path += ordered_a2_path

#         if len(a1_segments) > len(a2_segments):

#             limbo_last, seg_limbo_path = order_segments(limbo_segments, a1_last)
#             a1_path += seg_limbo_path
#             a1_last = limbo_last

#         else:

#             limbo_last, seg_limbo_path = order_segments(limbo_segments, a2_last)
#             a2_path += seg_limbo_path
#             a2_last = limbo_last

#     return a1_path, a2_path


def path_gen_also(segment_list, home):

    unvisited = segment_list.copy()
    path = []
    current_point = home

    while len(unvisited) > 0:
        i = get_closest_segment(unvisited, current_point)

        for point in unvisited[i].points:
            path.append(point)
        current_point = unvisited[i].points[-1]
        del unvisited[i]

    return path


def rlen(item):

    l = 0

    if type(item) == list:

        l = sum(rlen(subitem) for subitem in item)
        return l
    else:
        return 1


def path_gen(layers, home1, home2):

    a1_path = []
    a2_path = []

    for layer in layers:

        a1_path += path_gen_also(layer.a1_segments, home1)
        a2_path += path_gen_also(layer.a2_segments, home2)

        a1len = rlen(layer.a1_segments)
        a2len = rlen(layer.a2_segments)

        if a1len > a2len:  # if there are more a1 segments than a2
            limbo_path = path_gen_also(layer.limbo_segments, a1_path[-1])
            a1_path += limbo_path  # add limbo list to a1

        elif a1len <= a2len:
            limbo_path = path_gen_also(layer.limbo_segments, a2_path[-1])
            a2_path += limbo_path

    return a1_path, a2_path
