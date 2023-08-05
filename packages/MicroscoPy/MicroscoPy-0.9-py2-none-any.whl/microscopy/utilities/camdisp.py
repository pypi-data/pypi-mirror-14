__id__ = "$Id$"
__revision__ = filter(str.isdigit, "$Revision$")

# Derived from code from Alfredo Dubra Jan 2005

# Hacked by GL, Nov 2014, to add live display with TKinter's after() method.


import threading
from PIL import Image, ImageTk
import Tkinter

class CameraDisplay(object):
  """Display images from camera
  
  .. Warning::  
     (17/4/2012) The following are expected to avoid the
     tk-threadsafe issues, but have not yet got proper contention locks:
     set_zoom, set_top_corner, set_left_corner, get_zoom,
     get_top_corner, get_left_corner
  
  The constructor takes 2 integers, the width and height of the
  image, and create a window and canvas (were the image will be
  drawn) of the corresponding size.
  
  The :func:`title` function takes a string to be used as title of the
  window displaying the image.
  
  The :func:`show` function takes a string with the image. If the image
  is to be passed from C or C++ a function along the lines of::
  
      PyObject * RetrieveFrameToPython ()
      {
      char *buf = (char *)PointerTo8bitImage();
      return Py_BuildValue("s",buf,height*width);
      }
 
  is required to convert the data pointed to by the unsigned char
  pointer to a Python string.

  The :func:`show_zoomed` function takes a string with the image (see :func:`show`),
  a zoom factor (integer or float number) and a 2-uple with the
  coordinates of the center of the area to be zoomed. This 2-uple
  MUST be float (i.e. multiply each number by 1.0 if needed) and
  between the values 0 and 1. The (0,0) corresponds to the upper left
  corner of the image and (1,1) to the bottom right corner. Also
  notice that the zooming in done by copying the value of the nearest
  pixel. Thus, there is NO INTERPOLATION (ON PURPOSE).
  """

  def __init__(self, width, height, zoom=1,
               tk_window=None, imagemode="L"):
    """
    :param width: width of display image (in pixels)
    :param height: height of display image (in pixels)
    :param zoom: size of gui display w.r.t. image (default 1)
    :param tk_window: tk window object to use (default: None)
    :param imagemode: "L" for luminance (gray), "RGB" for colour (default "L")
    :param bit_depth: camera bit depth
    """
    self.width = abs(int(width))
    self.height = abs(int(height))

    #self.zoom = abs(int(zoom))
    self.zoom = abs(float(zoom))
    if self.zoom == 0:
      self.zoom = 1
      
    #self.depth = bit_depth
    #self.bitdepthscaling = 2.0**(8-bit_depth) # image data to be scaled by that munber as image depth must be 8 bits
    self.scale_amplitude = 1.0
    
    self.top = 0.0
    self.left = 0.0
    self.scale = 1.0

    self.image = Image.new(imagemode, (width, height))

    if tk_window is None:
      self._window = Tkinter.Tk()
    else:
      self._window = Tkinter.Toplevel(tk_window)

    # lock window size
    self._window.maxsize(width=int(width*zoom),
                         height=int(height*zoom))
    self._window.minsize(width=int(width*zoom),
                         height=int(height*zoom))

    # Tk canvas (where the image is painted)
    self._canvas = Tkinter.Canvas(self._window,
                                  width=int(width*zoom),
                                  height=int(height*zoom))
    self._canvas.pack()
    self.is_canvas_image_created = 0

    #double buffer images 
    self.imbuffid = 0
    self.aux_photoimage = [0, 0]

    self.imagelock = threading.Lock()
    self.configlock = threading.Lock()
    
    # Live display stuff
    self.live_delay = 100 # live refresh rate, in ms.
    self._autorefresh = False
    self.wheel = ('-',"\\",'|','/')
    self.count = 0
    
    
  def set_image(self, string_data):
    """Set the image data.
    
    :param string_data: a string containing the raw image 
    """
    with self.imagelock:
      if self.image.mode != 'RGB':
        self.image.fromstring(string_data, "raw", self.image.mode)
      else:
        #the same data in R,G and B channels to get greyscale:
        self.image.fromstring(string_data, "raw", "R")
        self.image.fromstring(string_data, "raw", "G")
        self.image.fromstring(string_data, "raw", "B")
        
  def set_image_frombuffer(self, buf):
    """Set the image data, using buffer rather than string data
    
    :param buf: image buffer
    
    .. TODO:: not working!
    """
    with self.imagelock:
      self.image.frombuffer(self.image.mode, (self.width, self.height), buf, "raw", self.image.mode, 0, 1)
  
  def title(self, string_title):
    """Set the window title."""
    self._window.title(string_title)

  # show image from a string of data
  # TODO: overload for reading uchar, ushort float, etc
  def show(self):
    """
    Update gui display - redraw the image canvas and call the gui update.
    """
    # CPaterson(3/3/08)
    # Note: added double buffering of the image that is displayed:
    #(create_image and itemconfigure seem to store references to the 
    #image data supplied as parameters)
    # 
    # image scaling
    with self.configlock: 
      zoomed_section = (self.left * self.width,
                        self.top * self.height,
                        (self.left + 1.0 / self.scale) * self.width,
                        (self.top + 1.0 / self.scale) * self.height)
  
      with self.imagelock:
        sectioned_image = self.image.transform(
          (int(self.width / self.scale), int(self.height / self.scale)),
          Image.EXTENT, zoomed_section)
  
      zoomed_image = sectioned_image.transform(
        (self.width, self.height), Image.AFFINE,
        (1.0 / self.scale, 0, 0, 0, 1.0 / self.scale, 0, 0))
      # scaling to fit into the display
      scaled_image = zoomed_image.transform(
        (int(self.width * self.zoom),
         int(self.height * self.zoom)),
        Image.AFFINE,
        (1/self.zoom, 0, 0, 0,
         1/self.zoom, 0, 0))
      
      self.imbuffid = (self.imbuffid + 1) % 2
      
      #rescaled_image = scaled_image.point(lambda x:int(x*self.bitdepthscaling*self.scale_amplitude))
      self.aux_photoimage[self.imbuffid] = ImageTk.PhotoImage(scaled_image)
      
      if self.is_canvas_image_created == 0:
        # this is what takes the most time (SLOWEST)
        self._canvas.create_image(
          int(self.width / 2 * self.zoom),
          int(self.height / 2 * self.zoom),
          image=self.aux_photoimage[self.imbuffid], tags='img')
        self.is_canvas_image_created = 1
      else:
        self._canvas.itemconfigure(
          'img', image=self.aux_photoimage[self.imbuffid])
    
    #self.rescaled_image = rescaled_image
    self.zoomed_image = zoomed_image
    self.sectioned_image = sectioned_image
    self.scaled_image = scaled_image
    self._canvas.update_idletasks()

  def __del__(self):
    try:
      self._canvas.destroy()
    except:
      pass
    try:
      self._window.destroy()
    except:
      pass

  def set_region(self, top, left, scale):
    """
    Sets the region of the image to be displayed.
    
    :param top:
    :param left: coordinates of top,left corner (as a fraction of the image) 
    :param scale: magnification zoom factor (min 1.0)
    
    The specified region must be contained within the whole image.
    If not, the region is not set and a warning is issued.
    """
    valid = ((scale >= 1.0)  and
             (top >= 0.0  and top + 1.0/scale <= 1.0) and
             (left >= 0.0  and left + 1.0/scale <= 1.0))
    if not valid:
      print "Warning: set_region() -- specified region invalid."
    with self.configlock: 
      self.scale = 1.0 * scale
      self.top = 1.0 * top
      self.left = 1.0 * left
      
  # Live display stuff
  # user to override the following function:
  # - get_image_data() : pass image data to the LiveDisplay class
  # - title_string() : returns a custom title string
  
  def get_image_data(self):
    """Return 8-bits 2D image data, or None if there are no new data.
    
    This function must be overridden by child classes in order to use the autorefresh functionality.
    """
    raise NotImplementedError
  
  def title_string(self):
    """Return a string to use as window title. Can be overrident by child classes."""
    return ""
  
  def rescale(self, min=None, max=None):
    """Tuple: (min, max) that rescales the pixel amplitudes to lie between min and max."""
    self._rescale = (0 if min is None else min, self.dyn if max is None else max)
  
  def start(self):  
    """ Start live display"""
    data = self.get_image_data()
    if data is not None:
      self.set_image(data)
      self.show()
      self.title(self.title_string())
      self.count = self.count + 1
    self.callback_id = self._window.after(self.live_delay, self.start)
    self._autorefresh = True
    
  def stop(self):
    """ Stop live display"""
    self._window.after_cancel(self.callback_id)
    self._autorefresh = False   

  @property
  def autorefresh(self):
    return self._autorefresh
  @autorefresh.setter
  def autorefresh(self, b):
    if b and not self._autorefresh:
      self.start()
    elif not b and self._autorefresh:
      self.stop()
