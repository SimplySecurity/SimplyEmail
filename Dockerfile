# image base
FROM ubuntu:16.04

# extra metadata
LABEL maintainer="SimplySecurity"
LABEL description="Dockerfile base for SimplyEmail."

# env setup
ENV DEBIAN_FRONTEND=noninteractive

# set the def shell for ENV
SHELL ["/bin/bash", "-c"]

# install basic build items
RUN apt-get update && apt-get install -qy \
    wget \
    curl \
    git \
    sudo \
    apt-utils \
    lsb-core \
    python2.7

# cleanup image
RUN apt-get -qy clean \
    autoremove


RUN git clone -b master https://github.com/SimplySecurity/SimplyEmail.git  /opt/SimplyEmail && \
	cd /opt/SimplyEmail/ && \
	./setup/setup.sh 

WORKDIR "/opt/SimplyEmail"
ENTRYPOINT ["./SimplyEmail.py"]
