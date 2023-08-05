"""
The :mod:`scan` module is part of the :mod:`microscopy` package. It provides
a framework for multidimensional scanning routines while acquiring data.

.. Warning::
   **Problem solved (hopefully)**
   Occasionally, when pausing/resuming a scan, the active scan will
   save a wrong number of data points. As a result the pos and spec arrays 
   are not properly dimensioned, causing an exception when saving to HDF5.

Usage
-----

Assuming ``cam`` and ``ax`` are :class:`hal.Sensor` and :class:`hal.Actuator`
objects, representing for example a camera as sensor and a translation stage
as actuator. Create and start a 1D scan with

>>> from microscopy.scan import Scan1D, ScanND
>>> scan = Scan1D((10, -0.6, -0.01), cam, ax)
>>> scan.run()
    X: -0.5999 V  # scan progress is printed in console

For multidimensional scans, simply create as many :class:`Scan1D` objects
as required and combined them with :func:`ScanND`:

>>> scan3d = ScanND((scan1, scan2, scan3, ...))
>>> scan3d.run(thread=True)

Here the scan was started in a background thread to avoid blocking
the Python console. The first scan in the list will be the slowest.

Scans can be paused and resumed at will by pressing :kbd:`Ctrl+C` (if running in
the main thread) or ``scan.pause()`` (if running in a background thread).
To resume, simply recall ``scan.run()`` or ``scan.run(thread=True)``.
To see the scan progress:

>>> scan.ax.print_position()
    X: -0.5999 V

.. _scan_hooks:

Interfacing with other Python objects
-------------------------------------

Several hooks are provided:

  1) Attributes :attr:`Scan1D.at_every_point`, :attr:`Scan1D.at_start`, :attr:`Scan1D.at_end`
     are list of functions that will be called after every sensor acquisition, at the beginning
     of a scan, and at the end of a scan, respectively. The functions must have no arguments.
     They can be passed to the constructor as keyword arguments, or appended to/removed from the
     attributes at any time with immediate effect.
     
  2) A :class:`threading.Event` object may be passed to the constructor's
     :attr:`Scan1D.iteration_event` keyword.
     The Event will be set at after every sensor acquisition to notify
     any object that may be waiting on the Event.
     
  3) A function returning a bool may be passed to the optional ``check`` argument
     The function will be called after every point,
     and the scan will be terminated if True is returned.
     
  Method 1 is more suitable to trigger actions that will take place in the same thread as the scan,
  while Method 2 allows interaction with objects in a different thread.

Saving data
-----------

Inside a :class:`Scan1D` object, the acquired data is saved as a multi-dimensional
:class:`numpy.ndarray` in the :attr:`Scan1D.spectra`. Similarly the position is recorded
in :attr:`Scan1D.pos`, the position of all axes is recorded at every point.
The :func:`Scan1D.save` method will write these arrays in a HDF5 :class:`h5py.File`:

>>> scan.save('filename', 'dataset_name', comment='some comments')

------
"""

import numpy as np
import time
import sys
import hal
from copy import copy
import threading
import logging
import warnings
import h5py

from .utilities import interruptable_region as ctlc
from .utilities import terminal

scan_history = []
logger = logging.getLogger(__name__) # not in use yet

###
### Scanning
###

#: Overwrite this with a :class:`Tkinter.StringVar` from the setup script
#: so that all scan use this var to display status info.
_status_var = None


