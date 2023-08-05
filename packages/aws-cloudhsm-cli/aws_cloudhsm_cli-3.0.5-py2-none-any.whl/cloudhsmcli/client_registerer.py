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

logger = logging.getLogger('cloudhsmcli.client_registerer')

class ClientRegisterer(HsmWorker):
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
            self.register_client_and_assign_partition()
        except:
            logger.info('Registration of the client failed')
            raise
        else:
            return {
                'Status': 'Registration of the client {0} to the HA partition group {1} successful'.format(self.client_arn, self.hapg_arn)
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

    def register_client_and_assign_partition(self):
        '''
        Register the given client on all relevant HSMs and assign partitions to it
        '''
        logger.info ("Registering the given client and assigning partitions to it")

        client_data = self.cloudhsm.describe_client(self.client_arn)
        client_label = client_data['Label']
        client_cert = client_data['Certificate']

        client_cert_path = os.path.join('/tmp', client_label + '.pem')
        util.write_to_file(client_cert_path, util.rebuild_cert(client_cert))

        for (hsm_ip, partition_serial) in self.hsm_info:
            self.register_client_on_hsm(hsm_ip, client_label, client_cert_path)
            self.assign_partition_to_client(hsm_ip, client_label, partition_serial=partition_serial)
