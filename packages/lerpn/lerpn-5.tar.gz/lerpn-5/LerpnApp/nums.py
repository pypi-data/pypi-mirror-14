"""Code dealing with numbers.
"""

import re
import math

FLOAT_RE = re.compile(r"[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")
FLOAT_RE_UNDER = re.compile(r"[-_+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")

NUM_PARSE_RE = re.compile(
    r"\s*(?P<re>" + FLOAT_RE_UNDER.pattern + r")" +     # real part
    r"\s*(?P<im>[jJ]\s*" + FLOAT_RE_UNDER.pattern + ")?" + # imaginary part
    r'\s*(?P<tag>".*)?' +                               # tag
    "$")

# number with radix
RNUM_PARSE_RE = re.compile(
    r"\s*(?P<radix>0[bdoh])" +                          # radix
    r"\s*(?P<re>[-+]?[0-9A-Fa-f]+)" +                   # real part
    r'\s*(?P<tag>".*)?' +                               # tag
    "$")

def num_parser(in_str):
    """Parse a number from user input.

    This accepts any combination of real part, imaginary part, and tag;
    or any combination of radix, integer, and tag:

    1.2e3   j5.4e-8     " random complex number
    0h      fffe        " my favorite number :)
    """

    match = RNUM_PARSE_RE.match(in_str)
    if match is not None:
        # integer with radix
        return num_parser_with_radix(match)

    match = NUM_PARSE_RE.match(in_str)

    if match is None:
        raise ValueError("Cannot parse value %r" % in_str)

    real_str = match.group("re")
    if real_str.startswith("_"):
        real_str = "-" + real_str[1:]
    real = float(real_str)

    if match.group("im") is not None:
        imag_str = match.group("im")[1:].strip()
        if imag_str.startswith("_"):
            imag_str = "-" + imag_str[1:]
        imag = float(imag_str)
    else:
        imag = None

    if imag is None:
        value = real
    else:
        value = complex(real, imag)

    if match.group("tag") is not None:
        value = Tagged(value, match.group("tag")[1:].strip())

    return value

def num_parser_with_radix(match):
    """Take over from num_parser for anything with a radix."""

    radname = match.group("radix").lower()
    radix_map = {"0h": 16, "0d": 10, "0o": 8, "0b": 2}
    radix = radix_map[radname]

    value = float(int(match.group("re"), radix))

    if match.group("tag") is not None:
        value = Tagged(value, match.group("tag")[1:].strip())

    return value

class UndoStack(list):
    """Stack supporting an 'undo' action.
    This is used as the main RPN stack. You can append() and pop() and [] just
    like with a normal list. You can also use undopush() to push a duplicate of
    the stack itself onto a "stack of stacks", and then undo() to restore that.

    undo() moves the last item to the redo stack. Use drop() to drop it without
    doing this.
    """

    def __init__(self, v=None):
        """Initialize an UndoStack from an optional source list.
        """
        self.__redo_held = None
        if v is None:
            list.__init__(self)
            self.__stack = [[]]
            self.__redo = []

        else:
            list.__init__(self, v)
            self.__stack = [[]]
            self.__redo = []

        self.parent = None

    def __repr__(self):
        return 'UndoStack(%r)' % (list(self))

    def undopush(self):
        """Save the current stack state to be restored later with undo()
        """
        self.__redo_held = self.__redo
        self.__redo = []
        self.__stack.append(self[:])

    def undo(self):
        """Restore the last saved undo state"""
        self.__redo.append(self[:])
        self.drop()

    def drop(self):
        """Restore the last saved undo state, but do not push the current
        state to the redo stack.
        """
        if len(self.__stack) > 1:
            self[:] = self.__stack.pop()
        else:
            self[:] = []

    def redo(self):
        """Undo the last undo"""
        if self.__redo:
            self[:] = self.__redo.pop()

    def replace_redo(self):
        """replace the redo stack directly after undopush has cleared it."""
        self.__redo = self.__redo_held

    def __str__(self):
        return "<< STACK(%d) >>" % len(self)

    def __add__(self, other):
        if isinstance(other, UndoStack):
            assert self.parent is other.parent
            new_stack = UndoStack(list.__add__(self, other))
            new_stack.parent = self.parent
            return new_stack
        else:
            return self.__add_real__(other) # pylint: disable=no-member

    def __radd__(self, other):
        # pylint: disable=no-member
        return self.__radd_real__(other)

    @classmethod
    def generate_operators(cls):
        """Autogenerates a set of operator overloads"""
        # Add operations to Tagged
        ops = [
            ("add_real", lambda x, y: x+y),
            ("sub", lambda x, y: x-y),
            ("mul", lambda x, y: x*y),
            ("div", lambda x, y: x/y),
            ("truediv", lambda x, y: x/y),
            ("mod", lambda x, y: x%y),
            ("pow", lambda x, y: x**y),
            ]
        for opname, opfunc in ops:
            def method(self, other, opfunc=opfunc):
                """automatically defined operator"""
                if not isinstance(other, float) and not isinstance(other, complex):
                    return NotImplemented
                new_stack = cls(opfunc(i, other) for i in self)
                new_stack.parent = self.parent
                return new_stack

            def rmethod(self, other, opfunc=opfunc):
                """automatically defined operator"""
                if not isinstance(other, float) and not isinstance(other, complex):
                    return NotImplemented
                new_stack = cls(opfunc(other, i) for i in self)
                new_stack.parent = self.parent
                return new_stack

            setattr(cls, "__%s__" % opname, method)
            setattr(cls, "__r%s__" % opname, rmethod)

