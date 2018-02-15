ARG QGIS_TEST_VERSION=latest
FROM  agenciaimplementacion/qgis:${QGIS_TEST_VERSION}
MAINTAINER Agencia Implementacion <agenciadeimplementacion@incige.com>

#RUN apt-get update && \
#    apt-get -y install default-jre
#    apt-get -y install python3-pip

#RUN pip3 install --upgrade pip

#RUN pip3 install psycopg2 \
#  nose2 \
#  pyyaml \
#  future \
#  transifex-client

RUN apt-get update && \
    apt-get -y install \
    iputils-ping \
    dnsutils \
    nmap \
    wget \
    unzip

RUN wget https://github.com/AgenciaImplementacion/projectgenerator/releases/download/2.0.1.1/projectgenerator.zip -O /tmp/projectgenerator.zip
RUN unzip /tmp/projectgenerator.zip -d /usr/share/qgis/python/plugins
RUN rm -rf /tmp/projectgenerator.zip

ENV LANG=C.UTF-8

WORKDIR /
