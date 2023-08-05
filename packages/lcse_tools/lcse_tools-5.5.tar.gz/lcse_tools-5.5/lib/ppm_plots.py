#!/usr/bin/env python

'''
This file contains plotting routines for RProfile data. It is for now
the repository of all plot functions... should be moved somewhere.

# TODO: Add an installable script we can just run
'''

import os
import sys
import numpy as np
import logging

from matplotlib import colors
from matplotlib.path import Path
import matplotlib.patches as patches

import lcse
import image_util

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)

log = logging.getLogger(__name__)
log.propagate = False
log.addHandler(ch)
log.setLevel(logging.INFO)
#log.setLevel(logging.ERROR)

#########################################
#                                       #
#  Basic Building Blocks for Plotting   #
#                                       #
#########################################

colors = ['g', 'b', 'y', 'm']
styles = ['o-', 'v-', 'D-', 'x-', '<-', '*-', 'H-','+-', '^-','>-', '+-']

default_plot_path = './plots'

def get_styles(count):
  """Return `count` number of style attributes for plotting"""

  return [styles[ i % len(styles)] for i in range(count)]

def new_figure(figsize=None):
  """ 
     Create a new figure of size `figsize` that has a white background 
  """

#  log.info("Creating new figure")

  figsize = figsize if figsize else (12, 8)

  if "matplotlib" not in sys.modules:
    import matplotlib
    matplotlib.use("Agg")
   
  import matplotlib.pyplot as plt

  fig = plt.figure(figsize=figsize, facecolor='w', edgecolor='k')
  fig.patch.set_facecolor('white')
  fig.patch.set_alpha(1.0)
  return fig

def update_axis(ax, rp=None, **kwargs):
  """ `xlim` and `ylim` """

  xlim = kwargs.get('xlim')
  ylim = kwargs.get('ylim')

  ax.legend(loc=0)
  ax.grid(True)

  if xlim:
    ax.set_xlim(xlim)
  elif rp:
    ax.set_xlim((rp.get('radinner'), rp.get('radouter')))

  if ylim:
    ax.set_ylim(ylim)

def get_filename(prefix, **kwargs):
  """ 
  Construct a filename from `dump`, `bucket`, `path`, `filename`.
  """

  dump = kwargs.get('dump')
  bucket = kwargs.get('bucket', 0)
  filename = kwargs.get('filename')

  path = os.path.join(kwargs.get('path', default_plot_path), prefix)

  if not filename:
    pieces = [prefix]

    if bucket: pieces.append("_%03i" % bucket)
    
    if dump is not None: pieces.append("_%04i" % dump)
     
    pieces.append('.png')
    
    filename = ''.join(pieces)

  path_out = os.path.join(path, filename)
  log.debug("get_filename %s" % path_out)
  return path_out

def check_exists(prefix, **kwargs):

  filename = get_filename(prefix, **kwargs)

  if os.path.exists(filename):
    log.info("Skipping figure %s because it exists" % filename)
    return True
  else:
    return False

def save_fig(fig, prefix, **kwargs):
  """ 
  Save a figure 

  Keywords:

  `dump` 

  `dpi` the dpi for the figure, default is 200

  `path`

  `filename`

  `bucket`

  `tight` True/False to use fig.tight_layout

  """

  dpi = kwargs.get('dpi', 200)

  filename = get_filename(prefix, **kwargs)
  path = os.path.dirname(filename)

  if not os.path.exists(path):
    os.makedirs(path)

  if os.path.exists(filename):
    log.info("Skipping figure %s because it exists" % filename)
    return

  if kwargs.get("tight"):
    fig.tight_layout()

  fig.savefig(filename, dpi=dpi)
  log.info("Saved figure to %s" % filename)
  
  
#################################################
#                                               #
#  Generic or multi-purpose plotting routines   #
#                                               #
#################################################

