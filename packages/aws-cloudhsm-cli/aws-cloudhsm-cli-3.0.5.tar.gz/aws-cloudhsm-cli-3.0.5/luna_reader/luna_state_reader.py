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

from luna_device_connections.luna_outputs import *
from luna_device_connections.luna_ssh_connection import LunaSshConnection
from luna_reader.luna_reading_adapter import LunaReadingAdapter
from luna_reader.luna_reading_adapter_53 import LunaReadingAdapter53
from luna_reader.luna_reading_adapter_54 import LunaReadingAdapter54
import logging
logger = logging.getLogger('luna_reader.luna_state_reader')

class LunaStateReader(object):
    software_version_to_adapter = {
        'default': LunaReadingAdapter,
        '5.0': LunaReadingAdapter,
        '5.1': LunaReadingAdapter,
        '5.2': LunaReadingAdapter,
        '5.3': LunaReadingAdapter53,
        '5.4': LunaReadingAdapter54
    }

    def __init__(self, device_address=None, cred_provider=None, connection=None):
        if not connection:
            if device_address:
                # Given an IP address, attempting an ssh connection
                connection = LunaSshConnection(cred_provider, device_address)

        connection.connect()
        self._set_adapter(connection, device_address)

    def _set_adapter(self, connection, device_address):
        #Find the real software version
        self.adapter = self.software_version_to_adapter['default'](connection)
        software_version = self.get_software_version()

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
            LunaReadingAdapter
        )(connection)

    def get_everything(self):
        return self.adapter.get_everything()

    def get_hostname(self):
        return self.adapter.get_hostname()

    def get_interface_info(self):
        return self.adapter.get_interface_info()

    def get_syslog_servers(self):
        return self.adapter.get_syslog_servers()

    def get_ntp_servers(self):
        return self.adapter.get_ntp_servers()

    def get_ntp_configuration_and_status(self):
        return self.adapter.get_ntp_configuration_and_status()

    def get_route_table(self):
        return self.adapter.get_route_table()

    def get_serial_number(self):
        return self.adapter.get_serial_number()

    def get_snmp_configuration_and_status(self):
        return self.adapter.get_snmp_configuration_and_status()

    def get_software_version(self):
        return self.adapter.get_software_version()

    def get_syslog_configuration_and_status(self):
        return self.adapter.get_syslog_configuration_and_status()

    def get_users(self):
        return self.adapter.get_users()

    def is_luna_zeroized(self):
        return self.adapter.is_luna_zeroized()

    def is_package_installed(self, package_name):
        return self.adapter.is_package_installed(package_name)

    def has_key_material(self):
        return self.adapter.has_key_material()

    def get_clients(self):
        return self.adapter.get_clients()

    def get_partitions(self):
        return self.adapter.get_partitions()

    def count_partition_objects(self, partition_serial):
        return self.adapter.count_partition_objects(partition_serial)

    def get_client_partitions(self, client_label):
        return self.adapter.get_client_partitions(client_label)

    def get_client_fingerprint(self, client_label):
        return self.adapter.get_client_fingerprint(client_label)

    def get_firmware_version(self):
        return self.adapter.get_firmware_version()

    def get_installed_packages(self):
        return self.adapter.get_installed_packages()
