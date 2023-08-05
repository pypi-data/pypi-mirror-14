#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
C Pre-Processor #define evaluator.

Usage:

.. code:: bash

  eval_pp.py input_file.F -o output_file.F -D israyprofile=0 isrestart=0
'''

__author__ = "Stou Sandalski"
__email__ = "stou@icapsid.net"
__date__ = '25 Apr 2015'
__license__ = "Apache 2.0"
__version__ = "1.0"


import argparse
import logging
import re

# TODO: Remove blank statements

class def_stmt(object):
  
  def __init__(self, l):
    self.line = l
    
    tmp = l.split()
    self.name = tmp[1]
    self.expr = tmp[2:]

  def __str__(self):
    return str(self.line)

class if_stmt(object):
  
  def __init__(self, l):
    self.line = l
    self.first = []
    self.second = []

    tmp = l.split()

    self.expr = ' '.join(tmp[1:])
    self.eval_res = None
    self.prefix = tmp[0]

    self._ifdef = tmp[0] == '#ifdef'
    
  def __str__(self):

    out = [self.line]
    out += [str(s) for s in self.first]

    if self.second:
      out += ['#else\n']
      out += [str(s) for s in self.second]

    out += ['#endif\n']
    s = ''.join(out)

    return s

  def eval_cond(self, symbols):
    ''' Evaluate this if statment '''

    # Propagate the eval to nested if statements
    first = [s.eval_cond(symbols)[1] if isinstance(s, if_stmt) else s for s in self.first]
    second = [s.eval_cond(symbols)[1] if isinstance(s, if_stmt) else s for s in self.second]

    expr = self.expr.strip()

    res = None

    if self._ifdef:
      # We don't want to remove undefined symbols at this point. 
      # Could be an option in the future.
      res = True if expr in symbols else None
    else:
      expr = filter_expr(expr, symbols)

      try:
      	res = bool(eval(expr))
      except NameError:
        res = None
      except SyntaxError as e:
        print expr, self.expr

    res_str = ''

    if res is True:
      res_str = ''.join(str(s) for s in first)
    elif res is False:
      res_str = ''.join(str(s) for s in second)
    else:
      out = ['%s %s\n' % (self.prefix, expr)]
      out += [str(s) for s in first]

      if second:
        out += ['#else\n']
        out += [str(s) for s in second]

      out += ['#endif\n']
      res_str = ''.join(out)
   
    return res, res_str

def filter_expr(expr, symbols):
  '''Tokenize expr and replace symbols in the stream. Otherwise doing a search 
     and replace on a symbol can partially match other symbols (isSPU vs isSPUC)
  '''
  res_expr = []
    
  for s in re.split('(\W)', expr):
    if len(s) > 0:
      res_expr.append(s if s not in symbols else symbols[s])

  return ''.join(res_expr)

def process_file(file_in, file_out, **kwargs):

  # Read the file in full (we have enough ram)
  f = open(file_in)
  lines = f.readlines() 
  f.close()

  ix = 0

  eval_list = {'ismpi':1}

  symbols = {}

  statements_raw, ix = consume_lines(lines, symbols, ix, 0)

  eval_symbols = kwargs.get('symbols')

  statements = []

  if eval_symbols:
    for s in statements_raw:
      if isinstance(s, if_stmt):
         r, res_s = s.eval_cond(eval_symbols)
         statements.append(res_s)
      else:
        statements.append(s)
  else:
    statements = statements_raw

  f = open(file_out, 'w')
  f.write(''.join(str(s) for s in statements))
  f.close()

def consume_lines(lines, symbols, ix, level):
  
  statements = []

  lines_ct = len(lines)

  ifs = None

  while ix < lines_ct:

    top = lines[ix]

    if top.startswith('#define'):
      ds = def_stmt(top)

      if level == 0:
        symbols[ds.name] = ds

      statements.append(ds)
      ix += 1
    elif top.startswith('#if'):
      ifs = if_stmt(top)
      ifs.first, ix = consume_lines(lines, symbols, ix+1, level+1)
    elif top.startswith('#else'):
      if ifs:
        ifs.second, ix = consume_lines(lines, symbols, ix+1, level+1)
      else:
        return statements, ix
    elif top.startswith('#endif'):
      if ifs:
        statements.append(ifs)
        ix += 1
        ifs = None
      else:
        return statements, ix
    else:
      statements.append(top)
      ix += 1

  return statements, ix
  
def build_argparse():

  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('file_in', metavar='input', help='Intput file')
  parser.add_argument('-o', dest='file_out', metavar='output', default='code.F', help='Output file')
  parser.add_argument('-D', dest='symbols', metavar='key=value', nargs='*', help='Space separated key=value to evaluate')
  
  return parser

def main():

  parser = build_argparse()

  args = parser.parse_args()

  symbols = dict(s.split('=') for s in args.symbols) if args.symbols else {}

  process_file(args.file_in, args.file_out, symbols=symbols)

if __name__ == '__main__':
  main()