def plot_var_one_bucket(rp, var, fig, **kwargs):
  ''' Plot the `var` with variable

  `xlim` and `ylim` are the axis limits
  '''

  bucket = kwargs.get('bucket', 0)
  dump = rp.get('dump')

  prefix = kwargs.get('prefix', '%s' % var)

  if check_exists(prefix, dump=dump, **kwargs):
    return

  y = rp.get('y_hi' if var == 'fv_hi' else 'y')

  data = rp.get_table(var)
  var_avg = data[0,:,bucket]
  var_min = data[1,:,bucket]
  var_max = data[2,:,bucket]
  var_sd = data[3,:,bucket]

  ax = fig.add_subplot(111)

  bucket_name = 'bucket %i' % bucket if bucket > 0 else 'global bucket'
  ax.set_title('%s for %s dump %04i' % (var, bucket_name, dump))
  ax.set_xlabel('Radius ($10^3 km$)')

  ax.plot(y, var_avg, 'k')
#  ax.plot(y, var_min,'b', label="min")
#  ax.plot(y, var_max,'r', label="max")
#  ax.errorbar(y, var_avg, yerr=var_sd,
#              label='average',
#              elinewidth=2, fmt='o', ecolor='g')

  update_axis(ax, rp=rp)

  save_fig(fig, prefix, dump=dump, **kwargs)
  return ax

def plot_log_var_one_bucket(rp, var, fig, **kwargs):
  ''' Plot the `var` multiplied by the volume of that shell
  `xlim` and `ylim` are the axis limits
  '''

  bucket = kwargs.get('bucket', 0)
  dump = rp.get('dump')

  prefix = kwargs.get('prefix', 'log_%s' % var)

  if check_exists(prefix, dump=dump, **kwargs):
    return

  y = rp.get('y_hi' if var == 'fv_hi' else 'y')
  d = rp.get_table(var)[0,:,bucket]

  ax = fig.add_subplot(111)

  bucket_name = 'bucket %i' % bucket if bucket > 0 else 'global bucket'

  ax.set_title('%s for %s dump %04i' % (var, bucket_name, dump))
  ax.set_xlabel('Radius ($10^3 km$)')
  ax.plot(y, np.log10(d),'k')

  update_axis(ax, rp=rp, **kwargs)

  save_fig(fig, prefix, dump=dump, **kwargs)
  return ax

def plot_var_many_buckets(rp, var, fig, **kwargs):
  ''' Create a plot of several buckets against the global
  of a single variable. Only min/max/sd for the global are
  shown

  `buckets` if specified is a list of buckets to add to the plot
            otherwise we plot everything
  '''

#  fig = kwargs.get('fig', new_figure())
  buckets = kwargs.get('buckets', range(rp.bucket_count + 1))

#  if check_exists(prefix, dump=dump, **kwargs):
#    return

  y = rp.get('y_hi' if var == 'fv_hi' else 'y')
  d = rp.get_table(var)

  ax = fig.add_subplot(111)

  ax.set_title('%s for many bucket' % (var))
  ax.set_xlabel('Radius ($10^3 km$)')

  ax.plot(y, d[0,:,0],'k')
  ax.plot(y, d[1,:,0],'b', label="min")
  ax.plot(y, d[2,:,0],'r', label="max")
  ax.errorbar(y, d[0,:,0], yerr=d[3,:,0],
                    elinewidth=2, fmt='o', ecolor='g')

  for bucket in buckets:
    ax.plot(y, d[0,:,bucket],'k')

  update_axis(ax, rp=rp, **kwargs)
  return ax

def plot_log_var_many_buckets(rp, var, fig, **kwargs):
  ''' Create a plot of several buckets against the global
  of a single variable. Only min/max/sd for the global are
  shown

  `buckets` if specified is a list of buckets to add to the plot
            otherwise we plot everything

  `min`

  `max`

  `labeled` if True each bucket plot is labled individualy 
  '''

  buckets = kwargs.get('buckets', range(rp.bucket_count + 1))

