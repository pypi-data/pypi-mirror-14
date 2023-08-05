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
from mock import Mock

from hamcrest import assert_that, raises, calling

from ubersmith_client.exceptions import UbersmithException, BadRequest, UnknownError, Forbidden, NotFound, Unauthorized
from tests.ubersmith_json.response_data_structure import a_response_data
from ubersmith_client.ubersmith_request import UbersmithRequest


class UbersmithRequestTest(unittest.TestCase):
    def test_process_ubersmith_response(self):
        response = Mock()
        response.status_code = 200
        json_data = {
            'client_id': '1',
            'first': 'Rick',
            'last': 'Sanchez',
            'company': 'Wubba lubba dub dub!'
        }

        response.json = Mock(return_value=a_response_data(data=json_data))

        self.assertDictEqual(json_data, UbersmithRequest.process_ubersmith_response(response))

    def test_process_ubersmith_response_raise_exception(self):
        response = Mock()
        response.status_code = 400
        assert_that(calling(UbersmithRequest.process_ubersmith_response).with_args(response), raises(BadRequest))

        response.status_code = 401
        assert_that(calling(UbersmithRequest.process_ubersmith_response).with_args(response), raises(Unauthorized))

        response.status_code = 403
        assert_that(calling(UbersmithRequest.process_ubersmith_response).with_args(response), raises(Forbidden))

        response.status_code = 404
        assert_that(calling(UbersmithRequest.process_ubersmith_response).with_args(response), raises(NotFound))

        response.status_code = 500
        assert_that(calling(UbersmithRequest.process_ubersmith_response).with_args(response), raises(UnknownError))

        response.status_code = 200
        response.json = Mock(return_value={'status': False, 'error_code': 42, 'error_message': 'come and watch tv'})
        assert_that(calling(UbersmithRequest.process_ubersmith_response).with_args(response),
                    raises(UbersmithException, "Error code 42 - message: come and watch tv"))
