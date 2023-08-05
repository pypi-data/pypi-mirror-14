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

from luna_manipulating_adapter import LunaManipulatingAdapter
from luna_device_connections.luna_outputs import *
import re

class LunaManipulatingAdapter53(LunaManipulatingAdapter):

    def add_syslog_host_and_restart_syslog(self, host):
        """
        Adds a remotehost to which syslogs is to be forwarded to, and restart syslog.
        """
        # 5.3 HSMs automatically restart syslog when a new remotehost is added
        self.add_syslog_host(host)

    def add_syslog_host(self, host):
        """
        Adds a remotehost to which syslogs is to be forwarded to.
        """
        command = "syslog remotehost add -host {0}".format(host)
        # 5.3 HSMs automatically restart syslog when a new remotehost is added, and the output reflects that
        self.send_command_and_check_output(command,expected_syslog_host_added_output, suppress=False, timeout=600)

    def remove_syslog_host(self, host):
        """
        Removes a remotehost to which syslogs are forwarded.
        If there are a lot of syslog hosts on the hsm, this can take a very long time, as it includes a syslog restart.
        """
        command = "syslog remotehost delete -host {0}".format(host)
        self.send_command_and_check_output(command, generic_success_regex, timeout=600, suppress=False)

    def restart_syslog(self):
        """
        Restarts the syslog service on the HSM.
        """
        self._restart_service("syslog", expected_syslog_restarted_output, timeout=600)

    def remove_syslog_host_and_restart_syslog(self, host):
        """
        Removes a remotehost to which syslogs are forwarded and restarts syslog.
        If there are a lot of syslog hosts on the hsm, this can take a very long time, as it includes a syslog restart.
        """
        self.remove_syslog_host(host)