#  if check_exists(prefix, dump=dump, **kwargs):
#    return

  y = rp.get('y_hi' if var == 'fv_hi' else 'y')
  d = rp.get_table(var)

  ax = fig.add_subplot(111)

  ax.set_title('%s for many bucket' % (var))
  ax.set_xlabel('Radius ($10^3 km$)')
  ax.set_ylabel('$\log_{10}(%s)$' % var)

  ax.plot(y, np.log10(d[1,:,0]), 'b', label="min")
  ax.plot(y, np.log10(d[2,:,0]), 'r', label="max")
  ax.plot(y, np.log10(d[0,:,0]))

  labeled = kwargs.get('labeled')

  if labeled:
    for i, s in zip(buckets, style):
      ax.plot(np.log10(data[0,:,i]), s, label="%i" % i)
  else:
    for bucket in buckets:
      ax.plot(y, np.log10(d[0,:,bucket]), 'k')

  update_axis(ax, rp=rp, **kwargs)
  return ax

def plot_two_log_vars_buckets(rp, var1, var2, fig, buckets, xlim=None):
    
  data1 = rp.get_table(var1)
  data2 = rp.get_table(var2)

  styles = get_styles(len(buckets))

  ax = fig.add_subplot(111)
  ax2 = ax.twinx()
  
  print data1[0,:,5].shape
  
  for i, b in enumerate(buckets):
      ax.plot(np.log10(data1[0,:,i]), styles[i], label="%s - %i" % (var1, b))
      ax2.plot(np.log10(data2[0,:,i]), label="%s - %i" % (var2, b))

  ax2.plot(np.log10(data1[0,:,0]), "o", label="global %s" % var2)   
  ax.set_title("dump %i" % rp.get("dump"))
     
  if xlim:
      ax.set_xlim(xlim)
#     ax.set_ylim([-8, 0])
#     ax2.set_ylim([-8, 0])
 
  ax.grid()
  ax.legend(loc=2)
#    ax2.legend(loc=1)
  return ax, ax2
  
  
  
##############################################
#                                            #
#  Specialized and Single Purpose Routines   #
#                                            #
##############################################

def plot_ceul_mach_global(rp, fig, **kwargs):

  prefix = 'ceul_mach_global'

  dump = rp.get('dump')

  if check_exists(prefix, dump=dump, **kwargs):
    return

  y = rp.get('y')
  ceul = rp.get('ceul')
  mach = rp.get('mach')

  ax = fig.add_subplot(111)
  ax.set_title('$C_{eul}$ and Mach number for dump %4i' % dump)
  ax.set_xlabel('Radius ($10^3 km$)')

  ax.plot(y, ceul[2], '-', label='$\max C_{eul}$')
  ax.plot(y, ceul[0], '-', label='$C_{eul}$')
  ax.plot(y, ceul[1], '-', label='$\min C_{eul}$')

  ax2 = ax.twinx()
  ax2.plot(y, mach[2], 'r', label='max(M)')
  ax2.plot(y, mach[0], '+k', label='M')
  ax2.plot(y, mach[1], 'g', label='min(M)')

  update_axis(ax, rp=rp)

  ax.legend(loc=2, prop={'size':6})
  ax2.legend(prop={'size':6})

  save_fig(fig, prefix, dump=dump, **kwargs)
  return ax

def plot_ekr_ekt_entropy(rp, fig, **kwargs):
  ''' Do not use this method to loop over buckets and plot many of them
  since it will be quite inefficient.
  '''

  prefix = 'ekr_ekt_entropy_global'

  dump = rp.get('dump')

  if check_exists(prefix, dump=dump, **kwargs):
    return

  y = rp.get('y')
  ekr = rp.get('ekr')
  ekt = rp.get('ekt')
  p = rp.get('p')
  rho = rp.get('rho')

  entropy = p[0, :] / (rho[0, :]**(5./3.))

  ix_entropy = entropy > 0.0
  log_entropy = np.log10(entropy[ix_entropy])

  fig.clear()

  ax = fig.add_subplot(111)
  ax.set_title('ekr/ekt and entropy for dump %04i' % (dump))
  ax.set_xlabel('Radius ($10^3 km$)')

  ax.plot(y, ekr[0, :], 'r', label='ekr')
  ax.plot(y, ekt[0, :], 'g', label='ekt')

  ax2 = ax.twinx()
  ax2.plot(y[ix_entropy], log_entropy, 'b', label='log(A)')

  update_axis(ax, rp=rp)
  ax.legend(loc=2)
  ax2.legend(loc=1)

  save_fig(fig, prefix, dump=dump, **kwargs)
  return ax

