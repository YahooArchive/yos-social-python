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


"""Errors used on the Python opensocial client libraries."""


__author__ = 'davidbyttow@google.com (David Byttow)'


class Error(Exception):
  """Base opensocial.client error type."""


class ConfigError(Error):
  """Raised when the client has not been configured properly."""
  

class BadResponseError(Error):
  """Raised when the status code is not OK or data returned is invalid."""
  def __init__(self, code, message=""):
    self.code = code
    self.message = message

  def __str__(self):
      return "Bad Response: %d - %s" % (self.code, self.message)
  

class BadRequestError(Error):
  """Raised when a malformed request is detected."""
  def __init__(self, response):
    self.response = response
    
  def __str__(self):
    return 'STATUS: %d\nRESPONSE: %s' % (self.response.status,
                                         self.response.content)


class UnauthorizedRequestError(Error):
  """Raised when a request failed due to bad authorization credentials."""
  def __init__(self, response):
    self.response = response
