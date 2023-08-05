"""All the calculator commands.

This file contains the commands made available to the user. Single-key
commands are in the SINGLE_KEY_COMMANDS OrderedDict, and full-name
commands are in the COMMANDS OrderedDict.
"""

# pylint: disable=missing-docstring,unused-argument

import cmath
import collections
import curses
import math
import os
import subprocess
import sys
import traceback

from . import nums, env, curses_stuff
from .extramath import *

###############################################################################
# COMMAND GENERATORS
#
# Use these to generate common cases, rather than implementing from scratch.

def BINARY(func, docstring=None):
    """Create a binary operator from a lambda function."""
    def cmd(stack, arg):
        y_val = stack.pop()
        x_val = stack.pop()
        stack.append(func(x_val, y_val))

    cmd.__doc__ = docstring or func.__doc__
    assert cmd.__doc__

    return cmd

def UNARY(func, docstring=None, autostack=True):
    """Create a unary operator from a lambda function.
    The unary operators know how to handle tagged numbers - they reapply the
    same tag after performing the operation.

    expect_stack: if True (default), automatically expand func(stack) to
    [func(i) for i in stack]. if False, pass the stack to func like any
    other number."""
    def cmd_one_value(value):
        if isinstance(value, nums.Tagged):
            newtagged = nums.Tagged(func(value.num), value.tag)
            return newtagged
        else:
            return func(value)

    def cmd_noauto(stack, arg):
        stack.append(cmd_one_value(stack.pop()))

    def cmd_auto(stack, arg):
        value = stack.pop()
        if isinstance(value, nums.UndoStack):
            newstack = nums.UndoStack([cmd_one_value(i) for i in value])
            newstack.parent = stack
            stack.append(newstack)
        else:
            stack.append(cmd_one_value(value))

    if autostack:
        cmd = cmd_auto
    else:
        cmd = cmd_noauto

    cmd.__doc__ = docstring or func.__doc__
    assert cmd.__doc__

    return cmd

def CONST(val, descr):
    """Return a command function to push a constant"""

    def cmd(stack, arg):
        stack.append(val)
    cmd.__doc__ = descr
    return cmd

###############################################################################
# COMMAND HELPERS
def untagged(num):
    """return a number without its tag, if it is tagged"""
    if isinstance(num, nums.Tagged):
        return num.num
    else:
        return num

###############################################################################
# MATH COMMANDS

def _divmod(stack, arg):
    """(y/x, y%x)"""
    x = untagged(stack.pop())
    y = untagged(stack.pop())
    stack.append(float(math.floor(y / x)))
    stack.append(y % x)

def _reim(stack, arg):
    """split into real and imaginary parts"""
    num = untagged(stack.pop())
    stack.append(num.real)
    stack.append(num.imag)

def _polar(stack, arg):
    """split into absolute value and angle"""
    num = untagged(stack.pop())
    stack.append(abs(num))
    stack.append(cmath.phase(num))

def _fcart(stack, arg):
    """make complex from Cartesian real, imag"""
    imag = untagged(stack.pop())
    real = untagged(stack.pop())

    stack.append(complex(real, imag))

def _fpolar(stack, arg):
    """make complex from polar abs val, angle(rad)"""
    angle = untagged(stack.pop())
    absval = untagged(stack.pop())

    stack.append(cmath.rect(absval, angle))

def _pvar(stack, arg):
    """population variance"""
    nest = stack.pop()
    mean = sum(nest) / float(len(nest))
    sdiff = [(i - mean) ** 2 for i in nest]
    pvar = sum(sdiff) / float(len(sdiff))
    stack.append(pvar)

def _pdev(stack, arg):
    """population std deviation"""
    _pvar(stack, arg)
    stack.append(stack.pop() ** 0.5)

def _svar(stack, arg):
    """sample variance"""
    nest = stack.pop()
    mean = sum(nest) / float(len(nest))
    sdiff = [(i - mean) ** 2 for i in nest]
    svar = sum(sdiff) / float(len(sdiff) - 1)
    stack.append(svar)

def _sdev(stack, arg):
    """sample std deviation"""
    _svar(stack, arg)
    stack.append(stack.pop() ** 0.5)

