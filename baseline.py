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

SUITS = ['c', 'd', 'h', 's']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']


def totuple(strcard):
    """Ac -> (0, 12)"""
    return (SUITS.index(strcard[1]), VALUES.index(strcard[0]))


def tostr(tuplecard):
    """(0, 12) -> Ac"""
    return VALUES[tuplecard[1]] + SUITS[tuplecard[0]]
