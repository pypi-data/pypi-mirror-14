""":mod:`Tkinter` virtual keypad for motion devices.

This is part of the :mod:`microscopy` package.

The devices must conform to the interface defined in :class:`hal.Actuator`.

:Example:

To create a keypad for three axes X, Y and Z, 
controlled by PageUp/PageDown, Up/Down and Left/Right respectively:

>>> kp = keypad.Keypad(((z, ('Prior', 'Next')), 
                        (x, ('Up', 'Down')), 
                        (y, ('Left', 'Right'))), 
                       title='XYZ')
                       
Pressing a key will make the device move until the key is released.
Pressing Shift+key at the same time will make an incremental step.
Pressing Ctlr+key will increase or decrese the step size.
Arbitrary numbers of axes are supported.

.. Warning::
   Key repeat for the control keys will be disabled while the widget has focus.
   This requires that the module variable :data:`X_KEY_CODES` knows the correspondance
   between Tkinter key names and the X server keycodes (see Tip below).
   
.. Tip::
   - http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html
     for the Tkinter key names.
   - http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-handlers.html
     for the how to handle key modifiers (shift, control etc.).
   - Use the ``xev`` utility to figure out the X server key codes.

(c) Guillaume Lepert, November 2015

------------------------------------------
"""

import Tkinter as tk
from subprocess import call
from matplotlib.cbook import Stack
import time

#: X server key codes for enabling/disabling key repeats (as returned by xev)
X_KEY_CODES = {
  'Left': 113, 'Right': 114,
  'Up': 111, 'Down': 116,
  'Prior': 112, 'Next': 117,
  'KP_4': 83, 'KP_6': 85,
  'KP_8': 80, 'KP_2': 88}

# tkinter special key modifiers:
#KEY_MODS = {
  #0x0001: 'Shift',
  #0x0002: 'Caps Lock',
  #0x0004: 'Control',
  #0x0008: 'Left-hand Alt',
  #0X0010: 'Num Lock',
  #0x0080: 'Right-hand Alt',
  #0x0100: 'Mouse button 1',
  #0x0200: 'Mouse button 2',
  #0x0400: 'Mouse button 3'}

#: Tkinter key modifier masks (see http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-handlers.html)
KEY_MODS = {
  'Shift':     0x001,
  'Caps_Lock': 0x002,
  'Control':   0x004,
  'Alt_L':     0x008,
  'Num_Lock':  0x010,
  'Alt_R':     0x080,
  'Mouse_1':   0x100,
  'Mouse_2':   0x200,
  'Mouse_3':   0x400}

# Not in use. Is it worth pursuing?
def check_key_modifier(event_state, modifiers):
  if isinstance(modifiers, str):
    modifiers = (modifiers, )
  mods = 0
  for m in modifiers:
    mods |= KEY_MODS[m]    
  return event_state & mods > 0

#event.state >> KEY_MODS['Shift']

#class KeyMods(object):
  #Shift = 1
  #Caps_Lock = 2
  #Control = 3
  #Alt_L = 4
  #Num_Lock = 5
  #Alt_R = 6
  #Mouse_1 = 7
  #Mouse_2 = 8
  #Mouse_3 = 9
  
  #def check(self, state, mod):
    #if 
    #return state >> mod

