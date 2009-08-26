#!/usr/bin/python

__author__   = 'Dustin Whittle <dustin@yahoo-inc.com>'
__version__  = '0.1'

import os, sys, unittest

# update sys path to include bundled modules with priority
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../src'))

import yahoo.yql

class YQLTest(unittest.TestCase):

  def setUp(self):
    self.yql = yahoo.yql.YQLQuery()

  def test_query_valid(self):
    """
    Tests the calling of yql public api given a valid query.
    """
    response = self.yql.execute('select * from search.web where query="dustin whittle"')
    self.assertTrue('query' in response and 'results' in response['query'])

  def test_query_invalid(self):
    """
    Tests error handling when calling a yql public api given an invalid query.
    """
    response = self.yql.execute('select * from delicious.feeds.unknown_test')
    self.assertEquals('No definition found for Table delicious.feeds.unknown_test', response['error']['description'])

  def tearDown(self):
      self.yql = None


if __name__ == '__main__':
  unittest.main()
