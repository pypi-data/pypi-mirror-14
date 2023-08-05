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

from device_connections.base_adapter import BaseAdapter
import logging

logger = logging.getLogger('luna_device_connections.luna_adapter')

class LunaAdapter(BaseAdapter):
    def _device_prompt(self):
        return 'lunash'

    def _get_to_device_prompt(self):
        """
        Returns to the Luna shell prompt.  Use this function to "reset" the state of the session between commands.
        """
        response = self.connection._send_command_and_return_response("", end_condition_regex='lunash')
        if "lunash" not in response:
            # You're most likely sitting at a prompt waiting for proceed/quit from the user (such as when resetting the HSM).  Sending a "quit" at a normal prompt is a noop and is safe.
            logger.info("Not seeing 'lunash' while trying to get back to the luna shell prompt.  Sending a 'quit'. Actual output: " + response)
            quit_response = self.connection._send_command_and_return_response("quit", 'lunash')
            if not 'lunash' in quit_response:
                logger.warn("Our connection has died. Reconnecting.")
                self.connection.connection = None
                self.connection.connect()
        
