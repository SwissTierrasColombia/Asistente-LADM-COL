ARG QGIS_TEST_VERSION=latest
FROM  qgis/qgis:${QGIS_TEST_VERSION}
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

ENV LANG=C.UTF-8

WORKDIR /
