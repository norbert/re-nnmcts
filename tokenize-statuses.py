#!/usr/bin/env python


from __future__ import print_function


import sys
import argparse


import twokenize


parser = argparse.ArgumentParser()
args = parser.parse_args()


for line in sys.stdin:
    fields = unicode(line.strip(), 'utf-8').split('\t')
    status_id = fields[3][2:].strip()  # FIXME
    user_id = fields[1]
    created_at = int(fields[0]) / 1000  # FIXME
    tokens = ' '.join(twokenize.tokenize(fields[2]))
    print('\t'.join([status_id, user_id, str(created_at), tokens])
          .encode('utf-8'))
