FROM httpd:2.4
LABEL maintainer="JackyCCC"
LABEL version="1.0"

RUN mkdir /syslog-server && \
    apt-get update && \
    apt-get install -y gnupg curl python3 python3-pip && \
    curl -s -L -f https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add - && \
    echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" > /etc/apt/sources.list.d/mongodb-org-4.4.list && \
    apt-get update && \
    apt-get install -y mongodb-org &&\
    apt-get upgrade -y && \
    pip3 install pymongo

EXPOSE 514/udp 80/tcp
WORKDIR /syslog-server

COPY conf/httpd.conf /usr/local/apache2/conf/httpd.conf
# Using MongoDB default config file
COPY src/cgi-bin /usr/local/apache2/cgi-bin
COPY src/syslog-server /syslog-server
COPY src/htdocs /usr/local/apache2/htdocs

CMD ["/syslog-server/startServer.sh"]