# syntax=docker/dockerfile:1

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive"

# Security Patch for CVE-2021-44228
ENV LOG4J_FORMAT_MSG_NO_LOOKUPS=true

LABEL maintainer="Albert Ferguson <https://github.com/albert118/> and Sebastian Schroder <https://github.com/DARKMOONlite>"

# Run a quiet and minimal installation
RUN apt-get update
RUN apt-get install -yqq --no-install-recommends openjdk-8-jre-headless default-jre
RUN apt-get install -yqq --no-install-recommends python3 python3-pip libmysqlclient-dev

RUN mkdir -p /Crafty_Controller_Fabric/app
WORKDIR /Crafty_Controller_Fabric

COPY ./configs /Crafty_Controller_Fabric/configs

COPY ./requirements.txt .
RUN pip3 install --upgrade pip --no-cache-dir -r requirements.txt

COPY ./app /Crafty_Controller_Fabric/app

RUN mkdir -p /Crafty_Controller_Fabric/server/server_1

COPY ./docker/minecraft_servers /Crafty_Controller_Fabric/server/server_1


# Web app port
EXPOSE 8010
# MC Server Ports
EXPOSE 25500-25600

COPY ./crafty.py .

CMD ["python3", "crafty.py", "-c", "/Crafty_Controller_Fabric/configs/docker_config.yml"]