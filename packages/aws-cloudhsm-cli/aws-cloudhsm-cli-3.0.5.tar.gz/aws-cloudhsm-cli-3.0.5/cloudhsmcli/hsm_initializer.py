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
from luna_manipulator.luna_appliance_manipulator import LunaApplianceManipulator
from cloudhsmcli.hsm_worker import HsmWorker
import logging

logger = logging.getLogger('cloudhsmcli.hsm_initializer')

class HsmInitializer(HsmWorker):
    def __init__(self, hsm_arn, so_password, cloning_domain, label, aws_creds):
        '''
        :param hsm_arn: An HSM ARN to initialize.
        :type hsm_arn: str
        :param so_password: The security officer password to set on the HSM
        :type so_password: str
        :param cloning_domain: The cloning domain to set on the HSM.
        :type cloning_domain: str
        :param label: The label for the HSM
        :type label: str
        :param aws_creds: The region and, optionally, access and secret to connect to CloudHSM.
        :type aws_creds: dict of strings to strings
        '''
        super(self.__class__, self).__init__()
        self.hsm_arn = hsm_arn
        self.so_password = so_password
        self.cloning_domain = cloning_domain
        self.label = label
        self.aws_creds = aws_creds

    def run(self):
        '''
        Operation flow:
        * Find IP addresses of the HSM and verify that it is not initialized.
        * Run the hsm init command
        * Restart and bind ntls to eth0
        '''
        try:
            self.connect_to_aws(self.aws_creds)
            self.discover_hsms([self.hsm_arn])
            self.confirm_zeroized(self.hsm_descriptions)
            self.eni_ip = self.hsm_descriptions[self.hsm_arn]["api_description"]["EniIp"]
            self.initialize_hsm()
            self.restart_and_bind_ntls()
        except:
            logger.info("HSM initialization failed")
            raise
        else:
            return {
                'Status': 'Initialization of the HSM successful'
            }

    def initialize_hsm(self):
        '''
        Run the hsm init command on the HSM
        '''
        logger.info("Running initialize command on HSM")

        manipulator = self.manipulator(self.eni_ip)
        manipulator.initialize_hsm(self.label, self.cloning_domain, self.so_password)

    def restart_and_bind_ntls(self):
        '''
        Restart ntls on the on the HSM and bind it to eth0
        '''
        logger.info("Restarting NTLS and binding to eth0 on the HSM")
        manipulator = self.manipulator(self.eni_ip)
        manipulator.restart_and_bind_ntls()
