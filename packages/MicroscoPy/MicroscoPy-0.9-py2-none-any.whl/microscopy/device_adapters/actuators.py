# -*- coding: utf-8 -*-
"""
:class:`hal.Actuators` device adapters shipped with MicroscoPy:

  - Newport :class:`ESP` (based on the driver :mod:`newportESP`)
  - MCCDAQ USB2600 analog output (driver :mod:`usb2600.usb2600`)
  - :class:`Time`: no motion, just a time sequence
  - :class:`Piezo`: smooth voltage trajectory to drive a piezo with minimum ringing
  - :class:`Zaber` ASR microscope stage (driver :mod:`zaber`)
  
--------------------------
"""

import time
from math import copysign

from .. import hal
#from microscopy import hal

class ESP(hal.Actuator):
  """Device adapter for Newport ESP :py:class:`newportESP.Axis` objects."""
  def __init__(self, axis, name="ESP", dir=1):
    self.axis = axis
    self.unit = "mm"
    self.name = name
    self.min_displacement = 0
    self.small_steps_accumulator = 0
    self.previous_dir = 0
    self._last_position_read = None
    self.dir = dir
  
  def move_to(self, p, wait=True):
    self.axis.move_to(p, wait=wait)

  def move_by(self, d, wait=True):
    if abs(d) > self.min_displacement:
      self.axis.move_by(d, wait=wait)
      self.small_steps_accumulator = 0
    else:
      self.small_steps_accumulator += d
      if abs(self.small_steps_accumulator) > self.min_displacement:
        self.axis.move_by(self.small_steps_accumulator, wait=wait)
        self.small_steps_accumulator = 0
    self.previous_dir = copysign(1, d)

  def move(self, dir):
    if dir < 0:
      self.axis.move_up()
    else:
      self.axis.move_down()

  def stop(self):
    self.axis.stop()
    
  def moving(self):
    return self.axis.moving

  def position(self):
    p = self.axis.position
    self._last_position_read = p
    return p
  
  def approach(self, start, step):
    """move 50um before the start position before scanning to avoid hysteresis."""
    self.move_to(start - step/abs(step)*0.050)
    self.move_to(start)

# The Piezo adapter depends on the waveform package and will only be
# available if it can be imported.

try:
  from ..utilities import waveform

  class Piezo(hal.Actuator):
    """This voltage Actuator moves between points along a smooth sine trajectory
    to drive a piezo with minimum ringing.
    
    When calling move_to() or move_by() with wait=False, the analog output scan
    will be delegated to a background thread.
    """
    def __init__(self, daq, output=2, name="PZ", wait=0.00, dt=0.050, rate=2000.0, tf=0.1):
      """
      :param daq: USB2600 instance (or anything with a compatible ScanAO method)
      :param output: integer: the voltage output to use
      :param name: a short, meaningfull name for the axis
      :type name: string
      :param dt: duration of the voltage ramp
      :type dt: float
      :param rate: sampling rate for the voltage ramp
      :type rate: float
      :param tf: scaling factor for the USB refresh rate (see :py:mod:`drivers.mccdaq.usb2600`)    
      """
      self.daq = daq
      self.output = output
      self.ao = getattr(self.daq, 'ao'+str(self.output)) # AO_Single instance for channel 'output'
      self.wait = wait
      self.unit = "V"
      self.name = name
      self.dt = dt
      self.tf = tf
      self.rate = rate
      self.limits = (0, 7.5)
      self.slope = 0.321 # piezo calibration, in um/V (V before amplification)
      
    def move_to(self, p, wait=True):
      assert self.limits[0] <= p <= self.limits[1], 'Final position %r ouside allowed limits %s' %(p, str(self.limits))
      self.wave = waveform.gosine(self.position(), p, self.dt, self.rate)
      self.scan = self.daq.AOScan((self.output,), self.wave, tf=self.tf, verbose=False)
      self.scan.run(n=1, thread=(not wait))

    def position(self):
      return self.ao()
      