class Scan1D(object):
  """Flexible 1D scan."""
  def __init__(self, scan_range, cam, ax,
                at_start=(), at_every_point =(), at_end=(), iteration_event=None, check=lambda scan: False,
                reverse_next=False, repeat=1,
                history=scan_history, primary=True):
    """
    **Required arguments**:
    
    :param scan_range: (start, length, step)
    :param cam: A Sensor object that implements the snap() method
    :param ax: an Actuator object that implements the move_to() and position() methods
    
    **Optional arguments**:
    
    :param at_start: tuple of functions that will be called before the scan start, after each snap, or at the end, respectively. Useful to run some optimisation routines or checks.
    :param at_every_point: Similar to at_start, but the functions are called at every point in the scan
    :param at_end: Similar to at_start
    :param iteration_event: a threading.Event object that is set() at the end 
                            of every iteration.
    :param check: function , called after every acquired data point.
                  The scan will terminates it True is returned.
    :param bool reverse_next: Whether to run the next scan in reverse
    :param int repeat: Repeat the scan n times, appending the data.
                       E.g. set reverse_next=True and repeat=2 to close the scan trajectory.
    :param history: append a copy of scan object to this list when scan finishes.
    :param primary: True if this is a true 1D scan, false if multi-dimensional.
    """
    self.scan_range = scan_range
    (self.start, self.length, self.step) = scan_range
    self._current_step = self.start
    self.stop = self.start + self.length
    self.pos = []
    self.spec = []
    self.snap_info = []
    self.cam = cam
    self.ax = ax
    # Hooks
    self.at_start = at_start
    self.at_every_point = at_every_point
    self.at_end = at_end
    self.iteration_event = iteration_event
    self.check = check
    # Scan controls
    self.paused = False
    self.reverse_next = reverse_next
    self.repeat = repeat
    self._pause_flag = threading.Event()
    self.unsaved_data = False
    self.scan_status = 'Created'
    self.resume_at_same_position = True # whether to repeat the last point when resuming a paused scan
    
    self.primary = primary
    self.history = history
    global _status_var
    self._status_var = _status_var 
    
    # currently save scan here and at end. Maybe remove one?
    if self.history is not None:
      self.history.append(self)
    
    # Check hooks are valid
    for func_list in (self.at_end, self.at_start, self.at_every_point):
      b = True
      for func in func_list:
        b &= callable(func)
      assert hasattr(func_list, '__iter__') and b, 'Hook must be a list of callable objects'    
    
  def __repr__(self):
    return '<microscope.Scan1D object on axis ' + self.ax.name + '.>'
  
  def _initialise(self):
    """Stuff to do before a new scan can start."""
    self.do(self.at_start)
    if not self.keep_old_data:
      self.pos = []
      self.spec = []
      self.snap_info = []
      self.proc = []
    self.start_actual = self.start
    self.ax.iteration = 0
    if not self.threaded:
      terminal.printr('  > ' + self.ax.name +': moving to start position...')
    self.ax.approach(self.start, self.step)
    self.t_start = time.time()
    self.scan_status = 'Running'
    
  def _resume(self):
    """Stuff to do so the interrupted scan can resume gracefully."""
    self.paused = self._paused = False
    if not self.threaded:
      print("Resume " + self.ax.name + " scan ? (y/n): ")
      resume = sys.stdin.readline()[0] # raw_input has problems with Tkinter...
    else:
      resume = 'y' # Automatically resume is running in a thread.
      
    if resume is 'y':
      print "Resuming " + self.ax.name + " scan at position " + str(self.start_actual)
    else:
      print "Restarting " + self.ax.name + " scan."
      self._initialise()

  def pause(self):
    # Public pause, to be called in main thread
    """Tell the scan to pause when running in a background thread."""
    self.paused = self.ax.paused = self.cam.paused = True
    self.scan_status = 'Paused'
    # self.cam.paused effectively tells the fast scan, if any, to pause too.
    self._paused = False # will be set to True when the scan is paused
    while not self._paused:
      time.sleep(0.1)

  def _pause(self, index, position):
    # Internal pause, called from :func:`loop`
    """Stuff to do so the interrupted scan can resume gracefully."""
    self.start_actual = position + (0 if self.resume_at_same_position else self.step)
    self.paused = self.ax.paused = self.cam.paused = True
    self.t_stop = time.time()
    print("%s paused at position (%d, %f). Call run() again to resume." % (self.ax.name, index, self.start_actual))
    if self._status_var is not None:
      self._status_var.set(self.position_string())
    self._paused = True
    
  def _iteration(self, p):
    """Stuff to do for one scan iteration at position p."""
    self._current_step = p
    self.ax.move_to(p)
    if not self.threaded:
      terminal.printr(self.position_string())
    elif self._status_var is not None:
      self._status_var.set(self.position_string())
    new_data = self.cam.snap()
    if new_data is not None:
      self.spec.append(new_data)
      self.pos.append(self.ax.position()) # MUST be called AFTER snap() (required by Scan2D)
      self.proc.append(self.process(self.spec[-1]))
      snap_info = self.cam.snap_info()
      if snap_info is not None:
        self.snap_info.append(snap_info)
    if self.primary:
      self.do(self.at_every_point)
      if self.iteration_event is not None:
        self.iteration_event.set()
    self.ax.iteration += 1
    if not self.threaded:
      self.cam.update_display()

  def process(self, spectrum):
    #do some live processing? Would have to be done in a thread :-(
    return None
    
  def extend(self, distance):
    """Extend the scan by an extra distance. 
    
    The scan state is set to 'paused'. Call run() to acquire the extended segment."""
    self.start_actual = self.stop + self.step
    self.stop = self.stop + self.step + distance
    self.paused = True
  
  def reset(self):
    """
    Call reset() if the scan as been interrupted but you want to restart at the beginning, not where is was stopped.
    
    Note that the data will not be erased until run() is called.
    """
    self.paused = False
    
  #def check(self):
    #"""This function is called at the end of each iteration. If it returns True, the scan is stopped.
    #Override this function """
    #return False # Do noth
  
  def loop(self, repeat=None, keep_old_data=False):
    """Do one scan, and return True upon completion, False if interrupted.
    
    Not to be called directly by the user (use :func:`run` instead).
    
    Ctrl+C to gracefully stop it before scheduled end while keeping the acquired data.
    
    :param int repeat: How many times to repeat the scan, default=1 (no repeat).
                       Can be used with reverse_next.

    :returns: True if the scan is terminated successfully, False if interrupted before completion.
    :rtype: bool
    """
    self.keep_old_data = keep_old_data
    # initialise
    if self.paused:
      self._resume()
    else:
      self._initialise()
    self.steps = np.arange(self.start_actual, self.stop + 0.1*self.step, self.step)
    # catch Ctrl+C to pause scan when not threaded. Because the signal is not reset immediately, all scans will get the interrupt.
    with ctlc.InterruptableRegion(disable=self.threaded) as interrupt:
      for (i, p) in enumerate(self.steps): # ugly but otherwise it overshoots when self.resume_at_last_position=False.
        self._iteration(p)
        if self.check(self):
          return True
        if interrupt.interrupted or (not self.cam.status) or self.paused:
          # Ctrl+C caught or snap interrupted. Save scan state and exit function.
          self._pause(i, p)
          return False
    
    # Scan complete. Clean up:
    self.do(self.at_end)
    # Reverse direction of next scan
    if self.reverse_next:
      (self.start, self.stop, self.step) = (self.stop, self.start, -self.step)
    # Start next scan
    if repeat is None:
      repeat = self.repeat
    if repeat > 1:
      self.loop(repeat=repeat-1, keep_old_data=True)
    # Update status
    self.t_end = time.time()
    self.scan_status = 'Done'
    if self._status_var is not None:
      self._status_var.set(self.position_string()) 
    # Safeguards
    self.unsaved_data = True
    if self.history is not None:
      self.history.append(copy(self))

    return True

  def run(self, thread=False, keep_old_data=False):
    """Start the scan.
    
    :param bool thread: whether to run the scan in a background thread.
    :param bool keep_old_data: if True, new data will be appended to the existing one.
                               If False, any existing data will be overwritten.
    """
    # wrapper to insert camera initialisation.
    def start_run():
      with self.cam: # Set camera in Kinetic mode
        return self.loop(self.repeat, keep_old_data)

    # initialise scan hierarchy
    self.ax.level = 0
    
    # Prompt user to avoid accidental lost of data
    if self.unsaved_data and not self._paused:
      reply = raw_input("Data has not been saved. Overwrite ('o'), Append (a) or Abort ? : ")
      if reply not in 'oOaA':
        print 'Aborting scan.'
        return False
      elif reply in 'aA':
        print 'New data will be appended to the existing one.'
        keep_old_data = True
      else:
        print 'Deleting old data.'

    if thread:
      try:
        if self.thread.is_alive() or "Scan1D" in [t.name for t in threading.enumerate()]:
          raise RuntimeError("Threaded scan is already running!")
      except AttributeError:
        pass
      self.thread = threading.Thread(target=start_run, name="Scan1D")
      self.threaded = True
      self.thread.start()      
      # Wait until the Sensor wakes up
      while self.cam.paused:
        time.sleep(0.1)
    else:
      self.threaded = False
      start_run()

  #Propagate 'threaded' down the scan chain
  @property
  def threaded(self):
    return self.cam.threaded      
  @threaded.setter
  def threaded(self, boolean):
    self.cam.threaded = self.ax.threaded = boolean

  def do(self, func_list, *args, **kwargs):
    """Call all functions in func_list (with self as first argument)"""
    for func in func_list:
      func(self, *args, **kwargs)

  def _save_data(self, h5file, dataset_name):
    """Save the data (HDF5 file and dataset defined in :func:`save`)."""
    h5file.create_dataset(dataset_name+"/spectra", data=np.array(self.spec))
    h5file.create_dataset(dataset_name+"/positions", data=np.array(self.pos))
    if len(self.snap_info) > 0:
      h5file.create_dataset(dataset_name+"/params", data=np.array(self.snap_info))
      h5file[dataset_name+"/params"].attrs['description'] = np.string_(self.cam.snap_info_description)
  
  def _save_metadata(self, h5file, dataset_name):
    """Append metadata to the previously created HDF5 group."""
    h5file[dataset_name].attrs['created'] = time.strftime("%d/%m/%Y %H:%M:%S")
    h5file[dataset_name].attrs['time_saved'] = time.time()
    h5file[dataset_name].attrs['time_start'] = self.t_start
    h5file[dataset_name].attrs['scan_start'] = self.start
    h5file[dataset_name].attrs['scan_stop'] = self.stop
    h5file[dataset_name].attrs['scan_step'] = self.step
    try:
      h5file[dataset_name].attrs['time_end'] = self.t_end
    except AttributeError:
      pass

  def save(self, filename, dataset_name, comment=""):
    """Save data and metadata in a new HDF5 group.
    
    :param string filename: name of the H5 file (must already exist).
    :param string dataset_name: name of the dataset (must not already exist).
    :param string comment: to be saved as attribute 'comment' under 'dataset_name'.
    """
    with h5py.File(filename, 'r+') as h5file:
      self._save_data(h5file, dataset_name)
      self._save_metadata(h5file, dataset_name)
      self.cam.save_metadata(h5file, dataset_name)
      h5file[dataset_name].attrs['comment'] = comment
    self.unsaved_data = False
    
  def print_position(self):
    """Print a pretty status string to the terminal."""
    terminal.printr(self.position_string())

  def position_string(self):
    """Return a formatted status string."""
    self.ax.append_to_position_string = " ({:.0f}%)".format(100*abs(self.start-self._current_step)/float(abs(self.stop-self.start)))
    return self.scan_status + ' : ' + self.ax.position_string()


