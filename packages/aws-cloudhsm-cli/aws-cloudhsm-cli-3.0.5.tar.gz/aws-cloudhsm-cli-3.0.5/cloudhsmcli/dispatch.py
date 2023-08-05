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


'''
This module implements the various subcommands.
'''
import cloudhsmcli.api as api
import cloudhsmcli.util as util
from cloudhsmcli.hsm_worker import HsmWorker
from cloudhsmcli.hsm_initializer import HsmInitializer
from cloudhsmcli.hapg_adder import HapgAdder
from cloudhsmcli.hapg_remover import HapgRemover
from cloudhsmcli.client_registerer import ClientRegisterer
from cloudhsmcli.client_deregisterer import ClientDeregisterer
from cloudhsmcli.hapg_cloner import HapgCloner
from cloudhsmcli.hsm_cloner import HsmCloner
from cloudhsmcli import __version__
import json, sys, os, time, datetime, subprocess, shutil
import logging
from device_connections.hsm_credential_provider import HsmCredentialProvider
from getpass import getpass

logger = logging.getLogger("cloudhsmcli.dispatch")

def _lift_aws_args(args_map):
    '''
    Extract common arguments used to connect to AWS.
    This modifies its main argument!
    '''
    aws = {}
    aws['region'] = args_map.pop('aws_region')
    for arg in ('aws_access_key_id', 'aws_secret_access_key'):
        aws[arg] = args_map.pop(arg, None)
    aws['host'] = args_map.pop('aws_host', None)
    port = args_map.pop('aws_port', None)
    if port is not None:
        aws['port'] = int(port)
    for key in aws.keys():
        if aws[key] is None:
            del aws[key]
    return aws

def _pretty_print(result):
    '''
    Print results to STDOUT in an aesthetically pleasing way.
    '''
    json.dump(result, sys.stdout, indent=4, sort_keys=True)
    print >>sys.stdout

def _align_message(message):
    lines = []
    current_line = ""
    for word in message.split():
        if len(current_line + word) > 80:
            lines.append(current_line[:-1])
            current_line = word + " "
        else:
            current_line = current_line + word + " "
    lines.append(current_line[:-1])
    return "\n".join(lines)

def _ominous_warning(message):
    prompt = """
################################################################################
                              CloudHSM CLI Tools WARNING
--------------------------------------------------------------------------------
{0}
--------------------------------------------------------------------------------
Enter y to continue, anything else to cancel:""".format(_align_message(message))
    choice = raw_input(prompt).lower()
    if choice in ['y', 'Y']:
        return
    else:
        raise RuntimeError("Canceled at warning prompt")

def add_hsm_to_hapg(hapg_arn, hsm_arn, partition_password, cloning_domain, so_password, **kw):
    '''
    Add an HSM to an hapg.
    '''
    aws_creds = _lift_aws_args(kw)

    adder = HapgAdder(hapg_arn=hapg_arn, hsm_arn=hsm_arn, partition_password=partition_password,
                      cloning_domain=cloning_domain, aws_creds=aws_creds, so_password=so_password)
    data = adder.run()
    _pretty_print(data)

def add_tag_to_resource(resource_arn, key, value, **kw):
    '''
    Add tags to resource.
    '''
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    data = conn.add_tag_to_resource(resource_arn, key, value)
    _pretty_print(data)

def clone_hapg(src_hapg_arn, dest_hapg_arn, hapg_password, override, **kw):
    '''
    Clone a group to another group.
    '''
    if not override:
        _ominous_warning("""Running this command will create temporary config files that may disrupt
                            HSM-backed applications running on this server. Stop any applications that use
                            HSMs before proceeding, or run this command from a different server that doesn't
                            have any HSM-backed applications.""")
    aws_creds = _lift_aws_args(kw)
    cloner = HapgCloner(src_hapg_arn=src_hapg_arn, dest_hapg_arn=dest_hapg_arn, hapg_password=hapg_password, aws_creds=aws_creds)
    data = cloner.run()
    _pretty_print(data)

def clone_hsm(src_hsm_arn, dest_hsm_arn, so_password, override, **kw):
    '''
    Clone an HSM to another HSM.
    '''
    if not override:
        _ominous_warning("""Running this command will create temporary config files that may disrupt
                            HSM-backed applications running on this server. Stop any applications that use
                            HSMs before proceeding, or run this command from a different server that doesn't
                            have any HSM-backed applications.""")
    aws_creds = _lift_aws_args(kw)
    cloner = HsmCloner(src_hsm_arn=src_hsm_arn, dest_hsm_arn=dest_hsm_arn, so_password=so_password, aws_creds=aws_creds)
    data = cloner.run()
    _pretty_print(data)