except ImportError:
  print 'Cannot import module "waveform", Piezo adapter will not be available.'

  
class VoltOut(hal.Actuator):
  """Analog output device adapter."""
  def __init__(self, ao, name="V", wait=0.02):
    """
    :param ao: the analog output (any callable object that, when called with a float as argument,
               set the voltage to that value; when called with no argument, return the current voltage).
    :param str name: a short name
    :param float wait: waiting time after setting the voltage
    """
    self.ao = ao
    self.wait = wait
    self.unit = "V"
    self.name = name
    self.disable_key_repeat = False
    
  def move_to(self, p, wait=True):
    self.ao(p)
    if wait:
      time.sleep(self.wait)
    
  def position(self):
    return self.ao()
    
    
class Time(hal.Actuator):
  """A special Actuator that performs a scan in time. 
  
  .. Note::
     The scan_range=(start, length, step) arguments of
     microscope.Scan1D are in units of dt. Set start=0 to start
     scan immediately upon calling run(), or to a positive number
     for a delayed start.
  """
  def __init__(self, dt):
    """:param dt: time between points, in seconds."""
    self.dt = dt; assert dt>=0
    self.name = "T"
    self.unit = "s"
  
  def position(self):
    return time.time() - self.time_started
    
  def move_to(self, p):
    # p is the scan iteration number, which we want to start at:
    time_next = time.time() - self.time_latest
    # wait until time_next, or start immediately if in the past
    if time_next < self.dt:
      time.sleep(self.dt - time_next)
    self.time_latest = time.time()
    
  def approach(self, *args):
    self.time_started = time.time()
    self.time_latest = time.time()


class ZaberAxis(hal.Actuator):
  """Device adapter for :class:`zaber.serial.AsciiAxis` objects.
  
  .. Important:
     For thread-safe operation, the adapter relies on a :class:`Lock` object
     being present in the actuators's parent serial port :class:`zaber.serial.AsciiSerial`.

  """
  def __init__(self, axis, name='zaber', use_mm=True):
    """
    :param axis: a :py:class:`zaber.serial.AsciiAxis` instance
    :param name: a meaningful name (eg. "X")
    :type name: string
    :param use_mm: if True, considers that all inputs are in mm.
                   if False, use microsteps units.
    :type use_mm: bool
    """
    self.axis = axis
    self._use_mm = use_mm
    self._resolution = int(axis.send('get resolution').data)
    self._mm_per_rev = 2
    self._steps_per_rev = 200
    self.ustep_per_mm = float(self._steps_per_rev*self._resolution/self._mm_per_rev)
    self.unit = 'mm' if use_mm else 'µsteps'
    self.name = name
    self.velocity = 10000
    self.step_scaling = 1 if use_mm else 10000
    
  def usteps(self, mm):
    """Convert milimeters to microsteps."""
    return int(mm * self.ustep_per_mm)
    
  def mm(self, usteps):
    """Convert usteps to milimeters."""
    return usteps / self.ustep_per_mm
    
  def move_to(self, p, wait=True):
    if self._use_mm:
      p = self.usteps(p)
    with self.axis.parent.port.lock:
      self.axis.move_abs(int(p), blocking=wait)
 
  def move_by(self, p, wait=True):
    if self._use_mm:
      p = self.usteps(p)
    with self.axis.parent.port.lock:
      self.axis.move_rel(int(p), blocking=wait)
    
  def move(self, dir):
    with self.axis.parent.port.lock:
      self.axis.move_vel(int(copysign(self.velocity, dir)))
    
  def position(self):
    with self.axis.parent.port.lock:
      usteps = int(self.axis.send('get pos').data)
    if self._use_mm:
      return self.mm(usteps)
    else:
      return usteps
    
  def stop(self):
    with self.axis.parent.port.lock:
      self.axis.stop()

  def moving(self):
    with self.axis.parent.port.lock:
      status = self.axis.get_status()
    return status == 'BUSY'
