#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
==================================================
    Filename:   discardodds.py

 Description:   Chance of four discard outcomes

     Version:   1.0
     Created:   2017-01-13
    Revision:   none
    Compiler:   python 3.5

      Author:   David Amirault
==================================================
"""

import random
import hands


def verboseplay(deck):
    """Returns more info"""
    random.shuffle(deck)
    hand, table = deck[:2], deck[2:5]
    tossed = [False, False]
    for ind in range(2):
        toss = hands.flush(hand, table, [0, 0])
        toss = hands.straight(hand, table, toss)
        toss = hands.pair(hand, table, toss)
        if max(toss) >= 0:
            tossed[ind] = True
            if toss[0] == toss[1]:
                hand[int(hand[0][1] > hand[1][1])] = deck[7 + ind]
            else:
                hand[int(toss[0] < toss[1])] = deck[7 + ind]
        table = deck[2:6 + ind]
    return tossed, hand + table


def discardodds():
    """Plays 10 ** 6 hands"""
    deck, discards = [], []
    for ind1 in range(4):
        for ind2 in range(13):
            deck.append((ind1, ind2))
        discards.append([0, 0])
    for _ in range(10 ** 6):
        meta = verboseplay(deck)
        tossed, cards = meta[0], meta[1]
        option = tossed[0] * 2 + tossed[1]
        discards[option][0] += 1
        discards[option][1] += hands.handcode(cards)
    for data in discards:
        print(str(data[0] / 10 ** 4) + ': ' + str(data[1] / data[0]))

discardodds()
