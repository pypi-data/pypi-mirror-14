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
from mock import patch, Mock, mock_open, call, MagicMock, DEFAULT, ANY
from unittest import TestCase
from datetime import datetime
from cloudhsmcli.hsm_worker import HsmWorker
from cloudhsmcli.exceptions import HsmNotZeroizedException, HsmZeroizedException
from device_connections.hsm_credential_provider import HsmCredentialProvider

class TestHsmWorker(TestCase):
    @patch('cloudhsmcli.hsm_worker.api.connect')
    def test_connect_to_aws(self, connect):
        '''
        Test that worker connect_to_aws connects to AWS.
        '''
        connect.return_value = "connection!"
        worker = HsmWorker()
        worker.connect_to_aws({'region':'fake'})
        # Verify
        assert_equals(worker.cloudhsm, "connection!")
        connect.assert_called_once_with(region='fake')

    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    def test_discover_hsms_normal(self, lsr):
        '''
        Test that worker discover_hsms handles the normal case.
        '''
        worker = HsmWorker()
        worker.cloudhsm = Mock()
        worker.cloudhsm.describe_hsm.side_effect = [{ "EniIp": "10.0.0.1" }]
        lsr.return_value.is_luna_zeroized.return_value = "ISLUNAZEROIZED"
        lsr.return_value.get_serial_number.return_value = "GETSERIALNUMBER"
        
        # Test
        worker.discover_hsms({"hsm_arn": None})
        # Verify
        assert_equals(worker.hsm_descriptions, {
                                                   "hsm_arn": {
                                                        "api_description": { "EniIp": "10.0.0.1" },
                                                        "hsm_description": {
                                                            "zeroized": "ISLUNAZEROIZED",
                                                            "serial_number": "GETSERIALNUMBER"
                                                        }
                                                    }
                                               })
        assert_equals(lsr.mock_calls,
                      [call('10.0.0.1'), call().is_luna_zeroized(), call().get_serial_number()])

    def test_confirm_zeroized_when_all_zeroized(self):
        '''
        Test that worker does nothing when confirm_zeroized is called and all HSMs are zeroized
        '''
        worker = HsmWorker()
        hsm_descriptions = {'hsm_1': {'hsm_description': {'zeroized': True}},
                            'hsm_2': {'hsm_description': {'zeroized': True}}}
        worker.confirm_zeroized(hsm_descriptions)

    @raises(HsmNotZeroizedException)
    def test_confirm_zeroized_when_not_zeroized(self):
        '''
        Test that worker raises HsmNotZeroizedException when confirm_zeroized is called and HSM is not zeroized
        '''
        worker = HsmWorker()
        hsm_descriptions = {'hsm_1': {'hsm_description': {'zeroized': True}},
                            'hsm_2': {'hsm_description': {'zeroized': False}, 'api_description': {'EniIp': '234'}}}
        worker.confirm_zeroized(hsm_descriptions)

    @raises(HsmZeroizedException)
    def test_confirm_not_zeroized_when_all_zeroized(self):
        '''
        Test that worker raises HsmZeroizedException when confirm_zeroized is called and all HSM is zeroized
        '''
        worker = HsmWorker()
        hsm_descriptions = {'hsm_1': {'hsm_description': {'zeroized': False}},
                            'hsm_2': {'hsm_description': {'zeroized': True}, 'api_description': {'EniIp': '234'}}}
        worker.confirm_not_zeroized(hsm_descriptions)

    def test_confirm_not_zeroized_when_not_zeroized(self):
        '''
        Test that worker does nothing when confirm_not_zeroized is called and HSMs are not zeroized
        '''
        worker = HsmWorker()
        hsm_descriptions = {'hsm_1': {'hsm_description': {'zeroized': False}},
                            'hsm_2': {'hsm_description': {'zeroized': False}}}
        worker.confirm_not_zeroized(hsm_descriptions)

    def test_lookup_partition_serial_not_found(self):
        '''
        Test that lockup_partition_serial returns None when partition with wanted label is not found
        '''
        mock_reader = Mock()
        mock_reader.get_partitions.return_value = [(1, 'a'), (2, 'b')]
        
        worker = HsmWorker()

        assert_equals(None, worker.lookup_partition_serial(mock_reader, 'c'))

    def test_lookup_partition_serial_found(self):
        '''
        Test that lockup_partition_serial returns serial when partition with wanted label is found
        '''
        mock_reader = Mock()
        mock_reader.get_partitions.return_value = [(1, 'a'), (2, 'b')]
        
        worker = HsmWorker()

        assert_equals(2, worker.lookup_partition_serial(mock_reader, 'b'))

    def test_generate_partition_label(self):
        '''
        Test that generate_partition_label behaves how we expect
        '''
        worker = HsmWorker()
        hapg_arn = 'arn:aws:cloudhsm:us-east-1:5550001234567:hapg-fff55500'
        expectation = "hapg-fff55500_12345"
        reality = worker.generate_partition_label(hapg_arn, '12345')
        assert_equals(expectation, reality)

    @patch('cloudhsmcli.hsm_worker.os.remove')
    @patch('cloudhsmcli.util.concatenate_files')
    @patch('cloudhsmcli.util.scp_file_from_remote_source')
    def test_scp_server_cert_from_hsm(self, scp_mock, cat_mock, remove_mock):
        '''
        Test that scp_server_cert_from_hsm behaves how we expect
        '''
        worker = HsmWorker()
        worker.scp_server_cert_from_hsm('1.2.3.4', '/usr/safenet/lunaclient/cert/server/CAFile.pem')

        assert_equals(scp_mock.call_args_list,
                      [call('1.2.3.4', 'server.pem', '/tmp/1.2.3.4_server.pem', ANY)])

        assert_equals(cat_mock.call_args_list,
                      [call('/tmp/1.2.3.4_server.pem', '/usr/safenet/lunaclient/cert/server/CAFile.pem')])

        assert_equals(remove_mock.call_args_list, [call('/tmp/1.2.3.4_server.pem')])

    @patch('cloudhsmcli.util.scp_file_to_remote_destination')
    def test_scp_client_cert_onto_hsm(self, scp_mock):
        '''
        Test that scp_client_cert_onto_hsm behaves how we expect
        '''
        worker = HsmWorker()
        worker.scp_client_cert_onto_hsm('1.2.3.4', '/usr/safenet/lunaclient/cert/client/clitest.pem')

        assert_equals(scp_mock.call_args_list,
                      [call('1.2.3.4', '/usr/safenet/lunaclient/cert/client/clitest.pem', '', ANY)])

    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    def test_register_client_on_hsm(self, lam, lsr):
        '''
        Test that register_client_on_hsm behaves how we expect
        '''
        lsr.return_value.get_clients.return_value = ['c2c', 'c3c']
        mock_scp_client_cert_onto_hsm = Mock()

        worker = HsmWorker()
        worker.scp_client_cert_onto_hsm = mock_scp_client_cert_onto_hsm
        worker.register_client_on_hsm('10.0.0.20', 'c1c', '/usr/safenet/lunaclient/cert/client/c1c.pem')

        assert_equals(worker.scp_client_cert_onto_hsm.call_args_list,
                      [call('10.0.0.20', '/usr/safenet/lunaclient/cert/client/c1c.pem')]
                     )

        assert_equals(lam.mock_calls,
                      [call('10.0.0.20'),
                       call().register_client('c1c', 'c1c')])

    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    def test_remove_client_from_hsm(self, lam, lsr):
        '''
        Test that remove_client_from_hsm behaves how we expect
        '''
        lsr.return_value.get_clients.return_value = ['c2c', 'c3c', 'c1c']
        lsr.return_value.get_client_partitions.return_value = []

        worker = HsmWorker()
        worker.remove_client_from_hsm('10.0.0.20', 'c1c')

        assert_equals(lam.mock_calls,
                      [call('10.0.0.20'),
                       call().remove_client('c1c')])

    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    def test_assign_partition_to_client(self, lam, lsr):
        '''
        Test that assign_partition_to_client behaves how we expect
        '''
        lsr.return_value.get_partitions.return_value = [('123456789', 'p4p'), ('234567890', 'p6p')]
        lsr.return_value.get_client_partitions.return_value = []

        worker = HsmWorker()
        worker.assign_partition_to_client('10.0.0.20', 'c1c', '123456789')

        assert_equals(lam.mock_calls,
                      [call('10.0.0.20'),
                       call().assign_partition_to_client('c1c', 'p4p')])

    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    def test_revoke_partition_from_client(self, lam, lsr):
        '''
        Test that revoke_partition_from_client behaves how we expect
        '''
        lsr.return_value.get_partitions.return_value = [('123456789', 'p4p'), ('234567890', 'p6p')]
        lsr.return_value.get_client_partitions.return_value = ['p6p', 'p8p']

        worker = HsmWorker()
        worker.revoke_partition_from_client('10.0.0.20', 'c1c', '234567890')

        assert_equals(lam.mock_calls,
                      [call('10.0.0.20'),
                       call().revoke_partition_from_client('c1c', 'p6p')])

    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    def test_ensure_ntls(self, lam):
        '''
        Test that ensure_ntls calls the same method on the manipulator.
        '''
        worker = HsmWorker()
        worker.ensure_ntls('1.2.3.4')

        assert_equals(lam.mock_calls,
                      [call('1.2.3.4'),
                       call().ensure_ntls()])
