"""
==================================================
    Filename:   discard.py

 Description:   Optimal discard algorithm

     Version:   1.0
     Created:   2017-01-13
    Revision:   none
    Compiler:   python 3.5

      Author:   David Amirault
==================================================
"""

# The vast majority of hands are easy to decide what to do with
# Here are some of the problematic ones:
# pair vs flush draw
# pair vs (open or closed) straight draw
# pair vs two off from flush
# (low) pocket pair vs nothing in flop
# The above hands can have zero, one, or two free hole cards, depending
#
# Solution: pass a safety value to the discard function to specify the extent
# to which we are willing to break pairs to hunt for something better


def suitmult(cards, card):
    """Number of cards with the same suit as card"""
    return len([c for c in cards if c[0] == card[0]])


def suitdistro(board):
    """Splits up the cards by suit"""
    distro = [0] * 4
    for card in board:
        distro[card[0]] += 1
    return distro


def flopflush(board, hole, utility):
    """
    Hands to be considered:
    flush
    flush draw (one free hole card) 58.6%
    flush draw (zero free hole cards) 39.0%
    two off from flush (two free hole cards) 19.4%
    two off from flush (one free hole card) 16.6%
    """
    distro = suitdistro(board)
    potential = max(distro)
    suit = distro.index(potential)
    if potential == 3:
        if hole[0][0] == suit and hole[1][0] == suit:  # flush
            utility[0] += 100
            utility[1] += 100
        elif hole[0][0] == suit:  # flush draw (one free)
            utility[1] -= 80
        elif hole[1][0] == suit:
            utility[0] -= 80
        else:  # two off from flush (two free)
            utility[0] -= 6
            utility[1] -= 6
    elif potential == 2:
        if hole[0][0] == suit and hole[1][0] == suit:  # flush draw (zero free)
            utility[0] += 80
            utility[1] += 80
        elif hole[0][0] == suit:  # two off from flush (one free)
            utility[1] -= 6
        elif hole[1][0] == suit:
            utility[0] -= 6
    return utility


def valuemult(cards, card):
    """Number of cards with the same value as card"""
    return len([c for c in cards if c[1] == card[1]])


def valuedistro(board, hole=None):
    """Splits up the cards by value, with multiplicity"""
    distro = [0] * 13
    if hole is not None:
        distro[hole[0][1]] += 0.6  # distinguishes hole cards
        distro[hole[1][1]] += 0.8
    for card in board:
        distro[card[1]] += 1
    return distro


def straightdistro(board, hole=None):
    """Splits up the cards by value, no multiplicity"""
    distro = [0] * 13
    if hole is not None:
        distro[hole[0][1]] = 0.6
        distro[hole[1][1]] = 0.8
    for card in board:
        distro[card[1]] = 1
    distro.insert(0, distro[-1])  # aces can be low or high
    return distro


def straightval(cards):
    """Checks for existence and value of straight"""
    distro = straightdistro(cards)
    for ind in range(9, -1, -1):
        test = sum(distro[ind:ind + 5])
        if test == 5:
            return ind + 1
    return 0


def straightpotential(board, hole):
    """Differentiates types of straights"""
    distro = straightdistro(board, hole)
    best = 0
    for ind in range(10):
        test = sum(distro[ind:ind + 5])
        inner = ((ind != 0 or distro[ind] == 0) and
                 (ind != 9 or distro[ind + 4] == 0)) or test > 4
        if (test > 3 and inner and distro[ind + 1] > 0 and
                distro[ind + 2] > 0 and distro[ind + 3] > 0):
            test += 1  # distinguishes open and closed straight draws
        best = max(best, test)
    return best


def flopstraight(board, hole, utility, safety):
    """
    Hands to be considered:
    straight
    open straight draw (one free hole card) 53.9%
    open straight draw (zero free hole cards) 31.5%
    closed straight draw (one free hole card) 30.8%
    closed straight draw (zero free hole cards) 16.5%
    """
    potential = straightpotential(board, hole)
    if potential > 5:  # straight
        utility[0] += 100
        utility[1] += 100
    elif potential > 4.5:  # open straight draw (one free)
        utility[int(potential < 4.7)] -= 40
    elif potential > 4:  # open straight draw (zero free)
        utility[0] += 40
        utility[1] += 40
    elif potential > 3.5:  # closed straight draw (one free)
        utility[int(potential < 3.7)] -= 20
    elif potential > 3:  # closed straight draw (zero free)
        utility[0] += 8 - safety
        utility[1] += 8 - safety
    return utility


def messypair(spec, board, hole, utility, safety):
    """Sorts out messy two pair and pair hands"""
    if spec > 1.9:
        return utility
    util = hole[0][1]
    if spec > 1.7:
        util = hole[1][1]
    status = len([c for c in board if c[1] < util])
    util += status + safety
    if spec > 1.5:
        utility[int(spec > 1.7)] += util  # yes this should be >
    else:
        utility[0] += util - 5
        utility[1] += util - 5
    return utility


