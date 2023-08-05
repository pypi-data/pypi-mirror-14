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

from device_connections.device_connection import DeviceConnection
from mock import call, patch, MagicMock, Mock
from nose.tools import *
import pexpect
from unittest import TestCase

class MockSubclass(DeviceConnection):
    def __init__(self):
        DeviceConnection.__init__(self, Mock())
        self.calls = []

    def connect(self):
        self.connection = True
        self.calls.append("connect")

    def disconnect(self):
        self.connection = False
        self.calls.append("disconnect")

class TestDeviceConnection(TestCase):
    @raises(NotImplementedError)
    def test_non_subclassed_connect(self):
        '''
        Test that connect is abstract.
        '''
        obj = DeviceConnection(Mock())
        obj.connect()

    @raises(NotImplementedError)
    def test_non_subclassed_prompt(self):
        '''
        Test that _prompt is abstract.
        '''
        obj = DeviceConnection(Mock())
        obj._prompt()

    @raises(NotImplementedError)
    def test_non_subclassed_disconnect(self):
        '''
        Test that disconnect is abstract.
        '''
        obj = DeviceConnection(Mock())
        obj.disconnect()

    def test_context_manager(self):
        '''
        Test that the context manager methods work.
        '''
        with MockSubclass() as obj:
            self.assertTrue(obj.connection)
        self.assertEquals(obj.calls, ["connect", "disconnect"])
        self.assertFalse(obj.connection)
                          
    def test_deletion(self):
        '''
        Test that disconnect is invoked by garbage collection.
        '''
        obj = MockSubclass()
        obj.__del__()
        self.assertEquals(obj.calls, ["disconnect"])
        self.assertFalse(obj.connection)

    @raises(ValueError)
    def test_acquire(self):
        '''
        Test that aquiring a connection raises if it happens twice.
        '''
        obj = MockSubclass()
        try:
            obj.acquire()
        except:
            raise AssertionError("Shouldn't get an exception here.")
        obj.acquire()

    @raises(ValueError)
    def test_release(self):
        '''
        Test that releasing a connection raises if it happens twice.
        '''
        obj = MockSubclass()
        try:
            obj.acquire()
            obj.release()
        except:
            raise AssertionError("Shouldn't get an exception here.")
        obj.release()

class TestBaseRead(TestCase):
    @raises(RuntimeError)
    def test_read_raises_exception_if_connection_not_set(self):
        """
        Test that _read raises a RuntimeError if self.connection is not set
        """
        conn = DeviceConnection(Mock())
        conn._read()

    def test_read_collects_output_until_eof(self):
        """
        Test that _read uses read_nonblocking to collect output from connection until EOF
        """
        conn = DeviceConnection(Mock())
        conn.connection = Mock()
        conn._prompt = lambda: "stuff"
        conn.connection.read_nonblocking = Mock(side_effect=['tron is a ', 'cool guy', pexpect.EOF(Mock())])

        assert_equal(conn._read(), 'tron is a cool guy')

    def test_read_collects_output_until_timeout(self):
        """
        Test that _read uses read_nonblocking to collect output from connection until timeout
        """
        conn = DeviceConnection(Mock())
        conn.connection = Mock()
        conn._prompt = lambda: "stuff"
        conn.connection.read_nonblocking = Mock(side_effect=['tron is a ', 'cool guy', pexpect.TIMEOUT(Mock())])

        assert_equal(conn._read(), 'tron is a cool guy')
    
    def test_read_timeout_set_by_argument(self):
        """
        Test that _read passes timeout to read_nonblocking
        """
        conn = DeviceConnection(Mock())
        conn.connection = Mock()
        conn._prompt = lambda: "stuff"
        conn.connection.read_nonblocking = Mock(side_effect=[pexpect.EOF(Mock())])

        conn._read(42)

        assert_equal(conn.connection.read_nonblocking.call_args_list, [call(timeout=42, size=1024)])
    
    def test_read_stops_if_end_condition_regex_appears(self):
        """
        Test that _read stops reading and returns output if end_condition_regex appears in output
        """
        conn = DeviceConnection(Mock())
        conn.connection = Mock()
        conn._prompt = lambda: "stuff"
        conn.connection.read_nonblocking = Mock(side_effect=['tron is a ', 'cool guy', ' I guess', pexpect.EOF(Mock())])

        assert_equal(conn._read(end_condition_regex='guy'), 'tron is a cool guy')

    # See TODO in code.
    #def test_read_stops_if_prompt_appears(self):
    #    """
    #    Test that _read stops reading and returns output if self._prompt() appears in output
    #    """
    #    conn = DeviceConnection(Mock())
    #    conn.connection = Mock()
    #    conn._prompt = lambda: "stuff"
    #    conn.connection.read_nonblocking = Mock(side_effect=['tron is a ', 'cool guy', ' stuff', "lol", pexpect.EOF(Mock())])

    #    assert_equal(conn._read(), 'tron is a cool guy stuff')

