"""
:class:`hal.Sensor` device adapters shipped with MicroscoPy:

              - :mod:`andor2` EMCCD cameras
              - PCO :mod:`pxlfly` CCD cameras
              - MCCDAQ USB2600 analog input
"""

import numpy as np
import time
import sys
from math import copysign
import matplotlib.pyplot as plt

#from .. import hal
from .. import hal

class Dummy_Camera(hal.Sensor):
  """Dummy scan for debug purpose."""
  def __init__(self):
    self.snap_count = 0
    self.current_position = 0
    
  def snap(self, **kwargs):
    self.paused = False # 
    self.snap_count += 1
    self.status = True
    #print "snap()+ # "+str(self.snap_count)
    return self.snap_count
    
  def update_display(self):
    pass


# Andor EMCCD adapters
# Available only if the andor driver can be imported

try:
  from andor import AndorError

  class Andor(hal.Sensor):
    """Device adapter for the Andor EMCCD :class:`andor2.Andor`.
    
    The camera is operated in Kinetic mode.
    
    The exposure property allows changing the exposure on-the-fly (i.e.,
    without pausing the scan first).
    """
    def __init__(self, cam, n=1, display=None, thermistor=None):
      """   
      :param cam: an AndorUI object
      :type cam: :py:class:`andor2.Andor`
      :param n: number of images to take (default 1)
      :type n: int
      :param display: the active camera live display
      :type display: :class:`microscopy.display.LiveDisplay`
      :param thermistor: a Thermistor object to keep track of ambient temperature.
      """
      self.cam = cam
      self.n = n
      self.display = display
      self.thermistor = thermistor
      self._sleep = []
      self.snap_info_description = "(exposure, )"
      self._queued_exposure = None

    @property
    def exposure(self):
      """Query or set the exposure time (in ms).
      
      If the camera is acquiring, the exposure change will be applied once the current snap is finished.
      """
      return self.cam.exposure
    @exposure.setter
    def exposure(self, exp_ms):
      try:
        self.cam.exposure = exp_ms
      except AndorError as error:
        if error.string is "DRV_ACQUIRING":
          self._queued_exposure = exp_ms
        else:
          raise error

    def snap(self, new=True):
      """Return the latest data, either from a new acquisition sequence (new=True, default),
      or from the last one (new=False).
      
      The data is also available """
      if new:
        self.paused = False
        self.cam.Acquire.start()
        #self.cam.Acquire.wait()  # this blocks the main thread also! Use sleep + polling instead
        time.sleep(0.9*self.cam.exposure / 1000.0) # sleep for one exposure time (which is in ms)
        self._sleep.append(0)
        while self.cam.Acquire.running:
          self._sleep[-1] += 1
          time.sleep(0.01)

        self.status = True
        #get data and insert a reference here and in andorui as well.
        self.last_snap = self.cam.Acquire.GetAcquiredData()
        self.cam.Acquire.last_snap = self.last_snap
        
        # Apply exposure change
        if self._queued_exposure is not None:
          self.cam.exposure = self._queued_exposure
          self._queued_exposure = None
        
      return self.last_snap

    def snap_info(self):
      return (self.cam.exposure, )

    def update_display(self):
      if self.display is not None:
        self.display.update()
      else:
        pass

    def initialise_acquisition(self):
      self.saved_mode = self.cam.Acquire
      self.cam.Acquire.stop()
      self.cam.Acquire.Kinetic(self.n, 0)

    def terminate_acquisition(self):
      self.cam.Acquire = self.saved_mode
      self.cam.Acquire()

    def save_metadata(self, h5file, dataset_name):
      """Add acquisition atributes to an existing HDF5 dataset.
      
      :param h5file: a :class:`h5py.File` (must be open)
      :param string dataset_name: name of the dataset (must have already  been created).
      """
      h5file[dataset_name].attrs['mode'] = self.cam.Acquire._name
      h5file[dataset_name].attrs['exposure'] = self.cam.exposure
      h5file[dataset_name].attrs['em_gain'] = self.cam.EM._read_gain_from_camera()
      if self.thermistor is not None:
        h5file[dataset_name].attrs['temperature'] = self.thermistor.temperature()
      h5file.flush()
      # Save dark image if available
      try:
        h5file.create_dataset(dataset_name+"/dark", data=np.array(self.dark_image))
      except AttributeError:
        pass
      h5file.flush()

    def dark(self):
      """Return a dark image (acquired with shutter closed)."""
      self.cam.Shutter.Close()
      self.dark_image = self.snap()
      self.cam.Shutter.Open()
      return self.dark_image

    def intensity(self, center, width, new=True):
      # Not used, currently the interferometer relies on roi_1D
      """Return the sum of pixel values in a ROI centered at *center*, of with *width*.
      
      *center* and *width* must be tuples. Works with 1D and 2D data.
      If new=True, snap a new image, otherwise use the last acquired image."""
      imdata = self.snap(new=new)
      self.imdata = imdata
      imdata = imdata.sum(0) # add all images in Kinematic sequence.
      if imdata.ndim == 2:
        subarea = imdata[center[0]-width[0]:center[0]+width[0],
                         center[1]-width[1]:center[1]+width[1]]
      else:
        subarea = imdata[center[0]-width[0]:center[0]+width[0]]
      return subarea.sum()

    def roi_1D(self, center, width, new=True):
      """Return a region of interest from a 1D spectrum.
      
      :param int center: center of the ROI (in pixel).
      :param int width: half-width of the ROI (in pixels).
      :param bool new: if True (default), acquire a new spectrum.
                   Otherwise use the last acquired spectrum.
      :return: 1D array
      
      .. todo::      
         This looks a bit trivial.
         Should we move all of this code to :class:`interferometer.RayleighIntensity`? 
      """
      imdata = self.snap(new=new)
      imdata = imdata.sum(0) # add all images in Kinematic sequence.
      assert imdata.ndim == 1, "intensity_with_max() works only on 1D data"
      return imdata[center-width:center+width]


  class AndorExposures(Andor):
    """An extension of the Andor camera class where for each scan position several
    images are taken with different exposures."""
    def __init__(self, cam, exposures, n=1, display=None, thermistor=None):
      super(AndorExposures, self).__init__(cam, n=n, display=display, thermistor=thermistor)
      self.exposures = exposures

    def snap(self, **kwargs):
      self.paused = False
      data = []
      for exp in self.exposures:
        self.cam.exposure = exp
        self.cam.Acquire.start()
        self.cam.Acquire.wait()
        data.append(self.cam.Acquire.GetAcquiredData())
      self.status = True
      return np.array(data)

