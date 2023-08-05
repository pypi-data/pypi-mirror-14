
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

import inspect 
from luna_device_connections.exceptions import HsmNotInitializedException
from luna_manipulator.luna_appliance_manipulator import LunaApplianceManipulator 
from mock import call, patch, MagicMock, Mock
from nose.tools import *
import unittest

class TestLunaApplianceManipulator(unittest.TestCase):
    @patch('luna_manipulator.luna_appliance_manipulator.LunaStateReader')
    @patch('luna_manipulator.luna_appliance_manipulator.LunaSshConnection')
    def test_creates_luna_ssh_connection_if_connection_not_supplied(self, conn_mock, reader_mock):
        '''
        Test that the manipulator creates a LunaSshConnection if a connection is not provided
        '''
        reader_mock.return_value.get_software_version.side_effect = ['5.1.3-1', '5.3.0-11']
        
        manipulator = LunaApplianceManipulator('address', 'prov')

        assert_equal(conn_mock.call_args_list,
                     [call('prov', 'address')])

    @patch('luna_manipulator.luna_appliance_manipulator.LunaStateReader')
    def test_correctly_matches_adapter_to_hsm_software_version(self, reader_mock):
        '''
        Test that the manipulator uses the correct adapter for the detected HSM software version
        '''
        reader_mock.return_value.get_software_version.side_effect = [
            '5.1.3-1', '5.3.0-11', '5.4.7-13'
        ]

        luna_manipulator_a = LunaApplianceManipulator(connection=MagicMock())
        luna_manipulator_b = LunaApplianceManipulator(connection=MagicMock())
        luna_manipulator_c = LunaApplianceManipulator(connection=MagicMock())
        
        assert_equals(
            luna_manipulator_a.adapter.__class__.__name__,
            'LunaManipulatingAdapter'
        )
        assert_equals(
            luna_manipulator_b.adapter.__class__.__name__,
            'LunaManipulatingAdapter53'
        )
        assert_equals(
            luna_manipulator_c.adapter.__class__.__name__,
            'LunaManipulatingAdapter54'
        )
    
    @patch('luna_manipulator.luna_appliance_manipulator.LunaStateReader')
    def test_manipulator_uses_default_adapter_if_hsm_not_initialized_arg_passed(self, reader_mock):
        '''
        Test that the manipulator uses default adapter if hsm is not initialized
        '''

        luna_manipulator = LunaApplianceManipulator(connection=MagicMock(),
                                                    luna_is_initialized=False)
        assert_equals(0, reader_mock.call_count)
        assert_equals(
                      luna_manipulator.adapter.__class__.__name__,
                      'LunaManipulatingAdapter'
                     )
    @patch('luna_manipulator.luna_appliance_manipulator.LunaStateReader')
    def test_manipulator_uses_default_adapter_if_hsm_not_initialized(self, reader_mock):
        '''
        Test that the manipulator uses default adapter if hsm is not initialized
        '''
        connection = MagicMock()
        connection.connect.side_effect = HsmNotInitializedException
        luna_manipulator = LunaApplianceManipulator(connection=connection)
        assert_equals(0, reader_mock.call_count)
        assert_equals(
            'LunaManipulatingAdapter',
            luna_manipulator.adapter.__class__.__name__
        )
                          
    @patch('luna_manipulator.luna_appliance_manipulator.LunaStateReader')
    def test_uses_default_adapter_if_finds_unknown_hsm_software_version(self, reader_mock):
        '''
        Test that the manipulator uses default adapter 
        if it finds an unsupported HSM software version
        '''
        reader_mock.return_value.get_software_version.return_value = 'bogus.version'
        luna_manipulator = LunaApplianceManipulator(connection=MagicMock())
        assert_equals(
            'LunaManipulatingAdapter',
            luna_manipulator.adapter.__class__.__name__
        )

    def test_calls_adapter_methods_correctly(self):
        '''
        Test that the manipulator calls its adapter's methods as expected
        '''
        mock_adapter = MagicMock()
        
        methods_to_check = [item for item in inspect.getmembers(LunaApplianceManipulator, predicate=inspect.ismethod) if item[0][0]!='_']
        
        with patch.object(LunaApplianceManipulator, '_set_adapter') as mock_set_adapter:
            luna_manipulator = LunaApplianceManipulator(connection=MagicMock())
            luna_manipulator.adapter = mock_adapter
            
            for method in methods_to_check:
                method_name = method[0]
                function = method[1]
                num_args = len(inspect.getargspec(function)[0]) - 1
                mocks = [Mock() for i in xrange(num_args)]
                
                appliance_manipulator_method = getattr(luna_manipulator, method_name)
                adapter_method = getattr(luna_manipulator.adapter, method_name)
                
                appliance_manipulator_method(*mocks)
                
                assert_equals(adapter_method.call_args_list,
                              [call(*mocks)]) 
