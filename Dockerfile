ARG QGIS_TEST_VERSION=latest
FROM  agenciaimplementacion/qgis:${QGIS_TEST_VERSION}
MAINTAINER SwissTierrasColombia <administracion@swisstierrascolombia.com>

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

# Install OpenJDK-8
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

# Python deps
RUN apt-get -y install \
    python3-pip

# Python pip installs
# temporally pip==9.0.3 version
RUN pip3 install --upgrade pip==9.0.3 && \
    pip3 install --upgrade psycopg2

# When our PRs get merged in time!
# RUN wget https://github.com/opengisch/QgisModelBaker/releases/download/v6.1.1/qgis-model-baker.v6.1.1.zip -O /tmp/QgisModelBaker.zip

# When we need a custom release
RUN wget https://github.com/SwissTierrasColombia/QgisModelBaker/releases/download/v6.1.1.1/QgisModelBaker_6111.zip -O /tmp/QgisModelBaker.zip

RUN unzip /tmp/QgisModelBaker.zip -d /usr/share/qgis/python/plugins
RUN rm -rf /tmp/QgisModelBaker.zip

ENV LANG=C.UTF-8

WORKDIR /
