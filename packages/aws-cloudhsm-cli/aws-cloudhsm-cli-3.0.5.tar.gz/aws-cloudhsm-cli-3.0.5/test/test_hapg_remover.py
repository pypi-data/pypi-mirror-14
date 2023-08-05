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
from cloudhsmcli.hapg_remover import HapgRemover
from device_connections.hsm_credential_provider import HsmCredentialProvider
from cloudhsmcli.exceptions import HsmNotInHapgException
import copy

class TestHapgRemover(TestCase):
    def setUp(self):
        self.base_args = {
            'hsm_arn': 'arn:hsm',
            'hapg_arn': 'arn:aws:cloudhsm:us-east-1:555000123456:hapg-fff55500',
            'so_password': 'pwd',
            'aws_creds': {'region': 'fake'},
        }

        self.hsm_descriptions = {
            'arn:hsm': {
                'hsm_description': {'serial_number': '1234'},
                'api_description': {'EniIp': '10.0.0.1'}
            }
        }

        self.hapg_description = {'PartitionSerialList':['12345'], 'Label': 'label'}

    def test_run_normal_case(self):
        '''
        Test that remover run method calls all submethods correctly.
        '''
        remover = HapgRemover(**self.base_args)
        call_sequence = []
        with patch.multiple(remover, connect_to_aws=DEFAULT, discover_hsms=DEFAULT,
                            _remove_partition=DEFAULT, _modify_hapg=DEFAULT) as mocks:
            for k, v in mocks.items():
                def side_effect(method=k):
                    call_sequence.append(method)
                    return None
                v.side_effect = side_effect
            #Test
            remover.hsm_descriptions={'arn:hsm':{'api_description':{'EniIp':'1234'}}}
            remover.run()
        # Verify
        self.assertEquals(call_sequence,
                          [self.base_args['aws_creds'], 
                           [self.base_args['hsm_arn']], 
                           '_remove_partition',
                           '_modify_hapg'])

    @raises(ZeroDivisionError)
    def test_run_raises_exception(self):
        '''
        Test that remover run method reraises an exception
        '''
        remover = HapgRemover(**self.base_args)
        def connect_to_aws(arg):
            return 1/0
        remover.connect_to_aws = connect_to_aws
        # Test
        remover.run()
    
    def test_init(self):
        '''
        Test that remover __init__ sets up instance variables.
        '''
        remover = HapgRemover(**self.base_args)
        self.assertEquals(remover.so_password, self.base_args['so_password'])
        self.assertEquals(remover.hsm_arn, self.base_args['hsm_arn'])
        self.assertEquals(remover.hapg_arn, self.base_args['hapg_arn'])
        self.assertEquals(remover.aws_creds, self.base_args['aws_creds'])
 
    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    def test__remove_partition_normal(self, mock_manipulator, mock_reader):
        '''
        Test that _remove_partition removes a partition when one for this group does already exist
        '''
        remover = HapgRemover(**self.base_args)
        remover.hsm_descriptions = self.hsm_descriptions
        remover.hapg_description = self.hapg_description
        remover.eni_ip = '10.0.0.1'

        mock_lookup = Mock()
        mock_lookup.side_effect = ['12345', None]
        remover.lookup_partition_serial = mock_lookup
       
        mock_label_gen = Mock()
        mock_label_gen.return_value = 'label'
        remover.generate_partition_label = mock_label_gen

        remover._remove_partition()

        mock_manipulator.assert_called_once_with('10.0.0.1')
        mock_manipulator.return_value.hsm_login.assert_called_once_with(password = self.base_args['so_password'])
        mock_manipulator.return_value.delete_partition.assert_called_once_with(partition_label = 'label')

    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    def test__remove_partition_does_not_exist(self, mock_manipulator, mock_reader):
        '''
        Test that _remove_partition does not do anything when partition does not exist
        '''
        remover = HapgRemover(**self.base_args)
        remover.hsm_descriptions = self.hsm_descriptions
        remover.hapg_description = self.hapg_description
        remover.eni_ip = '1.2.3.4'

        mock_lookup = Mock()
        mock_lookup.return_value = None
        remover.lookup_partition_serial = mock_lookup
       
        mock_label_gen = Mock()
        mock_label_gen.return_value = 'label'
        remover.generate_partition_label = mock_label_gen

        remover._remove_partition()
        
        assert_equals(0, mock_manipulator.return_value.hsm_login.call_count)
        assert_equals(0, mock_manipulator.return_value.create_partition.call_count)

    @raises(RuntimeError)
    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    def test__remove_partition_raises(self, mock_manipulator, mock_reader):
        '''
        Test that _remove_partition raises an exception when created partition is found after delete
        '''
        remover = HapgRemover(**self.base_args)
        remover.hsm_descriptions = self.hsm_descriptions
        remover.cloudhsm = Mock()
        remover.cloudhsm.describe_hapg.return_value = self.hapg_description
        remover.eni_ip = '1.2.3.4'

        mock_lookup = Mock()
        mock_lookup.return_value = '12345'
        remover.lookup_partition_serial = mock_lookup
       
        remover._remove_partition()

    def test__modify_hapg_normal(self):
        '''
        Test that _modify_hapg behaves as expected in normal case
        '''
        remover = HapgRemover(**self.base_args)
        remover.hsm_descriptions = self.hsm_descriptions
        remover.cloudhsm = Mock()
        remover.cloudhsm.describe_hapg.return_value = copy.deepcopy(self.hapg_description)

        remover._modify_hapg()

        expected_list = self.hapg_description['PartitionSerialList']
        expected_list.remove('12345')
        remover.cloudhsm.modify_hapg.assert_called_once_with(self.base_args['hapg_arn'], partition_serial_list=expected_list)


