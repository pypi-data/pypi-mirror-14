"""
This module provides the setup guidelines for the normalazy library.
"""

from distutils.core import setup
from codecs import open
from normalazy import __version__
from os import path

#: Defines the current directory.
here = path.abspath(path.dirname(__file__))

## Get the long description from the README file:
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

## Setup now:
setup(name="normalazy",
      version=__version__,
      description="A mapper to normalize records for lazy people",
      long_description=long_description,
      license="BSD",
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Intended Audience :: Developers",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "License :: OSI Approved :: BSD License",
          "Topic :: Software Development :: Libraries"
      ],
      keywords=["normalizer", "DSL"],
      author="Vehbi Sinan Tunalioglu",
      author_email="vst@vsthost.com",
      url="https://github.com/vst/normalazy",
      py_modules=["normalazy"],
      install_requires=[
          "six==1.10.0",
      ])

