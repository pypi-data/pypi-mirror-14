"""
Live display of 2D data (e.g. images) and 1D data (e.g. spectra) for MicroscoPy

This classes are not meant to be used directly but subclassed for specific
purpose/hardware. In particular, :class:`LivePlot` must be extended with 
a :func:`get_data` method that returns the data to be plotted.


Widgets
-------

Extra widgets are added to LivePlot with the widgets keywords, for examples::

  widgets = [[w1,w2,w3],  # one sublist per row
             [w4],        # widgets in sublist go in column
             [w5,w6]]

will add six widgets (in three rows) below the main figure.

w1, w2, ... are not the widgets themselves, but functions that will be called
by the LivePlot constructor, and must take exactly two arguments:

  - a Tkinter object used as parent for the new widget (so the widget knows where to go)
  - a reference to the LivePlot object (so the widget can interact with the application)

In addition we may want the widget to interact objects outside the LivePlot.
This can be achieved thus::

  def create_widget_X(*args, **kwargs):
  def inner(parent, display):
    return Widget_X(parent, [display], *args, **kwargs)
  return inner

and then w1 above would be::

  widgets = [[create_widget_X(cam), ..], ...] # 
  
"""

import numpy as np
import Tkinter as tk
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt


class CustomToolbar(NavigationToolbar2TkAgg):
  """matplotlib toolbar with extra buttons for:
    1. toggle live display
    2. That's all!
    """
  # Just add a tuple (Name, Tooltip, Icon, Method) to toolitems to set more buttons.
  def __init__(self, canvas_, parent_, toggle):
    self.toolitems = super(CustomToolbar, self).toolitems + (('Live', 'Toggle live display', 'stock_refresh', 'toggle'),)
    self.toggle = toggle
    super(CustomToolbar, self).__init__(canvas_, parent_)


class LivePlot(object):
  """Provides a window to display 1D data (eg profiles across images or when in Single-Track/FVB acquisition mode).
  
  To use it you must either
    1) Provide a function to the data_func keyword argument, or
    2) Sub-class LivePlot and define a get_data() method.

  Both data_func and get_data must return a 2D array od dimensions (ntracks, npoints).
  
  In addition, the following methods can be overriden if necessary:
    - init_plot
    - if_new_data_ready
    - title
  
  All tracks will be displayed in the same plot.
  Use start() to update the plot automatically (every 100ms by default, settable via the delay property).
  """
  def __init__(self, ntracks, npoints, data_func=None, master=None, widgets=None):
    """Create a pyplot window and initialise the plot with zeros.
    
    :param ntracks: number of lines to display
    :param npoints: line length
    :param master: Tkinter parent object (will create a Toplevel if provided,
                   otherwise a new Tkinter instance)
    :param data_func: function that return data as a numpy array of shape (ntracks, npoints).
                      Alternative to overriding :func:`get_data`
    :param widgets: a nested list of optional widgets to add to the plot.
    """
    if master is None:
      self.window = tk.Tk()
    else:
      self.window = tk.Toplevel(master)
    self.live = False
    self.data_func = data_func
    # Create figure
    plt.ion()
    self._init_app(widgets)
    self.init_fig(ntracks, npoints)
    # Stuff for live updating
    self.delay = 100 # refresh rate, in ms.
    self._wheel = ('-',"\\",'|','/')
    self.count = 0
    self._if_new_data_ready_counter = 0
    self.last_image_read = None
    self.transform = lambda x: x
    
  def _init_app(self, extra):
    """Initialise the window with main plot area and widgets
    
    :param extra: a (possibly nested) list of widgets.
    """
    self.figure = mpl.figure.Figure()
    self.ax = self.figure.add_subplot(111)
    self.canvas = FigureCanvasTkAgg(self.figure, self.window)
    self.tb_frame = tk.Frame(self.window)
    self.toolbar = CustomToolbar(self.canvas, self.tb_frame, self.toggle)
    self.toolbar.update()
    self.widget = self.canvas.get_tk_widget()
    self.widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    self.extra_widgets = []
    self.extra_widgets_update = []
    self.extra_widgets_frames = []
    if extra is not None:
      for lines in extra:
        self.extra_widgets_frames.append(tk.Frame(self.tb_frame))
        for w in lines:
          self.extra_widgets.append(w(self.extra_widgets_frames[-1], self))
          self.extra_widgets[-1].pack(side=tk.LEFT)
          try:
            self.extra_widgets_update.append(self.extra_widgets[-1].refresh)
          except AttributeError:
            pass
          #self.extra_widgets_side = tk.LEFT if self.extra_widgets[-1].top else tk.TOP
        #self.extra_widgets_frames[-1].pack(side=self.extra_widgets_side)
        self.extra_widgets_frames[-1].pack(side=tk.TOP, fill=tk.BOTH, expand=1, anchor=tk.W)
    self.tb_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    self.canvas.show()


  def init_fig(self, ntracks, npoints):
    """Initialise figure with n tracks of n points each."""
    self.ntracks = ntracks
    self.npoints = npoints
    for i in range(self.ntracks):   # create as many line plots as lines in the data set (eg, 2 if there are two tracks
      self.ax.plot(np.arange(1, self.npoints+1), np.zeros(shape=self.npoints))
      
  def title(self):
    """A title string for the plot window"""
    return ""
  
  #@if_new_data_ready # now taken care of by the get_data() method
  def update(self):
    """Update the live plot."""
    self.data = self.get_data()
    if self.data is not None:
      for i, line in enumerate(self.ax.lines):
        line.set_ydata(self.transform(self.data[i])) # update ydata of each line
      for w_func in self.extra_widgets_update:
        w_func()
      self.window.title(self.title())
      self.canvas.draw()

  def get_data(self):
    """Specifies how to get the data to be plotted.
    
    It must either be overidden by subclasses or provided to the object constructor kwarg "data_func"
    Return None if no new data is available.
    """
    if self.data_func is None:
      raise NotImplementedError, "No method to get data!"
    else:
      return self.data_func()

  def start(self):
    """Start live updating of the plot."""
    self.update()
    self.callback_id = self.widget.after(int(self.delay), self.start)
    self.live = True
    self.count += 1
    
  def stop(self):
    """Stop live updating."""
    self.widget.after_cancel(self.callback_id)
    self.live = False
    
  def toggle(self):
    """Toggle live updating."""
    if self.live:
      self.stop()
    else:
      self.start()
    
  def __del__(self):
    self.stop()
  
  @property
  def autorefresh(self):
    return self.live
  @autorefresh.setter
  def autorefresh(self, b):
    if b and not self.live:
      self.start()
    elif not b and self.live:
      self.stop()


