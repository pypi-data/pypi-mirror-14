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

import collections


class TestReport(object):
    def __init__(self, name, suites_by_module, build_number, is_incremental):
        self.name = name

        self.suites_by_module = suites_by_module
        self.build_number = build_number
        self.is_incremental = is_incremental

    def accumulate_results(self):
        results = collections.defaultdict(int)
        for suites in self.suites_by_module.values():
            for suite in suites:
                self.test_suite_result(suite, results)
        return results

    def test_suite_result(self, test_suite, result):
        for test_case in test_suite.test_cases:
            result[self.test_case_result(test_case)] += 1

    def test_case_result(self, test_case):
        if test_case.is_skipped():
            return "SKIPPED"
        elif test_case.is_failure():
            return "FAILED"
        elif test_case.is_error():
            return "ERROR"
        else:
            return "PASSED"

    @property
    def test_suites(self):
        for suites in self.suites_by_module.values():
            for suite in suites:
                yield suite

    @property
    def total(self):
        return sum(self.accumulate_results().values())

    @property
    def is_successful(self):
        results = self.accumulate_results()
        return results['ERROR'] == 0 and results['FAILED'] == 0 and results['PASSED'] > 0

    def __repr__(self):
        results = self.accumulate_results()
        return "TestReport(total=" + str(self.total) + ", skipped=" + str(results['SKIPPED']) + ", failures=" \
               + str(results['FAILED']) + ", errors=" + str(results['ERROR']) + ", #suites=" + str(
            len(self.suites_by_module)) + ")"


class Failure(object):
    def __init__(self, message, type):
        self.message = message
        self.type = type
