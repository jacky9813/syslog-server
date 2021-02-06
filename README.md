# Syslog Server

## Introduction
It is a docker container that can receive Syslog Message (RFC3164), store in database and display via website.

## Use (from Docker Registry)
Work in progress

## Use (Build)
Prerequisites:
* Docker and Docker Compose is installed
* Check the ports specified in docker-compose.yml is not occupied
```bash
$ git clone https://github.com/jacky9813/syslog-server
$ cd syslog-server-master
$ mkdir db
$ sudo docker-compose build && sudo docker-compose up -d
```

## Use (Offline)
* Build the image using ```$ sudo docker-compose build```
* Export Docker image with ```$ sudo docker save syslog-server | pigz -9 -c > syslog-server.tar.gz```
* Move syslog-server.tar.gz file to Offline Server
* Import Docker image with ```$ pigz -d -c syslog-server.tar.gz | sudo docker load ```
* Run

## Volumes
Take a look at docker-compose.yml. Most useful volumes are specified in there.