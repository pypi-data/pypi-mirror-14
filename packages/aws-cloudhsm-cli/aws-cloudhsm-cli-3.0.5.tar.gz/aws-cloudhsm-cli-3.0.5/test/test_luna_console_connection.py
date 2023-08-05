from luna_device_connections.luna_console_connection import *
from luna_device_connections.exceptions import HsmNotInitializedException
from mock import Mock, patch, call
from nose.tools import *
import signal
from unittest import TestCase

def _get_test_provider():
    return LunaConsoleProvider('console_server_username',
                               'console_server_password',
                               'hsm_username',
                               'hsm_password',
                               None,
                               'ssh_password')

def _get_test_connection(host_key_checking=False):
    return LunaConsoleConnection(_get_test_provider(),
                                 'console_bastion',
                                 'console_server',
                                 'port',
                                 host_key_checking)

@patch('luna_device_connections.luna_console_connection.time.sleep', Mock())
class TestConnect(TestCase):
    @patch('luna_device_connections.luna_console_connection.os')
    def test_build_ssh_args_builds_correct_args_without_host_key_checking(self, mock_os):
        """
        Test that _build_ssh_args builds the correct args when host_key_checking is false
        """
        mock_os.path.devnull = 'devnull'
        conn = _get_test_connection()
        assert_equal(conn._build_ssh_args(),
                     ['ssh',
                      '-o',
                      'StrictHostKeyChecking=no',
                      '-o',
                      'UserKnownHostsFile=devnull',
                      '-A',
                      '-t',
                      'console_bastion',
                      'telnet',
                      'console_server',
                      'port']
                    )

    @patch('luna_device_connections.luna_console_connection.os')
    def test_build_ssh_args_builds_correct_args_with_host_key_checking(self, mock_os):
        """
        Test that _build_ssh_args builds the correct args when host_key_checking is true
        """
        mock_os.path.devnull = 'devnull'
        conn = _get_test_connection(True)

        assert_equal(conn._build_ssh_args(),
                     ['ssh',
                      '-t',
                      'console_bastion',
                      'telnet',
                      'console_server',
                      'port']
                    )

    def test_build_telnet_args_builds_correct_args(self):
        """
        Test that _build_telnet_args builds the correct args
        """
        conn = _get_test_connection()

        assert_equal(conn._build_telnet_args(),
                     ['telnet',
                      'console_server',
                      'port']
                    )

    @raises(AttributeError)
    def test_build_telnet_args_raises_error_when_host_not_given(self):
        """
        Test that _build_telnet_args raises AttributeError when host not available
        """
        conn = _get_test_connection()
        del conn.console_server

        conn._build_telnet_args()

    @raises(AttributeError)
    def test_build_telnet_args_raises_error_when_port_not_given(self):
        """
        Test that _build_telnet_args raises AttributeError when port not available
        """
        conn = _get_test_connection()
        del conn.port

        conn._build_telnet_args()

    def test_connect_to_console_bastion_returns_when_we_hit_console_server(self):
        conn = _get_test_connection()
        conn.connection = Mock()
        conn._build_ssh_args = Mock(return_value=['ssh', 'stuff'])
        conn._send_command_and_return_response = Mock(return_value='what Username')
        
        assert_equal(conn._connect_to_console_bastion(), 'what Username')
        assert_equal(conn._send_command_and_return_response.call_args_list,
                     [call('ssh stuff', end_condition_regex='(Username)|(@.*password)')]
                    )

    def test_connect_to_console_bastion_negotiates_bastion(self):
        conn = _get_test_connection()
        conn.connection = Mock()
        conn._build_ssh_args = Mock(return_value=['ssh', 'stuff'])
        conn._send_command_and_return_response = Mock(return_value='password')
        conn._send_command_and_error_on_unexpected_output = Mock(return_value='what Username')
        
        assert_equal(conn._connect_to_console_bastion(), 'what Username')
        assert_equal(conn._send_command_and_return_response.call_args_list,
                     [call('ssh stuff', end_condition_regex='(Username)|(@.*password)')]
                    )
        assert_equal(conn._send_command_and_error_on_unexpected_output.call_args_list,
                     [call('ssh_password', 'Username', redact_string='ssh_password')]
                    )

    def test_connect_to_console_server(self):
        """
        Test _connect_to_console_server. This tests implementation more that I'd like, but I haven't thought of
        a better test yet.
        """
        conn = _get_test_connection()
        conn.connection = Mock()
        conn._send_command_and_error_on_unexpected_output = Mock(side_effect=['username output', 'password output'])
        
        assert_equal(conn._connect_to_console_server(), 'password output')
        assert_equal(conn._send_command_and_error_on_unexpected_output.call_args_list,
                     [call('console_server_username', 'LocalPassword'),
                      call('console_server_password', timeout=2, redact_string='console_server_password')]
                    )

    def test_connect_to_luna_when_admin_password_set(self):
        """
        Test _connect_to_luna when admin user and password is set
        """
        conn = _get_test_connection()
        conn._send_command_and_return_response = Mock(return_value='newlines output')
        conn._send_command_and_error_on_unexpected_output = Mock(side_effect=['username output', 'password output'])

        assert_equal(conn._connect_to_luna(), 'password output')
        assert_equal(conn._send_command_and_return_response.call_args_list,
                     [call('\r\n\r\n',
                           end_condition_regex='(login)|(Enter new password:)')])
        assert_equal(conn._send_command_and_error_on_unexpected_output.call_args_list,
                     [call('hsm_username', 'Password'),
                      call('hsm_password', 'lunash', redact_string='hsm_password')]
                    )

    @raises(HsmNotInitializedException)
    def test_connect_to_luna_raises_exception_when_admin_password_not_set(self):
        """
        Test _connect_to_luna when admin user and password is not set.
        """
        conn = _get_test_connection()
        conn._send_command_and_return_response = Mock(return_value='newlines output')
        conn._send_command_and_error_on_unexpected_output = Mock(side_effect=['username output', RuntimeError('Boom!'), 'username output', 'password output'])

        conn._connect_to_luna()

    def test_connect_to_luna_calls_correct_methods_when_admin_password_not_set(self):
        """
        Test _connect_to_luna when admin user and password is not set.
        """
        conn = _get_test_connection()
        conn._send_command_and_return_response = Mock(return_value='newlines output')
        conn._send_command_and_error_on_unexpected_output = Mock(side_effect=['username output', RuntimeError('Boom!'), 'username output', 'password output'])

        try:
            conn._connect_to_luna()
        except HsmNotInitializedException:
            pass

        assert_equal(conn._send_command_and_return_response.call_args_list,
                     [call('\r\n\r\n',
                           end_condition_regex='(login)|(Enter new password:)')])
        assert_equal(conn._send_command_and_error_on_unexpected_output.call_args_list,
                     [call('hsm_username', 'Password'),
                      call('hsm_password', 'lunash', redact_string='hsm_password'),
                      call('admin', 'Password'),
                      call('PASSWORD', 'Enter new password:', suppress=False)]
                    )


    def test_connect_to_luna_stops_if_it_sees_luna_shell_early(self):
        """
        Test that _connect_to_luna returns if it sees lunash after sending newlines
        """
        conn = _get_test_connection()
        conn._send_command_and_return_response = Mock(return_value='[hsm-megazord] lunash:>')
        conn._send_command_and_error_on_unexpected_output = Mock()

        assert_equal(conn._connect_to_luna(), '[hsm-megazord] lunash:>')
        assert_equal(conn._send_command_and_return_response.call_args_list,
                     [call('\r\n\r\n',
                           end_condition_regex='(login)|(Enter new password:)')])
        assert_equal(conn._send_command_and_error_on_unexpected_output.call_count, 0)

    @raises(HsmNotInitializedException)
    def test_connect_to_luna_raises_exception_when_it_sees_enter_new_password_prompt_early(self):
        """
        Test that _connect_to_luna raises HsmNotInitializedException when it sees Enter new password prompt after sending newlines
        """
        conn = _get_test_connection()
        conn._send_command_and_return_response = Mock(return_value='Enter new password:')
        conn._send_command_and_error_on_unexpected_output = Mock()

        conn._connect_to_luna()

    def test_connect_to_luna_stops_if_it_sees_enter_new_password_prompt_early(self):
        """
        Test that _connect_to_luna returns if it sees Enter new password prompt after sending newlines
        """
        conn = _get_test_connection()
        conn._send_command_and_return_response = Mock(return_value='Enter new password:')
        conn._send_command_and_error_on_unexpected_output = Mock()
        try:
            conn._connect_to_luna()
        except HsmNotInitializedException:
            pass

        assert_equal(conn._send_command_and_return_response.call_args_list,
                     [call('\r\n\r\n',
                           end_condition_regex='(login)|(Enter new password:)')])
        assert_equal(conn._send_command_and_error_on_unexpected_output.call_count, 0)

    def test_connect_does_not_perform_hops_if_connection_already_exists(self):
        """
        Test connect does not call _perform_hops if self.connection already exists
        """
        conn = _get_test_connection()
        conn._perform_hops = Mock()
        conn.connection = Mock()

        conn.connect()

        assert_equal(conn._perform_hops.call_count, 0)

    def test_connect_passes_all_connect_methods_to_perform_hops(self):
        """
        Test connect passes all connect methods and 'lunash' to _perform_hops
        """
        conn = _get_test_connection()
        conn._perform_hops = Mock()

        conn.connect()

        assert_equal(conn._perform_hops.call_args_list,
                     [call([conn._spawn_connection,
                            conn._connect_to_console_bastion,
                            conn._connect_to_console_server,
                            conn._connect_to_luna],
                            'lunash',
                            error_on_success_not_met=True)])

