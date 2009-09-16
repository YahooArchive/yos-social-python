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

# Yahoo! OAuth Credentials - http://developer.yahoo.com/dashboard/
CONSUMER_KEY      = 'dj0yJmk9UHdCeXB0a3lDUzNhJmQ9WVdrOVdHWlJWRFJaTm0wbWNHbzlNVE01T0RBM05EQTBNdy0tJnM9Y29uc3VtZXJzZWNyZXQmeD1jYw--'
CONSUMER_SECRET   = 'c629e2fce32ceaf981e11f996e6a16beaea59138'
APPLICATION_ID    = 'XfQT4Y6m'
CALLBACK_URL      = 'http://yapdemo.appspot.com/'

##############################################################################
# Requires: Python 2.6 + oauth + simplejson                                  #
##############################################################################

# import required modules
import os, sys, getopt, pprint, logging, cgi, urllib

# import google app engine webapp framework
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch

# update sys path to include bundled modules with priority
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sdk/'))

import oauthlib.oauth, gmemsess
import yahoo.oauth, yahoo.yql, yahoo.application

oauthapp = yahoo.application.OAuthApplication(CONSUMER_KEY, CONSUMER_SECRET, APPLICATION_ID, CALLBACK_URL)

"""
/        -> shows login button, if needed, otherwise shows user profile, connection, and updates
/oauth   -> handled login button -> oauth dance -> get request token -> redirect user -> get access token
"""

class IndexController(webapp.RequestHandler):

    def get(self):

        # create a memcache session for storing oauth tokens
        session = gmemsess.Session(self)

        # user does not have access token
        if 'access_token' not in session:

          # user does not have request token
          if 'request_token' not in session:

            # get request token
            request_token = oauthapp.get_request_token(CALLBACK_URL)

            # store unapproved request token in session
            session['request_token'] = request_token.to_string()
            session.save()

            # redirect the user to authorize the request token
            self.redirect(oauthapp.get_authorization_url(request_token, CALLBACK_URL))

          else:

            # retrieve approved request token from session
            request_token = yahoo.oauth.RequestToken.from_string(session['request_token'])

            # exchange approved request token for valid access token
            access_token = oauthapp.get_access_token(request_token, self.request.get('oauth_verifier'))

            # store access token in session
            session['access_token'] = access_token.to_string()
            session.save()

            self.redirect(CALLBACK_URL)

        else:

          oauthapp.token = yahoo.oauth.AccessToken.from_string(session['access_token'])

          profile     = oauthapp.getProfile()
          connections = oauthapp.getConnections()
          updates     = oauthapp.getUpdates()

          self.response.out.write(template.render(os.path.join(os.path.dirname(__file__), 'templates/social.html'), { 'profile': profile, 'connections': connections, 'updates': updates } ))

          # session.invalidate()


class OAuthController(webapp.RequestHandler):
    def get(self):
        session=gmemsess.Session(self)
        if 'access_token' in session:
            request_token = session['request_token'] if 'request_token' in session else None
            if not request_token:
                self.response.out.write("No un-authed token found in session")
                return
            token = oauth.OAuthToken.from_string(request_token)
            if token.key != urllib.unquote( self.request.get('oauth_token', 'no-token') ):
                self.response.out.write("Something went wrong! Tokens do not match")
                return
            session.save()

            self.redirect('/')

        else:
            path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
            self.response.out.write(template.render(path, {}))

application = webapp.WSGIApplication([('/', IndexController), ('/oauth', OAuthController)], debug=True)

def main():
  logging.getLogger().setLevel(logging.DEBUG)
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
