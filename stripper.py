from classes import *
import re


def stripFile(path):
    pattern = re.compile(r"M107")
    comment_pattern = re.compile(r";.*\n")

    with open(path, "r") as f:  # open file in read mode

        contents = f.read()
        matches = pattern.finditer(contents)

        start2end = []

        for match in matches:
            start2end.append(match.span())

    snipped_code = contents[start2end[0][1] + 1 : start2end[1][0] - 1]

    while comment_pattern.search(snipped_code) is not None:
        comment = comment_pattern.search(snipped_code).span()
        cstart = comment[0]
        cstop = comment[1]
        if len(snipped_code) > cstop:
            snipped_code = snipped_code[0:cstart:] + snipped_code[cstop::]

    return snipped_code


def extractPointsAndLayers(path):

    
    global layers

    lines = []

    stripped_file = stripFile(path)

    matches = re.findall(r"(.*)\n", stripped_file, re.MULTILINE)

    for line in matches:

        lines.append(line)


    layer_index = -1
    current_Z_value = -696969

    #please the above be improbable

    G_value = 0
    F_value = 0
    X_value = 0
    Y_value = 0
    Z_value = 0
    E_value = 0

    for line in lines:

        patternG = re.compile(r"G([0-9.]+)(\s|$)")
        matches = patternG.search(line)

        if matches != None:
            G_value = int(matches.group(1))

        else:
            G_value = 0

        patternF = re.compile(r"F([0-9.]+)(\s|$)")
        matches = patternF.search(line)

        if matches != None:
            F_value = float(matches.group(1))

        patternX = re.compile(r"X([0-9.]+)(\s|$)")
        matches = patternX.search(line)

        if matches != None:
            X_value = float(matches.group(1))

        patternY = re.compile(r"Y([0-9.]+)(\s|$)")
        matches = patternY.search(line)

        if matches != None:
            Y_value = float(matches.group(1))

        patternZ = re.compile(r"Z([0-9.]+)(\s|$)")
        matches = patternZ.search(line)

        if matches != None:
            Z_value = float(matches.group(1))

        patternE = re.compile(r"E([0-9.]+)(\s|$)")
        matches = patternE.search(line)

        if matches != None:
            E_value = float(matches.group(1))

        else:
            E_value = 0


        if (Z_value != current_Z_value):

            current_Z_value = Z_value
            layer_index += 1
            layers.append(Layer(layer_index))
        
        layers[layer_index].add_point(
                G_value, F_value, X_value, Y_value, Z_value, E_value
            )


  
segments = []
layers = []

extractPointsAndLayers("babycode.txt")

for layer in layers:

    layer.print_layer()

for layer in layers:

    layer.extract_segments()

    for segment in layer.segments_in_layer:

        print("new segment")
        segment.print_segment()
    




##TESTING SEGMENTS

##layers.append(Layer(0))
##
##layers[0].add_point(0, 0, 1, 2, 1, 0)
##layers[0].add_point(0, 0, 3, 4, 1, 1)
##layers[0].add_point(0, 0, 5, 6, 1, 0)
##layers[0].add_point(0, 0, 7, 8, 1, 1)
##layers[0].add_point(0, 0, 9, 10, 1, 0)
##layers[0].add_point(0, 0, 1, 2, 1, 0)
##layers[0].add_point(0, 0, 3, 4, 1, 1)
##layers[0].add_point(0, 0, 5, 6, 1, 0)
##layers[0].add_point(0, 0, 7, 8, 1, 1)
##layers[0].add_point(0, 0, 9, 10, 1, 0)
##
##
##layers[0].print_layer()
##
##layers[0].extract_segments()
##
##for segment in layers[0].segments_in_layer:
##
##    print("new segment")
##    segment.print_segment()



