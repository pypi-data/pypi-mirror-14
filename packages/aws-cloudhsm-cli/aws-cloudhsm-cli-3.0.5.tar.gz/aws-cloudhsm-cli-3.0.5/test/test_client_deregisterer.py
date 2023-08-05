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
from cloudhsmcli.client_deregisterer import ClientDeregisterer
from cloudhsmcli.exceptions import PartitionNotFoundException
from scraps import hapg_description, client_description, hsm1_desc, hsm2_desc, hsm3_desc

class TestClientDeregisterer(TestCase):
    def setUp(self):
        self.base_args = {
            'client_arn': 'arn:client',
            'hapg_arn': 'arn:hapg',
            'aws_creds': {'region': 'fake'}}

    def test_run_normal_case(self):
        '''
        Test that deregisterer run method calls all submethods correctly.
        '''

        deregisterer = ClientDeregisterer(**self.base_args)
        call_sequence = []
        with patch.multiple(deregisterer, connect_to_aws=DEFAULT, find_hsm_info=DEFAULT, revoke_partition_and_remove_client=DEFAULT) as mocks:
            for k, v in mocks.items():
                def side_effect(method=k):
                    call_sequence.append(method)
                    return None
                v.side_effect = side_effect
            #Run Test
            deregisterer.run()
        # Verify
        self.assertEquals(call_sequence, [{'region': 'fake'}, 'find_hsm_info', 'revoke_partition_and_remove_client'])

    def test_init(self):
        '''
        Test that deregisterer __init__ sets up instance variables.
        '''
        deregisterer = ClientDeregisterer(**self.base_args)
        self.assertEquals(deregisterer.client_arn, self.base_args['client_arn'])
        self.assertEquals(deregisterer.hapg_arn, self.base_args['hapg_arn'])
        self.assertEquals(deregisterer.aws_creds, self.base_args['aws_creds'])

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
        deregisterer = ClientDeregisterer(**self.base_args)
        deregisterer.cloudhsm = mock_cloudhsm
        deregisterer.find_hsm_info()
        # Verify
        assert_equals(deregisterer.hsm_info, [('1.2.3.4', '123456001'), ('2.3.4.5', '234567002')])

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
        deregisterer = ClientDeregisterer(**self.base_args)
        deregisterer.cloudhsm = mock_cloudhsm
        deregisterer.find_hsm_info()

    def test_revoke_partition_and_remove_client(self):
        '''
        Test that revoke_partition_and_remove_client revokes partitions and remove clients properly.
        '''
        # Set up the mocks
        mock_cloudhsm = MagicMock()
        mock_cloudhsm.describe_client.return_value = {'Label': 'clitest'}
        mock_remove_client_from_hsm = Mock()
        mock_remove_client_from_hsm.return_value = True
        mock_revoke_partition_from_client = Mock()
        mock_revoke_partition_from_client.return_value = True

        # Run test
        deregisterer = ClientDeregisterer(**self.base_args)
        deregisterer.hsm_info = [('1.2.3.4', '123456001'), ('2.3.4.5', '234567002')]
        deregisterer.cloudhsm = mock_cloudhsm
        deregisterer.remove_client_from_hsm = mock_remove_client_from_hsm
        deregisterer.revoke_partition_from_client = mock_revoke_partition_from_client
        deregisterer.revoke_partition_and_remove_client()

        # Verify
        assert_equals(deregisterer.revoke_partition_from_client.call_args_list,
                      [call('1.2.3.4', 'clitest', '123456001'),
                       call('2.3.4.5', 'clitest', '234567002')]
                     )

        assert_equals(deregisterer.remove_client_from_hsm.call_args_list,
                      [call('1.2.3.4', 'clitest'),
                       call('2.3.4.5', 'clitest')]
                     )
