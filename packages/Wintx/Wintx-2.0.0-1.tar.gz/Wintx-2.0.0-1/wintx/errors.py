#!/usr/bin/env python

class WintxError(Exception):
  """Base error class for Wintx errors"""
  pass

class WintxConfigError(WintxError):
  """Error class handling configuration errors"""
  pass

class WintxDatabaseError(WintxError):
  """Error class handling database errors"""
  pass

class WintxDriverError(WintxError):
  """Error class handling driver errors"""
  pass

class WintxFunctionNotImplemented(WintxDriverError):
  """Error class handling functions not supported by a driver"""

class WintxUserError(WintxError):
  """Error class handling user based errors"""
  pass

class WintxMalformedPolygonError(WintxUserError):
  """Error class handling malformed polygons"""
  pass

class WintxMalformedQueryError(WintxUserError):
  """Error class handling malformed queries"""
  pass

class WintxMalformedRecordError(WintxUserError):
  """Error class handling malformed records"""
  pass

class WintxMalformedSortError(WintxUserError):
  """Error class handling malformed sort lists"""
  pass

class WintxImportError(WintxError):
  """Error class handling import issues"""
  pass
