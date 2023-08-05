# Copyright 2015 Huawei Technologies Co., Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import mock
import testtools

from mistralclient.api import client


class BaseClientTests(testtools.TestCase):

    @mock.patch('keystoneclient.v3.client.Client')
    @mock.patch('mistralclient.api.httpclient.HTTPClient')
    def test_mistral_url_defult(self, mock, keystone_client_mock):
        client.client(username='mistral',
                      project_name='misteal',
                      auth_url="http://localhost:35357/v3")
        self.assertTrue(mock.called)
        params = mock.call_args
        self.assertEqual('http://localhost:8989/v2',
                         params[0][0])
