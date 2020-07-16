REM This hasn't been tested extensively. Be careful with it :) 
set PGPASSWORD=clave_ladm_col
path C:\Program Files\PostgreSQL\10\bin;%PATH%
set DB_BACKUP = %1

psql -h postgres -U usuario_ladm_col -d ladm_col --command='CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'
psql -h postgres -U usuario_ladm_col -d ladm_col -f sql/%DB_BACKUP%