set PGPASSWORD=clave_ladm_col
path C:\Program Files\PostgreSQL\10\bin;%PATH%
set DB_BACKUP = %1
pg_restore -h postgres -U usuario_ladm_col -d ladm_col sql/%DB_BACKUP%
