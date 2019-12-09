REM This hasn't been tested extensively. Be careful with it :) 
set PGPASSWORD=clave_ladm_col
path C:\Program Files\PostgreSQL\10\bin;%PATH%
set DB_BACKUP = %1
set SCHEMA = %2

psql -h postgres -U usuario_ladm_col -d ladm_col --command='DROP SCHEMA IF EXISTS '%SCHEMA%' CASCADE'
psql -h postgres -U usuario_ladm_col -d ladm_col --command='CREATE SCHEMA '%SCHEMA%
psql -h postgres -U usuario_ladm_col -d ladm_col --command='CREATE EXTENSION IF NOT EXISTS postgis'
psql -h postgres -U usuario_ladm_col -d ladm_col --command='CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'
pg_restore --clean -h postgres -U usuario_ladm_col -d ladm_col sql/%DB_BACKUP%