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
from mock import patch, Mock, mock_open, call, ANY
from unittest import TestCase
import cloudhsmcli.dispatch as dispatch
from io import BytesIO, StringIO
from scraps import hsm_description, hapg_description, client_description
import json
from device_connections.hsm_credential_provider import HsmCredentialProvider
import subprocess, mock

class TestLiftAwsArgs(TestCase):
    def test_lift_aws_args_normal_case(self):
        '''
        Test that _lift_aws_args works in the normal case.
        '''
        arg_map = { 'aws_region': 'fake_region',
                    'aws_access_key_id': 'fake_access',
                    'aws_secret_access_key': 'fake_secret',
                    'aws_host': 'fake_host',
                    'aws_port': '80',
                    'other_arg': 'some_value'
                }
        aws_specific = dispatch._lift_aws_args(arg_map)
        assert_equals(aws_specific, {
            'region': 'fake_region',
            'aws_access_key_id': 'fake_access',
            'aws_secret_access_key': 'fake_secret',
            'host': 'fake_host',
            'port': 80
        })
        assert_equals(arg_map, { 'other_arg': 'some_value' })

    @raises(KeyError)
    def test_lift_aws_args_no_region(self):
        '''
        Test that _lift_aws_args raises an error if no region.
        '''
        arg_map = { 'aws_access_key_id': 'fake_access',
                    'aws_secret_access_key': 'fake_secret',
                    'other_arg': 'some_value'
                }
        dispatch._lift_aws_args(arg_map)

    def test_lift_aws_args_no_access_secret(self):
        '''
        Test that _lift_aws_args handles missing optional args
        '''
        arg_map = { 'aws_region': 'fake_region',
                    'other_arg': 'some_value'
                }
        aws_specific = dispatch._lift_aws_args(arg_map)
        assert_equals(aws_specific, { 'region': 'fake_region' })
        assert_equals(arg_map, { 'other_arg': 'some_value' })

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
class TestPrettyPrint(TestCase):
    def test_pretty_print_normal_case(self, stdout):
        '''
        Test that _pretty_print prints prettily.
        '''
        dispatch._pretty_print({"a": 1, "b": 2})
        output = stdout.getvalue()
        assert_equals(output, '{\n    "a": 1, \n    "b": 2\n}\n')

