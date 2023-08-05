#!/usr/bin/env python

"""
Layers the fv and enuc together
"""


import argparse
import os
import re
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

from lcse_tools import image_util as iu

#temp_template = '/u/sciteam/sandalsk/scratch/timed/%s'

def make_stuff(prefix_a, prefix_b, output_path, output_prefix, dump_range):
  """ Layer images with `prefix_b` on top of `prefix_a`
  """

  # We want to combine images from A on top of B
  mask_a = prefix_a + "%04d.png"
  mask_b = prefix_b + "%04d.png"

#  rtp = lcse.rtplot_reader(project_path)
#  dumps = rtp.dump_map.keys()
#  dumps.sort()
  dumps = range(dump_range[0], dump_range[1] + 1)

  print "Processing dummps %s" % dumps

  path = os.path.join(os.path.abspath(output_path), output_prefix)

  if not os.path.exists(path):
     os.makedirs(path)

  for dump in dumps:
        
    filename_out = os.path.join(path, '%s-%04d.png' % (output_prefix, dump))

    if os.path.exists(filename_out):
      continue
    
    print filename_out
    
    # load fv image
    try:
        # Open
        image_a = Image.open(mask_a % dump).convert("RGBA")
        image_b = Image.open(mask_b % dump).convert("RGBA")
        
        # Crop
        image_a = iu.square_crop(image_a, image_a.size[1])
        image_b = iu.square_crop(image_b, image_b.size[1])
        
        # Make the second image transparent
        image_b = iu.color_to_alpha(image_b, threshold=30)      
        image_a = iu.alpha_composite(image_b, image_a)
        
#        draw_time(image_a, font, dump=dump, time=rtp.dump_map[dump]['T'])
        image_a.save(filename_out)
        
    except IOError as e:
        print e
        continue

def build_argparse():

  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--top', help='Top image', required=True)
  parser.add_argument('--bottom', help='Bottom image', required=True)
  parser.add_argument('--output-prefix', help='Prefix for output filenames <prefix>-<dump>.png', required=True)
  parser.add_argument('--output-path', help='Path to store image files', default=".")
  parser.add_argument('--dumps', nargs='+',type=int, help='Dump range to process (e.g. --dumps 10 200)')

  return parser
  
def main():

  parser = build_argparse()
  args = parser.parse_args()

  if  len(args.dumps) < 2:
    print "Specifiy dump range like --dumps 10 200"
    return

  make_stuff(args.bottom, args.top, args.output_path, args.output_prefix, args.dumps)


  return

  parser.add_argument('--add-time', help='Add time from an RTplot.ppm file')
  parser.add_argument('--font', help='/home/stou/lcse_tools/fonts/Roboto-Bold.ttf')

  prefixes = args.prefixes if args.prefixes else os.listdir(args.i)

  return

if __name__ == '__main__':
  main()
