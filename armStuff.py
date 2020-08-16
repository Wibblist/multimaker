
all_layer_segments = []
a1_segments = []
a2_segments = []
limbo_segments = []

clearance = 2

#iterate over all segments

for segments in all_layer_segments:

    #this list tracks the location of each point:
    #"a1", "a2", or "limbo"
    
    point_locations = []

    for point in segments.point:

        #if point is below a1 clearance line

        if (Point.Y_value < Point.X_value + clearance):

            #if point is below a1 clearance line
            #AND above a2 clearance line

            if (Point.X_value < Point.Y_value + clearance):

                point_locations.append("limbo")

            #if point is below a1 clearance line
            #AND below a2 clearance line

            else:

                point_locations.append("a2")

        #if point is above a1 clearance line

        else:

            point_locations.append("a1")
            

    #now check the point_locations list to see
    #if any of the points themselves are in limbo

    if "limbo" in point_locations:

        limbo_segments.append(segment)


    #if not, check if a1 occurs in point_locations   

    elif "a1" in point_locations:

        #if a2 occurs in point_locations as well as a1

        if "a2" in point_locations:

            limbo_segments.append(segment)

        #if a2 does not occur in addition to a1

        else:

            a1_segments.append(segment)

    #if a1 does not occur in the list, and neither does limbo
    
    else:

        a2_segments.append(segment)


    #remove segment from all_layer_segments

    all_layer_segments.remove(segment)
    

                    

                    
            
            

            

    
