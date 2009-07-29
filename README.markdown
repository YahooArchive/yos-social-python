Yahoo! Python SDK
=================

Find documentation and support on Yahoo! Developer Network: http://developer.yahoo.com

 * Yahoo! Application Platform - http://developer.yahoo.com/yap/
 * Yahoo! Social APIs - http://developer.yahoo.com/social/
 * Yahoo! Query Language - http://developer.yahoo.com/yql/

Hosted on GitHub: http://github.com/yahoo/yos-social-python/tree/master

License
=======

@copyright: Copyrights for code authored by Yahoo! Inc. is licensed under the following terms:
@license:   MIT Open Source License

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

The Yahoo! Social Python SDK code is subject to the MIT license, see the LICENSE file.


Requirements
============

The following dependencies are bundled with the Yahoo! Python SDK, but are under
terms of a separate license:

 * SimpleJSON - http://code.google.com/p/simplejson
 * OAuth - http://code.google.com/p/oauth
 * OpenID - http://openidenabled.com/python-openid


Install
=======

Simply make sure that this app is on your PYTHON PATH. Once it is in your PYTHON PATH
then to use it in your project. The sdk also requires the oauth and simplejson modules:

    easy_install oauth simplejson
		python setup.py install


Examples
========

## Fetching YQL:
    import yahoo.yql

    response = yahoo.yql.YQLQuery().execute('select * from delicious.feeds.popular')
    if 'query' in response and 'results' in response['query']:
      print response['query']['results']
    elif 'error' in response:
      print 'YQL query failed with error: "%s".' % response['error']['description']
    else:
      print 'YQL response malformed.'


## Fetching Social Data:
    import yahoo.application

		# Yahoo! OAuth Credentials - http://developer.yahoo.com/dashboard/

		CONSUMER_KEY      = '##'
		CONSUMER_SECRET   = '##'
		APPLICATION_ID    = '##'
		CALLBACK_URL      = '##'

		oauthapp      = yahoo.application.OAuthApplication(CONSUMER_KEY, CONSUMER_SECRET, APPLICATION_ID, CALLBACK_URL)

		# Fetch request token
		request_token = oauthapp.get_request_token()

		# Redirect user to authorization url
		redirect_url  = oauthapp.get_authorization_url(request_token, CALLBACK_URL)

		# Exchange request token for authorized access token
		access_token  = oauthapp.get_access_token(request_token)

		# update access token
		oauthapp.token = access_token

		profile = oauthapp.getProfile()

		print profile


Tests
=====

The Yahoo! Python SDK comes with a test suite to validate functionality. The tests also
show functional examples and results. To run the test suite, simply execute the test suite:

    python test/run_unit_tests.py

