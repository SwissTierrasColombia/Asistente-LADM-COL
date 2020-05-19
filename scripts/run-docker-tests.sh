#!/usr/bin/env bash
#***************************************************************************
#                             -------------------
#       begin                : 2017-08-24
#       git sha              : :%H$
#       copyright            : (C) 2017 by OPENGIS.ch
#       email                : info@opengis.ch
#***************************************************************************
#
#***************************************************************************
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU General Public License as published by  *
#*   the Free Software Foundation; either version 2 of the License, or     *
#*   (at your option) any later version.                                   *
#*                                                                         *
#***************************************************************************

set -e

chmod u+x /usr/src/scripts/setup-mssql.sh
/usr/src/scripts/setup-mssql.sh

# rationale: Wait for postgres container to become available
# link: https://cstan.io/?p=8620&lang=en
dig postgres
nmap -p 5432 postgres
ping -c 1 postgres
printf "Wait a moment while loading the database."
while ! PGPASSWORD='clave_ladm_col' psql -h postgres -U usuario_ladm_col -p 5432 -l &> /dev/null
do
  printf "."
  sleep 2
done
printf "\n"

pushd /usr/src/asistente_ladm_col
make
cd ..
export PYTHONPATH=/usr/share/qgis/python/plugins:$PYTHONPATH
xvfb-run nose2-3  # asistente_ladm_col.tests.test_mssql
popd