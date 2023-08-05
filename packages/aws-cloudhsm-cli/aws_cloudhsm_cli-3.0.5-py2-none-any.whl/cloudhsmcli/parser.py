#!/usr/bin/python
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

import argparse
import logging
from cloudhsmcli import dispatch
import ConfigParser
import sys, os, errno
import re

class CloudHSMCLI(object):
    """
    Command-line interface to CloudHSM API and HSMs from AWS CloudHSM
    """
    def add_add_hsm_to_hapg_subparser(self, subparsers):
        add_hsm_to_hapg_subparser = subparsers.add_parser('add-hsm-to-hapg', help="Add an HSM to an HAPG. In event of failure, retry; duplicate partitions will not be created.")
        add_hsm_to_hapg_subparser.set_defaults(**self.defaults)
        add_hsm_to_hapg_subparser.add_argument('-H', "--hsm-arn", help="ARN describing HSM to add to the HAPG", metavar='ARN', action='store', required=self._check_arg_not_parsed('hsm_arn'), dest="hsm_arn")
        add_hsm_to_hapg_subparser.add_argument('-G', "--hapg-arn", help="ARN describing the HAPG to which the HSM will be added", metavar='ARN', action='store', required=self._check_arg_not_parsed('hapg_arn'), dest="hapg_arn")
        add_hsm_to_hapg_subparser.add_argument("--so-password", help="The security officer password", metavar='PASSWORD', action='store', required=self._check_arg_not_parsed('so_password'))
        add_hsm_to_hapg_subparser.add_argument("--partition-password", help="The password to set for created partition. Must be same for all partitions (or HSMs) in HAPG", metavar='PASSWORD', action='store', required=self._check_arg_not_parsed('partition_password'))
        add_hsm_to_hapg_subparser.add_argument('-d', "--cloning-domain", help="The cloning domain to set for created partition. Must be same for all partitions (or HSMs) in HAPG", metavar='DOMAIN', action='store', required=self._check_arg_not_parsed('cloning_domain'))
        self.add_aws_args(add_hsm_to_hapg_subparser)
        return add_hsm_to_hapg_subparser

    def add_add_tag_to_resouce_subparser(self, subparsers):
        add_tag_to_resource_subparser = subparsers.add_parser('add-tag-to-resource', help="Add tag to CloudHSM resource. Use AWS CLI to to add multiple tags in one command.")
        add_tag_to_resource_subparser.add_argument("--resource-arn", help="The ARN identifying the resource in CloudHSM. Service currently only supports HSM ARNs.", metavar='ARN', action='store', required=self._check_arg_not_parsed('resource_arn'))
        add_tag_to_resource_subparser.add_argument("--key", help="The key for the tag", metavar='KEY', action='store', required=self._check_arg_not_parsed('key'))
        add_tag_to_resource_subparser.add_argument("--value", help="The value for the tag", metavar='VALUE', action='store', required=self._check_arg_not_parsed('value'))
        add_tag_to_resource_subparser.set_defaults(**self.defaults)
        self.add_aws_args(add_tag_to_resource_subparser)
        return add_tag_to_resource_subparser

    def add_clone_hapg_subparser(self, subparsers):
        clone_ha_subparser = subparsers.add_parser('clone-hapg', help="Clone a high availability partition group (HAPG)")
        clone_ha_subparser.set_defaults(**self.defaults)
        clone_ha_subparser.add_argument('-S', "--src-hapg-arn", help="The ARN of the HAPG to clone from", metavar='ARN', action='store', required=self._check_arg_not_parsed('src_hapg_arn'))
        clone_ha_subparser.add_argument('-D', "--dest-hapg-arn", help="The ARN of the HAPG to clone to", metavar='ARN', action='store', required=self._check_arg_not_parsed('dest_hapg_arn'))
        clone_ha_subparser.add_argument("--hapg-password", help="The password of the member partitions", metavar='PASSWORD', action='store', required=self._check_arg_not_parsed('hapg_password'))
        clone_ha_subparser.add_argument("-y", "--force", help="Override safety check message", action="store_true", dest="override", required=False, default=False)
        self.add_aws_args(clone_ha_subparser)
        return clone_ha_subparser

    def add_clone_hsm_subparser(self, subparsers):
        clone_hsm_subparser = subparsers.add_parser('clone-hsm', help="Duplicate the group memberships and key material from one HSM on another.")
        clone_hsm_subparser.set_defaults(**self.defaults)
        clone_hsm_subparser.add_argument('-S', "--src-hsm-arn", help="The ARN identifying the HSM you wish to duplicate",
                metavar='ARN', action='store', required=self._check_arg_not_parsed('source_hsm_arn'))
        clone_hsm_subparser.add_argument('-D', "--dest-hsm-arn", help="The ARN identifying the HSM you wish to be the clone",
                metavar='ARN', action='store', required=self._check_arg_not_parsed('source_hsm_arn'))
        clone_hsm_subparser.add_argument("--so-password", help="The security officer password", metavar='PASSWORD', action='store', required=self._check_arg_not_parsed('so_password'))
        clone_hsm_subparser.add_argument("-y", "--force", help="Override safety check message", action="store_true", dest="override", required=False, default=False)
        self.add_aws_args(clone_hsm_subparser)

    def add_create_client_subparser(self, subparsers):
        create_client_subparser = subparsers.add_parser('create-client', help="Create an HSM client.")
        create_client_subparser.set_defaults(**self.defaults)
        create_client_subparser.add_argument('-t', "--certificate-file", help="The Base64-Encoded X.509 v3 certificate associated with the client.",
                                             metavar='CERTIFICATE', action='store', required=self._check_arg_not_parsed('certificate_file'), type=argparse.FileType('r'))
        self.add_aws_args(create_client_subparser)
        return create_client_subparser

    def add_create_hapg_subparser(self, subparsers):
        create_ha_subparser = subparsers.add_parser('create-hapg', help="Create a high availability partition group (HAPG)")
        create_ha_subparser.set_defaults(**self.defaults)
        create_ha_subparser.add_argument('-l', "--group-label", help="The label of the high availability partition group (HAPG)", metavar='LABEL', action='store', required=self._check_arg_not_parsed('group_label'))
        self.add_aws_args(create_ha_subparser)
        return create_ha_subparser

    def add_create_hsm_subparser(self, subparsers):
        create_hsm_subparser = subparsers.add_parser('create-hsm', help="Create an uninitialized HSM instance in the CloudHSM service.")
        create_hsm_subparser.set_defaults(**self.defaults)
        create_hsm_subparser.add_argument('-n', "--subnet-id", help="The subnet in your VPC in which to place the HSM.", action='store', required=self._check_arg_not_parsed('subnet_id'))
        create_hsm_subparser.add_argument("--ssh-public-key-file",
                                          help="The ssh public key to upload to the manager account.",
                                          action='store',
                                          required=self._check_arg_not_parsed('ssh_public_key_file'),
                                          type=argparse.FileType('r'))
        create_hsm_subparser.add_argument("--iam-role-arn", help="The ARN of an IAM role to enable the CloudHSM service to construct an ENI on your behalf.", action='store', required=self._check_arg_not_parsed('iam_role_arn'))
        create_hsm_subparser.add_argument("--external-id", help="Your IAM role may have this attribute; if you used the CloudFormation template you can disregard.", action='store', required=False)
        create_hsm_subparser.add_argument("--fips-certified", help="Whether or not you would like FIPS-certified firmware to be run on the HSM.  Default: False", action="store_true", required=False, default=False)
        create_hsm_subparser.add_argument("--hsm-ip", help="The desired IP address of the HSM; this will appear as an Elastic Network Interface (ENI).", action='store', required=False)
        create_hsm_subparser.add_argument("--software-version", help="The SafeNet Luna software version you wish the provisioned HSM to run.  Current valid options are: '5.1.5', '5.3.5'.  Default: '5.3.5'.", action='store', required=False, default='5.3.5')
        create_hsm_subparser.add_argument("--syslog-ip", help="The IP address for the syslog monitoring server.", action='store', required=False)
        self.add_aws_args(create_hsm_subparser)
        return create_hsm_subparser

    def add_delete_client_subparser(self, subparsers):
        delete_client_subparser = subparsers.add_parser('delete-client', help="Delete an HSM client.")
        delete_client_subparser.set_defaults(**self.defaults)
        delete_client_subparser.add_argument('-C', "--client-arn", help="CLIENT ARN", metavar='ARN', action='store', required=self._check_arg_not_parsed('client_arn'))
        self.add_aws_args(delete_client_subparser)
        return delete_client_subparser

    def add_delete_hapg_subparser(self, subparsers):
        delete_ha_subparser = subparsers.add_parser('delete-hapg', help="Delete a high availability partition group (HAPG)")
        delete_ha_subparser.set_defaults(**self.defaults)
        delete_ha_subparser.add_argument('-G', "--hapg-arn", help="The HAPG ARN identifying the high availability partition group to be deleted", metavar='ARN', action='store', required=self._check_arg_not_parsed('hapg_arn'), dest="hapg_arn")
        delete_ha_subparser.add_argument("-y", "--force", help="Override safety check message", action="store_true", dest="override", required=False, default=False)
        self.add_aws_args(delete_ha_subparser)
        return delete_ha_subparser

    def add_delete_hsm_subparser(self, subparsers):
        delete_hsm_subparser = subparsers.add_parser('delete-hsm', help="Delete a CloudHSM, returning the device to AWS")
        delete_hsm_subparser.set_defaults(**self.defaults)
        delete_hsm_subparser.add_argument('-H', "--hsm-arn", help="HSM ARN", metavar='ARN', action='store', required=self._check_arg_not_parsed('hsm_arn'))
        delete_hsm_subparser.add_argument("-y", "--force", help="Override safety check message", action="store_true", dest="override", required=False, default=False)
        self.add_aws_args(delete_hsm_subparser)
        return delete_hsm_subparser

    def add_deregister_client_from_hapg_subparser(self, subparsers):
        deregister_client_from_hapg_subparser = subparsers.add_parser('deregister-client-from-hapg', help="Deregister a client from an HAPG. In event of failure, retry.")
        deregister_client_from_hapg_subparser.set_defaults(**self.defaults)
        deregister_client_from_hapg_subparser.add_argument('-C', "--client-arn", help="ARN describing the client to deregister from the HAPG", metavar='ARN', action='store', required=self._check_arg_not_parsed('client_arn'), dest="client_arn")
        deregister_client_from_hapg_subparser.add_argument('-G', "--hapg-arn", help="ARN describing the HAPG from which the client will be deregistered", metavar='ARN', action='store', required=self._check_arg_not_parsed('hapg_arn'), dest="hapg_arn")
        self.add_aws_args(deregister_client_from_hapg_subparser)
        return deregister_client_from_hapg_subparser

    def add_describe_client_subparser(self, subparsers):
        describe_client_subparser = subparsers.add_parser('describe-client', help="Describe a client by querying CloudHSM")
        describe_client_subparser.set_defaults(**self.defaults)
        describe_client_subparser.add_argument('-C', "--client-arn", help="CLIENT ARN", metavar='ARN', action='store', required=self._check_arg_not_parsed('client_arn'))
        self.add_aws_args(describe_client_subparser)
        return describe_client_subparser

    def add_describe_hapg_subparser(self, subparsers):
        describe_hapg_subparser = subparsers.add_parser('describe-hapg', help="Describe an HAPG by querying CloudHSM")
        describe_hapg_subparser.set_defaults(**self.defaults)
        describe_hapg_subparser.add_argument('-G', "--hapg-arn", help="HAPG ARN", metavar='ARN', action='store', required=self._check_arg_not_parsed('hapg_arn'))
        self.add_aws_args(describe_hapg_subparser)
        return describe_hapg_subparser

    def add_describe_hsm_subparser(self, subparsers):
        describe_hsm_subparser = subparsers.add_parser('describe-hsm', help="Describe an HSM by querying CloudHSM")
        describe_hsm_subparser.set_defaults(**self.defaults)
        describe_hsm_subparser.add_argument('-H', "--hsm-arn", help="HSM ARN", metavar='ARN', action='store', required=self._check_arg_not_parsed('hsm_arn'))
        self.add_aws_args(describe_hsm_subparser)
        return describe_hsm_subparser

    def add_get_client_configuration_subparser(self, subparsers):
        get_client_configuration_subparser = subparsers.add_parser('get-client-configuration', help="Get configuration files for the client setup.")
        get_client_configuration_subparser.set_defaults(**self.defaults)
        get_client_configuration_subparser.add_argument('-C', "--client-arn", help="The ARN identifying the HSM client",
                metavar='ARN', action='store', required=self._check_arg_not_parsed('client_arn'))
        get_client_configuration_subparser.add_argument('-G', "--hapg-arns", help="One or more ARNs identifying the HAPG(s) that are associated with the HSM client",
                metavar='ARN', action='store', nargs='+', required=self._check_arg_not_parsed('hapg_arns'), dest="hapg_arns")
        #need to come up with something better than -f and -F
        get_client_configuration_subparser.add_argument('-f', "--cert-directory",
                help="The directory in which the server certificate will be written",
                metavar='CERT_PATH', action='store', required=False,
                default=os.getcwd())
        get_client_configuration_subparser.add_argument('-F', "--config-directory",
                help="The directory in which the chrystoki.conf file will be written",
                metavar='CONFIG_PATH', action='store', required=False,
                default=os.getcwd())
        self.add_aws_args(get_client_configuration_subparser)
        return get_client_configuration_subparser

    def add_initialize_subparser(self, subparsers):
        initialize_subparser = subparsers.add_parser('initialize-hsm', help="Initial configuration of the HSM. It assumes that you have already called the CloudHSM API to allocate the HSM resource and that you have the resulting HSM ARN.")
        initialize_subparser.set_defaults(**self.defaults)
        initialize_subparser.add_argument('-H', "--hsm-arn", help="The ARN identifying the HSM in CloudHSM", metavar='ARN', action='store', required=self._check_arg_not_parsed('hsm_arn'))
        initialize_subparser.add_argument('-l', "--label", help="The label for the HSM", metavar='LABEL', action='store', required=self._check_arg_not_parsed('label'))
        initialize_subparser.add_argument("--so-password", help="The security officer password", metavar='PASSWORD', action='store', required=self._check_arg_not_parsed('so_password'))
        initialize_subparser.add_argument('-d', "--cloning-domain", help="The cloning domain", metavar='DOMAIN', action='store', required=self._check_arg_not_parsed('cloning_domain'))
        self.add_aws_args(initialize_subparser)
        return initialize_subparser

    def add_list_clients_subparser(self, subparsers):
        list_subparser = subparsers.add_parser('list-clients', help="Returns a list of client-arns for the current user")
        list_subparser.set_defaults(**self.defaults)
        self.add_aws_args(list_subparser)
        return list_subparser

    def add_list_hapgs_subparser(self, subparsers):
        list_subparser = subparsers.add_parser('list-hapgs', help="Returns a list of hapg-arns for the current user")
        list_subparser.set_defaults(**self.defaults)
        self.add_aws_args(list_subparser)
        return list_subparser

    def add_list_hsms_subparser(self, subparsers):
        list_subparser = subparsers.add_parser('list-hsms', help="Returns a list of hsm-arns for the current user")
        list_subparser.set_defaults(**self.defaults)
        self.add_aws_args(list_subparser)
        return list_subparser

    def add_list_tags_for_resouce_subparser(self, subparsers):
        list_tags_for_resource_subparser = subparsers.add_parser('list-tags-for-resource', help="List tags for CloudHSM resource.")
        list_tags_for_resource_subparser.add_argument("--resource-arn", help="The ARN identifying the resource in CloudHSM. Service currently only supports HSM ARNs.", metavar='ARN', action='store', required=self._check_arg_not_parsed('resource_arn'))
        list_tags_for_resource_subparser.set_defaults(**self.defaults)
        self.add_aws_args(list_tags_for_resource_subparser)
        return list_tags_for_resource_subparser

    def add_modify_hsm_subparser(self, subparsers):
        modify_hsm_subparser = subparsers.add_parser('modify-hsm', help="Modifies an HSM instance in the CloudHSM service.")
        modify_hsm_subparser.set_defaults(**self.defaults)
        modify_hsm_subparser.add_argument('-H', "--hsm-arn", help="The ARN identifying the HSM in CloudHSM", metavar='ARN', action='store', required=self._check_arg_not_parsed('hsm_arn'))
        modify_hsm_subparser.add_argument('-n', "--subnet-id", help="The new subnet in your VPC in which to place the HSM.", action='store', required=False)
        modify_hsm_subparser.add_argument("--iam-role-arn", help="The new ARN of an IAM role to enable the CloudHSM service to construct an ENI on your behalf.", action='store', required=False)
        modify_hsm_subparser.add_argument("--hsm-ip", help="The desired IP address of the HSM; this will appear as an Elastic Network Interface (ENI).", action='store', required=False)
        modify_hsm_subparser.add_argument("--external-id", help="Your IAM role may have this attribute; if you used the CloudFormation template you can disregard.", action='store', required=False)
        modify_hsm_subparser.add_argument("--syslog-ip", help="The new IP address for the syslog monitoring server.", action='store', required=False)
        modify_hsm_subparser.add_argument("-y", "--force", help="Override safety check message", action="store_true", dest="override", required=False, default=False)
        self.add_aws_args(modify_hsm_subparser)
        return modify_hsm_subparser

    def add_register_client_to_hapg_subparser(self, subparsers):
        register_client_to_hapg_subparser = subparsers.add_parser('register-client-to-hapg', help="Register a client to an HAPG. In event of failure, retry.")
        register_client_to_hapg_subparser.set_defaults(**self.defaults)
        register_client_to_hapg_subparser.add_argument('-C', "--client-arn", help="ARN describing the client to register to the HAPG", metavar='ARN', action='store', required=self._check_arg_not_parsed('client_arn'), dest="client_arn")
        register_client_to_hapg_subparser.add_argument('-G', "--hapg-arn", help="ARN describing the HAPG to which the client will be registered", metavar='ARN', action='store', required=self._check_arg_not_parsed('hapg_arn'), dest="hapg_arn")
        self.add_aws_args(register_client_to_hapg_subparser)
        return register_client_to_hapg_subparser

    def add_remove_hsm_from_hapg_subparser(self, subparsers):
        remove_hsm_from_hapg_subparser = subparsers.add_parser('remove-hsm-from-hapg', help="Remove an HSM from an HAPG. In event of failure, retry.")
        remove_hsm_from_hapg_subparser.set_defaults(**self.defaults)
        remove_hsm_from_hapg_subparser.add_argument('-H', "--hsm-arn", help="ARN describing HSM to remove from the HAPG", metavar='ARN', action='store', required=self._check_arg_not_parsed('hsm_arn'), dest="hsm_arn")
        remove_hsm_from_hapg_subparser.add_argument('-G', "--hapg-arn", help="ARN describing the HAPG from which the HSM will be removed", metavar='ARN', action='store', required=self._check_arg_not_parsed('hapg_arn'), dest="hapg_arn")
        remove_hsm_from_hapg_subparser.add_argument("--so-password", help="The security officer password", metavar='PASSWORD', action='store', required=self._check_arg_not_parsed('so_password'))
        remove_hsm_from_hapg_subparser.add_argument("-y", "--force", help="Override safety check message", action="store_true", dest="override", required=False, default=False)
        self.add_aws_args(remove_hsm_from_hapg_subparser)
        return remove_hsm_from_hapg_subparser

    def add_remove_tags_from_resouce_subparser(self, subparsers):
        remove_tags_from_resource_subparser = subparsers.add_parser('remove-tags-from-resource', help="Remove tags from CloudHSM resource.")
        remove_tags_from_resource_subparser.add_argument("--resource-arn", help="The ARN identifying the resource in CloudHSM. Service currently only supports HSM ARNs.", metavar='ARN', action='store', required=self._check_arg_not_parsed('resource_arn'))
        remove_tags_from_resource_subparser.add_argument("--keys", help="List of tag keys", metavar='KEY', nargs="+", action='store', required=self._check_arg_not_parsed('key'))
        remove_tags_from_resource_subparser.set_defaults(**self.defaults)
        self.add_aws_args(remove_tags_from_resource_subparser)
        return remove_tags_from_resource_subparser

    def add_version_subparser(self, subparsers):
        version_subparser = subparsers.add_parser('version', help="Display version of CloudHSM CLI")
        version_subparser.set_defaults(**self.defaults)
        return version_subparser

    def add_aws_args(self, subparser):
        subparser.add_argument("-r", "--aws-region", help="The region to connect to, e.g. us-east-1", metavar="REGION", action='store', required=self._check_arg_not_parsed('aws_region'))
        subparser.set_defaults(**self.defaults)
        subparser.add_argument("-k", "--aws-access-key-id", help="The AWS access key id for this AWS account", metavar="ACCESS", action='store')
        subparser.add_argument("-s", "--aws-secret-access-key", help="The AWS secret access key for this AWS account", metavar="SECRET", action='store')
        subparser.add_argument("--aws-host", help="Override the CloudHSM endpoint host", metavar="HOST", action='store')
        subparser.add_argument("--aws-port", help="Override the CloudHSM endpoint port", metavar="PORT", action='store')

    def _check_arg_not_parsed(self, arg):
        return not arg in self.defaults

    def _check_no_args_in_group_parsed(self, args_list):
        for arg in args_list:
            if self.defaults.get(arg):
                return False
        return True

    def _configure_output(self, quiet, verbose):
        if quiet:
            log_level = logging.ERROR
            sys.tracebacklimit = 0
        elif verbose:
            log_level = logging.DEBUG
        else:
            log_level = logging.WARN
            sys.tracebacklimit = 0

        logging.basicConfig(level=log_level, format="%(name)s: %(message)s")

    def _parse_config_file(self, conf_file):
        """
        Parse the configuration file (conf_file) if it exists, and store values in self.defaults
        """
        self.defaults = {}
        if conf_file:
            config = ConfigParser.SafeConfigParser()
            config.read([conf_file])
            for section in config.sections():
                for key, value in config.items(section):
                    if '\n' in value:
                        #Handle multi-line items
                        self.defaults[key] = [line.strip() for line in value.splitlines() if line]
                    else:
                        #Handle single-line items
                        self.defaults[key] = value.strip()

    def _parse_args(self):
        # The config parser is separate so we can run it before the main parser and pass values from the config file as defaults
        conf_parser = argparse.ArgumentParser(add_help=False)
        conf_parser.add_argument("-c", "--conf_file", help="Path to config file", metavar="FILE")
        args, remaining_args = conf_parser.parse_known_args()

        # read the default values in configuration file
        self._parse_config_file(args.conf_file)

        # prepare parser
        parser = argparse.ArgumentParser(description='Command-line interface to CloudHSM API and HSMs from AWS CloudHSM', parents=[conf_parser])
        output_prefs = parser.add_mutually_exclusive_group(required=False)
        output_prefs.add_argument('-q', '--quiet', help="Hide all messages but errors.", dest='quiet', action='store_true')
        output_prefs.add_argument('-v', '--verbose', help="Show all messages including debug.", dest='verbose', action='store_true')

        parser.set_defaults(**self.defaults)

        subparsers = parser.add_subparsers(help='commands', dest='command')

        # add subparsers
        for attr in dir(self):
            if re.match('add_.*_subparser', attr):
                getattr(self, attr)(subparsers)

        # parse args, call function
        return parser.parse_args(remaining_args)

    def run(self):
        opts = self._parse_args()
        self._configure_output(opts.quiet, opts.verbose)

        lib_function = opts.command.replace('-', '_')
        args_dict = vars(opts)

        try:
            getattr(dispatch, lib_function)(**args_dict)
        except EnvironmentError as e:
            try:
                if e.errno == errno.EACCES:
                    exit("Error writing to %s: Permission denied" % e.filename)
                elif e.errno == errno.ENOENT:
                    exit("Error writing to %s: Directory not found" % e.filename)
                else:
                   raise
            except AttributeError:
                pass
