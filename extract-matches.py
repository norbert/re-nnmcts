#!/usr/bin/env python


from __future__ import print_function


import sys
import argparse
from collections import OrderedDict


import twokenize


parser = argparse.ArgumentParser()
parser.add_argument('lists', metavar='LIST', type=argparse.FileType('rb'),
                    nargs='+')
args = parser.parse_args()


NAMES = OrderedDict()


def extract_names(fn):
    for line in f:
        fields = unicode(line.strip(), 'utf-8').split('\t')
        name = ' '.join(twokenize.tokenize(fields[0].lower()))
        NAMES[name] = True
for f in args.lists:
    extract_names(f)


for line in sys.stdin:
    prefix, tokens = unicode(line.strip(), 'utf-8').rsplit('\t', 1)
    tokens = ' ' + tokens.lower() + ' '
    matches = []
    for name in NAMES:
        if ' ' + name + ' ' in tokens:
            matches.append(name)
    if len(matches) > 0:
        print('\t'.join([prefix] + matches).encode('utf-8'))
