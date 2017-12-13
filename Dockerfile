ARG QGIS_TEST_VERSION=latest
FROM  qgis/qgis:${QGIS_TEST_VERSION}
MAINTAINER Agencia Implementacion <agenciadeimplementacion@incige.com>

#RUN apt-get update && \
#    apt-get -y install default-jre

ENV LANG=C.UTF-8

WORKDIR /

CMD ["sh", "/usr/src/scripts/run-docker-tests.sh"]
