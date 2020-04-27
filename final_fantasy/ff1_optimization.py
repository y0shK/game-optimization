
# use several characteristics to assess optimality
# each character has one specific array
# array = [physAtk, physDef, spd, magAtk, magDef, blackMagicUse, whiteMagicUse]

# determine optimality through:
    # raw point values (party must have cumulative point value of > x)
    # stat point values (party must have > x in certain stat)
    # party must have one good healer or two average healers

warrior = [5, 5, 2, 1, 2, False, False] # 15
thief = [4, 3, 5, 1, 1, False, False] # 14
monk = [5, 4, 3, 1, 2, False, False] # 15
mageWhite = [1, 2, 3, 5, 4, False, True] # 15, can heal
mageBlack = [1, 2, 3, 5, 4, True, False] # 15, black magic
mageRed = [3, 4, 2, 4, 3, True, True] # 16, can heal

names = ["Warrior", "Thief", "Monk", "White Mage", "Black Mage", "Red Mage"]
attributes = ["physAtk", "physDef", "spd", "magAtk", "magDef"]

ff_classes = [warrior, thief, monk, mageWhite, mageBlack, mageRed]

for member in range(len(names)):
    print(names[member] + " " + str(member))
    print(str(ff_classes[member]))

# user input to check an arbitrary party configuration
print("\nPick 4 party members. Warrior is 0, ..., Red Mage is 5.")
choice1 = int(input())
choice2 = int(input())
choice3 = int(input())
choice4 = int(input())

party = [choice1, choice2, choice3, choice4]
totalStats = 0 # set to 0, will increment stats based on different class permutations

for stat in party:
    stats = sum(ff_classes[stat])

    if ff_classes[stat] is True: # if black or white magic is apparent
        stats += 1 # give extra stats, incentivize magic use

    print(str(stats))
    totalStats += stats
    print("--party total: ", int(totalStats))
print(str(totalStats))

if totalStats >= 60:
    print("cumulative stats good\n")
else:
    print("cumulative stats not good\n")

def checkPartyStats(array, num):
    total = 0
    statArray = []

    for part in range(0, 4):
        subChoice = array[part]
        total += subChoice[num]
        statArray.append(total)

        # stat amount team-wide should be at least 7 for above-average party
        if total > 7:
            statsOptimal = True
        else:
            statsOptimal = False

    print(str(statArray))
    print(str(total))
    print(str("Stat total optimal? " + str(statsOptimal)) + "\n")

    return statsOptimal

def checkMagic(int1, int2, int3, int4):
    array = [int1, int2, int3, int4]
    nuke = False
    heal = False
    magicConditions = False
    redCount = 0 # two red mages count as one healer

    # red mages count as a black mage and half a white mage
    for element in array:
        if element == 4 or element == 5:
            nuke = True

    for element in array:
        if element == 3:
            heal = True
        elif element == 5:
            redCount += 1
            if redCount > 1:
                heal = True

    print("\nBlack Magic: " + str(nuke))
    print("White/Red Healing Magic: " + str(heal))

    if nuke and heal:
        magicConditions = True
    return magicConditions

for stat in range (0, 5):
    print(attributes[stat])
    checkPartyStats(ff_classes, stat)

magicInParty = checkMagic(choice1, choice2, choice3, choice4)
individualPartyMemberStats = checkPartyStats(ff_classes, stat)


if totalStats >= 60 and magicInParty and individualPartyMemberStats:
    print("The party is optimal!")
else:
    print("the party is not optimal, but still playable.")
