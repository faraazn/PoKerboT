"""
==================================================
    Filename:   simplediscard.py

 Description:   Old discard alg

     Version:   1.0
     Created:   2017-01-18
    Revision:   none
    Compiler:   python 3.5

      Author:   David Amirault
==================================================
"""


def multiplicity(cards, card):
    """Number of cards with the same value as card"""
    return len([c for c in cards if c[1] == card[1]])


def pair(hand, table, toss):
    """Also includes two pairs, three of a kind, etc"""
    if multiplicity(table, hand[0]) > 1:
        toss[0] -= 45
    if multiplicity(table, hand[1]) > 1:
        toss[1] -= 45
    if multiplicity(table, hand[0]) == 1 and multiplicity(table, hand[1]) == 1:
        toss[0] -= 45
        toss[1] -= 45
    else:  # bad two pairs at best
        if multiplicity(hand + table, hand[0]) == 2:
            toss[0] -= hand[0][1] + 1
        if multiplicity(hand + table, hand[1]) == 2:
            toss[1] -= hand[1][1] + 1
    return toss


def straightcount(cards):
    """Number of cards contributing to a straight"""
    values = [0] * 13
    for card in cards:
        values[card[1]] = 1
    values.insert(0, values[-1])
    best = 0
    for ind in range(10):
        test = sum(values[ind:ind + 5])
        if (test >= 4 and values[ind + 1] == 1 and
                values[ind + 2] == 1 and values[ind + 3] == 1):
            test += 1  # distinguish between open and closed straight draws
        best = max(best, test)
    return best


def straight(hand, table, toss):
    """Straight odds analysis"""
    scount = straightcount(hand + table)
    if scount == 6:  # straight
        toss[0] -= 45
        toss[1] -= 45
    elif scount == 5:  # open straight draw
        if straightcount([hand[0]] + table) == 4:
            toss[1] += 15
        elif straightcount([hand[1]] + table) == 4:
            toss[0] += 15
        else:
            toss[0] -= 15
            toss[1] -= 15
    elif scount == 4:  # closed straight draw
        if straightcount(table) == 4:
            toss[0] += 5
            toss[1] += 5
        elif straightcount([hand[0]] + table) == 4:
            toss[1] += 5
        elif straightcount([hand[1]] + table) == 4:
            toss[0] += 5
    return toss


def flushcount(cards):
    """Number of same-suited cards"""
    suits = [0] * 4
    for card in cards:
        suits[card[0]] += 1
    return max(suits)


def flush(hand, table, toss):
    """Flush odds analysis"""
    fcount = flushcount(hand + table)
    if fcount >= 5:  # flush
        toss[0] -= 45
        toss[1] -= 45
    elif fcount == 4:  # flush draw
        if flushcount([hand[0]] + table) == 4:
            toss[1] += 30
        elif flushcount([hand[1]] + table) == 4:
            toss[0] += 30
        else:
            toss[0] -= 30
            toss[1] -= 30
    return toss


def distribution(cards):
    """Splits up the cards by value"""
    distro = [0] * 13
    for card in cards:
        distro[card[1]] += 1
    distro = sorted(distro)
    return [distro.pop(), distro.pop()]
