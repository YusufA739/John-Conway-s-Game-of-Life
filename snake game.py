#imports of scripts and libs (*section 0*)

import time,pygame,random
from pygame import mixer

import random,sys,time,os,copy
from colorama import Fore, Back, Style

#function declarations (*section 1*)

#won't automatically wipe frame (when using text renderer, via commenting and uncommenting -> fix this!)
#as we allow user to have finer control over when they want it cleared
#tradeoff between finer control and less controls is more vs less complexity, respectively
def drawframe(imageData,lrtGiven=None,crtGiven=None,frtGiven=None,lpfGiven=None,cplGiven=None):
    global cellresttime, lineresttime, frameresttime, linesperframe, cellsperline
    if lrtGiven is None:
        lrtGiven = lineresttime
    if crtGiven is None:
        crtGiven = cellresttime
    if frtGiven is None:
        frtGiven = frameresttime
    if lpfGiven is None:
        lpfGiven = linesperframe
    if cplGiven is None:
        cplGiven = cellsperline
    # display next frame data
    for line in range(lpfGiven):
        for cell in range(cplGiven):
            if int(imageData[line][cell]) <= 0:
                # sys.stdout.write(Fore.BLACK + str(imageData[line][cell]))
                # sys.stdout.write(Fore.BLACK + "0")
                pygame.draw.rect(game_window, black, pygame.Rect(cell*10, line*10, 10, 10))
            else:
                # sys.stdout.write(Fore.WHITE + str(imageData[line][cell]))
                # sys.stdout.write(Fore.WHITE + "0")
                pygame.draw.rect(game_window, white, pygame.Rect(cell*10, line*10, 10, 10))
            time.sleep(crtGiven)#sleep for cell
        # sys.stdout.write("\n")

        time.sleep(lrtGiven)#sleep for line
    time.sleep(frtGiven)#sleep for frame

def clearframe():
    os.system("cls")

def remove1D(list1, target):#removes target elem, in a given 1D list/array
    new_list = []
    for carrier in list1:
        if carrier == target:
            pass
        else:
            new_list.append(carrier)
    return new_list

def removeDuplicateElements(list1):
    return list(dict.fromkeys(list1))

def deepCopy(list1):
    return copy.deepcopy(list1)

def logic(frameData,lpf,cpl):
    global linesperframe, cellsperline

    if lpf is None:
        lpf = linesperframe
    if cpl is None:
        cpl = cellsperline

    new_frameData = copy.deepcopy(frameData)

    for i in range(lpf):
        for j in range(cpl):
            deactivateTop = False  # no negative i so no i-1
            deactivateBottom = False  # no checking i+1
            deactivateLeft = False  # no checking j-1
            deactivateRight = False  # no checking j+1
            NeighbourCount = 0
            # if i == 0:
            #     if j == 0:
            #         NeighbourCount += livelinessGrid[i + 1][j]
            #         NeighbourCount += livelinessGrid[i + 1][j + 1]
            #         NeighbourCount += livelinessGrid[i + 1][j + 1]
            #     elif j > 0:
            #         NeighbourCount += livelinessGrid[i][j - 1]
            #         NeighbourCount += livelinessGrid[i + 1][j - 1]
            #         NeighbourCount += livelinessGrid[i + 1][j]
            #         NeighbourCount += livelinessGrid[i + 1][j + 1]
            #         NeighbourCount += livelinessGrid[i][j + 1]
            # didnt bother completing as ive simplified the redundancy between neighbour checking below

            if i == 0:
                deactivateTop = True
            if i == lpf - 1:
                deactivateBottom = True
            if j == 0:
                deactivateLeft = True
            if j == cpl - 1:
                deactivateRight = True

            if deactivateLeft == False:
                NeighbourCount += frameData[i][j - 1]
            if deactivateBottom == False and deactivateLeft == False:
                NeighbourCount += frameData[i + 1][j - 1]
            if deactivateBottom == False:
                NeighbourCount += frameData[i + 1][j]
            if deactivateBottom == False and deactivateRight == False:
                NeighbourCount += frameData[i + 1][j + 1]
            if deactivateRight == False:
                NeighbourCount += frameData[i][j + 1]
            if deactivateTop == False and deactivateRight == False:
                NeighbourCount += frameData[i - 1][j + 1]
            if deactivateTop == False:
                NeighbourCount += frameData[i - 1][j]
            if deactivateTop == False and deactivateLeft == False:
                NeighbourCount += frameData[i - 1][j - 1]

            #could be further optimised to only do checks on statements that are actually needed to be run
            #The Sieve of Eratosthenes was developed by the Greek mathematician Eratosthenes of Cyrene around 240 BCE.
            # Eratosthenes was a polymath, excelling in mathematics, astronomy, geography, and poetry, and is also
            # famous for calculating the Earth's circumference. The sieve is one of his notable contributions to number
            # theory, providing a systematic method to identify prime numbers

            if NeighbourCount < 2:
                new_frameData[i][j] = 0
            elif (NeighbourCount == 2 or NeighbourCount == 3) and frameData[i][j] == 1:  # can stay alive as it has
                # 2 or 3 neighbours
                new_frameData[i][j] = 1
            elif NeighbourCount == 3 and frameData[i][j] == 0:  # needs exactly 3 neighbours to be born
                new_frameData[i][j] = 1
            elif NeighbourCount > 3:  # >= 4 for accuracy to Conway's description of the rules on numberphile
                new_frameData[i][j] = 0

    return new_frameData

