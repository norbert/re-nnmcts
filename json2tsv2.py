#!/usr/bin/env python


import sys
import re
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('keys', metavar='KEY', nargs='+')
args = parser.parse_args()


KEYS = args.keys


WHITESPACE = re.compile(r'\s')


def stringify(value):
    if not isinstance(value, basestring):
        value = str(value)
    elif isinstance(value, unicode):
        value = value.encode('utf-8')
    return WHITESPACE.sub(' ', value)


for line in sys.stdin:
    record = json.loads(line)
    values = [stringify(record[k]) for k in KEYS]
    print('\t'.join(values))
