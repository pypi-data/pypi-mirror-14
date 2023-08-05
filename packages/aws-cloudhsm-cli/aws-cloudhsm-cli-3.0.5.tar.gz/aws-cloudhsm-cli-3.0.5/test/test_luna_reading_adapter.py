# Copyright 2013-2014 Amazon.comInc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache LicenseVersion 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASISWITHOUT WARRANTIES OR CONDITIONS OF ANY KINDeither
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.


import unittest
from nose.tools import *
from mock import call, patch, MagicMock, Mock
from luna_reader.luna_reading_adapter import LunaReadingAdapter
from luna_reader.exceptions import *
import luna_reading_utils as utils

class TestLunaReadingAdapter(unittest.TestCase):
    def test_can_get_everything(self):
        '''
        Test that the reading adapter can obtain all of the Luna's state
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = Mock(
            side_effect = [
                utils.raw_hostname,
                utils.raw_interface_info,
                utils.raw_ntp_status_running,
                utils.raw_ntp_server_list,
                utils.raw_snmp_status_running,
                utils.raw_snmp_user_list,
                utils.raw_snmp_notification_list,
                utils.raw_syslog_status_running,
                utils.raw_syslog_remote_host_list_51,
                utils.raw_user_list,
                utils.raw_client_list_full,
                utils.raw_package_list
            ]
        )
        
        reading_adapter.send_command_and_check_output = Mock(
            side_effect = [
                utils.raw_route_table,
                utils.raw_hsm_status_zeroized,
                utils.raw_hsm_status_zeroized,
                utils.raw_package_list,
                utils.raw_hsm_status_zeroized
            ]
        )
        
        returned_info = reading_adapter.get_everything()
        assert_equals(
            returned_info,
            utils.parsed_info
        )

    @raises(HsmCryptoCardUnreachableException)
    def test_get_hsm_show_output_raises_exception_when_hsm_unreachable(self):
        '''
        Test that the reading adapter throws HsmCryptoCardUnreachableException
        when hsm show command fails with the "Unable to communicate with HSM error"
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        error_message = """
            Error:    Unable to communicate with HSM.
            Please run 'hsm supportInfo' and contact customer support.
            """
        reading_adapter.send_command_and_check_output = MagicMock(
            side_effect = RuntimeError(
                "Did not receive expected output: Success. "
                "Actual output: {}".format(error_message)
            )
        )

        hsm_show_output = reading_adapter.get_hsm_show_output()
        self.fail("HsmCryptoCardUnreachableException was not raised")
    
    @raises(LunaShellCommandFailedException)
    def test_get_hsm_show_output_raises_exception_when_hsm_unreachable(self):
        '''
        Test that the reading adapter throws LunaShellCommandFailedException
        when hsm show command fails
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(
            side_effect = RuntimeError('fail')
        )

        hsm_show_output = reading_adapter.get_hsm_show_output()
        self.fail("LunaShellCommandFailedException was not raised")


    def test_can_get_hostname(self):
        '''
        Test that the reading adapter can obtain the Luna's hostname
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_hostname)

        returned_hostname = reading_adapter.get_hostname()
        assert_equals(
                      returned_hostname,
                      'hsm-2-1-2-6'
                     )

    def test_can_get_interface_info(self):
        '''
        Test that the reading adapter can obtain the Luna's interface information
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_interface_info)

        returned_interface_info = reading_adapter.get_interface_info()

        assert_equals(
                      returned_interface_info,
                      utils.parsed_interface_info
                     )

    def test_can_get_interface_info_even_if_it_has_ipv6(self):
        '''
        Test that the reading adapter can obtain the Luna's interface information even if it includes an ipv6 line
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_interface_info_with_inet6)

        returned_interface_info = reading_adapter.get_interface_info()

        assert_equals(
                      returned_interface_info,
                      utils.parsed_interface_info
                     )

    def test_can_get_ntp_info_if_running(self):
        '''
        Test that the reading adapter can obtain the Luna's current ntp configuration and status if ntp is running
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = Mock(side_effect = [utils.raw_ntp_status_running, utils.raw_ntp_server_list])

        returned_ntp_info = reading_adapter.get_ntp_configuration_and_status()

        assert_equals(
                      returned_ntp_info,
                      utils.parsed_ntp_info_running
                     )

    def test_can_get_ntp_info_if_not_running(self):
        '''
        Test that the reading adapter can obtain the Luna's current ntp configuration and status if ntp is not running
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = Mock(side_effect = [utils.raw_ntp_status_not_running, utils.raw_ntp_server_list])

        returned_ntp_info = reading_adapter.get_ntp_configuration_and_status()

        assert_equals(
                      returned_ntp_info,
                      utils.parsed_ntp_info_not_running
                     )

    def test_can_get_route_table(self):
        '''
        Test that the reading adapter can obtain the Luna's route table
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(return_value = utils.raw_route_table)

        returned_route_table = reading_adapter.get_route_table()
        assert_equals(
                      returned_route_table,
                      utils.parsed_route_table
                     )

    def test_returns_empty_list_if_route_table_empty(self):
        '''
        Test that the reading adapter will return an empty list if the the Luna's route table is empty
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(return_value = utils.empty_route_table)

        returned_route_table = reading_adapter.get_route_table()
        assert_equals(
                      returned_route_table,
                      []
                     )

    def test_will_say_hsm_is_zeroized_if_it_is(self):
        '''
        Test that the reading adapter will say the HSM is zeroized when it is.
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(return_value = utils.raw_hsm_status_zeroized)

        is_zeroized = reading_adapter.is_luna_zeroized()
        assert_equals(
                      is_zeroized,
                      True
                     )

    def test_will_say_hsm_isnt_zeroized_if_it_isnt(self):
        '''
        Test that the reading adapter will say the HSM isn't zeroized when it isn't.
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(return_value = utils.raw_hsm_status_unzeroized)

        is_zeroized = reading_adapter.is_luna_zeroized()
        assert_equals(
                      is_zeroized,
                      False
                     )

    def test_will_say_hsm_does_not_have_key_material_if_it_does_not(self):
        '''
        Test that the reading adapter will say the HSM doesn't have key material when it doesn't.
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(return_value = utils.raw_hsm_status_zeroized)

        has_key_material = reading_adapter.has_key_material()
        assert_equals(
                      has_key_material,
                      False
                     )

    def test_will_say_hsm_has_key_material_if_it_does(self):
        '''
        Test that the reading adapter will say the HSM has key material when it does.
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(return_value = utils.raw_hsm_status_unzeroized)

        has_key_material = reading_adapter.has_key_material()
        assert_equals(
                      has_key_material,
                      True
                     )

    def test_can_get_serial_number(self):
        '''
        Test that the reading adapter can obtain the Luna's serial number
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(return_value = utils.raw_hsm_status_zeroized)

        returned_serial = reading_adapter.get_serial_number()

        assert_equals(
                      returned_serial,
                      '156155'
                     )


    def test_can_get_snmp_info_if_running(self):
        '''
        Test that the reading adapter can obtain the Luna's current snmp configuration and status if snmp is running
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = Mock(side_effect = [utils.raw_snmp_status_running, utils.raw_snmp_user_list, utils.raw_snmp_notification_list])

        returned_snmp_info = reading_adapter.get_snmp_configuration_and_status()

        assert_equals(
                      returned_snmp_info,
                      utils.parsed_snmp_info_running
                     )

    def test_can_get_snmp_info_if_not_running(self):
        '''
        Test that the reading adapter can obtain the Luna's current snmp configuration and status if snmp is not running
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = Mock(side_effect = [utils.raw_snmp_status_not_running, utils.raw_snmp_user_list, utils.raw_snmp_notification_list])

        returned_snmp_info = reading_adapter.get_snmp_configuration_and_status()

        assert_equals(
                      returned_snmp_info,
                      utils.parsed_snmp_info_not_running
                     )

    def test_can_get_software_version(self):
        '''
        Test that the reading adapter can obtain the Luna's software version by looking through the list of installed packages
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(
            return_value = utils.raw_package_list
        )

        returned_version = reading_adapter.get_software_version()

        assert_equals(
            '5.1.3-1',
            returned_version
        )

    def test_can_get_515_software_version(self):
        '''
        Test that the reading adapter can obtain the Luna's software version by looking through the list of installed packages
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(
            return_value = utils.raw_package_list_515
        )

        returned_version = reading_adapter.get_software_version()

        assert_equals(
            '5.1.5-2',
            returned_version
        )

    def test_can_get_syslog_info_if_running(self):
        '''
        Test that the reading adapter can obtain the Luna's current syslog configuration and status if syslog is running
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = Mock(side_effect = [utils.raw_syslog_status_running, utils.raw_syslog_remote_host_list_51])

        returned_syslog_info = reading_adapter.get_syslog_configuration_and_status()

        assert_equals(
                      returned_syslog_info,
                      utils.parsed_syslog_info_running
                     )

    def test_get_syslog_servers(self):
        '''
        Test that get_syslog_servers gets the syslog servers
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = Mock(side_effect = [utils.raw_syslog_remote_host_list_51])

        returned_syslog_info = reading_adapter.get_syslog_servers()

        assert_equals(
                      returned_syslog_info['remote_hosts'],
                      utils.parsed_syslog_info_running['remote_hosts']
                     )

    def test_can_get_syslog_info_if_not_running(self):
        '''
        Test that the reading adapter can obtain the Luna's current syslog configuration and status if syslog is not running
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = Mock(side_effect = [utils.raw_syslog_status_not_running, utils.raw_syslog_remote_host_list_51])

        returned_syslog_info = reading_adapter.get_syslog_configuration_and_status()

        assert_equals(
                      returned_syslog_info,
                      utils.parsed_syslog_info_not_running
                     )

    def test_can_get_users(self):
        '''
        Test that the reading adapter can obtain the Luna's list of users
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_user_list)

        returned_users = reading_adapter.get_users()

        assert_equals(
                      returned_users,
                      utils.parsed_user_list
                     )

    def test_can_get_clients_if_they_exist(self):
        '''
        Test that the reading adapter can obtain the Luna's list of registered clients
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_client_list_full)

        returned_clients = reading_adapter.get_clients()

        assert_equals(
                      returned_clients,
                      utils.parsed_client_list
                     )

    def test_can_get_clients_returns_empty_list_if_no_clients(self):
        '''
        Test that the reading adapter will return an empty list if there are no registered clients
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_client_list_empty)

        returned_clients = reading_adapter.get_clients()

        assert_equals(
                      returned_clients,
                      []
                     )

    def test_can_get_partitions_if_they_exist(self):
        '''
        Test that the reading adapter can obtain the Luna's list of partitions
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_partition_list_full)

        returned_partitions = reading_adapter.get_partitions()

        assert_equals(
                      returned_partitions,
                      utils.parsed_partition_list
                     )

    def test_can_get_partitions_returns_empty_dict_if_no_partitions(self):
        '''
        Test that the reading adapter will return an empty list if there are no partitions
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_partition_list_empty)

        returned_partitions = reading_adapter.get_partitions()

        assert_equals(
                      returned_partitions,
                      []
                     )

    def test_can_count_partition_objects_if_any(self):
        '''
        Test that the reading adapter can return the number of objects in Luna's partitions
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_partition_list_full)

        returned_count = reading_adapter.count_partition_objects('157826011')

        assert_equals(
                      returned_count,
                      2
                     )

    def test_can_count_partition_objects_returns_minus_one_if_the_partition_does_not_exist(self):
        '''
        Test that the reading adapter will return -1 if the given partition does not exist
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_partition_list_full)

        returned_count = reading_adapter.count_partition_objects('157826008')

        assert_equals(
                      returned_count,
                      None
                     )

    def test_can_get_client_partitions_if_they_exist(self):
        '''
        Test that the reading adapter can obtain the list of partitions that are assigned to a client
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_client_partition_list_full)

        returned_partitions = reading_adapter.get_client_partitions('client1')

        assert_equals(
                      returned_partitions,
                      utils.parsed_client_partition_list
                     )

    def test_can_get_client_partitions_returns_empty_list_if_no_partitions(self):
        '''
        Test that the reading adapter will return an empty list if no partition is assigned to the client
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_client_partition_list_empty)

        returned_partitions = reading_adapter.get_client_partitions('client2')

        assert_equals(
                      returned_partitions,
                      []
                     )

    def test_can_get_client_partitions_returns_empty_list_if_no_client(self):
        '''
        Test that the reading adapter will return an empty list if the client doesn't exists
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_client_partition_list_error)

        returned_partitions = reading_adapter.get_client_partitions('client3')

        assert_equals(
                      returned_partitions,
                      []
                     )

    def test_can_get_client_fingerprint_if_the_client_exist(self):
        '''
        Test that the reading adapter can obtain the fingerprint of a client certificate
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_client_fingerprint)

        returned_fingerprint = reading_adapter.get_client_fingerprint('client1')

        assert_equals(
                      returned_fingerprint,
                      utils.parsed_client_fingerprint
                     )

    def test_can_get_client_fingerprint_returns_none_if_no_client(self):
        '''
        Test that the reading adapter will return none if the client doesn't exists
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_client_fingerprint_error)

        returned_fingerprint = reading_adapter.get_client_fingerprint('client2')

        assert_equals(
                      returned_fingerprint,
                      None
                     )

    def test_will_get_firmware_version(self):
        '''
        Test that the reading adapter will get the firmware version correctly.
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(return_value = utils.raw_hsm_status_unzeroized)

        firmware_version = reading_adapter.get_firmware_version()
        assert_equals(
                      firmware_version,
                      "6.10.1"
                     )

    def test_will_get_label(self):
        '''
        Test that the reading adapter will get the label correctly
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command_and_check_output = MagicMock(return_value = utils.raw_hsm_status_zeroized_53)

        label = reading_adapter.get_label()
        assert_equals(
                      label,
                      "no label"
                     )

    def test_can_find_if_package_installed(self):
        '''
        Test that the reading adapter can determine if a given package is installed
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_package_list)

        return_value = reading_adapter.is_package_installed('nash-5.1.19.6-54')

        assert_equals(
                      return_value,
                      True
                     )

    def test_can_find_if_package_not_installed(self):
        '''
        Test that the reading adapter can determine if a given package is not installed
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_package_list)

        return_value = reading_adapter.is_package_installed('nash-5.1.19.7')

        assert_equals(
                      return_value,
                      False
                     )

    def test_can_retrieve_installed_packages(self):
        '''
        Test that the reading adapter can retrieve the list of installed packages
        '''
        reading_adapter = LunaReadingAdapter(Mock())
        reading_adapter.send_command = MagicMock(return_value = utils.raw_package_list)

        return_value = reading_adapter.get_installed_packages()

        assert("sa_cmd_processor-5.1.3-1" in return_value)
        assert("tzdata-2009k-1.el5" in return_value)
        assert("cracklib-dicts-2.8.9-3.3" in return_value)
