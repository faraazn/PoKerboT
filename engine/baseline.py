"""
==================================================
    Filename:   baseline.py

 Description:   Useful general functions

     Version:   1.0
     Created:   2017-01-19
    Revision:   none
    Compiler:   python 3.5

      Author:   David Amirault,
                Faraaz Nadeem,
                Nilai Sarda,
                Arman Talkar
==================================================
"""

import discard


SUITS = ['c', 'd', 'h', 's']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']


def totuple(strcard):
    """Ac -> (0, 12)"""
    return (SUITS.index(strcard[1]), VALUES.index(strcard[0]))


def tostr(tuplecard):
    """(0, 12) -> Ac"""
    return VALUES[tuplecard[1]] + SUITS[tuplecard[0]]


def flushcode(board, hole):
    """2-, 2a, 2b, 2ab, 3, 3a, 3b, 3ab, 4, 4a, 4b, 4ab, 5, 5a, 5b, 5ab"""
    code = 0
    distro = discard.suitdistro(board)
    potential = max(distro)
    suit = distro.index(potential)
    suit2 = 3 - distro[::-1].index(potential)
    if potential >= 2:
        code = 4 * (potential - 2)
        if hole[0][0] == suit or hole[0][0] == suit2:
            code += 1 + int(hole[0][1] > hole[1][1])
        if hole[1][0] == suit or hole[1][0] == suit2:
            code += 1 + int(hole[0][1] < hole[1][1])
    return code
