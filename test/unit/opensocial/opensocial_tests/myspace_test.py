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

import opensocial


class TestMySpace(unittest.TestCase):
  
  def setUp(self):
    self.config = opensocial.ContainerConfig(
      oauth_consumer_key='http://opensocial-resources.googlecode.com/svn/samples/rest_rpc/sample.xml',
      oauth_consumer_secret='6a838d107daf4d09b7d446422f5e7a81',
      server_rest_base='http://api.myspace.com/v2')
    self.container = opensocial.ContainerContext(self.config)
    self.user_id = '425505213'

  def test_fetch_person(self):
    me = self.container.fetch_person(self.user_id)
    self.assertEquals('myspace.com:' + self.user_id, me.get_id())
    self.assertEquals('API', me.get_display_name())
    
  def test_fetch_person_fields(self):
    me = self.container.fetch_person(self.user_id, ['gender'])
    self.assertEquals('Male', me.get_field('gender'))
    
  def test_fetch_friends(self):
    friends = self.container.fetch_friends(self.user_id)
    self.assertEquals(5, len(friends))
    self.assertEquals(1, friends.startIndex)
    self.assertEquals(5, friends.totalResults)
    self.assertEquals('myspace.com:6221', friends[0].get_id())
    self.assertEquals('myspace.com:431404430', friends[1].get_id())
