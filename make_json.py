#!/usr/bin/env python

import json
from sys import stderr

from ecfr import AGENCIES, TITLES, TITLE_VERSIONS, SLUG_CHECKSUM, WORD_COUNTS


def make_agency(agency):
  a = {}
  a['hash'] = SLUG_CHECKSUM[agency['slug']]
  a['name'] = agency['sortable_name']
  a['cfr_references'] = agency['cfr_references']
  wc = 0
  for cfr in agency['cfr_references']:
    sub = 'chapter' if 'chapter' in cfr else 'subtitle'
    try:
      wc += WORD_COUNTS[':'.join((str(cfr['title']), sub, cfr[sub]))]
    except KeyError as e:
      print(e, file=stderr)
  a['wc'] = wc
  return a


def main():
  payload = {}

  agencies = []
  for agency in AGENCIES:
    children = [make_agency(child) for child in agency['children']]
    a = make_agency(agency)
    a['children'] = children
    agencies.append(a)
  payload['agencies'] = agencies

  titles = []
  for title in TITLES:
    if title['reserved']:
      continue
    t = {}
    t['number'] = title['number']
    t['name'] = title['name']
    t['versions'] = TITLE_VERSIONS[t['number']]
    titles.append(t)
  payload['titles'] = titles

  with open('payload.json', 'w') as f:
    json.dump(payload, f)
  print('Written payload.json', file=stderr)


if __name__ == '__main__':
  main()
