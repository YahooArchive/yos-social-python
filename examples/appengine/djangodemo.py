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
import os, sys, getopt, pprint, pickle, logging

# update sys path to include bundled modules with priority
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sdk/'))

import oauthlib.oauth

import yahoo.oauth, yahoo.yql, yahoo.application


# google app engine: django 1.0 support
from google.appengine.dist import use_library
use_library('django', '1.0')

from google.appengine.ext.webapp import util

# Force Django to reload its settings.
from django.conf import settings
settings._target = None

# Must set this env var before importing any part of Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import logging
import django.core.handlers.wsgi
import django.core.signals
import django.db
import django.dispatch.dispatcher

def log_exception(*args, **kwds):
  logging.exception('Exception in request:')

# Log errors.
django.dispatch.dispatcher.connect( log_exception, django.core.signals.got_request_exception)

# Unregister the rollback event handler.
django.dispatch.dispatcher.disconnect(django.db._rollback_on_exception,django.core.signals.got_request_exception)

def main():

  # Create a Django application for WSGI.
  application = django.core.handlers.wsgi.WSGIHandler()


  # Run the WSGI CGI handler with that application.
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