def plot_unwraped_quantity(rp, data, label, fig, **kwargs):
  """ Plot a scatter plot where the points represent bucket centers
  
  `rp` ray profile instance
  
  `data` data with dimension of the size of the buckets.

  `label` the text string to use for the plot quantities
  
  `fig` instances
  
  
  """

  path = kwargs.get('path', '.')
  save = kwargs.get('save', False)
  normalize = kwargs.get('normalize', True)
  scale = kwargs.get('scale', 3000.0)
  global_range = kwargs.get('global_range')
  
  dump = rp.dump
  centers = rp.get_centers()

  phi_x = centers[0]
  theta_y = centers[1]
    
#     if not isinstance(scales, list):
#         scales = [scales for i in range(len(variables))]
    
#    colors = range(rp.get('nbuckets'))
#  cm = plt.cm.get_cmap('YlOrRd')
#  cm = plt.cm.get_cmap('bwr')
  
  mm = (data.min(), data.max()) if global_range is None else global_range
  
  if normalize:
    data = (data - mm[0]) / (mm[1] - mm[0])
    mm = (0.0, 1.0)

  colors = data
      
  fig.clear()
  ax = fig.add_subplot(111)
  
  ax.set_title('%s dump %4i' % (label, dump))
  ax.set_xlabel(r'$\phi$')
  ax.set_ylabel(r'$\theta$')
  ax.set_ylim([0.0, np.pi])

#    sc = ax.scatter(phi_x, theta_y, s=scale * data, c=colors, 
#                    alpha=0.5, vmin=mm[0], vmax=mm[1], cmap=cm)

  sc = ax.scatter(phi_x, theta_y,  s= scale * data,
                  alpha=0.5, vmin=mm[0], vmax=mm[1], norm=True)
    
  ax.set_xticks(np.pi * np.arange(-1, 1.5, 0.5))
  ax.set_xticklabels(["-$\pi$", "-$\pi/2$","0", "$\pi/2$", "$\pi$"])
  
  ax.set_yticks(np.pi * np.arange(0, 1.25, 0.25))
  ax.set_yticklabels(["0", "$\pi/4$", "$\pi/2$", "$3 \pi/4$", "$\pi$"])
     
  if kwargs.get("annotate"):
    for i in range(rp.get('nbuckets')):
      ax.annotate(str(i + 1), (phi_x[i], theta_y[i]))

  x = range(phi_x)
  ax.xticks(x, labels)

#    plt.colorbar(sc)

  if save:
    save_fig(fig, label, dump=dump)

  return ax

def plot_bucket_map(rp, fig=None):
  """Plot a map of bucket centers"""

  centers = rp.get_centers()
  phi_x = centers[0]
  theta_y = centers[1]
  
  if fig is None:    
    fig = new_figure()
    
  ax = fig.add_subplot(111)

  ax.set_title("Bucket Map")
  ax.set_xlabel(r'$\phi$')
  ax.set_ylabel(r'$\theta$')
  ax.set_ylim([0.0, np.pi])
      
  sc = ax.scatter(phi_x, theta_y)
     
  ax.set_xticks(np.pi * np.arange(-1, 1.5, 0.5))
  ax.set_xticklabels(["-$\pi$", "-$\pi/2$","0", "$\pi/2$", "$\pi$"])
  
  ax.set_yticks(np.pi * np.arange(0, 1.25, 0.25))
  ax.set_yticklabels(["0", "$\pi/4$", "$\pi/2$", "$3 \pi/4$", "$\pi$"])

  for i in range(rp.get('nbuckets')):
     ax.annotate(str(i + 1), (phi_x[i], theta_y[i]))

  ax.grid()

  return ax
  
