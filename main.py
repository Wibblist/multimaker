from classes import *
from path import *
from stripper import *


segments = []
layers = []

extractPointsAndLayers("babycode.txt", layers)

# for layer in layers:

#     layer.print_layer()

for layer in layers:

    layer.extract_segments()
    print("\nnew layer")

    # for segment in layer.segments_in_layer:

    #     print("new segment")
    #     segment.print_segment()


# PART 5 - Segment sorter
clearance = 2  # clearance between arm areas

segment_sorting(layers, clearance)

# PART 6 - Path Generator

home1 = Point(0, 3600, 0, 0, 0, 0)
home2 = Point(0, 3600, 200, 200, 0, 0)

a1 = path_gen(layers, home1, "a1")
a2 = path_gen(layers, home2, "a2")


print("\npath:")

for point in a2:
    point.print_point()
