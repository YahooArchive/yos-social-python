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
import logging
import sys
import urllib2
import hashlib 
from base64 import b64encode

import oauth
import simplejson
try:
  from google.appengine.api import urlfetch
except:
  pass


logging.basicConfig(level=logging.DEBUG)

VERBOSE = 0

def get_default_urlfetch():
  """Creates the default UrlFetch interface.
  
  If AppEngine environment is detected, then the AppEngineUrlFetch object
  will be created.
  
  TODO: Find a better way to determine if this is an AppEngine environment.

  """
  if sys.modules.has_key('google.appengine.api.urlfetch'):
    return AppEngineUrlFetch()
  return UrlFetch()

def log_request(request):
  logging.debug('URL: %s %s\nHEADERS: %s\nPOST: %s' %
                (request.get_method(),
                 request.get_url(),
                 str(request.get_headers()),
                 request.get_post_body()))


def log_response(response):
  logging.debug('Status: %d\nContent: %s' % (response.status,
                                             response.content.decode('utf-8')))


class UrlFetch(object):
  """An API which provides a simple interface for performing HTTP requests."""

  def fetch(self, request):    
    """Performs a synchronous fetch request.
    
    TODO: Handle HTTPMethod
    
    Args:
      request: The http.Request object that contains the request information.
    
    Returns: An http.Response object.
    
    """
    log_request(request)
    method = request.get_method()
    headers = request.get_headers()

    if VERBOSE > 0:
      logging.info("URL => %s", request.get_url())
      
    req = urllib2.Request(request.get_url(),
                          data=request.get_post_body(),
                          headers=headers)
    try:
      f = urllib2.urlopen(req)
      result = f.read()
      response = Response(httplib.OK, result)
    except urllib2.URLError, e:
      response = Response(e.code, e.read())

    log_response(response)
    return response

class AppEngineUrlFetch(UrlFetch):
  """Implementation of UrlFetch using AppEngine's URLFetch API."""

  def fetch(self, request):
    """Performs a synchronous fetch request.
    
    Args:
      request: The http.Request object that contains the request information.
    
    Returns: An http.Response object.

    """
    log_request(request)
    method = request.get_method()
    url = request.get_url()
    body = request.get_post_body()
    headers = request.get_headers()
    result = urlfetch.fetch(
        method=method,
        url=url,
        payload=body,
        headers=headers)
    response = Response(result.status_code, result.content)
    log_response(response)
    return response


class Request(object):
  """This object is used to make a UrlFetch interface request.
  
  It also will sign a request with OAuth.

  """

  def __init__(self, url, method='GET', signed_params=None, post_body=None):
    self.post_body = post_body or None
    """OAuth library will not create a request unless there is at least one
    parameter. So we are going to set at least one explicitly.
    """
    self.use_body_as_signing_parameter = False
    params = signed_params or {}
    params['opensocial_method'] = method
    self.oauth_request = oauth.OAuthRequest.from_request(method, url,
        parameters=params)
    assert self.oauth_request
    
  def add_security_token(self, security_token, parameter_name="st"):
    self.oauth_request.set_parameter(parameter_name, security_token)
    self.security_token_parameter = parameter_name
    
  def get_security_token(self):
    if hasattr(self, "security_token_parameter"):
      return self.oauth_request.get_parameter(self.security_token_parameter)
      
  def set_body_as_signing_parameter(self, use_body):
    self.use_body_as_signing_parameter = use_body
        
  def sign_request(self, consumer, signature_method):
    """Add oauth parameters and sign the request with the given method.
    
    Args:
      consumer: The OAuthConsumer set with a key and secret.
      signature_method: A supported method for signing the built request.

    """
    params = {
      'oauth_consumer_key': consumer.key,
      'oauth_timestamp': oauth.generate_timestamp(),
      'oauth_nonce': oauth.generate_nonce(),
      'oauth_version': oauth.OAuthRequest.version,
    }
          
    # PHP OAuth library contains a bug which interferes with signing.  Since
    # some containers use this library, we will implement a workaround here.
    if self.use_body_as_signing_parameter:
      params[self.get_post_body()] = ""
    else:
      # Otherwise, use the oauth_body_hash extension to sign the request body.
      if self.post_body:
        if VERBOSE > 0:
          logging.info("post_body => %s" % str(self.post_body))
          
        body_hash = b64encode(hashlib.sha1(self.get_post_body()).digest())
        params['oauth_body_hash'] = body_hash
      
    if self.get_security_token():
      self.set_parameter("xoauth_requestor_id", None)
    
    self.set_parameters(params)
    if VERBOSE > 0:
      key, raw = signature_method.build_signature_base_string(
                     self.oauth_request, consumer, None)
      logging.info("build_signature key => %s" % key)
      logging.info("build_signature raw => %s" % raw)
      
    self.oauth_request.sign_request(signature_method, consumer, None)
    
  def set_parameter(self, name, value):
    """Set a parameter for this request.
    
    Args:
      name: str The parameter name.
      value: str The parameter value.

    """
    self.oauth_request.set_parameter(name, value)
      
  def set_parameters(self, params):
    """Set the parameters for this request.
    
    Args:
      params: dict A dict of parameters.

    """
    for name, value in params.iteritems():
      self.set_parameter(name, value)
  
  def get_parameter(self, key):
    """Get the value of a particular parameter.
    
    Args:
      key: str The key of the requested parameter.
      
    Returns: The parameter value.

    """
    return self.oauth_request.get_parameter(key)
  
  def get_method(self):
    """Returns the HTTP normalized method of this request.
    
    Returns: The normalized HTTP method.

    """
    return self.oauth_request.get_normalized_http_method()
  
  def get_url(self):
    """Get the full URL of this request, including the post body.
    
    Returns: The full URL for this request.

    """
    return self.oauth_request.to_url()
  
  def get_normalized_url(self):
    """Get the normalized URL for this request.
    
    Returns: The normalized URL for this request.

    """
    return self.oauth_request.get_normalized_http_url()
  
  def get_headers(self):
    headers = {}
    if self.post_body:
      headers['Content-Type'] = 'application/json'
    return headers


  def get_post_body(self):
    """Get the JSON encoded post body."""
    if self.post_body:
      return simplejson.dumps(self.post_body)
    return None

class Response(object):
  """Represents a response from the UrlFetch interface."""

  def __init__(self, status, content):
    self.status = status
    self.content = content
