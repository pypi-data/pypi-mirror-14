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

#This regex term should match any allowable single term (such as a user name, hostname, client name, etc...) in an Luna command.  It should represent all valid characters the Luna accepts as part of a term.
luna_term_regex = r"[a-zA-Z0-9\-_\.]+"

#Regex for an valid IPv4 address
ipv4_regex = r"((\d{1,3})(\.)){3}(\d{1,3})"

luna_shell_prompt = 'lunash:>'

#Regex is useful for send_command_sequence where tokenizer is not used
generic_success_regex = r"Command Result : 0 \(Success\)\s+\[.*?\] lunash:>"

# This handles any command result without resorting to a timeout
tolerant_completion_regex = r"Command Result : [0-9]+ \(.+?\)"

expected_regenerate_server_cert_output = r"""
        WARNING !!  This command will overwrite the current server certificate and private key.
        All clients will have to add this server again with this new certificate.
        If you are sure that you wish to proceed, then type 'proceed', otherwise type 'quit'
        """

expected_regenerate_server_cert_proceed_output = r"""
        Proceeding...
        'sysconf regenCert' successful. NTLS must be \(re\)started before clients can connect.
        Please use the 'ntls show' command to ensure that NTLS is bound to an appropriate network device or IP address/hostname
        for the network device\(s\) NTLS should be active on. Use 'ntls bind' to change this binding if necessary.
        Command Result : 0 \(Success\)
        """

expected_ntls_bind_eth0_output = r"""Success: NTLS binding.*Command Result : 0 \(Success\)"""

expected_register_client_output = r"""
        'client register' successful.
        Command Result : 0 \(Success\)
        """

expected_assign_partition_to_client_output = r"""
        'client assignPartition' successful.
        Command Result : 0 \(Success\)
        """

expected_revoke_partition_from_client_output = r"""
        'client revokePartition' successful.
        Command Result : 0 \(Success\)
        """

expected_set_user_password_output = "Enter new password: "

expected_set_user_password_confirm_output = "Re-type new password: "

expected_add_user_role_output = r"""
        User {0} was successfully modified.
        Command Result : 0 \(Success\)
        """.format(luna_term_regex)

expected_register_public_key_output = r"""
        Public key added
        Command Result : 0 \(Success\)
        """

expected_enable_key_auth_output = r"""
        Public key authentication enabled
        Command Result : 0 \(Success\)
        """

generic_success_output = "Command Result : 0 \(Success\)"

expected_syslog_cleanup_output = r"""
        Deleting log files ...
        restart the rsyslogd service if it's running
        Command Result : 0 \(Success\)
        """

expected_reboot_output = r"""
        The system is going down for reboot NOW!
        Reboot commencing
        Command Result : 0 \(Success\)
        """

expected_remove_client_prompt = r"""
CAUTION:  Are you sure you wish to delete client named:
            {0}
          Type 'proceed' to delete the client, or 'quit'
          to quit now.
""".format(luna_term_regex)

expected_set_hostname_output = r"""
Success: Hostname {0} set.
""".format(luna_term_regex)

expected_initialize_hsm_output = r"""
        'hsm init' successful.
        Command Result : 0 \(Success\)
        """

expected_hsm_login_prompt = r"""
        Please enter the HSM Administrators' password:
        """

expected_hsm_login_output = r"""
        'hsm login' successful.
        Command Result : 0 \(Success\)
        """

expected_hsm_login_last_attempt_warning = r"Caution:  This is your LAST available HSM Admin login attempt"

expected_failed_hsm_login_not_zeroized_output = r"A00000 : LUNA_RET_UM_PIN_INCORRECT"

expected_failed_hsm_login_zeroized_output = r"30000F : LUNA_RET_SO_LOGIN_FAILURE_THRESHOLD"

expected_create_partition_output = r"""
        'partition create' successful.
        Command Result : 0 \(Success\)
        """

expected_delete_partition_output = r"""
        'partition delete' successful.
        Command Result : 0 \(Success\)
        """

expected_ntp_host_added_output = r"NTP server 'server {0}' added.".format(ipv4_regex)

expected_ntp_host_removed_output = r"NTP server {0} deleted".format(ipv4_regex)

expected_syslog_host_added_output=r"{0} added successfully".format(ipv4_regex)

expected_syslog_restarted_output=generic_success_regex

expected_snmp_restarted_output=generic_success_regex

expected_ntls_started_output=generic_success_regex

expected_snmp_enabled_output=r"SNMP is enabled\s.*\s.*\s*{0}".format(generic_success_regex)

