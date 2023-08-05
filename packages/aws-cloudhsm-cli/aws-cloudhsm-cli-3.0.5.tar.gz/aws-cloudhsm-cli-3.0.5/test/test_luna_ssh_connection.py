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

from unittest import TestCase
import pexpect
from nose.tools import *
from mock import call, patch, MagicMock, Mock
import luna_device_connections.luna_ssh_connection as luna
import time
from device_connections.hsm_credential_provider import HsmCredentialProvider

@patch('luna_device_connections.luna_ssh_connection.LunaSshConnection.__del__', MagicMock())
class TestLunaSshConnection(TestCase):
    @patch('luna_device_connections.luna_ssh_connection.LunaSshConnection._build_ssh_args', Mock(return_value=['test_arg']))
    @patch('luna_device_connections.luna_ssh_connection.LunaSshConnection._negotiate_password_or_passphrase_and_verify_connection', Mock())
    @patch('luna_device_connections.luna_ssh_connection.pexpect.spawn')
    def test_connect_once(self, spawn):
        '''
        Test connecting works, and happens only once.
        '''
        ssh = luna.LunaSshConnection(Mock(), "hostname")
        # Test
        ssh.connect()
        ssh.connect()
        # Verify
        spawn.assert_called_once_with("ssh", ['test_arg'])

    def test_build_ssh_args_case1(self):
        '''
        Test that correct arguments exist for password credentials, no host key checking.
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", password="password"),
                                      "hostname", hostKeyChecking=False)
        actual = ssh._build_ssh_args()
        expected = ["-o", "StrictHostKeyChecking=no",
                    "-o", "UserKnownHostsFile=/dev/null",
                    "-o", "NumberOfPasswordPrompts=1",
                    "manager@hostname"]
        self.assertEquals(actual, expected)

    def test_build_ssh_args_case2(self):
        '''
        Test that correct arguments exist for password credentials, with default host key checking.
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", password="password"),
                                      "hostname", hostKeyChecking=True)
        actual = ssh._build_ssh_args()
        expected = ["-o", "NumberOfPasswordPrompts=1",
                    "manager@hostname"]
        self.assertEquals(actual, expected)

    def test_build_ssh_args_case3(self):
        '''
        Test that correct arguments exist for keyfile credentials, no host key checking.
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", ssh_key_filename="test.pem"),
                                      "hostname", hostKeyChecking=False)
        actual = ssh._build_ssh_args()
        expected = ["-o", "StrictHostKeyChecking=no",
                    "-o", "UserKnownHostsFile=/dev/null",
                    "-i", "test.pem",
                    "manager@hostname"]
        self.assertEquals(actual, expected)

    def test_build_ssh_args_case4(self):
        '''
        Test that correct arguments exist for keyfile credentials, with default host key checking.
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", ssh_key_filename="test.pem"),
                                      "hostname", hostKeyChecking=True)
        actual = ssh._build_ssh_args()
        expected = ["-i", "test.pem",
                    "manager@hostname"]
        self.assertEquals(actual, expected)

    def test_build_ssh_args_case5(self):
        '''
        Test that correct arguments exist no credentials.
        '''
        ssh = luna.LunaSshConnection(None, "hostname")
        actual = ssh._build_ssh_args()
        expected = ["-o", 
                    "StrictHostKeyChecking=no", 
                    "-o",
                    "UserKnownHostsFile=/dev/null",
                    "hostname"]
        self.assertEquals(actual, expected)

    def test_negotiate_password(self):
        '''
        Test that negotiate password does in fact negotiate a password.
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", password="guest"),
                                      "hostname")
        ssh.connection = Mock()
        ssh.connection.expect.return_value = 0
        # Test
        ssh._negotiate_password_or_passphrase_and_verify_connection()
        # Verify
        self.assertEquals(ssh.connection.mock_calls,
                          [call.expect(['[pP]assword', '[pP]assphrase', 'lunash:>', 'refused', pexpect.TIMEOUT]),
                          call.sendline("guest"),
                          call.expect(['lunash:>', pexpect.TIMEOUT, pexpect.EOF])])

    def test_negotiate_passphrase(self):
        '''
        Test that negotiate password/passphrase does in fact negotiate a passphrase.
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", ssh_key_filename="test.pem", ssh_key_passphrase="tron"),
                                      "hostname")
        ssh.connection = Mock()
        ssh.connection.expect.side_effect = [1, 0]
        # Test
        ssh._negotiate_password_or_passphrase_and_verify_connection()
        # Verify
        self.assertEquals(ssh.connection.mock_calls,
                          [call.expect(['[pP]assword', '[pP]assphrase', 'lunash:>', 'refused', pexpect.TIMEOUT]),                                                                                                                                     
                           call.sendline("tron"),
                           call.expect(['lunash:>', pexpect.TIMEOUT, pexpect.EOF])])

    def test_negotiate_password_bypassed(self):
        '''
        Test that negotiate password is bypassed if we go straight to Luna shell.
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", ssh_key_filename="test.pem"),
                                      "hostname")
        ssh.connection = Mock()
        ssh.connection.expect.return_value = 2
        # Test
        ssh._negotiate_password_or_passphrase_and_verify_connection()
        # Verify
        self.assertEquals(ssh.connection.mock_calls,
                          [call.expect(['[pP]assword', '[pP]assphrase', 'lunash:>', 'refused', pexpect.TIMEOUT])])

    @raises(RuntimeError)
    def test_negotiate_password_raises_runtime_error_on_pexpect_timeout(self):
        '''
        Test that negotiate password raises a runtime error if pexpect times out while trying to connect.
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", ssh_key_filename="test.pem"),
                                      "hostname")
        ssh.connection = Mock()
        ssh.connection.expect.return_value = 3
        # Test
        ssh._negotiate_password_or_passphrase_and_verify_connection()
        # Verify
        self.assertEquals(ssh.connection.mock_calls,
                          [call.expect(['[pP]assword', '[pP]assphrase', 'lunash:>', 'refused', pexpect.TIMEOUT])])

    @raises(RuntimeError)
    def test_negotiate_password_raises_runtime_error_on_unexpected_behavior(self):
        '''
        Test that negotiate password raises a runtime error when it sees something unexpected.
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", ssh_key_filename="test.pem"),
                                      "hostname")
        ssh.connection = Mock()
        ssh.connection.expect.return_value = 'tron'
        # Test
        ssh._negotiate_password_or_passphrase_and_verify_connection()
        # Verify
        self.assertEquals(ssh.connection.mock_calls,
                          [call.expect(['[pP]assword', '[pP]assphrase', 'lunash:>', 'refused', pexpect.TIMEOUT])])

    @raises(ValueError)
    def test_negotiate_password_raises_value_error_if_password_requested_but_not_given(self):
        '''
        Test that negotiate password raises a runtime error if prompted for a password when the cred provider does not have one
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", ssh_key_filename="test.pem"),
                                      "hostname")
        ssh.connection = Mock()
        ssh.connection.expect.return_value = 0
        # Test
        ssh._negotiate_password_or_passphrase_and_verify_connection()
        # Verify
        self.assertEquals(ssh.connection.mock_calls,
                          [call.expect(['[pP]assword', '[pP]assphrase', 'lunash:>', 'refused', pexpect.TIMEOUT])])

    @raises(ValueError)
    def test_negotiate_password_raises_value_error_if_passphrase_requested_but_not_given(self):
        '''
        Test that negotiate password raises a runtime error if prompted for a passphrase when the cred provider does not have one
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", ssh_key_filename="test.pem"),
                                      "hostname")
        ssh.connection = Mock()
        ssh.connection.expect.return_value = 1
        # Test
        ssh._negotiate_password_or_passphrase_and_verify_connection()
        # Verify
        self.assertEquals(ssh.connection.mock_calls,
                          [call.expect(['[pP]assword', '[pP]assphrase', 'lunash:>', 'refused', pexpect.TIMEOUT])])

    @raises(RuntimeError)
    def test_negotiate_passphrase_raises_runtime_error_when_wrong_passphrase_given(self):
        '''
        Test that negotiate password/passphrase raises runtime error when wrong passphrase given
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", ssh_key_filename="test.pem", ssh_key_passphrase="tron"),
                                      "hostname")
        ssh.connection = Mock()
        ssh.connection.expect.side_effect = [1, 1]
        # Test
        ssh._negotiate_password_or_passphrase_and_verify_connection()

    @raises(RuntimeError)
    def test_negotiate_password_raises_runtime_error_when_wrong_password_given(self):
        '''
        Test that negotiate password/passphrase raises runtime error when wrong password given
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", password='tron'), 'hostname')
        ssh.connection = Mock()
        ssh.connection.expect.side_effect = [0, 1]
        # Test
        ssh._negotiate_password_or_passphrase_and_verify_connection()

    @raises(RuntimeError)
    def test_negotiate_password_raises_runtime_error_when_fails_to_connect_when_no_creds_given(self):
        '''
        Test that negotiate password/passphrase raises runtime error when failing to connect when no creds given
        '''
        ssh = luna.LunaSshConnection(None, 'hostname')
        ssh.connection = Mock()
        ssh.connection.expect.side_effect = [0, 1]
        # Test
        ssh._negotiate_password_or_passphrase_and_verify_connection()

    @patch('luna_device_connections.luna_ssh_connection.time.sleep', Mock())
    def test_disconnect(self):
        '''
        Test the normal disconnection.
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", ssh_key_filename="test.pem"),
                                      "hostname")
        ssh.connection = mock = Mock(isalive=Mock(return_value=False))
        # Test
        ssh.disconnect()
        ssh.disconnect() # Should do nothing.
        # Verify
        self.assertEquals(mock.mock_calls,
                          [call.kill(15),
                           call.isalive()])

    @patch('luna_device_connections.luna_ssh_connection.time.sleep', Mock())
    def test_disconnect_forced(self):
        '''
        Test a disconnection that doesn't exit cleanly.
        '''
        ssh = luna.LunaSshConnection(HsmCredentialProvider("manager", ssh_key_filename="test.pem"),
                                      "hostname")
        ssh.connection = mock = Mock(isalive=Mock(side_effect=[True, False, False]))
        # Test
        ssh.disconnect()
        ssh.disconnect() # Should do nothing.
        # Verify
        self.assertEquals(mock.mock_calls,
                          [call.kill(15),
                           call.isalive(),
                           call.kill(9)])

                           
