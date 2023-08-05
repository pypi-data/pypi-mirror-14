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

from nose.tools import raises, nottest, assert_equals, assert_true, assert_false
from mock import patch, Mock, mock_open, call
from unittest import TestCase
from cloudhsmcli.parser import CloudHSMCLI

@patch('cloudhsmcli.parser.dispatch')
@patch('cloudhsmcli.parser.ConfigParser')
@patch('cloudhsmcli.parser.argparse.ArgumentParser')
class TestParser(TestCase):
    def test_parser_calls_dispatch_function_with_same_name_as_command(self, mock_arg_parser, mock_config_parser, mock_dispatch):
        '''
        Test that parser calls the dispatch method with the same name as the command (underscores subbed for hyphens)
        '''
        mock_parser = Mock()
        mock_opts = Mock()
        mock_opts.command = 'test-command'
        mock_parser.parse_args.return_value = mock_opts
        mock_parser.parse_known_args.return_value = Mock(), Mock()
        mock_arg_parser.return_value = mock_parser

        cli = CloudHSMCLI()
        cli.run()

        assert_true(mock_dispatch.test_command.called)

    def test_parser_passes_args_to_dispatch_function(self, mock_arg_parser, mock_config_parser, mock_dispatch):
        '''
        Test that parser passes its args to the dispatch method with the same name as the command (underscores subbed for hyphens)
        '''
        mock_parser = Mock()
        mock_opts = Mock()
        mock_opts.command = 'test-command'
        mock_opts.test_arg_1 = 'test_arg_1'
        mock_opts.test_arg_2 = 'test_arg_2'
        mock_parser.parse_args.return_value = mock_opts
        mock_parser.parse_known_args.return_value = Mock(), Mock()
        mock_arg_parser.return_value = mock_parser

        cli = CloudHSMCLI()
        cli.run()
        
        assert_equals(
            mock_dispatch.test_command.call_args[1]['test_arg_1'],
            'test_arg_1'
            )

        assert_equals(
            mock_dispatch.test_command.call_args[1]['test_arg_2'],
            'test_arg_2'
            )

    def test_parser_reads_config_file_when_available(self, mock_arg_parser, mock_config_parser, mock_dispatch):
        '''
        Test that the parser reads values from a config file into its defaults dict
        '''
        mock_parser = Mock()
        mock_opts = Mock()
        mock_opts.command = 'test-command'
        mock_parser.parse_args.return_value = mock_opts
        conf_file_arg_parser_opts = Mock()
        conf_file_arg_parser_opts.conf_file = 'fake_path'
        mock_parser.parse_known_args.return_value = conf_file_arg_parser_opts, Mock()
        mock_arg_parser.return_value = mock_parser

        mock_cfg_file_parser = Mock()
        mock_cfg_file_parser.sections.return_value = ['cloudhsmcli', 'arn:aws:cloudhsm:us-east-1:123456789012:hsm-asdfasdf']
        mock_cfg_file_parser.items.side_effect = [[('key_1', 'value_1'), ('key_1a', 'value_1a')], [('ssh_key_filename', 'ssh_key')]]
        mock_config_parser.SafeConfigParser.return_value = mock_cfg_file_parser

        cli = CloudHSMCLI()
        cli.run()

        assert_equals(
            cli.defaults,
            {'key_1': 'value_1', 'key_1a': 'value_1a', 'ssh_key_filename': 'ssh_key'}
            )
        mock_cfg_file_parser.items.assert_any_call('cloudhsmcli')

