ARG QGIS_TEST_VERSION=latest
FROM  agenciaimplementacion/qgis:${QGIS_TEST_VERSION}
MAINTAINER Agencia Implementacion <agenciadeimplementacion@incige.com>

#RUN apt-get update && \
#    apt-get -y install default-jre
#    apt-get -y install python3-pip

#RUN /usr/bin/pip3 install --upgrade pip

#RUN pip3 install psycopg2 \
#  nose2 \
#  pyyaml \
#  future \
#  transifex-client


# SO deps
RUN apt-get update && \
    apt-get -y install \
    iputils-ping \
    dnsutils \
    nmap \
    wget \
    unzip \
    vim

# Python deps
RUN apt-get -y install \
    python3-pip

# Python pip installs
# temporally pip==9.0.3 version
RUN pip3 install --upgrade pip==9.0.3 && \
    pip3 install --upgrade psycopg2

# When our PRs get merged in time!
RUN wget https://github.com/opengisch/projectgenerator/releases/download/v3.2.0/projectgenerator-v3.2.0.zip -O /tmp/projectgenerator.zip

# When we need a custom release
# RUN wget https://github.com/AgenciaImplementacion/projectgenerator/releases/download/v3.0.2.1/projectgenerator.zip -O /tmp/projectgenerator.zip

RUN unzip /tmp/projectgenerator.zip -d /usr/share/qgis/python/plugins
RUN rm -rf /tmp/projectgenerator.zip

ENV LANG=C.UTF-8

WORKDIR /
