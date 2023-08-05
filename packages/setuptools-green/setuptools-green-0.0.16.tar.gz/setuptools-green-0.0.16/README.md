# Setuptools Green

This module provides a "green" command for setuptools scripts that uses
[green](https://github.com/CleanCut/green) to run tests.

## Status

| Travis CI (Ubuntu) | AppVeyor (Windows) | Coverage | PyPI | Licence |
|--------------------|--------------------|----------|------|---------|
|[![Travis](https://img.shields.io/travis/polysquare/setuptools-green.svg)](http://travis-ci.org/polysquare/setuptools-green)|[![AppVeyor](https://img.shields.io/appveyor/ci/smspillaz/setuptools-green.svg)](https://ci.appveyor.com/project/smspillaz/setuptools-green)|[![Coveralls](https://img.shields.io/coveralls/polysquare/setuptools-green.svg)](http://coveralls.io/polysquare/setuptools-green)|[![PyPIVersion](https://img.shields.io/pypi/v/setuptools-green.svg)](https://pypi.python.org/pypi/setuptools-green)[![PyPIPythons](https://img.shields.io/pypi/pyversions/setuptools-green.svg)](https://pypi.python.org/pypi/setuptools-green)|[![License](https://img.shields.io/github/license/polysquare/setuptools-green.svg)](http://github.com/polysquare/setuptools-green)|

## Usage

    Options for 'GreenTestCommand' command:
      --quiet          Don't show test descriptions when running
      --concurrent     Run tests concurrently
      --coverage       Collect coverage
      --coverage-omit  Patterns to omit from coverage, comma separated
      --target         Name of subdirectory where tests are to be found

By default, the verbose mode is used, but you can pass --quiet
to just show dots for passes and "E" for failures.
