#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


def play(deck):
    """Plays one hand with discards"""
    random.shuffle(deck)
    hand, table = deck[:2], deck[2:5]
    for ind in range(2):
        toss = simplediscard.flush(hand, table, [0, 0])  # higher means toss it
        toss = simplediscard.straight(hand, table, toss)
        toss = simplediscard.pair(hand, table, toss)
        if max(toss) >= 0:
            if toss[0] == toss[1]:
                hand[int(hand[0][1] > hand[1][1])] = deck[7 + ind]
            else:
                hand[int(toss[0] < toss[1])] = deck[7 + ind]
        table = deck[2:6 + ind]
    # print(hand)
    # print(table)
    return hand + table


def benchmark():
    """Plays 10 ** 5 hands"""
    deck = []
    for ind1 in range(4):
        for ind2 in range(13):
            deck.append((ind1, ind2))
    codes = [0] * 9
    for _ in range(10 ** 5):
        codes[simplediscard.handcode(play(deck))] += 1
    print([c / 10 ** 3 for c in codes])

benchmark()