###########################
# Widgets for LiveDisplay #
###########################

# - Widgets must be subclasses of Tkinter objects
# - If it has a refresh() method, it will be called by LiveDisplay.update()
# - LiveDisplay expects not the already created widget, but a function that will create 
#   the widget, with the following signature
#     def create_widget_func(parent, display):
#       return Widget_X(parent)
# 
# To pass additional parameters to the widget, wrap the previous function:
#   def create_widget_X(*args, **kwargs):
#     def create_widget_func(parent, display):
#       return Widget_X(parent, display, *args, **kwargs)
#     return create_widget_func



# Add a status bar

def status_widget(status_var=None, **kwargs):
	"""Return a function that can be passed to :class:`LivePlot` to add a :class:`StatusWidget`"""
	def inner(parent, display):
		# Single line widget, return as list
		return StatusWidget(parent, status_var=status_var, **kwargs)
	return inner

class StatusWidgetVar(object):
	"""Thread-safe read/write buffer for :class:`StatusWidget`."""
	def __init__(self):
		self.set('')
	def set(self, string):
		self._string = string
		self.new = True
	def get(self):
		self.new = False
		return self._string

class StatusWidget(tk.Label):
	def __init__(self, master, status_var):
		self.string = status_var # StatusWidgetVar object
		self._var = tk.StringVar(master)
		tk.Label.__init__(self, master, textvariable= self._var, text='No status info', anchor=tk.W)

	def pack(self, **kwargs):
		tk.Label.pack(self, fill=tk.BOTH, expand=1, **kwargs)

	def refresh(self):
		if self.string.new:
			self._var.set(self.string.get())


# Add an exposure setting 

def exposure_widget(cam, **kwargs):
	"""Return a function that can be passed to :class:`LivePlot` to add an :class:`ExposureWidget`"""
	def inner(parent, display):
		return ExposureWidget(parent, cam, **kwargs)
	return inner