# snmp return messages can have various forms, reduce expectation to only check for generic_success_regex.
expected_snmp_host_added_output=r"SNMP notification target information added.*{0}".format(generic_success_regex)

expected_snmp_user_added_output=r"SNMP user account information added\s*{0}".format(generic_success_regex)

# Due to the need to expedite a fix, we're not validating this.
# expected_ntls_ipcheck_disable_output=r"NTLS client source IP validation(?: is already)? disabled?\s*{0}".format(generic_success_regex)
expected_ntls_ipcheck_disable_output = tolerant_completion_regex

expected_patch_hsm_succeeded_output=r"SOFTWARE UPDATE COMPLETED!"

raw_hsm_status_unzeroized_with_data = """
[hsm-2-1-2-6] lunash:>hsm show


   Appliance Details:
   ==================
   Software Version:                5.3.0-11

   HSM Details:
   ============
   HSM Label:                          patchLuna
   Serial #:                           157541
   Firmware:                           6.10.1
   Hardware Model:                     Luna K6
   Authentication Method:              Password
   HSM Admin login status:             Not Logged In
   HSM Admin login attempts left:      3 before HSM zeroization!
   RPV Initialized:                    No
   Audit Role Initialized:             No
   Remote Login Initialized:           No
   Manually Zeroized:                  No

   Partitions created on HSM:
   ==========================
   Partition: 157541008,     Name: patchPart

   FIPS 140-2 Operation:
   =====================
   The HSM is NOT in FIPS 140-2 approved operation mode.

   HSM Storage Information:
   ========================
   Maximum HSM Storage Space (Bytes):   2097152
   Space In Use (Bytes):                104857
   Free Space Left (Bytes):             1992295


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_hsm_status_unzeroized_3_attempts_remaining = """
[hsm-2-1-2-6] lunash:>hsm show


   Appliance Details:
   ==================
   Software Version:                5.3.0-11

   HSM Details:
   ============
   HSM Label:                          patchLuna
   Serial #:                           157541
   Firmware:                           6.10.1
   Hardware Model:                     Luna K6
   Authentication Method:              Password
   HSM Admin login status:             Not Logged In
   HSM Admin login attempts left:      3 before HSM zeroization!
   RPV Initialized:                    No
   Audit Role Initialized:             No
   Remote Login Initialized:           No
   Manually Zeroized:                  No

   Partitions created on HSM:
   ==========================
   Partition: 157541008,     Name: patchPart

   FIPS 140-2 Operation:
   =====================
   The HSM is NOT in FIPS 140-2 approved operation mode.

   HSM Storage Information:
   ========================
   Maximum HSM Storage Space (Bytes):   2097152
   Space In Use (Bytes):                0
   Free Space Left (Bytes):             2097152


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_hsm_status_unzeroized_2_attempts_remaining = """
[hsm-2-1-2-6] lunash:>hsm show


   Appliance Details:
   ==================
   Software Version:                5.3.0-11

   HSM Details:
   ============
   HSM Label:                          patchLuna
   Serial #:                           157541
   Firmware:                           6.10.1
   Hardware Model:                     Luna K6
   Authentication Method:              Password
   HSM Admin login status:             Not Logged In
   HSM Admin login attempts left:      2 before HSM zeroization!
   RPV Initialized:                    No
   Audit Role Initialized:             No
   Remote Login Initialized:           No
   Manually Zeroized:                  No

   Partitions created on HSM:
   ==========================
   Partition: 157541008,     Name: patchPart

   FIPS 140-2 Operation:
   =====================
   The HSM is NOT in FIPS 140-2 approved operation mode.

   HSM Storage Information:
   ========================
   Maximum HSM Storage Space (Bytes):   2097152
   Space In Use (Bytes):                0
   Free Space Left (Bytes):             2097152


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_hsm_status_unzeroized_1_attempt_remaining = """
[hsm-2-1-2-6] lunash:>hsm show


   Appliance Details:
   ==================
   Software Version:                5.3.0-11

   HSM Details:
   ============
   HSM Label:                          patchLuna
   Serial #:                           157541
   Firmware:                           6.10.1
   Hardware Model:                     Luna K6
   Authentication Method:              Password
   HSM Admin login status:             Not Logged In
   HSM Admin login attempts left:      1 before HSM zeroization!
   RPV Initialized:                    No
   Audit Role Initialized:             No
   Remote Login Initialized:           No
   Manually Zeroized:                  No

   Partitions created on HSM:
   ==========================
   Partition: 157541008,     Name: patchPart

   FIPS 140-2 Operation:
   =====================
   The HSM is NOT in FIPS 140-2 approved operation mode.

   HSM Storage Information:
   ========================
   Maximum HSM Storage Space (Bytes):   2097152
   Space In Use (Bytes):                0
   Free Space Left (Bytes):             2097152


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_hsm_status_zeroized = """
[hsm-2-1-2-5] lunash:>hsm show


   Appliance Details:
   ==================
   Software Version:                5.1.0-25

   HSM Details:
   ============
   HSM Label:                          no label
   Serial #:                           156155
   Firmware:                           6.2.1
   Hardware Model:                     Luna K6
   Authentication Method:              Password
   HSM Admin login status:             Not Logged In
   HSM Admin login attempts left:      HSM IS ZEROIZED !!!!
   RPV Initialized:                    No
   Manually Zeroized:                  No

   Partitions created on HSM:
   ==========================
   There are no partitions.


   FIPS 140-2 Operation:
   =====================
   The HSM is NOT in FIPS 140-2 approved operation mode.

   HSM Storage Information:
   ========================
   Maximum HSM Storage Space (Bytes):   2097152
   Space In Use (Bytes):                0
   Free Space Left (Bytes):             2097152


Command Result : 0 (Success)
[hsm-2-1-2-5] lunash:>
"""

