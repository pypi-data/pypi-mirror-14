#!/usr/bin/env python

'''
This thing consists of a master rank which sends out work to worker ranks. Both
master and worker do work using multiple python threads. These are not exactly OS
threads and can not really run on multiple cores but they are ok for data processing
since the executables will run on separate cores ok.

It can operate in 2 modes: Processing or Rendering.

In processing mode each dump-variable is reformated, bob2hv-ed, rendered to png
using the provided keys. Rendering is done as a step of the processing, not in
a separate thread. This makes things much more simple at the cost of less
efficient hardware usage. At some point we can probably overlap processing and
rendering and gain a minute or something processing time per dump. Too complicated
right now.

To use `python on Blue Waters <https://bluewaters.ncsa.illinois.edu/python>`_ one must load the gnu environment, 
load python, python mpi and opengl 

.. code:: bash

  module swap PrgEnv-cray PrgEnv-gnu
  module load bwpy
  module load bwpy-mpi
  module load opengl

'''

__version__ = 5.1

# TODO: Capture Ctrl+C  (nompi) http://snakesthatbite.blogspot.com/2010/09/cpython-threading-interrupting.html
# TODO: Make default options process everything
# TODO: Simplify command line options (--vars)
# TODO: Processing status report (dump: processed, hvs)

import argparse
import gzip
import hashlib
import io
import os
import threading
import time
import logging
import lockfile
import shutil
import signal
import subprocess
import sys
import tempfile
import Queue

log = logging.getLogger(__name__)
log.propagate = False
ch = logging.StreamHandler()
log.addHandler(ch)
log.setLevel(logging.INFO)
#log.setLevel(logging.DEBUG)

try:
  import lcse
  hvr_enabled = True
except ImportError:
  hvr_enabled = False
  error = "Warning: LCSE Python library not found, HVR rendering disabled"
  log.error(error)

from lcse_tools import ppm_plots

tag_ready = 1
tag_dump = 2

variable_list = [
    dict(name='fv', original='FV-hires-01', dir='FV-hiret-01', file='FV-hiret01', ext='bob8aaa', resolution=2),
    dict(name='vort', original='Lg10Vort-01', dir='Lg10Voru-01'),
    dict(name='enuc', original='Lg10ENUCbyP', dir='Lg10ENVCbyP'),
    dict(name='uy', original='TanhUY--001', dir='TanhUY-0001'),
    dict(name='divu', original='TanhDivU-01', dir='TanhDivV-01')
    ]

var_map = dict((k['name'], k) for k in variable_list)
#var_map = dict((k['dir'], k) for k in variable_list)
variables_original = [k['original'] for k in variable_list]

dir_t = '{dir:s}/{dump:04d}/{var:s}'
dir_var_t = '{dir:s}/{var:s}'
dir_var2_t = '{dir:s}/{var:s}-{suffix:s}'

filename_t = '{var:s}-{dump:04d}.{ext:s}'
path_t = '{dir:s}/{var:s}/{var:s}-{dump:04d}.{ext:s}'
path2_t = '{dir:s}/{var:s}-{suffix:s}/{var:s}-{suffix:s}-{dump:04d}.{ext:s}'

# 1010/FV-hiret-01/FV-hiret01-1010.bob8aaa
# 1010/Lg10Voru-01/Lg10Voru-01-1010.bobaaa
# 1010/TanhUY-0001/TanhUY-0001-1010.bobaaa
# 1010/TanhDivV-01/TanhDivV-01-1010.bobaaa
# 1010/Lg10ENVCbyP/Lg10ENVCbyP-1010.bobaaa

#TODO: Remove this garbage
class keyfile_reader(object):

  #TODO: Change image with / height
  def __init__(self, filename, hv_dir, img_dir, image_size):

    self.key_name = os.path.basename(filename)[:-4]

    self.hv_dir = os.path.normpath(hv_dir) if hv_dir else None
    self.img_dir = os.path.normpath(img_dir) if img_dir else None
    self.image_size = image_size

    self.key = lcse.hvr_key(filename)
    hvfile = self.key.get('hvfile')

    self.var = os.path.basename(hvfile)[:-8]

    if hv_dir:
      self.key._data['hvfile'] = os.path.join(hv_dir, os.path.basename(hvfile))

last_sigint = None

def sig_int_handler(signal, frame):
  global last_sigint

  log.info("Received signal %s last %s" % (signal, last_sigint))

  t = time.time()

  if last_sigint is not None and (t - last_sigint) < 5.0:
    log.info("Received second Ctrl+C within 5 seconds, exiting")
  sys.exit(0)

  last_sigint = t

