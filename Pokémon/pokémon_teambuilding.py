import csv
import pandas
import random

from mpl_toolkits.mplot3d import Axes3D # <--- unused statement for graphing
from matplotlib import cm # warm-color color map for pokemon 3D graph
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import math

"""
-Pokemon CSV array data: https://www.kaggle.com/abcsds/pokemon
[number, pokemon name, type 1, type 2, sum of stats, HP,
attack, defense, special attack, special defense, speed,
generation, boolean isLegendary]
- Stealth Rock list: https://www.serebii.net/attackdex-bw/stealthrock.shtml

-https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty
-https://stackoverflow.com/questions/52050346/passing-csv-files-as-arguments-to-a-function
-https://stackoverflow.com/questions/37711538/matplotlib-3d-axes-ticks-labels-and-latex
-https://en.wikipedia.org/wiki/Gradient_descent#Python
"""

csvDirectory = '/home/yash/Downloads/pokemon.csv/Pokemon.csv'
pokemonList = pandas.read_csv(csvDirectory)
print(pokemonList)

# create a hyper-offensive team, with four sweepers + tank + Stealth Rock
physBulk = []
physSpd = []
spBulk = []
spSpd = []
tank = []
sweepers = [physBulk, physSpd, spBulk, spSpd] # for loop iteration

# define stealth rockers based on competitive viability (e.g. ubers, OU/UU)
stealthRock = ['Golem', 'Steelix', 'Gigalith', 'Crustle', 'Sandslash',
               'Nidoqueen', 'Nidoking', 'Clefairy', 'Clefable', 'Wigglytuff',
               'Marowak', 'Dugtrio', 'Chansey', 'Pinsir', 'PinsirMega Pinsir',
               'Omastar', 'Kabutops', 'Aerodactyl', 'Mew', 'Sudowoodo',
               'Forretress', 'Corsola', 'Skarmory', 'Donphan', 'Blissey',
               'Miltank', 'Tyranitar', 'Celebi', 'Swampert',
               'SwampertMega Swampert', 'Aggron', 'Camerupt', 'Lunatone',
               'Armaldo', 'Kecleon', 'Relicanth', 'Metagross', 'Regirock',
               'Registeel', 'Groudon', 'GroudonMega Groudon', 'Jirachi',
               'Deoxys', 'Torterra', 'Infernape', 'Empoleon', 'Bibarel',
               'Rampardos', 'Bastiodon', 'Bronzong', 'Garchomp', 'Rhyperior',
               'Hippowdon', 'Gliscor', 'Mamoswine', 'Probopass', 'Uxie',
               'Mesperit', 'Azelf', 'Dialga', 'Heatran', 'Arceus', 'Excadrill',
               'Seismitoad', 'Krookodile', 'Carracosta', 'Archeops', 'Ferrothorn',
               'Stunfisk', 'Druddigon', 'Bisharp', 'Cobalion', 'Terrakion', 'Landorus']

def checkSweepers(directory):
    # row 5 is HP, 6 is Attack, 7 is Special Attack, 9 is Special Defense, 10 is Speed
    with open(directory, newline="") as file:
        reader = csv.reader(file)
        next(file) # skip intro line
        for row in reader:
            if int(row[5]) >= 105 and int(row[6]) >= 105:
                physBulk.append(row[1])
            if int(row[10]) >= 105 and int(row[6]) >= 105:
                physSpd.append(row[1])
            if int(row[5]) >= 105 and int(row[7]) >= 105:
                spBulk.append(row[1])
            if int(row[10]) >= 105 and int(row[7]) >= 105:
                spSpd.append((row[1]))
            if int(row[7]) >= 105 and int(row[9]) >= 105:
                tank.append(row[1])

checkSweepers(csvDirectory)
print(physBulk)
print(physSpd)
print(spBulk)
print(spSpd)
print(tank)

"""
-choose 6 random Pokemon
-one of each category + stealth rocker
-implement restrictions; no duplicates, mega evolutions <= 1
"""

# take qualified Pokemon from each category and pick one at random to add to the team
def addToTeam(teamNiche, teamArray):
    teamArray.append(teamNiche[(random.randrange(0, len(teamNiche)))])

