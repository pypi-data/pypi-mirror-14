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
import logging
import re
from luna_manipulator.luna_manipulating_adapter_53 import LunaManipulatingAdapter53
import luna_device_connections.luna_outputs as utils

class TestLunaManipulatingAdapter53(unittest.TestCase):
    def test_add_syslog_host_adds_host_successfully_when_host_is_valid_Ip_53(self):
        '''
        Test that host is added as remote syslog host, if it is a valid IP (on a 5.3 HSM)
        '''
        adapter = LunaManipulatingAdapter53(MagicMock())
        adapter.send_command_and_check_output= MagicMock()
        adapter.add_syslog_host(host='10.2.106.67')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call("syslog remotehost add -host 10.2.106.67", utils.expected_syslog_host_added_output, suppress=False, timeout = 600)])

    def test_add_syslog_host_and_restart_syslog_adds_host_successfully_when_host_is_valid_Ip_53(self):
        '''
        Test that host is added as remote syslog host, if it is a valid IP (on a 5.3 HSM)
        '''
        adapter = LunaManipulatingAdapter53(MagicMock())
        adapter.send_command_and_check_output= MagicMock()
        adapter.add_syslog_host(host='10.2.106.67')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call("syslog remotehost add -host 10.2.106.67", utils.expected_syslog_host_added_output, suppress=False, timeout = 600)])

    def test_remove_syslog_host_deletes_host_successfully_when_host_is_valid_Ip_53(self):
        '''
        Test that host is removed as syslog server, if it is a valid IP
        '''

        adapter = LunaManipulatingAdapter53(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.send_command = MagicMock(return_value =
                utils.raw_output_syslog_host_removed)

        adapter.remove_syslog_host(host='12.3.4.5')
        assert_equal(adapter.send_command_and_check_output.call_args_list,
                     [call("syslog remotehost delete -host 12.3.4.5", utils.generic_success_regex, timeout=600, suppress=False)])

    def test_remove_syslog_host_and_restart_syslog_deletes_host_successfully_when_host_is_valid_Ip_53(self):
        '''
        Test that host is removed as syslog server, if it is a valid IP
        '''

        adapter = LunaManipulatingAdapter53(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.send_command = MagicMock(return_value =
                utils.raw_output_syslog_host_removed)

        adapter.remove_syslog_host_and_restart_syslog(host='12.3.4.5')
        assert_equal(adapter.send_command_and_check_output.call_args_list,
                     [call("syslog remotehost delete -host 12.3.4.5", utils.generic_success_regex, timeout=600, suppress=False)])

    def test_restart_syslog_successfully_restarts_syslog_53(self):
        '''
        Test to restart syslog. Successfully restart syslog server
        '''

        adapter = LunaManipulatingAdapter53(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.send_command = MagicMock(return_value = utils.raw_output_syslog_service_restarted)

        adapter.restart_syslog()

        assert_equal(adapter.send_command_and_check_output.call_args_list,[call("service restart syslog",utils.expected_syslog_restarted_output,suppress=False,timeout=600)])
