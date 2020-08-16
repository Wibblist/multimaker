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

    # layer_no is redundant since we're calculating from Z value
    layer_index = 0
    segments_in_layer = []

    # points: stores all the points
    points = []

    def __init__(self, layer_index):

        self.layer_index = layer_index
        self.segments_in_layer = []
        self.points = []

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

        #might need a -1 or +1, will see when I run

        for i, point in enumerate(self.points):

            if (i == 0):

                pass

            #is the segment currently empty? in that case, check for a non-zero
            #E value to be the second point. Once that's point, store the
            #previous E value as the beginning of the segment.
            
            elif len(pointsInSegment) == 0:

                if (self.points[i].E_value != 0):

                    pointsInSegment.append(self.points[i - 1])
                    pointsInSegment.append(self.points[i])

            #does the list already have a first and second point?
            
            else:

                #are there more points?

                if (self.points[i].E_value != 0):

                    pointsInSegment.append(self.points[i])


                #if there are no more points in this segment

                else:

                    #segments.append(Segment(pointsInSegment))
                    
                    self.segments_in_layer.append(Segment(pointsInSegment))
                    pointsInSegment = []
                    
##            i += 1
##            previousPoint = self.points[i - 1]
##            currentPoint = self.points[i]
            

class Segment:

    #stores points

    points = []


    def __init__(self, pointsList):

        self.points = pointsList


    def print_segment(self):

        for point in self.points:

            point.print_point()



















