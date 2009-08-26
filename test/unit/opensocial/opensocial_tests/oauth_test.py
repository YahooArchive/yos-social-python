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


import logging
import unittest
import urllib2

import opensocial

from opensocial import oauth


class TestOAuth(unittest.TestCase):
  
  def setUp(self):
    self.config = opensocial.ContainerConfig(
        oauth_consumer_key='oauth.org:12345689',
        oauth_consumer_secret='not_a_secret',
        server_rpc_base='http://oauthbox.appspot.com/rpc')
    self.container = opensocial.ContainerContext(self.config)
    self.user_id = '101'

  def test_fetch(self):
    data = self.container.fetch_person(self.user_id)
    self.assertEquals(data.get_field('verified'), 'True')