def create_client(certificate_file, **kw):
    '''
    Create a client.
    '''
    aws_specific = _lift_aws_args(kw)
    certificate = certificate_file.read()

    conn = api.connect(**aws_specific)
    data = conn.create_client(certificate)
    _pretty_print(data)

def create_hapg(group_label, **kw):
    '''
    Creates a high availability partition group.
    '''
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    response = conn.create_hapg(group_label)
    _pretty_print(response)

def create_hsm(subnet_id, ssh_public_key_file, iam_role_arn, hsm_ip=None, external_id=None, syslog_ip=None, fips_certified=False, software_version="5.3.5", **kw):
    '''
    Creates an HSM.
    '''
    prompt = """
#################################################################################################
                              CloudHSM CLI Tools WARNING
-------------------------------------------------------------------------------------------------
Continuing with this command will result in a one-time charge of $5,000 to your AWS account!
If you want to try the CloudHSM service for free, please refer to:
    https://aws.amazon.com/cloudhsm/free-trial/
If you're unsure, please consult the user guide:
    https://docs.aws.amazon.com/cloudhsm/latest/userguide/provisioning-hsms.html
-------------------------------------------------------------------------------------------------
Type 5000 to proceed, anything else to cancel:"""
    choice = raw_input(prompt).lower()
    if choice != '5000':
        raise RuntimeError("Canceled at warning prompt")
    else:
        print("""
If you accidentally provisioned an HSM and want to request a refund, please consult the user
guide: https://docs.aws.amazon.com/cloudhsm/latest/userguide/provisioning-hsms.html""")

    aws_specific = _lift_aws_args(kw)
    ssh_public_key = ssh_public_key_file.read()

    conn = api.connect(**aws_specific)
    data = conn.create_hsm(subnet_id=subnet_id, ssh_public_key=ssh_public_key.strip(),
                           iam_role_arn=iam_role_arn, hsm_ip=hsm_ip,
                           external_id=external_id, syslog_ip=syslog_ip,
                           fips_certified=fips_certified, software_version=software_version)
    _pretty_print(data)

def delete_client(client_arn, **kw):
    '''
    Delete a client.
    '''
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    data = conn.delete_client(client_arn)
    _pretty_print(data)

def delete_hapg(hapg_arn, override, **kw):
    '''
    Deletes a high availability partition group.
    '''
    if not override:
        _ominous_warning("""Running this command will delete the given HAPG object. Any key material on the
                            HSM(s) in the group will not be deleted. To delete key material from HSM(s),
                            first use the 'remove-hsm-from-hapg' command.""")
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    response = conn.delete_hapg(hapg_arn)
    _pretty_print(response)

def delete_hsm(hsm_arn, override, **kw):
    '''
    Deletes a CloudHSM.
    '''
    if not override:
        _ominous_warning("""Running this command will delete the given CloudHSM instance if and only if the
                            HSM is zeroized. If the HSM is not zeroized, the delete operation will fail and
                            you will continue to be charged for the HSM until you delete it successfully.""")
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    response = conn.delete_hsm(hsm_arn)
    _pretty_print(response)

def deregister_client_from_hapg(client_arn, hapg_arn, **kw):
    '''
    Deregister a client from a group.
    '''
    aws_creds = _lift_aws_args(kw)
    deregisterer = ClientDeregisterer(client_arn=client_arn, hapg_arn=hapg_arn, aws_creds=aws_creds)
    data = deregisterer.run()
    _pretty_print(data)

def describe_client(client_arn=None, fingerprint=None, **kw):
    '''
    Describe a client.
    '''
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    description = conn.describe_client(client_arn, fingerprint)
    _pretty_print(description)

def describe_hapg(hapg_arn, **kw):
    '''
    Describe an HAPG.
    '''
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    description = conn.describe_hapg(hapg_arn)
    _pretty_print(description)

def describe_hsm(hsm_arn, **kw):
    '''
    Describe an HSM.
    '''
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    description = conn.describe_hsm(hsm_arn)
    _pretty_print(description)

