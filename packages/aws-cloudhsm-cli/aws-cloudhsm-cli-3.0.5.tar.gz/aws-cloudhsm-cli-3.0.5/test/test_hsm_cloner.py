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
from cloudhsmcli.hsm_cloner import HsmCloner
import subprocess

class TestHsmCloner(TestCase):
    def setUp(self):
        self.base_args = {
            'src_hsm_arn': 'arn:hsm1',
            'dest_hsm_arn': 'arn:hsm2',
            'so_password': 'pass',
            'aws_creds': {'region': 'fake'}}

    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    @patch('cloudhsmcli.hsm_cloner.os.remove')
    @patch('cloudhsmcli.hsm_cloner.shutil.copyfile')
    @patch('cloudhsmcli.hsm_cloner.os.path.isfile', return_value=True)
    def test_run_when_CAFile_cert_exists(self, isfile_mock, copy_mock, remove_mock, dir_mock):
        '''
        Test that cloner run method calls all submethods correctly.
        '''

        cloner = HsmCloner(**self.base_args)
        cloner.isClient = True
        cloner.registeredClient = True
        cloner.synchronizedHsms = True
        cloner.src_hsm_ip = '1.2.3.4'
        cloner.dest_hsm_ip = '5.6.7.8'
        call_sequence = []
        with patch.multiple(cloner, connect_to_aws=DEFAULT,
                            determine_partitions_to_be_cloned=DEFAULT,
                            create_partitions_on_clone_hsm=DEFAULT,
                            create_temporary_client=DEFAULT,
                            register_client_and_assign_partition=DEFAULT,
                            synchronize_hsms=DEFAULT,
                            revoke_partition_and_remove_client=DEFAULT,
                            delete_temp_client=DEFAULT,
                            clone_client_configuration=DEFAULT,
                            ensure_ntls=DEFAULT) as mocks:
            for k, v in mocks.items():
                def maker(method):
                    def side_effect(*args):
                        call_sequence.append((method,) + args)
                        return None
                    return side_effect
                v.side_effect = maker(k)
            #Run Test
            cloner.run()
        # Verify
        self.assertEquals(call_sequence,
                          [('connect_to_aws', {'region': 'fake'}),
                           ('determine_partitions_to_be_cloned',),
                           ('create_partitions_on_clone_hsm',),
                           ('create_temporary_client',),
                           ('register_client_and_assign_partition',),
                           ('ensure_ntls', '1.2.3.4'),
                           ('ensure_ntls', '5.6.7.8'),
                           ('synchronize_hsms',),
                           ('revoke_partition_and_remove_client',),
                           ('delete_temp_client',),
                           ('clone_client_configuration',)])
        assert_equals(4, copy_mock.call_count)
        assert_equals(2, remove_mock.call_count)
    
    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    @patch('cloudhsmcli.hsm_cloner.os.remove')
    @patch('cloudhsmcli.hsm_cloner.shutil.copyfile')
    @patch('cloudhsmcli.hsm_cloner.os.path.isfile')
    def test_run_when_CAFile_cert_does_not_exist(self, isfile_mock, copy_mock, remove_mock, dir_mock):
        '''
        Test that cloner run method calls all submethods correctly.
        '''

        cloner = HsmCloner(**self.base_args)
        cloner.isClient = True
        cloner.registeredClient = True
        cloner.synchronizedHsms = True
        isfile_mock.side_effect = [False, True, False]
        cloner.src_hsm_ip = '1.2.3.4'
        cloner.dest_hsm_ip = '5.6.7.8'
        call_sequence = []
        with patch.multiple(cloner, connect_to_aws=DEFAULT,
                            determine_partitions_to_be_cloned=DEFAULT,
                            create_partitions_on_clone_hsm=DEFAULT,
                            create_temporary_client=DEFAULT,
                            register_client_and_assign_partition=DEFAULT,
                            synchronize_hsms=DEFAULT,
                            revoke_partition_and_remove_client=DEFAULT,
                            delete_temp_client=DEFAULT,
                            clone_client_configuration=DEFAULT,
                            ensure_ntls=DEFAULT) as mocks:
            for k, v in mocks.items():
                def maker(method):
                    def side_effect(*args):
                        call_sequence.append((method,) + args)
                        return None
                    return side_effect
                v.side_effect = maker(k)
            #Run Test
            cloner.run()
        # Verify
        self.assertEquals(call_sequence,
                          [('connect_to_aws', {'region': 'fake'}),
                           ('determine_partitions_to_be_cloned',),
                           ('create_partitions_on_clone_hsm',),
                           ('create_temporary_client',),
                           ('register_client_and_assign_partition',),
                           ('ensure_ntls', '1.2.3.4'),
                           ('ensure_ntls', '5.6.7.8'),
                           ('synchronize_hsms',),
                           ('revoke_partition_and_remove_client',),
                           ('delete_temp_client',),
                           ('clone_client_configuration',)])
        assert_equals(2, copy_mock.call_count)
        assert_equals(2, remove_mock.call_count)

    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_init(self, dir_mock):
        '''
        Test that cloner __init__ sets up instance variables.
        '''
        # Run test
        cloner = HsmCloner(**self.base_args)
        # Verify
        self.assertEquals(cloner.src_hsm_arn, self.base_args['src_hsm_arn'])
        self.assertEquals(cloner.dest_hsm_arn, self.base_args['dest_hsm_arn'])
        self.assertEquals(cloner.so_password, self.base_args['so_password'])
        self.assertEquals(cloner.aws_creds, self.base_args['aws_creds'])


    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_init(self, dir_mock):
        '''
        Test that cloner __init__ sets up instance variables.
        '''
        # Run test
        cloner = HsmCloner(**self.base_args)
        # Verify
        self.assertEquals(cloner.src_hsm_arn, self.base_args['src_hsm_arn'])
        self.assertEquals(cloner.dest_hsm_arn, self.base_args['dest_hsm_arn'])
        self.assertEquals(cloner.so_password, self.base_args['so_password'])
        self.assertEquals(cloner.aws_creds, self.base_args['aws_creds'])

    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_determine_partitions_to_be_cloned(self, dir_mock, lsr):
        '''
        Test that determine_partitions_to_be_cloned compiles a list of partitions on src_hsm_arn properly
        '''
        # Set up the mocks
        mock_cloudhsm = MagicMock()
        mock_cloudhsm.describe_hsm.side_effect = [{'HsmArn': 'arn:src_hsm', 'EniIp': '10.99.99.1', 'SerialNumber': '123456'},
                                                  {'HsmArn': 'arn:dest_hsm', 'EniIp': '10.99.99.2', 'SerialNumber': '234567'}]
        lsr.return_value.get_partitions.return_value = [('123456011', 'testPar1'), ('123456012', 'testPar2')]
        # Run test
        cloner = HsmCloner(**self.base_args)
        cloner.cloudhsm = mock_cloudhsm
        cloner.determine_partitions_to_be_cloned()
        # Verify
        assert_equals(cloner.src_hsm_ip, '10.99.99.1')
        assert_equals(cloner.src_hsm_serial, '123456')
        assert_equals(cloner.dest_hsm_ip, '10.99.99.2')
        assert_equals(cloner.dest_hsm_serial, '234567')

        lsr.assert_called_once_with('10.99.99.1')
        assert_equals(cloner.src_partition_info, {'123456011': 'testPar1', '123456012': 'testPar2'})

    @patch('cloudhsmcli.hsm_cloner.getpass.getpass', Mock(side_effect=['pass1', 'domain1', 'pass2', 'domain2', 'pass3', 'domain3']))
    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.hsm_worker.LunaApplianceManipulator')
    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_create_partitions_on_clone_hsm(self, dir_mock, lam, lsr):
        '''
        Test that create_partitions_on_clone_hsm creates all corresponding partitions on dest_hsm_arn
        '''
        # Set up the mocks
        lsr.return_value.get_partitions.side_effect = [[('234567012', 'hapg-ijkl4321_234567')],
                                                       [('234567012', 'hapg-ijkl4321_234567'), ('234567011', 'hapg-opqr4321_234567')],
                                                       [('234567012', 'hapg-ijkl4321_234567'), ('234567011', 'hapg-opqr4321_234567'), ('234567013', 'testPartition')]]
        mock_cloudhsm = MagicMock()
        mock_cloudhsm.describe_hapg.side_effect = [{'HapgArn': 'hapg-opqr4321', 'PartitionSerialList': ['123456011', '345678011']},
                                                   {'HapgArn': 'hapg-ijkl4321', 'PartitionSerialList': ['123456012', '234567012', '345678012']}]
        # Run test
        cloner = HsmCloner(**self.base_args)
        cloner.cloudhsm = mock_cloudhsm
        cloner.src_hsm_arn = 'arn:aws:cloudhsm:eu-central-1:057079634151:hsm-xyz56789'
        cloner.dest_hsm_ip = '2.3.4.5'
        cloner.dest_hsm_serial = '234567'
        cloner.src_partition_info = {'123456011': 'hapg-opqr4321_123456', '123456013': 'testPartition', '123456012': 'hapg-ijkl4321_123456'}
        cloner.create_partitions_on_clone_hsm()
        # Verify
        lsr.assert_called_once_with('2.3.4.5')
        lam.assert_called_once_with('2.3.4.5')
        lam.return_value.hsm_login.assert_called_once_with(password = self.base_args['so_password'])
        assert_equals(lam.return_value.create_partition.call_args_list,
                      [call(partition_label = 'hapg-opqr4321_234567', partition_password = 'pass1', cloning_domain = 'domain1'),
                       call(partition_label = 'testPartition', partition_password = 'pass2', cloning_domain = 'domain2')]
                     )
        assert_equals(cloner.dest_partition_info, {'234567011': 'hapg-opqr4321_234567', '234567012': 'hapg-ijkl4321_234567', '234567013': 'testPartition'})
        assert_equals(cloner.src_dest_serials, [('123456011', '234567011', 'pass1'), ('123456013', '234567013', 'pass2'), ('123456012', '234567012', 'pass3')])

    @patch('cloudhsmcli.hsm_cloner.subprocess.Popen')
    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_create_temporary_client(self, dir_mock, popen_mock):
        '''
        Test that create_temporary_client behaves correctly.
        '''
        # Set up the mocks
        popen_mock.return_value.returncode = 0
        popen_mock.return_value.communicate.return_value = ('Private Key created and written to:', None)
        # Run test
        cloner = HsmCloner(**self.base_args)
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
        cloner = HsmCloner(**self.base_args)
        cloner.src_hsm_ip = '1.2.3.4'
        cloner.dest_hsm_ip = '2.3.4.5'
        cloner.client_name = 'temp_client_time'
        cloner.src_partition_info = {'123456011': 'testPar1', '123456012': 'testPar2'}
        cloner.dest_partition_info = {'234567011': 'testPar1', '234567012': 'testPar2'}
        cloner.register_client_on_hsm = mock_register_client_on_hsm
        cloner.assign_partition_to_client = mock_assign_partition_to_client
        cloner.register_client_and_assign_partition()
        # Verify
        assert_equals(cloner.register_client_on_hsm.call_args_list,
                      [call('1.2.3.4', 'temp_client_time', '/usr/safenet/lunaclient/cert/client/temp_client_time.pem'),
                       call('2.3.4.5', 'temp_client_time', '/usr/safenet/lunaclient/cert/client/temp_client_time.pem')]
                     )
        assert_equals(cloner.assign_partition_to_client.call_args_list,
                      [call('1.2.3.4', 'temp_client_time', partition_serial='123456011'),
                       call('1.2.3.4', 'temp_client_time', partition_serial='123456012'),
                       call('2.3.4.5', 'temp_client_time', partition_serial='234567011'),
                       call('2.3.4.5', 'temp_client_time', partition_serial='234567012')]
                     )

    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.util.write_to_file')
    @patch('cloudhsmcli.util.generate_luna_53_config')
    @patch('cloudhsmcli.hsm_cloner.subprocess.Popen')
    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_synchronize_hsms(self, dir_mock, popen_mock, gen_mock, write_mock, lsr):
        '''
        Test that synchronize_hsms calls generate_luna_53_config() and runs the VTL command with proper arguments
        '''
        # Set up the mocks
        popen_mock.return_value.returncode = 0
        popen_mock.return_value.communicate.return_value = ('Synchronization', None)
        mock_scp_server_cert_from_hsm = Mock()
        # Run test
        cloner = HsmCloner(**self.base_args)
        cloner.src_hsm_ip = '1.2.3.4'
        cloner.dest_hsm_ip = '2.3.4.5'
        cloner.client_name = 'temp_client_time'
        cloner.group_label = 'temp_group_time'
        cloner.src_dest_serials = [('123456011', '234567011', 'pass1'), ('123456012', '234567012', 'pass2')]
        cloner.scp_server_cert_from_hsm = mock_scp_server_cert_from_hsm
        lsr.return_value.count_partition_objects.return_value = 2
        cloner.synchronize_hsms()
        # Verify
        assert_equals(cloner.scp_server_cert_from_hsm.call_args_list,
                      [call('1.2.3.4', '/usr/safenet/lunaclient/cert/server/CAFile.pem'),
                       call('2.3.4.5', '/usr/safenet/lunaclient/cert/server/CAFile.pem')])
        assert_equals(gen_mock.call_args_list,
                      [call('temp_client_time', ['1.2.3.4', '2.3.4.5'], {'temp_group_time': ['123456011', '234567011']}),
                       call('temp_client_time', ['1.2.3.4', '2.3.4.5'], {'temp_group_time': ['123456012', '234567012']})]
                     )
        assert_equals(popen_mock.call_args_list,
                      [call(['/usr/safenet/lunaclient/bin/vtl', 'haAdmin', 'synchronize', '-group', 'temp_group_time', '-password', 'pass1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE),
                       call(['/usr/safenet/lunaclient/bin/vtl', 'haAdmin', 'synchronize', '-group', 'temp_group_time', '-password', 'pass2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)])

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
        cloner = HsmCloner(**self.base_args)
        cloner.client_name = 'temp_client_time'
        cloner.src_hsm_ip = '1.2.3.4'
        cloner.dest_hsm_ip = '2.3.4.5'
        cloner.src_partition_info = {'123456011': 'testPar1', '123456012': 'testPar2'}
        cloner.dest_partition_info = {'234567011': 'testPar1', '234567012': 'testPar2'}
        cloner.remove_client_from_hsm = mock_remove_client_from_hsm
        cloner.revoke_partition_from_client = mock_revoke_partition_from_client
        cloner.revoke_partition_and_remove_client()
        # Verify
        assert_equals(cloner.revoke_partition_from_client.call_args_list,
                      [call('1.2.3.4', 'temp_client_time', '123456011'),
                       call('1.2.3.4', 'temp_client_time', '123456012'),
                       call('2.3.4.5', 'temp_client_time', '234567011'),
                       call('2.3.4.5', 'temp_client_time', '234567012')]
                     )
        assert_equals(cloner.remove_client_from_hsm.call_args_list,
                      [call('1.2.3.4', 'temp_client_time'),
                       call('2.3.4.5', 'temp_client_time')]
                     )

    @patch('cloudhsmcli.hsm_worker.LunaStateReader')
    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    @patch('cloudhsmcli.util.write_to_file')
    @patch('cloudhsmcli.hsm_cloner.os.remove')
    def test_clone_client_configuration(self, remove_mock, write_mock, dir_mock, lsr):
        '''
        Test that clone_client_configuration clones client configurations as expected.
        '''
        # Set up the mocks
        mock_cloudhsm = MagicMock()
        mock_register_client_on_hsm = Mock()
        mock_register_client_on_hsm.return_value = True
        mock_assign_partition_to_client = Mock()
        mock_assign_partition_to_client.return_value = True
        lsr.return_value.get_clients.return_value = ['client1', 'client2']
        lsr.return_value.get_client_fingerprint.side_effect = [['AA:BB:CC:DD:EE:FF:11:22:33:44:55:66:77:88:99:00'], ['11:22:33:44:55:66:77:88:99:00:AA:BB:CC:DD:EE:FF']]
        lsr.return_value.get_client_partitions.side_effect = [['hapg-opqr4321_123456'], ['hapg-opqr4321_123456', 'hapg-ijkl4321_123456']]
        # Run test
        cloner = HsmCloner(**self.base_args)
        cloner.dest_hsm_ip = '2.3.4.5'
        cloner.dest_hsm_serial = '234567'
        cloner.cloudhsm = mock_cloudhsm
        cloner.register_client_on_hsm = mock_register_client_on_hsm
        cloner.assign_partition_to_client = mock_assign_partition_to_client
        cloner.clone_client_configuration()
        # Verify
        assert_equals(cloner.register_client_on_hsm.call_args_list,
                      [call('2.3.4.5', 'client1', 'client1.pem'),
                       call('2.3.4.5', 'client2', 'client2.pem')]
                     )
        assert_equals(cloner.assign_partition_to_client.call_args_list,
                      [call('2.3.4.5', 'client1', partition_label='hapg-opqr4321_234567'),
                       call('2.3.4.5', 'client2', partition_label='hapg-opqr4321_234567'),
                       call('2.3.4.5', 'client2', partition_label='hapg-ijkl4321_234567')]
                     )
        assert_equals(remove_mock.call_count, 2)

    @patch('cloudhsmcli.hsm_cloner.os.remove')
    @patch('cloudhsmcli.util.os.path.isdir', return_value=True)
    def test_delete_temp_client(self, dir_mock, remove_mock):
        '''
        Test that delete_temp_client deletes the temporary client locally
        '''
        # Run test
        cloner = HsmCloner(**self.base_args)
        cloner.client_name = 'temp_client_time'
        cloner.delete_temp_client()
        # Verify
        assert_equals(remove_mock.call_args_list,
                      [call('/usr/safenet/lunaclient/cert/client/temp_client_time.pem'),
                       call('/usr/safenet/lunaclient/cert/client/temp_client_timeKey.pem')])

