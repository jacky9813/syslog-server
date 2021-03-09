#!/bin/bash
BASEDIR=/syslog-server

APACHE_PID_FILE=/var/run/apache2/apache2.pid
if [ -f "$APACHE_PID_FILE" ]; then
    if [ ! -d "/proc/$(<$APACHE_PID_FILE)"]; then
        
    fi
fi

# Starting MongoDB
mongod --config /etc/mongod.conf --verbose --fork

# Starting httpd foreground
/usr/local/bin/httpd-foreground &

# Starting syslog-server
cd $BASEDIR
python3 main.py