def rainlogic(currentframelengthofraindrop,linesperframe,cellsperline,lowestraindropnumber,highestraindropnumber,lowestvalue,stopvalue,highestvalue):
    # calculate the next frame's data (changes impacting frame: new line added at top, deletion at bottom)
    nextline = ""
    lengthofraindropNextLine = deepCopy(currentframelengthofraindrop[0])
    for i in range(cellsperline):#same as len(lengthofraindropNextLine)
        if lengthofraindropNextLine[i] > stopvalue:
            if highestraindropnumber > lowestraindropnumber:
                nextline += str(random.randint(lowestraindropnumber, highestraindropnumber))# change to (0,1) for binary
                lengthofraindropNextLine[i] -= 1
            else:
                nextline += str(lowestraindropnumber)
                lengthofraindropNextLine[i] -= 1
        elif lengthofraindropNextLine[i] <= lowestvalue:
            if highestraindropnumber > lowestraindropnumber:
                nextline += str(random.randint(lowestraindropnumber, highestraindropnumber))# change to (0,1) for binary
                lengthofraindropNextLine[i] = random.randint(stopvalue, highestvalue)
            else:
                nextline += str(lowestraindropnumber)
                lengthofraindropNextLine[i] = random.randint(stopvalue, highestvalue)
        else:
            nextline += str(lowestraindropnumber)
            lengthofraindropNextLine[i] -= 1

    # update future frame with new information
    for carrier in range(linesperframe - 1, 0, -1):
        # update all unaltered lines down, skipping overwriting the first, so line 1 and 2 will be identical for now,
        # and also not rewriting the last line to another line
        currentframelengthofraindrop[carrier] = currentframelengthofraindrop[carrier - 1].copy()

    # finally, update the next frame's first line
    currentframelengthofraindrop[0] = lengthofraindropNextLine.copy()
    # tracks droplength remaining to generate. Tells us when the raindrop has reached zero length.
    # Once zero length, we wait until it goes past a certain negative
    # negative acts like the reverse of a drop. So just black bg/a gap.
    # Once we hit the negative floor, we choose a random positive int to make a new droplet


    return currentframelengthofraindrop


#variable declaration (*section 2*)

#change these to change frame size
linesperframe = 50#55x209 for fullscreen command prompt for my pc
cellsperline = 100
# linesperframe = int(input("type in your height:"))
# cellsperline = len(input("use this to calibrate your width and paste the line length:"))

grid = []#used to keep all pixels zero
livelinessGrid = []
new_livelinessGrid = []#can be removed, and then overwrite in-place the new pixel data to the current storage using ->
# livelinessGrid = deepCopy(logic(x,y,z)), to prevent any issues with byref data

#helper arrays (for building our 2D array grids, for tracking pixel data between frames)
gridlines = []#for building grid only (see below in for loops)
livelines = []#for building grid only (see below in for loops)

nextline = ""
currentframe = []
currentframelengthofraindrop = []
lengthofraindropNextLine = []

# change these to alter the length of raindrops and the length in between new raindrops in the same column
lowestvalue = -1000  # increasing the spacing between raindrops in the same column
stopvalue = 0  # value to signify the "stop" length of a raindrop, within lowest value and highest value range
highestvalue = 10  # max len of raindrops

# change these to change what numbers appear in the raindrops
lowestraindropnumber = 5
highestraindropnumber = 5


#code moved from lower sections to better match section labelling

#change to alter line rest time and frame rest time (in seconds)
cellresttime = 0
lineresttime = 0
frameresttime = 0

#target framerate
targetFramerate = 144
currentFramerate = 0

frameCount = 0
# file = open("framerate.txt", "w")#there seems to be a time limit on file opening. will investigate and temp patch
start = time.perf_counter()#for inital measurement, will be wrong until it updates in if statement
# (reduces frame delays due to extra timer processing)

#assigment of vars used for logic checks
deactivateTop = False # no negative i so no i-1
deactivateBottom = False# no checking i+1
deactivateLeft = False# no checking j-1
deactivateRight = False#no checking j+1


#unused so far (from old raindrops code)
#change these to change what numbers appear in the raindrops
lowestraindropnumber = 0
highestraindropnumber = 9
if highestraindropnumber > lowestraindropnumber:
    highestraindropnumber = lowestraindropnumber



#manual checks to see if code is working

# livelinessGrid[6][8] = 12
# livelinessGrid[7][7] = 1
#
# livelinessGrid[7][8] = 1
#
# livelinessGrid[7][9] = 1
# livelinessGrid[8][7] = 1
# # livelinessGrid[8][8] = 1
# livelinessGrid[8][9] = 1
# livelinessGrid[9][8] = 1
# # livelinessGrid[9][8] = 1
# # livelinessGrid[9][9] = 1





