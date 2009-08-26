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

import urllib
import httplib
import hashlib
import unittest
from base64 import b64encode

from opensocial import *
from opensocial import mock_http, simplejson, test_data


TEST_CONFIG = ContainerConfig(
    server_rest_base='http://www.foo.com/rest/',
)

class TestHttp(unittest.TestCase):
  
  def setUp(self):
    self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
    self.consumer = oauth.OAuthConsumer("consumer_key", "consumer_secret")

  def test_body_hash(self):
    post_body = "I am a post body"
    post_body_json = simplejson.dumps(post_body)
    post_body_hash = b64encode(hashlib.sha1(post_body_json).digest())
    post_body_param = simplejson.dumps(post_body)
    
    request = http.Request("http://example.com", "POST", post_body=post_body)
    request.set_body_as_signing_parameter(False)
    request.sign_request(self.consumer, self.signature_method)
    
    self.assertEquals(post_body_hash, request.get_parameter('oauth_body_hash'))
    headers = request.get_headers()
    self.assertEquals("application/json", headers['Content-Type'])
    
    try:
      request.get_parameter(post_body_param)
    except oauth.OAuthError:
      return
    self.fail()
    
  def test_body_as_signing_param(self):
    post_body = "I am a post body"
    post_body_param = simplejson.dumps(post_body)
    post_body_param_quoted = urllib.quote(post_body_param)
    
    request = http.Request("http://example.com", "POST", post_body=post_body)
    request.set_body_as_signing_parameter(True)
    request.sign_request(self.consumer, self.signature_method)
    
    param_location = request.get_url().find(post_body_param_quoted)
    self.assertTrue(param_location > -1)
    self.assertEquals("", request.get_parameter(post_body_param))
    
    try:
      request.get_parameter('oauth_body_hash')
    except oauth.OAuthError:
      return
    self.fail()
    
class TestRestRequest(unittest.TestCase):

  def test_http_request(self):
    rest_request = request.RestRequestInfo('@me/@friends')
    http_request = rest_request.make_http_request(TEST_CONFIG.server_rest_base)
    self.assertEquals('GET', http_request.get_method())
    self.assertEquals(
        'http://www.foo.com/rest/@me/@friends?opensocial_method=GET',
        http_request.get_url())

    
class TestRpcRequest(unittest.TestCase):

  def test_rpc_body(self):
    rpc_request = RpcRequestInfo('people.get',
                                 params={'userId': '101',
                                         'groupId': '@friends'},
                                 id='foo')
    rpc_body = rpc_request.get_rpc_body()
    self.assertEquals('people.get', rpc_body['method'])
    self.assertEquals('foo', rpc_body['id'])
    self.assertEquals('101', rpc_body['params']['userId'])
    self.assertEquals('@friends', rpc_body['params']['groupId'])


class TestContainerContext(unittest.TestCase):

  viewer_response = http.Response(httplib.OK, simplejson.dumps(
      test_data.VIEWER_FIELDS))

  friends_response = http.Response(httplib.OK, simplejson.dumps(
      test_data.FRIEND_COLLECTION_FIELDS))

  noauth_response = http.Response(httplib.OK,
                                  simplejson.dumps(test_data.NO_AUTH))

  def add_canned_response(self, request_url, http_response, requestor_id=None):
    http_request = http.Request(request_url)
    if requestor_id:
      http_request.set_parameter('xoauth_requestor_id', requestor_id)
    http_request.set_parameter('opensocial_method', 'GET')
    self.urlfetch.add_response(http_request, http_response)

  def setUp(self):
    self.urlfetch = mock_http.MockUrlFetch()
    self.container = ContainerContext(TEST_CONFIG, self.urlfetch)

    self.add_canned_response('http://www.foo.com/rest/people/@me/@self',
                             TestContainerContext.viewer_response)

    self.add_canned_response('http://www.foo.com/rest/people/@me/@friends',
                             TestContainerContext.friends_response)

    self.add_canned_response('http://www.foo.com/rest/people/102/@friends',
                             TestContainerContext.noauth_response,
                             requestor_id='102')

    self.add_canned_response('http://www.foo.com/rest/people/103/@friends',
                              http.Response(httplib.NOT_FOUND, 'Error'),
                              requestor_id='103')

  def test_supports_rpc(self):
    self.assertEqual(False, self.container.supports_rpc())
    
  def test_fetch_person(self):
    person = self.container.fetch_person('@me')
    self.assertEqual(test_data.VIEWER.get_id(), person.get_id())
    self.assertEqual(test_data.VIEWER.get_display_name(),
                     person.get_display_name())

  def test_fetch_friends(self):
    friends = self.container.fetch_friends('@me')
    self.assertEqual(friends.startIndex,
                     test_data.FRIENDS.startIndex)
    self.assertEqual(friends.totalResults,
                     test_data.FRIENDS.totalResults)
    for i in range(len(friends)):
      person = friends[i]
      test_person = test_data.FRIENDS[i]
      self.assertEqual(person.get_id(), test_person.get_id())
      self.assertEqual(person.get_display_name(),
                       test_person.get_display_name())
      
  def test_unauthorized_request(self):
    self.assertRaises(UnauthorizedRequestError,
                      self.container.fetch_friends,
                      '102')
 
  def test_bad_request(self):
    self.assertRaises(BadRequestError, self.container.fetch_friends, '103')
    self.assertRaises(BadRequestError, self.container.fetch_friends, '??')
