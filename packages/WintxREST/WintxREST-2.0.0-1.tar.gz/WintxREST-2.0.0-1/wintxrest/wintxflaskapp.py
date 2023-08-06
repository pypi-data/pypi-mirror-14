#!/usr/bin/env python
from datetime import datetime
from flask import Flask, json, jsonify, request, abort
from flask.ext.cors import CORS
from functools import wraps
import logging
from logging import FileHandler
import sys
from wintx import WintxError
from wintx.interfaces import Query
from wintxrest import default_settings

app = Flask(__name__)
app.config.from_object(default_settings.Config)
app.config.from_envvar('WINTXREST_SETTINGS', silent=True)
cors = CORS(app, resources='*', allow_headers='Content-Type')

# Error Codes:
#   200 - OK
#   201 - Created
#   400 - Bad Request
#   401 - Unauthorized (may request user & password)
#   403 - Forbidden
#   404 - Resource Not Found
#   405 - Method Not Allowed (ie. POST to GET)
#   500 - Internal Server Error
#   501 - Not Implemented
#   503 - Service Unavailable

################################################################################
# Global Constants
################################################################################
QUERY_COLUMNS = ['datatype', 'latitude', 'level', 'leveltype', 'longitude', 'time', 'varname']
QUERY_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


################################################################################
# Global Variables
################################################################################
wintxConfigFile = app.config['WINTX_CONFIG']
logFile = app.config['LOG_FILE']
logLevel = logging.getLevelName(app.config['LOG_LEVEL'])
useReloader = app.config['RELOADER']
useDebugger = app.config['DEBUGGER']


################################################################################
# Loggers
################################################################################
logfile_handler = FileHandler(logFile)
logfile_handler.setLevel(logLevel)
app.logger.addHandler(logfile_handler)


################################################################################
# Helper Functions
################################################################################
def formQuery(query_string):
  query_dict_given = json.loads(query_string.replace('\'', '"'))
  query_dict = {}
  if( type(query_dict_given) != type({}) ):
    abort(400)

  for column in query_dict_given:
    if( column in QUERY_COLUMNS ):
      if( column == 'time' ):
        if( type(query_dict_given[column]) == type({}) ):
          query_dict[column] = {}
          for comparison in query_dict_given[column]:
            query_dict[column][comparison] =  datetime.strptime(query_dict_given[column][comparison], QUERY_DATETIME_FORMAT)
        else:
          query_dict[column] = datetime.strptime(query_dict_given[column], QUERY_DATETIME_FORMAT)
      else:
        query_dict[column] = query_dict_given[column]
    else:
      # Invalid column
      abort(400)

  return query_dict

def formSort(sort_string):
  sort_list_given = json.loads(sort_string.replace('\'','"'))
  sort_list = []
  if( type(sort_list_given) != type([]) ):
    abort(400)

  for column in sort_list_given:
    if( type(column) != type([]) ):
      abort(400)
    if( len(column) != 2 ):
      abort(400)
    if( column[1] != 'asc' and column[1] != 'dsc' ):
      abort(400)
    if( column[0] not in QUERY_COLUMNS ):
      abort(400)

    sort_list.append((column[0], column[1]))

  return sort_list

def prepareReturnRecords(records):
  for record in records:
    o_time = record['time']
    record['time'] = o_time.strftime(QUERY_DATETIME_FORMAT)

  return records

def formatReturnTime(r_time):
  return r_time.strftime(QUERY_DATETIME_FORMAT)

def getWintxInstance():
  try:
    wintx_instance = Query(wintxConfigFile)
  except WintxError as err:
    abort(500, 'Can not form backend')

  return wintx_instance


################################################################################
# Error Handlers
################################################################################
@app.errorhandler(404)
def page_not_found(error):
  return jsonify({'error': 'Function not found'}), 404


################################################################################
# Authentication Handlers
################################################################################
def authorizeCheck():
  return True, None

def authorize(func):
  @wraps(func)
  def decorated(*args, **kwargs):
    # authorize_check returns a tuple:
    #   (boolean, Response)
    #   - boolean - if authorized or not (t/f respectively)
    #   - Response - None if authorized, otherwise this is a Flask Repsonse object
    #                This will be used to return an error code, redirect the 
    #                the browser, or any other tasks that the browser needs to perform
    authorized, response = authorizeCheck()
    if( not authorized ):
      return response
    return func(*args, **kwargs)
  return decorated