def load_output(stdout):
    stdout.seek(0)
    return json.load(stdout)

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.HapgAdder')
class TestAddHsmToHapgCommand(TestCase):
    def test_add_hsm_to_hapg_normal_case(self, mock_adder, stdout):
        '''
        Test that the add_hsm_to_hapg command handles the normal case.
        '''
        expected = {"Status": "successful"}
        mock_adder.return_value.run.return_value = expected
        # Test
        dispatch.add_hsm_to_hapg(hapg_arn = 'hapg_arn', hsm_arn='hsm_arn', partition_password='partition_password', 
                                 cloning_domain='cloning_domain', ssh_username='username', so_password='so_password',
                                 ssh_key_filename='filename', aws_region='region')
        # Verify
        assert_equals(mock_adder.call_args_list,
                      [call( cloning_domain='cloning_domain', 
                            partition_password='partition_password', 
                            hsm_arn='hsm_arn', 
                            so_password='so_password', 
                            hapg_arn='hapg_arn', 
                            aws_creds={'region': 'region'})]
                     )
        output = load_output(stdout)
        assert_equals(output, expected)

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.api.connect')
class TestAddTagToResourceCommand(TestCase):
    def test_add_tag_normal_case(self, connect, stdout):
        '''
        Test that the add_tag_to_resource command handles the normal case.
        '''
        connect.return_value.add_tag_to_resource.return_value = {
            'RequestId': 'fake_id', 'Status': 'Successful'
        }
        # Test
        dispatch.add_tag_to_resource(
            resource_arn='arn:aws:clerdhsm:qe-westeast-42:123412341234:hsm-b0b',
            aws_region='fake-region', key='key', value='value'
        )
        # Verify
        connect.assert_called_once_with(region='fake-region')
        connect.return_value.add_tag_to_resource.assert_called_once_with(
            'arn:aws:clerdhsm:qe-westeast-42:123412341234:hsm-b0b',
            'key', 'value'
        )

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.HapgCloner')
class TestCloneHapgCommand(TestCase):
    def test_clone_hapg_normal_case(self, mock_cloner, stdout):
        '''
        Test that the clone_hapg command handles the normal case.
        '''
        expected = {"Status": "Cloning the HA partition group src_hapg_arn to the HA partition group dest_hapg_arn successful"}
        mock_cloner.return_value.run.return_value = expected
        # Test
        dispatch.clone_hapg(src_hapg_arn = 'src_hapg_arn', dest_hapg_arn='dest_hapg_arn', hapg_password='hapg_password',
                            override=True, aws_region='region')
        # Verify
        assert_equals(mock_cloner.call_args_list,
                      [call(src_hapg_arn='src_hapg_arn',
                            dest_hapg_arn='dest_hapg_arn',
                            hapg_password='hapg_password',
                            aws_creds={'region': 'region'})]
                     )
        output = load_output(stdout)
        assert_equals(output, expected)

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.HsmCloner')
class TestCloneHsmCommand(TestCase):
    def test_clone_hsm_normal_case(self, mock_cloner, stdout):
        '''
        Test that the clone_hsm command handles the normal case.
        '''
        expected = {"Status": "Cloning the HSM src_hsm_arn to the HSM dest_hsm_arn successful"}
        mock_cloner.return_value.run.return_value = expected
        # Test
        dispatch.clone_hsm(src_hsm_arn = 'src_hsm_arn', dest_hsm_arn='dest_hsm_arn', so_password='so_password',
                           override=True, aws_region='region')
        # Verify
        assert_equals(mock_cloner.call_args_list,
                      [call(src_hsm_arn='src_hsm_arn',
                            dest_hsm_arn='dest_hsm_arn',
                            so_password='so_password',
                            aws_creds={'region': 'region'})]
                     )
        output = load_output(stdout)
        assert_equals(output, expected)

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.api.connect')
class TestListHsmsCommand(TestCase):
    def test_list_hsms_normal_case(self, connect, stdout):
        '''
        Test that the list command handles the normal case.
        '''
        connect.return_value.list_hsms.return_value = {
            'HsmList': ["arn:fake", "arn:fake"],
            'RequestId': "fake_id"
        }
        # Test
        dispatch.list_hsms(aws_region='fake-region')
        # Verify
        connect.assert_called_once_with(region='fake-region')
        connect.return_value.list_hsms.assert_called_once_with()
        output = load_output(stdout)
        assert_equals(output, { "HsmList": ["arn:fake", "arn:fake"],
                                    "RequestId": "fake_id"})

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.api.connect')
class TestListTagsForResourceCommand(TestCase):
    def test_list_tags_normal_case(self, connect, stdout):
        '''
        Test that the list_tags_for_resource command handles the normal case.
        '''
        connect.return_value.list_tags_for_resource.return_value = {
            'RequestId': 'fake_id', 'ouput': 'list of tags'
        }
        # Test
        dispatch.list_tags_for_resource(
            resource_arn='arn:aws:cloudvolt:qe-westeast-42:123412341234:hsm-b0b',
            aws_region='fake-region'
        )
        # Verify
        connect.assert_called_once_with(region='fake-region')
        connect.return_value.list_tags_for_resource.assert_called_once_with(
            'arn:aws:cloudvolt:qe-westeast-42:123412341234:hsm-b0b'
        )

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.api.connect')
class TestDescribeHsmCommand(TestCase):
    def test_describe_hsm_normal_case(self, connect, stdout):
        '''
        Test that the describe_hsm command handles the normal case.
        '''
        # Somewhat realistic
        hsm = hsm_description.copy()
        hsm['RequestId'] = 'fake_id'
        connect.return_value.describe_hsm.return_value = hsm
        expected = hsm.copy()
        # Test
        dispatch.describe_hsm(aws_region='fake-region', hsm_arn='arn:aws:cloudhsm:qe-westeast-42:123412341234:hsm-b0b')
        # Verify
        connect.assert_called_once_with(region='fake-region')
        connect.return_value.describe_hsm.assert_called_once_with('arn:aws:cloudhsm:qe-westeast-42:123412341234:hsm-b0b')
        output = load_output(stdout)
        assert_equals(output, expected)

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.api.connect')
class TestDescribeClientCommand(TestCase):
    def test_describe_normal_case(self, connect, stdout):
        '''
        Test that the describe_client command handles the normal case.
        '''
        # Somewhat realistic
        client = client_description.copy()
        client['RequestId'] = 'fake_id'
        connect.return_value.describe_client.return_value = client
        expected = client.copy()
        # Test
        dispatch.describe_client(aws_region='fake-region', client_arn='arn:aws:cloudhsm:qe-westeast-42:123412341234:client-b0b')
        # Verify
        connect.assert_called_once_with(region='fake-region')
        connect.return_value.describe_client.assert_called_once_with('arn:aws:cloudhsm:qe-westeast-42:123412341234:client-b0b', None)
        output = load_output(stdout)
        assert_equals(output, expected)

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.api.connect')
class TestDescribeHapgCommand(TestCase):
    def test_describe_hapg_normal_case(self, connect, stdout):
        '''
        Test that the describe_hapg command handles the normal case.
        '''
        # Somewhat realistic
        hapg = hapg_description.copy()
        hapg['RequestId'] = 'fake_id'
        connect.return_value.describe_hapg.return_value = hapg
        expected = hapg.copy()
        # Test
        dispatch.describe_hapg(aws_region='fake-region', hapg_arn='arn:aws:cloudhsm:qe-westeast-42:123412341234:hapg-b0b')
        # Verify
        connect.assert_called_once_with(region='fake-region')
        connect.return_value.describe_hapg.assert_called_once_with('arn:aws:cloudhsm:qe-westeast-42:123412341234:hapg-b0b')
        output = load_output(stdout)
        assert_equals(output, expected)

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.HsmInitializer')
class TestInitializeHsm(TestCase):
    def test_initialize_hsm_runs(self, initializer, stdout):
        '''
        Test that initialize_hsm constructs an initializer correctly and runs it.
        '''
        initializer.return_value.run.return_value = {
            'Status': "Initialization of the HSM successful"
        }
        dispatch.initialize_hsm(hsm_arn='fake_arn', so_password='guest',
                                cloning_domain='domain', label='label',
                                aws_region='fake-region')
        # Verify
        initializer.assert_called_once_with(hsm_arn='fake_arn', so_password='guest',
                                cloning_domain='domain', label='label',
                                aws_creds={'region': 'fake-region'})
        output = load_output(stdout)
        assert_equals(output, {"Status": "Initialization of the HSM successful"})

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.api.connect')
class TestCreateHapgCommand(TestCase):
    def test_create_hapg_normal_case(self, connect, stdout):
        '''
        Test that the create_hapg command handles the normal case.
        '''
        # Somewhat realistic
        hapg_arn = {"hapg_arn": "arn"}
        connect.return_value.create_hapg.return_value = hapg_arn
        expected = hapg_arn.copy()
        # Test
        dispatch.create_hapg(aws_region='fake-region', group_label='label')
        # Verify
        connect.assert_called_once_with(region='fake-region')
        connect.return_value.create_hapg.assert_called_once_with('label')
        output = load_output(stdout)
        assert_equals(output, expected)


