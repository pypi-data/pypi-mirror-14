# -*- coding: utf-8 -*-
"""Hardware abstraction layer (HAL) for MicroscoPy.

It defines abstract classes Actuator and Sensor for the scanning stages and acquisition devices

-------------------------------
"""

import numpy as np
from time import sleep
import time
import sys
import matplotlib.pyplot as plt
from math import copysign

from .utilities import plotting, terminal
#from utilities.terminal import printr


###
### "Actuator" objects provide an interface between motion devices and the microscope
### 

class Actuator(object):
  """Abstract representation of a uniaxial actuator (eg translation stage).
  
  The :mod:`scan` module requires at mimimum that sub-classes override
  the functions :func:`move_to` and :func:`position`. 
  
  .. todo::
      move support for different units here (currently implemented in :py:class:`ZaberAxis`)
  
  """
  unit = "" # unit string to display after position
  disable_key_repeat = True # only devices that implement move() need this
                            # disable by default as it is the safest option
  dir = 1
  hours_interval = 4
  history = []
  
  def move_to(self, p, wait=True):
    """Instructs the scanning stage to move to absolute position p.
    
    This function MUST be overriden by child classes.
    
    :param p: the target position, in the actuator's own unit
    :type p: float
    :param wait: if True (default), the function returns after motion is completed.
                 Otherwise, return immediately.
    :type wait: bool
    """
    raise NotImplementedError
  
  def move_by(self, p, wait=True):
    """Instructs the scanning stage to move by a relative amount.
    
    Unless overridden, ``move_by`` relies on :py:func:`move_to`.
    
    :param p: the target position, in the actuator's own unit
    :type p: float
    :param wait: if True (default), the function returns after motion is completed.
                 Otherwise, return immediately.
    :type wait: bool
    """
    self.move_to(self.position() + p, wait=wait)
  
  def move(self, dir):
    """Move continuously.
    
    :param dir: direction of motion (positive or negative)
    :type dir: float 
    """
    raise NotImplementedError
  
  def stop(self):
    """Stop a continuous move.
    
    Unless overridden, does nothing
    """
    pass
  
  def moving(self):
    """Returns True if the stage is moving, false otherwise."""
    return False
  
  def approach(self, *args):
    """Stuff the scanning stage has to do before the scan can start.
    
    E.g. backlash/hysteresis compensation. Does nothing unless overridden.
    """
    pass

  def position(self):
    """Retrieve the scanning stage's actual position.
    
    This function MUST be overriden by child classes.
    
    :returns: the position
    :rtype: float
    """
    raise NotImplementedError

  def _format_position(self, p=None):
    """Format the position by adding the axis name and the content of :py:attr:`prepend_to_position_string`.
    
    :py:attr:`prepend_to_position_string` is used to concatenate the position strings of several :py:class:`Actuator` objects combined with :py:func:`microscope.ScanND`.
        
    :param p: the position to format. If None (default), read the current position.
    :rtype: string
    
    Private function; the public version is :func:`position_string`
    """
    if p is None:
      p = self.position()
    try:
      prepend = self.prepend_to_position_string
    except AttributeError:
      prepend = ""
    try:
      append = self.append_to_position_string
    except AttributeError:
      append = ""
    return prepend + self.name + ": " + '{:+.4f}{}'.format(p, self.unit) + append

  def print_position(self, string=None):
    """Print the axis name and the position.
    
    :param string string: the string to print. 
    """
    if string is None:
      string = self.position_string()
    terminal.printr(string)
    
  def position_string(self):
    """Return a nicely formated string with position information.
    
    This public function can be overriden; subclasses may then use :func:`_format_position`.
    """
    return self._format_position()

  def __enter__(self):
    self._context_locked = True
    
  def __exit__(self, exc_type, exc_value, traceback):
    self._context_locked = False

  @property
  def ready(self):
    """Check that the sensor is ready for use.
    
    The default behaviour is to return True if the context manager has 
    not been acquired, False if already in use.
    """
    return not self._context_locked

  def save_position(self, flag=False):
    """Append the current (time, position, flag) to the history."""
    self.history.append((time.time(), self.position(), flag))

      
  def history_array(self, span=0, flag=None):
    """Return the last *span* seconds of history records as a numpy array.
    
    If flag=None, return all record. If True or False, return only records with the same flag.
    """
    now = 0 if span==0 else time.time()
    all_rec = (flag is None)
    return np.array([(t, p, f) for (t, p, f) in self.history if t >= (now - span) and (f or all_rec)])


  def plot(self, all=False, ax=None):
    """Plot position v time.
    
    :param bool all: whether to plot all data in ``history``, or only new
                     data since the last call.
    :param ax: a matplotlib Axes object. If None, create a new Figure.
    """
    if all:
        data = self.history
    else:
      try:
        data = self.history[self.last_plotted:]
      except AttributeError:
        data = self.history
    self.last_plotted = len(self.history)-1
    if self.last_plotted > 2:
      self.figure = plotting.plot_time(np.array(data)[:,0], np.array(data)[:,1], ax=ax, hours_interval=self.hours_interval)
      return self.figure
    else:
      print "Warning: no position data to plot."
    

