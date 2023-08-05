"""Code dealing directly with the text user interface.

Currently this ties in heavily with curses. Eventually, curses will be
abstracted out.
"""

import curses
import os
import string
import sys
from .commands import SINGLE_KEY_COMMANDS, COMMANDS
from . import env, nums, curses_stuff

def format_stack(stack, recurse=True, firstcall=True):
    """Converts a single stack to a list of lines of text.
    If the stack has a parent and recurse is true, draw the parents
    as well.

    Also returns a list of x coordinates where dividers should be
    drawn.
    """

    lines = []

    for i, item in enumerate(stack):
        formatted = env.FORMAT.format(item)
        stack_n = i

        margin = ("%3d  " % stack_n) if firstcall else "| "

        if hasattr(item, "tag"):
            text = "%20s : %s" % (formatted, item.tag)
        else:
            text = "%20s" % formatted

        lines.append(margin + text)

    lines = lines[::-1]

    if recurse and stack.parent is not None:
        parent_lines, parent_dividers = format_stack(stack.parent, firstcall=False)

        # Line up lines at the bottom
        lines.extend([""] * (len(parent_lines) - len(lines)))
        parent_lines.extend([""] * (len(lines) - len(parent_lines)))

        # Concatenate
        concat_len = 35 if firstcall else 15

        joined_lines = []
        for i, j in zip(lines, parent_lines):
            if len(i) < concat_len:
                i += " " * (concat_len - len(i))
            i = i[:concat_len]
            joined_lines.append(i + j)
        return joined_lines, [concat_len] + [i + concat_len for i in parent_dividers]

    return lines, []


def draw_stack(stack):
    """Draw the stack.
    """

    lines, dividers = format_stack(stack)

    curses_stuff.draw_text(env.STDSCR, lines, offset=-1, xoffset=0, padding=2)

    for xoff in dividers:
        curses_stuff.draw_vline(env.STDSCR, xoff, 2, -1)

    curses.doupdate()

def get_single_key_command(key):
    """
    Return a single-key command for the key, or None.
    """
    if key > 127:
        lookup_key = key
    else:
        try:
            lookup_key = chr(key)
        except ValueError:
            lookup_key = key
    return SINGLE_KEY_COMMANDS.get(lookup_key, None)

def do_command(stack, cmd, arg):
    """ Execute the command on the stack in an exception wrapper.

    Returns None if no exception, or sys.exc_info() if there was one.
    """

    # pylint: disable=broad-except
    try:
        stack.undopush()
        rtn = cmd(stack, arg)
    except Exception:
        stack.undo()
        return sys.exc_info()
    else:
        assert rtn is None
        return None

ENTER_KEYS = [curses.KEY_ENTER, 10, 13]
BACKSPACE_KEYS = [curses.KEY_BACKSPACE, 127, 8]

def do_edit(key, strbuf):
    """
    Line-edit.
    Returns edit_type, new_strbuf
        edit_type: one of "BACKSPACE", "ENTER", None
    """

    if key in BACKSPACE_KEYS:
        return "BACKSPACE", strbuf[:-1]

    if key in ENTER_KEYS:
        return "ENTER", strbuf

    try:
        c = chr(key)
    except ValueError:
        c = ""

    return None, strbuf + c

def do_exit(stack, extra_text=None):
    """Perform the exit action.

    In this case, the stack is formatted to stdout,
    then we exit.
    """

    def exit_helper():
        """Format extra text and the stack to stdout."""
        if "LERPN_TEST_PRINT" in os.environ:
            print("BEGIN_PRINT")
            if extra_text is not None:
                print(extra_text)
            for item in stack:
                natural = nums.NaturalMode.format(item)
                print("%s" % (natural))

    # Using atexit allows us to register the function to be called after
    # curses.wrapper() performs cleanup
    import atexit
    atexit.register(exit_helper)

    sys.exit(0)

