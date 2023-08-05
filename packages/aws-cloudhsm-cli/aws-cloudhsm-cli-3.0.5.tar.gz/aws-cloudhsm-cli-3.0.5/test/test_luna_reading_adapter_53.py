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
from luna_reader.luna_reading_adapter_53 import LunaReadingAdapter53
import luna_reading_utils as utils

class TestLunaReadingAdapter53(unittest.TestCase):
    def test_can_get_syslog_info_if_running(self):
        '''
        Test that the 5.3 reading adapter can obtain the Luna's current syslog configuration and status if syslog is running
        '''
        reading_adapter = LunaReadingAdapter53(Mock())
        reading_adapter.send_command = Mock(side_effect = [utils.raw_syslog_status_running, utils.raw_syslog_remote_host_list_53])

        returned_syslog_info = reading_adapter.get_syslog_configuration_and_status()

        assert_equals(
                      returned_syslog_info,
                      utils.parsed_syslog_info_running
                     )

    def test_can_get_syslog_info_if_not_running(self):
        '''
        Test that the 5.3 reading adapter can obtain the Luna's current syslog configuration and status if syslog is not running
        '''
        reading_adapter = LunaReadingAdapter53(Mock())
        reading_adapter.send_command = Mock(side_effect = [utils.raw_syslog_status_not_running, utils.raw_syslog_remote_host_list_53])

        returned_syslog_info = reading_adapter.get_syslog_configuration_and_status()

        assert_equals(
                      returned_syslog_info,
                      utils.parsed_syslog_info_not_running
                     )

    def test_get_syslog_servers(self):
        '''
        Test that get_syslog_servers gets the syslog servers
        '''
        reading_adapter = LunaReadingAdapter53(Mock())
        reading_adapter.send_command = Mock(side_effect = [utils.raw_syslog_remote_host_list_53])

        returned_syslog_info = reading_adapter.get_syslog_servers()

        assert_equals(
                      returned_syslog_info['remote_hosts'],
                      utils.parsed_syslog_info_running['remote_hosts']
                     )

    def test_is_zeroized_works_with_unzeroized_hsm_without_partitions(self):
        '''
        Test that is_zeroized returns false on a 5.3 HSM without partitions (case where user
        has initialized HSM but not generated partitions)
        '''
        reading_adapter = LunaReadingAdapter53(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(return_value = utils.raw_hsm_status_unzeroized_no_partitions_53)

        assert not reading_adapter.is_luna_zeroized()

    def test_is_zeroized_works_with_zeroized_hsm(self):
        '''
        Test that is_zeroized returns true on a 5.3 HSM that is zeroized
        '''
        reading_adapter = LunaReadingAdapter53(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(return_value = utils.raw_hsm_status_zeroized_53)

        assert reading_adapter.is_luna_zeroized()
