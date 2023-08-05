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
from mock import ANY, patch, Mock, mock_open, call, MagicMock, DEFAULT
from unittest import TestCase
from datetime import datetime
from cloudhsmcli.hapg_adder import HapgAdder
from device_connections.hsm_credential_provider import HsmCredentialProvider
from cloudhsmcli.exceptions import HsmAlreadyInHapgException
import copy

class TestHapgAdder(TestCase):
    def setUp(self):
        self.base_args = {
            'hsm_arn': 'arn:hsm',
            'hapg_arn': 'arn:aws:cloudhsm:us-east-1:5550001234567:hapg-fff55500',
            'partition_password': 'part',
            'so_password': 'pwd',
            'cloning_domain': 'dom',
            'aws_creds': {'region': 'fake'},
        }

        self.hsm_descriptions = {
            'arn:hsm': {
                'hsm_description': {'serial_number': '1234'},
                'api_description': {'EniIp': '10.0.0.1'}
            }
        }

        self.hapg_description = {'PartitionSerialList':['56789'], 'Label': 'label'}

    def test_run_normal_case(self):
        '''
        Test that adder run method calls all submethods correctly.
        '''
        adder = HapgAdder(**self.base_args)
        call_sequence = []
        with patch.multiple(adder, connect_to_aws=DEFAULT, discover_hsms=DEFAULT, confirm_not_zeroized=DEFAULT,
                            _confirm_hsm_not_in_hapg=DEFAULT, _create_partition=DEFAULT, _modify_hapg=DEFAULT) as mocks:
            for k, v in mocks.items():
                def side_effect(method=k):
                    call_sequence.append(method)
                    return None
                v.side_effect = side_effect
            #Test
            adder.hsm_descriptions={'arn:hsm':{'api_description':{'EniIp':'1234'}}}
            adder.run()
        # Verify
        self.assertEquals(call_sequence,
                          [self.base_args['aws_creds'], 
                           [self.base_args['hsm_arn']], 
                           adder.hsm_descriptions,
                           '_confirm_hsm_not_in_hapg', 
                           '_create_partition',
                           '_modify_hapg'])

    @raises(ZeroDivisionError)
    def test_run_raises_exception(self):
        '''
        Test that adder run method reraises an exception
        '''
        adder = HapgAdder(**self.base_args)
        def connect_to_aws(arg):
            return 1/0
        adder.connect_to_aws = connect_to_aws
        # Test
        adder.run()
    
    def test_init(self):
        '''
        Test that adder __init__ sets up instance variables.
        '''
        adder = HapgAdder(**self.base_args)
        self.assertEquals(adder.so_password, self.base_args['so_password'])
        self.assertEquals(adder.partition_password, self.base_args['partition_password'])
        self.assertEquals(adder.cloning_domain, self.base_args['cloning_domain'])
        self.assertEquals(adder.hsm_arn, self.base_args['hsm_arn'])
        self.assertEquals(adder.hapg_arn, self.base_args['hapg_arn'])
        self.assertEquals(adder.aws_creds, self.base_args['aws_creds'])
  
    def test__confirm_hsm_not_in_hapg_normal_case(self):
        '''
        Test that _confirm_hsm_not_in_hapg completes when hsm is not already in hapg
        '''
        mock_conn = Mock()
        mock_conn.describe_hapg.return_value = self.hapg_description

        adder = HapgAdder(**self.base_args)
        adder.cloudhsm = mock_conn
        adder.hsm_descriptions = self.hsm_descriptions

        adder._confirm_hsm_not_in_hapg()

        mock_conn.describe_hapg.assert_called_once_with(self.base_args['hapg_arn'])

    @raises(HsmAlreadyInHapgException)
    def test__confirm_hsm_not_in_hapg_raises_exception(self):
        '''
        Test that _confirm_hsm_not_in_hapg raises an exception when hsm is already in hapg
        '''
        mock_conn = Mock()
        self.hapg_description['PartitionSerialList'].append('12345')
        mock_conn.describe_hapg.return_value = self.hapg_description
        
        adder = HapgAdder(**self.base_args)
        adder.cloudhsm = mock_conn
        adder.hsm_descriptions = self.hsm_descriptions

        adder._confirm_hsm_not_in_hapg()

    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    def test__create_partition_normal(self, mock_manipulator, mock_reader):
        '''
        Test that _create_partition creates a partition when one for this group does not already exist
        '''
        adder = HapgAdder(**self.base_args)
        adder.hsm_descriptions = self.hsm_descriptions
        adder.hapg_description = self.hapg_description

        mock_lookup = Mock()
        mock_lookup.side_effect = [None, '12345']
        adder.lookup_partition_serial = mock_lookup
       
        mock_label_gen = Mock()
        mock_label_gen.return_value = 'label'
        adder.generate_partition_label = mock_label_gen

        adder._create_partition()

        assert_equals(adder.partition_serial, '12345')
        mock_manipulator.assert_called_once_with('10.0.0.1')
        mock_manipulator.return_value.hsm_login.assert_called_once_with(password = self.base_args['so_password'])
        mock_manipulator.return_value.create_partition.assert_called_once_with(partition_label = 'label',
                                                                               partition_password = self.base_args['partition_password'],
                                                                               cloning_domain = self.base_args['cloning_domain'])

    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    def test__create_partition_already_exists(self, mock_manipulator, mock_reader):
        '''
        Test that _create_partition does not create a partition but does set serial when partition for this group already exists
        '''
        adder = HapgAdder(**self.base_args)
        adder.hsm_descriptions = self.hsm_descriptions
        adder.hapg_description = self.hapg_description
        adder.eni_ip = '1.2.3.4'

        mock_lookup = Mock()
        mock_lookup.return_value = '12345'
        adder.lookup_partition_serial = mock_lookup
       
        mock_label_gen = Mock()
        mock_label_gen.return_value = 'label'
        adder.generate_partition_label = mock_label_gen

        adder._create_partition()
        
        assert_equals(adder.partition_serial, '12345')
        assert_equals(0, mock_manipulator.return_value.hsm_login.call_count)
        assert_equals(0, mock_manipulator.return_value.create_partition.call_count)

    @raises(RuntimeError)
    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    def test__create_partition_raises(self, mock_manipulator, mock_reader):
        '''
        Test that _create_partition raises an exception when created partition is not found
        '''
        adder = HapgAdder(**self.base_args)
        adder.hsm_descriptions = self.hsm_descriptions
        adder.hapg_description = self.hapg_description
        adder.eni_ip = '1.2.3.4'

        mock_lookup = Mock()
        mock_lookup.return_value = None
        adder.lookup_partition_serial = mock_lookup
       
        adder._create_partition()

    def test__modify_hapg_normal(self):
        '''
        Test that _modify_hapg behaves as expected in normal case
        '''
        adder = HapgAdder(**self.base_args)
        adder.hapg_description = copy.deepcopy(self.hapg_description)
        adder.partition_serial = '12345'
        adder.cloudhsm = Mock()

        adder._modify_hapg()

        expected_list = self.hapg_description['PartitionSerialList']
        expected_list.append('12345')
        adder.cloudhsm.modify_hapg.assert_called_once_with(self.base_args['hapg_arn'], partition_serial_list=expected_list)
