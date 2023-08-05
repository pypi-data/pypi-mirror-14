"""General-purpose plotting utilities."""

import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from contextlib import contextmanager
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import Tkinter as tk
from cycler import cycler

@contextmanager
def interactive(status):
	"""Make sure that pyplot interactive mode is on or off for the duration of the context manager"""
	status_out = plt.isinteractive()  # status before calling the context manager
	if status_out == status:
		yield
	else:
		plt.interactive(status)
		yield
		plt.interactive(status_out)


class CustomToolbar(NavigationToolbar2TkAgg):
	"""matplotlib toolbar with extra buttons for:
	  1. toggle live display
	  2. That's all!
	"""
	# Just add a tuple (Name, Tooltip, Icon, Method) to toolitems to set more buttons.
	def __init__(self, canvas_, parent_, refresh, share_xlim):
	  self.toolitems = super(CustomToolbar, self).toolitems + (('Refresh', 'Refresh display', 'stock_refresh', 'refresh'), ('Lock', 'Set all xlims to that of top graph', 'subplots', 'share_xlim'))
	  self.refresh = refresh
	  self.share_xlim = share_xlim
	  super(CustomToolbar, self).__init__(canvas_, parent_)


class Display(object):
  """Display multiple data in subplots, with a `refresh` button and automatic refresh.
  
  .. note:: Clicking the ``close`` button will hide the window, not close it.
            Recall the window with ``..window.deiconify()``
  """
  def __init__(self, elems, master=None, title='Live plot window', color_cycle=None):
    """
    :param elems: a list of objects, all of which must have a ``plot()`` method.
    :param master: Tkinter parent object. If None, create a new Tkinter app.
    :param string title: window title.
    """
    self.elems = elems
    if master is None:
      self.window = tk.Tk()
    else:
      self.window = tk.Toplevel(master)
    self.figure = mpl.figure.Figure()
    self.canvas = FigureCanvasTkAgg(self.figure, self.window)
    self.toolbar = CustomToolbar(self.canvas, self.window, self.plot_refresh, self.share_xlim)
    self.toolbar.update()
    self.widget = self.canvas.get_tk_widget()
    self.widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    self.window.title(title)
    self.window.protocol("WM_DELETE_WINDOW", self.window.withdraw)

    for (i, e) in enumerate(self.elems):
      self.figure.add_subplot(len(elems), 1, i+1)
      e.ax = self.figure.axes[i]
      if color_cycle is not None:
		e.ax.set_prop_cycle(cycler('color', color_cycle[i]))
      try: 
        e.ax.set_ylabel(e.name)
      except AttributeError:
        pass
    
    #: The reresh rate, in seconds
    self.refresh_rate = 10
    self._auto_refresh = False

  def plot_refresh(self, **kwargs):
    """Add all new data to the plotting areas."""
    with interactive(False):
      for e in self.elems:
        e.plot(ax=e.ax, **kwargs)

  def _plot_auto_refresh(self): #, auto=None):
    """
    Automatically update the display with newly acquired data.
    
    :param auto: None or bool:
                 - None: use self._auto_refresh
                 - True: start auto refresh
                 - False: stop auto refresh
    The refresh rate is specified by :attr:`refresh_rate`
    """
    self.plot_refresh()
    #if auto is not None:
    #  self._auto_refresh = auto
    if self._auto_refresh:
      self._after_id = self.window.after(self.refresh_rate*1000, self._plot_auto_refresh)

  @property
  def auto_refresh(self):
    return self._auto_refresh
    
  @auto_refresh.setter
  def auto_refresh(self, b):
    """Set to True to start the autorefresh, False to stop."""
    if b is True and not self._auto_refresh: # start refresh only if not running already
      self._auto_refresh = True
      self._plot_auto_refresh()
    elif not b and self._auto_refresh:
      self._auto_refresh = False
      self.window.after_cancel(self._after_id)
      
  def share_xlim(self):
    xlim = self.figure.axes[0].get_xlim()
    for ax in self.figure.axes[1:]:
      ax.set_xlim(xlim)
      self.plot_refresh()


def plot_time(time, data, ax=None, hours_interval=4, color_cycle='bgrcmyk'):
	"""Returns a plot of *data* vs *time*, with the time axis nicely formatted.

	:param data: the data to plot (1D array)
	:type  data: array-like
	:param time: timestamp for each element of *data* (as returned by :func:`time.time`)
	:param fig: a matplotlib Figure object. If None, create one.
	:param hours_interval: time axis tick interval, in hours.
	:type  hours_interval: float
	"""
	# see example code of the matplotlib.dates module at
	# http://matplotlib.org/examples/pylab_examples/date_demo1.html
	# http://stackoverflow.com/questions/5498510/creating-graph-with-date-and-time-in-axis-labels-with-matplotlib
	epoch = time
	temp = data
	if ax is None:
		(fig, ax) = plt.subplots()
	else:
		fig = ax.figure
	#ax.set_prop_cycle(cycler('color', color_cycle))
	fds = mdates.date2num(map(datetime.datetime.fromtimestamp, epoch))
	ax.plot(fds, temp)
	ax.xaxis.set_major_locator(mdates.HourLocator(interval=hours_interval))
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
	plt.xticks(rotation=35)
	plt.subplots_adjust(bottom=.18)
	fig.canvas.show()
	return fig
