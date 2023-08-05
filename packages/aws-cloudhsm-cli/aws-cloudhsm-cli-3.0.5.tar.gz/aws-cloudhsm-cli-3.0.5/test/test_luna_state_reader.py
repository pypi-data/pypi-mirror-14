
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
import unittest
from nose.tools import *
from mock import call, patch, MagicMock, Mock
import logging
 
from luna_reader.luna_state_reader import LunaStateReader 

class TestLunaStateReader(unittest.TestCase):
    @patch('luna_reader.luna_state_reader.LunaSshConnection')
    def test_creates_luna_ssh_connection_if_connection_not_supplied(self, conn_mock):
        '''
        Test that the reader creates a LunaSshConnection if a connection is not provided
        '''
        with patch.object(LunaStateReader, 'get_software_version', side_effect = ['5.1.3-1']) as mock_get_version:
            reader = LunaStateReader('address', 'prov')

            assert_equal(conn_mock.call_args_list,
                         [call('prov', 'address')])

    def test_correctly_matches_adapter_to_hsm_software_version(self):
        '''
        Test that the reader uses the correct adapter for the detected HSM software version
        '''
        with patch.object(LunaStateReader, 'get_software_version', side_effect = ['5.1.3-1', '5.3.0-11', '5.4.7-13']) as mock_get_version:
            luna_reader_a = LunaStateReader(connection=MagicMock())
            luna_reader_b = LunaStateReader(connection=MagicMock())
            luna_reader_c = LunaStateReader(connection=MagicMock())
            
            assert_equals(
                luna_reader_a.adapter.__class__.__name__,
                'LunaReadingAdapter'
            )
            assert_equals(
                luna_reader_b.adapter.__class__.__name__,
                'LunaReadingAdapter53'
            )
            assert_equals(
                luna_reader_c.adapter.__class__.__name__,
                'LunaReadingAdapter54'
            )
                     
    def test_calls_adapter_methods_correctly(self):
        '''
        Test that the reader calls its adapter's methods as expected
        '''
        mock_adapter = MagicMock()
        
        methods_to_check = [item for item in inspect.getmembers(LunaStateReader, predicate=inspect.ismethod) if item[0][0]!='_']

        with patch.object(LunaStateReader, '_set_adapter') as mock_set_adapter:
            luna_reader = LunaStateReader(connection=MagicMock())
            luna_reader.adapter = mock_adapter
            
            for method in methods_to_check:
                method_name = method[0]
                function = method[1]
                num_args = len(inspect.getargspec(function)[0]) - 1
                mocks = [Mock() for i in xrange(num_args)]

                state_reader_method = getattr(luna_reader, method_name)
                adapter_method = getattr(luna_reader.adapter, method_name)
        
                state_reader_method(*mocks)
                
                assert_equals(adapter_method.call_args_list,
                              [call(*mocks)])

