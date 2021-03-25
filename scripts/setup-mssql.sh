#!/usr/bin/env bash

##############################
# Restore SQL Server test data
##############################

set -e

echo "Creating database for test SQL Server"

export SQLUSER=sa
export SQLHOST=mssql
export SQLPORT=1433
export SQLPASSWORD='<YourStrong!Passw0rd>'

export PATH=$PATH:/opt/mssql-tools/bin

printf "Wait a moment while creating the MSSQL database."
for i in {1..15}
do
  if sqlcmd -S $SQLHOST,$SQLPORT -U $SQLUSER -P $SQLPASSWORD -Q "CREATE DATABASE ladm_col;" &> /dev/null; then
    break
  fi
  printf "\nAttempt $i..."
  sleep 2
done
printf "\nMSSQL ready!\n"