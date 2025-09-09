#!/usr/bin/env python

from hashlib import sha256
import json
from os import mkdir, path, unlink
import re
from sys import stderr
from urllib.request import urlretrieve
from xml.etree import ElementTree as et


# import me!
# TODO: cache computed ones in redis (?) and refresh when dirty from fetching
AGENCIES: dict
TITLES: dict
TITLE_VERSIONS = {}
SLUG_CHECKSUM: dict
WORD_COUNTS = {}

_ECFR_API = 'https://www.ecfr.gov/api/'
_CHECKSUM_LEN = 4  # bump if needed
_WORD_RE = re.compile(r'[^\s]+')
_WORD_COUNTS_PATH = path.join('cache', 'word_counts.json')


if __name__ == '__main__':
  print('Warming up the cache for eCFR documents.  This may take a while...',
        file=stderr)


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
    type_ = elem.attrib.get('TYPE', '')
    if type_ in ('CHAPTER', 'SUBTITLE'):
      WORD_COUNTS[':'.join((str(title_number), type_.lower(),
                            elem.attrib['N']))] = \
          len(re.findall(_WORD_RE, ''.join(elem.itertext())))


# retrieves title and version history
def _maybe_fetch_title(date: str, number: int) -> str:
  try:
    mkdir(path.join('cache', date))
  except FileExistsError:
    pass
  file = path.join('cache', date, f'title-{number}.xml')
  if not path.exists(file):
    # delete existing version history since it must have been updated
    try:
      unlink(path.join('cache', f'title-{number}.json'))
    except FileNotFoundError:
      pass
    if __name__ == '__main__':
      print(f'Retrieving {file}...', end='', file=stderr)
    urlretrieve(_ECFR_API + f'versioner/v1/full/{date}/title-{number}.xml',
                filename=file)
    if __name__ == '__main__':
      print('done.', file=stderr)
    _count_words_per_chapter(number, file)
  versions = _maybe_fetch_to_json(f'versioner/v1/versions/title-{number}.json')
  return file, versions['content_versions']


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
      return json.load(f)
  except FileNotFoundError:
    try:
      urlretrieve(_ECFR_API + endpoint, filename=file)
      with open(file, 'r') as f:
        return json.load(f)
    except Exception as e:
      print(endpoint, file=stderr)
      print(e, file=stderr)
      raise


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
  _, versions = _maybe_fetch_title(title['latest_amended_on'], title['number'])
  TITLE_VERSIONS[title['number']] = sorted(set([v['date'] for v in versions]),
                                           reverse=True)


with open(_WORD_COUNTS_PATH, 'w') as f:
  json.dump(WORD_COUNTS, f)


if __name__ == '__main__':
  keys = [k for k in globals().keys() if 'A' <= k[0] <= 'Z']
  print('Done!', file=stderr)
  print(f'import {", ".join(keys)} from this module', file=stderr)
