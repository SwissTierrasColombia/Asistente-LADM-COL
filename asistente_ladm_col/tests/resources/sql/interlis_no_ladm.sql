--
-- PostgreSQL database dump
--

-- Dumped from database version 11.8 (Ubuntu 11.8-1.pgdg20.04+1)
-- Dumped by pg_dump version 12.3 (Ubuntu 12.3-1.pgdg20.04+1)

-- Started on 2020-07-15 12:29:17 -05

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 9 (class 2615 OID 334996)
-- Name: interlis_no_ladm; Type: SCHEMA; Schema: -; Owner: postgres
--

DROP SCHEMA IF EXISTS interlis_no_ladm CASCADE;
CREATE SCHEMA interlis_no_ladm;


ALTER SCHEMA interlis_no_ladm OWNER TO postgres;

--
-- TOC entry 1942 (class 1259 OID 334997)
-- Name: t_ili2db_seq; Type: SEQUENCE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE SEQUENCE interlis_no_ladm.t_ili2db_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE interlis_no_ladm.t_ili2db_seq OWNER TO postgres;

SET default_tablespace = '';

--
-- TOC entry 1943 (class 1259 OID 334999)
-- Name: art; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.art (
    t_id bigint DEFAULT nextval('interlis_no_ladm.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_no_ladm.art OWNER TO postgres;

--
-- TOC entry 1944 (class 1259 OID 335006)
-- Name: datei; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.datei (
    t_id bigint DEFAULT nextval('interlis_no_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    aname character varying(100) NOT NULL,
    inhalt bytea NOT NULL,
    objektinformation_dateien bigint
);


ALTER TABLE interlis_no_ladm.datei OWNER TO postgres;

--
-- TOC entry 1945 (class 1259 OID 335013)
-- Name: liegenschaft; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.liegenschaft (
    t_id bigint DEFAULT nextval('interlis_no_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    kennung character varying(25) NOT NULL,
    erstelltvon character varying(100) NOT NULL,
    erstelltam date NOT NULL,
    geaendertvon character varying(100) NOT NULL,
    geaendertam date NOT NULL,
    art bigint NOT NULL,
    grundstuecknr character varying(50) NOT NULL,
    bezeichnung character varying(250) NOT NULL,
    adresse character varying(50) NOT NULL,
    ortsteil bigint NOT NULL,
    nutzung character varying(250) NOT NULL,
    istbauland boolean NOT NULL,
    gebaeudeart character varying(250),
    bemerkung character varying(250),
    flaeche integer,
    zonennamekurz character varying(10) NOT NULL,
    CONSTRAINT liegenschaft_flaeche_check CHECK (((flaeche >= 0) AND (flaeche <= 999999)))
);


ALTER TABLE interlis_no_ladm.liegenschaft OWNER TO postgres;

--
-- TOC entry 1946 (class 1259 OID 335021)
-- Name: liegenschaftgeom; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.liegenschaftgeom (
    t_id bigint DEFAULT nextval('interlis_no_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    geometrie public.geometry(Polygon,4326) NOT NULL,
    rliegenschaft bigint NOT NULL
);


ALTER TABLE interlis_no_ladm.liegenschaftgeom OWNER TO postgres;

--
-- TOC entry 1947 (class 1259 OID 335028)
-- Name: objektinformation; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.objektinformation (
    t_id bigint DEFAULT nextval('interlis_no_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    nummer character varying(10) NOT NULL,
    erstelltvon character varying(100) NOT NULL,
    erstelltam date NOT NULL,
    geaendertvon character varying(100) NOT NULL,
    geaendertam date NOT NULL,
    aname character varying(50) NOT NULL,
    beschrieb character varying(250) NOT NULL,
    naechsteschritte character varying(1500)
);


ALTER TABLE interlis_no_ladm.objektinformation OWNER TO postgres;

--
-- TOC entry 1948 (class 1259 OID 335035)
-- Name: objektinformationgeom; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.objektinformationgeom (
    t_id bigint DEFAULT nextval('interlis_no_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    geometrie public.geometry(Polygon,4326) NOT NULL,
    robjektinformation bigint NOT NULL
);


ALTER TABLE interlis_no_ladm.objektinformationgeom OWNER TO postgres;

--
-- TOC entry 1949 (class 1259 OID 335042)
-- Name: ortsteil; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.ortsteil (
    t_id bigint DEFAULT nextval('interlis_no_ladm.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_no_ladm.ortsteil OWNER TO postgres;

--
-- TOC entry 1950 (class 1259 OID 335049)
-- Name: t_ili2db_attrname; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.t_ili2db_attrname (
    iliname character varying(1024) NOT NULL,
    sqlname character varying(1024) NOT NULL,
    colowner character varying(1024) NOT NULL,
    target character varying(1024)
);


ALTER TABLE interlis_no_ladm.t_ili2db_attrname OWNER TO postgres;

--
-- TOC entry 1951 (class 1259 OID 335055)
-- Name: t_ili2db_basket; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.t_ili2db_basket (
    t_id bigint NOT NULL,
    dataset bigint,
    topic character varying(200) NOT NULL,
    t_ili_tid character varying(200),
    attachmentkey character varying(200) NOT NULL,
    domains character varying(1024)
);


ALTER TABLE interlis_no_ladm.t_ili2db_basket OWNER TO postgres;

--
-- TOC entry 1952 (class 1259 OID 335061)
-- Name: t_ili2db_classname; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.t_ili2db_classname (
    iliname character varying(1024) NOT NULL,
    sqlname character varying(1024) NOT NULL
);


ALTER TABLE interlis_no_ladm.t_ili2db_classname OWNER TO postgres;

--
-- TOC entry 1953 (class 1259 OID 335067)
-- Name: t_ili2db_column_prop; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.t_ili2db_column_prop (
    tablename character varying(255) NOT NULL,
    subtype character varying(255),
    columnname character varying(255) NOT NULL,
    tag character varying(1024) NOT NULL,
    setting character varying(1024) NOT NULL
);


ALTER TABLE interlis_no_ladm.t_ili2db_column_prop OWNER TO postgres;

--
-- TOC entry 1954 (class 1259 OID 335073)
-- Name: t_ili2db_dataset; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.t_ili2db_dataset (
    t_id bigint NOT NULL,
    datasetname character varying(200)
);


ALTER TABLE interlis_no_ladm.t_ili2db_dataset OWNER TO postgres;

--
-- TOC entry 1955 (class 1259 OID 335076)
-- Name: t_ili2db_inheritance; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.t_ili2db_inheritance (
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024)
);


ALTER TABLE interlis_no_ladm.t_ili2db_inheritance OWNER TO postgres;

--
-- TOC entry 1956 (class 1259 OID 335082)
-- Name: t_ili2db_meta_attrs; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.t_ili2db_meta_attrs (
    ilielement character varying(255) NOT NULL,
    attr_name character varying(1024) NOT NULL,
    attr_value character varying(1024) NOT NULL
);


ALTER TABLE interlis_no_ladm.t_ili2db_meta_attrs OWNER TO postgres;

--
-- TOC entry 1957 (class 1259 OID 335088)
-- Name: t_ili2db_model; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.t_ili2db_model (
    filename character varying(250) NOT NULL,
    iliversion character varying(3) NOT NULL,
    modelname text NOT NULL,
    content text NOT NULL,
    importdate timestamp without time zone NOT NULL
);


ALTER TABLE interlis_no_ladm.t_ili2db_model OWNER TO postgres;

--
-- TOC entry 1958 (class 1259 OID 335094)
-- Name: t_ili2db_settings; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.t_ili2db_settings (
    tag character varying(60) NOT NULL,
    setting character varying(1024)
);


ALTER TABLE interlis_no_ladm.t_ili2db_settings OWNER TO postgres;

--
-- TOC entry 1959 (class 1259 OID 335100)
-- Name: t_ili2db_table_prop; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.t_ili2db_table_prop (
    tablename character varying(255) NOT NULL,
    tag character varying(1024) NOT NULL,
    setting character varying(1024) NOT NULL
);


ALTER TABLE interlis_no_ladm.t_ili2db_table_prop OWNER TO postgres;

--
-- TOC entry 1960 (class 1259 OID 335106)
-- Name: t_ili2db_trafo; Type: TABLE; Schema: interlis_no_ladm; Owner: postgres
--

CREATE TABLE interlis_no_ladm.t_ili2db_trafo (
    iliname character varying(1024) NOT NULL,
    tag character varying(1024) NOT NULL,
    setting character varying(1024) NOT NULL
);


ALTER TABLE interlis_no_ladm.t_ili2db_trafo OWNER TO postgres;

--
-- TOC entry 10377 (class 0 OID 334999)
-- Dependencies: 1943
-- Data for Name: art; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.art (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
1	SZ_Freienbach2035_20180622.Gemeindeinformationen.Art	\N	0	Eigentum	\N	f	Eigentum	\N
2	SZ_Freienbach2035_20180622.Gemeindeinformationen.Art	\N	1	Baurecht_Miete_Pacht	\N	f	Baurecht Miete Pacht	\N
\.


--
-- TOC entry 10378 (class 0 OID 335006)
-- Dependencies: 1944
-- Data for Name: datei; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.datei (t_id, t_seq, aname, inhalt, objektinformation_dateien) FROM stdin;
\.


--
-- TOC entry 10379 (class 0 OID 335013)
-- Dependencies: 1945
-- Data for Name: liegenschaft; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.liegenschaft (t_id, t_ili_tid, kennung, erstelltvon, erstelltam, geaendertvon, geaendertam, art, grundstuecknr, bezeichnung, adresse, ortsteil, nutzung, istbauland, gebaeudeart, bemerkung, flaeche, zonennamekurz) FROM stdin;
\.


--
-- TOC entry 10380 (class 0 OID 335021)
-- Dependencies: 1946
-- Data for Name: liegenschaftgeom; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.liegenschaftgeom (t_id, t_ili_tid, geometrie, rliegenschaft) FROM stdin;
\.


--
-- TOC entry 10381 (class 0 OID 335028)
-- Dependencies: 1947
-- Data for Name: objektinformation; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.objektinformation (t_id, t_ili_tid, nummer, erstelltvon, erstelltam, geaendertvon, geaendertam, aname, beschrieb, naechsteschritte) FROM stdin;
\.


--
-- TOC entry 10382 (class 0 OID 335035)
-- Dependencies: 1948
-- Data for Name: objektinformationgeom; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.objektinformationgeom (t_id, t_ili_tid, geometrie, robjektinformation) FROM stdin;
\.


--
-- TOC entry 10383 (class 0 OID 335042)
-- Dependencies: 1949
-- Data for Name: ortsteil; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.ortsteil (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
3	SZ_Freienbach2035_20180622.Gemeindeinformationen.Ortsteil	\N	0	Pfaeffikon	\N	f	Pfaeffikon	\N
4	SZ_Freienbach2035_20180622.Gemeindeinformationen.Ortsteil	\N	1	Freienbach	\N	f	Freienbach	\N
5	SZ_Freienbach2035_20180622.Gemeindeinformationen.Ortsteil	\N	2	Baech	\N	f	Baech	\N
6	SZ_Freienbach2035_20180622.Gemeindeinformationen.Ortsteil	\N	3	Wilen	\N	f	Wilen	\N
7	SZ_Freienbach2035_20180622.Gemeindeinformationen.Ortsteil	\N	4	Hurden	\N	f	Hurden	\N
\.


--
-- TOC entry 10384 (class 0 OID 335049)
-- Dependencies: 1950
-- Data for Name: t_ili2db_attrname; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.t_ili2db_attrname (iliname, sqlname, colowner, target) FROM stdin;
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.geaendertVon	geaendertvon	objektinformation	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.ObjektinformationGeom.Geometrie	geometrie	objektinformationgeom	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.erstelltVon	erstelltvon	objektinformation	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Nutzung	nutzung	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.erstelltAm	erstelltam	objektinformation	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.geaendertAm	geaendertam	objektinformation	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Gebaeudeart	gebaeudeart	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Dateien	objektinformation_dateien	datei	objektinformation
SZ_Freienbach2035_20180622.Gemeindeinformationen.LiegenschaftGeom.Geometrie	geometrie	liegenschaftgeom	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.istBauland	istbauland	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Kennung	kennung	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.erstelltVon	erstelltvon	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Nummer	nummer	objektinformation	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Name	aname	objektinformation	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.naechsteSchritte	naechsteschritte	objektinformation	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Ortsteil	ortsteil	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.GrundstueckNr	grundstuecknr	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.erstelltAm	erstelltam	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.geaendertAm	geaendertam	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom.rLiegenschaft	rliegenschaft	liegenschaftgeom	liegenschaft
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.geaendertVon	geaendertvon	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Art	art	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation.Beschrieb	beschrieb	objektinformation	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.ZonennameKurz	zonennamekurz	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Adresse	adresse	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Bezeichnung	bezeichnung	liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom.rObjektinformation	robjektinformation	objektinformationgeom	objektinformation
SZ_Freienbach2035_20180622.Datei.Inhalt	inhalt	datei	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Flaeche	flaeche	liegenschaft	\N
SZ_Freienbach2035_20180622.Datei.Name	aname	datei	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft.Bemerkung	bemerkung	liegenschaft	\N
\.


--
-- TOC entry 10385 (class 0 OID 335055)
-- Dependencies: 1951
-- Data for Name: t_ili2db_basket; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.t_ili2db_basket (t_id, dataset, topic, t_ili_tid, attachmentkey, domains) FROM stdin;
\.


--
-- TOC entry 10386 (class 0 OID 335061)
-- Dependencies: 1952
-- Data for Name: t_ili2db_classname; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.t_ili2db_classname (iliname, sqlname) FROM stdin;
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom	liegenschaft_liegenschaftgeom
SZ_Freienbach2035_20180622.Gemeindeinformationen.LiegenschaftGeom	liegenschaftgeom
SZ_Freienbach2035_20180622.Gemeindeinformationen.ObjektinformationGeom	objektinformationgeom
SZ_Freienbach2035_20180622.Datei	datei
SZ_Freienbach2035_20180622.Gemeindeinformationen.Ortsteil	ortsteil
SZ_Freienbach2035_20180622.Gemeindeinformationen.Art	art
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation	objektinformation
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft	liegenschaft
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom	objektinformation_objektinformationgeom
\.


--
-- TOC entry 10387 (class 0 OID 335067)
-- Dependencies: 1953
-- Data for Name: t_ili2db_column_prop; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.t_ili2db_column_prop (tablename, subtype, columnname, tag, setting) FROM stdin;
objektinformationgeom	\N	geometrie	ch.ehi.ili2db.coordDimension	2
objektinformationgeom	\N	geometrie	ch.ehi.ili2db.c1Max	2719000.000
objektinformationgeom	\N	geometrie	ch.ehi.ili2db.c2Max	1232000.000
objektinformationgeom	\N	geometrie	ch.ehi.ili2db.geomType	POLYGON
objektinformationgeom	\N	geometrie	ch.ehi.ili2db.c1Min	2672000.000
objektinformationgeom	\N	geometrie	ch.ehi.ili2db.c2Min	1193000.000
objektinformationgeom	\N	geometrie	ch.ehi.ili2db.srid	4326
liegenschaft	\N	art	ch.ehi.ili2db.foreignKey	art
liegenschaft	\N	ortsteil	ch.ehi.ili2db.foreignKey	ortsteil
datei	\N	objektinformation_dateien	ch.ehi.ili2db.foreignKey	objektinformation
objektinformation	\N	naechsteschritte	ch.ehi.ili2db.textKind	MTEXT
objektinformationgeom	\N	robjektinformation	ch.ehi.ili2db.foreignKey	objektinformation
liegenschaftgeom	\N	geometrie	ch.ehi.ili2db.coordDimension	2
liegenschaftgeom	\N	geometrie	ch.ehi.ili2db.c1Max	2719000.000
liegenschaftgeom	\N	geometrie	ch.ehi.ili2db.c2Max	1232000.000
liegenschaftgeom	\N	geometrie	ch.ehi.ili2db.geomType	POLYGON
liegenschaftgeom	\N	geometrie	ch.ehi.ili2db.c1Min	2672000.000
liegenschaftgeom	\N	geometrie	ch.ehi.ili2db.c2Min	1193000.000
liegenschaftgeom	\N	geometrie	ch.ehi.ili2db.srid	4326
liegenschaftgeom	\N	rliegenschaft	ch.ehi.ili2db.foreignKey	liegenschaft
\.


--
-- TOC entry 10388 (class 0 OID 335073)
-- Dependencies: 1954
-- Data for Name: t_ili2db_dataset; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.t_ili2db_dataset (t_id, datasetname) FROM stdin;
\.


--
-- TOC entry 10389 (class 0 OID 335076)
-- Dependencies: 1955
-- Data for Name: t_ili2db_inheritance; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.t_ili2db_inheritance (thisclass, baseclass) FROM stdin;
SZ_Freienbach2035_20180622.Datei	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.ObjektinformationGeom	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.LiegenschaftGeom	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom	\N
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation	\N
\.


--
-- TOC entry 10390 (class 0 OID 335082)
-- Dependencies: 1956
-- Data for Name: t_ili2db_meta_attrs; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.t_ili2db_meta_attrs (ilielement, attr_name, attr_value) FROM stdin;
SZ_Freienbach2035_20180622	furtherInformation	https://www.sz.ch
SZ_Freienbach2035_20180622	Issuer	http://www.sz.ch/avg
SZ_Freienbach2035_20180622	Themennummer	A110
SZ_Freienbach2035_20180622	kGeoiV_Code	- - -
SZ_Freienbach2035_20180622	Title	Freienbach 2035
SZ_Freienbach2035_20180622	kGeoiV_ID	- - -
SZ_Freienbach2035_20180622	iliCompilerVersion	4.7.11-20181209
SZ_Freienbach2035_20180622	shortDescription	'Freienbach 2035' ist der Projektname für die Neuausrichtung der Gemeinde Freienbach. Dieses Modell beschreibt die Struktur der Daten, die auf der Infrastruktur des Kantons erfasst werden
SZ_Freienbach2035_20180622	File	SZ_Freienbach2035_2018-06-22.ili
SZ_Freienbach2035_20180622	technicalContact	mailto:geoportal@sz.ch
\.


--
-- TOC entry 10391 (class 0 OID 335088)
-- Dependencies: 1957
-- Data for Name: t_ili2db_model; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.t_ili2db_model (filename, iliversion, modelname, content, importdate) FROM stdin;
SZ_Freienbach2035_2018-06-22.ili	2.3	SZ_Freienbach2035_20180622	INTERLIS 2.3;\r\n!!==============================================================================\r\n!!@ File                = "SZ_Freienbach2035_2018-06-22.ili";\r\n!!@ Title               = "Freienbach 2035";\r\n!!@ shortDescription    = "'Freienbach 2035' ist der Projektname für die Neuausrichtung der Gemeinde Freienbach. Dieses Modell beschreibt die Struktur der Daten, die auf der Infrastruktur des Kantons erfasst werden";\r\n!!@ Issuer              = "http://www.sz.ch/avg";\r\n!!@ technicalContact    = "mailto:geoportal@sz.ch";\r\n!!@ furtherInformation  = "https://www.sz.ch";\r\n!!@ kGeoiV_ID           = "- - -";\r\n!!@ kGeoiV_Code         = "- - -";\r\n!!@ Themennummer        = "A110";\r\n!!@ iliCompilerVersion  = "4.7.11-20181209";\r\n!!------------------------------------------------------------------------------\r\n!! Todo: - - -\r\n!!------------------------------------------------------------------------------\r\n!! Version    | wer | Änderung\r\n!!------------------------------------------------------------------------------\r\n!! 2018-12-12 | Vd  | Attribut naechsteSchritte: neu MTEXT,Laenge: 1500 Zeichen\r\n!! 2018-06-22 | Kep | Erstfassung\r\n!!==============================================================================\r\nMODEL SZ_Freienbach2035_20180622 (de)\r\n  AT "http://models.geo.sz.ch"\r\n  VERSION "2018-06-22" =\r\n\r\n  DOMAIN\r\n    Punkt =\r\n      COORD 2672000.000 .. 2719000.000 [INTERLIS.m]\r\n           ,1193000.000 .. 1232000.000 [INTERLIS.m]\r\n           ,ROTATION 2 -> 1\r\n    ;\r\n    \r\n    Einzelflaeche =\r\n      SURFACE WITH (STRAIGHTS) VERTEX Punkt WITHOUT OVERLAPS > 0.1;\r\n\r\n  STRUCTURE Datei =\r\n    Name    :  MANDATORY  TEXT*100;\r\n    Inhalt  :  MANDATORY  BLACKBOX BINARY;\r\n  END Datei;\r\n\r\n!!------------------------------------------------------------------------------\r\n  TOPIC Gemeindeinformationen =\r\n!!------------------------------------------------------------------------------\r\n    DOMAIN\r\n      Art = (\r\n        Eigentum\r\n       ,Baurecht_Miete_Pacht\r\n      );\r\n\r\n      Ortsteil = (\r\n        Pfaeffikon\r\n       ,Freienbach\r\n       ,Baech\r\n       ,Wilen\r\n       ,Hurden\r\n      );\r\n\r\n    CLASS Liegenschaft =\r\n      Kennung        :  MANDATORY  TEXT*25;    !! ein eindeutiger Fachschlüssel ("Eintragsnummer")\r\n      erstelltVon    :  MANDATORY  TEXT*100;\r\n      erstelltAm     :  MANDATORY  INTERLIS.XMLDate;\r\n      geaendertVon   :  MANDATORY  TEXT*100;\r\n      geaendertAm    :  MANDATORY  INTERLIS.XMLDate;\r\n      Art            :  MANDATORY  Art;\r\n      GrundstueckNr  :  MANDATORY  TEXT*50;    !! Einzeleinträge; kommagetrennt zu erfassen\r\n      Bezeichnung    :  MANDATORY  TEXT*250;\r\n      Adresse        :  MANDATORY  TEXT*50;\r\n      Ortsteil       :  MANDATORY  Ortsteil;\r\n      Nutzung        :  MANDATORY  TEXT*250;\r\n      istBauland     :  MANDATORY  BOOLEAN;\r\n      Gebaeudeart    :             TEXT*250;\r\n      Bemerkung      :             TEXT*250;\r\n      Flaeche        :             0 .. 999999;\r\n      ZonennameKurz  :  MANDATORY  TEXT*10;\r\n      UNIQUE Kennung;\r\n    END Liegenschaft;\r\n\r\n    CLASS Objektinformation =\r\n      Nummer            :  MANDATORY  TEXT*10;\r\n      erstelltVon       :  MANDATORY  TEXT*100;\r\n      erstelltAm        :  MANDATORY  INTERLIS.XMLDate;\r\n      geaendertVon      :  MANDATORY  TEXT*100;\r\n      geaendertAm       :  MANDATORY  INTERLIS.XMLDate;\r\n      Name              :  MANDATORY  TEXT*50;\r\n      Beschrieb         :  MANDATORY  TEXT*250;\r\n      naechsteSchritte  :             MTEXT*1500;\r\n      Dateien           :             BAG {0..*} OF Datei;\r\n      UNIQUE Nummer;\r\n    END Objektinformation;\r\n\r\n    CLASS LiegenschaftGeom =\r\n      Geometrie         :  MANDATORY  Einzelflaeche;\r\n    END LiegenschaftGeom;\r\n\r\n    CLASS ObjektinformationGeom =\r\n      Geometrie         :  MANDATORY  Einzelflaeche;\r\n    END ObjektinformationGeom;\r\n\r\n    ASSOCIATION Liegenschaft_LiegenschaftGeom =\r\n      rLiegenschaft  -- {1}     Liegenschaft;\r\n      rGeometrie     -- {1..*}  LiegenschaftGeom;\r\n    END Liegenschaft_LiegenschaftGeom;\r\n\r\n    ASSOCIATION Objektinformation_ObjektinformationGeom =\r\n      rObjektinformation  -- {1}     Objektinformation;\r\n      rGeometrie          -- {0..*}  ObjektinformationGeom;\r\n    END Objektinformation_ObjektinformationGeom;\r\n\r\n  END Gemeindeinformationen;\r\n\r\nEND SZ_Freienbach2035_20180622.	2020-01-28 08:51:45.963
\.


--
-- TOC entry 10392 (class 0 OID 335094)
-- Dependencies: 1958
-- Data for Name: t_ili2db_settings; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.t_ili2db_settings (tag, setting) FROM stdin;
ch.ehi.ili2db.createMetaInfo	True
ch.ehi.ili2db.beautifyEnumDispName	underscore
ch.ehi.ili2db.arrayTrafo	coalesce
ch.ehi.ili2db.localisedTrafo	expand
ch.ehi.ili2db.numericCheckConstraints	create
ch.ehi.ili2db.sender	ili2pg-4.3.2-70c2c19de9928155e48437dedb68f5eef82896a7
ch.ehi.ili2db.createForeignKey	yes
ch.ehi.sqlgen.createGeomIndex	True
ch.ehi.ili2db.defaultSrsAuthority	EPSG
ch.ehi.ili2db.defaultSrsCode	4326
ch.ehi.ili2db.uuidDefaultValue	uuid_generate_v4()
ch.ehi.ili2db.StrokeArcs	enable
ch.ehi.ili2db.multiLineTrafo	coalesce
ch.interlis.ili2c.ilidirs	%ILI_FROM_DB;%XTF_DIR;http://models.interlis.ch/;%JAR_DIR
ch.ehi.ili2db.TidHandling	property
ch.ehi.ili2db.createForeignKeyIndex	yes
ch.ehi.ili2db.jsonTrafo	coalesce
ch.ehi.ili2db.createEnumDefs	multiTableWithId
ch.ehi.ili2db.uniqueConstraints	create
ch.ehi.ili2db.maxSqlNameLength	60
ch.ehi.ili2db.inheritanceTrafo	smart2
ch.ehi.ili2db.catalogueRefTrafo	coalesce
ch.ehi.ili2db.multiPointTrafo	coalesce
ch.ehi.ili2db.multiSurfaceTrafo	coalesce
ch.ehi.ili2db.multilingualTrafo	expand
\.


--
-- TOC entry 10393 (class 0 OID 335100)
-- Dependencies: 1959
-- Data for Name: t_ili2db_table_prop; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.t_ili2db_table_prop (tablename, tag, setting) FROM stdin;
art	ch.ehi.ili2db.tableKind	ENUM
ortsteil	ch.ehi.ili2db.tableKind	ENUM
liegenschaftgeom	ch.ehi.ili2db.tableKind	CLASS
objektinformation	ch.ehi.ili2db.tableKind	CLASS
datei	ch.ehi.ili2db.tableKind	STRUCTURE
objektinformationgeom	ch.ehi.ili2db.tableKind	CLASS
liegenschaft	ch.ehi.ili2db.tableKind	CLASS
\.


--
-- TOC entry 10394 (class 0 OID 335106)
-- Dependencies: 1960
-- Data for Name: t_ili2db_trafo; Type: TABLE DATA; Schema: interlis_no_ladm; Owner: postgres
--

COPY interlis_no_ladm.t_ili2db_trafo (iliname, tag, setting) FROM stdin;
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft_LiegenschaftGeom	ch.ehi.ili2db.inheritance	embedded
SZ_Freienbach2035_20180622.Gemeindeinformationen.LiegenschaftGeom	ch.ehi.ili2db.inheritance	newAndSubClass
SZ_Freienbach2035_20180622.Gemeindeinformationen.ObjektinformationGeom	ch.ehi.ili2db.inheritance	newAndSubClass
SZ_Freienbach2035_20180622.Datei	ch.ehi.ili2db.inheritance	newAndSubClass
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation	ch.ehi.ili2db.inheritance	newAndSubClass
SZ_Freienbach2035_20180622.Gemeindeinformationen.Liegenschaft	ch.ehi.ili2db.inheritance	newAndSubClass
SZ_Freienbach2035_20180622.Gemeindeinformationen.Objektinformation_ObjektinformationGeom	ch.ehi.ili2db.inheritance	embedded
\.


--
-- TOC entry 10400 (class 0 OID 0)
-- Dependencies: 1942
-- Name: t_ili2db_seq; Type: SEQUENCE SET; Schema: interlis_no_ladm; Owner: postgres
--

SELECT pg_catalog.setval('interlis_no_ladm.t_ili2db_seq', 7, true);


--
-- TOC entry 10206 (class 2606 OID 335113)
-- Name: art art_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.art
    ADD CONSTRAINT art_pkey PRIMARY KEY (t_id);


--
-- TOC entry 10209 (class 2606 OID 335115)
-- Name: datei datei_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.datei
    ADD CONSTRAINT datei_pkey PRIMARY KEY (t_id);


--
-- TOC entry 10213 (class 2606 OID 335117)
-- Name: liegenschaft liegenschaft_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.liegenschaft
    ADD CONSTRAINT liegenschaft_pkey PRIMARY KEY (t_id);


--
-- TOC entry 10216 (class 2606 OID 335119)
-- Name: liegenschaftgeom liegenschaftgeom_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.liegenschaftgeom
    ADD CONSTRAINT liegenschaftgeom_pkey PRIMARY KEY (t_id);


--
-- TOC entry 10219 (class 2606 OID 335121)
-- Name: objektinformation objektinformation_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.objektinformation
    ADD CONSTRAINT objektinformation_pkey PRIMARY KEY (t_id);


--
-- TOC entry 10222 (class 2606 OID 335123)
-- Name: objektinformationgeom objektinformationgeom_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.objektinformationgeom
    ADD CONSTRAINT objektinformationgeom_pkey PRIMARY KEY (t_id);


--
-- TOC entry 10225 (class 2606 OID 335125)
-- Name: ortsteil ortsteil_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.ortsteil
    ADD CONSTRAINT ortsteil_pkey PRIMARY KEY (t_id);


--
-- TOC entry 10228 (class 2606 OID 335127)
-- Name: t_ili2db_attrname t_ili2db_attrname_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.t_ili2db_attrname
    ADD CONSTRAINT t_ili2db_attrname_pkey PRIMARY KEY (colowner, sqlname);


--
-- TOC entry 10231 (class 2606 OID 335129)
-- Name: t_ili2db_basket t_ili2db_basket_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.t_ili2db_basket
    ADD CONSTRAINT t_ili2db_basket_pkey PRIMARY KEY (t_id);


--
-- TOC entry 10233 (class 2606 OID 335131)
-- Name: t_ili2db_classname t_ili2db_classname_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.t_ili2db_classname
    ADD CONSTRAINT t_ili2db_classname_pkey PRIMARY KEY (iliname);


--
-- TOC entry 10236 (class 2606 OID 335133)
-- Name: t_ili2db_dataset t_ili2db_dataset_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.t_ili2db_dataset
    ADD CONSTRAINT t_ili2db_dataset_pkey PRIMARY KEY (t_id);


--
-- TOC entry 10238 (class 2606 OID 335135)
-- Name: t_ili2db_inheritance t_ili2db_inheritance_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.t_ili2db_inheritance
    ADD CONSTRAINT t_ili2db_inheritance_pkey PRIMARY KEY (thisclass);


--
-- TOC entry 10241 (class 2606 OID 335137)
-- Name: t_ili2db_model t_ili2db_model_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.t_ili2db_model
    ADD CONSTRAINT t_ili2db_model_pkey PRIMARY KEY (modelname, iliversion);


--
-- TOC entry 10243 (class 2606 OID 335139)
-- Name: t_ili2db_settings t_ili2db_settings_pkey; Type: CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.t_ili2db_settings
    ADD CONSTRAINT t_ili2db_settings_pkey PRIMARY KEY (tag);


--
-- TOC entry 10207 (class 1259 OID 335140)
-- Name: datei_objektinformation_dateien_idx; Type: INDEX; Schema: interlis_no_ladm; Owner: postgres
--

CREATE INDEX datei_objektinformation_dateien_idx ON interlis_no_ladm.datei USING btree (objektinformation_dateien);


--
-- TOC entry 10210 (class 1259 OID 335141)
-- Name: liegenschaft_art_idx; Type: INDEX; Schema: interlis_no_ladm; Owner: postgres
--

CREATE INDEX liegenschaft_art_idx ON interlis_no_ladm.liegenschaft USING btree (art);


--
-- TOC entry 10211 (class 1259 OID 335142)
-- Name: liegenschaft_ortsteil_idx; Type: INDEX; Schema: interlis_no_ladm; Owner: postgres
--

CREATE INDEX liegenschaft_ortsteil_idx ON interlis_no_ladm.liegenschaft USING btree (ortsteil);


--
-- TOC entry 10214 (class 1259 OID 335143)
-- Name: liegenschaftgeom_geometrie_idx; Type: INDEX; Schema: interlis_no_ladm; Owner: postgres
--

CREATE INDEX liegenschaftgeom_geometrie_idx ON interlis_no_ladm.liegenschaftgeom USING gist (geometrie);


--
-- TOC entry 10217 (class 1259 OID 335144)
-- Name: liegenschaftgeom_rliegenschaft_idx; Type: INDEX; Schema: interlis_no_ladm; Owner: postgres
--

CREATE INDEX liegenschaftgeom_rliegenschaft_idx ON interlis_no_ladm.liegenschaftgeom USING btree (rliegenschaft);


--
-- TOC entry 10220 (class 1259 OID 335145)
-- Name: objektinformationgeom_geometrie_idx; Type: INDEX; Schema: interlis_no_ladm; Owner: postgres
--

CREATE INDEX objektinformationgeom_geometrie_idx ON interlis_no_ladm.objektinformationgeom USING gist (geometrie);


--
-- TOC entry 10223 (class 1259 OID 335146)
-- Name: objektinformationgeom_robjektinformation_idx; Type: INDEX; Schema: interlis_no_ladm; Owner: postgres
--

CREATE INDEX objektinformationgeom_robjektinformation_idx ON interlis_no_ladm.objektinformationgeom USING btree (robjektinformation);


--
-- TOC entry 10226 (class 1259 OID 335147)
-- Name: t_ili2db_attrname_colowner_sqlname_key; Type: INDEX; Schema: interlis_no_ladm; Owner: postgres
--

CREATE UNIQUE INDEX t_ili2db_attrname_colowner_sqlname_key ON interlis_no_ladm.t_ili2db_attrname USING btree (colowner, sqlname);


--
-- TOC entry 10229 (class 1259 OID 335148)
-- Name: t_ili2db_basket_dataset_idx; Type: INDEX; Schema: interlis_no_ladm; Owner: postgres
--

CREATE INDEX t_ili2db_basket_dataset_idx ON interlis_no_ladm.t_ili2db_basket USING btree (dataset);


--
-- TOC entry 10234 (class 1259 OID 335149)
-- Name: t_ili2db_dataset_datasetname_key; Type: INDEX; Schema: interlis_no_ladm; Owner: postgres
--

CREATE UNIQUE INDEX t_ili2db_dataset_datasetname_key ON interlis_no_ladm.t_ili2db_dataset USING btree (datasetname);


--
-- TOC entry 10239 (class 1259 OID 335150)
-- Name: t_ili2db_model_modelname_iliversion_key; Type: INDEX; Schema: interlis_no_ladm; Owner: postgres
--

CREATE UNIQUE INDEX t_ili2db_model_modelname_iliversion_key ON interlis_no_ladm.t_ili2db_model USING btree (modelname, iliversion);


--
-- TOC entry 10244 (class 2606 OID 335151)
-- Name: datei datei_objektinformation_dateien_fkey; Type: FK CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.datei
    ADD CONSTRAINT datei_objektinformation_dateien_fkey FOREIGN KEY (objektinformation_dateien) REFERENCES interlis_no_ladm.objektinformation(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 10245 (class 2606 OID 335156)
-- Name: liegenschaft liegenschaft_art_fkey; Type: FK CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.liegenschaft
    ADD CONSTRAINT liegenschaft_art_fkey FOREIGN KEY (art) REFERENCES interlis_no_ladm.art(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 10246 (class 2606 OID 335161)
-- Name: liegenschaft liegenschaft_ortsteil_fkey; Type: FK CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.liegenschaft
    ADD CONSTRAINT liegenschaft_ortsteil_fkey FOREIGN KEY (ortsteil) REFERENCES interlis_no_ladm.ortsteil(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 10247 (class 2606 OID 335166)
-- Name: liegenschaftgeom liegenschaftgeom_rliegenschaft_fkey; Type: FK CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.liegenschaftgeom
    ADD CONSTRAINT liegenschaftgeom_rliegenschaft_fkey FOREIGN KEY (rliegenschaft) REFERENCES interlis_no_ladm.liegenschaft(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 10248 (class 2606 OID 335171)
-- Name: objektinformationgeom objektinformationgeom_robjektinformation_fkey; Type: FK CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.objektinformationgeom
    ADD CONSTRAINT objektinformationgeom_robjektinformation_fkey FOREIGN KEY (robjektinformation) REFERENCES interlis_no_ladm.objektinformation(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 10249 (class 2606 OID 335176)
-- Name: t_ili2db_basket t_ili2db_basket_dataset_fkey; Type: FK CONSTRAINT; Schema: interlis_no_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_no_ladm.t_ili2db_basket
    ADD CONSTRAINT t_ili2db_basket_dataset_fkey FOREIGN KEY (dataset) REFERENCES interlis_no_ladm.t_ili2db_dataset(t_id) DEFERRABLE INITIALLY DEFERRED;


-- Completed on 2020-07-15 12:29:17 -05

--
-- PostgreSQL database dump complete
--