class _FastAxis(hal.Sensor):
  """Take a Scan1D object and turn it into a Sensor object which
  can be used as the fast scan axis of a second Scan1D object 
  to create a 2D scan.
  
  See :func:`ScanND`
  """
  def __init__(self, fast_scan):
    """
    :param fast_scan: the fast scan, a :class:`Scan1D` instance
    """
    self.fast_scan = fast_scan
    self.is_scanning_sensor = True
    # Type-checking isinstance(self.fast_scan.cam, _FastAxis) would be
    # less ugly but always returns False??
    # Only the lowest-level scan (whose Sensor would be missing the is_scanning_sensor
    # attribute) should resume_at_same_position = False
    try:
      if self.fast_scan.cam.is_scanning_sensor:
        self.fast_scan.resume_at_same_position = True
      else:
        self.fast_scan.resume_at_same_position = False
    except AttributeError:
      self.fast_scan.resume_at_same_position = False
    
  def __repr__(self):
    return "<FastAxis Sensor; scanning axis: " + self.fast_scan.ax.name + ".>"
  
  def snap(self):
    self.status = self.fast_scan.loop()
    if self.status: # ignore data if scan was interrupted
      return np.array(self.fast_scan.spec)
    else:
      return None

  def snap_info(self):
    snap_info = self.fast_scan.snap_info
    if len(snap_info) > 0:
      return np.array(snap_info)
    else:
      return None
      
  def update_display(self):
    self.fast_scan.cam.update_display()
  
  def save_metadata(self, h5file, dataset_name):
    self.fast_scan.cam.save_metadata(h5file, dataset_name)
    
  def initialise_acquisition(self):
    self.fast_scan.cam.initialise_acquisition()
    
  def terminate_acquisition(self):
    self.fast_scan.cam.terminate_acquisition()
  
  # Propagate pause request down the scan chain
  @property
  def paused(self):
    return self.fast_scan.paused   
  @paused.setter
  def paused(self, b):
    self.fast_scan.paused = self.fast_scan.cam.paused = b


