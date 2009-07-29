"""
Yahoo! Python SDK

 * Yahoo! Query Language
 * Yahoo! Social API

Find documentation and support on Yahoo! Developer Network: http://developer.yahoo.com

Hosted on GitHub: http://github.com/yahoo/yos-social-python/tree/master

@copyright: Copyrights for code authored by Yahoo! Inc. is licensed under the following terms:
@license:   BSD Open Source License

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
"""

__author__   = 'Dustin Whittle <dustin@yahoo-inc.com>'
__version__  = '0.1'

import httplib, urllib, urlparse, cgi, oauthlib.oauth, simplejson

from . import oauth
from . import yql

# Yahoo! Social API
SOCIAL_API_URL = 'http://social.yahooapis.com/v1'

class OAuthApplicationException(Exception):
  pass

class OAuthApplication(object):

  def __init__(self, consumer_key, consumer_secret, application_id, callback_url = None, token = None):

    self.client = oauth.Client()

    self.consumer_key        = consumer_key
    self.consumer_secret     = consumer_secret
    self.application_id      = application_id
    self.callback_url        = callback_url
    self.token               = token

    self.consumer = oauthlib.oauth.OAuthConsumer(self.consumer_key, self.consumer_secret)
    self.signature_method_plaintext = oauthlib.oauth.OAuthSignatureMethod_PLAINTEXT()
    self.signature_method_hmac_sha1 = oauthlib.oauth.OAuthSignatureMethod_HMAC_SHA1()

  # oauth standard apis
  def get_request_token(self):
    parameters = { 'xoauth_lang_pref': 'en' }
    request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(self.consumer, http_method='GET', http_url=self.client.request_token_url, parameters=parameters)
    request.sign_request(self.signature_method_plaintext, self.consumer, None)
    return self.client.fetch_request_token(request)

  def get_authorization_url(self, request_token, callback):
    return oauthlib.oauth.OAuthRequest.from_token_and_callback(token=request_token, callback=callback, http_method='GET', http_url=self.client.authorization_url).to_url()

  def get_access_token(self, request_token, verifier=None):
    if verifier == None:
      parameters = { }
    else:
      parameters = { 'oauth_verifier': verifier }
    request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=request_token, http_method='GET', http_url=self.client.access_token_url, parameters=parameters)
    request.sign_request(self.signature_method_hmac_sha1, self.consumer, request_token)
    self.token = self.client.fetch_access_token(request)
    return self.token

  def refresh_access_token(self, access_token):
    parameters = { 'oauth_session_handle': access_token.session_handle }
    request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=access_token, http_method='GET', http_url=self.client.access_token_url, parameters=parameters)
    request.sign_request(self.signature_method_plaintext, self.consumer, access_token)
    self.token = self.client.fetch_access_token(request)
    return self.token

  def getProfile(self, guid=None):
    if guid == None:
      guid = self.token.yahoo_guid
    url = SOCIAL_API_URL + '/user/%s/profile' % guid
    parameters = { 'format': 'json' }
    request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=self.token, http_method='GET', http_url=url, parameters=parameters)
    request.sign_request(self.signature_method_hmac_sha1, self.consumer, self.token)
    try:
      return simplejson.loads(self.client.access_resource(request))['profile']
    except:
      return False

  def getPresence(self, guid=None):
    if guid == None:
      guid = self.token.yahoo_guid
    url = SOCIAL_API_URL + '/user/%s/presence/presence' % guid
    parameters = { 'format': 'json' }
    request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=self.token, http_method='GET', http_url=url, parameters=parameters)
    request.sign_request(self.signature_method_hmac_sha1, self.consumer, self.token)
    try:
      return simplejson.loads(self.client.access_resource(request))['presence']
    except:
      return False

  def getConnections(self, guid=None, offset=0, limit=10000):
    if guid == None:
      guid = self.token.yahoo_guid
    url = SOCIAL_API_URL + '/user/%s/connections' % guid
    parameters = { 'format': 'json', 'view': 'usercard', 'start': offset, 'count': limit }
    request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=self.token, http_method='GET', http_url=url, parameters=parameters)
    request.sign_request(self.signature_method_hmac_sha1, self.consumer, self.token)
    try:
      return simplejson.loads(self.client.access_resource(request))
    except:
      return False

  def getContacts(self, guid=None, offset=0, limit=10000):
    if guid == None:
      guid = self.token.yahoo_guid
    url = SOCIAL_API_URL + '/user/%s/connections' % guid
    parameters = { 'format': 'json', 'view': 'tinyusercard', 'start': offset, 'count': limit }
    request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=self.token, http_method='GET', http_url=url, parameters=parameters)
    request.sign_request(self.signature_method_hmac_sha1, self.consumer, self.token)
    try:
      return simplejson.loads(self.client.access_resource(request))
    except:
      return False

  def getUpdates(self, guid=None, offset=0, limit=10000):
    if guid == None:
      guid = self.token.yahoo_guid
    url = SOCIAL_API_URL + '/user/%s/updates' % guid
    parameters = { 'format': 'json', 'start': offset, 'count': limit }
    request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=self.token, http_method='GET', http_url=url, parameters=parameters)
    request.sign_request(self.signature_method_hmac_sha1, self.consumer, self.token)
    try:
      return simplejson.loads(self.client.access_resource(request))
    except:
      return False

  def yql(self, query):
    parameters = { 'q': query, 'format': 'json', 'env': yql.DATATABLES_URL }
    request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=self.token, http_method='GET', http_url=yql.OAUTH_API_URL, parameters=parameters)
    request.sign_request(self.signature_method_hmac_sha1, self.consumer, self.token)
    try:
      return simplejson.loads(self.client.access_resource(request))
    except:
      return False