class Keypad(object):
  """Tkinter virtual keypad for motion devices."""  
  def __init__(self, axes, master=None, title=''):
    """
    :param axes: list of :class:`hal.Actuator` objects.
    :param master: a Tkinter object.
                   The keypad will be created as a :class:`Tkinter.Toplevel`
                   object. If no master is provided, a new :class:`Tkinter.Tk` instance 
                   is started
    :param title: the window title.
    """
    self.root = tk.Tk() if master is None else tk.Toplevel(master)
    
    tab = max([len(axis.name) for (axis, keys) in axes])
    self.n_axes = len(axes)
    
    # set up text widget
    self.root.geometry('450x%d' % (20*(self.n_axes*2+4)))
    self.text = tk.Text(self.root, background='black', foreground='white', font=('Monospace', 12))
    self.text.pack()
    self.root.title(title)    
    for i in range(self.n_axes*3):
      self.text.insert('1.0', '\n')

    # Attach axes and print position/step size
    self.axes = []
    for (index, (axis, keys)) in enumerate(axes):
      self.text.insert('%d.0' % (self.n_axes*2+2+index), axis.name + ':           ')
      self.text.insert('%d.%d' % (self.n_axes*2+2+index, tab+2), '%s/%s                ' %(keys[0], keys[1])) 
      setattr(self, axis.name, KeypadAxis(axis, keys, self.text, 2*index+1, tab+1, axis.dir))
      self.axes.append(getattr(self, axis.name))

    # print instructions
    self.text.delete('%d.%d' % (self.n_axes*2+2, 18), '%d.0-1c' % (self.n_axes*2+2+1))
    self.text.insert('%d.%d' % (self.n_axes*2+2, 18), '| +Shift: step motion.')
    self.text.delete('%d.%d' % (self.n_axes*2+3, 18), '%d.0-1c' % (self.n_axes*2+3+1))
    self.text.insert('%d.%d' % (self.n_axes*2+3, 18), '| +Ctrl: change step size.')
    
    # Bindings to delete keystrokes (emulates a text-only widget) 
    # and disable key repeat when widget has focus 
    self.root.bind('<Key>', self.read_only)
    self.root.bind('<FocusIn>', self.disable_key_repeat)
    self.root.bind('<FocusOut>', self.enable_key_repeat)
    
    self.update_rate = 2

  def disable_key_repeat(self, event):
    """Disable key repeats for all actuator control keys.""" 
    for axis in self.axes:
      axis.disable_key_repeat()

  def enable_key_repeat(self, event):
    """Enable key repeats for all actuator control keys."""
    for axis in self.axes:
      axis.enable_key_repeat()

  def read_only(self, event):
    """Emulates a read-only text widget by immediately deleting all input characters."""
    #print event.char
    if event.char is not '':
      self.text.delete('insert-1c')
      
  def update_pos(self):
    for ax in self.axes:
      ax.print_pos()
    self.pos_update_id = self.text.after(self.update_rate, self.update_pos)


