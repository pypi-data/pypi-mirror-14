# Copyright 2013-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# is located at
# 
#     http://aws.amazon.com/apache2.0/
# 
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS,  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

import logging
import pexpect
import re

logger = logging.getLogger('device_connections.device_connection')

class DeviceConnection(object):
    """
    A generic connection handler
    """
    
    def __init__(self, provider):
        self.provider = provider
        self.connection = None
        self.is_in_use = False
        
    def __del__(self):
        ''' 
        Make sure we clean up the external connection on object deletion
        '''
        self.disconnect()
        
    def __enter__(self):
        self.connect()
        return self
        
    def __exit__(self, exception_type, exception_value, traceback):
        self.disconnect()

    def acquire(self):
        ''' 
        This prevents multiple users from using the same connection at the same time.
        '''
        if self.is_in_use:
            raise ValueError("The connection is already in use.  You cannot hand it out until the other session releases it.")
        self.is_in_use = True
        
    def connect(self):
        ''' 
        This method should be overridden by a subclass with specific connection semantics.
        '''
        raise NotImplementedError("Must be overridden.")
    
    def disconnect(self):
        ''' 
        This method should be overridden by a subclass with specific disconnection semantics.
        '''
        raise NotImplementedError("Must be overridden.")

    def _prompt(self):
        '''
        This method should be overridden by a subclass to return the prompt for whatever device the subclass is connecting
        to. This is used by _read to stop waiting for the proper output from a device when the shell prompt has already
        been returned.
        '''
        raise NotImplementedError("Must be overridden.")

    def release(self):
        if not self.is_in_use:
            raise ValueError("You tried to release a connection that wasn't in use.  Something went wrong")
        self.is_in_use = False
    
    def _clean_up_white_space(self, string_to_clean_up):
        """
        Replace any whitespace with single spaces and clean up leading/trailing whitespaces.  This function allows the device to do weird things with its returned whitespace without us having to worry about it.  It also allows us to format our regex patterns in a manner that is easy to read and makes it easier to see differences between the expected and actual values when matching.
        """
        return re.sub(r"\s+", " ", string_to_clean_up.strip()) 

    def _read(self, timeout=None, end_condition_regex=None):
        """
        Retrieve output from self.connection
        """
        timeout = timeout if timeout else 120
        # 2015-11-01: Commenting this out because it has broken preprovisioning. The issue: We often send newlines
        # before our commands because we want to "flush" the tty. This causes a prompt to show up in the output before we've
        # even sent our command. As a result, our stuff is terminating reading early and not seeing the end_condition_regex 
        # in cases when it does appear. I generally dislike TODOs, but I'm doing one here so we can get unstuck and come up
        # with the proper solution later.
        #end_condition_regex = end_condition_regex + "|" + self._prompt() if end_condition_regex else self._prompt()

        logger.debug("_read: timeout: {0} end_condition_regex: {1}".format(timeout, end_condition_regex))
        if not self.connection:
            raise RuntimeError("Cannot read from None connection")
        buff = ""
        while True:
            try:
                # Read 1024 at a time. This number was chosen arbitrarily.
                buff = buff + self.connection.read_nonblocking(size=1024, timeout=timeout)
                if end_condition_regex:
                    # If end_condition_regex is provided, this may let us end before the timeout.
                    sanitized_regex = self._clean_up_white_space(end_condition_regex)
                    sanitized_buff = self._clean_up_white_space(buff)
                    if re.search(sanitized_regex, sanitized_buff):
                        return buff
            except pexpect.EOF:
                # Got an End-Of-File.
                return buff
            except pexpect.TIMEOUT:
                # There is no more input but we haven't hit the EOF. This occurs when the shell is waiting for more input.
                return buff 
    
    def _send_command_and_return_response(self, command, suppress=False, timeout=None, end_condition_regex=None, redact_string=None):
        """
        Private base send method.  Setting suppress to True prevents the method from printing the actual commands and responses being sent from/to the device.
        """
        if not self.connection:
            raise RuntimeError("Cannot send command to None connection")

        redacted_command = command.replace(redact_string, 'REDACTED') if redact_string else command
        if suppress:
            logger.debug('Sending command (logging suppressed)')
        else:
            logger.debug('Sending command {0}'.format(redacted_command))
        
        self.connection.sendline(command)
        response = self._read(timeout=timeout, end_condition_regex=end_condition_regex)

        redacted_response = response.replace(redact_string, 'REDACTED') if redact_string else response
        if suppress:
            logger.debug('Received output (logging suppressed)')
        else:
            logger.debug('Received output {0}'.format(redacted_response))

        return response

    def _send_command_and_error_on_unexpected_output(self, command, expected_output_regex=None, timeout=None, suppress=False, redact_string=None):
        response = self._send_command_and_return_response(command, end_condition_regex=expected_output_regex, timeout=timeout, suppress=suppress, redact_string=redact_string)
        redacted_response = response.replace(redact_string, 'REDACTED') if redact_string else response
        if expected_output_regex:
            sanitized_regex = self._clean_up_white_space(expected_output_regex)
            sanitized_response = self._clean_up_white_space(response)
            if not re.search(sanitized_regex, sanitized_response):
                if suppress:
                    raise RuntimeError("Did not receive expected output '{0}'. Actual output suppressed.".format(expected_output_regex))
                else:
                    raise RuntimeError("Did not receive expected output '{0}'. Actual output: {1}".format(expected_output_regex, redacted_response))
        return response

    def _perform_hops(self, hops, success_condition=None, previous_output="", error_on_success_not_met=False):
        """
        This function iterates through the passed in hops, running them and passing the output from each hop to the next.
        It also accepts an optional success condition regex that, if present, stops iteration. This function also
        optionally accepts previous_output, allowing you to chain calls to _perform_hops together.
  
        A hop is a function that performs a connection "hop". Hops take the output of the previous hop as input, perform
        some connection steps (can be no-op based on input), and return the current output from self.connection. This 
        function is a hop, so hops can be chained arbitrarily deeply. Yo dawg, I herd you like hops...
        """
        previous_output = previous_output
        for hop in hops:
            if success_condition and re.search(success_condition, previous_output):
                logger.info("Success condition {0} reached".format(success_condition))
                return previous_output
            logger.info("Performing hop {0}".format(hop))
            previous_output = hop(previous_output)
       
        if success_condition and not re.search(success_condition, previous_output):
            logger.info("All hops completed but success condition not met")
            if error_on_success_not_met:
                raise RuntimeError("All hops completed but success condition not met")
            
        return previous_output        
        
    def _spawn_connection(self, *args, **kwargs):
        self.connection = pexpect.spawn('bash')
        bash_output = self._read(1)
  
        logger.info("Connection object created")
        return bash_output 
