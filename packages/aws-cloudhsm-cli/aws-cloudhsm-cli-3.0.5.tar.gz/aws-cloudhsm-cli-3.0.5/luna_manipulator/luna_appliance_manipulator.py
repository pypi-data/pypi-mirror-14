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

from luna_device_connections.luna_ssh_connection import LunaSshConnection
from luna_device_connections.exceptions import HsmNotInitializedException
from luna_device_connections.luna_outputs import *
from luna_manipulating_adapter import LunaManipulatingAdapter
from luna_manipulating_adapter_53 import LunaManipulatingAdapter53
from luna_manipulating_adapter_54 import LunaManipulatingAdapter54
from luna_reader.luna_state_reader import LunaStateReader
import re
import logging
logger = logging.getLogger('luna_manipulator.luna_appliance_manipulator')

class LunaApplianceManipulator(object):
    software_version_to_adapter = {
        'default': LunaManipulatingAdapter, 
        '5.0': LunaManipulatingAdapter,
        '5.1': LunaManipulatingAdapter, 
        '5.3': LunaManipulatingAdapter53,
        '5.4': LunaManipulatingAdapter54
    }

    def __init__(self, device_address=None, cred_provider=None, connection=None,
            luna_is_initialized=True):
        if not connection:
            if device_address:
                # Given an IP address, attempting an ssh connection
                connection = LunaSshConnection(cred_provider, device_address)
        try:
            connection.connect()
        except HsmNotInitializedException:
            luna_is_initialized = False

        if luna_is_initialized:
            self._set_adapter(connection, device_address)
        else: 
            self.adapter = LunaManipulatingAdapter(connection)
    
    def _set_adapter(self, connection, device_address):
        #Find the real software version
        software_version = LunaStateReader(connection=connection).get_software_version()

        #Set the adapter to match that version or throw an exception if it isn't supported
        split_version_info = software_version.split('.') #Convert from '5.3.0-11' -> ['5', '3', '0-11']
        major_and_minor_version = '{0}.{1}'.format(split_version_info[0], split_version_info[1]) #Convert from ['5', '3', '0-11'] -> '5.3'

        # We want the FixHsmWorkflow to be able to try and provision, deprovision
        # an hsm that is on an unsupported software version so that it can be
        # repersonalized to a supported version. 
        if major_and_minor_version not in self.software_version_to_adapter.keys():
            logger.warn(
                "Hsm at address {0} is on an unsupported software version"
                ": {1}".format(device_address, major_and_minor_version)
            )
        
        self.adapter = self.software_version_to_adapter.get(
            major_and_minor_version, 
            LunaManipulatingAdapter)(connection)

    def regenerate_server_cert(self):
        return self.adapter.regenerate_server_cert()

    def run_hsm_self_test(self):
        return self.adapter.run_hsm_self_test()

    def register_client(self, client_label, hostname):
        return self.adapter.register_client(client_label, hostname)

    def assign_partition_to_client(self, client_label, partition_label):
        return self.adapter.assign_partition_to_client(client_label, partition_label)

    def revoke_partition_from_client(self, client_label, partition_label):
        return self.adapter.revoke_partition_from_client(client_label, partition_label)

    def add_user(self, user):
        return self.adapter.add_user(user)

    def add_snmp_user_with_credentials(self, snmp_user_credentials_dict):
        return self.adapter.add_snmp_user_with_credentials(snmp_user_credentials_dict)

    def set_user_password(self, user, password):
        return self.adapter.set_user_password(user, password)

    def add_user_role(self, user, role):
        return self.adapter.add_user_role(user, role)

    def register_public_key(self, key_label, filename):
        return self.adapter.register_public_key(key_label, filename)

    def enable_key_auth(self):
        return self.adapter.enable_key_auth()

    def cleanup_config_and_logs(self):
        return self.adapter.cleanup_config_and_logs()

    def reboot_appliance(self):
        return self.adapter.reboot_appliance()

    def remove_user(self, user):
        return self.adapter.remove_user(user)

    def remove_client(self, client):
        return self.adapter.remove_client(client)

    def set_hostname(self, hostname):
        return self.adapter.set_hostname(hostname)

    def add_network_interface(self, network_interface, hsm_ip_address, netmask, gateway_ip=''):
        return self.adapter.add_network_interface(network_interface, hsm_ip_address, netmask, gateway_ip)
  
    def delete_network_interface(self, network_interface):
        return self.adapter.delete_network_interface(network_interface)

    def ping(self, ip_address):
        return self.adapter.ping(ip_address)
   
    def add_network_route(self, network_interface, destination_ip, netmask, gateway_ip):
        return self.adapter.add_network_route(network_interface, destination_ip, netmask, gateway_ip)

    def set_initial_password(self, password):
        return self.adapter.set_initial_password(password)
    
    def initialize_hsm(self, label, cloning_domain, password):
        return self.adapter.initialize_hsm(label, cloning_domain, password)

    def hsm_login(self, password):
        return self.adapter.hsm_login(password)

    def create_partition(self, partition_label, partition_password, cloning_domain):
        return self.adapter.create_partition(partition_label, partition_password, cloning_domain)

    def delete_partition(self, partition_label):
        return self.adapter.delete_partition(partition_label)

    def zeroize_hsm(self):
        return self.adapter.zeroize_hsm()

    def add_ntp_host(self, host):
        return self.adapter.add_ntp_host(host)

    def remove_ntp_host(self, host):
        return self.adapter.remove_ntp_host(host)

    def start_ntp(self):
        return self.adapter.start_ntp()

    def set_timezone(self, timezone):
        return self.adapter.set_timezone(timezone)

    def add_syslog_host_and_restart_syslog(self, host):
        return self.adapter.add_syslog_host_and_restart_syslog(host)

    def add_syslog_host(self, host):
        return self.adapter.add_syslog_host(host)

    def remove_syslog_host(self, host):
        return self.adapter.remove_syslog_host(host)

    def restart_syslog(self):
        return self.adapter.restart_syslog()

    def start_syslog(self):
        return self.adapter.start_syslog()

    def restart_snmp(self):
        return self.adapter.restart_snmp()

    def ensure_ntls(self):
        return self.adapter.ensure_ntls()

    def disable_ipcheck(self):
        return self.adapter.disable_ipcheck()

    def add_snmp_host_with_credentials(self, host, snmp_credentials_dict):
        return self.adapter.add_snmp_host_with_credentials(host, snmp_credentials_dict)

    def enable_snmp(self):
        return self.adapter.enable_snmp()

    def patch_hsm(self, patch_file_name, auth_code):
        return self.adapter.patch_hsm(patch_file_name, auth_code)

    def reset_hsm_counters(self):
        return self.adapter.reset_hsm_counters()

    def restart_and_bind_ntls(self):
        return self.adapter.restart_and_bind_ntls()

    def enable_cpu_governor(self):
        return self.adapter.enable_cpu_governor()