class TestSendCommandFunctions(TestCase):
    @raises(RuntimeError)
    def test_send_command_and_return_response_raises_runtime_error_if_connection_not_set(self):
        """
        Test that _send_command_and_return_reponse raises a RuntimeError if self.connection is not set
        """
        conn = DeviceConnection(Mock())
        conn._send_command_and_return_response('command')

    def test_send_command_and_return_response_uses_connection_sendline_to_send_command(self):
        """
        Test that _send_command_and_return_reponse sends the provided command with connection.sendline
        """
        conn = DeviceConnection(Mock())
        conn.connection = Mock()
        conn._read = Mock()
        conn._send_command_and_return_response('command')

        assert_equal(conn.connection.sendline.call_args_list, [call('command')])

    def test_send_command_and_return_response_passes_timeout_and_end_condition_regex_to_read(self):
        """
        Test that _send_command_and_return_reponse passes timeout and end_condition_regex to _read
        """
        conn = DeviceConnection(Mock())
        conn.connection = Mock()
        conn._read = Mock()
        conn._send_command_and_return_response('command', timeout=42, end_condition_regex='tron')

        assert_equal(conn._read.call_args_list, [call(timeout=42, end_condition_regex='tron')])
    
    @raises(RuntimeError)
    def test_send_command_and_error_on_unexpected_output_raises_runtime_error_if_expected_output_regex_not_in_output(self):
        """
        Test that _send_command_and_error_on_unexpected_output raises RuntimeError if expected_output_regex not in output
        """
        conn = DeviceConnection(Mock())
        conn._send_command_and_return_response = Mock(return_value='tron')
        conn._send_command_and_error_on_unexpected_output('command', 'megazord')

    def test_send_command_and_error_on_unexpected_output_returns_output_from_send_command_and_return_response(self):
        """
        Test that _send_command_and_error_on_unexpected_output returns output from _send_command_and_return_response
        """
        conn = DeviceConnection(Mock())
        conn._send_command_and_return_response = Mock(return_value='tron')
        
        assert_equal(conn._send_command_and_error_on_unexpected_output('command', 'tron'), 'tron')

class TestPerformHops(TestCase):
    def test_perform_hops_executes_all_hops_if_no_success_condition(self):
        """
        Test that _perform_hops executes all given hops is no success condition provided
        """
        conn = DeviceConnection(Mock())
        hops = [Mock(), Mock(), Mock()]

        conn._perform_hops(hops)

        assert_list_equal([1, 1, 1], map(lambda x: x.call_count, hops))

    def test_perform_hops_stops_when_success_condition_reached(self):
        """
        Test that _perform_hops stops executing hops when success condition_reached
        """
        conn = DeviceConnection(Mock())
        hops = [Mock(return_value='test'), Mock(return_value='tron'), Mock()]

        conn._perform_hops(hops, 'tron')

        assert_list_equal([1, 1, 0], map(lambda x: x.call_count, hops))

    def test_perform_hops_passes_output_from_hop_to_hop(self):
        """
        Test that _perform_hops passes previous_output to first hop and passes output from hop to hop
        """
        conn = DeviceConnection(Mock())
        hops = [Mock(return_value='of'), Mock(return_value='the'), Mock(return_value='Spirit')]

        assert_equal(conn._perform_hops(hops, previous_output='Marrow'), 'Spirit')
        assert_list_equal([call('Marrow'), call('of'), call('the')], map(lambda x: x.call_args, hops))

    @raises(RuntimeError)
    def test_perform_hops_errors_if_success_not_met_and_flag_set(self):
        """
        Test that _perform_hops raises RuntimeError if success not met and error_if_success_not_reached
        is True
        """
        conn = DeviceConnection(Mock())
        hops = [Mock(return_value='of'), Mock(return_value='the'), Mock(return_value='Spirit')]

        conn._perform_hops(hops, 'Mantle', 'Marrow', True)

class TestSpawnConnection(TestCase):
    @patch('device_connections.device_connection.pexpect.spawn')
    def test_spawn_connection(self, mock_spawn):
        """
        Test that _spawn_connection calls pexpect.spawn and returns the output of _read
        """
        conn = DeviceConnection(Mock())
        conn._read = Mock(return_value="tron")

        assert_equal(conn._spawn_connection(), "tron")
        assert_equal(mock_spawn.call_args_list, [call('bash')])

