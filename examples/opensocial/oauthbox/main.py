#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import logging
import wsgiref.handlers

import opensocial

from opensocial import simplejson
from opensocial import oauth
from google.appengine.ext import webapp


class MainHandler(webapp.RequestHandler):

  def get(self):
    pass

  def post(self):
    oauth_version = self.request.get('oauth_version')
    oauth_nonce = self.request.get('oauth_nonce')
    oauth_timestamp = self.request.get('oauth_timestamp')
    oauth_consumer_key = self.request.get('oauth_consumer_key')
    oauth_signature = self.request.get('oauth_signature')
    xoauth_requestor_id = self.request.get('xoauth_requestor_id')
    opensocial_method = self.request.get('opensocial_method')
    post_body = self.request.body
    post_data = simplejson.loads(post_body)[0]
    id = post_data.get('id')
    
    params = {}
    for key, value in self.request.params.mixed().items():
      params[key] = value.encode('utf-8', 'ignore')

    oauth_request = oauth.OAuthRequest.from_request(self.request.method,
                                                    self.request.url,
                                                    params)
    consumer = oauth.OAuthConsumer('oauth.org:123456789', 'not_a_secret')

    signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
    built_signature = signature_method.build_signature(oauth_request,
                                                       consumer, 
                                                       None)
    verified = built_signature == oauth_signature
    data = {
      'request': {
        'method': self.request.method,
        'url': self.request.url,
        'oauth_version': oauth_version,
        'oauth_nonce': oauth_nonce,
        'oauth_timestamp': oauth_timestamp,
        'oauth_consumer_key': oauth_consumer_key,
        'oauth_signature': oauth_signature,
        'post_body': post_body
      },
      'response': {
        'built_signature': built_signature
      },
      'verified': str(verified),
    }

    json = {
      'id': id,
      'data': data
    }
    
    output = simplejson.dumps([json])
    if verified:
      logging.info(output)
    else:
      logging.error(output)
    self.response.out.write(output)


def main():
  application = webapp.WSGIApplication([('.*', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
