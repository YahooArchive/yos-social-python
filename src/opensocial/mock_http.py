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

from opensocial import http


class ResponseRecord(object):
  
  def __init__(self, request, response):
    self.request = request
    self.response = response


class MockUrlFetch(http.UrlFetch):
  """A mock UrlFetch implementation for unit tests.
  
  Used to set canned responses for particular requests. The default canned
  response (Error 500) will be returned if a response is not found.

  """
  
  def __init__(self):
    self.records = []
    self.default_response = http.Response(httplib.INTERNAL_SERVER_ERROR, '')

  def add_response(self, request, response):
    """Adds a canned response for a given request.
    
    Args:
      request: An http.Request object used to trigger this response.
      response: An http.Response object that will be returned.

    """
    self.records.append(ResponseRecord(request, response))

  def fetch(self, request):
    """Perform the fake fetch.
    
    Looks up the details of the specified request and returns a canned
    response if one is found, otherwise 500 error.

    """
    response = self._lookup_request(request)
    return response

  def _lookup_request(self, request):
    url = request.get_url()
    for record in self.records:
      other_url = record.request.get_url()
      if (record.request.get_method() == request.get_method() and
          url == other_url and
          record.request.post_body == request.post_body):
        return record.response
    return self.default_response