raw_output_ntp_host_added="""
NTP server 'server 12.3.4.5' added.
WARNING !! Server '12.3.4.5' added without authentication.
NTP is enabled
Shutting down ntpd:                                        [  OK  ]
Starting ntpd:                                             [  OK  ]
Please wait to see the result ......

NTP is running
===========================================================
NTP Associations Status:

ind assid status  conf reach auth condition  last_event cnt
===========================================================
1 14047  963a   yes   yes  none  sys.peer    sys_peer  3
2 14048  8011   yes    no  none    reject    mobilize  1
3 14049  8011   yes    no  none    reject    mobilize  1
4 14050  8011   yes    no  none    reject    mobilize  1
===========================================================
Please look at the ntp log to see any potential problem.

Command Result : 0 (Success)
"""

raw_output_ntp_host_removed="""
NTP server 12.3.4.5 deleted
NTP is enabled
Shutting down ntpd:                                        [  OK  ]
Starting ntpd:                                             [  OK  ]
Please wait to see the result ......

NTP is running
===========================================================
NTP Associations Status:

ind assid status  conf reach auth condition  last_event cnt
===========================================================
  1 61641  963a   yes   yes  none  sys.peer    sys_peer  3
  2 61642  8011   yes    no  none    reject    mobilize  1
  3 61643  8011   yes    no  none    reject    mobilize  1
  4 61644  8011   yes    no  none    reject    mobilize  1
  5 61645  8011   yes    no  none    reject    mobilize  1
===========================================================
Please look at the ntp log to see any potential problem.

Command Result : 0 (Success)
"""

raw_output_syslog_host_removed="""


1.2.3.4 deleted successfully
Please restart syslog with <service restart syslog> command
to stop logs to be sent to 1.2.3.4

Command Result : 0 (Success)
"""

raw_output_syslog_host_removed_53="""

Shutting down kernel logger:                               [  OK  ]
Shutting down system logger:                               [  OK  ]
Starting system logger:                                    [  OK  ]
Starting kernel logger:                                    [  OK  ]
Saving firewall rules to /etc/sysconfig/iptables:          [  OK  ]

Command Result : 0 (Success)
"""

raw_output_syslog_host_added="""
10.2.106.67 added successfully
Please restart syslog with <service restart syslog> command
Make sure syslog service is started on 10.2.106.67 with -r option

Command Result : 0 (Success)
"""

raw_output_syslog_host_added_53="""
[hsm-2-1-2-5] lunash:>syslog remotehost add -host 192.168.0.101
Shutting down kernel logger: [ OK ]
Shutting down system logger: [ OK ]
Starting system logger: [ OK ]
Starting kernel logger: [ OK ]
Saving firewall rules to /etc/sysconfig/iptables: [ OK ]
192.168.0.101 added successfully
Make sure the rsyslog service on 192.168.0.101 is properly configured to receive the logs
Command Result : 0 (Success)
[hsm-2-1-2-5] lunash:>
"""

raw_output_syslog_service_restarted="""

Shutting down kernel logger:                               [  OK  ]
Shutting down system logger:                               [  OK  ]
Starting system logger:                                    [  OK  ]
Starting kernel logger:                                    [  OK  ]

Command Result : 0 (Success)
"""

raw_output_snmp_service_restarted="""
Stopping snmpd:                                            [FAILED]
Starting snmpd:                                            [  OK  ]

Command Result : 0 (Success)
[hsm-3-1-1-19] lunash:>
"""