def plot_unwrapped_map(rp, fig=None, buckets=[], even_stretch=False, fill_colors=None, highlight=[], highlight_color=None):
  """
  `rp` ray profile
  `fig` figure to plot this on
  `buckets` is a list of bucket IDs (1 based)
  `even_stretch` takes the cos of phi to spread the centers out more
  `fill_color` is an array of colors
  `highlight` the given bucket IDs (1-based bucket number) will be highlighted with `highlight_color`
  """

  centers = -rp.get_centers()[2:,]
  theta_center = np.arctan2(centers[1,:], centers[0,:])
  phi_center = np.arccos(centers[2,:])

  if not buckets:
    buckets = range(centers.shape[1])

  if not fig:
    fig = new_figure()
    
  if highlight and fill_colors is None:
    highlight_color = highlight_color or 'indigo'
    fill_colors = [highlight_color if i+1 in highlight else 'white' for i in buckets]

  #def get_corners(rp):
  normals = rp.get_normals()
  corners = np.zeros((3, 3, normals.shape[2]))
  corners[:,0,:] = np.cross(normals[:,0,:], normals[:,1,:], axis=0)
  corners[:,1,:] = np.cross(normals[:,1,:], normals[:,2,:], axis=0)
  corners[:,2,:] = np.cross(normals[:,2,:], normals[:,0,:], axis=0)  
  corners[:,:,:] /= np.sqrt((corners * corners).sum(0))

  theta = np.arctan2(corners[1,:,:], corners[0,:,:]).reshape((1, 3, -1))
  phi = np.arccos(corners[2,:]).reshape((1, 3, -1))
  
  corners_rad = np.vstack((theta, phi))

  for i in range(theta_center.shape[0]):
    positive = 0
    negative = 0
    ambigous = []
    
    for j in range(3):
        
      if (corners_rad[1,j,i] < 1e-7) or (corners_rad[1,j,i] >= np.pi - 1e-7):
        corners_rad[0,j,i] = theta_center[i]
      
      if (abs(theta_center[i]) >= np.pi - 1e-7):
        if theta_center[i] > 0.0 and corners_rad[0,j,i] < 0.0:
          corners_rad[0,j,i] += 2 * np.pi
  
      if (abs(corners_rad[0,j,i]) >= np.pi - 1e-7):
        ambigous.append(j)

      if corners_rad[0,j,i] > 0.0:
        positive += 1
      else:
        negative += 1

    if positive > 0 and negative > 0:
      sign = -1 if theta_center[i] < 0.0 else 1

      for a in ambigous:
        corners_rad[0,a,i] = sign * abs(corners_rad[0,a,i])
      
  if even_stretch:
    corners_rad[1,:,:] = -np.cos(corners_rad[1,:,:])

  codes = [Path.MOVETO,
           Path.LINETO,
           Path.LINETO,
           Path.CLOSEPOLY,
           ]

  ax = fig.add_subplot(111)
  
  if fill_colors is not None:
      get_patch = lambda path, ix: patches.PathPatch(path, facecolor=fill_colors[ix], lw=1)
  else:
      get_patch = lambda path, ix: patches.PathPatch(path, facecolor='white', lw=1)

  for b in buckets:
    verts = corners_rad[:,:,b].T.tolist() + [[0., 0.]]
    path = Path(verts, codes)
    patch = get_patch(path, b)
    ax.add_patch(patch)

  ax.set_xlim(-1.01 * np.pi, 1.19 * np.pi)
  ax.set_ylim(0, np.pi)
  ax.grid(True)
   
  ax.set_xticks(np.pi * np.arange(-1, 1.5, 0.5))
  ax.set_xticklabels(["-$\pi$", "-$\pi/2$","0", "$\pi/2$", "$\pi$"])

  ax.set_yticks(np.pi * np.arange(0, 1.25, 0.25))
  ax.set_yticklabels(["0", "$\pi/4$", "$\pi/2$", "$3 \pi/4$", "$\pi$"])

  for i in range(rp.get('nbuckets')):
    ax.annotate(str(i+1), (theta_center[i], phi_center[i]))
  
  return ax


