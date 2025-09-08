#!/usr/bin/env python

from hashlib import sha256
import json
from os import mkdir, path
import re
from urllib.request import urlretrieve
from xml.etree import ElementTree as et


# import me!
# TODO: cache computed ones in redis (?) and refresh when dirty from fetching
AGENCIES: dict
TITLES: dict
SLUG_CHECKSUM: dict
WORD_COUNTS = {}

_ECFR_API = 'https://www.ecfr.gov/api/'
_CHECKSUM_LEN = 4  # bump if needed
_WORD_RE = re.compile(r'[^\s]+')
_WORD_COUNTS_PATH = path.join('cache', 'word_counts.json')


if __name__ == '__main__':
  print('Warming up the cache for eCFR documents.  This may take a while...')


if not path.exists('cache'):
  mkdir('cache')


try:
  with open(_WORD_COUNTS_PATH, 'r') as f:
    WORD_COUNTS = json.load(f)
except FileNotFoundError:
  pass


def _checksum(string: str) -> str:
  return sha256(string.encode('ascii')).hexdigest()[:_CHECKSUM_LEN]


def _count_words_per_chapter(title_number: int, filename: str):
  for _, elem in et.iterparse(filename):
    if elem.attrib.get('TYPE', '') == 'CHAPTER':
      WORD_COUNTS[':'.join((str(title_number), elem.attrib['N']))] = \
          len(re.findall(_WORD_RE, ''.join(elem.itertext())))


def _maybe_fetch_title(date: str, number: int) -> str:
  try:
    mkdir(path.join('cache', date))
  except FileExistsError:
    pass
  file = path.join('cache', date, f'title-{number}.xml')
  if not path.exists(file):
    if __name__ == '__main__':
      print(f'Retrieving {file}...', end='')
    urlretrieve(_ECFR_API + f'versioner/v1/full/{date}/title-{number}.xml',
                filename=file)
    if __name__ == '__main__':
      print('done')
    _count_words_per_chapter(number, file)
  return file


def _fetch_to_json(endpoint: str) -> dict:
  file = path.join('cache', endpoint.split('/')[-1])
  # TODO: rate limit this by checking file timestamp
  urlretrieve(_ECFR_API + endpoint, filename=file)
  with open(file, 'r') as f:
    return json.load(f)


def _maybe_fetch_to_json(endpoint: str) -> dict:
  file = path.join('cache', endpoint.split('/')[-1])
  try:
    with open(file, 'r') as f:
      return json.loads(f.read())
  except FileNotFoundError:
    urlretrieve(_ECFR_API + endpoint, filename=file)
    with open(file, 'r') as f:
      return json.load(f)


AGENCIES = _fetch_to_json('admin/v1/agencies.json')['agencies']
TITLES = _fetch_to_json('versioner/v1/titles.json')['titles']


# populating slug to agency checksums
_slugs = sorted([agency['slug'] for agency in AGENCIES] +
                [child['slug'] for agency in AGENCIES
                               for child in agency['children']])
SLUG_CHECKSUM = dict([(slug, _checksum(slug)) for slug in _slugs])
if len(_slugs) != len(set(SLUG_CHECKSUM.values())):
  raise AssertionError('_CHECKSUM_LEN is too small, please increase by 1')


# populating word counts
for title in TITLES:
  if not title['latest_amended_on']:
    continue
  _maybe_fetch_title(title['latest_amended_on'], title['number'])


with open(_WORD_COUNTS_PATH, 'w') as f:
  json.dump(WORD_COUNTS, f)


for agency in AGENCIES:
  wc = 0
  for ref in agency['cfr_references']:
    pass
  break


if __name__ == '__main__':
  keys = [k for k in globals().keys() if 'A' <= k[0] <= 'Z']
  print('Done!')
  print(f'import {", ".join(keys)} from this module')
