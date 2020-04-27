import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from sklearn import linear_model
from sympy import *

"""
-I assume max amount of frames for executing move
-I used the SmashBoards Falco frame data thread to assign frames
    -https://smashboards.com/threads/falco-hitboxes-and-frame-data.300397/
-Other useful resources:
    -https://stackoverflow.com/questions/30486263/sorting-by-absolute-value-without-changing-the-data
    -https://stackoverflow.com/questions/14847457/how-do-i-find-the-length-or-dimensions-size-of-a-numpy-matrix-in-python
"""

falco = {'Frames': [17, 20, 36, 39, 26, 26, 26, 23, 29, 49, 59, 39, 49, 46,
                    45, 51, 57, 29, 29, 21, 21, 64, 1],
         'Damage': [3, 4, 5, 9, 8, 8, 8, 8, 10, 11, 13, 10, 14, 8, 17, 15,
                    16, 5, 5, 7, 7, 16, 8]}

df_falco = DataFrame(falco, columns=['Frames', 'Damage'])
print(df_falco)

"""
sort values in dictionary key by ascending, then reassign dictionary
    values to their keys so I keep each ordered pair (x, y) intact
"""
X = df_falco['Frames'].sort_values(ascending=True)
Y = df_falco['Damage'].reindex(df_falco['Frames'].sort_values().index)

plt.scatter(X, Y, color='red')
plt.title('Falco Frame Data vs. Damage Given', fontsize=14)
plt.xlabel('Frames (frames)', fontsize=12)
plt.ylabel('Damage (%)', fontsize=12)
plt.grid(True)

# plot a linear polynomial for a trend line
z = np.polyfit(X, Y, 1)
f = np.poly1d(z)
plt.plot(X, f(X))
plt.show()

# calculate mean sum squared error
mseSum = 0
for i in range(len(df_falco)): # iterate through all elements (i.e. frames + %)
    mse = np.mean((Y[i] - f(X)) ** 2) # takes difference of (individual dot - trend line)
    mseSum += mse
print("Total mean sum squared error: " + str(mseSum)) # total error for all points to the trend line

# new DataFrame arrays, 2d for input + 1d for output
xRegression = df_falco[['Frames']]
yRegression = df_falco['Damage']

regression = linear_model.LinearRegression()
regression.fit(xRegression, yRegression)

y_int = regression.intercept_
x_coefficient = regression.coef_
x_coefficient = float(x_coefficient) # convert from array to float

# use sympy modules for differentiation
x = Symbol('x')
yFn = x_coefficient * x + y_int

print("\nY-intercept: " + str(y_int))
print("Coefficient: " + str(x_coefficient))
print("Trend line equation: " + str(yFn))

"""
-I need m x n and n x o matrices for the matrix product
-the resulting product is an m x o matrix which crosses the elements
    of the trend line with the DataFrame data
"""
trendLine = [x_coefficient, y_int]
trendLineArray = np.array([trendLine]) # 1x2
falcoArray = np.array([df_falco['Frames'], df_falco['Damage']]) #2x23

print("\nThe 1x2 matrix from the trend line equation: " + str(trendLineArray))
print("Falco's 2x23 matrix of frame data and damage: " + str(falcoArray))

# dot product performs multiplication for each element
matrixProduct = trendLineArray.dot(falcoArray)
print("\nThe matrix product of the trend line and Falco's stats: "
      + str(matrixProduct))
print("\nThe product is a %sx%s matrix." % (matrixProduct.shape[0],
        matrixProduct.shape[1]))
