from math import sqrt


class Point:  # Each line of gcode is a point
    def __init__(self, G_value, F_value, X_value, Y_value, Z_value, E_value):
        self.G_value = G_value
        self.F_value = F_value
        self.X_value = X_value
        self.Y_value = Y_value
        self.Z_value = Z_value
        self.E_value = E_value

    # debugging
    # def print_point(self):

    #     print(
    #         str(self.G_value)
    #         + ", "
    #         + str(self.F_value)
    #         + ", "
    #         + str(self.X_value)
    #         + ", "
    #         + str(self.Y_value)
    #         + ", "
    #         + str(self.Z_value)
    #         + ", "
    #         + str(self.E_value)
    #     )


class Segment:  # a Segment is a list of points connected by extrusion
    def __init__(self, pointsList):

        self.points = pointsList

    # debugging
    # def print_segment(self):

    #     print("new segment")

    #     for point in self.points:

    #         point.print_point()


class Layer:  # contains every point and segment
    def __init__(self, layer_index, layer_no):

        self.layer_index = layer_index  # index of layer in the layer list
        self.segments_in_layer = []
        self.points = []
        self.a1_segments = []
        self.a2_segments = []
        self.limbo_segments = []
        self.layer_no = layer_no

    # add point to all points list
    def add_point(self, G_value, F_value, X_value, Y_value, Z_value, E_value):

        self.points.append(Point(G_value, F_value, X_value, Y_value, Z_value, E_value))

    # debugging
    # def print_layer(self):

    #     for point in self.points:

    #         point.print_point()

    #     print("end layer")

    def extract_segments(self):  # extracts segments from all points list

        pointsInSegment = []

        for i, point in enumerate(self.points):

            if self.points[i].E_value > 0:

                if len(pointsInSegment) == 0:

                    pointsInSegment.append(self.points[i - 1])

                pointsInSegment.append(self.points[i])

                if i == (len(self.points) - 1):

                    self.segments_in_layer.append(Segment(pointsInSegment))

            elif len(pointsInSegment) > 0:

                self.segments_in_layer.append(Segment(pointsInSegment))
                pointsInSegment = []


class Arm:
    def __init__(self, origin):

        self.doneExtruding = False  # arm done printing for layer?
        self.i = 0
        self.origin = origin  # where printhead starts
        self.hypo = 0  #
        self.printheadPos = [origin.X_value + 100, origin.Y_value - 100]  #
        self.path = []
        self.doneWithLayer = False  #

    def Extrude(self, speed):

        start = self.path[self.i - 1]
        end = self.path[self.i]

        a1 = sqrt(
            pow(abs(end.X_value - start.X_value), 2)
            + pow((abs(end.Y_value - start.Y_value)), 2)
        )

        if self.hypo <= a1:

            if start.X_value != end.X_value:

                x2 = start.X_value + (
                    (end.X_value - start.X_value) * ((self.hypo) / a1)
                )

            else:

                x2 = end.X_value

            if start.Y_value != end.Y_value:

                y2 = start.Y_value + (
                    (end.Y_value - start.Y_value) * ((self.hypo) / a1)
                )

            else:

                y2 = end.Y_value

            self.hypo += speed

        elif self.hypo <= (a1 + speed):

            x2 = end.X_value
            y2 = end.Y_value

            self.doneExtruding = True

        self.previousPoint = [start.X_value + 100, 300 - start.Y_value]
        self.printheadPos = [x2 + 100, 300 - y2]

