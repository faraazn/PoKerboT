"""
==================================================
    Filename:   discardodds.py

 Description:   Probabilities of four discard outcomes

     Version:   1.0
     Created:   2017-01-13
    Revision:   none
    Compiler:   python 3.5

      Author:   David Amirault
==================================================
"""

import random
import simplediscard
import discard


def verboseplay(deck):
    """Returns more info"""
    random.shuffle(deck)
    hand, table = deck[:2], deck[2:5]
    tossed = [False, False]
    for ind in range(2):
        toss = simplediscard.flush(hand, table, [0, 0])
        toss = simplediscard.straight(hand, table, toss)
        toss = simplediscard.pair(hand, table, toss)
        if max(toss) >= 0:
            tossed[ind] = True
            if toss[0] == toss[1]:
                hand[int(hand[0][1] > hand[1][1])] = deck[7 + ind]
            else:
                hand[int(toss[0] < toss[1])] = deck[7 + ind]
        table = deck[2:6 + ind]
    return tossed, hand + table


def verbosesmartplay(deck):
    """Returns more info"""
    random.shuffle(deck)
    board, hole = deck[2:5], deck[:2]
    tossed = [False, False]
    toss = discard.flop(board, hole, 1)
    if toss is not None:
        tossed[0] = True
        if toss == hole[0]:
            hole[0] = deck[7]
        elif toss == hole[1]:
            hole[1] = deck[7]
    board = deck[2:6]
    toss = discard.turn(board, hole, 1)
    if toss is not None:
        tossed[1] = True
        if toss == hole[0]:
            hole[0] = deck[8]
        elif toss == hole[1]:
            hole[1] = deck[8]
    board = deck[2:7]
    return tossed, hole + board


def discardodds():
    """Plays 10 ** 5 hands"""
    deck, discards = [], []
    for ind1 in range(4):
        for ind2 in range(13):
            deck.append((ind1, ind2))
        discards.append([0, 0])
    for _ in range(10 ** 5):
        meta = verbosesmartplay(deck)
        tossed, cards = meta[0], meta[1]
        option = tossed[0] * 2 + tossed[1]
        discards[option][0] += 1
        discards[option][1] += discard.handcode(cards)
    for data in discards:
        print(str(data[0] / 10 ** 3) + ': ' + str(data[1] / data[0]))

discardodds()
