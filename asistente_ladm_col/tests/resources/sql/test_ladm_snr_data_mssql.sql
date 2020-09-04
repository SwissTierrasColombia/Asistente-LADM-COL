IF NOT EXISTS (SELECT  schema_name FROM information_schema.schemata WHERE schema_name = 'test_ladm_snr_data')EXEC sp_executesql N'CREATE SCHEMA test_ladm_snr_data';
CREATE SEQUENCE test_ladm_snr_data.t_ili2db_seq START WITH 1;;
-- LADM_COL_V3_0.LADM_Nucleo.ExtArchivo
CREATE TABLE test_ladm_snr_data.extarchivo (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for test_ladm_snr_data.t_ili2db_seq)
  ,[T_Seq] BIGINT NULL
  ,[fecha_aceptacion] DATE NULL
  ,[datos] VARCHAR(255) NULL
  ,[extraccion] DATE NULL
  ,[fecha_grabacion] DATE NULL
  ,[fecha_entrega] DATE NULL
  ,[espacio_de_nombres] VARCHAR(255) NOT NULL
  ,[local_id] VARCHAR(255) NOT NULL
  ,[snr_fuentecabidalndros_archivo] BIGINT NULL
)
;
-- Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho
CREATE TABLE test_ladm_snr_data.snr_derecho (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for test_ladm_snr_data.t_ili2db_seq)
  ,[calidad_derecho_registro] BIGINT NOT NULL
  ,[codigo_naturaleza_juridica] VARCHAR(5) NULL
  ,[snr_fuente_derecho] BIGINT NOT NULL
  ,[snr_predio_registro] BIGINT NOT NULL
)
;
-- Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz
CREATE TABLE test_ladm_snr_data.snr_estructuramatriculamatriz (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for test_ladm_snr_data.t_ili2db_seq)
  ,[T_Seq] BIGINT NULL
  ,[codigo_orip] VARCHAR(20) NULL
  ,[matricula_inmobiliaria] VARCHAR(20) NULL
  ,[snr_predioregistro_matricula_inmobiliaria_matriz] BIGINT NULL
)
;
-- Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos
CREATE TABLE test_ladm_snr_data.snr_fuentecabidalinderos (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for test_ladm_snr_data.t_ili2db_seq)
  ,[tipo_documento] BIGINT NULL
  ,[numero_documento] VARCHAR(255) NULL
  ,[fecha_documento] DATE NULL
  ,[ente_emisor] VARCHAR(255) NULL
  ,[ciudad_emisora] VARCHAR(255) NULL
)
;
-- Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho
CREATE TABLE test_ladm_snr_data.snr_fuentederecho (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for test_ladm_snr_data.t_ili2db_seq)
  ,[tipo_documento] BIGINT NULL
  ,[numero_documento] VARCHAR(255) NULL
  ,[fecha_documento] DATE NULL
  ,[ente_emisor] VARCHAR(255) NULL
  ,[ciudad_emisora] VARCHAR(255) NULL
)
;
-- Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular
CREATE TABLE test_ladm_snr_data.snr_titular (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for test_ladm_snr_data.t_ili2db_seq)
  ,[tipo_persona] BIGINT NULL
  ,[tipo_documento] BIGINT NULL
  ,[numero_documento] VARCHAR(50) NOT NULL
  ,[nombres] VARCHAR(500) NULL
  ,[primer_apellido] VARCHAR(255) NULL
  ,[segundo_apellido] VARCHAR(255) NULL
  ,[razon_social] VARCHAR(255) NULL
)
;
-- Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro
CREATE TABLE test_ladm_snr_data.snr_predioregistro (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for test_ladm_snr_data.t_ili2db_seq)
  ,[codigo_orip] VARCHAR(3) NULL
  ,[matricula_inmobiliaria] VARCHAR(80) NULL
  ,[numero_predial_nuevo_en_fmi] VARCHAR(100) NULL
  ,[numero_predial_anterior_en_fmi] VARCHAR(100) NULL
  ,[nomenclatura_registro] VARCHAR(255) NULL
  ,[cabida_linderos] VARCHAR(MAX) NULL
  ,[clase_suelo_registro] BIGINT NULL
  ,[fecha_datos] DATE NOT NULL
  ,[snr_fuente_cabidalinderos] BIGINT NULL
)
;
-- Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho
CREATE TABLE test_ladm_snr_data.snr_titular_derecho (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for test_ladm_snr_data.t_ili2db_seq)
  ,[snr_titular] BIGINT NOT NULL
  ,[snr_derecho] BIGINT NOT NULL
  ,[porcentaje_participacion] VARCHAR(100) NULL
)
;
CREATE TABLE test_ladm_snr_data.T_ILI2DB_BASKET (
  [T_Id] BIGINT PRIMARY KEY
  ,[dataset] BIGINT NULL
  ,[topic] VARCHAR(200) NOT NULL
  ,[T_Ili_Tid] VARCHAR(200) NULL
  ,[attachmentKey] VARCHAR(200) NOT NULL
  ,[domains] VARCHAR(1024) NULL
)
;
CREATE TABLE test_ladm_snr_data.T_ILI2DB_DATASET (
  [T_Id] BIGINT PRIMARY KEY
  ,[datasetName] VARCHAR(200) NULL
)
;
CREATE TABLE test_ladm_snr_data.T_ILI2DB_INHERITANCE (
  [thisClass] VARCHAR(1024) PRIMARY KEY
  ,[baseClass] VARCHAR(1024) NULL
)
;
CREATE TABLE test_ladm_snr_data.T_ILI2DB_SETTINGS (
  [tag] VARCHAR(60) PRIMARY KEY
  ,[setting] VARCHAR(1024) NULL
)
;
CREATE TABLE test_ladm_snr_data.T_ILI2DB_TRAFO (
  [iliname] VARCHAR(1024) NOT NULL
  ,[tag] VARCHAR(1024) NOT NULL
  ,[setting] VARCHAR(1024) NOT NULL
)
;
CREATE TABLE test_ladm_snr_data.T_ILI2DB_MODEL (
  [filename] VARCHAR(250) NOT NULL
  ,[iliversion] VARCHAR(3) NOT NULL
  ,[modelName] VARCHAR(400) NOT NULL
  ,[content] VARCHAR(MAX) NOT NULL
  ,[importDate] DATETIME NOT NULL
  ,PRIMARY KEY (iliversion,modelName)
)
;
CREATE TABLE test_ladm_snr_data.snr_personatitulartipo (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for test_ladm_snr_data.t_ili2db_seq)
  ,[thisClass] VARCHAR(1024) NOT NULL
  ,[baseClass] VARCHAR(1024) NULL
  ,[itfCode] NUMERIC(4) NOT NULL
  ,[iliCode] VARCHAR(1024) NOT NULL
  ,[seq] NUMERIC(4) NULL
  ,[inactive] BIT NOT NULL
  ,[dispName] VARCHAR(250) NOT NULL
  ,[description] VARCHAR(1024) NULL
)
;
CREATE TABLE test_ladm_snr_data.snr_calidadderechotipo (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for test_ladm_snr_data.t_ili2db_seq)
  ,[thisClass] VARCHAR(1024) NOT NULL
  ,[baseClass] VARCHAR(1024) NULL
  ,[itfCode] NUMERIC(4) NOT NULL
  ,[iliCode] VARCHAR(1024) NOT NULL
  ,[seq] NUMERIC(4) NULL
  ,[inactive] BIT NOT NULL
  ,[dispName] VARCHAR(250) NOT NULL
  ,[description] VARCHAR(1024) NULL
)
;
CREATE TABLE test_ladm_snr_data.snr_clasepredioregistrotipo (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for test_ladm_snr_data.t_ili2db_seq)
  ,[thisClass] VARCHAR(1024) NOT NULL
  ,[baseClass] VARCHAR(1024) NULL
  ,[itfCode] NUMERIC(4) NOT NULL
  ,[iliCode] VARCHAR(1024) NOT NULL
  ,[seq] NUMERIC(4) NULL
  ,[inactive] BIT NOT NULL
  ,[dispName] VARCHAR(250) NOT NULL
  ,[description] VARCHAR(1024) NULL
)
;
CREATE TABLE test_ladm_snr_data.snr_documentotitulartipo (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for test_ladm_snr_data.t_ili2db_seq)
  ,[thisClass] VARCHAR(1024) NOT NULL
  ,[baseClass] VARCHAR(1024) NULL
  ,[itfCode] NUMERIC(4) NOT NULL
  ,[iliCode] VARCHAR(1024) NOT NULL
  ,[seq] NUMERIC(4) NULL
  ,[inactive] BIT NOT NULL
  ,[dispName] VARCHAR(250) NOT NULL
  ,[description] VARCHAR(1024) NULL
)
;
CREATE TABLE test_ladm_snr_data.snr_fuentetipo (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for test_ladm_snr_data.t_ili2db_seq)
  ,[thisClass] VARCHAR(1024) NOT NULL
  ,[baseClass] VARCHAR(1024) NULL
  ,[itfCode] NUMERIC(4) NOT NULL
  ,[iliCode] VARCHAR(1024) NOT NULL
  ,[seq] NUMERIC(4) NULL
  ,[inactive] BIT NOT NULL
  ,[dispName] VARCHAR(250) NOT NULL
  ,[description] VARCHAR(1024) NULL
)
;
CREATE TABLE test_ladm_snr_data.T_ILI2DB_CLASSNAME (
  [IliName] VARCHAR(1024) PRIMARY KEY
  ,[SqlName] VARCHAR(1024) NOT NULL
)
;
CREATE TABLE test_ladm_snr_data.T_ILI2DB_ATTRNAME (
  [IliName] VARCHAR(1024) NOT NULL
  ,[SqlName] VARCHAR(1024) NOT NULL
  ,[ColOwner] VARCHAR(1024) NOT NULL
  ,[Target] VARCHAR(1024) NULL
  ,PRIMARY KEY (SqlName,ColOwner)
)
;
CREATE TABLE test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (
  [tablename] VARCHAR(255) NOT NULL
  ,[subtype] VARCHAR(255) NULL
  ,[columnname] VARCHAR(255) NOT NULL
  ,[tag] VARCHAR(1024) NOT NULL
  ,[setting] VARCHAR(1024) NOT NULL
)
;
CREATE TABLE test_ladm_snr_data.T_ILI2DB_TABLE_PROP (
  [tablename] VARCHAR(255) NOT NULL
  ,[tag] VARCHAR(1024) NOT NULL
  ,[setting] VARCHAR(1024) NOT NULL
)
;
CREATE TABLE test_ladm_snr_data.T_ILI2DB_META_ATTRS (
  [ilielement] VARCHAR(255) NOT NULL
  ,[attr_name] VARCHAR(1024) NOT NULL
  ,[attr_value] VARCHAR(1024) NOT NULL
)
;
ALTER TABLE test_ladm_snr_data.extarchivo ADD CONSTRAINT extarchivo_snr_fuentecabdlndrs_rchivo_fkey FOREIGN KEY ( snr_fuentecabidalndros_archivo ) REFERENCES test_ladm_snr_data.snr_fuentecabidalinderos;
ALTER TABLE test_ladm_snr_data.snr_derecho ADD CONSTRAINT snr_derecho_calidad_derecho_registro_fkey FOREIGN KEY ( calidad_derecho_registro ) REFERENCES test_ladm_snr_data.snr_calidadderechotipo;
ALTER TABLE test_ladm_snr_data.snr_derecho ADD CONSTRAINT snr_derecho_snr_fuente_derecho_fkey FOREIGN KEY ( snr_fuente_derecho ) REFERENCES test_ladm_snr_data.snr_fuentederecho;
ALTER TABLE test_ladm_snr_data.snr_derecho ADD CONSTRAINT snr_derecho_snr_predio_registro_fkey FOREIGN KEY ( snr_predio_registro ) REFERENCES test_ladm_snr_data.snr_predioregistro;
ALTER TABLE test_ladm_snr_data.snr_estructuramatriculamatriz ADD CONSTRAINT snr_estructuramatriclmtriz_snr_prdrgstr_l_nmblr_mtriz_fkey FOREIGN KEY ( snr_predioregistro_matricula_inmobiliaria_matriz ) REFERENCES test_ladm_snr_data.snr_predioregistro;
ALTER TABLE test_ladm_snr_data.snr_fuentecabidalinderos ADD CONSTRAINT snr_fuentecabidalinderos_tipo_documento_fkey FOREIGN KEY ( tipo_documento ) REFERENCES test_ladm_snr_data.snr_fuentetipo;
ALTER TABLE test_ladm_snr_data.snr_fuentederecho ADD CONSTRAINT snr_fuentederecho_tipo_documento_fkey FOREIGN KEY ( tipo_documento ) REFERENCES test_ladm_snr_data.snr_fuentetipo;
ALTER TABLE test_ladm_snr_data.snr_titular ADD CONSTRAINT snr_titular_tipo_persona_fkey FOREIGN KEY ( tipo_persona ) REFERENCES test_ladm_snr_data.snr_personatitulartipo;
ALTER TABLE test_ladm_snr_data.snr_titular ADD CONSTRAINT snr_titular_tipo_documento_fkey FOREIGN KEY ( tipo_documento ) REFERENCES test_ladm_snr_data.snr_documentotitulartipo;
ALTER TABLE test_ladm_snr_data.snr_predioregistro ADD CONSTRAINT snr_predioregistro_clase_suelo_registro_fkey FOREIGN KEY ( clase_suelo_registro ) REFERENCES test_ladm_snr_data.snr_clasepredioregistrotipo;
ALTER TABLE test_ladm_snr_data.snr_predioregistro ADD CONSTRAINT snr_predioregistro_snr_fuente_cabidalinderos_fkey FOREIGN KEY ( snr_fuente_cabidalinderos ) REFERENCES test_ladm_snr_data.snr_fuentecabidalinderos;
ALTER TABLE test_ladm_snr_data.snr_titular_derecho ADD CONSTRAINT snr_titular_derecho_snr_titular_fkey FOREIGN KEY ( snr_titular ) REFERENCES test_ladm_snr_data.snr_titular;
ALTER TABLE test_ladm_snr_data.snr_titular_derecho ADD CONSTRAINT snr_titular_derecho_snr_derecho_fkey FOREIGN KEY ( snr_derecho ) REFERENCES test_ladm_snr_data.snr_derecho;
ALTER TABLE test_ladm_snr_data.T_ILI2DB_BASKET ADD CONSTRAINT T_ILI2DB_BASKET_dataset_fkey FOREIGN KEY ( dataset ) REFERENCES test_ladm_snr_data.T_ILI2DB_DATASET;
CREATE UNIQUE INDEX T_ILI2DB_DATASET_datasetName_key ON test_ladm_snr_data.T_ILI2DB_DATASET (datasetName) WHERE  datasetName is not null
;
CREATE UNIQUE INDEX T_ILI2DB_MODEL_iliversion_modelName_key ON test_ladm_snr_data.T_ILI2DB_MODEL (iliversion,modelName) WHERE  iliversion is not null AND modelName is not null
;
CREATE UNIQUE INDEX T_ILI2DB_ATTRNAME_SqlName_ColOwner_key ON test_ladm_snr_data.T_ILI2DB_ATTRNAME (SqlName,ColOwner) WHERE  SqlName is not null AND ColOwner is not null
;
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz','snr_estructuramatriculamatriz');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_predio_registro_fuente_cabidalinderos','snr_predio_registro_fuente_cabidalinderos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.SNR_CalidadDerechoTipo','snr_calidadderechotipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho','snr_fuentederecho');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular','snr_titular');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_predio','snr_derecho_predio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.SNR_FuenteTipo','snr_fuentetipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.SNR_DocumentoTitularTipo','snr_documentotitulartipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.SNR_ClasePredioRegistroTipo','snr_clasepredioregistrotipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo','extarchivo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho','snr_titular_derecho');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro','snr_predioregistro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_fuente_derecho','snr_derecho_fuente_derecho');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos','snr_fuentecabidalinderos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.SNR_PersonaTitularTipo','snr_personatitulartipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho','snr_derecho');
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Espacio_De_Nombres','espacio_de_nombres','extarchivo',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_fuente_derecho.snr_fuente_derecho','snr_fuente_derecho','snr_derecho','snr_fuentederecho');
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Datos','datos','extarchivo',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Tipo_Documento','tipo_documento','snr_fuentederecho',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Cabida_Linderos','cabida_linderos','snr_predioregistro',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Clase_Suelo_Registro','clase_suelo_registro','snr_predioregistro',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_predio_registro_fuente_cabidalinderos.snr_fuente_cabidalinderos','snr_fuente_cabidalinderos','snr_predioregistro','snr_fuentecabidalinderos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Archivo','snr_fuentecabidalndros_archivo','extarchivo','snr_fuentecabidalinderos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Ciudad_Emisora','ciudad_emisora','snr_fuentederecho',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Numero_Documento','numero_documento','snr_fuentecabidalinderos',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.snr_titular','snr_titular','snr_titular_derecho','snr_titular');
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Tipo_Persona','tipo_persona','snr_titular',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Extraccion','extraccion','extarchivo',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Nomenclatura_Registro','nomenclatura_registro','snr_predioregistro',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Aceptacion','fecha_aceptacion','extarchivo',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Segundo_Apellido','segundo_apellido','snr_titular',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Tipo_Documento','tipo_documento','snr_fuentecabidalinderos',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Ente_Emisor','ente_emisor','snr_fuentederecho',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Tipo_Documento','tipo_documento','snr_titular',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Numero_Predial_Anterior_en_FMI','numero_predial_anterior_en_fmi','snr_predioregistro',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.Porcentaje_Participacion','porcentaje_participacion','snr_titular_derecho',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Local_Id','local_id','extarchivo',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Entrega','fecha_entrega','extarchivo',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Nombres','nombres','snr_titular',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Matricula_Inmobiliaria','matricula_inmobiliaria','snr_predioregistro',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Matricula_Inmobiliaria_Matriz','snr_predioregistro_matricula_inmobiliaria_matriz','snr_estructuramatriculamatriz','snr_predioregistro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Ente_Emisor','ente_emisor','snr_fuentecabidalinderos',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Fecha_Documento','fecha_documento','snr_fuentederecho',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Ciudad_Emisora','ciudad_emisora','snr_fuentecabidalinderos',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Numero_Documento','numero_documento','snr_titular',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Codigo_ORIP','codigo_orip','snr_predioregistro',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Razon_Social','razon_social','snr_titular',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.snr_derecho','snr_derecho','snr_titular_derecho','snr_derecho');
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Numero_Documento','numero_documento','snr_fuentederecho',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Fecha_Documento','fecha_documento','snr_fuentecabidalinderos',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Fecha_Datos','fecha_datos','snr_predioregistro',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho.Calidad_Derecho_Registro','calidad_derecho_registro','snr_derecho',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho.Codigo_Naturaleza_Juridica','codigo_naturaleza_juridica','snr_derecho',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_predio.snr_predio_registro','snr_predio_registro','snr_derecho','snr_predioregistro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Grabacion','fecha_grabacion','extarchivo',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz.Matricula_Inmobiliaria','matricula_inmobiliaria','snr_estructuramatriculamatriz',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz.Codigo_ORIP','codigo_orip','snr_estructuramatriculamatriz',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Numero_Predial_Nuevo_en_FMI','numero_predial_nuevo_en_fmi','snr_predioregistro',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Primer_Apellido','primer_apellido','snr_titular',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz','ch.ehi.ili2db.inheritance','newAndSubClass');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_predio_registro_fuente_cabidalinderos','ch.ehi.ili2db.inheritance','embedded');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo','ch.ehi.ili2db.inheritance','newAndSubClass');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho','ch.ehi.ili2db.inheritance','newAndSubClass');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro','ch.ehi.ili2db.inheritance','newAndSubClass');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_fuente_derecho','ch.ehi.ili2db.inheritance','embedded');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos','ch.ehi.ili2db.inheritance','newAndSubClass');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho','ch.ehi.ili2db.inheritance','newAndSubClass');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular','ch.ehi.ili2db.inheritance','newAndSubClass');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_predio','ch.ehi.ili2db.inheritance','embedded');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho','ch.ehi.ili2db.inheritance','newAndSubClass');
INSERT INTO test_ladm_snr_data.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_predio',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_predio_registro_fuente_cabidalinderos',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_fuente_derecho',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho',NULL);
INSERT INTO test_ladm_snr_data.snr_personatitulartipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Persona_Natural',0,'Persona natural','0','Se refiere a la persona humana.','Submodelo_Insumos_SNR_V1_0.SNR_PersonaTitularTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_personatitulartipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Persona_Juridica',1,'Persona jurídica','0','Se llama persona jurídica, una persona ficticia, capaz de ejercer derechos y contraer obligaciones civiles, y de ser representada judicial y extrajudicialmente. Las personas jurídicas son de dos especies: corporaciones y fundaciones de beneficencia pública.','Submodelo_Insumos_SNR_V1_0.SNR_PersonaTitularTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_calidadderechotipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Dominio',0,'Dominio','0','El dominio que se llama también propiedad es el derecho real en una cosa corporal, para gozar y disponer de ella arbitrariamente, no siendo contra ley o contra derecho ajeno. (Art. 669 CC):

0100
0101
0102
0103
0106
0107
0108
0109
0110
0111
0112
0113
0114
0115
0116
0117
0118
0119
0120
0121
0122
0124
0125
0126
0127
0128
0129
0130
0131
0132
0133
0135
0137
0138
0139
0140
0141
0142
0143
0144
0145
0146
0147
0148
0150
0151
0152
0153
0154
0155
0156
0157
0158
0159
0160
0161
0163
0164
0165
0166
0167
0168
0169
0171
0172
0173
0175
0177
0178
0179
0180
0181
0182
0183
0184
0185
0186
0187
0188
0189
0190
0191
0192
0193
0194
0195
0196
0197
0198
0199
01003
01004
01005
01006
01007
01008
01009
01010
01012
01013
01014
0301
0307
0321
0332
0348
0356
0374
0375
0376
0377
0906
0907
0910
0911
0912
0913
0915
0917
0918
0919
0920
0924
0935
0959
0962
0963','Submodelo_Insumos_SNR_V1_0.SNR_CalidadDerechoTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_calidadderechotipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Falsa_Tradicion',1,'Falsa tradición','0','Es la inscripción en la Oficina de Registro de Instrumentos Públicos, de todo acto de transferencia de un derecho incompleto que se hace a favor de una persona, por parte de quien carece del derecho de dominio sobre determinado inmueble:

