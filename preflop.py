#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
==================================================
    Filename:   hands.py

 Description:   Pre-flop hand odds

     Version:   1.0
     Created:   2017-01-11
    Revision:   none
    Compiler:   python 3.5

      Author:   David Amirault
==================================================
"""

import random
import hands


def winner(hand1, hand2):
    """True: hand1 wins"""
    code1 = hands.handcode(hand1)
    code2 = hands.handcode(hand2)
    if code1 > code2:
        return True
    if code1 < code2:
        return False
    card1 = max(hand1[0][1], hand1[1][1])
    card2 = max(hand2[0][1], hand2[1][1])
    if card1 > card2:
        return True
    if card1 < card2:
        return False
    # Note: this ghetto approximation gets lots of hands wrong
    return min(hand1[0][1], hand1[1][1]) >= min(hand2[0][1], hand2[1][1])


def twoplay(deck):
    """Plays two hand with discards"""
    random.shuffle(deck)
    hand, table = [deck[:2], deck[2:4]], deck[4:7]
    for ind1 in range(2):
        for ind2 in range(2):
            toss = hands.flush(hand[ind2], table, [0, 0])
            toss = hands.straight(hand[ind2], table, toss)
            toss = hands.pair(hand[ind2], table, toss)
            if max(toss) >= 0:
                if toss[0] == toss[1]:
                    hand[ind2][int(hand[ind2][0][1] > hand[ind2][1][1])] = \
                            deck[9 + 2 * ind1 + ind2]
                else:
                    hand[ind2][int(toss[0] < toss[1])] = \
                            deck[9 + 2 * ind1 + ind2]
        table = deck[4:8 + ind1]
    return hand[0] + table, hand[1] + table


def preflop():
    """Plays 10 ** 6 hands"""
    deck = []
    for ind1 in range(4):
        for ind2 in range(13):
            deck.append((ind1, ind2))
    preflopping = [[[[0, 0], [0, 0]] for i in range(13)] for j in range(13)]
    for _ in range(5 * 10 ** 5):
        hand1, hand2 = twoplay(deck)
        if hand1[0][0] == hand1[1][0]:
            preflopping[hand1[0][1]][hand1[1][1]][1][1] += 1
            if winner(hand1, hand2):
                preflopping[hand1[0][1]][hand1[1][1]][1][0] += 1
        else:
            preflopping[hand1[0][1]][hand1[1][1]][0][1] += 1
            if winner(hand1, hand2):
                preflopping[hand1[0][1]][hand1[1][1]][0][0] += 1
    for ind2 in range(2):
        print()
        for ind3 in range(13):
            line = ''
            for ind4 in range(13):
                ans = -1
                if preflopping[ind3][ind4][ind2][1] != 0:
                    ans = round(preflopping[ind3][ind4][ind2][0] /
                                preflopping[ind3][ind4][ind2][1], 4)
                line += str(ans).ljust(7)
            print(line)

preflop()
