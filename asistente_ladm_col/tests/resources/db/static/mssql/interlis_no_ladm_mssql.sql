IF NOT EXISTS (SELECT  schema_name FROM information_schema.schemata WHERE schema_name = 'interlis_no_ladm')EXEC sp_executesql N'CREATE SCHEMA interlis_no_ladm';
CREATE SEQUENCE interlis_no_ladm.t_ili2db_seq START WITH 1;;
-- SZ_Freienbach2035_20180622.Datei
CREATE TABLE interlis_no_ladm.datei (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for interlis_no_ladm.t_ili2db_seq)
  ,[T_Seq] BIGINT NULL
  ,[aname] VARCHAR(100) NOT NULL
  ,[inhalt] VARCHAR(MAX) NOT NULL
  ,[objektinformation_dateien] BIGINT NULL
)
;
-- SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft
CREATE TABLE interlis_no_ladm.liegenschaft (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for interlis_no_ladm.t_ili2db_seq)
  ,[kennung] VARCHAR(25) NOT NULL
  ,[erstelltvon] VARCHAR(100) NOT NULL
  ,[erstelltam] DATE NOT NULL
  ,[geaendertvon] VARCHAR(100) NOT NULL
  ,[geaendertam] DATE NOT NULL
  ,[art] BIGINT NOT NULL
  ,[grundstuecknr] VARCHAR(50) NOT NULL
  ,[bezeichnung] VARCHAR(250) NOT NULL
  ,[adresse] VARCHAR(50) NOT NULL
  ,[ortsteil] BIGINT NOT NULL
  ,[nutzung] VARCHAR(250) NOT NULL
  ,[istbauland] BIT NOT NULL
  ,[gebaeudeart] VARCHAR(250) NULL
  ,[bemerkung] VARCHAR(250) NULL
  ,[flaeche] NUMERIC(6) NULL
  ,[zonennamekurz] VARCHAR(10) NOT NULL
)
;
-- SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation
CREATE TABLE interlis_no_ladm.objektinformation (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for interlis_no_ladm.t_ili2db_seq)
  ,[nummer] VARCHAR(10) NOT NULL
  ,[erstelltvon] VARCHAR(100) NOT NULL
  ,[erstelltam] DATE NOT NULL
  ,[geaendertvon] VARCHAR(100) NOT NULL
  ,[geaendertam] DATE NOT NULL
  ,[aname] VARCHAR(50) NOT NULL
  ,[beschrieb] VARCHAR(250) NOT NULL
  ,[naechsteschritte] VARCHAR(1500) NULL
)
;
-- SZ_Freienbach2035_20180622.Gemeindeinformationen.LiegenschaftGeom
CREATE TABLE interlis_no_ladm.liegenschaftgeom (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for interlis_no_ladm.t_ili2db_seq)
  ,[geometrie] GEOMETRY NOT NULL
  ,[rliegenschaft] BIGINT NOT NULL
)
;
-- SZ_Freienbach2035_20180622.Gemeindeinformationen.ObjektinformationGeom
CREATE TABLE interlis_no_ladm.objektinformationgeom (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for interlis_no_ladm.t_ili2db_seq)
  ,[geometrie] GEOMETRY NOT NULL
  ,[robjektinformation] BIGINT NOT NULL
)
;
CREATE TABLE interlis_no_ladm.T_ILI2DB_BASKET (
  [T_Id] BIGINT PRIMARY KEY
  ,[dataset] BIGINT NULL
  ,[topic] VARCHAR(200) NOT NULL
  ,[T_Ili_Tid] VARCHAR(200) NULL
  ,[attachmentKey] VARCHAR(200) NOT NULL
  ,[domains] VARCHAR(1024) NULL
)
;
CREATE TABLE interlis_no_ladm.T_ILI2DB_DATASET (
  [T_Id] BIGINT PRIMARY KEY
  ,[datasetName] VARCHAR(200) NULL
)
;
CREATE TABLE interlis_no_ladm.T_ILI2DB_INHERITANCE (
  [thisClass] VARCHAR(1024) PRIMARY KEY
  ,[baseClass] VARCHAR(1024) NULL
)
;
CREATE TABLE interlis_no_ladm.T_ILI2DB_SETTINGS (
  [tag] VARCHAR(60) PRIMARY KEY
  ,[setting] VARCHAR(1024) NULL
)
;
CREATE TABLE interlis_no_ladm.T_ILI2DB_TRAFO (
  [iliname] VARCHAR(1024) NOT NULL
  ,[tag] VARCHAR(1024) NOT NULL
  ,[setting] VARCHAR(1024) NOT NULL
)
;
CREATE TABLE interlis_no_ladm.T_ILI2DB_MODEL (
  [filename] VARCHAR(250) NOT NULL
  ,[iliversion] VARCHAR(3) NOT NULL
  ,[modelName] VARCHAR(400) NOT NULL
  ,[content] VARCHAR(MAX) NOT NULL
  ,[importDate] DATETIME NOT NULL
  ,PRIMARY KEY (modelName,iliversion)
)
;
CREATE TABLE interlis_no_ladm.art (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for interlis_no_ladm.t_ili2db_seq)
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
CREATE TABLE interlis_no_ladm.ortsteil (
  [T_Id] BIGINT PRIMARY KEY DEFAULT (next value for interlis_no_ladm.t_ili2db_seq)
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
CREATE TABLE interlis_no_ladm.T_ILI2DB_CLASSNAME (
  [IliName] VARCHAR(1024) PRIMARY KEY
  ,[SqlName] VARCHAR(1024) NOT NULL
)
;
CREATE TABLE interlis_no_ladm.T_ILI2DB_ATTRNAME (
  [IliName] VARCHAR(1024) NOT NULL
  ,[SqlName] VARCHAR(1024) NOT NULL
  ,[ColOwner] VARCHAR(1024) NOT NULL
  ,[Target] VARCHAR(1024) NULL
  ,PRIMARY KEY (ColOwner,SqlName)
)
;
CREATE TABLE interlis_no_ladm.T_ILI2DB_COLUMN_PROP (
  [tablename] VARCHAR(255) NOT NULL
  ,[subtype] VARCHAR(255) NULL
  ,[columnname] VARCHAR(255) NOT NULL
  ,[tag] VARCHAR(1024) NOT NULL
  ,[setting] VARCHAR(1024) NOT NULL
)
;
CREATE TABLE interlis_no_ladm.T_ILI2DB_TABLE_PROP (
  [tablename] VARCHAR(255) NOT NULL
  ,[tag] VARCHAR(1024) NOT NULL
  ,[setting] VARCHAR(1024) NOT NULL
)
;
CREATE TABLE interlis_no_ladm.T_ILI2DB_META_ATTRS (
  [ilielement] VARCHAR(255) NOT NULL
  ,[attr_name] VARCHAR(1024) NOT NULL
  ,[attr_value] VARCHAR(1024) NOT NULL
)
;
ALTER TABLE interlis_no_ladm.datei ADD CONSTRAINT datei_objektinformation_dateien_fkey FOREIGN KEY ( objektinformation_dateien ) REFERENCES interlis_no_ladm.objektinformation;
ALTER TABLE interlis_no_ladm.liegenschaft ADD CONSTRAINT liegenschaft_art_fkey FOREIGN KEY ( art ) REFERENCES interlis_no_ladm.art;
ALTER TABLE interlis_no_ladm.liegenschaft ADD CONSTRAINT liegenschaft_ortsteil_fkey FOREIGN KEY ( ortsteil ) REFERENCES interlis_no_ladm.ortsteil;
ALTER TABLE interlis_no_ladm.liegenschaft ADD CONSTRAINT liegenschaft_flaeche_check CHECK( flaeche BETWEEN 0 AND 999999);
ALTER TABLE interlis_no_ladm.liegenschaftgeom ADD CONSTRAINT liegenschaftgeom_rliegenschaft_fkey FOREIGN KEY ( rliegenschaft ) REFERENCES interlis_no_ladm.liegenschaft;
ALTER TABLE interlis_no_ladm.objektinformationgeom ADD CONSTRAINT objektinformationgeom_robjektinformation_fkey FOREIGN KEY ( robjektinformation ) REFERENCES interlis_no_ladm.objektinformation;
ALTER TABLE interlis_no_ladm.T_ILI2DB_BASKET ADD CONSTRAINT T_ILI2DB_BASKET_dataset_fkey FOREIGN KEY ( dataset ) REFERENCES interlis_no_ladm.T_ILI2DB_DATASET;
CREATE UNIQUE INDEX T_ILI2DB_DATASET_datasetName_key ON interlis_no_ladm.T_ILI2DB_DATASET (datasetName) WHERE  datasetName is not null
;
CREATE UNIQUE INDEX T_ILI2DB_MODEL_modelName_iliversion_key ON interlis_no_ladm.T_ILI2DB_MODEL (modelName,iliversion) WHERE  modelName is not null AND iliversion is not null
;
CREATE UNIQUE INDEX T_ILI2DB_ATTRNAME_ColOwner_SqlName_key ON interlis_no_ladm.T_ILI2DB_ATTRNAME (ColOwner,SqlName) WHERE  ColOwner is not null AND SqlName is not null
;
INSERT INTO interlis_no_ladm.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom','liegenschaft_liegenschaftgeom');
INSERT INTO interlis_no_ladm.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.LiegenschaftGeom','liegenschaftgeom');
INSERT INTO interlis_no_ladm.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.ObjektinformationGeom','objektinformationgeom');
INSERT INTO interlis_no_ladm.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('SZ_Freienbach2035_20180622.Datei','datei');
INSERT INTO interlis_no_ladm.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Ortsteil','ortsteil');
INSERT INTO interlis_no_ladm.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Art','art');
INSERT INTO interlis_no_ladm.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation','objektinformation');
INSERT INTO interlis_no_ladm.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft','liegenschaft');
INSERT INTO interlis_no_ladm.T_ILI2DB_CLASSNAME (IliName,SqlName) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom','objektinformation_objektinformationgeom');
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.geaendertVon','geaendertvon','objektinformation',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.ObjektinformationGeom.Geometrie','geometrie','objektinformationgeom',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.erstelltVon','erstelltvon','objektinformation',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Nutzung','nutzung','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.erstelltAm','erstelltam','objektinformation',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.geaendertAm','geaendertam','objektinformation',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Gebaeudeart','gebaeudeart','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Dateien','objektinformation_dateien','datei','objektinformation');
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.LiegenschaftGeom.Geometrie','geometrie','liegenschaftgeom',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.istBauland','istbauland','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Kennung','kennung','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.erstelltVon','erstelltvon','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Nummer','nummer','objektinformation',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Name','aname','objektinformation',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.naechsteSchritte','naechsteschritte','objektinformation',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Ortsteil','ortsteil','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.GrundstueckNr','grundstuecknr','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.erstelltAm','erstelltam','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.geaendertAm','geaendertam','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom.rLiegenschaft','rliegenschaft','liegenschaftgeom','liegenschaft');
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.geaendertVon','geaendertvon','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Art','art','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Beschrieb','beschrieb','objektinformation',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.ZonennameKurz','zonennamekurz','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Adresse','adresse','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Bezeichnung','bezeichnung','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom.rObjektinformation','robjektinformation','objektinformationgeom','objektinformation');
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Datei.Inhalt','inhalt','datei',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Flaeche','flaeche','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Datei.Name','aname','datei',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_ATTRNAME (IliName,SqlName,ColOwner,Target) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Bemerkung','bemerkung','liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom','ch.ehi.ili2db.inheritance','embedded');
INSERT INTO interlis_no_ladm.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.LiegenschaftGeom','ch.ehi.ili2db.inheritance','newAndSubClass');
INSERT INTO interlis_no_ladm.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.ObjektinformationGeom','ch.ehi.ili2db.inheritance','newAndSubClass');
INSERT INTO interlis_no_ladm.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('SZ_Freienbach2035_20180622.Datei','ch.ehi.ili2db.inheritance','newAndSubClass');
INSERT INTO interlis_no_ladm.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation','ch.ehi.ili2db.inheritance','newAndSubClass');
INSERT INTO interlis_no_ladm.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft','ch.ehi.ili2db.inheritance','newAndSubClass');
INSERT INTO interlis_no_ladm.T_ILI2DB_TRAFO (iliname,tag,setting) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom','ch.ehi.ili2db.inheritance','embedded');
INSERT INTO interlis_no_ladm.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.LiegenschaftGeom',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('SZ_Freienbach2035_20180622.Datei',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.ObjektinformationGeom',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_INHERITANCE (thisClass,baseClass) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom',NULL);
INSERT INTO interlis_no_ladm.art (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Eigentum',0,'Eigentum','0',NULL,'SZ_Freienbach2035_20180622.Gemeindeinformationen.Art',NULL);
INSERT INTO interlis_no_ladm.art (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Baurecht_Miete_Pacht',1,'Baurecht Miete Pacht','0',NULL,'SZ_Freienbach2035_20180622.Gemeindeinformationen.Art',NULL);
INSERT INTO interlis_no_ladm.ortsteil (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Pfaeffikon',0,'Pfaeffikon','0',NULL,'SZ_Freienbach2035_20180622.Gemeindeinformationen.Ortsteil',NULL);
INSERT INTO interlis_no_ladm.ortsteil (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Freienbach',1,'Freienbach','0',NULL,'SZ_Freienbach2035_20180622.Gemeindeinformationen.Ortsteil',NULL);
INSERT INTO interlis_no_ladm.ortsteil (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Baech',2,'Baech','0',NULL,'SZ_Freienbach2035_20180622.Gemeindeinformationen.Ortsteil',NULL);
INSERT INTO interlis_no_ladm.ortsteil (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Wilen',3,'Wilen','0',NULL,'SZ_Freienbach2035_20180622.Gemeindeinformationen.Ortsteil',NULL);
INSERT INTO interlis_no_ladm.ortsteil (seq,iliCode,itfCode,dispName,inactive,description,thisClass,baseClass) VALUES (NULL,'Hurden',4,'Hurden','0',NULL,'SZ_Freienbach2035_20180622.Gemeindeinformationen.Ortsteil',NULL);
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('objektinformationgeom',NULL,'geometrie','ch.ehi.ili2db.coordDimension','2');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('objektinformationgeom',NULL,'geometrie','ch.ehi.ili2db.c1Max','2719000.000');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('objektinformationgeom',NULL,'geometrie','ch.ehi.ili2db.c2Max','1232000.000');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('objektinformationgeom',NULL,'geometrie','ch.ehi.ili2db.geomType','POLYGON');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('objektinformationgeom',NULL,'geometrie','ch.ehi.ili2db.c1Min','2672000.000');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('objektinformationgeom',NULL,'geometrie','ch.ehi.ili2db.c2Min','1193000.000');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('objektinformationgeom',NULL,'geometrie','ch.ehi.ili2db.srid','3116');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('liegenschaft',NULL,'art','ch.ehi.ili2db.foreignKey','art');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('liegenschaft',NULL,'ortsteil','ch.ehi.ili2db.foreignKey','ortsteil');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('datei',NULL,'objektinformation_dateien','ch.ehi.ili2db.foreignKey','objektinformation');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('objektinformation',NULL,'naechsteschritte','ch.ehi.ili2db.textKind','MTEXT');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('objektinformationgeom',NULL,'robjektinformation','ch.ehi.ili2db.foreignKey','objektinformation');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('liegenschaftgeom',NULL,'geometrie','ch.ehi.ili2db.coordDimension','2');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('liegenschaftgeom',NULL,'geometrie','ch.ehi.ili2db.c1Max','2719000.000');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('liegenschaftgeom',NULL,'geometrie','ch.ehi.ili2db.c2Max','1232000.000');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('liegenschaftgeom',NULL,'geometrie','ch.ehi.ili2db.geomType','POLYGON');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('liegenschaftgeom',NULL,'geometrie','ch.ehi.ili2db.c1Min','2672000.000');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('liegenschaftgeom',NULL,'geometrie','ch.ehi.ili2db.c2Min','1193000.000');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('liegenschaftgeom',NULL,'geometrie','ch.ehi.ili2db.srid','3116');
INSERT INTO interlis_no_ladm.T_ILI2DB_COLUMN_PROP (tablename,subtype,columnname,tag,setting) VALUES ('liegenschaftgeom',NULL,'rliegenschaft','ch.ehi.ili2db.foreignKey','liegenschaft');
INSERT INTO interlis_no_ladm.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('art','ch.ehi.ili2db.tableKind','ENUM');
INSERT INTO interlis_no_ladm.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('ortsteil','ch.ehi.ili2db.tableKind','ENUM');
INSERT INTO interlis_no_ladm.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('liegenschaftgeom','ch.ehi.ili2db.tableKind','CLASS');
INSERT INTO interlis_no_ladm.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('datei','ch.ehi.ili2db.tableKind','STRUCTURE');
INSERT INTO interlis_no_ladm.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('objektinformation','ch.ehi.ili2db.tableKind','CLASS');
INSERT INTO interlis_no_ladm.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('objektinformationgeom','ch.ehi.ili2db.tableKind','CLASS');
INSERT INTO interlis_no_ladm.T_ILI2DB_TABLE_PROP (tablename,tag,setting) VALUES ('liegenschaft','ch.ehi.ili2db.tableKind','CLASS');
INSERT INTO interlis_no_ladm.T_ILI2DB_MODEL (filename,iliversion,modelName,content,importDate) VALUES ('interlis_no_ladm.ili','2.3','SZ_Freienbach2035_20180622','INTERLIS 2.3;
!!==============================================================================
!!@ File                = "SZ_Freienbach2035_2018-06-22.ili";
!!@ Title               = "Freienbach 2035";
!!@ shortDescription    = "''Freienbach 2035'' ist der Projektname für die Neuausrichtung der Gemeinde Freienbach. Dieses Modell beschreibt die Struktur der Daten, die auf der Infrastruktur des Kantons erfasst werden";
!!@ Issuer              = "http://www.sz.ch/avg";
!!@ technicalContact    = "mailto:geoportal@sz.ch";
!!@ furtherInformation  = "https://www.sz.ch";
!!@ kGeoiV_ID           = "- - -";
!!@ kGeoiV_Code         = "- - -";
!!@ Themennummer        = "A110";
!!@ iliCompilerVersion  = "4.7.11-20181209";
!!------------------------------------------------------------------------------
!! Todo: - - -
!!------------------------------------------------------------------------------
!! Version    | wer | Änderung
!!------------------------------------------------------------------------------
!! 2018-12-12 | Vd  | Attribut naechsteSchritte: neu MTEXT,Laenge: 1500 Zeichen
!! 2018-06-22 | Kep | Erstfassung
!!==============================================================================
MODEL SZ_Freienbach2035_20180622 (de)
  AT "http://models.geo.sz.ch"
  VERSION "2018-06-22" =

  DOMAIN
    Punkt =
      COORD 2672000.000 .. 2719000.000 [INTERLIS.m]
           ,1193000.000 .. 1232000.000 [INTERLIS.m]
           ,ROTATION 2 -> 1
    ;
    
    Einzelflaeche =
      SURFACE WITH (STRAIGHTS) VERTEX Punkt WITHOUT OVERLAPS > 0.1;

  STRUCTURE Datei =
    Name    :  MANDATORY  TEXT*100;
    Inhalt  :  MANDATORY  BLACKBOX BINARY;
  END Datei;

!!------------------------------------------------------------------------------
  TOPIC Gemeindeinformationen =
!!------------------------------------------------------------------------------
    DOMAIN
      Art = (
        Eigentum
       ,Baurecht_Miete_Pacht
      );

      Ortsteil = (
        Pfaeffikon
       ,Freienbach
       ,Baech
       ,Wilen
       ,Hurden
      );

    CLASS Liegenschaft =
      Kennung        :  MANDATORY  TEXT*25;    !! ein eindeutiger Fachschlüssel ("Eintragsnummer")
      erstelltVon    :  MANDATORY  TEXT*100;
      erstelltAm     :  MANDATORY  INTERLIS.XMLDate;
      geaendertVon   :  MANDATORY  TEXT*100;
      geaendertAm    :  MANDATORY  INTERLIS.XMLDate;
      Art            :  MANDATORY  Art;
      GrundstueckNr  :  MANDATORY  TEXT*50;    !! Einzeleinträge; kommagetrennt zu erfassen
      Bezeichnung    :  MANDATORY  TEXT*250;
      Adresse        :  MANDATORY  TEXT*50;
      Ortsteil       :  MANDATORY  Ortsteil;
      Nutzung        :  MANDATORY  TEXT*250;
      istBauland     :  MANDATORY  BOOLEAN;
      Gebaeudeart    :             TEXT*250;
      Bemerkung      :             TEXT*250;
      Flaeche        :             0 .. 999999;
      ZonennameKurz  :  MANDATORY  TEXT*10;
      UNIQUE Kennung;
    END Liegenschaft;

    CLASS Objektinformation =
      Nummer            :  MANDATORY  TEXT*10;
      erstelltVon       :  MANDATORY  TEXT*100;
      erstelltAm        :  MANDATORY  INTERLIS.XMLDate;
      geaendertVon      :  MANDATORY  TEXT*100;
      geaendertAm       :  MANDATORY  INTERLIS.XMLDate;
      Name              :  MANDATORY  TEXT*50;
      Beschrieb         :  MANDATORY  TEXT*250;
      naechsteSchritte  :             MTEXT*1500;
      Dateien           :             BAG {0..*} OF Datei;
      UNIQUE Nummer;
    END Objektinformation;

    CLASS LiegenschaftGeom =
      Geometrie         :  MANDATORY  Einzelflaeche;
    END LiegenschaftGeom;

    CLASS ObjektinformationGeom =
      Geometrie         :  MANDATORY  Einzelflaeche;
    END ObjektinformationGeom;

    ASSOCIATION Liegenschaft_LiegenschaftGeom =
      rLiegenschaft  -- {1}     Liegenschaft;
      rGeometrie     -- {1..*}  LiegenschaftGeom;
    END Liegenschaft_LiegenschaftGeom;

    ASSOCIATION Objektinformation_ObjektinformationGeom =
      rObjektinformation  -- {1}     Objektinformation;
      rGeometrie          -- {0..*}  ObjektinformationGeom;
    END Objektinformation_ObjektinformationGeom;

  END Gemeindeinformationen;

END SZ_Freienbach2035_20180622.','2020-05-28 12:10:44.062');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.createMetaInfo','True');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.beautifyEnumDispName','underscore');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.arrayTrafo','coalesce');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.localisedTrafo','expand');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.numericCheckConstraints','create');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.sender','ili2mssql-4.4.3-SNAPSHOT-89cd285dadc9d002f6d35791956b957bd2b419d1');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.createForeignKey','yes');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.sqlgen.createGeomIndex','True');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.defaultSrsAuthority','EPSG');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.defaultSrsCode','3116');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.uuidDefaultValue','NEWID()');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.StrokeArcs','enable');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.multiLineTrafo','coalesce');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.interlis.ili2c.ilidirs','E:\test_asistente\interlis_no_ladm');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.createForeignKeyIndex','yes');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.jsonTrafo','coalesce');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.createEnumDefs','multiTableWithId');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.uniqueConstraints','create');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.maxSqlNameLength','60');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.inheritanceTrafo','smart2');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.catalogueRefTrafo','coalesce');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.multiPointTrafo','coalesce');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.multiSurfaceTrafo','coalesce');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.multilingualTrafo','expand');
INSERT INTO interlis_no_ladm.T_ILI2DB_SETTINGS (tag,setting) VALUES ('ch.ehi.ili2db.modelsTabModelnameColSize','400');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.LiegenschaftGeom.Geometrie','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.LiegenschaftGeom.Geometrie','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.ObjektinformationGeom.Geometrie','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.ObjektinformationGeom.Geometrie','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.geaendertVon','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.geaendertVon','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Bezeichnung','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Bezeichnung','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.istBauland','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.istBauland','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom.rLiegenschaft','ili2db.ili.assocCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom.rLiegenschaft','ili2db.ili.assocCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom.rLiegenschaft','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Ortsteil','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Ortsteil','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Art','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Art','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Name','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Name','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.erstelltVon','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.erstelltVon','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Nutzung','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Nutzung','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Gebaeudeart','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Gebaeudeart','ili2db.ili.attrCardinalityMin','0');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622','furtherInformation','https://www.sz.ch');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622','Issuer','http://www.sz.ch/avg');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622','Themennummer','A110');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622','kGeoiV_Code','- - -');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622','Title','Freienbach 2035');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622','kGeoiV_ID','- - -');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622','iliCompilerVersion','4.7.11-20181209');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622','shortDescription','Freienbach 2035 ist der Projektname für die Neuausrichtung der Gemeinde Freienbach. Dieses Modell beschreibt die Struktur der Daten, die auf der Infrastruktur des Kantons erfasst werden');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622','File','SZ_Freienbach2035_2018-06-22.ili');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622','technicalContact','mailto:geoportal@sz.ch');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.geaendertAm','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.geaendertAm','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Adresse','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Adresse','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Flaeche','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Flaeche','ili2db.ili.attrCardinalityMin','0');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom.rObjektinformation','ili2db.ili.assocCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom.rObjektinformation','ili2db.ili.assocCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom.rObjektinformation','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Nummer','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Nummer','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.erstelltAm','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.erstelltAm','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Kennung','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Kennung','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Beschrieb','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Beschrieb','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Datei.Inhalt','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Datei.Inhalt','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.erstelltAm','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.erstelltAm','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.geaendertVon','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.geaendertVon','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom.rGeometrie','ili2db.ili.assocCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom.rGeometrie','ili2db.ili.assocCardinalityMax','*');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom.rGeometrie','ili2db.ili.assocKind','ASSOCIATE');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.naechsteSchritte','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.naechsteSchritte','ili2db.ili.attrCardinalityMin','0');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.ZonennameKurz','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.ZonennameKurz','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.erstelltVon','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.erstelltVon','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.geaendertAm','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.geaendertAm','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Datei.Name','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Datei.Name','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Bemerkung','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Bemerkung','ili2db.ili.attrCardinalityMin','0');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.GrundstueckNr','ili2db.ili.attrCardinalityMax','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.GrundstueckNr','ili2db.ili.attrCardinalityMin','1');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Dateien','ili2db.ili.attrCardinalityMax','*');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Dateien','ili2db.ili.attrCardinalityMin','0');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom.rGeometrie','ili2db.ili.assocCardinalityMin','0');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom.rGeometrie','ili2db.ili.assocCardinalityMax','*');
INSERT INTO interlis_no_ladm.T_ILI2DB_META_ATTRS (ilielement,attr_name,attr_value) VALUES ('SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom.rGeometrie','ili2db.ili.assocKind','ASSOCIATE');
