#!/bin/bash
BASEDIR=/syslog-server

# Starting MongoDB
mongod --config /etc/mongod.conf --verbose --fork

# Starting httpd foreground
/usr/local/bin/httpd-foreground &

# Starting syslog-server
cd $BASEDIR
python3 main.py