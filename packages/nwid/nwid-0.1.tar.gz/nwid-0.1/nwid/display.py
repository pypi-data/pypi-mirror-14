#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             display.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       02/19/2016
#

"""
nwid.display
~~~~~~~~~~~~

This module contains the RawDisplay class as well as the Coordinates data
structure.
"""

from __future__ import absolute_import


class Coordinates(object):
    def __init__(self, x, y):
        """Initializes the x and y attributes."""
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __repr__(self):
        return 'Coordinates' + str(self)

    def __eq__(self, other):
        """Compares 2 sets of coordinates."""
        try:
            return self.x == other.x and self.y == other.y
        except AttributeError:  # Can also take a tuple (x, y)
            return self.x == other[0] and self.y == other[1]

    def __add__(self, other):
        """Adds 2 sets of coordinates, or one integer to the x and y of this object."""
        try:
            return Coordinates(self.x + other.x, self.y + other.y)
        except AttributeError:  # Can also take a tuple (x, y)
            return Coordinates(self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        """Adds 2 sets of coordinates, or one integer to the x and y of this object."""
        return self.__add__(other)

    def __sub__(self, other):
        """Subtracts corresponding x and y  or an integer from this object."""
        try:
            return Coordinates(self.x - other.x, self.y - other.y)
        except AttributeError:  # Can also take a tuple (x, y)
            return Coordinates(self.x - other[0], self.y - other[1])

    def __rsub__(self, other):
        """Subtracts this object's x and y from a set of coordinates or an integer."""
        try:
            return Coordinates(other.x - self.x, other.y - self.y)
        except AttributeError:  # Can also take a tuple (x, y)
            return Coordinates(other[0] - self.x, other[1] - self.y)


class RawDisplay(object):
    pass
