# program optimizing flight paths in FTL

"""
FTL is a game in which a spaceship has to travel from sector to sector to gain points.
The goal is to visit as many sectors as possible in the y component while never moving backwards in the x component.
The optimal pattern looks like a sinusoidal function, but varies based on gameplay.
This program aims to optimize the flight path given a random field of sectors.

Links referenced:
https://stackoverflow.com/questions/35363444/plotting-lines-connecting-points
"""

import matplotlib.pyplot as plt
import random # random library to simulate the gameplay loop's random field

xLoc = []
yLoc = []
upperBound = 10 # arbitrarily chosen to enclose points
iterator = 3 # arbitrarily chosen to make travel between points feasible, not too far apart


# artificially bound the points together so path travel is actually possible, not zigzagging all over the plane
def pointBounds(array, bound, delta, index1, index2):
    while abs(array[index1] - array[index2]) > delta: # distance between points is greater than a given value
        array[index1] = array[index2] + delta
        if array[index1] > bound or array[index2] > bound: # if a point is out of the plane, bring it back in
            array[index1] = bound - random.randint(0, bound)
        if abs(array[index1] - array[index2]) <= delta: # conditions met, plane is sufficiently constricted
            break

def graph(xAxis, yAxis):
    # graph lines that connect the ordered pairs to show connections
    for i in range(1, len(xAxis)):
        x1, x2 = xAxis[i], xAxis[i-1]
        y1, y2 = yAxis[i], yAxis[i-1]
        plt.plot([x1, x2], [y1, y2])

    plt.scatter(xAxis, yAxis)
    plt.title("FTL graph")
    plt.show()

# assign random locations in space to use for path optimization
for i in range(0, 10):
    xLoc.append(random.randint(0, upperBound))
    yLoc.append(random.randint(0,upperBound))

for i in range(len(xLoc)):
    # base case
    pointBounds(xLoc, upperBound, iterator, 0, 1)
    pointBounds(yLoc, upperBound, iterator, 0, 1)

    # induction
    pointBounds(xLoc, upperBound, iterator, 0, 1)
    pointBounds(yLoc, upperBound, iterator, i, i-1)

xLoc.sort() # sort x-coordinates so no backwards motion occurs, all vertical motion okay
print("X-coordinates: %s" % xLoc)
print("Y-coordinates: %s" % yLoc)

graph(xLoc, yLoc)
