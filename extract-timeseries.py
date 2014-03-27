#!/usr/bin/env python


from __future__ import print_function


import sys
import re
import argparse
from collections import OrderedDict


import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('minimum', metavar='MIN', type=int)
parser.add_argument('maximum', metavar='MAX', type=int)
parser.add_argument('resolution', metavar='RES', type=int)
parser.add_argument('lists', metavar='LIST', type=argparse.FileType('rb'),
                    nargs='*')
args = parser.parse_args()


MIN = args.minimum
MAX = args.maximum
RESOLUTION = args.resolution
MAX_IDX = (MAX - MIN) / RESOLUTION


NAMES = OrderedDict()
TIMESERIES = OrderedDict()


def extract_names(f):
    for line in f:
        fields = unicode(line.strip(), 'utf-8').split('\t')
        name = fields[0]
        if name in NAMES:
            raise RuntimeError
        label = int(len(fields) > 1)
        NAMES[name] = label
for f in args.lists:
    extract_names(f)


for line in sys.stdin:
    fields = unicode(line.strip(), 'utf-8').split('\t')
    created_at = int(fields[2])
    matches = fields[3:]
    idx = (created_at - MIN) / RESOLUTION
    if idx >= 0 and idx < MAX_IDX:
        for match in matches:
            if NAMES and not match in NAMES:
                continue
            if not match in TIMESERIES:
                values = np.zeros(MAX_IDX, dtype='int16')
                TIMESERIES[match] = values
            else:
                values = TIMESERIES[match]
            values[idx] += 1


for name in (NAMES or TIMESERIES):
    if not name in TIMESERIES:
        continue
    values = TIMESERIES[name]
    print('\t'.join([name, ' '.join([str(x) for x in values])])
          .encode('utf-8'))
