from DesmosKiller.DesmosKiller.DesmosKiller import *
import numpy as np
import seaborn as sns

with open("livecellvsframecount.txt","r") as file:
    data = file.readlines()
    for carrier in range(len(data)):
        data[carrier] = data[carrier].strip("\n").split(",")
    file.close()

data.remove(data[len(data)-1])

print(data)

startCoords=[]
endCoords=[]

for carrier in range(len(data)):
    if carrier%2 == 1:
        startCoords.append([int(data[carrier][0]),int(data[carrier][1])])
    else:
        endCoords.append([int(data[carrier][0]),int(data[carrier][1])])


def quicksortCartesian(list1):
    if len(list1) < 2:
        return list1
    pivot = list1[len(list1)//2][0]
    lower = [list1[carrier] for carrier in range(len(list1)) if list1[carrier][0] < pivot]
    middle = [list1[carrier] for carrier in range(len(list1)) if list1[carrier][0] == pivot]
    upper = [list1[carrier] for carrier in range(len(list1)) if list1[carrier][0] > pivot]

    return quicksortCartesian(lower) + middle + quicksortCartesian(upper)



def ks(eray):
    if len(eray) < 2:
        return eray
    pivot = eray[len(eray) // 2]
    left = [x for x in eray if x < pivot]
    midul = [x for x in eray if x == pivot]
    right = [x for x in eray if x > pivot]
    return ks(left) + midul + ks(right)

print(startCoords)

new = quicksortCartesian(startCoords)

print(new)

input("sorted lists above")

xlistStart = []
ylistStart = []
for carrier in range(len(new)):
    xlistStart.append(new[carrier][0])
    ylistStart.append(new[carrier][1])

graph(xlist=xlistStart,ylist=ylistStart)
show()


def polynomialcobf(x, y, degree):

    try:
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)
    except ValueError:
        raise ValueError("x and y must be numeric sequences.")

    if x.shape != y.shape:
        raise ValueError("x and y must have the same length.")
    if degree < 0:
        raise ValueError("Degree must be a non-negative integer.")
    if degree >= len(x):
        raise ValueError("Degree must be less than number of data points.")

    #fit polynomial coefficients
    coeffs = np.polyfit(x, y, 1)

    #create polynomial function from coefficients
    poly_func = np.poly1d(coeffs)

    # Generate smooth x values for plotting the curve
    x_smooth = np.linspace(min(x), max(x), 500)
    y_smooth = poly_func(x_smooth)

    #plot original data points
    plt.scatter(x, y, color='orange', label='Data points')

    #plot polynomial fit
    plt.plot(x_smooth, y_smooth, color='red',
             label=f'Polynomial degree {degree}')

    #labels and legend
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Polynomial Fit (degree {degree})')
    plt.legend()
    plt.grid(True)
    plt.show()


#test data
# x_data = [1, 2, 3, 4, 5, 6]
# y_data = [2.2, 2.8, 3.6, 4.5, 6.1, 7.8]

# sns.regplot(x=x_data, y=y_data, ci=None, scatter_kws={"color": "blue"}, line_kws={"color": "red"})


polynomialcobf(xlistStart, ylistStart, degree=3)