@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.api.connect')
class TestCreateHsm(TestCase):
    def test_create_hsm_production(self, connect, stdout):
        '''
        Test that the create_hsm command handles the normal production case.
        '''
        connect.return_value.create_hsm.return_value = {
            'HsmArn': "arn:fake",
            'RequestId': "fake_id"
        }
        f = Mock(spec=file)
        f.read.return_value = 'pem data'
        # Test
        with patch('__builtin__.raw_input', return_value='5000'):
            dispatch.create_hsm(aws_region='fake-region',
                                subnet_id='subnet_1234',
                                ssh_public_key_file=f,
                                iam_role_arn='arn:iam_role',
                                hsm_ip='1.2.3.4',
                                external_id='external',
                                syslog_ip='4.3.2.1')
            connect.assert_called_once_with(region='fake-region')
            connect.return_value.create_hsm.assert_called_once_with(
                subnet_id='subnet_1234', ssh_public_key='pem data',
                iam_role_arn='arn:iam_role', external_id='external',
                hsm_ip='1.2.3.4', syslog_ip='4.3.2.1', 
                fips_certified=False, software_version='5.3.5')

            stdout.seek(0)
            lines = stdout.readlines()
            # Search for the JSON blob
            json_index = lines.index('{\n')
            # Convert the list into a JSON object
            output = json.load(StringIO(u''.join(lines[json_index:])))
            assert_equals(output, {"HsmArn": "arn:fake",
                                   "RequestId": "fake_id"})

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.api.connect')
class TestModifyHsm(TestCase):
    def test_modify_hsm(self, connect, stdout):
        '''
        Test that the modify_hsm command handles the normal case.
        '''
        connect.return_value.modify_hsm.return_value = {
            'HsmArn': "arn:fake",
            'RequestId': "fake_id"
        }
        # Test
        dispatch.modify_hsm(hsm_arn="arn:fake",
                            aws_region='fake-region',
                            subnet_id='subnet_1234',
                            iam_role_arn='arn:iam_role',
                            hsm_ip='1.2.3.4',
                            external_id='external',
                            override=True)
 
        connect.assert_called_once_with(region='fake-region')
        connect.return_value.modify_hsm.assert_called_once_with(
               hsm_arn="arn:fake", 
               subnet_id='subnet_1234', 
               iam_role_arn='arn:iam_role', 
               external_id='external', 
               eni_ip='1.2.3.4',
               syslog_ip=None)
        output = load_output(stdout)
        assert_equals(output, {"HsmArn": "arn:fake",
                               "RequestId": "fake_id"})
            
