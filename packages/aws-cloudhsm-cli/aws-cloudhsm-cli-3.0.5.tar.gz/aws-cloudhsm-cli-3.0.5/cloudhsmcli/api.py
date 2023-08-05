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


"""
This module provides an interface to perform API connections.
"""

from boto.connection import AWSAuthConnection
from boto.exception import BotoServerError, NoAuthHandlerFound
import json, logging, os.path, uuid

logger = logging.getLogger('cloudhsmcli.api')

class CloudHsmConnection(AWSAuthConnection):
    """
    A connection to a CloudHSM endpoint. We recommend using the connect
    method to look up the correct settings for you.
    """
    def __init__(self, **kw):
        region = kw.pop('region', None)
        try:
            super(CloudHsmConnection, self).__init__(**kw)
        except NoAuthHandlerFound as e:
            e.message = "Problem configuring access to CloudHSM API: " + e.message
            raise e
        if region:
            self.auth_service_name = 'cloudhsm'
            self.auth_region_name = region

    def _required_auth_capability(self):
        """
        An override to ensure that we use HMAC v4 signing.
        """
        return ['hmac-v4']

    def rpcv1_request(self, operation, payload=None, **kw):
        """
        Makes an RPCv1 request.

        The operation should be a FrontendService operation, and the payload
        should be a Python object that corresponds to the service model.

        Additional parameters are passed directly to make_request.

        :rtype: HttpResponse
        """
        if payload is None:
            data = ''
        else:
            data = json.dumps(payload)

        headers = {
            'Accept': 'application/json',
            'Content-Encoding': 'amz-1.0',
            'Content-Type': 'application/json',
            'X-Amz-Target': 'com.amazonaws.cloudhsm.CloudHsmFrontendService.'
                            + operation
        }

        return self.make_request(method='POST', path=self.path, headers=headers,
                                 data=data, **kw)

    def rpcv1_unpack(self, response):
        """
        Unpack the HttpResponse from an RPCv1 request.

        This will return a valid response, or raise exceptions for bad requests or internal server errors.
        It may also raise an exception if an underlying network request fails.

        :type response: HttpResponse

        :returns: unpacked JSON
        :rtype: dict
        """
        try:
            status = response.status
            request_id = response.getheader('x-amzn-requestid')
            try:
                payload = json.load(response)
            except ValueError:
                payload = {}
        finally:
            response.close()
        if 200 <= response.status < 300:
            payload['RequestId'] = request_id
            return payload
        else:
            raise interpret_error_response(response.status, payload)
    
    def add_tag_to_resource(self, resource_arn, key, value):
        """
        Perform the AddTagsToResource call and return the response.

        :param resource_arn: arn of the cloudhsm resource to add the tag to
        :type resource_arn: str that is a correctly formatted ARN

        :param key: tag key 
        :type key: str that is a correctly formatted tag key

        :param vale: tag value 
        :type key: str that is a correctly formatted tag value

        :returns: the api response
        :rtype: dict, e.g. {"Status": "Successfully added tag to resource."}
        """
        args = {
            "ResourceArn": resource_arn,
            "TagList": [{
                    "Key": key,
                    "Value": value
            }]   
        }
        response = self.rpcv1_request("AddTagsToResource", args)
        return self.rpcv1_unpack(response)

    def create_client(self, cert):
        """
        Perform the CreateLunaClient call and return the ARN of the client.

        :type label: str, matches /^[a-zA-Z_0-9]{1,64}$/

        :param cert: the certificate associated with the client
        :type cert: str, a valid X.509 v3 certificate

        :returns: the api response
        :rtype: dict, e.g. {"ClientArn": "arn:..."}
        """
        response = self.rpcv1_request("CreateLunaClient", {
            "Certificate": cert
        })
        return self.rpcv1_unpack(response)

    def create_hapg(self, label):
        """
        Perform the CreateHapg API call and return the ARN of
        the new high availability partition group.

        :param label: the label for the new hapg
        :type label: str, matches /^[a-zA-Z_0-9]{1,64}$/ (enforced by server)

        :returns: the api response, e.g. { 'HapgArn': 'arn:...' }
        :rtype: dict
        """
        response = self.rpcv1_request("CreateHapg", {"Label": label})
        return self.rpcv1_unpack(response)

    def create_hsm(self, subnet_id, ssh_public_key, iam_role_arn,
                   hsm_ip=None, external_id=None, client_token=None,
                   syslog_ip=None, fips_certified=False, software_version="5.3.5"):
        """
        Performs the CreateHsm API call. Returns immediately; use describe to inspect the progress.

        :param subnet_id: A subnet (from a VPC) in which to place the new HSM.
        :type subnet_id: str

        :param ssh_public_key: A public key to add as an authorized user for the manager account.
        :type ssh_public_key: str

        :param iam_role_arn: An ARN identifying an IAM role that will allow the CloudHSM service to construct the ENI for us.
        :type iam_role_arn: str (an Amazon Resource Name)

        :param hsm_ip: The desired IP address of the HSM. If we don't specify this, the service will pick one for us.
        :type hsm_ip: str (dotted quad)

        :param external_id: The external ID field of the IAM role, if applicable.
        :type external_id: str

        :param client_token: A nonce to allow retrying requests without creating duplicate HSMs.
        :type client_token: str
        
        :param syslog_ip: The IP address for the syslog monitoring server.
        :type client_token: str
        
        :param syslog_ip: The HSM software version to use.
        :type client_token: str
        
        :param syslog_ip: Whether to use a FIPS-certified firmware version or not.
        :type client_token: boolean
        """
        if client_token is None:
            # Boto has a bult-in retry mechanism, so we should always provide
            # a client token.
            client_token = uuid.uuid4().hex
        args = {"SubscriptionType": "PRODUCTION",
                "ClientToken": client_token}
        passed_args = {"SubnetId": subnet_id,
                       "SshKey": ssh_public_key,
                       "IamRoleArn": iam_role_arn,
                       "EniIp": hsm_ip,
                       "ExternalId": external_id,
                       "SyslogIp": syslog_ip,
                       "HsmSoftwareVersion": software_version,
                       "FipsCertified": fips_certified
                       }
        args.update({k:v for k, v in passed_args.items() if v is not None})
        response = self.rpcv1_request("CreateHsm", args)
        return self.rpcv1_unpack(response)

    def delete_client(self, client_arn):
        """
        Perform the DeleteLunaClient call and return the response.

        :param client_arn: the arn of the client to delete
        :type client_arn: str that is a correctly formatted ARN

        :returns: the api response
        :rtype: dict, e.g. {"Status": "Deletion of client ... successful."}
        """
        response = self.rpcv1_request("DeleteLunaClient", {"ClientArn": client_arn})
        return self.rpcv1_unpack(response)

    def delete_hapg(self, hapg_arn):
        """
        Perform the DeleteHapg call and return the response.

        :param hapg_arn: the arn of the hapg to delete
        :type hapg_arn: str that is a correctly formatted ARN

        :returns: the api response
        :rtype: dict, e.g. {"Status": "Deletion of Hapg ... successful."}
        """
        response = self.rpcv1_request("DeleteHapg", {"HapgArn": hapg_arn})
        return self.rpcv1_unpack(response)

    def delete_hsm(self, hsm_arn):
        """
        Perform the DeleteHsm call and return the response.

        :param hsm_arn: the arn of the hsm to delete
        :type hsm_arn: str that is a correctly formatted ARN

        :returns: the api response
        :rtype: dict
        """
        response = self.rpcv1_request("DeleteHsm", {"HsmArn": hsm_arn})
        return self.rpcv1_unpack(response)

    def describe_client(self, client_arn=None, fingerprint=None):
        """
        Perform the DescribeLunaClient API call and return the response.

        :returns: the api response, e.g. { 'ClientArn': [ ..., "HapgList": ["arn:...", "arn..."], ..., "State": ... ] }
        :rtype: dict
        """
        request_params = {}

        if client_arn:
            request_params["ClientArn"] = client_arn
        if fingerprint:
            request_params["CertificateFingerprint"] = fingerprint

        response = self.rpcv1_request("DescribeLunaClient", request_params)
        return self.rpcv1_unpack(response)

    def describe_hapg(self, hapg_arn):
        """
        Perform the DescribeHapg API call and return the response.

        :returns: the api response, e.g. { 'HapgArn': [ ..., "Label": "...", ..., "PartitionList": ["arn:...", "arn..."] ] }
        :rtype: dict
        """
        response = self.rpcv1_request("DescribeHapg", {"HapgArn": hapg_arn})
        return self.rpcv1_unpack(response)

    def describe_hsm(self, hsm_arn):
        """
        Perform the DescribeHsm call, returning an object that describes attributes of a single HSM.

        :param hsm_arn: the arn (obtained from list_hsms) of the hsm to describe
        :type hsm_arn: str that is a correctly formatted ARN

        :returns: the api response
        :rtype: dict
        """
        response = self.rpcv1_request("DescribeHsm", {"HsmArn": hsm_arn})
        return self.rpcv1_unpack(response)

    def list_clients(self):
        """
        Perform the ListLunaClients API call and return the response.

        :returns: the api response, e.g. { 'ClientList': [ 'arn:...', 'arn:...'] }
        :rtype: dict
        """
        response = self.rpcv1_request("ListLunaClients", {})
        return self.rpcv1_unpack(response)

    def list_hapgs(self):
        """
        Perform the ListHapgs API call and return the response.

        :returns: the api response, e.g. { 'HapgList': [ 'arn:...', 'arn:...'] }
        :rtype: dict
        """
        response = self.rpcv1_request("ListHapgs", {})
        return self.rpcv1_unpack(response)

    def list_hsms(self):
        """
        Perform the ListHsms API call and return the response.

        :returns: the api response, e.g. { 'HsmList': [ 'arn:...', 'arn:...'] }
        :rtype: dict
        """
        response = self.rpcv1_request("ListHsms", {})
        return self.rpcv1_unpack(response)

    def list_tags_for_resource(self, resource_arn):
        """
        Perform the ListTagsForResource call and return the response.
        
        :param resource_arn: arn of the cloudhsm resource to list the tags for
        :type resource_arn: str that is a correctly formatted ARN
        
        :returns: the api response
        :rtype: dict, e.g. {"TagList": "[{"Key": "foo", "Value": "foo", ...}]"}
        """
        args = {
            "ResourceArn": resource_arn
        }
        response = self.rpcv1_request("ListTagsForResource", args)
        return self.rpcv1_unpack(response)

    def modify_hapg(self, hapg_arn, label=None, partition_serial_list=None):
        args = {'HapgArn': hapg_arn}
        if label is not None:
            args["Label"] = label
        if partition_serial_list is not None:
            args["PartitionSerialList"] = partition_serial_list
        response = self.rpcv1_request("ModifyHapg", args)
        return self.rpcv1_unpack(response)

    def modify_hsm(self, hsm_arn, subnet_id=None, eni_ip=None, iam_role_arn=None, external_id=None, syslog_ip=None):
        """
        Performs the ModifyHsm API call. Returns immediately; use describe to inspect the progress.

        :param hsm_arn: the arn (obtained from list_hsms) of the hsm to modify
        :type hsm_arn: str that is a correctly formatted ARN

        :param subnet_id: New subnet (from a VPC) in which to place the existing HSM.
        :type subnet_id: str

        :param iam_role_arn: An ARN identifying the new IAM role that will allow the CloudHSM service to construct the ENI for us.
        :type iam_role_arn: str (an Amazon Resource Name)

        :param hsm_ip: The desired IP address of the HSM. If we don't specify this, the service will pick one for us or use existing one.
        :type hsm_ip: str (dotted quad)

        :param external_id: The external ID field of the new IAM role, if applicable.
        :type external_id: str

        :param syslog_ip: The IP address for the syslog monitoring server.
        :type syslog_ip: str

        """
        args = {'HsmArn': hsm_arn}
        passed_args = {'SubnetId': subnet_id,
                       'EniIp': eni_ip,
                       'IamRoleArn': iam_role_arn,
                       'ExternalId': external_id,
                       'SyslogIp': syslog_ip}
        args.update({k:v for k, v in passed_args.items() if v is not None})
        response = self.rpcv1_request("ModifyHsm", args)
        return self.rpcv1_unpack(response)

    def remove_tags_from_resource(self, resource_arn, keys):
        """
        Perform the RemoveTagsFromResource call and return the response.

        :param resource_arn: arn of the cloudhsm resource to remove the tags from
        :type resource_arn: str that is a correctly formatted ARN

        :param keys: tag keys 
        :type list: list of correctly formatted tag key strings

        :returns: the api response
        :rtype: dict, e.g. {"status": "Successfully deleted tags from resource."}
        """
        args = {
            "ResourceArn": resource_arn,
            "TagKeyList": keys
        }
        response = self.rpcv1_request("RemoveTagsFromResource", args)
        return self.rpcv1_unpack(response)

