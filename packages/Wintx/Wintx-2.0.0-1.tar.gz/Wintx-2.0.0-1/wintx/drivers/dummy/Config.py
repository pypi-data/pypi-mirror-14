#!/usr/bin/env python

from voluptuous import All, Length, Optional, Range, Required

class Config(object):
  CONFIG_SCHEMA = {
      'test_key': str,
      Required('test_required'): All(str, Length(min=1, max=10)),
      Required('test_required_int'): All(int, Range(min=50)),
      Optional('test_optional'): All(int, Range(min=0, max=100)),
  }
