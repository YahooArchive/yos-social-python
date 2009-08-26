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


__author__ = 'kurrik@google.com (Arne Roomann-Kurrik)'


import unittest
import urllib2

import opensocial
from opensocial import errors

class TestGoogleSandbox(unittest.TestCase):
  
  def setUp(self):
    self.config = opensocial.ContainerConfig(      
        oauth_consumer_key='google.com:249475676706',
        oauth_consumer_secret='fWPcoVP6DOLVqZOF2HH+ihU2',
        server_rpc_base='http://www-opensocial-sandbox.googleusercontent.com/api/rpc',
    )
    self.container = opensocial.ContainerContext(self.config)
    self.user_id = '101911127807751034357'


  def test_invalid_request(self):
    # Invalid ID
    req_error1 = opensocial.FetchAppDataRequest('asfsdkfaja','@self')

    # Single response raises an Error
    self.assertRaises(errors.Error, self.container.send_request, req_error1)

    batch = opensocial.RequestBatch()
    batch.add_request('er1', req_error1)
    batch.send(self.container)
    
    # Batch responses return an Error
    self.assertTrue(isinstance(batch.get('er1'), errors.Error))
    