def plot_energy(data_path, label, fig, stride=1, style="b-"):
  rp_set = lcse.rprofile_set(path=data_path, stride=stride)

  volumes = rp_set.get_dump().get_cell_volumes()

  t = []
  energy = []

  for rp in rp_set:
    dump = rp.dump

    timerescaled = rp.get('timerescaled')
    t.append(timerescaled)

    enuc = rp.get_table('enuc')[0,:,1:]
    enuc *= volumes

    energy.append(enuc.sum())

  ax = fig.add_subplot(1,1,1)
  ax.ticklabel_format(useOffset=False)
  ax.grid(True)
  ax.set_ylabel("energy")
  ax.set_xlabel("time [min]")

  ax.plot(t, log(energy), style, label=label)

#  if save:
#    save_fig(fig, label)
  return ax

def plot_diff_from_avg(r, rp_table, filter_fn=None, fig=None):
  """`rp_table` is a table with the same format as returned by .get_table().
  
  pass array through `filter_fn`, example filter_fn=np.log10 will make the plot
  log
  """
  
#     if check_exists(prefix, dump=dump, **kwargs):
#         return
  
  diffs = rp_table[0,:,1:] - rp_table[0,:,0].reshape((-1, 1))
  diff_size = sqrt((diffs * diffs).sum(1))

  if not fig:
    fig = new_figure()

  ax = fig.add_subplot(111)
      
  if filter_fn:
    ax.plot(r, filter_fn(diff_size))
  else:
    ax.plot(r, diff_size)
      
  ax.grid()
  return ax

from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

class RayProfileCenter(FancyArrowPatch):
  def __init__(self, row, *args, **kwargs):
    FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
    self.center = row

  def draw(self, renderer):
    xs, ys, zs = proj3d.proj_transform(self.center[0], self.center[1], self.center[2], renderer.M)
    self.set_positions((0, 0),(xs, ys))
    FancyArrowPatch.draw(self, renderer)

def plot_centers_3d(rp, buckets, fig=None, **kwrds):
  """ Make a 3d plot of the bucket centers
  
  `buckets` list of buckets to plot 
  `fig` a figure object
  """
  
  from mpl_toolkits.mplot3d import Axes3D
  from itertools import product, combinations

  if not fig:
    fig = new_figure(figsize=(10, 10))

  ax = fig.gca(projection='3d')
#  ax.set_aspect("equal")
  size = 2

  # Draw cube
  r = [-size, size]
  for s, e in combinations(np.array(list(product(r,r,r))), 2):
    if np.sum(np.abs(s-e)) == r[1]-r[0]:
      ax.view_init(elev=90., azim=-90.0)
      ax.plot3D(*zip(s,e), color="b")

  ax.set_xlabel('X axis')
  ax.set_ylabel('Y axis')
  ax.set_zlabel('Z axis')

  # Draw axis
#  a = RayProfileCenter((1,0,0), mutation_scale=20, lw=1, arrowstyle="-|>", color="k")
#  a = RayProfileCenter((0,1,0), mutation_scale=20, lw=1, arrowstyle="-|>", color="k")
#  ax.add_artist(a)

  ax.add_artist(ax.text(0.0, -2.0, -2.0, '10', text='X'))
  ax.add_artist(ax.text(-2.0, 0.0, -2.0, '10', text='Y'))
  ax.add_artist(ax.text(-2.0, -2.0, 0.0, '10', text='Z'))

  # Draw a point
  ax.scatter([0],[0],[0],color="g",s=100)
    
  rp_centers = rp.get_centers()

  for i in range(1, rp_centers.shape[1] + 1):
    if i not in buckets:
      continue
    
    center = size * rp_centers[2:,i-1]

    a = RayProfileCenter(center, mutation_scale=20, lw=1, arrowstyle="-|>", color="k")
    ax.add_artist(a)
    t = ax.text(1.15 * center[0], 1.15 * center[1], 1.15 * center[2], '10', text='%i' % i , color='k')
        
    ax.add_artist(t)

  ax.grid()

  return ax