raw_output_snmp_enabled="""

SNMP is enabled
Starting snmpd:                                            [  OK  ]
SNMP is started

Command Result : 0 (Success)
[hsm-2-1-2-5] lunash:>
"""

raw_output_snmp_host_added="""

SNMP notification target information added
snmpd: send_trap: Timeout
NET-SNMP version 5.5

Command Result : 0 (Success)
"""

raw_output_snmp_user_added="""

SNMP user account information added

Command Result : 0 (Success)
"""

raw_output_patch_hsm_succeeded="""


Command succeeded:  decrypt package

Command succeeded:  verify package certificate

Command succeeded:  verify package signature
Preparing packages for installation...
lunasa_update-5.1.3-1
Running update script

Version file found.
BEGINNING UPDATE......

UNPACKING UPDATE FILES......

VERIFYING SOFTWARE PACKAGES......

1...Passed

INSTALLING SOFTWARE PACKAGES......

1...Passed



RESTARTING SERVICES......

SOFTWARE UPDATE COMPLETED!

The system MUST now be rebooted for the changes to take effect.
Please ensure all client connections are terminated prior to rebooting the
system.
To reboot, use the command "sysconf appliance reboot".

Update Completed


Command Result : 0 (Success)
[hsm-3-4-1-17] lunash:>
"""

snmp_disabled_status="""

SNMP is not running

SNMP is disabled


Command Result : 0 (Success)
[hsm-2-3-2-1] lunash:>
"""

snmp_enabled_status="""

SNMP is running

SNMP is enabled


Command Result : 0 (Success)
[hsm-2-3-2-1] lunash:>
"""

ntp_enabled_status="""

NTP is not running

NTP is enabled

Peers:
==============================================================================
ntpq: read: Connection refused
==============================================================================

Associations:
==============================================================================
ntpq: read: Connection refused
==============================================================================

NTP Time:
==============================================================================
ntp_gettime() returns code 0 (OK)
  time d99b32e4.35d51000  Wed, Sep  9 2015 22:36:20.210, (.210282),
  maximum error 117776 us, estimated error 16 us
ntp_adjtime() returns code 0 (OK)
  modes 0x0 (),
  offset 0.000 us, frequency 0.000 ppm, interval 1 s,
  maximum error 117776 us, estimated error 16 us,
  status 0x1 (PLL),
  time constant 3, precision 1.000 us, tolerance 512 ppm,
==============================================================================


Command Result : 0 (Success)
[hsm-2-3-2-1] lunash:>
"""

ntp_disabled_status="""

NTP is running

NTP is disabled

Peers:
==============================================================================
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
 10.0.10.7       74.120.8.2       3 u    2   64    1    0.395  -146593   0.001
==============================================================================

Associations:
==============================================================================

ind assid status  conf reach auth condition  last_event cnt
===========================================================
  1 30976  9024   yes   yes  none    reject   reachable  2
==============================================================================

NTP Time:
==============================================================================
ntp_gettime() returns code 0 (OK)
  time d99b3419.2506d000  Wed, Sep  9 2015 22:41:29.144, (.144635),
  maximum error 11792 us, estimated error 16 us
ntp_adjtime() returns code 0 (OK)
  modes 0x0 (),
  offset 0.000 us, frequency 0.000 ppm, interval 1 s,
  maximum error 11792 us, estimated error 16 us,
  status 0x1 (PLL),
  time constant 3, precision 1.000 us, tolerance 512 ppm,
==============================================================================


Command Result : 0 (Success)
[hsm-2-3-2-1] lunash:>
"""
ntp_enabled_and_running_status="""
NTP is running

NTP is enabled

Peers:
==============================================================================
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
 10.0.10.7       74.120.8.2       3 u    8   64    1    0.471  -146593   0.000
==============================================================================

Associations:
==============================================================================

ind assid status  conf reach auth condition  last_event cnt
===========================================================
  1 64242  9024   yes   yes  none    reject   reachable  2
==============================================================================

NTP Time:
==============================================================================
ntp_gettime() returns code 0 (OK)
  time d99b331b.d5431000  Wed, Sep  9 2015 22:37:15.833, (.833055),
  maximum error 14864 us, estimated error 16 us
ntp_adjtime() returns code 0 (OK)
  modes 0x0 (),
  offset 0.000 us, frequency 0.000 ppm, interval 1 s,
  maximum error 14864 us, estimated error 16 us,
  status 0x1 (PLL),
  time constant 3, precision 1.000 us, tolerance 512 ppm,
==============================================================================


Command Result : 0 (Success)
[hsm-2-3-2-1] lunash:>
"""
