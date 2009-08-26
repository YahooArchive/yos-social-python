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


import httplib
import urllib
import urlparse

import http
import oauth
import simplejson

from data import *
from errors import *
from request import *


class ContainerConfig(object):
  """Setup parameters for connecting to a container."""
  
  def __init__(self, oauth_consumer_key=None, oauth_consumer_secret=None,
               server_rpc_base=None, server_rest_base=None, 
               security_token=None,
               security_token_param=None,
               sign_with_body=False):
    """Constructor for ContainerConfig.
    
    If no oauth parameters are present, then oauth will not be used to sign
    requests, and as such, the client connection will most likely not work.
    
    At least one of server_rpc_base or server_rest_base should be specified,
    otherwise, all requests will fail. If both are supplied, the container
    will attempt to default to rpc and fall back on REST.

    """
    self.oauth_consumer_key = oauth_consumer_key 
    self.oauth_consumer_secret = oauth_consumer_secret
    self.server_rpc_base = server_rpc_base
    self.server_rest_base = server_rest_base
    self.security_token = security_token
    self.security_token_param = security_token_param
    self.sign_with_body = sign_with_body
    if not server_rpc_base and not server_rest_base:
      raise ConfigError("Neither 'server_rpc_base' nor 'server_rest_base' set")


class ContainerContext(object):
  """The context for a container connection.
  
  This class manages the connection to a specific container and provides
  methods for fetching common data via either te REST or RPC protocol, depending
  on the configuration.

  """
  
  def __init__(self, config, url_fetch=None):
    """Constructor for ContainerContext.
    
    If a UrlFetch implementation is not given, will attempt to construct
    the default implementation based on the environment.
    
    Args:
      config: The ContainerConfig to use for this connection.
      url_fetch: (optional) An implementation of the UrlFetch interface.

    """
    self.config = config
    if not self.config:
      raise ConfigError('Invalid ContainerConfig.')
    self.url_fetch = url_fetch or http.get_default_urlfetch()
    self.oauth_signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1() 
    self.oauth_consumer = None
    self.allow_rpc = True
    if self.config.oauth_consumer_key and self.config.oauth_consumer_secret:
      self.oauth_consumer = oauth.OAuthConsumer(
          self.config.oauth_consumer_key,
          self.config.oauth_consumer_secret)
      
  def set_allow_rpc(self, allowed):
    """Sets if RPC requests are allowed if they are supported."""
    self.allow_rpc = allowed
    
  def supports_rpc(self):
    """Tells whether or not the container was setup for RPC protocol.
    
    Returns: bool Is this container using the RPC protocol?
    
    TODO: Figure out what is going wrong with POST body signing, fix and
    re-enable this.

    """
    return self.allow_rpc and self.config.server_rpc_base is not None
  
  def fetch_person(self, user_id='@me', fields=None):
    """Fetches a person by user id.
    
    Args:
      user_id: str The person's container-specific id.
      fields: list (optional) List of fields to retrieve.
      
    Returns: A Person object representing the specified user id.

    """
    request = FetchPersonRequest(user_id, fields=fields)
    return self.send_request(request)

  def fetch_friends(self, user_id='@me', fields=None):
    """Fetches the friends of a given user by id.
    
    Args:
      user_id: str The person's container-specific id for which to retrieve
      friends.
      fields: list (optional) List of fields to retrieve.
      
    Returns: A Collection of Person objects.

    """
    request = FetchPeopleRequest(user_id, '@friends', fields=fields)
    return self.send_request(request)

  def send_request(self, request, use_rest=False):
    """Sends the request.
    
    May throw a BadRequestError, BadResponseError or 
    UnauthorizedRequestError exceptions.

    Args:
      request: A Request object.
      use_rest: bool (optional) If True, will just use the REST protocol.
      
    Returns: The OpenSocial object returned from the container.

    """
    if not use_rest and self.supports_rpc():
      batch = RequestBatch()
      batch.add_request(0, request)
      batch.send(self)
      response = batch.get(0)
      if isinstance(response, Error):
        raise response
      return response
    else:
      return self._send_rest_request(request)
  
  def send_request_batch(self, batch, use_rest=False):
    """Send a batch of requests.
    
    Batches are only useful when RPC is supported. Otherwise, all requests
    are sent synchronously. May throw a BadRequest, BadResponse or
    UnauthorizedRequest exceptions.

    Args:
      batch: The RequestBatch object.
      use_rest: bool (optional) If True, will just use the REST protocol.

    """
    if not use_rest and self.supports_rpc():
      self._send_rpc_requests(batch)
    else:
      """REST protocol does not support batching, so just process each
      request individually.
      """
      for key, request in batch.requests.iteritems():
        try:
          result = self._send_rest_request(request)
        except Error, e:
          result = e
        batch._set_data(key, result)
  
  def _send_rest_request(self, request):
    http_request = request.make_rest_request(self.config.server_rest_base)
    http_response = self._send_http_request(http_request)
    json = self._handle_response(http_response)
    return request.process_json(json)
    
  def _send_rpc_requests(self, batch):
    rpcs = []
    id_to_key_map = {}
    query_params = {}
    """Build up a list of RPC calls. Also, create a mapping of RPC request id's
    to batch keys in order to populate the batch object with the responses.
    """
    for key, request in batch.requests.iteritems():
      query_params.update(request.get_query_params())
      rpc_body = request.get_rpc_body()
      rpc_id = rpc_body.get('id')
      id_to_key_map[rpc_id] = key
      rpcs.append(rpc_body)

    http_request = http.Request(self.config.server_rpc_base,
                                method='POST',
                                signed_params=query_params,
                                post_body=rpcs)
    
    http_response = self._send_http_request(http_request)
    json = self._handle_response(http_response)
    
    """Pull out all of the results and insert them into the batch object."""
    for response in json:
      id = response.get('id')
      key = id_to_key_map[id]
      if 'error' in response:
        code = response.get('error').get('code')
        message = response.get('error').get('message')
        error = BadResponseError(code, message)
        batch._set_data(key, error)
      else:
        json = response.get('data')
        request = batch.requests[key]
        batch._set_data(key, request.process_json(json))
      
  def _send_http_request(self, http_request):
    if self.config.security_token:
      http_request.add_security_token(self.config.security_token,
                                      self.config.security_token_param)

    if self.oauth_consumer and self.oauth_signature_method:
      http_request.set_body_as_signing_parameter(self.config.sign_with_body)
      http_request.sign_request(self.oauth_consumer,
                                self.oauth_signature_method)
      
    http_response = self.url_fetch.fetch(http_request)
    return http_response
      
  def _handle_response(self, http_response):
    """ If status code "OK", then we can safely inspect the returned JSON."""
    if http_response.status == httplib.OK:
      if http.VERBOSE > 0:
        logging.info("http_response.content => %s" % http_response.content)
        
      json = simplejson.loads(http_response.content)
      # Check for any JSON-RPC 2.0 errors.
      if 'error' in json:
        code = json.get('error').get('code')
        message = json.get('error').get('message')
        if code == httplib.UNAUTHORIZED:
          raise UnauthorizedRequestError(http_response)
        else:
          raise BadResponseError(code, message)
      return json
    else:
      raise BadRequestError(http_response)
