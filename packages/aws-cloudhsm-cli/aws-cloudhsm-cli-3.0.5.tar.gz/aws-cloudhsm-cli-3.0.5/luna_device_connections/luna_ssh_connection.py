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


import pexpect
import time
from device_connections.device_connection import DeviceConnection
import logging
import tempfile
import os
import os.path
import signal

logger = logging.getLogger('luna_device_connections.luna_ssh_connection')

class LunaSshConnection(DeviceConnection):
    def __init__(self, provider, host, hostKeyChecking=False):
        self.host = host
        self.hostKeyChecking = hostKeyChecking
        DeviceConnection.__init__(self, provider)

    def connect(self):
        '''
        Form the ssh connection to the Luna device
        '''
        if not self.connection:
            ssh_bin = "ssh"
            ssh_args = self._build_ssh_args()
            logger.info("Connecting to the Luna device with command %s and args %r", ssh_bin, ssh_args)
            self.connection = pexpect.spawn(ssh_bin, ssh_args)
            self._negotiate_password_or_passphrase_and_verify_connection()
            logger.info("Connection to the Luna device established")
        else:
            logger.info("Already connected to the Luna device. Skipping connection formation steps.")

    def _prompt(self):
        return r"lunash:>"

    def _build_ssh_args(self):
        '''
        Assemble the arguments to an ssh command.
        '''
        ssh_args = []
        if not self.hostKeyChecking:
            ssh_args.extend(["-o", "StrictHostKeyChecking=no",
                             "-o", "UserKnownHostsFile=" + os.path.devnull])
        if self.provider:
            if self.provider.key_filename:
                ssh_args.extend(["-i", os.path.expanduser(self.provider.key_filename)])
            if self.provider.password:
                ssh_args.extend(["-o", "NumberOfPasswordPrompts=1"])

            ssh_args.append("{0}@{1}".format(self.provider.username, self.host))
        else:
            ssh_args.append(self.host)

        return ssh_args

    def _negotiate_password_or_passphrase_and_verify_connection(self):
        '''
        Determine if we're being prompted for a password or passphrase or just sitting at the Luna prompt
        '''
        response_index = self.connection.expect(['[pP]assword', '[pP]assphrase', 'lunash:>', 'refused', pexpect.TIMEOUT])

        if response_index == 0:
            # Host we're connecting to wants a password
            if not self.provider:
                self._die_and_raise(RuntimeError, "Luna is requesting a password. This indicates that there is no persistent SSH connection to the HSM. Consult the CloudHSM CLI docs for instructions on how to set up a persistent connection.")
            if not self.provider.password:
                self._die_and_raise(ValueError, "Luna is requesting a password but one was not provided. If you're connecting using an ssh key, it may be improperly installed or configured.")
            self.connection.sendline(self.provider.password)
            second_response_index = self.connection.expect(['lunash:>', pexpect.TIMEOUT, pexpect.EOF])
            if second_response_index != 0:
                self._die_and_raise(RuntimeError, "Password provided is incorrect.")
        elif response_index == 1:
            # The ssh key we're using to connect has a passphrase
            if not self.provider.key_passphrase:
                self._die_and_raise(ValueError, "The ssh key used to connect requires a passphrase but one was not provided.")
            self.connection.sendline(self.provider.key_passphrase)
            second_response_index = self.connection.expect(['lunash:>', pexpect.TIMEOUT, pexpect.EOF])
            if second_response_index != 0:
                self._die_and_raise(RuntimeError, "Passphrase provided is incorrect.")
        elif response_index == 2:
            # We're at the luna prompt
            return
        elif response_index == 3:
            # ssh connection refused
            self._die_and_raise(RuntimeError, "Luna refused connection. sshd may not be up yet or otherwise configured to refuse connections.")
        elif response_index == 4:
            # pexpect timeout
            self._die_and_raise(RuntimeError, "Timed out when trying to talk to Luna. It may not be at the address provided. Communication may also be blocked by security groups.")
        else:
            # Something weird
            self._die_and_raise(RuntimeError, "An unexpected error occurred while trying to connect to the Luna.")
            
    def _die_and_raise(self, exception=Exception, message="Connection failed"):
        self.connection = None
        logger.error("Connection failed; dying and raising exception")
        raise exception(message)

    def disconnect(self):
        '''
        Terminate the ssh connection to the Luna device
        '''
        if self.connection:
            # First try to kill the connection gracefully with a SIGTERM
            logger.info("Attempting to disconnect from the Luna device gracefully...")
            self.connection.kill(signal.SIGTERM)
            time.sleep(2)
            
            # If the connection hangs, we'll send it a SIGKILL
            if self.connection.isalive():
                logger.info("Graceful disconnection attempt failed, sending SIGKILL...")
                self.connection.kill(signal.SIGKILL)
            logger.info("Disconnected from the Luna device")
            self.connection = None
        else:
            logger.info("No connection exists. Skipping disconnection steps.")
