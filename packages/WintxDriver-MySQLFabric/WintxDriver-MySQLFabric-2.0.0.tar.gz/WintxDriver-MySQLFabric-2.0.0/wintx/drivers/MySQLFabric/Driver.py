#!/usr/bin/env python
"""MySQL Fabric driver for Wintx"""

# MySQL Fabric
import hashlib
import mysql.connector
import Queue

from datetime import datetime
from mysql.connector import fabric, pooling
from mysql.connector import ProgrammingError, IntegrityError, InterfaceError, Error as MySQLError
from threading import Lock, Thread
from wintx.errors import WintxDatabaseError

class Driver(object):
  """MySQL Fabric Wintx Driver"""

  QUERY_INSERT_LOCATION = 'INSERT `Location`(`lat_lon`) VALUES'
  QUERY_INSERT_LOCATION_VALUE = '(GeomFromText(\'POINT(%(latitude).20f %(longitude).20f)\'))'
  QUERY_INSERT_LEVEL =    'INSERT `Level`(`level`, `level_type`) VALUES'
  QUERY_INSERT_LEVEL_VALUE = '(%(level)d, \'%(leveltype)s\')'
  QUERY_INSERT_VARIABLE = 'INSERT `Variable`(`datatype`, `variable_name`) VALUES'
  QUERY_INSERT_VARIABLE_VALUE = '(\'%(datatype)s\', \'%(varname)s\')'
  QUERY_INSERT_DATA =     'INSERT INTO `Data`(`data_id`, `timestamp`, `loc_id`, `level_id`, `var_id`, `data`) VALUES'
  QUERY_INSERT_DATA_VALUE = '(UNHEX(\'%(data_id)s\'), %(timestamp)d, %(loc_id)d, %(level_id)d, %(var_id)d, %(value).20f)'

  QUERY_SELECT_LOCATION =  'SELECT `loc_id`, X(`lat_lon`), Y(`lat_lon`) FROM `Location`'
  QUERY_SELECT_LEVEL =     'SELECT `level_id`, `level`, `level_type` FROM `Level`'
  QUERY_SELECT_VARIABLE =  'SELECT `var_id`, `datatype`, `variable_name` FROM `Variable`'
  QUERY_SELECT_GTID_WAIT = 'SELECT WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS(\'%s\', 0)'

  QUERY_SELECT_LOCATION_ID = 'SELECT `loc_id` FROM `Location` WHERE `lat_lon` = GeomFromText(\'POINT(%(latitude).20f %(longitude).20f)\')'
  QUERY_SELECT_LEVEL_ID =    'SELECT `level_id` FROM `Level` WHERE `level`=%(level)d AND `level_type` LIKE \'%(leveltype)s\''
  QUERY_SELECT_VARIABLE_ID = 'SELECT `var_id` FROM `Variable` WHERE `datatype` LIKE \'%(datatype)s\' AND `variable_name` LIKE \'%(varname)s\''

  QUERY_SELECT_DATA =     'SELECT Data.timestamp, X(Location.lat_lon), Y(Location.lat_lon), Level.level, ' \
      'Level.level_type, Variable.datatype, Variable.variable_name, Data.data FROM ' \
      'Data INNER JOIN Location ON Data.loc_id=Location.loc_id ' \
      'INNER JOIN Level ON Data.level_id=Level.level_id ' \
      'INNER JOIN Variable ON Data.var_id=Variable.var_id'

  def __init__(self, host='127.0.0.1', port=32274, user='user', password='abc123', \
               database_name='wintx', fabric_user='user', fabric_password='abc123', \
               global_group='global', shard_groups=[], \
               timeout=60, poolsize=5, bulkquantity=1000, attempts=3):
    """MySQL Fabric Initialization
    Input:
      host: string of hostname of the MySQL Fabric server
      port: integer of port of the MySQL Fabric server
      user: string of MySQL username
      password: string of MySQL password
      database_name: string of the name of the MySQL database
      fabric_user: string of MySQL username
      fabric_password: string of MySQL password
      global_group: string of MySQL Fabric global group name
      shard_group: list of strings of MySQL Fabric shard group names
      timeout: integer of seconds before a connection times out
      poolsize: number of threads to perform queries on
      bulkquantity: number of records to import at a time
      attempts: number of times to retry a connection
    """
    self.db_name = database_name
    self.shard_groups = shard_groups
    self.global_group = global_group
    self.poolsize = poolsize
    self.bulkquantity = bulkquantity
    self.connection_attempts = attempts
    self.db_config = {
        'fabric': {
          'username': fabric_user,
          'password': fabric_password,
          'host': host,
          'port': port
        },
        'user': user,
        'password': password,
        'database': self.db_name,
        'connection_timeout': timeout,
        'compress': False,
        'raise_on_warnings': False,
        'autocommit': True,
    }

    self.connection = None
    self.cursor = None
    self.meta_locations = {}
    self.meta_variables = {}
    self.meta_levels = {}

    self.meta_lock = Lock()
    self.connect()

  def __del__(self):
    """Deconstructor to handle closing a persistent connection"""
    # Try to close the connection, silently fail if connection is not initialized
    try:
      if( self.connection is not None and self.isConnectedToServer() ):
        self.connection.disconnect()
    except Exception as err:
      pass

  def __getTime__(self, timestamp):
    return wintx.getTime(timestamp)

  def __getTimestamp(self, time):
    return wintx.getTimestamp(time)

  def __setGlobalConnectionProperty__(self, connection=None, readonly=False):
    """Sets the properties of a connection for a global query."""
    if( connection is None ):
      connection = self.connection

    mode = fabric.MODE_READWRITE
    if( readonly ):
      mode = fabric.MODE_READONLY

    connection.set_property(
        mode=mode,
        scope=fabric.SCOPE_GLOBAL,
        group=self.global_group,
        tables=None,
        key=None,
    )

    self.connectDbServer(connection)

  def __setLocalConnectionProperty__(self, key, connection=None, readonly=False):
    """Sets the properties of a connection for a sharded query."""
    if( connection is None ):
      connection = self.connection

    mode = fabric.MODE_READWRITE
    if( readonly ):
      mode = fabric.MODE_READONLY

    connection.set_property(
        mode=mode,
        scope=fabric.SCOPE_LOCAL,
        group=None,
        tables=['%s.Data' % self.db_config['database']],
        key=key,
    )

    self.connectDbServer(connection)

  # TODO Check if duplicate of setLocalConnectionProperty with extra parameter
  def __setLocalConnectionGroupProperty__(self, group, connection=None, readonly=False):
    """Sets the group property of a connection for a sharded query."""
    if( connection is None ):
      connection = self.connection

    mode = fabric.MODE_READWRITE
    if( readonly ):
      mode = fabric.MODE_READONLY

    connection.set_property(
        mode=mode,
        scope=fabric.SCOPE_LOCAL,
        group=group,
        tables=None,
        key=None,
    )

    self.connectDbServer(connection)

  def __getTimestamp__(self, time):
    """Converts a datetime into a timestamp."""
    #timestamp = (time - datetime.utcfromtimestamp(0)).total_seconds()
    dtime = (time - datetime.utcfromtimestamp(0))
    timestamp = (dtime.days * 86400) + dtime.seconds
    return int(timestamp)

  def __getTime__(self, timestamp):
    """Converts a timestamp into a datetime object."""
    time = datetime.utcfromtimestamp(timestamp)
    return time

  def connect(self):
    """Makes a connection to the MySQL Fabric server."""
    attempts = self.connection_attempts
    for i in range(1, attempts + 1):
      try:
        self.connection = mysql.connector.connect(**self.db_config)
        break
      except InterfaceError as err:
        if( i < attempts ):
          continue
        else:
          raise WintxDatabaseError('Was unable to form a stable connection to ' \
              '%s@%s:%s.' % (self.db_config['user'], self.db_config['fabric']['host'],
                             self.db_config['fabric']['port']))
      except MySQLError as e:
        raise WintxDatabaseError('Was unable to connect to %s@%s:%s - %s' %
            (self.db_config['user'], self.db_config['fabric']['host'], 
             self.db_config['fabric']['port'], str(e)))

    if( not self.isConnectedToServer() ):
      raise WintxDatabaseError('Was unable to connect to %s@%s:%s for an unknown ' \
          'reason.' % (self.db_config['user'], self.db_config['host'], 
                       self.db_config['port']))

  def connectDbServer(self, connection):
    """Attempts to force MySQL Fabric to connect to the db server for the 
       group. This will attempt to connect n (default 3) times."""
    attempts = self.connection_attempts
    for i in range(1, attempts + 1):
      try:
        connection._connect()
        break
      except InterfaceError as err:
        if( i < attempts ):
          continue
        else:
          raise WintxDatabaseError('Failed to form underlying connection to ' \
              'database. MySQL Fabric reset the connection too many times.')

  def __safeFabricExecute__(self, fabric_command, args=[], kwargs={}):
    """TODO"""
    attempts = self.connection_attempts
    result = None

    for i in range(1, attempts + 1):
      try:
        result = fabric_command(*args, **kwargs)
        break
      except InterfaceError as err:
        if( i < attempts ):
          continue
        else:
          raise WintxDatabaseError('Was unable to form a stable connection to ' \
              '%s@%s:%s while executing command "%s".' % (self.db_config['user'],
              self.db_config['host'], self.db_config['port'], fabric_command.__name__))
      except Exception as err:
        raise err

    return result

  def isConnectedToServer(self):
    """Determine if a connection persists."""
    return self.connection is not None

  def __connectedOrDie__(self):
    """Checks if a connection is formed and raises an error if not."""
    if( not self.isConnectedToServer() ):
      raise WintxDatabaseError('Not connected to server.')
    return True

  def disconnect(self):
    """Ensures the global connection is closed."""
    if( self.cursor is not None ):
      self.cursor.close()
      self.cursor = None

    if( self.connection is not None or self.connection.is_connected ):
      self.connection.disconnect()
      self.connection = None

  def __startTransaction__(self, snapshot=False, readonly=False):
    """Prepares a transaction and cursor for database operations. Limits to one
       global cursor at a time."""
    self.__connectedOrDie__()

    if( self.cursor is not None or self.connection.in_transaction ):
      raise WintxDatabaseError('A transaction is currently active. A new '\
          'transaction may not begin until the current transaction has completed.')

    try:
      self.connection.start_transaction(consistent_snapshot=snapshot, readonly=readonly)
      #self.cursor = self.connection.cursor(dictionary=True, buffered=False)

      self.cursor = self.connection.cursor()
    except ProgrammingError as e:
      if( self.cursor is not None ):
        self.cursor.close()

      if(self.connection.in_transaction ):
        self.connection.rollback()
      raise WintxDatabaseError('A transaction is currently active. A new '\
          'transaction may not begin until the current transaction has completed.')

  def __endTransaction__(self, commit=False):
    """Ends a transaction and closes the cursor."""
    self.__connectedOrDie__()

    if( self.cursor is not None ):
      try:
        for result in self.cursor:
          if( type(result) == type(()) ):
            break
          elif( result.with_rows ):
            result.fetchall()
        self.cursor.close()
      except Exception as err:
        raise WintxDatabaseError('Error closing the cursor: %s' % str(err))
    self.cursor = None

    if( self.connection.in_transaction ):
      if( commit ):
        self.connection.commit()
      else:
        self.connection.rollback()

  def __connectionThread__(self, thread_function, args, kwargs):
    """Creates a connection to be used by a given function."""
    thread_db_config = self.db_config.copy()
    del thread_db_config['connection_timeout']
    thread_db_config['autocommit'] = False
    thread_connection = mysql.connector.connect(**thread_db_config)
    thread_function(connection=thread_connection, *args, **kwargs)
    return

  def __multiThreadedConnections__(self, numTasks, thread_function, args, kwargs):
    """Executes a function across multiple threads, each with a unique connection."""
    threads = []

    numConnections = min(numTasks, self.poolsize)
    if( numConnections > 1 ):
      for i in range(numConnections):
        threads.append(
            Thread(
                name='Wintx-Thread-%05d' % i,
                target=self.__connectionThread__,
                args=(thread_function, args, kwargs,),
        ))

      for thread in threads:
        thread.daemon = True
        thread.start()
      for thread in threads:
        thread.join()

    else:
      self.__connectionThread__(thread_function, args, kwargs)

    return

  def __prepareQuery__(self, query_dict, restricted=None, polygonWhere=None):
    if( restricted is None ):
      restricted = []

    for key in query_dict:
      if( key in restricted ):
        raise WintxDatabaseError('Column "%s" is restricted for this query.' % key)

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
            value = self.__getTimestamp__(value)

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
          value = self.__getTimestamp__(value)

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

  def __queryAllShardsThread__(self, groupQueue, query, resultList, connection=None):
    """Thread instance handling querying individual shard groups."""
    connection.set_property(scope=fabric.SCOPE_LOCAL, mode=fabric.MODE_READONLY)

    while( not groupQueue.empty() ):
      group = groupQueue.get()
      connection.set_property(group=group)

      cursor = connection.cursor()
      cursor.execute(query)
      results = cursor.fetchall()
      cursor.close()

      self.meta_lock.acquire()
      for result in results:
        resultList.append(result)
      self.meta_lock.release()

      groupQueue.task_done()

  def __queryAllShards__(self, query):
    """Executes a query across all shard groups."""
    results = []
    groupQueue = Queue.Queue()
    for group in self.shard_groups:
      groupQueue.put(group)

    self.__multiThreadedConnections__(groupQueue.qsize(), self.__queryAllShardsThread__, (groupQueue, query, results), {})
    return results

  def __finalizeRecords__(self, results, sort=None):
    """Prepares results from a query into a list of dictionary entries, sorted if specified."""
    records = []
    for record in results:
      records.append({'time': self.__getTime__(record[0]), 'latitude': record[1],
          'longitude': record[2], 'level': record[3], 'leveltype': record[4],
          'datatype': record[5], 'varname': record[6], 'value': record[7]})
   
    if( sort is not None ):
      if( type(sort) is not type([]) ):
        raise WintxDatabaseError('Sort parameters should be given as a list.')

      sort.reverse()
      for column in sort:
        if( column[1].lower() == 'asc' ):
          records.sort(key=lambda item: item[column[0]], reverse=False)
        elif( column[1].lower() == 'dsc' ):
          records.sort(key=lambda item: item[column[0]], reverse=True)
        else:
          raise WintxDatabaseError('Invalid sort direction \'%s\'' % column[1])

    return records

  def query(self, query_dict, sort_column=None):
    """Queries the database for records in a readonly environment.
    Inputs:
      query_dict: dictionary forming a query request
      sort_column: column, direction tuple list in order of complex sort
        example: [('time', 'asc'), ('leveltype', 'asc'), ('level', 'dsc')]
    Outputs:
      list: of finalized record dictionaries
    """
    
    self.__connectedOrDie__()

    query = self.__prepareQuery__(query_dict)

    results = self.__queryAllShards__(query)
    records = self.__finalizeRecords__(results, sort_column)

    return records

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
    restricted_columns = ['latitude', 'longitude']

    first_point = polygon[0]
    poly_where = 'ST_Contains(GeomFromText("POLYGON(('

    if( reverse_points ):
      for point in polygon:
        poly_where = '%s%.20f %.20f, ' % (poly_where, point[1], point[0])
      poly_where = '%s%.20f %.20f))"), `lat_lon`)' % (poly_where, first_point[1], first_point[0])
    else:
      for point in polygon:
        poly_where = '%s%.20f %.20f, ' % (poly_where, point[0], point[1])
      poly_where = '%s%.20f %.20f))"), `lat_lon`)' % (poly_where, first_point[0], first_point[1])

    query = self.__prepareQuery__(query_dict, restricted=restricted_columns, polygonWhere=poly_where)

    results = self.__queryAllShards__(query)
    records = self.__finalizeRecords__(results, sort_column)
    return records

  def __getOrAddId__(self, cache, key, find_query, insert_query):
    """Find or insert metadata.
    Searches the cache, then the database for a metadata id. If the metadata
    does not exist, insert the metadata into the database.
    Inputs:
      cache: dictionary of the metadata
      key: tuple of the metadata forming the metadata key
        example: (latitude, longitude) or (level, leveltype)
      find_query: database query to search for metadata
      insert_query: database query to insert metadata
    Outputs:
      int: database id of metadata
    """
    key_id = -1

    if( not cache.has_key(key) ):
      self.__setGlobalConnectionProperty__()
      self.__startTransaction__()
      commit = True
      gtid_sync = None
      results = None

      try:
        self.cursor.execute(find_query)
        results = self.cursor.fetchall()
      except MySQLError as err:
        results = []

      if( not results ):
        try:
          self.cursor.execute(insert_query)
          key_id = self.cursor.lastrowid

          self.cursor.execute("SELECT @@global.gtid_executed")
          gtid_sync = self.cursor.fetchall()[0][0]
        except MySQLError as err:
          commit = False
          raise WintxDatabaseError('Failed to insert metadata key %s.' % key)
      else:
        key_id = results[0][0]

      self.__endTransaction__(commit)

      cache[key] = (key_id, gtid_sync)
    else:
      key_id = cache[key][0]

    return key_id

  def __setBulkMeta__(self, cache, records):
    """Places records into the cache.
    Inputs:
      cache: metadata dictionary for records to cache within
      records: record metadata to be cached
    """
    for r in records:
      cache[(r[1], r[2])] = (r[0], None)

  def clearMetadataCache(self):
    """Clears the local metadata cache."""
    del self.meta_locations
    del self.meta_levels
    del self.meta_variables
    self.meta_locations = {}
    self.meta_levels = {}
    self.meta_variables = {}

  def loadMetadataCache(self):
    """Loads the metadata into a local cache."""
    if( not self.meta_levels or not self.meta_variables or not self.meta_locations ):
      self.meta_levels = {}
      self.meta_locations = {}
      self.meta_variables = {}

      self.__setGlobalConnectionProperty__(readonly=True)
      self.__startTransaction__(readonly=True)

      self.cursor.execute(self.QUERY_SELECT_LOCATION)
      self.__setBulkMeta__(self.meta_locations, self.cursor.fetchall())
      self.cursor.execute(self.QUERY_SELECT_LEVEL)
      self.__setBulkMeta__(self.meta_levels, self.cursor.fetchall())
      self.cursor.execute(self.QUERY_SELECT_VARIABLE)
      self.__setBulkMeta__(self.meta_variables, self.cursor.fetchall())

      self.__endTransaction__()

  def __formDataDict__(self, record):
    """Forms insert ready dictionary.
    It is assumed that the cache has been loaded prior this call.
    Inputs:
      record: dictionary containing a data point's metadata and data values
    Outputs:
      dictionary: insert ready dictionary containing metadata id's and data values
        format: {'loc_id': 1, 'var_id': 1, 'level_id': 1,
                 'timestamp': datetime, 'value': 1.0}
    """
    loc_id = self.meta_locations[record['latitude'], record['longitude']][0]
    level_id = self.meta_levels[record['level'], record['leveltype']][0]
    var_id = self.meta_variables[record['datatype'], record['varname']][0]
    timestamp = self.__getTimestamp__(record['time'])

    data_dict = {'timestamp': timestamp, 'data_id': None,
        'value': record['value'], 'loc_id': loc_id,
        'var_id': var_id,
        'level_id': level_id}

    data_dict['data_id'] = hashlib.md5('%(timestamp)d-%(loc_id)s-%(level_id)s-%(var_id)s' % data_dict).hexdigest()

    return data_dict

  def __determineShardGroup__(self, data_dict):
    """Retreives the shard group that MySQL Fabric determines the record belongs to.
    Inputs:
      data_dict: a dictionary prepared to be inserted into the Data table
    Outputs:
      string: name of the shard group the record will insert into
    """
    key = data_dict['data_id']
    table = '%s.Data' % self.db_name
    server = self.__safeFabricExecute__(self.connection._fabric.get_shard_server,
        [(table,), key], {'scope': fabric.SCOPE_LOCAL, 'mode': fabric.MODE_READWRITE})
    return server[1]

  def __makeRecordGroupJobQueue__(self, groups_dict):
    """Converts a dictionary of group to record lists into list of jobs.
    This will split record lists into multiple lists with 
    bulkquantity records per list.
    Inputs:
      groups_dict: dictionary of record lists keyed by group names.
    Outputs:
      Queue: of job dictionaries containing group information and a record list
             with no more than bulkquantity records
    """
    jobs_count = 0
    jobList = {}
    jobQueue = Queue.Queue()
    record_import_quantity = self.bulkquantity

    for group in groups_dict:
      count = 0
      cur_list = []
      jobList[group] = []
      jobList[group].append(cur_list)

      for data_dict in groups_dict[group]:
        count = count + 1
        if( count % record_import_quantity == 0 ):
          cur_list = []
          jobList[group].append(cur_list)
        cur_list.append(data_dict)
      jobs_count = jobs_count + len(jobList[group])

    # Distributes jobs so groups evenly receive thread time
    while( jobQueue.qsize() < jobs_count ):
      for group in jobList:
        try:
          job = jobList[group].pop()
          jobQueue.put({'group': group, 'records': job})
        except IndexError as err:
          pass

    return jobQueue

  def __threadMetadataInsert__(self, metadataQueue, connection=None):
    """Inserts metadata in bulk."""
    while ( not metadataQueue.empty() ):
      try:
        job = metadataQueue.get(block=False)
      except Queue.Empty as err:
        continue

      group = job['group']
      records = job['records']
      if( len(records) == 0 ):
        continue

      query = ''
      value = ''
      if( group == 'global_loc' ):
        query = self.QUERY_INSERT_LOCATION
        value = self.QUERY_INSERT_LOCATION_VALUE
      elif( group == 'global_var' ):
        query = self.QUERY_INSERT_VARIABLE
        value = self.QUERY_INSERT_VARIABLE_VALUE
      elif( group == 'global_lev' ):
        query = self.QUERY_INSERT_LEVEL
        value = self.QUERY_INSERT_LEVEL_VALUE
      else:
        raise WintxDatabaseError('Invalid group provided for metadata import. Group: %s' % group)

      self.__setGlobalConnectionProperty__(connection=connection)

      cursor = None
      attempt = 0
      while( cursor is None ):
        attempt = attempt + 1
        if( attempt > 6 ):
          raise WintxDatabaseError('Failed to connect to fabric global server.')
        try:
          cursor = connection.cursor()
        except InterfaceError as err:
          cursor = None
          continue

      importBatch = []
      for rec in records:
        importBatch.append(value % rec)
      cursor.execute('%s %s' % (query, ', '.join(importBatch)))

      cursor.close()
      cursor = None
      connection.commit()
      metadataQueue.task_done()

    return

  def __insertRecord__(self, record, insert_dict, cursor):
    """Inserts record into the server of a given cursor.
    Inputs:
      record: dicitionary containing metadata and data values for data point
      insert_dict: insert ready data dictionary
      cursor: a connected Fabric cursor with local/global properties set
    """
    try:
      cursor.execute(self.QUERY_INSERT_DATA % insert_dict)
    except IntegrityError as err:
      # Foreign Key Failure
      if( err.errno == 1452 ):
        if( 'Location' in str(err) ):
          loc_id = (record['latitude'], record['longitude'])
          if( self.meta_locations[loc_id][1] is None ):
            raise WintxDatabaseError('Foreign key constraint error with "Location" table. GTID sync key not found. The location metadata was not successfully inserted.')
          gtid = self.meta_locations[loc_id][1]
          cursor.execute(self.QUERY_SELECT_GTID_WAIT % gtid)
          cursor.fetchall()
        elif( 'Variable' in str(err) ):
          var_id = (record['datatype'], record['varname'])
          if( self.meta_variables[var_id][1] is None ):
            raise WintxDatabaseError('Foreign key constraint error with "Variable" table. GTID sync key not found. The variable metadata was not successfully inserted.')
          gtid = self.meta_variables[var_id][1]
          cursor.execute(self.QUERY_SELECT_GTID_WAIT % gtid)
          cursor.fetchall()
        elif( 'Level' in str(err) ):
          level_id = (record['level'], record['leveltype'])
          if( self.meta_levels[level_id][1] ):
            raise WintxDatabaseError('Foreign key constraint error with "Level" table. GTID sync key not found. The level metadata was not successfully inserted.')
          gtid = self.meta_levels[level_id][1]
          cursor.execute(self.QUERY_SELECT_GTID_WAIT % gtid)
          cursor.fetchall()
        else:
          raise WintxDatabaseError('Unknown foreign key constraint error: %s' % str(err))

        self.__insertRecord__(record, insert_dict, cursor)

      # Duplicate Key
      elif( err.errno == 1022 ):
        raise WintxDatabaseError('Duplicate record found for %s.' % record)
    except MySQLError as err:
      raise WintxDatabaseError('unknown database error occurred: %s' % str(err))

  def __threadInsert__(self, jobQueue, resultDict, connection=None):
    """Thread instance handling inserting a data record."""
    successful_records = 0
    duplicate_records = []
    errors_list = []

    while( not jobQueue.empty() ):
      try:
        job = jobQueue.get(block=False)
      except Queue.Empty as err:
        continue
      shard_group = job['group']
      records = job['records']

      self.__setLocalConnectionGroupProperty__(shard_group, connection=connection)
      connection.start_transaction(readonly=False)
      cursor = None

      # Connections were not connecting, had to run multiple times to successfully  connect
      attempt = 0
      while( cursor is None ):
        attempt = attempt + 1
        if( attempt > 6 ):
          raise WintxDatabaseError('Failed to connect to fabric server for group %s.' % shard_group)
        try:
          cursor = connection.cursor()
        except InterfaceError as err:
          cursor = None
          pass

      importData = []
      data_ids = []
      data_id_mapping = {}
      for rec in records:
        data_ids.append('UNHEX(\'%s\')' % rec[1]['data_id'])
        data_id_mapping[rec[1]['data_id']] = rec[0]
      
      # Check for duplicate ids
      cursor.execute('SELECT HEX(`data_id`) FROM `Data` WHERE `data_id` IN (%s)' % ', '.join(data_ids))
      results = cursor.fetchall()
      if( len(results) > 0 ):
        for res in results:
          if( res[0].lower() in data_id_mapping.keys() ):
            duplicate_records.append(data_id_mapping[res[0].lower()])

      for rec in records:
        if( rec[0] not in duplicate_records ):
          importData.append(self.QUERY_INSERT_DATA_VALUE % rec[1])

      if( len(importData) > 0 ):
        try:
          cursor.execute('SET foreign_key_checks=0')
          cursor.execute('SET unique_checks=0')
          cursor.execute('%s %s' % (self.QUERY_INSERT_DATA, ', '.join(importData)))
          cursor.execute('SET unique_checks=1')
          cursor.execute('SET foreign_key_checks=1')
          successful_records = successful_records+ len(importData)
        except IntegrityError as err:
          errors_list.append(str(err))
        except MySQLError as err:
          errors_list.append(str(err))

      cursor.close()
      cursor = None

      connection.commit()

      jobQueue.task_done()

    self.meta_lock.acquire()
    resultDict['insertedRecords'] = resultDict['insertedRecords'] + successful_records
    resultDict['duplicateRecords'] = resultDict['duplicateRecords'] + duplicate_records
    resultDict['errors'] = resultDict['errors'] + errors_list
    self.meta_lock.release()
    return

  def insertRecords(self, records, clear_cache=False):
    """Inserts multiple records."""
    self.__connectedOrDie__()

    self.loadMetadataCache()

    results = {
        'insertedRecords': 0,
        'duplicateRecords': [],
        'errors': []
    }

    insert_loc = set()
    insert_var = set()
    insert_lev = set()

    # Prepare metadata for import
    for record in records:
      loc = (record['latitude'], record['longitude'])
      var = (record['datatype'], record['varname'])
      lev = (record['level'], record['leveltype'])
      if( not self.meta_locations.has_key(loc) ):
        insert_loc.add(loc)
      if( not self.meta_variables.has_key(var) ):
        insert_var.add(var)
      if( not self.meta_levels.has_key(lev) ):
        insert_lev.add(lev)

    # Import metadata
    metadataList = {'global_loc': [],
        'global_lev': [],
        'global_var': []}
    if( len(insert_loc) > 0 ):
      for loc in insert_loc:
        metadataList['global_loc'].append({'latitude': loc[0], 'longitude': loc[1]})
    if( len(insert_lev) > 0 ):
      for lev in insert_lev:
        metadataList['global_lev'].append({'level': lev[0], 'leveltype': lev[1]})
    if( len(insert_var) > 0 ):
      for var in insert_var:
        metadataList['global_var'].append({'datatype': var[0], 'varname': var[1]})
    metadataQueue = self.__makeRecordGroupJobQueue__(metadataList)
    self.__multiThreadedConnections__(metadataQueue.qsize(), self.__threadMetadataInsert__, (metadataQueue,), {})

    self.clearMetadataCache()
    self.loadMetadataCache()

    # Sorts records into their shard groups
    shard_groups = {}
    for record in records:
      data_dict = self.__formDataDict__(record)
      shard = self.__determineShardGroup__(data_dict)
      if( shard not in shard_groups ):
        shard_groups[shard] = []
      shard_groups[shard].append((record, data_dict))

    jobQueue = self.__makeRecordGroupJobQueue__(shard_groups)

    # Create the threads handling record imports
    self.__multiThreadedConnections__(jobQueue.qsize(), self.__threadInsert__, (jobQueue, results), {})

    if( clear_cache ):
      self.clearMetadataCache()

    return results

  def getTimes(self):
    """Retreives the unique timestamps stored in the database."""
    self.__connectedOrDie__()
    results = self.__queryAllShards__("SELECT DISTINCT(`timestamp`) FROM Data")

    timestamps = set()
    for timestamp in results:
      timestamps.add(timestamp[0])

    final_times = []
    for timestamp in timestamps:
      final_times.append(self.__getTime__(timestamp))

    final_times.sort()
    return final_times

  def getVariables(self):
    """Retreives the variables stored in the database."""
    self.__connectedOrDie__()
    self.__setGlobalConnectionProperty__()
    self.__startTransaction__(readonly=True)
    self.cursor.execute('SELECT DISTINCT(`variable_name`) FROM `Variable` ORDER BY `variable_name` ASC')
    results = self.cursor.fetchall()
    self.__endTransaction__()

    variables = []
    for r in results:
      variables.append(r[0])

    return variables

  def getLevels(self):
    """Retreives the levels stored in the database."""
    self.__connectedOrDie__()
    self.__setGlobalConnectionProperty__()
    self.__startTransaction__(readonly=True)
    self.cursor.execute('SELECT `level`, `level_type` FROM `Level` ORDER BY `level_type`, `level` ASC')
    results = self.cursor.fetchall()
    self.__endTransaction__()

    levels = []
    for r in results:
      levels.append((r[1], r[0]))

    return levels

  def getLocationCorners(self):
    """Retreives the corners of the stored latitude/longitude values in the database."""
    self.__connectedOrDie__()
    self.__setGlobalConnectionProperty__()
    self.__startTransaction__(readonly=True)
    self.cursor.execute('SELECT MAX(X(`lat_lon`)) AS `MAX_LAT`, ' \
        'MIN(X(`lat_lon`)) AS `MIN_LAT`, MAX(Y(`lat_lon`)) AS `MAX_LON`, ' \
        'MIN(Y(`lat_lon`)) AS `MIN_LON` FROM `Location`')
    results = self.cursor.fetchall()
    self.__endTransaction__()

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
    """Retreives the size of the database and tables.
       Return: dict
    """
    self.__connectedOrDie__()
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

    tables = self.__queryAllShards__('SHOW TABLE STATUS FROM %s' % self.settings['mysql']['db_name'])

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

  def getVarnamesAtTime(self, time, time_end=None):
    """Retreives variable names that are valid at a given time.
    """
    self.__connectedOrDie__()
    query_templ = "SELECT Data.timestamp, Variable.datatype, Variable.variable_name FROM " \
          "(SELECT DISTINCT Data.timestamp, Data.var_id FROM Data %s) AS Data " \
        "INNER JOIN Variable ON Data.var_id=Variable.var_id " \
        "ORDER BY Data.timestamp, Variable.datatype, Variable.variable_name"

    where_clause = "WHERE Data.timestamp=%d" % self.__getTimestamp__(time)
    if( time_end is not None ):
      where_clause = "WHERE Data.timestamp BETWEEN %d AND %d" % (self.__getTimestamp__(time), self.__getTimestamp__(time_end))

    query = query_templ % where_clause

    variables_raw = self.__queryAllShards__(query)

    variables_fixed = {}
    for var in variables_raw:
      time = self.__getTime__(var[0])
      if( time not in variables_fixed ):
        variables_fixed[time] = []
      variables_fixed[time].append({'varname': var[2], 'datatype': var[1]})

    return variables_fixed
