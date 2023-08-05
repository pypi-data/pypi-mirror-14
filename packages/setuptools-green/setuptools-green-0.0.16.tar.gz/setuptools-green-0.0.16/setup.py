# /setup.py
#
# Installation and setup script for setuptools-green
#
# See /LICENCE.md for Copyright information
"""Installation and setup script for setuptools-green."""

from setuptools import find_packages
from setuptools import setup

try:
    from setuptools_green import GreenTestCommand
    _CMD_CLASSES = {
        "green": GreenTestCommand
    }
except ImportError:
    _CMD_CLASSES = dict()

setup(name="setuptools-green",
      version="0.0.16",
      description="Provides a 'test' command for running tests with green",
      long_description_markdown_filename="README.md",
      author="Sam Spilsbury",
      author_email="smspillaz@gmail.com",
      url="http://github.com/polysquare/setuptools-green",
      classifiers=["Development Status :: 3 - Alpha",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.1",
                   "Programming Language :: Python :: 3.2",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Intended Audience :: Developers",
                   "Topic :: Software Development :: Build Tools",
                   "License :: OSI Approved :: MIT License"],
      license="MIT",
      keywords="development testing",
      packages=find_packages(exclude=["tests"]),
      cmdclass=_CMD_CLASSES,
      install_requires=["setuptools", "green>=2.0.0"],
      extras_require={
          "upload": ["setuptools-markdown"]
      },
      entry_points={
          "distutils.commands": [
              "green=setuptools_green:GreenTestCommand",
          ]
      },
      zip_safe=True,
      include_package_data=True)
