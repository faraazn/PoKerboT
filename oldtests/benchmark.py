"""
==================================================
    Filename:   benchmark.py

 Description:   For improving discard.py

     Version:   1.0
     Created:   2017-01-18
    Revision:   none
    Compiler:   python 3.5

      Author:   David Amirault
==================================================
"""

import random
import simplediscard
import discard


def play(deck):
    """Plays one hand with discards"""
    random.shuffle(deck)
    hand, table = deck[:2], deck[2:5]
    for ind in range(2):
        toss = simplediscard.flush(hand, table, [0, 0])
        toss = simplediscard.straight(hand, table, toss)
        toss = simplediscard.pair(hand, table, toss)
        if max(toss) >= 0:
            if toss[0] == toss[1]:
                hand[int(hand[0][1] > hand[1][1])] = deck[7 + ind]
            else:
                hand[int(toss[0] < toss[1])] = deck[7 + ind]
        table = deck[2:6 + ind]
    return hand + table


def smartplay(deck):
    """Plays one hand with smart discards"""
    random.shuffle(deck)
    board, hole = deck[2:5], deck[:2]
    toss = discard.flop(board, hole, 1)
    if toss is not None:
        if toss == hole[0]:
            hole[0] = deck[7]
        elif toss == hole[1]:
            hole[1] = deck[7]
    board = deck[2:6]
    toss = discard.turn(board, hole, 1)
    if toss is not None:
        if toss == hole[0]:
            hole[0] = deck[8]
        elif toss == hole[1]:
            hole[1] = deck[8]
    board = deck[2:7]
    return hole + board


def benchmark():
    """Plays 10 ** 5 hands"""
    deck = []
    for ind1 in range(4):
        for ind2 in range(13):
            deck.append((ind1, ind2))
    codes = [0] * 9
    smartcodes = [0] * 9
    for _ in range(10 ** 5):
        codes[discard.handcode(play(deck))] += 1
        smartcodes[discard.handcode(smartplay(deck))] += 1
    print([c / 10 ** 3 for c in codes])
    print([c / 10 ** 3 for c in smartcodes])

benchmark()
