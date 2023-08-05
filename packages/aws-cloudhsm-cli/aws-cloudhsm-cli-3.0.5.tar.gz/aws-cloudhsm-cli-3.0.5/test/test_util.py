from nose.tools import raises, nottest, assert_equals
from mock import patch, Mock, mock_open, call, ANY
from unittest import TestCase
import cloudhsmcli.util as util
from io import BytesIO
from scraps import hsm_ips, group_partition_serials
from os import path

@patch('cloudhsmcli.util.sys.stdout', new_callable=BytesIO)
class TestWriteToFile(TestCase):
    def test_write_to_file_normal_case(self, stdout):
        '''
        Test that write_to_file writes data to a file properly.
        '''
        # Test
        opener = mock_open()
        with patch('__builtin__.open', opener):
            util.write_to_file(path='/tmp/test.conf', data='fake-data')
        # Verify
        self.assertEquals(opener.mock_calls, [call('/tmp/test.conf', 'w'), call().__enter__(), call().write('fake-data'), call().__exit__(None, None, None)])

@patch('cloudhsmcli.util.os.path.isfile')
@patch('cloudhsmcli.util.os.remove')
@patch('cloudhsmcli.util.os.rename')
class TestMoveFile(TestCase):
    def test_move_a_file_normal_case(self, rename_mock, remove_mock, isfile_mock):
        '''
        Test that move_a_file moves the file from source to dest properly.
        '''
        # Test
        isfile_mock.return_value = False
        util.move_a_file(source='/tmp/source.conf', dest='/tmp/dest.conf')
        # Verify
        assert_equals(remove_mock.call_count, 0)
        assert_equals(rename_mock.call_count, 0)

        # Test
        isfile_mock.return_value = True
        util.move_a_file(source='/tmp/source.cert', dest='/tmp/dest.cert')
        # Verify
        assert_equals(remove_mock.call_args_list,
                      [call('/tmp/dest.cert')])
        assert_equals(rename_mock.call_args_list,
                      [call('/tmp/source.cert', '/tmp/dest.cert')])

@patch('cloudhsmcli.util.sys.stdout', new_callable=BytesIO)
class TestConcatenateFiles(TestCase):
    def test_concatenate_files_normal_case(self, stdout):
        '''
        Test that concatenate_files appends the data of a file to another properly.
        '''
        # Test
        opener = mock_open()
        with patch('__builtin__.open', opener):
            util.concatenate_files(source='/tmp/server.pem', dest='/cert/server.pem')
        # Verify
        self.assertEquals(opener.mock_calls, [call('/tmp/server.pem', 'r'), call().__enter__(), call('/cert/server.pem', 'a'), call().__enter__(),
                                              call().readlines(), call().writelines(ANY), call().__exit__(None, None, None), call().__exit__(None, None, None)])

@patch('cloudhsmcli.util.os.path.isdir')
class TestFindLunaDir(TestCase):
    def test_find_luna_dir_normal_case(self, isdir_mock):
        '''
        Test that find_luna_dir returns the directories properly.
        '''
        # Test
        isdir_mock.return_value = True
        luna_dir_1 = util.find_luna_dir()
        # Verify
        assert_equals(luna_dir_1, '/usr/safenet/lunaclient')

        # Test
        isdir_mock.side_effect = [False, True]
        luna_dir_2 = util.find_luna_dir()
        # Verify
        assert_equals(luna_dir_2, '/usr/lunasa')

class TestScpFile(TestCase):
    @patch('cloudhsmcli.util.subprocess.Popen')
    def test_perform_scp_operation(self, mock_popen):
        """ Test that perform_scp behaves correctly when the scp operation succeeds.
        """
        mock_popen.return_value.returncode = 0
        mock_popen.return_value.communicate.return_value = ('server.pem    100% 1176     1.2KB/s   00:00', None)
        util._perform_scp_operation(["hostname:source", "dest"], None)
        mock_popen.assert_called_once_with(["scp", "-o", "StrictHostKeyChecking=no",
                                                   "-o", "UserKnownHostsFile=/dev/null",
                                                   "hostname:source","dest"],stdout=-1,
                                                   stderr=-1)

    @patch('cloudhsmcli.util._perform_scp_operation')
    def test_scp_file_to_remote_destination(self, _perform_scp_operation):
        """ Test that scp_file_to_remote_destination performs the correct scp
        command.
        """
        util.scp_file_to_remote_destination("hostname", "source_path", "destination_path")
        _perform_scp_operation.assert_called_once_with(
            ["source_path", "hostname:destination_path"], None)

    @patch('cloudhsmcli.util._perform_scp_operation')
    def test_scp_file_from_remote_source(self, _perform_scp_operation):
        """Test that scp_file_from_remote_source performs the correct scp
        command.
        """
        util.scp_file_from_remote_source("hostname", "source_path", "destination_path")
        _perform_scp_operation.assert_called_once_with(
            ["hostname:source_path", "destination_path"], None)

class TestRebuildCert(TestCase):
    def test_rebuild_cert_normal_case(self):
        '''
        Test that rebuild_cert returns the directories properly.
        '''
        # Test
        rebuilt = util.rebuild_cert('-----BEGIN CERTIFICATE-----\n\r' + '01234\r567' * 24 + "\n\r\n\r-----END CERTIFICATE-----\n\r")
        assert_equals(rebuilt, '-----BEGIN CERTIFICATE-----\n' + ('01234567' * 8 + '\n') * 3 + '-----END CERTIFICATE-----\n')

here = path.abspath(path.dirname(__file__))

@patch('cloudhsmcli.util.random')
class TestGenerateLuna51Config(TestCase):
    def test_generate_luna_51_config_normal_case(self, rand_mock):
        '''
        Test that generate_luna_51_config returns the config file properly.
        '''
        # Test
        rand_mock.randint.side_effect = [12, 34567, 987654321]
        config_file = util.generate_luna_51_config('unit-test-client-1', hsm_ips, group_partition_serials)
        # Verify
        with open(path.join(here, 'sample-Chrystoki-1.conf'), 'r') as f:
            test_config_file = f.read()

        assert_equals(config_file, test_config_file)

@patch('cloudhsmcli.util.random')
class TestGenerateLuna53Config(TestCase):
    def test_generate_luna_53_config_normal_case(self, rand_mock):
        '''
        Test that generate_luna_53_config returns the config file properly.
        '''
        # Test
        rand_mock.randint.side_effect = [1234567890, 9876, 543210]
        config_file = util.generate_luna_53_config('unit-test-client-3', hsm_ips, group_partition_serials)
        # Verify
        with open(path.join(here, 'sample-Chrystoki-3.conf'), 'r') as f:
            test_config_file = f.read()

        assert_equals(config_file, test_config_file)
