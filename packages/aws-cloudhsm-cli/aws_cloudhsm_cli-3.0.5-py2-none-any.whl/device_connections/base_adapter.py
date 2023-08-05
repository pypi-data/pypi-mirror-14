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

import logging

logger = logging.getLogger('device_connections.base_adapter')

class BaseAdapter(object):
    def __init__(self, connection):
        self.connection = connection

    def _remove_rows_without_correct_number_of_tokens(self, list_of_lists, desired_number_of_tokens):
        """
        This function will take a list of lists, discard any rows that have a number items not equal to the parameter passed in, and return the result.
        """
        filtered_list = []
        for row in list_of_lists:
            if len(row) == desired_number_of_tokens:
                filtered_list.append(row)
    
        return filtered_list
    
    def _tokenize_string(self, input_string):
        '''
        Split the input string up by lines and spaces.  Remove any empty lines from the resulting list.  The result is a list of lists of all the tokens in the input, in       their original order.
        '''
        return_value = []
        input_split_by_lines = input_string.splitlines()
        for line in input_split_by_lines:
            line_split_by_spaces = line.split()
    
            #If the line isn't empty, add it to the return value
            if line_split_by_spaces:
                return_value.append(line_split_by_spaces)
    
        return return_value

    def _get_to_device_prompt(self):
        raise NotImplementedError

    def send_command(self, command, suppress=False, timeout=None, end_condition_regex=None):
        '''
        Ensures that the connection is ready to receive the new command and then sends it to the cisco device.
        '''
        self._get_to_device_prompt()

        return self.connection._send_command_and_return_response(command, suppress=suppress, timeout=timeout,end_condition_regex=end_condition_regex)

    def send_command_and_check_output(self, command, expected_output=None, suppress=False, timeout=None, custom_exception_type=None,custom_exception_message=None, followup=False):
        if not expected_output:
            expected_output = self._device_prompt()

        if not followup:
            self._get_to_device_prompt()

        try:
            response = self.connection._send_command_and_error_on_unexpected_output(command, expected_output, timeout=timeout, suppress=suppress)
        except RuntimeError as e:
            if custom_exception_message:
                message = custom_exception_message
            else:
                message = e.message

            if custom_exception_type:
                exception_type = custom_exception_type
            else:
                exception_type = RuntimeError

            raise exception_type(message)
    
        return response

    def send_command_sequence(self, commands_and_responses, suppress=False, custom_exception_type=None,           custom_exception_message=None, timeout=None):
        logger.debug('send_command_sequence: sending first command')

        first_command, first_response = commands_and_responses[0]
        self.send_command_and_check_output(first_command, first_response, suppress=suppress, timeout=timeout, custom_exception_type=custom_exception_type, custom_exception_message=custom_exception_message)

        output = None
        for command, response in commands_and_responses[1:]:
            logger.debug('send_command_sequence: sending followup command')
            output = self.send_command_and_check_output(command, response, suppress=suppress, timeout=timeout, custom_exception_type=custom_exception_type, custom_exception_message=custom_exception_message, followup=True)

        return output
