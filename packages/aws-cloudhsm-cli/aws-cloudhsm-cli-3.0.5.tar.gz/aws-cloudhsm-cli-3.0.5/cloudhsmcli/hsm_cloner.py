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


import cloudhsmcli.util as util
from cloudhsmcli.hsm_worker import HsmWorker
import logging, datetime, os, subprocess, shutil, getpass

logger = logging.getLogger('cloudhsmcli.hsm_cloner')

class HsmCloner(HsmWorker):
    def __init__(self, src_hsm_arn, dest_hsm_arn, so_password, aws_creds):
        super(self.__class__, self).__init__()
        self.src_hsm_arn = src_hsm_arn
        self.dest_hsm_arn = dest_hsm_arn
        self.so_password = so_password
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
        self.synchronizedHsms = False
        self.src_hsm_ip = ''
        self.src_hsm_serial = ''
        self.dest_hsm_ip = ''
        self.dest_hsm_serial = ''
        self.src_partition_info = {}
        self.dest_partition_info = {}
        self.src_dest_serials = []

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

            logger.warn('Collecting information about the HSMs')
            self.connect_to_aws(self.aws_creds)
            self.determine_partitions_to_be_cloned()

            logger.warn('Creating partitions on the destination HSM')
            self.create_partitions_on_clone_hsm()

            logger.warn('Setting up a cloning environment')
            self.create_temporary_client()
            self.register_client_and_assign_partition()

            logger.warn('Replicating keys from the source HSM')
            self.ensure_ntls(self.src_hsm_ip)
            self.ensure_ntls(self.dest_hsm_ip)
            self.synchronize_hsms()

        except:
            logger.warn('Cloning HSMs failed')
            raise
        else:
            return {
                'Status': 'Completed cloning the HSM {0} to the HSM {1}'.format(self.src_hsm_arn, self.dest_hsm_arn)
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

            # Call clone_client_configuration() after revoke_partition_and_remove_client()
            # If clone_client_configuration() is called before revoke_partition_and_remove_client(),
            # then it'll try and fail to clone the temporary client.
            logger.warn('Cloning the client/partition configuration on HSM')
            if self.synchronizedHsms:
                self.clone_client_configuration()

    def determine_partitions_to_be_cloned(self):
        '''
        Compile a list of partitions on the source HSM
        '''
        logger.info("Collecting the partition information from %s", self.src_hsm_arn)

        src_hsm_desc = self.cloudhsm.describe_hsm(self.src_hsm_arn)
        self.src_hsm_ip = src_hsm_desc['EniIp']
        self.src_hsm_serial = src_hsm_desc['SerialNumber']
        dest_hsm_desc = self.cloudhsm.describe_hsm(self.dest_hsm_arn)
        self.dest_hsm_ip = dest_hsm_desc['EniIp']
        self.dest_hsm_serial = dest_hsm_desc['SerialNumber']

        reader = self.reader(self.src_hsm_ip)
        partitions = reader.get_partitions()
        if partitions:
            for serial, label in partitions:
                self.src_partition_info[serial] = label
        else:
            raise Exception('There is no partition on the source HSM to clone')

    def create_partitions_on_clone_hsm(self):
        '''
        Create partitions on the destination HSM
        '''
        logger.info("Creating partitions on %s", self.dest_hsm_arn)

        temp_partition_info = {}
        reader = self.reader(self.dest_hsm_ip)
        existing_partitions = reader.get_partitions()
        for serial, label in existing_partitions:
            self.dest_partition_info[serial] = label
            temp_partition_info[label] = serial

        manipulator = self.manipulator(self.dest_hsm_ip)
        manipulator.hsm_login(password=self.so_password)
        for src_partition_serial, src_partition_label in self.src_partition_info.iteritems():
            partition_password = getpass.getpass(prompt='Please provide the password for {0}:'.format(src_partition_label))
            cloning_domain = getpass.getpass(prompt='Please provide the cloning domain for {0}:'.format(src_partition_label))

            if len(src_partition_label) == 20 and src_partition_label.startswith('hapg') and src_partition_label.endswith(self.src_hsm_serial):
                hapg_arn = self.src_hsm_arn[:-12] + src_partition_label[:13]
                dest_partition_label = self.generate_partition_label(hapg_arn, self.dest_hsm_serial)
            else:
                dest_partition_label = src_partition_label

            if dest_partition_label in self.dest_partition_info.values():
                dest_partition_serial = temp_partition_info[dest_partition_label]
                logger.warn('The partition {0} ({1}) already exists'.format(dest_partition_label, dest_partition_serial))
            else:
                manipulator.create_partition(partition_label = dest_partition_label,
                                             partition_password = partition_password, cloning_domain = cloning_domain)
                partitions = reader.get_partitions()
                dest_partition_serial = {v:k for k,v in partitions}[dest_partition_label]
                self.dest_partition_info[dest_partition_serial] = dest_partition_label
                temp_partition_info[dest_partition_label] = dest_partition_serial
                logger.warn('A partition was created: {0} ({1})'.format(dest_partition_label, dest_partition_serial))

                if len(dest_partition_label) == 20 and dest_partition_label.startswith('hapg') and dest_partition_label.endswith(self.dest_hsm_serial):
                    try:
                        hapg_arn = self.dest_hsm_arn[:-12] + dest_partition_label[:13]
                        hapg_desc = self.cloudhsm.describe_hapg(hapg_arn)
                        group_partition_serials = hapg_desc['PartitionSerialList']
                        group_partition_serials.append(dest_partition_serial)
                        self.cloudhsm.modify_hapg(hapg_arn, partition_serial_list = group_partition_serials)
                    except Exception:
                        logger.exception('Update to the HAPG information failed')

            self.src_dest_serials.append((src_partition_serial, dest_partition_serial, partition_password));

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
        Register the temporary client on both HSMs and assign partitions to it
        '''
        logger.info ("Registering the temporary client and assigning partitions to it")

        self.registeredClient = True
        client_cert_path = os.path.join(self.luna_dir, 'cert', 'client', self.client_name + '.pem')

        self.register_client_on_hsm(self.src_hsm_ip, self.client_name, client_cert_path)
        for src_partition_serial in self.src_partition_info.keys():
            self.assign_partition_to_client(self.src_hsm_ip, self.client_name, partition_serial=src_partition_serial)

        self.register_client_on_hsm(self.dest_hsm_ip, self.client_name, client_cert_path)
        for dest_partition_serial in self.dest_partition_info.keys():
            self.assign_partition_to_client(self.dest_hsm_ip, self.client_name, partition_serial=dest_partition_serial)

    def synchronize_hsms(self):
        '''
        Synchronize the partitions on the two HSMs
        '''
        logger.info("Synchronizing the two HSMs")

        self.scp_server_cert_from_hsm(self.src_hsm_ip, os.path.join(self.luna_dir, 'cert', 'server', 'CAFile.pem'))
        self.scp_server_cert_from_hsm(self.dest_hsm_ip, os.path.join(self.luna_dir, 'cert', 'server', 'CAFile.pem'))

        hsm_ips = [self.src_hsm_ip, self.dest_hsm_ip]
        for src_partition_serial, dest_partition_serial, partition_password in self.src_dest_serials:
            if 'lunaclient' in self.luna_dir:
                config_file = util.generate_luna_53_config(self.client_name, hsm_ips, {self.group_label: [src_partition_serial, dest_partition_serial]})
                util.write_to_file(self.std_conf_path, config_file)
                proc = subprocess.Popen([os.path.join(self.luna_dir, 'bin', 'vtl'), 'haAdmin', 'synchronize', '-group', self.group_label, '-password', partition_password], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                config_file = util.generate_luna_51_config(self.client_name, hsm_ips, {self.group_label: [src_partition_serial, dest_partition_serial]})
                util.write_to_file(self.std_conf_path, config_file)
                proc = subprocess.Popen([os.path.join(self.luna_dir, 'bin', 'vtl'), 'haAdmin', '-synchronize', '-group', self.group_label, '-password', partition_password], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            reader = self.reader(self.src_hsm_ip)
            src_object_count = reader.count_partition_objects(src_partition_serial)
            reader = self.reader(self.dest_hsm_ip)
            dest_object_count = reader.count_partition_objects(dest_partition_serial)
            if src_object_count == dest_object_count:
                logger.warn('Replicated keys from the partition {0} to {1}'.format(src_partition_serial, dest_partition_serial))
            else:
                logger.warn('The VTL command failed to replicate the keys from the partition {0} to {1}. This may have happened for the following reasons:\n1. The two partitions have different passwords.\n2. The two partitions have different domains.'.format(src_partition_serial, dest_partition_serial))

        self.synchronizedHsms = True

    def clone_client_configuration(self):
        '''
        Clone the client configuration of the source HSM to the destination
        '''
        logger.info("Cloning the client configuration")

        reader = self.reader(self.src_hsm_ip)
        clients = reader.get_clients()
        for client_label in clients:
            try:
                certificate_fingerprint = reader.get_client_fingerprint(client_label)
                client_desc = self.cloudhsm.describe_client(fingerprint=certificate_fingerprint)

                try:
                    temp_client_cert_path = '{0}.pem'.format(client_label)
                    util.write_to_file(temp_client_cert_path, util.rebuild_cert(client_desc['Certificate']))
                    self.register_client_on_hsm(self.dest_hsm_ip, client_label, temp_client_cert_path)

                    src_partitions = reader.get_client_partitions(client_label)
                    for src_partition_label in src_partitions:
                        if len(src_partition_label) == 20 and src_partition_label.startswith('hapg') and src_partition_label.endswith(self.src_hsm_serial):
                            dest_partition_label = src_partition_label[:13] + '_' + self.dest_hsm_serial
                        else:
                            dest_partition_label = src_partition_label
                        self.assign_partition_to_client(self.dest_hsm_ip, client_label, partition_label=dest_partition_label)
                except Exception:
                    logger.exception('Failed to register the client')
                finally:
                    os.remove(temp_client_cert_path)
            except Exception:
                logger.exception('Unable to find the client certificate')

    def revoke_partition_and_remove_client(self):
        '''
        Revoke partitions from the temporary client and remove it
        '''
        logger.info ("Revoking partitions from the temporary client and removing it")

        for src_partition_serial in self.src_partition_info.keys():
            self.revoke_partition_from_client(self.src_hsm_ip, self.client_name, src_partition_serial)
        self.remove_client_from_hsm(self.src_hsm_ip, self.client_name)

        for dest_partition_serial in self.dest_partition_info.keys():
            self.revoke_partition_from_client(self.dest_hsm_ip, self.client_name, dest_partition_serial)
        self.remove_client_from_hsm(self.dest_hsm_ip, self.client_name)

    def delete_temp_client(self):
        '''
        Delete the temporary client
        '''
        logger.info("Deleting temporary client %s", self.client_name)

        try:
            os.remove(os.path.join(self.luna_dir, 'cert', 'client', self.client_name + '.pem'))
        finally:
            os.remove(os.path.join(self.luna_dir, 'cert', 'client', self.client_name + 'Key.pem'))
