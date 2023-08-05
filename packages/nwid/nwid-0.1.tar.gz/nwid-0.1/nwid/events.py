#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             events.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       02/06/2016
#

"""
nwid.events
~~~~~~~~~~~

This module contains the Event object and the EventHandler mixin as well as the
EventDict and HandlerList data structures.
"""

from __future__ import absolute_import

from collections import namedtuple

class HandlerList(object):
    """This class defines an ordered list of a namedtuple with a callback_func and priority.
    The list is ordered based off the priority with lower integers coming
    before higher integers. This list is intended to be used as the list of
    handlers for one particular event."""

    Item = namedtuple('HandlerListItem', ['callback_func', 'priority'])

    def __init__(self, callback_func=None, priority=50):
        """Initializes an empty list. Can optionally add an item at initialization."""
        self._list = []
        if callback_func:
            self.add(callback_func, priority)

    def __len__(self):
        """Returns the length of the list."""
        return len(self._list)

    def add(self, callback_func, priority=50):
        """Inserts item of (callback_func, priority) into the list based on priority."""
        new_item = self.Item(callback_func, priority)
        for index, item in enumerate(self._list):
            if priority < item.priority:
                self._list = self._list[:index] + [new_item] + self._list[index:]
                break
        else:
            self._list.append(self.Item(callback_func, priority))

    def remove(self, callback_func=None):
        """Removes (all) item(s) with callback_func."""
        if not callback_func:
            raise TypeError('HandlerList.remove() method must take either a callback_func or an identifier.')
        for item in self._list:
            if item.callback_func == callback_func:
                self._list.remove(item)

    def __getitem__(self, index):
        """Returns _only_ the callback_func. Priority is only intended to be used internally."""
        return self._list[index].callback_func
