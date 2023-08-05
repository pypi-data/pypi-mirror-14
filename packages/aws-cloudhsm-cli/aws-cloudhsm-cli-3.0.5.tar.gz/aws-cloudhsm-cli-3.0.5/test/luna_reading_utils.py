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

parsed_info = {'syslog_info': {'remote_hosts': ['54.208.217.148', '10.0.106.107'], 'running': True}, 'ntp_info': {'running': True, 'enabled': True, 'remote_servers': ['127.127.1.0', '54.208.217.148']}, 'software_version': '5.1.3-1', 'firmware_version': '6.2.1', 'hostname': 'hsm-2-1-2-6', 'zeroized': True, 'route_table': [{'Genmask': '255.255.255.0', 'Use': '0', 'Iface': 'eth0', 'Flags': 'U', 'Metric': '0', 'Destination': '192.168.101.0', 'Ref': '0', 'Gateway': '0.0.0.0'}, {'Genmask': '255.255.255.0', 'Use': '0', 'Iface': 'eth1', 'Flags': 'UG', 'Metric': '0', 'Destination': '10.0.106.0', 'Ref': '0', 'Gateway': '172.16.106.1'}, {'Genmask': '255.255.255.0', 'Use': '0', 'Iface': 'eth1', 'Flags': 'U', 'Metric': '0', 'Destination': '172.16.106.0', 'Ref': '0', 'Gateway': '0.0.0.0'}, {'Genmask': '0.0.0.0', 'Use': '0', 'Iface': 'eth0', 'Flags': 'UG', 'Metric': '0', 'Destination': '0.0.0.0', 'Ref': '0', 'Gateway': '192.168.101.1'}], 'interface_info': [{'status_tokens': ['UP', 'BROADCAST', 'RUNNING', 'MULTICAST'], 'net_mask': '255.255.255.0', 'broadcast': '192.168.101.255', 'mac_address': '00:15:B2:A4:A7:C2', 'interface': 'eth0', 'ip_address': '192.168.101.16'}, {'status_tokens': ['UP', 'BROADCAST', 'RUNNING', 'MULTICAST'], 'net_mask': '255.255.255.0', 'broadcast': '172.16.106.255', 'mac_address': '00:15:B2:A4:A7:C3', 'interface': 'eth1', 'ip_address': '172.16.106.16'}], 'serial_number': '156155', 'snmp_info': {'notifications': [{'username': 'test_user', 'ip_address': '10.0.106.107', 'port': '162'}], 'running': True, 'enabled': True, 'users': ['aws', 'test_user']}, 'users': [{'username': 'admin', 'status': 'enabled', 'radius': 'no', 'roles': 'admin'}, {'username': 'monitor', 'status': 'enabled', 'radius': 'no', 'roles': 'monitor'}, {'username': 'operator', 'status': 'disabled', 'radius': 'no', 'roles': 'operator'}], 'clients': ['client_name', 'client name with spaces'], "installed_packages": ['configurator-5.1.0-25', 'lunacm-5.1.0-25', 'lunausb-2.3.1-4', 'lush-utils-5.1.0-25', 'pedClient-5.1.0-25', 'salogin-5.1.0-25', 'sysstatd-5.1.0-25', 'fwupG4-realcert-5.0.0-32', 'sa_cmd_processor-5.1.3-1', 'setup-2.5.58-7.el5', 'basesystem-8.0-5.1.1.el5.centos', 'nash-5.1.19.6-54', 'tzdata-2009k-1.el5', 'cracklib-dicts-2.8.9-3.3', 'glibc-2.5-42']}

raw_hostname = """
[hsm-2-1-2-6] lunash:>
[hsm-2-1-2-6] lunash:>
"""

