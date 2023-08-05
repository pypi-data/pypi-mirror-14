# coding=utf-8

"""

   Copyright 2015 Andreas Würl

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""

from __future__ import print_function
import os

import unittest
from assertpy import assert_that

from citools.maven.dependencies import DependencyList


class TestDependencies(unittest.TestCase):
    def setUp(self):
        self.dependency_list = DependencyList()

    def test_parsing_of_dependency_list_output(self):
        with open(os.path.join(os.path.dirname(__file__), 'mvn_dependency_list_output.txt'), 'r') as output_file:
            output = output_file.read()

        dependencies = self.dependency_list.parse_dependencies(output)

        assert_that(dependencies).is_length(22)
