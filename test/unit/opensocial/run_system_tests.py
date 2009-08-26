#!/usr/bin/python
#
# Copyright (C) 2007, 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'davidbyttow@google.com (David Byttow)'


import module_test_runner
import opensocial_tests.orkut_test
import opensocial_tests.myspace_test
import opensocial_tests.partuza_test
import opensocial_tests.oauth_test
import opensocial_tests.google_sandbox_test

def RunSystemTests():
  test_runner = module_test_runner.ModuleTestRunner()
  test_runner.modules = [
       opensocial_tests.orkut_test,
       opensocial_tests.myspace_test,
       opensocial_tests.partuza_test,                  
       opensocial_tests.oauth_test,
       opensocial_tests.google_sandbox_test,
  ]
  test_runner.RunAllTests()


if __name__ == '__main__':
  RunSystemTests()
