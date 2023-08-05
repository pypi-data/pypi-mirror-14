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
from cloudhsmcli.client_registerer import ClientRegisterer
from cloudhsmcli.exceptions import PartitionNotFoundException
from scraps import hapg_description, client_description, hsm1_desc, hsm2_desc, hsm3_desc

class TestClientRegisterer(TestCase):
    def setUp(self):
        self.base_args = {
            'client_arn': 'arn:client',
            'hapg_arn': 'arn:hapg',
            'aws_creds': {'region': 'fake'}}

    def test_run_normal_case(self):
        '''
        Test that registerer run method calls all submethods correctly.
        '''

        registerer = ClientRegisterer(**self.base_args)
        call_sequence = []
        with patch.multiple(registerer, connect_to_aws=DEFAULT, find_hsm_info=DEFAULT, register_client_and_assign_partition=DEFAULT) as mocks:
            for k, v in mocks.items():
                def side_effect(method=k):
                    call_sequence.append(method)
                    return None
                v.side_effect = side_effect
            #Run Test
            registerer.run()
        # Verify
        self.assertEquals(call_sequence, [{'region': 'fake'}, 'find_hsm_info', 'register_client_and_assign_partition'])

    def test_init(self):
        '''
        Test that registerer __init__ sets up instance variables.
        '''
        registerer = ClientRegisterer(**self.base_args)
        self.assertEquals(registerer.client_arn, self.base_args['client_arn'])
        self.assertEquals(registerer.hapg_arn, self.base_args['hapg_arn'])
        self.assertEquals(registerer.aws_creds, self.base_args['aws_creds'])

    def test_find_hsm_info(self):
        '''
        Test that find_hsm_info collects all the hsm information for the given partition list
        '''
        # Set up the mocks
        mock_cloudhsm = MagicMock()
        mock_cloudhsm.list_hsms.return_value = {'HsmList': ['arn:hsm1', 'arn:hsm2']}
        mock_cloudhsm.describe_hsm.side_effect = [{'SerialNumber': '123456', 'EniIp': '1.2.3.4'},
                                                  {'SerialNumber': '234567', 'EniIp': '2.3.4.5'}]
        mock_cloudhsm.describe_hapg.return_value = {'PartitionSerialList': ['123456001', '234567002']}

        # Run test
        registerer = ClientRegisterer(**self.base_args)
        registerer.cloudhsm = mock_cloudhsm
        registerer.find_hsm_info()
        # Verify
        assert_equals(registerer.hsm_info, [('1.2.3.4', '123456001'), ('2.3.4.5', '234567002')])

    @raises(PartitionNotFoundException)
    def test_find_hsm_info_raises_exception(self):
        '''
        Test that find_hsm_info raises an exception when a partition can't be found on user's HSMs
        '''
        # Set up the mocks
        mock_cloudhsm = MagicMock()
        mock_cloudhsm.list_hsms.return_value = {'HsmList': ['arn:hsm1', 'arn:hsm2']}
        mock_cloudhsm.describe_hsm.side_effect = [{'SerialNumber': '123456', 'EniIp': '1.2.3.4'},
                                                  {'SerialNumber': '234567', 'EniIp': '2.3.4.5'}]
        mock_cloudhsm.describe_hapg.return_value = {'PartitionSerialList': ['123456001', '234567002', '345678901']}

        # Run test
        registerer = ClientRegisterer(**self.base_args)
        registerer.cloudhsm = mock_cloudhsm
        registerer.find_hsm_info()

    @patch('cloudhsmcli.util.write_to_file')
    def test_register_client_and_assign_partition(self, write_mock):
        '''
        Test that register_client_and_assign_partition registers clients and assigns partitions properly.
        '''
        # Set up the mocks
        mock_cloudhsm = MagicMock()
        mock_cloudhsm.describe_client.return_value = {'Label': 'clitest', 'Certificate': '-----BEGIN CERTIFICATE-----\n\r-----END CERTIFICATE-----\n\r'}
        mock_register_client_on_hsm = Mock()
        mock_register_client_on_hsm.return_value = True
        mock_assign_partition_to_client = Mock()
        mock_assign_partition_to_client.return_value = True

        # Run test
        registerer = ClientRegisterer(**self.base_args)
        registerer.hsm_info = [('1.2.3.4', '123456001'), ('2.3.4.5', '234567002')]
        registerer.cloudhsm = mock_cloudhsm
        registerer.register_client_on_hsm = mock_register_client_on_hsm
        registerer.assign_partition_to_client = mock_assign_partition_to_client
        registerer.register_client_and_assign_partition()

        # Verify
        assert_equals(registerer.register_client_on_hsm.call_args_list,
                      [call('1.2.3.4', 'clitest', '/tmp/clitest.pem'),
                       call('2.3.4.5', 'clitest', '/tmp/clitest.pem')]
                     )

        assert_equals(registerer.assign_partition_to_client.call_args_list,
                      [call('1.2.3.4', 'clitest', partition_serial='123456001'),
                       call('2.3.4.5', 'clitest', partition_serial='234567002')]
                     )
