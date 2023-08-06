#!/usr/bin/env python
import wintx

from Interface import Interface
from wintx.errors import WintxMalformedPolygonError

class Query(Interface):
  """Module for querying Wintx"""

  def __checkPolygon__(self, polygon):
    """Verifies a polygon is properly formed
    Input:
      polygon: list of tuples of latitude, longitude paris
        example: [(1.0, 2.0), (1.0, 1.0), (2.0, 1.0)]
    """
    for geo_set in polygon:
      if( type(geo_set) is not type(()) and type(geo_set) is not type([]) ):
        raise WintxMalformedPolygonError('Point is not a tuple')
      if( type(geo_set[0]) is not type(1) and type(geo_set[0]) is not type(1.0) and
          type(geo_set[1]) is not type(1) and type(geo_set[1]) is not type(1.0) ):
        raise WintxMalformedPolygonError('Point is not a numerical pair')

  def __fixPolygon__(self, polygon, reverse_points=False):
    """Ensures the last point is equal to the first, reverse points if necessary
    Input:
      polygon: list of tuples of latitude, longitude paris
        example: [(1.0, 2.0), (1.0, 1.0), (2.0, 1.0)]
      reverse_points: boolean whether to flip every point
        example: if true point (1, 2) will be interpreted as (2, 1)
    """
    poly = []
    for point in polygon:
      if( reverse_points ):
        poly.append((point[1], point[0]))
      else:
        poly.append((point[0], point[1]))

    if( poly[-1] != poly[0] ):
      poly.append(poly[0])

    return poly

  def query(self, query_dict, sort_column=None):
    """Searches the database for geospatial data
    Input:
      query_dict: dictionary forming a query request
      sort_column: column, direction tuple list in sort order
        example: [('time','asc'), ('leveltype','dsc')]
    Output:
      list of finalized record dictionaries
    """
    wintx.checkQueryDict(query_dict)
    if( sort_column is not None ):
      wintx.checkSortList(sort_column)

    return self.fastener.query(query_dict, sort_column)

  def queryWithin(self, polygon, query_dict, reverse_points=False, sort_column=None):
    """A spatial query finding all points within a polygon.
    Inputs:
      polygon: point tuple list ordered by sequence of points forming a shape
        example: [(1, 1), (1, 2), (2, 2), (2, 1)]
      query_dict: dictionary forming a query request
      reverse_points: boolean specifying if each point tuple needs to be flipped
        example: if true and given point (1, 2), point will be read as (2, 1)
      sort_column: column, direction tuple list in order of complex sort
        example: [('time', 'asc'), ('leveltype', 'asc'), ('level', 'dsc')]
    Outputs:
      list: of finalized record dictionaries
    """
    wintx.checkQueryDict(query_dict, ['latitude', 'longitude'])
    if( sort_column is not None ):
      wintx.checkSortList(sort_column, ['latitude', 'longitude'])

    self.__checkPolygon__(polygon)
    query_polygon = self.__fixPolygon__(polygon, reverse_points=reverse_points)

    return self.fastener.queryWithin(query_polygon, query_dict, sort_column)

  def getTimes(self):
    """Retreives the date/times from the database
    Output:
      list of datetime objects
    """
    return self.fastener.getTimes()

  def getVariables(self):
    """Retreives the unique variables from the database
    Output:
      list of dictionaries of variable, datatype combinations
    """
    return self.fastener.getVariables()

  def getLevels(self):
    """Retreives the unique levels from the database
    Output:
      list of dictionaries of level, leveltype combinations
    """
    return self.fastener.getLevels()

  def getLocationCorners(self):
    """Retreives the latitude/longitude corners in teh database
    Output:
      dictionary {'topleft': 1, 'topright': 1, 'bottomleft': 1, 'bottomright': 1}
    """
    return self.fastener.getLocationCorners()

  def getDatabaseStats(self):
    """Retreives the size of the database and tables, different for every driver
    Output:
      dictionary of database stats
    """
    return self.fastener.getDatabaseStats()

  def getVarnamesAtTime(self, time, time_end=None):
    """Retreives variable names that exist at a given time
    Output:
      list of dictionaries with variable, datatype combinations
      example: [{'varname': 'variable', 'datatype': 'type1'}]
    """
    return self.fastener.getVarnamesAtTime(time, time_end)