def flopfours(specs, utility):
    """Four of a kind"""
    if specs[0] > 3.5:
        utility[int(specs[0] < 3.7)] -= 100  # to bluff a weaker hand
    else:
        utility[0] += 100
        utility[1] += 100
    return utility


def flopthrees(specs, utility):
    """Full house, three of a kind"""
    if specs[1] > 1:  # full house
        utility[0] += 100
        utility[1] += 100
    elif specs[0] > 2.9:  # three of a kind
        utility[0] -= 5
        utility[1] -= 5
    elif specs[0] > 2.5:
        utility[int(specs[0] < 2.7)] -= 100
    else:
        utility[0] += 100
        utility[1] += 100
    return utility


def floptwos(specs, board, hole, utility, safety):
    """Two pair, pair"""
    if specs[0] > 1.9 and specs[1] > 1.5:  # two pair
        utility[int(specs[1] < 1.7)] -= 100
    elif specs[1] > 1:
        utility[0] += 100
        utility[1] += 100
    else:  # pair
        utility = messypair(specs[0], board, hole, utility, safety)
    return utility


def floppair(board, hole, utility, safety):
    """
    Hands to be considered:
    four of a kind
    full house
    three of a kind
    two pair
    pair
    """
    distro = sorted(valuedistro(board, hole))
    specs = [distro.pop(), distro.pop()]
    if specs[0] > 3:
        utility = flopfours(specs, utility)
    elif specs[0] > 2:
        utility = flopthrees(specs, utility)
    elif specs[0] > 1:
        utility = floptwos(specs, board, hole, utility, safety)
    return utility


def decide(board, hole, utility):
    """Chooses what to discard based on utility"""
    if min(utility) <= 0:
        if utility[0] == utility[1]:
            if hole[0][1] == hole[1][1]:
                return hole[int(suitmult(board, hole[0]) >
                                suitmult(board, hole[1]))]
            return hole[int(hole[0][1] > hole[1][1])]
        return hole[int(utility[0] > utility[1])]
    return None


def flop(board, hole, safety):
    """safety = 1 is the default"""
    utility = [0, 0]  # keeps track of importance of hole cards
    utility = flopflush(board, hole, utility)
    utility = flopstraight(board, hole, utility, safety)
    utility = floppair(board, hole, utility, safety)
    return decide(board, hole, utility)


def freedomflush(board, hole, utility, suit):
    """Flush with freedom, flush, flush draw (two free)"""
    if hole[0][0] == suit and hole[1][0] == suit:  # flush with freedom
        pot = straightpotential(board, hole)
        split = sorted([hole[0][1], hole[1][1]])
        if pot > 5.5:  # straight flush
            utility[int(pot < 5.7)] -= 200  # to bluff a weaker hand
        elif pot > 5:
            utility[0] += 200
            utility[1] += 200
        elif (len([c for c in board if split[0] < c[1] and c[1] < split[1]]) ==
              abs(hole[0][1] - hole[1][1]) - 1) and pot - int(pot) > 0.5:
            utility[int(pot - int(pot) < 0.7)] -= 200
            # hole cards are equivalent; go for the straight flush
        else:
            utility[int(hole[0][1] > hole[1][1])] -= 200
    elif hole[0][0] == suit:  # flush
        utility[1] -= 200
    elif hole[1][0] == suit:
        utility[0] -= 200
    else:  # flush draw (two free)
        utility[0] -= 80
        utility[1] -= 80
    return utility


def turnflush(board, hole, utility):
    """
    Hands to be considered:
    flush with freedom
    flush
    flush draw (one free hole card) 35.7%
    flush draw (two free hole cards) 19.6%
    flush draw (zero free hole cards) 19.6%
    """
    distro = suitdistro(board)
    potential = max(distro)
    suit = distro.index(potential)
    if potential == 4:
        utility = freedomflush(board, hole, utility, suit)
    elif potential == 3:
        if hole[0][0] == suit and hole[1][0] == suit:  # flush
            utility[0] += 200
            utility[1] += 200
        elif hole[0][0] == suit:  # flush draw (one free)
            utility[1] -= 80
        elif hole[1][0] == suit:
            utility[0] -= 80
        else:  # two off from flush (two free)
            utility[0] -= 6
            utility[1] -= 6
    elif potential == 2:
        if max(suitdistro(board + hole)) == 4:  # flush draw (zero free)
            utility[0] += 80
            utility[1] += 80
        else:
            if suitmult(board, hole[0]) == 2:  # two off from flush (one free)
                utility[1] -= 6
            if suitmult(board, hole[1]) == 2:
                utility[0] -= 6
    return utility


