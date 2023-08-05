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
from mock import patch, Mock, mock_open, call
from unittest import TestCase
import cloudhsmcli.api as api
from datetime import datetime
from boto.provider import Provider
from boto.exception import BotoServerError, NoAuthHandlerFound
import json
from scraps import hsm_description, hapg_description, client_description

def get_unit_connection(**kw):
    '''
    We pass a provider object in so that the authentication objects think
    we're configured correctly.
    '''
    prov = Provider('aws', access_key='fake_key', secret_key='fake_secret')
    return api.CloudHsmConnection(region='fake_region', host='fake-host',
                                  provider=prov, **kw)

@patch('cloudhsmcli.api.AWSAuthConnection.__setattr__')
@patch('cloudhsmcli.api.AWSAuthConnection.__init__', return_value=None)
class TestInit(TestCase):
    def test_init_normal(self, init, setter):
        '''
        Check that CloudHsmConnection.__init__ handles normal case.
        '''
        connection = api.CloudHsmConnection(region='fake_region', fake_arg1='foo',
                                            fake_arg2='bar')
        init.assert_called_once_with(fake_arg1='foo', fake_arg2='bar')
        self.assertEquals([call('auth_service_name', 'cloudhsm'),
                            call('auth_region_name', 'fake_region')],
                          setter.call_args_list)

    def test_init_no_region(self, init, setter):
        '''
        Check that CloudHsmConnection.__init__ handles no region.
        '''
        connection = api.CloudHsmConnection(fake_arg1='foo', fake_arg2='bar')
        init.assert_called_once_with(fake_arg1='foo', fake_arg2='bar')
        self.assertFalse(setter.called)

    @raises(NoAuthHandlerFound)
    def test_init_reraises_noauthhandlerfound(self, init, setter):
        '''
        Check that CloudHsmConnection.__init__ reraises a NoAuthHandlerFound exception.
        '''
        expected = NoAuthHandlerFound('No authentication handler found.')
        init.side_effect = expected
        try:
            api.CloudHsmConnection(fake_arg1='foo', fake_arg2='bar')
        except NoAuthHandlerFound as actual:
            self.assertIs(expected, actual)
            self.assertEquals('Problem configuring access to CloudHSM API: No authentication handler found.',
                              actual.message)
            raise actual

class MockResponse(object):
    def __init__(self, status, payload=None, headers=None, **kw):
        self.status = status
        if payload is not None:
            self._payload = payload
        else:
            self._payload = json.dumps(kw)
        if headers is None:
            self._headers = { 'x-amzn-requestid': 'fake_id'}
        else:
            self._headers = headers
        self._closed = False
    def getheader(self, hdr):
        return self._headers.get(hdr)
    def getheaders(self):
        hdrs = self._headers.items()
        hdrs.sort()
        return hdrs
    def read(self):
        if self._closed:
            raise IOError("Can't read, closed")
        out = self._payload
        self._payload = ''
        return out
    def close(self):
        self._closed = True

