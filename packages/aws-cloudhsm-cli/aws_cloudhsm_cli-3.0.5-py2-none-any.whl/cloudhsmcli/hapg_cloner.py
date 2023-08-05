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
import logging, datetime, os, subprocess, shutil

logger = logging.getLogger('cloudhsmcli.hapg_cloner')

class HapgCloner(HsmWorker):
    def __init__(self, src_hapg_arn, dest_hapg_arn, hapg_password, aws_creds):
        super(self.__class__, self).__init__()
        self.src_hapg_arn = src_hapg_arn
        self.dest_hapg_arn = dest_hapg_arn
        self.hapg_password = hapg_password
        self.aws_creds = aws_creds

        self.luna_dir = util.find_luna_dir()

        self.std_conf_path = os.path.join('/etc', 'Chrystoki.conf')
        self.std_cert_path = os.path.join(self.luna_dir, 'cert', 'server', 'CAFile.pem')

        current = str(datetime.datetime.now().isoformat())
        self.suffix = current[-6:]
        self.temp_conf_path = os.path.join('/tmp', 'Chrystoki.conf_' + self.suffix)
        self.temp_cert_path = os.path.join('/tmp', 'CAFile.pem_' + self.suffix)
        self.client_name = 'temp_client_' + self.suffix
        self.group_label = 'temp_group_' + self.suffix

        self.isClient = False
        self.hasCAFile = False
        self.registeredClient = False
        self.partition_serials = []
        self.hsm_info = []

    def run(self):
        try:
            # Back up Luna conf
            logger.warn('Backing up existing config file')
            shutil.copyfile(self.std_conf_path, self.temp_conf_path)
            # Back up cert only if it exists
            if os.path.isfile(self.std_cert_path):
                logger.warn('Backing up existing cert file')
                self.hasCAFile = True
                shutil.copyfile(self.std_cert_path, self.temp_cert_path)

            logger.warn('Collecting information about the HA partition groups')
            self.connect_to_aws(self.aws_creds)
            self.merge_partition_serials()
            self.find_hsm_info()

            logger.warn('Setting up a cloning environment')
            self.create_temporary_client()
            self.register_client_and_assign_partition()
            self.generate_client_config()
            self.ensure_ntls_on_all()

            logger.warn('Cloning the HA partition groups')
            self.synchronize_hapgs()

        except:
            logger.warn('Cloning HA partition groups failed')
            raise
        else:
            return {
                'Status': 'Completed cloning the HA partition group {0} to the HA partition group {1}'.format(self.src_hapg_arn, self.dest_hapg_arn)
            }
        finally:
            logger.warn('Cleaning up the cloning environment')
            if self.registeredClient:
                self.revoke_partition_and_remove_client()
            if self.isClient:
                self.delete_temp_client()

            # Restore client to original state
            if os.path.isfile(self.temp_conf_path):
                logger.warn('Restoring existing config file')
                shutil.copyfile(self.temp_conf_path, self.std_conf_path)
                os.remove(self.temp_conf_path)
            if os.path.isfile(self.temp_cert_path):
                logger.warn('Restoring existing cert file')
                shutil.copyfile(self.temp_cert_path, self.std_cert_path)
                os.remove(self.temp_cert_path)
            if not self.hasCAFile:
                os.remove(self.std_cert_path)


    def merge_partition_serials(self):
        '''
        Merge the lists of partition serial numbers
        '''
        logger.info("Merging the lists of partition serial numbers")

        src_hapg_data = self.cloudhsm.describe_hapg(self.src_hapg_arn)
        if not src_hapg_data['PartitionSerialList']:
            raise Exception('The source HAPG has no member partitions. There is nothing to clone from.')

        dest_hapg_data = self.cloudhsm.describe_hapg(self.dest_hapg_arn)
        if not dest_hapg_data['PartitionSerialList']:
            raise Exception('The destination HAPG has no member partitions. There is nothing to clone to.')

        self.partition_serials = src_hapg_data['PartitionSerialList'] + dest_hapg_data['PartitionSerialList']

    def find_hsm_info(self):
        '''
        Find the HSM IPs of the two HA partition groups
        '''
        logger.info("Find the HSM IPs of the two HA partition groups")

        count = 0
        hsm_data = self.cloudhsm.list_hsms()
        for hsm_arn in hsm_data['HsmList']:
            partition_list = []
            hsm_desc = self.cloudhsm.describe_hsm(hsm_arn)
            for partition_serial in self.partition_serials:
                if partition_serial.startswith(hsm_desc['SerialNumber']):
                    partition_list.append(partition_serial)
            if partition_list:
                self.hsm_info.append((hsm_desc['EniIp'], partition_list))
                count = count + len(partition_list)

        if count != len(self.partition_serials):
            raise Exception('Unable to connect to all members of the HAPGs')

    def create_temporary_client(self):
        '''
        Use Safenet tools to generate a client cert for use during synchronize
        '''
        logger.info ("Creating temporary client")

        proc = subprocess.Popen([os.path.join(self.luna_dir, 'bin', 'vtl'), 'createCert', '-n', self.client_name], stdout=subprocess.PIPE)
        out, err = proc.communicate()
        if proc.returncode != 0 or not 'Private Key created' in out:
            raise Exception('The VTL command failed to create a Luna client')
        else:
            self.isClient = True

    def register_client_and_assign_partition(self):
        '''
        Register the temporary client and assign partitions to it
        '''
        logger.info ("Registering the temporary client and assigning partitions to it")

        self.registeredClient = True
        client_cert_path = os.path.join(self.luna_dir, 'cert', 'client', self.client_name + '.pem')
        for (hsm_ip, partition_list) in self.hsm_info:
            self.register_client_on_hsm(hsm_ip, self.client_name, client_cert_path)
            for partition_serial in partition_list:
                self.assign_partition_to_client(hsm_ip, self.client_name, partition_serial=partition_serial)

    @property
    def hsm_ips(self):
        return set(hsm_ip for hsm_ip, partition_list in self.hsm_info)

    def generate_client_config(self):
        '''
        Generate client configuration
        '''
        logger.info ("Generating client configuration")

        hsm_ips = self.hsm_ips

        if 'lunaclient' in self.luna_dir:
            config_file = util.generate_luna_53_config(self.client_name, hsm_ips, {self.group_label: self.partition_serials})
        else:
            config_file = util.generate_luna_51_config(self.client_name, hsm_ips, {self.group_label: self.partition_serials})

        util.write_to_file(self.std_conf_path, config_file)

        for hsm_ip in hsm_ips:
            self.scp_server_cert_from_hsm(hsm_ip, os.path.join(self.luna_dir, 'cert', 'server', 'CAFile.pem'))

    def ensure_ntls_on_all(self):
        '''
        Make sure the NTLS service is started for all hsms.
        '''
        for hsm_ip in self.hsm_ips:
            self.ensure_ntls(hsm_ip)

    def synchronize_hapgs(self):
        '''
        Run the synchronize command with the temporary hapg
        '''
        logger.info("Synchronizing the two HA partition groups")

        if 'lunaclient' in self.luna_dir:
            proc = subprocess.Popen([os.path.join(self.luna_dir, 'bin', 'vtl'), 'haAdmin', 'synchronize', '-group', self.group_label, '-password', self.hapg_password], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            proc = subprocess.Popen([os.path.join(self.luna_dir, 'bin', 'vtl'), 'haAdmin', '-synchronize', '-group', self.group_label, '-password', self.hapg_password], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        count = -1
        for (hsm_ip, partition_list) in self.hsm_info:
            reader = self.reader(hsm_ip)
            for partition_serial in partition_list:
                object_count = reader.count_partition_objects(partition_serial)
                if count == -1:
                    count = object_count
                elif count != object_count:
                    raise RuntimeError('The VTL command failed to synchronize the partitions. This may have happened for the following reasons:\n1. The source and destination groups have different partition passwords.\n2. The source and destination groups have different domains.\nEnsure that these match and try again. If failure persists, contact support.')

    def revoke_partition_and_remove_client(self):
        '''
        Revoke partitions from the temporary client and remove it
        '''
        logger.info ("Revoking partitions from the temporary client and removing it")

        for hsm_ip, partition_list in self.hsm_info:
            for partition_serial in partition_list:
                self.revoke_partition_from_client(hsm_ip, self.client_name, partition_serial)
            self.remove_client_from_hsm(hsm_ip, self.client_name)

    def delete_temp_client(self):
        '''
        Delete the temporary client
        '''
        logger.info("Deleting temporary client %s", self.client_name)

        os.remove(os.path.join(self.luna_dir, 'cert', 'client', self.client_name + '.pem'))
        os.remove(os.path.join(self.luna_dir, 'cert', 'client', self.client_name + 'Key.pem'))
