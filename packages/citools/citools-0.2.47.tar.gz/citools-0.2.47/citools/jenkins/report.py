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

from junit_xml import TestCase, TestSuite
from ..data import TestReport


class Report(object):
    CASE_MAP = {'skipped': None, 'failedSince': None, 'className': 'classname', 'age': None}
    SUITE_MAP = {'timestamp': None, 'cases': 'testcases', 'id': None}

    def __init__(self, jenkins):
        self.jenkins = jenkins

    def get_report(self, job_name, build_number=None):
        project_info = self.jenkins.job(job_name)

        if build_number is None:
            build_number = project_info['lastCompletedBuild']['number']
        else:
            build_number = int(build_number)

        build_url = next(
            iter([build['url'] for build in project_info['builds'] if build['number'] == build_number]), None)

        if build_url is None:
            raise ValueError("no build with number {} found".format(build_number))

        build_info = self.jenkins.get_api(build_url)

        timestamp = build_info['timestamp']

        test_report = self.jenkins.get_api(build_url + '/testReport')

        suites_by_module = {}

        job_url = self.jenkins.job_url(job_name)
        if test_report is not None and 'childReports' in test_report:
            for child_report in test_report['childReports']:
                child_result = child_report['result']

                if 'child' in child_report and 'url' in child_report['child']:
                    module_url = child_report['child']['url']
                    module = module_url[len(job_url):].split('/')[1].replace('$', ':')

                    suites = [self.create_suite(suite, timestamp, module) for suite in child_result['suites']]
                    suites_by_module[module] = suites
                else:
                    print("ERROR: unknown module in ", child_report)

        is_incremental = bool([cause for cause in self.get_causes(build_info['actions'])
                               if cause['shortDescription'] == "Started by an SCM change"
                               or cause['shortDescription'].startswith("commit notification ")])

        print("causes: " + ", ".join(
            [str(cause) for cause in self.get_causes(build_info['actions'])]))

        return TestReport(build_info['displayName'], suites_by_module,
                          build_number, is_incremental)

    def create_suite(self, props, timestamp, module):
        props = self.map_keys(props, self.SUITE_MAP)

        test_cases = [self.create_case(case) for case in props['testcases']]
        test_cases = [test_case for test_case in test_cases if test_case is not None]

        return TestSuite(props['name'].decode('ascii', 'ignore'), test_cases=test_cases, timestamp=timestamp, package=module)

    def create_case(self, props):
        try:
            test_case = TestCase(classname=props['className'].decode('ascii'), elapsed_sec=props['duration'], name=props['name'].decode('ascii', 'ignore'))
        except UnicodeEncodeError:
            return None

        status = props['status']
        if status == 'SKIPPED':
            test_case.add_skipped_info(status)
        elif status == 'FAILED':
            test_case.add_failure_info(status)
        elif status == 'ERROR':
            test_case.add_error_info(status)

        return test_case

    def map_keys(self, target, key_map):
        for old_key, new_key in key_map.iteritems():
            value = target.pop(old_key)
            if value is not None and new_key is not None:
                target[new_key] = value

        return target

    def get_causes(self, actions):
        for action in actions:
            if 'causes' in action:
                return action['causes']
        return []