UndoStack.generate_operators()

class Tagged(object):
    """Tagged number object.
    This behaves like a number, but also contains a string tag. The values
    are accessible at .num and .tag
    """
    def __init__(self, num, tag):
        assert isinstance(tag, str)
        self._num = num
        self._tag = tag

    @property
    def num(self):
        """the number that is tagged"""
        return self._num

    @property
    def tag(self):
        """the tag applied to the number"""
        return self._tag

    def __repr__(self):
        return "Tagged(%r, %r)" % (self._num, self._tag)

    @classmethod
    def generate_operators(cls):
        """Autogenerates a set of operator overloads"""
        # Add operations to Tagged
        ops = [
            ("add", lambda x, y: x+y),
            ("sub", lambda x, y: x-y),
            ("mul", lambda x, y: x*y),
            ("div", lambda x, y: x/y),
            ("truediv", lambda x, y: x/y),
            ("mod", lambda x, y: x%y),
            ("pow", lambda x, y: x**y),
            ]
        for opname, opfunc in ops:
            # For the uninitiated, the default-argument parameters create a new
            # scope for the variable, allowing passing each loop iteration's value
            # to the closure instead of closing around the single final value.
            def method(self, other, opfunc=opfunc):
                """automatically defined operator"""
                if isinstance(other, cls):
                    # If both are tagged, just remove the tag.
                    return opfunc(self.num, other.num)
                if not isinstance(other, float) and not isinstance(other, complex):
                    return NotImplemented
                return cls(opfunc(self.num, other), self.tag)

            def rmethod(self, other, opfunc=opfunc):
                """automatically defined operator"""
                if isinstance(other, cls):
                    # If both are tagged, just remove the tag.
                    return opfunc(other.num, self.num)
                if not isinstance(other, float) and not isinstance(other, complex):
                    return NotImplemented
                return cls(opfunc(other, self.num), self.tag)

            setattr(cls, "__%s__" % opname, method)
            setattr(cls, "__r%s__" % opname, rmethod)

Tagged.generate_operators()

LUT_UNICODE = {
    -24: "y", -21: "z", -18: "a", -15: "f", -12: "p",
    -9: "n", -6: u"\xb5", -3: "m", 0: "", 3: "k",
    6: "M", 9: "G", 12: "T", 15: "P", 18: "E",
    21: "Z", 24: "Y"
}

LUT_ASCII = {
    -24: "y", -21: "z", -18: "a", -15: "f", -12: "p",
    -9: "n", -6: "u", -3: "m", 0: "", 3: "k",
    6: "M", 9: "G", 12: "T", 15: "P", 18: "E",
    21: "Z", 24: "Y"
}

import curses
if hasattr(curses, "unget_wch"):
    LUT = LUT_UNICODE
else:
    LUT = LUT_ASCII

def eng(num, sigfigs=7):
    """Return num in engineering notation"""

    if isinstance(num, complex):
        real = num.real
        imag = num.imag
        imag_sign = "+" if imag >= 0.0 else "-"
        imag_abs = abs(imag)

        return "(%s %sj %s)" %(eng(real), imag_sign, eng(imag_abs))

    if num == 0.0:
        return "0"

    elif num < 0.0:
        return '-'+eng(-num, sigfigs)

    try:
        magnitude = math.floor(math.log10(num)/3)*3
    except (OverflowError, ValueError):
        # inf, nan
        return str(num)


    coeff = "{0:.{1}g}".format(num * 10.0 ** (-magnitude), sigfigs)
    lut = LUT.get(magnitude, None)
    if lut is None:
        return coeff + "e" + str(magnitude)
    if lut != '':
        lut = '_' + lut
    return coeff + lut