class ReverseChecker(object):
  """Prevents suprious motion reversal."""
  def __init__(self, actuator, max=1):
    self.actuator = actuator
    self.max = max
    self.last_step = 0
    self.counter = self.max
  
  def move_by(self, d, wait=True):
    if d * self.last_step > 0 or self.counter == 0:
      self.counter = self.max
      self.last_step = d
      self.actuator.move_by(d, wait)
    else:
      self.counter -= 1
      
  def check(self, move_by_func):
    def move_by_decorated(d, wait=True):
      if d * self.last_step >= 0 or self.counter == 0:
        self.counter = self.max
        self.last_step = d
        move_by_func(d, wait)
      else:
        self.counter -= 1
    return move_by_decorated


def reverse_checking(actuator, max=1):
  actuator.reverse = ReverseChecker(max)
  actuator.move_by = actuator.reverse.check(actuator.move_by)
  return actuator

def reverse_checking_decorator(cls, max=1):
  class ActuatorWithReverseChecking(cls):
    def __init__(self, *args, **kargs):
      super(ActuatorWithReverseChecking, self).__init__(*args, **kargs)
      self.reverse = ReverseChecker(max)
      self.move_by = self.reverse.check(super(ActuatorWithReverseChecking, self).move_by)
  return ActuatorWithReverseChecking
  
def small_steps_decorator(cls, min_motion=0):
  class ActuatorWithSmallStepsAccumulator(cls):
    def __init__(self, *args, **kargs):
      super(ActuatorWithSmallStepsAccumulator, self).__init__(*args, **kargs)
      self.small_steps = SmallStepsAccumulator(min_motion)
      self.move_by = self.small_steps.check(super(ActuatorWithSmallStepsAccumulator, self).move_by)
  return ActuatorWithSmallStepsAccumulator

class SmallStepsAccumulator(object):
  """Accumulate steps that are too small, and start moving ."""
  def __init__(self, actuator, min_motion=0):
    self.actuator = actuator
    self.min_motion = min_motion
    self.accumulator = 0
  
  def move_by(self, d, wait=True):
    self.accumulator += d
    if abs(self.accumulator) > self.min_motion:
      self.actuator.move_by(self.accumulator, wait)
      self.accumulator = 0


def small_steps(actuator, min_motion=0):
  actuator.small_steps = SmallStepsAccumulator(actuator, min_motion)
  actuator.move_by = actuator.small_steps.move_by
  return actuator


def negate_position(func):
  def move_decorated(self, p, **kwargs):
    func(-p, **kwargs)
  return move_decorated


###
### "Sensor" object provide an interface between specific acquisition device and the microscope
###

class Sensor(object):
  """Abstract representation of a sensor (eg camera, analog input...).
  
  The :py:mod:`microscope` module requires at mimimum that sub-classes override
  the functions :py:func:`snap`. :py:func:`update_display` and :py:func:`save_metadata`
  are optional.
  """
  status = True
  paused = False
  snap_info_description = None
  
  def snap(self):
    """Instructs the acquisition device to take a dataset and return the data.
    
    This function MUST be overriden by child classes.
    A successful snap must set the attributes :py:attr:`status` to True
    and :py:attr:`paused` to False.
    
    :returns: the data, or None (in which case :py:class.`Scan1D` will ignore this snap).
    """
    raise NotImplementedError
    
  def snap_info(self):
    """Return a tuple of numeric or float parameters associated with a single call to :func:`snap`, or None."""
    return None
  
  def update_display(self):
    """Specifies how to update the display
    
    This function CAN be overriden by child classes but is optional.
    """
    pass
    
  def save_metadata(self, h5file, name):
    """Saves sensor-specific metadata as HDF5 attributes.
    
    :param h5file: an open HDF5 file
    :type h5file: :py:class:`h5py.File`
    :param name: name of dataset within the file
    :type name: string
    """
    pass
    
  def initialise_acquisition(self):
    """Stuff to do before the scan can start (eg setting acq mode, exposure time...)"""
    pass
  
  def terminate_acquisition(self):
    """Stuff to do after the scan (eg return to Video mode...)"""
    pass
  
  def dark(self):
    """Take a dark/background image. shutter closed."""
    pass
  
  def intensity(*args):
    """Returns the integrated intensity."""
    raise NotImplementedError
    
  def __enter__(self):
    try:
      if self._context_locked:
        raise RuntimeError("Sensor already in use, aborting.")
    except AttributeError:
      pass
    self.initialise_acquisition()
    self._context_locked = True
    
  def __exit__(self, exc_type, exc_value, traceback):
    self._context_locked = False
    self.terminate_acquisition()
    
  @property
  def ready(self):
    """Check that the sensor is ready for use.
    
    The default behaviour is to return True if the context manager has 
    not been acquired, False if already in use.
    """
    try:
      return not self._context_locked
    except AttributeError:
      return True