class Prompt(object):
    """State machine for user input prompt"""

    def __init__(self):
        self.state = self.state_firstchar
        self.strbuf = ""
        self.actions = []
        self.key = None
        self.char = None
        self.edit_type = None
        self.exception = None

    def draw_statusbar(self):
        """Display a reverse-video statusbar at the top of the screen"""
        if self.exception is not None:
            env.LAST_ERROR = self.exception
            err_text = "ERROR: %s" % str(self.exception[1])
            self.exception = None
            curses_stuff.draw_reverse_line(env.STDSCR, err_text, 0)
        else:
            curses_stuff.draw_reverse_line(env.STDSCR, self.get_status_text(), 0)

    def get_status_text(self):
        """Return the text to be displayed in the status bar. Does not
        handle error messages."""
        return env.FORMAT.name()

    def loop(self, stack):
        """Displays the prompt and executes a user action from it.
        stack:  buffer current UndoStack
        """
        self.state = self.state_firstchar
        self.strbuf = ""

        self.draw_statusbar()
        while self.state is not None:
            self.cycle(stack)

    def cycle(self, stack):
        """Perform one cycle of the state machine. Not generally called externally."""
        self.actions = []
        self.exception = None

        if self.do_io(stack):
            return

        if self.state is not None:
            self.state()

        self.do_actions(stack)

    def do_io(self, stack):
        """Handle input/output. Returns True if this cycle should be skipped."""

        draw_stack(stack)
        prompt_line = "? " + self.strbuf
        curses_stuff.draw_textline(env.STDSCR, prompt_line, -1, 0, True)
        curses.doupdate()

        self.key, self.char = curses_stuff.getkey(env.STDSCR)

        if self.key == curses.KEY_F5:
            self.actions.append(('push', str(self.state)))
        elif self.key == curses.KEY_RESIZE:
            env.STDSCR.clear()
            self.draw_statusbar()
            return True

        self.edit_type, self.strbuf = do_edit(self.key, self.strbuf)
        return False

    def do_actions(self, stack):
        """Execute any actions accumulated over a machine cycle."""
        for cmd, arg in self.actions:
            if cmd == "parse":
                # pylint: disable=broad-except
                try:
                    parsed = nums.num_parser(arg)
                except Exception:
                    self.exception = sys.exc_info()
                else:
                    stack.undopush()
                    stack.append(parsed)
            elif cmd == "push":
                stack.append(arg)
            elif cmd == "undopush":
                stack.undopush()
            else:
                self.exception = do_command(stack, cmd, arg)


    def state_firstchar(self):
        """State 'firstchar': look at the first character typed and determine the kind of input."""
        # Try single-key commands first
        cmd = get_single_key_command(self.key)
        if cmd is not None:
            self.actions.append((cmd, None))
            self.state = None

        elif self.char is None:
            self.state = self.state_firstchar

        elif self.char in string.digits + "_.":
            self.state = self.state_numeric

        elif self.char == "'":
            self.state = self.state_command

        elif self.char == '"':
            self.state = self.state_string

        else:
            self.strbuf = ""

    def state_numeric(self):
        """State 'numeric': number entry"""

        # When typing a number, it is sometimes necessary to forbid
        # the interpretation of single-key commands:

        cmdblock_tag = ('"' in self.strbuf)
        cmdblock_sci = (self.strbuf[-2:-1] in "ej")
        cmdblock_hex = (self.strbuf[0:2] == "0h" and
                        self.char is not None and
                        self.char in "abcdef")

        cmdblock = cmdblock_tag or cmdblock_sci or cmdblock_hex

        if cmdblock or self.edit_type in ("BACKSPACE", "ENTER"):
            cmd = None
        else:
            cmd = get_single_key_command(self.key)

        if not self.strbuf:
            self.state = None

        elif self.char == "'":
            self.state = self.state_command
            self.actions.append(("parse", self.strbuf[:-1]))
            self.strbuf = "'"

        elif self.edit_type == "ENTER":
            self.state = None
            self.actions.append(("parse", self.strbuf))
            self.strbuf = ""

        elif cmd is not None:
            self.state = None
            self.actions.append(("parse", self.strbuf[:-1]))
            self.actions.append((cmd, None))
            self.strbuf = ""

    def state_command(self):
        """State 'command': named command entry"""
        if self.edit_type == "ENTER":
            cmdname, _, arg = self.strbuf.partition(" ")
            cmd = COMMANDS.get(cmdname, None)
            if cmd is not None:
                self.actions.append((cmd, arg))
            elif len(self.strbuf):
                try:
                    raise KeyError("Command not found: %s" % self.strbuf)
                except KeyError:
                    self.exception = sys.exc_info()

            self.state = None

        if not self.strbuf:
            self.state = None

    def state_string(self):
        """State 'string': string entry"""
        if not self.strbuf:
            self.state = None
        elif self.edit_type == "ENTER":
            self.actions.append(("push", self.strbuf.lstrip('"')))
            self.state = None

