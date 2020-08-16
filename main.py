from classes import *
from path import *
from stripper import *


segments = []
layers = []

extractPointsAndLayers("babycode.txt", layers)

for layer in layers:

    layer.print_layer()

for layer in layers:

    layer.extract_segments()
    print("\nnew layer")

    for segment in layer.segments_in_layer:

        print("new segment")
        segment.print_segment()

# PART 5

unvisited_segments = layers[0].segments_in_layer

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


# END PART 5

print("\npath:")

for thing in a1:

    thing.print_point()
