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

import httplib, urllib, urlparse, cgi, oauthlib.oauth

# Yahoo! OAuth APIs
REQUEST_TOKEN_API_URL = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
AUTHORIZATION_API_URL = 'https://api.login.yahoo.com/oauth/v2/request_auth'
ACCESS_TOKEN_API_URL  = 'https://api.login.yahoo.com/oauth/v2/get_token'

# http://developer.yahoo.com/oauth/guide/oauth-auth-flow.html


class RequestToken(oauthlib.oauth.OAuthToken):
  """
  RequestToken is a data type that represents an end user via a request token.

  key -- the token
  secret -- the token secret
  expires_in -- authorization expiration from issue
  request_auth_url -- request token authorization url

  """
  key              = None
  secret           = None
  expires_in       = None
  request_auth_url = None

  def __init__(self, key, secret, expires_in=None, request_auth_url=None):
    self.key = key
    self.secret = secret
    self.expires_in = expires_in
    self.request_auth_url = request_auth_url

  def to_string(self):
    return urllib.urlencode({'oauth_token': self.key,
                             'oauth_token_secret': self.secret,
                             'oauth_expires_in': self.expires_in,
                             'xoauth_request_auth_url': self.request_auth_url
                             })

  def from_string(s):
    """
    Returns a token from something like: oauth_token_secret=xxx&oauth_token=xxx
    """
    params = cgi.parse_qs(s, keep_blank_values=False)
    key = params['oauth_token'][0]
    secret = params['oauth_token_secret'][0]
    expires_in = params['oauth_expires_in'][0]
    request_auth_url = params['xoauth_request_auth_url'][0]
    return RequestToken(key, secret, expires_in, request_auth_url)
  from_string = staticmethod(from_string)


class AccessToken(oauthlib.oauth.OAuthToken):
  """
  AccessToken is a data type that represents an end user via an access token.

  key -- the token
  secret -- the token secret
  expires_in -- authorization expiration from issue
  session_handle -- scalable oauth session handle
  authorization_expires_in -- authorization expiration timestamp
  yahoo_guid -- yahoo guid

  """
  key                      = None
  secret                   = None
  expires_in               = None
  session_handle           = None
  authorization_expires_in = None
  yahoo_guid               = None

  def __init__(self, key, secret, expires_in=None, session_handle=None, authorization_expires_in=None, yahoo_guid=None):
    self.key = key
    self.secret = secret
    self.expires_in = expires_in
    self.session_handle = session_handle
    self.authorization_expires_in = authorization_expires_in
    self.yahoo_guid = yahoo_guid

  def to_string(self):
    return urllib.urlencode({'oauth_token': self.key,
                             'oauth_token_secret': self.secret,
                             'oauth_expires_in': self.expires_in,
                             'oauth_session_handle': self.session_handle,
                             'oauth_authorization_expires_in': self.authorization_expires_in,
                             'xoauth_yahoo_guid': self.yahoo_guid
                             })

  def from_string(s):
    """
    Returns a token from something like: oauth_token_secret=xxx&oauth_token=xxx
    """
    params = cgi.parse_qs(s, keep_blank_values=False)

    key = params['oauth_token'][0]
    secret = params['oauth_token_secret'][0]
    expires_in = params['oauth_expires_in'][0]
    session_handle = params['oauth_session_handle'][0]
    authorization_expires_in = params['oauth_authorization_expires_in'][0]
    yahoo_guid = params['xoauth_yahoo_guid'][0]

    return AccessToken(key, secret, expires_in, session_handle, authorization_expires_in, yahoo_guid)
  from_string = staticmethod(from_string)


class Client(oauthlib.oauth.OAuthClient):

  def __init__(self, server='https://api.login.yahoo.com/', port=httplib.HTTPS_PORT, request_token_url=REQUEST_TOKEN_API_URL, access_token_url=ACCESS_TOKEN_API_URL, authorization_url=AUTHORIZATION_API_URL):
    urlData = urlparse.urlparse(server)

    self.server            = urlData.netloc
    self.port              = port
    self.request_token_url = request_token_url
    self.access_token_url  = access_token_url
    self.authorization_url = authorization_url

    if urlData.scheme == 'https':
      self.connection = httplib.HTTPSConnection("%s:%d" % (urlData.netloc, self.port))
    else:
      self.connection = httplib.HTTPConnection("%s:%d" % (urlData.netloc, self.port))

#    self.connection.set_debuglevel(3)

  def fetch_request_token(self, oauth_request):
    self.connection.request(oauth_request.http_method, self.request_token_url, headers=oauth_request.to_header('yahooapis.com'))
    return RequestToken.from_string(self.connection.getresponse().read().strip())

  def fetch_access_token(self, oauth_request):
    self.connection.request(oauth_request.http_method, self.access_token_url, headers=oauth_request.to_header('yahooapis.com'))
    return AccessToken.from_string(self.connection.getresponse().read().strip())

  def authorize_token(self, oauth_request):
    self.connection.request(oauth_request.http_method, self.authorization_url, headers=oauth_request.to_header('yahooapis.com'))
    return self.connection.getresponse().read().strip()

  def access_resource(self, oauth_request, body = None):
    urlData = urlparse.urlparse(oauth_request.get_normalized_http_url())

    if urlData.scheme == 'https':
      connection = httplib.HTTPSConnection("%s:443" % urlData.netloc)
    else:
      connection = httplib.HTTPConnection("%s:80" % urlData.netloc)

    if oauth_request.http_method == 'GET':
      connection.request(oauth_request.http_method, oauth_request.to_url())
    elif oauth_request.http_method in ('PUT', 'POST', 'DELETE'):
      connection.request(oauth_request.http_method, oauth_request.to_url(), body=body)
    else:
      connection.request(oauth_request.http_method, oauth_request.to_url())

    return connection.getresponse().read().strip()