###############################################################################
# TAG COMMANDS

def _tag(stack, arg):
    """attach tag to number"""

    if arg:
        tag = arg.strip()
    else:
        tag = stack.pop()

    num = stack.pop()
    if not isinstance(tag, str):
        raise TypeError("to create tagged number, give Y: number, X: string")

    elif not isinstance(num, float) and not isinstance(num, nums.UndoStack):
        raise TypeError("to create tagged number, give Y: number, X: string ")

    stack.append(nums.Tagged(num, tag))

def _untag(stack, arg):
    """unTag"""
    stack.append(untagged(stack.pop()))

################################################################################
# STACK/SHELL COMMANDS

def _drop(stack, arg):
    """drop"""
    stack.pop()

def _dup(stack, arg, n=-1):
    """dup"""

    # @param n - which index to dup. This allows _dup to be wrapped by other
    # commands like _get and avoid some duplication.

    if n == -1:
        # pop instead of access so we get the same, consistent error message if
        # there isn't one.
        item = stack.pop(n)
        stack.append(item)
    else:
        item = stack[n]

    if isinstance(item, nums.UndoStack):
        new_stack = nums.UndoStack(item)
        new_stack.parent = stack
        stack.append(new_stack)
    elif isinstance(item, nums.Tagged) and isinstance(item.num, nums.UndoStack):
        new_stack = nums.UndoStack(item.num)
        new_stack.parent = stack
        stack.append(nums.Tagged(new_stack, item.tag))
    else:
        stack.append(item)

def _rotup(stack, arg):
    """rotate up"""
    stack.append(stack.pop(0))

def _rotdown(stack, arg):
    """rotate down"""
    stack.insert(0, stack.pop(-1))

def _pull(stack, arg):
    """move item from index to front"""
    idx = int(stack.pop())
    stack.append(stack.pop(idx))

def _push(stack, arg):
    """move item from front to index"""
    idx = int(stack.pop())
    stack.insert(idx, stack.pop())

def _undo(stack, arg):
    """undo"""
    # Drop the undopush that was done for /this/ command
    stack.replace_redo()
    stack.drop()
    stack.undo()

def _redo(stack, arg):
    """redo"""
    # Drop the undopush that was done for /this/ command
    stack.replace_redo()
    stack.drop()
    stack.redo()

def _xchg(stack, arg):
    """exchange/swap"""
    x = stack.pop()
    y = stack.pop()
    stack.append(x)
    stack.append(y)

def _get(stack, arg):
    """dup item by number"""
    stack_idx = clamp(0, int(untagged(stack.pop())), len(stack) - 1)
    _dup(stack, arg, n=stack_idx)

