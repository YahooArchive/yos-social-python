#!/usr/bin/python
#
# Copyright (C) 2007, 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'davidbyttow@google.com (David Byttow)'


import hashlib
import random
import time
import urlparse
from types import ListType

import data
import http

from opensocial import simplejson


def generate_uuid(*args):
  """Simple method for generating a unique identifier.
  
  Args: Any arguments used to help make this uuid more unique.
  
  Returns: A 128-bit hex identifier.

  """
  t = long(time.time() * 1000)
  r = long(random.random() * 1000000000000000L)
  a = random.random() * 1000000000000000L
  data = '%s %s %s %s' % (str(t), str(r), str(a), str(args))
  return hashlib.md5(data).hexdigest()


class Request(object):
  """Represents an OpenSocial request that can be processed via RPC or REST."""
  
  def __init__(self, rest_request, rpc_request, requestor=None):
    self.rest_request = rest_request
    self.rpc_request = rpc_request
    self.set_requestor(requestor)
    
  def get_requestor(self):
    """Get the requestor id for this request.
    
    Returns: The requestor's id.
    
    """
    return self.__requestor
  
  def set_requestor(self, id):
    """Set the requestor id for this request.
    
    This does not accept any keywords such as @me.
    TODO: Refactor the id check out of here, it feels wrong.
    
    Args:
      id: str The requestor's id.
      
    """
    if id and id[0] is not '@':
      self.__requestor = id
    else:
      self.__requestor = None
    
  def get_query_params(self):
    """Returns the query params string for this request."""
    query_params = {}
    if self.get_requestor():
      query_params['xoauth_requestor_id'] = self.get_requestor()
    return query_params
  
  def make_rest_request(self, url_base):
    """Creates a RESTful HTTP request.
    
    Args:
      url_base: str The base REST URL.

    """
    return self.rest_request.make_http_request(url_base,
                                               self.get_query_params())

  def get_rpc_body(self):
    return self.rpc_request.get_rpc_body()


class FetchPeopleRequest(Request):    
  """A request for handling fetching a collection of people."""
  
  def __init__(self, user_id, group_id, fields=None, params=None):
    params = params or {}
    if fields:
      params['fields'] = ','.join(fields)
    rest_request = RestRequestInfo('/'.join(('people', user_id, group_id)),
                                   params=params)
    rpc_params = params.copy()
    rpc_params.update({'userId': user_id,
                       'groupId': group_id})
    rpc_request = RpcRequestInfo('people.get', params=rpc_params)
    super(FetchPeopleRequest, self).__init__(rest_request,
                                             rpc_request,
                                             user_id)
    
  def process_json(self, json):
    """Construct the appropriate OpenSocial object from a JSON dict.
    
    Args:
      json: dict The JSON structure.
      
    Returns: a Collection of Person objects.

    """
    return data.Collection.parse_json(json, data.Person)

    
class FetchPersonRequest(FetchPeopleRequest):
  """A request for handling fetching a single person by id."""

  def __init__(self, user_id, fields=None, params={}):
    super(FetchPersonRequest, self).__init__(user_id,
                                             '@self',
                                             fields=fields,
                                             params=params)

  def process_json(self, json):
    """Construct the appropriate OpenSocial object from a JSON dict.
    
    Args:
      json: dict The JSON structure.
      
    Returns: A Person object.

    """
    return data.Person.parse_json(json)


class FetchAppDataRequest(Request):
  """A request for handling fetching app data."""

  def __init__(self, user_id, group_id, app_id='@app', fields=None, 
               params=None):
    params = params or {}
    if fields:
      params['fields'] = ','.join(fields)
    
    rest_path = '/'.join(('appdata', user_id, group_id, app_id))
    rest_request = RestRequestInfo(rest_path, params=params)
    
    # TODO: Handle REST fields.
    params.update({'userId': user_id,
                   'groupId': group_id,
                   'appId': app_id,
                   'keys': fields})
    rpc_request = RpcRequestInfo('appdata.get', params=params)
    super(FetchAppDataRequest, self).__init__(rest_request,
                                              rpc_request,
                                              user_id)

  def process_json(self, json):
    """Construct the appropriate OpenSocial object from a JSON dict.
    
    Args:
      json: dict The JSON structure.
      
    Returns: An AppData object.

    """
    if type(json) == ListType:
      return json
    else:
      return data.AppData.parse_json(json)


class UpdateAppDataRequest(Request):
  """A request for handling updating app data."""

  def __init__(self, user_id, group_id, app_id='@app', fields=None, data={}, 
               params=None):
    params = params or {}
    if fields:
      params['fields'] = ','.join(fields)

    params['data'] = data

    #TODO: add support for rest
    params.update({'userId': user_id,
                   'groupId': group_id,
                   'appId': app_id})
    rpc_request = RpcRequestInfo('appdata.update', params=params)
    super(UpdateAppDataRequest, self).__init__(None,
                                              rpc_request,
                                              user_id)

  def process_json(self, json):
    return json


class DeleteAppDataRequest(Request):
  """A request for handling deleting app data."""

  def __init__(self, user_id, group_id, app_id='@app', fields=None, 
               params=None):
    params = params or {}
    if fields:
      params['fields'] = ','.join(fields)

    #TODO: add support for rest
    params.update({'userId': user_id,
                   'groupId': group_id,
                   'appId': app_id,
                   'keys': params['fields']})
    rpc_request = RpcRequestInfo('appdata.delete', params=params)
    super(DeleteAppDataRequest, self).__init__(None,
                                              rpc_request,
                                              user_id)

  def process_json(self, json):
    return json


class RestRequestInfo(object):
  """Represents a pending REST request."""

  def __init__(self, path, method='GET', params=None):
    self.method = method
    self.path = path
    self.params = params or {}

  def make_http_request(self, url_base, query_params=None):
    """Generates a http.Request object for the UrlFetch interface.
    
    Args:
      url_base: str The base REST URL.
    
    Returns: The http.Request object.

    """
    # Ensure that there is a path separator.
    if url_base[-1] is not '/' and self.path[0] is not '/':
      url_base = url_base + '/'
    url = url_base + self.path
    if query_params:
      self.params.update(query_params)
    return http.Request(url, method=self.method, signed_params=self.params)


class RpcRequestInfo(object):
  """Represents a pending RPC request."""

  def __init__(self, method, params, id=None):
    self.method = method
    self.params = params
    self.id = id or generate_uuid(method)
    
  def get_rpc_body(self):
    """Creates the JSON dict structure for thie RPC request.
    
    Returns: dict The JSON body for this RPC.

    """
    rpc_body = {
      'params': self.params,
      'method': self.method,
      'id': self.id,
    }
    return rpc_body


class RequestBatch(object):
  """This class will manage the batching of requests."""
  
  def __init__(self):
    self.requests = {}
    self.data = {}
  
  def add_request(self, key, request):
    """Adds a request to this batch.
    
    Args:
      key: str A unique key to pair with the result of this request.
      request: obj The request object.

    """
    if key:
      request.rpc_request.id = key
    self.requests[key] = request

  def get(self, key):
    """Get the result value for a given request key.
    
    Args:
      key: str The key to retrieve.

    """
    return self.data.get(key)

  def send(self, container):
    """Execute the batch with the specified container.
    
    Args:
      container: The container to execute this batch on.

    """
    container.send_request_batch(self, False)

  def _set_data(self, key, data):
    self.data[key] = data
