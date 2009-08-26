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
import os, sys, getopt, pprint

# update sys path to include bundled modules with priority
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import yahoo.yql

def main():
  """
  Demonstrates usage of YQL (public api) via commandline:
  """

  yql = ''

  # use command line options if present, otherwise prompt user
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['yql='])
    for option, arg in opts:
      if option == '--yql':
        yql = arg
    while not yql:
      yql = raw_input('Please enter yql query: ')
  except getopt.error, msg:
    print ('python yql.py --yql="select * from delicious.feeds.popular"')
    sys.exit(2)

  # make public yql call
  response = yahoo.yql.YQLQuery().execute(yql)
  if 'query' in response and 'results' in response['query']:
    pprint.PrettyPrinter(indent=2).pprint(response['query']['results'])
  elif 'error' in response:
    print 'YQL query failed with error: "%s".' % response['error']['description']
  else:
    print 'YQL response malformed.'


if __name__ == '__main__':
  main()
