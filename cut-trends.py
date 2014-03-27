#!/usr/bin/env python


from __future__ import print_function


import sys
import argparse


import twokenize


parser = argparse.ArgumentParser()
parser.add_argument('minimum', metavar='MIN', type=int)
parser.add_argument('maximum', metavar='MAX', type=int)
args = parser.parse_args()


MIN = args.minimum
MAX = args.maximum


for line in sys.stdin:
    fields = unicode(line.strip(), 'utf-8').split('\t')
    name = ' '.join(twokenize.tokenize(fields[0].lower()))
    collected_at = int(fields[1])
    rank = int(fields[2])
    if collected_at >= MIN and collected_at < MAX:
        print('\t'.join([name, str(collected_at), str(rank)]).encode('utf-8'))