def _sh(stack, arg):
    """run shell command, $N = number"""
    assert arg, "argument expected!"
    newenv = dict(os.environ)
    if not stack:
        newenv["N"] = "0"
    else:
        num = untagged(stack[-1])
        if isinstance(num, float):
            newenv["N"] = "%g" % num
        elif isinstance(num, complex):
            newenv["N"] = "%g+%gj" %(num.real, num.imag)

    try:
        proc = subprocess.Popen(
            arg, shell=True, env=newenv, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        data = proc.stdout.read()
        proc.wait()
    except KeyboardInterrupt:
        data = b""

    if sys.version_info >= (3, 0):
        data = data.decode("utf8")

    match = nums.FLOAT_RE.search(data)
    if match is not None:
        try:
            stack.append(float(match.group(0)))
        except ValueError:
            pass

    scrollbox = curses_stuff.CursesScrollBox(env.STDSCR, -4, -4)
    scrollbox.set_title("COMMAND OUTPUT")
    scrollbox.set_text(data)
    scrollbox.show()

def _newstack(stack, arg):
    """push a new nested stack"""
    new_stack = nums.UndoStack()
    new_stack.parent = stack
    stack.append(new_stack)
    env.STACK = new_stack

def _enterstack(stack, arg):
    """enter a nested stack"""
    child = untagged(stack[-1])
    if not isinstance(child, nums.UndoStack):
        raise TypeError("can only enter a nested stack, not a value")
    env.STACK = child

    # Remove extra undo item
    stack.undo()

def _leavestack(stack, arg):
    """return to the parent stack"""
    if stack.parent is None:
        raise Exception("cannot move above the root stack")
    env.STACK = stack.parent

    # Remove extra undo item
    stack.undo()

def _merge(stack, arg):
    """merge a nested stack into this stack"""
    nested = stack.pop()
    if not isinstance(nested, nums.UndoStack):
        raise TypeError("can only merge stack, not value")
    for i in nested:
        if isinstance(i, nums.UndoStack):
            new_i = nums.UndoStack(i)
            new_i.parent = stack
            stack.append(new_i)
        else:
            stack.append(i)

def _flatten(stack, arg):
    """flatten the current stack"""

    def flatten_recursive(items, target):
        for i in items:
            if isinstance(i, nums.UndoStack):
                flatten_recursive(i, target)
            else:
                target.append(i)

    items = stack[:]
    del stack[:]
    flatten_recursive(items, stack)

def _seq(stack, arg):
    """seq start stop step"""

    args = [float(i) for i in arg.split()]
    if len(args) != 3:
        raise Exception("expected args: start stop step")

    start, stop, step = args

    newstack = nums.UndoStack(frange(start, stop, step))
    newstack.parent = stack
    stack.append(newstack)


################################################################################
# DISPLAY/FORMATTING/SETTINGS/HELP COMMANDS

def _help(stack, arg):
    """display help"""
    scrollbox = curses_stuff.CursesScrollBox(env.STDSCR, -4, -4)
    scrollbox.set_title("HELP")

    lines_left = []
    lines_right = []

    for key in COMMANDS.keys():
        val = COMMANDS[key]
        if isinstance(key, int):
            lines_left.append(" " * 26)
            lines_left.append("%-26s" % val)
        else:
            doc = val.__doc__
            if doc is None:
                doc = "NODOC: " + key
            lines_left.append("%-10s %-15s" % (key, doc.partition("\n")[0]))

    for key in SINGLE_KEY_COMMANDS.keys():
        key_name = curses_stuff.KEY_TO_NAME.get(key, key)
        val = SINGLE_KEY_COMMANDS[key]
        if val is None:
            continue
        lines_right.append("%-10s %-15s" % (key_name, val.__doc__.partition("\n")[0]))

    if len(lines_left) < len(lines_right):
        lines_left.extend([""] * (len(lines_right) - len(lines_left)))
    if len(lines_left) > len(lines_right):
        lines_right.extend([""] * (len(lines_left) - len(lines_right)))

    lines = [i + "    " + j for i, j in zip(lines_left, lines_right)]
    scrollbox.set_text(lines)

    scrollbox.show()

def _exc(stack, arg):
    """display the latest exception"""
    if env.LAST_ERROR is None:
        return
    last_bt = traceback.format_exception(*env.LAST_ERROR)
    scrollbox = curses_stuff.CursesScrollBox(env.STDSCR, -4, -4)
    scrollbox.set_title("LAST BACKTRACE")
    scrollbox.set_text(last_bt)
    scrollbox.show()

def _repr(stack, arg):
    """debug: repr(x)"""
    stack.append(repr(stack.pop()))

def _str(stack, arg):
    """debug: stringify"""
    stack.append(env.FORMAT.format(stack.pop()))

def _nat(stack, arg):
    """natural mode"""
    env.FORMAT = nums.NaturalMode

def _fix(stack, arg):
    """fixed mode, digits = 6 or command argument"""
    env.FORMAT = nums.FixMode

    if arg is not None and arg.strip():
        nums.FixMode.digits = int(arg.strip())
    else:
        nums.FixMode.digits = 6

def _eng(stack, arg):
    """engineering mode, sig figs = 7 or command argument"""
    env.FORMAT = nums.EngMode

    if arg is not None and arg.strip():
        nums.EngMode.sigfigs = int(arg.strip())
    else:
        nums.EngMode.sigfigs = 7

def _sci(stack, arg):
    """scientific mode"""
    env.FORMAT = nums.SciMode

def _hex(stack, arg):
    """hexadecimal display mode"""
    env.FORMAT = nums.HexMode

def _dec(stack, arg):
    """decimal display mode"""
    env.FORMAT = nums.DecMode

def _oct(stack, arg):
    """octal display mode"""
    env.FORMAT = nums.OctMode

def _bin(stack, arg):
    """binary display mode"""
    env.FORMAT = nums.BinMode


################################################################################
# ADDING SINGLE-LETTER COMMANDS
#
# Insert a tuple into the OrderedDict below:
# (key, command)
#
# key:      the key returned by curses. For printables, just the character.
# command:  a function that takes the current UndoStack, operates on it,
#               and returns nothing. Any exceptions thrown in here will be
#               caught and handled, so don't worry about those.
#
# The command must have a docstring. The first line of this will be used as its
# help text.
#
# Standard unary and binary operators can be made with UNARY() and BINARY(),
# which accept a lambda function taking one or two arguments and return an
# operator closure around it. These take the desired docstring as the second
# argument.

SINGLE_KEY_COMMANDS = collections.OrderedDict([
    ("\x7f", _drop),
    ("\x08", _drop),
    (curses.KEY_BACKSPACE, _drop),

    ("\r", _dup),
    ("\n", _dup),
    (curses.KEY_ENTER, _dup),

    (curses.KEY_UP, _rotup),
    (curses.KEY_DOWN, _rotdown),

    ("-", BINARY(lambda x, y: x - y, "subtract")),
    ("+", BINARY(lambda x, y: x + y, "add")),
    ("*", BINARY(lambda x, y: x * y, "multiply")),
    ("/", BINARY(lambda x, y: x / y, "divide")),
    ("%", BINARY(lambda x, y: x % y, "modulo")),
    ("^", BINARY(lambda x, y: x ** y, "power")),
    ("E", UNARY(autoc("exp"), "exponential")),
    ("l", UNARY(autoc("log"), "log base e")),
    ("L", UNARY(autoc("log10"), "log base 10")),
    ("r", UNARY(lambda x: x ** 0.5, "sq root")),
    ("i", UNARY(lambda x: 1/x, "reciprocal")),
    ("!", UNARY(lambda x: math.gamma(x + 1), "factorial")),
    ("P", BINARY(lambda x, y: math.gamma(x+1) / math.gamma(x-y+1), "permutations")),
    ("C", BINARY(lambda x, y: math.gamma(x+1) / (math.gamma(y+1)*math.gamma(x-y+1)), "combinations")),

    ("u", _undo),
    ("R", _redo),
    ("x", _xchg),
    ("[", _get),
    ("{", _pull),
    ("}", _push),

    ("t", _tag),
    ("T", _untag),

    ("S", _newstack),
    (">", _enterstack),
    ("<", _leavestack),

    ("?", _help),

    # RESERVED: these appear inside numbers
    ("e", None),
    ("j", None),
    ("h", None),
    ("d", None),
    ("o", None),
    ("b", None),
    ('"', None),
    ("_", None),
    (".", None),
])

################################################################################
# ADDING NAMED COMMANDS
#
# Insert a tuple into the OrderedDict below:
# (key, command)
#
# name:     the full command name, including beginning single-quote
# command:  a function that takes the current UndoStack, operates on it,
#               and returns nothing. Any exceptions thrown in here will be
#               caught and handled, so don't worry about those.
#
# The command must have a docstring. The first line of this will be used as its
# help text.
#
# Standard unary and binary operators can be made with UNARY() and BINARY(),
# which accept a lambda function taking one or two arguments and return an
# operator closure around it. These take the desired docstring as the second
# argument.
#
# You can insert section headers into the help text by adding a tuple:
# (id, header)
#
# id:       any unique integer
# header:   header text

COMMANDS = collections.OrderedDict([
    (10, "==TRIGONOMETRY, RAD=="),
    ("'sin", UNARY(autoc("sin"), "sin(rad)")),
    ("'cos", UNARY(autoc("cos"), "cos(rad)")),
    ("'tan", UNARY(autoc("tan"), "tan(rad)")),
    ("'asin", UNARY(autoc("asin"), "asin->rad")),
    ("'acos", UNARY(autoc("acos"), "acos->rad")),
    ("'atan", UNARY(autoc("atan"), "atan->rad")),
    (20, "==TRIGONOMETRY, DEG=="),
    ("'sind", UNARY(degree_trig(autoc("sin")), "sin(deg)")),
    ("'cosd", UNARY(degree_trig(autoc("cos")), "cos(deg)")),
    ("'tand", UNARY(degree_trig(autoc("tan")), "tan(deg)")),
    ("'asind", UNARY(degree_invtrig(autoc("asin")), "asin->deg")),
    ("'acosd", UNARY(degree_invtrig(autoc("acos")), "acos->deg")),
    ("'atand", UNARY(degree_invtrig(autoc("atan")), "atan->deg")),
    ("'deg", UNARY(lambda x: x * 180 / math.pi, "rad->deg")),
    ("'rad", UNARY(lambda x: x * math.pi / 180, "deg->rad")),
    (30, "==HYPERBOLICS=="),
    ("'sinh", UNARY(autoc("sinh"), "sinh")),
    ("'cosh", UNARY(autoc("cosh"), "cosh")),
    ("'tanh", UNARY(autoc("tanh"), "tanh")),
    ("'asinh", UNARY(autoc("asinh"), "asinh")),
    ("'acosh", UNARY(autoc("acosh"), "acosh")),
    ("'atanh", UNARY(autoc("atanh"), "atanh")),
    (40, "==SIMPLE=="),
    ("'exp", UNARY(autoc("exp"), "exponential")),
    ("'log", UNARY(autoc("log"), "log base e")),
    ("'log10", UNARY(autoc("log10"), "log base 10")),
    ("'log2", UNARY(lambda x: autoc("log")(x, 2), "log base 2")),
    ("'divmod", _divmod),
    (50, "==COMPLEX=="),
    ("'re", UNARY(lambda x: x.real, "real part")),
    ("'im", UNARY(lambda x: x.imag, "imaginary part")),
    ("'conj", UNARY(lambda x: complex(x.real, -x.imag), "complex conjugate")),
    ("'reim", _reim),
    ("'abs", UNARY(abs, "absolute value")),
    ("'angle", UNARY(cmath.phase, "angle/phase (rad)")),
    ("'polar", _polar),
    ("'fcart", _fcart),
    ("'fpolar", _fpolar),
    (60, "==NESTED STACKS=="),
    ("'sum", UNARY(sum, "sum of stack", autostack=False)),
    ("'mean", UNARY(lambda x: sum(x) / float(len(x)), "mean of stack", autostack=False)),
    ("'rms", UNARY(lambda x: (sum(i**2 for i in x) / float(len(x)))**0.5, "quadratic mean of stack", autostack=False)),
    ("'pvar", _pvar),
    ("'pdev", _pdev),
    ("'svar", _svar),
    ("'sdev", _sdev),
    ("'merge", _merge),
    ("'flatten", _flatten),
    ("'seq", _seq),
    (70, "==CONSTANTS=="),
    ("'pi", CONST(math.pi, "const PI")),
    ("'e", CONST(math.e, "const E")),
    ("'j", CONST(0+1j, "imaginary unit")),
    ("'c", CONST(2.99792458e8, "speed of light, m/s")),
    ("'h", CONST(6.6260755e-34, "Planck constant, J s")),
    ("'k", CONST(1.380658e-23, "Boltzmann constant, J/K")),
    ("'elec", CONST(1.60217733e-19, "Charge of electron, C")),
    ("'e0", CONST(8.854187817e-12, "Permittivity of vacuum, F/m")),
    ("'amu", CONST(1.6605402e-27, "Atomic mass unit, kg")),
    ("'Na", CONST(6.0221367e23, "Avogadro's number, mol^-1")),
    ("'atm", CONST(101325., "Standard atmosphere, Pa")),
    (80, "==LERPN=="),
    ("'sh", _sh),
    ("'help", _help),
    ("'exc", _exc),
    ("'repr", _repr),
    ("'str", _str),
    ("'eng", _eng),
    ("'sci", _sci),
    ("'fix", _fix),
    ("'nat", _nat),
    ("'hex", _hex),
    ("'dec", _dec),
    ("'oct", _oct),
    ("'bin", _bin),
])
