#!/usr/bin/env python
""" Wintx API """

import errors
import interfaces

from Fastener import Fastener

# Imports for backwards compatibility
from Wintx import Wintx
from errors import *

__all__ = ['Fastener', 'Wintx', 'errors', 'interface']

def getWintxDict():
  """Returns dictionary of all wintx database columns
  Output:
    dictionary representing a record with default values
  """
  from datetime import datetime

  return {'latitude': 0.0, 'longitude': 0.0, 'time': datetime.now(),
      'datatype': '', 'varname': '', 'leveltype': '', 'level': 0,
      'value': None}

def getWintxIndexesDict():
  """Returns dictionary of all wintx indexed columns
  Output:
    dictionary representing a record with default values
  """
  # TODO change this function to return a list of keys
  from datetime import datetime

  return {'latitude': 0.0, 'longitude': 0.0, 'vertical': 0, 'time': datetime.now(),
      'datatype': '', 'varname': '', 'level': 0, 'leveltype': ''}

def checkQueryDict(query, restricted_columns=None):
  """Verifies a query dictionary is properly formed
  Input:
    query: dictionary of a query to be checked upon
    restricted_columns: list of column names that are not permitted
  """
  from datetime import datetime

  comparison_operands = ['<', '<=', '>', '>=', '==']

  if( query is None ):
    raise WintxMalformedQueryError('No query provided.')
  if( type(query) is not type({}) ):
    raise WintxMalformedQueryError('Query provided is not a dictionary.')

  if( restricted_columns is None ):
    restricted_columns = []
  elif( type(restricted_columns) is not type([]) and
        type(restricted_columns) is not type(()) ):
    raise WintxMalformedQueryError('Restricted query parameter list provided is not a list or tuple.')

  for column in query:
    if( column in restricted_columns ):
      raise WintxMalformedQueryError('Parameter \'%s\' is restricted for this query.' % column)
    if( column == 'latitude' or column == 'longitude' or column == 'level' ):
      if( type(query[column]) is not type(1) and
          type(query[column]) is not type(1.1) and
          type(query[column]) is not type({}) ):
        raise WintxMalformedQueryError('Invalid query comparison operand/operation(s) provided for parameter \'%s\'.' % column)
      if( type(query[column]) is type({}) ):
        for comparison in query[column]:
          if( comparison not in comparison_operands ):
            raise WintxMalformedQueryError('Invalid query comparison operation \'%s\' provided for parameter \'%s\'.' % (comparison, column))
          if( type(query[column][comparison]) is not type(1.1) and
              type(query[column][comparison]) is not type(1) ):
            raise WintxMalformedQueryError('Invalid query operand provided for the comparison operation \'%s\' under the parameter \'%s\'.' % (comparison, column))
    elif( column == 'leveltype' or column == 'leveltype' or column == 'datatype' or column == 'varname' ):
      if( type(query[column]) is not type('') and
          type(query[column]) is not type(u'') and
          type(query[column]) is not type([]) ):
        raise WintxMalformedQueryError('Invalid query comparison operation(s) provided for parameter \'%s\'.' % column)
      if( type(query[column]) is type([]) ):
        for parameter in query[column]:
          if( type(parameter) is not type('') and
              type(parameter) is not type(u'') ):
            raise WintxMalformedQueryError('Invalid query comparison operand \'%s\' provided for parameter \'%s\'.' % (query[column], column))
    elif( column == 'time' ):
      if( type(query[column]) is not type(datetime.now()) and
          type(query[column]) is not type({}) ):
        raise WintxMalformedQueryError('Invalid query comparison operation(s) provided for parameter \'%s\'.' % column)
      if( type(query[column]) is type({}) ):
        for comparison in query[column]:
          if( comparison not in comparison_operands ):
            raise WintxMalformedQueryError('Invalid query comparison operation \'%s\' provided for parameter \'%s\'.' % (comparison, column))
          if( type(query[column][comparison]) is not type(datetime.now()) ):
            raise WintxMalformedQueryError('Invalid query comparison operand \'%s\' provided for parameter \'%s\'.' % (comparison, column))
    else:
      raise WintxMalformedQueryError('Unknown query parameter \'%s\' found.' % column)

