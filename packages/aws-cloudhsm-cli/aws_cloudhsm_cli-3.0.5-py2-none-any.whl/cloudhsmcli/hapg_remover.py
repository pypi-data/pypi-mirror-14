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
import logging, re

logger = logging.getLogger('cloudhsmcli.hapg_remover')

class HapgRemover(HsmWorker):
    def __init__(self, hapg_arn, hsm_arn, aws_creds, so_password):
        super(self.__class__, self).__init__()
        self.hsm_arn = hsm_arn
        self.hapg_arn = hapg_arn
        self.so_password = so_password
        self.aws_creds = aws_creds

    def run(self):
        try:
            self.connect_to_aws(self.aws_creds)
            self.discover_hsms([self.hsm_arn])
            self._remove_partition()
            self._modify_hapg()
        except:
            logger.info("HSM removal failed")
            raise
        else:
            return {
                'Status': 'Removal of HSM {0} from HAPG {1} successful'.format(self.hsm_arn, self.hapg_arn)
            }

    def _remove_partition(self):
        logger.info("Removing partition from HSM")

        self.eni_ip = self.hsm_descriptions[self.hsm_arn]["api_description"]["EniIp"]
        manipulator = self.manipulator(self.eni_ip)
        reader = self.reader(self.eni_ip)

        hsm_serial = self.hsm_descriptions[self.hsm_arn]["hsm_description"]["serial_number"]
        par_label = self.generate_partition_label(self.hapg_arn, hsm_serial)

        # Check if partition with label matching naming convention already exists. If a partition does not exist,
        # a previous delete operation may have failed after deleting the partition but before updating the HAPG
        # object. This handles that case.
        partition_serial = self.lookup_partition_serial(reader, par_label)
        if not partition_serial:
            logger.info("Did not find partition with label %s", par_label)
            return

        logger.info("Partition with label %s and serial %s found, deleting", par_label, partition_serial)

        # Delete partition
        manipulator.hsm_login(password=self.so_password)
        manipulator.delete_partition(partition_label=par_label)

        # Verify partition deleted
        after_par_serial = self.lookup_partition_serial(reader, par_label)
        if after_par_serial:
            raise RuntimeError("Partition with label {0} still on HSM. Delete operation failed.".format(par_label))

        logger.info("Deleted partition %s with serial %s", par_label, partition_serial)

    def _modify_hapg(self):
        logger.info("Updating HAPG object, removing partition serial")

        hapg_description = self.cloudhsm.describe_hapg(self.hapg_arn)

        # make sure everything is str
        hsm_serial = str(self.hsm_descriptions[self.hsm_arn]['hsm_description']['serial_number'])
        existing_serials = map(str, hapg_description["PartitionSerialList"])

        # remove serials that don't start with the hsm_serial
        existing_serials = [serial for serial in existing_serials if not serial.startswith(hsm_serial)]

        self.cloudhsm.modify_hapg(self.hapg_arn, partition_serial_list = existing_serials)