def get_client_configuration(client_arn, hapg_arns, cert_directory, config_directory, **kw):
    '''
    Get configuration files for the client setup.
    '''
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)

    hsm_ips = []
    group_partition_serials = {}

    hsm_data = conn.list_hsms()
    all_hsms = hsm_data['HsmList']
    for hapg_arn in hapg_arns:
        hapg_desc = conn.describe_hapg(hapg_arn)
        group_partition_serials[hapg_desc['Label']] = hapg_desc['PartitionSerialList']
        for partition_serial in hapg_desc['PartitionSerialList']:
            for hsm_arn in all_hsms:
                hsm_desc = conn.describe_hsm(hsm_arn)
                if partition_serial.startswith(hsm_desc['SerialNumber']):
                    hsm_ips.append(hsm_desc['EniIp'])
                    all_hsms.remove(hsm_arn)

    client_desc = conn.describe_client(client_arn=client_arn)

    if 'lunaclient' in cert_directory:
        config_file = util.generate_luna_53_config(client_desc['Label'], hsm_ips, group_partition_serials)
    elif 'lunasa' in cert_directory:
        config_file = util.generate_luna_51_config(client_desc['Label'], hsm_ips, group_partition_serials)
    elif 'lunaclient' in util.find_luna_dir():
        config_file = util.generate_luna_53_config(client_desc['Label'], hsm_ips, group_partition_serials)
    else:
        config_file = util.generate_luna_51_config(client_desc['Label'], hsm_ips, group_partition_serials)

    util.write_to_file(os.path.join(config_directory, 'Chrystoki.conf'), config_file)

    worker = HsmWorker()
    for hsm_ip in hsm_ips:
        worker.scp_server_cert_from_hsm(hsm_ip, os.path.join(cert_directory, 'CAFile.pem'))

    print "The configuration file has been copied to {0}".format(config_directory)
    print "The server certificate has been copied to {0}".format(cert_directory)

def initialize_hsm(hsm_arn, cloning_domain, label, so_password, **kw):
    '''
    Initialize an HSM.
    '''
    aws_creds = _lift_aws_args(kw)
    initializer = HsmInitializer(hsm_arn=hsm_arn, cloning_domain=cloning_domain,
                                 label=label, aws_creds=aws_creds, so_password=so_password)
    data = initializer.run()
    _pretty_print(data)

def list_clients(**kw):
    '''
    List the clients in this account.
    '''
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    data = conn.list_clients()
    _pretty_print(data)

def list_hapgs(**kw):
    '''
    List the HAPGs in this account.
    '''
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    data = conn.list_hapgs()
    _pretty_print(data)

def list_hsms(**kw):
    '''
    List the HSMs in this account.
    '''
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    data = conn.list_hsms()
    _pretty_print(data)

def list_tags_for_resource(resource_arn, **kw):
    '''
    List the tags for resource.
    '''
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    data = conn.list_tags_for_resource(resource_arn)
    _pretty_print(data)

def modify_hsm(hsm_arn, override, subnet_id=None, iam_role_arn=None, hsm_ip=None,
               external_id=None, syslog_ip=None, **kw):
    '''
    Modifies an HSM.
    '''
    if not override:
        _ominous_warning("""Running this command will cause this HSM to be unavailable
                            for up to 15 minutes. Before proceeding, you should ensure
                            any HSM-backed applications that are dependent on this HSM
                            are stopped or properly configured for High Availability.
                            See http://docs.aws.amazon.com/cloudhsm/latest/gsg/ha-best-practices.html
                            for more information""")
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    data = conn.modify_hsm(hsm_arn=hsm_arn, subnet_id=subnet_id, iam_role_arn=iam_role_arn, eni_ip=hsm_ip, external_id=external_id, syslog_ip=syslog_ip)
    _pretty_print(data)

def register_client_to_hapg(client_arn, hapg_arn, **kw):
    '''
    Register a client to a group.
    '''
    aws_creds = _lift_aws_args(kw)
    registerer = ClientRegisterer(client_arn=client_arn, hapg_arn=hapg_arn, aws_creds=aws_creds)
    data = registerer.run()
    _pretty_print(data)

def remove_hsm_from_hapg(hapg_arn, hsm_arn, override, so_password, **kw):
    '''
    Remove an HSM from an hapg.
    '''
    if not override:
        _ominous_warning("""Running this command will delete the partition on the given HSM from the given
                            HAPG. This will irrevocably delete the keys on the deleted partition.""")

    aws_creds = _lift_aws_args(kw)
    remover = HapgRemover(hapg_arn=hapg_arn, hsm_arn=hsm_arn, aws_creds=aws_creds, so_password=so_password)
    data = remover.run()
    _pretty_print(data)

def remove_tags_from_resource(resource_arn, keys, **kw):
    '''
    Remove the tags from resource.
    '''
    aws_specific = _lift_aws_args(kw)
    conn = api.connect(**aws_specific)
    data = conn.remove_tags_from_resource(resource_arn, keys)
    _pretty_print(data)

def version(*args, **kw):
    '''
    Display the CloudHSM CLI version info
    '''
    _pretty_print({"Version": __version__})
