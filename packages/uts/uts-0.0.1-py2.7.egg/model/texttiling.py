# -*- coding: utf-8 -*-
# Based on nltk texttiling implementation with some modifications
import re
import math
import numpy as np
from collections import Counter
from copy import deepcopy
from utils import *

class TextTiling:

    def __init__(self, window=5):
        self.window = window
        self.debug_mode = debug_mode

    def segment(self, document, language='Chinese', para_cnts=None):
        assert(language == 'Chinese' or language == 'English')
        # step 1, do preprocessing
        n = len(document)
        self.window = max(min(self.window, n / 3), 1)
        if language == 'Chinese':
            # for chinese, add character one by one
            cnts = [Counter(document[i]) for i in xrange(n)]
        elif language == 'English':
            document = map(lambda d: d.lower(), document)
            # for english, split sentence by space
            cnts = [Counter(document[i].split()) for i in xrange(n)]

        # step 2, calculate gap score
        gap_score = [0 for _ in xrange(n)]
        for i in xrange(n):
            sz = min(min(i + 1, n - i - 1), self.window)
            lcnt, rcnt = Counter(), Counter()
            for j in xrange(i - sz + 1, i + 1):
                lcnt += cnts[j]
            for j in xrange(i + 1, i + sz + 1):
                rcnt += cnts[j]
            gap_score[i] = cosine_sim(lcnt, rcnt)

        # step 3, calculate depth score
        depth_score = [0 for _ in xrange(n)]
        for i in xrange(n):
            if i < self.window or i + self.window >= n:
                continue
            ptr = i - 1
            while ptr >= 0 and gap_score[ptr] >= gap_score[ptr + 1]:
                ptr -= 1
            lval = gap_score[ptr + 1]
            ptr = i + 1
            while ptr < n and gap_score[ptr] >= gap_score[ptr - 1]:
                ptr += 1
            rval = gap_score[ptr - 1]
            depth_score[i] = lval + rval - 2 * gap_score[i]

        # step 4, smooth depth score with fixed window size 3
        smooth_dep_score = [0 for _ in xrange(n)]
        for i in xrange(n):
            if i - 1 < 0 or i + 1 >= n:
                smooth_dep_score[i] = depth_score[i]
            else:
                smooth_dep_score[i] = np.average(depth_score[(i - 1):(i + 2)])

        # step 5, determine boundaries
        boundaries = [0 for _ in xrange(n)]
        avg = np.average(smooth_dep_score)
        stdev = np.std(smooth_dep_score)
        cutoff = avg - stdev / 2.0

        # smooth_dep_score = deepcopy(depth_score)
        depth_tuples = zip(smooth_dep_score, range(len(smooth_dep_score)))
        depth_tuples.sort()
        depth_tuples.reverse()
        # hp = depth_tuples[:len(depth_tuples) / 5]
        hp = filter(lambda x: (x[0] > cutoff), depth_tuples)
        for dt in hp:
            boundaries[dt[1]] = 1
            for i in xrange(dt[1] - 4, dt[1] + 4 + 1):
                if i != dt[1] and i >= 0 and i < n and boundaries[i] == 1:
                    boundaries[dt[1]] = 0
                    break
        return boundaries
