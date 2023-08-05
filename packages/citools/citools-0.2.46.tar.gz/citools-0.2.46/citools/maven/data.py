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

class Artifact(object):
    def __init__(self, group_id, artifact_id, package_type, version):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.package_type = package_type
        self.version = version

    def __repr__(self):
        return "Artifact[{}:{}:{}:{}]".format(self.group_id, self.artifact_id, self.package_type, self.version)


class Dependency(Artifact):
    def __init__(self, group_id, artifact_id, package_type, version, scope):
        super(Dependency, self).__init__(group_id, artifact_id, package_type, version)
        self.scope = scope

    def __repr__(self):
        return "Dependency[{}:{}:{}:{}, scope={}]".format(self.group_id, self.artifact_id, self.package_type,
                                                          self.version, self.scope)
