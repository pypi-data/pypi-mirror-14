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
from cloudhsmcli.hapg_cloner import HapgCloner
import subprocess

class TestHapgCloner(TestCase):
    def setUp(self):
        self.base_args = {
            'src_hapg_arn': 'arn:hapg1',
            'dest_hapg_arn': 'arn:hapg2',
            'hapg_password': 'pass',
            'aws_creds': {'region': 'fake'}}

    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    @patch('cloudhsmcli.hapg_cloner.os.remove')
    @patch('cloudhsmcli.hapg_cloner.shutil.copyfile')
    @patch('cloudhsmcli.hapg_cloner.os.path.isfile', return_value=True)
    def test_run_when_CAFile_cert_exists(self, isfile_mock, copy_mock, remove_mock, dir_mock):
        '''
        Test that cloner run method calls all submethods correctly.
        '''

        cloner = HapgCloner(**self.base_args)
        cloner.isClient = True
        cloner.registeredClient = True
        call_sequence = []
        with patch.multiple(cloner, connect_to_aws=DEFAULT, merge_partition_serials=DEFAULT, find_hsm_info=DEFAULT, ensure_ntls_on_all=DEFAULT,
                            create_temporary_client=DEFAULT, register_client_and_assign_partition=DEFAULT, generate_client_config=DEFAULT,
                            synchronize_hapgs=DEFAULT, revoke_partition_and_remove_client=DEFAULT, delete_temp_client=DEFAULT) as mocks:
            for k, v in mocks.items():
                def side_effect(method=k):
                    call_sequence.append(method)
                    return None
                v.side_effect = side_effect
            #Run Test
            cloner.run()
        # Verify
        self.assertEquals(call_sequence,
                          [{'region': 'fake'}, 'merge_partition_serials', 'find_hsm_info', 'create_temporary_client',
                           'register_client_and_assign_partition', 'generate_client_config', 'ensure_ntls_on_all',
                           'synchronize_hapgs', 'revoke_partition_and_remove_client', 'delete_temp_client'])
        assert_equals(copy_mock.call_count, 4)
        assert_equals(remove_mock.call_count, 2)

    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    @patch('cloudhsmcli.hapg_cloner.os.remove')
    @patch('cloudhsmcli.hapg_cloner.shutil.copyfile')
    @patch('cloudhsmcli.hapg_cloner.os.path.isfile')
    def test_run_when_CAFile_cert_does_not_exist(self, isfile_mock, copy_mock, remove_mock, dir_mock):
        '''
        Test that cloner run method calls all submethods correctly.
        '''

        cloner = HapgCloner(**self.base_args)
        cloner.isClient = True
        cloner.registeredClient = True
        isfile_mock.side_effect = [False, True, False]
        call_sequence = []
        with patch.multiple(cloner, connect_to_aws=DEFAULT, merge_partition_serials=DEFAULT, find_hsm_info=DEFAULT, ensure_ntls_on_all=DEFAULT,
                            create_temporary_client=DEFAULT, register_client_and_assign_partition=DEFAULT, generate_client_config=DEFAULT,
                            synchronize_hapgs=DEFAULT, revoke_partition_and_remove_client=DEFAULT, delete_temp_client=DEFAULT) as mocks:
            for k, v in mocks.items():
                def side_effect(method=k):
                    call_sequence.append(method)
                    return None
                v.side_effect = side_effect
            #Run Test
            cloner.run()
        # Verify
        self.assertEquals(call_sequence,
                          [{'region': 'fake'}, 'merge_partition_serials', 'find_hsm_info', 'create_temporary_client',
                           'register_client_and_assign_partition', 'generate_client_config', 'ensure_ntls_on_all',
                           'synchronize_hapgs', 'revoke_partition_and_remove_client', 'delete_temp_client'])
        assert_equals(copy_mock.call_count, 2)
        assert_equals(remove_mock.call_count, 2)


    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_init(self, dir_mock):
        '''
        Test that cloner __init__ sets up instance variables.
        '''
        # Run test
        cloner = HapgCloner(**self.base_args)
        # Verify
        self.assertEquals(cloner.src_hapg_arn, self.base_args['src_hapg_arn'])
        self.assertEquals(cloner.dest_hapg_arn, self.base_args['dest_hapg_arn'])
        self.assertEquals(cloner.hapg_password, self.base_args['hapg_password'])
        self.assertEquals(cloner.aws_creds, self.base_args['aws_creds'])

    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_merge_partition_serials(self, dir_mock):
        '''
        Test that merge_partition_serials merges the partitions of src_hapg and dest_hapg into a list properly
        '''
        # Set up the mocks
        mock_cloudhsm = MagicMock()
        mock_cloudhsm.describe_hapg.side_effect = [{'Label': 'hapg1', 'PartitionSerialList': ['123456001', '234567002']}, 
                                                   {'Label': 'hapg2', 'PartitionSerialList': ['123456003', '234567004']}]

        # Run test
        cloner = HapgCloner(**self.base_args)
        cloner.cloudhsm = mock_cloudhsm
        cloner.merge_partition_serials()
        # Verify
        assert_equals(cloner.partition_serials, ['123456001', '234567002', '123456003', '234567004'])

    @raises(Exception)
    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_merge_partition_serials(self, dir_mock):
        '''
        Test that merge_partition_serials raises exceptions when src_hapg/dest_hapg is empty
        '''
        # Set up the mocks
        mock_cloudhsm = MagicMock()
        mock_cloudhsm.describe_hapg.side_effect = [{'Label': 'hapg1', 'PartitionSerialList': ['123456001', '234567002']},
                                                   {'Label': 'hapg2', 'PartitionSerialList': []}]

        # Run test
        cloner = HapgCloner(**self.base_args)
        cloner.cloudhsm = mock_cloudhsm
        cloner.merge_partition_serials()

    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_find_hsm_info(self, dir_mock):
        '''
        Test that find_hsm_info collects all the hsm information for the given partition list
        '''
        # Set up the mocks
        mock_cloudhsm = MagicMock()
        mock_cloudhsm.list_hsms.return_value = {'HsmList': ['arn:hsm1', 'arn:hsm2']}
        mock_cloudhsm.describe_hsm.side_effect = [{'SerialNumber': '123456', 'EniIp': '1.2.3.4'}, 
                                                  {'SerialNumber': '234567', 'EniIp': '2.3.4.5'}]

        # Run test
        cloner = HapgCloner(**self.base_args)
        cloner.cloudhsm = mock_cloudhsm
        cloner.partition_serials = ['123456001', '234567002', '123456003', '234567004']
        cloner.find_hsm_info()
        # Verify
        assert_equals(cloner.hsm_info, [('1.2.3.4', ['123456001', '123456003']), ('2.3.4.5', ['234567002', '234567004'])])

    @patch('cloudhsmcli.hapg_cloner.subprocess.Popen')
    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_create_temporary_client(self, dir_mock, popen_mock):
        '''
        Test that create_temporary_client behaves correctly.
        '''
        # Set up the mocks
        popen_mock.return_value.returncode = 0
        popen_mock.return_value.communicate.return_value = ('Private Key created and written to:', None)
        # Run test
        cloner = HapgCloner(**self.base_args)
        cloner.client_name = 'temp_client_time'
        cloner.create_temporary_client()
        # Verify
        assert_equals(popen_mock.call_args_list,
                      [call(['/usr/safenet/lunaclient/bin/vtl', 'createCert', '-n', 'temp_client_time'], stdout=-1)])

    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_register_client_and_assign_partition(self, dir_mock):
        '''
        Test that register_client_and_assign_partition registers clients and assigns partitions properly.
        '''
        # Set up the mocks
        mock_register_client_on_hsm = Mock()
        mock_register_client_on_hsm.return_value = True
        mock_assign_partition_to_client = Mock()
        mock_assign_partition_to_client.return_value = True

        # Run test
        cloner = HapgCloner(**self.base_args)
        cloner.client_name = 'temp_client_time'
        cloner.hsm_info = [('1.2.3.4', ['123456001', '123456003']), ('2.3.4.5', ['234567002', '234567004'])]
        cloner.register_client_on_hsm = mock_register_client_on_hsm
        cloner.assign_partition_to_client = mock_assign_partition_to_client
        cloner.register_client_and_assign_partition()

        # Verify
        assert_equals(cloner.register_client_on_hsm.call_args_list,
                      [call('1.2.3.4', 'temp_client_time', '/usr/safenet/lunaclient/cert/client/temp_client_time.pem'),
                       call('2.3.4.5', 'temp_client_time', '/usr/safenet/lunaclient/cert/client/temp_client_time.pem')]
                     )

        assert_equals(cloner.assign_partition_to_client.call_args_list,
                      [call('1.2.3.4', 'temp_client_time', partition_serial='123456001'),
                       call('1.2.3.4', 'temp_client_time', partition_serial='123456003'),
                       call('2.3.4.5', 'temp_client_time', partition_serial='234567002'),
                       call('2.3.4.5', 'temp_client_time', partition_serial='234567004')]
                     )

    @patch('cloudhsmcli.util.write_to_file')
    @patch('cloudhsmcli.util.generate_luna_53_config')
    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_generate_client_config(self, dir_mock, gen_mock, write_mock):
        '''
        Test that generate_client_config generates and writes the temporary config file to disk
        '''
        # Set up the mocks
        mock_scp_server_cert_from_hsm = Mock()
        # Run test
        cloner = HapgCloner(**self.base_args)
        cloner.client_name = 'temp_client_time'
        cloner.group_label = 'temp_group_time'
        cloner.hsm_info = [('1.2.3.4', ['123456001', '123456003']), ('2.3.4.5', ['234567002', '234567004'])]
        cloner.partition_serials = ['123456001', '234567002', '123456003', '234567004']
        cloner.scp_server_cert_from_hsm = mock_scp_server_cert_from_hsm
        cloner.generate_client_config()
        # Verify
        assert_equals(gen_mock.call_args_list,
                      [call('temp_client_time', set(['1.2.3.4', '2.3.4.5']), {'temp_group_time': ['123456001', '234567002', '123456003', '234567004']})])
        cloner.scp_server_cert_from_hsm.assert_has_calls(
            [call('1.2.3.4', '/usr/safenet/lunaclient/cert/server/CAFile.pem'),
             call('2.3.4.5', '/usr/safenet/lunaclient/cert/server/CAFile.pem')], any_order=True)

    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.hapg_cloner.subprocess.Popen')
    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_synchronize_hapgs(self, dir_mock, popen_mock, lsr):
        '''
        Test that synchronize_hapgs runs the VTL command with the proper arguments
        '''
        # Set up the mocks
        popen_mock.return_value.returncode = 0
        popen_mock.return_value.communicate.return_value = ('Synchronization completed', None)
        lsr.return_value.count_partition_objects.return_value = 2
        # Run test
        cloner = HapgCloner(**self.base_args)
        cloner.group_label = 'temp_group_time'
        cloner.hapg_password = 'pass'
        cloner.synchronize_hapgs()
        # Verify
        assert_equals(popen_mock.call_args_list,
                      [call(['/usr/safenet/lunaclient/bin/vtl', 'haAdmin', 'synchronize', '-group', 'temp_group_time', '-password', 'pass'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)])

    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_revoke_partition_and_remove_client(self, dir_mock):
        '''
        Test that revoke_partition_and_remove_client deregisters clients and revokes partitions properly.
        '''
        # Set up the mocks
        mock_remove_client_from_hsm = Mock()
        mock_remove_client_from_hsm.return_value = True
        mock_revoke_partition_from_client = Mock()
        mock_revoke_partition_from_client.return_value = True

        # Run test
        cloner = HapgCloner(**self.base_args)
        cloner.client_name = 'temp_client_time'
        cloner.hsm_info = [('1.2.3.4', ['123456001', '123456003']), ('2.3.4.5', ['234567002', '234567004'])]
        cloner.remove_client_from_hsm = mock_remove_client_from_hsm
        cloner.revoke_partition_from_client = mock_revoke_partition_from_client
        cloner.revoke_partition_and_remove_client()

        # Verify
        assert_equals(cloner.revoke_partition_from_client.call_args_list,
                      [call('1.2.3.4', 'temp_client_time', '123456001'),
                       call('1.2.3.4', 'temp_client_time', '123456003'),
                       call('2.3.4.5', 'temp_client_time', '234567002'),
                       call('2.3.4.5', 'temp_client_time', '234567004')]
                     )

        assert_equals(cloner.remove_client_from_hsm.call_args_list,
                      [call('1.2.3.4', 'temp_client_time'),
                       call('2.3.4.5', 'temp_client_time')]
                     )

    @patch('cloudhsmcli.hapg_cloner.os.remove')
    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_delete_temp_client(self, dir_mock, remove_mock):
        '''
        Test that delete_temp_client deletes the temporary client locally
        '''
        # Run test
        cloner = HapgCloner(**self.base_args)
        cloner.client_name = 'temp_client_time'
        cloner.delete_temp_client()
        # Verify
        assert_equals(remove_mock.call_args_list,
                      [call('/usr/safenet/lunaclient/cert/client/temp_client_time.pem'),
                       call('/usr/safenet/lunaclient/cert/client/temp_client_timeKey.pem')])

