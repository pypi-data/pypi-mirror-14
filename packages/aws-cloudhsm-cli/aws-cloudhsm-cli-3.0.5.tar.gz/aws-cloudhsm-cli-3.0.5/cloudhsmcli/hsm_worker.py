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
from luna_manipulator.luna_appliance_manipulator import LunaApplianceManipulator
from luna_reader.luna_state_reader import LunaStateReader
import logging, os
from cloudhsmcli.exceptions import HsmNotZeroizedException, HsmZeroizedException

logger = logging.getLogger('cloudhsmcli.hsm_worker')

class HsmWorker(object):
    def __init__(self):
        self._readers = {}
        self._manipulators = {}

    def connect_to_aws(self, aws_creds):
        '''
        Create the CloudHSM connection object
        '''
        logger.info("Connecting to AWS")
        self.cloudhsm = api.connect(**aws_creds)

    def reader(self, eni_ip):
        '''
        Create or reuse a LunaStateReader by eni_ip.
        '''
        if eni_ip not in self._readers:
            self._readers[eni_ip] = LunaStateReader(eni_ip)
        return self._readers[eni_ip]

    def manipulator(self, eni_ip):
        '''
        Create or reuse a LunaApplianceManipulator by eni_ip.
        '''
        if eni_ip not in self._manipulators:
            self._manipulators[eni_ip] = LunaApplianceManipulator(eni_ip)
        return self._manipulators[eni_ip]

    def discover_hsms(self, hsm_arns):
        '''
        Call into AWS to describe the HSMs. Then connect to the HSMs to determine status.
        :param hsms: list of hsm arns
        '''
        self.hsm_descriptions = {}
        for hsm_arn in hsm_arns:
            logger.info("Inspecting %s", hsm_arn)

            # from the API, get the hsm description
            self.hsm_descriptions[hsm_arn] = {}
            self.hsm_descriptions[hsm_arn]["api_description"] = self.cloudhsm.describe_hsm(hsm_arn)
            eni_ip = self.hsm_descriptions[hsm_arn]["api_description"]["EniIp"]
            logger.debug("Found %s ip: %s", hsm_arn, eni_ip)

            # from the HSM, pick ithe nformation that we will need
            reader = self.reader(eni_ip)
            self.hsm_descriptions[hsm_arn]["hsm_description"] = {}
            self.hsm_descriptions[hsm_arn]["hsm_description"]["zeroized"] = reader.is_luna_zeroized()
            self.hsm_descriptions[hsm_arn]["hsm_description"]["serial_number"] = reader.get_serial_number()

    def confirm_zeroized(self, hsm_descriptions):
        '''
        Confirm all HSMs described in hsm_descriptions are zeroized. Throw HsmNotZeroizedException if not.
        '''
        for hsm_arn in hsm_descriptions:
            zeroized = hsm_descriptions[hsm_arn]["hsm_description"]["zeroized"]
            if not zeroized:
                eni_ip = hsm_descriptions[hsm_arn]["api_description"]["EniIp"]
                raise HsmNotZeroizedException(hsm_arn, eni_ip)

    def confirm_not_zeroized(self, hsm_descriptions):
        '''
        Confirm all HSMs described in hsm_descriptions are not zeroized. Throw HsmZeroizedException if HSM is zeroized.
        '''
        for hsm_arn in hsm_descriptions:
            zeroized = hsm_descriptions[hsm_arn]["hsm_description"]["zeroized"]
            if zeroized:
                eni_ip = hsm_descriptions[hsm_arn]["api_description"]["EniIp"]
                raise HsmZeroizedException(hsm_arn, eni_ip)

    def generate_partition_label(self, hapg_arn, hsm_serial):
        '''
        Generate the partition label with hapg identifier and serial of the hsm
        '''
        hapg_identifier = hapg_arn.split(':')[5]
        return "%s_%s" % (hapg_identifier, hsm_serial)

    def lookup_partition_serial(self, reader, label):
        for par_serial, par_label in reader.get_partitions():
            if label == par_label:
                return par_serial
        return None

    def scp_server_cert_from_hsm(self, hsm_ip, server_cert_path, retries=3, sleeptime=10):
        '''
        Copy the HSM server cert to the local environment
        '''
        temp_server_cert_path = os.path.join('/tmp', hsm_ip + '_server.pem')

        for retry in range(retries):
            try:
                util.scp_file_from_remote_source(hsm_ip, 'server.pem', temp_server_cert_path, logger)
            except OSError:
                if retry == retries - 1:
                    return False
                else:
                    sleep(sleeptime)
                    continue
            else:
                break

        util.concatenate_files(temp_server_cert_path, server_cert_path)
        os.remove(temp_server_cert_path)

        return True

    def scp_client_cert_onto_hsm(self, hsm_ip, client_cert_path, retries=3, sleeptime=10):
        '''
        Copy the client cert onto the HSM
        '''
        for retry in range(retries):
            try:
                util.scp_file_to_remote_destination(hsm_ip, client_cert_path, '', logger)
            except OSError:
                if retry == retries - 1:
                    return False
                else:
                    sleep(sleeptime)
                    continue
            else:
                break

        return True

    def register_client_on_hsm(self, hsm_ip, client_label, cert_path):
        '''
        Register a client on an HSM
        '''
        reader = self.reader(hsm_ip)
        clients = reader.get_clients()
        if client_label in clients:
            return True

        transferred = self.scp_client_cert_onto_hsm(hsm_ip, cert_path)
        if transferred:
            # register the client on the hsm
            manipulator = self.manipulator(hsm_ip)
            logger.info('Registering the client {0} on {1}'.format(client_label, hsm_ip))
            return manipulator.register_client(client_label, client_label)
        else:
            return False

    def remove_client_from_hsm(self, hsm_ip, client_label):
        '''
        Remove a client from an HSM
        '''
        reader = self.reader(hsm_ip)
        clients = reader.get_clients()
        if client_label in clients:
            partitions = reader.get_client_partitions(client_label)
            if not partitions:
                # remove the client from the hsm
                manipulator = self.manipulator(hsm_ip)
                logger.info('Deleting the client {0} from {1}'.format(client_label, hsm_ip))
                return manipulator.remove_client(client_label)

        return True

    def assign_partition_to_client(self, hsm_ip, client_label, partition_serial=None, partition_label=None):
        '''
        Assign a client to a partition on HSM
        '''
        reader = self.reader(hsm_ip)
        partitions = reader.get_client_partitions(client_label)
        if not partition_label:
            partition_label = dict(reader.get_partitions())[partition_serial]

        if partition_label in partitions:
            return True
        else:
            # assign the partition to the client
            manipulator = self.manipulator(hsm_ip)
            logger.info('Assigning the partition {0} on {1} to the client {2}'.format(partition_label, hsm_ip, client_label))
            return manipulator.assign_partition_to_client(client_label, partition_label)

    def revoke_partition_from_client(self, hsm_ip, client_label, partition_serial):
        '''
        Revoke a partition from a client on HSM
        '''
        reader = self.reader(hsm_ip)
        partition_label = dict(reader.get_partitions())[partition_serial]
        partitions = reader.get_client_partitions(client_label)
        if partition_label in partitions:
            # revoke the partition from the client
            manipulator = self.manipulator(hsm_ip)
            logger.info('Revoking the partition {0} on {1} from the client {2}'.format(partition_label, hsm_ip, client_label))
            return manipulator.revoke_partition_from_client(client_label, partition_label)

        return True

    def ensure_ntls(self, hsm_ip):
        '''
        Make sure the NTLS service is active.
        '''
        manipulator = self.manipulator(hsm_ip)
        manipulator.ensure_ntls()