class KeypadAxis(object):
  """Represent individual actuators within a :class:`Keypad` instance.""" 
  def __init__(self, axis, keys, widget, line, tab=10, dir=1):
    """
    :param axis: 
    :type axis: :class:`hal.Actuator`
    :param keys: the two controlling keys (see http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html
                 for info about Tkinter key identifiers)
    :param widget: Tkinter widget where the axis should be attached.
                   (normally :attr:`Keypad.text`)
    :param line: in the text widget, number of the line where the 
                 axis position should be printed.
    :type  line: int
    :param tab: number of characters reserved for printing the axis name
    :type  tab: int
    :param dir: The requested motion will be multiplied by this number.
                Most useful to swap the direction of motion if the actuator
                is set up in such a way that it goes up when it is expected 
                to go down.
    :type  dir: float
    """
    self.axis = axis
    self.keys = keys
    self.title = axis.name
    self.text = widget
    self.line = line # print widget info on this line
    self.tab = tab
    self.t_tab = ''.join([' ' for i in range(self.tab)])
    widget.bind('<KeyPress-%s>' % keys[0], self.move_up)
    widget.bind('<KeyPress-%s>' % keys[1], self.move_down)
    widget.bind('<KeyRelease-%s>' % keys[0], self.stop)
    widget.bind('<KeyRelease-%s>' % keys[1], self.stop)
    self.dir = dir
    
    #self.rate = 0 # drift rate, in um/h
    #self.dt = 10  # drift compensation update perdiod, in s
    
    #: Position update rate, in seconds.  
    self.update_rate = 2
    
    # Step size is implemented as a matplotlib cookbook Stack.
    # Use Actuator property (if it exists) to scale the default list.
    try:
      step_scaling = self.axis.step_scaling
    except AttributeError:
      step_scaling = 1
    self.step = Stack()
    for s in (1, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001):
      self.step.push(step_scaling * s)

    #self.update_pos()
    self.print_pos()
    self.print_step()

  def enable_key_repeat(self):
    """Enable key repeats for the control keys.""" 
    if self.axis.disable_key_repeat:
      call('xset r %d; xset r %d' % (X_KEY_CODES[self.keys[0]], X_KEY_CODES[self.keys[1]]), shell=True)

  def disable_key_repeat(self):
    """Disable key repeats for the control keys.""" 
    if self.axis.disable_key_repeat:
      call('xset -r %d; xset -r %d' % (X_KEY_CODES[self.keys[0]], X_KEY_CODES[self.keys[1]]), shell=True)

  def print_pos(self):
    """Print the current position on text widget."""
    self.text.delete(str(self.line)+'.0', str(self.line+1)+'.0-1c')
    self.text.insert(str(self.line)+'.0', self.title + self.t_tab)
    self.text.insert('%d.%d' % (self.line, self.tab), '| Position: %f %s' % (self.axis.position(), self.axis.unit))
    
  def print_step(self):
    """Print current step size on text widget."""
    self.text.delete(str(self.line+1)+'.0', str(self.line+2)+'.0-1c')
    self.text.insert(str(self.line+1)+'.0', self.t_tab)
    self.text.insert('%d.%d' % (self.line+1, self.tab), '| Step size: %g %s' %(self.step(), self.axis.unit))
  
  def update_pos(self):
    """Update the axis position at regular interval."""
    #def func():
    #  self.print_pos()
    self.print_pos()
    self.axis.pos_after_id = self.text.after(self.update_rate, self.update_pos)

  def move_up(self, event):
    """Returns a event binding function that moves towards the positive direction."""
    if event.state & KEY_MODS['Shift']:
      self.axis.move_by(+self.dir * self.step())
    elif event.state & KEY_MODS['Control'] > 0:
      self.step.back()
      self.print_step()
    else:
      try:
        self.axis.move(+self.dir)
      except NotImplementedError:
        self.axis.move_by(+self.dir * self.step())
    self.print_pos()

  def move_down(self, event):
    """Returns a event binding function that moves towards the negative direction."""
    if event.state & KEY_MODS['Shift']:
      self.axis.move_by(- self.dir * self.step())
    elif event.state & KEY_MODS['Control'] > 0:
      self.step.forward()
      self.print_step()
    else:
      try:
        self.axis.move(-self.dir)
      except NotImplementedError:
        self.axis.move_by(- self.dir * self.step())
    self.print_pos()

  def stop(self, event):
    """Returns a event binding function that stops motion on the specified axis."""
    if not event.state & KEY_MODS['Shift']:   # no need to call stop() on step motion
      self.axis.stop()
    while self.axis.moving():
      time.sleep(0.05)
    self.print_pos()

  def compensate_drift(self):
    
    self.text.after(dt*1000, self.compensate_drift)


class Drift(object):
	def __init__(self, ax, rate, dt):
		self.ax = ax  # KeypadAxis
		self.rate = rate # in mm/s
		self.dt = dt
		self.min_motion = 0.0002 # 200nm 

	def update(self):
		t = time.time()
		dx = self.rate * (t - self.t)
		if abs(dx) > self.min_motion:
			self.ax.move_by(dx)
			self.t = t
		self.after_id = self.ax.text.after(self.dt*1000, self.update)

	def stop():
		self.ax.text.after_cancel(self.after_id)

	def start():
		self.t = time.time()
		self.after_id = self.ax.text.after(self.dt*1000, self.update)
