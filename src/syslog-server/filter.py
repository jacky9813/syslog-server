#!/bin/env python3
# Replace this file if more advanced filter is needed

from rfc3164 import RFC3164, Severity, Facility
import json

filter_setting = {
    "severity": 7,
    "facility": []
}

try:
    with open("config.json", mode="r") as fd:
        settings = {**({"filter":{}}) , **json.load(fd)}
except:
    settings = {"filter":{}}

filter_setting = {**filter_setting , **settings["filter"]}

# Filtering syslog
def filter(obj:RFC3164):
    if obj.PRI.getSeverity() > Severity(filter_setting["severity"]):
        return False
    if obj.PRI.getFacility() in filter_setting["facility"]:
        return False
    return True