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


from nose.tools import raises, nottest, assert_equals
from mock import patch, Mock, mock_open, call, MagicMock, DEFAULT
from unittest import TestCase
from datetime import datetime
from cloudhsmcli.hsm_initializer import HsmInitializer
from device_connections.hsm_credential_provider import HsmCredentialProvider

class TestHsmInitializer(TestCase):
    def test_run_normal_case(self):
        '''
        Test that initializer run method calls all submethods correctly.
        '''
        init = HsmInitializer(**self.base_args)
        call_sequence = []
        with patch.multiple(init, connect_to_aws=DEFAULT, discover_hsms=DEFAULT, confirm_zeroized=DEFAULT,
                            initialize_hsm=DEFAULT, restart_and_bind_ntls=DEFAULT) as mocks:
            for k, v in mocks.items():
                def side_effect(method=k):
                    call_sequence.append(method)
                    return None
                v.side_effect = side_effect
            #Test
            init.hsm_descriptions={'arn:hsm':{'api_description':{'EniIp':'1234'}}}
            init.run()
        # Verify
        self.assertEquals(call_sequence,
                          [self.base_args['aws_creds'], 
                           [self.base_args['hsm_arn']], 
                           init.hsm_descriptions,
                           'initialize_hsm', 
                           'restart_and_bind_ntls'])

    @raises(ZeroDivisionError)
    def test_run_raises_exception(self):
        '''
        Test that initializer run method reraises an exception
        '''
        init = HsmInitializer(**self.base_args)
        def connect_to_aws(arg):
            return 1/0
        init.connect_to_aws = connect_to_aws
        # Test
        init.run()

    def test_init(self):
        '''
        Test that initializer __init__ sets up instance variables.
        '''
        init = HsmInitializer(**self.base_args)
        self.assertEquals(init.label, self.base_args['label'])
        self.assertEquals(init.so_password, self.base_args['so_password'])
        self.assertEquals(init.cloning_domain, self.base_args['cloning_domain'])
        self.assertEquals(init.hsm_arn, self.base_args['hsm_arn'])
        self.assertEquals(init.aws_creds, self.base_args['aws_creds'])

    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    def test_initialize_hsm_normal(self, lam):
        '''
        Test that initializer initialize_hsm handles the normal case
        '''
        init = HsmInitializer(**self.base_args)
        init.eni_ip = '10.0.0.1'
        # Test
        init.initialize_hsm()
        # Verify
        self.assertEquals(lam.mock_calls,
                          [call('10.0.0.1'),
                           call().initialize_hsm(self.base_args['label'], 
                                                 self.base_args['cloning_domain'], 
                                                 self.base_args['so_password'])])

    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    def test_restart_and_bind_ntls_normal(self, lam):
        '''
        Test that initializer restart_and_bind_ntls handles the normal case
        '''
        init = HsmInitializer(**self.base_args)
        init.eni_ip = '10.0.0.1'
        # Test
        init.restart_and_bind_ntls()
        # Verify
        self.assertEquals(lam.mock_calls,
                          [call('10.0.0.1'),
                           call().restart_and_bind_ntls()])

    base_args = {
        'hsm_arn': 'arn:hsm',
        'so_password': 'pwd',
        'cloning_domain': 'dom',
        'label': 'label',
        'aws_creds': {'region': 'fake'},
    }