class ExposureWidget(tk.Frame):
	"""Frame with an Entry that sets the exposure of the camera."""
	def __init__(self, master, cam, label_on_top=True):
		"""
		:param master: the widget's parent
		:param cam: the camera (any object with a settable ``exposure`` property)
		:param bool label_on_top: whether to display the label aboveor left of the widget
		"""
		self._cam = cam
		tk.Frame.__init__(self, master)
		self._var = tk.IntVar(self)
		#self._var.trace('w', self._set_exposure)
		self._var.set(int(cam.exposure))
		self._label = tk.Label(self, text='Exposure (ms)')
		self._entry = tk.Entry(self, textvariable=self._var, width=5, justify=tk.RIGHT)
		self._entry.bind('<KeyPress-Return>', self._set_exposure)
		self._entry.bind('<KeyPress-KP_Enter>', self._set_exposure)
		self._label.pack(side=tk.TOP if label_on_top else tk.LEFT)
		self._entry.pack()
		
	def _set_exposure(self, *args):
		try:
			exp = self._var.get()
			self._cam.exposure = exp
		except ValueError:
			pass


# Add an autorefresh buttom

def autorefresh_widget(**kwargs):
	"""Return a function that can be passed to :class:`LivePlot` to add an :class:`AutoRefreshWidgetWidget`."""
	def inner(parent, display):
		return AutoRefreshWidget(parent, display, **kwargs)
	return inner

class AutoRefreshWidget(tk.Frame):
	"""A Frame with an Button that toggle the display autorefresh state."""
	def __init__(self, master, display):
		"""
		:param master: the widget's parent
		:param disp: the camera display (any object with a settable ``autorefresh`` property)
		"""
		self._display = display
		tk.Frame.__init__(self, master)
		self._autorefresh_status = display.autorefresh
		self._button = tk.Button(self, width=15, justify=tk.RIGHT,
		                         command=self._set_autorefresh)
		if self._autorefresh_status:
			self._button.config(text='Autorefresh ON', relief=tk.SUNKEN)
		else:
			self._button.config(text='Autorefresh OFF', relief=tk.RAISED)
		self._button.pack()

	def _set_autorefresh(self, *args):
		# Toggle auto-refresh state
		self._autorefresh_status = not self._display.autorefresh
		self._display.autorefresh = self._autorefresh_status
		if self._autorefresh_status:
			self._button.config(text='Autorefresh ON', relief=tk.SUNKEN)
		else:
			self._button.config(text='Autorefresh OFF', relief=tk.RAISED)


# Add a log/linear scale menu and offset 

def scale_widget(**kwargs):
	"""Return a function that can be passed to :class:`LivePlot` to add an :class:`VerticalScaleWidget`"""
	def inner(parent, display):
		return VerticalScaleWidget(parent, display, **kwargs)
	return inner

class VerticalScaleWidget(tk.Frame):
	"""Frame with a linear/log menu and vertical offset"""
	def __init__(self, master, disp, label_on_top=True):
		"""
		:param master: the widget's parent
		:param disp: the camera display (any object with a settable ``transform`` property)
		:param bool label_on_top: whether to display the label aboveor left of the widget
		"""
		self._disp = disp
		side = 0 if label_on_top else 1
		tk.Frame.__init__(self, master)
		
		self._saved_lin_scale = self._disp.ax.get_ylim()
		
		self._scale_var = tk.StringVar(self)
		self._offset_var = tk.IntVar(self)
		self._scale_var.trace('w', self._set_scale)
		self._offset_var.trace('w', self._set_offset)
		
		self._scale_label = tk.Label(self, text='Scale')
		self._scale_optionmenu = apply(tk.OptionMenu, (self, self._scale_var) + ('linear', 'log'))
		self._scale_optionmenu.config(width=6)
		self._scale_var.set('linear')
		
		self._offset_label = tk.Label(self, text='Offset')
		self._offset_entry = tk.Entry(self, textvariable=self._offset_var, width=5, justify=tk.RIGHT)

		self._scale_label.grid(row=0, column=0)
		self._scale_optionmenu.grid(row=1-side, column=0+side)
		self._offset_label.grid(row=0, column=1+side)
		self._offset_entry.grid(row=1-side, column=1+2*side)
	
	def _set_scale(self, *args):
		self._disp.ax.set_yscale(self._scale_var.get())
	
	def _set_offset(self, *args):
		try: 
			offset = self._offset_var.get()
			self._disp.transform = lambda x: x - offset
		except ValueError:
			pass
