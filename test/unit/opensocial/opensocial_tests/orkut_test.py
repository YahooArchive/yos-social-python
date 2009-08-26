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


import unittest
import urllib2

import opensocial

from opensocial import oauth
from opensocial import request


class TestOrkut(unittest.TestCase):
  
  def setUp(self):
    self.config = opensocial.ContainerConfig(
        oauth_consumer_key='orkut.com:623061448914',
        oauth_consumer_secret='uynAeXiWTisflWX99KU1D2q5',
        server_rpc_base='http://sandbox.orkut.com/social/rpc',
        server_rest_base='http://sandbox.orkut.com/social/rest')
    self.container = opensocial.ContainerContext(self.config)
    self.user_id = '03067092798963641994'

  def validate_user(self, user):
    self.assertEquals(self.user_id, user.get_id())

  def validate_friends(self, friends):
    self.assertEquals(6, len(friends))
    self.assertEquals(0, friends.startIndex)
    self.assertEquals(6, friends.totalResults)
    self.assertEquals('13314698784882897227', friends[0].get_id())
    self.assertEquals('04285289033838943214', friends[1].get_id())
    
  def do_fetch_person(self, use_rpc, fields=None):
    self.container.set_allow_rpc(use_rpc)
    person = self.container.fetch_person(self.user_id, fields)
    return person

  def do_fetch_friends(self, use_rpc, fields=None):
    self.container.set_allow_rpc(use_rpc)
    friends = self.container.fetch_friends(self.user_id, fields)
    return friends
  
  def test_fetch_person_rpc(self):
    person = self.do_fetch_person(True)
    self.validate_user(person)

  def test_fetch_person_rest(self):
    person = self.do_fetch_person(False)
    self.validate_user(person)
    
  def test_fetch_friends_rpc(self):
    friends = self.do_fetch_friends(True)
    self.validate_friends(friends)

  def test_fetch_friends_rest(self):
    friends = self.do_fetch_friends(False)
    self.validate_friends(friends)
    
  def test_fetch_person_fields_rpc(self):
    person = self.do_fetch_person(True, ['gender'])
    self.assertEquals('male', person.get_field('gender'))
    
  def test_fetch_person_fields_rest(self):
    person = self.do_fetch_person(False, ['gender'])
    self.assertEquals('male', person.get_field('gender'))

  def test_batch(self):
    batch = opensocial.request.RequestBatch()
    batch.add_request('me',
                      opensocial.request.FetchPersonRequest(self.user_id))
    batch.add_request('friends',
                      opensocial.request.FetchPeopleRequest(self.user_id,
                                                            '@friends'))
    batch.send(self.container)
    
    me = batch.get('me')
    friends = batch.get('friends')
    self.validate_user(me)
    self.validate_friends(friends)