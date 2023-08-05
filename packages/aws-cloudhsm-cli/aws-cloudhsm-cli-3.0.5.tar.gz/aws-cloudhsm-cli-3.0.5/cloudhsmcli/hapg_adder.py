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

from cloudhsmcli.hsm_worker import HsmWorker
from cloudhsmcli.exceptions import HsmAlreadyInHapgException
import logging

logger = logging.getLogger('cloudhsmcli.hapg_adder')

class HapgAdder(HsmWorker):
    def __init__(self, hapg_arn, hsm_arn, partition_password, cloning_domain, aws_creds, so_password):
        super(self.__class__, self).__init__()
        self.hsm_arn = hsm_arn
        self.hapg_arn = hapg_arn
        self.partition_password = partition_password
        self.so_password = so_password
        self.cloning_domain = cloning_domain
        self.aws_creds = aws_creds

    def run(self):
        try:
            self.connect_to_aws(self.aws_creds)
            self.discover_hsms([self.hsm_arn])
            self.confirm_not_zeroized(self.hsm_descriptions)
            self._confirm_hsm_not_in_hapg()
            self._create_partition()
            self._modify_hapg()
        except:
            logger.info("HSM addition failed")
            raise
        else:
            return {
                'Status': 'Addition of HSM {0} to HAPG {1} successful'.format(self.hsm_arn, self.hapg_arn)
            }

    def _confirm_hsm_not_in_hapg(self):
        # This confirms that the HAPG object in the API does not contain a serial number for a partition
        # on the target HSM. If a partition's serial starts with the hsm's serial, this means the
        # partition belongs to that hsm, therefore the hsm is already in the hapg.
        logger.info("Checking if HSM is already in HAPG")

        self.hapg_description = self.cloudhsm.describe_hapg(self.hapg_arn)
        hsm_serial = self.hsm_descriptions[self.hsm_arn]['hsm_description']['serial_number']
        for part_serial in self.hapg_description['PartitionSerialList']:
            if part_serial.startswith(hsm_serial):
                raise HsmAlreadyInHapgException(self.hsm_arn, self.hapg_arn)

    def _create_partition(self):
        logger.info("Creating partition on HSM")

        self.eni_ip = self.hsm_descriptions[self.hsm_arn]["api_description"]["EniIp"]
        manipulator = self.manipulator(self.eni_ip)
        reader = self.reader(self.eni_ip)

        hsm_serial = self.hsm_descriptions[self.hsm_arn]["hsm_description"]["serial_number"]
        par_label = self.generate_partition_label(self.hapg_arn, hsm_serial)

        # Check if partition with label matching naming convention already exists. If it does, it's possible
        # that a previous run created a partition but failed before updating the API. This handles that case.
        par_serial = self.lookup_partition_serial(reader, par_label)
        if par_serial:
            logger.info("Found partition with label %s and serial %s", par_label, par_serial)
            self.partition_serial = par_serial
            return

        logger.info("Partition with label %s not found, creating", par_label)

        # Create new partition
        manipulator.hsm_login(password=self.so_password)
        manipulator.create_partition(
            partition_label = par_label,
            partition_password = self.partition_password,
            cloning_domain = self.cloning_domain)

        # Verify new partition
        par_serial = self.lookup_partition_serial(reader, par_label)
        if not par_serial:
            raise RuntimeError("Unable to determine the partition serial number after creating partition {0}. This means there was an error in the creation of the partition. Contact CloudHSM for assistance.".format(par_label))

        self.partition_serial = par_serial
        logger.info("Created partition %s with serial %s", par_label, par_serial)

    def _modify_hapg(self):
        logger.info("Updating HAPG object with new partition serial")

        existing_serials = self.hapg_description["PartitionSerialList"]
        existing_serials.append(self.partition_serial)

        self.cloudhsm.modify_hapg(self.hapg_arn, partition_serial_list = existing_serials)