# Import data and create grid frame for rendering (*section 3*)

# import data and adjust grid frame for Conway-Based variables (*section 3.1*)

# Import data

try:#if file found, load the data from it into memory (program/user space, i think)
    with open("initialState.txt", "r") as file:
        information = file.readlines()

        cellsperline = 0
        maxLens = []
        for carrier in range(len(information)):
            currentCellsperline = len(remove1D(information[carrier], "\n"))#not assigned outside, will go out of
            #scope and be destroyed
            if cellsperline < currentCellsperline:
                cellsperline = currentCellsperline
        linesperframe = len(information)
        # cellsperline = len(remove1D(information[0],"\n"))

        for line in information:
            for cell in line:
                isint = False
                try:
                    int(cell)
                    isint = True
                except:
                    isint=False

                # if cell != "\n":
                if isint == True:
                    livelines.append(int(cell))
                #no need for elif, as it will just not run the if, if there is a linebreak char (now modified for any
                #non-convertable string to int string char
            if len(livelines) != cellsperline:
                for carrier in range(cellsperline - len(livelines)):
                    livelines.append(0)#pad it out extra, otherwise we will get errors when it tries to render a pixel
                    #that doesn't exist
                    #next improvement: try to make padding out even (so, we pad on the left and right side
            livelinessGrid.append(deepCopy(livelines))
            livelines = []

except:#create the file instead, if not found
    with open("initialState.txt", "a") as file:
        stringDataExport = ""
        for line in range(linesperframe):
            for cell in range(cellsperline):
                livelines.append(random.randint(0,1))
                stringDataExport += str(livelines[len(livelines)-1])
            file.write(stringDataExport + "\n")
            livelinessGrid.append(copy.deepcopy(livelines))
            livelines = []
            stringDataExport = ""
        file.close()


# create grid frame for other variables (*section 3.2*)

# make the first line
for placeholder in range(cellsperline):  # cells per line is given by user input
    lengthofraindropNextLine.append(random.randint(lowestvalue, highestvalue))
    nextline += str(random.randint(lowestraindropnumber, highestraindropnumber))
    gridlines.append(0)
    # we need this to know initial raindrop lengths and placements

# make the first frame using the first line
for i in range(linesperframe):
    currentframe.append(nextline)# every line starts out the same singular line copied out
    currentframelengthofraindrop.append(deepCopy(lengthofraindropNextLine))
    # only the first line is necessary, but I will leave for now

for carrier in range(linesperframe):
    grid.append(copy.deepcopy(gridlines))



# pygame code (*section 4*)

#variable assignment does take place here, but it looks more logically sound to keep it in this section as it matches
#the heading better
#window size
window_x = cellsperline * 10
window_y = linesperframe * 10

mixer.init()
mixer.music.set_volume(1)
mixer.Sound("Ilmari Hakkola - Bad Piggies Theme.mp3").play(-1)


#colors
black=pygame.Color(0,0,0) # capital C for pygame.Color(0,0,0)
white=pygame.Color(255,255,255)
red=pygame.Color(255,0,0)
green=pygame.Color(0,255,0)
blue=pygame.Color(0,0,255)

#initialising pygame
pygame.init()

#init game window
pygame.display.set_caption("John Conway's Game of Life: Python Edition (PyGame)")
game_window=pygame.display.set_mode((window_x, window_y))

#FPS (frames per second) controller
fps=pygame.time.Clock()



# Main Function
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    # new_livelinessGrid = logic(livelinessGrid,linesperframe,cellsperline)
    currentframelengthofraindrop = rainlogic(currentframelengthofraindrop,linesperframe,cellsperline,lowestraindropnumber,highestraindropnumber,lowestvalue,stopvalue,highestvalue)
    drawframe(currentframelengthofraindrop,lineresttime,cellresttime,frameresttime,linesperframe,cellsperline)

    # draw frame using data. Note: linesperframe is basically how many y then cellsperline is how many x
    # drawframe(new_livelinessGrid, cellresttime, lineresttime, frameresttime, linesperframe, cellsperline)

    #clearframe()  # this needs to be the last operation so that more time is spent as displaying vs more time spent showing blank screen
    # frame is over and wiped the screen for the next frame's preparation

    # end = time.perf_counter()#if only 1 frame
    # all of nextline and future frame calculations have been done. Track framerate now (overhead from file.write could be added, but it won't be for now)

    # livelinessGrid = copy.deepcopy(new_livelinessGrid)

    frameCount += 1

    if frameCount % targetFramerate == 0:
        end = time.perf_counter()
        delta = end - start
        deltaPerFrameArithmeticAverage = delta / frameCount
        file.write(
            "Target: " + str(targetFramerate) + "\n" + "Actual: " + str(1 / deltaPerFrameArithmeticAverage) + "\n")
        file.flush()  # will force the buffer to write to file so that if the program is closed without closing file, it will still save the last result
        start = time.perf_counter()
     
    # Refresh game screen
    pygame.display.update()
 
    # Frame Per Second /Refresh Rate
    fps.tick(60)



