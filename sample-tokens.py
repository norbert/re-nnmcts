#!/usr/bin/env python


from __future__ import print_function


import os
import sys
import re
import random
import argparse


import twokenize


RANDOM_SEED = os.environ.get('RANDOM_SEED', None)
random.seed(RANDOM_SEED)


parser = argparse.ArgumentParser()
parser.add_argument('-H', '--hashtags', action='store_true')
parser.add_argument('-c', '--count', metavar='COUNT', type=int)
parser.add_argument('-l', '--limit', metavar='LIMIT', type=int)
parser.add_argument('trends', metavar='TRENDS', type=argparse.FileType('rb'))
args = parser.parse_args()


MATCHER = re.compile(r'^#[a-z]{3,}$') if args.hashtags else None
COUNT = args.count
LIMIT = args.limit


TRENDS = set()
TOKENS = dict()


for line in args.trends:
    fields = unicode(line.strip(), 'utf-8').split('\t')
    name = fields[0]
    tokens = twokenize.tokenize(name.lower())
    for token in tokens:
        TRENDS.add(token)


for line in sys.stdin:
    fields = unicode(line.strip(), 'utf-8').split('\t')
    token = fields[0].lower()
    count = int(fields[1])
    if not token in TRENDS:
        if MATCHER and not MATCHER.match(token):
            continue
        if not token in TOKENS:
            TOKENS[token] = count
        else:
            TOKENS[token] += count


SAMPLE = TOKENS.keys()
if LIMIT:
    SAMPLE = filter(lambda x: TOKENS.get(x) >= LIMIT, SAMPLE)
if COUNT:
    SAMPLE = random.sample(SAMPLE, COUNT)


for token in sorted(SAMPLE, key=TOKENS.get, reverse=True):
    count = TOKENS[token]
    print('\t'.join([token, str(count)]).encode('utf-8'))