def plot_centers_on_image(rp, buckets=None, img=None, fig=None, index_x=0, index_y=1, scale=1.15, alpha=0.6, prefix=None):
    """
    
    `buckets` a list of buckets to plot

    `img` can be an image which will be used in `imshow(img)` or a string in which
    case the image will be loaded, or none.
    
    `index_x` and `index_y` are the coordinate index to draw as x and as y. By default
    these are index_x = 0, index_y = 1 which gives the standard coordinates. Setting this to 0, 2 will
    provide a top view
    
    `scale` is the size of the arrows.
    
    `alpha` background image alpha
    
    `fig` figure instance
    
    """
        
    index_z = tuple(set((0, 1, 2)).difference((index_x, index_y)))[0]
    axis_labels = ['X', 'Y', 'Z']
    
    if not fig:
      fig = new_figure()
    
    ax = fig.add_subplot(111)
    
    if img:
        # Draw the image
        if isinstance(img, str):
          img = Image.open(img)

        img = image_util.square_crop(img)
        ax.imshow(img, zorder=0, extent=[-1.0, 1.0, -1.0, 1.0], alpha=alpha)

    # Draw the buckets
    if buckets:
      bucket_ids = [i - 1 for i in buckets]
      centers = scale * rp.get_centers()[2:,bucket_ids]
    else:
      centers = scale * rp.get_centers()[2:,]
      buckets = range(centers.shape[1])
        
    x = np.zeros(centers.shape[1])

    q = ax.quiver(x, x, centers[index_x,:], centers[index_y,:], angles='xy', scale_units='xy', scale=1.0)

#     center_colors = np.zeros(centers.shape[1])
#     center_colors[centers[index_z,:] > 0.0] = 1.0
#     q = ax.quiver(x, x, centers[index_x,:], centers[index_y,:], center_colors, angles='xy', scale_units='xy', scale=1.0)
    
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.2, 1.2)
    
    ax.set_xlabel("%s axis" % axis_labels[index_x])
    ax.set_ylabel("%s axis" % axis_labels[index_y])
    
    ax.grid()
    
    colors = ['g', 'b']
    
    for i, bucket in enumerate(buckets):
        ax.quiverkey(q, centers[index_x,i], 1.2 * centers[index_y,i], 0, '%i' % bucket, 
                     coordinates='data', color=colors[0 if centers[index_z, i] > 0.0 else 1])
  
    if not prefix:
      prefix = 'centers' 
    
    save_fig(fig, prefix, dump=rp.dump)
        
    return ax

# 
# Untested  
# 

def plot_spike(rp_set, fig, **kwargs):

  prefix = 'fuel'

  rp_main = rp_set.ray_profiles[0]

  limits = kwargs.get('limits', (rp_main.get('radinner'), rp_main.get('radouter')))

  y = rp_main.get('y')
  half_dx = 0.5 * (y[1] - y[0])

  spikes = kwargs.get('spikes', [])
  dumps = kwargs.get('dumps', [])
  times = kwargs.get('times', [])

  for i, rp in enumerate(rp_set):

    dump = rp.dump
    time = rp.get('time')

    print dump,

    if dump in dumps or dump < 1:
      continue

    y = rp.get('y')
    y_limit = (y < limits[1]) & (y > limits[0])
    y = y[y_limit]

    fv = rp.get('fv')[0, y_limit]
    fv1 = 1.0 - fv

    rhobub = rp.get('rhobubble')[0, y_limit]
    rhospike = rp.get('rhospike')[0, y_limit]

    vols = (4. * np.pi / 3.) * ((y + half_dx)**3 - (y - half_dx)**3)
    bub_mass = vols * rhobub * fv1
    spike_mass = vols * rhospike * fv

    spikes.append(spike_mass.sum())
    dumps.append(dump)
    times.append(rp.get('time'))

  import matplotlib
  y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)

  ax = fig.add_subplot(111)
  ax.set_title('H-quantity')
  ax.plot(dumps, spikes, 'k')

  ax.set_xlabel("Time")
  ax.yaxis.set_major_formatter(y_formatter)
  ax.grid(True)

  save_fig(fig, prefix, **kwargs)

  return dumps, times, spikes