class TestConnection(TestCase):
    def test_gets_hmacv4(self):
        '''
        Test that we're correctly requesting an authorization handler with hmac-v4 capability.

        This tests the _required_auth_capability override, but it's behavioral; we don't
        care exactly how it's done, that just seems the simplest method.
        '''
        connection = get_unit_connection()
        self.assertIn('hmac-v4', connection._auth_handler.capability)

    def test_rpcv1_request_with_payload(self):
        '''
        Test that rpcv1 decorates the request correctly.
        '''
        payload = {'fake_request': [1, 2, 3, 4]}
        obj = get_unit_connection()
        obj.make_request = Mock(return_value="check_return")
        returned = obj.rpcv1_request('FakeOp', payload=payload, fake_kw=1)
        self.assertEquals(returned, "check_return")
        obj.make_request.assert_called_once_with(method='POST', path='/', headers={
            'Accept': 'application/json',
            'Content-Encoding': 'amz-1.0',
            'Content-Type': 'application/json',
            'X-Amz-Target': 'com.amazonaws.cloudhsm.CloudHsmFrontendService.FakeOp'
        }, data='{"fake_request": [1, 2, 3, 4]}', fake_kw=1)

    def test_rpcv1_request_with_no_payload(self):
        '''
        Test that rpcv1 decorates the request correctly when there is no payload.
        '''
        operation = 'FakeOp'
        make_request = Mock(return_value="check_return")
        obj = get_unit_connection(path='/')
        obj.make_request = Mock(return_value="check_return")
        returned = obj.rpcv1_request(operation, fake_kw=1)
        self.assertEquals(returned, "check_return")
        obj.make_request.assert_called_once_with(method='POST', path='/', headers={
            'Accept': 'application/json',
            'Content-Encoding': 'amz-1.0',
            'Content-Type': 'application/json',
            'X-Amz-Target': 'com.amazonaws.cloudhsm.CloudHsmFrontendService.FakeOp'
        }, data='', fake_kw=1)

    def test_rpcv1_unpack_ok(self):
        '''
        Test that we unpack a normal response correctly.
        '''
        response = MockResponse(200, arg=[1, 2, 3])
        conn = get_unit_connection()
        result = conn.rpcv1_unpack(response)
        self.assertEquals(result, { u'arg': [1, 2, 3],
                                    u'RequestId': 'fake_id' })
        self.assertTrue(response._closed, "didn't close the response obejct")

    def test_rpcv1_unpack_blank(self):
        '''
        Test that we unpack a response with an empty payload correctly.
        '''
        response = MockResponse(200, payload='')
        conn = get_unit_connection()
        result = conn.rpcv1_unpack(response)
        self.assertEquals(result, { u'RequestId': 'fake_id' })
        self.assertTrue(response._closed, "didn't close the response obejct")


    @raises(ValueError)
    @patch('cloudhsmcli.api.interpret_error_response')
    def test_rpcv1_unpack_error_response(self, interpret):
        '''
        Test that we unpack a non-200 response correctly.
        '''
        response = MockResponse(400, message="You did something wrong")
        interpret.return_value = ValueError()
        conn = get_unit_connection()
        try:
            result = conn.rpcv1_unpack(response)
        finally:
            interpret.assert_called_once_with(400, {u"message": u"You did something wrong"})
            self.assertTrue(response._closed, "didn't close the response obejct")

    @patch.dict(api.ENDPOINTS, fake_region=dict(arg1=1, arg2=2))
    def test_region_defaults(self):
        '''
        Test that region_defaults makes a copy from ENDPOINTS.

        We aren't guaranteeing it's a deep copy, though.
        '''
        actual = api.region_defaults('fake_region')
        self.assertIsNot(actual, api.ENDPOINTS['fake_region'], 'region_defaults is returning original dict rather than copy')
        self.assertEquals(actual, api.ENDPOINTS['fake_region'])

    @raises(RuntimeError)
    def test_unsupported_region(self):
        '''
        Test that a meaningful output is displayed when an unsupported region is specified
        '''
        actual = api.region_defaults('fake-region')
        self.assertEquals(actual, 'The region you specified is currently unsupported')

    @patch('cloudhsmcli.api.CloudHsmConnection')
    def test_connect(self, Connection):
        '''
        Test that connect looks up defaults and allows user overrides.
        '''
        actual = api.connect('ap-southeast-2', path='/override')
        self.assertEquals(actual, Connection.return_value)
        Connection.assert_called_once_with(is_secure=True, path='/override',
                                        host='cloudhsm.ap-southeast-2.amazonaws.com',
                                        region='ap-southeast-2')

    @patch('cloudhsmcli.api.CloudHsmConnection')
    def test_connect_with_host_override(self, Connection):
        '''
        Test that connect does not look up defaults when user provides host override.
        '''
        actual = api.connect('ap-northwest-2', host='fake-host.amazon.com')
        self.assertEquals(actual, Connection.return_value)
        Connection.assert_called_once_with(host='fake-host.amazon.com',
                                        region='ap-northwest-2')

mock_error_codes = [] # Python evaluates @patch immediately; this is fully defined at end of file.

