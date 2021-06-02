import math
from random import randint

# Todo crit is +15 now
def chanceCrits(choice = 1, Attacker = 4, Defender = (6,12),rolls=10000, outputResultOnly=False):
    # Choice 0: Stand Still
    # Choice 1: Run zigzag
    # Choice 2: Run dodge

    # AgiD is Agility of defender for dodging
    # deflectionD is deflection of defender from armor
    AgiD, deflectionD = Defender
    # hitA is hitbonus of attacker
    hitA = Attacker

    # Accumulator for number of hits
    crits = 0
    type=""
    if choice < 0 or choice > 2: raise ValueError
    elif choice == 0:
        # Stand still, only deflection
        type = "MELEE/RANGE, Stand still, only deflection"
        for i in range(rolls):
            resA = randint(1, 20) + hitA
            if deflectionD <= resA-10:
                crits += 1
    elif choice == 1:
        # Run zigzag => +4 deflection for projectiles
        type = "RANGE, run zigzag"
        deflectionD += 4
        for i in range(rolls):
            resA = randint(1, 20) + hitA
            if deflectionD <= resA-10:
                crits += 1
    elif choice == 2:
        # dodge attack, roll for dodge
        type = "MELEE/RANGE, dodge attack"
        for i in range(rolls):
            resD = randint(1, 20) + AgiD
            resA = randint(1, 20) + hitA
            if max(resD, deflectionD) <= resA-10:
                crits += 1
    if not outputResultOnly:
        text = "For: {}\nAttacker crit:{}, Defender agility: {}, deflection: {}\nrolls: {}, crits: {}, chance for crit: {}%\n".\
            format(type.upper(), hitA, AgiD, deflectionD , rolls,crits, 100*crits/rolls)
        print(text)
        return text
    else:
        print(crits/rolls)
        return crits/rolls



def chanceHits(choice = 1, Attacker = 4, Defender = (6,12),rolls=10000,outputResultOnly=False):
    # Choice 0: Stand Still
    # Choice 1: Run zigzag
    # Choice 2: Run dodge

    # AgiD is Agility of defender for dodging
    # deflectionD is deflection of defender from armor
    AgiD, deflectionD = Defender
    # hitA is hitbonus of attacker
    hitA = Attacker

    # Accumulator for number of hits
    hits = 0
    type=""
    if choice < 0 or choice > 2: raise ValueError
    elif choice == 0:
        # Stand still, only deflection
        type = "MELEE/RANGE, Stand still, only deflection"
        for i in range(rolls):
            if deflectionD < randint(1, 20) + hitA: hits += 1
    elif choice == 1:
        # Run zigzag => +4 deflection for projectiles
        type = "RANGE, run zigzag"
        deflectionD += 4
        for i in range(rolls):
            if deflectionD < randint(1, 20) + hitA: hits += 1
    elif choice == 2:
        # dodge attack, roll for dodge
        type = "MELEE/RANGE, dodge attack"
        for i in range(rolls):
            if max(randint(1, 20) + AgiD, deflectionD) < randint(1, 20) + hitA: hits += 1
    if not outputResultOnly:
        text = "For: {}\nAttacker hit:{}, Defender agility: {}, deflection: {}\nrolls: {}, hits: {}, chance for hit: {}%\n".\
            format(type.upper(), hitA, AgiD, deflectionD , rolls,hits, 100*hits/rolls)
        print(text)
        return text
    else:
        print(hits/rolls)
        return hits/rolls


def rollDice(die, mod, exploding):
    roll = randint(1,die)
    while roll % die ==0 and exploding:
        roll += randint(1,die)
    return roll+mod

