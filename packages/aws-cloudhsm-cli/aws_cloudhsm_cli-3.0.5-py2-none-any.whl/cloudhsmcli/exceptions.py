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

class HsmNotZeroizedException(Exception):
    def __init__(self, hsm_arn, eni_ip):
        self.hsm_arn = hsm_arn
        self.eni_ip = eni_ip
        message = "HSM {0} at IP address {1} is not zeroized.".format(hsm_arn, eni_ip)
        super(HsmNotZeroizedException, self).__init__(self, message)

class HsmZeroizedException(Exception):
    def __init__(self, hsm_arn, eni_ip):
        self.hsm_arn = hsm_arn
        self.eni_ip = eni_ip
        message = "HSM {0} at IP address {1} is zeroized. It should be initialized.".format(hsm_arn, eni_ip)
        super(HsmZeroizedException, self).__init__(self, message)

class HsmAlreadyInHapgException(Exception):
    def __init__(self, hsm_arn, hapg_arn):
        self.hsm_arn = hsm_arn
        self.hapg_arn = hapg_arn
        message = "HSM {0} is already a member of HAPG {1}. If you wish to re-add the HSM to the HAPG, you must first use the remove-hsm-from-hapg command to end the present membership.".format(hsm_arn, hapg_arn)
        super(HsmAlreadyInHapgException, self).__init__(self, message)

class HsmNotInHapgException(Exception):
    def __init__(self, hsm_arn, hapg_arn):
        self.hsm_arn = hsm_arn
        self.hapg_arn = hapg_arn
        message = "HSM {0} is not a member of HAPG {1}. If the operation to add the HSM to the HAPG failed, retry the add-hsm-to-hapg command.".format(hsm_arn, hapg_arn)
        super(HsmNotInHapgException, self).__init__(self, message)

class PartitionNotFoundException(Exception):
    def __init__(self, partition_serial):
        self.partition_serial = partition_serial
        message = "Partition with serial number {0} cannot be found on any of your HSMs.".format(partition_serial)
        super(PartitionNotFoundException, self).__init__(self, message)