@patch('luna_device_connections.luna_console_connection.time.sleep', Mock())
class TestDisconnect(TestCase):
    def test_exit_luna(self):
        """
        Test _exit_luna. This tests implementation more that I'd like, but I haven't thought of
        a better test yet.
        """
        conn = _get_test_connection()
        conn._send_command_and_return_response = Mock(side_effect=['exit output'])

        assert_equal(conn._exit_luna(), 'exit output')
        assert_equal(conn._send_command_and_return_response.call_args_list,
                     [call('exit', end_condition_regex = '(Success)|(Exiting)')])

    def test_disconnect_from_telnet_session_sends_telnet_escape_char(self):
        """
        Test _disconnect_from_telnet_session sends telnet escape character
        """
        conn = _get_test_connection()
        conn._read = Mock(return_value='telnet')
        conn.connection = Mock()
        conn._send_command_and_error_on_unexpected_output = Mock()

        conn._disconnect_from_telnet_session()
        assert_equal(conn.connection.send.call_args_list,
                     [call(chr(29))]
                    )

    @raises(RuntimeError)
    def test_disconnect_from_telnet_session_raises_exception_if_does_not_reach_telnet_shell(self):
        """
        Test _disconnect_from_telnet_session raises an exception if it fails to reach the telnet shell
        """
        conn = _get_test_connection()
        conn._read = Mock(return_value='tron')
        conn.connection = Mock()

        conn._disconnect_from_telnet_session()

    def test_disconnect_from_ssh_session_normal(self):
        """
        Test _disconnect_from_ssh_session normal path
        """
        conn = _get_test_connection()
        conn._read = Mock(return_value='telnet')
        conn.connection = Mock(isalive=Mock(return_value=False))
        conn._send_command_and_error_on_unexpected_output = Mock()

        conn._disconnect_from_ssh_session()

        assert_equal(conn.connection.kill.call_args_list, [call(signal.SIGTERM)])

    def test_disconnect_from_ssh_session_force(self):
        """
        Test _disconnect_from_ssh_session force path
        """
        conn = _get_test_connection()
        conn._read = Mock(return_value='telnet')
        conn.connection = Mock(isalive=Mock(return_value=True))
        conn._send_command_and_error_on_unexpected_output = Mock()

        conn._disconnect_from_ssh_session()

        assert_equal(conn.connection.kill.call_args_list, [call(signal.SIGTERM), call(signal.SIGKILL)])
