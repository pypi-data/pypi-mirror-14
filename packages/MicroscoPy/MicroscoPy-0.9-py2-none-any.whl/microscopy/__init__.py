# package microscopy/__init__.py
"""

This page gives a quick overview of the MicroscoPy environment. For more
details, refer to the documentation of the individual modules.

Introduction
------------

MicroscoPy is a simple platform for scanning confocal microscopy and spectroscopy in Python.
It is controlled entirely from the (I)Python interactive console, with the 
addition of a few graphic widget to control the instruments and visualise data.

The core modules are:

- :mod:`~microscopy.hal`: a simple API that makes it easy to integrate new hardware in MicroscoPy
                by wrapping any existing device as :class:`microscopy.hal.Actuator` or :class:`microscopy.hal.Sensor` objects.
- :mod:`~microscopy.scan`: flexible, scalable scanning routines. Multidimensional scans are build from arbitrary
                 combinations of unidimensional scans
- :mod:`~microscopy.keypad`: Tkinter widgets to control actuators from the keyboard
- :mod:`~microscopy.display`: Tkinter widgets to display camera images and 1D spectra in real time.


The tutorial provide a quick overview of MicroscoPy's usage:

.. toctree::
   :maxdepth: 2
   
   quickstart


Hardware abtraction layer
-------------------------

The :mod:`microscopy.hal` module dictates a API for any piece of hardware used in a MicroscoPy application.
Two abstract device classes are defined : :class:`microscopy.hal.Actuator` and :class:`microscopy.hal.Sensor`,
for motion devices (be they linear actuators on analog outputs)
and acquisition devices (such as cameras and analog inputs).

The API specification is extremely simple, so it only takes a few minutes
to integrate a new piece of hardware to a MicroscoPy application:

- :class:`microscopy.hal.Actuator` must be extended with two functions,
  :func:`~microscopy.hal.Actuator.move_to` and :func:`~microscopy.hal.Actuator.position`
  (to request a motion and query the position).
  
- :class:`microscopy.hal.Sensor` must be extended with a single function
  :func:`~microscopy.hal.Sensor.snap` that return some data.

The API defines other, optional functionalities. 

MicroscoPy includes a few device adapters that wrap existing third-party
device drivers into Sensor or Actuator objects (module :mod:`microscopy.device_adapters`):

* Actuators:

  - :class:`~microscopy.device_adapters.actuators.ESP`: Newport ESP 100 & 300 (based on the driver :mod:`newportESP`)
  - :class:`~microscopy.device_adapters.actuators.VoltOut`: generic analog output
  - :class:`~microscopy.device_adapters.actuators.Time`: no motion, just a time sequence
  - :class:`~microscopy.device_adapters.actuators.Piezo`: smooth voltage trajectory to drive a piezo with minimum ringing
  - :class:`~microscopy.device_adapters.actuators.ZaberAxis`: Zaber ASR microscope stage (driver :py:mod:`zaber`)

* Sensors: 
  - :class:`~microscopy.device_adapters.sensors.Andor`: EMCCD cameras (SDK v.2, driver :mod:`andor2`)
  - :class:`~microscopy.device_adapters.sensors.Pixelfly`: PCO Pixelfly CCD cameras (driver :mod:`pxlfly`)
  - :class:`~microscopy.device_adapters.sensors.VoltIn`: generic analog input

**Reference:**

See the the documentation of the :mod:`microscopy.hal` module for the API specification,
and to the built-in adapters in module :mod:`microscopy.device_adapters` for working example:

.. toctree::
   :maxdepth: 2
   
   hal
   device_adapters


Scanning microscopy
-------------------

Microscopy tries to keep it simple while being flexible and powerful:

- 1D scanning is the job of the :class:`~microscopy.scan.Scan1D` class, which combines
  an :class:`~microscopy.hal.Actuator` and :class:`~microscopy.hal.Sensor`.
- 2D scanning is done repackaging a :class:`~microscopy.scan.Scan1D`
  object as an :class:`~microscopy.hal.Actuator` and another as a :class:`~microscopy.hal.Sensor`,
  and creating another :class:`~microscopy.scan.Scan1D` object.
- 3D, and higher-dimensional scans, are created by repeating the process.
  
Scans can be paused, resumed and extended seamlessly.

Modyfying the behaviour of a scan and interacting with other parts of a larger application
is possible via several :ref:`microscopy.hooks, as described in the module documentation <scan_hooks>`.

**Reference:**

.. toctree::
   :maxdepth: 2
   
   quickstart
   scan


Graphic user interface
----------------------

Although MicroscoPy is primarly controlled from the interactive Python console,
it also comes with handy (semi-)graphical Tkinter widgets:

  - the :mod:`microscopy.keypad` module provides a :mod:`microscopy.Tkinter` widget to control
    any number of :class:`microscopy.hal.Actuator` object from the keyboard. In the example
    below, a keypad controls a XYZ stage (in reality, one vertical stage and two 
    scanning mirrors) with the Page Up/Page Down, Up/Down and Left/Right keys:
    
    .. image::
      xyz-keypad.png

  - the :mod:`microscopy.display` module provides a video display for 2D camera data,
    and another for 1D data (e.g. spectra). The later can optionally include
    widgets to control data formatting, camera exposure, and information 
    about running scans:
    
    .. image:: display-spectrum.*

**Reference:**
   
.. toctree::
   :maxdepth: 2
   
   keypad
   display


Utilities
---------

MicroscoPy also comes with a couple of small modules providing additional functionalities:

  - the ``waveform`` module defines an API for 'waveforms', regularly sampled time series.
    Required by the :class:`~microscopy.device_adapters.actuators.Piezo` device adapter.
  
  - the ``interruptible_region`` module will delay KeyboardInterrupts until it is safe
    to stop the program.
    
  - the ``terminal`` module provides functions to manipulate and print in the terminal.
  
  - the ``plotting`` module provides widgets to display multiple data, useful for monitoring 
    parameters.
"""