@patch('cloudhsmcli.api.ERRORCODES', mock_error_codes)
class TestInterpretErrorResponse(TestCase):
    def test_match_direct(self):
        '''
        Test interpret error codes matches a direct value.
        '''
        actual = api.interpret_error_response(400, {})
        self.assertIs(type(actual), RuntimeError)
        self.assertEquals(actual.message, "400.")

    def test_match_gets_payload_message(self):
        '''
        Test interpret error codes matches a direct value, and keeps the payload message.
        '''
        actual = api.interpret_error_response(402, { "message": "Payload message."})
        self.assertIs(type(actual), ValueError)
        self.assertEquals(actual.message, "402; Payload message.")

    def test_match_overlapping(self):
        '''
        Test interpret error codes allows later cases to overlap correctly.
        '''
        actual = api.interpret_error_response(401, {})
        self.assertIs(type(actual), RuntimeError)
        self.assertEquals(actual.message, "400 - 499.")

    def test_match_default(self):
        '''
        Test interpret error codes handles default
        '''
        actual = api.interpret_error_response(42, {})
        self.assertIs(type(actual), RuntimeError)
        self.assertEquals(actual.message, "Default.")

class TestInterpretErrorResponse2(TestCase):
    @patch('cloudhsmcli.api.ERRORCODES', [])
    def test_interpret_error_response_fallback_fallback(self):
        actual = api.interpret_error_response(42, { "message": "Payload message."})
        self.assertIs(type(actual), RuntimeError)
        self.assertEquals(actual.message, "Unexpected error; Payload message.")

    def test_sanity_of_real_error_codes(self):
        '''
        Check that errorcodes.json isn't broken.
        '''
        count = 0
        for handler in api.ERRORCODES:
            self.assertIsInstance(handler["message"], (str, unicode))
            self.assertTrue(handler["message"])
            self.assertFalse(handler["message"].endswith("."))
            self.assertIsInstance(handler.get("default", False), bool)
            self.assertIsInstance(handler.get("user", False), bool)
            if handler.get("default"):
                break
            count += 1
            if "type" in handler:
                self.assertIsInstance(handler["type"], (str, unicode))
                continue
            start, stop = handler["start"], handler["stop"]
            self.assertIsInstance(start, int)
            self.assertIsInstance(stop, int)
            self.assertTrue(stop >= start)
        self.assertTrue(count >= 3)

