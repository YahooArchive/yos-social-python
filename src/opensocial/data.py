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


def extract_fields(json):
  """Extracts a JSON dict of fields.
  
  REST and RPC protocols use different JSON keys for OpenSocial objects. This
  abstracts that and handles both cases.
  
  Args:
    json: dict The JSON object.
  
  Returns: A JSON dict of field/value pairs.

  """
  return json.get('entry') or json


class Object(dict):
  """Generic container for opensocial.* objects."""

  def get_field(self, name):
    """Retrieves a specific field value for this Object.

    N.B.: Deprecated in favor of type dict methods.
    
    Returns: The field value.

    """ 
    return self.get(name)


class Person(Object):
  """An opensocial.Person representation."""

  def __init__(self, fields):
    super(Person, self).__init__(fields)

  def get_id(self):
    """Returns the id of this Person.
    
    Returns: The container-specific id of this Person.

    """ 
    return self.get_field('id')
      
  def get_display_name(self):
    """Returns the full name of this Person.
    
    Returns: The full name of this Person.

    """
    display_name = self.get_field('displayName')
    if display_name:
      return display_name
    names = self.get_field('name')
    if names:
      return '%s %s' % (names['givenName'], names['familyName'])
    return ''

  @staticmethod
  def parse_json(json):
    """Creates a Person object from a JSON dict of fields.
    Args:
      json: dict The Person fields.
      
    Returns: A Person object.      

    """
    return Person(extract_fields(json))


class AppData(Object):

  def __init__(self, data):
    super(AppData, self).__init__(data)

  @staticmethod
  def parse_json(json):
    return AppData(extract_fields(json))


class Collection(list):
  """Contains a collection of OpenSocial objects.
  
  Handles the parsing of a JSON object and creation of the associated OpenSocial
  data object.

  """
  
  def __init__(self, items, start, total):
    for v in items:
      self.append(v)
    self.startIndex = start
    self.totalResults = total
        
  @staticmethod
  def parse_json(json, cls):
    """Creates a collection from a JSON object returned by an OpenSocial
    container.
    
    Args:
      json: dict The JSON object.
      cls: The OpenSocial data type to instantiate for each entry in the
           collection.
    
    Returns: A Collection of OpenSocial objects.

    """
    
    start = json.get('startIndex')
    total = json.get('totalResults')
    items = []
    json_list = json.get('entry') or json.get('list')      
    for fields in json_list:
      items.append(cls(fields))
    return Collection(items, start, total)
