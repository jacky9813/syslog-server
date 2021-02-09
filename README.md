# Syslog Server

## Introduction
It is a docker container that can receive Syslog Message (RFC3164), store in database and display via website.

## Use (from Docker Registry)
Work in progress

## Use (Build from source)
Prerequisites:
* Docker and Docker Compose is installed
* Check the ports specified in docker-compose.yml is not occupied
```bash
$ git clone https://github.com/jacky9813/syslog-server
$ cd syslog-server
$ ./build.sh
$ mkdir db
$ sudo docker-compose up -d
```

## Use (Build and export image file to offline server)
* Build the image using ```$ sudo docker-compose build```
* Export Docker image (```$ sudo docker save syslog-server | pigz -9 -c > syslog-server.tar.gz``` will export image as a gzip compressed tarball)
* Copy syslog-server.tar.gz file to offline server
* Import Docker image (```$ pigz -d -c syslog-server.tar.gz | sudo docker load ```, it feeds docker load with decompressed tarball)
* Run

## Volumes
Take a look at docker-compose.yml. Most useful volumes are specified in there.

## Syslog input filter
src/syslog-server/filter.py has basic filter function. Change conf/syslog-server.json can adjust verbosity(severity) and facility filtering parameter.

Optionally src/syslog-server/filter.py can be override using volume.