# neural network for The Elder Scrolls III: Morrowind
# given a character's species and stats, how optimal is their given skill set?

import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

class OptimalMorrowind:
    def __init__(self, weight):
        self.weight = weight

    def feed_forward(self, input):
        total = np.dot(self.weight, input)
        return sigmoid(total)

names = ["Altmer", "Argonian", "Bosmer", "Breton", "Dunmer",
             "Imperial", "Khajiit", "Nord", "Orc", "Redguard"]

# strength, intelligence, willpower, speed, endurance
altmer = [30, 50, 40, 30, 40,]
argonian = [40, 40, 30, 40, 30]
bosmer = [30, 40, 30, 50, 30]
breton = [40, 50, 50, 40, 30]
dunmer = [40, 40, 30, 50, 35]
imperial = [40, 40, 30, 40, 40]
khajiit = [40, 40, 30, 50, 40]
nord = [50, 30, 40, 40, 50]
orc = [45, 30, 50, 30, 50]
redguard = [50, 30, 30, 40, 50]

speciesArray= [altmer, argonian, bosmer, breton, dunmer, imperial,
             khajiit, nord, orc, redguard]

# get user input - what character build will they use?
for name in names:
    print(name, end=" ")

print("\nWhat race is your character? Enter 0 for Altmer, etc.")
characterNum = int(input())

# weight for neural network determined by playstyle
print("\nWhat kind of playstyle are you planning?"
      "\nEnter 0 for mage, 1 for warrior, and a decimal"
      " between 0 and 1 for mixed.")
playStyle = float(input())

# calculate the optimality
character = speciesArray[characterNum]

# setting weights by checking 2d array for stats
if playStyle == 0:
    weight = np.array(speciesArray[characterNum][1]) # check int
elif playStyle == 1:
    weight = np.array(speciesArray[characterNum][0]) # check str
elif 0 < playStyle < 1:
    if playStyle > 0.5:
        weight = np.array(speciesArray[characterNum][0]) * 2/3 \
                + np.array(speciesArray[characterNum][1]) * 1/3
    else:
        weight = np.array(speciesArray[characterNum][1]) * 2/3 \
                 + np.array(speciesArray[characterNum][0]) * 1/3
else: # cannot choose a non-physical or non-magical style
    print("Not a valid playstyle.")

# acts as bias for neural net, which customizes character
print("\nPhysical, magical, or stealth skill tree?"
      " Enter 0 for physical, etc.")
skill = int(input())

# bias directly adding to neural net calculations
for species in speciesArray:
    if skill == 0: # warrior - physical
        species[0] += 10
    elif skill == 1: # mage - magical
        species[1] += 10
    elif skill == 2: # thief - stealth
        species[3] += 10
    else:
        print("Not a valid skill tree.")

# set nerevarArray to 0.1 for neural net dot product calculation
nerevarArray = [0.1]
nerevar = OptimalMorrowind(weight)
optimalCalc = nerevar.feed_forward(nerevarArray)

print("Your character's optimality: " + optimalCalc)