@patch('cloudhsmcli.api.CloudHsmConnection.rpcv1_request')
class TestApiCalls(TestCase):
    def test_list_hsms(self, rpcv1_request):
        '''
        Test that list_hsms makes a ListHsms call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, HsmList=["arn:fake", "arn:fake"])
        conn = get_unit_connection()
        actual = conn.list_hsms()
        self.assertEquals(actual, { u'HsmList': [u"arn:fake", u"arn:fake"],
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with("ListHsms", {})

    def test_list_hapgs(self, rpcv1_request):
        '''
        Test that list_hapgs makes a ListHsms call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, HapgList=["arn:fake", "arn:fake"])
        conn = get_unit_connection()
        actual = conn.list_hapgs()
        self.assertEquals(actual, { u'HapgList': [u"arn:fake", u"arn:fake"],
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with("ListHapgs", {})

    def test_list_clients(self, rpcv1_request):
        '''
        Test that list_clients makes a ListLunaClients call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, ClientList=["arn:fake", "arn:fake"])
        conn = get_unit_connection()
        actual = conn.list_clients()
        self.assertEquals(actual, { u'ClientList': [u"arn:fake", u"arn:fake"],
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with("ListLunaClients", {})

    def test_list_tags_for_resource(self, rpcv1_request):
        '''
        Test that list_tags_for_resource makes a ListTagsForResource call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, Status="successful"
        )
        # Test
        conn = get_unit_connection()
        actual = conn.list_tags_for_resource('arn:fake')
        self.assertEquals(actual, { u'Status': u"successful",
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with(
            "ListTagsForResource", 
            {'ResourceArn': "arn:fake"}
        )

    def test_describe_hsm(self, rpcv1_request):
        '''
        Test that describe_hsms makes a DescribeHsms call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, **hsm_description)
        expected = hsm_description.copy()
        expected['RequestId'] = "fake_id"
        hsm_arn=hsm_description["HsmArn"]
        # Test
        conn = get_unit_connection()
        actual = conn.describe_hsm(hsm_arn=hsm_arn)
        self.assertEquals(actual, expected)
        rpcv1_request.assert_called_once_with(
            "DescribeHsm", {'HsmArn': hsm_arn})

    def test_describe_hapg(self, rpcv1_request):
        '''
        Test that describe_hapg makes a DescribeHapg call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, **hapg_description)
        expected = hapg_description.copy()
        expected['RequestId'] = "fake_id"
        hapg_arn=hapg_description["HapgArn"]
        # Test
        conn = get_unit_connection()
        actual = conn.describe_hapg(hapg_arn=hapg_arn)
        self.assertEquals(actual, expected)
        rpcv1_request.assert_called_once_with(
            "DescribeHapg", {'HapgArn': hapg_arn})

    def test_describe_client(self, rpcv1_request):
        '''
        Test that describe_client makes a DescribeLunaClient call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, **client_description)
        expected = client_description.copy()
        expected['RequestId'] = "fake_id"
        client_arn=client_description["ClientArn"]
        # Test
        conn = get_unit_connection()
        actual = conn.describe_client(client_arn=client_arn)
        self.assertEquals(actual, expected)
        rpcv1_request.assert_called_once_with(
            "DescribeLunaClient", {'ClientArn': client_arn})

    def test_describe_client_fingerprint(self, rpcv1_request):
        '''
        Test that describe_client makes a DescribeLunaClient call with a fingerprint.
        '''
        rpcv1_request.return_value = MockResponse(
            200, **client_description)
        expected = client_description.copy()
        expected['RequestId'] = "fake_id"
        fingerprint="mock fingerprint"
        # Test
        conn = get_unit_connection()
        actual = conn.describe_client(fingerprint=fingerprint)
        self.assertEquals(actual, expected)
        rpcv1_request.assert_called_once_with(
            "DescribeLunaClient", {'CertificateFingerprint': fingerprint})

    def test_add_tag_to_resource(self, rpcv1_request):
        '''
        Test that add_tag_to_resource makes a AddTagsToResource call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, Status="successful"
        )
        # Test
        conn = get_unit_connection()
        actual = conn.add_tag_to_resource('arn:fake', 'key', 'value')
        self.assertEquals(actual, { u'Status': u"successful",
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with(
            "AddTagsToResource", 
            {
                'ResourceArn': "arn:fake",
                'TagList': [{
                    'Key': 'key',
                    'Value': 'value'
                }]
            }
        )

    @patch('cloudhsmcli.api.uuid.uuid4', Mock(return_value=Mock(hex='fake_uuid')))
    def test_create_hsm_no_client_token(self, rpcv1_request):
        '''
        Test that create_hsm makes a CreateHsm call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, HsmArn="arn:fake")
        conn = get_unit_connection()
        actual = conn.create_hsm(subnet_id='subnet-1234', ssh_public_key='public_key.pem',
                                 iam_role_arn='arn:iam_role')
        self.assertEquals(actual, { u'HsmArn': u"arn:fake",
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with(
            "CreateHsm", {
                'SshKey': 'public_key.pem', 'SubscriptionType': 'PRODUCTION',
                'IamRoleArn': 'arn:iam_role', 'ClientToken': 'fake_uuid',
                'SubnetId': 'subnet-1234', 'FipsCertified': False, 'HsmSoftwareVersion': '5.3.5'})

    def test_create_hsm_all_args(self, rpcv1_request):
        '''
        Test that create_hsm makes a CreateHsm call with optional args specified.
        '''
        rpcv1_request.return_value = MockResponse(
            200, HsmArn="arn:fake")
        conn = get_unit_connection()
        actual = conn.create_hsm(subnet_id='subnet-1234', ssh_public_key='public_key.pem',
                                 iam_role_arn='arn:iam_role', hsm_ip='1.2.3.4', external_id='ext_id',
                                 client_token='banana', syslog_ip='4.3.2.1', fips_certified=False, software_version='5.1.5')
        self.assertEquals(actual, { u'HsmArn': u"arn:fake",
                                    u'RequestId': u"fake_id" })
        rpcv1_request.assert_called_once_with("CreateHsm", {
            'SshKey': 'public_key.pem', 'SubscriptionType': 'PRODUCTION',
            'IamRoleArn': 'arn:iam_role', 'EniIp': '1.2.3.4', 'ExternalId': 'ext_id',
            'ClientToken': 'banana', 'SubnetId': 'subnet-1234', 'SyslogIp':
            '4.3.2.1', 'FipsCertified': False, 'HsmSoftwareVersion': '5.1.5'})

    def test_create_hapg(self, rpcv1_request):
        '''
        Test that create_hapg makes a CreateHapg call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, HapgArn="arn:fake")
        conn = get_unit_connection()
        actual = conn.create_hapg('my_label')
        self.assertEquals(actual, { u'HapgArn': u"arn:fake",
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with("CreateHapg",
                                              {"Label": "my_label"})

    def test_delete_hapg(self, rpcv1_request):
        '''
        Test that delete_hapg makes a DeleteHapg call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, Status="successful")
        # Test
        conn = get_unit_connection()
        actual = conn.delete_hapg('arn:fake')
        self.assertEquals(actual, { u'Status': u"successful",
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with(
            "DeleteHapg", {'HapgArn': "arn:fake"})

    def test_delete_hsm(self, rpcv1_request):
        '''
        Test that delete_hsm makes a DeleteHsm call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, Status="successful")
        # Test
        conn = get_unit_connection()
        actual = conn.delete_hsm('arn:fake')
        self.assertEquals(actual, { u'Status': u"successful",
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with(
            "DeleteHsm", {'HsmArn': "arn:fake"})

    def test_remove_tags_from_resource(self, rpcv1_request):
        '''
        Test that remove_tags_from_resource makes a RemoveTagsFromResource call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, Status="successful"
        )
        # Test
        conn = get_unit_connection()
        actual = conn.remove_tags_from_resource('arn:fake', ['key1', 'key2'])
        self.assertEquals(actual, { u'Status': u"successful",
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with(
            "RemoveTagsFromResource", 
            {
                'ResourceArn': "arn:fake",
                'TagKeyList': ['key1', 'key2']
            }
        )

    def test_create_client(self, rpcv1_request):
        '''
        Test that create_client makes a CreateLunaClient call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, ClientArn="arn:fake")
        conn = get_unit_connection()
        actual = conn.create_client('my_cert')
        self.assertEquals(actual, { u'ClientArn': u"arn:fake",
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with("CreateLunaClient",{"Certificate": "my_cert"})

    def test_delete_client(self, rpcv1_request):
        '''
        Test that delete_client makes a DeleteLunaClient call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, Status="successful")
        # Test
        conn = get_unit_connection()
        actual = conn.delete_client('arn:fake')
        self.assertEquals(actual, { u'Status': u"successful",
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with(
            "DeleteLunaClient", {'ClientArn': "arn:fake"})

    def test_modify_hapg_no_args(self, rpcv1_request):
        '''
        Test that modify_hapg makes a ModifyHapg call when only HapgArn provided.
        '''
        rpcv1_request.return_value = MockResponse(
            200, Status="successful")
        # Test
        conn = get_unit_connection()
        actual = conn.modify_hapg('arn:fake')
        self.assertEquals(actual, { u'Status': u"successful",
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with(
            "ModifyHapg", {'HapgArn': "arn:fake"})

    def test_modify_hapg_all_args(self, rpcv1_request):
        '''
        Test that modify_hapg makes a ModifyHapg call when all args provided.
        '''
        rpcv1_request.return_value = MockResponse(
            200, Status="successful")
        # Test
        conn = get_unit_connection()
        actual = conn.modify_hapg('arn:fake', label='label', partition_serial_list=[1,2,3,4])
        self.assertEquals(actual, { u'Status': u"successful",
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with(
            "ModifyHapg", {'HapgArn': "arn:fake", "Label": 'label', "PartitionSerialList": [1,2,3,4]})

    def test_modify_hsm(self, rpcv1_request):
        '''
        Test that modify_hsm makes a ModifyHsm call.
        '''
        rpcv1_request.return_value = MockResponse(
            200, Status="successful")
        # Test
        conn = get_unit_connection()
        actual = conn.modify_hsm('arn:fake', subnet_id='subnet', eni_ip='1.2.3.4', syslog_ip='2.3.4.5')
        self.assertEquals(actual, { u'Status': u"successful",
                                    u'RequestId': u"fake_id"})
        rpcv1_request.assert_called_once_with(
                "ModifyHsm", {'HsmArn': "arn:fake", "SubnetId": 'subnet', "EniIp": "1.2.3.4", "SyslogIp": "2.3.4.5"})

mock_error_codes.extend([
    {
        "start": 400,
        "stop": 400,
        "message": "Should never match",
        "user": True
    }, {
        "start": 400,
        "stop": 401,
        "message": "400"
    }, {
        "start": 402,
        "stop": 403,
        "message": "402",
        "user": True
    }, {
        "start": 400,
        "stop": 500,
        "message": "400 - 499"
    }, {
        "default": True,
        "message": "Default"
    }
])