0600
0601
0602
0604
0605
0606
0607
0608
0609
0610
0611
0613
0614
0615
0616
0617
0618
0619
0620
0621
0622
0136
0508
0927','Submodelo_Insumos_SNR_V1_0.SNR_CalidadDerechoTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_calidadderechotipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Nuda_Propiedad',2,'Nuda propiedad','0','La propiedad separada del goce de la cosa se llama mera o nuda propiedad (art 669 CC):

Códigos:

0302
0308
0322
0349
0379','Submodelo_Insumos_SNR_V1_0.SNR_CalidadDerechoTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_calidadderechotipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Derecho_Propiedad_Colectiva',3,'Derecho de propiedad colectiva','0','Es la propiedad de toda una comunidad sea indígena o negra. Adjudicacion Baldios En Propiedad Colectiva A Comunidades Negras, Adjudicacion Baldios Resguardos Indigenas, Constitución Resguardo Indigena,
Ampliación De Resguardo Indígena

Códigos:

0104
0105
01001
01002','Submodelo_Insumos_SNR_V1_0.SNR_CalidadDerechoTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_calidadderechotipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Usufructo',4,'Usufructo','0','El derecho de usufructo es un derecho real que consiste en la facultad de gozar de una cosa con cargo de conservar su forma y sustancia, y de restituir a su dueño, si la cosa no es fungible; o con cargo de volver igual cantidad y calidad del mismo género, o de pagar su valor si la cosa es fungible. (art. 823 CC):

0310
0314
0323
0333
0378
0380
0382
0383','Submodelo_Insumos_SNR_V1_0.SNR_CalidadDerechoTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_clasepredioregistrotipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Rural',0,'Rural','0','Constituyen esta categoría los terrenos no aptos para el uso urbano, por razones de oportunidad, o por su destinación a usos agrícolas, ganaderos, forestales, de explotación de recursos naturales y actividades análogas. (Artículo 33, Ley 388 de 1997)','Submodelo_Insumos_SNR_V1_0.SNR_ClasePredioRegistroTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_clasepredioregistrotipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Urbano',1,'Urbano','0','Constituyen el suelo urbano, las áreas del territorio distrital o municipal destinadas a usos urbanos por el plan de ordenamiento, que cuenten con infraestructura vial y redes primarias de energía, acueducto y alcantarillado, posibilitándose su urbanización y edificación, según sea el caso. Podrán pertenecer a esta categoría aquellas zonas con procesos de urbanización incompletos, comprendidos en áreas consolidadas con edificación, que se definan como áreas de mejoramiento integral en los planes de ordenamiento territorial.

