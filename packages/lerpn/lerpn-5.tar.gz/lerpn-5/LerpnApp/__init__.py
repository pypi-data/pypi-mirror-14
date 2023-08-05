"""lerpn application module

To run lerpn, call main().
"""

__version__ = "5"

# Written in 2015 by Christopher Pavlina.
###############################################################################
#
# This software is free. Do whatever the fuck you want with it. Copy it, change
# it, steal it, strip away this notice, print it and tear it into confetti to
# throw at random dudes on the street. Really, I don't care.

# pylint: disable=wrong-import-position
import curses
import os
import signal
import sys
from . import nums, env, tui

def wrapped_main(stdscr):
    """main function to be wrapped by curses.wrapper
    """
    curses.nonl()
    env.STDSCR = stdscr
    env.STACK = nums.UndoStack()
    prompt = tui.Prompt()

    # Register exit handler
    # pylint: disable=unused-argument
    def exit_handler(signum, frame):
        """Call the lerpn cleanup/exit function, to be used as a signal handler"""
        tui.do_exit(env.STACK)

    signal.signal(signal.SIGINT, exit_handler)

    while True:
        stdscr.clear()
        prompt.loop(env.STACK)

def main():
    """call this to launch lerpn
    """
    debug = os.getenv("DEBUG_LERPN")
    if debug is not None and int(debug):
        import rpdb
        rpdb.set_trace()

    if "--help" in sys.argv or "-h" in sys.argv:
        print("usage: %s [--version] [--help]" % os.path.basename(sys.argv[0]))
        print("")
        print("lerpn (Linux Engineering RPN calculator)")
        print("Run with no arguments to start the calculator. Once started, try")
        print("pressing ? to see a list of commands.")
        return

    if "--version" in sys.argv:
        print("lerpn version " + __version__)
        return

    curses.wrapper(wrapped_main)

def gen_commands_md():
    """generate a Markdown reference of all commands"""

    from . import commands, curses_stuff

    print("# Quick Command Reference")
    print()
    print("This list is auto-generated from the code, and contains the same")
    print("text you would see in the in-program help box.")
    print()
    print("## Single-key commands")
    print()
    print("Key | Description")
    print("--- | -----------")
    for cmd in commands.SINGLE_KEY_COMMANDS:
        cmd_name = curses_stuff.KEY_TO_NAME.get(cmd, "`%s`" % cmd)
        cmd_function = commands.SINGLE_KEY_COMMANDS[cmd]
        if cmd_function is None:
            continue
        cmd_desc = cmd_function.__doc__.partition("\n")[0]
        print("%s | %s" % (cmd_name, cmd_desc))
    print()

    print("## Long commands")
    print()
    print("Name | Description")
    print("---- | -----------")
    for cmd in commands.COMMANDS:
        if isinstance(cmd, int):
            cmd_name = ""
            cmd_desc = "**%s**" % commands.COMMANDS[cmd]
        else:
            cmd_name = "`%s`" % cmd
            cmd_desc = commands.COMMANDS[cmd].__doc__.partition("\n")[0]
        print("%s | %s" % (cmd_name, cmd_desc))
    print()

if __name__ == "__main__":
    main()
