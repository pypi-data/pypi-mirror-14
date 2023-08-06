#!/usr/bin/env python
"""MySQL driver for Wintx"""

import hashlib
import mysql.connector
import wintx

from mysql.connector import errorcode, Error as MySQLClientError, IntegrityError, InterfaceError
from MySQLError import MySQLError
from wintx.errors import WintxDatabaseError

class Driver(object):
  """Driver class"""

  def __init__(self, host='localhost', user='', password='', database='', timeout='3',\
      port=3306, use_ssl=False, ssl_ca=None, ssl_cert=None, ssl_key=None, compress=False):
    self.connection = None
    self.mysql_config = {
        'host': host,
        'user': user,
        'port': port,
        'password': password,
        'database': database,
        'raise_on_warnings': False,
        'autocommit': False,
    }

    if( use_ssl ):
      if( ssl_ca is not None ):
        self.mysql_config['ssl_verify_cert'] = True
        self.mysql_config['ssl_ca'] = ssl_ca
      if( ssl_cert is not None ):
        self.mysql_config['ssl_cert'] = ssl_cert
      if( ssl_key is not None ):
        self.mysql_config['ssl_key'] = ssl_key

    self.connection = mysql.connector.connect(**self.mysql_config)
    self.cursor = None

  def __destructor__(self):
    """Class destruction method"""
    if( self.connection is not None ):
      try:
        self.connection.close()
      except MySQLClientError as err:
        pass # gracefully

  def __startTransaction__(self, snapshot=False, readonly=False):
    """Creates a global cursor object
       MAINTAINED FOR BACKWARDS COMPATIBILITY
    """
    if( self.cursor is None ):
      try:
        self.connection.start_transaction(consistent_snapshot=snapshot, readonly=readonly)
      except ValueError as err:
        pass

      self.cursor = self.connection.cursor()

  def __endTransaction__(self, commit=False):
    """Ends a transaction and closes the cursor
       MAINTAINED FOR BACKWARDS COMPATIBILITY
    """
    if( self.cursor is not None ):
      # Clear any results that may exist
      for result in self.cursor:
        if( type(result) == type(()) ):
          break
        elif( result.with_rows ):
          result.fetchall()

      # Close cursor
      self.cursor.close()
      self.cursor = None

      # End transaction
      if( commit ):
        self.connection.commit()
      else:
        self.connection.rollback()

  def __prepareQuery__(self, query_dict, polygonWhere=None):
    """Convert a query dictionary to an SQL statement
    Input:
      query_dict: dictionary representing a query
      polygon: list of corrected GIS points
    Output:
      String representing SQL statement
    """
    query_table_wheres = {
        'location': [],
        'variable': [],
        'level': [],
        'data': []
    }

    if( polygonWhere is not None ):
      query_table_wheres['location'].append(polygonWhere)

    for key in query_dict:
      column_name = ''
      column_eq = ''
      where_column = ''

      if( key=='time' ):
        column_name = 'Data.timestamp'
        column_eq = '='
      elif( key=='latitude' ):
        column_name = 'X(Location.lat_lon)'
        column_eq = '='
      elif( key=='longitude' ):
        column_name = 'Y(Location.lat_lon)'
        column_eq = '='
      elif( key=='level' ):
        column_name = 'Level.level'
        column_eq = '='
      elif( key=='leveltype' ):
        column_name = 'Level.level_type'
        column_eq = 'LIKE'
      elif( key=='datatype' ):
        column_name = 'Variable.datatype'
        column_eq = 'LIKE'
      elif( key=='varname' ):
        column_name = 'Variable.variable_name'
        column_eq = 'LIKE'
      else:
        raise WintxDatabaseError('Invalid column name found in query. '\
            'Column "%s" does not exist.' % key)

      where_columns = []
      if( type(query_dict[key]) == type({}) ):
        for param in query_dict[key]:
          comparison = ''
          if( param=='>' ):
            comparison = '>'
          if( param=='>=' ):
            comparison = '>='
          elif( param=='<' ):
            comparison = '<'
          elif( param=='<=' ):
            comparison = '<='
          elif( param=='==' ):
            comparison = column_eq

          value = query_dict[key][param]
          if( key=='time' ):
            value = wintx.getTimestamp(value)

          if( comparison=='LIKE' ):
            value = '"%s"' % value
          where_column = "%s %s %s" % (column_name, comparison, value)
          where_columns.append(where_column)
      elif( type(query_dict[key]) == type([]) ):
        where_column = "%s IN ('%s')" % (column_name, "', '".join(query_dict[key]))
        where_columns.append(where_column)
      else:
        value = query_dict[key]
        if( key=='time' ):
          value = wintx.getTimestamp(value)

        if( column_eq=='LIKE' ):
          value = '"%s"' % value
        where_column = "%s %s %s" % (column_name, column_eq, value)
        where_columns.append(where_column)

      if( key=='level' or key=='leveltype' ):
        query_table_wheres['level'].extend(where_columns)
      elif( key=='latitude' or key=='longitude' ):
        query_table_wheres['location'].extend(where_columns)
      elif( key=='datatype' or key=='varname' ):
        query_table_wheres['variable'].extend(where_columns)
      elif( key=='time' ):
        query_table_wheres['data'].extend(where_columns)

    data_subquery_where = []
    if( len(query_table_wheres['location']) > 0 ):
      data_subquery_where.append('Data.loc_id IN (SELECT Location.loc_id FROM Location WHERE %s)' % ' AND '.join(query_table_wheres['location']))
    if( len(query_table_wheres['variable']) > 0 ):
      data_subquery_where.append('Data.var_id IN (SELECT Variable.var_id FROM Variable WHERE %s)' % ' AND '.join(query_table_wheres['variable']))
    if( len(query_table_wheres['level']) > 0 ):
      data_subquery_where.append('Data.level_id IN (SELECT Level.level_id FROM Level WHERE %s)' % ' AND '.join(query_table_wheres['level']))
    if( len(query_table_wheres['data']) > 0 ):
      data_subquery_where.append(' AND '.join(query_table_wheres['data']))

    data_subquery = 'SELECT * FROM Data'
    if( len(data_subquery_where) > 0 ):
      data_subquery = '%s WHERE %s' % (data_subquery, ' AND '.join(data_subquery_where))
    query = 'SELECT Data.timestamp, X(Location.lat_lon), Y(Location.lat_lon), Level.level, ' \
      'Level.level_type, Variable.datatype, Variable.variable_name, Data.data FROM ' \
      '(%s) AS Data INNER JOIN Location ON Data.loc_id=Location.loc_id ' \
      'INNER JOIN Level ON Data.level_id=Level.level_id ' \
      'INNER JOIN Variable ON Data.var_id=Variable.var_id' % data_subquery

    return query

  def __prepareSort__(self, sort_list):
    """Convert a sort list into an ORDER BY statement
    Inputs:
      sort_list: list of column, direction tuples
    Output:
      String representing ORDER BY statement
    """
    order_by_list = []

    for key, direction in sort_list:
      column_name = ''
      if( key=='time' ):
        column_name = 'Data.timestamp'
      elif( key=='latitude' ):
        column_name = 'X(Location.lat_lon)'
      elif( key=='longitude' ):
        column_name = 'Y(Location.lat_lon)'
      elif( key=='level' ):
        column_name = 'Level.level'
      elif( key=='leveltype' ):
        column_name = 'Level.level_type'
      elif( key=='datatype' ):
        column_name = 'Variable.datatype'
      elif( key=='varname' ):
        column_name = 'Variable.variable_name'
      else:
        raise WintxDatabaseError('Invalid column name found in query. '\
            'Column "%s" does not exist.' % key)

      direction = ''
      if( direction == 'asc' ):
        direction = 'ASC'
      elif( direction == 'dsc' ):
        direction = 'DSC'

      order_by_list.append('%s %s' % (column_name, direction))

    return 'ORDER BY %s' % ', '.join(order_by_list)

  def __preparePolygon__(self, polygon):
    """Convert a polygon into a within where search
    Inputs:
      polygon: list of latitude, longitude sets
    Output:
      String representing within where SQL clause
    """
    formatted_points = []
    for point in polygon:
      formatted_points.append('%.20f %.20f' % (point[0], point[1]))

    return 'ST_Contains(GeomFromText("POLYGON((%s))"), `lat_lon`)' % (', '.join(formatted_points))

  def __convertRecordToWintxDict__(self, record):
    """Converts a record from the database into a Wintx record dictionary
    Inputs:
      record: list of record values from the database in the order time, latitude,
              longitude, level, leveltype, datatype, varname, value
    Output:
      Wintx record dictionary
    """
    return {'time': wintx.getTime(record[0]), 'latitude': record[1],
        'longitude': record[2], 'level': record[3], 'leveltype': record[4],
        'datatype': record[5], 'varname': record[6], 'value': record[7]}

  def query(self, query_dict, sort_list=None):
    """ """
    if( sort_list is not None ):
      query = '%s %s' % (self.__prepareQuery__(query_dict), self.__prepareSort__(sort_list))
    else:
      query = self.__prepareQuery__(query_dict)

    cursor = self.connection.cursor()
    cursor.execute(query)
    results = []
    for record in cursor.fetchall():
      results.append(self.__convertRecordToWintxDict__(record))
    cursor.close()
    self.connection.rollback()

    return results

  def queryWithin(self, polygon, query_dict, sort_list=None):
    """ """
    polygon_where = self.__preparePolygon__(polygon)
    if( sort_list is not None ):
      query = '%s %s' % (self.__prepareQuery__(query_dict, polygonWhere=polygon_where), self.__prepareSort__(sort_list))
    else:
      query = self.__prepareQuery__(query_dict, polygonWhere=polygon_where)

    cursor = self.connection.cursor()
    cursor.execute(query)
    results = []
    for record in cursor.fetchall():
      results.append(self.__convertRecordToWintxDict__(record))
    cursor.close()
    self.connection.rollback()

    return results

  def queryMetadata(self, sort_list, query_dict):
    """Query for metadata information provided in the sort list
    Inputs:
      sort_list: list of column, direction tuples that represent metadata columns to retrieve
      query_dict: Wintx query dictionary representing search parameters
    Ouput:
      list of dictionaries keyed by requested columns
    """
    pass

  def getVarnamesAtTime(self, time, time_end=None):
    """Retreives variable names that are valid at a given time
    """
    results = None
    query_templ = "SELECT Data.timestamp, Variable.datatype, Variable.variable_name FROM " \
        "(SELECT DISTINCT Data.timestamp, Data.var_id FROM Data %s) AS Data " \
        "INNER JOIN Variable ON Data.var_id=Variable.var_id " \
        "ORDER BY Data.timestamp, Variable.datatype, Variable.variable_name"

    where_clause = "WHERE Data.timestamp=%d" % wintx.getTimestamp(time)
    if( time_end is not None ):
      where_clause = "WHERE Data.timestamp BETWEEN %d AND %d" % (wintx.getTimestamp(time), wintx.getTimestamp(time_end))

    query = query_templ % where_clause

    variables_raw = None
    cursor = self.connection.cursor()
    cursor.execute(query)
    variables_raw = cursor.fetchall()
    cursor.close()
    self.connection.rollback()

    variables_fixed = {}
    for var in variables_raw:
      time = wintx.getTime(var[0])
      if( time not in variables_fixed ):
        variables_fixed[time] = []
      variables_fixed[time].append({'varname': var[2], 'datatype': var[1]})

    return variables_fixed

  def getTimes(self):
    """Retreives the unique timestamps stored in the database"""
    results = None
    cursor = self.connection.cursor()
    cursor.execute("SELECT DISTINCT(`timestamp`) FROM Data")
    results = cursor.fetchall()
    cursor.close()
    self.connection.rollback()

    timestamps = set()
    for timestamp in results:
      timestamps.add(timestamp[0])

    final_times = []
    for timestamp in timestamps:
      final_times.append(wintx.getTime(timestamp))

    final_times.sort()
    return final_times

  def getVariables(self):
    """Retreives the variables stored in the database"""
    results = None
    cursor = self.connection.cursor()
    cursor.execute('SELECT DISTINCT(`variable_name`) FROM `Variable` ORDER BY `variable_name` ASC')
    results = cursor.fetchall()
    cursor.close()
    self.connection.rollback()

    variables = []
    for r in results:
      variables.append(r[0])

    return variables

  def getLevels(self):
    """Retreives the levels stored in the database"""
    results = None
    cursor = self.connection.cursor()
    cursor.execute('SELECT `level`, `level_type` FROM `Level` ORDER BY `level_type`, `level` ASC')
    results = cursor.fetchall()
    cursor.close()
    self.connection.rollback()

    levels = []
    for r in results:
      levels.append((r[1], r[0]))

    return levels

  def getLocationCorners(self):
    """Retreives the corners of the stored latitude/longitude values in the database"""
    results = None
    cursor = self.connection.cursor()
    cursor.execute('SELECT MAX(X(`lat_lon`)) AS `MAX_LAT`, ' \
        'MIN(X(`lat_lon`)) AS `MIN_LAT`, MAX(Y(`lat_lon`)) AS `MAX_LON`, ' \
        'MIN(Y(`lat_lon`)) AS `MIN_LON` FROM `Location`')
    results = cursor.fetchall()
    cursor.close()
    self.connection.rollback()

    lat_max = results[0][0]
    lat_min = results[0][1]
    lon_max = results[0][2]
    lon_min = results[0][3]

    corners = {
        'topright':    (lat_max, lon_max),
        'topleft':     (lat_max, lon_min),
        'bottomright': (lat_min, lon_max),
        'bottomleft':  (lat_min, lon_min),
    }

    return corners

  def getDatabaseStats(self):
    """Retreives the size of the database and tables"""
    stat_dict = {
        'totalSize': 0,
        'numRecords': 0,
        'avgRecordSize': 0,
        'numIndexes': 0,
        'indexSize': 0,
        'indexes': []}

    stats = {
        'database': stat_dict.copy(),
        'tables': {}}

    cursor = self.connection.cursor()
    cursor.execute('SHOW TABLE STATUS FROM %s' % self.mysql_config['database'])
    tables = cursor.fetchall()
    cursor.close()
    self.connection.rollback()

    for table in tables:
      if( table[0] == u'Data' ):
        stats['database']['numRecords'] = table[4]
        stats['database']['avgRecordSize'] = table[5]
      stats['database']['totalSize'] = stats['database']['totalSize'] + table[6]
      stats['database']['indexSize'] = stats['database']['indexSize'] + table[8]
      stats['tables'][table[0]] = stat_dict.copy()
      stats['tables'][table[0]]['totalSize'] = table[6]
      stats['tables'][table[0]]['numRecords'] = table[4]
      stats['tables'][table[0]]['avgRecordSize'] = table[5]
      stats['tables'][table[0]]['indexSize'] = table[8]

    return stats

  def insertRecords(self, records):
    """Inserts a list of Wintx records
    Inputs:
      records: list of Wintx record dictionaries
    Outputs:
      dictionary of errors, duplicate records, and inserted records
    """
    variable_values = set()
    location_values = set()
    level_values = set()

    variables = {}
    locations = {}
    levels = {}

    inserted_records = 0
    duplicate_records = []

    for record in records:
      variable_values.add((record['datatype'], record['varname']))
      location_values.add((record['latitude'], record['longitude']))
      level_values.add((record['level'], record['leveltype']))

    cursor = self.connection.cursor()
    try:
      for variable in variable_values:
        cursor.execute('SELECT var_id FROM Variable WHERE datatype LIKE "%s" AND variable_name LIKE "%s"' % (variable[0], variable[1]))
        var_id = cursor.fetchone()
        if( var_id is None ):
          cursor.execute('INSERT Variable (datatype, variable_name) VALUES ("%s", "%s")' % (variable[0], variable[1]))
          var_id = cursor.lastrowid
        else:
          var_id = var_id[0]
        variables[variable] = var_id

      for level in level_values:
        cursor.execute('SELECT level_id FROM Level WHERE level=%d AND level_type LIKE "%s"' % (level[0], level[1]))
        level_id = cursor.fetchone()
        if( level_id is None ):
          cursor.execute('INSERT Level (level, level_type) VALUES (%d, "%s")' % (level[0], level[1]))
          level_id = cursor.lastrowid
        else:
          level_id = level_id[0]
        levels[level] = level_id

      for location in location_values:
        cursor.execute('SELECT loc_id FROM Location WHERE lat_lon = GeomFromText("POINT(%.20f %.20f)")' % (location[0], location[1]))
        loc_id = cursor.fetchone()
        if( loc_id is None ):
          cursor.execute('INSERT Location(lat_lon) VALUES ((GeomFromText("POINT(%.20f %.20f)")))' % (location[0], location[1]))
          loc_id = cursor.lastrowid
        else:
          loc_id = loc_id[0]
        locations[location] = loc_id

      self.connection.commit()
    except MySQLClientError as err:
      self.connection.rollback()
      raise MySQLError(err)
    cursor.close()

    cursor = self.connection.cursor()
    try:
      for record in records:
        var_id = variables[(record['datatype'], record['varname'])]
        loc_id = locations[(record['latitude'], record['longitude'])]
        level_id = levels[(record['level'], record['leveltype'])]
        timestamp = wintx.getTimestamp(record['time'])
        data_id = hashlib.md5('%d-%s-%s-%s' % (timestamp, loc_id, level_id, var_id)).hexdigest()

        try:
          cursor.execute('INSERT Data (data_id, timestamp, loc_id, level_id, var_id, data) VALUES(UNHEX("%s"), %d, %s, %s, %s, %.20f)' % (data_id, timestamp, loc_id, level_id, var_id, record['value']))
          inserted_records = inserted_records + 1
        except IntegrityError as err:
          if( err.errno == errorcode.ER_DUP_KEY or
              err.errno == errorcode.ER_DUP_ENTRY or
              err.errno == errorcode.ER_DUP_KEYNAME or
              err.errno == errorcode.ER_DUP_ARGUMENT or
              err.errno == errorcode.ER_DUP_UNIQUE ):
            duplicate_records.append(record)
          else:
            raise err
        except InterfaceError as err:
          # There is a bug where MySQL Error classes can not parse binary data
          # This catches the error raised by the bug to ensure it is a duplicate error
          if( 'Duplicate entry' in str(err) ):
            duplicate_records.append(record)
          else:
            raise err
        except MySQLClientError as err:
          if( err.errno == errorcode.ER_DUP_KEY ):
            duplicate_records.append(record)
          else:
            raise err

      self.connection.commit()
    except MySQLClientError as err:
      self.connection.rollback()
      raise err
      raise MySQLError(err)
    cursor.close()

    return {'insertedRecords': inserted_records,
            'duplicateRecords': duplicate_records,
            'errors': []
           }
