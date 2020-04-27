import random
import numpy as np

# set up classes
warrior = [5, 5, 2, 1, 2, False, False]
thief = [4, 3, 5, 1, 1, False, False]
monk = [5, 4, 3, 1, 2, False, False]
mageWhite = [1, 2, 3, 5, 4, False, True]
mageBlack = [1, 2, 3, 5 , 4, True, False]
mageRed = [3, 4, 2, 4, 3, True, True]

# set up array that links to stats to create party
ff_classes = [warrior, thief, monk, mageWhite, mageBlack, mageRed]

# need two damage dealers, one healer, and one offensive mage
keepDPS = False
keepHealer = False
keepNuker = False

# set up genetic algorithm with functions
def genClasses(party, array, partyMems):
    for member in range(partyMems):
        member = random.randint(0, 5)
        party.append(array[member])
    print(party)

def fourPartyMems(num, ff_party):
    # reduce party if > 4 members
    tot1= np.array(ff_party[num-1][0]) + np.array(ff_party[num-1][1]) + \
                np.array(ff_party[num-1][2])
    tot2 = np.array(ff_party[num][0]) + np.array(ff_party[num][1]) + \
                np.array(ff_party[num][2])

    if tot1 > tot2:
        ff_party.pop(num)
    elif tot2 > tot1:
        ff_party.pop(num-1)
    else:
        ff_party.pop()

ff_party = []
genClasses(ff_party, ff_classes, 4)

"""
Genetic algorithms randomize, optimize, regenerate, and repeat.
Randomize the party, set booleans to check for "good" party configs
(i.e. magic) and use those to create the next, extra-fit generation.
"""
for member in ff_party:
    if member[5]:
        keepHealer = True
    if member[6]:
        keepNuker = True

ff_party = [] # reset party with booleans on for next generation

# the next generation is more fit; already checked for magic
# keep those changes by adding them to the party array

if keepHealer:
    ff_party.append(mageWhite)
if not keepHealer and keepNuker:
    ff_party.append(mageBlack)
elif keepHealer and keepNuker:
    ff_party.append(mageRed)

# though some of the party is configured, I need four members
# the other members are randomized genetically; repeat process
genClasses(ff_party, ff_classes, (4-len(ff_party)))

# check for adding damage dealers to party by assessing stats

partyMemCheck = np.array(ff_party[2][0]) + \
    np.array(ff_party[2][1]) + np.array(ff_party[2][2])
if partyMemCheck >= 10:
    keepDPS = True
    mem = ff_party[2]
ff_party = [] # reset party for third generation

# keep the changes of the third generation and regenerate

if keepDPS:
    ff_party.append(mem)
if keepHealer:
    ff_party.append(mageWhite)
if not keepHealer and keepNuker:
    ff_party.append(mageBlack)
elif keepHealer and keepNuker:
    ff_party.append(mageRed)

# add/reduce party members as necessary for right amount; the members themselves are already genetically optimized
while len(ff_party) < 4:
    genClasses(ff_party, ff_classes, (4-len(ff_party)))

    for member in range(0, len(ff_party)):
        if np.array(ff_party[member][0]) + np.array(ff_party[member][1]) + \
                np.array(ff_party[member][2]) >= 10:
            ff_party.append(ff_party[member])

while len(ff_party) > 4:
    if len(ff_party) == 5:
        fourPartyMems(4, ff_party)
    elif len(ff_party) == 6:
        fourPartyMems(5, ff_party)

print("Final: ")
print(ff_party)
