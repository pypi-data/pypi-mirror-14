#!/usr/bin/env python
"""Dummy driver for unittesting."""

class Driver(object):

  def __init__(self, test_required=None, test_required_int=None):
    self.value = 'success'
    self.abort_value = 'abort'
    self.test_required = test_required
    self.test_required_int = test_required_int
    pass

  def testFunction(self):
    return True

  def testValue(self, value):
    return value
