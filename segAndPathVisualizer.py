import pygame, sys
from classes import *
from path import *
from stripper import *

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont("Arial", 20)


width = 400
height = 400
gameDisplay = pygame.display.set_mode((width, height))
fpsClock = pygame.time.Clock()

origin = [0, 300]

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
darkblue = (160, 160, 255)
red = (255, 0, 0)
darkred = (255, 160, 160)
green = (0, 255, 0)

ticks = 0

seconds = 0
minutes = 0
hours = 0

currentLayer = 0
previousLayer = 0
offset = 0

donePrinting = False


# this belong here?

####


def getCurrentLayer():

    global currentLayer

    if (len(a1.path) > 1) and (len(a2.path) > 1):

        if not ((a1.i == len(a1.path)) or (a2.i == len(a2.path))):

            currentLayer = min(a1.path[a1.i].Z_value, a2.path[a2.i].Z_value)

        elif a1.i == len(a1.path):

            currentLayer = a2.path[a2.i].Z_value

        elif a2.i == len(a2.path):

            currentLayer = a1.path[a1.i].Z_value

    elif len(a1.path) == 1:

        currentLayer = a2.path[a2.i].Z_value

    elif len(a2.path) == 1:

        currentLayer = a1.path[a1.i].Z_value


def drawModel(arm):

    global speed

    if arm == a1:

        materialColor = darkred
        printheadColor = red

    elif arm == a2:

        materialColor = darkblue
        printheadColor = blue

    if arm.i == 0:

        arm.i += 1

    elif arm.i < len(arm.path):

        if arm.path[arm.i].Z_value == currentLayer:

            if arm.doneExtruding == True:

                arm.hypo = 0
                arm.doneExtruding = False
                arm.i += 1

            elif arm.doneExtruding == False:

                arm.Extrude(speed)

                if arm.path[arm.i].E_value != 0:

                    pygame.draw.aaline(
                        gameDisplay, materialColor, arm.previousPoint, arm.printheadPos
                    )

        else:

            arm.doneWithLayer = True

    else:

        arm.doneWithLayer = True

    for j, point in enumerate(arm.path):

        if (j < arm.i) and (arm.path[j].E_value != 0):

            if arm.path[j].Z_value == currentLayer:

                pygame.draw.aaline(
                    gameDisplay,
                    materialColor,
                    [arm.path[j - 1].X_value + 100, 300 - arm.path[j - 1].Y_value],
                    [arm.path[j].X_value + 100, 300 - arm.path[j].Y_value],
                )

            elif (arm.doneWithLayer == True) and (arm.path[j].Z_value == previousLayer):

                pygame.draw.aaline(
                    gameDisplay,
                    materialColor,
                    [arm.path[j - 1].X_value + 100, 300 - arm.path[j - 1].Y_value],
                    [arm.path[j].X_value + 100, 300 - arm.path[j].Y_value],
                )


segments = []
layers = []

file_to_print = "m2.gcode"
scale = 1
offset = 0
framerate = 240

# file_to_print = input("Which file should be used?\n")
# scale = int(input("What is the scale?\n"))
# offset = int(input("What is the offset?\n"))


# #speed = int(input("What is the speed?\n"))
# framerate = int(input("What is the frame rate?\n"))

speed = 10


extractPointsAndLayers(file_to_print, layers, int(scale), int(offset))

# for layer in layers:

#     layer.print_layer()

for layer in layers:

    layer.extract_segments()
##    print("\nnew layer")

# for segment in layer.segments_in_layer:

#     print("new segment")
#     segment.print_segment()


# PART 5 - Segment sorter
clearance = 2  # clearance between arm areas

segment_sorting(layers, clearance)

# PART 6 - Path Generator

home1 = Point(0, 3600, 0, 0, 0, 0)
home2 = Point(0, 3600, 200, 200, 0, 0)

##print("\na1 points:")
##
##for segment in layers[0].a1_segments:
##    segment.print_segment()
##
##    print("\na2 points:")
##
##for segment in layers[0].a2_segments:
##    segment.print_segment()
##
##print("\nlimbo")
##
##for segment in layers[0].limbo_segments:
##    segment.print_segment()

a1 = Arm(home1)
a2 = Arm(home2)


a1.path = path_gen(layers, home1, "a1")
a2.path = path_gen(layers, home2, "a2")

f = open("export.txt", "w+")
for point in a1.path:
    output = (
        "G"
        + str(point.G_value)
        + " F"
        + str(round(point.F_value, 3))
        + " X"
        + str(round(point.X_value, 3))
        + " Y"
        + str(round(point.Y_value, 3))
        + " Z"
        + str(round(point.Z_value, 1))
        + " E"
        + str(round(point.E_value, 5))
        + "\n"
    )
    f.write(output)
f.close()

##print("\na1 path")
##
##for point in a1.path:
##
##    point.print_point()
##
##print("\na2 path")
##
##for point in a2.path:
##
##    point.print_point()

if (len(a1.path) > 1) and (len(a2.path) > 1):

    currentLayer = min(a1.path[1].Z_value, a2.path[1].Z_value)

elif len(a1.path) == 1:

    currentLayer = a2.path[a2.i].Z_value

elif len(a2.path) == 1:

    currentLayer = a1.path[a1.i].Z_value

###

while True:

    gameDisplay.fill(white)

    game_window = pygame.draw.rect(
        gameDisplay, black, ((width // 2) - 100, (height // 2) - 100, 200, 200)
    )

    # pygame.draw.aaline(gameDisplay, blue, [100, 100], [300, 300])

    ##    drawSegments(0, "a1")
    ##    drawSegments(0, "a2")
    ##    drawSegments(0, "limbo")

    if donePrinting == False:

        getCurrentLayer()

    if len(a1.path) > 1:

        drawModel(a1)

    else:

        a1.doneWithLayer = True
        a1.i = 1

    if len(a2.path) > 1:

        drawModel(a2)

    else:

        a2.doneWithLayer = True
        a2.i = 1

    pygame.draw.circle(
        gameDisplay, red, [int(a1.printheadPos[0]), int(a1.printheadPos[1])], 3
    )
    pygame.draw.circle(
        gameDisplay, blue, [int(a2.printheadPos[0]), int(a2.printheadPos[1])], 3
    )

    if (a1.doneWithLayer == True) and (a2.doneWithLayer == True):

        a1.doneWithLayer = False
        a2.doneWithLayer = False

        # print("ran")

    if (a1.i == len(a1.path)) and (a2.i == len(a2.path)):

        donePrinting = True

    elif a1.i == len(a1.path):

        a1.doneWithLayer = True

    elif a2.i == len(a2.path):

        a2.doneWithLayer = True

    if donePrinting == False:

        ticks += 1

        seconds = ticks // framerate

        seconds = seconds % (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

    textsurface = myfont.render(str(hours), True, black)
    text_rect = textsurface.get_rect(center=(200, 30))
    gameDisplay.blit(textsurface, text_rect)

    textsurface = myfont.render(str(minutes), True, black)
    text_rect = textsurface.get_rect(center=(200, 50))
    gameDisplay.blit(textsurface, text_rect)

    textsurface = myfont.render(str(seconds), True, black)
    text_rect = textsurface.get_rect(center=(200, 70))
    gameDisplay.blit(textsurface, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(framerate)
