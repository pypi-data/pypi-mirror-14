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

from luna_device_connections.luna_adapter import LunaAdapter
from luna_device_connections.luna_outputs import *
import re

class LunaManipulatingAdapter(LunaAdapter):

    def regenerate_server_cert(self):
        self.send_command_and_check_output('sysconf regenCert -force', generic_success_regex)
        self.send_command_and_check_output('ntls bind eth0 -force', expected_ntls_bind_eth0_output, timeout=60)

    def run_hsm_self_test(self):
        self.send_command_and_check_output(
            'hsm selfTest', generic_success_regex, timeout=120
        )

    def register_client(self, client_label, hostname):
        command = "client register -client {0} -hostname {1}".format(client_label, hostname)
        return_value = self.send_command_and_check_output(command, expected_register_client_output)
        return return_value

    def assign_partition_to_client(self, client_label, partition_label):
        command = "client assignPartition -client {0} -partition {1}".format(client_label, partition_label)
        return_value = self.send_command_and_check_output(command, expected_assign_partition_to_client_output)
        return return_value

    def add_network_interface(self, network_interface, hsm_ip_address, netmask, gateway_ip=''):
        if gateway_ip:
            gateway_ip = "-g {0}".format(gateway_ip)
        command = "network interface -dev {0} -i {1} -n {2} {3} -f".format(network_interface, hsm_ip_address, netmask, gateway_ip)
        return_value = self.send_command_and_check_output(command, generic_success_output)
    
    def delete_network_interface(self, network_interface):
        command = "network interface delete -d {0}".format(network_interface)
        return_value = self.send_command_and_check_output(command, generic_success_output)
    
    def ping(self, ip_address):
        command = "network ping {0}".format(ip_address)
        return_value = self.send_command_and_check_output(command, luna_shell_prompt)


    def add_network_route(self, network_interface, destination_ip, netmask, gateway_ip):
        command = "network route add network {0} -dev {1} -netmask {2} -gateway {3} -f".format(destination_ip, network_interface, netmask, gateway_ip)
        return_value = self.send_command_and_check_output(command, generic_success_output) 
    
    def revoke_partition_from_client(self, client_label, partition_label):
        command = "client revokePartition -client {0} -partition {1}".format(client_label, partition_label)
        return_value = self.send_command_and_check_output(command, expected_revoke_partition_from_client_output)
        return return_value

    def add_user(self, user):
        command = "user add -userName {0}".format(user)
        self.send_command_and_check_output(command, generic_success_output)

    def add_snmp_user_with_credentials(self, snmp_user_credentials_dict):
        """
        Adds an snmp user with the specified credentials. The
        snmp_user_credentials_dict contains securityName, Authentication
        Password and Privacy Password.
        """
        command = "sysconf snmp user add -secName {0} -authPassword {1} -privPassword {2}".format(snmp_user_credentials_dict['secName'],  snmp_user_credentials_dict['authPassword'], snmp_user_credentials_dict['privPassword'])
        self.send_command_and_check_output(command, generic_success_regex, suppress=True)

    def set_user_password(self, user, password):
        command = "user password {0}".format(user)
        commands_and_prompts = [(command, expected_set_user_password_output),
                                (password, expected_set_user_password_confirm_output),
                                (password, generic_success_regex)]
        self.send_command_sequence(commands_and_prompts, suppress = True)

    def set_initial_password(self, password):
        self.send_command_and_check_output(password, expected_set_user_password_confirm_output, suppress=True, followup=True)
        self.send_command_and_check_output(password, luna_shell_prompt, suppress=True, followup=True)

    def add_user_role(self, user, role):
        """
        Adds Role to the existing user account on the appliance.
        """
        command = "user role add -role {0} -userName {1}".format(role, user)
        self.send_command_and_check_output(command, expected_add_user_role_output)

    def register_public_key(self, key_label, filename):
        command = "sysconf ssh publickey add {0} -f {1}".format(key_label, filename)
        self.send_command_and_check_output(command, expected_register_public_key_output)

    def enable_key_auth(self):
        command = "sysconf ssh publickey enable"
        self.send_command_and_check_output(command, expected_enable_key_auth_output)

    def cleanup_config_and_logs(self):
        self.send_command_and_check_output('sysconf config clear -force', generic_success_regex)
        self.send_command_and_check_output('syslog cleanup -force', generic_success_regex)
        self.send_command_and_check_output('my file clear -force', generic_success_regex)

    def reboot_appliance(self):
        self.send_command_and_check_output('sysconf appliance reboot -force', expected_reboot_output)

    def remove_user(self, user):
        command = 'user delete -u {0}'.format(user)
        self.send_command_and_check_output(command, generic_success_output)

    def remove_client(self, client):
        command = "client delete -c {0}".format(client)
        commands_and_prompts = [(command, expected_remove_client_prompt),
                                ('proceed', generic_success_regex)]

        self.send_command_sequence(commands_and_prompts, suppress = False)

    def set_hostname(self, hostname):
        command = 'network hostname {0}'.format(hostname)
        self.send_command_and_check_output(command, expected_set_hostname_output)

    def initialize_hsm(self, label, cloning_domain, password):
        command = 'hsm init -label {0} -domain {1} -password {2} -f'.format(label, cloning_domain, password)
        self.send_command_and_check_output(command, expected_initialize_hsm_output, suppress=True)

    def hsm_login(self, password):
        commands_and_prompts = [('hsm login', expected_hsm_login_prompt),
                                (password, expected_hsm_login_output)]
        self.send_command_sequence(commands_and_prompts,
                                   suppress = True,
                                   custom_exception_type=ValueError,
                                   custom_exception_message="Incorrect SO password provided or final login attempt before zeroization. Login manually to clear zeroization counter.")

    def create_partition(self, partition_label, partition_password, cloning_domain):
        command = "partition create -partition {0} -password {1} -domain {2} -f".format(partition_label, partition_password, cloning_domain)
        self.send_command_and_check_output(command, generic_success_regex, suppress=True)

    def delete_partition(self, partition_label):
        command = "partition delete -partition {0} -f".format(partition_label)
        self.send_command_and_check_output(command, generic_success_regex, suppress=True)

    def zeroize_hsm(self):
        raw_output = self.send_command("hsm show", end_condition_regex = 'Command Result')
        if "HSM IS ZEROIZED !!!!" in raw_output:
            # HSM is already zeroized.  Nothing to do.
            return
        space_regex = 'Space In Use \(Bytes\):\s+0\s+'
        if not re.search(space_regex, raw_output):
            # There's still key material on the device.  DO NOT zeroize it.
            # There's currently no reason that we'd need to zeroize an HSM with key material.
            # If such a need arises, we'll remove this check.
            raise Exception("HSM NOT ZEROIZED!")

        # We know this (>7)-long password is invalid because it doesn't meet SafeNet's password guidelines.
        invalid_password = 'asdfg123'
        if "3 before HSM zeroization!" in raw_output:
            commands_and_prompts = [('hsm login -p ' + invalid_password, expected_failed_hsm_login_not_zeroized_output)]
            self.send_command_sequence(commands_and_prompts)
        raw_output = self.send_command("hsm show", end_condition_regex = 'Command Result')
        if "2 before HSM zeroization!" in raw_output:
            commands_and_prompts = [('hsm login -p ' + invalid_password, expected_failed_hsm_login_not_zeroized_output)]
            self.send_command_sequence(commands_and_prompts)
        commands_and_prompts = [('hsm login', expected_hsm_login_last_attempt_warning),
                                ('proceed', expected_hsm_login_prompt),
                                (invalid_password, expected_failed_hsm_login_zeroized_output)]
        self.send_command_sequence(commands_and_prompts)

    def add_ntp_host(self, host):
        """
        Adds a remotehost that serves as the NTP server.
        """
        command = "sysconf ntp addserver {0}".format(host)
        self.send_command_and_check_output(command,expected_ntp_host_added_output, suppress=False)

    def remove_ntp_host(self, host):
        """
        Remove an NTP remotehost
        """
        command = "sysconf ntp deleteserver {0}".format(host)
        self.send_command_and_check_output(command,expected_ntp_host_removed_output, suppress=False)

    def start_ntp(self):
        """
        Enables and starts NTP service on the HSM. Does nothing if NTP is
        already enabled and running
        """
        self._start_service("ntp", generic_success_regex)
        ntp_status = self.send_command_and_check_output(
            'sysconf ntp status',
            generic_success_regex,
            timeout=60
        )
        if 'disabled' in ntp_status:
            self.send_command_and_check_output(
                'sysconf ntp enable', 
                generic_success_regex
            )

    def set_timezone(self, timezone):
        """
        Sets timezone on HSM
        """
        self.send_command_and_check_output(
            "sysconf timezone set {}".format(timezone), 
            generic_success_regex
        )

    def add_syslog_host_and_restart_syslog(self, host):
        """
        Adds a remotehost to which syslogs is to be forwarded to, and restart syslog.
        """
        self.add_syslog_host(host)
        self.restart_syslog()

    def add_syslog_host(self, host):
        """
        Adds a remotehost to which syslogs is to be forwarded to.
        """
        command = "syslog remotehost add {0}".format(host)
        self.send_command_and_check_output(command,expected_syslog_host_added_output, suppress=False)

    def remove_syslog_host(self, host):
        """
        Removes a remotehost to which syslogs are forwarded.
        """
        command = "syslog remotehost delete {0}".format(host)
        self.send_command_and_check_output(command, generic_success_regex, suppress=False)

    def remove_syslog_host_and_restart_syslog(self, host):
        """
        Removes a remotehost to which syslogs are forwarded and restarts syslog.
        If there are a lot of syslog hosts on the hsm, this can take a very long time, as it includes a syslog restart.
        """
        self.remove_syslog_host(host)
        self.restart_syslog()

    def restart_syslog(self):
        """
        Restarts the syslog service on the HSM.
        """
        self._restart_service("syslog", expected_syslog_restarted_output)

    def start_syslog(self):
        """
        Starts syslog service on the HSM. Does nothing if it is already on
        """
        self._start_service("syslog", generic_success_regex)

    def restart_snmp(self):
        """
        Restarts the snmp service on the HSM.
        """
        self._restart_service("snmp", expected_snmp_restarted_output)

    def ensure_ntls(self):
        """
        Starts the ntls service or does nothing if it's already running.
        """
        self._start_service("ntls", expected_ntls_started_output)

    def add_snmp_host_with_credentials(self, host, snmp_credentials_dict):
        """
        Sets up a new snmp remote host with the specified credentials.
        """
        command = "sysconf snmp notification add -ipAddress {0} -authPassword {1} -privPassword {2} -secName {3} -notifyType inform".format(host, snmp_credentials_dict['authPassword'],  snmp_credentials_dict['privPassword'], snmp_credentials_dict['secName'])
        self.send_command_and_check_output(command, generic_success_regex, suppress=True)

    def enable_snmp(self):
        """
        Enables and starts SNMP service on the HSM. Does nothing if SNMP is
        already enabled and running
        """
        snmp_status = self.send_command_and_check_output(
            'sysconf snmp show',
            generic_success_regex
        )
        if 'not running' in snmp_status or 'disabled' in snmp_status:
            #Disable and re-enable snmp
            self.send_command_and_check_output(
                'sysconf snmp disable', 
                generic_success_regex
            )
            self.send_command_and_check_output(
                'sysconf snmp enable', 
                generic_success_regex
            )

    def patch_hsm(self, patch_file_name, auth_code):
        """
        Runs the package update command on the hsm to patch the hsm.
        """
        command = "package update {0} -authcode {1}".format(patch_file_name, auth_code)
        self.send_command_and_check_output(command, expected_patch_hsm_succeeded_output, suppress=True)

    def reset_hsm_counters(self):
        """
        Resets the HSM information counters
        """
        command = "hsm information reset"
        self.send_command_and_check_output(command, generic_success_output)

    def disable_ipcheck(self):
        """
        Disables IP check; this is required for client authentication to work with CloudHSM.
        """
        command = "ntls ipcheck disable"
        self.send_command_and_check_output(command, expected_ntls_ipcheck_disable_output)

    def restart_and_bind_ntls(self):
        self.send_command_and_check_output('ntls bind eth0 -force', expected_ntls_bind_eth0_output, timeout=60)

    def enable_cpu_governor(self):
        """
        Enables the HSM's CPU governor.
        """
        command = "sysconf appliance cpuGovernor enable"
        self.send_command_and_check_output(command, generic_success_output, suppress=False)

    def _restart_service(self, service_name, expected_service_restarted_output, timeout=60):
        command = "service restart {0}".format(service_name)
        self.send_command_and_check_output(command, expected_service_restarted_output, suppress=False, timeout=timeout)

    def _start_service(self, service_name, expected_output, timeout=60):
        '''
        Will start service only if it is not already running
        '''
        service_status_output = self.send_command_and_check_output(
            "service status {}".format(service_name), 
            generic_success_regex,
        )
        if 'not running' in service_status_output:
            command = "service start {0}".format(service_name)
            self.send_command_and_check_output(
                command, expected_output, 
                timeout=timeout
            )
