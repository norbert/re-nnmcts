#!/usr/bin/env python


from __future__ import print_function


import sys
import re
import argparse
from collections import OrderedDict


import twokenize


parser = argparse.ArgumentParser()
parser.add_argument('-b', '--boundary', metavar='BOUNDARY', type=int)
parser.add_argument('minimum', metavar='MIN', type=int)
parser.add_argument('maximum', metavar='MAX', type=int)
args = parser.parse_args()


MIN = args.minimum
MAX = args.maximum
BOUNDARY = args.boundary or 0


TRENDS = OrderedDict()


for line in sys.stdin:
    fields = unicode(line.strip(), 'utf-8').split('\t')
    name = ' '.join(twokenize.tokenize(fields[0].lower()))
    collected_at = int(fields[1])
    rank = int(fields[2])
    onset = collected_at if rank <= 3 else None
    if not name in TRENDS:
        TRENDS[name] = [rank, collected_at, collected_at, onset]
    else:
        t = TRENDS[name]
        if onset is not None:
            t[3] = min(onset, t[3]) if t[3] is not None else onset
        t[0] = min(rank, t[0])
        t[1] = min(collected_at, t[1])
        t[2] = max(collected_at, t[2])


for name, t in TRENDS.iteritems():
    if t[3] is None:
        continue
    duration = t[2] - t[1]
    if duration < (30 * 60):
        continue
    elif duration > (24 * 60 * 60):
        continue
    elif t[1] < MIN + BOUNDARY:
        continue
    elif t[1] >= MAX - BOUNDARY:
        continue
    print('\t'.join([name, str(t[1]), str(t[0]), str(duration)])
          .encode('utf-8'))
