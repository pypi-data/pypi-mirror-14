#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# ///////////////////////////////////////////
#
# Standard Output Functions
#
# ///////////////////////////////////////////


def stdout(msg, statuscode=None):
    """Writes msg to the standard output stream with option to exit program with the exit status code
    statuscode.  If statuscode is not defined, sys.exit() is not called by the function.

    :param msg: The data to print in the standard output stream
    :param statuscode: (optional) an integer that represents the exit status code."""

    sys.stdout.write(msg + "\n")
    if statuscode is not None:
        assert isinstance(statuscode, object)
        sys.exit(statuscode)


# def stdout_xnl(msg, statuscode=None):
#     sys.stdout.write(msg)
#     if statuscode is not None:
#         assert isinstance(statuscode, object)
#         sys.exit(statuscode)
#
#
# def stdout_iter(iterable, statuscode=None):
#     for msg in iterable:
#         sys.stdout.write(msg + "\n")
#     if statuscode is not None:
#         assert isinstance(statuscode, object)
#         sys.exit(statuscode)


# ///////////////////////////////////////////
#
# Standard Error Functions
#
# ///////////////////////////////////////////


def stderr(msg, statuscode=None):
    """Writes msg to the standard error stream with option to exit program with the exit status code
    statuscode.  If statuscode is not defined, sys.exit() is not called by the function.

    :param msg: The data to print in the standard error stream
    :param statuscode: (optional) an integer that represents the exit status code."""

    sys.stderr.write(msg + "\n")
    if statuscode is not None:
        assert isinstance(statuscode, object)
        sys.exit(statuscode)


# def stderr_xnl(msg, statuscode=None):
#     sys.stderr.write(msg)
#     if statuscode is not None:
#         assert isinstance(statuscode, object)
#         sys.exit(statuscode)
#
#
# def stderr_iter(iterable, statuscode=None):
#     for msg in iterable:
#         sys.stderr.write(msg + "\n")
#     if statuscode is not None:
#         assert isinstance(statuscode, object)
#         sys.exit(statuscode)


# ///////////////////////////////////////////
#
# Standard Input Functions
#
# ///////////////////////////////////////////

def stdin():
    """Reads and returns all data in the standard input stream.  The function blocks until all data is read.

    :returns: Standard input stream data
    """

    return sys.stdin.read()


def stdin_lines():
    """A generator function that reads and returns all data in the standard input stream by each newline value.

    :returns: Standard input stream data by newline
    """
    for line in sys.stdin.readlines():
        yield line


# def stdin_is_piped():
#     """Returns a boolean answer to the question 'Is the standard input being piped to the script from another
#     application rather than being run interactively?'
#
#     :returns: boolean.  True = stadard input is piped from another program; False = standard input is not piped from
#     another program
#     """
#     if sys.stdin.isatty() is True:
#         return False
#     else:
#         return True
#
#
# def prompt(msg):
#     if (sys.version_info[0] == 2) is True:
#         try:
#             return raw_input(msg)
#         except NameError:
#             return input(msg)
#     else:
#         return input(msg)
