# a Chrono Trigger neural network
# This neural network accounts for the various possibilities of characters and playstyles.
# It then calculates the optimality of the given settings.

import numpy as np

# hp, mp, power, hit, magic, evade, stamina, magicDef, speed - at level 1
chrono = np.array([70, 8, 5, 8, 5, 8, 8, 2, 12])
lucca = np.array([62, 12, 2, 8, 8, 7, 6, 7, 6])
robo = np.array([130, 6, 7, 7, 3, 7, 10, 1, 6])
ayla = np.array([80, 4, 10, 10, 3, 12, 9, 1, 13])
marle = np.array([65, 12, 2, 8, 8, 6, 6, 8, 8])
frog = np.array([80, 9, 4, 8, 6, 8, 8, 3, 11])
magus = np.array([110, 14, 8, 12, 10, 10, 7, 9, 12])

characterArray = [chrono, lucca, robo, ayla, marle, frog, magus]
characterStringArray = ["Chrono", "Lucca", "Robo", "Ayla", "Marle", "Frog", "Magus"]

print("Chrono, Lucca, Robo, Ayla, Marle, Frog, Magus")
print("Pick three CT characters. Please enter them as integers.")
print("Chrono = 0, Lucca = 1, etc.")
c1 = int(input())
c2 = int(input())
c3 = int(input())

if 0 <= c1 <= 7 and 0 <= c2 <= 7 and 0 <= c3 <= 7:
    party = [characterArray[c1], characterArray[c2], characterArray[c3]]
    partyString = [characterStringArray[c1], characterStringArray[c2], characterStringArray[c3]]
    for i in range(0, 3):
        print("Party member %s: %s" % ((i+1), partyString[i]))

# weights are hp, mp, power, and magic
# 0 is HP, 1 is MP, 2 and 4 are physical and magical slots respectively
computeWeights(c1, c2, c3, characterArray, 0, 1, 2, 4)

#add party type as bias to network
print("\nDo you want a physical, magical, or balanced party?")
party = input()
party = party.lower()

if party == "physical":
    computeBias(c1, c2, c3, characterArray, 2)
elif party == "magical":
    computeBias(c1, c2, c3, characterArray, 4)
elif party == "balanced":
    totalSum = computeBias(c1, c2, c3, characterArray, 2) + computeBias(c1, c2, c3, characterArray, 4)
    avgStat = totalSum / 2
else:
    print("Please try again with a legitimate party type.")

class OptimalParty:
    def __init__(self, weight, bias):
        self.weight = weight
        self.bias = bias

    def feed_forward(self, inputParty):
        totalParty = float(self.weight) + float(np.sum(inputParty)) + float(self.bias)

        # squishes the output between 0 and 1 for network use
        return sigmoid(totalParty)

def sigmoid(x):
    return 1/(1+np.exp(-x))

def computeWeights(x1, x2, x3, bigArray, hp_slot, mp_slot, phys_slot, mag_slot):
    # x1, x2, and x3 are character parameters - which party members are included?
    # this information segues into a computation of weights based on the stats of those party members
    small1 = bigArray[x1]
    small2 = bigArray[x2]
    small3 = bigArray[x3]

    hp_mp1 = small1[hp_slot] + small1[mp_slot]
    hp_mp2 = small2[hp_slot] + small2[mp_slot]
    hp_mp3 = small3[hp_slot] + small3[mp_slot]

    atk1 = small1[phys_slot] + small1[mag_slot]
    atk2 = small2[phys_slot] + small2[mag_slot]
    atk3 = small3[phys_slot] + small3[mag_slot]

    hpmp = hp_mp1 + hp_mp2 + hp_mp3
    stat = atk1 + atk2 + atk3

    computeWeights.totalStat = hpmp + stat
    computeWeights.totalStat = computeWeights.totalStat / 1000

    return computeWeights.totalStat

def computeBias(x1, x2, x3, bigArray, slot):
    small1 = bigArray[x1]
    small2 = bigArray[x2]
    small3 = bigArray[x3]

    num1 = small1[slot]
    num2 = small2[slot]
    num3 = small3[slot]
    computeBias.stat = num1 + num2 + num3

    # stat will have double digits, which needs to be in [0, 1] for the sigmoid
    return computeBias.stat

computeWeights(c1, c2, c3, characterArray, 0, 1, 2, 4)
weight = computeWeights.totalStat
bias = computeBias.stat

partySum = np.sum(characterArray[c1]) + np.sum(characterArray[c2]) + np.sum(characterArray[c3])

# sigmoid needs inputs between 0 and 1, squishes partySum into a decimal
partySum = partySum / 1000
partyArray = [partySum]

partyOptimize = OptimalParty(weight, bias)
partyCalc = partyOptimize.feed_forward(partyArray)
print("Your party optimality as a decimal: " + str(partyCalc))
