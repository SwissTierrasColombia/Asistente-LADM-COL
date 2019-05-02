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

ENV PYTHONPATH="/usr/share/qgis/python"

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
RUN wget https://github.com/opengisch/QgisModelBaker/releases/download/v4.2.2/QgisModelBaker.v4.2.2.zip -O /tmp/QgisModelBaker.zip

# When we need a custom release
#RUN wget https://github.com/AgenciaImplementacion/QgisModelBaker/releases/download/v4.1.0.1/QgisModelBaker.zip -O /tmp/QgisModelBaker.zip

RUN unzip /tmp/QgisModelBaker.zip -d /usr/share/qgis/python/plugins
RUN rm -rf /tmp/QgisModelBaker.zip

ENV LANG=C.UTF-8

WORKDIR /