class _SlowAxis(hal.Actuator):
  """Take two Scan1D object and create an Actuator object which can be used to create a 2D scan.
  
  See :func:`ScanND`
  """
  def __init__(self, slow, fast):
    """
    :param slow: the slow scan, a :class:`Scan1D` instance
    :param fast: the fast scan, a :class:`Scan1D` instance
    """
    self.slow = slow
    self.fast = fast
    self.name = self.slow.ax.name
    self.unit = self.slow.ax.unit
    self.approach = self.slow.ax.approach
  
  def __repr__(self):
    return "<SlowAxis Actuator on axis " + self.name + " (recursion level " + str(self.level) + ").>"

  def move_to(self,p):
    self.slow.ax.move_to(p)

  def position(self):
    """Takes the pos array returned by the subsidiary scan, and append the 
    current slow-axis position."""
    slow_pos = self.slow.ax.position()
    fast_pos = np.array(self.fast.pos)

    if len(fast_pos.shape) == 1:
      # 2D scan is a special case because the 1D scan has no extra dimension for the coordinate array.
      return np.vstack((fast_pos, slow_pos * np.ones(shape=len(fast_pos)))).transpose()

    elif len(fast_pos.shape) >=3:
      # ND scan, N>3
      n = len(fast_pos.shape)
      new_pos_array = slow_pos * np.ones(shape=fast_pos.shape[0:n-1] + (1,))
      return np.concatenate((fast_pos, new_pos_array), axis=n-1)

  def position_string(self):
    """Extend :func:hal.Actuator.position_string` to concatenate position info from all axes in the scan chain."""
    slow_pos = self.slow.ax.position()
    self.fast.ax.prepend_to_position_string = self._format_position(slow_pos) + " | "
    return self.fast.ax.position_string()
  
  #: Propagate the 'threaded' attribute down the scan chain
  @property
  def threaded(self):
    return self.fast.threaded    
  @threaded.setter
  def threaded(self, b):
    self.slow.threaded = self.fast.threaded = b
  
  #: Useful to assert the axis hierarchy.
  @property
  def level(self):
    return self._level
  @level.setter
  def level(self, n):
    self._level = n
    self.slow.ax.level = n+2
    self.fast.ax.level = n+1


