import matplotlib.pyplot as plt
from pandas import DataFrame
from sklearn import linear_model

"""
array format: [avg, HR, RBI, WAR]
    x = avg, HR, RBI
    y = WAR
choose 2018 statistics of All-Stars and reg. players to compute how the effect of Triple Crown stats contribute to WAR
players chosen: 
    Mike Trout, Mookie Betts, Buster Posey, Kyle Seager,
    Mike Moustakas, Scooter Gennett, Salvador Perez, Andrew McCutchen
    Andrelton Simmons, Joey Votto, Eugenio Suarez, Tommy Pham,
    Giancarlo Stanton, Jurickson Profar, Jackie Bradley Jr., Jason Kipnis,
    Jose Martinez, Corey Dickerson, Nolan Arenado, Trevor Story,
    Lorenzo Cain, Michael Brantley, Freddie Freeman, Christian Yelich
"""

players = {'Average': [.312, .346, .284, .221, .251, .310, .235, .255, .292,
                       .284, .283, .275, .266, .254, .234, .230, .305, .300, .297,
                       .291, .308, .309, .309, .326],
           'HR': [39, 32, 5, 22, 28, 23, 27, 20, 11, 12, 34, 21, 38, 20, 13, 18,
                  17, 13, 38, 37, 10, 17, 23, 36],
           'RBI': [79, 80, 41, 78, 95, 92, 80, 65, 75, 67, 104, 63, 100, 77, 59,
           75, 83, 55, 110, 108, 38, 76, 98, 110],
           'WAR': [10.2, 10.9, 2.9, 0.8, 2.5, 4.2, 2.4, 2.7, 6.2, 3.5, 4.2, 3.4, 4.0,
                   2.0, 2.1, 1.6, 1.5, 3.8, 5.6, 5.6, 6.9, 3.6, 6.1, 7.6]}

df = DataFrame(players, columns=['Average', 'HR', 'RBI', 'WAR'])
print(df)

def create_plt(string, color):
    plt.scatter(df[string], df['WAR'], color='%s' % color)
    plt.title('WAR vs. %s' % string, fontsize=14)
    plt.xlabel("%s" % string, fontsize=12)
    plt.ylabel("WAR", fontsize=12)
    plt.grid(True)
    plt.show()

create_plt('Average', 'red')
create_plt('HR', 'blue')
create_plt('RBI', 'green')

# use Pandas data frames to gauge Triple-Crown stats vs. WAR
X = df[["Average", "HR", "RBI"]]
Y = df['WAR']

regression = linear_model.LinearRegression()
regression.fit(X, Y)

print("Y-intercept: " + str(regression.intercept_))
print("Coefficient: " + str(regression.coef_))
print("AVG: y= %sx + %s" % (regression.coef_[0], regression.intercept_))
print("HR: y= %sx + %s" % (regression.coef_[1], regression.intercept_))
print("RBI: y= %sx + %s" % (regression.coef_[2], regression.intercept_))

# given a certain set of numbers (for a specific player or for a general archetype), find WAR
print("\nEnter AVG")
avg = float(input())

print("\nEnter HR")
hr = int(input())

print("\nEnter RBI")
rbi = int(input())

print("Predicted WAR: " + str(regression.predict([[avg, hr, rbi]])))
