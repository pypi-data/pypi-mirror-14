#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             ansi.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       02/23/2016
#

"""
ext_pylib.terminal.ansi
~~~~~~~~~~~~~~~~~~~~~~~

Ansi escape codes and functions.

Most of these functions write their results directly to standard out unless
passed get_string=True, in which case they just return the escape as a string.
"""

from sys import stdout


# GENERAL ASCII CODES

NULL = '\00' # Null character
BEL = '\007' # Terminal Bell
BS = '\010'  # Backspace
HT = '\011'  # Horizontal Tab
LF = '\012'  # Linefeed (newline)
VT = '\013'  # Vertical Tab
FF = '\014'  # Formfeed (or NP: new page)
CR = '\015'  # Carriage Return
ESC = '\033' # Escape character
DEL = '\177' # Delete character


# ESCAPE SEQUENCES

CSI = '\033['
OSC = '\033]'
DELIMITER = ';'

def attributes(*args):
    """Returns multiple attributes concatenated and separated by DELIMITER."""
    return reduce(lambda a, b: str(a) + DELIMITER + str(b), args)

def escape(escape, get_string):
    """Prints an escape sequence or returns it as a string."""
    if get_string:
        return escape
    stdout.write(escape)
    stdout.flush()


    ## Cursor Handling ##

def cursor_hide(get_string=False):
    """Hides the cursor."""
    return escape(ansi.CSI + '?25l', get_string)

def cursor_show(get_string=False):
    """Shows the cursor."""
    return escape(ansi.CSI + '?25h', get_string)

def cursor_up(n=1, get_string=False):
    """Moves your cursor up 'n' cells."""
    return escape(CSI + str(n) + 'A', get_string)

def cursor_down(n=1, get_string=False):
    """Moves your cursor down 'n' cells."""
    return escape(CSI + str(n) + 'B', get_string)

def cursor_right(n=1, get_string=False):
    """Moves your cursor right (forward) 'n' cells."""
    return escape(CSI + str(n) + 'C', get_string)

def cursor_left(n=1, get_string=False):
    """Moves your cursor left (backward) 'n' cells."""
    return escape(CSI + str(n) + 'D', get_string)

def cursor_next_line(n=1, get_string=False):
    """Moves your cursor to the next 'n' lines."""
    return escape(CSI + str(n) + 'F', get_string)

def cursor_previous_line(n=1, get_string=False):
    """Moves your cursor to the previous 'n' lines."""
    return escape(CSI + str(n) + 'G', get_string)

def cursor_horizontal_absolute(n=1, get_string=False):
    """Moves your cursor to the 'n' column."""
    return escape(CSI + str(n) + 'G', get_string)

def cursor_position(x=0, y=0, get_string=False):
    """Moves youescape = cursor to position (x, y).
    NOTE: This assumes starting at (0, 0) which is different than the ANSI
    standard; it also assumes (x, y) and not (y, x) per ANSI standard."""
    return escape(CSI + attributes(y+1, x+1) + 'f', get_string)

def cursor_save(get_string=False):
    """Save the current cursor position."""
    return escape(CSI + 's', get_string)

def cursor_restore(get_string=False):
    """Restore the last saved cursor position."""
    return escape(CSI + 'u', get_string)

def attributes_save(get_string=False):
    """Save the current cursor position and attributes."""
    return escape(ESC + '7', get_string)

def attributes_restore(get_string=False):
    """Restore the last saved cursor position and attributes."""
    return escape(ESC + '8', get_string)

def get_cursor_pos():
    """Returns a tuple of (x, y) of current cursor position.
    Note this follows conventional (x, y) order and starts with (0, 0) and not
    the order according to the ANSI standard."""
    QCU = CSI + '6n'  # Query cursor position (to stdin)
    RCU = CSI + '{0};{1}R' # Reports Cursor positon (result from above query
                           # Reports as <ESC>[{row};{column}R
                           # Note that this is backwards order


    ## Clearing the screen ##

def clear(get_string=False):
    """Clears the entire screen."""
    return escape(CSI + '2J', get_string)

def clear_down(get_string=False):
    """Clears the screen from the cursor down."""
    return escape(CSI + '0J', get_string)

def clear_up(get_string=False):
    """Clears the screen from the cursor down."""
    return escape(CSI + '1J', get_string)

def clear_line(get_string=False):
    """Clears the entire line."""
    return escape(CSI + '2K', get_string)

def clear_line_forward(get_string=False):
    """Clears the entire line."""
    return escape(CSI + '0K', get_string)

def clear_line_back(get_string=False):
    """Clears the entire line."""
    return escape(CSI + '1K', get_string)

def reset(get_string=False):
    """Clears the entire screen and places cursor at top left corner."""
    return escape(clear(get_string=True) + cursor_position(0, 0, get_string=True), get_string)


    ## Terminal Settings ##

def reset_terminal(get_string=False):
    """Resets the terminal."""
    return escape(ESC + 'c', get_string)

def enable_line_wrap(get_string=False):
    """Enables line wrapping."""
    return escape(CSI + '7h', get_string)

def disable_line_wrap(get_string=False):
    """Disables line wrapping."""
    return escape(CSI + '7h', get_string)

def set_scroll_all(get_string=False):
    """Enable scrolling for the entire screen."""
    return escape(CSI + 'r', get_string)

def set_scroll(start_row, end_row, get_string=False):
    """Enable scrolling from start_row to end_row."""
    return escape(CSI + attributes(start_row, end_row) + 'r', get_string)

def scroll_up(get_string=False):
    """Scrolls up."""
    return escape(ESC + 'D', get_string)

def scroll_down(get_string=False):
    """Scrolls down."""
    return escape(ESC + 'M', get_string)


    ## SGR Escape Sequences ##

def sgr(*args):
    """Returns an SGR (Select Graphic Rendition) escape sequence given one or
    more attributes."""
    return CSI + attributes(*args) + 'm'

RESET = '0'
BOLD = '1'
UNDERLINE = '4'
BLINK = '5'
RBLINK = '6'
REVERSE = '7'
CONCEAL = '8'

BLACK = '30'
RED = '31'
GREEN = '32'
YELLOW = '33'
BLUE = '34'
MAGENTA = '35'
CYAN = '36'
WHITE = '37'
EXTENDED = '38'

BG_BLACK = '40'
BG_RED = '41'
BG_GREEN = '42'
BG_YELLOW = '43'
BG_BLUE = '44'
BG_MAGENTA = '45'
BG_CYAN = '46'
BG_WHITE = '47'
BG_EXTENDED = '48'
