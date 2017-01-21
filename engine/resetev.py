"""
==================================================
    Filename:   resetev.py

 Description:   Be careful, this could delete data

     Version:   1.0
     Created:   2017-01-21
    Revision:   none
    Compiler:   python 3.5

      Author:   David Amirault
==================================================
"""

from collections import Counter
import pickle
import baseline


def ping():
    """Checks how ev.pickle looks"""
    with open('ev.pickle', 'rb') as handle:
        ev = pickle.load(handle)
    print(Counter([v[1] for v in ev.values()]))


def combine():
    """Combines hero.pickle and villain.pickle"""
    with open('hero.pickle', 'rb') as handle:
        ev = pickle.load(handle)
    with open('villain.pickle', 'rb') as handle:
        ev2 = pickle.load(handle)
    for key in ev:
        ev[key][0] += ev2[key][0]
        ev[key][1] += ev2[key][1]
    with open('ev.pickle', 'wb') as handle:
        pickle.dump(ev, handle, protocol=pickle.HIGHEST_PROTOCOL)


def reset():
    """Cleans up hero.pickle, villain.pickle"""
    ev = {}
    for ind1 in range(13):
        for ind2 in range(ind1, 13):
            for ind3 in range(ind2, 13):
                for ind4 in range(ind3, 13):
                    for ind5 in range(ind4, 13):
                        if ind5 != ind1:
                            for ind6 in range(13):
                                if not ((ind6 == ind5 and ind6 == ind2) or (ind6 == ind4 and ind6 == ind1)):
                                    for ind7 in range(ind6, 13):
                                        if not ((ind7 == ind6 and ((ind7 == ind5 and ind7 == ind3) or (ind7 == ind4 and ind7 == ind2) or (ind7 == ind3 and ind7 == ind1))) or (ind7 != ind6 and ((ind7 == ind5 and ind7 == ind2) or (ind7 == ind4 and ind7 == ind1)))):
                                            distinct = 1
                                            if ind2 != ind1:
                                                distinct += 1
                                            if ind3 != ind2:
                                                distinct += 1
                                            if ind4 != ind3:
                                                distinct += 1
                                            if ind5 != ind4:
                                                distinct += 1
                                            if ind7 == ind6:
                                                for ind8 in range(distinct - 1):
                                                    ev[((ind1, ind2, ind3, ind4, ind5), (ind6, ind7), 4 * ind8)] = [0, 0]
                                                    ev[((ind1, ind2, ind3, ind4, ind5), (ind6, ind7), 4 * ind8 + 1)] = [0, 0]
                                                    ev[((ind1, ind2, ind3, ind4, ind5), (ind6, ind7), 4 * ind8 + 2)] = [0, 0]
                                            else:
                                                for ind8 in range(distinct - 1):
                                                    ev[((ind1, ind2, ind3, ind4, ind5), (ind6, ind7), 4 * ind8)] = [0, 0]
                                                    ev[((ind1, ind2, ind3, ind4, ind5), (ind6, ind7), 4 * ind8 + 1)] = [0, 0]
                                                    ev[((ind1, ind2, ind3, ind4, ind5), (ind6, ind7), 4 * ind8 + 2)] = [0, 0]
                                                    ev[((ind1, ind2, ind3, ind4, ind5), (ind6, ind7), 4 * ind8 + 3)] = [0, 0]
    for ind1 in range(13):
        for ind2 in range(ind1, 13):
            for ind3 in range(ind2, 13):
                for ind4 in range(ind3, 13):
                    for ind5 in range(13):
                        if not (ind5 == ind4 and ind5 == ind1):
                            for ind6 in range(ind5, 13):
                                if not ((ind6 == ind5 and ((ind6 == ind4 and ind6 == ind2) or (ind6 == ind3 and ind6 == ind1))) or (ind6 != ind5 and (ind6 == ind4 and ind6 == ind1))):
                                    distinct = 1
                                    if ind2 != ind1:
                                        distinct += 1
                                    if ind3 != ind2:
                                        distinct += 1
                                    if ind4 != ind3:
                                        distinct += 1
                                    if distinct == 1:
                                        distinct = 2
                                    if ind6 == ind5:
                                        for ind7 in range(distinct - 1):
                                            ev[((ind1, ind2, ind3, ind4), (ind5, ind6), 4 * ind7)] = [0, 0]
                                            ev[((ind1, ind2, ind3, ind4), (ind5, ind6), 4 * ind7 + 1)] = [0, 0]
                                            ev[((ind1, ind2, ind3, ind4), (ind5, ind6), 4 * ind7 + 2)] = [0, 0]
                                    else:
                                        for ind7 in range(distinct - 1):
                                            ev[((ind1, ind2, ind3, ind4), (ind5, ind6), 4 * ind7)] = [0, 0]
                                            ev[((ind1, ind2, ind3, ind4), (ind5, ind6), 4 * ind7 + 1)] = [0, 0]
                                            ev[((ind1, ind2, ind3, ind4), (ind5, ind6), 4 * ind7 + 2)] = [0, 0]
                                            ev[((ind1, ind2, ind3, ind4), (ind5, ind6), 4 * ind7 + 3)] = [0, 0]
    for ind1 in range(13):
        for ind2 in range(ind1, 13):
            for ind3 in range(ind2, 13):
                for ind4 in range(13):
                    for ind5 in range(ind4, 13):
                        if not (ind5 == ind4 and ind5 == ind3 and ind5 == ind1):
                            distinct = 1
                            if ind2 != ind1:
                                distinct += 1
                            if ind3 != ind2:
                                distinct += 1
                            if distinct == 1:
                                distinct = 2
                            if ind5 == ind4:
                                for ind6 in range(distinct - 1):
                                    ev[((ind1, ind2, ind3), (ind4, ind5), 4 * ind6)] = [0, 0]
                                    ev[((ind1, ind2, ind3), (ind4, ind5), 4 * ind6 + 1)] = [0, 0]
                                    ev[((ind1, ind2, ind3), (ind4, ind5), 4 * ind6 + 2)] = [0, 0]
                            else:
                                for ind6 in range(distinct - 1):
                                    ev[((ind1, ind2, ind3), (ind4, ind5), 4 * ind6)] = [0, 0]
                                    ev[((ind1, ind2, ind3), (ind4, ind5), 4 * ind6 + 1)] = [0, 0]
                                    ev[((ind1, ind2, ind3), (ind4, ind5), 4 * ind6 + 2)] = [0, 0]
                                    ev[((ind1, ind2, ind3), (ind4, ind5), 4 * ind6 + 3)] = [0, 0]
    with open('hero.pickle', 'wb') as handle:
        pickle.dump(ev, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('villain.pickle', 'wb') as handle:
        pickle.dump(ev, handle, protocol=pickle.HIGHEST_PROTOCOL)
