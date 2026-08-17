linesperframe = 10
cellsperline = 10
livelines = []
frame=[]
try:
    with open("initialState.txt", "r") as file:
        information = file.readlines()

        for carrier in information:
            for carrier2 in carrier:
                if carrier2 != "\n":
                    livelines.append(int(carrier2))
            frame.append(livelines)
            livelines = []


except:
    with open("initialState.txt", "a") as file: file.close()

print(frame)