class DisplayMode(object):
    """Static class with methods to implement a display mode"""

    @classmethod
    def format_real(cls, num):
        """Format a real number (float) according to this display mode.
        Must be implemented for each mode."""
        raise NotImplementedError

    @classmethod
    def format(cls, num):
        """Format the number in the subclass mode. Do not call this directly
        on DisplayMode, only on its subclasses."""
        if isinstance(num, Tagged):
            return cls.format(num.num)

        elif isinstance(num, float):
            return cls.format_real(num)

        elif isinstance(num, complex):
            real = num.real
            imag = num.imag
            imag_sign = "+" if imag >= 0.0 else "-"
            imag_abs = abs(imag)

            return "(%s %sj %s)" % (cls.format_real(real), imag_sign, cls.format_real(imag_abs))

        elif isinstance(num, str):
            return repr(num)

        else:
            return str(num)

    @classmethod
    def name(cls):
        """Return a short name for displaying in the status bar"""
        return str(cls)

class EngMode(DisplayMode):
    """Engineering mode. Numbers are displayed similarly to scientific notation,
    but with exponents always a multiple of 3, and using metric prefixes:

    13000.  becomes 13_k
    """

    sigfigs = 7

    @classmethod
    def format_real(cls, num):
        """Format a float in engineering mode"""
        return eng(num, cls.sigfigs)

    @classmethod
    def name(cls):
        return "ENG(%d)" % cls.sigfigs

class FixMode(DisplayMode):
    """Fixed mode. Numbers are displayed with a fixed number of places after
    the decimal point."""

    digits = 6

    @classmethod
    def format_real(cls, num):
        """Format a float in fixed mode"""
        return "%.*f" % (cls.digits, num)

    @classmethod
    def name(cls):
        return "FIX(%d)" % cls.digits

class NaturalMode(DisplayMode):
    """Natural mode. Very large or small numbers are displayed in scientific notation;
    midrange numbers are displayed in standard notation."""

    @classmethod
    def format_real(cls, num):
        """Format a float in natural mode"""
        return "%g" % num

    @classmethod
    def name(cls):
        return "NAT"

class SciMode(DisplayMode):
    """Scientific mode. All numbers are displayed as as [-]d.ddde+dd"""

    @classmethod
    def format_real(cls, num):
        """Format a float in scientific mode"""
        return "%e" % num

    @classmethod
    def name(cls):
        return "SCI"

class HexMode(DisplayMode):
    """Display integers in hexadecimal, floats in natural mode."""
    @classmethod
    def format_real(cls, num):
        """Format a float, rounded to integer, in hexadecimal"""

        def hex_h(v):
            """same as hex(), but use 0h as the prefix instead of 0x"""
            return "0h" + hex(v)[2:]

        return format_int(num, hex_h)

    @classmethod
    def name(cls):
        return "HEX+NAT"

class DecMode(DisplayMode):
    """Display integers in decimal, floats in natural mode."""
    @classmethod
    def format_real(cls, num):
        """Format a float, rounded to integer, in decimal"""
        return format_int(num, lambda x: str(int(x)))

    @classmethod
    def name(cls):
        return "DEC+NAT"

class OctMode(DisplayMode):
    """Display integers in octal, floats in natural mode."""
    @classmethod
    def format_real(cls, num):
        """Format a float, rounded to integer, in octal"""

        def consistent_oct(n):
            """Format octal consistently, always 0o123 rather than
            0123 regardless of Python version."""
            octalized = oct(n)
            if octalized.startswith("0o"):
                return octalized
            else:
                return "0o" + octalized[1:]

        return format_int(num, consistent_oct)

    @classmethod
    def name(cls):
        return "OCT+NAT"

class BinMode(DisplayMode):
    """Display integers in binary, floats in natural mode."""
    @classmethod
    def format_real(cls, num):
        """Format a float, rounded to integer, in binary"""
        return format_int(num, bin)

    @classmethod
    def name(cls):
        return "BIN+NAT"

def format_int(value, fxn):
    """If 'value', as a float, is "close" to an integer, format it as
    fxn(int(value)), otherwise as "%g" % value."""

    fracpart = value - float(int(value))
    if abs(fracpart) < 0.001 or abs(fracpart) > 0.999:
        return fxn(int(value))
    else:
        return "%g" % value
