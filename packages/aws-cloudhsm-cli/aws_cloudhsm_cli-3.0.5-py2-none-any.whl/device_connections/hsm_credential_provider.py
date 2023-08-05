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
import tempfile

logger = logging.getLogger('device_connections.hsm_credential_provider')

class HsmCredentialProvider(object):
    def __init__(self, username, password=None, ssh_key_filename=None, ssh_key_passphrase=None):
        self.username = username
        self.key_passphrase = ssh_key_passphrase
        self.password = password
        self.key_filename = ssh_key_filename

    def __eq__(self, other):
        return self.username == other.username and \
            self.password == other.password and \
            self.key_filename == other.key_filename and \
            self.key_passphrase == other.key_passphrase