teamValid = False # becomes true if randomized team meets criteria
def verifyTeam(team):
    unique = True
    megaCount = 0
    megaCountGood = True
    global teamValid

    # ensure through iteration that each team member is distinct
    for i in range(0, len(team)):
        if 0 < i < 5 and team[i] == team[i+1]:
            unique = False
            if team[i] in team[i+1]: # check to make sure one Pokemon isn't a Mega and another pokemon isn't a regular form of the same Mega
                unique = False
        elif i == 5 and team[5] == team[0]:
            unique = False
            if team[5] in team[0]:
                unique = False
        if "Mega" in team[i]: # ensure that Mega Pokemon are <= 1 on each team
            megaCount += 1
    if megaCount > 1:
        megaCountGood = False
    print(megaCountGood)
    if unique and megaCountGood: # conditions met, so return boolean True
        teamValid = True
        print(team)
        return teamValid
    else: # team is not valid; regenerate team
        team = []
        for pokemonName in categories:
            addToTeam(pokemonName, team)
        unique = True
        megaCount = 0
        megaCountGood = True

        for i in range(0, len(team)):
            if 0 < i < 5 and team[i] == team[i + 1]:
                unique = False
                # check to make sure one Pokemon isn't a Mega and another pokemon isn't a regular form of the same Mega
                if team[i] in team[i + 1]:
                    unique = False
            elif i == 5 and team[5] == team[0]:
                unique = False
                if team[5] in team[0]:
                    unique = False
            if "Mega" in team[i]:
                megaCount += 1
        if megaCount > 1:
            megaCountGood = False
        print(megaCountGood)
        if unique and megaCountGood:
            teamValid = True
            print(team)
            return teamValid
        else:
            exit() # can't graph + perform gradient descent if function isn't smooth

team = []
categories = [physBulk, physSpd, spBulk, spSpd, tank, stealthRock]

for pokemon in categories:
    addToTeam(pokemon, team)
verifyTeam(team)

# create arrays for stats of each Pokemon, which go into matplotlib
physBulkArray = []
physSpdArray = []
spBulkArray = []
spSpdArray = []
tankArray = []
stealthRockArray = []

def addValuesToTeam(directory):
    global physBulkArray
    global physSpdArray
    global spBulkArray
    global spSpdArray
    global tankArray
    global stealthRockArray

    with open(directory, newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            for member in team:
                # if the team member shows up in the csv file and in the array as a suitable candidate, the stats are appended
                if member in row and member in physBulk:
                    physBulkArray = [int(row[6]), int(row[5]), int(row[4])]
                if member in row and member in physSpd:
                    physSpdArray = [int(row[6]), int(row[10]), int(row[4])]
                if member in row and member in spBulk:
                    spBulkArray = [int(row[8]), int(row[5]), int(row[4])]
                if member in row and member in spSpd:
                    spSpdArray = [int(row[8]), int(row[10]), int(row[4])]
                if member in row and member in tank:
                    tankArray = [int(row[7]), int(row[9]), int(row[4])]
                if member in row and member in stealthRock:
                    stealthRockArray = [int(row[6]), int(row[7]), int(row[4])]

addValuesToTeam(csvDirectory)

print(physBulkArray)
print(physSpdArray)
print(spBulkArray)
print(spSpdArray)
print(tankArray)
print(stealthRockArray)

x1 = [1, physBulkArray[0], physBulkArray[1]]
x2 = [1, physSpdArray[0], physSpdArray[1]]
x3 = [1, spBulkArray[0], spBulkArray[1]]
x4 = [1, spSpdArray[0], spSpdArray[1]]
x5 = [1, tankArray[0], tankArray[1]]
x6 = [1, stealthRockArray[0], stealthRockArray[1]]
matrix = np.array([x1, x2, x3, x4, x5, x6])

y = np.array([physBulkArray[2], physSpdArray[2], spBulkArray[2],
              spSpdArray[2], tankArray[2], stealthRockArray[2]])

transpose = matrix.transpose()
matrixProduct = transpose.dot(matrix)

try:
    matrixProduct = np.linalg.inv(matrix)
except np.linalg.LinAlgError:
    # matrix is not invertible
    pass

matrixProduct2 = transpose.dot(y)
theta = matrixProduct.dot(matrixProduct2)
print(str(theta))

fig = plt.figure()
ax = fig.gca(projection='3d')

tank_0 = int(tankArray[0]) / 10
tank_1 = int(tankArray[1]) / 10
stealthRock_0= int(stealthRockArray[0]) / 10
stealthRock_1 = int(stealthRockArray[1]) / 10

if tank_0 > tank_1:
    a = np.arange(-1 * tank_1, tank_0, 1)
else:
    a = np.arange(-1 * tank_0, tank_1, 1)

if stealthRock_0 > stealthRock_1:
    b = np.arange(-1 * stealthRock_1, stealthRock_0, 1)
else:
    b = np.arange(-1 * stealthRock_0, stealthRock_1, 1)

a, b = np.meshgrid(a, b)
r = np.sqrt(a**2 + b**2)

# base graph is cos x, plug in point (r, cos(r))
z = np.cos(r) # use sinusoidal to reduce size of input & scale it
# if RuntimeWarning or ZeroDivisionError:
    #print("Division by zero occurred, graph is invalid")
    #exit() # algorithm won't work without a smooth function

surf = ax.plot_surface(a, b, z, linewidth=0, antialiased = False)

ax.set_title("Tank vs. Stealth Rocker Gradient Descent", fontsize=14)
ax.set_xlabel("Tank defense + special defense", fontsize=10)
ax.set_ylabel("Stealth Rock attack + defense", fontsize=10)

ax.set_zlim(-2, 2)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.set_zticks([-2, 0, 2])

fig.colorbar(surf, shrink=1, aspect=5)
plt.show()
