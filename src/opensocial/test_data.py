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


"""This file provides test data explicitly for usage in library unit tests.""" 


__author__ = 'davidbyttow@google.com (David Byttow)'


import httplib

import data
import simplejson


VIEWER_FIELDS = {
  'entry': {'id': '101',
            'name': {'givenName': 'Kenny', 'familyName': ''}},
}

FRIEND_COLLECTION_FIELDS = {
  'startIndex': 0,
  'totalResults': 3,
  'entry': [
    { 
      'id': '102',
      'name': {'givenName': 'Stan', 'familyName': 'Marsh'},
    },
    { 
      'id': '103',
      'name': {'givenName': 'Kyle', 'familyName': 'Broflovski'},
    },
    { 
      'id': '104',
      'name': {'givenName': 'Eric', 'familyName': 'Cartman'},
    }
  ]
}

VIEWER = data.Person.parse_json(VIEWER_FIELDS)

FRIENDS = data.Collection.parse_json(FRIEND_COLLECTION_FIELDS,
                                     data.Person)

NO_AUTH = { 'error' : { 'code': httplib.UNAUTHORIZED }}