Las áreas que conforman el suelo urbano serán delimitadas por perímetros y podrán incluir los centros poblados de los corregimientos. En ningún caso el perímetro urbano podrá ser mayor que el denominado perímetro de servicios públicos o sanitario. (Artículo 31, Ley 388 de 1997)','Submodelo_Insumos_SNR_V1_0.SNR_ClasePredioRegistroTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_clasepredioregistrotipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Sin_Informacion',2,'Sin información','0',NULL,'Submodelo_Insumos_SNR_V1_0.SNR_ClasePredioRegistroTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_documentotitulartipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Cedula_Ciudadania',0,'Cédula de ciudadanía','0','Es un documento emitido por la Registraduría Nacional del Estado Civil para permitir la identificación personal de los ciudadanos.','Submodelo_Insumos_SNR_V1_0.SNR_DocumentoTitularTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_documentotitulartipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Cedula_Extranjeria',1,'Cédula de extranjería','0','Es el documento que cumple los fines de identificación de los extranjeros en el territorio nacional y su utilización deberá estar acorde con la visa otorgada al extranjero.','Submodelo_Insumos_SNR_V1_0.SNR_DocumentoTitularTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_documentotitulartipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'NIT',2,'NIT','0','El Número de Identificación Tributaria (NIT) es un código privado, secreto e intransferible que solamente debe conocer el contribuyente.','Submodelo_Insumos_SNR_V1_0.SNR_DocumentoTitularTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_documentotitulartipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Tarjeta_Identidad',3,'Tarjeta de identidad','0','Es el documento oficial que hace las veces de identificación para los menores de edad entre los 7 y los 18 años.','Submodelo_Insumos_SNR_V1_0.SNR_DocumentoTitularTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_documentotitulartipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Registro_Civil',4,'Registro civil','0','Registro donde se hacen constar por autoridades competentes los nacimientos, matrimonios, defunciones y demás hechos relativos al estado civil de las personas. En el modelo se tendrá en cuenta el número de registro como identificación personal de las personas de 0 a 7 años.','Submodelo_Insumos_SNR_V1_0.SNR_DocumentoTitularTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_documentotitulartipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'NUIP',5,'NUIP','0','El Número Único de Identificación Personal, es el número que permite identificar a los colombianos durante toda su vida.','Submodelo_Insumos_SNR_V1_0.SNR_DocumentoTitularTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_documentotitulartipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Secuencial_SNR',6,'Secuencial SNR','0','Es un consecutivo asignado automáticamente en registro en lugar del número de la identificación de la persona que hace el trámite, se usa especialmente en trámites de construcción cuando el proyecto está a nombre de una Fiducia el cual tiene el mismo número del banco.','Submodelo_Insumos_SNR_V1_0.SNR_DocumentoTitularTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_fuentetipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Acto_Administrativo',0,'Acto administrativo','0','Un acto administrativo es toda manifestación o declaración emanada de la administración pública en el ejercicio de potestades administrativas, mediante el que impone su voluntad sobre los derechos, libertades o intereses de otros sujetos públicos o privados y que queda bajo el del comienzo.','Submodelo_Insumos_SNR_V1_0.SNR_FuenteTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_fuentetipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Escritura_Publica',1,'Escritura pública','0','Una escritura pública es un documento público en el que se realiza ante un notario público un determinado hecho o un derecho autorizado por dicho fedatario público, que firma con el otorgante u otorgantes,mostrando sobre la capacidad jurídica del contenido y de la fecha en que se realizó','Submodelo_Insumos_SNR_V1_0.SNR_FuenteTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_fuentetipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Sentencia_Judicial',2,'Sentencia judicial','0','La sentencia es la resolución judicial definitiva dictada por un juez o tribunal que pone fin a la litis o caso sometido a su conocimiento y cierra definitivamente su actuación en el mismo','Submodelo_Insumos_SNR_V1_0.SNR_FuenteTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_fuentetipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Documento_Privado',3,'Documento privado','0','Documento que contiene un compromiso entre dos o más personas que lo firman.','Submodelo_Insumos_SNR_V1_0.SNR_FuenteTipo',NULL);
INSERT INTO test_ladm_snr_data.snr_fuentetipo (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Sin_Documento',4,'Sin documento','0','Cuando no se haya documento soporte pero puede ser una declaración verbal.','Submodelo_Insumos_SNR_V1_0.SNR_FuenteTipo',NULL);
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_derecho',NULL,'codigo_naturaleza_juridica','ch.ehi.ili2db.dispName','Código naturaleza jurídica');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_titular',NULL,'primer_apellido','ch.ehi.ili2db.dispName','Primer apellido');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('extarchivo',NULL,'fecha_grabacion','ch.ehi.ili2db.dispName','Fecha de grabación');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_estructuramatriculamatriz',NULL,'codigo_orip','ch.ehi.ili2db.dispName','Código ORIP');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_fuentecabidalinderos',NULL,'tipo_documento','ch.ehi.ili2db.foreignKey','snr_fuentetipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_fuentecabidalinderos',NULL,'tipo_documento','ch.ehi.ili2db.dispName','Tipo de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('extarchivo',NULL,'snr_fuentecabidalndros_archivo','ch.ehi.ili2db.foreignKey','snr_fuentecabidalinderos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_derecho',NULL,'snr_fuente_derecho','ch.ehi.ili2db.foreignKey','snr_fuentederecho');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_titular_derecho',NULL,'snr_derecho','ch.ehi.ili2db.foreignKey','snr_derecho');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_predioregistro',NULL,'snr_fuente_cabidalinderos','ch.ehi.ili2db.foreignKey','snr_fuentecabidalinderos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_fuentederecho',NULL,'fecha_documento','ch.ehi.ili2db.dispName','Fecha del documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_titular',NULL,'numero_documento','ch.ehi.ili2db.dispName','Número de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_predioregistro',NULL,'codigo_orip','ch.ehi.ili2db.dispName','Código ORIP');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('extarchivo',NULL,'extraccion','ch.ehi.ili2db.dispName','Extracción');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_fuentederecho',NULL,'ciudad_emisora','ch.ehi.ili2db.dispName','Ciudad emisora');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_predioregistro',NULL,'cabida_linderos','ch.ehi.ili2db.textKind','MTEXT');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_predioregistro',NULL,'cabida_linderos','ch.ehi.ili2db.dispName','Cabida y linderos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_fuentecabidalinderos',NULL,'ente_emisor','ch.ehi.ili2db.dispName','Ente emisor');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_fuentecabidalinderos',NULL,'ciudad_emisora','ch.ehi.ili2db.dispName','Ciudad emisora');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_predioregistro',NULL,'numero_predial_anterior_en_fmi','ch.ehi.ili2db.dispName','Número predial anterior en FMI');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_titular',NULL,'tipo_documento','ch.ehi.ili2db.foreignKey','snr_documentotitulartipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_titular',NULL,'tipo_documento','ch.ehi.ili2db.dispName','Tipo de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_predioregistro',NULL,'numero_predial_nuevo_en_fmi','ch.ehi.ili2db.dispName','Número predial nuevo en FMI');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_titular_derecho',NULL,'snr_titular','ch.ehi.ili2db.foreignKey','snr_titular');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('extarchivo',NULL,'fecha_aceptacion','ch.ehi.ili2db.dispName','Fecha de aceptación');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_fuentederecho',NULL,'ente_emisor','ch.ehi.ili2db.textKind','MTEXT');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_fuentederecho',NULL,'ente_emisor','ch.ehi.ili2db.dispName','Ente emisor');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_predioregistro',NULL,'fecha_datos','ch.ehi.ili2db.dispName','Fecha de datos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_fuentederecho',NULL,'numero_documento','ch.ehi.ili2db.dispName','Número de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('extarchivo',NULL,'fecha_entrega','ch.ehi.ili2db.dispName','Fecha de entrega');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_titular',NULL,'nombres','ch.ehi.ili2db.dispName','Nombres');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_predioregistro',NULL,'matricula_inmobiliaria','ch.ehi.ili2db.dispName','Matrícula inmobiliaria');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_estructuramatriculamatriz',NULL,'snr_predioregistro_matricula_inmobiliaria_matriz','ch.ehi.ili2db.foreignKey','snr_predioregistro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_fuentecabidalinderos',NULL,'fecha_documento','ch.ehi.ili2db.dispName','Fecha de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('extarchivo',NULL,'espacio_de_nombres','ch.ehi.ili2db.dispName','Espacio de nombres');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('extarchivo',NULL,'datos','ch.ehi.ili2db.dispName','Datos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_predioregistro',NULL,'nomenclatura_registro','ch.ehi.ili2db.dispName','Nomenclatura según registro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_derecho',NULL,'snr_predio_registro','ch.ehi.ili2db.foreignKey','snr_predioregistro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_titular',NULL,'segundo_apellido','ch.ehi.ili2db.dispName','Segundo apellido');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('extarchivo',NULL,'local_id','ch.ehi.ili2db.dispName','Local ID');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_derecho',NULL,'calidad_derecho_registro','ch.ehi.ili2db.foreignKey','snr_calidadderechotipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_derecho',NULL,'calidad_derecho_registro','ch.ehi.ili2db.dispName','Calidad derecho registro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_titular',NULL,'tipo_persona','ch.ehi.ili2db.foreignKey','snr_personatitulartipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_titular',NULL,'tipo_persona','ch.ehi.ili2db.dispName','Tipo de persona');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_estructuramatriculamatriz',NULL,'matricula_inmobiliaria','ch.ehi.ili2db.dispName','Matrícula inmobiliaria');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_predioregistro',NULL,'clase_suelo_registro','ch.ehi.ili2db.foreignKey','snr_clasepredioregistrotipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_predioregistro',NULL,'clase_suelo_registro','ch.ehi.ili2db.dispName','Clase del suelo según registro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_fuentecabidalinderos',NULL,'numero_documento','ch.ehi.ili2db.dispName','Número de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_fuentederecho',NULL,'tipo_documento','ch.ehi.ili2db.foreignKey','snr_fuentetipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_fuentederecho',NULL,'tipo_documento','ch.ehi.ili2db.dispName','Tipo de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_titular',NULL,'razon_social','ch.ehi.ili2db.textKind','MTEXT');
INSERT INTO test_ladm_snr_data.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('snr_titular',NULL,'razon_social','ch.ehi.ili2db.dispName','Razón social');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_calidadderechotipo','ch.ehi.ili2db.tableKind','ENUM');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_fuentederecho','ch.ehi.ili2db.tableKind','CLASS');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_fuentederecho','ch.ehi.ili2db.dispName','(SNR) Fuente Derecho');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_documentotitulartipo','ch.ehi.ili2db.tableKind','ENUM');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_fuentetipo','ch.ehi.ili2db.tableKind','ENUM');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_titular','ch.ehi.ili2db.tableKind','CLASS');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_titular','ch.ehi.ili2db.dispName','(SNR) Titular');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('extarchivo','ch.ehi.ili2db.tableKind','STRUCTURE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('extarchivo','ch.ehi.ili2db.dispName','Archivo fuente');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_clasepredioregistrotipo','ch.ehi.ili2db.tableKind','ENUM');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_estructuramatriculamatriz','ch.ehi.ili2db.tableKind','STRUCTURE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_estructuramatriculamatriz','ch.ehi.ili2db.dispName','(SNR) Estructura Matrícula Matriz');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_personatitulartipo','ch.ehi.ili2db.tableKind','ENUM');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_fuentecabidalinderos','ch.ehi.ili2db.tableKind','CLASS');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_fuentecabidalinderos','ch.ehi.ili2db.dispName','(SNR) Fuente Cabida Linderos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_derecho','ch.ehi.ili2db.tableKind','CLASS');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_derecho','ch.ehi.ili2db.dispName','(SNR) Derecho');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_predioregistro','ch.ehi.ili2db.tableKind','CLASS');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_predioregistro','ch.ehi.ili2db.dispName','(SNR) Predio Registro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('snr_titular_derecho','ch.ehi.ili2db.tableKind','ASSOCIATION');
INSERT INTO test_ladm_snr_data.T_ILI2DB_MODEL (filename,iliversion,modelName,content,importDate) VALUES ('LADM_COL_V3_0.ili','2.3','LADM_COL_V3_0{ ISO19107_PLANAS_V3_0}','INTERLIS 2.3;

/** ISO 19152 LADM country profile COL Core Model.
 * 
 * -----------------------------------------------------------
 * 
 * LADM es un modelo conceptual de la realidad que concreta una ontología y establece una semántica para la administración del territorio.
 * 
 * -----------------------------------------------------------
 *  revision history
 * -----------------------------------------------------------
 * 
 *  30.01.2018/fm : Cambio del tipo de dato del atributo Ext_Direccion de la clase Unidad Espacial a ExtDireccion; atributo ext_PID de la calse LA_Interesado cambia de OID a ExtInteresado; Cambio de cardinalidad en relacion miembros entre LA_Interesado y LA_Agrupacion_Interesados de 0..1 a 0..*
 *  07.02.2018/fm-gc: Ajuste al tipo de dato de la unidad Peso, pasa a tener precision 1 para evitar ser tratado cmo atributo entero y aumentar su tamaño
 *  19.02.2018/fm-gc: ampliación del dominio al tipo de dato Peso
 *  26.02.2018/fm-lj: cambio del nombre del dominio ISO19125_Type a ISO19125_Tipo
 *  19.04.2018/vb fm: Ajuste al constraint Fraccion, denominador mayor a 0
 *  19.04.2018/vb fm: Cambio en la cardinalidad del atributo u_Local_Id de la clase LA_BAUnit de 0..1 a 1
 * 17.07.2018/fm : se incluye escritura en dominio COL_FuenteAdministrativaTipo
 * 10.08.2018/fm : Se eliminan los atributos ai_local_id y ai_espacio_de_nombres de la clase LA_Agrupacion_Interesados
 * 27.08.2018/fm : Ajuste a la cardinalidad de asociacion puntoFuente de 1..* a 0..*
 * 25.09.2018/at: Se ajusta la longitud del atributo Codigo_Registral_Transaccion en la clase COL_FuenteAdministrativa a 5 caracteres de acuerdo a la Resolución 3973 de 2018
 * -----------------------------------------------------------
 * 
 *  (c) IGAC y SNR con apoyo de la Cooperacion Suiza
 * 
 * -----------------------------------------------------------
 */
MODEL LADM_COL_V3_0 (es)
AT "http://www.proadmintierra.info/"
VERSION "V1.2.0"  // 2019-08-13 // =
  IMPORTS ISO19107_PLANAS_V3_0;

  UNIT

    PesoColombiano [COP] EXTENDS INTERLIS.MONEY;

    Area (ABSTRACT) = (INTERLIS.LENGTH * INTERLIS.LENGTH);

    MetroCuadrado [m2] EXTENDS Area = (INTERLIS.m * INTERLIS.m);

    Centrimetro [cm] = 1 / 100 [INTERLIS.m];

  TOPIC LADM_Nucleo(ABSTRACT) =

    DOMAIN

      CharacterString = TEXT*255;

      /** Traducción del dominio CI_PresentationFormCode de la norma ISO 19115:2003. Indica el modo en el que se representan los datos.
       */
      CI_Forma_Presentacion_Codigo = (
        /** Definición en la ISO 19115:2003.
         */
        !!@ ili2db.dispName = "Imagen"
        Imagen,
        !!@ ili2db.dispName = "Documento"
        Documento,
        /** Definición en la ISO 19115:2003.
         */
        !!@ ili2db.dispName = "Mapa"
        Mapa,
        /** Definición en la ISO 19115:2003.
         */
        !!@ ili2db.dispName = "Video"
        Video,
        /** Definición en la ISO 19115:2003.
         */
        !!@ ili2db.dispName = "Otro"
        Otro
      );

      COL_AreaTipo = (
        /** Corresponde al área gráfica inscrita en la base de datos catastral sobre un predio antes de efectuar la transformación al nuevo sistema de proyección para catastro.
         */
        !!@ ili2db.dispName = "Area catastral gráfica del predio"
        Area_Catastral_Grafica,
        /** Corresponde al área alfanumérica inscrita en la base de datos catastral sobre un predio antes de efectuar la transformación al nuevo sistema de proyección para catastro. En la mayoría de los casos el área alfanumérica corresponde al valor de área inscrita en los datos de Registro.
         */
        !!@ ili2db.dispName = "Area catastral alfanumérica"
        Area_Catastral_Alfanumerica
      );

      COL_ContenidoNivelTipo = (
        !!@ ili2db.dispName = "Construcción convencional"
        Construccion_Convencional,
        !!@ ili2db.dispName = "Construcción no convencional"
        Construccion_No_Convencional,
        !!@ ili2db.dispName = "Consuetudinario"
        Consuetudinario,
        !!@ ili2db.dispName = "Formal"
        Formal,
        !!@ ili2db.dispName = "Informal"
        Informal,
        !!@ ili2db.dispName = "Responsabilidad"
        Responsabilidad,
        !!@ ili2db.dispName = "Restricción derecho público"
        Restriccion_Derecho_Publico,
        !!@ ili2db.dispName = "Restricción derecho privado"
        Restriccion_Derecho_Privado
      );

      COL_DimensionTipo = (
        !!@ ili2db.dispName = "Dimensión 2D"
        Dim2D,
        !!@ ili2db.dispName = "Dimensión 3D"
        Dim3D,
        !!@ ili2db.dispName = "Otro"
        Otro
      );

      COL_EstadoRedServiciosTipo = (
        !!@ ili2db.dispName = "Planeado"
        Planeado,
        !!@ ili2db.dispName = "En uso"
        En_Uso,
        !!@ ili2db.dispName = "Fuera de servicio"
        Fuera_De_Servicio,
        !!@ ili2db.dispName = "Otro"
        Otro
      );

      COL_EstructuraTipo = (
        !!@ ili2db.dispName = "Croquis"
        Croquis,
        !!@ ili2db.dispName = "Línea no estructurada"
        Linea_no_Estructurada,
        !!@ ili2db.dispName = "Texto"
        Texto,
        !!@ ili2db.dispName = "Topológico"
        Topologico
      );

      COL_FuenteEspacialTipo = (
        /** Ilustración análoga del levantamiento catastral de un predio.
         */
        !!@ ili2db.dispName = "Croquis de campo"
        Croquis_Campo,
        /** Datos tomados por un equipo GNSS sin ningún tipo de postprocesamiento.
         */
        !!@ ili2db.dispName = "Datos crudos (GPS, Estación total, LiDAR, etc.)"
        Datos_Crudos,
        /** Imagen producto de la toma de fotografías aéreas o satélites, en la cual han sido corregidos los desplazamientos causados por la inclinación de la cámara o sensor y la curvatura de la superficie del terreno. Está referida a un sistema de proyección cartográfica, por lo que posee las características geométricas de un mapa con el factor adicional de que los objetos se encuentran representados de forma real en la imagen de la fotográfica.
         */
        !!@ ili2db.dispName = "Ortofoto"
        Ortofoto,
        /** Informe técnico de levantamiento catastral de un predio.
         */
        !!@ ili2db.dispName = "Informe técnico"
        Informe_Tecnico,
        /** Registro fotográfico del levantamiento catastral de un predio.
         */
        !!@ ili2db.dispName = "Registro fotográfico"
        Registro_Fotografico
      );

      COL_GrupoInteresadoTipo = (
        /** Agrupación de personas naturales.
         */
        !!@ ili2db.dispName = "Grupo civil"
        Grupo_Civil,
        /** Agrupación de personas jurídicas.
         */
        !!@ ili2db.dispName = "Grupo empresarial"
        Grupo_Empresarial,
        /** Agrupación de personas pertenecientes a un grupo étnico.
         */
        !!@ ili2db.dispName = "Grupo étnico"
        Grupo_Etnico,
        /** Agrupación de personas naturales y jurídicas.
         */
        !!@ ili2db.dispName = "Grupo mixto"
        Grupo_Mixto
      );

      /** Si ha sido situado por interpolación, de qué manera se ha hecho.
       */
      COL_InterpolacionTipo = (
        !!@ ili2db.dispName = "Aislado"
        Aislado,
        !!@ ili2db.dispName = "Intermedio arco"
        Intermedio_Arco,
        !!@ ili2db.dispName = "Intermedio línea"
        Intermedio_Linea
      );

      COL_MetodoProduccionTipo = (
        /** Aquellos que requieren una visita campo con el fin de
         * recolectar la realidad de los bienes inmuebles.
         */
        !!@ ili2db.dispName = "Método directo"
        Metodo_Directo,
        /** aquellos métodos identificación física, jurídica y
         * económica de los inmuebles a través del uso de de sensores
         * remotos, integración registros administrativos, modelos ísticos y
         * econométricos, análisis de Big Data y fuentes secundarias como
         * observatorios inmobiliarios, su posterior incorporación en la base catastral.
         */
        !!@ ili2db.dispName = "Método indirecto"
        Metodo_Indirecto,
        /** Son los derivados participación de la comunidad en el suministro de información que sirva como insumo para el desarrollo de los procesos catastrales. Los gestores catastrales propenderán por la adopción nuevas tecnologías y procesos comunitarios que faciliten la participación los ciudadanos.
         */
        !!@ ili2db.dispName = "Metodo declarativo y colaborativo"
        Metodo_Declarativo_y_Colaborativo
      );

      COL_PuntoTipo = (
        !!@ ili2db.dispName = "Control"
        Control,
        !!@ ili2db.dispName = "Catastro"
        Catastro,
        !!@ ili2db.dispName = "Otro"
        Otro
      );

      COL_RegistroTipo = (
        !!@ ili2db.dispName = "Rural"
        Rural,
        !!@ ili2db.dispName = "Urbano"
        Urbano,
        !!@ ili2db.dispName = "Otro"
        Otro
      );

      COL_UnidadAdministrativaBasicaTipo = (
        /** Unidad administrativa básica de la temática predial.
         */
        !!@ ili2db.dispName = "Predio"
        Predio,
        /** Unidad administrativa básica de la temática de ordenamiento territorial.
         */
        !!@ ili2db.dispName = "Ordenamiento territorial"
        Ordenamiento_Territorial,
        /** Unidad administrativa básica de la temática de servicios públicos.
         */
        !!@ ili2db.dispName = "Servicios públicos"
        Servicios_Publicos,
        /** Unidad administrativa básica de la temática de reservas naturales.
         */
        !!@ ili2db.dispName = "Reservas naturales"
        Reservas_Naturales,
        /** Unidad administrativa básica de la temática de parques naturales.
         */
        !!@ ili2db.dispName = "Parques naturales"
        Parques_Naturales,
        /** Unidad administrativa básica de la temática de amenazas de riesgo.
         */
        !!@ ili2db.dispName = "Amenazas de riesgos"
        Amenazas_Riesgos,
        /** Unidad administrativa básica de la temática de servidumbres.
         */
        !!@ ili2db.dispName = "Servidumbre"
        Servidumbre,
        /** Unidad administrativa básica de la temática de superficies de agua.
         */
        !!@ ili2db.dispName = "Superficies de agua"
        Superficies_Agua,
        /** Unidad administrativa básica de la temática de transporte.
         */
        !!@ ili2db.dispName = "Transporte"
        Transporte
      );

      COL_VolumenTipo = (
        !!@ ili2db.dispName = "Oficial"
        Oficial,
        !!@ ili2db.dispName = "Calculado"
        Calculado,
        !!@ ili2db.dispName = "Otro"
        Otro
      );

      Integer = 0 .. 999999999;

      COL_EstadoDisponibilidadTipo = (
        /** La fuente fue convertida o recibió algún tratamiento.
         */
        !!@ ili2db.dispName = "Convertido"
        Convertido,
        /** Se desconoce la disponibilidad de la fuente.
         */
        !!@ ili2db.dispName = "Desconocido"
        Desconocido,
        /** La fuente está disponible.
         */
        !!@ ili2db.dispName = "Disponible"
        Disponible
      );

      COL_ISO19125_Tipo = (
        !!@ ili2db.dispName = "Disjunto"
        Disjunto,
        !!@ ili2db.dispName = "Toca"
        Toca,
        !!@ ili2db.dispName = "Superpone"
        Superpone,
        !!@ ili2db.dispName = "Desconocido"
        Desconocido
      );

      COL_RelacionSuperficieTipo = (
        !!@ ili2db.dispName = "En rasante"
        En_Rasante,
        !!@ ili2db.dispName = "En vuelo"
        En_Vuelo,
        !!@ ili2db.dispName = "En subsuelo"
        En_Subsuelo,
        !!@ ili2db.dispName = "Otro"
        Otro
      );

      COL_UnidadEdificacionTipo = (
        !!@ ili2db.dispName = "Compartido"
        Compartido,
        !!@ ili2db.dispName = "Individual"
        Individual
      );

      Currency = -2000000000.00 .. 2000000000.00;

      Real = 0.000 .. 999999999.999;

    /** Estructura que proviene de la traducción de la clase CC_OperationMethod de la ISO 19111. Indica el método utilizado, mediante un algoritmo o un procedimiento, para realizar operaciones con coordenadas.
     */
    STRUCTURE CC_MetodoOperacion =
      /** Fórmulas o procedimientos utilizadoa por este método de operación de coordenadas. Esto puede ser una referencia a una publicación. Tenga en cuenta que el método de operación puede no ser analítico, en cuyo caso este atributo hace referencia o contiene el procedimiento, no una fórmula analítica.
       */
      !!@ ili2db.dispName = "Fórmula"
      Formula : MANDATORY CharacterString;
      /** Número de dimensiones en la fuente CRS de este método de operación de coordenadas.
       */
      !!@ ili2db.dispName = "Dimensiones origen"
      Dimensiones_Origen : Integer;
      /** Número de dimensiones en el CRS de destino de este método de operación de coordenadas.
       */
      !!@ ili2db.dispName = "Ddimensiones objetivo"
      Ddimensiones_Objetivo : Integer;
    END CC_MetodoOperacion;

    !!@ ili2db.dispName = "Valores de área"
    STRUCTURE COL_AreaValor =
      /** Indica si el valor a registrar corresponde al área gráfica o alfanumérica de la base de datos catastral.
       */
      !!@ ili2db.dispName = "Tipo"
      Tipo : MANDATORY COL_AreaTipo;
      /** Corresponde al valor del área registrada en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Área"
      Area : MANDATORY 0.0 .. 99999999999999.9 [LADM_COL_V3_0.m2];
      /** Parametros de la proyección utilizada para el cálculo del área de la forma proj, ejemplo: ''EPSG:3116'', ''+proj=tmerc +lat_0=4.59620041666667 +lon_0=-74.0775079166667 +k=1 +x_0=1000000 +y_0=1000000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs''
       */
      !!@ ili2db.dispName = "Datos de la proyección"
      Datos_Proyeccion : TEXT;
    END COL_AreaValor;

    /** Referencia a una clase externa para gestionar direcciones.
     */
    !!@ ili2db.dispName = "Dirección"
    STRUCTURE ExtDireccion =
      !!@ ili2db.dispName = "Tipo de dirección"
      Tipo_Direccion : MANDATORY (
        !!@ ili2db.dispName = "Estructurada"
        Estructurada,
        !!@ ili2db.dispName = "No estructurada"
        No_Estructurada
      );
      !!@ ili2db.dispName = "Es dirección principal"
      Es_Direccion_Principal : BOOLEAN;
      /** Par de valores georreferenciados (x,y) en la que se encuentra la dirección.
       */
      !!@ ili2db.dispName = "Localización"
      Localizacion : ISO19107_PLANAS_V3_0.GM_Point3D;
      !!@ ili2db.dispName = "Código postal"
      Codigo_Postal : CharacterString;
      !!@ ili2db.dispName = "Clase de vía principal"
      Clase_Via_Principal : (
        !!@ ili2db.dispName = "Avenida calle"
        Avenida_Calle,
        !!@ ili2db.dispName = "Avenida carrera"
        Avenida_Carrera,
        !!@ ili2db.dispName = "Avenida"
        Avenida,
        !!@ ili2db.dispName = "Autopista"
        Autopista,
        !!@ ili2db.dispName = "Circunvalar"
        Circunvalar,
        !!@ ili2db.dispName = "Calle"
        Calle,
        !!@ ili2db.dispName = "Carrera"
        Carrera,
        !!@ ili2db.dispName = "Diagonal"
        Diagonal,
        !!@ ili2db.dispName = "Transversal"
        Transversal,
        !!@ ili2db.dispName = "Circular"
        Circular
      );
      !!@ ili2db.dispName = "Valor vía principal"
      Valor_Via_Principal : TEXT*100;
      !!@ ili2db.dispName = "Letra vía principal"
      Letra_Via_Principal : TEXT*20;
      !!@ ili2db.dispName = "Sector de la ciudad"
      Sector_Ciudad : (
        Norte,
        Sur,
        Este,
        Oeste
      );
      !!@ ili2db.dispName = "Valor de vía generadora"
      Valor_Via_Generadora : TEXT*100;
      !!@ ili2db.dispName = "Letra de vía generadora"
      Letra_Via_Generadora : TEXT*20;
      !!@ ili2db.dispName = "Número del predio"
      Numero_Predio : TEXT*20;
      !!@ ili2db.dispName = "Sector del predio"
      Sector_Predio : (
        Norte,
        Sur,
        Este,
        Oeste
      );
      !!@ ili2db.dispName = "Complemento"
      Complemento : TEXT*255;
      !!@ ili2db.dispName = "Nombre del predio"
      Nombre_Predio : TEXT*255;
    END ExtDireccion;

    /** Estructura para la definición de un tipo de dato personalizado que permite indicar una fracción o quebrado cona serie específica de condiciones.
     */
    STRUCTURE Fraccion =
      /** Parte inferior de la fracción. Debe ser mayor que 0. Debe ser mayor que el numerador.
       */
      !!@ ili2db.dispName = "Denominador"
      Denominador : MANDATORY Integer;
      /** Parte superior de la fracción. Debe ser mayor que 0. Debe sder menor que el denominador.
       */
      !!@ ili2db.dispName = "Numerador"
      Numerador : MANDATORY Integer;
      MANDATORY CONSTRAINT
        Denominador > 0;
      MANDATORY CONSTRAINT
        Numerador > 0;
      MANDATORY CONSTRAINT
        Denominador >= Numerador;
    END Fraccion;

    CLASS Oid (ABSTRACT) =
      /** Identificador único global. Corresponde al atributo de la clase en LADM.
       */
      !!@ ili2db.dispName = "Espacio de nombres"
      Espacio_De_Nombres : MANDATORY CharacterString;
      /** Identificador único local.
       */
      !!@ ili2db.dispName = "Local ID"
      Local_Id : MANDATORY CharacterString;
    END Oid;

    DOMAIN

      COL_FuenteAdministrativaTipo = (
        /** Documento público es el otorgado por el funcionario público en ejercicio de sus funciones o con su intervención. Así mismo, es público el documento otorgado por un particular en ejercicio de funciones públicas o con su intervención. Cuando consiste en un escrito autorizado o suscrito por el respectivo funcionario, es instrumento público; cuando es autorizado por un notario o quien haga sus veces y ha sido incorporado en el respectivo protocolo, se denomina escritura pública.
         */
        !!@ ili2db.dispName = "Documento público"
        Documento_Publico,
        /** El documento privado es aquel documento que no cumple los requisitos del documento público, es decir, es un documento que no ha sido elaborado por un funcionario público, ni ha habido intervención de éste para su elaboración.
         */
        !!@ ili2db.dispName = "Documento privado"
        Documento_Privado
      );

      COL_RedServiciosTipo = (
        !!@ ili2db.dispName = "Petróleo"
        Petroleo,
        !!@ ili2db.dispName = "Químicos"
        Quimicos,
        !!@ ili2db.dispName = "Red térmica"
        Red_Termica,
        !!@ ili2db.dispName = "Telecomunicación"
        Telecomunicacion
      );

      Peso = 0.0 .. 999999999999999.0 [LADM_COL_V3_0.COP];

    /** Registro de la fórmula o procedimiento utilizado en la transformación y de su resultado.
     */
    STRUCTURE COL_Transformacion =
      /** Fórmula o procedimiento utilizado en la transformación.
       */
      !!@ ili2db.dispName = "Transformación"
      Transformacion : MANDATORY LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion;
      /** Geometría una vez realizado el proceso de transformación.
       */
      !!@ ili2db.dispName = "Localización transformada"
      Localizacion_Transformada : MANDATORY ISO19107_PLANAS_V3_0.GM_Point3D;
    END COL_Transformacion;

    /** Control externo de la unidad de edificación física.
     */
    STRUCTURE ExtUnidadEdificacionFisica =
      !!@ ili2db.dispName = "Ext dirección id"
      Ext_Direccion_ID : LADM_COL_V3_0.LADM_Nucleo.ExtDireccion;
    END ExtUnidadEdificacionFisica;

    /** Referencia a una imagen mediante su url.
     */
    STRUCTURE Imagen =
      /** url de la imagen.
       */
      !!@ ili2db.dispName = "uri"
      uri : CharacterString;
    END Imagen;

    /** Clase abstracta que permite gestionar el histórico del conjunto de clases, las cuales heredan de esta, excepto las fuentes.
     */
    CLASS ObjetoVersionado (ABSTRACT)
    EXTENDS Oid =
      /** Comienzo de la validez actual de la instancia de un objeto.
       */
      !!@ ili2db.dispName = "Versión de comienzo de vida útil"
      Comienzo_Vida_Util_Version : MANDATORY INTERLIS.XMLDateTime;
      /** Finalización de la validez actual de la instancia de un objeto.
       */
      !!@ ili2db.dispName = "Versión de fin de vida útil"
      Fin_Vida_Util_Version : INTERLIS.XMLDateTime;
      MANDATORY CONSTRAINT
        Fin_Vida_Util_Version >= Comienzo_Vida_Util_Version;
    END ObjetoVersionado;

    /** Referencia a una clase externa para gestionar direcciones.
     */
    STRUCTURE ExtInteresado =
      /** Identificador externo del interesado.
       */
      !!@ ili2db.dispName = "Ext dirección id"
      Ext_Direccion_ID : LADM_COL_V3_0.LADM_Nucleo.ExtDireccion;
      /** Imagen de la huella dactilar del interesado.
       */
      !!@ ili2db.dispName = "Huella dactilar"
      Huella_Dactilar : LADM_COL_V3_0.LADM_Nucleo.Imagen;
      /** Campo de nombre del interesado.
       */
      !!@ ili2db.dispName = "Nombre"
      Nombre : CharacterString;
      /** Fotografía del interesado.
       */
      !!@ ili2db.dispName = "Fotografía"
      Fotografia : LADM_COL_V3_0.LADM_Nucleo.Imagen;
      /** Firma del interesado.
       */
      !!@ ili2db.dispName = "Firma"
      Firma : LADM_COL_V3_0.LADM_Nucleo.Imagen;
      /** Ruta de almacenamiento del documento escaneado del interesado.
       */
      !!@ ili2db.dispName = "Documento escaneado"
      Documento_Escaneado : CharacterString;
    END ExtInteresado;

    /** Referencia a una clase externa para gestionar las redes físicas de servicios.
     */
    STRUCTURE ExtRedServiciosFisica =
      /** Indica si la red de servicios tiene un gradiente o no.
       */
      !!@ ili2db.dispName = "Orientada"
      Orientada : BOOLEAN;
      /** Identificador de referencia a un interesado externo que es el administrador.
       */
      !!@ ili2db.dispName = "Ext interesado administrador id"
      Ext_Interesado_Administrador_ID : LADM_COL_V3_0.LADM_Nucleo.ExtInteresado;
    END ExtRedServiciosFisica;

    /** Referencia a clase externa desde donde se gestiona el repositorio de archivos.
     */
    !!@ ili2db.dispName = "Archivo fuente"
    STRUCTURE ExtArchivo =
      /** Fecha en la que ha sido aceptado el documento.
       */
      !!@ ili2db.dispName = "Fecha de aceptación"
      Fecha_Aceptacion : INTERLIS.XMLDate;
      /** Datos que contiene el documento.
       */
      !!@ ili2db.dispName = "Datos"
      Datos : CharacterString;
      /** Última fecha de extracción del documento.
       */
      !!@ ili2db.dispName = "Extracción"
      Extraccion : INTERLIS.XMLDate;
      /** Fecha en la que el documento es aceptado en el sistema.
       */
      !!@ ili2db.dispName = "Fecha de grabación"
      Fecha_Grabacion : INTERLIS.XMLDate;
      /** Fecha en la que fue entregado el documento.
       */
      !!@ ili2db.dispName = "Fecha de entrega"
      Fecha_Entrega : INTERLIS.XMLDate;
      !!@ ili2db.dispName = "Espacio de nombres"
      Espacio_De_Nombres : MANDATORY CharacterString;
      !!@ ili2db.dispName = "Local ID"
      Local_Id : MANDATORY CharacterString;
    END ExtArchivo;

    /** Clase abstracta. Esta clase es la personalización en el modelo del perfil colombiano de la clase de LADM LA_Source.
     */
    CLASS COL_Fuente (ABSTRACT)
    EXTENDS Oid =
      /** Indica si la fuente está o no disponible y en qué condiciones. También puede indicar porqué ha dejado de estar disponible, si ha ocurrido.
       */
      !!@ ili2db.dispName = "Estado de disponibilidad"
      Estado_Disponibilidad : MANDATORY COL_EstadoDisponibilidadTipo;
      /** Identificador del archivo fuente controlado por una clase externa.
       */
      !!@ ili2db.dispName = "Ext archivo id"
      Ext_Archivo_ID : LADM_COL_V3_0.LADM_Nucleo.ExtArchivo;
      /** Tipo de formato en el que es presentada la fuente, de acuerdo con el registro de metadatos.
       */
      !!@ ili2db.dispName = "Tipo principal"
      Tipo_Principal : CI_Forma_Presentacion_Codigo;
      /** Fecha de expedición del documento de la fuente.
       */
      !!@ ili2db.dispName = "Fecha de documento fuente"
      Fecha_Documento_Fuente : INTERLIS.XMLDate;
    END COL_Fuente;

    /** Estructura para la definición de un tipo de dato personalizado que permite indicar la medición de un volumen y la naturaleza de este.
     */
    STRUCTURE COL_VolumenValor =
      /** Medición del volumen en m3.
       */
      !!@ ili2db.dispName = "Volumen medición"
      Volumen_Medicion : MANDATORY 0.0 .. 99999999999999.9 [INTERLIS.m];
      /** Indicación de si el volumen es calculado, si figura como oficial o si se da otra circunstancia.
       */
      !!@ ili2db.dispName = "Tipo"
      Tipo : MANDATORY COL_VolumenTipo;
    END COL_VolumenValor;

    /** Especialización de la clase COL_Fuente para almacenar aquellas fuentes constituidas por documentos (documento hipotecario, documentos notariales, documentos históricos, etc.) que documentan la relación entre instancias de interesados y de predios.
     */
    CLASS COL_FuenteAdministrativa (ABSTRACT)
    EXTENDS COL_Fuente =
      /** Observaciones o descripción del documento de la fuente administrativa.
       */
      !!@ ili2db.dispName = "Observación"
      Observacion : CharacterString;
      /** Tipo de documento de fuente administrativa.
       */
      !!@ ili2db.dispName = "Tipo"
      Tipo : MANDATORY COL_FuenteAdministrativaTipo;
      /** Identificador del documento, ejemplo: número de la resolución, número de la escritura pública o número de radicado de una sentencia.
       */
      !!@ ili2db.dispName = "Número de fuente"
      Numero_Fuente : TEXT*150;
    END COL_FuenteAdministrativa;

    /** Representación gráfica del terreno, construcción, unidad de construcción y/o servidumbre de paso.
     */
    CLASS COL_UnidadEspacial (ABSTRACT)
    EXTENDS ObjetoVersionado =
      /** Registros del área en diferentes sistemas.
       */
      !!@ ili2db.dispName = "Área"
      Area : LIST {0..*} OF LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor;
      /** Dimensión del objeto.
       */
      !!@ ili2db.dispName = "Dimensión"
      Dimension : COL_DimensionTipo;
      /** Corresponde al atributo extAddressID de la clase en LADM.
       */
      !!@ ili2db.dispName = "Ext dirección id"
      Ext_Direccion_ID : LIST {0..*} OF LADM_COL_V3_0.LADM_Nucleo.ExtDireccion;
      /** Corresponde al atributo label de la clase en LADM.
       */
      !!@ ili2db.dispName = "Etiqueta"
      Etiqueta : CharacterString;
      /** Corresponde al atributo surfaceRelation de la clase en LADM.
       */
      !!@ ili2db.dispName = "Relación superficie"
      Relacion_Superficie : COL_RelacionSuperficieTipo;
      /** Corresponde al atributo volume de la clase en LADM.
       */
      !!@ ili2db.dispName = "Volumen"
      Volumen : LIST {0..*} OF LADM_COL_V3_0.LADM_Nucleo.COL_VolumenValor;
      /** Materializacion del metodo createArea(). Almacena de forma permanente la geometría de tipo poligonal.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface3D;
    END COL_UnidadEspacial;

    /** Agrupa unidades espaciales, es decir, representaciones geográficas de las unidades administrativas básicas (clase LA_BAUnit) para representar otras unidades espaciales que se forman en base a estas, como puede ser el caso de los polígonos catastrales.
     */
    CLASS COL_AgrupacionUnidadesEspaciales (ABSTRACT)
    EXTENDS ObjetoVersionado =
      /** Nivel jerárquico de la agrupación, dentro del anidamiento de diferentes agrupaciones.
       */
      !!@ ili2db.dispName = "Nivel jerárquico"
      Nivel_Jerarquico : MANDATORY Integer;
      /** Definición de la agrupación.
       */
      !!@ ili2db.dispName = "Etiqueta"
      Etiqueta : CharacterString;
      /** Nombre que recibe la agrupación.
       */
      !!@ ili2db.dispName = "Nombre"
      Nombre : CharacterString;
      /** Punto de referencia de toda la agrupación, a modo de centro de masas.
       */
      !!@ ili2db.dispName = "Punto de referencia"
      Punto_Referencia : ISO19107_PLANAS_V3_0.GM_Point3D;
    END COL_AgrupacionUnidadesEspaciales;

    /** Traducción al español de la clase LA_LegalSpaceBuildingUnit. Sus intancias son las unidades de edificación
     */
    CLASS COL_EspacioJuridicoUnidadEdificacion (ABSTRACT)
    EXTENDS COL_UnidadEspacial =
      /** Identificador de la unidad de edificación.
       */
      !!@ ili2db.dispName = "Ext unidad edificación física id"
      Ext_Unidad_Edificacion_Fisica_ID : LADM_COL_V3_0.LADM_Nucleo.ExtUnidadEdificacionFisica;
      /** Tipo de unidad de edificación de la que se trata.
       */
      !!@ ili2db.dispName = "Tipo"
      Tipo : COL_UnidadEdificacionTipo;
    END COL_EspacioJuridicoUnidadEdificacion;

    ASSOCIATION col_ueJerarquiaGrupo =
      agrupacion -<> {0..1} COL_AgrupacionUnidadesEspaciales;
      elemento -- {0..*} COL_AgrupacionUnidadesEspaciales;
    END col_ueJerarquiaGrupo;

    /** Traducción al español de la clase LA_LegalSpaceUtilityNetwork. Representa un tipo de unidad espacial (LA_UNidadEspacial) cuyas instancias son las redes de servicios.
     */
    CLASS COL_EspacioJuridicoRedServicios (ABSTRACT)
    EXTENDS COL_UnidadEspacial =
      /** Identificador de la red física hacia una referencia externa.
       */
      !!@ ili2db.dispName = "Ext id red física"
      ext_ID_Red_Fisica : LADM_COL_V3_0.LADM_Nucleo.ExtRedServiciosFisica;
      /** Estado de operatividad de la red.
       */
      !!@ ili2db.dispName = "Estado"
      Estado : COL_EstadoRedServiciosTipo;
      /** Tipo de servicio que presta.
       */
      !!@ ili2db.dispName = "Tipo"
      Tipo : COL_RedServiciosTipo;
    END COL_EspacioJuridicoRedServicios;

    ASSOCIATION col_ueUeGrupo =
      parte -- {0..*} COL_UnidadEspacial;
      todo -- {0..*} COL_AgrupacionUnidadesEspaciales;
    END col_ueUeGrupo;

    /** Traducción de la clase LA_Level de LADM.
     */
    CLASS COL_Nivel (ABSTRACT)
    EXTENDS ObjetoVersionado =
      !!@ ili2db.dispName = "Nombre"
      Nombre : CharacterString;
      !!@ ili2db.dispName = "Tipo de registro"
      Registro_Tipo : COL_RegistroTipo;
      !!@ ili2db.dispName = "Estructura"
      Estructura : COL_EstructuraTipo;
      !!@ ili2db.dispName = "Tipo"
      Tipo : COL_ContenidoNivelTipo;
    END COL_Nivel;

    /** Traducción al español de la clase LA_RequiredRelationshipSpatialUnit de LADM.
     */
    CLASS COL_RelacionNecesariaUnidadesEspaciales (ABSTRACT)
    EXTENDS ObjetoVersionado =
      !!@ ili2db.dispName = "Relación"
      Relacion : MANDATORY COL_ISO19125_Tipo;
    END COL_RelacionNecesariaUnidadesEspaciales;

    ASSOCIATION col_ueNivel =
      ue -- {0..*} COL_UnidadEspacial;
      nivel -- {0..1} COL_Nivel;
    END col_ueNivel;

    /** Clase abstracta que agrupa los atributos comunes de las clases para los derechos (rights), las responsabilidades (responsabilities) y las restricciones (restrictions).
     */
    CLASS COL_DRR (ABSTRACT)
    EXTENDS ObjetoVersionado =
      /** Descripción asociada al derecho, la responsabilidad o la restricción.
       */
      !!@ ili2db.dispName = "Descripción"
      Descripcion : CharacterString;
    END COL_DRR;

    /** De forma genérica, representa el objeto territorial legal (Catastro 2014) que se gestiona en el modelo, en este caso, la parcela catastral o predio. Es independiente del conocimiento de su realidad espacial y se centra en su existencia conocida y reconocida.
     */
    CLASS COL_UnidadAdministrativaBasica (ABSTRACT)
    EXTENDS ObjetoVersionado =
      /** Nombre que recibe la unidad administrativa básica, en muchos casos toponímico, especialmente en terrenos rústicos.
       */
      !!@ ili2db.dispName = "Nombre"
      Nombre : CharacterString;
      /** Tipo de derecho que la reconoce.
       */
      !!@ ili2db.dispName = "Tipo"
      Tipo : MANDATORY COL_UnidadAdministrativaBasicaTipo;
    END COL_UnidadAdministrativaBasica;

    ASSOCIATION col_rrrFuente =
      fuente_administrativa -- {1..*} COL_FuenteAdministrativa;
      rrr -- {0..*} COL_DRR;
    END col_rrrFuente;

    /** Traducción de la clase LA_RequiredRelationshipBAUnit de LADM.
     */
    CLASS COL_RelacionNecesariaBAUnits (ABSTRACT)
    EXTENDS ObjetoVersionado =
      !!@ ili2db.dispName = "Relación"
      Relacion : MANDATORY CharacterString;
    END COL_RelacionNecesariaBAUnits;

    ASSOCIATION col_baunitRrr =
      unidad -- {1} COL_UnidadAdministrativaBasica;
      rrr -- {1..*} COL_DRR;
    END col_baunitRrr;

    ASSOCIATION col_ueBaunit =
      ue (EXTERNAL) -- {0..*} COL_UnidadEspacial;
      baunit -- {0..*} COL_UnidadAdministrativaBasica;
    END col_ueBaunit;

    ASSOCIATION col_relacionFuente =
      fuente_administrativa -- {0..*} COL_FuenteAdministrativa;
      relacionrequeridaBaunit -- {0..*} COL_RelacionNecesariaBAUnits;
    END col_relacionFuente;

    ASSOCIATION col_unidadFuente =
      fuente_administrativa -- {0..*} COL_FuenteAdministrativa;
      unidad -- {0..*} COL_UnidadAdministrativaBasica;
    END col_unidadFuente;

    /** Clase especializada para la administración de los tipos de puntos.
     */
    CLASS COL_Punto (ABSTRACT)
    EXTENDS ObjetoVersionado =
      /** Posición de interpolación.
       */
      !!@ ili2db.dispName = "Posición interpolación"
      Posicion_Interpolacion : COL_InterpolacionTipo;
      /** Clasificación del tipo de punto identificado en el levantamiento catastral.
       */
      !!@ ili2db.dispName = "Tipo de punto"
      PuntoTipo : MANDATORY COL_PuntoTipo;
      /** Indica si el método de levantamiento catastral: método directo o indirecto.
       */
      !!@ ili2db.dispName = "Método de producción"
      MetodoProduccion : MANDATORY COL_MetodoProduccionTipo;
      /** Transformación y Resultado.
       */
      !!@ ili2db.dispName = "Transformación y resultado"
      Transformacion_Y_Resultado : LIST {0..*} OF LADM_COL_V3_0.LADM_Nucleo.COL_Transformacion;
      /** Geometria punto para administración de los objetos: punto de lindero, punto levantamiento y punto de control.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : MANDATORY ISO19107_PLANAS_V3_0.GM_Point3D;
    END COL_Punto;

    /** Especialización de la clase COL_Fuente para almacenar las fuentes constituidas por datos espaciales (entidades geográficas, imágenes de satélite, vuelos fotogramétricos, listados de coordenadas, mapas, planos antiguos o modernos, descripción de localizaciones, etc.) que documentan técnicamente la relación entre instancias de interesados y de predios
     */
    CLASS COL_FuenteEspacial (ABSTRACT)
    EXTENDS COL_Fuente =
      /** Nombre de la fuente espacial del levantamiento catastral de un predio.
       */
      !!@ ili2db.dispName = "Nombre"
      Nombre : MANDATORY TEXT*255;
      /** Tipo de fuente espacial.
       */
      !!@ ili2db.dispName = "Tipo"
      Tipo : MANDATORY COL_FuenteEspacialTipo;
      /** Descripción de la fuente espacial.
       */
      !!@ ili2db.dispName = "Descripción"
      Descripcion : MANDATORY MTEXT;
      /** Metadato de la fuente espacial.
       */
      !!@ ili2db.dispName = "Metadato"
      Metadato : MTEXT;
    END COL_FuenteEspacial;

    /** Traducción al español de la clase LA_BoundaryFaceString de LADM. Define los linderos y a su vez puede estar definida por una descrición textual o por dos o más puntos. Puede estar asociada a una fuente espacial o más.
     */
    CLASS COL_CadenaCarasLimite (ABSTRACT)
    EXTENDS ObjetoVersionado =
      /** Geometría lineal que define el lindero. Puede estar asociada a geometrías de tipo punto que definen sus vértices o ser una entidad lineal independiente.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_Curve3D;
      /** Descripción de la localización, cuando esta se basa en texto.
       */
      !!@ ili2db.dispName = "Localización textual"
      Localizacion_Textual : CharacterString;
    END COL_CadenaCarasLimite;

    /** Traducción de la clase LA_BoundaryFace de LADM. De forma similar a LA_CadenaCarasLindero, representa los límites, pero en este caso permite representación 3D.
     */
    CLASS COL_CarasLindero (ABSTRACT)
    EXTENDS ObjetoVersionado =
      /** Geometría en 3D del límite o lindero, asociada a putos o a descripciones textuales.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface3D;
      /** Cuando la localización del límte está dada por una descripción textual, aquí se recoge esta.
       */
      !!@ ili2db.dispName = "Localización textual"
      Localizacion_Textual : CharacterString;
    END COL_CarasLindero;

    ASSOCIATION col_puntoReferencia =
      ue (EXTERNAL) -- {0..1} COL_UnidadEspacial;
      punto -- {0..1} COL_Punto;
    END col_puntoReferencia;

    ASSOCIATION col_puntoFuente =
      fuente_espacial -- {0..*} COL_FuenteEspacial;
      punto -- {0..*} COL_Punto;
    END col_puntoFuente;

    ASSOCIATION col_ueFuente =
      ue (EXTERNAL) -- {0..*} COL_UnidadEspacial;
      fuente_espacial -- {0..*} COL_FuenteEspacial;
    END col_ueFuente;

    ASSOCIATION col_baunitFuente =
      fuente_espacial -- {0..*} COL_FuenteEspacial;
      unidad (EXTERNAL) -- {0..*} COL_UnidadAdministrativaBasica;
    END col_baunitFuente;

    ASSOCIATION col_relacionFuenteUespacial =
      fuente_espacial -- {0..*} COL_FuenteEspacial;
      relacionrequeridaUe (EXTERNAL) -- {0..*} COL_RelacionNecesariaUnidadesEspaciales;
    END col_relacionFuenteUespacial;

    ASSOCIATION col_cclFuente =
      ccl -- {0..*} COL_CadenaCarasLimite;
      fuente_espacial -- {0..*} COL_FuenteEspacial;
    END col_cclFuente;

    ASSOCIATION col_menosCcl =
      ccl_menos -- {0..*} COL_CadenaCarasLimite;
      ue_menos (EXTERNAL) -- {0..*} COL_UnidadEspacial;
    END col_menosCcl;

    ASSOCIATION col_masCcl =
      ccl_mas -- {0..*} COL_CadenaCarasLimite;
      ue_mas (EXTERNAL) -- {0..*} COL_UnidadEspacial;
    END col_masCcl;

    ASSOCIATION col_puntoCcl =
      punto -- {2..*} COL_Punto;
      ccl -- {0..*} COL_CadenaCarasLimite;
    END col_puntoCcl;

    ASSOCIATION col_clFuente =
      cl -- {0..*} COL_CarasLindero;
      fuente_espacial -- {0..*} COL_FuenteEspacial;
    END col_clFuente;

    ASSOCIATION col_menosCl =
      cl_menos -- {0..*} COL_CarasLindero;
      ue_menos (EXTERNAL) -- {0..*} COL_UnidadEspacial;
    END col_menosCl;

    ASSOCIATION col_masCl =
      cl_mas -- {0..*} COL_CarasLindero;
      ue_mas (EXTERNAL) -- {0..*} COL_UnidadEspacial;
    END col_masCl;

    ASSOCIATION col_puntoCl =
      punto -- {3..*} COL_Punto;
      cl -- {0..*} COL_CarasLindero;
    END col_puntoCl;

    /** Traducción de la clase LA_Party de LADM. Representa a las personas que ejercen derechos y responsabilidades  o sufren restricciones respecto a una BAUnit.
     */
    CLASS COL_Interesado (ABSTRACT)
    EXTENDS ObjetoVersionado =
      /** Identificador del interesado.
       */
      !!@ ili2db.dispName = "Ext PID"
      ext_PID : LADM_COL_V3_0.LADM_Nucleo.ExtInteresado;
      /** Nombre del interesado.
       */
      !!@ ili2db.dispName = "Nombre"
      Nombre : CharacterString;
    END COL_Interesado;

    /** Relaciona los interesados que ostentan la propiedad, posesión u ocupación de un predio. Se registra el grupo en si e independientemete las personas por separado.
     */
    CLASS COL_AgrupacionInteresados (ABSTRACT)
    EXTENDS COL_Interesado =
      /** Indica el tipo de agrupación del que se trata.
       */
      !!@ ili2db.dispName = "Tipo"
      Tipo : MANDATORY COL_GrupoInteresadoTipo;
    END COL_AgrupacionInteresados;

    ASSOCIATION col_baunitComoInteresado =
      interesado -- {0..*} COL_Interesado;
      unidad (EXTERNAL) -- {0..*} COL_UnidadAdministrativaBasica;
    END col_baunitComoInteresado;

    ASSOCIATION col_responsableFuente =
      fuente_administrativa (EXTERNAL) -- {0..*} COL_FuenteAdministrativa;
      interesado -- {0..*} COL_Interesado;
    END col_responsableFuente;

    ASSOCIATION col_rrrInteresado =
      rrr (EXTERNAL) -- {0..*} COL_DRR;
      interesado -- {0..1} COL_Interesado;
    END col_rrrInteresado;

    ASSOCIATION col_topografoFuente =
      fuente_espacial (EXTERNAL) -- {0..*} COL_FuenteEspacial;
      topografo -- {0..*} COL_Interesado;
    END col_topografoFuente;

    ASSOCIATION col_miembros =
      interesado -- {2..*} COL_Interesado;
      agrupacion -<> {0..*} COL_AgrupacionInteresados;
      participacion : LADM_COL_V3_0.LADM_Nucleo.Fraccion;
    END col_miembros;

  END LADM_Nucleo;

END LADM_COL_V3_0.
','2020-08-20 18:07:45.681');
INSERT INTO test_ladm_snr_data.T_ILI2DB_MODEL (filename,iliversion,modelName,content,importDate) VALUES ('ISO19107_PLANAS_V3_0.ili','2.3','ISO19107_PLANAS_V3_0','INTERLIS 2.3;

TYPE MODEL ISO19107_PLANAS_V3_0 (es)
AT "http://www.swisslm.ch/models"
VERSION "2016-03-07"  =

  DOMAIN

    GM_Point2D = COORD 3980000.000 .. 5700000.000 [INTERLIS.m], 1080000.000 .. 3100000.000 [INTERLIS.m] ,ROTATION 2 -> 1;

    GM_Curve2D = POLYLINE WITH (ARCS,STRAIGHTS) VERTEX GM_Point2D WITHOUT OVERLAPS>0.001;

    GM_Surface2D = SURFACE WITH (ARCS,STRAIGHTS) VERTEX GM_Point2D WITHOUT OVERLAPS>0.001;

    GM_Point3D = COORD 3980000.000 .. 5700000.000 [INTERLIS.m], 1080000.000 .. 3100000.000 [INTERLIS.m], -5000.000 .. 6000.000 [INTERLIS.m] ,ROTATION 2 -> 1;

    GM_Curve3D = POLYLINE WITH (ARCS,STRAIGHTS) VERTEX GM_Point3D WITHOUT OVERLAPS>0.001;

    GM_Surface3D = SURFACE WITH (ARCS,STRAIGHTS) VERTEX GM_Point3D WITHOUT OVERLAPS>0.001;

  STRUCTURE GM_Geometry2DListValue =
  END GM_Geometry2DListValue;

  STRUCTURE GM_Curve2DListValue =
    value : MANDATORY GM_Curve2D;
  END GM_Curve2DListValue;

  STRUCTURE GM_Surface2DListValue =
    value : MANDATORY GM_Surface2D;
  END GM_Surface2DListValue;

  !!@ ili2db.mapping = "MultiLine"
STRUCTURE GM_MultiCurve2D =
    geometry : LIST {1..*} OF ISO19107_PLANAS_V3_0.GM_Curve2DListValue;
  END GM_MultiCurve2D;

  !!@ ili2db.mapping = "MultiSurface"
STRUCTURE GM_MultiSurface2D =
    geometry : LIST {1..*} OF ISO19107_PLANAS_V3_0.GM_Surface2DListValue;
  END GM_MultiSurface2D;

  STRUCTURE GM_Curve3DListValue =
    value : MANDATORY GM_Curve3D;
  END GM_Curve3DListValue;

  STRUCTURE GM_Surface3DListValue =
    value : MANDATORY GM_Surface3D;
  END GM_Surface3DListValue;

  !!@ ili2db.mapping = "MultiLine"
STRUCTURE GM_MultiCurve3D =
    geometry : LIST {1..*} OF ISO19107_PLANAS_V3_0.GM_Curve3DListValue;
  END GM_MultiCurve3D;

  !!@ ili2db.mapping = "MultiSurface"
STRUCTURE GM_MultiSurface3D =
    geometry : LIST {1..*} OF ISO19107_PLANAS_V3_0.GM_Surface3DListValue;
  END GM_MultiSurface3D;

END ISO19107_PLANAS_V3_0.
','2020-08-20 18:07:45.681');
INSERT INTO test_ladm_snr_data.T_ILI2DB_MODEL (filename,iliversion,modelName,content,importDate) VALUES ('Submodelo_Insumos_V1_0.ili','2.3','Submodelo_Insumos_Gestor_Catastral_V1_0{ LADM_COL_V3_0 ISO19107_PLANAS_V3_0} Submodelo_Insumos_SNR_V1_0{ LADM_COL_V3_0} Submodelo_Integracion_Insumos_V1_0{ Submodelo_Insumos_Gestor_Catastral_V1_0 Submodelo_Insumos_SNR_V1_0}','INTERLIS 2.3;

MODEL Submodelo_Insumos_Gestor_Catastral_V1_0 (es)
AT "mailto:PC4@localhost"
VERSION "2019-08-01"  =
  IMPORTS ISO19107_PLANAS_V3_0,LADM_COL_V3_0;

  DOMAIN

    GC_CondicionPredioTipo = (
      /** Predio no sometido al régimen de propiedad horizontal.
       */
      !!@ ili2db.dispName = "No propiedad horizontal"
      NPH,
      /** Predio sometido al régimen de propiedad horizontal mediante escritura pública registrada
       */
      !!@ ili2db.dispName = "Propiedad horizontal"
      PH(
        /** Predio matriz del régimen de propiedad horizontal sobre el cual se segregan todas las unidades prediales.
         */
        !!@ ili2db.dispName = "(PH) Matriz"
        Matriz,
        /** Apartamento, garaje, depósito o cualquier otro tipo de unidad predial dentro del PH que se encuentra debidamente inscrito en el registro de instrumentos públicos
         */
        !!@ ili2db.dispName = "(PH) Unidad predial"
        Unidad_Predial
      ),
      /** Predio sometido al régimen de propiedad horizontal mediante escritura pública registrada en cuyo reglamento define para cada unidad predial un área privada de terreno.
       */
      !!@ ili2db.dispName = "Condiminio"
      Condominio(
        /** Predio matriz del condominio sobre el cual se segregan todas las unidades prediales.
         */
        !!@ ili2db.dispName = "(Condominio) Matriz"
        Matriz,
        /** Unidad predial dentro del condominio matriz.
         */
        !!@ ili2db.dispName = "(Condominio) Unidad predial"
        Unidad_Predial
      ),
      /** Es la construcción o edificación instalada por una persona natural o jurídica sobre un predio que no le pertenece.
       */
      !!@ ili2db.dispName = "Mejora"
      Mejora(
        /** Mejora sobre un predio sometido a régimen de propiedad horizontal
         */
        !!@ ili2db.dispName = "(Mejora) Propiedad horizontal"
        PH,
        /** Mejora sobre un predio no sometido a régimen de propiedad horizontal.
         */
        !!@ ili2db.dispName = "(Mejora) No propiedad horizontal"
        NPH
      ),
      /** Predios sobre los cuales las áreas de terreno y construcciones son dedicadas a la cremación, inhumación o enterramiento de personas fallecidas.
       */
      !!@ ili2db.dispName = "Parque cementerio"
      Parque_Cementerio(
        /** Predios sobre los cuales las áreas de terreno y construcciones son dedicadas a la cremación, inhumación o enterramiento de personas fallecidas.
         */
        !!@ ili2db.dispName = "(Parque cementerio) Matriz"
        Matriz,
        /** Área o sección de terreno con función de tumba, esta debe encontrarse inscrita en el registro de instrumentos públicos.
         */
        !!@ ili2db.dispName = "(Parque cementerio) Unidad predial"
        Unidad_Predial
      ),
      /** Espacio (terreno y construcción) diseñado y destinado para el tránsito de vehículos, personas, entre otros.
       */
      !!@ ili2db.dispName = "Vía"
      Via,
      /** Inmuebles que siendo de dominio de la Nación, o una entidad territorial o de particulares, están destinados al uso de los habitantes.
       */
      !!@ ili2db.dispName = "Bien de uso público"
      Bien_Uso_Publico
    );

    GC_SistemaProcedenciaDatosTipo = (
      /** Datos extraídos del Sistema Nacional Catastral del IGAC.
       */
      !!@ ili2db.dispName = "Sistema Nacional Catastral"
      SNC,
      /** Datos extraídos del Sistema COBOL del IGAC.
       */
      !!@ ili2db.dispName = "Cobol"
      Cobol
    );

    GC_UnidadConstruccionTipo = (
      /** Se refiere aquellas construcciones de uso residencial, comercial e industrial.
       */
      !!@ ili2db.dispName = "Convencional"
      Convencional,
      /** Se refiere aquellas construcciones considereadas anexos de construcción.
       */
      !!@ ili2db.dispName = "No convencional"
      No_Convencional
    );

  TOPIC Datos_Gestor_Catastral =

    /** Dato geografico aportado por el Gestor Catastral respecto de los barrios de una entidad territorial.
     */
    !!@ ili2db.dispName = "(GC) Barrio"
    CLASS GC_Barrio =
      /** Código de identificación del barrio.
       */
      !!@ ili2db.dispName = "Código"
      Codigo : TEXT*13;
      /** Nombre del barrio.
       */
      !!@ ili2db.dispName = "Nombre"
      Nombre : TEXT*100;
      /** Código del sector donde se encuentra localizado el barrio.
       */
      !!@ ili2db.dispName = "Código sector"
      Codigo_Sector : TEXT*9;
      /** Tipo de geometría y su representación georrefenciada que definen los límites y el área ocupada por el barrio.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface2D;
    END GC_Barrio;

    /** Relaciona la calificación de las unidades de construcción de los datos de insumos del Gestor Catastral.
     */
    !!@ ili2db.dispName = "(GC) Calificación unidad de construcción"
    CLASS GC_CalificacionUnidadConstruccion =
      /** Indica el componente de la calificación de la unidad de construcción.
       */
      !!@ ili2db.dispName = "Componente"
      Componente : TEXT*255;
      /** Indica el elemento de calificación de la unidad de construcción.
       */
      !!@ ili2db.dispName = "Elemento de calificación"
      Elemento_Calificacion : TEXT*255;
      /** Indica el detalle de calificación del elemento de calificación de la unidad de construcción.
       */
      !!@ ili2db.dispName = "Detalle de calificación"
      Detalle_Calificacion : TEXT*255;
      /** Puntaje asociado al detalle del elemento de calificación.
       */
      !!@ ili2db.dispName = "Puntos"
      Puntos : 0 .. 100;
    END GC_CalificacionUnidadConstruccion;

    /** Construcciones que no cuentan con información alfanumérica en la base de datos catastral.
     */
    !!@ ili2db.dispName = "(GC) Comisiones Construcción"
    CLASS GC_ComisionesConstruccion =
      /** Numero Predial del Construcciones que no cuentan con información alfanumérica en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Número predial"
      Numero_Predial : MANDATORY TEXT*30;
      /** Construcciones que no cuentan con información alfanumérica en la base catastral.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface3D;
    END GC_ComisionesConstruccion;

    /** Terrenos que no cuentan con información alfanumérica en la base de datos catastral.
     */
    !!@ ili2db.dispName = "(GC) Comisiones Terreno"
    CLASS GC_ComisionesTerreno =
      /** Numero Predial del terreno que no cuentan con información
       * alfanumérica en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Número predial"
      Numero_Predial : MANDATORY TEXT*30;
      /** Terrenos que no cuentan con información alfanumérica en la base catastral.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface2D;
    END GC_ComisionesTerreno;

    /** Unidades de construcción que no cuentan con información alfanumérica en la base de datos catastral.
     */
    !!@ ili2db.dispName = "(GC) Comisiones Unidad Construcción"
    CLASS GC_ComisionesUnidadConstruccion =
      /** Numero Predial del terreno que no cuentan con información alfanumérica en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Número predial"
      Numero_Predial : MANDATORY TEXT*30;
      /** Unidades de construcción que no cuentan con información alfanumérica en la base catastral.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface3D;
    END GC_ComisionesUnidadConstruccion;

    /** Datos de las construcciones inscritas en las bases de datos catastrales en una entidad territorial.
     */
    !!@ ili2db.dispName = "(GC) Construcción"
    CLASS GC_Construccion =
      /** Identificado de la unidad de construcción, su codificación puede ser por letras del abecedario.
       */
      !!@ ili2db.dispName = "Identificador"
      Identificador : TEXT*30;
      /** Etiqueta de la construcción.
       */
      !!@ ili2db.dispName = "Etiqueta"
      Etiqueta : TEXT*50;
      /** Indica si la construcción es de tipo convencional o no convencional.
       */
      !!@ ili2db.dispName = "Tipo de construcción"
      Tipo_Construccion : Submodelo_Insumos_Gestor_Catastral_V1_0.GC_UnidadConstruccionTipo;
      /** Indica el tipo de dominio de la unidad de construcción: común y privado.
       */
      !!@ ili2db.dispName = "Tipo de dominio"
      Tipo_Dominio : TEXT*20;
      /** Número total de pisos de la construcción.
       */
      !!@ ili2db.dispName = "Número de pisos"
      Numero_Pisos : 0 .. 200;
      /** Número total de sótanos de la construcción.
       */
      !!@ ili2db.dispName = "Número de sótanos"
      Numero_Sotanos : 0 .. 99;
      /** Número total de mezanines de la construcción.
       */
      !!@ ili2db.dispName = "Número de mezanines"
      Numero_Mezanines : 0 .. 99;
      /** Número total de semisótanos de la construcción.
       */
      !!@ ili2db.dispName = "Número de semisótanos"
      Numero_Semisotanos : 0 .. 99;
      /** Código catastral de la construcción.
       */
      !!@ ili2db.dispName = "Código de edificación"
      Codigo_Edificacion : 0 .. 10000000000000000000;
      /** Código de terreno donde se encuentra ubicada la construcción.
       */
      !!@ ili2db.dispName = "Código de terreno"
      Codigo_Terreno : TEXT*30;
      /** Área total construida.
       */
      !!@ ili2db.dispName = "Área construida"
      Area_Construida : 0.00 .. 99999999999999.98 [LADM_COL_V3_0.m2];
      /** Polígono de la construcción existente en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface3D;
    END GC_Construccion;

    /** Clase que contiene los datos principales del predio matriz sometido al regimen de propiedad horizontal inscrito en las bases de datos catastrales.
     */
    !!@ ili2db.dispName = "(GC) Datos Propiedad Horizontal Condominio"
    CLASS GC_DatosPHCondominio =
      /** Área total privada del terreno del PH o Condominio Matriz.
       */
      !!@ ili2db.dispName = "Área total de terreno privada"
      Area_Total_Terreno_Privada : 0.00 .. 99999999999999.98 [LADM_COL_V3_0.m2];
      /** Área total de terreno común del PH o Condominio Matriz.
       */
      !!@ ili2db.dispName = "Área total de terreno común"
      Area_Total_Terreno_Comun : 0.00 .. 99999999999999.98 [LADM_COL_V3_0.m2];
      /** Área total construida privada del PH o Condominio Matriz.
       */
      !!@ ili2db.dispName = "Área total construida privada"
      Area_Total_Construida_Privada : 0.00 .. 99999999999999.98 [LADM_COL_V3_0.m2];
      /** Área total construida común del PH o Condominio Matriz.
       */
      !!@ ili2db.dispName = "Área total construida común"
      Area_Total_Construida_Comun : 0.00 .. 99999999999999.98 [LADM_COL_V3_0.m2];
      /** Total de unidades privadas en el PH o Condominio.
       */
      !!@ ili2db.dispName = "Total de unidades privadas"
      Total_Unidades_Privadas : 0 .. 99999999;
      /** Total de unidades prediales en el sótano del PH o Condominio.
       */
      !!@ ili2db.dispName = "Total de unidades de sótano"
      Total_Unidades_Sotano : 0 .. 99999999;
      /** Avalúo catastral total de la propiedad horizontal o condominio.
       */
      !!@ ili2db.dispName = "Valor total avaúo catastral"
      Valor_Total_Avaluo_Catastral : LADM_COL_V3_0.LADM_Nucleo.Peso;
    END GC_DatosPHCondominio;

    /** Relaciona la información de las torres asociadas al PH o Condominio de los datos insumos del Gestor Catastral
     */
    !!@ ili2db.dispName = "(GC) Datos torre PH"
    CLASS GC_DatosTorrePH =
      /** Número de torre en el PH o Condominio.
       */
      !!@ ili2db.dispName = "Torre"
      Torre : 0 .. 1500;
      /** Total de pisos de la torre.
       */
      !!@ ili2db.dispName = "Total de pisos torre"
      Total_Pisos_Torre : 0 .. 100;
      /** Total de unidades privadas en la torre.
       */
      !!@ ili2db.dispName = "Total de unidades privadas"
      Total_Unidades_Privadas : 0 .. 99999999;
      /** Total de sótanos en la torre.
       */
      !!@ ili2db.dispName = "Total de sótanos"
      Total_Sotanos : 0 .. 99;
      /** Total de unidades prediales en el sótano de la torre.
       */
      !!@ ili2db.dispName = "Total de unidades sótano"
      Total_Unidades_Sotano : 0 .. 99999999;
    END GC_DatosTorrePH;

    !!@ ili2db.dispName = "(GC) Dirección"
    STRUCTURE GC_Direccion =
      /** Registros de la direcciones del predio.
       */
      !!@ ili2db.dispName = "Valor"
      Valor : TEXT*255;
      /** Indica si el registro de la dirección corresponde a la principal.
       */
      !!@ ili2db.dispName = "Principal"
      Principal : BOOLEAN;
      /** Línea de donde se encuentra la placa de nomenclatura del predio.
       */
      !!@ ili2db.dispName = "Geometría de referencia"
      Geometria_Referencia : ISO19107_PLANAS_V3_0.GM_Curve3D;
    END GC_Direccion;

    /** Estructura que contiene el estado del predio en la base de datos catastral.
     */
    !!@ ili2db.dispName = "(GC) EstadoPredio"
    STRUCTURE GC_EstadoPredio =
      /** Indica el estado del predio en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Estado alerta"
      Estado_Alerta : TEXT*30;
      /** Entidad emisora del estado de alerta del predio.
       */
      !!@ ili2db.dispName = "Entidad emisora de la alerta"
      Entidad_Emisora_Alerta : TEXT*255;
      /** Fecha de la alerta en el sistema de gestión catastral.
       */
      !!@ ili2db.dispName = "Fecha de alerta"
      Fecha_Alerta : INTERLIS.XMLDate;
    END GC_EstadoPredio;

    /** Dato geografico aportado por el Gestor Catastral respecto de las manzanas de una entidad territorial.
     */
    !!@ ili2db.dispName = "(GC) Manzana"
    CLASS GC_Manzana =
      /** Código catastral de 17 dígitos de la manzana.
       */
      !!@ ili2db.dispName = "Código"
      Codigo : TEXT*17;
      /** Código catastral anterior de la manzana.
       */
      !!@ ili2db.dispName = "Código anterior"
      Codigo_Anterior : TEXT*255;
      /** Código catastral de 13 dígitos del barrio donde se encuentra la manzana.
       */
      !!@ ili2db.dispName = "Código de barrio"
      Codigo_Barrio : TEXT*13;
      /** Polígonos de la manzanas catastrales.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface2D;
    END GC_Manzana;

    /** Dato geografico aportado por el Gestor Catastral respecto del perimetro urbano de una entidad territorial.
     */
    !!@ ili2db.dispName = "(GC) Perímetro"
    CLASS GC_Perimetro =
      /** Código de 2 dígitos del Departamento según clasificación de Divipola.
       */
      !!@ ili2db.dispName = "Código del departamento"
      Codigo_Departamento : TEXT*2;
      /** Código de 5 dígitos que une los 2 dígitos del Departamento y los 3 dígitos del municipio según la clasificación de Divipola.
       */
      !!@ ili2db.dispName = "Código del municipio"
      Codigo_Municipio : TEXT*5;
      /** Tipo de avalúo catastral del perímetro urbano.
       */
      !!@ ili2db.dispName = "Tipo de avalúo"
      Tipo_Avaluo : TEXT*30;
      /** Nombre geográfico del perímetro municipal, por ejemplo el nombre del municipio.
       */
      !!@ ili2db.dispName = "Nombre geográfico"
      Nombre_Geografico : TEXT*50;
      /** Código del nombre geográfico.
       */
      !!@ ili2db.dispName = "Código nombre"
      Codigo_Nombre : TEXT*255;
      /** Polígono del perímetro urbano.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface2D;
    END GC_Perimetro;

    /** Datos de los propietarios inscritos en las bases de datos catastrales que tienen relación con un predio.
     */
    !!@ ili2db.dispName = "(GC) Propietario"
    CLASS GC_Propietario =
      /** Tipo de documento del propietario registrado en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Tipo de documento"
      Tipo_Documento : TEXT*100;
      /** Número de documento del propietario registrado en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Número de documento"
      Numero_Documento : TEXT*50;
      /** Dígito de verificación de las personas jurídicas.
       */
      !!@ ili2db.dispName = "Dígito de verificación"
      Digito_Verificacion : TEXT*1;
      /** Primer nombre del propietario en catastro.
       */
      !!@ ili2db.dispName = "Primer nombre"
      Primer_Nombre : TEXT*255;
      /** Segundo nombre del propietario en catastro.
       */
      !!@ ili2db.dispName = "Segundo nombre"
      Segundo_Nombre : TEXT*255;
      /** Primer apellido del propietario en catastro.
       */
      !!@ ili2db.dispName = "Primer apellido"
      Primer_Apellido : TEXT*255;
      /** Segundo apellido del propietario en catastro.
       */
      !!@ ili2db.dispName = "Segundo apellido"
      Segundo_Apellido : TEXT*255;
      /** Razon social de las personas jurídicas inscritas como propietarios en catastro.
       */
      !!@ ili2db.dispName = "Razón social"
      Razon_Social : TEXT*255;
    END GC_Propietario;

    /** Dato geografico aportado por el Gestor Catastral respecto de los sectores catastrales rurales de una entidad territorial.
     */
    !!@ ili2db.dispName = "(GC) Sector Rural"
    CLASS GC_SectorRural =
      /** Código catastral de 9 dígitos del sector catastral.
       */
      !!@ ili2db.dispName = "Código"
      Codigo : TEXT*9;
      /** Polígono de los sectores catastrales existentes en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface2D;
    END GC_SectorRural;

    /** Dato geografico aportado por el Gestor Catastral respecto de los sectores catastrales urbanos de una entidad territorial.
     */
    !!@ ili2db.dispName = "(GC) Sector Urbano"
    CLASS GC_SectorUrbano =
      /** Código catastral de 9 dígitos del sector catastral.
       */
      !!@ ili2db.dispName = "Código"
      Codigo : TEXT*9;
      /** Polígono de los sectores catastrales existentes en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface2D;
    END GC_SectorUrbano;

    /** Datos de los terrenos inscritos en las bases de datos catastrales en una entidad territorial.
     */
    !!@ ili2db.dispName = "(GC) Terreno"
    CLASS GC_Terreno =
      /** Área de terreno alfanumérica registrada en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Área terreno alfanumérica"
      Area_Terreno_Alfanumerica : 0.00 .. 99999999999999.98 [LADM_COL_V3_0.m2];
      /** Área de terreno digital registrada en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Área terreno digital"
      Area_Terreno_Digital : 0.00 .. 99999999999999.98 [LADM_COL_V3_0.m2];
      /** Código de la manzana o vereda donde se localiza el terreno.
       */
      !!@ ili2db.dispName = "Código de manzana vereda"
      Manzana_Vereda_Codigo : TEXT*17;
      /** Número de subterráneos en el terreno.
       */
      !!@ ili2db.dispName = "Número de subterráneos"
      Numero_Subterraneos : 0 .. 999999999999999;
      /** Polígono de la unidad de construcción existente en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface2D;
    END GC_Terreno;

    /** Datos de las unidades de construcción inscritas en las bases de datos catastrales en una entidad territorial.
     */
    !!@ ili2db.dispName = "(GC) Unidad Construcción"
    CLASS GC_UnidadConstruccion =
      /** Identificado de la unidad de construcción, su codificación puede ser por letras del abecedario.
       */
      !!@ ili2db.dispName = "Identificador"
      Identificador : TEXT*2;
      /** Etiqueta de la unidad de construcción.
       */
      !!@ ili2db.dispName = "Etiqueta"
      Etiqueta : TEXT*50;
      /** Indica el tipo de dominio de la unidad de construcción: común y privado.
       */
      !!@ ili2db.dispName = "Tipo de dominio"
      Tipo_Dominio : TEXT*20;
      /** Indica si la construcción es de tipo convencional o no convencional.
       */
      !!@ ili2db.dispName = "Tipo de construcción"
      Tipo_Construccion : Submodelo_Insumos_Gestor_Catastral_V1_0.GC_UnidadConstruccionTipo;
      /** Indica numéricamente la ubicación del predio de acuerdo al tipo de planta.
       */
      !!@ ili2db.dispName = "Planta"
      Planta : TEXT*10;
      /** Número total de  habitaciones en la unidad de construcción.
       */
      !!@ ili2db.dispName = "Total de habitaciones"
      Total_Habitaciones : 0 .. 999999;
      /** Número total de baños en la unidad de construcción.
       */
      !!@ ili2db.dispName = "Total de baños"
      Total_Banios : 0 .. 999999;
      /** Número total de locales en la unidad de construcción.
       */
      !!@ ili2db.dispName = "Total de locales"
      Total_Locales : 0 .. 999999;
      /** Número total de pisos en la unidad de construcción.
       */
      !!@ ili2db.dispName = "Total de pisos"
      Total_Pisos : 0 .. 150;
      /** Actividad que se desarrolla en una unidad de construcción.
       */
      !!@ ili2db.dispName = "Uso"
      Uso : TEXT*255;
      /** Año de construcción de la unidad de construcción.
       */
      !!@ ili2db.dispName = "Año de construcción"
      Anio_Construccion : 1512 .. 2500;
      /** Puntaje total de la calificación de construcción.
       */
      !!@ ili2db.dispName = "Puntaje"
      Puntaje : 0 .. 200;
      /** Área total construida en la unidad de construcción.
       */
      !!@ ili2db.dispName = "Área construida"
      Area_Construida : 0.00 .. 99999999999999.98 [LADM_COL_V3_0.m2];
      /** Área total privada de la unidad de construcción para los predios en régimen de propiedad horizontal.
       */
      !!@ ili2db.dispName = "Área privada"
      Area_Privada : 0.00 .. 99999999999999.98 [LADM_COL_V3_0.m2];
      /** Código catastral del terreno donde se encuentra localizada la unidad de construcción.
       */
      !!@ ili2db.dispName = "Código terreno"
      Codigo_Terreno : TEXT*30;
      /** Polígono de la unidad de construcción existente en la base de datos catastral.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface3D;
    END GC_UnidadConstruccion;

    /** Dato geografico aportado por el Gestor Catastral respecto de las veredades de una entidad territorial.
     */
    !!@ ili2db.dispName = "(GC) Vereda"
    CLASS GC_Vereda =
      /** Código catastral de 17 dígitos de la vereda.
       */
      !!@ ili2db.dispName = "Código"
      Codigo : TEXT*17;
      /** Código catastral de 13 dígitos de la vereda.
       */
      !!@ ili2db.dispName = "Código anterior"
      Codigo_Anterior : TEXT*13;
      /** Nombre de la vereda.
       */
      !!@ ili2db.dispName = "Nombre"
      Nombre : TEXT*100;
      /** Código catastral de 9 dígitos del código de sector donde se encuentra la vereda.
       */
      !!@ ili2db.dispName = "Código del sector"
      Codigo_Sector : TEXT*9;
      /** Geometría en 2D de la vereda.
       */
      !!@ ili2db.dispName = "Geometría"
      Geometria : ISO19107_PLANAS_V3_0.GM_MultiSurface2D;
    END GC_Vereda;

    /** Información existente en las bases de datos catastrales respecto de los predios en una entidad territorial.
     */
    !!@ ili2db.dispName = "(GC) Predio Catastro"
    CLASS GC_PredioCatastro =
      /** Indica si el predio se encuentra en catastro fiscal o Ley 14.
       */
      !!@ ili2db.dispName = "Tipo de catastro"
      Tipo_Catastro : TEXT*255;
      /** Código numérico de 30 dígitos que permita localizarlo inequívocamente en los respectivos documentos catastrales, según el modelo determinado por el Instituto Geográfico Agustín Codazzi.
       */
      !!@ ili2db.dispName = "Número predial"
      Numero_Predial : TEXT*30;
      /** Código numérico de 20 dígitos que permita localizarlo inequívocamente en los respectivos documentos catastrales, según el modelo determinado por el Instituto Geográfico Agustín Codazzi.
       */
      !!@ ili2db.dispName = "Número predial anterior"
      Numero_Predial_Anterior : TEXT*20;
      /** Es un código único para identificar los inmuebles tanto en los sistemas de información catastral como registral. El NUPRE no implicará supresión de la numeración catastral ni registral asociada a la cédula catastral ni a la matrícula inmobiliaria actual.
       */
      !!@ ili2db.dispName = "Número único predial"
      NUPRE : TEXT*11;
      /** Circulo registral al que se encuentra inscrito el predio.
       */
      !!@ ili2db.dispName = "Círculo registral"
      Circulo_Registral : TEXT*4;
      /** Identificador único asignado por las oficinas de registro de instrumentos públicos.
       */
      !!@ ili2db.dispName = "Matrícula inmobiliaria catastro"
      Matricula_Inmobiliaria_Catastro : TEXT*80;
      /** Direcciones del predio inscritas en catastro.
       */
      !!@ ili2db.dispName = "Direcciones"
      Direcciones : BAG {0..*} OF Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion;
      /** Tipo de predio inscrito en catastro: Nacional, Departamental, Municipal, Particular, Baldío, Ejido, Resguardo Indígena, Tierra de comunidades negras y Reservas Naturales.
       */
      !!@ ili2db.dispName = "Tipo de predio"
      Tipo_Predio : TEXT*100;
      /** Caracterización temática del predio.
       */
      !!@ ili2db.dispName = "Condición del predio"
      Condicion_Predio : Submodelo_Insumos_Gestor_Catastral_V1_0.GC_CondicionPredioTipo;
      /** Es la clasificación para fines estadísticos que se da a cada inmueble en su conjunto–terreno, construcciones o edificaciones-, en el momento de la identificación predial de conformidad con la actividad predominante que en él se desarrolle.
       */
      !!@ ili2db.dispName = "Destinación económica"
      Destinacion_Economica : TEXT*150;
      /** Estado del predio en la base de datos catastral según los actos administrativos o judiciales que versan sobre el mismo.
       */
      !!@ ili2db.dispName = "Estado del predio"
      Estado_Predio : BAG {0..*} OF Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio;
      /** Indica el sistema de gestión catastral de donde proceden los datos, en el caso del IGAC puede ser COBOL o SNC.
       */
      !!@ ili2db.dispName = "Sistema procedencia de los datos"
      Sistema_Procedencia_Datos : Submodelo_Insumos_Gestor_Catastral_V1_0.GC_SistemaProcedenciaDatosTipo;
      /** Fecha de la vigencia de los datos.
       */
      !!@ ili2db.dispName = "Fecha de los datos"
      Fecha_Datos : MANDATORY INTERLIS.XMLDate;
    END GC_PredioCatastro;

    ASSOCIATION gc_construccion_unidad =
      gc_unidad_construccion -- {0..*} GC_UnidadConstruccion;
      gc_construccion -- {1} GC_Construccion;
    END gc_construccion_unidad;

    ASSOCIATION gc_datosphcondominio_datostorreph =
      gc_datostorreph -- {0..*} GC_DatosTorrePH;
      gc_datosphcondominio -- {0..1} GC_DatosPHCondominio;
    END gc_datosphcondominio_datostorreph;

    ASSOCIATION gc_unidadconstruccion_calificacionunidadconstruccion =
      gc_unidadconstruccion -- {0..1} GC_UnidadConstruccion;
      gc_calificacionunidadconstruccion -- {0..*} GC_CalificacionUnidadConstruccion;
    END gc_unidadconstruccion_calificacionunidadconstruccion;

    ASSOCIATION gc_construccion_predio =
      gc_predio -- {1} GC_PredioCatastro;
      gc_construccion -- {0..*} GC_Construccion;
    END gc_construccion_predio;

    /** Clase que relaciona las unidades prediales a los predios matrices bajo el regimen de propiedad horizontal inscritos en las bases de datos catastrales.
     */
    ASSOCIATION gc_copropiedad =
      gc_matriz -<> {0..1} GC_PredioCatastro;
      gc_unidad -- {0..*} GC_PredioCatastro;
      Coeficiente_Copropiedad : 0.0000000 .. 100.0000000;
    END gc_copropiedad;

    ASSOCIATION gc_ph_predio =
      gc_predio -- {1} GC_PredioCatastro;
      gc_datos_ph -- {0..1} GC_DatosPHCondominio;
    END gc_ph_predio;

    ASSOCIATION gc_propietario_predio =
      gc_predio_catastro -- {1} GC_PredioCatastro;
      gc_propietario -- {0..*} GC_Propietario;
    END gc_propietario_predio;

    ASSOCIATION gc_terreno_predio =
      gc_predio -- {1} GC_PredioCatastro;
      gc_terreno -- {0..*} GC_Terreno;
    END gc_terreno_predio;

  END Datos_Gestor_Catastral;

END Submodelo_Insumos_Gestor_Catastral_V1_0.

MODEL Submodelo_Insumos_SNR_V1_0 (es)
AT "http://www.proadmintierra.info/"
VERSION "V2.3"  // 2019-07-31 // =
  IMPORTS LADM_COL_V3_0;

  DOMAIN

    SNR_CalidadDerechoTipo = (
      /** El dominio que se llama también propiedad es el derecho real en una cosa corporal, para gozar y disponer de ella arbitrariamente, no siendo contra ley o contra derecho ajeno. (Art. 669 CC):
       * 
       * 0100
       * 0101
       * 0102
       * 0103
       * 0106
       * 0107
       * 0108
       * 0109
       * 0110
       * 0111
       * 0112
       * 0113
       * 0114
       * 0115
       * 0116
       * 0117
       * 0118
       * 0119
       * 0120
       * 0121
       * 0122
       * 0124
       * 0125
       * 0126
       * 0127
       * 0128
       * 0129
       * 0130
       * 0131
       * 0132
       * 0133
       * 0135
       * 0137
       * 0138
       * 0139
       * 0140
       * 0141
       * 0142
       * 0143
       * 0144
       * 0145
       * 0146
       * 0147
       * 0148
       * 0150
       * 0151
       * 0152
       * 0153
       * 0154
       * 0155
       * 0156
       * 0157
       * 0158
       * 0159
       * 0160
       * 0161
       * 0163
       * 0164
       * 0165
       * 0166
       * 0167
       * 0168
       * 0169
       * 0171
       * 0172
       * 0173
       * 0175
       * 0177
       * 0178
       * 0179
       * 0180
       * 0181
       * 0182
       * 0183
       * 0184
       * 0185
       * 0186
       * 0187
       * 0188
       * 0189
       * 0190
       * 0191
       * 0192
       * 0193
       * 0194
       * 0195
       * 0196
       * 0197
       * 0198
       * 0199
       * 01003
       * 01004
       * 01005
       * 01006
       * 01007
       * 01008
       * 01009
       * 01010
       * 01012
       * 01013
       * 01014
       * 0301
       * 0307
       * 0321
       * 0332
       * 0348
       * 0356
       * 0374
       * 0375
       * 0376
       * 0377
       * 0906
       * 0907
       * 0910
       * 0911
       * 0912
       * 0913
       * 0915
       * 0917
       * 0918
       * 0919
       * 0920
       * 0924
       * 0935
       * 0959
       * 0962
       * 0963
       */
      !!@ ili2db.dispName = "Dominio"
      Dominio,
      /** Es la inscripción en la Oficina de Registro de Instrumentos Públicos, de todo acto de transferencia de un derecho incompleto que se hace a favor de una persona, por parte de quien carece del derecho de dominio sobre determinado inmueble: 
       * 
       * 0600
       * 0601
       * 0602
       * 0604
       * 0605
       * 0606
       * 0607
       * 0608
       * 0609
       * 0610
       * 0611
       * 0613
       * 0614
       * 0615
       * 0616
       * 0617
       * 0618
       * 0619
       * 0620
       * 0621
       * 0622
       * 0136
       * 0508
       * 0927
       */
      !!@ ili2db.dispName = "Falsa tradición"
      Falsa_Tradicion,
      /** La propiedad separada del goce de la cosa se llama mera o nuda propiedad (art 669 CC):
       * 
       * Códigos:
       * 
       * 0302
       * 0308
       * 0322
       * 0349
       * 0379
       */
      !!@ ili2db.dispName = "Nuda propiedad"
      Nuda_Propiedad,
      /** Es la propiedad de toda una comunidad sea indígena o negra. Adjudicacion Baldios En Propiedad Colectiva A Comunidades Negras, Adjudicacion Baldios Resguardos Indigenas, Constitución Resguardo Indigena,
       * Ampliación De Resguardo Indígena
       * 
       * Códigos:
       * 
       * 0104
       * 0105
       * 01001
       * 01002
       */
      !!@ ili2db.dispName = "Derecho de propiedad colectiva"
      Derecho_Propiedad_Colectiva,
      /** El derecho de usufructo es un derecho real que consiste en la facultad de gozar de una cosa con cargo de conservar su forma y sustancia, y de restituir a su dueño, si la cosa no es fungible; o con cargo de volver igual cantidad y calidad del mismo género, o de pagar su valor si la cosa es fungible. (art. 823 CC):
       * 
       * 0310
       * 0314
       * 0323
       * 0333
       * 0378
       * 0380
       * 0382
       * 0383
       */
      !!@ ili2db.dispName = "Usufructo"
      Usufructo
    );

    SNR_ClasePredioRegistroTipo = (
      /** Constituyen esta categoría los terrenos no aptos para el uso urbano, por razones de oportunidad, o por su destinación a usos agrícolas, ganaderos, forestales, de explotación de recursos naturales y actividades análogas. (Artículo 33, Ley 388 de 1997)
       */
      !!@ ili2db.dispName = "Rural"
      Rural,
      /** Constituyen el suelo urbano, las áreas del territorio distrital o municipal destinadas a usos urbanos por el plan de ordenamiento, que cuenten con infraestructura vial y redes primarias de energía, acueducto y alcantarillado, posibilitándose su urbanización y edificación, según sea el caso. Podrán pertenecer a esta categoría aquellas zonas con procesos de urbanización incompletos, comprendidos en áreas consolidadas con edificación, que se definan como áreas de mejoramiento integral en los planes de ordenamiento territorial.
       * 
       * Las áreas que conforman el suelo urbano serán delimitadas por perímetros y podrán incluir los centros poblados de los corregimientos. En ningún caso el perímetro urbano podrá ser mayor que el denominado perímetro de servicios públicos o sanitario. (Artículo 31, Ley 388 de 1997)
       */
      !!@ ili2db.dispName = "Urbano"
      Urbano,
      !!@ ili2db.dispName = "Sin información"
      Sin_Informacion
    );

    SNR_DocumentoTitularTipo = (
      /** Es un documento emitido por la Registraduría Nacional del Estado Civil para permitir la identificación personal de los ciudadanos.
       */
      !!@ ili2db.dispName = "Cédula de ciudadanía"
      Cedula_Ciudadania,
      /** Es el documento que cumple los fines de identificación de los extranjeros en el territorio nacional y su utilización deberá estar acorde con la visa otorgada al extranjero.
       */
      !!@ ili2db.dispName = "Cédula de extranjería"
      Cedula_Extranjeria,
      /** El Número de Identificación Tributaria (NIT) es un código privado, secreto e intransferible que solamente debe conocer el contribuyente.
       */
      !!@ ili2db.dispName = "NIT"
      NIT,
      /** Es el documento oficial que hace las veces de identificación para los menores de edad entre los 7 y los 18 años.
       */
      !!@ ili2db.dispName = "Tarjeta de identidad"
      Tarjeta_Identidad,
      /** Registro donde se hacen constar por autoridades competentes los nacimientos, matrimonios, defunciones y demás hechos relativos al estado civil de las personas. En el modelo se tendrá en cuenta el número de registro como identificación personal de las personas de 0 a 7 años.
       */
      !!@ ili2db.dispName = "Registro civil"
      Registro_Civil,
      /** El Número Único de Identificación Personal, es el número que permite identificar a los colombianos durante toda su vida.
       */
      !!@ ili2db.dispName = "NUIP"
      NUIP,
      /** Es un consecutivo asignado automáticamente en registro en lugar del número de la identificación de la persona que hace el trámite, se usa especialmente en trámites de construcción cuando el proyecto está a nombre de una Fiducia el cual tiene el mismo número del banco.
       */
      !!@ ili2db.dispName = "Secuencial SNR"
      Secuencial_SNR
    );

    SNR_FuenteTipo = (
      /** Un acto administrativo es toda manifestación o declaración emanada de la administración pública en el ejercicio de potestades administrativas, mediante el que impone su voluntad sobre los derechos, libertades o intereses de otros sujetos públicos o privados y que queda bajo el del comienzo.
       */
      !!@ ili2db.dispName = "Acto administrativo"
      Acto_Administrativo,
      /** Una escritura pública es un documento público en el que se realiza ante un notario público un determinado hecho o un derecho autorizado por dicho fedatario público, que firma con el otorgante u otorgantes,mostrando sobre la capacidad jurídica del contenido y de la fecha en que se realizó
       */
      !!@ ili2db.dispName = "Escritura pública"
      Escritura_Publica,
      /** La sentencia es la resolución judicial definitiva dictada por un juez o tribunal que pone fin a la litis o caso sometido a su conocimiento y cierra definitivamente su actuación en el mismo
       */
      !!@ ili2db.dispName = "Sentencia judicial"
      Sentencia_Judicial,
      /** Documento que contiene un compromiso entre dos o más personas que lo firman.
       */
      !!@ ili2db.dispName = "Documento privado"
      Documento_Privado,
      /** Cuando no se haya documento soporte pero puede ser una declaración verbal.
       */
      !!@ ili2db.dispName = "Sin documento"
      Sin_Documento
    );

    SNR_PersonaTitularTipo = (
      /** Se refiere a la persona humana.
       */
      !!@ ili2db.dispName = "Persona natural"
      Persona_Natural,
      /** Se llama persona jurídica, una persona ficticia, capaz de ejercer derechos y contraer obligaciones civiles, y de ser representada judicial y extrajudicialmente. Las personas jurídicas son de dos especies: corporaciones y fundaciones de beneficencia pública.
       */
      !!@ ili2db.dispName = "Persona jurídica"
      Persona_Juridica
    );

  TOPIC Datos_SNR =

    /** Datos del derecho inscrito en la SNR.
     */
    !!@ ili2db.dispName = "(SNR) Derecho"
    CLASS SNR_Derecho =
      /** Calidad de derecho en registro
       */
      !!@ ili2db.dispName = "Calidad derecho registro"
      Calidad_Derecho_Registro : MANDATORY Submodelo_Insumos_SNR_V1_0.SNR_CalidadDerechoTipo;
      /** es el número asignado en el registro a cada acto sujeto a registro.
       */
      !!@ ili2db.dispName = "Código naturaleza jurídica"
      Codigo_Naturaleza_Juridica : TEXT*5;
    END SNR_Derecho;

    !!@ ili2db.dispName = "(SNR) Estructura Matrícula Matriz"
    STRUCTURE SNR_EstructuraMatriculaMatriz =
      /** Es el nùmero que se ha asignado a la Oficina de Registro de Instrumentos públicos correspondiente.
       */
      !!@ ili2db.dispName = "Código ORIP"
      Codigo_ORIP : TEXT*20;
      /** Es el consecutivo que se asigna a cada predio jurídico abierto en la ORIP.
       */
      !!@ ili2db.dispName = "Matrícula inmobiliaria"
      Matricula_Inmobiliaria : TEXT*20;
    END SNR_EstructuraMatriculaMatriz;

    /** Datos del documento que soporta la descripción de cabida y linderos.
     */
    !!@ ili2db.dispName = "(SNR) Fuente Cabida Linderos"
    CLASS SNR_FuenteCabidaLinderos =
      /** Tipo de documento que soporta la relación de tenencia entre el interesado con el predio.
       */
      !!@ ili2db.dispName = "Tipo de documento"
      Tipo_Documento : Submodelo_Insumos_SNR_V1_0.SNR_FuenteTipo;
      /** Identificador del documento, ejemplo: numero de la resolución
       */
      !!@ ili2db.dispName = "Número de documento"
      Numero_Documento : TEXT*255;
      !!@ ili2db.dispName = "Fecha de documento"
      Fecha_Documento : INTERLIS.XMLDate;
      /** Es tipo de oficina que emite el documento (notaria, juzgado)
       */
      !!@ ili2db.dispName = "Ente emisor"
      Ente_Emisor : TEXT*255;
      /** Es la ciudad donde se encuentra ubicada la oficina que expide el documento.
       */
      !!@ ili2db.dispName = "Ciudad emisora"
      Ciudad_Emisora : TEXT*255;
      /** Identificador del archivo fuente controlado por una clase externa.
       */
      !!@ ili2db.dispName = "Archivo"
      Archivo : LADM_COL_V3_0.LADM_Nucleo.ExtArchivo;
    END SNR_FuenteCabidaLinderos;

    /** Datos del documento que soporta el derecho.
     */
    !!@ ili2db.dispName = "(SNR) Fuente Derecho"
    CLASS SNR_FuenteDerecho =
      /** Tipo de documento que soporta la relación de tenencia entre el interesado con el predio.
       */
      !!@ ili2db.dispName = "Tipo de documento"
      Tipo_Documento : Submodelo_Insumos_SNR_V1_0.SNR_FuenteTipo;
      /** Identificador del documento, ejemplo: numero de la resolución
       */
      !!@ ili2db.dispName = "Número de documento"
      Numero_Documento : TEXT*255;
      !!@ ili2db.dispName = "Fecha del documento"
      Fecha_Documento : INTERLIS.XMLDate;
      /** Es tipo de oficina que emite el documento (notaria, juzgado)
       */
      !!@ ili2db.dispName = "Ente emisor"
      Ente_Emisor : MTEXT*255;
      /** Es la ciudad donde se encuentra ubicada la oficina que expide el documento.
       */
      !!@ ili2db.dispName = "Ciudad emisora"
      Ciudad_Emisora : TEXT*255;
    END SNR_FuenteDerecho;

    /** Datos de titulares de derecho inscritos en la SNR.
     */
    !!@ ili2db.dispName = "(SNR) Titular"
    CLASS SNR_Titular =
      /** Tipo de persona
       */
      !!@ ili2db.dispName = "Tipo de persona"
      Tipo_Persona : Submodelo_Insumos_SNR_V1_0.SNR_PersonaTitularTipo;
      /** Tipo de documento del que se trata.
       */
      !!@ ili2db.dispName = "Tipo de documento"
      Tipo_Documento : Submodelo_Insumos_SNR_V1_0.SNR_DocumentoTitularTipo;
      /** Documento de identidad del interesado.
       */
      !!@ ili2db.dispName = "Número de documento"
      Numero_Documento : MANDATORY TEXT*50;
      /** Nombres de la persona física.
       */
      !!@ ili2db.dispName = "Nombres"
      Nombres : TEXT*500;
      /** Primer apellido de la persona física.
       */
      !!@ ili2db.dispName = "Primer apellido"
      Primer_Apellido : TEXT*255;
      /** Segundo apellido de la persona física.
       */
      !!@ ili2db.dispName = "Segundo apellido"
      Segundo_Apellido : TEXT*255;
      /** Nombre con el que está inscrita la persona jurídica
       */
      !!@ ili2db.dispName = "Razón social"
      Razon_Social : MTEXT*255;
    END SNR_Titular;

    /** Datos del predio entregados por la SNR.
     */
    !!@ ili2db.dispName = "(SNR) Predio Registro"
    CLASS SNR_PredioRegistro =
      /** Es el nùmero que se ha asignado a la Oficina de Registro de Instrumentos públicos correspondiente.
       */
      !!@ ili2db.dispName = "Código ORIP"
      Codigo_ORIP : TEXT*3;
      /** Es el consecutivo que se asigna a cada predio jurídico abierto en la ORIP.
       */
      !!@ ili2db.dispName = "Matrícula inmobiliaria"
      Matricula_Inmobiliaria : TEXT*80;
      /** Nuevo código númerico de treinta (30) dígitos, que se le asigna a cada predio y busca localizarlo inequívocamente en los documentos catastrales, según el modelo determinado por el Instituto Geográfico Agustin Codazzi, registrado en SNR.
       */
      !!@ ili2db.dispName = "Número predial nuevo en FMI"
      Numero_Predial_Nuevo_en_FMI : TEXT*100;
      /** Anterior código númerico de veinte (20) digitos, que se le asigna a cada predio y busca localizarlo inequívocamente en los documentos catastrales, según el modelo determinado por el Instituto Geográfico Agustin Codazzi, registrado en SNR.
       */
      !!@ ili2db.dispName = "Número predial anterior en FMI"
      Numero_Predial_Anterior_en_FMI : TEXT*100;
      /** Conjunto de símbolos alfanuméricos, los cuales designan vías y predios de la ciudad.
       */
      !!@ ili2db.dispName = "Nomenclatura según registro"
      Nomenclatura_Registro : TEXT*255;
      /** El texto de cabida y linderosque está consignado en el registro público de la propiedad sobre el cual se ejercen los derechos.
       */
      !!@ ili2db.dispName = "Cabida y linderos"
      Cabida_Linderos : MTEXT;
      /** Corresponde al dato de tipo de predio incorporado en las bases de datos registrales
       */
      !!@ ili2db.dispName = "Clase del suelo según registro"
      Clase_Suelo_Registro : Submodelo_Insumos_SNR_V1_0.SNR_ClasePredioRegistroTipo;
      /** Es la matrícula por la cual se dio apertura al predio objeto de estudio (la madre).
       */
      !!@ ili2db.dispName = "Matrícula inmobiliaria matriz"
      Matricula_Inmobiliaria_Matriz : BAG {0..*} OF Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz;
      /** Fecha de la generación de datos.
       */
      !!@ ili2db.dispName = "Fecha de datos"
      Fecha_Datos : MANDATORY INTERLIS.XMLDate;
    END SNR_PredioRegistro;

    ASSOCIATION snr_derecho_fuente_derecho =
      snr_derecho -- {1..*} SNR_Derecho;
      snr_fuente_derecho -- {1} SNR_FuenteDerecho;
    END snr_derecho_fuente_derecho;

    /** Datos del titular del derecho con relación al porcentaje de participación en el derecho
     */
    ASSOCIATION snr_titular_derecho =
      snr_titular -- {1..*} SNR_Titular;
      snr_derecho -- {1..*} SNR_Derecho;
      Porcentaje_Participacion : TEXT*100;
    END snr_titular_derecho;

    ASSOCIATION snr_derecho_predio =
      snr_predio_registro -- {1} SNR_PredioRegistro;
      snr_derecho -- {1..*} SNR_Derecho;
    END snr_derecho_predio;

    ASSOCIATION snr_predio_registro_fuente_cabidalinderos =
      snr_predio_registro -- {0..*} SNR_PredioRegistro;
      snr_fuente_cabidalinderos -- {0..1} SNR_FuenteCabidaLinderos;
    END snr_predio_registro_fuente_cabidalinderos;

  END Datos_SNR;

END Submodelo_Insumos_SNR_V1_0.

MODEL Submodelo_Integracion_Insumos_V1_0 (es)
AT "mailto:PC4@localhost"
VERSION "2019-09-06"  =
  IMPORTS Submodelo_Insumos_Gestor_Catastral_V1_0,Submodelo_Insumos_SNR_V1_0;

  DOMAIN

    INI_EmparejamientoTipo = (
      /** FMI SNR - Matricula Inmobiliaria IGAC ; Número Predial IGAC - Número predial SNR ; Número predial Anterior IGAC - Número predial Anterior SNR
       */
      !!@ ili2db.dispName = "Tipo 1"
      Tipo_1,
      /** FMI SNR - Matricula Inmobiliaria IGAC ; Número Predial IGAC - Número predial SNR
       */
      !!@ ili2db.dispName = "Tipo 2"
      Tipo_2,
      /** FMI SNR - Matricula Inmobiliaria IGAC ; Número predial Anterior IGAC - Número predial Anterior SNR
       */
      !!@ ili2db.dispName = "Tipo 3"
      Tipo_3,
      /** FMI SNR - Matricula Inmobiliaria IGAC ; Número Predial IGAC - Número predial Anterior SNR
       */
      !!@ ili2db.dispName = "Tipo 4"
      Tipo_4,
      /** FMI SNR - Matricula Inmobiliaria IGAC ; Número predial Anterior IGAC - Número predial SNR
       */
      !!@ ili2db.dispName = "Tipo 5"
      Tipo_5,
      /** Número Predial IGAC - Número predial SNR ; Número predial Anterior IGAC - Número predial Anterior SNR
       */
      !!@ ili2db.dispName = "Tipo 6"
      Tipo_6,
      /** Número Predial IGAC - Número predial SNR
       */
      !!@ ili2db.dispName = "Tipo 7"
      Tipo_7,
      /** Número predial Anterior IGAC - Número predial Anterior SNR
       */
      !!@ ili2db.dispName = "Tipo 8"
      Tipo_8,
      /** Número Predial IGAC - Número predial Anterior SNR
       */
      !!@ ili2db.dispName = "Tipo 9"
      Tipo_9,
      /** Número predial Anterior IGAC - Número predial SNR
       */
      !!@ ili2db.dispName = "Tipo 10"
      Tipo_10,
      /** FMI SNR - Matricula Inmobiliaria IGAC
       */
      !!@ ili2db.dispName = "Tipo 11"
      Tipo_11
    );

  TOPIC Datos_Integracion_Insumos =
    DEPENDS ON Submodelo_Insumos_SNR_V1_0.Datos_SNR,Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral;

    /** Clase que relaciona los predios en los modelos de insumos para el Gestor Catastral y la SNR.
     */
    !!@ ili2db.dispName = "(Integración Insumos) Predio Insumos"
    CLASS INI_PredioInsumos =
      /** Tipo de emparejamiento de insumos Catastro-Registro
       */
      !!@ ili2db.dispName = "Tipo de emparejamiento"
      Tipo_Emparejamiento : Submodelo_Integracion_Insumos_V1_0.INI_EmparejamientoTipo;
      /** Observaciones de la relación.
       */
      !!@ ili2db.dispName = "Observaciones"
      Observaciones : TEXT;
    END INI_PredioInsumos;

    ASSOCIATION ini_predio_integracion_gc =
      gc_predio_catastro (EXTERNAL) -- {0..1} Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro;
      ini_predio_insumos -- {0..*} INI_PredioInsumos;
    END ini_predio_integracion_gc;

    ASSOCIATION ini_predio_integracion_snr =
      snr_predio_juridico (EXTERNAL) -- {0..1} Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro;
      ini_predio -- {0..*} INI_PredioInsumos;
    END ini_predio_integracion_snr;

  END Datos_Integracion_Insumos;

END Submodelo_Integracion_Insumos_V1_0.
','2020-08-20 18:07:45.681');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.createMetaInfo','True');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.beautifyEnumDispName','underscore');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.arrayTrafo','coalesce');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.localisedTrafo','expand');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.numericCheckConstraints','create');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.sender','ili2mssql-4.4.3-658b7daf37ba45ed2330ca3e3a3c3d59c96e91fa');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.createForeignKey','yes');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.sqlgen.createGeomIndex','True');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.defaultSrsAuthority','EPSG');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.defaultSrsCode','3116');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.uuidDefaultValue','NEWID()');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.StrokeArcs','enable');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.multiLineTrafo','coalesce');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.interlis.ili2c.ilidirs','E:\_swissphoto\_cod\qgis_dev\Asistente-LADM_COL\asistente_ladm_col\resources\models');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.createForeignKeyIndex','yes');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.jsonTrafo','coalesce');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.createEnumDefs','multiTableWithId');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.uniqueConstraints','create');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.maxSqlNameLength','60');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.inheritanceTrafo','smart2');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.catalogueRefTrafo','coalesce');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.multiPointTrafo','coalesce');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.multiSurfaceTrafo','coalesce');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.multilingualTrafo','expand');
INSERT INTO test_ladm_snr_data.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.modelsTabModelnameColSize','400');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Etiqueta','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Etiqueta','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Etiqueta','ili2db.dispName','Etiqueta');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesTerreno','ili2db.dispName','(GC) Comisiones Terreno');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Sotanos','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Sotanos','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Sotanos','ili2db.dispName','Número de sótanos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Pisos_Torre','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Pisos_Torre','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Pisos_Torre','ili2db.dispName','Total de pisos torre');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Descripcion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Descripcion','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Descripcion','ili2db.dispName','Descripción');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Etiqueta','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Etiqueta','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Etiqueta','ili2db.dispName','Etiqueta');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_terreno_predio.gc_predio','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_terreno_predio.gc_predio','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_terreno_predio.gc_predio','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesTerreno.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesTerreno.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesTerreno.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial_Anterior','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial_Anterior','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial_Anterior','ili2db.dispName','Número predial anterior');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_responsableFuente.fuente_administrativa','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_responsableFuente.fuente_administrativa','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_responsableFuente.fuente_administrativa','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Codigo_Barrio','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Codigo_Barrio','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Codigo_Barrio','ili2db.dispName','Código de barrio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_rrrFuente.fuente_administrativa','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_rrrFuente.fuente_administrativa','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_rrrFuente.fuente_administrativa','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion.Principal','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion.Principal','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion.Principal','ili2db.dispName','Principal');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Manzana_Vereda_Codigo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Manzana_Vereda_Codigo','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Manzana_Vereda_Codigo','ili2db.dispName','Código de manzana vereda');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadAdministrativaBasica.Tipo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadAdministrativaBasica.Tipo','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadAdministrativaBasica.Tipo','ili2db.dispName','Tipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesUnidadConstruccion.Numero_Predial','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesUnidadConstruccion.Numero_Predial','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesUnidadConstruccion.Numero_Predial','ili2db.dispName','Número predial');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Unidades_Sotano','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Unidades_Sotano','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Unidades_Sotano','ili2db.dispName','Total de unidades sótano');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_clFuente.cl','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_clFuente.cl','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_clFuente.cl','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Valor_Via_Generadora','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Valor_Via_Generadora','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Valor_Via_Generadora','ili2db.dispName','Valor de vía generadora');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Terreno_Privada','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Terreno_Privada','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Terreno_Privada','ili2db.dispName','Área total de terreno privada');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Nombre_Predio','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Nombre_Predio','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Nombre_Predio','ili2db.dispName','Nombre del predio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitRrr.unidad','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitRrr.unidad','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitRrr.unidad','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Interesado.ext_PID','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Interesado.ext_PID','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Interesado.ext_PID','ili2db.dispName','Ext PID');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Primer_Apellido','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Primer_Apellido','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Primer_Apellido','ili2db.dispName','Primer apellido');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Locales','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Locales','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Locales','ili2db.dispName','Total de locales');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Fecha_Documento','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Fecha_Documento','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Fecha_Documento','ili2db.dispName','Fecha del documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoRedServicios.Estado','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoRedServicios.Estado','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoRedServicios.Estado','ili2db.dispName','Estado');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Nombre','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Nombre','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Nombre','ili2db.dispName','Nombre');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio','ili2db.dispName','(GC) Datos Propiedad Horizontal Condominio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Sotanos','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Sotanos','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Sotanos','ili2db.dispName','Total de sótanos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Pisos','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Pisos','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Pisos','ili2db.dispName','Total de pisos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_CarasLindero.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_CarasLindero.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_CarasLindero.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Semisotanos','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Semisotanos','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Semisotanos','ili2db.dispName','Número de semisótanos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueNivel.ue','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueNivel.ue','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueNivel.ue','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueNivel.nivel','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueNivel.nivel','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueNivel.nivel','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Mezanines','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Mezanines','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Mezanines','ili2db.dispName','Número de mezanines');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Tipo_Documento','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Tipo_Documento','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Tipo_Documento','ili2db.dispName','Tipo de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_fuente_derecho.snr_derecho','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_fuente_derecho.snr_derecho','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_fuente_derecho.snr_derecho','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_unidad.gc_construccion','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_unidad.gc_construccion','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_unidad.gc_construccion','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Segundo_Apellido','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Segundo_Apellido','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Segundo_Apellido','ili2db.dispName','Segundo apellido');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.INI_PredioInsumos.Observaciones','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.INI_PredioInsumos.Observaciones','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.INI_PredioInsumos.Observaciones','ili2db.dispName','Observaciones');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo','ili2db.dispName','Archivo fuente');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtRedServiciosFisica.Orientada','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtRedServiciosFisica.Orientada','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtRedServiciosFisica.Orientada','ili2db.dispName','Orientada');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_copropiedad.gc_matriz','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_copropiedad.gc_matriz','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_copropiedad.gc_matriz','ili2db.ili.assocKind','AGGREGATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Fraccion.Denominador','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Fraccion.Denominador','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Fraccion.Denominador','ili2db.dispName','Denominador');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtRedServiciosFisica.Ext_Interesado_Administrador_ID','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtRedServiciosFisica.Ext_Interesado_Administrador_ID','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtRedServiciosFisica.Ext_Interesado_Administrador_ID','ili2db.dispName','Ext interesado administrador id');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Direcciones','ili2db.ili.attrCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Direcciones','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Direcciones','ili2db.dispName','Direcciones');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Codigo_Edificacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Codigo_Edificacion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Codigo_Edificacion','ili2db.dispName','Código de edificación');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Construida_Comun','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Construida_Comun','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Construida_Comun','ili2db.dispName','Área total construida común');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteAdministrativa.Tipo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteAdministrativa.Tipo','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteAdministrativa.Tipo','ili2db.dispName','Tipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Sector_Ciudad','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Sector_Ciudad','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Sector_Ciudad','ili2db.dispName','Sector de la ciudad');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorRural','ili2db.dispName','(GC) Sector Rural');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.Porcentaje_Participacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.Porcentaje_Participacion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Oid.Local_Id','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Oid.Local_Id','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Oid.Local_Id','ili2db.dispName','Local ID');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Codigo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Codigo','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Codigo','ili2db.dispName','Código');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Complemento','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Complemento','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Complemento','ili2db.dispName','Complemento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Pisos','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Pisos','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Pisos','ili2db.dispName','Número de pisos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Terreno_Comun','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Terreno_Comun','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Terreno_Comun','ili2db.dispName','Área total de terreno común');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Transformacion.Transformacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Transformacion.Transformacion','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Transformacion.Transformacion','ili2db.dispName','Transformación');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Espacio_De_Nombres','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Espacio_De_Nombres','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Espacio_De_Nombres','ili2db.dispName','Espacio de nombres');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion','ili2db.dispName','(GC) Construcción');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio.Fecha_Alerta','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio.Fecha_Alerta','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio.Fecha_Alerta','ili2db.dispName','Fecha de alerta');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_propietario_predio.gc_predio_catastro','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_propietario_predio.gc_predio_catastro','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_propietario_predio.gc_predio_catastro','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion','ili2db.dispName','(GC) Dirección');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Condicion_Predio','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Condicion_Predio','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Condicion_Predio','ili2db.dispName','Condición del predio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_unidadconstruccion_calificacionunidadconstruccion.gc_unidadconstruccion','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_unidadconstruccion_calificacionunidadconstruccion.gc_unidadconstruccion','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_unidadconstruccion_calificacionunidadconstruccion.gc_unidadconstruccion','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Matricula_Inmobiliaria_Matriz','ili2db.ili.attrCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Matricula_Inmobiliaria_Matriz','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Matricula_Inmobiliaria_Matriz','ili2db.dispName','Matrícula inmobiliaria matriz');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Tipo_Construccion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Tipo_Construccion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Tipo_Construccion','ili2db.dispName','Tipo de construcción');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoCl.punto','ili2db.ili.assocCardinalityMin','3');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoCl.punto','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoCl.punto','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_unidadFuente.unidad','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_unidadFuente.unidad','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_unidadFuente.unidad','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Sector_Predio','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Sector_Predio','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Sector_Predio','ili2db.dispName','Sector del predio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Etiqueta','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Etiqueta','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Etiqueta','ili2db.dispName','Etiqueta');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_predio.gc_predio','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_predio.gc_predio','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_predio.gc_predio','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Fecha_Datos','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Fecha_Datos','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Fecha_Datos','ili2db.dispName','Fecha de datos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Codigo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Codigo','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Codigo','ili2db.dispName','Código');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Numero_Predial_Nuevo_en_FMI','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Numero_Predial_Nuevo_en_FMI','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Numero_Predial_Nuevo_en_FMI','ili2db.dispName','Número predial nuevo en FMI');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_predio_registro_fuente_cabidalinderos.snr_fuente_cabidalinderos','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_predio_registro_fuente_cabidalinderos.snr_fuente_cabidalinderos','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_predio_registro_fuente_cabidalinderos.snr_fuente_cabidalinderos','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital','ili2db.dispName','Área terreno digital');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Fraccion.Numerador','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Fraccion.Numerador','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Fraccion.Numerador','ili2db.dispName','Numerador');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Entrega','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Entrega','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Entrega','ili2db.dispName','Fecha de entrega');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_unidadconstruccion_calificacionunidadconstruccion.gc_calificacionunidadconstruccion','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_unidadconstruccion_calificacionunidadconstruccion.gc_calificacionunidadconstruccion','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_unidadconstruccion_calificacionunidadconstruccion.gc_calificacionunidadconstruccion','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_propietario_predio.gc_propietario','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_propietario_predio.gc_propietario','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_propietario_predio.gc_propietario','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Matricula_Inmobiliaria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Matricula_Inmobiliaria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Matricula_Inmobiliaria','ili2db.dispName','Matrícula inmobiliaria');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad','ili2db.dispName','Estado de disponibilidad');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente','ili2db.dispName','Fecha de documento fuente');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Geometria','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Nombre','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Nombre','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Nombre','ili2db.dispName','Código nombre');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Ente_Emisor','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Ente_Emisor','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Ente_Emisor','ili2db.dispName','Ente emisor');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Nomenclatura_Registro','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Nomenclatura_Registro','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Nomenclatura_Registro','ili2db.dispName','Nomenclatura según registro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_topografoFuente.topografo','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_topografoFuente.topografo','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_topografoFuente.topografo','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_datosphcondominio_datostorreph.gc_datostorreph','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_datosphcondominio_datostorreph.gc_datostorreph','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_datosphcondominio_datostorreph.gc_datostorreph','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.INI_PredioInsumos','ili2db.dispName','(Integración Insumos) Predio Insumos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Predio','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Predio','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Predio','ili2db.dispName','Tipo de predio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion.Tipo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion.Tipo','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion.Tipo','ili2db.dispName','Tipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Clase_Suelo_Registro','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Clase_Suelo_Registro','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Clase_Suelo_Registro','ili2db.dispName','Clase del suelo según registro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Tipo_Construccion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Tipo_Construccion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Tipo_Construccion','ili2db.dispName','Tipo de construcción');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_RelacionNecesariaUnidadesEspaciales.Relacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_RelacionNecesariaUnidadesEspaciales.Relacion','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_RelacionNecesariaUnidadesEspaciales.Relacion','ili2db.dispName','Relación');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Nombre','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Nombre','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Nombre','ili2db.dispName','Nombre');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Puntos','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Puntos','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Puntos','ili2db.dispName','Puntos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor.Area','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor.Area','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor.Area','ili2db.dispName','Área');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_topografoFuente.fuente_espacial','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_topografoFuente.fuente_espacial','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_topografoFuente.fuente_espacial','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Es_Direccion_Principal','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Es_Direccion_Principal','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Es_Direccion_Principal','ili2db.dispName','Es dirección principal');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_VolumenValor.Tipo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_VolumenValor.Tipo','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_VolumenValor.Tipo','ili2db.dispName','Tipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoRedServicios.ext_ID_Red_Fisica','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoRedServicios.ext_ID_Red_Fisica','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoRedServicios.ext_ID_Red_Fisica','ili2db.dispName','Ext id red física');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro','ili2db.dispName','(GC) Predio Catastro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Nivel.Estructura','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Nivel.Estructura','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Nivel.Estructura','ili2db.dispName','Estructura');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Localizacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Localizacion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Localizacion','ili2db.dispName','Localización');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Numero_Predio','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Numero_Predio','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Numero_Predio','ili2db.dispName','Número del predio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion.Geometria_Referencia','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion.Geometria_Referencia','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion.Geometria_Referencia','ili2db.dispName','Geometría de referencia');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_relacionFuenteUespacial.fuente_espacial','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_relacionFuenteUespacial.fuente_espacial','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_relacionFuenteUespacial.fuente_espacial','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_copropiedad.gc_unidad','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_copropiedad.gc_unidad','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_copropiedad.gc_unidad','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Planta','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Planta','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Planta','ili2db.dispName','Planta');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Area_Construida','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Area_Construida','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Area_Construida','ili2db.dispName','Área construida');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Nivel.Tipo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Nivel.Tipo','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Nivel.Tipo','ili2db.dispName','Tipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado','ili2db.ili.attrCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado','ili2db.dispName','Transformación y resultado');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_snr.snr_predio_juridico','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_snr.snr_predio_juridico','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_snr.snr_predio_juridico','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Identificador','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Identificador','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Identificador','ili2db.dispName','Identificador');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Unidades_Privadas','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Unidades_Privadas','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Unidades_Privadas','ili2db.dispName','Total de unidades privadas');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_RelacionNecesariaBAUnits.Relacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_RelacionNecesariaBAUnits.Relacion','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_RelacionNecesariaBAUnits.Relacion','ili2db.dispName','Relación');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Codigo_Sector','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Codigo_Sector','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Codigo_Sector','ili2db.dispName','Código sector');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueFuente.fuente_espacial','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueFuente.fuente_espacial','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueFuente.fuente_espacial','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Catastro','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Catastro','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Catastro','ili2db.dispName','Tipo de catastro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Tipo_Dominio','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Tipo_Dominio','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Tipo_Dominio','ili2db.dispName','Tipo de dominio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_rrrInteresado.rrr','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_rrrInteresado.rrr','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_rrrInteresado.rrr','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_unidad.gc_unidad_construccion','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_unidad.gc_unidad_construccion','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_unidad.gc_unidad_construccion','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Codigo_ORIP','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Codigo_ORIP','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Codigo_ORIP','ili2db.dispName','Código ORIP');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.snr_titular','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.snr_titular','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.snr_titular','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Valor_Via_Principal','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Valor_Via_Principal','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Valor_Via_Principal','ili2db.dispName','Valor vía principal');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesUnidadConstruccion.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesUnidadConstruccion.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesUnidadConstruccion.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor','ili2db.dispName','Valores de área');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Letra_Via_Generadora','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Letra_Via_Generadora','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Letra_Via_Generadora','ili2db.dispName','Letra de vía generadora');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Digito_Verificacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Digito_Verificacion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Digito_Verificacion','ili2db.dispName','Dígito de verificación');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoReferencia.ue','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoReferencia.ue','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoReferencia.ue','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion','ili2db.dispName','(GC) Calificación unidad de construcción');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_responsableFuente.interesado','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_responsableFuente.interesado','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_responsableFuente.interesado','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.PuntoTipo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.PuntoTipo','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.PuntoTipo','ili2db.dispName','Tipo de punto');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Fotografia','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Fotografia','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Fotografia','ili2db.dispName','Fotografía');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoCcl.ccl','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoCcl.ccl','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoCcl.ccl','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Numero_Subterraneos','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Numero_Subterraneos','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Numero_Subterraneos','ili2db.dispName','Número de subterráneos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho','ili2db.dispName','(SNR) Derecho');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz.Codigo_ORIP','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz.Codigo_ORIP','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz.Codigo_ORIP','ili2db.dispName','Código ORIP');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Numero_Predial_Anterior_en_FMI','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Numero_Predial_Anterior_en_FMI','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Numero_Predial_Anterior_en_FMI','ili2db.dispName','Número predial anterior en FMI');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Area_Construida','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Area_Construida','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Area_Construida','ili2db.dispName','Área construida');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Datos','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Datos','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Datos','ili2db.dispName','Datos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_copropiedad.Coeficiente_Copropiedad','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_copropiedad.Coeficiente_Copropiedad','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Ciudad_Emisora','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Ciudad_Emisora','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Ciudad_Emisora','ili2db.dispName','Ciudad emisora');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Letra_Via_Principal','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Letra_Via_Principal','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Letra_Via_Principal','ili2db.dispName','Letra vía principal');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro','ili2db.dispName','(GC) Perímetro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho.Calidad_Derecho_Registro','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho.Calidad_Derecho_Registro','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho.Calidad_Derecho_Registro','ili2db.dispName','Calidad derecho registro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueBaunit.baunit','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueBaunit.baunit','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueBaunit.baunit','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion','ili2db.dispName','(GC) Unidad Construcción');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_clFuente.fuente_espacial','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_clFuente.fuente_espacial','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_clFuente.fuente_espacial','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.snr_derecho','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.snr_derecho','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.snr_derecho','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Nombre','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Nombre','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Nombre','ili2db.dispName','Nombre');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Puntaje','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Puntaje','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Puntaje','ili2db.dispName','Puntaje');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Banios','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Banios','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Banios','ili2db.dispName','Total de baños');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Codigo_Sector','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Codigo_Sector','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Codigo_Sector','ili2db.dispName','Código del sector');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Primer_Nombre','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Primer_Nombre','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Primer_Nombre','ili2db.dispName','Primer nombre');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz.Matricula_Inmobiliaria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz.Matricula_Inmobiliaria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz.Matricula_Inmobiliaria','ili2db.dispName','Matrícula inmobiliaria');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_masCcl.ue_mas','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_masCcl.ue_mas','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_masCcl.ue_mas','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Ciudad_Emisora','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Ciudad_Emisora','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Ciudad_Emisora','ili2db.dispName','Ciudad emisora');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueUeGrupo.todo','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueUeGrupo.todo','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueUeGrupo.todo','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_relacionFuenteUespacial.relacionrequeridaUe','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_relacionFuenteUespacial.relacionrequeridaUe','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_relacionFuenteUespacial.relacionrequeridaUe','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Uso','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Uso','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Uso','ili2db.dispName','Uso');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueFuente.ue','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueFuente.ue','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueFuente.ue','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_fuente_derecho.snr_fuente_derecho','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_fuente_derecho.snr_fuente_derecho','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_fuente_derecho.snr_fuente_derecho','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Ext_Direccion_ID','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Ext_Direccion_ID','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Ext_Direccion_ID','ili2db.dispName','Ext dirección id');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Local_Id','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Local_Id','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Local_Id','ili2db.dispName','Local ID');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor.Datos_Proyeccion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor.Datos_Proyeccion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor.Datos_Proyeccion','ili2db.dispName','Datos de la proyección');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Total_Unidades_Sotano','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Total_Unidades_Sotano','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Total_Unidades_Sotano','ili2db.dispName','Total de unidades de sótano');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueJerarquiaGrupo.agrupacion','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueJerarquiaGrupo.agrupacion','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueJerarquiaGrupo.agrupacion','ili2db.ili.assocKind','AGGREGATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_relacionFuente.fuente_administrativa','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_relacionFuente.fuente_administrativa','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_relacionFuente.fuente_administrativa','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular','ili2db.dispName','(SNR) Titular');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_gc.ini_predio_insumos','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_gc.ini_predio_insumos','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_gc.ini_predio_insumos','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID','ili2db.dispName','Ext archivo id');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion','ili2db.dispName','Dirección');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Habitaciones','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Habitaciones','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Habitaciones','ili2db.dispName','Total de habitaciones');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.MetodoProduccion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.MetodoProduccion','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.MetodoProduccion','ili2db.dispName','Método de producción');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_cclFuente.fuente_espacial','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_cclFuente.fuente_espacial','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_cclFuente.fuente_espacial','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_masCl.ue_mas','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_masCl.ue_mas','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_masCl.ue_mas','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio.Entidad_Emisora_Alerta','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio.Entidad_Emisora_Alerta','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio.Entidad_Emisora_Alerta','ili2db.dispName','Entidad emisora de la alerta');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos','ili2db.dispName','(SNR) Fuente Cabida Linderos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_predio_registro_fuente_cabidalinderos.snr_predio_registro','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_predio_registro_fuente_cabidalinderos.snr_predio_registro','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_predio_registro_fuente_cabidalinderos.snr_predio_registro','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtUnidadEdificacionFisica.Ext_Direccion_ID','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtUnidadEdificacionFisica.Ext_Direccion_ID','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtUnidadEdificacionFisica.Ext_Direccion_ID','ili2db.dispName','Ext dirección id');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion.Dimensiones_Origen','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion.Dimensiones_Origen','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion.Dimensiones_Origen','ili2db.dispName','Dimensiones origen');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoFuente.fuente_espacial','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoFuente.fuente_espacial','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoFuente.fuente_espacial','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio.Estado_Alerta','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio.Estado_Alerta','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio.Estado_Alerta','ili2db.dispName','Estado alerta');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoReferencia.punto','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoReferencia.punto','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoReferencia.punto','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Nombre','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Nombre','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Nombre','ili2db.dispName','Nombre');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Volumen','ili2db.ili.attrCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Volumen','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Volumen','ili2db.dispName','Volumen');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Codigo_Anterior','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Codigo_Anterior','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Codigo_Anterior','ili2db.dispName','Código anterior');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Firma','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Firma','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Firma','ili2db.dispName','Firma');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitRrr.rrr','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitRrr.rrr','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitRrr.rrr','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_miembros.interesado','ili2db.ili.assocCardinalityMin','2');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_miembros.interesado','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_miembros.interesado','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_menosCcl.ccl_menos','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_menosCcl.ccl_menos','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_menosCcl.ccl_menos','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorUrbano.Codigo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorUrbano.Codigo','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorUrbano.Codigo','ili2db.dispName','Código');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Dimension','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Dimension','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Dimension','ili2db.dispName','Dimensión');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio','ili2db.dispName','(GC) EstadoPredio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Fecha_Datos','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Fecha_Datos','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Fecha_Datos','ili2db.dispName','Fecha de los datos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_cclFuente.ccl','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_cclFuente.ccl','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_cclFuente.ccl','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueUeGrupo.parte','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueUeGrupo.parte','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueUeGrupo.parte','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_VolumenValor.Volumen_Medicion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_VolumenValor.Volumen_Medicion','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_VolumenValor.Volumen_Medicion','ili2db.dispName','Volumen medición');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorUrbano','ili2db.dispName','(GC) Sector Urbano');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Total_Unidades_Privadas','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Total_Unidades_Privadas','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Total_Unidades_Privadas','ili2db.dispName','Total de unidades privadas');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Anio_Construccion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Anio_Construccion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Anio_Construccion','ili2db.dispName','Año de construcción');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Estado_Predio','ili2db.ili.attrCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Estado_Predio','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Estado_Predio','ili2db.dispName','Estado del predio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion.Ddimensiones_Objetivo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion.Ddimensiones_Objetivo','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion.Ddimensiones_Objetivo','ili2db.dispName','Ddimensiones objetivo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Codigo_Postal','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Codigo_Postal','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Codigo_Postal','ili2db.dispName','Código postal');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Aceptacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Aceptacion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Aceptacion','ili2db.dispName','Fecha de aceptación');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorUrbano.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorUrbano.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorUrbano.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_predio.snr_predio_registro','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_predio.snr_predio_registro','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_predio.snr_predio_registro','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Tipo_Dominio','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Tipo_Dominio','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Tipo_Dominio','ili2db.dispName','Tipo de dominio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz','ili2db.dispName','(SNR) Estructura Matrícula Matriz');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Nivel.Registro_Tipo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Nivel.Registro_Tipo','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Nivel.Registro_Tipo','ili2db.dispName','Tipo de registro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Construida_Privada','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Construida_Privada','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Construida_Privada','ili2db.dispName','Área total construida privada');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Elemento_Calificacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Elemento_Calificacion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Elemento_Calificacion','ili2db.dispName','Elemento de calificación');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Tipo_Principal','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Tipo_Principal','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Tipo_Principal','ili2db.dispName','Tipo principal');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Codigo_Terreno','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Codigo_Terreno','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Codigo_Terreno','ili2db.dispName','Código terreno');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesUnidadConstruccion','ili2db.dispName','(GC) Comisiones Unidad Construcción');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Tipo_Documento','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Tipo_Documento','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Tipo_Documento','ili2db.dispName','Tipo de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version','ili2db.dispName','Versión de comienzo de vida útil');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda','ili2db.dispName','(GC) Vereda');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Cabida_Linderos','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Cabida_Linderos','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Cabida_Linderos','ili2db.dispName','Cabida y linderos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_CarasLindero.Localizacion_Textual','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_CarasLindero.Localizacion_Textual','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_CarasLindero.Localizacion_Textual','ili2db.dispName','Localización textual');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_CadenaCarasLimite.Localizacion_Textual','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_CadenaCarasLimite.Localizacion_Textual','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_CadenaCarasLimite.Localizacion_Textual','ili2db.dispName','Localización textual');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Circulo_Registral','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Circulo_Registral','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Circulo_Registral','ili2db.dispName','Círculo registral');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_relacionFuente.relacionrequeridaBaunit','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_relacionFuente.relacionrequeridaBaunit','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_relacionFuente.relacionrequeridaBaunit','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Sistema_Procedencia_Datos','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Sistema_Procedencia_Datos','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Sistema_Procedencia_Datos','ili2db.dispName','Sistema procedencia de los datos');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Codigo_Anterior','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Codigo_Anterior','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Codigo_Anterior','ili2db.dispName','Código anterior');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Grabacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Grabacion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Grabacion','ili2db.dispName','Fecha de grabación');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH','ili2db.dispName','(GC) Datos torre PH');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Oid.Espacio_De_Nombres','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Oid.Espacio_De_Nombres','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Oid.Espacio_De_Nombres','ili2db.dispName','Espacio de nombres');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Punto_Referencia','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Punto_Referencia','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Punto_Referencia','ili2db.dispName','Punto de referencia');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_rrrFuente.rrr','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_rrrFuente.rrr','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_rrrFuente.rrr','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Extraccion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Extraccion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Extraccion','ili2db.dispName','Extracción');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Segundo_Apellido','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Segundo_Apellido','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Segundo_Apellido','ili2db.dispName','Segundo apellido');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitComoInteresado.interesado','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitComoInteresado.interesado','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitComoInteresado.interesado','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Transformacion.Localizacion_Transformada','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Transformacion.Localizacion_Transformada','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Transformacion.Localizacion_Transformada','ili2db.dispName','Localización transformada');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_terreno_predio.gc_terreno','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_terreno_predio.gc_terreno','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_terreno_predio.gc_terreno','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_menosCcl.ue_menos','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_menosCcl.ue_menos','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_menosCcl.ue_menos','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_menosCl.cl_menos','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_menosCl.cl_menos','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_menosCl.cl_menos','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Departamento','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Departamento','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Departamento','ili2db.dispName','Código del departamento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Fecha_Documento','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Fecha_Documento','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Fecha_Documento','ili2db.dispName','Fecha de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Numero_Documento','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Numero_Documento','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Numero_Documento','ili2db.dispName','Número de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Archivo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Archivo','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Archivo','ili2db.dispName','Archivo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Etiqueta','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Etiqueta','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Etiqueta','ili2db.dispName','Etiqueta');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Identificador','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Identificador','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Identificador','ili2db.dispName','Identificador');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Area_Privada','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Area_Privada','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Area_Privada','ili2db.dispName','Área privada');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana','ili2db.dispName','(GC) Manzana');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Numero_Documento','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Numero_Documento','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Numero_Documento','ili2db.dispName','Número de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario','ili2db.dispName','(GC) Propietario');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorRural.Codigo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorRural.Codigo','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorRural.Codigo','ili2db.dispName','Código');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.INI_PredioInsumos.Tipo_Emparejamiento','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.INI_PredioInsumos.Tipo_Emparejamiento','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.INI_PredioInsumos.Tipo_Emparejamiento','ili2db.dispName','Tipo de emparejamiento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Tipo_Direccion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Tipo_Direccion','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Tipo_Direccion','ili2db.dispName','Tipo de dirección');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesConstruccion.Numero_Predial','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesConstruccion.Numero_Predial','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesConstruccion.Numero_Predial','ili2db.dispName','Número predial');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitFuente.unidad','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitFuente.unidad','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitFuente.unidad','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Tipo_Documento','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Tipo_Documento','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Tipo_Documento','ili2db.dispName','Tipo de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_snr.ini_predio','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_snr.ini_predio','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_snr.ini_predio','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_datosphcondominio_datostorreph.gc_datosphcondominio','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_datosphcondominio_datostorreph.gc_datosphcondominio','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_datosphcondominio_datostorreph.gc_datosphcondominio','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Codigo_Terreno','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Codigo_Terreno','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Codigo_Terreno','ili2db.dispName','Código de terreno');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_unidadFuente.fuente_administrativa','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_unidadFuente.fuente_administrativa','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_unidadFuente.fuente_administrativa','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoCcl.punto','ili2db.ili.assocCardinalityMin','2');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoCcl.punto','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoCcl.punto','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_menosCl.ue_menos','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_menosCl.ue_menos','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_menosCl.ue_menos','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_ph_predio.gc_datos_ph','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_ph_predio.gc_datos_ph','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_ph_predio.gc_datos_ph','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio','ili2db.dispName','(GC) Barrio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Destinacion_Economica','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Destinacion_Economica','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Destinacion_Economica','ili2db.dispName','Destinación económica');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion.Valor','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion.Valor','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion.Valor','ili2db.dispName','Valor');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Area','ili2db.ili.attrCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Area','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Area','ili2db.dispName','Área');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Numero_Documento','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Numero_Documento','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Numero_Documento','ili2db.dispName','Número de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionInteresados.Tipo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionInteresados.Tipo','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionInteresados.Tipo','ili2db.dispName','Tipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Primer_Apellido','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Primer_Apellido','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Primer_Apellido','ili2db.dispName','Primer apellido');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_masCcl.ccl_mas','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_masCcl.ccl_mas','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_masCcl.ccl_mas','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Tipo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Tipo','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Tipo','ili2db.dispName','Tipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitFuente.fuente_espacial','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitFuente.fuente_espacial','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitFuente.fuente_espacial','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesTerreno.Numero_Predial','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesTerreno.Numero_Predial','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesTerreno.Numero_Predial','ili2db.dispName','Número predial');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Torre','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Torre','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Torre','ili2db.dispName','Torre');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica','ili2db.dispName','Área terreno alfanumérica');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie','ili2db.dispName','Relación superficie');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Posicion_Interpolacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Posicion_Interpolacion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Posicion_Interpolacion','ili2db.dispName','Posición interpolación');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho.Codigo_Naturaleza_Juridica','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho.Codigo_Naturaleza_Juridica','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho.Codigo_Naturaleza_Juridica','ili2db.dispName','Código naturaleza jurídica');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoCl.cl','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoCl.cl','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoCl.cl','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_gc.gc_predio_catastro','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_gc.gc_predio_catastro','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_gc.gc_predio_catastro','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Huella_Dactilar','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Huella_Dactilar','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Huella_Dactilar','ili2db.dispName','Huella dactilar');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno','ili2db.dispName','(GC) Terreno');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueBaunit.ue','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueBaunit.ue','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueBaunit.ue','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Interesado.Nombre','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Interesado.Nombre','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Interesado.Nombre','ili2db.dispName','Nombre');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadAdministrativaBasica.Nombre','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadAdministrativaBasica.Nombre','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadAdministrativaBasica.Nombre','ili2db.dispName','Nombre');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_rrrInteresado.interesado','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_rrrInteresado.interesado','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_rrrInteresado.interesado','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteAdministrativa.Numero_Fuente','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteAdministrativa.Numero_Fuente','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteAdministrativa.Numero_Fuente','ili2db.dispName','Número de fuente');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Razon_Social','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Razon_Social','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Razon_Social','ili2db.dispName','Razón social');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version','ili2db.dispName','Versión de fin de vida útil');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Documento_Escaneado','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Documento_Escaneado','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Documento_Escaneado','ili2db.dispName','Documento escaneado');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_predio.snr_derecho','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_predio.snr_derecho','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_predio.snr_derecho','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion.Formula','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion.Formula','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion.Formula','ili2db.dispName','Fórmula');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Nombres','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Nombres','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Nombres','ili2db.dispName','Nombres');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID','ili2db.ili.attrCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID','ili2db.dispName','Ext dirección id');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_predio.gc_construccion','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_predio.gc_construccion','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_predio.gc_construccion','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Imagen.uri','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Imagen.uri','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.Imagen.uri','ili2db.dispName','uri');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Metadato','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Metadato','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Metadato','ili2db.dispName','Metadato');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Clase_Via_Principal','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Clase_Via_Principal','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Clase_Via_Principal','ili2db.dispName','Clase de vía principal');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueJerarquiaGrupo.elemento','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueJerarquiaGrupo.elemento','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_ueJerarquiaGrupo.elemento','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_ph_predio.gc_predio','ili2db.ili.assocCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_ph_predio.gc_predio','ili2db.ili.assocCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_ph_predio.gc_predio','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Codigo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Codigo','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Codigo','ili2db.dispName','Código');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor.Tipo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor.Tipo','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor.Tipo','ili2db.dispName','Tipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesConstruccion','ili2db.dispName','(GC) Comisiones Construcción');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Nombre_Geografico','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Nombre_Geografico','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Nombre_Geografico','ili2db.dispName','Nombre geográfico');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Nivel.Nombre','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Nivel.Nombre','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_Nivel.Nombre','ili2db.dispName','Nombre');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Detalle_Calificacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Detalle_Calificacion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Detalle_Calificacion','ili2db.dispName','Detalle de calificación');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial','ili2db.dispName','Número predial');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_CadenaCarasLimite.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_CadenaCarasLimite.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_CadenaCarasLimite.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion.Ext_Unidad_Edificacion_Fisica_ID','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion.Ext_Unidad_Edificacion_Fisica_ID','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion.Ext_Unidad_Edificacion_Fisica_ID','ili2db.dispName','Ext unidad edificación física id');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoRedServicios.Tipo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoRedServicios.Tipo','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_EspacioJuridicoRedServicios.Tipo','ili2db.dispName','Tipo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoFuente.punto','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoFuente.punto','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_puntoFuente.punto','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.NUPRE','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.NUPRE','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.NUPRE','ili2db.dispName','Número único predial');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_miembros.agrupacion','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_miembros.agrupacion','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_miembros.agrupacion','ili2db.ili.assocKind','AGGREGATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro','ili2db.dispName','(SNR) Predio Registro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesConstruccion.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesConstruccion.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesConstruccion.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Nombre','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Nombre','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Nombre','ili2db.dispName','Nombre');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Nivel_Jerarquico','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Nivel_Jerarquico','ili2db.ili.attrCardinalityMin','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Nivel_Jerarquico','ili2db.dispName','Nivel jerárquico');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Municipio','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Municipio','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Municipio','ili2db.dispName','Código del municipio');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_DRR.Descripcion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_DRR.Descripcion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_DRR.Descripcion','ili2db.dispName','Descripción');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Tipo_Avaluo','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Tipo_Avaluo','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Tipo_Avaluo','ili2db.dispName','Tipo de avalúo');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Numero_Documento','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Numero_Documento','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Numero_Documento','ili2db.dispName','Número de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Componente','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Componente','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Componente','ili2db.dispName','Componente');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho','ili2db.dispName','(SNR) Fuente Derecho');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorRural.Geometria','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorRural.Geometria','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorRural.Geometria','ili2db.dispName','Geometría');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Tipo_Persona','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Tipo_Persona','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Tipo_Persona','ili2db.dispName','Tipo de persona');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Matricula_Inmobiliaria_Catastro','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Matricula_Inmobiliaria_Catastro','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Matricula_Inmobiliaria_Catastro','ili2db.dispName','Matrícula inmobiliaria catastro');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_miembros.participacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_miembros.participacion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitComoInteresado.unidad','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitComoInteresado.unidad','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_baunitComoInteresado.unidad','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Segundo_Nombre','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Segundo_Nombre','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Segundo_Nombre','ili2db.dispName','Segundo nombre');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Tipo_Documento','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Tipo_Documento','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Tipo_Documento','ili2db.dispName','Tipo de documento');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Razon_Social','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Razon_Social','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Razon_Social','ili2db.dispName','Razón social');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Ente_Emisor','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Ente_Emisor','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Ente_Emisor','ili2db.dispName','Ente emisor');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteAdministrativa.Observacion','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteAdministrativa.Observacion','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.COL_FuenteAdministrativa.Observacion','ili2db.dispName','Observación');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_masCl.cl_mas','ili2db.ili.assocCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_masCl.cl_mas','ili2db.ili.assocCardinalityMax','*');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('LADM_COL_V3_0.LADM_Nucleo.col_masCl.cl_mas','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Valor_Total_Avaluo_Catastral','ili2db.ili.attrCardinalityMax','1');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Valor_Total_Avaluo_Catastral','ili2db.ili.attrCardinalityMin','0');
INSERT INTO test_ladm_snr_data.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Valor_Total_Avaluo_Catastral','ili2db.dispName','Valor total avaúo catastral');