def setup_logging(args):

  if not args.mpi:
    try:
      from colorlog import ColoredFormatter

      formatter = ColoredFormatter("%(log_color)s %(asctime)s - %(levelname)s : %(white)s%(message)s",
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
      return
    except:
      pass

 # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  ch.setFormatter(formatter)

  if args.log:
    if not os.path.exists(args.logs_dir):
      os.makedirs(args.logs_dir)

    fh = logging.FileHandler(os.path.join(args.logs_dir, args.log))
    fh.setFormatter(formatter)
    log.addHandler(fh)

def execute(rank, thread, cmd, cwd=None):

  if cmd[0].startswith('.'):
    cmd[0] =  os.path.abspath(cmd[0])
    print cmd[0]

  cmd_line = ' '.join(cmd)
  log.info("rank %i.%i : exec '%s'" % (rank, thread, cmd_line))
  a = time.time()

  try:
    p = subprocess.Popen(cmd_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, shell=True)
    p.communicate()
    ret_val = p.wait()
  except Exception as e:
    log.warning("execute() caught an exception %s" % e)
    ret_val = -1

  b = time.time()
  duration = b - a
  log.info("rank %i.%i : exec '%s' finished with code %i in %f.2" % (rank, thread, cmd_line, ret_val, duration))

  return (ret_val, duration)

def get_dumps(args):

  if args.auto:
    dumps_contents = [d for d in os.listdir(args.dumps_dir) if os.path.isdir(os.path.join(args.dumps_dir, d))]
    dumps = [int(c) for c in dumps_contents if c.isdigit()]

    if not dumps and args.render:
      dumps = list(set([int(hv[-7:-3]) for hv in os.listdir(args.hvs_dir) if hv.endswith('.hv')]))

  else:
    # Should be able to run for 1 or a range of dumps
    dumps = args.dumps if len(args.dumps) == 1 else range(args.dumps[0], args.dumps[1]+1)

  dumps.sort()

  if args.start_dump:
    log.info("Starting from dump %i" % args.start_dump)
    dumps = [d for d in dumps if d > args.start_dump]

  log.debug("Dumps are: %s" % dumps)

  return dumps

def get_keys(args):
  return

def remove_processed(vars, dumps):

  #TODO: Write this list as a shell script
  # for creating paths
  hv_contents = os.listdir(args.hvs_dir)

  # Generate list of all files
  hvr_dict = dict(ext='hvr', var='', dump='')

  for var in vars:
    for dump in dumps:
      names.append(filename_t.format(dump=dump, var=var, ext='hvr'))

#
def archive_dump(args, thread_id, dump):
  """
  We take files like ./0340/FV-hires-01/FV-hires01-0340.bob8abd and compress them into
  ./dump-archive/FV-hires-01/FV-hires-01-0340.gz/FV-hires01-0340.bob8abd.gz
  """

  results = {}

  log.info("rank %i.%i : started archiving dump %i" % (args.rank, thread_id, dump))

  output_dir = args.archive_dir

  gzip_path_t = '{dir:s}/{var:s}/{var:s}-{dump:04d}.gz/'
  gzip_filename = '{filename:s}.gz'

  #unpack_command = 'gzip -d {gzip:s};\nmv {file:s} {dest:s}'

  for var in variables_original:

    var_dir = var_map[var]['dir']

    bob_dir = dir_t.format(dir=args.dumps_dir, dump=dump, var=var_dir)
    bob_files = os.listdir(bob_dir)
    bob_files.sort()

    dir_out = gzip_path_t.format(dir=args.archive_dir, var=var_dir, dump=dump)

    if not os.path.exists(dir_out):
      os.makedirs(dir_out)

    hashes_path = os.path.join(dir_out, 'hashes.md5')
    moveum_path = os.path.join(dir_out, 'uncompressum.sh')
    verifyum_path = os.path.join(dir_out, 'verifyum.sh')

    if os.path.exists(hashes_path):
      log.warning("rank %i.%i : hashes file %s already exists skipping this dump/variable" % (args.rank, thread_id, hashes_path))
      continue

    hashes = []
    file_pairs = []

    for filename in bob_files:

      path_in = os.path.join(bob_dir, filename)
      filename_gz = gzip_filename.format(filename=filename)
      path_out = os.path.join(dir_out, filename_gz)

      file_pairs.append((filename, filename_gz))

      if os.path.exists(path_out):
#        log.info("rank %i.%i : gzip file %s exists, skipping" % (args.rank, thread_id, path_out))
        log.warn("rank %i.%i : gzip file %s exists, not skipping (for safety)" % (args.rank, thread_id, path_out))

      #TODO: Timing information
      with open(path_in, 'rb') as f_in, gzip.open(path_out, 'wb') as f_out:

        data_in = f_in.read()

        # Gzip save the data
        f_out.write(data_in)

        # Compute MD5 sum
        m = hashlib.md5()
        m.update(data_in)

        hash = m.hexdigest()
        hashes.append((filename, hash))

        log.info("rank %i.%i : gziping file %s (md5sum: %s) to %s" % (args.rank, thread_id, path_in,
                                                                      hash, path_out))

    if not hashes:
      continue

    # Write out the uncompressed hashes file
    with io.open(hashes_path, 'wb') as f:
      f.writelines('%s *%s\n' % (hash, filename) for filename, hash in hashes)
      log.debug("rank %i.%i : wrote hashes to %s" % (args.rank, thread_id, hashes_path))

    out_path = '../../uncompressed-dumps/%04d/%s' % (dump, var_dir)

    # Write out the moveum file
    with io.open(moveum_path, 'wb') as f:
      f.write("mkdir -p %s\n" % out_path)
      f.writelines('gzip -cd %s > %s/%s\n' % (filename_gz, out_path, filename) for filename, filename_gz in file_pairs)
      log.debug("rank %i.%i : wrote moveum to %s" % (args.rank, thread_id, hashes_path))

    # Write out hashes file
    with io.open(verifyum_path, 'wb') as f:
      for filename, hash in hashes:
        f.write('''a=`gzip -cd %s.gz | md5sum | awk '{print $1}'`; b="%s"; \n''' % (filename, hash))
        f.write('''if [ "$a" == "$b" ]; then echo "%s ok"; else echo %s fail"; fi; unset a; unset b; \n\n''' % (filename, filename));

      log.debug("rank %i.%i : wrote verifyum to %s" % (args.rank, thread_id, hashes_path))


  log.info("rank %i.%i : finished archiving dump %i" % (args.rank, thread_id, dump))

  return results

def process_dump(args, dump, thread_id):

  log.info("rank %i.%i : started processing dump %i" % (args.rank, thread_id, dump))

  results = {}

  # Process the dumps
  rank = args.rank

  vars = []
  existing = []

  to_process = []

  for var in args.vars:

    var_dir = var_map[var]['dir']

    hv_dir = dir_var_t.format(dir=args.hvs_dir, var=var_map[var].get('file', var_dir))
    hv_file = path_t.format(dir=args.hvs_dir, var=var_map[var].get('file', var_dir), dump=dump, ext='hv')

    if not os.path.exists(hv_file):
      vars.append(var)
      to_process.append((var, hv_dir))
    else:
      existing.append(var)

  # Check if we are duplicating something
  # TODO: Could reuse the paths here
  results['existing'] = existing

  xreformat_path = args.xreformat_exec
  bob2hv_path = args.bob2hv_exec

  # Clean up any stale old files
  rm_cmd = []
  if args.cleanup or args.reformat:
    rm_cmd.extend(['rm', '-rf'])
    rm_cmd.extend([dir_t.format(dir=args.dumps_dir, dump=dump, var=var_map[var]['dir']) for var in args.vars])

  if vars and args.reformat:
    dump_str = '%04i' % dump

    # Remove old and stale stuff before running reformat
    execute(args.rank, thread_id, rm_cmd)

    cwd = args.dumps_dir if args.multidir else dir_t.format(dir=args.dumps_dir, dump=dump, var=var_map[to_process[0][0]]['original'])
    log.warning("CWD is " + cwd)

    reformat_cmd = [xreformat_path, dump_str, dump_str, ">> ./logs/process.%s.log 2>&1" % dump_str]
    ret_val, t = execute(args.rank, thread_id, reformat_cmd, cwd=cwd)
    results['reformat'] = dict(ret=ret_val, duration=t)

  if args.bob2hv:
   results['bob2hv'] = {}
   results['mv_hv'] = {}

  for var, hv_dir in to_process:
    var_info = var_map[var]
    var_dir = var_info['dir']
    res = var_info.get('resolution', 1)
    ext = var_info.get('ext', 'bobaaa')
    file_prefix = var_info.get('file', var_dir)
    dump_dir = dir_t.format(dir=args.dumps_dir, dump=dump, var=var_dir)

    # Run bob2hv
    if args.bob2hv:
      if not os.path.exists(dump_dir):
        log.info("rank %i.%i : skipping %4i:%s because %s does not exist" % (args.rank, thread_id,
                                                                             dump, var, dump_dir))
        continue

      size = [str(res * i) for i in args.tile_size]
      teams = [str(t) for t in args.tiles]
      bob_filename = filename_t.format(dump=dump, var=file_prefix, ext=ext)
      bob2hv_cmd = [bob2hv_path, str(size[0]), str(size[1]), str(size[2]),
                    bob_filename, '-t', teams[0], teams[1], teams[2], '-s', '128',
                   ">> ../../logs/process.%04i.log 2>&1" % dump]
      ret_val, duration = execute(args.rank, thread_id, bob2hv_cmd, cwd=dump_dir)
      results['bob2hv']['vars'] = dict(ret=ret_val, duration=duration)

      if not os.path.exists(hv_dir):
         os.makedirs(hv_dir)

      hv_file_path = os.path.join(dump_dir, filename_t.format(dump=dump, var=file_prefix, ext='hv'))

      if not os.path.exists(hv_file_path):
        log.warning("rank %i.%i : hv %s not created for dump %4i" % (args.rank, thread_id,
                                                                     hv_file_path, dump))
        continue

      mv_cmd = ['mv', hv_file_path, hv_dir]

      ret_val, duration = execute(args.rank, thread_id, mv_cmd)
      results['mv_hv']['vars'] = dict(ret=ret_val, duration=duration)

      results['success'] = True

  if args.cleanup:
    execute(args.rank, thread_id, rm_cmd)

  log.info("rank %i.%i : finished processing dump %i" % (args.rank, thread_id, dump))

  return results

def render_dump(args, thread_id, dump):

  log.info("rank %i.%i : started rendering dump %4i" % (args.rank, thread_id, dump))

  hvr_path = args.hvr_exec
  keys = args.keys

  results = {'success': False}

  for key in keys:

    for var in args.specified_vars:

      if var not in args.lut_map:
        log.info("rank %i.%i : skipping dump %4i variable %s because no lut was provided" % (args.rank, thread_id, dump, var))
        continue

      size_str = 'x'.join(str(d) for d in key.key.get('imagesize'))

      hv_name = var_map[var].get('file', var_map[var]['dir'])
      hv_file = path_t.format(dir=args.hvs_dir, var=hv_name, dump=dump, ext='hv')

      if not os.path.exists(hv_file):
        log.warning("rank %i.%i : skipping dump %4i because %s does not exist" % (args.rank, thread_id,
                                                                                  dump, hv_file))
        continue

      var_name = var_map[var]['original']
      luts = args.lut_map[var]

      for lut in luts:

        #suffix = '%s-%s' % (lut.name, key.key_name)
        suffix = '%s-%s' % (lut.name, key.key_name) if len(luts) > 1 else key.key_name

        # Have to remap the annoying Fv-hires thing
        raw_file = path2_t.format(dir=args.images_dir, var=var_name, dump=dump, suffix=suffix, ext='raw')
        png_file = path2_t.format(dir=args.images_dir, var=var_name, dump=dump, suffix=suffix, ext='png')
        var_dir = dir_var2_t.format(dir=args.images_dir, var=var_name, suffix=suffix)

        if not os.path.exists(var_dir):
          os.makedirs(var_dir)

        if os.path.exists(png_file):
          log.info("rank %i.%i : skipping dump %4i because %s exists" % (args.rank, thread_id, dump,
                                                                       png_file))
#          results['success'] = True
          continue

        if not os.path.exists(raw_file):
          key.key._data['hvfile'] = hv_file
          key.key._data['imagefile'] = raw_file
          key.key.lut = lut

#        key_filename = os.path.join(args.temp_dir, "%s_tmp_%s.key" % (var, key.key_name))
#        key.key.save(key_filename)

          _, key_filename = tempfile.mkstemp(prefix='%s-%s' % (var_name, suffix), dir=args.temp_dir)

          with open(key_filename, 'wb') as key_file:
            key_file.write(str(key.key))

          log.debug('rank %i.%i : calling hvr for %s, temp %s' % (args.rank, thread_id, hv_file, key_filename))

          hvr_cmd = [hvr_path, '<', key_filename]
#          hvr_cmd = [hvr_path, '<', key_filename, ">> ./logs/render.%04i.log 2>&1" % dump]
          ret,_ = execute(args.rank, thread_id, hvr_cmd)

#          log.debug('rank %i.%i : calling hvr for %s' % (args.rank, thread_id, hv_file))
#          key_string = str(key)
#          p = subprocess.Popen(hvr_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#          output = p.communicate(key_string)
#          ret = p.wait()
          log.debug('rank %i.%i : hvr exit with code %i' % (args.rank, thread_id, ret))

        if os.path.exists(raw_file):
          convert_cmd = ['convert','-depth','8','-flip', '-size', size_str, 'rgb:%s' % raw_file, png_file]
          ret,_ = execute(args.rank, thread_id, convert_cmd)

          # Delete .raw file only if we converted it to png successfuly
          if ret == 0:
            rm_raw_cmd = ['rm', '-f', raw_file]
            ret = execute(args.rank, thread_id, rm_raw_cmd)
            results['success'] = True

  log.info("rank %i.%i : finished rendering dump %4i, success %s" % (args.rank, thread_id, dump, results['success']))

  return results

def render_keyfile(args, thread_id, keyfile):

  hvr_path = args.hvr_exec

  key = keyfile_reader(keyfile, args.hvs_dir, args.images_dir, args.image_size)
  raw_file = os.path.join(args.images_dir, '%s.raw' % key.key_name)
  png_file = os.path.join(args.images_dir, '%s.png' % key.key_name)

  results = {}

  log.info("rank %i.%i : started rendering keyfile %s" % (args.rank, thread_id, keyfile))

  if os.path.exists(png_file):
    log.info("rank %i.%i : skipping keyfile %s because %s exists" % (args.rank, thread_id, keyfile, png_file))
    return results

  key.key.set('imagefile', raw_file)

  key_filename = "%s_%04i_%04i_tmp.key" % (key.key_name, args.rank, thread_id)
  key.save(key_filename)

  hvr_cmd = [hvr_path, '<', key_filename, ">> ./logs/render.%s.log 2>&1" % key.key_name]
  ret,_ = execute(args.rank, thread_id, hvr_cmd)

  if os.path.exists(raw_file):
    size = key.key.get('imagesize')
    convert_cmd = ['convert','-depth','8','-flip', '-size', 'x'.join(size), 'rgb:%s' % raw_file, png_file]
    ret, duration = execute(args.rank, thread_id, convert_cmd)

  if ret == 0:
    rm_raw_cmd = ['rm', '-f', raw_file]
    ret, _ = execute(args.rank, thread_id, rm_raw_cmd)

  log.info("rank %i.%i : finished rendering keyfile %s" % (args.rank, thread_id, keyfile))

  return results

def work_thread_main(args, in_queue, out_queue, thread_id):
  '''Process data from in_queue and write it to out_queue'''

# TODO: Make the lock more generic so it locks anything we need .lock.<work_type>
# TODO: The message payload should indicate the type of work we are doing

  processing = args.bob2hv or args.cleanup or args.reformat
  rendering = args.render and hvr_enabled

  log.info("rank %i.%i : work_thread_main" % (args.rank, thread_id))

  while True:
    work = in_queue.get()

    if isinstance(work, dict) and work.get('exit'):
      log.info("rank %i.%i : worker commanded to exit" % (args.rank, thread_id))
      break

    results = {'work':work}

    try:

      if not work and work != 0:
        log.info("rank %i.%i : worker is out of work, exiting. (work %s)" % (args.rank, thread_id, str(work)))
        break

      if args.plot:
        results.update(plot_dump(args, thread_id, work))

      if args.render_keys:
        keyfile = work
        results.update(render_keyfile(args, thread_id, keyfile))

      elif processing or rendering:
        dump = work

        log.debug("rank %i.%i : worker start processing unit %s" % (args.rank, thread_id, work))

        if processing:
          lock_path = dir_t.format(dir=args.dumps_dir, dump=dump, var='.dpp%s' % args.lock_name)
          lock = lockfile.LockFile(lock_path)

          if lock.is_locked():

            lock_age = time.time() - os.path.getctime(lock.lock_file)

            #  Anything over 60 minutes is stale
            if lock_age > 3600.0:
              log.info("rank %i.%i : found stale lock (%i s) on %4i" % (args.rank, thread_id,
                                                                        int(lock_age), dump))
              lock.break_lock()

          try:
            lock.acquire(timeout=-1)

            results.update(process_dump(args, dump, thread_id))

            lock.release()
          except lockfile.AlreadyLocked:
            log.warning("rank %i.%i : dump %4i is locked, skipping" % (args.rank, thread_id, dump))

        if rendering:
          results.update(render_dump(args, thread_id, work))

      elif args.archive:
        results.update(archive_dump(args, thread_id, work))

    except IndexError as e:
#    except Exception as e:
      log.error("rank %i.%i : failed processing work %s with Exception: %s" % (args.rank,
                                                                               thread_id, work,e))
    in_queue.task_done()
    out_queue.put(results)

def monitor_thread_main(args, work_queue, start_dumps):

  sleep_time = 60
  known = list(start_dumps)
  thread_id = 0

  while True:
    dumps = get_dumps(args)
    new_dumps = [d for d in dumps if d not in known]
    new_dumps.sort()
    # Last dumps is sort of invalid anyway
    new_dumps = new_dumps[:-1]

    if new_dumps:
      log.info("rank %i.%i : monitor found new dumps %s" % (args.rank, thread_id, new_dumps))

      for d in new_dumps:
        work_queue.put(d)
        known.append(d)

    time.sleep(sleep_time)

def plot_dump(args, thread_id, dump):
  """ Plot all of the things """

  rp = args.rp_set.get_file(dump)

  fig = args.fig
  plot_path = args.plot_dir

  dump = rp.get('dump')
  log.info("rank %i.%i : plotting dump %04i" % (args.rank, thread_id, dump))

  fig.clear()
  ppm_plots.plot_ceul_mach_global(rp, fig, path=plot_path)

  fig.clear()
  ppm_plots.plot_ekr_ekt_entropy(rp, fig, path=plot_path)

  # Linear plots
  for var in ["enuc", "fnuc"]:
    fig.clear()
    ppm_plots.plot_var_one_bucket(rp, var, fig, path=plot_path)

  # Log plots
  for var in ["enuc", "fnuc", "fv_hi"]:
    fig.clear()
    ppm_plots.plot_log_var_one_bucket(rp, var, fig, path=plot_path)

  # Process per-dump things
  for bucket in range(1, rp.get('nbuckets') + 1):
    for var in ["enuc", "fv_hi", "p"]:

      fig.clear()
      ppm_plots.plot_log_var_one_bucket(rp, var, fig, path=plot_path, bucket=bucket)

      fig.clear()
      ppm_plots.plot_var_one_bucket(rp, var, fig, path=plot_path, bucket=bucket)

  return {}

def worker_thread_manager(args, in_queue, out_queue):

  threads = []
  nthreads = args.threads

  for thread_id in range(1, nthreads+1):
    log.info("rank %i.%i : worker_thread_manager spawning thread %i " % (args.rank, 0, thread_id))

    t = threading.Thread(target=work_thread_main, args=(args, in_queue, out_queue, thread_id))
    t.daemon = True
    t.start()

    threads.append(t)

  return threads

def mpi_worker_main(comm, args):
  '''Query server for new data and process it'''

  processing = args.bob2hv

  process_q = Queue.Queue()
  ready_q = Queue.Queue()

  nthreads = args.threads

  log.debug("rank %i.%i : mpi_worker_main asking for work" % (args.rank, 0))

  comm.send({'ready':True, 'units':nthreads}, dest=0, tag=1)
  data = comm.recv(source=0, tag=2)
  work_units = data.get('work')

  threads = worker_thread_manager(args, process_q, ready_q)

  while work_units:

    for w in work_units:
      process_q.put(w)

    log.info("rank %i.%i : Waiting for item" % (args.rank, 0))
    results = ready_q.get()
    log.info("rank %i.%i : Got item %s " % (args.rank, 0, results))

    comm.send({'ready':True, 'results':results}, dest=0, tag=1)
    log.info("rank %i.%i : sent %s to leader" % (args.rank, 0, results))

    data = comm.recv(source=0, tag=2)
    log.info("rank %i.%i : recv %s from leader" % (args.rank, 0, data))
    work_units = data.get('work')

  # Wait for all items to finish
  log.info("rank %i.%i : mpi_worker_main waiting for all items to finish" % (args.rank, 0))
  process_q.join()

  for i in range(nthreads):
    process_q.put({'exit':True})

  results = []

  log.info("rank %i.%i : mpi_worker_main collecting final results" % (args.rank, 0))
  while not process_q.empty():
    results.append(process_q.get())

  log.info("rank %i.%i : mpi_worker_main reporting final results" % (args.rank, 0))
  comm.send({'ready':False, 'results':results}, dest=0, tag=1)

def run_el_presidente(args):
  '''Main routine for work distribution rank'''

  rendering = (args.render_keys or args.render) and hvr_enabled

  log.info("El Presidente version %s: starting %s " % (str(__version__), "rendering" if (args.render_keys) else "processing"))

  # Make directories
  dirs_to_make = [args.logs_dir]

  if args.bob2hv: dirs_to_make.append(args.hvs_dir)
  if rendering: dirs_to_make.extend([args.images_dir])
  if args.plot: dirs_to_make.append(args.plots_dir)

  for d in dirs_to_make:
    if not os.path.exists(d):
      os.makedirs(d)

  process_q = Queue.Queue()
  ready_q = Queue.Queue()

  work_units = []
  processed = []

  if args.render_keys:
    keys_dir = args.render_keys
    work_units = [dict(keyfile=os.path.join(keys_dir, f)) for f in os.listdir(keys_dir) if f.endswith('.key')]
  else:
    work_units = get_dumps(args)

  for w in work_units:
    process_q.put(w)

  log.info("El Presidente: starting worker-thread manager")
  threads = worker_thread_manager(args, process_q, ready_q)

  if args.monitor:
    #TODO: This should be able to monitor a directory for keys?
    t = threading.Thread(target=monitor_thread_main, args=(args, process_q, work_units))
    t.daemon = True
    t.start()

  if args.mpi:
    # Start MPI things that will be handling workers

    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    ranks = range(1,size)
    status = MPI.Status()

    wait_q = Queue.Queue()

    while True:
      msg_in = comm.recv(source=MPI.ANY_SOURCE, status=status, tag=tag_ready)

      log.debug("El Presidente: Received message %s" % msg_in)

      if status is None:
         log.error("el_presidente: Received status None")
         continue

      source = status.Get_source()
      units = msg_in.get('units', 1)

      log.info("El Presidente: Recieved request for %i units for %i " % (units, source))

      msg_out = {}
      work_out = []

      # Here if we are a monitor we will block on this and wait indefinitely for more
      # queue elements. If we are not a monitor we should terminate when the queue
      # is empty.

      try:
        for i in range(units):
          work_out.append(process_q.get(args.monitor))
      except Queue.Empty:
        log.info("El Presidente: out of work")
        break

      log.info("El Presidente: sending %s work to %i " % (work_out, source))
      comm.send({'work':work_out}, dest=source, tag=tag_dump)

    # Clean up
    log.info("Cleaning up %s " % ranks)
    for source in ranks:
      log.info("Cleaning up rank %i" % source)
      msg_in = comm.recv(source=source, status=status, tag=tag_ready)
      comm.send({'work':[]}, dest=source, tag=tag_dump)

  log.info("El Presidente: Waiting for Processing Queue to be complete")
  process_q.join()

  log.info("El Presidente: Sending Quit messages")
  for i in range(args.threads):
    process_q.put({'exit':True})

  log.info("El Presidente: Exiting")
  
  
def build_argparse():

  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--dumps', nargs='+',type=int, help='Manually specify dump number or dump range (e.g. `--dumps 355` or `--dumps 800 900)`')
  parser.add_argument('--start-dump', type=int, help='Start processing from this dump')
  parser.add_argument('--threads', type=int, default=1, help='Number of threads')
  parser.add_argument('--local', dest='mpi', action='store_false', help='Run without MPI')
  parser.add_argument('--process', action='store_true', help='reformat, generate HVs, move, cleanup')
  parser.add_argument('--render', action='store_true', help='Render dump after processing')
  parser.add_argument('--archive', action='store_true', help='Create a gzip archive of the dumps')
  parser.add_argument('--plot', action='store_true', help='Plot RProfiles')
  parser.add_argument('--plot-dir', default='./plots', help='')

  parser.add_argument('--archive-dir', default='./dump-archive', help='Directory containing dump files')
  parser.add_argument('--dumps-dir', default='.', help='Directory containing dump files')
  parser.add_argument('--hvs-dir', default='./hvs', help='Directory to move HV files')
  parser.add_argument('--logs-dir', default='./logs', help='Logs directory')
  parser.add_argument('--plots-dir', default='./plots', help='Directory for plots')
  parser.add_argument('--temp-dir', help='Temp directory')

  parser.add_argument('--lock-name', default='', help='Hack: Unique name for this lock (e.g. "bob" or "bob8")')
  parser.add_argument('--log', help='Log filename')

  p_group = parser.add_argument_group('Processing Options')
  p_group.add_argument('--reformat', action='store_true', help='Reformat bobs')
  p_group.add_argument('--bob2hv', action='store_true', help='Generate HV files')
  p_group.add_argument('--cleanup', action='store_true', help='Remove reformated bobs')
  p_group.add_argument('--monitor', action='store_true', help='Keep checking for new dumps to appear')
  p_group.add_argument('-t', '--tiles', nargs='+', type=int, help='Number of tiles (1 or 3 numbers)')
  p_group.add_argument('-g', '--tile-size', nargs='+', type=int, help='Size of a single tile (1 or 3 numbers)')
  p_group.add_argument('--bob2hv-exec', default='/u/sciteam/sandalsk/tools/bob2hv', help='')
  p_group.add_argument('--hvr-exec', default='/u/sciteam/sandalsk/lcse_serv/hvr_cl.exe', help='')
  p_group.add_argument('--xreformat-exec', default='./xreformat', help='')
  p_group.add_argument('--no-multidir', dest='multidir', action='store_false', default=True)

  r_group = parser.add_argument_group('Rendering Options')
  r_group.add_argument('--image-size', nargs='+', type=int, help='Image size as two space separated numbers (e.g. 1280 768). By default it uses the information from they key file')
  r_group.add_argument('--render-keys', help='Render key files in the given directory')
  r_group.add_argument('--keys', dest='key_files', nargs='+', help='A directory of key files or a list of key files to render for the selected dumps')
  r_group.add_argument('--images-dir', default='./images', help='Directory to store images')

  # Variable specific color maps that are used instead of the stuff inside the .lut
  r_group.add_argument('--lut-fv', nargs='+', help='')
  r_group.add_argument('--lut-vort', nargs='+', help='')
  r_group.add_argument('--lut-uy', nargs='+', help='')
  r_group.add_argument('--lut-enuc', nargs='+', help='')
  r_group.add_argument('--lut-divu', nargs='+', help='')

  v_group = parser.add_argument_group('Variables')
  v_group.add_argument('--all-vars', action='store_true', help='Process all things (fv, enuc, vort, divu, uy) (default)')
  v_group.add_argument('--fv', action='append_const', const='fv', dest='vars', help='FV High-Res (FV-hires-01)')
  v_group.add_argument('--vort', action='append_const', const='vort', dest='vars', help='Vorticity (Lg10Vort-01)')
  v_group.add_argument('--uy', action='append_const', const='uy', dest='vars', help='(TanhUY--001)')
  v_group.add_argument('--enuc', action='append_const',  const='enuc', dest='vars', help='Process Enuc files (Lg10ENUCbyP)')
  v_group.add_argument('--divu', action='append_const', const='divu', dest='vars', help='(TanhDivU-01')

#  v_group.add_argument('--fv', action='append_const', const='FV-hiret-01', dest='vars', help='FV High-Res (FV-hires-01)')
#  v_group.add_argument('--vort', action='append_const', const='Lg10Voru-01', dest='vars', help='Vorticity (Lg10Vort-01)')
#  v_group.add_argument('--uy', action='append_const', const='TanhUY-0001', dest='vars', help='(TanhUY--001)')
#  v_group.add_argument('--enuc', action='append_const',  const='Lg10ENVCbyP', dest='vars', help='Process Enuc files (Lg10ENUCbyP)')
#  v_group.add_argument('--divu', action='append_const', const='TanhDivV-01', dest='vars', help='(TanhDivU-01')

  return parser

def main():


  # Available variables
  parser = build_argparse()
  
  args = parser.parse_args()

  setup_logging(args)

  if not args.render_keys:
    args.auto = not (args.dumps and len(args.dumps) <= 2)

  args.rank = 0


  # If the grid is symmetric we want to be able to specify only one size
  if args.tile_size:
    args.tile_size = args.tile_size if len(args.tile_size) == 3 else 3 * [args.tile_size[0]]

  if args.tiles:
    args.tiles = args.tiles if len(args.tiles) == 3 else 3 * [args.tiles[0]]

  if args.process:
    args.reformat = True
    args.bob2hv = True
    args.cleanup = True

  if args.plot:
    args.rp_set = lcse.rprofile_set(path="./RProfile-01", lazy=False, logging=True)
    args.fig = ppm_plots.new_figure()

  if args.vars:
    args.specified_vars = args.vars
  else:
    args.vars = var_map.keys()
    args.specified_vars = []

  if args.bob2hv and not (args.tile_size and args.tiles):

    reformat_file = 'Reformat-mPPM.F'

    if os.path.exists(reformat_file):
      defines = dict(l.split()[1:] for l in open(reformat_file).readlines() if l.startswith('#define'))
      defines_expanded = dict([(k, defines.get(v, v)) for k,v in defines.items()])

      args.tiles = [int(defines_expanded[v]) for v in ['nnxteams', 'nnyteams', 'nnzteams']]
      args.tile_size = [int(defines_expanded['nnnn%s' % v]) * int(defines_expanded['nnt%sbricks' % v]) for v in ['x', 'y', 'z']]

      log.info("Parsing %s indicates %s tiles of size %s" % (reformat_file, args.tiles, args.tile_size))
    else:
      log.error("Tile-size and number of tiles are required for bob2hv. Specify -t and -g options or a `Reformat-mPPM.F` file.")
      return 1

  # Here we go over the key files and create key objects
  args.keys = []

  if args.key_files:

    if len(args.key_files) == 1 and os.path.isdir(args.key_files[0]):
      keys_dir = args.key_files[0]
      args.key_files = [os.path.join(keys_dir, f) for f in os.listdir(keys_dir) if f.endswith('.key')]

    for k in args.key_files:
      log.debug("main() generating key for %s" % (k))
      key = keyfile_reader(k, args.hvs_dir, args.images_dir, args.image_size)
      args.keys.append(key)

  lut_file_map = {}

  # HACK:
  if args.lut_fv:
    lut_file_map['fv'] = args.lut_fv
  if args.lut_vort:
    lut_file_map['vort'] = args.lut_vort
  if args.lut_enuc:
    lut_file_map['enuc'] = args.lut_enuc
  if args.lut_divu:
    lut_file_map['divu'] = args.lut_divu
  if args.lut_uy:
    lut_file_map['uy'] = args.lut_uy

  args.lut_map = {}

  if lut_file_map:
    for k, v in lut_file_map.items():
      args.lut_map[k] = [lcse.lut(filename=f) for f in v]

  # Register the signal handler
#  signal.signal(signal.SIGINT, sig_int_handler)
#  signal.pause()

  if args.mpi:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD

    args.rank = comm.Get_rank()
    size = comm.Get_size()
    args.mpi = size > 0

    log.info("We are running in MPI mode, I am %s of %s" % (args.rank, size))

    if args.rank > 0:
      mpi_worker_main(comm, args)
      return

  # Either way we run El Presidente
  run_el_presidente(args)

if __name__ == '__main__':
  main()
