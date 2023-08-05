#!/usr/bin/env python
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
import json

import os
import requests


class Jenkins(object):
    API_JSON = "/api/json"

    def __init__(self):
        self.__url = os.environ['JENKINS_URL']
        if self.__url is None:
            raise RuntimeError("JENKINS_URL should be set.")

    @property
    def url(self):
        return self.__url

    def job(self, job_name):
        url = self.job_url(job_name)
        return self.get_api(url)

    def job_url(self, job_name):
        url = "{0}job/{1}".format(self.__url, job_name)
        return url

    def get_api(self, url):
        print('get_api({0})'.format(url + self.API_JSON))
        response = requests.get(url + self.API_JSON)

        if response.status_code != 200:
            print("could not get {0}: status code {1}".format(url, response.status_code))
            return None

        return json.loads(response.text)
