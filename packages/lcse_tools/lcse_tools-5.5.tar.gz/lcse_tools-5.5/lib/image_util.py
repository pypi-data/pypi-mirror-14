
try:
  import numpy as np
except ImportError:
  print "Numpy not installed"

try:
  from PIL import Image, ImageDraw, ImageFont
except ImportError:
  print "Numpy not installed"

def square_crop(im, target_size=None):
  """ Crop image to `target_size`. If that's None the image is squared 
  to the smallest size
  """
  w = im.size[0]
  h = im.size[1]

  target_size = target_size if target_size else min(w, h)

  dx = (w - target_size) / 2
  dy = (h - target_size) / 2

  return im.crop((dx, dy, dx + target_size, dy + target_size))

def draw_time(im, font, time=None, dump=None, padding_x=0.25, padding_y=0.07):

  padding = padding_x
  w, h = im.size

  y_loc = h - padding_y * h

  draw = ImageDraw.Draw(im)

  if dump:
    line = "%04i" % dump
    text_w, text_h = draw.textsize(line, font=font)

    x_loc = padding * w / 2.0
    draw.text((x_loc, y_loc), line, (255,255,255), font=font)

  if time:
    line = "%0.f min" % time
    text_w, text_h = draw.textsize(line, font=font)

    x_loc = w - text_w - padding * w / 2.0
    draw.text((x_loc, y_loc), line, (255,255,255), font=font)

def color_to_alpha(im_in, color=(0, 0, 0, 255), threshold=50):

    im_out = im_in.convert("RGBA")
    pixdata = im_out.load()

    for y in xrange(im_in.size[1]):
        for x in xrange(im_in.size[0]):
            pd = pixdata[x, y]
            
            if pixdata[x, y] == color:
                pixdata[x, y] = (0, 0, 0, 0)
            else:               
                avg = int((pd[0] + pd[2] + pd[1]) / 3.0)
                
                if avg < threshold:
                    pixdata[x, y] = (pd[0], pd[1], pd[2], avg)
                           
                
    return im_out   

def alpha_composite(src, dst):
    '''
    Return the alpha composite of src and dst.

    Parameters:
    src -- PIL RGBA Image object
    dst -- PIL RGBA Image object

    The algorithm comes from http://en.wikipedia.org/wiki/Alpha_compositing
    '''
    
    # http://stackoverflow.com/a/3375291/190597
    # http://stackoverflow.com/a/9166671/190597
    
    src = np.asarray(src)
    dst = np.asarray(dst)
    out = np.empty(src.shape, dtype = 'float')
    alpha = np.index_exp[:, :, 3:]
    rgb = np.index_exp[:, :, :3]
    src_a = src[alpha]/255.0
    dst_a = dst[alpha]/255.0
    out[alpha] = src_a+dst_a*(1-src_a)
    old_setting = np.seterr(invalid = 'ignore')
    out[rgb] = (src[rgb]*src_a + dst[rgb]*dst_a*(1-src_a))/out[alpha]
    np.seterr(**old_setting)    
    out[alpha] *= 255
    np.clip(out,0,255)
    # astype('uint8') maps np.nan (and np.inf) to 0
    out = out.astype('uint8')
    out = Image.fromarray(out, 'RGBA')
    return out


