#!/bin/env python

"""
Check for missing files in directories containing sequences of files. For example sequences of rendered images or plots, .hv files, etc.

Usage:

.. code:: bash

  check_missing.py <path>
"""

__author__ = 'Stou Sandalski <stou@icapsid.net>'
__license__= 'Public Domain'



import logging
import os
import re

#TODO: Add a total

# create file handler which logs debug messages
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

try:
  from colorlog import ColoredFormatter

  formatter = ColoredFormatter(
  # "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
  #  "%(log_color)s %(asctime)s - %(name)s - %(levelname)s : %(white)s%(message)s",
    "%(log_color)s %(asctime)s - %(levelname)s : %(white)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
      'DEBUG':    'cyan',
      'INFO':     'green',
      'WARNING':  'yellow',
      'ERROR':    'red',
      'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
    )
  ch.setFormatter(formatter)
except:
#  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  ch.setFormatter(formatter)

log = logging.getLogger('check_missing')
log.addHandler(ch)
log.setLevel(logging.INFO)
#log.propagate = False

fmt_missing = 'Missing \033[1;33m {0:>3d}\033[1;m in {1:28}: {2} in range {3:04d}-{4:04d}'
fmt_ok = '{0:25} range {1:04d}-{2:04d}: \033[1;32m ok \033[1;m'

def check_missing_items(path):
  log.debug("Checking for missing items in %s " % path)

  dump_re = re.compile('(.*)-([\d]{4})\.')

  contents = [os.path.join(path, f) for f in os.listdir(path)]
  files = [os.path.basename(p) for p in contents if os.path.isfile(p)]

  dump_maps = {}

  for f in files:
    m = dump_re.match(f)

    if not m:
      continue

    prefix, dump = m.groups()

    dm = dump_maps.get(prefix, [])
    dm.append(int(dump))
    dump_maps[prefix] = dm

  for name, items in dump_maps.items():

    items.sort()

    items_theory = range(items[0], items[-1] + 1)
    items = set(items)

    missing = list(set(items_theory).difference(items))
    missing.sort()

    missing_ct = len(missing)

    if missing_ct <= 0:
      log.info(fmt_ok.format(name, items_theory[0], items_theory[-1]))
      return []

    log.warning(fmt_missing.format(missing_ct, name, ', '.join(str(d) for d in missing), items_theory[0], items_theory[-1]))

  dirs = [p for p in contents if os.path.isdir(p)]
  dirs.sort()

  for d in dirs:
    check_missing_items(d)


if __name__ == '__main__':

  import sys

  if len(sys.argv) < 2:
    print "Usage check_missing.py <path>"
  else:
    path = sys.argv[1]
    check_missing_items(path)
