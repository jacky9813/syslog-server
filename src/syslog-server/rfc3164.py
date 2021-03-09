#!/bin/env python3
from datetime import datetime
import re
import socket
from enum import IntEnum, auto

class Severity(IntEnum):
    EMERG = 0
    ALERT = 1
    CRIT = 2
    ERR = 3
    WARNING = 4
    NOTICE = 5
    INFO = 6
    DEBUG = 7
    def __str__(self):
        return self.name.lower()

class Facility(IntEnum):
    KERN = 0
    USER = 1
    MAIL = 2
    DAEMON = 3
    AUTH = 4
    SYSLOG = 5
    LPR = 6
    NEWS = 7
    UUCP = 8
    CRON = 9
    AUTHPRIV = 10
    FTP = 11
    NTP = 12
    SECURITY = 13
    CONSOLE = 14
    SOLARIS_CRON = 15
    LOCAL0 = 16
    LOCAL1 = 17
    LOCAL2 = 18
    LOCAL3 = 19
    LOCAL4 = 20
    LOCAL5 = 21
    LOCAL6 = 22
    LOCAL7 = 23
    def __str__(self):
        return self.name.lower()
    
MAXPRIVALUE = ((len(Facility) - 1) << 3) | (len(Severity) - 1)

# The PRI Section defined by RFC3164.
# This section has 1 8-bit integet, which represents Facility (High 5 bits) and Severity (Low 3 bits)
class RFC3164_PRI():
    def __init__(self, prival=13, **kwargs):
        if ("facility" in kwargs.keys()) and ("severity" in kwargs.keys()):
            if type(kwargs["facility"]) == int and type(kwargs["severity"]) == int:
                self._prival = (kwargs["facility"] & 0x1F ) << 3 | (kwargs["severity"] & 0x07)
                if self._prival == 0:
                    # Unidentifiable PRI
                    # RFC 3164 4.3.3 specifies that unidentifiable PRI should be inserted a PRI with 13 as value
                    self._prival = 13
            else:
                raise TypeError("Both facility and severity has to be integers")
        else:
            self._prival = prival
    # Convert to human readable string
    def __str__(self):
        return str(self.getFacility()) + "." + str(self.getSeverity())
    def __int__(self):
        return self._prival
    def getFacility(self, out_type = Facility):
        if out_type == Facility:
            return Facility(self.getFacility(int))
        elif out_type == int:
            return self._prival >> 3
        elif out_type == str:
            return str(self.getFacility())
    def getSeverity(self, out_type = Severity):
        if out_type == int:
            return self._prival & 0x07
        elif out_type == Severity:
            return Severity(self.getSeverity(int))
        elif out_type == str:
            return str(self.getSeverity())
    def setSeverity(self, severity):
        if type(severity) == int:
            if severity >= 0 and severity < len(Severity):
                self._prival = (self._prival & 0xF8) | (severity & 0x07)
            else:
                raise ValueError("Value out of range (Expected: 0-%d)" % (len(Severity) - 1))
        elif type(severity) == str:
            if severity.upper() in [i.name for i in list(Severity)]:
                self._prival = (self._prival & 0xF8) | (Severity[severity.upper()] & 0x07)
            else:
                raise ValueError("Invalid value")
        elif type(severity) == Severity:
            self._prival = (self._prival & 0xF8) | severity
        else:
            raise TypeError("Unsupported argument type")
    def setFacility(self, facility):
        if type(facility) == int:
            if facility >= 0 and facility < len(Facility):
                self._prival = ((facility & 0x1F) << 3) | (self._prival & 0x07)
            else:
                raise ValueError("Value out of range (Expected: 0-%d)" % (len(Facility) - 1))
        elif type(facility) == str:
            if facility.upper() in [i.name for i in list(Facility)]:
                self._prival = (Facility[facility.upper()] << 3) | (self._prival & 0x07)
            else:
                raise ValueError("Invalid value")
        elif type(facility) == Facility:
            self._prival = facility << 3 | (self._prival & 0x07)
        else:
            raise TypeError("Unsupported argument type")
    def getPRIvalue(self):
        return int(self)
    def setPRIvalue(self, prival):
        if prival <= MAXPRIVALUE and prival >= 0:
            self._prival = prival
        else:
            raise ValueError("Value out of range (Expected: 0-%d)" % (MAXPRIVALUE))