raw_interface_info = """
[hsm-2-1-2-6] lunash:>status interface

eth0      Link encap:Ethernet  HWaddr 00:15:B2:A4:A7:C2  
          inet addr:192.168.101.16  Bcast:192.168.101.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:5957353 errors:0 dropped:0 overruns:0 frame:0
          TX packets:13245144 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:1842964477 (1.7 GiB)  TX bytes:2245163157 (2.0 GiB)
          Interrupt:58 Memory:fb4c0000-fb4e0000 

eth1      Link encap:Ethernet  HWaddr 00:15:B2:A4:A7:C3  
          inet addr:172.16.106.16  Bcast:172.16.106.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:143232 errors:0 dropped:0 overruns:0 frame:0
          TX packets:162801 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:14257870 (13.5 MiB)  TX bytes:19854007 (18.9 MiB)
          Interrupt:169 Memory:fb6e0000-fb700000 

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:29 errors:0 dropped:0 overruns:0 frame:0
          TX packets:29 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:3025 (2.9 KiB)  TX bytes:3025 (2.9 KiB)


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_interface_info_with_inet6 = """
[hsm-2-1-2-6] lunash:>status interface

eth0      Link encap:Ethernet  HWaddr 00:15:B2:A4:A7:C2  
          inet addr:192.168.101.16  Bcast:192.168.101.255  Mask:255.255.255.0
          inet6 addr: fe80::215:b2ff:fea4:5d54/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:5957353 errors:0 dropped:0 overruns:0 frame:0
          TX packets:13245144 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:1842964477 (1.7 GiB)  TX bytes:2245163157 (2.0 GiB)
          Interrupt:58 Memory:fb4c0000-fb4e0000 