################################################################################
# Routing Handlers
################################################################################
@app.route('/query', methods=['GET'])
@authorize
def query():
  """Request - query, sort"""
  query_dict = {}
  if( 'query' in request.args ):
    query_dict = formQuery(request.args['query'])

  sort_list = None
  if( 'sort' in request.args ):
    sort_list = formSort(request.args['sort'])

  # Fetch records
  records = None
  wintx_instance = getWintxInstance()
  try:
    records = wintx_instance.query(query_dict, sort_column=sort_list)
  except WintxError as err:
    return jsonify({'error': err.message}), 500

  records = prepareReturnRecords(records)

  return jsonify({'records': records}), 200

@app.route('/query/polygon', methods=['GET'])
@authorize
def query_polygon():
  """Request - query, sort, polygon, invert"""
  if( 'polygon' not in request.args ):
    abort(400)

  polygon = json.loads(request.args['polygon'].replace('\'','"'))
  if( type(polygon) != type([]) ):
    abort(400)

  for point in polygon:
    if( type(point) != type([]) or len(point) != 2 ):
      abort(400)

  query_dict = {}
  if( 'query' in request.args ):
    query_dict = formQuery(request.args['query'])

  sort_list = None
  if( 'sort' in request.args ):
    sort_list = formSort(request.args['sort'])

  invert_points = False
  if( 'invert' in request.args ):
    invert_points = json.loads(request.args['invert'].replace('\'','"'))
    if( type(invert_points) != type(True) ):
      abort(400)

  # Fetch records
  records = None
  wintx_instance = getWintxInstance()
  try:
    records = wintx_instance.queryWithin(polygon, query_dict, reverse_points=invert_points, sort_column=sort_list)
  except WintxError as err:
    return jsonify({'error': err.message}), 500

  records = prepareReturnRecords(records)

  return jsonify({'records': records}), 200

@app.route('/metadata/times', methods=['GET'])
@authorize
def metadata_times():
  wintx_instance = getWintxInstance()
  return_times = []
  try:
    times = wintx_instance.getTimes()
    for t in times:
      return_times.append(formatReturnTime(t))
  except WintxError as err:
    return jsonify({'error': err.message}), 200
  return jsonify({'times': return_times}), 200

@app.route('/metadata/variables/time', methods=['GET'])
@authorize
def metadata_get_variables_at_time():
  variables = None
  corrected_vars = {}
  time = None
  time_end = None
  if( 'time' in request.args ):
    time = datetime.strptime(request.args['time'], QUERY_DATETIME_FORMAT)
  else:
    abort(400)

  if( 'time_end' in request.args):
    time_end = datetime.strptime(request.args['time_end'], QUERY_DATETIME_FORMAT)

  wintx_instance = getWintxInstance()
  try:
    variables = wintx_instance.getVarnamesAtTime(time, time_end=time_end)
    for time in variables:
      t = formatReturnTime(time)
      corrected_vars[t] = variables[time]
  except WintxError as err:
    return jsonify({'error': err.message})
  return jsonify(corrected_vars), 200

@app.route('/metadata/variables', methods=['GET'])
@authorize
def metadata_variables():
  # Fetch records
  variables = None
  wintx_instance = getWintxInstance()
  try:
    variables = wintx_instance.getVariables()
  except WintxError as err:
    return jsonify({'error': err.message}), 200
  return jsonify({'variables': variables}), 200

@app.route('/metadata/levels', methods=['GET'])
@authorize
def metadata_levels():
  levels = []
  wintx_instance = getWintxInstance()
  try:
    levels = wintx_instance.getLevels()
  except WintxError as err:
    return jsonify({'error': err.message}), 500
  return jsonify({'levels': levels}), 200

@app.route('/metadata/corners', methods=['GET'])
@authorize
def metadata_corners():
  corners = None
  wintx_instance = getWintxInstance()
  try:
    corners = wintx_instance.getLocationCorners()
  except WintxError as err:
    return jsonify({'error': err.message}), 200
  return jsonify(corners), 200

@app.route('/database/stats', methods=['GET'])
@authorize
def database_stats():
  stats = None
  wintx_instance = getWintxInstance()
  try:
    stats = wintx_instance.getDatabaseStats()
  except WintxError as err:
    return jsonify({'error': err.message}), 500
  return jsonify(stats), 200


################################################################################
# Checks if this is a script and handles server execution
################################################################################
if( __name__ == '__main__' ):
  app.run(use_debugger=useDebugger, use_reloader=useReloader, host='0.0.0.0')

