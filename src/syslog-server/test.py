#!/bin/env python3

from rfc3164 import RFC3164
from datetime import datetime

a = RFC3164.fromMessage("<189>506: *Mar 18 06:30:17: %SYS-5-CONFIG_I: Configured from console by vty0 (192.168.1.101)", "192.168.1.3")

print("PRI = %d" % a.PRI.getPRIvalue())
print("SEVERITY = %s(%d)" % (a.PRI.getSeverity(str), a.PRI.getSeverity()))
print("FACILITY = %s(%d)" % (a.PRI.getFacility(str), a.PRI.getFacility()))
print("HEADER = %s" % str(a.HEAD))
print("MSG = %s" % a.MSG)

print("======================================================================")

a = RFC3164.fromMessage("<86>Jan 29 14:54:21 R430-GP9RMK2-Debian10 sudo: pam_unix(sudo:session): session closed for user root", "192.168.1.51")

print("PRI = %d" % a.PRI.getPRIvalue())
print("SEVERITY = %s(%d)" % (a.PRI.getSeverity(str), a.PRI.getSeverity()))
print("FACILITY = %s(%d)" % (a.PRI.getFacility(str), a.PRI.getFacility()))
print("HEADER = %s" % str(a.HEAD))
print("MSG = %s" % a.MSG)

print("======================================================================")

a = RFC3164.fromMessage("<30>Jan 29 15:10:10 ppp: [wan_link0] PPPoE connection timeout after 9 seconds", "192.168.1.4", datetime(2021,1,29,15,10,9,695))

print("PRI = %d" % a.PRI.getPRIvalue())
print("SEVERITY = %s(%d)" % (a.PRI.getSeverity(str), a.PRI.getSeverity()))
print("FACILITY = %s(%d)" % (a.PRI.getFacility(str), a.PRI.getFacility()))
print("HEADER = %s" % str(a.HEAD))
print("MSG = %s" % a.MSG)

print("======================================================================")

a = RFC3164.fromObject({"PRI": 134, "HEAD": {"timestamp": "Jan 30 00:47:54", "hostname": "192.168.1.4", "process": "filterlog"}, "MSG": ": 58,,,11000,lagg0.101,match,block,in,4,0x10,,64,0,0,DF,17,udp,356,0.0.0.0,255.255.255.255,68,67,336"})

print("PRI = %d" % a.PRI.getPRIvalue())
print("SEVERITY = %s(%d)" % (a.PRI.getSeverity(str), a.PRI.getSeverity()))
print("FACILITY = %s(%d)" % (a.PRI.getFacility(str), a.PRI.getFacility()))
print("HEADER = %s" % str(a.HEAD))
print("MSG = %s" % a.MSG)