def local_json(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path) as fh:
        return json.load(fh)

ENDPOINTS = local_json('endpoints.json')

def region_defaults(region):
    '''
    Look up the default settings for connecting to a region.

    :param region: an availability zone such as us-east-1 or eu-west-1.
    :type region: str
    '''
    try:
        args = ENDPOINTS[region].copy()
    except KeyError:
        raise RuntimeError('The region you specified is currently unsupported')

    return args

def connect(region, **kw):
    '''
    Initiate a CloudHsmConnection with the arguments provided.

    :param region: an availability zone such as us-east-1 or eu-west-1.
    :type region: str
    '''
    # Do not load region_defaults if a host override is provided
    args = {'region': region} if kw.get('host') else region_defaults(region)
    args.update(kw)
    return CloudHsmConnection(**args)

ERRORCODES = local_json('errorcodes.json')

def interpret_error_response(status_code, payload):
    '''
    Given a list of error code objects, return an exception with the appropriate error message.
    '''
    logger.debug("Status code: %r; Payload: %r", status_code, payload)
    payload_message = payload.get("message")
    # Typically com.amazon.coral.service#ExceptionName
    exception_type = payload.get("__type", u"").split("#")[-1]
    handler = { "message": "Unexpected error" }
    for check in ERRORCODES:
        if check.get("default"):
            handler = check
            break
        elif "type" in check:
            if check["type"] == exception_type:
                handler = check
                break
        elif check["start"] <= status_code < check["stop"]:
            handler = check
            break
    handler_message = handler["message"]
    if payload_message is not None:
        message = "%s; %s" % (handler_message, payload_message)
    else:
        message = "%s." % handler_message
    if handler.get("user", False):
        return ValueError(message)
    else:
        return RuntimeError(message)
