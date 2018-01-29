set PGPASSWORD=clave_ladm_col
path C:\Program Files\PostgreSQL\10\bin;%PATH%
pg_restore -h postgres -U usuario_ladm_col -d ladm_col sql/ladm_col_v2.2.0.backup
