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
import requests

from ubersmith_client.exceptions import UbersmithException, get_exception_for


def init(url, user, password, timeout=60):
    return UbersmithApi(url, user, password, timeout)


class UbersmithApi(object):
    def __init__(self, url, user, password, timeout):
        self.url = url
        self.user = user
        self.password = password
        self.timeout = timeout

    def __getattr__(self, module):
        return UbersmithRequest(self.url, self.user, self.password, module, self.timeout)


class UbersmithRequest(object):
    def __init__(self, url, user, password, module, timeout):
        self.url = url
        self.user = user
        self.password = password
        self.module = module
        self.methods = []
        self.http_methods = {'GET': 'get', 'POST': 'post'}
        self.timeout = timeout

    def __getattr__(self, function):
        self.methods.append(function)
        return self

    def __call__(self, **kwargs):
        return self.http_get(**kwargs)

    def process_request(self, http_method, **kwargs):
        callable_http_method = getattr(requests, http_method)

        response = callable_http_method(
            self.url,
            auth=(self.user, self.password),
            timeout=self.timeout,
            **kwargs
        )

        if response.status_code < 200 or response.status_code >= 400:
            raise get_exception_for(status_code=response.status_code)

        response_json = response.json()
        if not response_json['status']:
            raise UbersmithException(
                500,
                "error {0}, {1}".format(response_json['error_code'], response_json['error_message'])
            )

        return response.json()["data"]

    def http_get(self, **kwargs):
        self._build_request_params(kwargs)

        response = self.process_request(self.http_methods.get('GET'), params=kwargs)

        return response

    def http_post(self, **kwargs):
        self._build_request_params(kwargs)

        response = self.process_request(self.http_methods.get('POST'), data=kwargs)

        return response

    def _build_request_params(self, kwargs):
        _methods = ".".join(self.methods)
        kwargs['method'] = "{0}.{1}".format(self.module, _methods)