eth1      Link encap:Ethernet  HWaddr 00:15:B2:A4:A7:C3  
          inet addr:172.16.106.16  Bcast:172.16.106.255  Mask:255.255.255.0
          inet6 addr: fe80::215:b2ff:fea4:5d55/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:143232 errors:0 dropped:0 overruns:0 frame:0
          TX packets:162801 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:14257870 (13.5 MiB)  TX bytes:19854007 (18.9 MiB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:29 errors:0 dropped:0 overruns:0 frame:0
          TX packets:29 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:3025 (2.9 KiB)  TX bytes:3025 (2.9 KiB)


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

parsed_interface_info = [{'interface': 'eth0', 'mac_address': '00:15:B2:A4:A7:C2', 'ip_address': '192.168.101.16', 'broadcast': '192.168.101.255', 'net_mask': '255.255.255.0', 'status_tokens': ['UP', 'BROADCAST', 'RUNNING', 'MULTICAST']}, {'interface': 'eth1', 'mac_address': '00:15:B2:A4:A7:C3', 'ip_address': '172.16.106.16', 'broadcast': '172.16.106.255', 'net_mask': '255.255.255.0', 'status_tokens': ['UP', 'BROADCAST', 'RUNNING', 'MULTICAST']}]

raw_ntp_server_list = """
[hsm-2-1-2-6] lunash:>sysconf ntp li

=================================================================
NTP Servers:
server 127.127.1.0
server 54.208.217.148
=================================================================

Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_ntp_status_running = """
[hsm-2-1-2-6] lunash:>sysconf ntp status


NTP is running

NTP is enabled

Peers:
==============================================================================
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*LOCAL(0)        .LOCL.          10 l   42   64  377    0.000    0.000   0.001
 54.208.217.148  .INIT.          16 u    - 1024    0    0.000    0.000   0.000
==============================================================================

Associations:
==============================================================================

ind assid status  conf reach auth condition  last_event cnt
===========================================================
  1 48268  963a   yes   yes  none  sys.peer    sys_peer  3
  2 48269  8011   yes    no  none    reject    mobilize  1
==============================================================================

NTP Time:
==============================================================================
ntp_gettime() returns code 0 (OK)
  time d63616fd.db500000  Tue, Nov 19 2013 11:57:33.856, (.856689),
  maximum error 42672 us, estimated error 0 us
ntp_adjtime() returns code 0 (OK)
  modes 0x0 (),
  offset 0.000 us, frequency 0.000 ppm, interval 1 s,
  maximum error 42672 us, estimated error 0 us,
  status 0x1 (PLL),
  time constant 2, precision 1.000 us, tolerance 512 ppm,
==============================================================================


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_ntp_status_not_running = """
[hsm-2-1-2-6] lunash:>sysconf ntp status


NTP is not running

NTP is disabled

Peers:
==============================================================================
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*LOCAL(0)        .LOCL.          10 l   42   64  377    0.000    0.000   0.001
 54.208.217.148  .INIT.          16 u    - 1024    0    0.000    0.000   0.000
==============================================================================

Associations:
==============================================================================

ind assid status  conf reach auth condition  last_event cnt
===========================================================
  1 48268  963a   yes   yes  none  sys.peer    sys_peer  3
  2 48269  8011   yes    no  none    reject    mobilize  1
==============================================================================

NTP Time:
==============================================================================
ntp_gettime() returns code 0 (OK)
  time d63616fd.db500000  Tue, Nov 19 2013 11:57:33.856, (.856689),
  maximum error 42672 us, estimated error 0 us
ntp_adjtime() returns code 0 (OK)
  modes 0x0 (),
  offset 0.000 us, frequency 0.000 ppm, interval 1 s,
  maximum error 42672 us, estimated error 0 us,
  status 0x1 (PLL),
  time constant 2, precision 1.000 us, tolerance 512 ppm,
==============================================================================


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

parsed_ntp_info_running = {'remote_servers': ['127.127.1.0', '54.208.217.148'], 'running': True, 'enabled': True}
parsed_ntp_info_not_running = {'remote_servers': ['127.127.1.0', '54.208.217.148'], 'running': False, 'enabled': False}

raw_route_table = """
[hsm-2-1-2-6] lunash:>network route show


Manually configured routes
10.0.106.0/24 via 172.16.106.1 metric 0 dev eth1

Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
192.168.101.0   0.0.0.0         255.255.255.0   U     0      0        0 eth0
10.0.106.0      172.16.106.1    255.255.255.0   UG    0      0        0 eth1
172.16.106.0    0.0.0.0         255.255.255.0   U     0      0        0 eth1
0.0.0.0         192.168.101.1   0.0.0.0         UG    0      0        0 eth0


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

parsed_route_table = [{'Genmask': '255.255.255.0', 'Use': '0', 'Iface': 'eth0', 'Flags': 'U', 'Metric': '0', 'Destination': '192.168.101.0', 'Ref': '0', 'Gateway': '0.0.0.0'}, {'Genmask': '255.255.255.0', 'Use': '0', 'Iface': 'eth1', 'Flags': 'UG', 'Metric': '0', 'Destination': '10.0.106.0', 'Ref': '0', 'Gateway': '172.16.106.1'}, {'Genmask': '255.255.255.0', 'Use': '0', 'Iface': 'eth1', 'Flags': 'U', 'Metric': '0', 'Destination': '172.16.106.0', 'Ref': '0', 'Gateway': '0.0.0.0'}, {'Genmask': '0.0.0.0', 'Use': '0', 'Iface': 'eth0', 'Flags': 'UG', 'Metric': '0', 'Destination': '0.0.0.0', 'Ref': '0', 'Gateway': '192.168.101.1'}]

empty_route_table = """
[hsm-2-1-2-6] lunash:>network route show


Manually configured routes
10.0.106.0/24 via 172.16.106.1 metric 0 dev eth1

Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface


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

raw_hsm_status_unzeroized = """
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

raw_hsm_status_zeroized_53 = """
[hsm-2-1-2-6] lunash:>hsm show


   Appliance Details:
   ==================
   Software Version:                5.3.0-11

   HSM Details: 
   ============
   HSM Label:                          no label
   Serial #:                           157541
   Firmware:                           6.10.2
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
"""

raw_hsm_status_unzeroized_no_partitions_53 = """
[hsm-2-1-2-6] lunash:>hsm show


   Appliance Details:
   ==================
   Software Version:                5.3.0-11

   HSM Details: 
   ============
   HSM Label:                          HAIL_SANTA
   Serial #:                           157541
   Firmware:                           6.10.2
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
"""

raw_snmp_notification_list = """
[hsm-2-1-2-6] lunash:>sysconf snmp notification list                                                                                           


SNMP Notification Targets:
--------------------------
10.0.106.107:162 "test_user" SHA


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_snmp_status_not_running = """
[hsm-2-1-2-6] lunash:>sysconf snmp show


SNMP is not running

SNMP is disabled


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_snmp_status_running = """
[hsm-2-1-2-6] lunash:>sysconf snmp show


SNMP is running

SNMP is enabled


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_snmp_user_list = """
[hsm-2-1-2-6] lunash:>sysconf snmp user list                                                                                                        


SNMP Users:
-----------
aws
test_user


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

parsed_snmp_info_running = {'users': ['aws', 'test_user'], 'running': True, 'enabled': True, 'notifications': [{'ip_address': '10.0.106.107', 'port': '162', 'username': 'test_user'}]}
parsed_snmp_info_not_running = {'users': ['aws', 'test_user'], 'running': False, 'enabled': False, 'notifications': [{'ip_address': '10.0.106.107', 'port': '162', 'username': 'test_user'}]}

raw_package_list = """
[hsm-2-1-2-5] lunash:>package list


RPM LIST (SYSTEM)
-------------------
configurator-5.1.0-25
lunacm-5.1.0-25
lunausb-2.3.1-4
lush-utils-5.1.0-25
pedClient-5.1.0-25
salogin-5.1.0-25
sysstatd-5.1.0-25
fwupG4-realcert-5.0.0-32
sa_cmd_processor-5.1.3-1
setup-2.5.58-7.el5
basesystem-8.0-5.1.1.el5.centos
nash-5.1.19.6-54
tzdata-2009k-1.el5
cracklib-dicts-2.8.9-3.3
glibc-2.5-42


RPM LIST (SOFTWARE)
-------------------

Command Result : 0 (Success)
[hsm-2-1-2-5] lunash:>
"""

raw_package_list_515 = """
[hsm-2-1-2-6] lunash:>package list


RPM LIST (SYSTEM)
-------------------
libcryptoki-5.1.0-25
vkd-5.1.0-25
certmonitord-5.1.0-25
lunalogd-5.1.0-25
lush-standard-users-5.1.0-25
oamp-5.1.0-25
release-SA-5.1.5-2
snmp-5.1.0-17
uhd-5.1.0-25
fwupK6-bare-5.1.0-8
basesystem-8.0-5.1.1.el5.centos
nash-5.1.19.6-54
readline-5.1-3.el5
mkinitrd-5.1.19.6-54
vtsd-5.1.2-2
lush-base-5.1.0-25
configurator-5.1.0-25
lunacm-5.1.0-25
lush-utils-5.1.0-25
pedClient-5.1.0-25
salogin-5.1.0-25
sysstatd-5.1.5-2
sa_cmd_processor-5.1.3-1

RPM LIST (SOFTWARE)
-------------------

Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_syslog_status_running = """
[hsm-2-1-2-6] lunash:>service status syslog

   syslog is running


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_syslog_status_not_running = """
[hsm-2-1-2-6] lunash:>service status syslog

   syslog is not running


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_syslog_remote_host_list_51 = """
[hsm-3-1-1-10] lunash:>syslog remotehost list


List of syslog remote hosts:

54.208.217.148
10.0.106.107

Command Result : 0 (Success)
[hsm-3-1-1-10] lunash:>
"""

raw_syslog_remote_host_list_53 = """
[hsm-2-1-2-6] lunash:>syslog remotehost list

Remote logging server(s):
=========================

  54.208.217.148:514, udp
  10.0.106.107:514, udp

Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

parsed_syslog_info_not_running = {'remote_hosts': ['54.208.217.148', '10.0.106.107'], 'running': False}
parsed_syslog_info_running = {'remote_hosts': ['54.208.217.148', '10.0.106.107'], 'running': True}

raw_user_list = """
[hsm-2-1-2-6] lunash:>user list

                   Users       Roles      Status      RADIUS
    --------------------    --------    --------    --------
                   admin       admin     enabled          no
                 monitor     monitor     enabled          no
                operator    operator    disabled          no

Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""
parsed_user_list = [{'username': 'admin', 'roles': 'admin', 'status': 'enabled', 'radius': 'no'}, {'username': 'monitor', 'roles': 'monitor', 'status': 'enabled', 'radius': 'no'}, {'username': 'operator', 'roles': 'operator', 'status': 'disabled', 'radius': 'no'}]

raw_client_list_full = """
[hsm-2-1-2-6] lunash:>client list

registered client 1: client_name
registered client 2: client name with spaces


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

raw_client_list_empty = """
[hsm-2-1-2-6] lunash:>client list

No clients are registered.


Command Result : 0 (Success)
[hsm-2-1-2-6] lunash:>
"""

parsed_client_list = ['client_name', 'client name with spaces']

raw_partition_list_full = """
[hsm-4-1-1-9] lunash:>partition list

                                                      Storage (bytes)
                                                ----------------------------
 Partition    Name                     Objects     Total      Used      Free
 ===========================================================================
 157826004    testPar1                       0    102701         0    102701
 157826011    testPar2                       2    102701         0    102701


Command Result : 0 (Success)
[hsm-4-1-1-9] lunash:>
"""

raw_partition_list_empty = """
[hsm-4-1-1-9] lunash:>partition list

   There are no partitions.



Command Result : 0 (Success)
[hsm-4-1-1-9] lunash:>
"""

parsed_partition_list = [('157826004', 'testPar1'), ('157826011', 'testPar2')]

raw_client_partition_list_full = """
[hsm-4-1-1-9] lunash:>client show -c client1


ClientID:     client1
Hostname:     client1
Partitions:   "clientPar1", "clientPar2", "clientPar3"


Command Result : 0 (Success)
[hsm-4-1-1-9] lunash:>
"""

raw_client_partition_list_empty = """
[hsm-4-1-1-9] lunash:>client show -c client2


ClientID:     client2
Hostname:     client2
HTL Required: no
OTT Expiry:   n/a
Partitions:   <none>


Command Result : 0 (Success)
[hsm-4-1-1-9] lunash:>
"""

raw_client_partition_list_error = """
[hsm-4-1-1-9] lunash:>client show -c client3


Error:  'client show' failed. (C000040A : RC_OBJECT_NOT_IN_LIST)

Error:  Specified client does not exist.


Command Result : 65535 (Luna Shell execution)
[hsm-4-1-1-9] lunash:>
"""

parsed_client_partition_list = ['clientPar1', 'clientPar2', 'clientPar3']

raw_client_fingerprint = """
[hsm-1-2-1-16] lunash:>client fingerprint -c client1



Certificate fingerprint: D9:9E:25:B3:A9:68:06:50:8F:C4:90:FC:E5:50:E2:BC


Command Result : 0 (Success)
[hsm-1-2-1-16] lunash:>
"""

raw_client_fingerprint_error = """
[hsm-1-2-1-16] lunash:>client fingerprint -c client2


Error:  The client you specified does not exist.
        Use 'client list' to list all available clients.
Error:  'client fingerprint' failed. (C000040A : RC_OBJECT_NOT_IN_LIST)


Command Result : 65535 (Luna Shell execution)
[hsm-1-2-1-16] lunash:>
"""

parsed_client_fingerprint = 'D9:9E:25:B3:A9:68:06:50:8F:C4:90:FC:E5:50:E2:BC'
