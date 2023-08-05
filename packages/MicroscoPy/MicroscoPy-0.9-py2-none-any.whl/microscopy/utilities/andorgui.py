"""Live displays for the Andor camera.

This used to be part of the andor2 module, but was moved to utilities.
"""

import numpy as np

from drivers.andor import AndorError
from microscopy import display
from . import camdisp


def get_new_data(cam, display):
  """Return the latest available data from the Andor camera, or None if there are no new data.
  
  Use within the :func:`get_data` methods of CameraDisplay and LivePlot.
  
  :param cam: andor2.Andor object
  :param display: one of the display defined in this module 
  :param int type: get data as 16 or 32 bits uint
  """
  # Video and Single/Kinetic modes have to be handled differently.
  if cam.Acquire._name == 'Video':
    try:
      if cam.Acquire.images_in_buffer['last'] != display.last_image_read:
        display.last_image_read = cam.Acquire.images_in_buffer['last']
        return cam.Acquire.Newest(type=32)  # need 32 bits for the rescaling
      else:
        return None
    except AndorError as error:               # Arise when changing exposure on the fly, 
      if error.string == 'DRV_NO_NEW_DATA':   # can be safely ignored
        return None
      else:
        raise error
  else:  # not Video. Assume the acquisition as been triggered via a Sensor.snap() method
    try:
      if cam.Acquire.snapshot_count != display.last_image_read:
        display.last_image_read = cam.Acquire.snapshot_count
        return cam.Acquire.last_snap[0] # 
      else:
        return None
    except AttributeError:
        return None


class AndorDisplay(camdisp.CameraDisplay):
  """Specialises CameraDisplay for the Andor camera."""
  
  def __init__(self, cam, master=None):
    """
    :param cam: an Andor2.Andor instance
    :param master: Tkinter parent widget
    """
    self.cam = cam
    self.dyn = 2**cam.Detector.bit_depth - 1 # camera dynamic range (12 bits)
    self._rescale = (0, self.dyn)
    shape = cam.ReadMode.current.shape
    self.last_image_read = 0
    super(AndorDisplay, self).__init__(shape[0], shape[1], tk_window=master)

  def get_image_data(self):
    self.imdata = get_new_data(self.cam, self)
    if self.imdata is not None:
      rescaled_data = ((self.imdata - self._rescale[0])*self.dyn)/(self._rescale[1]-self._rescale[0])
      return np.uint8(rescaled_data/2**(self.cam.Detector.bit_depth-8))
    else:
      return None

  def title_string(self):
    s = 'Andor track | Exp: {exp: 3.2f} ms | max: {m: >5d} | Image #{imgno: >5d}'
    return s.format(mode=self.cam.ReadMode.current._name, 
                    exp=self.cam.exposure, m=int(self.imdata.max()),
                    imgno=self.last_image_read)


class TrackPlot(display.LivePlot):
  """Specialises LivePlot to display Single-Track, Multi-Track and FVB data.
  
  All tracks will be displayed in the same plot.
  """
  def __init__(self, cam, master=None, transpose=False, **kwargs):
    """
    :param cam: andor2.Andor driver
    :param master: Tkinter parent object
    :param bool transpose: whether to transpose the data
    
    All other kwargs are passed to :class:`microscopy.display.LivePlot`
    """
    self._cam = cam
    if self._cam.ReadMode.current.ndims > 1:
      self.ntracks = self._cam.ReadMode.current.shape[0 if not transpose else 1]
      self.npoints = self._cam.ReadMode.current.shape[1 if not transpose else 0]
    else:
      self.ntracks = 1
      self.npoints = self._cam.ReadMode.current.shape[0]
    super(TrackPlot, self).__init__(self.ntracks, self.npoints, master=master, **kwargs)
    self.ax.set_ylim(1, 2**self._cam.Detector.bit_depth) # do not set lower ylim to 0 to use log scale
    self.ax.set_xlim(0, self.npoints + 1)
    self.ax.set_xlabel("pixels")
    self.offset = 0
    #self.transform = lambda x:x
    self.transpose = transpose
    
  def get_data(self):
    """Return the latest available data for plotting."""
    data = get_new_data(self._cam, self)
    if data is None:
      return data
    if self.ntracks == 1:
      #return [self.transform(data) - self.offset]
      return [data - self.offset] 
    else:
      if self.transpose:
        data = data.T
      #return self.transform(data) - self.offset
      return data - self.offset

  def title(self):
    """A title string for the plot window"""
    s = 'Andor track | Exp: {exp: 3.2f} ms | max: {m: >5d} | Image #{imgno: >5d}'
    return s.format(mode=self._cam.ReadMode.current._name, 
                    exp=self._cam.exposure, m=int(self.data[0].max()),
                    imgno=self.last_image_read)


class ImageProfile(display.LivePlot):
  """Provides a plot to display profiles from the image display.
  
  NOT IMPLEMENTED
  """ 
  def __init__(self):
    pass


class Histogram(display.LivePlot):
  #UNTESTED
  def __init__(self, display, pixels_per_bin, master=None):
    super(Histogram, self).__init__(1, display.dyn/pixels_per_bin, master=master)
    self._pixels_per_bin = pixels_per_bin
    self._display = display
    
  def get_data(self):
    self.hi = np.histogram(self._display.imdata, 
      bins=self._display.dyn/self.pixels_per_bin, 
      range=(0, self._display.dyn))[0]
    return self.hi

  def __repr__(self):
    return "Andor image histogram. Pixels per bins: %d." % (self._pixels_per_bin)

  @property
  def pixels_per_bin(self):
    return self._pixels_per_bin
  @pixels_per_bin.setter
  def pixels_per_bin(self, value):
    self.init_fig(1, self._display.dyn/value)
    self._pixels_per_bin = value


class XYProfiles(display.LivePlot):
  """Plots X and Y profiles of the image."""
  def __init__(self, display):
    self._cam = display.cam
    self._display = display
    self._xlim = (1, self._cam.ReadMode.current.shape[0])
    self._ylim = (1, self._cam.ReadMode.current.shape[1])
    self.offset = (0,0)
    super(XYProfiles, self).__init__(self._cam.ReadMode.current.shape[0], self._cam.ReadMode.current.shape[1], data_func=None)
  
  def init_fig(self, dummx, dummy):  # need special init_fig as both axis may have different dimensions
    # Initialise figure
    self.xdim = self.xlim[1] - self.xlim[0] + 1
    self.ydim = self.ylim[1] - self.ylim[0] + 1
    self.ax.set_ylim(0, 2**self._cam.Detector.bit_depth)
    self.ax.lines = []
    for dim in [self.xdim, self.ydim]:
      self.ax.plot(np.arange(1, dim+1), np.zeros(shape=dim))
  
  @property
  def xlim(self):
    return self._xlim
  @xlim.setter
  def xlim(self, startstop):
    self.stop()
    self._xlim = startstop
    self.init_fig(None, None)
    self.start()
    
  @property
  def ylim(self):
    return self._ylim
  @ylim.setter
  def ylim(self, startstop):
    self.stop()
    self._ylim = startstop
    self.init_fig(None, None)
    self.start()
  
  def get_data(self):
    data = self._display.imdata[self.xlim[0]-1:self.xlim[1], self.ylim[0]-1:self.ylim[1]]
    return [data.sum(1)/len(data[0])-self.offset[0], data.sum(0)/len(data[:,0]) - self.offset[1]]
