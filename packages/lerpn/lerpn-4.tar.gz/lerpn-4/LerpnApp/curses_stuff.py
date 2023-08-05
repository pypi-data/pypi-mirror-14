"""Curses utilities.
"""

import curses

# Reference of nonprintables to printable names
KEY_TO_NAME = {
    "\x7f": "[0x7f]",
    "\x08": "[0x08]",
    curses.KEY_BACKSPACE: "[bksp]",
    "\r": "[CR]",
    "\n": "[LF]",
    curses.KEY_ENTER: "[enter]",
    curses.KEY_UP: "[up]",
    curses.KEY_DOWN: "[down]",
    curses.KEY_LEFT: "[left]",
    curses.KEY_RIGHT: "[right]",
    curses.KEY_PPAGE: "[pgup]",
    curses.KEY_NPAGE: "[pgdn]",
    curses.KEY_HOME: "[home]",
    curses.KEY_END: "[end]",
}

# pylint: disable=too-many-instance-attributes
class CursesScrollBox(object):
    """Displays some text in a scroll box."""

    def __init__(self, parent, width, height):
        """Initialize.

        @param width - desired width: positive for absolute width, negative
                    for margin around window edge
        @param height - desired height: positive for absolute height,
                    negative for margin around window edge
        """
        self.parent = parent
        self.width = width
        self.height = height
        self.title = ""
        self.text = ""
        self.vpos = 0
        self.hpos = 0

        self._width = None
        self._height = None
        self._xoff = None
        self._yoff = None

    def set_text(self, text):
        """Set the text displayed in the scroll box. This can be a string, which
        will be split into lines, or a list of lines"""

        # Split the text?
        if isinstance(text, str):
            text_split = text.split("\n")
        elif isinstance(text, list):
            text_split = text
        else:
            raise TypeError("Text must be list or str")

        # Tab-expand the text so it horizontally scrolls nicely
        lines = []
        for line in text_split:
            new_line = []
            col = 0
            for char in line:
                col += 1
                if char == "\t":
                    n_spaces = 8 - (col - 1) % 8
                    new_line.extend([" "] * n_spaces)
                    col += n_spaces - 1
                else:
                    new_line.append(char)
            lines.append(''.join(new_line))
        self.text = lines

    def set_title(self, title):
        """Set the title to be displayed at the top."""
        self.title = title

    def show(self):
        """
        Display the window on the curses display
        """

        curses.curs_set(0)
        curses.doupdate()
        self._set_dimensions(None)
        window = curses.newwin(self._height, self._width, self._yoff, self._xoff)
        window.keypad(1)

        cycle = True
        while cycle:
            self._draw(window)
            cycle = self._nav(window)

        curses.curs_set(1)


    def _set_dimensions(self, window):
        """
        Configure _width, _height, _xoff, _yoff from screen dimensions.
        """
        lines, cols = self.parent.getmaxyx()

        if self.width < 0:
            self._width = cols + self.width
        else:
            self._width = self.width
        if self.height < 0:
            self._height = lines + self.height
        else:
            self._height = self.height
        self._xoff = cols // 2 - self._width // 2
        self._yoff = lines // 2 - self._height // 2

        if window is not None:
            window.resize(self._height, self._width)
            try:
                window.move(self._yoff, self._xoff)
            except curses.error:
                pass

    def _clamp_offsets(self):
        """
        Clamp vpos and hpos into the display range
        """

        longest_line = max(len(i) for i in self.text)
        yscroll_limit = max(0, len(self.text) - self._height // 2)
        xscroll_limit = max(0, longest_line - self._width // 2)

        self.vpos = max(0, self.vpos)
        self.vpos = min(self.vpos, yscroll_limit)

        self.hpos = max(0, self.hpos)
        self.hpos = min(self.hpos, xscroll_limit)


    def _draw(self, window):
        """
        Draw the scroll box.
        """

        window.clear()
        try:
            window.addstr(1, 2, self.title)
        except curses.error:
            pass

        self._clamp_offsets()

        view_lines = self.text[self.vpos:self.vpos+self._height - 4]

        try:
            for idx, line in enumerate(view_lines):
                window.addstr(idx + 3, 2, line[self.hpos:self._width - 2 + self.hpos])
        except curses.error:
            pass

        try:
            if self.vpos > 0:
                window.addstr(2, self._width - 3, "+")
            if self.vpos + self._height < len(self.text) + 4:
                window.addstr(self._height - 2, self._width - 3, "+")
        except curses.error:
            pass

        window.border()

    def _nav(self, window):
        """Handle the navigation keys. Return True to continue for another cycle,
        or False to exit."""

        try:
            key = window.getch()
        except KeyboardInterrupt:
            key = None

        if key in (curses.KEY_UP, ord('k')):
            self.vpos -= 1
        elif key in (curses.KEY_DOWN, ord('j')):
            self.vpos += 1
        elif key in (curses.KEY_LEFT, ord('h')):
            self.hpos -= 5
        elif key in (curses.KEY_RIGHT, ord('l')):
            self.hpos += 5

        elif key == curses.KEY_PPAGE:
            self.vpos -= (self._height // 2)
        elif key == curses.KEY_NPAGE:
            self.vpos += (self._height // 2)

        elif key == curses.KEY_HOME:
            self.vpos = 0
        elif key == curses.KEY_END:
            self.vpos = len(self.text)

        elif key == curses.KEY_RESIZE:
            self._set_dimensions(window)
            self.parent.clear()
            self.parent.refresh()

        else:
            return False

        return True

def draw_text(window, lines, offset, xoffset, padding):
    """Draw a list of text lines onto the window.

    @param window - curses window
    @param lines - list of lines
    @param offset - line number to start at. Negative to start at bottom
    @param xoffset - horizontal offset
    @param padding - distance from other end at which to stop
    """

    w_height, w_width = window.getmaxyx()
    lines_wclamp = [i[:w_width] for i in lines]
    lines_hwclamp = lines_wclamp[:(w_height - abs(offset) - padding)]

    for idx, line in enumerate(lines_hwclamp):
        if offset < 0:
            yoffset = w_height - idx + offset - 1
        else:
            yoffset = idx + offset
        window.addstr(yoffset, xoffset, line)

def draw_vline(window, xpos, ystart, height):
    """Draw a vertical line onto the window

    @param window - curses window
    @param xpos - x coordinate (pos from left, neg from right)
    @param ystart - y coordinate (pos from top, neg from bottom)
    @param height - line height (pos absolute, neg relative to window height)
    """

    w_height, w_width = window.getmaxyx()

    xpos %= w_width
    height %= w_height

    if ystart < 0:
        ystart = w_height - height + ystart

    # pylint: disable=no-member
    # ACS_VLINE is populated at load
    window.vline(ystart, xpos, curses.ACS_VLINE, height)

def draw_textline(window, line, yoff, xoff, clearline=False):
    """Draw a line of text onto the window

    @param window - curses window
    @param line - line of text
    @param yoff - y offset, pos from top, neg from bottom
    @param xoff - x offset, pos from left, neg from right
    @param clearline - True to clear the rest of the line
    @return True on success (can fail if yoff/xoff is invalid)
    """

    w_height, w_width = window.getmaxyx()

    yoff %= w_height
    xoff %= w_width

    try:
        window.move(yoff, xoff)
    except curses.error:
        return False

    window.addstr(line)
    if clearline:
        window.clrtoeol()

    return True

def getkey(window):
    """Get a keypress from the window.

    @return keycode, character  - character will be None if there is no match
    """

    key = window.getch()
    try:
        char = chr(key)
    except ValueError:
        char = None
    return key, char

def draw_reverse_line(window, line, yoff):
    """Draw a line of text (like a status bar) in reverse video, filling in all
    the way across the window."""

    _, w = window.getmaxyx()

    window.addstr(yoff, 0, line, curses.A_REVERSE)
    window.addstr(yoff, len(line), " " * (w - len(line)), curses.A_REVERSE)
