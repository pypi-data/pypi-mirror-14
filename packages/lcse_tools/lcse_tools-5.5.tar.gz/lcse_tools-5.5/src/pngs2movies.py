#!/usr/bin/env python

"""
Create movies out of a series of pngs. Add dump and/or time value from an RTplot.ppm file.


.. code:: bash

  $  pngs2movies.py --tmp-dir $PWD/images_4k_timed \
               --add-time RTplot.ppm \
               -i images_4k \
               -o movies_4k \
               --font-size=100 \
               --video-prefix=asdf \
               --video-suffix=4k \
               --threads 8 \
               --process-only

This command assumes that movies live in movies_4k and that the root of the image directory tree is in 
images_4k. Also dump number and its corresponding time (from RTplot.ppm) will be added to each frame and 
the result stored in images_4k_timed. images_4k is a directory containing directories of images 
(e.g. ./foo/foo_0001.png,foo_0002.png,..,foo_1020.png, ; ./bar/bar_0001.png, ..., bar_1929.png). 

Movies will be created as ./movies_4k/asdf-<some-name>-4k.avi

This will not overwrite movies. 
"""

import argparse
import os
import pkg_resources
import re
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

import lcse
from lcse_tools import image_util as iu

Image.DEBUG = False

def filter_files(path, prefix=None, suffix=None):
  # Switch to https://docs.python.org/2/library/fnmatch.html

  try:
    cond = lambda x : (x.startswith(prefix) if prefix else True) and (x.endswith(suffix) if suffix else True)
    files = [os.path.join(path, f) for f in os.listdir(path) if cond(f)]
    return files
  except Exception as e:
    print e


# 1. Create temp directory to work in
# 2. Fully composite image
# 3. Write out to temp file (don't overwrite if it exists)
# 4. Make movie

def add_time_to_pngs(image_path, prefix, font_name, temp_prefix, time_map={}, font_size=50):

  print temp_prefix
  print font_name

  temp_path = os.path.join(temp_prefix, prefix)

  if not os.path.exists(temp_path):
    os.makedirs(temp_path)

  font = ImageFont.truetype(font_name, font_size)

  image_files = filter_files(image_path, suffix='.png')
  image_files.sort()

  dump_re = re.compile('(.*)([-_])([\d]{4,6})(.*)')

  prefix = os.path.basename(os.path.commonprefix(image_files))

  for filename in image_files:

    m = dump_re.match(filename)

    if not m:
      continue

    dump = int(m.group(3))
    filename_out = os.path.join(temp_path, os.path.basename(filename))

    if os.path.exists(filename_out):
      continue

    im = Image.open(filename)
    iu.draw_time(im, font, dump=dump, time=time_map.get(dump))

    print filename, '->', filename_out

    im.save(filename_out)

  return temp_path

def make_movie_from_pngs(image_path, **kwargs):
  prefix = kwargs.get('prefix', '')

  add_time = kwargs.get('add_time')

  if add_time is not None:
    if add_time:
      rtp = lcse.rtplot_reader(add_time[0])
      time_map = dict((dump, val['T']) for dump, val in rtp.dump_map.items())
    else:
      time_map = {}

    image_path = add_time_to_pngs(image_path, prefix, kwargs.get('font'), kwargs.get('tmp_dir'), time_map,
                                  font_size=kwargs.get("font_size"))

  fps = kwargs.get('fps', 24)
  tune = kwargs.get('tune', 'stillimage')
  threads = kwargs.get('threads') or 'auto'

  print prefix

  files = filter_files(image_path, prefix=prefix, suffix='.png')
  dumps = [int(f[-8:-4]) for f in files]
  dumps.sort()

  if not dumps:
    print "Nothing found for %s in %s" % (prefix, image_path)
    return

  dmin, dmax = min(dumps), max(dumps)

  elements = []
  if kwargs.get('video_prefix'): elements.append(kwargs.get('video_prefix'))
  elements.append(prefix)
  elements.append('%04i-%04i' % (dmin, dmax))
  if kwargs.get('video_suffix'): elements.append(kwargs.get('video_suffix'))
  elements.append(str(fps))

  video_filename = "%s.avi" % ('_'.join(elements))

#  video_suffix = "%s_%s" % (kwargs.get('video_suffix'), fps if kwargs.get('video_suffix') else str(fps)
#  video_filename = '%s_%04i-%04i_%s.avi' % (video_prefix, dmin, dmax, video_suffix)
  video_path = os.path.abspath(os.path.join(kwargs.get('movies_path', '.'), video_filename))

  if not os.path.exists(kwargs.get('movies_path', '.')):
    os.makedirs(kwargs.get('movies_path', '.'))

  if os.path.exists(video_path):
    print "File %s exists, skipping" % video_path
    return

  if kwargs.get('process_only'):
    print "Not making movie %s. Processing only" % video_path
    return

  # Make Video
  args = ['mencoder', 'mf://%s*.png' % prefix,
          '-mf', 'fps=%i:type=png' % fps,
          '-oac', 'copy',
          '-ovc', 'x264', '-x264encopts',
          'preset=veryslow:tune=%s:crf=15:frameref=15:fast_pskip=0:threads=%s' % (tune, threads),
          '-o', video_path]

  print("Output file is %s" % video_path)

  p = subprocess.Popen(args, cwd=image_path)
  s, i = p.communicate()
  p.wait()

def build_argparse():

  default_font = os.path.abspath(os.path.join(pkg_resources.resource_filename(__name__, '../../fonts'), 'Roboto-Bold.ttf'))


  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('-i', help='Path to images base directory',  default='.')
  parser.add_argument('-o', help='Path to video save directory', default='.')
  parser.add_argument('--fps', nargs='+',type=int, help='List of fps to create', default=[18])
  parser.add_argument('--prefixes', nargs='+', help='List of prefixes to try. Otherwise everything inside input-path is used')
  parser.add_argument('--video-prefix', help='Prefix to add to output video files')
  parser.add_argument('--video-suffix', help='Suffix to add to output video files')

  parser.add_argument('--add-time', nargs='*', help='Specify RTplot.ppm file to use for timing info')
  parser.add_argument('--font', help='Font to use', default=default_font)
  parser.add_argument('--font-size', type=int, help='Size of font to use', default=50)
  parser.add_argument('--tmp-dir', help='Temporary directory to store intermediate files', default='/tmp/timed')
  parser.add_argument('--threads', help='Number of threads to use for video encoding')
  parser.add_argument('--process-only', help='Process images only, do not make a movie', action='store_true')

  return parser
  

def main():

  parser = build_argparse()
  args = parser.parse_args()

  if args.prefixes:
    prefixes = args.prefixes
  else:
    prefixes = os.listdir(args.i)
    prefixes.sort()

  print "Using prefixes", prefixes, args.i, args.o

  for fps in args.fps:
    for prefix in prefixes:
      try:

        in_path = os.path.join(args.i, prefix)

        if not os.path.isdir(in_path):
          continue

        make_movie_from_pngs(in_path, prefix=prefix,
                             video_prefix=args.video_prefix or '',
                             video_suffix=args.video_suffix or '',
                             fps=fps, movies_path=args.o, font=args.font,
                             add_time=args.add_time, tmp_dir=args.tmp_dir,
                             font_size=args.font_size, threads=args.threads,
                             process_only=args.process_only)
      except Exception as e:
        print "Problem", e

  return

if __name__ == '__main__':
  main()
