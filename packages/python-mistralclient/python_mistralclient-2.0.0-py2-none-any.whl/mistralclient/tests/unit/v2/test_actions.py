# Copyright 2015 Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
from mistralclient.api.v2 import actions
from mistralclient.tests.unit.v2 import base


ACTION_DEF = """
---
version: 2.0

my_action:
  base: std.echo
  base-input:
    output: 'Bye!'
  output:
    info: <% $.output %>
"""

ACTION = {
    'id': '123',
    'name': 'my_action',
    'input': '',
    'definition': ACTION_DEF
}

URL_TEMPLATE = '/actions'
URL_TEMPLATE_SCOPE = '/actions?scope=private'
URL_TEMPLATE_NAME = '/actions/%s'


class TestActionsV2(base.BaseClientV2Test):
    def test_create(self):
        mock = self.mock_http_post(content={'actions': [ACTION]})

        actions = self.actions.create(ACTION_DEF)

        self.assertIsNotNone(actions)
        self.assertEqual(ACTION_DEF, actions[0].definition)

        mock.assert_called_once_with(
            URL_TEMPLATE_SCOPE,
            ACTION_DEF,
            headers={'content-type': 'text/plain'}
        )

    def test_update(self):
        mock = self.mock_http_put(content={'actions': [ACTION]})

        actions = self.actions.update(ACTION_DEF)

        self.assertIsNotNone(actions)
        self.assertEqual(ACTION_DEF, actions[0].definition)

        mock.assert_called_once_with(
            URL_TEMPLATE_SCOPE,
            ACTION_DEF,
            headers={'content-type': 'text/plain'}
        )

    def test_list(self):
        mock = self.mock_http_get(content={'actions': [ACTION]})

        action_list = self.actions.list()

        self.assertEqual(1, len(action_list))

        action = action_list[0]

        self.assertEqual(
            actions.Action(self.actions, ACTION).to_dict(),
            action.to_dict()
        )

        mock.assert_called_once_with(URL_TEMPLATE)

    def test_list_with_pagination(self):
        mock = self.mock_http_get(
            content={'actions': [ACTION], 'next': '/actions?fake'}
        )

        action_list = self.actions.list(
            limit=1,
            sort_keys='created_at',
            sort_dirs='asc'
        )

        self.assertEqual(1, len(action_list))

        # The url param order is unpredictable.
        self.assertIn('limit=1', mock.call_args[0][0])
        self.assertIn('sort_keys=created_at', mock.call_args[0][0])
        self.assertIn('sort_dirs=asc', mock.call_args[0][0])

    def test_get(self):
        mock = self.mock_http_get(content=ACTION)

        action = self.actions.get('action')

        self.assertIsNotNone(action)
        self.assertEqual(
            actions.Action(self.actions, ACTION).to_dict(),
            action.to_dict()
        )

        mock.assert_called_once_with(URL_TEMPLATE_NAME % 'action')

    def test_delete(self):
        mock = self.mock_http_delete(status_code=204)

        self.actions.delete('action')

        mock.assert_called_once_with(URL_TEMPLATE_NAME % 'action')
