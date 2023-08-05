#!/usr/bin/env python

"""
Plot the standard set of plots

Usage:

.. code:: bash

  plot_rprofiles.py [<rprofile_path>] [<start_dump>]
"""

import matplotlib as mpl
mpl.use("Agg")
#mpl.use("Cairo")
import matplotlib.pyplot as plt

#from matplotlib import rc
#rc('mathtext', default='regular')

import numpy as np
import time
import os
import subprocess
import sys

import lcse
from lcse_tools import ppm_plots

def main():

  if len(sys.argv) < 2:
    print "Usage:\n plot_rprofiles.py [<rprofile_path>] [<start_dump>]"
    return

  rprofile_path = sys.argv[1] if len(sys.argv) > 1 else './RProfile-01'
  start_dump = int(sys.argv[2]) if len(sys.argv) > 2 else 0

  plot_path = 'plots'
  sleep_time = 15 * 60

  fig = plt.figure()

  if not os.path.exists('plots'):
    os.makedirs('plots')

  try:
    # Load all the dumps from last time
    f = open('processed.dat', 'r')
    processed = [int(k) for k in f.readlines()]
    f.close()
  except IOError:
    processed = []

  print "Loading RProfiles from %s" % rprofile_path
  rp_set = lcse.rprofile_set(rprofile_path, lazy=False, logging=True, stride=1, start_dump=start_dump)

  if not rp_set.dumps:
    print "No RProfiles found"

#  volumes = rp_set.get_dump().get_cell_volumes()

  # Cache for the plot_spike plot
  fuel_dumps = []
  fuel_times = []
  fuel_spikes = []

  interface_data = []
  time_data = []
  energy_data = []

  levels = (0.5, 0.1, 0.01, 0.001, 1e-5)

  while True:
    rp_set.check_for_new(path=rprofile_path)

    for rp in rp_set:
      dump = rp.get('dump')

      if dump == 0 or dump in processed:
        print 'Skipping dump %04d' % dump
        continue

      print 'Processing dump %04d' % dump

      fig.clear()
      ppm_plots.plot_ceul_mach_global(rp, fig, path=plot_path)

      fig.clear()
      ppm_plots.plot_ekr_ekt_entropy(rp, fig, path=plot_path)

      # Linear plots
      for var in ["enuc"]:
      #for var in ["enuc", "fnuc"]:
        fig.clear()
        ppm_plots.plot_var_one_bucket(rp, var, fig, path=plot_path)

      # Log plots
      for var in ["enuc", "fv_hi"]:
      #for var in ["enuc", "fnuc", "fv_hi"]:
        fig.clear()
        ppm_plots.plot_log_var_one_bucket(rp, var, fig, path=plot_path)


      # Process per-dump things
      processed.append(dump)

      # Fuel interface
      d = ppm_plots.get_interface_location(rp, levels)
      interface_data.append((dump, d))

      time_data.append('%0.f' % rp.get("timerescaled"))

#      enuc = rp.get_table('enuc')[0,:,1:]
#      enuc *= volumes
#      energy_data.append(enuc.sum())

    # Routines that require all buckets
    fig.clear()
#    fuel_dumps, fuel_times, fuel_spikes = ppm_plots.plot_spike(rp_set, fig, dumps=fuel_dumps, times=fuel_times,
#                                                               spikes=fuel_spikes, path=plot_path)

#    dumps, results = ppm_plots.get_interface_statistics(interface_data)

#    xlimits = None
#    ppm_plots.plot_interface(dumps, time_data, results, levels, filename='fv_interface.png',
#                             xlimits=xlimits, path=plot_path)
#
#    ppm_plots.plot_interface(dumps, time_data, results, levels, filename='fv_interface_sd_only.png',
#                             xlimits=xlimits, sd_only=True, path=plot_path)

#    ax = fig.add_subplot(1,1,1)
#    ax.ticklabel_format(useOffset=False)
#    ax.grid(True)
#    ax.set_ylabel("energy")
#    ax.set_xlabel("time [min]")
#
#    ax.plot(time_data, np.log10(energy_data), label="enuc_total")
#    ax.set_ylim([-6,0])
#    ppm_plots.save_fig(fig, "enuc_total", dump=0000, path=plot_path)

    # Save processed dumps
    processed.sort()
    f = open('processed.dat', 'w')
    f.write('\n'.join(str(k) for k in processed))
    f.close()

    # Sleep for a while
    time.sleep(sleep_time)

if __name__ == '__main__':
  main()
