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


"""
This module implements some utility methods
"""

import os, sys, logging, time, random, subprocess

logger = logging.getLogger("cloudhsmcli.util")

def write_to_file(path, data):
    '''
    Write some data to a file
    '''
    with open(path, 'w') as fh:
        fh.write(data)

def move_a_file(source, dest):
    '''
    Move a file on disk. It can be used for backing up files and restoring files
    '''
    logger.info("Moving {0} to {1}".format(source, dest))
    if os.path.isfile(source):
        if os.path.isfile(dest):
            os.remove(dest)
        os.rename(source, dest)
        logger.info("{0} is renamed as {1}".format(source, dest))

def file_has_read_permission(file_path):
    '''
    Check if user executing CLI command has read permission to file path
    '''
    return os.access(file_path, os.R_OK)

def file_has_write_permission(file_path):
    '''
    Check if user executing CLI command has write permission to file path
    '''
    return os.access(file_path, os.W_OK)

def concatenate_files(source, dest):
    '''
    Concatenate the content of a file into another
    '''
    logger.info("Concatenate {0} to {1}".format(source, dest))
    with open(source, 'r') as outfile:
        with open(dest, 'a') as infile:
            infile.writelines(outfile.readlines())
            logger.info("The content in {0} is appended to {1}".format(source, dest))

def find_luna_dir():
    '''
    Returns the luna client directory
    '''
    if os.path.isdir('/usr/safenet/lunaclient'):
        return '/usr/safenet/lunaclient'
    elif os.path.isdir('/usr/lunasa'):
        return '/usr/lunasa'
    else:
        raise RuntimeError("It requires the installation of Luna client software to perform this operation.")

def scp_file_to_remote_destination(hostname, source_path, destination_path, logger=None):
    '''
    Launches scp to log in to a remote host and upload a file.
    '''
    scp_args = [source_path, "{0}:{1}".format(hostname, destination_path)]
    _perform_scp_operation(scp_args, logger)

def scp_file_from_remote_source(hostname, source_path, destination_path, logger=None):
    '''
    Launches scp to log in to a remote host and download a file.
    '''
    scp_args = ["{0}:{1}".format(hostname, source_path), destination_path]
    _perform_scp_operation(scp_args, logger)

