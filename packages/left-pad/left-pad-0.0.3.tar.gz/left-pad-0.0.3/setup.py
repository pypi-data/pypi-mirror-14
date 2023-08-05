#!/usr/bin/env/python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

LONG = """
Pad a string to the left with any number of characters

    pip install left-pad

Then

    >>> from left_pad import left_pad
    >>> s = "abc"
    >>> left_pad(s, 2, "+")
    '++abc'

Make sure to add left-pad to your dependencies in your next project.

Or, if you want to reinvent the wheel, go ahead and try to do it
with the standard library

    >>> s.rjust(len(s) + 2, '+')
    '++abc'
"""

setup(name='left-pad',
      version='0.0.3',
      description='Pad a string to the left with any number of characters',
      license='BSD',
      author='Matthew Perry',
      author_email='perrygeo@gmail.com',
      long_description=LONG,
      url='https://docs.python.org/2/library/stdtypes.html#str.rjust',
      py_modules=['left_pad'],
      install_requires=[],
)
