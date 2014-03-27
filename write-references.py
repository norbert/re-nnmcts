#!/usr/bin/env python


from __future__ import print_function


import math
import sys
import os
import re
import random
import argparse
from collections import OrderedDict


RANDOM_SEED = os.environ.get('RANDOM_SEED', None)
random.seed(RANDOM_SEED)


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--divisor', metavar='DIV', type=int, default=1)
parser.add_argument('minimum', metavar='MIN', type=int)
parser.add_argument('maximum', metavar='MAX', type=int)
parser.add_argument('resolution', metavar='RES', type=int)
parser.add_argument('lists', metavar='LIST', type=argparse.FileType('rb'),
                    nargs='+')
args = parser.parse_args()


MIN = args.minimum
MAX = args.maximum
DIVISOR = args.divisor
RESOLUTION = args.resolution * DIVISOR


H_ref = 24
N_ref = (H_ref * 60 * 60) / RESOLUTION


MAX_IDX = (MAX - MIN) / RESOLUTION
POS_IDX_RANGE = (N_ref, MAX_IDX - N_ref)
NEG_IDX_RANGE = (0, (MAX_IDX - (N_ref * 2)))


NAMES = OrderedDict()
TIMESERIES = dict()


def extract_names(f):
    for line in f:
        fields = unicode(line.strip(), 'utf-8').split('\t')
        name = fields[0]
        if name in NAMES:
            raise RuntimeError
        onset = int(fields[1]) if len(fields) > 1 else None
        NAMES[name] = onset
for f in args.lists:
    extract_names(f)


for line in sys.stdin:
    fields = unicode(line.strip(), 'utf-8').split('\t')
    name, values = fields
    if not name in NAMES:
        continue
    if name in TIMESERIES:
        raise RuntimeError
    onset = NAMES[name]
    values = [int(x) for x in values.split(' ')]
    if onset is not None:
        idxon = int(math.ceil((onset - MIN) / float(RESOLUTION))) + 1
        if idxon >= POS_IDX_RANGE[0] and idxon < POS_IDX_RANGE[1]:
            idxstart = idxon - N_ref
            values = values[idxstart:(idxstart + (N_ref * 2))]
            if sum(values) < 1:
                continue
        else:
            continue
    else:
        if sum(values) < 1:
            continue
        rand_values = None
        while rand_values is None:
            idxstart = random.randint(*NEG_IDX_RANGE)
            rand_values = values[idxstart:(idxstart + N_ref * 2)]
            if sum(rand_values) < 0:
                rand_values = None
        values = rand_values
    TIMESERIES[name] = values


for name, onset in NAMES.iteritems():
    if not name in TIMESERIES:
        continue
    label = int(onset is not None)
    values = TIMESERIES[name]
    print('\t'.join([name, str(label), ' '.join([str(x) for x in values])])
          .encode('utf-8'))
