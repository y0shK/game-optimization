import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from sklearn import linear_model
from sympy import *

"""
players chosen:
    Mike Trout, Mookie Betts, Buster Posey, Kyle Seager,
    Mike Moustakas, Scooter Gennett, Salvador Perez, Andrew McCutchen
    Andrelton Simmons, Joey Votto, Eugenio Suarez, Tommy Pham,
    Giancarlo Stanton, Jurickson Profar, Jackie Bradley Jr., Jason Kipnis,
    Jose Martinez, Corey Dickerson, Nolan Arenado, Trevor Story,
    Lorenzo Cain, Michael Brantley, Freddie Freeman, Christian Yelich
"""

players = {'Average': [.312, .346, .284, .221, .251, .310, .235, .255,
                       .292, .284, .283, .275, .266, .254, .234, .230, .305, .300,
                       .297, .291, .308, .309, .309, .326],
                   'WAR': [10.2, 10.9, 2.9, 0.8, 2.5, 4.2, 2.4, 2.7, 6.2, 3.5, 4.2,
                        3.4, 4.0, 2.0, 2.1, 1.6, 1.5, 3.8, 5.6, 5.6, 6.9, 3.6, 6.1, 7.6]}

df = DataFrame(players, columns=['Average', 'WAR'])
print(df)

# set up DataFrame arrays + AVG vs. WAR plot
X = df['Average']
Y = df['WAR']

plt.scatter(X, Y, color='red')
plt.title('WAR vs. Average', fontsize=14)
plt.xlabel("Average", fontsize=12)
plt.ylabel("WAR", fontsize=12)
plt.grid(True)

# use numpy modules to create a 1D trend line
z = np.polyfit(X, Y, 1)
p = np.poly1d(z)
plt.plot(X, p(X))
plt.show()

# calculate mean sum squared error
mseSum = 0
for i in range(len(df)): # iterate through all elements (i.e. batters)
    mse = np.mean((Y[i] - p(X)) ** 2) # takes difference of (individual dot - trendline)
    mseSum += mse
print(mseSum) # total error for all points to the trendline

# new DataFrame arrays, 2d for input + 1d for output
xRegression = df[['Average']]
yRegression = df['WAR']

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
print("AVG: " + str(yFn))

"""
-the derivative of a first order Taylor polynomial is a single value
-for gradient descent, the derivative (which is a Taylor polynomial
of order 0) is used as input for the cost function J(theta), such that
theta = value of the derivative as calculated by the trendline
"""
trendDeriv = yFn.diff(x)
print(str(trendDeriv))

"""
-let theta be written as "t"
-the algorithm is: t = t +- alpha * d/dt (mseSum) / (2m), where:
alpha is the learning rate parameter
m is the number of element pairs (x, y) in the set
mseSum is the sum from 1 to m of (the differences between the
    actual values and the values plotted on the trendline)^2
"""
alpha = 0.01 # arbitrary constant
theta = trendDeriv # starting definition

"""
-the derivative of the cost function (which is a quadratic) becomes
linear, so the chain rule will cancel out the 2 in the denominator
-theta (which is the slope of the trendline) is used in the cost function
    as the domain; it goes to 0 and gradient descent finishes
"""

# if alpha is too big, theta can oscillate between > and < 0 like sin(x)
def check_oscillation(thetaVal, batch):
    posOdd = False
    posEven = False
    negOdd = False
    negEven = False

    """
    if two successive numbers are opposite signs (and they are
    opposite parities by definition of succession) then we know that
    theta values are oscillating, so we check parity and sign to stop it
    """
    if (0 < thetaVal < 0.01) and batch % 2 == 1 or batch % 2 == 0:
        posOdd = True
    if (0 < thetaVal < 0.01) and batch % 2 == 0 or batch % 2 == 1:
        posEven = True
    if (-0.09 < thetaVal < 0) and batch % 2 == 1 or batch % 2 == 0:
        negOdd = True
    if (-0.09 < thetaVal < 0) and batch % 2 == 0 or batch % 2 == 1:
        negEven = True

    # parity and sign are guaranteed to switch; stop the algorithm
    if (posOdd and negEven) or (negOdd and posEven):
        print("The gradient descent will oscillate! Let's stop here.")
        print("It took %s steps." % str(batch))
        exit()

def gradient_descent(thetaVal, alphaVal, mseSum, mValue):
    # m is the list of elements, so the length of the DataFrame is the m value
    batch = 0
    while thetaVal != 0: # operation +- depending on the sign of theta
        if thetaVal > 0:
            thetaVal = thetaVal - (alphaVal * mseSum) / (mValue + 1) # mValue is zero-indexed
        elif thetaVal < 0:
            thetaVal = thetaVal + (alphaVal * mseSum) / (mValue + 1)
        else:
            print("Gradient descent completed! It took %s steps" % str(batch))
            exit()
        print(thetaVal)
        batch += 1

        # check after every new value to stop the algorithm when necessary
        check_oscillation(thetaVal, batch)

gradient_descent(theta, alpha, mseSum, len(df))
