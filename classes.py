from math import sqrt


class Point:

    # feels so naked without the type ;-;
    G_value = 0
    F_value = 0
    X_value = 0
    Y_value = 0
    Z_value = 0
    E_value = 0

    def __init__(self, G_value, F_value, X_value, Y_value, Z_value, E_value):
        self.G_value = G_value
        self.F_value = F_value
        self.X_value = X_value
        self.Y_value = Y_value
        self.Z_value = Z_value
        self.E_value = E_value

    # print this point

    def print_point(self):

        print(
            str(self.G_value)
            + ", "
            + str(self.F_value)
            + ", "
            + str(self.X_value)
            + ", "
            + str(self.Y_value)
            + ", "
            + str(self.Z_value)
            + ", "
            + str(self.E_value)
        )


class Layer:

    layer_no = 0
    layer_index = 0
    segments_in_layer = []
    a1_segments = []
    a2_segments = []
    limbo_segments = []

    # points: stores all the points
    points = []

    def __init__(self, layer_index, layer_no):

        self.layer_index = layer_index
        self.segments_in_layer = []
        self.points = []
        self.a1_segments = []
        self.a2_segments = []
        self.limbo_segments = []
        self.layer_no = layer_no

    def add_point(self, G_value, F_value, X_value, Y_value, Z_value, E_value):

        self.points.append(Point(G_value, F_value, X_value, Y_value, Z_value, E_value))

    def print_layer(self):

        for point in self.points:

            point.print_point()

        print("end layer")

    # extracts segments

    def extract_segments(self):

        pointsInSegment = []
        ##        i = 1
        ##        previousPoint = self.points[i - 1]
        ##        currentPoint = self.points[i]

        # might need a -1 or +1, will see when I run

        for i, point in enumerate(self.points):

            if i == 0:

                pass

            # is the segment currently empty? in that case, check for a non-zero
            # E value to be the second point. Once that's point, store the
            # previous E value as the beginning of the segment.

            elif len(pointsInSegment) == 0:

                if self.points[i].E_value != 0:

                    pointsInSegment.append(self.points[i - 1])
                    pointsInSegment.append(self.points[i])

            # does the list already have a first and second point?

            else:

                # are there more points?

                if self.points[i].E_value != 0:

                    pointsInSegment.append(self.points[i])

                # if there are no more points in this segment

                else:

                    # segments.append(Segment(pointsInSegment))

                    self.segments_in_layer.append(Segment(pointsInSegment))
                    pointsInSegment = []


##            i += 1
##            previousPoint = self.points[i - 1]
##            currentPoint = self.points[i]


class Segment:

    # stores points

    points = []

    def __init__(self, pointsList):

        self.points = pointsList

    def print_segment(self):

        print("new segment")

        for point in self.points:

            point.print_point()


class Arm:

    path = []
    doneExtruding = False
    i = 0
    origin = [0, 300]
    hypo = 0
    lastPoint = [0, 300]
    printheadPos = [0, 300]
    doneWithLayer = False
    doneWithPath = False
    #currentLayer = 0
    #previousLayer = 0

    def __init__(self, origin):

        self.doneExtruding = False
        self.i = 0
        self.origin = origin
        self.hypo = 0
        self.lastPoint = []
        self.printheadPos = [origin.X_value + 100, origin.Y_value - 100]
        self.path = []
        self.doneWithLayer = False
        self.doneWithPath = False

    
    def getValuesForExtrude(self, speed):

        start = self.path[self.i - 1]
        end = self.path[self.i]

        a1 = sqrt(pow(abs(end.X_value - start.X_value), 2) + pow((abs(end.Y_value - start.Y_value)), 2))

        #print(a1)
        #print("a2: " + str(a2))

        if self.hypo <= a1:

            if (start.X_value != end.X_value):

                x2 = start.X_value +((end.X_value - start.X_value) * ((self.hypo)/a1))

            else:

                x2 = end.X_value


            if (start.Y_value != end.Y_value):

                y2 = start.Y_value +((end.Y_value - start.Y_value) * ((self.hypo)/a1))

            else:

                y2 = end.Y_value


            #print(x2)
            #print(y2)

            self.hypo += speed
            

        elif (self.hypo <= (a1 + speed)):

            x2 = end.X_value
            y2 = end.Y_value

            self.doneExtruding = True

            #print("done")
            
        self.previousPoint = [start.X_value + 100, 300 - start.Y_value]
        self.printheadPos = [x2 + 100, 300 - y2 ]
        

        #print("ran")


