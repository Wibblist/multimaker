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


def path_gen(layers, home, arm):

    # NEW POSITION OF
    arm_path = [home]

    for layer in layers:

        limbo_segments = []
        shorter_path = False

        if arm == "a1":
            unvisited_segments = layer.a1_segments.copy()

            if len(layer.a1_segments) > len(layer.a2_segments):

                limbo_segments = layer.limbo_segments.copy()

            else:

                shorter_path = True

        elif arm == "a2":
            unvisited_segments = layer.a2_segments.copy()

            if len(layer.a1_segments) <= len(layer.a2_segments):

                limbo_segments = layer.limbo_segments.copy()

            else:

                shorter_path = True

        elif arm == "limbo":
            unvisited_segments = layer.limbo_segments.copy()

        visited_segments = []

        # ORIGINAL POSITION OF
        # arm_path = []

        # path of arm
        current_point = home  # start

        while len(unvisited_segments) > 0:
            i = get_closest_segment(unvisited_segments, current_point)

            for point in unvisited_segments[i].points:
                arm_path.append(point)
            current_point = unvisited_segments[i].points[-1]
            # visited_segments.append(unvisited_segments[i])
            del unvisited_segments[i]

        while len(limbo_segments) > 0:
            i = get_closest_segment(limbo_segments, current_point)

            for point in limbo_segments[i].points:
                arm_path.append(point)
            current_point = limbo_segments[i].points[-1]
            # visited_segments.append(unvisited_segments[i])
            del limbo_segments[i]

        if shorter_path == True:

            arm_path.append(
                Point(
                    home.G_value,
                    home.F_value,
                    home.X_value,
                    home.Y_value,
                    layer.layer_no,
                    home.E_value,
                )
            )

    return arm_path