def Scan2D(slow, fast):
  """Return a 2D scan made from two Scan1D objects.
  
  The first scan is the slow one."""
  return Scan1D(slow.scan_range, _FastAxis(fast), _SlowAxis(slow, fast), primary=False)


def ScanND(scan_list):
  """Return a mulidimensional scan from a list od 1D scans.
  
  The slowest scan goes first.
  
  Internally, individual scans are repackaged as :py:class:`hal.Actuator` and :py:class:`hal.Sensor` objects, 
  and the multi-dimensional scan is a regular Scan1D object.
  
  :param scan_list: a list of Scan1D objects
  :rtype: Scan1D
    
  :Example:
  
  >>> xscan = Scan1D((-1, 2, 0.008), h.cam, h.x)
  >>> yscan = Scan1D((-1, 2, 0.008), h.cam, h.y)
  >>> xyscan = ScanND((xscan, yscan))
  >>> xyscan.run()
  """
  def build_scan_rec(scan_list, part_scan):
    if part_scan is None:
      # Initiate recursion
      return build_scan_rec(scan_list[0:-2], Scan2D(scan_list[-2], scan_list[-1]))
    elif len(scan_list) == 0:
      # Terminate recursion
      return part_scan
    else:
      # Continue recursion
      return build_scan_rec(scan_list[0:-1], Scan2D(scan_list[-1], part_scan))

  assert len(scan_list) >= 2, 'Require at least two Scan1D objects to make a multidimensional scan!'
  return build_scan_rec(scan_list, None)


class Stepper(object):
  """Transform a regular (square) scan into a stair-like scan by increase the start point of the scan by ``step`` every ``n`` scans::
  
  |.........         ...          # in this example: 
  |.........         ......       #   - step = 1
  |.........   -->   .........    #   - n= 3
  |.........         .........
  |                     ......
  |                        ... 
  
  :Usage:
  
  Pass a Stepper object to the ``at_end`` keyword argument of the :class:`Scan1D` constructor, 
  and use the latter as the slow axis of a multidimensional scan as as usual:
  
  >>> xscan = Scan1D((start, length, stop), cam, ax, at_end=[Stepper(step, n)])
  >>> yscan = Scan1D(...)
  >>> xyscan = ScanND((yscan, xscan))
  
  .. Note:: The scans will have to be recreated before running it again.
  """
  def __init__(self, step, n):
    """
    :param step: the offset introduced by every step
    :param int n: number of scans between offset increase
    """
    self.n = n
    self.i = 0
    self.step = step
    
  def __call__(self, scan):
    """To be called by a :class:`Scan1D` at the end of the scan.
    
    :param scan: reference to the calling scan
    """
    self.i += 1
    if self.i % self.n ==0:
      scan.start += self.step
      scan.stop += self.step