def get_interface_location(rp, levels):

  nbuckets = rp.get('nbuckets')
  level_ct = len(levels)

  j_hi = rp.get_table('j_hi')
  y_hi = rp.get_table('y_hi')
  fv_hi = rp.get_table('fv_hi')[0,:,:]

  data = np.zeros((level_ct, nbuckets+1))

  #TODO: Don't loop
  for bucket in range(nbuckets+1):

    one_thing = fv_hi[:, bucket]

    first = np.argmax(one_thing > 0.0)
    last = np.argmin(one_thing < 1.0)

    j_restricted = j_hi[first-1:last-1]
    y_restricted = y_hi[first-1:last-1]

    fv_restricted = fv_hi[first-1:last-1, bucket]

    if fv_restricted.size == 0:
      continue

    for l, val in enumerate(levels):
      data[l, bucket] = np.interp(val, fv_restricted, y_restricted)

  return data

def get_interface_statistics(dump_data, dumps=None, results=None):
  log.info("get_interface_statistics")

  data_len = len(dump_data)

  if data_len == 0:
    return

  dumps = np.zeros(data_len, dtype=np.int32) if not dumps else dumps
  results = np.zeros((2, dump_data[0][1].shape[0], data_len)) if not results else results

  for i, d in enumerate(dump_data):

    dumps[i] = d[0]
    r = d[1][:,1:]

    print d[0],

    for l in range(r.shape[0]):
      results[0, l, i] = r[l].mean()
      results[1, l, i] = np.std(r[l])

  return dumps, results

def plot_interface(dumps, time_data, results, levels, **kwargs):

  styles_len = len(styles)
  colors_len = len(colors)

  fig = kwargs.get('fig', new_figure())
  quiet = kwargs.get('quiet', False)

  x_limits = kwargs.get('xlimits')
  y_limits = kwargs.get('ylimits')
  sd_only = kwargs.get('sd_only', False)

  ax = fig.add_subplot(1,1,1)
  ax.ticklabel_format(useOffset=False)
  ax.grid(True)
  ax.set_xlabel("dump #")
  ax.set_ylabel("r [1000 km]")

  if not sd_only:
    ax.set_title("Location of FV interface", y=1.08)
    for i, v in enumerate(levels):
      avg = results[0,i,:]
      sd = results[1,i,:]
      color = colors[ i % colors_len]

      ax.errorbar(dumps, avg, yerr=sd, label='fv=%f' % v,
                  fmt='k.-', ecolor=color)
  else:
    ax.set_title("Standard-Deviation of FV interface", y=1.08)
    for i, v in enumerate(levels):
      sd = results[1,i,:]
      style = styles[ i % styles_len]
      ax.plot(dumps, sd, style, label='fv=%f' % v)

  if x_limits:
    print "X LIMITS", x_limits
    ax.set_xlim(x_limits)
    #ax2.set_xlim(x_limits)

  if y_limits:
    ax.set_ylim(y_limits)
    #ax2.set_ylim(y_limits)

  ax.legend(loc=2)
  ax2 = ax.twiny()
  ax2.set_xlabel("time [min]")
  ax2.set_xticks(ax.get_xticks())
  ax2.set_xticklabels(time_data)
  ax2.set_xbound(ax.get_xbound())
  ax2.set_ybound(ax.get_ybound())


  save_fig(fig, 'interface', **kwargs)

  if quiet:
    matplotlib.pyplot.close(fig)

def plot_interface_analysis(rps, **kwargs):

  dumps = kwargs.get('dumps')
  time_data = kwargs.get('timing', [])
  prefix = kwargs.get('prefix')
  xlimits = kwargs.get('xlimits')
  levels = kwargs.get("levels", (0.5, 0.1, 0.01, 0.001, 1e-5))

  dump_data = []

  for rp in rps:
    dump = rp.dump

    if dumps and dump not in dumps:
      continue

    print dump,

    d = get_interface_location(rp, levels)
    dump_data.append((dump, d))
    time_data.append('%0.f' % rp.get('timerescaled'))

  dumps, results = get_interface_statistics(dump_data)

  plot_interface(dumps, time_data, results, levels, filename='%s.png' % prefix,
                 xlimits=xlimits)

  plot_interface(dumps, time_data, results, levels, filename='%s_sd_only.png' % prefix,
                 xlimits=xlimits, sd_only=True)

  # Return dump_data so we can cache it
  return dump_data