HOSTNAME_CHECK_REGEX = re.compile(r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$")

class RFC3164_HEADER():
    def __init__(self, **kwargs):
        if "timestamp" in kwargs.keys():
            if type(kwargs["timestamp"]) == datetime:
                self.time = kwargs["timestamp"]
            elif type(kwargs["timestamp"]) == int or type(kwargs["timestamp"]) == float:
                # POSIX timestamp expected
                self.time = datetime.fromtimestamp(kwargs["timestamp"])
            elif type(kwargs["timestamp"]) == str:
                # ISO format or syslog format expected
                try:
                    self.time = datetime.fromisoformat(kwargs["timestamp"])
                except ValueError:
                    self.time = datetime.strptime("%d " % (datetime.today().year) + kwargs["timestamp"], "%Y %b %d %H:%M:%S")
            elif kwargs["timestamp"] is None:
                self.time = datetime.now()
            else:
                raise TypeError("Unsupported timestamp type")
        else:
            self.time = datetime.now()
        if "hostname" in kwargs.keys():
            if type(kwargs["hostname"]) == str:
                # Checking if hostname or IP address is valid
                h = HOSTNAME_CHECK_REGEX.match(kwargs["hostname"])
                if h is not None:
                    self.hostname = kwargs["hostname"]
                else:
                    try:
                        # Check IPv4
                        socket.inet_pton(socket.AF_INET, kwargs["hostname"])
                        self.hostname = kwargs["hostname"]
                    except OSError:
                        # Check IPv6
                        socket.inet_pton(socket.AF_INET6, kwargs["hostname"])
                        self.hostname = kwargs["hostname"]
            else:
                raise TypeError("Invalid type for hostname")
        else:
            self.hostname = ""
        if "process" in kwargs.keys():
            if type(kwargs["process"]) == str:
                self.process = kwargs["process"]
            else:
                raise TypeError("Invalid process type (Expected: str | None)")
        else:
            self.process = ""
    def __str__(self):
        return " ".join([self.time.strftime("%b %d %H:%M:%S"), "\""+self.hostname+"\"", "\""+self.process+"\""])
    def toObject(self):
        return {
            "timestamp": self.time.strftime("%b %d %H:%M:%S"),
            "hostname": self.hostname,
            "process": self.process
        }
    @classmethod
    def fromObject(cls, obj):
        param = {
            "timestamp": datetime.now().strftime("%b %d %H:%M:%S"),
            "hostname": "",
            "process": ""
        }
        param = {**param, **obj}
        return cls(timestamp=param["timestamp"], hostname=param["hostname"], process=param["process"])


RFC3164_PRI_REGEX = re.compile(r"^<([0-1]{0,1}[0-9]{1,2})>")
RFC3164_TIME_REGEX = re.compile(r"^(<[0-9]{1,3}>)?(([A-Z][a-z]{2}) *([0-9]{1,2}) *([0-9]{2}):([0-9]{2}):([0-9]{2}))")

class RFC3164():
    def __init__(self, **kwargs):
        if "pri" in kwargs.keys():
            if type(kwargs["pri"]) == RFC3164_PRI:
                self.PRI = kwargs["pri"]
            else:
                self.PRI = RFC3164_PRI(kwargs["pri"])
        else:
            # Use unidentifiable PRI
            self.PRI = RFC3164_PRI()
        if "msg" in kwargs.keys():
            self.MSG = str(kwargs["msg"])
        else:
            raise ValueError("msg MUST not missing as a argument")
        if "header" in kwargs.keys():
            if type(kwargs["header"]) == RFC3164_HEADER:
                self.HEAD = kwargs["header"]
            else:
                raise TypeError("Invalid argument type")
        else:
            self.HEAD = None

    @classmethod
    def fromMessage(cls, msg, source_host = None, receive_timestamp = None):
        if type(msg) == bytes:
            msg = msg.decode("utf-8")
        # retrieving PRI
        pri_re = RFC3164_PRI_REGEX.match(msg)
        if pri_re is not None:
            pri = int(pri_re.groups()[0])
            nopri = False
        else:
            # Set PRI value as unidentifiable since No PRI message is detected
            pri = 13
            nopri = True
        timestamp_re = RFC3164_TIME_REGEX.match(msg)
        if timestamp_re is not None:
            timestamp = timestamp_re.groups()[1]
            notime = False
        else:
            # Receeiver has to add in timestamp if sender did not.
            timestamp = receive_timestamp
            notime = True
        hostname_re = re.match(r"<[0-9]{1,3}>" + (r"[A-Z][a-z]{2} *[0-9]{1,2} *[0-9]{2}:[0-9]{2}:[0-9]{2}" if not notime else "") + r" *(([a-zA-Z0-9][a-zA-Z0-9:\.\-]*)+)", msg)
        if hostname_re is not None:
            hostname = hostname_re.groups()[0]
            nohostname = False
            try:
                # Check IPv4
                socket.inet_pton(socket.AF_INET, hostname)
            except OSError:
                # Not IPv4, Check IPv6
                try:
                    socket.inet_pton(socket.AF_INET6, hostname)
                except OSError:
                    # Neither IPv4 or IPv6, check valid hostname
                    h = HOSTNAME_CHECK_REGEX.match(hostname)
                    if h is None:
                        # All failed
                        hostname = source_host
                        nohostname = True
        else:
            hostname = source_host
            nohostname = True
        process_re = re.match(  (r"<[0-9]{1,3}>" if not nopri else "") +
                                (r"[A-Z][a-z]{2} *[0-9]{1,2} *[0-9]{2}:[0-9]{2}:[0-9]{2}" if not notime else "") + 
                                (r" *[a-zA-Z0-9][a-zA-Z0-9:\.\-]*" if not nohostname else "") + 
                                r" *([a-zA-Z0-9\-\.\/]+)", msg)
        if process_re is not None:
            process = process_re.groups()[0]
            noprocess = False
        else:
            process = ""
            noprocess = True
        
        msg_re = re.match(  (r"<[0-9]{1,3}>" if not nopri else "") +
                            (r"[A-Z][a-z]{2} *[0-9]{1,2} *[0-9]{2}:[0-9]{2}:[0-9]{2}" if not notime else "") + 
                            (r" *[a-zA-Z0-9][a-zA-Z0-9:\.\-]*" if not nohostname else "") + 
                            (r" *[a-zA-Z0-9\-\.\/]*" if not noprocess else "") + 
                            r"(.+)", msg)
        
        if msg_re is not None:
            message = msg_re.groups()[0]
        else:
            # How the hell is this message has no content
            message = ""
        
        return cls(
            pri = RFC3164_PRI(pri),
            header = RFC3164_HEADER(process=process, hostname=hostname, timestamp=timestamp),
            msg=message
        )

    def __str__(self):
        return "<%s>%s  %s"% (str(self.PRI), str(self.HEAD), self.MSG)
    def toObject(self):
        return {
            "PRI": int(self.PRI),
            "HEAD": self.HEAD.toObject(),
            "MSG": self.MSG
        }
    @classmethod
    def fromObject(cls, obj):
        param = {
            "PRI": 13,
            "HEAD": {
                "timestamp": datetime.now().strftime("%b %d %H:%M:%S"),
                "hostname": "",
                "process": ""
            },
            "MSG": ""
        }
        param = {**param, **obj}
        return cls(pri=param["PRI"], header=RFC3164_HEADER.fromObject(param["HEAD"]), msg=param["MSG"])