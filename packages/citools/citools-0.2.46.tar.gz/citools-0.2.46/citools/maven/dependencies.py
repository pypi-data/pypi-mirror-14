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

from subprocess import Popen, PIPE
import re

from .data import Dependency


class DependencyList(object):
    regexp = re.compile(r'([\w\.-]*):([\w\.-]*):(\w*):([\w\.-]*):(\w*)')

    def get_dependencies(self, project_name):
        pipe = Popen(['mvn', 'dependencies:list', '-pl', project_name], stdout=PIPE)
        (dependencies_output, _) = pipe.communicate()

        return self.parse_dependencies(dependencies_output)

    def parse_dependencies(self, output):
        dependency_matches = self.regexp.findall(output)

        return [Dependency(*match) for match in dependency_matches]
