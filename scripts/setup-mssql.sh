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

echo "sleep"
sleep 90

sqlcmd -S $SQLHOST,$SQLPORT -U $SQLUSER -P $SQLPASSWORD -Q "CREATE DATABASE ladm_col;"