def _perform_scp_operation(scp_args, logger):
    '''
    Performs an scp operation given a valid SSH session.
    '''
    scp_command = ['scp', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null'] + scp_args
    scp_string = " ".join(scp_command)
    if logger:
        logger.info("scp-ing file with command: {0}".format(scp_string))

    proc = subprocess.Popen(scp_command, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError('scp file transfer failed')

    if logger:
        logger.info("scp file transfer completed successfully")

def rebuild_cert(cert):
    '''
    Ensures that cert is a string, no unicode
    '''
    stripped_cert = str(cert)
    stripped_cert = stripped_cert.translate(None, "\n\r")
    begin_tag = stripped_cert[:27]
    end_tag = stripped_cert[-25:]
    stripped_cert = stripped_cert[27:-25]
    new_cert = [begin_tag]

    #This formats the middle blob in rows 64 chars long
    for line in xrange(0, len(stripped_cert), 64):
        new_cert.append(stripped_cert[line:line+64])

    new_cert.append(end_tag)

    return ''.join(line + "\n" for line in new_cert)

def generate_luna_51_config(client_label, hsm_ips, group_partition_serials):
    '''
    Generates a Luna 5.1 client configuration file
    '''
    config_file = ''

    # For now, assume that the client environment is Linux 64-bit
    config_file += 'Chrystoki2 = {\n'
    config_file += '   LibUNIX = /usr/lib/libCryptoki2_64.so;\n'
    config_file += '}\n\n'

    # Hardcode the default settings here because they are unlikely to change
    config_file += 'Luna = {\n'
    config_file += '   DefaultTimeOut=500000;\n'
    config_file += '   PEDTimeout1=100000;\n'
    config_file += '   PEDTimeout2=100000;\n'
    config_file += '   PEDTimeout3=10000;\n'
    config_file += '   KeypairGenTimeOut=2700000;\n'
    config_file += '   CloningCommandTimeOut=300000;\n'
    config_file += '}\n\n'

    config_file += 'CardReader = {\n'
    config_file += '   RemoteCommand=1;\n'
    config_file += '}\n\n'

    # For now, assume that customers place the files at the specified locations
    config_file += 'LunaSA Client = {\n'
    config_file += '   ClientPrivKeyFile = /usr/lunasa/cert/client/{0}Key.pem;\n'.format(client_label)
    config_file += '   ClientCertFile = /usr/lunasa/cert/client/{0}.pem;\n'.format(client_label)
    config_file += '   NetClient = 1;\n'
    config_file += '   ServerCAFile = /usr/lunasa/cert/server/CAFile.pem;\n'
    config_file += '   SSLConfigFile = /usr/lunasa/bin/openssl.cnf;\n'
    config_file += '   ReceiveTimeout = 20000;\n'

    # List the IP addresses of HSMs
    counter = 0
    for hsm_ip in hsm_ips:
        config_file += '   ServerPort{:02d} = 1792;\n'.format(counter)
        config_file += '   ServerName{0:02d} = {1};\n'.format(counter, hsm_ip)
        counter += 1;
    config_file += '}\n\n'

    # List the information of all groups
    config_file += 'VirtualToken = {\n'
    counter = 0;
    for group_label, partition_serials in group_partition_serials.items():
        config_file += '   VirtualToken{:02d}Members = '.format(counter)
        comma = False;
        for partition_serial in partition_serials:
            if comma:
                config_file += ','
            else:
                comma = True;
            config_file += partition_serial
        config_file += ';\n'
        # Use a random number as the group serial number
        config_file += '   VirtualToken{0:02d}SN = {1:010d};\n'.format(counter, random.randint(0,9999999999))
        config_file += '   VirtualToken{0:02d}Label = {1};\n'.format(counter, group_label)
        counter += 1;
    config_file += '}\n\n'

    # Turn on synchronization by default for all group(s)
    config_file += 'HASynchronize = {\n'
    for group_label in group_partition_serials.keys():
        config_file += '   {0} = 1;\n'.format(group_label)
    config_file += '}\n\n'

    # Use recommended settings here
    config_file += 'HAConfiguration = {\n'
    config_file += '   reconnAtt = -1;\n'
    config_file += '   AutoReconnectInterval = 60;\n'
    config_file += '   HAOnly = 1;\n'
    config_file += '}\n'

    return config_file

def generate_luna_53_config(client_label, hsm_ips, group_partition_serials):
    '''
    Generates a Luna 5.3 client configuration file
    '''
    config_file = ''

    config_file += 'Chrystoki2 = {\n'
    config_file += '   LibUNIX = /usr/lib/libCryptoki2.so;\n'
    config_file += '   LibUNIX64 = /usr/lib/libCryptoki2_64.so;\n'
    config_file += '}\n\n'

    # Hardcode the default settings here because they are unlikely to change
    config_file += 'Luna = {\n'
    config_file += '  DefaultTimeOut = 500000;\n'
    config_file += '  PEDTimeout1 = 100000;\n'
    config_file += '  PEDTimeout2 = 100000;\n'
    config_file += '  PEDTimeout3 = 10000;\n'
    config_file += '  KeypairGenTimeOut = 2700000;\n'
    config_file += '  CloningCommandTimeOut = 300000;\n'
    config_file += '}\n\n'

    config_file += 'CardReader = {\n'
    config_file += '  RemoteCommand = 1;\n'
    config_file += '}\n'

    # For now, assume that customers place the files at the specified locations
    config_file += 'LunaSA Client = {\n'
    config_file += '   ReceiveTimeout = 20000;\n'
    config_file += '   SSLConfigFile = /usr/safenet/lunaclient/bin/openssl.cnf;\n'
    config_file += '   ClientPrivKeyFile = /usr/safenet/lunaclient/cert/client/{0}Key.pem;\n'.format(client_label)
    config_file += '   ClientCertFile = /usr/safenet/lunaclient/cert/client/{0}.pem;\n'.format(client_label)
    config_file += '   ServerCAFile = /usr/safenet/lunaclient/cert/server/CAFile.pem;\n'
    config_file += '   NetClient = 1;\n'
    config_file += '   HtlDir = /usr/safenet/lunaclient/htl/;\n'

    # List the IP addresses of HSMs
    counter = 0
    for hsm_ip in hsm_ips:
        config_file += '   ServerName{0:02d} = {1};\n'.format(counter, hsm_ip)
        config_file += '   ServerPort{:02d} = 1792;\n'.format(counter)
        config_file += '   ServerHtl{:02d} = 0;\n'.format(counter)
        counter += 1
    config_file += '}\n'

    # Set the directory of Luna client utilities
    config_file += 'Misc = {\n'
    config_file += '   ToolsDir = /usr/safenet/lunaclient/bin;\n'
    config_file += '}\n'

    counter = 0
    # List the information of all groups
    config_file += 'VirtualToken = {\n'
    for group_label, partition_serials in group_partition_serials.items():
        config_file += '   VirtualToken{0:02d}Label = {1};\n'.format(counter, group_label)
        # Use a random number as the group serial number
        config_file += '   VirtualToken{0:02d}SN = {1:010d};\n'.format(counter, random.randint(0,9999999999))
        config_file += '   VirtualToken{:02d}Members = '.format(counter)
        comma = False;
        for partition_serial in partition_serials:
            if comma:
                config_file += ','
            else:
                comma = True;
            config_file += partition_serial
        config_file += ';\n'
        counter += 1
    config_file += '}\n'

    # Turn on synchronization by default for all groups
    config_file += 'HASynchronize = {\n'
    for group_label in group_partition_serials.keys():
        config_file += '   {0} = 1;\n'.format(group_label)
    config_file += '}\n'

    # Use recommended settings here
    config_file += 'HAConfiguration = {\n'
    config_file += '   reconnAtt = -1;\n'
    config_file += '   AutoReconnectInterval = 60;\n'
    config_file += '   HAOnly = 1;\n'
    config_file += '}\n'

    return config_file
