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

# MSSQL: client side
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list | tee /etc/apt/sources.list.d/msprod.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools unixodbc unixodbc-dev

# Python deps
RUN apt-get -y install \
    python3-pip \
    python3-pyodbc

# Avoid sqlcmd termination due to locale -- see https://github.com/Microsoft/mssql-docker/issues/163
RUN echo "nb_NO.UTF-8 UTF-8" > /etc/locale.gen
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen
ENV PATH="/usr/local/bin:${PATH}"

# Python pip installs
# temporally pip==9.0.3 version
RUN pip3 install --upgrade pip==9.0.3 && \
    pip3 install --upgrade psycopg2

# When our PRs get merged in time!
RUN wget https://github.com/opengisch/QgisModelBaker/releases/download/v6.1.1/qgis-model-baker.v6.1.1.zip -O /tmp/QgisModelBaker.zip

# When we need a custom release
#RUN wget https://github.com/AgenciaImplementacion/QgisModelBaker/releases/download/v4.3.1.2/QgisModelBaker.zip -O /tmp/QgisModelBaker.zip

RUN unzip /tmp/QgisModelBaker.zip -d /usr/share/qgis/python/plugins
RUN rm -rf /tmp/QgisModelBaker.zip

ENV LANG=C.UTF-8

WORKDIR /
