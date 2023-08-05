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
from luna_manipulator.luna_manipulating_adapter import LunaManipulatingAdapter
import luna_device_connections.luna_outputs as utils

class TestLunaManipulatingAdapter(unittest.TestCase):
    def test_luna_term_regex_matches_expected_character_types(self):
        '''
        Test that regex that is supposed to match the expected acceptable Luna term characters actually does so.
        '''
        pattern = re.compile(utils.luna_term_regex)
        acceptable_term = "aB1._-"

        assert(pattern.search(acceptable_term))

    def test_regenerate_server_cert_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that regenerate_server_cert sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output= MagicMock()
        adapter.regenerate_server_cert()

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call('sysconf regenCert -force', utils.generic_success_regex),
                      call('ntls bind eth0 -force', utils.expected_ntls_bind_eth0_output, timeout=60)]
                    )
    
    def test_run_hsm_self_test_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that run_hsm_self_test sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock(return_value=utils.generic_success_regex)
        adapter.run_hsm_self_test()

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call('hsm selfTest', utils.generic_success_regex, timeout=120)]
                    )

    def test_register_client_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that register_client sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.register_client(client_label = "client label", hostname = "hostname")

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [
                      call('client register -client client label -hostname hostname', utils.expected_register_client_output)
                     ]
                    )

    def test_assign_partition_to_client_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that assign_partition_to_client sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.assign_partition_to_client(client_label = "client label", partition_label = "partition label")

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [
                      call('client assignPartition -client client label -partition partition label', utils.expected_assign_partition_to_client_output)
                     ]
                    )

    def test_revoke_partition_from_client_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that revoke_partition_from_client sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.revoke_partition_from_client(client_label = "client label", partition_label = "partition label")

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [
                      call('client revokePartition -client client label -partition partition label', utils.expected_revoke_partition_from_client_output)
                     ]
                    )

    def test_add_usersends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that add_user sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.add_user(user = 'tron')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [
                      call('user add -userName tron', utils.generic_success_output)
                     ]
                    )
    
    def test_start_syslog_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that start_syslog sends the correct commands to the HSM when given normal output
        '''
        adapter = LunaManipulatingAdapter(MagicMock())
        mock_start_service = MagicMock()
        adapter._start_service = mock_start_service
        
        adapter.start_syslog()
        
        mock_start_service.assert_called_once_with(
            'syslog', utils.generic_success_regex
        )
     
    def test_start_ntp_starts_ntp_only_if_it_is_not_running(self):
        '''
        Test that start_ntp starts ntp only if it is not running
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        mock_send_command = MagicMock()
        adapter.send_command_and_check_output = mock_send_command
        mock_send_command.side_effect = [
            utils.ntp_enabled_status, 
            utils.generic_success_regex, 
            utils.generic_success_regex 
        ]
        adapter.start_ntp()
        
        expected_calls = [
            call('service status ntp', utils.generic_success_regex),
            call('service start ntp', utils.generic_success_regex, timeout=60),
            call('sysconf ntp status', utils.generic_success_regex, timeout=60)
        ]
        mock_send_command.assert_has_calls(expected_calls)
        
    def test_start_ntp_enables_ntp_only_if_it_is_disabled(self):
        '''
        Test that start_ntp enables ntp only if it is disabled
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        mock_send_command = MagicMock()
        adapter.send_command_and_check_output = mock_send_command
        mock_send_command.side_effect = [
            utils.generic_success_regex, 
            utils.ntp_disabled_status, 
            utils.generic_success_regex 
        ]
        adapter.start_ntp()
        
        expected_calls = [
            call('service status ntp', utils.generic_success_regex),
            call('sysconf ntp status', utils.generic_success_regex, timeout=60),
            call('sysconf ntp enable', utils.generic_success_regex)
        ]
        mock_send_command.assert_has_calls(expected_calls)
     
    def test_start_ntp_does_nothing_when_ntp_is_enabled_and_running(self):
        '''
        Test that start_ntp does nothing when ntp is enabled and running
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        mock_send_command = MagicMock()
        adapter.send_command_and_check_output = mock_send_command
        mock_send_command.side_effect = [
            utils.ntp_enabled_and_running_status, 
            utils.generic_success_regex 
        ]
        adapter.start_ntp()
        
        expected_calls = [
            call('service status ntp', utils.generic_success_regex),
            call('sysconf ntp status', utils.generic_success_regex, timeout=60),
        ]
        mock_send_command.assert_has_calls(expected_calls)
     
    def test_start_service_starts_service_when_service_is_not_running(self):
        '''
        Test that _start_service starts service when service is not running
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        mock_send_command = MagicMock()
        adapter.send_command_and_check_output = mock_send_command
        mock_send_command.side_effect = [
            'service is not running',
            utils.generic_success_regex
        ]
        adapter._start_service('xyz', utils.generic_success_regex)
        
        expected_calls = [
            call('service status xyz', utils.generic_success_regex),
            call('service start xyz', utils.generic_success_regex, timeout=60),
        ]
        mock_send_command.assert_has_calls(expected_calls)
     
    def test_start_service_does_nothing_when_service_is_running(self):
        '''
        Test that _start_service does nothing when service is running
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        mock_send_command = MagicMock()
        adapter.send_command_and_check_output = mock_send_command
        mock_send_command.side_effect = [
            'service is running', 
        ]
        adapter._start_service('xyz', utils.generic_success_regex)
        
        expected_calls = [
            call('service status xyz', utils.generic_success_regex),
        ]
        mock_send_command.assert_has_calls(expected_calls)
        
    def test_set_timezone_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that set_timezone sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.set_timezone('zone')

        assert_equal(
            [call('sysconf timezone set zone', 
                  utils.generic_success_regex)],
            adapter.send_command_and_check_output.call_args_list,
        )

    def test_set_user_passwordsends_correct_commands(self):
        '''
        Test that set_user_password sends the correct commands to the HSM
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_sequence = MagicMock()
        adapter.set_user_password(user = 'tron', password = 'the master control program is a tool')

        assert_equal(
                     adapter.send_command_sequence.call_args_list,
                     [call([
                            ('user password tron', utils.expected_set_user_password_output),
                            ('the master control program is a tool', utils.expected_set_user_password_confirm_output),
                            ('the master control program is a tool', utils.generic_success_regex)
                           ],
                           suppress = True
                          )
                     ]
                    )

    def test_register_public_keysends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that register_public_key sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.register_public_key(key_label = 'tronkey', filename = 'rsakey.pub')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [
                      call('sysconf ssh publickey add tronkey -f rsakey.pub', utils.expected_register_public_key_output),
                     ]
                    )

    def test_enable_key_authsends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that enable_key_auth sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.enable_key_auth()

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [
                      call('sysconf ssh publickey enable', utils.expected_enable_key_auth_output),
                     ]
                    )

    def test_cleanup_config_and_logssends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that cleanup_config_and_logs sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.cleanup_config_and_logs()

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call('sysconf config clear -force', utils.generic_success_regex),
                      call('syslog cleanup -force', utils.generic_success_regex),
                      call('my file clear -force', utils.generic_success_regex)]
                    )

    def test_reboot_appliancesends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that reboot_appliance sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.reboot_appliance()

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [
                      call('sysconf appliance reboot -force', utils.expected_reboot_output)
                     ]
                    )

    def test_add_user_rolesends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that add_user_role sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.add_user_role(user = 'tron', role = 'mcp')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [
                      call('user role add -role mcp -userName tron', utils.expected_add_user_role_output.format('tron')),
                     ]
                    )

    def test_remove_usersends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that remove_user sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.remove_user(user = 'tron')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [
                      call('user delete -u tron', utils.generic_success_output)
                     ]
                    )

    def test_remove_client_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that remove_client sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_sequence = MagicMock()
        adapter.remove_client(client = 'tron')

        assert_equal(
                     adapter.send_command_sequence.call_args_list,
                     [call([
                            ('client delete -c tron', utils.expected_remove_client_prompt.format('tron')),
                            ('proceed', utils.generic_success_regex)
                           ],
                           suppress = False
                          )
                     ]
                    )

    def test_set_hostname_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that set_hostname sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.set_hostname(hostname = 'tron')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call('network hostname tron', utils.expected_set_hostname_output)]
                    )

    def test_initialize_hsm_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that initialize_hsm sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.initialize_hsm(label='label', cloning_domain='domain', password='password')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call('hsm init -label label -domain domain -password password -f', utils.expected_initialize_hsm_output, suppress=True)]
                    )
    
    def test_set_initial_password_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that set_initial_password sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.set_initial_password('password')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call('password', utils.expected_set_user_password_confirm_output, suppress=True, followup=True),
                      call('password', utils.luna_shell_prompt, suppress=True, followup=True)]
                    )
    
    def test_add_network_interface_sends_correct_commands_when_gateway_ip_is_provided(self):
        '''
        Test that add_network_interface sends the correct commands to HSM when gateway_ip is provided
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.add_network_interface('network_interface', 'hsm_ip_address', 'netmask', 'gateway_ip')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call('network interface -dev network_interface -i hsm_ip_address -n netmask -g gateway_ip -f',
                           utils.generic_success_output)]
                    )
        
    def test_add_network_route_sends_correct_commands(self):
        '''
        Test that add_network_route sends the correct commands to HSM
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.add_network_route('network_interface', 'destination_ip', 'netmask', 'gateway_ip')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call("network route add network destination_ip -dev network_interface -netmask netmask -gateway gateway_ip -f",    
                           utils.generic_success_output)]
                    )


    def test_add_network_interface_sends_correct_commands_when_gateway_ip_is_not_provided(self):
        '''
        Test that add_network_interface sends the correct commands to HSM when gateway_ip is not provided
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.add_network_interface('network_interface', 'hsm_ip_address', 'netmask')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call('network interface -dev network_interface -i hsm_ip_address -n netmask  -f',
                           utils.generic_success_output)]
                    )

    def test_hsm_login_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that hsm_login sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_sequence = MagicMock()
        adapter.hsm_login(password='password')

        assert_equal(
                     adapter.send_command_sequence.call_args,
                     call(
                          [('hsm login', utils.expected_hsm_login_prompt),
                           ('password', utils.expected_hsm_login_output)],
                          suppress=True,
                          custom_exception_type=ValueError,
                          custom_exception_message='Incorrect SO password provided or final login attempt before zeroization. Login manually to clear zeroization counter.'
                         )
                    )

    def test_create_partition_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that create_partition sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.create_partition(partition_label='label', partition_password='password', cloning_domain='domain')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call('partition create -partition label -password password -domain domain -f', utils.generic_success_regex, suppress=True)]
                    )

    def test_delete_partition_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that delete_partition sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.delete_partition(partition_label='label')

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call('partition delete -partition label -f', utils.generic_success_regex, suppress=True)]
                    )

    def test_zeroize_hsm_sends_correct_commands_when_hsm_contains_no_key_material(self):
        '''
        Test that zeroize_hsm sends the correct commands to the HSM when the hsm contains no key material
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_sequence = MagicMock()
        adapter.send_command = MagicMock(side_effect = [utils.raw_hsm_status_unzeroized_3_attempts_remaining, utils.raw_hsm_status_unzeroized_2_attempts_remaining, utils.raw_hsm_status_unzeroized_1_attempt_remaining])
        adapter.zeroize_hsm()

        assert_equal(
                     adapter.send_command_sequence.call_args_list[0],
                     call(
                          [('hsm login -p asdfg123', utils.expected_failed_hsm_login_not_zeroized_output)]
                         )
                    )
        assert_equal(
                     adapter.send_command_sequence.call_args_list[1],
                     call(
                          [('hsm login -p asdfg123', utils.expected_failed_hsm_login_not_zeroized_output)]
                         )
                    )
        assert_equal(
                     adapter.send_command_sequence.call_args_list[2],
                     call(
                          [('hsm login', utils.expected_hsm_login_last_attempt_warning),
                           ('proceed', utils.expected_hsm_login_prompt),
                           ('asdfg123', utils.expected_failed_hsm_login_zeroized_output)]
                         )
                    )

    def test_zeroize_hsm_does_nothing_when_hsm_zeroized(self):
        '''
        Test that zeroize_hsm doesn't manipulate anything when the HSM is fully zeroized
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_sequence = MagicMock()
        adapter.send_command = MagicMock(return_value = utils.raw_hsm_status_zeroized)

        adapter.zeroize_hsm()

        assert_equal(len(adapter.send_command_sequence.call_args_list), 0)

    def test_zeroize_hsm_raises_exception_when_hsm_contains_key_material(self):
        '''
        Test that zeroize_hsm raises an exception when the HSM contains key material
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_sequence = MagicMock()
        adapter.send_command = MagicMock(return_value = utils.raw_hsm_status_unzeroized_with_data)

        self.assertRaises(Exception, adapter.zeroize_hsm, )

    def test_add_ntp_host_adds_host_successfully_when_host_is_valid_Ip(self):
        '''
        Test that host is added as ntp server, if it is a valid IP
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.send_command = MagicMock(return_value =
                utils.raw_output_ntp_host_added)

        adapter.add_ntp_host(host='12.3.4.5')
        assert_equal(adapter.send_command_and_check_output.call_args_list,
                     [call("sysconf ntp addserver 12.3.4.5",utils.expected_ntp_host_added_output, suppress=False)])

    def test_remove_ntp_host_deletes_host_successfully_when_host_is_valid_Ip(self):
        '''
        Test that host is removed as ntp server, if it is a valid IP
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.send_command = MagicMock(return_value =
                utils.raw_output_ntp_host_removed)

        adapter.remove_ntp_host(host='12.3.4.5')
        assert_equal(adapter.send_command_and_check_output.call_args_list,
                     [call("sysconf ntp deleteserver 12.3.4.5", utils.expected_ntp_host_removed_output, suppress=False)])

    def test_add_syslog_host_adds_host_successfully_when_host_is_valid_Ip(self):
        '''
        Test that host is added as remote syslog host, if it is a valid IP
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.send_command = MagicMock(return_value = utils.raw_output_syslog_host_added)

        adapter.add_syslog_host(host='10.2.106.67')
        assert_equal(adapter.send_command_and_check_output.call_args_list,
                     [call("syslog remotehost add 10.2.106.67", utils.expected_syslog_host_added_output, suppress=False)])

    def test_remove_syslog_host_deletes_host_successfully_when_host_is_valid_Ip(self):
        '''
        Test that host is removed as syslog server, if it is a valid IP
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.send_command = MagicMock(return_value =
                utils.raw_output_syslog_host_removed)

        adapter.remove_syslog_host(host='12.3.4.5')
        assert_equal(adapter.send_command_and_check_output.call_args_list,
                     [call("syslog remotehost delete 12.3.4.5", utils.generic_success_regex, suppress=False)])

    def test_remove_syslog_host_and_restart_syslog_deletes_host_successfully_when_host_is_valid_Ip(self):
        '''
        Test that host is removed as syslog server, if it is a valid IP
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.send_command = MagicMock(return_value =
                utils.raw_output_syslog_host_removed)

        adapter.remove_syslog_host_and_restart_syslog(host='12.3.4.5')
        assert_equal(adapter.send_command_and_check_output.call_args_list,
                     [
                         call("syslog remotehost delete 12.3.4.5", utils.generic_success_regex, suppress=False),
                         call("service restart syslog",utils.expected_syslog_restarted_output,suppress=False, timeout=60)
                     ])

    def test_restart_syslog_successfully_restarts_syslog(self):
        '''
        Test to restart syslog. Successfully restart syslog server
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.send_command = MagicMock(return_value = utils.raw_output_syslog_service_restarted)

        adapter.restart_syslog()

        assert_equal(adapter.send_command_and_check_output.call_args_list,[call("service restart syslog",utils.expected_syslog_restarted_output,suppress=False,timeout=60)])

    def test_restart_snmp_successfully_restarts_snmp_service(self):
        '''
        Test to restart snmp. Successfully restart snmp server
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.send_command = MagicMock(return_value = utils.raw_output_snmp_service_restarted)

        adapter.restart_snmp()

        assert_equal(adapter.send_command_and_check_output.call_args_list,[call("service restart snmp",utils.expected_snmp_restarted_output,suppress=False,timeout=60)])

    def test_add_snmp_host_with_credentials(self):
        '''
        Test add_snmp host with appropriate credentials when it adds
        successfully
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.send_command = MagicMock(
                return_value = utils.generic_success_regex)
        fake_snmp_credentials_dict = {
                'authPassword' : 'fakepasswd1',
                'privPassword' : 'fakepasswd2', 
                'secName' : 'fakeUser' }
        command = "sysconf snmp notification add -ipAddress 1.2.3.4 -authPassword fakepasswd1 -privPassword fakepasswd2 -secName fakeUser -notifyType inform"
        
        adapter.add_snmp_host_with_credentials(host="1.2.3.4", snmp_credentials_dict=fake_snmp_credentials_dict)

        assert_equal(adapter.send_command_and_check_output.call_args_list,
                     [call(command, utils.generic_success_regex, suppress=True)])

    def test_enable_snmp_enables_snmp_only_if_it_is_not_running(self):
        '''
        Test that snmp_enable disables and enables snmp
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        mock_send_command = MagicMock()
        adapter.send_command_and_check_output = mock_send_command
        mock_send_command.side_effect = [
            utils.snmp_disabled_status, 
            utils.generic_success_regex, 
            utils.generic_success_regex
        ]
        adapter.enable_snmp()
        
        expected_calls = [
            call('sysconf snmp show', utils.generic_success_regex),
            call('sysconf snmp disable', utils.generic_success_regex),
            call('sysconf snmp enable', utils.generic_success_regex)
        ]
        mock_send_command.assert_has_calls(expected_calls)

    def test_enable_snmp_enables_snmp_does_nothing_if_snmp_is_running(self):
        '''
        Test that snmp_enable does nothing if snmp is running
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        mock_send_command = MagicMock(
            return_value = utils.snmp_enabled_status
        )
        adapter.send_command_and_check_output = mock_send_command
        adapter.enable_snmp()
        
        expected_calls = [
            call('sysconf snmp show', utils.generic_success_regex),
        ]
        mock_send_command.assert_has_calls(expected_calls)
        
    def test_add_snmp_user_with_credentials(self):
        '''
        Test that adds snmp user successfully.
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.send_command = MagicMock(
                return_value = utils.generic_success_regex)

        fake_snmp_user_credentials_dict = {'authPassword' : 'fakepasswd1',
'privPassword' : 'fakepasswd2', 'secName' : 'fakeUser' }
        command = "sysconf snmp user add -secName fakeUser -authPassword fakepasswd1 -privPassword fakepasswd2"

        adapter.add_snmp_user_with_credentials(
snmp_user_credentials_dict=fake_snmp_user_credentials_dict)

        assert_equal(adapter.send_command_and_check_output.call_args_list,
                     [call(command, utils.generic_success_regex, suppress=True)])

    def test_patch_hsm_correctly_patches_hsm(self):
        '''
        Test that patches hsm successfully.
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.send_command = MagicMock(return_value = utils.raw_output_patch_hsm_succeeded)

        command = "package update lunasa_update-5.1.3-1 -authcode xYr5@asdf"

        adapter.patch_hsm(patch_file_name='lunasa_update-5.1.3-1', auth_code='xYr5@asdf')

        assert_equal(adapter.send_command_and_check_output.call_args_list,
                     [call(command, utils.expected_patch_hsm_succeeded_output,suppress=True)])

    def test_reset_hsm_counters_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that reset_hsm_counters sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()
        adapter.reset_hsm_counters()

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [
                         call('hsm information reset', utils.generic_success_output)
                     ]
                    )

    def test_restart_and_bind_ntls_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that restart_and_bind_ntls sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output= MagicMock()
        adapter.restart_and_bind_ntls()

        assert_equal(
                     adapter.send_command_and_check_output.call_args_list,
                     [call('ntls bind eth0 -force', utils.expected_ntls_bind_eth0_output, timeout=60)]
                    )

    def test_ensure_ntls_sends_correct_commands_when_receiving_correct_output(self):
        '''
        Test that ensure_ntls sends the correct commands to the HSM when given normal output
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        mock_start_service = MagicMock()
        adapter._start_service = mock_start_service
        
        adapter.ensure_ntls()
        
        mock_start_service.assert_called_once_with(
            'ntls', utils.expected_ntls_started_output
        )

    def test_disable_ipcheck(self):
        '''
        Test that disable ipcheck issues the correct command.
        '''

        adapter = LunaManipulatingAdapter(Mock())
        adapter.send_command_and_check_output = Mock()

        adapter.disable_ipcheck()

        assert_equal(adapter.send_command_and_check_output.call_args_list,[call("ntls ipcheck disable",utils.expected_ntls_ipcheck_disable_output)])

    def test_enable_cpu_governor(self):
        '''
        Test that enable_cpu_governor does that
        '''

        adapter = LunaManipulatingAdapter(MagicMock())
        adapter.send_command_and_check_output = MagicMock()

        adapter.enable_cpu_governor()
        assert_equal(adapter.send_command_and_check_output.call_args_list,
                     [call("sysconf appliance cpuGovernor enable", utils.generic_success_output, suppress=False)])
