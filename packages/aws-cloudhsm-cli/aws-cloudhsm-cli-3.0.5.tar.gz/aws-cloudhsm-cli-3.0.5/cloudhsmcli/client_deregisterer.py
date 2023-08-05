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


import cloudhsmcli.api as api
import cloudhsmcli.util as util
from cloudhsmcli.hsm_worker import HsmWorker
from cloudhsmcli.exceptions import PartitionNotFoundException
import logging, os

logger = logging.getLogger('cloudhsmcli.client_deregisterer')

class ClientDeregisterer(HsmWorker):
    def __init__(self, client_arn, hapg_arn, aws_creds):
        super(self.__class__, self).__init__()
        self.client_arn = client_arn
        self.hapg_arn = hapg_arn
        self.aws_creds = aws_creds
        self.hsm_info = []

    def run(self):
        try:
            self.connect_to_aws(self.aws_creds)
            self.find_hsm_info()
            self.revoke_partition_and_remove_client()
        except:
            logger.info('Deregistration of the client failed')
            raise
        else:
            return {
                'Status': 'Deregistration of the client {0} from the HA partition group {1} successful'.format(self.client_arn, self.hapg_arn)
            }

    def find_hsm_info(self):
        '''
        Find the HSM IPs of the HA partition group
        '''
        logger.info("Finding the HSM IPs of the HA partition group")

        hapg_data = self.cloudhsm.describe_hapg(self.hapg_arn)
        partition_serials = hapg_data['PartitionSerialList']

        if not partition_serials:
            raise Exception('The HAPG has no member partitions.')

        hsm_data = self.cloudhsm.list_hsms()
        for hsm_arn in hsm_data['HsmList']:
            hsm_desc = self.cloudhsm.describe_hsm(hsm_arn)
            for partition_serial in partition_serials:
                if partition_serial.startswith(hsm_desc['SerialNumber']):
                    self.hsm_info.append((hsm_desc['EniIp'], partition_serial))
                    partition_serials.remove(partition_serial)

        if partition_serials:
            raise PartitionNotFoundException(partition_serials[0])

    def revoke_partition_and_remove_client(self):
        '''
        Revoke partitions from the temporary client and remove it
        '''
        logger.info ("Revoking partitions from the temporary client and removing it")

        client_data = self.cloudhsm.describe_client(self.client_arn)
        client_label = client_data['Label']

        for (hsm_ip, partition_serial) in self.hsm_info:
            self.revoke_partition_from_client(hsm_ip, client_label, partition_serial)
            self.remove_client_from_hsm(hsm_ip, client_label)
