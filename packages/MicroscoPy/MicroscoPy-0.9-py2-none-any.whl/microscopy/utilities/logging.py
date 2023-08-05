import sys
from ScrolledText import ScrolledText
import logging


class LogWindow(logging.Handler):
  """Creates a Tkinter scrollable text window in wish to write the log."""
  def __init__(self, master=None):
    super(LogWindow, self).__init__(self)
    self.window = Tkinter.TopLevel(master)
    self.text = ScrolledText(self.window)
    self.text.pack()
    
  def emit(self, record, newline=True, overwrite=False):
    """
    newline=True: write record on new line, otherwise try overwriting the last entry
    overwrite=False: force next record to start a new line."""
    r = '\n' if (newline or not self.allow_overwrite) else '\r'
    self.text.insert(Tkinter.END, r + record)
    self.allow_overwrite = overwrite