def freedomstraight(board, hole, utility):
    """Straight with freedom, straight"""
    works = [straightval(board + [hole[0]]),
             straightval(board + [hole[1]]),
             straightval(board + hole)]
    if works[0] and works[1]:  # straight with freedom
        utility[int(works[0] > works[1])] -= 40
    elif works[0]:
        utility[0] += 100
        if works[2] > works[0] or suitmult(board, hole[1]) == 3:
            utility[1] += 40
        else:
            utility[1] -= 40
    elif works[1]:
        utility[1] += 100
        if works[2] > works[1] or suitmult(board, hole[0]) == 3:
            utility[0] += 40
        else:
            utility[1] -= 40
    else:  # straight
        utility[0] += 100
        utility[1] += 100
    return utility


def turnstraight(board, hole, utility, safety):
    """
    Hands to be considered:
    straight with freedom
    straight
    open straight draw (one free hole card) 32.1%
    open straight draw (zero free hole cards) 17.4%
    open straight draw (two free hole cards) 17.4%
    closed straight draw (one free hole card) 16.8%
    closed straight draw (zero free hole cards) 8.7%
    closed straight draw (two free hole cards) 8.7%
    """
    potential = straightpotential(board, hole)
    if potential > 5:
        utility = freedomstraight(board, hole, utility)
    elif potential > 4.9:  # open straight draw (two free)
        utility[0] -= 40
        utility[1] -= 40
    elif potential > 4.5:  # open straight draw (one free)
        utility[int(potential < 4.7)] -= 40
    elif potential > 4:  # open straight draw (zero free)
        utility[0] += 40
        utility[1] += 40
    elif potential > 3.9:  # closed straight draw (two free)
        utility[0] -= 20
        utility[1] -= 20
    elif potential > 3.5:  # closed straight draw (one free)
        utility[int(potential < 3.7)] -= 20
    elif potential > 3:  # closed straight draw (zero free)
        utility[0] += 8 - safety
        utility[1] += 8 - safety
    return utility


def turnfours(specs, hole, utility):
    """Four of a kind"""
    if specs[0] > 3.9:
        utility[int(hole[0][1] > hole[1][1])] -= 100
    elif specs[0] > 3.5:
        utility[int(specs[0] < 3.7)] -= 100  # to bluff a weaker hand
    else:
        utility[0] += 100
        utility[1] += 100
    return utility


def turnthrees(specs, hole, utility):
    """Full house, three of a kind"""
    if specs[1] > 2.5:  # full house
        utility[int(hole[0][1] > hole[1][1])] -= 100
    elif specs[1] > 1:
        utility[0] += 100
        utility[1] += 100
    elif specs[0] > 2.9:  # three of a kind
        utility[0] -= 5
        utility[1] -= 5
    elif specs[0] > 2.5:
        utility[int(specs[0] < 2.7)] -= 100
    else:
        utility[0] += 100
        utility[1] += 100
    return utility


def turntwos(specs, board, hole, utility, safety):
    """Two pair, pair"""
    if specs[2] > 1:  # three pair
        utility[0] += 100
        utility[1] += 100
    elif specs[0] > 1.9 and specs[1] > 1.9:  # two pair
        utility[0] -= 5
        utility[1] -= 5
    elif specs[0] > 1.9 and specs[1] > 1.5:
        utility[int(specs[1] < 1.7)] -= 100
    elif specs[1] > 1:
        utility[0] += 100
        utility[1] += 100
        # utility = messypair(specs[0], board, hole, utility, safety)
        # utility = messypair(specs[1], board, hole, utility, safety)
        # utility[0] += 30
        # utility[1] += 30
    else:  # pair
        utility = messypair(specs[0], board, hole, utility, safety)
    return utility


def turnpair(board, hole, utility, safety):
    """
    Hands to be considered:
    four of a kind
    full house
    three of a kind
    two pair
    pair
    """
    distro = sorted(valuedistro(board, hole))
    specs = [distro.pop(), distro.pop(), distro.pop()]
    if specs[0] > 3:
        utility = turnfours(specs, hole, utility)
    elif specs[0] > 2:
        utility = turnthrees(specs, hole, utility)
    elif specs[0] > 1:
        utility = turntwos(specs, board, hole, utility, safety)
    return utility


def turn(board, hole, safety):
    """safety = 1 is the default"""
    utility = [0, 0]
    utility = turnflush(board, hole, utility)
    utility = turnstraight(board, hole, utility, safety)
    utility = turnpair(board, hole, utility, safety)
    return decide(board, hole, utility)


def handcode(cards):
    """High card: 0, pair: 1, etc"""
    code = 0
    distro = sorted(valuedistro(cards))
    specs = [distro.pop(), distro.pop()]
    distro = suitdistro(cards)
    potential = max(distro)
    suit = distro.index(potential)
    if potential >= 5:
        code = 5
        suited = [c for c in cards if c[0] == suit]
        if straightval(suited):
            code = 8
    elif straightval(cards):
        code = 4
    elif specs[0] == 4:
        code = 7
    elif specs[0] == 3:
        code = 3
        if specs[1] >= 2:
            code = 6
    elif specs[0] == 2:
        code = 1
        if specs[1] == 2:
            code = 2
    return code
