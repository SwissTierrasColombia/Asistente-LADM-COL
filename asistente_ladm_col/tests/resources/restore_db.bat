set PGPASSWORD=clave_ladm_col
pg_restore -h postgres -U usuario_ladm_col -d ladm_col sql/ladm_col_v2.2.0.backup
