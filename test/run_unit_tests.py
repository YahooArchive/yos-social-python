#!/usr/bin/python

__author__   = 'Dustin Whittle <dustin@yahoo-inc.com>'
__version__  = '0.1'

import os, sys, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'unit/yahoo/'))
import test_oauth, test_application, test_yql

class TestRunner(object):

  def __init__(self, modules_to_test=None):
    self.modules_to_test = modules_to_test or [test_oauth, test_application, test_yql]

  def RunTests(self):
    runner = unittest.TextTestRunner(verbosity=2)
    for module in self.modules_to_test:
      print '\nRunning tests in module:' + module.__name__
      runner.run(unittest.defaultTestLoader.loadTestsFromModule(module))

def RunTests():
  runner = TestRunner()
  runner.modules_to_test = [test_oauth, test_application, test_yql]
  runner.RunTests()

if __name__ == '__main__':
  RunTests()
