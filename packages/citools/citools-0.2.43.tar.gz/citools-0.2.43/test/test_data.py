from assertpy import assert_that
import datetime
from junit_xml import TestSuite, TestCase
import pytest
from citools.data import TestReport

BUILD_NUMBER = 123

NAME = "name"


class TestTestReport:

    @pytest.fixture
    def empty_report(self):
        """empty test report"""
        return TestReport(NAME, {}, BUILD_NUMBER, True)

    @pytest.fixture
    def simple_report(self):
        """empty test report"""
        test_case_1 = TestCase("testcase1", elapsed_sec=1.5)

        test_case_2 = TestCase("testcase2", elapsed_sec=0.5)
        test_case_2.add_skipped_info("was skipped")

        test_case_3 = TestCase("testcase3", elapsed_sec=1.0)
        test_case_3.add_failure_info("failed")

        test_case_4 = TestCase("testcase4", elapsed_sec=0.25)
        test_case_4.add_error_info("errored")

        test_case_5 = TestCase("testcase5", elapsed_sec=0.1)

        test_cases = [
            test_case_1,
            test_case_2,
            test_case_3,
            test_case_4,
            test_case_5
        ]
        test_suites = [
            TestSuite('testsuite1', test_cases, timestamp=datetime.datetime.utcnow())
            ]
        return TestReport(NAME, {"module": test_suites}, BUILD_NUMBER, True)

    def test_suites(self, empty_report):
        assert_that(list(empty_report.test_suites)).is_empty()

    def test_simple_report_result(self, simple_report):
        assert_that(simple_report.total).is_equal_to(5)
        assert_that(simple_report.is_successful).is_false()
        assert_that(list(simple_report.test_suites)).is_length(1)