def checkSortList(sort_list, restricted_columns=None):
  """Verifies a sort list is properly formed
  Input:
    sort_column: list of tuples of column, direction strings
      example: [('column1','asc'), ('column2','dsc')]
    restricted_columns: list of column name strings
      example: ['column1', 'column2']
  """
  restricted = []
  if( restricted_columns is not None ):
    restricted = restricted_columns

  def __countColumn__(sort_list, column):
    count = 0
    for col in sort_list:
      if( col[0] == column ):
        count = count + 1
    return count

  for col_set in sort_list:
    if( type(col_set) is not type(()) ):
      raise WintxMalformedSortError('Sort column is not a tuple')
    if( type(col_set[0]) is not type('') and type(col_set[0]) is not type(u'') ):
      raise WintxMalformedSortError('Sort column name is not a string')
    if( type(col_set[1]) is not type('') and type(col_set[1]) is not type(u'') ):
      raise WintxMalformedSortError('Sort column direction is not a string')
    if( col_set[1] not in ['asc', 'dsc'] ):
      raise WintxMalformedSortError('Invalid sort column direction \'%s\'' % col_set[1])
    if( col_set[0] not in list(getWintxIndexesDict().keys()) ):
      raise WintxMalformedSortError('Invalid sort column name \'%s\'' % col_set[0])
    if( __countColumn__(sort_list, col_set[0]) > 1 ):
      raise WintxMalformedSortError('Sort column is listed twice')

def checkRecordDict(record):
  """Checks if supplied record is a properly formed Wintx dictionary"""
  from datetime import datetime

  if( not type(record) == type({}) ):
    raise WintxMalformedRecordError('Supplied record is not a dictionary.')

  for key in record:
    if( key == 'varname' ):
      if( type(record[key]) is not type('') and type(record[key]) is not type(u'') ):
        raise WintxMalformedRecordError('The variable name is not a string in the record dictionary.')
      else:
        pass
    elif( key == 'datatype' ):
      if( type(record[key]) is not type('') and type(record[key]) is not type(u'') ):
        raise WintxMalformedRecordError('The dataset name is not a string in the record dictionary.')
      else:
        pass
    elif( key == 'leveltype' ):
      if( type(record[key]) is not type('') and type(record[key]) is not type(u'') ):
        raise WintxMalformedRecordError('The level type is not a string in the record dictionary.')
      else:
        pass
    elif( key == 'level' ):
      if( type(record[key]) is not type(1) and type(record[key]) is not type(1.1) ):
        raise WintxMalformedRecordError('The level is not a numerical value in the record dictionary.')
      else:
        pass
    elif( key == 'latitude' ):
      if( type(record[key]) is not type(1) and type(record[key]) is not type(1.1) ):
        raise WintxMalformedRecordError('The latitude is not a numerical value in the record dictionary.')
      else:
        pass
    elif( key == 'longitude' ):
      if( type(record[key]) is not type(1) and type(record[key]) is not type(1.1) ):
        raise WintxMalformedRecordError('The longitude is not a numerical value in the record dictionary.')
      else:
        pass
    elif( key == 'value' ):
      if( type(record[key]) is not type(1) and type(record[key]) is not type(1.1) ):
        raise WintxMalformedRecordError('The value is not a numerical value in the record dictionary.')
      else:
        pass
    elif( key == 'time' ):
      if( type(record[key]) is not type(datetime.now()) ):
        raise WintxMalformedRecordError('The time is not a datetime object in the record dictionary.')
      else:
        pass
    else:
      raise WintxMalformedRecordError('The item \'%s\' in the record dictionary is not a valid entry.' % key)

  wintx_dict = getWintxDict()
  for key in wintx_dict.keys():
    if( key not in record.keys() ):
      raise WintxMalformedRecordError('Supplied record dictionary missing key %s' % key)

def getTimestamp(time):
  """Converts a datetime object into a timestamp
  Input:
    time: a datetime object
  Output:
    integer of seconds since a defined epoch
  """
  from datetime import datetime
  dtime = (time - datetime.utcfromtimestamp(0))
  timestamp = (dtime.days * 86400) + dtime.seconds
  return int(timestamp)

def getTime(timestamp):
  """Converts a timestamp into a datetime object
  Input:
    timestamp: integer of seconds since a defined epoch
  Output:
    datetime object representing the date-time
  """
  from datetime import datetime
  time = datetime.utcfromtimestamp(timestamp)
  return time
