from device_connections.base_adapter import BaseAdapter
from mock import call, patch, MagicMock, Mock
from nose.tools import *
import pexpect
from unittest import TestCase

class TestBaseAdapter(TestCase):
    def test_tokenize_string_functions_correctly(self):
        '''
        Test that _tokenize_string() tokenizes strings correctly
        '''
        #Run the test
        adapter = BaseAdapter(Mock())
        output_list = adapter._tokenize_string(input_string)
        
        assert_equal(
                     output_list,
                     input_string_tokenized
                    ) 

    def test_remove_rows_without_correct_number_of_tokens_removes_rows_correctly(self):
        '''
        Test that _remove_rows_without_correct_number_of_tokens() removes rows correctly
        '''
        #Run the test
        input_list = [[1, 2, 3], [], [1, 2]]
        expected_output_list = [[1, 2]]
        adapter = BaseAdapter(Mock())
        actual_output_list = adapter._remove_rows_without_correct_number_of_tokens(input_list, 2)
        
        assert_equal(
                     actual_output_list,
                     expected_output_list
                    )

    def test_command_sequence_passes_arguments_correctly(self):
        '''
        Test that _send_command_sequence calls send_command_and_check_output appropriately
        '''
        adapter = BaseAdapter(Mock())
        adapter.send_command_and_check_output = Mock()
        
        commands_and_responses = [('Command 1', 'Response 1'), ('Command 2', 'Response 2'), ('Command 3', 'Response 3')]
        adapter.send_command_sequence(commands_and_responses)

        assert_equals(adapter.send_command_and_check_output.call_args_list,
                      [call('Command 1', 'Response 1', suppress=False, custom_exception_type=None, timeout=None, custom_exception_message=None),
                       call('Command 2', 'Response 2', followup=True, suppress=False, custom_exception_type=None, timeout=None, custom_exception_message=None),
                       call('Command 3', 'Response 3', followup=True, suppress=False, custom_exception_type=None, timeout=None, custom_exception_message=None)])
 
    def test_send_command_calls_get_to_device_prompt_and_passes_args(self):
        '''
        Test that send_command calls _get_to_device_prompt and passes command/args to connection's _send_command_and_return_response
        '''
        mock_conn = Mock()
        adapter = BaseAdapter(mock_conn)
        adapter._get_to_device_prompt = Mock()

        adapter.send_command('tron is cool', True, 6, 'yes')

        assert_equals(adapter._get_to_device_prompt.call_count, 1)
        assert_equals(mock_conn._send_command_and_return_response.call_args_list,
                      [call('tron is cool', suppress=True, end_condition_regex='yes', timeout=6)])

    def test_send_command_and_check_output_returns_output(self):
        '''
        Test that send_command_and_check_output returns output
        '''
        mock_conn = Mock()
        mock_conn._send_command_and_error_on_unexpected_output.return_value = 'output'
        adapter = BaseAdapter(mock_conn)
        adapter._get_to_device_prompt = Mock()

        output = adapter.send_command_and_check_output('tron is cool', 'yes', True, 6)

        assert_equals(output, 'output')
    
    def test_send_command_and_check_output_handles_non_followup_case(self):
        '''
        Test that send_command_and_check_output calls _get_to_device_prompt and passes args to connection's _send_command_and_error_on_unexpected_output in non-followup case
        '''
        mock_conn = Mock()
        adapter = BaseAdapter(mock_conn)
        adapter._get_to_device_prompt = Mock()

        adapter.send_command_and_check_output('tron is cool', 'yes', True, 6)

        assert_equals(adapter._get_to_device_prompt.call_count, 1)
        assert_equals(mock_conn._send_command_and_error_on_unexpected_output.call_args_list,
                      [call('tron is cool', 'yes', timeout=6, suppress=True)])
    
    def test_send_command_and_check_output_handles_followup_case(self):
        '''
        Test that send_command_and_check_output does not call _get_to_device_prompt but passes args to connection's _send_command_and_error_on_unexpected_output in followup case
        '''
        mock_conn = Mock()
        adapter = BaseAdapter(mock_conn)
        adapter._get_to_device_prompt = Mock()

        adapter.send_command_and_check_output('tron is cool', 'yes', True, 6, followup=True)

        assert_equals(adapter._get_to_device_prompt.call_count, 0)
        assert_equals(mock_conn._send_command_and_error_on_unexpected_output.call_args_list,
                      [call('tron is cool', 'yes', timeout=6, suppress=True)])
    
    def test_send_command_and_check_output_handles_custom_exceptions(self):
        '''
        Test that send_command_and_check_output properly handles custom exception types and messages
        '''
        class CustomException(Exception):
            pass

        mock_conn = Mock()
        mock_conn._send_command_and_error_on_unexpected_output.side_effect = RuntimeError
        adapter = BaseAdapter(mock_conn)
        adapter._get_to_device_prompt = Mock()

        try:
            adapter.send_command_and_check_output('tron is cool', 'yes', True, 6, custom_exception_type=CustomException, custom_exception_message='tron is cool')
        except CustomException as e:
            assert_equal(e.message, 'tron is cool')
        else:
            assert False

    def test_send_command_and_check_output_end_regex_defaults_to_device_prompt(self):
        '''
        Test that send_command_and_check_output defaults the end_condition_regex to the return value of _device_prompt
        '''
        class SubClass(BaseAdapter):
            def _get_to_device_prompt(self):
                pass

            def _device_prompt(self):
                return 'zor'

        mock_conn = Mock()
        adapter = SubClass(mock_conn)
        adapter.send_command_and_check_output('tron')
        
        assert_equals(mock_conn._send_command_and_error_on_unexpected_output.call_args_list,
                      [call('tron', 'zor', timeout=None, suppress=False)])

    @raises(NotImplementedError)
    def test_exception_raised_if_subclass_does_not_implement_get_to_device_prompt(self):
        '''
        Test that an exception is raised if a subclass does not implement _get_to_device_prompt
        '''
        class SubClass(BaseAdapter):
            pass

        adapter = SubClass(Mock())
        adapter.send_command('tron', end_condition_regex='zor')

input_string = """
How do ye of uncouth race dare to demand aught of me, 
        
Elu Thingol, Lord of Beleriand, whose life began by     the waters of 
Cuivienen years uncounted ere the fathers of the stunted people awoke? 
"""

input_string_tokenized = [['How', 'do', 'ye', 'of', 'uncouth', 'race', 'dare', 'to', 'demand', 'aught', 'of', 'me,'], ['Elu', 'Thingol,', 'Lord', 'of',  'Beleriand,', 'whose', 'life', 'began', 'by', 'the', 'waters', 'of'], ['Cuivienen', 'years', 'uncounted', 'ere', 'the', 'fathers', 'of', 'the', 'stunted', 'people', 'awoke?']]  
