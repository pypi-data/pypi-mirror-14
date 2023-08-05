# Copyright 2013-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# is located at
# 
#     http://aws.amazon.com/apache2.0/
# 
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

import unittest
from nose.tools import *
from mock import call, patch, MagicMock, Mock
from luna_device_connections.luna_adapter import LunaAdapter

class TestLunaAdapter(unittest.TestCase):
    def test_get_to_device_prompt_returns_to_prompt_by_calling_quit(self):
        '''
        Test that the _get_to_device_prompt method calls quit if there's a timeout
        '''
        mock_conn = Mock()
        mock_conn._send_command_and_return_response.return_value = 'some luna stuff'
        mock_conn._send_command_and_error_on_unexpected_output = Mock()

        adapter = LunaAdapter(mock_conn)
        adapter._get_to_device_prompt()
        assert_equals(
                      mock_conn._send_command_and_return_response.call_args_list,
                      [call('', end_condition_regex='lunash'), call('quit', 'lunash')]
                     )
 
    def test_get_to_device_prompt_returns_to_prompt(self):
        '''
        Test that the _get_to_device_prompt method doesn't send any more commands if it gets back to the Luna shell
        '''
        mock_conn = Mock()
        mock_conn._send_command_and_return_response.return_value = '[hsm-megazord] lunash:>'
        mock_conn._send_command_and_error_on_unexpected_output = Mock()

        adapter = LunaAdapter(mock_conn)
        adapter._get_to_device_prompt()
        assert_equals(mock_conn._send_command_and_error_on_unexpected_output.call_count, 0)

