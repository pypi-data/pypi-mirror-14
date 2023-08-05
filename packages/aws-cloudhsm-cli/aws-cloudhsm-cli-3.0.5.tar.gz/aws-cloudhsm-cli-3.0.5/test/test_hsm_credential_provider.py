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

import unittest
import pexpect
from nose.tools import *
from mock import call, patch, MagicMock, Mock
from device_connections import hsm_credential_provider as hcp

def test_provider():
    '''
    Test that the credential provider equality works on passwords
    '''
    prov1 = hcp.HsmCredentialProvider(username='user', password='pass')
    prov2 = hcp.HsmCredentialProvider(username='user', password='pass')
    prov3 = hcp.HsmCredentialProvider(username='george', ssh_key_filename='fake.pem')
    assert_equal(prov1, prov2)
    assert_not_equal(prov1, prov3)

