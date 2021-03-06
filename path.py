import math
from classes import *


def segment_sorting(layers, clearance, mode):
    flip = False

    if mode == 1:

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

    elif mode == 2:

        for layer in layers:

            for segment in layer.segments_in_layer:

                # this list tracks the location of each point:
                # "a1", "a2", or "limbo"

                # support_segment = False

                support_points = []

                for point in segment.points:

                    if point.support == True:

                        support_points.append(point)

                ##                if point.support == True:
                ##
                ##                    support_segment = True

                if len(support_points) > 1:

                    layer.a2_segments.append(segment)

                else:

                    layer.a1_segments.append(segment)

    # elif mode == 3:

    #     for layer in layers:

    #         for segment in layer.segments_in_layer:

    #             layer.a1_segments.append(segment)


##        if len(layer.a1_segments) > len(layer.a2_segments):
##            layer.a1_segments = layer.a1_segments + layer.limbo_segments
##        else:
##            layer.a2_segments = layer.a2_segments + layer.limbo_segments


def get_closest_segment(segments_list, current_point):
    return segments_list.index(
        min(
            segments_list,
            key=lambda Segment: math.sqrt(
                (Segment.points[0].X_value - current_point.X_value) ** 2
                + (Segment.points[0].Y_value - current_point.Y_value) ** 2
            ),
        )
    )


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

    return current_point, path


def path_gen(layers, home1, home2, mode):

    a1_path = []
    a2_path = []
    a1_last = home1
    a2_last = home2

    for layer in layers:

        if mode == 1 or mode == 2:
            a1_last, ordered_a1 = path_gen_also(layer.a1_segments, home1)
            a2_last, ordered_a2 = path_gen_also(layer.a2_segments, home2)

            a1_path += ordered_a1
            a2_path += ordered_a2

            if len(ordered_a1) > len(
                ordered_a2
            ):  # if there are more a1 segments than a2
                limbo_path = path_gen_also(layer.limbo_segments, a1_last)[1]
                a1_path += limbo_path  # add limbo list to a1

            elif len(ordered_a1) <= len(ordered_a2):
                limbo_path = path_gen_also(layer.limbo_segments, a2_last)[1]
                a2_path += limbo_path

        elif mode == 3:

            for point in layer.points:

                a1_path.append(point)

    return a1_path, a2_path


def calcAngle(reqcos):
    res = math.atan2(math.sqrt(1 - math.pow(reqcos, 2)), reqcos)
    return res


def IKine(X, Y):
    px = X
    py = Y
    l1 = 141  # link 1 length
    l2 = 141  # link 2 length

    ctheta2 = (px ** 2 + py ** 2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2)
    stheta2 = math.sqrt(1 - math.pow(ctheta2, 2))
    ctheta1 = (px * (l1 + l2 * ctheta2) + py * l2 * stheta2) / (px ** 2 + py ** 2)

    theta1 = calcAngle(ctheta1)  # elbow down
    theta2 = calcAngle(ctheta2)

    return math.degrees(theta1), math.degrees(theta2)
