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

from exceptions import *
from luna_device_connections.luna_adapter import LunaAdapter
from luna_device_connections.luna_outputs import generic_success_regex
import re
import logging
logger = logging.getLogger('luna_reader.luna_reading_adapter')

class LunaReadingAdapter(LunaAdapter):
    """
    SafeNet changes the behavior of the Lunas based on their software version.  This class is intended to be a generic reading adapter that corresponds to software version 5.1.3-1.  As new versions are added and changes in behavior are found, new child classes that override the methods in this class should be created to handle the software version ideosyncracies.
    """
    def get_everything(self):
        all_info = {}
        all_info['hostname'] = self.get_hostname()
        all_info['interface_info'] = self.get_interface_info()
        all_info['ntp_info'] = self.get_ntp_configuration_and_status()
        all_info['route_table'] = self.get_route_table()
        all_info['zeroized'] = self.is_luna_zeroized()
        all_info['serial_number'] = self.get_serial_number()
        all_info['snmp_info'] = self.get_snmp_configuration_and_status()
        all_info['software_version'] = self.get_software_version()
        all_info['syslog_info'] = self.get_syslog_configuration_and_status()
        all_info['users'] = self.get_users()
        all_info['clients'] = self.get_clients()
        all_info['firmware_version'] = self.get_firmware_version()
        all_info['installed_packages'] = self.get_installed_packages()

        return all_info
    
    def get_hsm_show_output(self):
        '''
        hsm show command fails in two different ways
        1. It will fail with an error saying "Unable to communicate with HSM"
        2. It will just freeze and return incomplete hsm show output
        '''
        try:
            raw_output = self.send_command_and_check_output(
                "hsm show", 
                timeout=30,
                expected_output=generic_success_regex,
            )
            return raw_output
        except RuntimeError as e:
            logger.exception(e.message)
            if re.search("Unable to communicate with HSM", e.message):
                raise HsmCryptoCardUnreachableException(
                    "Unable to communicate with HSM card. Try rebooting the HSM"
                )
            else:
                raise LunaShellCommandFailedException(
                    "Hsm is unresponsive to lunash commands." 
                    "Try power-cycling the hsm."
                )

    def get_hostname(self):
        logger.info("Grabbing the hostname...")

        #Get the tokenized hostname
        raw_output = self.send_command("", end_condition_regex='lunash')
        tokenized_output = self._tokenize_string(raw_output)

        #Parse the tokens to get the hostname.  The expected format of the response is [["[hostname]", "lunash:>"], ...]
        hostname = tokenized_output[0][0][1:-1]

        logger.info("Hostname: {0}".format(hostname))
        return hostname

    def get_interface_info(self):
        '''
        Grab the interface info from the Luna device and return it as a list of dictionaries (1 per interface).
        '''
        interface_info = []
        logger.info("Grabbing the interface info...")

        #Get the tokenized interface info
        raw_output = self.send_command("status interface", end_condition_regex=generic_success_regex)
        tokenized_output = self._tokenize_string(raw_output)

        #The first line of each interface section will contain the string "Link encap:Ethernet".  Parse the tokenized output by scaning for that string then grabbing the required information from known relative positions.
        for current_line_number in range(len(tokenized_output)):
            if "Link encap:Ethernet" in " ".join(tokenized_output[current_line_number]):
                current_interface = {}

                interface_name = tokenized_output[current_line_number][0]
                current_interface['interface'] = interface_name

                mac_address = tokenized_output[current_line_number][4]
                current_interface['mac_address'] = mac_address

                ip_address = tokenized_output[current_line_number + 1][1].split(":")[1]
                current_interface['ip_address'] = ip_address

                broadcast = tokenized_output[current_line_number + 1][2].split(":")[1]
                current_interface['broadcast'] = broadcast

                net_mask = tokenized_output[current_line_number + 1][3].split(":")[1]
                current_interface['net_mask'] = net_mask

                #The status tokens are on the line following either the ip address line or the ipv6 address line (if it exists) which follows the ip address line.  The final status token is immediately followed a token of the format "MTU:<some number>".  Therefore, grab all tokens on that line before the MTU token.
                status_token_line_number = current_line_number + 2
                if "inet6" in " ".join(tokenized_output[status_token_line_number]):
                    status_token_line_number += 1

                status_token_list = []
                for token in tokenized_output[status_token_line_number]:
                    if 'MTU' in token:
                        break
                    else:
                        status_token_list.append(token)

                current_interface['status_tokens'] = status_token_list

                interface_info.append(current_interface)
        logger.info("Interface info: {0}".format(interface_info))
        return interface_info

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
        #The list of remote hosts has one tokens per line, so we can dump all lines with more tokens than that.
        sanitized_output = self._remove_rows_without_correct_number_of_tokens(tokenized_output, 1)
        for line in sanitized_output:
            syslog_info['remote_hosts'].append(line[0])
        logger.debug("Syslog servers: {0}".format(syslog_info['remote_hosts']))
        return syslog_info

    def get_ntp_servers(self):
        '''
        Grab the following ntp information: remote servers
        Getting the actual status on an HSM with a lot of servers takes a ridiculously long time
        and we usually don't care about that part.
        We're returning a list inside a dict so that it matches the output format of get_ntp_configuration_and_status.
        '''
        ntp_info = {'remote_servers': []}
        logger.info("Grabbing NTP config and status...")

        #Get the remote server list
        raw_output = self.send_command("sysconf ntp listservers", end_condition_regex=generic_success_regex)
        tokenized_output = self._tokenize_string(raw_output)
        for line in tokenized_output:
            if line[0] == "server":
                ntp_info['remote_servers'].append(line[1])
        logger.debug("NTP servers: {0}".format(ntp_info))
        return ntp_info

    def get_ntp_configuration_and_status(self):
        '''
        Grab the following ntp information: remote servers, is it running, is it enabled
        '''
        ntp_info = {'remote_servers': [], 'running': True, 'enabled': True}
        logger.info("Grabbing NTP config and status...")

        #Grab the running/enabled status
        raw_output = self.send_command("sysconf ntp status", end_condition_regex=generic_success_regex)
        if "not running" in raw_output:
            ntp_info['running'] = False
        if "disabled" in raw_output:
            ntp_info['enabled'] = False

        #Get the remote server list
        ntp_info['remote_servers'] = self.get_ntp_servers()['remote_servers']
        logger.info("NTP info: {0}".format(ntp_info))
        return ntp_info

    def get_route_table(self):
        '''
        Grab the route table from the Luna device and return it as a list of dictionaries.  If the route table is empty, this function returns an empty list.
        '''
        route_table = []
        logger.info("Grabbing the route table...")

        #Get the tokenized route table info
        raw_output = self.send_command_and_check_output("network route show", generic_success_regex)
        tokenized_output = self._tokenize_string(raw_output)
        
        #The lines in the routing table section will all have 8 tokens.
        sanitized_output = self._remove_rows_without_correct_number_of_tokens(tokenized_output, 8)
        
        #The column headings are in the first row; the rest of the table is the data
        column_labels = sanitized_output[0]
        routes = sanitized_output[1:]

        #Stick the routes in the table to be returned
        for route in routes:
            route_dictionary = {}
            for i in range(0,8):
                route_dictionary.update({column_labels[i]: route[i]})
            route_table.append(route_dictionary)

        logger.info("Route table: {0}".format(route_table))
        return route_table

    def get_serial_number(self):
        '''
        Grab the serial number and return it in a dictionary.
        '''
        serial_number = ""
        logger.info("Grabbing the serial number...")

        raw_output = self.get_hsm_show_output()
        tokenized_output = self._tokenize_string(raw_output)
        for line in tokenized_output:
            if " ".join(line).startswith("Serial #:"):
                serial_number = line[2]

        logger.info("Serial number: {0}".format(serial_number))
        return serial_number

    def get_snmp_configuration_and_status(self):
        '''
        Grab the following snmp information: users, notifications, is it running, is it enabled
        '''
        snmp_info = {'running': True, 'enabled': True, 'notifications': [], 'users': []}
        logger.info("Grabbing SNMP config and status...")

        #Grab the running/enabled status
        raw_output = self.send_command("sysconf snmp show", end_condition_regex=generic_success_regex)
        if "not running" in raw_output:
            snmp_info['running'] = False
        if "disabled" in raw_output:
            snmp_info['enabled'] = False

        #Grab the user list
        raw_output = self.send_command("sysconf snmp user list", end_condition_regex=generic_success_regex)
        tokenized_output = self._tokenize_string(raw_output)
        #The user list section only contains one token per line and starts with "-----------"
        sanitized_output = self._remove_rows_without_correct_number_of_tokens(tokenized_output, 1)
        for user in sanitized_output[1:]:
            snmp_info['users'].append(user[0])

        #Grab the notification list
        raw_output = self.send_command("sysconf snmp notification list", end_condition_regex=generic_success_regex)
        tokenized_output = self._tokenize_string(raw_output)
        #The notification list will be in the format: <ip address>:<port> "<user name>" <auth protocol>  We can therefore filter on token/line.
        sanitized_output = self._remove_rows_without_correct_number_of_tokens(tokenized_output, 3)
        #The first line in the sanitized output will be the line ['SNMP', 'Notification', 'Targets:',]
        notification_list = sanitized_output[1:]
        for notification in notification_list:
            ip_address, port = notification[0].split(":")
            user = notification[1][1:-1]
            snmp_info['notifications'].append({'ip_address': ip_address, 'port': port, 'username': user})

        logger.info("SNMP info: {0}".format(snmp_info))
        return snmp_info

    def get_software_version(self):
        '''
        Grab the software version by searching through the list of installed packages.  SafeNet doesn't always correctly update the listed software version display when running commands like "hsm show".
        '''
        software_version = ""
        logger.info("Grabbing the software version...")

        #Search through all the installed packages.  The software version packages have the format "sa_cmd_processor-<version number>".  Parse accordingly.
        #The 5.1.5 software is different. Its package list contains sa_cmd_processor-5.1.3-1 but no sa_cmd_processor-5.1.5-2.
        raw_output = self.send_command_and_check_output(
            "package list", 
            timeout=30,
            expected_output=generic_success_regex,
            custom_exception_type=FailedToDetermineSoftwareVersionException,
            custom_exception_message='package list command failed'
        )

        if 'release-SA-5.1.5-2' in raw_output:
            software_version = '5.1.5-2'
        else:
            for line in raw_output.splitlines():
                if line.startswith('sa_cmd_processor-'):
                    software_version = line[17:]

        logger.info("Software version: {0}".format(software_version))
        return software_version

    def get_syslog_configuration_and_status(self):
        '''
        Grab the following syslog information: remote hosts, is it running.  For reasons unkown, SafeNet varies the layout of their response to these commands across Luna software versions.
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
        #The list of remote hosts has one tokens per line, so we can dump all lines with more tokens than that.
        sanitized_output = self._remove_rows_without_correct_number_of_tokens(tokenized_output, 1)
        for line in sanitized_output:
            syslog_info['remote_hosts'].append(line[0])

        logger.info("Syslog info: {0}".format(syslog_info))
        return syslog_info

    def get_users(self):
        '''
        Grab the users, their roles, whether they are enabled, and their radii.
        '''
        users = []
        logger.info("Grabbing the users...")

        raw_output = self.send_command("user list", end_condition_regex=generic_success_regex)
        tokenized_output = self._tokenize_string(raw_output)

        #The user table has four columns.
        sanitized_output = self._remove_rows_without_correct_number_of_tokens(tokenized_output, 4)
        #The first two rows are the column headings
        for user in sanitized_output[2:]:
            users.append({'username': user[0], 'roles': user[1], 'status': user[2], 'radius': user[3]})

        return users

    def is_luna_zeroized(self):
        '''
        Returns True if the luna is zeroized and False otherwise.
        '''
        is_zeroized = False
        logger.info("Finding if the Luna is zeroized...")

        #Get the hsm status
        raw_output = self.get_hsm_show_output()

        if "HSM IS ZEROIZED !!!!" in raw_output:
            is_zeroized = True

        return is_zeroized

    def is_package_installed(self, package_name):
        '''
        Determine if a given package is installed on the HSM by searching through the list of installed packages and attempting to find a match with the supplied name.
        '''
        is_installed = False
        logger.info("Determining if a package {0} is installed...".format(package_name))

        #Search through all the installed packages and find if any of their names match the argument.
        raw_output = self.send_command("package list", end_condition_regex=generic_success_regex)
        if package_name in raw_output.splitlines():
            is_installed = True
            logger.info("Package {0} is installed.".format(package_name))
        else:
            logger.info("Package {0} is not installed.".format(package_name))

        return is_installed

    def has_key_material(self):
        '''
        Returns True if the luna contains key material and False otherwise.
        '''
        has_key_material = True
        logger.info("Finding if the Luna contains key material...")

        #Get the hsm status
        raw_output = self.get_hsm_show_output()
        space_regex = 'Space In Use \(Bytes\):\s+0\s+'
        if re.search(space_regex, raw_output):
            has_key_material = False
        return has_key_material

    def get_clients(self):
        '''
        Returns a list of all registered clients
        '''
        registered_clients = []
        logger.info("Grabbing the registered clients...")

        raw_output = self.send_command("client list", end_condition_regex=generic_success_regex)
        tokenized_output = self._tokenize_string(raw_output)

        #If there are no clients, the response will contain the string 'No clients are registered.'  Otherwise, it will contain list of client entries in the format 'registered client <number>: <client name>'.
        if not "No clients are registered." in raw_output:
            for line in tokenized_output:
                first_two_tokens_joined = " ".join(line[:2])
                if first_two_tokens_joined == "registered client":
                    current_client_name = " ".join(line[3:]) #Make sure to grab the full name if it includes spaces
                    registered_clients.append(current_client_name)

        return registered_clients

    def get_partitions(self):
        '''
        Returns an empty list if no partition exists on the HSM. Otherwise, return a list of tuples mapping partition labels to serial numbers.
        '''
        partitions = []
        logger.info("Grabbing the partitions...")

        #If there are no partitions, the response will contain the string 'There are no partitions.'  Otherwise, it will contain an output like the following:
        #                                                     Storage (bytes)
        #                                               ----------------------------
        #Partition    Name                     Objects     Total      Used      Free
        #===========================================================================
        #<serial_1>   <label_1>                    ...       ...       ...       ...
        #<serial_2>   <label_2>                    ...       ...       ...       ...
        #...

        raw_output = self.send_command("partition list", end_condition_regex=generic_success_regex)
        if not "There are no partitions." in raw_output:
            lines = raw_output.splitlines()
            is_partition_info = False
            for line in lines:
                if is_partition_info:
                    if line == "":
                        is_partition_info = False
                    else:
                        partitions.append((line.split()[0], line.split()[1]))
                elif re.match('\s*====', line):
                    is_partition_info = True

        return partitions

    def count_partition_objects(self, parition_serial):
        '''
        Returns the number of objects in the partition.
        '''

        logger.info("Grabbing the partitions...")

        #The expected output of the luna command "partition list" can be found above in the get_partitions() method

        raw_output = self.send_command("partition list", end_condition_regex=generic_success_regex)
        if "There are no partitions." in raw_output:
            return None
        else:
            lines = raw_output.splitlines()
            is_partition_info = False
            for line in lines:
                if is_partition_info:
                    if line == "":
                        is_partition_info = False
                    else:
                        if parition_serial == line.split()[0]:
                            return int(line.split()[2])
                elif re.match('\s*====', line):
                    is_partition_info = True

            return None

    def get_client_partitions(self, client_label):
        '''
        Returns a list of all partitions that are assigned to a client.
        '''
        partitions = []
        logger.info("Grabbing the partitions that are assigned to {0}...".format(client_label))

        #If no partition is assigned to the client, the response will contain an output like the following (5.1):

        #ClientID:     ...
        #Hostname:     ...
        #Partitions:   <none>

        #Otherwise, the output will contain a list of comma-separated, double-quoted partition labels (5.3):

        #ClientID:     ...
        #Hostname:     ...
        #HTL Required: ...
        #OTT Expiry:   ...
        #Partitions:   "<partition_1>", "<partition_2>", ...

        #Note: The outputs of 5.1 and 5.3 differ only in those two lines:
        #HTL Required: ...
        #OTT Expiry:   ...

        #Note: If no client with the given label exists on the HSM, the lunash command will return the following error. In this case, the code below will return an empty list of partitions without issues

        #Error:  'client show' failed. (C000040A : RC_OBJECT_NOT_IN_LIST)
        #Error:  Specified client does not exist.

        raw_output = self.send_command("client show -c {0}".format(client_label), end_condition_regex=generic_success_regex)
        tokenized_output = self._tokenize_string(raw_output)
        for line in tokenized_output:
            if line[0] == 'Partitions:':
                for label in line[1:]:
                    if (label.startswith("\"")):
                        partitions.append(label.split("\"")[1])

        return partitions

    def get_client_fingerprint(self, client_label):
        '''
        Returns the fingerprint of the client certificate.
        '''

        logger.info("Grabbing the certificate fingerprint of {0}...".format(client_label))
        raw_output = self.send_command("client fingerprint -c {0}".format(client_label), end_condition_regex=generic_success_regex)
        tokenized_output = self._tokenize_string(raw_output)
        for line in tokenized_output:
            if line[0] == 'Certificate' and line[1] == 'fingerprint:':
                return line[2]

    def get_firmware_version(self):
        '''
        Returns the firmware version of the HSM appliance
        '''
        firmware_version = ""
        logger.info("Grabbing the HSM appliance firmware version...")

        #Get the hsm status
        raw_output = self.get_hsm_show_output()
        tokenized_output = self._tokenize_string(raw_output)
        for line in tokenized_output:
            if " ".join(line).startswith("Firmware"):
                firmware_version = line[1]

        logger.info("Firmware Version: {0}".format(firmware_version))
        return firmware_version

    def get_label(self):
        '''
        Returns the HSM label
        '''
        logger.info("Grabbing the HSM label")
        label = "";
        raw_output = self.get_hsm_show_output()
        tokenized_output = self._tokenize_string(raw_output)
        for line in tokenized_output:
            if " ".join(line).startswith("HSM Label"):
                label = " ".join(line[2:])

        logger.info("HSM label: {0}".format(label))
        return label

    def get_installed_packages(self):
        '''
        Returns the list of installed packages
        '''
        logger.info("Grabbing the HSM's installed packages")
        installed_packages = [];

        """
        RPM LIST (SYSTEM)
        -------------------
        configurator-5.1.0-25
        lunacm-5.1.0-25
        .
        .
        .
        tzdata-2009k-1.el5
        cracklib-dicts-2.8.9-3.3
        glibc-2.5-42


        RPM LIST (SOFTWARE)
        -------------------
        """

        raw_output = self.send_command("package list", end_condition_regex=generic_success_regex)
        tokenized_output = self._tokenize_string(raw_output)
        tokenized_output.reverse() #Reversing the output allows us to begin popping from the top of the list and work our way down

        #Fast forward until we get to the installed packages
        while not "-------------------" in tokenized_output.pop():
            pass

        #Add all the packages to the returned list and stop when we get to the next section
        current_package = tokenized_output.pop()
        while not "RPM LIST (SOFTWARE)" == " ".join(current_package):
            installed_packages.append(current_package[0])
            current_package = tokenized_output.pop()

        logger.info("HSM installed packages: {0}".format(installed_packages))
        return installed_packages
