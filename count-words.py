#!/usr/bin/env python


from __future__ import print_function


import sys
import re
import argparse


parser = argparse.ArgumentParser()
args = parser.parse_args()


WORDS = dict()
MATCHER = re.compile(r'^[a-z]{3,}$')


for line in sys.stdin:
    fields = unicode(line.strip(), 'utf-8').split('\t')
    tokens = fields[3].split(' ')
    words = [t.lower() for t in tokens if MATCHER.match(t)]
    for word in words:
        if not word in WORDS:
            WORDS[word] = 1
        else:
            WORDS[word] += 1


for word, count in WORDS.iteritems():
    print('\t'.join([word, str(count)]).encode('utf-8'))