@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.api.connect')
class TestCreateClientCommand(TestCase):
    def test_create_client_normal_case(self, connect, stdout):
        '''
        Test that the create_client command handles the normal case.
        '''
        connect.return_value.create_client.return_value = {
            'ClientArn': "arn:fake",
            'RequestId': "fake_id"
        }
        f = Mock(spec=file)
        f.read.return_value='pem data'
        # Test
        dispatch.create_client(aws_region='fake-region', certificate_file=f)
        # Verify
        connect.assert_called_once_with(region='fake-region')
        connect.return_value.create_client.assert_called_once_with('pem data')
        output = load_output(stdout)
        assert_equals(output, {
            "ClientArn": "arn:fake",
            "RequestId": "fake_id"})

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.api.connect')
class TestDeleteClientCommand(TestCase):
    def test_delete_normal_case(self, connect, stdout):
        '''
        Test that the delete_client command handles the normal case.
        '''
        client = client_description.copy()
        client['RequestId'] = 'fake_id'
        connect.return_value.describe_client.return_value = client
        connect.return_value.delete_client.return_value = {
            'Status': 'successful',
            'RequestId': 'fake_id'
        }
        # Test
        dispatch.delete_client(aws_region='fake-region', client_arn='arn:aws:cloudhsm:qe-westeast-42:123412341234:client-b0b')
        # Verify
        connect.assert_called_once_with(region='fake-region')
        connect.return_value.delete_client.assert_called_once_with('arn:aws:cloudhsm:qe-westeast-42:123412341234:client-b0b')
        output = load_output(stdout)
        assert_equals(output, {
            'Status': 'successful',
            'RequestId': 'fake_id'})

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.ClientDeregisterer')
class TestDeregisterClientFromHapgCommand(TestCase):
    def test_deregister_client_from_hapg_normal_case(self, mock_deregisterer, stdout):
        '''
        Test that the deregister_client_from_hapg command handles the normal case.
        '''
        expected = {"Status": "Deregistration of the client c1c to the HA partition group d2d successful"}
        mock_deregisterer.return_value.run.return_value = expected
        # Test
        dispatch.deregister_client_from_hapg(client_arn = 'client_arn', hapg_arn='hapg_arn', aws_region='region')
        # Verify
        assert_equals(mock_deregisterer.call_args_list,
                      [call(client_arn='client_arn',
                            hapg_arn='hapg_arn',
                            aws_creds={'region': 'region'})]
                     )
        output = load_output(stdout)
        assert_equals(output, expected)

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.api.connect')
@patch('cloudhsmcli.util.os.path.isdir', return_value=True)
@patch('cloudhsmcli.util.generate_luna_53_config')
@patch('cloudhsmcli.util.write_to_file')
@patch('cloudhsmcli.dispatch.HsmWorker')
class TestGetClientConfigurationCommand(TestCase):
    def test_get_client_configuration_normal_case(self, mock_worker, write_mock, gen_mock, dir_mock, connect, stdout):
        '''
        Test that the get_client_configuration command handles the normal case.
        '''
        # Set up the mocks
        connect.return_value.describe_hapg.side_effect = [{'Label': 'hapg1', 'PartitionSerialList': ['123456001', '234567002']},
                                                          {'Label': 'hapg2', 'PartitionSerialList': ['123456003', '234567004']}]
        connect.return_value.list_hsms.return_value = {'HsmList': ['arn:hsm1', 'arn:hsm2']}
        connect.return_value.describe_hsm.side_effect = [{'SerialNumber': '123456', 'EniIp': '1.2.3.4'},
                                                         {'SerialNumber': '234567', 'EniIp': '2.3.4.5'}]
        connect.return_value.describe_client.return_value = {'Label': 'testclient'}

        # Test
        dispatch.get_client_configuration(aws_region='fake-region',
                    client_arn='arn:client', hapg_arns = ['arn:hapg1', 'arn:hapg2'],
                    config_directory='/tmp', cert_directory='/tmp')
        # Verify
        assert_equals(gen_mock.call_args_list,
                      [call('testclient', ['1.2.3.4', '2.3.4.5'],
                            {'hapg1': ['123456001', '234567002'], 'hapg2': ['123456003', '234567004']})]
                     )
        assert_equals(write_mock.call_args_list,
                      [call('/tmp/Chrystoki.conf', ANY)]
                     )
        assert_equals(mock_worker.return_value.scp_server_cert_from_hsm.call_args_list,
                      [call('1.2.3.4', '/tmp/CAFile.pem'), call('2.3.4.5', '/tmp/CAFile.pem')]
                     )

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.ClientRegisterer')
class TestRegisterClientToHapgCommand(TestCase):
    def test_register_client_to_hapg_normal_case(self, mock_registerer, stdout):
        '''
        Test that the register_client_to_hapg command handles the normal case.
        '''
        expected = {"Status": "Registration of the client c1c to the HA partition group d2d successful"}
        mock_registerer.return_value.run.return_value = expected
        # Test
        dispatch.register_client_to_hapg(client_arn = 'client_arn', hapg_arn='hapg_arn', aws_region='region')
        # Verify
        assert_equals(mock_registerer.call_args_list,
                      [call(client_arn='client_arn',
                            hapg_arn='hapg_arn',
                            aws_creds={'region': 'region'})]
                     )
        output = load_output(stdout)
        assert_equals(output, expected)

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.HapgRemover')
class TestRemoveHsmFromHapgCommand(TestCase):
    def test_remove_hsm_from_hapg_normal_case(self, mock_remover, stdout):
        '''
        Test that the remove_hsm_from_hapg command handles the normal case.
        '''
        expected = {"Status": "successful"}
        mock_remover.return_value.run.return_value = expected
        # Test
        dispatch.remove_hsm_from_hapg(hapg_arn = 'hapg_arn', hsm_arn='hsm_arn', override=True, so_password='so_password', aws_region='region')

        # Verify
        assert_equals(mock_remover.call_args_list,
                      [call(hsm_arn='hsm_arn', 
                            so_password='so_password', 
                            hapg_arn='hapg_arn', 
                            aws_creds={'region': 'region'})]
                     )
        output = load_output(stdout)
        assert_equals(output, expected)

