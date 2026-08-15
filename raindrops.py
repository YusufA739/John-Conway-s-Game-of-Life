import random,sys,time,os
from colorama import Fore, Back, Style
nextline = ""
currentframe = []
currentframelengthofraindrop = []
lengthofraindrop = []

#manually get screen width from user. They copy and paste one line; we use count to detect the cells per row
for carrier in range(500):
    sys.stdout.write("0")


#change these to change frame size
#linesperframe = 55#55x209 for fullscreen command prompt for my pc
#cellsperline = 222
linesperframe = int(input("type in your height:"))
cellsperline = len(input("use this to calibrate your width and paste the line length:"))

#change these to alter the length of raindrops and the length in between new raindrops in the same column
lowestvalue = -1000#increasing the spacing between raindrops in the same column
stopvalue = 0#value to signify the "stop" length of a raindrop, within lowest value and highest value range
highestvalue = 10#max len of raindrops

#change these to change what numbers appear in the raindrops
lowestraindropnumber = 5
highestraindropnumber = 5

#change to alter line rest time and frame rest time
lineresttime = 0
frameresttime = 0

targetFramerate = 40
currentFramerate = 0

#make the first line
for placeholder in range(cellsperline):#cells per line is given by user input
    lengthofraindrop.append(random.randint(lowestvalue,highestvalue))
    nextline += str(random.randint(lowestraindropnumber,highestraindropnumber))#we need this to know initial raindrop lengths and placements

#make the first frame using the first line
for i in range(linesperframe):
    currentframe.append(nextline)#every line starts out the same singular line copied out
    currentframelengthofraindrop.append(lengthofraindrop.copy())#only first line is necessary, but I will leave for now

frameCount = 0
file = open("framerate.txt", "w")
start = time.perf_counter()#for inital measurement, will be wrong until it updates in if statement (reduces frame delays due to extra timer processing)

while True:

    # calculate the next frame's data (changes impacting frame: new line added at top, deletion at bottom)
    nextline = ""
    lengthofraindrop = currentframelengthofraindrop[0].copy()
    for i in range(cellsperline):
        if lengthofraindrop[i] > stopvalue:
            if highestraindropnumber > lowestraindropnumber:
                nextline += str(random.randint(lowestraindropnumber, highestraindropnumber))  # change to (0,1) for binary
                lengthofraindrop[i] -= 1
            else:
                nextline += str(lowestraindropnumber)
                lengthofraindrop[i] -= 1
        elif lengthofraindrop[i] <= lowestvalue:
            if highestraindropnumber > lowestraindropnumber:
                nextline += str(random.randint(lowestraindropnumber, highestraindropnumber))  # change to (0,1) for binary
                lengthofraindrop[i] = random.randint(stopvalue, highestvalue)
            else:
                nextline += str(lowestraindropnumber)
                lengthofraindrop[i] = random.randint(stopvalue, highestvalue)
        else:
            nextline += str(lowestraindropnumber)
            lengthofraindrop[i] -= 1

    # update future frame with new information
    for carrier in range(linesperframe - 1, 0, -1):  # update all unaltered lines down, skipping overwriting the first, so line 1 and 2 will be identical for now, and also not rewriting the last line to another line
        currentframe[carrier] = currentframe[carrier - 1]
        currentframelengthofraindrop[carrier] = currentframelengthofraindrop[carrier - 1].copy()

    # finally, update the next frame's first line
    currentframe[0] = nextline
    currentframelengthofraindrop[0] = lengthofraindrop.copy()  # tracks droplength remaining to generate. Tells us when the raindrop has reached zero length. Once zero length, we wait until it goes past a certain negative
    # negative acts like the reverse of a drop. So just black bg/a gap. Once we hit the negative floor, we choose a random positive int to make a new droplet


    #display next frame data (updated frame data) (next is current frame)
    color = 1
    for line in range(linesperframe):
        for cell in range(cellsperline):
            if currentframelengthofraindrop[line][cell] <= 0:
                sys.stdout.write(Fore.BLACK + currentframe[line][cell])
            else:
                #color = random.randint(0,1)
                if color == 0:
                    sys.stdout.write(Fore.BLACK + currentframe[line][cell])
                elif color == 1:
                    sys.stdout.write(Fore.GREEN + currentframe[line][cell])
        sys.stdout.write("\n")
        time.sleep(lineresttime)
    time.sleep(frameresttime)


    os.system("cls")#this needs to be last operation so that more time is spent as displaying vs more time spent showing blank screen
    #frame is over and wiped the screen for the next frame's preparation

    #end = time.perf_counter()#if only 1 frame
    #all of nextline and future frame calculations have been done. Track framerate now (overhead from file.write could be added, but it won't be for now)

    frameCount += 1

    if frameCount % targetFramerate == 0:
        end = time.perf_counter()
        delta = end - start
        correctedDelta = delta / targetFramerate
        file.write("Target: "+str(targetFramerate)+"\n"+"Actual: "+str(1/correctedDelta)+"\n")
        file.flush()#will force the buffer to write to file so that if the program is closed without closing file, it will still save the last result
        start = time.perf_counter()