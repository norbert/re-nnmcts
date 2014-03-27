#!/usr/bin/env python


from __future__ import print_function


import sys
import re
import argparse
from collections import OrderedDict


import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--divisor', metavar='DIVISOR', type=int)
args = parser.parse_args()


DIVISOR = args.divisor


TIMESERIES = OrderedDict()


for line in sys.stdin:
    fields = unicode(line.strip(), 'utf-8').split('\t')
    name = fields[0]
    values = np.array([int(x) for x in fields[1].split(' ')], dtype='int16')
    if not name in TIMESERIES:
        TIMESERIES[name] = values
    else:
        TIMESERIES[name] += values


for name, values in TIMESERIES.iteritems():
    values = TIMESERIES[name]
    if DIVISOR and DIVISOR > 1:
        merged_values = np.zeros(np.ceil(values.shape[0] / float(DIVISOR)),
                                 dtype='int16')
        for idx, value in enumerate(values):
            merged_values[idx / DIVISOR] += value  # FIXME
        values = merged_values
    print('\t'.join([name, ' '.join([str(x) for x in values])])
          .encode('utf-8'))
