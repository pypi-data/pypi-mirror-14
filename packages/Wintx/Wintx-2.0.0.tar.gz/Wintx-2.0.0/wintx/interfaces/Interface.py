#!/usr/bin/env python

from wintx.Fastener import Fastener

class Interface(object):
  """Interface Parent Module"""

  def __init__(self, config_file='/etc/wintx.conf'):
    self.fastener = Fastener(config_file)
