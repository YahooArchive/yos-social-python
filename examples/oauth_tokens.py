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

##############################################################################
# Requires: Python 2.6 + oauth + simplejson                                  #
# Install dependencies at system level: easy_install oauth simplejson        #
##############################################################################

# import required modules
import os, sys, getopt, pprint, pickle

# update sys path to include bundled modules with priority
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import oauthlib.oauth

import yahoo.oauth, yahoo.yql, yahoo.application


# Yahoo! OAuth Credentials - http://developer.yahoo.com/dashboard/
CONSUMER_KEY      = 'dj0yJmk9WUxPUkhFUWxISWpvJmQ9WVdrOWFYWmhTVzVDTXpBbWNHbzlNVGt4TmpJNU1EazROdy0tJnM9Y29uc3VtZXJzZWNyZXQmeD01Ng--'
CONSUMER_SECRET   = 'f893cf549be5cb37f83b1414e2ff212df2ea4c18'
APPLICATION_ID    = 'ivaInB30'
CALLBACK_URL      = 'http://imaginingtheweb.com/'

TOKEN_STORAGE     = '/tmp/access_token.pkl'

def main():
  """
  Demonstrates fetching of oauth tokens from yahoo apis
  """

  ck  = CONSUMER_KEY
  cks = CONSUMER_SECRET
  app = APPLICATION_ID
  cb  = CALLBACK_URL

  # use command line options if present, otherwise prompt user
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['ck=','cks=','app=','cb='])
    for option, arg in opts:
      if option == '--ck':
        ck = arg
      if option == '--cks':
        cks = arg
      if option == '--app':
        app = arg
      if option == '--cb':
        cb = arg

    while not ck:
      ck = raw_input('Please enter consumer key: ')
    while not cks:
      cks = raw_input('Please enter consumer key secret: ')
    while not app:
      app = raw_input('Please enter application id: ')
    while not cb:
      cb = raw_input('Please enter callback url: ')
  except getopt.error, msg:
    print ('python basic.py')
    sys.exit(2)

  # make public request for data oauth requests for profiles
  oauthapp = yahoo.application.OAuthApplication(ck, cks, app, cb)

  # check if we've got a stored token
  try:
    pkl_file=open(TOKEN_STORAGE, 'rb')
    access_token=pickle.load(pkl_file)
    pkl_file.close()
  except:
    access_token=None
  if access_token:
    print 'You have an access token: %s' % str(access_token.to_string())
  else:
    # get request token
    print '* Obtain a request token ...'
    request_token = oauthapp.get_request_token()

    # authorize the request token
    print '\n* Authorize the request token ...'
    print '\nAuthorization URL:\n%s' % oauthapp.get_authorization_url(request_token, CALLBACK_URL)
    verifier = raw_input('Please authorize the url above ^^^')

    # now the token we get back is an access token
    print '\n* Obtain an access token ...'
    access_token = oauthapp.get_access_token(request_token)
    print '\nkey: %s' % str(access_token.key)
    print 'secret: %s' % str(access_token.secret)
    print 'yahoo guid: %s' % str(access_token.yahoo_guid)

    pkl_file=open(TOKEN_STORAGE, 'wb')
    pickle.dump(access_token, pkl_file)
    pkl_file.close()


  # set access token for oauth app
  oauthapp.token = access_token

  pprint.PrettyPrinter(indent=2).pprint(oauthapp.getProfile())



if __name__ == '__main__':
  main()
