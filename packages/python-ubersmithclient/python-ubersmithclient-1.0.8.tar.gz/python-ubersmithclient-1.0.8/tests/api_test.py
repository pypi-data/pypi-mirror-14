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
import base64
import unittest
import six.moves.urllib.parse as urllib_parse

import requests

from flexmock import flexmock, flexmock_teardown
from hamcrest import assert_that, equal_to, raises, calling
import requests_mock
from requests_mock.exceptions import NoMockAddress
import ubersmith_client
from ubersmith_client import api
from ubersmith_client.exceptions import BadRequest, UnknownError, Forbidden, NotFound, Unauthorized
from tests.ubersmith_json.response_data_structure import a_response_data


class UbersmithIWebTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://ubersmith.example.org/'
        self.username = 'admin'
        self.password = 'test'

    def tearDown(self):
        flexmock_teardown()

    @requests_mock.mock()
    def test_api_method_returns_without_arguments(self, request_mock):
        json_data = [
            {
                'client_id': '1',
                'first': 'John',
                'last': 'Snow',
                'company': 'The Night Watch'
            }
        ]
        data = a_response_data(data=json_data)
        self.expect_a_ubersmith_call(request_mock, "client.list", data=data)

        ubersmith_api = api.init(self.url, self.username, self.password)
        response = ubersmith_api.client.list()

        assert_that(response, equal_to(json_data))

    @requests_mock.mock()
    def test_api_method_returns_with_arguments(self, request_mock):
        json_data = {
            'group_id': '1',
            'client_id': '30001',
            'assignment_count': '1'
        }
        data = a_response_data(data=json_data)
        self.expect_a_ubersmith_call(request_mock, method="device.ip_group_list", fac_id='1', client_id='30001',
                                     data=data)

        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password)
        response = ubersmith_api.device.ip_group_list(fac_id=1, client_id=30001)

        assert_that(response, equal_to(json_data))

    @requests_mock.mock()
    def test_api_raises_exception_with_if_data_status_is_false(self, request_mock):
        data = a_response_data(status=False, error_code=1, error_message="invalid method specified: client.miss",
                               data=None)
        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password)

        self.expect_a_ubersmith_call(request_mock, method="client.miss", data=data)
        assert_that(calling(ubersmith_api.client.miss), raises(ubersmith_client.exceptions.UbersmithException))

    @requests_mock.mock()
    def test_api_raises_exception_for_invalid_status_code(self, request_mock):
        method = "client.list"
        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password)

        self.expect_a_ubersmith_call(request_mock, method=method, status_code=400)

        assert_that(calling(ubersmith_api.client.list), raises(BadRequest))

        self.expect_a_ubersmith_call(request_mock, method=method, status_code=401)
        assert_that(calling(ubersmith_api.client.list), raises(Unauthorized))

        self.expect_a_ubersmith_call(request_mock, method=method, status_code=403)
        assert_that(calling(ubersmith_api.client.list), raises(Forbidden))

        self.expect_a_ubersmith_call(request_mock, method=method, status_code=404)
        assert_that(calling(ubersmith_api.client.list), raises(NotFound))

        self.expect_a_ubersmith_call(request_mock, method=method, status_code=500)
        assert_that(calling(ubersmith_api.client.list), raises(UnknownError))

    @requests_mock.mock()
    def test_api_with_a_false_identifier(self, request_mock):
        method = "client.list"
        self.expect_a_ubersmith_call(request_mock, method=method)
        ubersmith_api = ubersmith_client.api.init(self.url, 'not_hapi', 'lol')

        with self.assertRaises(NoMockAddress) as ube:
            ubersmith_api.client.list()

        assert_that(str(ube.exception), equal_to("No mock address: GET " + self.url + "?method=" + method))

    @requests_mock.mock()
    def test_api_http_get_method(self, request_mock):
        json_data = {
            'group_id': '666',
            'client_id': '30666',
            'assignment_count': '1'
        }
        data = a_response_data(data=json_data)
        self.expect_a_ubersmith_call(request_mock, method="device.ip_group_list", fac_id='666', client_id='30666',
                                     data=data)

        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password)
        response = ubersmith_api.device.ip_group_list.http_get(fac_id=666, client_id=30666)

        assert_that(response, equal_to(json_data))

    @requests_mock.mock()
    def test_api_http_get_method_default(self, request_mock):
        json_data = {
            'group_id': '666',
            'client_id': '30666',
            'assignment_count': '1'
        }
        data = a_response_data(data=json_data)
        self.expect_a_ubersmith_call(request_mock, method="device.ip_group_list", fac_id='666', client_id='30666',
                                     data=data)

        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password)
        response = ubersmith_api.device.ip_group_list(fac_id=666, client_id=30666)

        assert_that(response, equal_to(json_data))

    @requests_mock.mock()
    def test_api_http_post_method_default(self, request_mock):
        json_data = {
            'group_id': '666',
            'client_id': '30666',
            'assignment_count': '1'
        }
        data = a_response_data(data=json_data)
        self.expect_a_ubersmith_call_post(request_mock, method='device.ip_group_list', fac_id='666', client_id='30666',
                                          response_body=data)

        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password, use_http_post=True)
        response = ubersmith_api.device.ip_group_list(fac_id=666, client_id=30666)

        assert_that(response, equal_to(json_data))

    @requests_mock.mock()
    def test_api_http_post_method_result_200(self, request_mock):
        json_data = {
            'data': '778',
            'error_code': None,
            'error_message': '',
            'status': True
        }

        self.expect_a_ubersmith_call_post(
            request_mock,
            method='support.ticket_submit',
            body='ticket body',
            subject='ticket subject',
            response_body=json_data,
        )

        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password)
        response = ubersmith_api.support.ticket_submit.http_post(body='ticket body', subject='ticket subject')

        assert_that(response, equal_to(json_data.get('data')))

    @requests_mock.mock()
    def test_api_http_post_method_raises_on_result_414(self, request_mock):
        json_data = {
            'data': '778',
            'error_code': None,
            'error_message': '',
            'status': True
        }

        self.expect_a_ubersmith_call_post(
            request_mock,
            method='support.ticket_submit',
            response_body=json_data,
            status_code=414
        )

        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password)

        assert_that(calling(ubersmith_api.support.ticket_submit.http_post), raises(UnknownError))

    def test_api_http_timeout(self):
        payload = dict(status=True, data="plop")
        response = flexmock(status_code=200, json=lambda: payload)
        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password, 666)

        flexmock(requests).should_receive("get").with_args(
            url=self.url, auth=(self.username, self.password), timeout=666, params={'method': 'uber.method_list'}
        ).and_return(response)

        ubersmith_api.uber.method_list()

    def test_api_http_default_timeout(self):
        payload = dict(status=True, data="plop")
        response = flexmock(status_code=200, json=lambda: payload)
        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password)

        flexmock(requests).should_receive("get").with_args(
            url=self.url, auth=(self.username, self.password), timeout=60, params={'method': 'uber.method_list'}
        ).and_return(response)

        ubersmith_api.uber.method_list()

    @requests_mock.mock()
    def test_api_http_post_method_raises_on_result_500(self, request_mock):
        json_data = {
            'data': '778',
            'error_code': None,
            'error_message': '',
            'status': False
        }

        self.expect_a_ubersmith_call_post(
            request_mock,
            method='support.ticket_submit',
            response_body=json_data,
        )

        ubersmith_api = ubersmith_client.api.init(self.url, self.username, self.password)

        assert_that(calling(ubersmith_api.support.ticket_submit.http_post),
                    raises(ubersmith_client.exceptions.UbersmithException))

    def expect_a_ubersmith_call(self, request_mock, method, data=None, status_code=200, **kwargs):
        url = self.url + '?' + get_url_params(method, **kwargs)
        headers = {
            'Content-Type': 'application/json',
        }
        request_mock.get(url, json=data, headers=headers, request_headers={
            'Authorization': self.get_auth_header()
        }, status_code=status_code)

    def expect_a_ubersmith_call_post(self, request_mock, method, response_body=None, status_code=200, **kwargs):
        headers = {
            'Content-Type': 'application/json',
        }
        expected_text = get_url_params(method, **kwargs)

        def response_callback(request, context):
            expected_params = urllib_parse.parse_qs(expected_text)
            parsed_params = urllib_parse.parse_qs(request.text)
            assert_that(parsed_params, equal_to(expected_params))
            return response_body

        request_mock.post(self.url, json=response_callback, headers=headers, request_headers={
            'Authorization': self.get_auth_header(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }, status_code=status_code)

    def get_auth_header(self):
        auth = base64.b64encode((self.username + ':' + self.password).encode('utf-8'))
        return 'Basic ' + auth.decode('utf-8')


def get_url_params(method, **kwargs):
    kwargs['method'] = method
    return urllib_parse.urlencode(kwargs)