def avgDmgParry2(Attacker=(3,8,6,True), Defender=(9, 10, 11), rolls=10000):
    A_dmgMod,A_dmgDie,A_hitMod,A_exploding = Attacker
    D_dmgModAndDR, D_dmgDie, D_deflection= Defender

    critRate = 15

    hits,crits, overCrits = 0,0,0
    hitDmg, critDmg, overCritDmg  = 0,0,0
    pains = 0

    # dmgAfterParryTotal, dmgAfterParryCritTotal, dmgAfterNonCritParryTotal = 0,0,0
    # timesTakingDmg = 0
    for i in range(rolls):
        # Attacker rolls
        resA = rollDice(20,A_hitMod,A_exploding)

        a = A_dmgDie
        # math.floor((resA - D_deflection) / critRate)
        if resA >=D_deflection + 2*15:
            overCrits += 1
            A = rollDice(a, A_dmgMod, True) + rollDice(a, 0, True) + rollDice(a, 0, True)
            D = rollDice(D_dmgDie, D_dmgModAndDR,False)
            hitDmg += max(0, A - D)
            pains += max(0, A - D) > 0
        elif resA >=D_deflection + 15:
            crits += 1
            A = rollDice(a, A_dmgMod, True) + rollDice(a, 0, True)
            D = rollDice(D_dmgDie, D_dmgModAndDR, False)
            critDmg += max(0, A - D)
            pains += max(0, A - D) > 0
        elif resA > D_deflection:
            hits += 1
            A = rollDice(a, A_dmgMod, True)
            D = rollDice(D_dmgDie, D_dmgModAndDR, False)
            overCritDmg += max(0, A - D)
            pains += max(0, A - D) > 0

        # If hit do these things, otherwise "continue" loop
        # if resA > D_deflection:
        #     hits += 1
        #     crits = crits+1 if resA >= D_deflection+critRate else crits
        #
        #     # Ex for a 1d8 damage weapon and we performe a crit
        #     # Ex deflection 10, roll 26 => 16 over deflect => 1 + floor(16/15) = rolls 2d8 for damage + modifier
        #     nrOfDiceLeft =1 + math.floor((resA-D_deflection-1)/critRate) # critRate = 15
        #
        #
        #     for i in range(nrOfDiceLeft):
        #         A = rollDice(A_dmgDie, 0, True)
        #     A += A_dmgMod
        #
        #
        #     # resA_Dmg = A+A_dmgMod
        #     resD_Dmg = randint(1, D_dmgDie) + D_dmgModAndDR
        #     dmgAfterParryTotal += max(0, resA_Dmg-resD_Dmg)
        #
        #
        #
        #     if max(0, resA_Dmg-resD_Dmg) > 0:
        #         timesTakingDmg +=1
        #     if resA >= D_deflection + critRate:
        #         dmgAfterParryCritTotal += max(0, resA_Dmg-resD_Dmg)
        #         # testList.append(max(0, resA_Dmg-resD_Dmg))
        #     else:
        #         dmgAfterNonCritParryTotal += max(0, resA_Dmg-resD_Dmg)

    # testList.sort()
    # for e in testList:
    #     print(e)
    # A_dmgMod, A_dmgDie, A_hitMod, A_exploding = Attacker
    # D_dmgMod, D_dmgDie, D_deflection = Defender
    text = "ATTACKER with a piercing[{}] weapon: 1d{}+{} and hitbonus: {},\n" \
           "DEFENDER parrying with a 1d{}+{} and deflection: {}\n" \
           "Rounds: {}, hits: {}, crits: {},\n" \
           "chance for hit: {:.2f}%, Average Hit damage: {:.2f},\n" \
           "chance for crit: {:.2f}%, average crit damage: {:.2f}\n" \
           "chance for overcrit: {:.2f}%, average overcrit damage: {:.2f}\n" \
           "Chance taking damage: {:.2f}%, Chance taking damage given a hit occurs: {:.2f}%.\n" \
           "Average damage per round: {:.2f}". \
        format(A_exploding,A_dmgDie,A_dmgMod,A_hitMod,
               D_dmgDie,D_dmgModAndDR,D_deflection,
               rolls, hits, crits,
               100 * hits / rolls, hitDmg/hits,
               100 * crits / rolls, critDmg/crits,
               100 * overCrits / rolls, overCritDmg/crits,
               100*(pains) / rolls, 100*pains/(hits + crits + overCrits),
               (hitDmg + critDmg + overCritDmg) / rolls, )
    print(text)

    return text


if __name__ == "__main__":
    # Choice 0: Stand Still
    # Choice 1: Run zigzag
    # Choice 2: Run dodge
    # chanceHits(choice=0, Attacker=4, Defender=(6, 12), rolls=10000,outputResultOnly=True)
    # chanceCrits(choice=0, Attacker=4, Defender=(6, 12), rolls=10000,outputResultOnly=True)


    #     A_dmgMod, A_dmgDie, A_hitMod, A_exploding = Attacker
    #     D_dmgModAndDR, D_dmgDie, D_deflection= Defender
    # Note D_dmgModAndDR = dmgMod/2 + DR

    avgDmgParry2(Attacker=(3, 8, 6, True), Defender=(6, 10, 11), rolls=100000)