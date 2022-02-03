FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive"

# Security Patch for CVE-2021-44228
ENV LOG4J_FORMAT_MSG_NO_LOOKUPS=true

LABEL maintainer="Albert Ferguson <https://github.com/albert118/> and Sebastian Schroder <https://github.com/DARKMOONlite>"

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip openjdk-8-jre-headless openjdk-11-jre-headless openjdk-16-jre-headless default-jre libmysqlclient-dev

COPY requirements.txt /crafty_web/requirements.txt
RUN pip3 install -r /crafty_web/requirements.txt

COPY ./ /crafty_web
WORKDIR /crafty_web

EXPOSE 8001
EXPOSE 25500-25600

CMD ["python3", "crafty.py", "-c", "/crafty_web/configs/docker_config.yml"]
