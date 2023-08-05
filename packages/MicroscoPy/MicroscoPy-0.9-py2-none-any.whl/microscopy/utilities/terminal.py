"""
Simple utilities to manipulate the terminal window and its content.
"""

import sys

def set_title(title):
    """Set the interpreter's terminal window or tab title."""
    sys.stdout.write("\x1b]2;%s\x07" % title)

#: Code to print to the console to erase the current line.
ERASE_LINE = '\x1b[2K'

def printr(text):
    """Print to stdout, overwriting current line."""
    sys.stdout.write("\r" + ERASE_LINE + text)
    sys.stdout.flush()
