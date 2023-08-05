# /setuptools_green/__init__.py
#
# Provides a setuptools command for running tests using the "green"
# test runner.
#
# See /LICENCE.md for Copyright information
"""Provide a setuptools command for running tests with green."""

import subprocess

import sys

from distutils.errors import DistutilsArgError  # suppress(import-error)

import setuptools


class GreenTestCommand(setuptools.Command):
    """Provide a test command using green."""

    def __init__(self, *args, **kwargs):
        """Initialize instance variables."""
        setuptools.Command.__init__(self, *args, **kwargs)
        self.quiet = False
        self.concurrent = False
        self.coverage = False
        self.coverage_omit = None
        self.target = None

    def run(self):   # suppress(unused-function)
        """Run tests using green."""
        argv = ["green", "-t"]

        if self.target:
            argv.append(self.target)

        if self.concurrent:
            argv.extend(["-s", "0"])

        if self.coverage:
            argv.append("-r")

        if self.coverage_omit:
            argv.extend(["-o", self.coverage_omit])

        if not self.quiet:
            argv.append("-vvv")

        sys.exit(subprocess.call(argv))

    def initialize_options(self):  # suppress(unused-function)
        """Set all options to their initial values."""
        self.quiet = False
        self.concurrent = False
        self.coverage = False
        self.coverage_omit = None
        self.target = None

    def finalize_options(self):  # suppress(unused-function)
        """Finalize options."""
        for arg in ("concurrent", "coverage", "quiet"):
            if not isinstance(getattr(self, arg), int):
                raise DistutilsArgError("""--{} takes no additional """
                                        """arguments.""".format(arg))

        for arg in ("target", "coverage-omit"):
            if not (isinstance(getattr(self, arg.replace("-", "_")), str) or
                    getattr(self, arg.replace("-", "_")) is None):
                upper_arg = arg.upper()
                raise DistutilsArgError("""--{l}={u}: {u} must be a """
                                        """string.""".format(l=arg,
                                                             u=upper_arg))

    user_options = [  # suppress(unused-variable)
        ("quiet", None, """Don't show test descriptions when running"""),
        ("concurrent", None, """Run tests concurrently"""),
        ("coverage", None, """Collect coverage"""),
        ("coverage-omit=", None, ("""Patterns to omit from coverage, """
                                  """comma separated""")),
        ("target=", None, ("""Name of subdirectory where tests are to be """
                           """found"""))
    ]
    # suppress(unused-variable)
    description = "run tests using the 'green' test runner"