except ImportError:
  print "Could not import 'andor2' module, 'Andor' adapter not available."


class VoltIn(hal.Sensor):
  """Analog input adapter."""
  def __init__(self, ai, scaling=-1, wait=0):
    """
    :param ai: analog input channel (any callable object that returns a float when called)
    :param float scaling: a multiplicative factor applied to the measured voltage
    :type float wait: delay (settling time) before taking measurement
    """
    self.ai = ai
    self.wait = wait
    self.scaling = scaling
    
  def snap(self, **kwargs):
    self.paused = False
    self.status = True
    time.sleep(self.wait)
    return self.scaling * self.ai()
  
  def roi_1D(self, **kwargs):
    return self.snap()

# Adapter for PCO Pixelfly CCD cameras.
# Will only be available if the pxlfly driver can be imported

try:
	from pxlfly import CameraBuffer

	class Pixelfly(hal.Sensor):
	  """Sensor adapter for PCO Pixelfly CCD cameras"""
	  def __init__(self, camera):
		""":param cam: a :class:`pxlfly.PyPixelfly` instance"""
		self.cam = camera
		status = True
		
	  def snap(self, new=True):
		with CameraBuffer(self.cam):
		  return self.cam.getframe().copy()
		  
except ImportError: 
	print "Cannot import module pxlfly, Pixelfly adapter not available"
