import random,sys,time,os,copy
from colorama import Fore, Back, Style


#change these to change frame size
linesperframe = 30#55x209 for fullscreen command prompt for my pc
cellsperline = 30
# linesperframe = int(input("type in your height:"))
# cellsperline = len(input("use this to calibrate your width and paste the line length:"))

grid = []
livelinessGrid = []
new_livelinessGrid = []
gridlines = []#for building grid only (see below in for loops)

for carrier in range(cellsperline):
    gridlines.append(0)

for carrier in range(linesperframe):
    grid.append(copy.deepcopy(gridlines))
    livelinessGrid.append(copy.deepcopy(gridlines))

livelinessGrid[6][8] = 1
livelinessGrid[7][7] = 1

livelinessGrid[7][8] = 1

livelinessGrid[7][9] = 1
livelinessGrid[8][7] = 1
# livelinessGrid[8][8] = 1
livelinessGrid[8][9] = 1
livelinessGrid[9][8] = 1
# livelinessGrid[9][8] = 1
# livelinessGrid[9][9] = 1

#change to alter line rest time and frame rest time (in seconds)
lineresttime = 0
frameresttime = 1

targetFramerate = 40
currentFramerate = 0

frameCount = 0
file = open("framerate.txt", "w")
start = time.perf_counter()#for inital measurement, will be wrong until it updates in if statement (reduces frame delays due to extra timer processing)

deactivateTop = False # no negative i so no i-1
deactivateBottom = False# no checking i+1
deactivateLeft = False# no checking j-1
deactivateRight = False#no checking j+1

def drawframe(new_livelinessGrid,lineresttime,frameresttime):
    global linesperframe, cellsperline
    # display next frame data
    for line in range(linesperframe):
        for cell in range(cellsperline):
            if new_livelinessGrid[line][cell] == 0:
                sys.stdout.write(Fore.BLACK + str(new_livelinessGrid[line][cell]))
            else:
                sys.stdout.write(Fore.WHITE + str(new_livelinessGrid[line][cell]))
        sys.stdout.write("\n")
        time.sleep(lineresttime)
    time.sleep(frameresttime)

#unused so far (from old raindrops code)
#change these to change what numbers appear in the raindrops
lowestraindropnumber = 0
highestraindropnumber = 9
if highestraindropnumber > lowestraindropnumber:
    highestraindropnumber = lowestraindropnumber


while True:
    new_livelinessGrid = copy.deepcopy(livelinessGrid)


    for i in range(linesperframe):
        for j in range(cellsperline):
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
            #didnt bother completing as ive simplified the redundancy between neighbour checking below

            if i == 0:
                deactivateTop = True
            if i == linesperframe - 1:
                deactivateBottom = True
            if j == 0:
                deactivateLeft = True
            if j == cellsperline - 1:
                deactivateRight = True

            if deactivateLeft == False:
                NeighbourCount += livelinessGrid[i][j - 1]
            if deactivateBottom == False and deactivateLeft == False:
                NeighbourCount += livelinessGrid[i + 1][j - 1]
            if deactivateBottom == False:
                NeighbourCount += livelinessGrid[i + 1][j]
            if deactivateBottom == False and deactivateRight == False:
                NeighbourCount += livelinessGrid[i + 1][j + 1]
            if deactivateRight == False:
                NeighbourCount += livelinessGrid[i][j + 1]
            if deactivateTop == False and deactivateRight == False:
                NeighbourCount += livelinessGrid[i - 1][j + 1]
            if deactivateTop == False:
                NeighbourCount += livelinessGrid[i - 1][j]
            if deactivateTop == False and deactivateLeft == False:
                NeighbourCount += livelinessGrid[i - 1][j - 1]

            #above can be further simplified, as can below. as above, so below
            #(idk i heard this in uncharted 3 but apparently they took it from a latin quote about
            #the macro scale universal attributes and micro scale universal attributes)

            if NeighbourCount < 2:
                new_livelinessGrid[i][j] = 0
            elif (NeighbourCount == 2 or NeighbourCount == 3) and livelinessGrid[i][j] == 1:#can stay alive as it has 2 or 3 neighbours
                new_livelinessGrid[i][j] = 1
            elif NeighbourCount == 3 and livelinessGrid[i][j] == 0:#needs exactly 3 neighbours to be born
                new_livelinessGrid[i][j] = 1
            elif NeighbourCount > 3:# >= 4 for accuracy to Conway's description of the rules on numberphile
                new_livelinessGrid[i][j] = 0


    #draw frame using data
    drawframe(new_livelinessGrid,lineresttime,frameresttime)


    os.system("cls")#this needs to be last operation so that more time is spent as displaying vs more time spent showing blank screen
    #frame is over and wiped the screen for the next frame's preparation

    #end = time.perf_counter()#if only 1 frame
    #all of nextline and future frame calculations have been done. Track framerate now (overhead from file.write could be added, but it won't be for now)

    livelinessGrid = copy.deepcopy(new_livelinessGrid)

    frameCount += 1

    if frameCount % targetFramerate == 0:
        end = time.perf_counter()
        delta = end - start
        correctedDelta = delta / targetFramerate
        file.write("Target: "+str(targetFramerate)+"\n"+"Actual: "+str(1/correctedDelta)+"\n")
        file.flush()#will force the buffer to write to file so that if the program is closed without closing file, it will still save the last result
        start = time.perf_counter()