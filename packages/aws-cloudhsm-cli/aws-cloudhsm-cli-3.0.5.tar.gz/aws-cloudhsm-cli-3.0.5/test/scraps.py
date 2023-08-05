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

hsm_description = {
    'HsmArn': 'arn:aws:cloudhsm:qe-westeast-42:123412341234:hsm-b0b',
    'Status': 'RUNNING',
    'AvailabilityZone': 'qe-westeast-42',
    'EniId': 'eni-1234',
    'EniIp': '10.0.0.10',
    'SubscriptionType': 'PROD',
    'SubscriptionStartDate': '2013-01-01T12:12:12Z',
    'SubscriptionEndDate': '',
    'VpcId': 'vpc-1234',
    'SubnetId': 'subnet-1234',
    'IamRoleArn': 'arn:aws:iam::123412341234:cloudHsmRole',
    'SerialNumber': '12345',
    'VendorName': 'Safenet',
    'HsmType': 'LunaSA',
    'SoftwareVersion': '5.1',
    'SshPublicKey': 'ssh_key',
    'SshKeypairName': '',
    'SshKeyLastUpdated': '2013-01-01T12:12:12Z',
    'ServerCertUri': 'http://mycert/',
    'ServerCertLastUpdated': '2013-01-01T12:12:12Z',
}

hapg_description = {
    'HapgArn': 'arn:aws:cloudhsm:qe-westeast-42:123412341234:hapg-d2d',
    'HapgSerial': '1234567890', 
    'Label': 'd2d', 
    'LastModifiedTimestamp': "1399045770", 
    'PartitionSerialList': ['123456789', '234567890'],
    'State': 'READY'
}

client_description = {
    'Certificate': '-----BEGIN CERTIFICATE-----\n\r' + '01234\r567' * 24 + '\n\r\n\r-----END CERTIFICATE-----\n\r',
    'ClientArn': 'arn:aws:cloudhsm:qe-westeast-42:123412341234:client-c1c', 
    'Label': 'c1c',
    'LastModifiedTimestamp': '1399045770', 
    'State': 'READY'
}

hsm1_desc = {
    'HsmArn': 'arn:aws:cloudhsm:qe-westeast-42:345678345678:hsm-e3e',
    'EniId': 'eni-345678',
    'EniIp': '10.0.0.10',
    'SerialNumber': '345678'
}

hsm2_desc = {
    'HsmArn': 'arn:aws:cloudhsm:qe-westeast-42:123456123456:hsm-f4f',
    'EniId': 'eni-123456',
    'EniIp': '10.0.0.20',
    'SerialNumber': '123456'
}

hsm3_desc = {
    'HsmArn': 'arn:aws:cloudhsm:qe-westeast-42:234567234567:hsm-g5g',
    'EniId': 'eni-234567',
    'EniIp': '10.0.0.30',
    'SerialNumber': '234567'
}

hsm_ips = ['10.99.99.101', '10.99.99.102', '10.99.99.103']

group_partition_serials = {
    'unit-test-hapg-1': ['157826011', '157714012'],
    'unit-test-hapg-2': ['153098011', '157826004'],
    'unit-test-hapg-3': ['157389010', '153313010']
}
