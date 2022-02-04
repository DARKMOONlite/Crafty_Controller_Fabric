# syntax=docker/dockerfile:1

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive"

# Security Patch for CVE-2021-44228
ENV LOG4J_FORMAT_MSG_NO_LOOKUPS=true

LABEL maintainer="Albert Ferguson <https://github.com/albert118/> and Sebastian Schroder <https://github.com/DARKMOONlite>"

RUN apt-get update
RUN apt-get install -y openjdk-8-jre-headless openjdk-11-jre-headless openjdk-16-jre-headless default-jre
RUN apt-get install -y python3 python3-dev python3-pip libmysqlclient-dev

COPY requirements.txt /Crafty_Controller_Fabric/requirements.txt
RUN pip3 install --no-cache -r /Crafty_Controller_Fabric/requirements.txt

COPY ./ /Crafty_Controller_Fabric
WORKDIR /Crafty_Controller_Fabric

# Web app port
EXPOSE 8010
# MC Server Ports
EXPOSE 25500-25600

CMD ["python3", "crafty.py", "-c", "/Crafty_Controller_Fabric/configs/docker_config.yml"]
