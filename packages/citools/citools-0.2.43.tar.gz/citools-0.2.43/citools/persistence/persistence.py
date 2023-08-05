import shelve


class Persistence(object):
    REPORT_KEY = 'report'
    JOB_INFO_KEY = 'job_info'

    def __init__(self, name):
        self.name = name
        self.shelve = shelve.open(name)

    @property
    def report(self):
        return self.shelve.get(self.REPORT_KEY)

    @report.setter
    def report(self, report):
        self.shelve[self.REPORT_KEY] = report

    @property
    def job_info(self):
        job_info = self.shelve.get(self.JOB_INFO_KEY)
        return job_info if job_info is not None else {}

    def add_job_info(self, job_name, build_number):
        job_info = self.job_info
        job_info[job_name] = build_number
        self.job_info = job_info

    @job_info.setter
    def job_info(self, source_jobs):
        self.shelve[self.JOB_INFO_KEY] = source_jobs

    def add_source_job(self, job_name, build_number):
        self.job_info[job_name] = build_number

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.shelve.close()
