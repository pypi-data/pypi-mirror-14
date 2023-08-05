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

from luna_device_connections.luna_outputs import generic_success_regex
from luna_reader.luna_reading_adapter import LunaReadingAdapter
import logging

logger = logging.getLogger('luna_reader.luna_reading_adapter_53')

class LunaReadingAdapter53(LunaReadingAdapter):
    def get_syslog_configuration_and_status(self):
        '''
        Grab the following syslog information: remote hosts, is it running
        '''
        syslog_info = {'remote_hosts': [], 'running': True}
        logger.info("Grabbing Syslog config and status...")

        #Grab the running status
        raw_output = self.send_command("service status syslog", end_condition_regex=generic_success_regex)
        if "not running" in raw_output:
            syslog_info['running'] = False

        #Grab the list of remote hosts.
        raw_output = self.send_command("syslog remotehost list", end_condition_regex=generic_success_regex)
        tokenized_output = self._tokenize_string(raw_output)
        #The list of remote hosts has two tokens per line, so we can dump all lines with more or less tokens than that.
        sanitized_output = self._remove_rows_without_correct_number_of_tokens(tokenized_output, 2)
        #The last entry in that filtered list of lines should be the command prompt (which also has two tokens).  Dump that last line.
        sanitized_output = sanitized_output[:-1]
        #The remaining lines should contain two tokens: "<ip address>:<port>," and "<protocol>".  Grab the IP's.
        for line in sanitized_output:
            split_on_colon = line[0].split(':')
            ip_address = split_on_colon[0]
            syslog_info['remote_hosts'].append(ip_address)

        logger.info("Syslog info: {0}".format(syslog_info))
        return syslog_info

    def is_luna_zeroized(self):
        '''
        Determine if HSm is zeroized
        '''
        if self.get_label() == "no label" and not self.has_key_material():
            return True
        else:
            return False

    def get_syslog_servers(self):
        '''
        Grab the following syslog information: remote servers
        '''
        syslog_info = {}
        syslog_info['remote_hosts'] = []
        logger.info("Grabbing syslog remotehosts...")

        #Get the remote server list
        raw_output = self.send_command("syslog remotehost list", end_condition_regex=generic_success_regex)
        tokenized_output = self._tokenize_string(raw_output)
       #The list of remote hosts has two tokens per line, so we can dump all lines with more or less tokens than that.
        sanitized_output = self._remove_rows_without_correct_number_of_tokens(tokenized_output, 2)
        #The last entry in that filtered list of lines should be the command prompt (which also has two tokens).  Dump that last line.
        sanitized_output = sanitized_output[:-1]
        #The remaining lines should contain two tokens: "<ip address>:<port>," and "<protocol>".  Grab the IP's.
        for line in sanitized_output:
            split_on_colon = line[0].split(':')
            ip_address = split_on_colon[0]
            syslog_info['remote_hosts'].append(ip_address)
        logger.debug("Syslog servers: {0}".format(syslog_info['remote_hosts']))
        return syslog_info
