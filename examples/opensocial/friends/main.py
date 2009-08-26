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
import wsgiref
import wsgiref.handlers

from opensocial import *
from google.appengine.ext import webapp


class Handler(webapp.RequestHandler):

  def get(self):
    self.test_friends('03067092798963641994')
 
  def get_container(self):
    config = ContainerConfig(oauth_consumer_key='orkut.com:623061448914',
        oauth_consumer_secret='uynAeXiWTisflWX99KU1D2q5',
        server_rest_base='http://sandbox.orkut.com/social/rest/',
        server_rpc_base='http://sandbox.orkut.com/social/rpc/')
    return ContainerContext(config)
    
  def test_friends(self, user_id):
    container = self.get_container()
    
    batch = RequestBatch()
    batch.add_request('me', request.FetchPersonRequest(user_id))
    batch.add_request('friends',
                      request.FetchPeopleRequest(user_id, '@friends'))
    batch.send(container)
    
    me = batch.get('me')
    friends = batch.get('friends')
    
    self.response.out.write('<h3>Test</h3>')
    self.output(me, friends)

  def output(self, me, friends):
    self.response.out.write('%s\'s Friends: ' % me.get_display_name())
    if not friends:
      self.response.out.write('You have no friends.')
    else:
      self.response.out.write('<ul>')
      for person in friends:
        self.response.out.write('<li>%s</li>' % person.get_display_name())
      self.response.out.write('</ul>')


def main():
  application = webapp.WSGIApplication([
      ('.*', Handler),
  ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
