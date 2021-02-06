#!/usr/bin/env python3
import socketserver
import json
import re

# Unix Timestamp in ms
from math import floor
from datetime import datetime

# RFC3164 input filter
from filter import filter
from rfc3164 import RFC3164

# Primary datastore
import pymongo
# Required for MongoDB query filter working correctly
from bson.son import SON

# Defining default settings
settings={
    "host": "0.0.0.0",
    "port": "514/udp",
    "dblink": "mongodb://localhost:27017/",
    "dbname": "syslog",
    "filter": {}
}

# Loading Config
try:
    with open("config.json",  mode="r") as fd:
        settings = {**settings, **json.load(fd)} # Joining 
except:
    pass

# Opening MongoDB
mongo = pymongo.MongoClient(settings["dblink"])
db = mongo[settings["dbname"]]
syslogTable = db["syslog"]

# Defining Message Handler
class syslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = RFC3164.fromMessage(
            self.request[0].strip(),
            self.client_address[0])
        if filter(data):
            o = {
                "timestamp": floor(datetime.now().timestamp()*1000),
                "data":SON({
                    **(data.toObject()), 
                    "PRI_SEVERITY": data.PRI.getSeverity(), 
                    "PRI_FACILITY": data.PRI.getFacility()
                    })}
            print(json.dumps(o))
            syslogTable.insert_one(o)

class syslogTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = RFC3164.fromMessage(
            self.request.recv(1024).strip(),
            self.client_address[0])
        if filter(data):
            o = {
                "timestamp": floor(datetime.now().timestamp()*1000),
                "data":SON({
                    **(data.toObject()), 
                    "PRI_SEVERITY": data.PRI.getSeverity(), 
                    "PRI_FACILITY": data.PRI.getFacility()
                    })}
            print(json.dumps(o))
            syslogTable.insert_one(o)

# Starting Server
if __name__ == "__main__":
    HOST = settings["host"]
    PORT, SOCK = re.match(r"([0-9]*)\/([a-zA-Z]*)", settings["port"]).groups()
    if SOCK.lower() == "udp":
        with socketserver.UDPServer((HOST, int(PORT)), syslogUDPHandler) as server:
            server.serve_forever()
    elif SOCK.lower() == "tcp":
        with socketserver.TCPServer((HOST, int(PORT)), syslogTCPHandler) as server:
            server.serve_forever()
    else:
        raise NotImplementedError("Unsupported Socket Type: %s" % SOCK)