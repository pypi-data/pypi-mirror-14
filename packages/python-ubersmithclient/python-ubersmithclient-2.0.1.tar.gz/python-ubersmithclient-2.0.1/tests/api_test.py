# Copyright 2016 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest
from hamcrest import assert_that, raises, calling
from mock import Mock
from requests.exceptions import ConnectionError, Timeout

import ubersmith_client
from ubersmith_client.exceptions import UbersmithConnectionError, UbersmithTimeout


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://ubersmith.example.com/'
        self.username = 'admin'
        self.password = 'test'

    def test_api_method_returns_handle_connection_error_exception(self):
        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password)
        ubersmith_api.ubersmith_request = Mock(side_effect=ConnectionError())

        assert_that(calling(ubersmith_api.__getattr__).with_args("client"), raises(UbersmithConnectionError))

    def test_api_method_returns_handle_timeout_exception(self):
        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password)
        ubersmith_api.ubersmith_request = Mock(side_effect=Timeout())

        assert_that(calling(ubersmith_api.__getattr__).with_args("client"), raises(UbersmithTimeout))
