MicroscoPy is a simple platform for scanning confocal microscopy and spectroscopy in Python.
It is controlled entirely from the (I)Python interactive console, with the 
addition of a few graphic widget to control the instruments and visualise data.

The core modules are:

- `hal`: a simple API that makes it easy to integrate new hardware in MicroscoPy
  by wrapping any existing device as `hal.Actuator` or `hal.Sensor` objects.
- `scan`: flexible, scalable scanning routines. Multidimensional scans are build from arbitrary
  combinations of unidimensional scans
- `keypad`: Tkinter widgets to control actuators from the keyboard
- `display`: Tkinter widgets to display camera images and 1D spectra in real time.


Installation
------------

MicroscoPy has only been tested in Python 2.7::

  $ pip2.7 install microscopy


