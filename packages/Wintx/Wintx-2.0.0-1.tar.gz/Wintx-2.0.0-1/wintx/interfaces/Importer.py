#!/usr/bin/env python
"""Wintx abstract importer for importing lists of records."""
import wintx

from datetime import datetime
from Interface import Interface
from wintx.errors import WintxMalformedQueryError, WintxImportError

class Importer(Interface):
  """Abstract class for import records into Wintx"""

  def __init__(self, dataset_name, filter_dict={}, config_file=None):
    """Initializes Wintx importer."""
    if( config_file is None ):
      super(Importer, self).__init__()
    else:
      super(Importer, self).__init__(config_file=config_file)

    try:
      wintx.checkQueryDict(filter_dict, ['datatype'])
      self.filter_dict = filter_dict
    except WintxMalformedQueryError as err:
      raise WintxImportError(str(err))

    self.dataset_name = dataset_name
    self.insert_queue = []

  def getRecordDictionary(self):
    """Returns the record dictionary, obtained from Wintx."""
    return wintx.getWintxDict()

  def __compareDictFromQuery__(self, value, comparedict):
    """Checks the values of a comparison dictionary provided from a column in a query dictionary."""
    if( type(comparedict) is not type({}) ):
      return False

    result = True
    for comparison in comparedict:
      if( comparison == '<' ):
        result = result and (value < comparedict[comparison])
      elif( comparison == '<=' ):
        result = result and (value <= comparedict[comparison])
      elif( comparison == '>' ):
        result = result and (value > comparedict[comparison])
      elif( comparison == '>=' ):
        result = result and (value >= comparedict[comparison])
      elif( comparison == '==' ):
        result = result and (value == comparedict[comparison])
      else:
        raise WinxImportError('Invalid comparison operation \'%s\' provided.' % comparison)
    return result

  def __checkString__(self, key, value):
    """Checks if the value provided is valid under the key in the filter."""
    if( type(value) is not type('') and type(value) is not type(u'')):
      raise WintxImportError('Invalid value type for %s.' % key)

    if( not key in self.filter_dict ):
      return True

    if( type(self.filter_dict[key]) is type('') ):
      return value == self.filter_dict[key]
    else:
      return value in self.filter_dict[key]

  def __checkInt__(self, key, value, type_date=False):
    """Checks if the value provided is valid under the key in the filter."""
    if( type_date ):
      if( type(value) is not type(datetime.now()) ):
        raise WintxImportError('Invalid value type for %s.' % key)
    else:
      if( type(value) is not type(1) and type(value) is not type(1.1) ):
        raise WintxImportError('Invalid value type for %s.' % key)

    if( not key in self.filter_dict ):
      return True

    if( type(self.filter_dict[key]) is type({}) ):
      return self.__compareDictFromQuery__(value, self.filter_dict[key])
    else:
      return value == self.filter_dict[key]

  def checkVariableName(self, varname):
    """Checks if the variable name provided is valid according to the filter."""
    return self.__checkString__('varname', varname)

  def checkLatitude(self, latitude):
    """Checks if the latitude provided is valid according to the filter."""
    return self.__checkInt__('latitude', latitude)

  def checkLongitude(self, longitude):
    """Checks if the longitude provided is valid according to the filter."""
    return self.__checkInt__('longitude', longitude)

  def checkLevel(self, level):
    """Checks if the level provided is valid according to the filter."""
    return self.__checkInt__('level', level)

  def checkLevelType(self, leveltype):
    """Checks if the level type provided is valid according to the filter."""
    return self.__checkString__('leveltype', leveltype)

  def checkTime(self, time_value):
    """Checks if the time provided is valid according to the filter."""
    return self.__checkInt__('time', time_value, type_date=True)

  def addRecord(self, latitude, longitude, leveltype, level, varname, time_value, value):
    """Adds a record to the insert queue."""
    wintx_dict = self.getRecordDictionary()

    if( not self.checkLatitude(latitude) or
        not self.checkLongitude(longitude) or
        not self.checkLevel(level) or
        not self.checkLevelType(leveltype) or
        not self.checkVariableName(varname) or
        not self.checkTime(time_value) ):
      return None
    
    wintx_dict['latitude'] = latitude
    wintx_dict['longitude'] = longitude
    wintx_dict['leveltype'] = leveltype
    wintx_dict['level'] = level
    wintx_dict['varname'] = varname
    wintx_dict['datatype'] = self.dataset_name
    wintx_dict['time'] = time_value
    wintx_dict['value'] = value

    wintx.checkRecordDict(wintx_dict)
    self.insert_queue.append(wintx_dict)

  def addRecordDict(self, record_dict):
    """Adds a pre-constructed record dictionary to the insert queue."""
    wintx.checkRecordDict(record_dict)
    self.insert_queue.append(record_dict)

  def importRecords(self):
    """Imports the records from the insert queue."""
    results = self.fastener.insertRecords(self.insert_queue)
    self.insert_queue = []
    return results
