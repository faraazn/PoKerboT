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

import pickle
import baseline


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
    with open('hero.pickle', 'wb') as handle:
        pickle.dump(ev, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('villain.pickle', 'wb') as handle:
        pickle.dump(ev, handle, protocol=pickle.HIGHEST_PROTOCOL)