@patch('cloudhsmcli.dispatch.sys.stdout', new_callable=BytesIO)
@patch('cloudhsmcli.dispatch.api.connect')
class TestRemoveTagsFromResourceCommand(TestCase):
    def test_remove_tags_normal_case(self, connect, stdout):
        '''
        Test that the remove_tags_from_resource command handles the normal case.
        '''
        connect.return_value.remove_tags_from_resource.return_value = {
            'RequestId': 'fake_id', 'Status': 'Successful'
        }
        # Test
        dispatch.remove_tags_from_resource(
            resource_arn='arn:aws:clerdhsm:qe-westeast-42:123412341234:hsm-b0b',
            aws_region='fake-region', keys=['key1', 'key2']
        )
        # Verify
        connect.assert_called_once_with(region='fake-region')
        connect.return_value.remove_tags_from_resource.assert_called_once_with(
            'arn:aws:clerdhsm:qe-westeast-42:123412341234:hsm-b0b',
            ['key1', 'key2']
        )

class TestUserMessaging(TestCase):
    def test_align_message_works(self):
        message = """I touch the string, though the harp may not sing, still I dig the sky for sunspots to guide. Down below, there's a land
                     with an ominous hole dug deep in the sands of belief."""
        aligned = """I touch the string, though the harp may not sing, still I dig the sky for
sunspots to guide. Down below, there's a land with an ominous hole dug deep in
the sands of belief.""" 
        assert_equals(dispatch._align_message(message), aligned)
