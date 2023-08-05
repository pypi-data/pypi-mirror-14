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

from collections import namedtuple
from device_connections.device_connection import DeviceConnection
import getpass
from luna_device_connections.exceptions import HsmNotInitializedException
import pexpect
import time
import logging
import os.path
import re
import signal
from sys import exit

logger = logging.getLogger('luna_device_connections.luna_console_connection')

class LunaConsoleProvider(object):
    def __init__(self, console_server_username, console_server_password, hsm_username, hsm_password, ssh_username=None, ssh_password=None):
        for k,v in locals().items():
            setattr(self, k, v)

class LunaConsoleConnection(DeviceConnection):
    def __init__(self, provider, console_bastion, console_server, port, hostKeyChecking=False):
        self.console_server = console_server
        self.console_bastion = console_bastion
        self.hostKeyChecking = hostKeyChecking
        self.port = port
        # this seems the most expedient way to add these things without breaking existing stuff
        DeviceConnection.__init__(self, provider)

    def connect(self):
        '''
        Form the console connection to the Luna device
        '''
        if not self.connection:
            hops = [self._spawn_connection,
                    self._connect_to_console_bastion,
                    self._connect_to_console_server,
                    self._connect_to_luna]
            self._perform_hops(hops, 'lunash', error_on_success_not_met=True)
            logger.info("Connection to the Luna device established")
        else:
            logger.info("Already connected to the Luna device. Skipping connection formation steps.")

    def _prompt(self):
        return r"lunash:>"

    def _build_ssh_args(self):
        '''
        Assemble the arguments to ssh to console bastion
        '''
        ssh_args = ['ssh']
        if not self.hostKeyChecking:
            ssh_args.extend(["-o", "StrictHostKeyChecking=no",
                             "-o", "UserKnownHostsFile=" + os.path.devnull,
                             "-A"])
        ssh_args.append('-t')
        if self.provider.ssh_username is not None:
            ssh_args.append(self.provider.ssh_username + "@" + self.console_bastion)
        else:
            ssh_args.append(self.console_bastion)
        ssh_args.extend(self._build_telnet_args())
        return ssh_args

    def _build_telnet_args(self):
        '''
        Assemble the arguments to telnet to device from console bastion
        '''
        telnet_args = ['telnet']
        try:
            telnet_args.extend([self.console_server, str(self.port)])
        except AttributeError as e:
            message = "Console host or port not provided; host: {0}, port: {1}".format(getattr(self, 'console_server', None), getattr(self, 'port', None))
            logger.error(message)
            raise AttributeError(message + ": " + e.message)

        return telnet_args

    def _connect_to_console_bastion(self, *args, **kwargs):
        ssh_command = ' '.join(self._build_ssh_args())
        ssh_response = self._send_command_and_return_response(ssh_command, end_condition_regex='(Username)|(@.*password)')
        if 'Username' in ssh_response:
            return ssh_response
        
        password_response = self._send_command_and_error_on_unexpected_output(self.provider.ssh_password, 'Username', redact_string=self.provider.ssh_password)
        return password_response

    def _connect_to_console_server(self, *args, **kwargs):
        username_response = self._send_command_and_error_on_unexpected_output(self.provider.console_server_username, "LocalPassword")
        password_response = self._send_command_and_error_on_unexpected_output(self.provider.console_server_password, timeout=2, redact_string=self.provider.console_server_password)
        
        logger.info("Connected to console server")
        return password_response

    def _connect_to_luna(self, *args, **kwargs):
        random_newlines = '\r\n\r\n'
        newlines_response = self._send_command_and_return_response(random_newlines, end_condition_regex='(login)|(Enter new password:)')
        if 'lunash' in newlines_response:
            logger.info("Hopped on open luna session")
            return newlines_response
        if 'Enter new password' in newlines_response:
            logger.info("Hopped on an open unitialized hsm session")
            raise HsmNotInitializedException
        
        try:
            username_response = self._send_command_and_error_on_unexpected_output(self.provider.hsm_username, 'Password')
            password_response = self._send_command_and_error_on_unexpected_output(self.provider.hsm_password, 'lunash', redact_string=self.provider.hsm_password)
            logger.info("Connected to Luna")
            return password_response
        except RuntimeError as e:
            logger.info("Login failed with message: {0}".format(e.message))
            logger.info("Retrying login using initial password")
        
        username_response = self._send_command_and_error_on_unexpected_output('admin', 'Password')
        self._send_command_and_error_on_unexpected_output('PASSWORD', 'Enter new password:', suppress=False)
        logger.info("Hopped on an unitialized hsm")
        raise HsmNotInitializedException

    def disconnect(self):
        '''
        Terminate the ssh connection to the Luna device
        '''
        if self.connection:
            telnet_hops = [self._exit_luna,
                           self._disconnect_from_telnet_session]
            self._perform_hops(telnet_hops)
            self._disconnect_from_ssh_session()
            logger.info("Disconnected from the Luna device")
            self.connection = None
        else:
            logger.info("No connection exists. Skipping disconnection steps.")

    def _exit_luna(self, *args, **kwargs):
        exit_output = self._send_command_and_return_response(
            'exit', end_condition_regex = '(Success)|(Exiting)'
        ) 
        return exit_output

    def _disconnect_from_telnet_session(self, *args, **kwargs):
        telnet_escape = chr(29)
        self.connection.send(telnet_escape)
        escape_output = self._read(end_condition_regex='telnet')
        if not 'telnet' in escape_output:
            raise RuntimeError("Failed to escape to telnet shell. Actual output: " + escape_output)
        logger.info("Escaped to telnet shell")

        quit_output = self._send_command_and_return_response('quit', end_condition_regex = "[$%]")
        
        logger.info("Quit telnet session")
        return quit_output

    def _disconnect_from_ssh_session(self):
        logger.info("Attempting to kill ssh session gracefully")
        self.connection.kill(signal.SIGTERM)
        time.sleep(2)

        if self.connection.isalive():
            logger.info("Graceful disconnection attempt failed, sending SIGKILL...")
            self.connection.kill(signal.SIGKILL)




