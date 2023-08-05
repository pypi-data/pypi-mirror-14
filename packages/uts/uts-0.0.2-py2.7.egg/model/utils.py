# -*- coding: utf-8 -*-
import numpy as np
from collections import Counter
def cosine_sim(c1, c2):
    try:
        # works for Counter
        n1 = np.sqrt(sum(map(lambda x: x * x, c1.values())))
        n2 = np.sqrt(sum(map(lambda x: x * x, c2.values())))
        num = sum([c1[key] * c2[key] for key in c1])
    except:
        # works for ordinary list
        assert(len(c1) == len(c2))
        n1 = np.sqrt(sum(map(lambda x: x * x, c1)))
        n2 = np.sqrt(sum(map(lambda x: x * x, c2)))
        num = sum([c1[i] * c2[i] for i in xrange(len(c1))])
    try:
        if n1 * n2 < 1e-9: # divide by zero case
            return 0
        return num / (n1 * n2)
    except:
        print n1, n2
