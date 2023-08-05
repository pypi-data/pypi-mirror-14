#!/usr/bin/env python

from Interface import Interface
from wintx.errors import *

class Deleter(Interface):
  """Whacka"""

  def remove(self, query_dict):
    """Removes records from the database matching the query"""
    # TODO
    pass

