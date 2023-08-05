import os
import tempfile
from unittest import TestCase
from assertpy import assert_that
from citools.persistence import Persistence


class PersistenceTest(TestCase):
    def setUp(self):
        temp_dir = tempfile.mkdtemp(prefix='persistence_test')
        self.persistence_file_name = os.path.join(temp_dir, 'name')
        self.persistence = Persistence(self.persistence_file_name)

    def tearDown(self):
        self.persistence.close()
        os.unlink(self.persistence_file_name)
        os.rmdir(os.path.dirname(self.persistence_file_name))

    def test_with_block(self):
        report = self.persistence.report

        assert_that(report).is_none()

        report_object = "foo"

        self.persistence.close()
        with Persistence(self.persistence_file_name) as persistence:
            persistence.report = report_object

        with Persistence(self.persistence_file_name) as persistence:
            report = persistence.report

        assert_that(report).is_equal_to(report_object)

    def test_with_block_with_non_existent_path(self):
        self.assertRaises(Exception, self.with_block_with_non_existent_path)

    def with_block_with_non_existent_path(self):
        with Persistence('/non/existent/path') as _:
            pass

    def test_add_job_info(self):
        self.persistence.add_job_info('job_name', 4234)

        assert_that(self.persistence.job_info).contains_entry({'job_name': 4234})
