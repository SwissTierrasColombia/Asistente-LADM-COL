--
-- PostgreSQL database dump
--

-- Dumped from database version 11.8 (Ubuntu 11.8-1.pgdg20.04+1)
-- Dumped by pg_dump version 12.3 (Ubuntu 12.3-1.pgdg20.04+1)

-- Started on 2020-07-15 12:42:40 -05

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
-- TOC entry 16 (class 2615 OID 338701)
-- Name: ladm_col_210; Type: SCHEMA; Schema: -; Owner: postgres
--

DROP SCHEMA IF EXISTS ladm_col_210 CASCADE;
CREATE SCHEMA ladm_col_210;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


ALTER SCHEMA ladm_col_210 OWNER TO postgres;

--
-- TOC entry 2129 (class 1259 OID 338702)
-- Name: t_ili2db_seq; Type: SEQUENCE; Schema: ladm_col_210; Owner: postgres
--

CREATE SEQUENCE ladm_col_210.t_ili2db_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ladm_col_210.t_ili2db_seq OWNER TO postgres;

SET default_tablespace = '';

--
-- TOC entry 2130 (class 1259 OID 338704)
-- Name: anystructure; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.anystructure (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    op_agrupacion_intrsdos_calidad bigint,
    op_agrupacion_intrsdos_procedencia bigint,
    op_construccion_calidad bigint,
    op_construccion_procedencia bigint,
    op_derecho_calidad bigint,
    op_derecho_procedencia bigint,
    op_interesado_calidad bigint,
    op_interesado_procedencia bigint,
    op_lindero_calidad bigint,
    op_lindero_procedencia bigint,
    op_predio_calidad bigint,
    op_predio_procedencia bigint,
    op_puntocontrol_calidad bigint,
    op_puntocontrol_procedencia bigint,
    op_puntolindero_calidad bigint,
    op_puntolindero_procedencia bigint,
    op_restriccion_calidad bigint,
    op_restriccion_procedencia bigint,
    op_terreno_calidad bigint,
    op_terreno_procedencia bigint,
    op_puntolevantamiento_calidad bigint,
    op_puntolevantamiento_procedencia bigint,
    op_servidumbretransito_calidad bigint,
    op_servidumbretransito_procedencia bigint,
    op_unidadconstruccion_calidad bigint,
    op_unidadconstruccion_procedencia bigint
);


ALTER TABLE ladm_col_210.anystructure OWNER TO postgres;

--
-- TOC entry 12711 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_agrupacion_intrsdos_calidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_agrupacion_intrsdos_calidad IS 'Metadatos relativos a la calidad de la instancia.';


--
-- TOC entry 12712 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_agrupacion_intrsdos_procedencia; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_agrupacion_intrsdos_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.';


--
-- TOC entry 12713 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_construccion_calidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_construccion_calidad IS 'Metadatos relativos a la calidad de la instancia.';


--
-- TOC entry 12714 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_construccion_procedencia; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_construccion_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.';


--
-- TOC entry 12715 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_derecho_calidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_derecho_calidad IS 'Metadatos relativos a la calidad de la instancia.';


--
-- TOC entry 12716 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_derecho_procedencia; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_derecho_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.';


--
-- TOC entry 12717 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_interesado_calidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_interesado_calidad IS 'Metadatos relativos a la calidad de la instancia.';


--
-- TOC entry 12718 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_interesado_procedencia; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_interesado_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.';


--
-- TOC entry 12719 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_lindero_calidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_lindero_calidad IS 'Metadatos relativos a la calidad de la instancia.';


--
-- TOC entry 12720 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_lindero_procedencia; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_lindero_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.';


--
-- TOC entry 12721 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_predio_calidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_predio_calidad IS 'Metadatos relativos a la calidad de la instancia.';


--
-- TOC entry 12722 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_predio_procedencia; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_predio_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.';


--
-- TOC entry 12723 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_puntocontrol_calidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_puntocontrol_calidad IS 'Metadatos relativos a la calidad de la instancia.';


--
-- TOC entry 12724 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_puntocontrol_procedencia; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_puntocontrol_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.';


--
-- TOC entry 12725 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_puntolindero_calidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_puntolindero_calidad IS 'Metadatos relativos a la calidad de la instancia.';


--
-- TOC entry 12726 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_puntolindero_procedencia; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_puntolindero_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.';


--
-- TOC entry 12727 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_restriccion_calidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_restriccion_calidad IS 'Metadatos relativos a la calidad de la instancia.';


--
-- TOC entry 12728 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_restriccion_procedencia; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_restriccion_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.';


--
-- TOC entry 12729 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_terreno_calidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_terreno_calidad IS 'Metadatos relativos a la calidad de la instancia.';


--
-- TOC entry 12730 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_terreno_procedencia; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_terreno_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.';


--
-- TOC entry 12731 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_puntolevantamiento_calidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_puntolevantamiento_calidad IS 'Metadatos relativos a la calidad de la instancia.';


--
-- TOC entry 12732 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_puntolevantamiento_procedencia; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_puntolevantamiento_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.';


--
-- TOC entry 12733 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_servidumbretransito_calidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_servidumbretransito_calidad IS 'Metadatos relativos a la calidad de la instancia.';


--
-- TOC entry 12734 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_servidumbretransito_procedencia; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_servidumbretransito_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.';


--
-- TOC entry 12735 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_unidadconstruccion_calidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_unidadconstruccion_calidad IS 'Metadatos relativos a la calidad de la instancia.';


--
-- TOC entry 12736 (class 0 OID 0)
-- Dependencies: 2130
-- Name: COLUMN anystructure.op_unidadconstruccion_procedencia; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.anystructure.op_unidadconstruccion_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.';


--
-- TOC entry 2131 (class 1259 OID 338708)
-- Name: cc_metodooperacion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.cc_metodooperacion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    formula character varying(255) NOT NULL,
    dimensiones_origen integer,
    ddimensiones_objetivo integer,
    col_transformacion_transformacion bigint,
    CONSTRAINT cc_metodooperacion_ddimensiones_objetivo_check CHECK (((ddimensiones_objetivo >= 0) AND (ddimensiones_objetivo <= 999999999))),
    CONSTRAINT cc_metodooperacion_dimensiones_origen_check CHECK (((dimensiones_origen >= 0) AND (dimensiones_origen <= 999999999)))
);


ALTER TABLE ladm_col_210.cc_metodooperacion OWNER TO postgres;

--
-- TOC entry 12737 (class 0 OID 0)
-- Dependencies: 2131
-- Name: TABLE cc_metodooperacion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.cc_metodooperacion IS 'Estructura que proviene de la traducción de la clase CC_OperationMethod de la ISO 19111. Indica el método utilizado, mediante un algoritmo o un procedimiento, para realizar operaciones con coordenadas.';


--
-- TOC entry 12738 (class 0 OID 0)
-- Dependencies: 2131
-- Name: COLUMN cc_metodooperacion.formula; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.cc_metodooperacion.formula IS 'Fórmulas o procedimientos utilizadoa por este método de operación de coordenadas. Esto puede ser una referencia a una publicación. Tenga en cuenta que el método de operación puede no ser analítico, en cuyo caso este atributo hace referencia o contiene el procedimiento, no una fórmula analítica.';


--
-- TOC entry 12739 (class 0 OID 0)
-- Dependencies: 2131
-- Name: COLUMN cc_metodooperacion.dimensiones_origen; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.cc_metodooperacion.dimensiones_origen IS 'Número de dimensiones en la fuente CRS de este método de operación de coordenadas.';


--
-- TOC entry 12740 (class 0 OID 0)
-- Dependencies: 2131
-- Name: COLUMN cc_metodooperacion.ddimensiones_objetivo; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.cc_metodooperacion.ddimensiones_objetivo IS 'Número de dimensiones en el CRS de destino de este método de operación de coordenadas.';


--
-- TOC entry 12741 (class 0 OID 0)
-- Dependencies: 2131
-- Name: COLUMN cc_metodooperacion.col_transformacion_transformacion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.cc_metodooperacion.col_transformacion_transformacion IS 'Fórmula o procedimiento utilizado en la transformación.';


--
-- TOC entry 2132 (class 1259 OID 338714)
-- Name: ci_forma_presentacion_codigo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.ci_forma_presentacion_codigo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.ci_forma_presentacion_codigo OWNER TO postgres;

--
-- TOC entry 2133 (class 1259 OID 338721)
-- Name: col_areatipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_areatipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_areatipo OWNER TO postgres;

--
-- TOC entry 2134 (class 1259 OID 338728)
-- Name: col_areavalor; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_areavalor (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    areasize numeric(15,1) NOT NULL,
    atype bigint NOT NULL,
    op_construccion_area bigint,
    op_terreno_area bigint,
    op_servidumbretransito_area bigint,
    op_unidadconstruccion_area bigint,
    CONSTRAINT col_areavalor_areasize_check CHECK (((areasize >= 0.0) AND (areasize <= 99999999999999.9)))
);


ALTER TABLE ladm_col_210.col_areavalor OWNER TO postgres;

--
-- TOC entry 2135 (class 1259 OID 338733)
-- Name: col_baunitcomointeresado; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_baunitcomointeresado (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    interesado_op_interesado bigint,
    interesado_op_agrupacion_interesados bigint,
    unidad bigint NOT NULL
);


ALTER TABLE ladm_col_210.col_baunitcomointeresado OWNER TO postgres;

--
-- TOC entry 2136 (class 1259 OID 338737)
-- Name: col_baunitfuente; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_baunitfuente (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    fuente_espacial bigint NOT NULL,
    unidad bigint NOT NULL
);


ALTER TABLE ladm_col_210.col_baunitfuente OWNER TO postgres;

--
-- TOC entry 2137 (class 1259 OID 338741)
-- Name: col_baunittipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_baunittipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_baunittipo OWNER TO postgres;

--
-- TOC entry 2138 (class 1259 OID 338748)
-- Name: col_cclfuente; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_cclfuente (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ccl bigint NOT NULL,
    fuente_espacial bigint NOT NULL
);


ALTER TABLE ladm_col_210.col_cclfuente OWNER TO postgres;

--
-- TOC entry 2139 (class 1259 OID 338752)
-- Name: col_clfuente; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_clfuente (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    fuente_espacial bigint NOT NULL
);


ALTER TABLE ladm_col_210.col_clfuente OWNER TO postgres;

--
-- TOC entry 2140 (class 1259 OID 338756)
-- Name: col_contenidoniveltipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_contenidoniveltipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_contenidoniveltipo OWNER TO postgres;

--
-- TOC entry 2141 (class 1259 OID 338763)
-- Name: col_dimensiontipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_dimensiontipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_dimensiontipo OWNER TO postgres;

--
-- TOC entry 2142 (class 1259 OID 338770)
-- Name: col_estadodisponibilidadtipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_estadodisponibilidadtipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_estadodisponibilidadtipo OWNER TO postgres;

--
-- TOC entry 2143 (class 1259 OID 338777)
-- Name: col_estadoredserviciostipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_estadoredserviciostipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_estadoredserviciostipo OWNER TO postgres;

--
-- TOC entry 2144 (class 1259 OID 338784)
-- Name: col_estructuratipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_estructuratipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_estructuratipo OWNER TO postgres;

--
-- TOC entry 2145 (class 1259 OID 338791)
-- Name: col_fuenteadministrativatipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_fuenteadministrativatipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_fuenteadministrativatipo OWNER TO postgres;

--
-- TOC entry 2146 (class 1259 OID 338798)
-- Name: col_fuenteespacialtipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_fuenteespacialtipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_fuenteespacialtipo OWNER TO postgres;

--
-- TOC entry 2147 (class 1259 OID 338805)
-- Name: col_grupointeresadotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_grupointeresadotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_grupointeresadotipo OWNER TO postgres;

--
-- TOC entry 2148 (class 1259 OID 338812)
-- Name: col_interpolaciontipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_interpolaciontipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_interpolaciontipo OWNER TO postgres;

--
-- TOC entry 2149 (class 1259 OID 338819)
-- Name: col_iso19125_tipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_iso19125_tipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_iso19125_tipo OWNER TO postgres;

--
-- TOC entry 2150 (class 1259 OID 338826)
-- Name: col_masccl; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_masccl (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ccl_mas bigint NOT NULL,
    ue_mas_op_construccion bigint,
    ue_mas_op_terreno bigint,
    ue_mas_op_servidumbretransito bigint,
    ue_mas_op_unidadconstruccion bigint
);


ALTER TABLE ladm_col_210.col_masccl OWNER TO postgres;

--
-- TOC entry 2151 (class 1259 OID 338830)
-- Name: col_mascl; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_mascl (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ue_mas_op_construccion bigint,
    ue_mas_op_terreno bigint,
    ue_mas_op_servidumbretransito bigint,
    ue_mas_op_unidadconstruccion bigint
);


ALTER TABLE ladm_col_210.col_mascl OWNER TO postgres;

--
-- TOC entry 2152 (class 1259 OID 338834)
-- Name: col_menosccl; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_menosccl (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ccl_menos bigint NOT NULL,
    ue_menos_op_construccion bigint,
    ue_menos_op_terreno bigint,
    ue_menos_op_servidumbretransito bigint,
    ue_menos_op_unidadconstruccion bigint
);


ALTER TABLE ladm_col_210.col_menosccl OWNER TO postgres;

--
-- TOC entry 2153 (class 1259 OID 338838)
-- Name: col_menoscl; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_menoscl (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ue_menos_op_construccion bigint,
    ue_menos_op_terreno bigint,
    ue_menos_op_servidumbretransito bigint,
    ue_menos_op_unidadconstruccion bigint
);


ALTER TABLE ladm_col_210.col_menoscl OWNER TO postgres;

--
-- TOC entry 2154 (class 1259 OID 338842)
-- Name: col_metodoproducciontipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_metodoproducciontipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_metodoproducciontipo OWNER TO postgres;

--
-- TOC entry 2155 (class 1259 OID 338849)
-- Name: col_miembros; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_miembros (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    interesado_op_interesado bigint,
    interesado_op_agrupacion_interesados bigint,
    agrupacion bigint NOT NULL
);


ALTER TABLE ladm_col_210.col_miembros OWNER TO postgres;

--
-- TOC entry 2156 (class 1259 OID 338853)
-- Name: col_puntoccl; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_puntoccl (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    punto_op_puntocontrol bigint,
    punto_op_puntolindero bigint,
    punto_op_puntolevantamiento bigint,
    ccl bigint NOT NULL
);


ALTER TABLE ladm_col_210.col_puntoccl OWNER TO postgres;

--
-- TOC entry 2157 (class 1259 OID 338857)
-- Name: col_puntocl; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_puntocl (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    punto_op_puntocontrol bigint,
    punto_op_puntolindero bigint,
    punto_op_puntolevantamiento bigint
);


ALTER TABLE ladm_col_210.col_puntocl OWNER TO postgres;

--
-- TOC entry 2158 (class 1259 OID 338861)
-- Name: col_puntofuente; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_puntofuente (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    fuente_espacial bigint NOT NULL,
    punto_op_puntocontrol bigint,
    punto_op_puntolindero bigint,
    punto_op_puntolevantamiento bigint
);


ALTER TABLE ladm_col_210.col_puntofuente OWNER TO postgres;

--
-- TOC entry 2159 (class 1259 OID 338865)
-- Name: col_puntotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_puntotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_puntotipo OWNER TO postgres;

--
-- TOC entry 2160 (class 1259 OID 338872)
-- Name: col_redserviciostipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_redserviciostipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_redserviciostipo OWNER TO postgres;

--
-- TOC entry 2161 (class 1259 OID 338879)
-- Name: col_registrotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_registrotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_registrotipo OWNER TO postgres;

--
-- TOC entry 2162 (class 1259 OID 338886)
-- Name: col_relacionfuente; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_relacionfuente (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    fuente_administrativa bigint NOT NULL
);


ALTER TABLE ladm_col_210.col_relacionfuente OWNER TO postgres;

--
-- TOC entry 2163 (class 1259 OID 338890)
-- Name: col_relacionfuenteuespacial; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_relacionfuenteuespacial (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    fuente_espacial bigint NOT NULL
);


ALTER TABLE ladm_col_210.col_relacionfuenteuespacial OWNER TO postgres;

--
-- TOC entry 2164 (class 1259 OID 338894)
-- Name: col_relacionsuperficietipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_relacionsuperficietipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_relacionsuperficietipo OWNER TO postgres;

--
-- TOC entry 2165 (class 1259 OID 338901)
-- Name: col_responsablefuente; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_responsablefuente (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    fuente_administrativa bigint NOT NULL,
    interesado_op_interesado bigint,
    interesado_op_agrupacion_interesados bigint
);


ALTER TABLE ladm_col_210.col_responsablefuente OWNER TO postgres;

--
-- TOC entry 2166 (class 1259 OID 338905)
-- Name: col_rrrfuente; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_rrrfuente (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    fuente_administrativa bigint NOT NULL,
    rrr_op_derecho bigint,
    rrr_op_restriccion bigint
);


ALTER TABLE ladm_col_210.col_rrrfuente OWNER TO postgres;

--
-- TOC entry 2167 (class 1259 OID 338909)
-- Name: col_topografofuente; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_topografofuente (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    fuente_espacial bigint NOT NULL,
    topografo_op_interesado bigint,
    topografo_op_agrupacion_interesados bigint
);


ALTER TABLE ladm_col_210.col_topografofuente OWNER TO postgres;

--
-- TOC entry 2168 (class 1259 OID 338913)
-- Name: col_transformacion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_transformacion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    localizacion_transformada public.geometry(PointZ,4326) NOT NULL,
    op_puntocontrol_transformacion_y_resultado bigint,
    op_puntolindero_transformacion_y_resultado bigint,
    op_puntolevantamiento_transformacion_y_resultado bigint
);


ALTER TABLE ladm_col_210.col_transformacion OWNER TO postgres;

--
-- TOC entry 12742 (class 0 OID 0)
-- Dependencies: 2168
-- Name: TABLE col_transformacion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.col_transformacion IS 'Registro de la fórmula o procedimiento utilizado en la transformación y de su resultado.';


--
-- TOC entry 12743 (class 0 OID 0)
-- Dependencies: 2168
-- Name: COLUMN col_transformacion.localizacion_transformada; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.col_transformacion.localizacion_transformada IS 'Geometría una vez realizado el proceso de transformación.';


--
-- TOC entry 2169 (class 1259 OID 338920)
-- Name: col_uebaunit; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_uebaunit (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ue_op_construccion bigint,
    ue_op_terreno bigint,
    ue_op_servidumbretransito bigint,
    ue_op_unidadconstruccion bigint,
    baunit bigint NOT NULL
);


ALTER TABLE ladm_col_210.col_uebaunit OWNER TO postgres;

--
-- TOC entry 2170 (class 1259 OID 338924)
-- Name: col_uefuente; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_uefuente (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ue_op_construccion bigint,
    ue_op_terreno bigint,
    ue_op_servidumbretransito bigint,
    ue_op_unidadconstruccion bigint,
    fuente_espacial bigint NOT NULL
);


ALTER TABLE ladm_col_210.col_uefuente OWNER TO postgres;

--
-- TOC entry 2171 (class 1259 OID 338928)
-- Name: col_ueuegrupo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_ueuegrupo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    parte_op_construccion bigint,
    parte_op_terreno bigint,
    parte_op_servidumbretransito bigint,
    parte_op_unidadconstruccion bigint
);


ALTER TABLE ladm_col_210.col_ueuegrupo OWNER TO postgres;

--
-- TOC entry 2172 (class 1259 OID 338932)
-- Name: col_unidadedificaciontipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_unidadedificaciontipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_unidadedificaciontipo OWNER TO postgres;

--
-- TOC entry 2173 (class 1259 OID 338939)
-- Name: col_unidadfuente; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_unidadfuente (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    fuente_administrativa bigint NOT NULL,
    unidad bigint NOT NULL
);


ALTER TABLE ladm_col_210.col_unidadfuente OWNER TO postgres;

--
-- TOC entry 2174 (class 1259 OID 338943)
-- Name: col_volumentipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_volumentipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.col_volumentipo OWNER TO postgres;

--
-- TOC entry 2175 (class 1259 OID 338950)
-- Name: col_volumenvalor; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.col_volumenvalor (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    volumen_medicion numeric(15,1) NOT NULL,
    tipo bigint NOT NULL,
    op_construccion_volumen bigint,
    op_terreno_volumen bigint,
    op_servidumbretransito_volumen bigint,
    op_unidadconstruccion_volumen bigint,
    CONSTRAINT col_volumenvalor_volumen_medicion_check CHECK (((volumen_medicion >= 0.0) AND (volumen_medicion <= 99999999999999.9)))
);


ALTER TABLE ladm_col_210.col_volumenvalor OWNER TO postgres;

--
-- TOC entry 12744 (class 0 OID 0)
-- Dependencies: 2175
-- Name: TABLE col_volumenvalor; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.col_volumenvalor IS 'Estructura para la definición de un tipo de dato personalizado que permite indicar la medición de un volumen y la naturaleza de este.';


--
-- TOC entry 12745 (class 0 OID 0)
-- Dependencies: 2175
-- Name: COLUMN col_volumenvalor.volumen_medicion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.col_volumenvalor.volumen_medicion IS 'Medición del volumen en m3.';


--
-- TOC entry 12746 (class 0 OID 0)
-- Dependencies: 2175
-- Name: COLUMN col_volumenvalor.tipo; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.col_volumenvalor.tipo IS 'Indicación de si el volumen es calculado, si figura como oficial o si se da otra circunstancia.';


--
-- TOC entry 12747 (class 0 OID 0)
-- Dependencies: 2175
-- Name: COLUMN col_volumenvalor.op_construccion_volumen; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.col_volumenvalor.op_construccion_volumen IS 'Corresponde al atributo volume de la clase en LADM.';


--
-- TOC entry 12748 (class 0 OID 0)
-- Dependencies: 2175
-- Name: COLUMN col_volumenvalor.op_terreno_volumen; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.col_volumenvalor.op_terreno_volumen IS 'Corresponde al atributo volume de la clase en LADM.';


--
-- TOC entry 12749 (class 0 OID 0)
-- Dependencies: 2175
-- Name: COLUMN col_volumenvalor.op_servidumbretransito_volumen; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.col_volumenvalor.op_servidumbretransito_volumen IS 'Corresponde al atributo volume de la clase en LADM.';


--
-- TOC entry 12750 (class 0 OID 0)
-- Dependencies: 2175
-- Name: COLUMN col_volumenvalor.op_unidadconstruccion_volumen; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.col_volumenvalor.op_unidadconstruccion_volumen IS 'Corresponde al atributo volume de la clase en LADM.';


--
-- TOC entry 2176 (class 1259 OID 338955)
-- Name: extarchivo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.extarchivo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    fecha_aceptacion date,
    datos character varying(255),
    extraccion date,
    fecha_grabacion date,
    fecha_entrega date,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL,
    snr_fuente_cabidlndros_archivo bigint,
    op_fuenteadministrtiva_ext_archivo_id bigint,
    op_fuenteespacial_ext_archivo_id bigint
);


ALTER TABLE ladm_col_210.extarchivo OWNER TO postgres;

--
-- TOC entry 12751 (class 0 OID 0)
-- Dependencies: 2176
-- Name: TABLE extarchivo; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.extarchivo IS 'Referencia a clase externa desde donde se gestiona el repositorio de archivos.';


--
-- TOC entry 12752 (class 0 OID 0)
-- Dependencies: 2176
-- Name: COLUMN extarchivo.fecha_aceptacion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extarchivo.fecha_aceptacion IS 'Fecha en la que ha sido aceptado el documento.';


--
-- TOC entry 12753 (class 0 OID 0)
-- Dependencies: 2176
-- Name: COLUMN extarchivo.datos; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extarchivo.datos IS 'Datos que contiene el documento.';


--
-- TOC entry 12754 (class 0 OID 0)
-- Dependencies: 2176
-- Name: COLUMN extarchivo.extraccion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extarchivo.extraccion IS 'Última fecha de extracción del documento.';


--
-- TOC entry 12755 (class 0 OID 0)
-- Dependencies: 2176
-- Name: COLUMN extarchivo.fecha_grabacion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extarchivo.fecha_grabacion IS 'Fecha en la que el documento es aceptado en el sistema.';


--
-- TOC entry 12756 (class 0 OID 0)
-- Dependencies: 2176
-- Name: COLUMN extarchivo.fecha_entrega; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extarchivo.fecha_entrega IS 'Fecha en la que fue entregado el documento.';


--
-- TOC entry 12757 (class 0 OID 0)
-- Dependencies: 2176
-- Name: COLUMN extarchivo.op_fuenteadministrtiva_ext_archivo_id; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extarchivo.op_fuenteadministrtiva_ext_archivo_id IS 'Identificador del archivo fuente controlado por una clase externa.';


--
-- TOC entry 12758 (class 0 OID 0)
-- Dependencies: 2176
-- Name: COLUMN extarchivo.op_fuenteespacial_ext_archivo_id; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extarchivo.op_fuenteespacial_ext_archivo_id IS 'Identificador del archivo fuente controlado por una clase externa.';


--
-- TOC entry 2177 (class 1259 OID 338962)
-- Name: extdireccion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.extdireccion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    tipo_direccion bigint NOT NULL,
    es_direccion_principal boolean,
    localizacion public.geometry(PointZ,4326),
    codigo_postal character varying(255),
    clase_via_principal bigint,
    valor_via_principal character varying(100),
    letra_via_principal character varying(20),
    sector_ciudad bigint,
    valor_via_generadora character varying(100),
    letra_via_generadora character varying(20),
    numero_predio character varying(20),
    sector_predio bigint,
    complemento character varying(255),
    nombre_predio character varying(255),
    extunidadedificcnfsica_ext_direccion_id bigint,
    extinteresado_ext_direccion_id bigint,
    op_construccion_ext_direccion_id bigint,
    op_terreno_ext_direccion_id bigint,
    op_servidumbretransito_ext_direccion_id bigint,
    op_unidadconstruccion_ext_direccion_id bigint
);


ALTER TABLE ladm_col_210.extdireccion OWNER TO postgres;

--
-- TOC entry 12759 (class 0 OID 0)
-- Dependencies: 2177
-- Name: TABLE extdireccion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.extdireccion IS 'Referencia a una clase externa para gestionar direcciones.';


--
-- TOC entry 12760 (class 0 OID 0)
-- Dependencies: 2177
-- Name: COLUMN extdireccion.localizacion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extdireccion.localizacion IS 'Par de valores georreferenciados (x,y) en la que se encuentra la dirección.';


--
-- TOC entry 12761 (class 0 OID 0)
-- Dependencies: 2177
-- Name: COLUMN extdireccion.extinteresado_ext_direccion_id; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extdireccion.extinteresado_ext_direccion_id IS 'Identificador externo del interesado.';


--
-- TOC entry 12762 (class 0 OID 0)
-- Dependencies: 2177
-- Name: COLUMN extdireccion.op_construccion_ext_direccion_id; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extdireccion.op_construccion_ext_direccion_id IS 'Corresponde al atributo extAddressID de la clase en LADM.';


--
-- TOC entry 12763 (class 0 OID 0)
-- Dependencies: 2177
-- Name: COLUMN extdireccion.op_terreno_ext_direccion_id; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extdireccion.op_terreno_ext_direccion_id IS 'Corresponde al atributo extAddressID de la clase en LADM.';


--
-- TOC entry 12764 (class 0 OID 0)
-- Dependencies: 2177
-- Name: COLUMN extdireccion.op_servidumbretransito_ext_direccion_id; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extdireccion.op_servidumbretransito_ext_direccion_id IS 'Corresponde al atributo extAddressID de la clase en LADM.';


--
-- TOC entry 12765 (class 0 OID 0)
-- Dependencies: 2177
-- Name: COLUMN extdireccion.op_unidadconstruccion_ext_direccion_id; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extdireccion.op_unidadconstruccion_ext_direccion_id IS 'Corresponde al atributo extAddressID de la clase en LADM.';


--
-- TOC entry 2178 (class 1259 OID 338969)
-- Name: extdireccion_clase_via_principal; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.extdireccion_clase_via_principal (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.extdireccion_clase_via_principal OWNER TO postgres;

--
-- TOC entry 2179 (class 1259 OID 338976)
-- Name: extdireccion_sector_ciudad; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.extdireccion_sector_ciudad (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.extdireccion_sector_ciudad OWNER TO postgres;

--
-- TOC entry 2180 (class 1259 OID 338983)
-- Name: extdireccion_sector_predio; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.extdireccion_sector_predio (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.extdireccion_sector_predio OWNER TO postgres;

--
-- TOC entry 2181 (class 1259 OID 338990)
-- Name: extdireccion_tipo_direccion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.extdireccion_tipo_direccion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.extdireccion_tipo_direccion OWNER TO postgres;

--
-- TOC entry 2182 (class 1259 OID 338997)
-- Name: extinteresado; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.extinteresado (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    nombre character varying(255),
    extredserviciosfisica_ext_interesado_administrador_id bigint,
    op_agrupacion_intrsdos_ext_pid bigint,
    op_interesado_ext_pid bigint
);


ALTER TABLE ladm_col_210.extinteresado OWNER TO postgres;

--
-- TOC entry 12766 (class 0 OID 0)
-- Dependencies: 2182
-- Name: TABLE extinteresado; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.extinteresado IS 'Referencia a una clase externa para gestionar direcciones.';


--
-- TOC entry 12767 (class 0 OID 0)
-- Dependencies: 2182
-- Name: COLUMN extinteresado.extredserviciosfisica_ext_interesado_administrador_id; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extinteresado.extredserviciosfisica_ext_interesado_administrador_id IS 'Identificador de referencia a un interesado externo que es el administrador.';


--
-- TOC entry 12768 (class 0 OID 0)
-- Dependencies: 2182
-- Name: COLUMN extinteresado.op_agrupacion_intrsdos_ext_pid; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extinteresado.op_agrupacion_intrsdos_ext_pid IS 'Identificador del interesado.';


--
-- TOC entry 12769 (class 0 OID 0)
-- Dependencies: 2182
-- Name: COLUMN extinteresado.op_interesado_ext_pid; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extinteresado.op_interesado_ext_pid IS 'Identificador del interesado.';


--
-- TOC entry 2183 (class 1259 OID 339001)
-- Name: extredserviciosfisica; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.extredserviciosfisica (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    orientada boolean
);


ALTER TABLE ladm_col_210.extredserviciosfisica OWNER TO postgres;

--
-- TOC entry 12770 (class 0 OID 0)
-- Dependencies: 2183
-- Name: TABLE extredserviciosfisica; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.extredserviciosfisica IS 'Referencia a una clase externa para gestionar las redes físicas de servicios.';


--
-- TOC entry 12771 (class 0 OID 0)
-- Dependencies: 2183
-- Name: COLUMN extredserviciosfisica.orientada; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.extredserviciosfisica.orientada IS 'Indica si la red de servicios tiene un gradiente o no.';


--
-- TOC entry 2184 (class 1259 OID 339005)
-- Name: extunidadedificacionfisica; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.extunidadedificacionfisica (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint
);


ALTER TABLE ladm_col_210.extunidadedificacionfisica OWNER TO postgres;

--
-- TOC entry 12772 (class 0 OID 0)
-- Dependencies: 2184
-- Name: TABLE extunidadedificacionfisica; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.extunidadedificacionfisica IS 'Control externo de la unidad de edificación física.';


--
-- TOC entry 2185 (class 1259 OID 339009)
-- Name: fraccion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.fraccion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    denominador integer NOT NULL,
    numerador integer NOT NULL,
    col_miembros_participacion bigint,
    op_predio_copropiedad_coeficiente bigint,
    CONSTRAINT fraccion_denominador_check CHECK (((denominador >= 0) AND (denominador <= 999999999))),
    CONSTRAINT fraccion_numerador_check CHECK (((numerador >= 0) AND (numerador <= 999999999)))
);


ALTER TABLE ladm_col_210.fraccion OWNER TO postgres;

--
-- TOC entry 12773 (class 0 OID 0)
-- Dependencies: 2185
-- Name: TABLE fraccion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.fraccion IS 'Estructura para la definición de un tipo de dato personalizado que permite indicar una fracción o quebrado cona serie específica de condiciones.';


--
-- TOC entry 12774 (class 0 OID 0)
-- Dependencies: 2185
-- Name: COLUMN fraccion.denominador; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.fraccion.denominador IS 'Parte inferior de la fracción. Debe ser mayor que 0. Debe ser mayor que el numerador.';


--
-- TOC entry 12775 (class 0 OID 0)
-- Dependencies: 2185
-- Name: COLUMN fraccion.numerador; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.fraccion.numerador IS 'Parte superior de la fracción. Debe ser mayor que 0. Debe sder menor que el denominador.';


--
-- TOC entry 2186 (class 1259 OID 339015)
-- Name: gc_barrio; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_barrio (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    codigo character varying(13),
    nombre character varying(100),
    codigo_sector character varying(9),
    geometria public.geometry(MultiPolygon,4326)
);


ALTER TABLE ladm_col_210.gc_barrio OWNER TO postgres;

--
-- TOC entry 2187 (class 1259 OID 339022)
-- Name: gc_comisiones_construccion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_comisiones_construccion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    geometria public.geometry(MultiPolygonZ,4326)
);


ALTER TABLE ladm_col_210.gc_comisiones_construccion OWNER TO postgres;

--
-- TOC entry 2188 (class 1259 OID 339029)
-- Name: gc_comisiones_terreno; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_comisiones_terreno (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    geometria public.geometry(MultiPolygon,4326)
);


ALTER TABLE ladm_col_210.gc_comisiones_terreno OWNER TO postgres;

--
-- TOC entry 2189 (class 1259 OID 339036)
-- Name: gc_comisiones_unidad_construccion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_comisiones_unidad_construccion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    geometria public.geometry(MultiPolygonZ,4326)
);


ALTER TABLE ladm_col_210.gc_comisiones_unidad_construccion OWNER TO postgres;

--
-- TOC entry 2190 (class 1259 OID 339043)
-- Name: gc_condicionprediotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_condicionprediotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.gc_condicionprediotipo OWNER TO postgres;

--
-- TOC entry 2191 (class 1259 OID 339050)
-- Name: gc_construccion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_construccion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    identificador character varying(30),
    etiqueta character varying(50),
    tipo_construccion bigint,
    tipo_dominio character varying(20),
    numero_pisos integer,
    numero_sotanos integer,
    numero_mezanines integer,
    numero_semisotanos integer,
    codigo_edificacion integer,
    codigo_terreno character varying(30),
    area_construida numeric(16,2),
    geometria public.geometry(MultiPolygonZ,4326),
    gc_predio bigint NOT NULL,
    CONSTRAINT gc_construccion_area_construida_check CHECK (((area_construida >= 0.0) AND (area_construida <= 99999999999999.98))),
    CONSTRAINT gc_construccion_codigo_edificacion_check CHECK (((codigo_edificacion >= 0) AND (codigo_edificacion <= 2147483647))),
    CONSTRAINT gc_construccion_numero_mezanines_check CHECK (((numero_mezanines >= 0) AND (numero_mezanines <= 99))),
    CONSTRAINT gc_construccion_numero_pisos_check CHECK (((numero_pisos >= 0) AND (numero_pisos <= 200))),
    CONSTRAINT gc_construccion_numero_semisotanos_check CHECK (((numero_semisotanos >= 0) AND (numero_semisotanos <= 99))),
    CONSTRAINT gc_construccion_numero_sotanos_check CHECK (((numero_sotanos >= 0) AND (numero_sotanos <= 99)))
);


ALTER TABLE ladm_col_210.gc_construccion OWNER TO postgres;

--
-- TOC entry 2192 (class 1259 OID 339063)
-- Name: gc_copropiedad; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_copropiedad (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    gc_matriz bigint NOT NULL,
    gc_unidad bigint NOT NULL,
    coeficiente_copropiedad numeric(10,7),
    CONSTRAINT gc_copropiedad_coeficiente_copropiedad_check CHECK (((coeficiente_copropiedad >= 0.0) AND (coeficiente_copropiedad <= 100.0)))
);


ALTER TABLE ladm_col_210.gc_copropiedad OWNER TO postgres;

--
-- TOC entry 2193 (class 1259 OID 339068)
-- Name: gc_datos_ph_condiminio; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_datos_ph_condiminio (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    area_total_terreno numeric(16,2),
    area_total_terreno_privada numeric(16,2),
    area_total_terreno_comun numeric(16,2),
    area_total_construida numeric(16,2),
    area_total_construida_privada numeric(16,2),
    area_total_construida_comun numeric(16,2),
    torre_no character varying(10),
    total_pisos_torre integer,
    total_unidades_privadas integer,
    total_sotanos integer,
    total_unidades_sotano integer,
    gc_predio bigint NOT NULL,
    CONSTRAINT gc_datos_ph_condiminio_area_total_constrd_prvada_check CHECK (((area_total_construida_privada >= 0.0) AND (area_total_construida_privada <= 99999999999999.98))),
    CONSTRAINT gc_datos_ph_condiminio_area_total_construid_cmun_check CHECK (((area_total_construida_comun >= 0.0) AND (area_total_construida_comun <= 99999999999999.98))),
    CONSTRAINT gc_datos_ph_condiminio_area_total_construida_check CHECK (((area_total_construida >= 0.0) AND (area_total_construida <= 99999999999999.98))),
    CONSTRAINT gc_datos_ph_condiminio_area_total_terreno_check CHECK (((area_total_terreno >= 0.0) AND (area_total_terreno <= 99999999999999.98))),
    CONSTRAINT gc_datos_ph_condiminio_area_total_terreno_comun_check CHECK (((area_total_terreno_comun >= 0.0) AND (area_total_terreno_comun <= 99999999999999.98))),
    CONSTRAINT gc_datos_ph_condiminio_area_total_terreno_prvada_check CHECK (((area_total_terreno_privada >= 0.0) AND (area_total_terreno_privada <= 99999999999999.98))),
    CONSTRAINT gc_datos_ph_condiminio_total_pisos_torre_check CHECK (((total_pisos_torre >= 0) AND (total_pisos_torre <= 200))),
    CONSTRAINT gc_datos_ph_condiminio_total_sotanos_check CHECK (((total_sotanos >= 0) AND (total_sotanos <= 30))),
    CONSTRAINT gc_datos_ph_condiminio_total_unidades_privadas_check CHECK (((total_unidades_privadas >= 0) AND (total_unidades_privadas <= 99999999))),
    CONSTRAINT gc_datos_ph_condiminio_total_unidades_sotano_check CHECK (((total_unidades_sotano >= 0) AND (total_unidades_sotano <= 99999999)))
);


ALTER TABLE ladm_col_210.gc_datos_ph_condiminio OWNER TO postgres;

--
-- TOC entry 2194 (class 1259 OID 339082)
-- Name: gc_direccion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_direccion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    valor character varying(255),
    principal boolean,
    geometria_referencia public.geometry(LineStringZ,4326),
    gc_predio_catastro_direcciones bigint
);


ALTER TABLE ladm_col_210.gc_direccion OWNER TO postgres;

--
-- TOC entry 2195 (class 1259 OID 339089)
-- Name: gc_manzana; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_manzana (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    codigo character varying(17),
    codigo_anterior character varying(255),
    codigo_barrio character varying(13),
    geometria public.geometry(MultiPolygon,4326)
);


ALTER TABLE ladm_col_210.gc_manzana OWNER TO postgres;

--
-- TOC entry 2196 (class 1259 OID 339096)
-- Name: gc_perimetro; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_perimetro (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    codigo_departamento character varying(2),
    codigo_municipio character varying(5),
    tipo_avaluo character varying(30),
    nombre_geografico character varying(50),
    codigo_nombre character varying(255),
    geometria public.geometry(MultiPolygon,4326)
);


ALTER TABLE ladm_col_210.gc_perimetro OWNER TO postgres;

--
-- TOC entry 2197 (class 1259 OID 339103)
-- Name: gc_predio_catastro; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_predio_catastro (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    tipo_catastro character varying(255),
    numero_predial character varying(30),
    numero_predial_anterior character varying(20),
    circulo_registral character varying(4),
    matricula_inmobiliaria_catastro character varying(80),
    tipo_predio character varying(100),
    condicion_predio bigint,
    destinacion_economica character varying(150),
    estado_alerta character varying(30),
    entidad_emisora_alerta character varying(255),
    fecha_alerta date,
    sistema_procedencia_datos bigint,
    fecha_datos date NOT NULL
);


ALTER TABLE ladm_col_210.gc_predio_catastro OWNER TO postgres;

--
-- TOC entry 12776 (class 0 OID 0)
-- Dependencies: 2197
-- Name: TABLE gc_predio_catastro; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.gc_predio_catastro IS 'Datos del propietario en catastro';


--
-- TOC entry 2198 (class 1259 OID 339110)
-- Name: gc_propietario; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_propietario (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    tipo_documento character varying(100),
    numero_documento character varying(50),
    digito_verificacion character varying(1),
    primer_nombre character varying(255),
    segundo_nombre character varying(255),
    primer_apellido character varying(255),
    segundo_apellido character varying(255),
    razon_social character varying(255),
    gc_predio_catastro bigint NOT NULL
);


ALTER TABLE ladm_col_210.gc_propietario OWNER TO postgres;

--
-- TOC entry 12777 (class 0 OID 0)
-- Dependencies: 2198
-- Name: TABLE gc_propietario; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.gc_propietario IS 'Datos del propietario en catastro';


--
-- TOC entry 2199 (class 1259 OID 339117)
-- Name: gc_sector_rural; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_sector_rural (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    codigo character varying(9),
    geometria public.geometry(MultiPolygon,4326)
);


ALTER TABLE ladm_col_210.gc_sector_rural OWNER TO postgres;

--
-- TOC entry 2200 (class 1259 OID 339124)
-- Name: gc_sector_urbano; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_sector_urbano (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    codigo character varying(9),
    geometria public.geometry(MultiPolygon,4326)
);


ALTER TABLE ladm_col_210.gc_sector_urbano OWNER TO postgres;

--
-- TOC entry 2201 (class 1259 OID 339131)
-- Name: gc_sistemaprocedenciadatostipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_sistemaprocedenciadatostipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.gc_sistemaprocedenciadatostipo OWNER TO postgres;

--
-- TOC entry 2202 (class 1259 OID 339138)
-- Name: gc_terreno; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_terreno (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    area_terreno_alfanumerica numeric(16,2),
    area_terreno_digital numeric(16,2),
    manzana_vereda_codigo character varying(17),
    numero_subterraneos integer,
    geometria public.geometry(MultiPolygon,4326),
    gc_predio bigint NOT NULL,
    CONSTRAINT gc_terreno_area_terreno_alfanumerica_check CHECK (((area_terreno_alfanumerica >= 0.0) AND (area_terreno_alfanumerica <= 99999999999999.98))),
    CONSTRAINT gc_terreno_area_terreno_digital_check CHECK (((area_terreno_digital >= 0.0) AND (area_terreno_digital <= 99999999999999.98))),
    CONSTRAINT gc_terreno_numero_subterraneos_check CHECK (((numero_subterraneos >= 0) AND (numero_subterraneos <= 2147483647)))
);


ALTER TABLE ladm_col_210.gc_terreno OWNER TO postgres;

--
-- TOC entry 12778 (class 0 OID 0)
-- Dependencies: 2202
-- Name: TABLE gc_terreno; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.gc_terreno IS 'Datos del terreno, asociado al predio en catastro';


--
-- TOC entry 2203 (class 1259 OID 339148)
-- Name: gc_unidad_construccion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_unidad_construccion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    identificador character varying(2),
    etiqueta character varying(50),
    tipo_dominio character varying(20),
    tipo_construccion bigint,
    planta character varying(10),
    total_habitaciones integer,
    total_banios integer,
    total_locales integer,
    total_pisos integer,
    uso character varying(255),
    anio_construccion integer,
    puntaje integer,
    area_construida numeric(16,2),
    area_privada numeric(16,2),
    codigo_terreno character varying(30),
    geometria public.geometry(MultiPolygonZ,4326),
    gc_construccion bigint NOT NULL,
    CONSTRAINT gc_unidad_construccion_anio_construccion_check CHECK (((anio_construccion >= 1512) AND (anio_construccion <= 2500))),
    CONSTRAINT gc_unidad_construccion_area_construida_check CHECK (((area_construida >= 0.0) AND (area_construida <= 99999999999999.98))),
    CONSTRAINT gc_unidad_construccion_area_privada_check CHECK (((area_privada >= 0.0) AND (area_privada <= 99999999999999.98))),
    CONSTRAINT gc_unidad_construccion_puntaje_check CHECK (((puntaje >= 0) AND (puntaje <= 200))),
    CONSTRAINT gc_unidad_construccion_total_banios_check CHECK (((total_banios >= 0) AND (total_banios <= 999999))),
    CONSTRAINT gc_unidad_construccion_total_habitaciones_check CHECK (((total_habitaciones >= 0) AND (total_habitaciones <= 999999))),
    CONSTRAINT gc_unidad_construccion_total_locales_check CHECK (((total_locales >= 0) AND (total_locales <= 999999))),
    CONSTRAINT gc_unidad_construccion_total_pisos_check CHECK (((total_pisos >= 0) AND (total_pisos <= 150)))
);


ALTER TABLE ladm_col_210.gc_unidad_construccion OWNER TO postgres;

--
-- TOC entry 2204 (class 1259 OID 339163)
-- Name: gc_unidadconstrucciontipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_unidadconstrucciontipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.gc_unidadconstrucciontipo OWNER TO postgres;

--
-- TOC entry 2205 (class 1259 OID 339170)
-- Name: gc_vereda; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gc_vereda (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    codigo character varying(17),
    codigo_anterior character varying(13),
    nombre character varying(100),
    codigo_sector character varying(9),
    geometria public.geometry(MultiPolygon,4326)
);


ALTER TABLE ladm_col_210.gc_vereda OWNER TO postgres;

--
-- TOC entry 2206 (class 1259 OID 339177)
-- Name: gm_multisurface2d; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gm_multisurface2d (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint
);


ALTER TABLE ladm_col_210.gm_multisurface2d OWNER TO postgres;

--
-- TOC entry 2207 (class 1259 OID 339181)
-- Name: gm_multisurface3d; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gm_multisurface3d (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint
);


ALTER TABLE ladm_col_210.gm_multisurface3d OWNER TO postgres;

--
-- TOC entry 2208 (class 1259 OID 339185)
-- Name: gm_surface2dlistvalue; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gm_surface2dlistvalue (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    avalue public.geometry(Polygon,4326) NOT NULL,
    gm_multisurface2d_geometry bigint
);


ALTER TABLE ladm_col_210.gm_surface2dlistvalue OWNER TO postgres;

--
-- TOC entry 2209 (class 1259 OID 339192)
-- Name: gm_surface3dlistvalue; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.gm_surface3dlistvalue (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    avalue public.geometry(PolygonZ,4326) NOT NULL,
    gm_multisurface3d_geometry bigint
);


ALTER TABLE ladm_col_210.gm_surface3dlistvalue OWNER TO postgres;

--
-- TOC entry 2210 (class 1259 OID 339199)
-- Name: imagen; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.imagen (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    uri character varying(255),
    extinteresado_huella_dactilar bigint,
    extinteresado_fotografia bigint,
    extinteresado_firma bigint
);


ALTER TABLE ladm_col_210.imagen OWNER TO postgres;

--
-- TOC entry 12779 (class 0 OID 0)
-- Dependencies: 2210
-- Name: TABLE imagen; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.imagen IS 'Referencia a una imagen mediante su url.';


--
-- TOC entry 12780 (class 0 OID 0)
-- Dependencies: 2210
-- Name: COLUMN imagen.uri; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.imagen.uri IS 'url de la imagen.';


--
-- TOC entry 2211 (class 1259 OID 339203)
-- Name: ini_predio_insumos; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.ini_predio_insumos (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    gc_predio_catastro bigint,
    snr_predio_juridico bigint
);


ALTER TABLE ladm_col_210.ini_predio_insumos OWNER TO postgres;

--
-- TOC entry 2212 (class 1259 OID 339207)
-- Name: op_acuerdotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_acuerdotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_acuerdotipo OWNER TO postgres;

--
-- TOC entry 2213 (class 1259 OID 339214)
-- Name: op_agrupacion_interesados; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_agrupacion_interesados (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    tipo bigint NOT NULL,
    nombre character varying(255),
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL
);


ALTER TABLE ladm_col_210.op_agrupacion_interesados OWNER TO postgres;

--
-- TOC entry 12781 (class 0 OID 0)
-- Dependencies: 2213
-- Name: COLUMN op_agrupacion_interesados.tipo; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_agrupacion_interesados.tipo IS 'Indica el tipo de agrupación del que se trata.';


--
-- TOC entry 12782 (class 0 OID 0)
-- Dependencies: 2213
-- Name: COLUMN op_agrupacion_interesados.nombre; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_agrupacion_interesados.nombre IS 'Nombre del interesado.';


--
-- TOC entry 12783 (class 0 OID 0)
-- Dependencies: 2213
-- Name: COLUMN op_agrupacion_interesados.comienzo_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_agrupacion_interesados.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 12784 (class 0 OID 0)
-- Dependencies: 2213
-- Name: COLUMN op_agrupacion_interesados.fin_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_agrupacion_interesados.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 2214 (class 1259 OID 339222)
-- Name: op_condicionprediotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_condicionprediotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_condicionprediotipo OWNER TO postgres;

--
-- TOC entry 2215 (class 1259 OID 339229)
-- Name: op_construccion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_construccion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    identificador character varying(2),
    tipo_construccion bigint,
    tipo_dominio bigint,
    numero_pisos integer NOT NULL,
    numero_sotanos integer,
    numero_mezanines integer,
    numero_semisotanos integer,
    codigo_edificacion integer,
    area_construccion numeric(15,1) NOT NULL,
    altura integer,
    avaluo_construccion numeric(16,1),
    dimension bigint,
    etiqueta character varying(255),
    relacion_superficie bigint,
    geometria public.geometry(MultiPolygonZ,4326),
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL,
    CONSTRAINT op_construccion_altura_check CHECK (((altura >= 1) AND (altura <= 1000))),
    CONSTRAINT op_construccion_area_construccion_check CHECK (((area_construccion >= 0.0) AND (area_construccion <= 99999999999999.9))),
    CONSTRAINT op_construccion_avaluo_construccion_check CHECK (((avaluo_construccion >= 0.0) AND (avaluo_construccion <= '999999999999999'::numeric))),
    CONSTRAINT op_construccion_codigo_edificacion_check CHECK (((codigo_edificacion >= 0) AND (codigo_edificacion <= 2147483647))),
    CONSTRAINT op_construccion_numero_mezanines_check CHECK (((numero_mezanines >= 0) AND (numero_mezanines <= 99))),
    CONSTRAINT op_construccion_numero_pisos_check CHECK (((numero_pisos >= 1) AND (numero_pisos <= 100))),
    CONSTRAINT op_construccion_numero_semisotanos_check CHECK (((numero_semisotanos >= 0) AND (numero_semisotanos <= 99))),
    CONSTRAINT op_construccion_numero_sotanos_check CHECK (((numero_sotanos >= 0) AND (numero_sotanos <= 99)))
);


ALTER TABLE ladm_col_210.op_construccion OWNER TO postgres;

--
-- TOC entry 12785 (class 0 OID 0)
-- Dependencies: 2215
-- Name: TABLE op_construccion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.op_construccion IS 'Es un tipo de espacio jurídico de la unidad de edificación del modelo LADM que almacena datos específicos del avalúo resultante del mismo.';


--
-- TOC entry 12786 (class 0 OID 0)
-- Dependencies: 2215
-- Name: COLUMN op_construccion.numero_pisos; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_construccion.numero_pisos IS 'Cantidad de plantas que tiene la construcción';


--
-- TOC entry 12787 (class 0 OID 0)
-- Dependencies: 2215
-- Name: COLUMN op_construccion.avaluo_construccion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_construccion.avaluo_construccion IS 'Rsultado del cálculo de su avalúo mediante la metodología legalmente establecida.';


--
-- TOC entry 12788 (class 0 OID 0)
-- Dependencies: 2215
-- Name: COLUMN op_construccion.etiqueta; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_construccion.etiqueta IS 'Corresponde al atributo label de la clase en LADM.';


--
-- TOC entry 12789 (class 0 OID 0)
-- Dependencies: 2215
-- Name: COLUMN op_construccion.relacion_superficie; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_construccion.relacion_superficie IS 'Corresponde al atributo surfaceRelation de la clase en LADM.';


--
-- TOC entry 12790 (class 0 OID 0)
-- Dependencies: 2215
-- Name: COLUMN op_construccion.geometria; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_construccion.geometria IS 'Materializacion del metodo createArea(). Almacena de forma permanente la geometría de tipo poligonal.';


--
-- TOC entry 12791 (class 0 OID 0)
-- Dependencies: 2215
-- Name: COLUMN op_construccion.comienzo_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_construccion.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 12792 (class 0 OID 0)
-- Dependencies: 2215
-- Name: COLUMN op_construccion.fin_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_construccion.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 2216 (class 1259 OID 339245)
-- Name: op_construccionplantatipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_construccionplantatipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_construccionplantatipo OWNER TO postgres;

--
-- TOC entry 2217 (class 1259 OID 339252)
-- Name: op_construcciontipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_construcciontipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_construcciontipo OWNER TO postgres;

--
-- TOC entry 2218 (class 1259 OID 339259)
-- Name: op_datos_ph_condominio; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_datos_ph_condominio (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    area_total_terreno numeric(16,2),
    area_total_terreno_privada numeric(16,2),
    area_total_terreno_comun numeric(16,2),
    area_total_construida numeric(16,2),
    area_total_construida_privada numeric(16,2),
    area_total_construida_comun numeric(16,2),
    torre_no character varying(10),
    total_pisos_torre integer,
    total_unidades_privadas integer,
    total_sotanos integer,
    total_unidades_sotanos integer,
    op_predio bigint NOT NULL,
    CONSTRAINT op_datos_ph_condominio_area_total_constrd_prvada_check CHECK (((area_total_construida_privada >= 0.0) AND (area_total_construida_privada <= 99999999999999.98))),
    CONSTRAINT op_datos_ph_condominio_area_total_construid_cmun_check CHECK (((area_total_construida_comun >= 0.0) AND (area_total_construida_comun <= 99999999999999.98))),
    CONSTRAINT op_datos_ph_condominio_area_total_construida_check CHECK (((area_total_construida >= 0.0) AND (area_total_construida <= 99999999999999.98))),
    CONSTRAINT op_datos_ph_condominio_area_total_terreno_check CHECK (((area_total_terreno >= 0.0) AND (area_total_terreno <= 99999999999999.98))),
    CONSTRAINT op_datos_ph_condominio_area_total_terreno_comun_check CHECK (((area_total_terreno_comun >= 0.0) AND (area_total_terreno_comun <= 99999999999999.98))),
    CONSTRAINT op_datos_ph_condominio_area_total_terreno_prvada_check CHECK (((area_total_terreno_privada >= 0.0) AND (area_total_terreno_privada <= 99999999999999.98))),
    CONSTRAINT op_datos_ph_condominio_total_pisos_torre_check CHECK (((total_pisos_torre >= 0) AND (total_pisos_torre <= 200))),
    CONSTRAINT op_datos_ph_condominio_total_sotanos_check CHECK (((total_sotanos >= 0) AND (total_sotanos <= 30))),
    CONSTRAINT op_datos_ph_condominio_total_unidades_privadas_check CHECK (((total_unidades_privadas >= 0) AND (total_unidades_privadas <= 99999999))),
    CONSTRAINT op_datos_ph_condominio_total_unidades_sotanos_check CHECK (((total_unidades_sotanos >= 0) AND (total_unidades_sotanos <= 99999999)))
);


ALTER TABLE ladm_col_210.op_datos_ph_condominio OWNER TO postgres;

--
-- TOC entry 2219 (class 1259 OID 339274)
-- Name: op_derecho; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_derecho (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    tipo bigint,
    descripcion character varying(255),
    comprobacion_comparte boolean,
    uso_efectivo character varying(255),
    interesado_op_interesado bigint,
    interesado_op_agrupacion_interesados bigint,
    unidad bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL
);


ALTER TABLE ladm_col_210.op_derecho OWNER TO postgres;

--
-- TOC entry 12793 (class 0 OID 0)
-- Dependencies: 2219
-- Name: TABLE op_derecho; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.op_derecho IS 'Clase que registra las instancias de los derechos que un interesado ejerce sobre un predio. Es una especialización de la clase LA_RRR del propio modelo.';


--
-- TOC entry 12794 (class 0 OID 0)
-- Dependencies: 2219
-- Name: COLUMN op_derecho.tipo; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_derecho.tipo IS 'Derecho que se ejerce.';


--
-- TOC entry 12795 (class 0 OID 0)
-- Dependencies: 2219
-- Name: COLUMN op_derecho.descripcion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_derecho.descripcion IS 'Descripción relatical al derecho, la responsabilidad o la restricción.';


--
-- TOC entry 12796 (class 0 OID 0)
-- Dependencies: 2219
-- Name: COLUMN op_derecho.comprobacion_comparte; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_derecho.comprobacion_comparte IS 'Indicación de si se activa el constraint (a+b+...+n=100%) de la fracción Compartido.';


--
-- TOC entry 12797 (class 0 OID 0)
-- Dependencies: 2219
-- Name: COLUMN op_derecho.uso_efectivo; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_derecho.uso_efectivo IS 'Descripción de cual es el uso efectivo.';


--
-- TOC entry 12798 (class 0 OID 0)
-- Dependencies: 2219
-- Name: COLUMN op_derecho.comienzo_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_derecho.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 12799 (class 0 OID 0)
-- Dependencies: 2219
-- Name: COLUMN op_derecho.fin_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_derecho.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 2220 (class 1259 OID 339282)
-- Name: op_derechotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_derechotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_derechotipo OWNER TO postgres;

--
-- TOC entry 2221 (class 1259 OID 339289)
-- Name: op_dominioconstrucciontipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_dominioconstrucciontipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_dominioconstrucciontipo OWNER TO postgres;

--
-- TOC entry 2222 (class 1259 OID 339296)
-- Name: op_fotoidentificaciontipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_fotoidentificaciontipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_fotoidentificaciontipo OWNER TO postgres;

--
-- TOC entry 2223 (class 1259 OID 339303)
-- Name: op_fuenteadministrativa; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_fuenteadministrativa (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    tipo bigint NOT NULL,
    ente_emisor character varying(255),
    observacion character varying(255),
    numero_fuente character varying(150),
    estado_disponibilidad bigint NOT NULL,
    tipo_principal bigint,
    fecha_documento_fuente date,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL
);


ALTER TABLE ladm_col_210.op_fuenteadministrativa OWNER TO postgres;

--
-- TOC entry 12800 (class 0 OID 0)
-- Dependencies: 2223
-- Name: COLUMN op_fuenteadministrativa.observacion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_fuenteadministrativa.observacion IS 'Descripción del documento.';


--
-- TOC entry 12801 (class 0 OID 0)
-- Dependencies: 2223
-- Name: COLUMN op_fuenteadministrativa.numero_fuente; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_fuenteadministrativa.numero_fuente IS 'Identificador del documento, ejemplo: numero de la resolución';


--
-- TOC entry 12802 (class 0 OID 0)
-- Dependencies: 2223
-- Name: COLUMN op_fuenteadministrativa.estado_disponibilidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_fuenteadministrativa.estado_disponibilidad IS 'Indica si la fuente está o no disponible y en qué condiciones. También puede indicar porqué ha dejado de estar disponible, si ha ocurrido.';


--
-- TOC entry 12803 (class 0 OID 0)
-- Dependencies: 2223
-- Name: COLUMN op_fuenteadministrativa.tipo_principal; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_fuenteadministrativa.tipo_principal IS 'Tipo de formato en el que es presentada la fuente, de acuerdo con el registro de metadatos.';


--
-- TOC entry 2224 (class 1259 OID 339311)
-- Name: op_fuenteadministrativatipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_fuenteadministrativatipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_fuenteadministrativatipo OWNER TO postgres;

--
-- TOC entry 2225 (class 1259 OID 339318)
-- Name: op_fuenteespacial; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_fuenteespacial (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    nombre character varying(255) NOT NULL,
    tipo bigint NOT NULL,
    descripcion text NOT NULL,
    metadato text,
    estado_disponibilidad bigint NOT NULL,
    tipo_principal bigint,
    fecha_documento_fuente date,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL
);


ALTER TABLE ladm_col_210.op_fuenteespacial OWNER TO postgres;

--
-- TOC entry 12804 (class 0 OID 0)
-- Dependencies: 2225
-- Name: COLUMN op_fuenteespacial.estado_disponibilidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_fuenteespacial.estado_disponibilidad IS 'Indica si la fuente está o no disponible y en qué condiciones. También puede indicar porqué ha dejado de estar disponible, si ha ocurrido.';


--
-- TOC entry 12805 (class 0 OID 0)
-- Dependencies: 2225
-- Name: COLUMN op_fuenteespacial.tipo_principal; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_fuenteespacial.tipo_principal IS 'Tipo de formato en el que es presentada la fuente, de acuerdo con el registro de metadatos.';


--
-- TOC entry 2226 (class 1259 OID 339326)
-- Name: op_grupoetnicotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_grupoetnicotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_grupoetnicotipo OWNER TO postgres;

--
-- TOC entry 2227 (class 1259 OID 339333)
-- Name: op_interesado; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_interesado (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    tipo bigint NOT NULL,
    tipo_documento bigint NOT NULL,
    documento_identidad character varying(50) NOT NULL,
    primer_nombre character varying(100),
    segundo_nombre character varying(100),
    primer_apellido character varying(100),
    segundo_apellido character varying(100),
    sexo bigint,
    grupo_etnico bigint,
    razon_social character varying(255),
    nombre character varying(255),
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL
);


ALTER TABLE ladm_col_210.op_interesado OWNER TO postgres;

--
-- TOC entry 12806 (class 0 OID 0)
-- Dependencies: 2227
-- Name: COLUMN op_interesado.tipo; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_interesado.tipo IS 'Tipo de persona del que se trata';


--
-- TOC entry 12807 (class 0 OID 0)
-- Dependencies: 2227
-- Name: COLUMN op_interesado.tipo_documento; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_interesado.tipo_documento IS 'Tipo de documento del que se trata.';


--
-- TOC entry 12808 (class 0 OID 0)
-- Dependencies: 2227
-- Name: COLUMN op_interesado.documento_identidad; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_interesado.documento_identidad IS 'Documento de identidad del interesado.';


--
-- TOC entry 12809 (class 0 OID 0)
-- Dependencies: 2227
-- Name: COLUMN op_interesado.primer_nombre; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_interesado.primer_nombre IS 'Primer nombre de la persona física.';


--
-- TOC entry 12810 (class 0 OID 0)
-- Dependencies: 2227
-- Name: COLUMN op_interesado.segundo_nombre; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_interesado.segundo_nombre IS 'Segundo nombre de la persona física.';


--
-- TOC entry 12811 (class 0 OID 0)
-- Dependencies: 2227
-- Name: COLUMN op_interesado.primer_apellido; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_interesado.primer_apellido IS 'Primer apellido de la persona física.';


--
-- TOC entry 12812 (class 0 OID 0)
-- Dependencies: 2227
-- Name: COLUMN op_interesado.segundo_apellido; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_interesado.segundo_apellido IS 'Segundo apellido de la persona física.';


--
-- TOC entry 12813 (class 0 OID 0)
-- Dependencies: 2227
-- Name: COLUMN op_interesado.razon_social; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_interesado.razon_social IS 'Nombre con el que está inscrito.';


--
-- TOC entry 12814 (class 0 OID 0)
-- Dependencies: 2227
-- Name: COLUMN op_interesado.nombre; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_interesado.nombre IS 'Nombre del interesado.';


--
-- TOC entry 12815 (class 0 OID 0)
-- Dependencies: 2227
-- Name: COLUMN op_interesado.comienzo_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_interesado.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 12816 (class 0 OID 0)
-- Dependencies: 2227
-- Name: COLUMN op_interesado.fin_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_interesado.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 2228 (class 1259 OID 339341)
-- Name: op_interesado_contacto; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_interesado_contacto (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    telefono1 character varying(20),
    telefono2 character varying(20),
    domicilio_notificacion character varying(500),
    direccion_residencia character varying(500),
    correo_electronico character varying(100),
    autoriza_notificacion_correo boolean,
    departamento character varying(100) NOT NULL,
    municipio character varying(100) NOT NULL,
    vereda character varying(100),
    corregimiento character varying(100),
    op_interesado bigint NOT NULL
);


ALTER TABLE ladm_col_210.op_interesado_contacto OWNER TO postgres;

--
-- TOC entry 12817 (class 0 OID 0)
-- Dependencies: 2228
-- Name: COLUMN op_interesado_contacto.autoriza_notificacion_correo; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_interesado_contacto.autoriza_notificacion_correo IS 'Indica si el interesado autoriza notificación vía correo electrónico';


--
-- TOC entry 2229 (class 1259 OID 339349)
-- Name: op_interesadodocumentotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_interesadodocumentotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_interesadodocumentotipo OWNER TO postgres;

--
-- TOC entry 2230 (class 1259 OID 339356)
-- Name: op_interesadotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_interesadotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_interesadotipo OWNER TO postgres;

--
-- TOC entry 2231 (class 1259 OID 339363)
-- Name: op_lindero; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_lindero (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    longitud numeric(6,1) NOT NULL,
    geometria public.geometry(LineStringZ,4326),
    localizacion_textual character varying(255),
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL,
    CONSTRAINT op_lindero_longitud_check CHECK (((longitud >= 0.0) AND (longitud <= 10000.0)))
);


ALTER TABLE ladm_col_210.op_lindero OWNER TO postgres;

--
-- TOC entry 12818 (class 0 OID 0)
-- Dependencies: 2231
-- Name: TABLE op_lindero; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.op_lindero IS 'Clase especializada de LA_CadenaCarasLindero que permite registrar los linderos.
Dos linderos no pueden cruzarse ni superponerse.';


--
-- TOC entry 12819 (class 0 OID 0)
-- Dependencies: 2231
-- Name: COLUMN op_lindero.longitud; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_lindero.longitud IS 'Lóngitud en m del lindero.';


--
-- TOC entry 12820 (class 0 OID 0)
-- Dependencies: 2231
-- Name: COLUMN op_lindero.geometria; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_lindero.geometria IS 'Geometría lineal que define el lindero. Puede estar asociada a geometrías de tipo punto que definen sus vértices o ser una entidad lineal independiente.';


--
-- TOC entry 12821 (class 0 OID 0)
-- Dependencies: 2231
-- Name: COLUMN op_lindero.localizacion_textual; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_lindero.localizacion_textual IS 'Descripción de la localización, cuando esta se basa en texto.';


--
-- TOC entry 12822 (class 0 OID 0)
-- Dependencies: 2231
-- Name: COLUMN op_lindero.comienzo_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_lindero.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 12823 (class 0 OID 0)
-- Dependencies: 2231
-- Name: COLUMN op_lindero.fin_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_lindero.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 2232 (class 1259 OID 339372)
-- Name: op_predio; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_predio (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    departamento character varying(2) NOT NULL,
    municipio character varying(3) NOT NULL,
    id_operacion character varying(30) NOT NULL,
    tiene_fmi boolean NOT NULL,
    codigo_orip character varying(3),
    matricula_inmobiliaria character varying(80),
    numero_predial character varying(30),
    numero_predial_anterior character varying(20),
    avaluo_catastral numeric(16,1),
    condicion_predio bigint NOT NULL,
    direccion character varying(255) NOT NULL,
    nombre character varying(255),
    tipo bigint NOT NULL,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL,
    CONSTRAINT op_predio_avaluo_catastral_check CHECK (((avaluo_catastral >= 0.0) AND (avaluo_catastral <= '999999999999999'::numeric)))
);


ALTER TABLE ladm_col_210.op_predio OWNER TO postgres;

--
-- TOC entry 12824 (class 0 OID 0)
-- Dependencies: 2232
-- Name: TABLE op_predio; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.op_predio IS 'Clase especializada de BaUnit, que describe la unidad administrativa básica para el caso de Colombia.
El predio es la unidad territorial legal propia de Catastro. Esta formada por el terreno y puede o no tener construcciones asociadas.';


--
-- TOC entry 12825 (class 0 OID 0)
-- Dependencies: 2232
-- Name: COLUMN op_predio.departamento; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_predio.departamento IS 'Corresponde al codigo del departamento al cual pertenece el predio. Es asignado por DIVIPOLA y tiene 2 dígitos.';


--
-- TOC entry 12826 (class 0 OID 0)
-- Dependencies: 2232
-- Name: COLUMN op_predio.municipio; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_predio.municipio IS 'Corresponde al codigo del municipio al cual pertenece el predio. Es asignado por DIVIPOLA y tiene 3 dígitos.';


--
-- TOC entry 12827 (class 0 OID 0)
-- Dependencies: 2232
-- Name: COLUMN op_predio.id_operacion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_predio.id_operacion IS 'Numero Unico de identificación Predial. Es el codigo definido en el proyecto de ley que será el codigo de identificación del predio tanto para catastratro como para Registro.';


--
-- TOC entry 12828 (class 0 OID 0)
-- Dependencies: 2232
-- Name: COLUMN op_predio.codigo_orip; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_predio.codigo_orip IS 'Circulo registral';


--
-- TOC entry 12829 (class 0 OID 0)
-- Dependencies: 2232
-- Name: COLUMN op_predio.matricula_inmobiliaria; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_predio.matricula_inmobiliaria IS 'Matricula inmobiliaria';


--
-- TOC entry 12830 (class 0 OID 0)
-- Dependencies: 2232
-- Name: COLUMN op_predio.numero_predial; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_predio.numero_predial IS 'Nuevo código númerico de treinta (30) dígitos, que se le asigna a cada predio y busca localizarlo inequívocamente en los documentos catastrales, según el modelo determinado por el Instituto Geográfico Agustin Codazzi.';


--
-- TOC entry 12831 (class 0 OID 0)
-- Dependencies: 2232
-- Name: COLUMN op_predio.numero_predial_anterior; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_predio.numero_predial_anterior IS 'Anterior código númerico de veinte (20) digitos, que se le asigna a cada predio y busca localizarlo inequívocamente en los documentos catastrales, según el modelo determinado por el Instituto Geográfico Agustin Codazzi.';


--
-- TOC entry 12832 (class 0 OID 0)
-- Dependencies: 2232
-- Name: COLUMN op_predio.avaluo_catastral; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_predio.avaluo_catastral IS 'Valor de cada predio, obtenido mediante investigación y análisis estadistico del mercado inmobiliario y la metodología de aplicación  correspondiente. El avalúo  catastral de cada predio se determina a partir de la adición de los avalúos parciales practicados independientemente para los terrenos y para las edificaciones en el comprendidos.';


--
-- TOC entry 12833 (class 0 OID 0)
-- Dependencies: 2232
-- Name: COLUMN op_predio.nombre; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_predio.nombre IS 'Nombre que recibe la unidad administrativa básica, en muchos casos toponímico, especialmente en terrenos rústicos.';


--
-- TOC entry 12834 (class 0 OID 0)
-- Dependencies: 2232
-- Name: COLUMN op_predio.tipo; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_predio.tipo IS 'Tipo de derecho que la reconoce.';


--
-- TOC entry 12835 (class 0 OID 0)
-- Dependencies: 2232
-- Name: COLUMN op_predio.comienzo_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_predio.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 12836 (class 0 OID 0)
-- Dependencies: 2232
-- Name: COLUMN op_predio.fin_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_predio.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 2233 (class 1259 OID 339381)
-- Name: op_predio_copropiedad; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_predio_copropiedad (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    predio bigint NOT NULL,
    copropiedad bigint NOT NULL
);


ALTER TABLE ladm_col_210.op_predio_copropiedad OWNER TO postgres;

--
-- TOC entry 2234 (class 1259 OID 339385)
-- Name: op_predio_insumos_operacion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_predio_insumos_operacion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ini_predio_insumos bigint NOT NULL,
    op_predio bigint NOT NULL
);


ALTER TABLE ladm_col_210.op_predio_insumos_operacion OWNER TO postgres;

--
-- TOC entry 2235 (class 1259 OID 339389)
-- Name: op_puntocontrol; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_puntocontrol (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    id_punto_control character varying(255) NOT NULL,
    puntotipo bigint NOT NULL,
    tipo_punto_control bigint,
    exactitud_horizontal integer NOT NULL,
    exactitud_vertical integer NOT NULL,
    posicion_interpolacion bigint,
    metodoproduccion bigint,
    geometria public.geometry(PointZ,4326) NOT NULL,
    ue_op_construccion bigint,
    ue_op_terreno bigint,
    ue_op_servidumbretransito bigint,
    ue_op_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL,
    CONSTRAINT op_puntocontrol_exactitud_horizontal_check CHECK (((exactitud_horizontal >= 0) AND (exactitud_horizontal <= 1000))),
    CONSTRAINT op_puntocontrol_exactitud_vertical_check CHECK (((exactitud_vertical >= 0) AND (exactitud_vertical <= 1000)))
);


ALTER TABLE ladm_col_210.op_puntocontrol OWNER TO postgres;

--
-- TOC entry 12837 (class 0 OID 0)
-- Dependencies: 2235
-- Name: TABLE op_puntocontrol; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.op_puntocontrol IS 'Clase especializada de LA_Punto que representa puntos de la densificación de la red local, que se utiliza en la operación catastral para el levantamiento de información fisica de los objetos territoriales, como puntos de control.';


--
-- TOC entry 12838 (class 0 OID 0)
-- Dependencies: 2235
-- Name: COLUMN op_puntocontrol.id_punto_control; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntocontrol.id_punto_control IS 'Nombre que recibe el punto.';


--
-- TOC entry 12839 (class 0 OID 0)
-- Dependencies: 2235
-- Name: COLUMN op_puntocontrol.tipo_punto_control; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntocontrol.tipo_punto_control IS 'Si se trata deun punto de control o de apoyo.';


--
-- TOC entry 12840 (class 0 OID 0)
-- Dependencies: 2235
-- Name: COLUMN op_puntocontrol.exactitud_horizontal; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntocontrol.exactitud_horizontal IS 'Exactitud horizontal de la medición del punto.';


--
-- TOC entry 12841 (class 0 OID 0)
-- Dependencies: 2235
-- Name: COLUMN op_puntocontrol.exactitud_vertical; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntocontrol.exactitud_vertical IS 'Exactitud vertical de la medición del punto.';


--
-- TOC entry 12842 (class 0 OID 0)
-- Dependencies: 2235
-- Name: COLUMN op_puntocontrol.comienzo_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntocontrol.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 12843 (class 0 OID 0)
-- Dependencies: 2235
-- Name: COLUMN op_puntocontrol.fin_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntocontrol.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 2236 (class 1259 OID 339399)
-- Name: op_puntocontroltipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_puntocontroltipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_puntocontroltipo OWNER TO postgres;

--
-- TOC entry 2237 (class 1259 OID 339406)
-- Name: op_puntolevantamiento; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_puntolevantamiento (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    id_punto_levantamiento character varying(255),
    puntotipo bigint NOT NULL,
    tipo_punto_levantamiento bigint,
    fotoidentificacion bigint,
    exactitud_horizontal integer NOT NULL,
    exactitud_vertical integer,
    posicion_interpolacion bigint,
    metodoproduccion bigint,
    geometria public.geometry(PointZ,4326) NOT NULL,
    ue_op_construccion bigint,
    ue_op_terreno bigint,
    ue_op_servidumbretransito bigint,
    ue_op_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL,
    CONSTRAINT op_puntolevantamiento_exactitud_horizontal_check CHECK (((exactitud_horizontal >= 0) AND (exactitud_horizontal <= 1000))),
    CONSTRAINT op_puntolevantamiento_exactitud_vertical_check CHECK (((exactitud_vertical >= 0) AND (exactitud_vertical <= 1000)))
);


ALTER TABLE ladm_col_210.op_puntolevantamiento OWNER TO postgres;

--
-- TOC entry 12844 (class 0 OID 0)
-- Dependencies: 2237
-- Name: TABLE op_puntolevantamiento; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.op_puntolevantamiento IS 'Clase especializada de LA_Punto que representa puntos demarcados que representan la posición horizontal de un vértice de construcción, servidumbre o auxiliare.';


--
-- TOC entry 12845 (class 0 OID 0)
-- Dependencies: 2237
-- Name: COLUMN op_puntolevantamiento.id_punto_levantamiento; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntolevantamiento.id_punto_levantamiento IS 'Se caracterizan los diferentes tipos de punto levantamiento, estos son punto de construccción, punto de servidumbre o punto auxiliar';


--
-- TOC entry 12846 (class 0 OID 0)
-- Dependencies: 2237
-- Name: COLUMN op_puntolevantamiento.exactitud_horizontal; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntolevantamiento.exactitud_horizontal IS 'Corresponde a la exactitud horizontal del punto levantamiento';


--
-- TOC entry 12847 (class 0 OID 0)
-- Dependencies: 2237
-- Name: COLUMN op_puntolevantamiento.exactitud_vertical; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntolevantamiento.exactitud_vertical IS 'Corresponde a la exactitud vertical del punto levantamiento';


--
-- TOC entry 12848 (class 0 OID 0)
-- Dependencies: 2237
-- Name: COLUMN op_puntolevantamiento.comienzo_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntolevantamiento.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 12849 (class 0 OID 0)
-- Dependencies: 2237
-- Name: COLUMN op_puntolevantamiento.fin_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntolevantamiento.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 2238 (class 1259 OID 339416)
-- Name: op_puntolevtipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_puntolevtipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_puntolevtipo OWNER TO postgres;

--
-- TOC entry 2239 (class 1259 OID 339423)
-- Name: op_puntolindero; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_puntolindero (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    id_punto_lindero character varying(255),
    puntotipo bigint NOT NULL,
    acuerdo bigint NOT NULL,
    fotoidentificacion bigint,
    ubicacion_punto bigint,
    exactitud_horizontal integer NOT NULL,
    exactitud_vertical integer,
    posicion_interpolacion bigint,
    metodoproduccion bigint,
    geometria public.geometry(PointZ,4326) NOT NULL,
    ue_op_construccion bigint,
    ue_op_terreno bigint,
    ue_op_servidumbretransito bigint,
    ue_op_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL,
    CONSTRAINT op_puntolindero_exactitud_horizontal_check CHECK (((exactitud_horizontal >= 0) AND (exactitud_horizontal <= 1000))),
    CONSTRAINT op_puntolindero_exactitud_vertical_check CHECK (((exactitud_vertical >= 0) AND (exactitud_vertical <= 1000)))
);


ALTER TABLE ladm_col_210.op_puntolindero OWNER TO postgres;

--
-- TOC entry 12850 (class 0 OID 0)
-- Dependencies: 2239
-- Name: TABLE op_puntolindero; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.op_puntolindero IS 'Clase especializada de LA_Punto que almacena puntos que definen un lindero, instancia de la clase LA_CadenaCarasLindero y sus especializaciones.';


--
-- TOC entry 12851 (class 0 OID 0)
-- Dependencies: 2239
-- Name: COLUMN op_puntolindero.id_punto_lindero; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntolindero.id_punto_lindero IS 'Nombre o codigo del punto lindero';


--
-- TOC entry 12852 (class 0 OID 0)
-- Dependencies: 2239
-- Name: COLUMN op_puntolindero.acuerdo; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntolindero.acuerdo IS 'Se Indica si existe acuerdo o no entre los colindantes en relación al punto lindero que se está midiendo.';


--
-- TOC entry 12853 (class 0 OID 0)
-- Dependencies: 2239
-- Name: COLUMN op_puntolindero.exactitud_horizontal; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntolindero.exactitud_horizontal IS 'Corresponde a la exactitud horizontal del punto lindero';


--
-- TOC entry 12854 (class 0 OID 0)
-- Dependencies: 2239
-- Name: COLUMN op_puntolindero.exactitud_vertical; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntolindero.exactitud_vertical IS 'Corresponde a la exactitud vertical del punto lindero';


--
-- TOC entry 12855 (class 0 OID 0)
-- Dependencies: 2239
-- Name: COLUMN op_puntolindero.comienzo_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntolindero.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 12856 (class 0 OID 0)
-- Dependencies: 2239
-- Name: COLUMN op_puntolindero.fin_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_puntolindero.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 2240 (class 1259 OID 339433)
-- Name: op_puntotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_puntotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_puntotipo OWNER TO postgres;

--
-- TOC entry 2241 (class 1259 OID 339440)
-- Name: op_restriccion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_restriccion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    tipo bigint NOT NULL,
    descripcion character varying(255),
    comprobacion_comparte boolean,
    uso_efectivo character varying(255),
    interesado_op_interesado bigint,
    interesado_op_agrupacion_interesados bigint,
    unidad bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL
);


ALTER TABLE ladm_col_210.op_restriccion OWNER TO postgres;

--
-- TOC entry 12857 (class 0 OID 0)
-- Dependencies: 2241
-- Name: COLUMN op_restriccion.descripcion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_restriccion.descripcion IS 'Descripción relatical al derecho, la responsabilidad o la restricción.';


--
-- TOC entry 12858 (class 0 OID 0)
-- Dependencies: 2241
-- Name: COLUMN op_restriccion.comprobacion_comparte; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_restriccion.comprobacion_comparte IS 'Indicación de si se activa el constraint (a+b+...+n=100%) de la fracción Compartido.';


--
-- TOC entry 12859 (class 0 OID 0)
-- Dependencies: 2241
-- Name: COLUMN op_restriccion.uso_efectivo; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_restriccion.uso_efectivo IS 'Descripción de cual es el uso efectivo.';


--
-- TOC entry 12860 (class 0 OID 0)
-- Dependencies: 2241
-- Name: COLUMN op_restriccion.comienzo_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_restriccion.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 12861 (class 0 OID 0)
-- Dependencies: 2241
-- Name: COLUMN op_restriccion.fin_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_restriccion.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 2242 (class 1259 OID 339448)
-- Name: op_restricciontipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_restricciontipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_restricciontipo OWNER TO postgres;

--
-- TOC entry 2243 (class 1259 OID 339455)
-- Name: op_servidumbretransito; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_servidumbretransito (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    area_servidumbre numeric(15,1) NOT NULL,
    dimension bigint,
    etiqueta character varying(255),
    relacion_superficie bigint,
    geometria public.geometry(MultiPolygonZ,4326),
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL,
    CONSTRAINT op_servidumbretransito_area_servidumbre_check CHECK (((area_servidumbre >= 0.0) AND (area_servidumbre <= 99999999999999.9)))
);


ALTER TABLE ladm_col_210.op_servidumbretransito OWNER TO postgres;

--
-- TOC entry 12862 (class 0 OID 0)
-- Dependencies: 2243
-- Name: TABLE op_servidumbretransito; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.op_servidumbretransito IS 'Tipo de unidad espacial que permite la representación de una servidumbre de paso asociada a una LA_BAUnit.';


--
-- TOC entry 12863 (class 0 OID 0)
-- Dependencies: 2243
-- Name: COLUMN op_servidumbretransito.area_servidumbre; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_servidumbretransito.area_servidumbre IS 'Fecha de inscripción de la servidumbre en el Catastro.';


--
-- TOC entry 12864 (class 0 OID 0)
-- Dependencies: 2243
-- Name: COLUMN op_servidumbretransito.etiqueta; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_servidumbretransito.etiqueta IS 'Corresponde al atributo label de la clase en LADM.';


--
-- TOC entry 12865 (class 0 OID 0)
-- Dependencies: 2243
-- Name: COLUMN op_servidumbretransito.relacion_superficie; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_servidumbretransito.relacion_superficie IS 'Corresponde al atributo surfaceRelation de la clase en LADM.';


--
-- TOC entry 12866 (class 0 OID 0)
-- Dependencies: 2243
-- Name: COLUMN op_servidumbretransito.geometria; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_servidumbretransito.geometria IS 'Materializacion del metodo createArea(). Almacena de forma permanente la geometría de tipo poligonal.';


--
-- TOC entry 12867 (class 0 OID 0)
-- Dependencies: 2243
-- Name: COLUMN op_servidumbretransito.comienzo_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_servidumbretransito.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 12868 (class 0 OID 0)
-- Dependencies: 2243
-- Name: COLUMN op_servidumbretransito.fin_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_servidumbretransito.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 2244 (class 1259 OID 339464)
-- Name: op_sexotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_sexotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_sexotipo OWNER TO postgres;

--
-- TOC entry 2245 (class 1259 OID 339471)
-- Name: op_terreno; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_terreno (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    area_terreno numeric(15,1) NOT NULL,
    avaluo_terreno numeric(16,1),
    manzana_vereda_codigo character varying(17),
    numero_subterraneos integer,
    geometria public.geometry(MultiPolygonZ,4326) NOT NULL,
    dimension bigint,
    etiqueta character varying(255),
    relacion_superficie bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL,
    CONSTRAINT op_terreno_area_terreno_check CHECK (((area_terreno >= 0.0) AND (area_terreno <= 99999999999999.9))),
    CONSTRAINT op_terreno_avaluo_terreno_check CHECK (((avaluo_terreno >= 0.0) AND (avaluo_terreno <= '999999999999999'::numeric))),
    CONSTRAINT op_terreno_numero_subterraneos_check CHECK (((numero_subterraneos >= 0) AND (numero_subterraneos <= 999)))
);


ALTER TABLE ladm_col_210.op_terreno OWNER TO postgres;

--
-- TOC entry 12869 (class 0 OID 0)
-- Dependencies: 2245
-- Name: TABLE op_terreno; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.op_terreno IS 'Porción de tierra con una extensión geográfica definida.';


--
-- TOC entry 12870 (class 0 OID 0)
-- Dependencies: 2245
-- Name: COLUMN op_terreno.area_terreno; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_terreno.area_terreno IS 'Área de predio resultado de los calculos realizados en el proceso de levantamiento planimetrico';


--
-- TOC entry 12871 (class 0 OID 0)
-- Dependencies: 2245
-- Name: COLUMN op_terreno.avaluo_terreno; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_terreno.avaluo_terreno IS 'Valor asignado en el proceso de valoración economica masiva al terreno del predio';


--
-- TOC entry 12872 (class 0 OID 0)
-- Dependencies: 2245
-- Name: COLUMN op_terreno.geometria; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_terreno.geometria IS 'Corresponde a la figura geometrica vectorial poligonal, generada a partir de los linderos del predio.';


--
-- TOC entry 12873 (class 0 OID 0)
-- Dependencies: 2245
-- Name: COLUMN op_terreno.etiqueta; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_terreno.etiqueta IS 'Corresponde al atributo label de la clase en LADM.';


--
-- TOC entry 12874 (class 0 OID 0)
-- Dependencies: 2245
-- Name: COLUMN op_terreno.relacion_superficie; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_terreno.relacion_superficie IS 'Corresponde al atributo surfaceRelation de la clase en LADM.';


--
-- TOC entry 12875 (class 0 OID 0)
-- Dependencies: 2245
-- Name: COLUMN op_terreno.comienzo_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_terreno.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 12876 (class 0 OID 0)
-- Dependencies: 2245
-- Name: COLUMN op_terreno.fin_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_terreno.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 2246 (class 1259 OID 339482)
-- Name: op_ubicacionpuntotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_ubicacionpuntotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_ubicacionpuntotipo OWNER TO postgres;

--
-- TOC entry 2247 (class 1259 OID 339489)
-- Name: op_unidadconstruccion; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_unidadconstruccion (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid uuid DEFAULT public.uuid_generate_v4(),
    identificador character varying(3),
    tipo_dominio bigint,
    tipo_construccion bigint,
    tipo_unidad_construccion bigint,
    tipo_planta bigint,
    planta_ubicacion integer,
    total_habitaciones integer,
    total_banios integer,
    total_locales integer,
    total_pisos integer,
    uso bigint NOT NULL,
    anio_construccion integer,
    avaluo_construccion numeric(16,1),
    area_construida numeric(15,1) NOT NULL,
    area_privada_construida numeric(15,1),
    altura integer,
    observaciones text,
    op_construccion bigint NOT NULL,
    dimension bigint,
    etiqueta character varying(255),
    relacion_superficie bigint,
    geometria public.geometry(MultiPolygonZ,4326),
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    espacio_de_nombres character varying(255) NOT NULL,
    local_id character varying(255) NOT NULL,
    CONSTRAINT op_unidadconstruccion_altura_check CHECK (((altura >= 1) AND (altura <= 1000))),
    CONSTRAINT op_unidadconstruccion_anio_construccion_check CHECK (((anio_construccion >= 1512) AND (anio_construccion <= 2500))),
    CONSTRAINT op_unidadconstruccion_area_construida_check CHECK (((area_construida >= 0.0) AND (area_construida <= 99999999999999.9))),
    CONSTRAINT op_unidadconstruccion_area_privada_construida_check CHECK (((area_privada_construida >= 0.0) AND (area_privada_construida <= 99999999999999.9))),
    CONSTRAINT op_unidadconstruccion_avaluo_construccion_check CHECK (((avaluo_construccion >= 0.0) AND (avaluo_construccion <= '999999999999999'::numeric))),
    CONSTRAINT op_unidadconstruccion_planta_ubicacion_check CHECK (((planta_ubicacion >= 0) AND (planta_ubicacion <= 500))),
    CONSTRAINT op_unidadconstruccion_total_banios_check CHECK (((total_banios >= 0) AND (total_banios <= 999999))),
    CONSTRAINT op_unidadconstruccion_total_habitaciones_check CHECK (((total_habitaciones >= 0) AND (total_habitaciones <= 999999))),
    CONSTRAINT op_unidadconstruccion_total_locales_check CHECK (((total_locales >= 0) AND (total_locales <= 999999))),
    CONSTRAINT op_unidadconstruccion_total_pisos_check CHECK (((total_pisos >= 0) AND (total_pisos <= 150)))
);


ALTER TABLE ladm_col_210.op_unidadconstruccion OWNER TO postgres;

--
-- TOC entry 12877 (class 0 OID 0)
-- Dependencies: 2247
-- Name: TABLE op_unidadconstruccion; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.op_unidadconstruccion IS 'Es cada conjunto de materiales consolidados dentro de un predio que tiene una caracteristicas especificas en cuanto a elementos constitutivos físicos y usos de los mismos.';


--
-- TOC entry 12878 (class 0 OID 0)
-- Dependencies: 2247
-- Name: COLUMN op_unidadconstruccion.area_construida; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_unidadconstruccion.area_construida IS 'Area de la unidad de contrucción.';


--
-- TOC entry 12879 (class 0 OID 0)
-- Dependencies: 2247
-- Name: COLUMN op_unidadconstruccion.area_privada_construida; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_unidadconstruccion.area_privada_construida IS 'Área privada de la unidad de construcción para el caso en que las construcciones tienen regimen de propiedad horizontal.';


--
-- TOC entry 12880 (class 0 OID 0)
-- Dependencies: 2247
-- Name: COLUMN op_unidadconstruccion.etiqueta; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_unidadconstruccion.etiqueta IS 'Corresponde al atributo label de la clase en LADM.';


--
-- TOC entry 12881 (class 0 OID 0)
-- Dependencies: 2247
-- Name: COLUMN op_unidadconstruccion.relacion_superficie; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_unidadconstruccion.relacion_superficie IS 'Corresponde al atributo surfaceRelation de la clase en LADM.';


--
-- TOC entry 12882 (class 0 OID 0)
-- Dependencies: 2247
-- Name: COLUMN op_unidadconstruccion.geometria; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_unidadconstruccion.geometria IS 'Materializacion del metodo createArea(). Almacena de forma permanente la geometría de tipo poligonal.';


--
-- TOC entry 12883 (class 0 OID 0)
-- Dependencies: 2247
-- Name: COLUMN op_unidadconstruccion.comienzo_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_unidadconstruccion.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 12884 (class 0 OID 0)
-- Dependencies: 2247
-- Name: COLUMN op_unidadconstruccion.fin_vida_util_version; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.op_unidadconstruccion.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.';


--
-- TOC entry 2248 (class 1259 OID 339507)
-- Name: op_unidadconstrucciontipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_unidadconstrucciontipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_unidadconstrucciontipo OWNER TO postgres;

--
-- TOC entry 2249 (class 1259 OID 339514)
-- Name: op_usouconstipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_usouconstipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_usouconstipo OWNER TO postgres;

--
-- TOC entry 2250 (class 1259 OID 339521)
-- Name: op_viatipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.op_viatipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.op_viatipo OWNER TO postgres;

--
-- TOC entry 2251 (class 1259 OID 339528)
-- Name: snr_calidadderechotipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.snr_calidadderechotipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.snr_calidadderechotipo OWNER TO postgres;

--
-- TOC entry 2252 (class 1259 OID 339535)
-- Name: snr_derecho; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.snr_derecho (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    calidad_derecho_registro bigint NOT NULL,
    codigo_naturaleza_juridica character varying(5),
    snr_fuente_derecho bigint NOT NULL,
    snr_predio_registro bigint NOT NULL
);


ALTER TABLE ladm_col_210.snr_derecho OWNER TO postgres;

--
-- TOC entry 12885 (class 0 OID 0)
-- Dependencies: 2252
-- Name: COLUMN snr_derecho.calidad_derecho_registro; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.snr_derecho.calidad_derecho_registro IS 'Calidad de derecho en registro';


--
-- TOC entry 2253 (class 1259 OID 339539)
-- Name: snr_documentotitulartipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.snr_documentotitulartipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.snr_documentotitulartipo OWNER TO postgres;

--
-- TOC entry 2254 (class 1259 OID 339546)
-- Name: snr_fuente_cabidalinderos; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.snr_fuente_cabidalinderos (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    tipo_documento bigint,
    numero_documento character varying(255),
    fecha_documento date,
    ente_emisor character varying(255),
    ciudad_emisora character varying(255)
);


ALTER TABLE ladm_col_210.snr_fuente_cabidalinderos OWNER TO postgres;

--
-- TOC entry 2255 (class 1259 OID 339553)
-- Name: snr_fuente_derecho; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.snr_fuente_derecho (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    tipo_documento bigint,
    numero_documento character varying(255),
    fecha_documento date,
    ente_emisor character varying(255),
    ciudad_emisora character varying(255)
);


ALTER TABLE ladm_col_210.snr_fuente_derecho OWNER TO postgres;

--
-- TOC entry 12886 (class 0 OID 0)
-- Dependencies: 2255
-- Name: TABLE snr_fuente_derecho; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.snr_fuente_derecho IS 'Datos del documento que soporta el derecho';


--
-- TOC entry 2256 (class 1259 OID 339560)
-- Name: snr_fuentetipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.snr_fuentetipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.snr_fuentetipo OWNER TO postgres;

--
-- TOC entry 2257 (class 1259 OID 339567)
-- Name: snr_personatitulartipo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.snr_personatitulartipo (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024),
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE ladm_col_210.snr_personatitulartipo OWNER TO postgres;

--
-- TOC entry 2258 (class 1259 OID 339574)
-- Name: snr_predio_registro; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.snr_predio_registro (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    codigo_orip character varying(3),
    matricula_inmobiliaria character varying(80),
    numero_predial_nuevo_en_fmi character varying(30),
    numero_predial_anterior_en_fmi character varying(30),
    cabida_linderos text,
    matricula_inmobiliaria_matriz character varying(80),
    fecha_datos date NOT NULL,
    snr_fuente_cabidalinderos bigint
);


ALTER TABLE ladm_col_210.snr_predio_registro OWNER TO postgres;

--
-- TOC entry 12887 (class 0 OID 0)
-- Dependencies: 2258
-- Name: TABLE snr_predio_registro; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.snr_predio_registro IS 'Datos del predio entregados por registro';


--
-- TOC entry 12888 (class 0 OID 0)
-- Dependencies: 2258
-- Name: COLUMN snr_predio_registro.matricula_inmobiliaria_matriz; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.snr_predio_registro.matricula_inmobiliaria_matriz IS 'Matricula inmobiliaria matriz, cuando aplique';


--
-- TOC entry 2259 (class 1259 OID 339581)
-- Name: snr_titular; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.snr_titular (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    tipo_persona bigint,
    tipo_documento bigint,
    numero_documento character varying(50) NOT NULL,
    nombres character varying(500),
    primer_apellido character varying(255),
    segundo_apellido character varying(255),
    razon_social character varying(255)
);


ALTER TABLE ladm_col_210.snr_titular OWNER TO postgres;

--
-- TOC entry 12889 (class 0 OID 0)
-- Dependencies: 2259
-- Name: TABLE snr_titular; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON TABLE ladm_col_210.snr_titular IS 'Datos de titulares de derecho en registro';


--
-- TOC entry 12890 (class 0 OID 0)
-- Dependencies: 2259
-- Name: COLUMN snr_titular.tipo_persona; Type: COMMENT; Schema: ladm_col_210; Owner: postgres
--

COMMENT ON COLUMN ladm_col_210.snr_titular.tipo_persona IS 'Tipo de persona';


--
-- TOC entry 2260 (class 1259 OID 339588)
-- Name: snr_titular_derecho; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.snr_titular_derecho (
    t_id bigint DEFAULT nextval('ladm_col_210.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    snr_titular bigint NOT NULL,
    snr_derecho bigint NOT NULL,
    porcentaje_participacion integer,
    CONSTRAINT snr_titular_derecho_porcentaje_participacion_check CHECK (((porcentaje_participacion >= 0) AND (porcentaje_participacion <= 100)))
);


ALTER TABLE ladm_col_210.snr_titular_derecho OWNER TO postgres;

--
-- TOC entry 2261 (class 1259 OID 339593)
-- Name: t_ili2db_attrname; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.t_ili2db_attrname (
    iliname character varying(1024) NOT NULL,
    sqlname character varying(1024) NOT NULL,
    colowner character varying(1024) NOT NULL,
    target character varying(1024)
);


ALTER TABLE ladm_col_210.t_ili2db_attrname OWNER TO postgres;

--
-- TOC entry 2262 (class 1259 OID 339599)
-- Name: t_ili2db_basket; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.t_ili2db_basket (
    t_id bigint NOT NULL,
    dataset bigint,
    topic character varying(200) NOT NULL,
    t_ili_tid character varying(200),
    attachmentkey character varying(200) NOT NULL,
    domains character varying(1024)
);


ALTER TABLE ladm_col_210.t_ili2db_basket OWNER TO postgres;

--
-- TOC entry 2263 (class 1259 OID 339605)
-- Name: t_ili2db_classname; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.t_ili2db_classname (
    iliname character varying(1024) NOT NULL,
    sqlname character varying(1024) NOT NULL
);


ALTER TABLE ladm_col_210.t_ili2db_classname OWNER TO postgres;

--
-- TOC entry 2264 (class 1259 OID 339611)
-- Name: t_ili2db_column_prop; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.t_ili2db_column_prop (
    tablename character varying(255) NOT NULL,
    subtype character varying(255),
    columnname character varying(255) NOT NULL,
    tag character varying(1024) NOT NULL,
    setting character varying(1024) NOT NULL
);


ALTER TABLE ladm_col_210.t_ili2db_column_prop OWNER TO postgres;

--
-- TOC entry 2265 (class 1259 OID 339617)
-- Name: t_ili2db_dataset; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.t_ili2db_dataset (
    t_id bigint NOT NULL,
    datasetname character varying(200)
);


ALTER TABLE ladm_col_210.t_ili2db_dataset OWNER TO postgres;

--
-- TOC entry 2266 (class 1259 OID 339620)
-- Name: t_ili2db_inheritance; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.t_ili2db_inheritance (
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024)
);


ALTER TABLE ladm_col_210.t_ili2db_inheritance OWNER TO postgres;

--
-- TOC entry 2267 (class 1259 OID 339626)
-- Name: t_ili2db_meta_attrs; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.t_ili2db_meta_attrs (
    ilielement character varying(255) NOT NULL,
    attr_name character varying(1024) NOT NULL,
    attr_value character varying(1024) NOT NULL
);


ALTER TABLE ladm_col_210.t_ili2db_meta_attrs OWNER TO postgres;

--
-- TOC entry 2268 (class 1259 OID 339632)
-- Name: t_ili2db_model; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.t_ili2db_model (
    filename character varying(250) NOT NULL,
    iliversion character varying(3) NOT NULL,
    modelname text NOT NULL,
    content text NOT NULL,
    importdate timestamp without time zone NOT NULL
);


ALTER TABLE ladm_col_210.t_ili2db_model OWNER TO postgres;

--
-- TOC entry 2269 (class 1259 OID 339638)
-- Name: t_ili2db_settings; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.t_ili2db_settings (
    tag character varying(60) NOT NULL,
    setting character varying(1024)
);


ALTER TABLE ladm_col_210.t_ili2db_settings OWNER TO postgres;

--
-- TOC entry 2270 (class 1259 OID 339644)
-- Name: t_ili2db_table_prop; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.t_ili2db_table_prop (
    tablename character varying(255) NOT NULL,
    tag character varying(1024) NOT NULL,
    setting character varying(1024) NOT NULL
);


ALTER TABLE ladm_col_210.t_ili2db_table_prop OWNER TO postgres;

--
-- TOC entry 2271 (class 1259 OID 339650)
-- Name: t_ili2db_trafo; Type: TABLE; Schema: ladm_col_210; Owner: postgres
--

CREATE TABLE ladm_col_210.t_ili2db_trafo (
    iliname character varying(1024) NOT NULL,
    tag character varying(1024) NOT NULL,
    setting character varying(1024) NOT NULL
);


ALTER TABLE ladm_col_210.t_ili2db_trafo OWNER TO postgres;

--
-- TOC entry 12564 (class 0 OID 338704)
-- Dependencies: 2130
-- Data for Name: anystructure; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.anystructure (t_id, t_seq, op_agrupacion_intrsdos_calidad, op_agrupacion_intrsdos_procedencia, op_construccion_calidad, op_construccion_procedencia, op_derecho_calidad, op_derecho_procedencia, op_interesado_calidad, op_interesado_procedencia, op_lindero_calidad, op_lindero_procedencia, op_predio_calidad, op_predio_procedencia, op_puntocontrol_calidad, op_puntocontrol_procedencia, op_puntolindero_calidad, op_puntolindero_procedencia, op_restriccion_calidad, op_restriccion_procedencia, op_terreno_calidad, op_terreno_procedencia, op_puntolevantamiento_calidad, op_puntolevantamiento_procedencia, op_servidumbretransito_calidad, op_servidumbretransito_procedencia, op_unidadconstruccion_calidad, op_unidadconstruccion_procedencia) FROM stdin;
\.


--
-- TOC entry 12565 (class 0 OID 338708)
-- Dependencies: 2131
-- Data for Name: cc_metodooperacion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.cc_metodooperacion (t_id, t_seq, formula, dimensiones_origen, ddimensiones_objetivo, col_transformacion_transformacion) FROM stdin;
\.


--
-- TOC entry 12566 (class 0 OID 338714)
-- Dependencies: 2132
-- Data for Name: ci_forma_presentacion_codigo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.ci_forma_presentacion_codigo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
302	LADM_COL_V1_6.LADM_Nucleo.CI_Forma_Presentacion_Codigo	\N	0	Imagen	\N	f	Imagen	Definición en la ISO 19115:2003.
303	LADM_COL_V1_6.LADM_Nucleo.CI_Forma_Presentacion_Codigo	\N	1	Documento	\N	f	Documento	\N
304	LADM_COL_V1_6.LADM_Nucleo.CI_Forma_Presentacion_Codigo	\N	2	Mapa	\N	f	Mapa	Definición en la ISO 19115:2003.
305	LADM_COL_V1_6.LADM_Nucleo.CI_Forma_Presentacion_Codigo	\N	3	Video	\N	f	Video	Definición en la ISO 19115:2003.
306	LADM_COL_V1_6.LADM_Nucleo.CI_Forma_Presentacion_Codigo	\N	4	Otro	\N	f	Otro	Definición en la ISO 19115:2003.
\.


--
-- TOC entry 12567 (class 0 OID 338721)
-- Dependencies: 2133
-- Data for Name: col_areatipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_areatipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
170	LADM_COL_V1_6.LADM_Nucleo.COL_AreaTipo	\N	0	Area_Calculada_Altura_Local	\N	f	Área calculada artura local	\N
171	LADM_COL_V1_6.LADM_Nucleo.COL_AreaTipo	\N	1	Area_Calculada_Altura_Mar	\N	f	Área calculada altura mar	\N
172	LADM_COL_V1_6.LADM_Nucleo.COL_AreaTipo	\N	2	Area_Catastral_Administrativa	\N	f	Área catastral administrativa	\N
173	LADM_COL_V1_6.LADM_Nucleo.COL_AreaTipo	\N	3	Area_Estimado_Construccion	\N	f	Área estimado construcción	\N
174	LADM_COL_V1_6.LADM_Nucleo.COL_AreaTipo	\N	4	Area_No_Oficial	\N	f	Área no oficial	\N
175	LADM_COL_V1_6.LADM_Nucleo.COL_AreaTipo	\N	5	Area_Registral	\N	f	Área registral	\N
\.


--
-- TOC entry 12568 (class 0 OID 338728)
-- Dependencies: 2134
-- Data for Name: col_areavalor; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_areavalor (t_id, t_seq, areasize, atype, op_construccion_area, op_terreno_area, op_servidumbretransito_area, op_unidadconstruccion_area) FROM stdin;
\.


--
-- TOC entry 12569 (class 0 OID 338733)
-- Dependencies: 2135
-- Data for Name: col_baunitcomointeresado; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_baunitcomointeresado (t_id, t_ili_tid, interesado_op_interesado, interesado_op_agrupacion_interesados, unidad) FROM stdin;
\.


--
-- TOC entry 12570 (class 0 OID 338737)
-- Dependencies: 2136
-- Data for Name: col_baunitfuente; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_baunitfuente (t_id, t_ili_tid, fuente_espacial, unidad) FROM stdin;
\.


--
-- TOC entry 12571 (class 0 OID 338741)
-- Dependencies: 2137
-- Data for Name: col_baunittipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_baunittipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
136	LADM_COL_V1_6.LADM_Nucleo.COL_BAUnitTipo	\N	0	Unidad_Propiedad_Basica	\N	f	Unidad propiedad básica	\N
137	LADM_COL_V1_6.LADM_Nucleo.COL_BAUnitTipo	\N	1	Unidad_Derecho	\N	f	Unidad derecho	\N
138	LADM_COL_V1_6.LADM_Nucleo.COL_BAUnitTipo	\N	2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12572 (class 0 OID 338748)
-- Dependencies: 2138
-- Data for Name: col_cclfuente; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_cclfuente (t_id, t_ili_tid, ccl, fuente_espacial) FROM stdin;
\.


--
-- TOC entry 12573 (class 0 OID 338752)
-- Dependencies: 2139
-- Data for Name: col_clfuente; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_clfuente (t_id, t_ili_tid, fuente_espacial) FROM stdin;
\.


--
-- TOC entry 12574 (class 0 OID 338756)
-- Dependencies: 2140
-- Data for Name: col_contenidoniveltipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_contenidoniveltipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
125	LADM_COL_V1_6.LADM_Nucleo.COL_ContenidoNivelTipo	\N	0	Construccion_Convencional	\N	f	Construcción convencional	\N
126	LADM_COL_V1_6.LADM_Nucleo.COL_ContenidoNivelTipo	\N	1	Construccion_No_Convencional	\N	f	Construcción no convencional	\N
127	LADM_COL_V1_6.LADM_Nucleo.COL_ContenidoNivelTipo	\N	2	Consuetudinario	\N	f	Consuetudinario	\N
128	LADM_COL_V1_6.LADM_Nucleo.COL_ContenidoNivelTipo	\N	3	Formal	\N	f	Formal	\N
129	LADM_COL_V1_6.LADM_Nucleo.COL_ContenidoNivelTipo	\N	4	Informal	\N	f	Informal	\N
130	LADM_COL_V1_6.LADM_Nucleo.COL_ContenidoNivelTipo	\N	5	Responsabilidad	\N	f	Responsabilidad	\N
131	LADM_COL_V1_6.LADM_Nucleo.COL_ContenidoNivelTipo	\N	6	Restriccion_Derecho_Publico	\N	f	Restricción derecho público	\N
132	LADM_COL_V1_6.LADM_Nucleo.COL_ContenidoNivelTipo	\N	7	Restriccion_Derecho_Privado	\N	f	Restricción derecho privado	\N
\.


--
-- TOC entry 12575 (class 0 OID 338763)
-- Dependencies: 2141
-- Data for Name: col_dimensiontipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_dimensiontipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
122	LADM_COL_V1_6.LADM_Nucleo.COL_DimensionTipo	\N	0	Dim2D	\N	f	Dimensión 2D	\N
123	LADM_COL_V1_6.LADM_Nucleo.COL_DimensionTipo	\N	1	Dim3D	\N	f	Dimensión 3D	\N
124	LADM_COL_V1_6.LADM_Nucleo.COL_DimensionTipo	\N	2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12576 (class 0 OID 338770)
-- Dependencies: 2142
-- Data for Name: col_estadodisponibilidadtipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_estadodisponibilidadtipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
182	LADM_COL_V1_6.LADM_Nucleo.COL_EstadoDisponibilidadTipo	\N	0	Convertido	\N	f	Convertido	\N
183	LADM_COL_V1_6.LADM_Nucleo.COL_EstadoDisponibilidadTipo	\N	1	Desconocido	\N	f	Desconocido	\N
184	LADM_COL_V1_6.LADM_Nucleo.COL_EstadoDisponibilidadTipo	\N	2	Disponible	\N	f	Disponible	\N
\.


--
-- TOC entry 12577 (class 0 OID 338777)
-- Dependencies: 2143
-- Data for Name: col_estadoredserviciostipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_estadoredserviciostipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
273	LADM_COL_V1_6.LADM_Nucleo.COL_EstadoRedServiciosTipo	\N	0	Planeado	\N	f	Planeado	\N
274	LADM_COL_V1_6.LADM_Nucleo.COL_EstadoRedServiciosTipo	\N	1	En_Uso	\N	f	En uso	\N
275	LADM_COL_V1_6.LADM_Nucleo.COL_EstadoRedServiciosTipo	\N	2	Fuera_De_Servicio	\N	f	Fuera de servicio	\N
276	LADM_COL_V1_6.LADM_Nucleo.COL_EstadoRedServiciosTipo	\N	3	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12578 (class 0 OID 338784)
-- Dependencies: 2144
-- Data for Name: col_estructuratipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_estructuratipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
100	LADM_COL_V1_6.LADM_Nucleo.COL_EstructuraTipo	\N	0	Croquis	\N	f	Croquis	\N
101	LADM_COL_V1_6.LADM_Nucleo.COL_EstructuraTipo	\N	1	Linea_no_Estructurada	\N	f	Línea no estructurada	\N
102	LADM_COL_V1_6.LADM_Nucleo.COL_EstructuraTipo	\N	2	Texto	\N	f	Texto	\N
103	LADM_COL_V1_6.LADM_Nucleo.COL_EstructuraTipo	\N	3	Topologico	\N	f	Topológico	\N
\.


--
-- TOC entry 12579 (class 0 OID 338791)
-- Dependencies: 2145
-- Data for Name: col_fuenteadministrativatipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_fuenteadministrativatipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
16	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	0	Escritura	\N	f	Escritura	\N
17	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	1	Certificado	\N	f	Certificado	\N
18	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	2	Contrato	\N	f	Contrato	\N
19	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	3	Documento_Identidad	\N	f	Documento de identidad	\N
20	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	4	Informe	\N	f	Informe	\N
21	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	5	Formulario_Predial	\N	f	Formulario predial	\N
22	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	6	Promesa_Compraventa	\N	f	Promesa de compraventa	\N
23	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	7	Reglamento	\N	f	Reglamento	\N
24	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	8	Resolucion	\N	f	Resolución	\N
25	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	9	Sentencia	\N	f	Sentencia	\N
26	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	10	Solicitud	\N	f	Solicitud	\N
27	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	11	Acta	\N	f	Acta	\N
28	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	12	Acuerdo	\N	f	Acuerdo	\N
29	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	13	Auto	\N	f	Auto	\N
30	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	14	Estatuto_Social	\N	f	Estatuto social	\N
31	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	15	Decreto	\N	f	Decreto	\N
32	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	16	Providencia	\N	f	Providencia	\N
33	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	17	Acta_Colindancia	\N	f	Acta de colindancia	\N
34	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	18	Libros_Antiguo_Sistema_Registral	\N	f	Libros antiguo sistema	\N
35	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	19	Informe_Colindancia	\N	f	Informe de colindancia	\N
36	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	20	Carta_Venta	\N	f	Carta vental	\N
37	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	\N	21	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12580 (class 0 OID 338798)
-- Dependencies: 2146
-- Data for Name: col_fuenteespacialtipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_fuenteespacialtipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
108	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacialTipo	\N	0	Croquis_Campo	\N	f	Croquis de campo	\N
109	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacialTipo	\N	1	Datos_Crudos	\N	f	Datos crudos (GPS, Estación total, LiDAR, etc.)	\N
110	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacialTipo	\N	2	Ortofoto	\N	f	Ortofoto	\N
111	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacialTipo	\N	3	Informe_Tecnico	\N	f	Informe técnico	\N
112	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacialTipo	\N	4	Registro_Fotografico	\N	f	Registro fotográfico	\N
\.


--
-- TOC entry 12581 (class 0 OID 338805)
-- Dependencies: 2147
-- Data for Name: col_grupointeresadotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_grupointeresadotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
277	LADM_COL_V1_6.LADM_Nucleo.COL_GrupoInteresadoTipo	\N	0	Grupo_Civil	\N	f	Grupo civil	\N
278	LADM_COL_V1_6.LADM_Nucleo.COL_GrupoInteresadoTipo	\N	1	Grupo_Empresarial	\N	f	Grupo empresarial	\N
279	LADM_COL_V1_6.LADM_Nucleo.COL_GrupoInteresadoTipo	\N	2	Grupo_Etnico	\N	f	Grupo étnico	\N
280	LADM_COL_V1_6.LADM_Nucleo.COL_GrupoInteresadoTipo	\N	3	Grupo_Mixto	\N	f	Grupo mixto	\N
\.


--
-- TOC entry 12582 (class 0 OID 338812)
-- Dependencies: 2148
-- Data for Name: col_interpolaciontipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_interpolaciontipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
290	LADM_COL_V1_6.LADM_Nucleo.COL_InterpolacionTipo	\N	0	Aislado	\N	f	Aislado	\N
291	LADM_COL_V1_6.LADM_Nucleo.COL_InterpolacionTipo	\N	1	Intermedio_Arco	\N	f	Intermedio arco	\N
292	LADM_COL_V1_6.LADM_Nucleo.COL_InterpolacionTipo	\N	2	Intermedio_Linea	\N	f	Intermedio línea	\N
\.


--
-- TOC entry 12583 (class 0 OID 338819)
-- Dependencies: 2149
-- Data for Name: col_iso19125_tipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_iso19125_tipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
176	LADM_COL_V1_6.LADM_Nucleo.COL_ISO19125_Tipo	\N	0	Disjunto	\N	f	Disjunto	\N
177	LADM_COL_V1_6.LADM_Nucleo.COL_ISO19125_Tipo	\N	1	Toca	\N	f	Toca	\N
178	LADM_COL_V1_6.LADM_Nucleo.COL_ISO19125_Tipo	\N	2	Superpone	\N	f	Superpone	\N
179	LADM_COL_V1_6.LADM_Nucleo.COL_ISO19125_Tipo	\N	3	Desconocido	\N	f	Desconocido	\N
\.


--
-- TOC entry 12584 (class 0 OID 338826)
-- Dependencies: 2150
-- Data for Name: col_masccl; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_masccl (t_id, t_ili_tid, ccl_mas, ue_mas_op_construccion, ue_mas_op_terreno, ue_mas_op_servidumbretransito, ue_mas_op_unidadconstruccion) FROM stdin;
\.


--
-- TOC entry 12585 (class 0 OID 338830)
-- Dependencies: 2151
-- Data for Name: col_mascl; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_mascl (t_id, t_ili_tid, ue_mas_op_construccion, ue_mas_op_terreno, ue_mas_op_servidumbretransito, ue_mas_op_unidadconstruccion) FROM stdin;
\.


--
-- TOC entry 12586 (class 0 OID 338834)
-- Dependencies: 2152
-- Data for Name: col_menosccl; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_menosccl (t_id, t_ili_tid, ccl_menos, ue_menos_op_construccion, ue_menos_op_terreno, ue_menos_op_servidumbretransito, ue_menos_op_unidadconstruccion) FROM stdin;
\.


--
-- TOC entry 12587 (class 0 OID 338838)
-- Dependencies: 2153
-- Data for Name: col_menoscl; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_menoscl (t_id, t_ili_tid, ue_menos_op_construccion, ue_menos_op_terreno, ue_menos_op_servidumbretransito, ue_menos_op_unidadconstruccion) FROM stdin;
\.


--
-- TOC entry 12588 (class 0 OID 338842)
-- Dependencies: 2154
-- Data for Name: col_metodoproducciontipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_metodoproducciontipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
139	LADM_COL_V1_6.LADM_Nucleo.COL_MetodoProduccionTipo	\N	0	Metodo_Directo	\N	f	Método directo	\N
140	LADM_COL_V1_6.LADM_Nucleo.COL_MetodoProduccionTipo	\N	1	Metodo_Indirecto	\N	f	Método indirecto	\N
\.


--
-- TOC entry 12589 (class 0 OID 338849)
-- Dependencies: 2155
-- Data for Name: col_miembros; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_miembros (t_id, t_ili_tid, interesado_op_interesado, interesado_op_agrupacion_interesados, agrupacion) FROM stdin;
\.


--
-- TOC entry 12590 (class 0 OID 338853)
-- Dependencies: 2156
-- Data for Name: col_puntoccl; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_puntoccl (t_id, t_ili_tid, punto_op_puntocontrol, punto_op_puntolindero, punto_op_puntolevantamiento, ccl) FROM stdin;
\.


--
-- TOC entry 12591 (class 0 OID 338857)
-- Dependencies: 2157
-- Data for Name: col_puntocl; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_puntocl (t_id, t_ili_tid, punto_op_puntocontrol, punto_op_puntolindero, punto_op_puntolevantamiento) FROM stdin;
\.


--
-- TOC entry 12592 (class 0 OID 338861)
-- Dependencies: 2158
-- Data for Name: col_puntofuente; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_puntofuente (t_id, t_ili_tid, fuente_espacial, punto_op_puntocontrol, punto_op_puntolindero, punto_op_puntolevantamiento) FROM stdin;
\.


--
-- TOC entry 12593 (class 0 OID 338865)
-- Dependencies: 2159
-- Data for Name: col_puntotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_puntotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
40	LADM_COL_V1_6.LADM_Nucleo.COL_PuntoTipo	\N	0	Control	\N	f	Control	\N
41	LADM_COL_V1_6.LADM_Nucleo.COL_PuntoTipo	\N	1	Catastro	\N	f	Catastro	\N
42	LADM_COL_V1_6.LADM_Nucleo.COL_PuntoTipo	\N	2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12594 (class 0 OID 338872)
-- Dependencies: 2160
-- Data for Name: col_redserviciostipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_redserviciostipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
185	LADM_COL_V1_6.LADM_Nucleo.COL_RedServiciosTipo	\N	0	Petroleo	\N	f	Petróleo	\N
186	LADM_COL_V1_6.LADM_Nucleo.COL_RedServiciosTipo	\N	1	Quimicos	\N	f	Químicos	\N
187	LADM_COL_V1_6.LADM_Nucleo.COL_RedServiciosTipo	\N	2	Red_Termica	\N	f	Red térmica	\N
188	LADM_COL_V1_6.LADM_Nucleo.COL_RedServiciosTipo	\N	3	Telecomunicacion	\N	f	Telecomunicación	\N
\.


--
-- TOC entry 12595 (class 0 OID 338879)
-- Dependencies: 2161
-- Data for Name: col_registrotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_registrotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
297	LADM_COL_V1_6.LADM_Nucleo.COL_RegistroTipo	\N	0	Rural	\N	f	Rural	\N
298	LADM_COL_V1_6.LADM_Nucleo.COL_RegistroTipo	\N	1	Urbano	\N	f	Urbano	\N
299	LADM_COL_V1_6.LADM_Nucleo.COL_RegistroTipo	\N	2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12596 (class 0 OID 338886)
-- Dependencies: 2162
-- Data for Name: col_relacionfuente; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_relacionfuente (t_id, t_ili_tid, fuente_administrativa) FROM stdin;
\.


--
-- TOC entry 12597 (class 0 OID 338890)
-- Dependencies: 2163
-- Data for Name: col_relacionfuenteuespacial; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_relacionfuenteuespacial (t_id, t_ili_tid, fuente_espacial) FROM stdin;
\.


--
-- TOC entry 12598 (class 0 OID 338894)
-- Dependencies: 2164
-- Data for Name: col_relacionsuperficietipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_relacionsuperficietipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
72	LADM_COL_V1_6.LADM_Nucleo.COL_RelacionSuperficieTipo	\N	0	En_Rasante	\N	f	En rasante	\N
73	LADM_COL_V1_6.LADM_Nucleo.COL_RelacionSuperficieTipo	\N	1	En_Vuelo	\N	f	En vuelo	\N
74	LADM_COL_V1_6.LADM_Nucleo.COL_RelacionSuperficieTipo	\N	2	En_Subsuelo	\N	f	En subsuelo	\N
75	LADM_COL_V1_6.LADM_Nucleo.COL_RelacionSuperficieTipo	\N	3	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12599 (class 0 OID 338901)
-- Dependencies: 2165
-- Data for Name: col_responsablefuente; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_responsablefuente (t_id, t_ili_tid, fuente_administrativa, interesado_op_interesado, interesado_op_agrupacion_interesados) FROM stdin;
\.


--
-- TOC entry 12600 (class 0 OID 338905)
-- Dependencies: 2166
-- Data for Name: col_rrrfuente; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_rrrfuente (t_id, t_ili_tid, fuente_administrativa, rrr_op_derecho, rrr_op_restriccion) FROM stdin;
\.


--
-- TOC entry 12601 (class 0 OID 338909)
-- Dependencies: 2167
-- Data for Name: col_topografofuente; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_topografofuente (t_id, t_ili_tid, fuente_espacial, topografo_op_interesado, topografo_op_agrupacion_interesados) FROM stdin;
\.


--
-- TOC entry 12602 (class 0 OID 338913)
-- Dependencies: 2168
-- Data for Name: col_transformacion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_transformacion (t_id, t_seq, localizacion_transformada, op_puntocontrol_transformacion_y_resultado, op_puntolindero_transformacion_y_resultado, op_puntolevantamiento_transformacion_y_resultado) FROM stdin;
\.


--
-- TOC entry 12603 (class 0 OID 338920)
-- Dependencies: 2169
-- Data for Name: col_uebaunit; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_uebaunit (t_id, t_ili_tid, ue_op_construccion, ue_op_terreno, ue_op_servidumbretransito, ue_op_unidadconstruccion, baunit) FROM stdin;
\.


--
-- TOC entry 12604 (class 0 OID 338924)
-- Dependencies: 2170
-- Data for Name: col_uefuente; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_uefuente (t_id, t_ili_tid, ue_op_construccion, ue_op_terreno, ue_op_servidumbretransito, ue_op_unidadconstruccion, fuente_espacial) FROM stdin;
\.


--
-- TOC entry 12605 (class 0 OID 338928)
-- Dependencies: 2171
-- Data for Name: col_ueuegrupo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_ueuegrupo (t_id, t_ili_tid, parte_op_construccion, parte_op_terreno, parte_op_servidumbretransito, parte_op_unidadconstruccion) FROM stdin;
\.


--
-- TOC entry 12606 (class 0 OID 338932)
-- Dependencies: 2172
-- Data for Name: col_unidadedificaciontipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_unidadedificaciontipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
168	LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEdificacionTipo	\N	0	Compartido	\N	f	Compartido	\N
169	LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEdificacionTipo	\N	1	Individual	\N	f	Individual	\N
\.


--
-- TOC entry 12607 (class 0 OID 338939)
-- Dependencies: 2173
-- Data for Name: col_unidadfuente; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_unidadfuente (t_id, t_ili_tid, fuente_administrativa, unidad) FROM stdin;
\.


--
-- TOC entry 12608 (class 0 OID 338943)
-- Dependencies: 2174
-- Data for Name: col_volumentipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_volumentipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
156	LADM_COL_V1_6.LADM_Nucleo.COL_VolumenTipo	\N	0	Oficial	\N	f	Oficial	\N
157	LADM_COL_V1_6.LADM_Nucleo.COL_VolumenTipo	\N	1	Calculado	\N	f	Calculado	\N
158	LADM_COL_V1_6.LADM_Nucleo.COL_VolumenTipo	\N	2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12609 (class 0 OID 338950)
-- Dependencies: 2175
-- Data for Name: col_volumenvalor; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.col_volumenvalor (t_id, t_seq, volumen_medicion, tipo, op_construccion_volumen, op_terreno_volumen, op_servidumbretransito_volumen, op_unidadconstruccion_volumen) FROM stdin;
\.


--
-- TOC entry 12610 (class 0 OID 338955)
-- Dependencies: 2176
-- Data for Name: extarchivo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.extarchivo (t_id, t_seq, fecha_aceptacion, datos, extraccion, fecha_grabacion, fecha_entrega, espacio_de_nombres, local_id, snr_fuente_cabidlndros_archivo, op_fuenteadministrtiva_ext_archivo_id, op_fuenteespacial_ext_archivo_id) FROM stdin;
\.


--
-- TOC entry 12611 (class 0 OID 338962)
-- Dependencies: 2177
-- Data for Name: extdireccion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.extdireccion (t_id, t_seq, tipo_direccion, es_direccion_principal, localizacion, codigo_postal, clase_via_principal, valor_via_principal, letra_via_principal, sector_ciudad, valor_via_generadora, letra_via_generadora, numero_predio, sector_predio, complemento, nombre_predio, extunidadedificcnfsica_ext_direccion_id, extinteresado_ext_direccion_id, op_construccion_ext_direccion_id, op_terreno_ext_direccion_id, op_servidumbretransito_ext_direccion_id, op_unidadconstruccion_ext_direccion_id) FROM stdin;
\.


--
-- TOC entry 12612 (class 0 OID 338969)
-- Dependencies: 2178
-- Data for Name: extdireccion_clase_via_principal; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.extdireccion_clase_via_principal (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
159	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Clase_Via_Principal	\N	0	Avenida_Calle	\N	f	Avenida calle	\N
160	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Clase_Via_Principal	\N	1	Avenida_Carrera	\N	f	Avenida carrera	\N
161	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Clase_Via_Principal	\N	2	Calle	\N	f	Calle	\N
162	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Clase_Via_Principal	\N	3	Carrera	\N	f	Carrera	\N
163	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Clase_Via_Principal	\N	4	Diagonal	\N	f	Diagonal	\N
164	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Clase_Via_Principal	\N	5	Transversal	\N	f	Transversal	\N
165	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Clase_Via_Principal	\N	6	Circular	\N	f	Circular	\N
\.


--
-- TOC entry 12613 (class 0 OID 338976)
-- Dependencies: 2179
-- Data for Name: extdireccion_sector_ciudad; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.extdireccion_sector_ciudad (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
59	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Ciudad	\N	0	Norte	\N	f	Norte	\N
60	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Ciudad	\N	1	Sur	\N	f	Sur	\N
61	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Ciudad	\N	2	Este	\N	f	Este	\N
62	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Ciudad	\N	3	Oeste	\N	f	Oeste	\N
\.


--
-- TOC entry 12614 (class 0 OID 338983)
-- Dependencies: 2180
-- Data for Name: extdireccion_sector_predio; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.extdireccion_sector_predio (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
293	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Predio	\N	0	Norte	\N	f	Norte	\N
294	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Predio	\N	1	Sur	\N	f	Sur	\N
295	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Predio	\N	2	Este	\N	f	Este	\N
296	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Predio	\N	3	Oeste	\N	f	Oeste	\N
\.


--
-- TOC entry 12615 (class 0 OID 338990)
-- Dependencies: 2181
-- Data for Name: extdireccion_tipo_direccion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.extdireccion_tipo_direccion (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
300	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Tipo_Direccion	\N	0	Estructurada	\N	f	Estructurada	\N
301	LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Tipo_Direccion	\N	1	No_Estructurada	\N	f	No estructurada	\N
\.


--
-- TOC entry 12616 (class 0 OID 338997)
-- Dependencies: 2182
-- Data for Name: extinteresado; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.extinteresado (t_id, t_seq, nombre, extredserviciosfisica_ext_interesado_administrador_id, op_agrupacion_intrsdos_ext_pid, op_interesado_ext_pid) FROM stdin;
\.


--
-- TOC entry 12617 (class 0 OID 339001)
-- Dependencies: 2183
-- Data for Name: extredserviciosfisica; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.extredserviciosfisica (t_id, t_seq, orientada) FROM stdin;
\.


--
-- TOC entry 12618 (class 0 OID 339005)
-- Dependencies: 2184
-- Data for Name: extunidadedificacionfisica; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.extunidadedificacionfisica (t_id, t_seq) FROM stdin;
\.


--
-- TOC entry 12619 (class 0 OID 339009)
-- Dependencies: 2185
-- Data for Name: fraccion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.fraccion (t_id, t_seq, denominador, numerador, col_miembros_participacion, op_predio_copropiedad_coeficiente) FROM stdin;
\.


--
-- TOC entry 12620 (class 0 OID 339015)
-- Dependencies: 2186
-- Data for Name: gc_barrio; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_barrio (t_id, t_ili_tid, codigo, nombre, codigo_sector, geometria) FROM stdin;
\.


--
-- TOC entry 12621 (class 0 OID 339022)
-- Dependencies: 2187
-- Data for Name: gc_comisiones_construccion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_comisiones_construccion (t_id, t_ili_tid, geometria) FROM stdin;
\.


--
-- TOC entry 12622 (class 0 OID 339029)
-- Dependencies: 2188
-- Data for Name: gc_comisiones_terreno; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_comisiones_terreno (t_id, t_ili_tid, geometria) FROM stdin;
\.


--
-- TOC entry 12623 (class 0 OID 339036)
-- Dependencies: 2189
-- Data for Name: gc_comisiones_unidad_construccion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_comisiones_unidad_construccion (t_id, t_ili_tid, geometria) FROM stdin;
\.


--
-- TOC entry 12624 (class 0 OID 339043)
-- Dependencies: 2190
-- Data for Name: gc_condicionprediotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_condicionprediotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
307	Datos_Gestor_Catastral_V2_10.GC_CondicionPredioTipo	\N	0	NPH	\N	f	No propiedad horizontal	\N
308	Datos_Gestor_Catastral_V2_10.GC_CondicionPredioTipo	\N	1	PH.Matriz	\N	f	PH.Matriz	\N
309	Datos_Gestor_Catastral_V2_10.GC_CondicionPredioTipo	\N	2	PH.Unidad_Predial	\N	f	PH.Unidad Predial	\N
310	Datos_Gestor_Catastral_V2_10.GC_CondicionPredioTipo	\N	3	Condominio.Matriz	\N	f	Condominio.Matriz	\N
311	Datos_Gestor_Catastral_V2_10.GC_CondicionPredioTipo	\N	4	Condominio.Unidad_Predial	\N	f	Condominio.Unidad Predial	\N
312	Datos_Gestor_Catastral_V2_10.GC_CondicionPredioTipo	\N	5	Mejora.PH	\N	f	Mejora.PH	\N
313	Datos_Gestor_Catastral_V2_10.GC_CondicionPredioTipo	\N	6	Mejora.NPH	\N	f	Mejora.NPH	\N
314	Datos_Gestor_Catastral_V2_10.GC_CondicionPredioTipo	\N	7	Parque_Cementerio.Matriz	\N	f	Parque Cementerio.Matriz	\N
315	Datos_Gestor_Catastral_V2_10.GC_CondicionPredioTipo	\N	8	Parque_Cementerio.Unidad_Predial	\N	f	Parque Cementerio.Unidad Predial	\N
316	Datos_Gestor_Catastral_V2_10.GC_CondicionPredioTipo	\N	9	Via	\N	f	Vía	\N
317	Datos_Gestor_Catastral_V2_10.GC_CondicionPredioTipo	\N	10	Bien_Uso_Publico	\N	f	Bien de uso público	\N
\.


--
-- TOC entry 12625 (class 0 OID 339050)
-- Dependencies: 2191
-- Data for Name: gc_construccion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_construccion (t_id, t_ili_tid, identificador, etiqueta, tipo_construccion, tipo_dominio, numero_pisos, numero_sotanos, numero_mezanines, numero_semisotanos, codigo_edificacion, codigo_terreno, area_construida, geometria, gc_predio) FROM stdin;
\.


--
-- TOC entry 12626 (class 0 OID 339063)
-- Dependencies: 2192
-- Data for Name: gc_copropiedad; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_copropiedad (t_id, gc_matriz, gc_unidad, coeficiente_copropiedad) FROM stdin;
\.


--
-- TOC entry 12627 (class 0 OID 339068)
-- Dependencies: 2193
-- Data for Name: gc_datos_ph_condiminio; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_datos_ph_condiminio (t_id, t_ili_tid, area_total_terreno, area_total_terreno_privada, area_total_terreno_comun, area_total_construida, area_total_construida_privada, area_total_construida_comun, torre_no, total_pisos_torre, total_unidades_privadas, total_sotanos, total_unidades_sotano, gc_predio) FROM stdin;
\.


--
-- TOC entry 12628 (class 0 OID 339082)
-- Dependencies: 2194
-- Data for Name: gc_direccion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_direccion (t_id, t_seq, valor, principal, geometria_referencia, gc_predio_catastro_direcciones) FROM stdin;
\.


--
-- TOC entry 12629 (class 0 OID 339089)
-- Dependencies: 2195
-- Data for Name: gc_manzana; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_manzana (t_id, t_ili_tid, codigo, codigo_anterior, codigo_barrio, geometria) FROM stdin;
\.


--
-- TOC entry 12630 (class 0 OID 339096)
-- Dependencies: 2196
-- Data for Name: gc_perimetro; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_perimetro (t_id, t_ili_tid, codigo_departamento, codigo_municipio, tipo_avaluo, nombre_geografico, codigo_nombre, geometria) FROM stdin;
\.


--
-- TOC entry 12631 (class 0 OID 339103)
-- Dependencies: 2197
-- Data for Name: gc_predio_catastro; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_predio_catastro (t_id, t_ili_tid, tipo_catastro, numero_predial, numero_predial_anterior, circulo_registral, matricula_inmobiliaria_catastro, tipo_predio, condicion_predio, destinacion_economica, estado_alerta, entidad_emisora_alerta, fecha_alerta, sistema_procedencia_datos, fecha_datos) FROM stdin;
\.


--
-- TOC entry 12632 (class 0 OID 339110)
-- Dependencies: 2198
-- Data for Name: gc_propietario; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_propietario (t_id, t_ili_tid, tipo_documento, numero_documento, digito_verificacion, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, razon_social, gc_predio_catastro) FROM stdin;
\.


--
-- TOC entry 12633 (class 0 OID 339117)
-- Dependencies: 2199
-- Data for Name: gc_sector_rural; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_sector_rural (t_id, t_ili_tid, codigo, geometria) FROM stdin;
\.


--
-- TOC entry 12634 (class 0 OID 339124)
-- Dependencies: 2200
-- Data for Name: gc_sector_urbano; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_sector_urbano (t_id, t_ili_tid, codigo, geometria) FROM stdin;
\.


--
-- TOC entry 12635 (class 0 OID 339131)
-- Dependencies: 2201
-- Data for Name: gc_sistemaprocedenciadatostipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_sistemaprocedenciadatostipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
63	Datos_Gestor_Catastral_V2_10.GC_SistemaProcedenciaDatosTipo	\N	0	SNC	\N	f	Sistema Nacional Catastral	\N
64	Datos_Gestor_Catastral_V2_10.GC_SistemaProcedenciaDatosTipo	\N	1	Cobol	\N	f	Cobol	\N
\.


--
-- TOC entry 12636 (class 0 OID 339138)
-- Dependencies: 2202
-- Data for Name: gc_terreno; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_terreno (t_id, t_ili_tid, area_terreno_alfanumerica, area_terreno_digital, manzana_vereda_codigo, numero_subterraneos, geometria, gc_predio) FROM stdin;
\.


--
-- TOC entry 12637 (class 0 OID 339148)
-- Dependencies: 2203
-- Data for Name: gc_unidad_construccion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_unidad_construccion (t_id, t_ili_tid, identificador, etiqueta, tipo_dominio, tipo_construccion, planta, total_habitaciones, total_banios, total_locales, total_pisos, uso, anio_construccion, puntaje, area_construida, area_privada, codigo_terreno, geometria, gc_construccion) FROM stdin;
\.


--
-- TOC entry 12638 (class 0 OID 339163)
-- Dependencies: 2204
-- Data for Name: gc_unidadconstrucciontipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_unidadconstrucciontipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
180	Datos_Gestor_Catastral_V2_10.GC_UnidadConstruccionTipo	\N	0	Convencional	\N	f	Convencional	\N
181	Datos_Gestor_Catastral_V2_10.GC_UnidadConstruccionTipo	\N	1	No_Convencional	\N	f	No convencional	\N
\.


--
-- TOC entry 12639 (class 0 OID 339170)
-- Dependencies: 2205
-- Data for Name: gc_vereda; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gc_vereda (t_id, t_ili_tid, codigo, codigo_anterior, nombre, codigo_sector, geometria) FROM stdin;
\.


--
-- TOC entry 12640 (class 0 OID 339177)
-- Dependencies: 2206
-- Data for Name: gm_multisurface2d; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gm_multisurface2d (t_id, t_seq) FROM stdin;
\.


--
-- TOC entry 12641 (class 0 OID 339181)
-- Dependencies: 2207
-- Data for Name: gm_multisurface3d; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gm_multisurface3d (t_id, t_seq) FROM stdin;
\.


--
-- TOC entry 12642 (class 0 OID 339185)
-- Dependencies: 2208
-- Data for Name: gm_surface2dlistvalue; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gm_surface2dlistvalue (t_id, t_seq, avalue, gm_multisurface2d_geometry) FROM stdin;
\.


--
-- TOC entry 12643 (class 0 OID 339192)
-- Dependencies: 2209
-- Data for Name: gm_surface3dlistvalue; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.gm_surface3dlistvalue (t_id, t_seq, avalue, gm_multisurface3d_geometry) FROM stdin;
\.


--
-- TOC entry 12644 (class 0 OID 339199)
-- Dependencies: 2210
-- Data for Name: imagen; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.imagen (t_id, t_seq, uri, extinteresado_huella_dactilar, extinteresado_fotografia, extinteresado_firma) FROM stdin;
\.


--
-- TOC entry 12645 (class 0 OID 339203)
-- Dependencies: 2211
-- Data for Name: ini_predio_insumos; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.ini_predio_insumos (t_id, t_ili_tid, gc_predio_catastro, snr_predio_juridico) FROM stdin;
\.


--
-- TOC entry 12646 (class 0 OID 339207)
-- Dependencies: 2212
-- Data for Name: op_acuerdotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_acuerdotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
1	Operacion_V2_10.OP_AcuerdoTipo	\N	0	Acuerdo	\N	f	Acuerdo	Existe un acuerdo sobre la posición del punto
2	Operacion_V2_10.OP_AcuerdoTipo	\N	1	Desacuerdo	\N	f	Desacuerdo	Existe un desacuerdo sobre la posición del punto
\.


--
-- TOC entry 12647 (class 0 OID 339214)
-- Dependencies: 2213
-- Data for Name: op_agrupacion_interesados; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_agrupacion_interesados (t_id, t_ili_tid, tipo, nombre, comienzo_vida_util_version, fin_vida_util_version, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12648 (class 0 OID 339222)
-- Dependencies: 2214
-- Data for Name: op_condicionprediotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_condicionprediotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
318	Operacion_V2_10.OP_CondicionPredioTipo	\N	0	NPH	\N	f	No propiedad horizontal	\N
319	Operacion_V2_10.OP_CondicionPredioTipo	\N	1	PH.Matriz	\N	f	(Propiedad horizontal) Matriz	\N
320	Operacion_V2_10.OP_CondicionPredioTipo	\N	2	PH.Unidad_Predial	\N	f	(Propiedad horizontal) Unidad Predial	\N
321	Operacion_V2_10.OP_CondicionPredioTipo	\N	3	Condominio.Matriz	\N	f	(Condominio) Matriz	\N
322	Operacion_V2_10.OP_CondicionPredioTipo	\N	4	Condominio.Unidad_Predial	\N	f	(Condominio) Unidad predial	\N
323	Operacion_V2_10.OP_CondicionPredioTipo	\N	5	Mejora.PH	\N	f	(Mejora) Propiedad horizontal	\N
324	Operacion_V2_10.OP_CondicionPredioTipo	\N	6	Mejora.NPH	\N	f	(Mejora) No propiedad horizontal	\N
325	Operacion_V2_10.OP_CondicionPredioTipo	\N	7	Parque_Cementerio.Matriz	\N	f	(Parque cementerio) Matriz	\N
326	Operacion_V2_10.OP_CondicionPredioTipo	\N	8	Parque_Cementerio.Unidad_Predial	\N	f	(Parque Cementerio) Unidad predial	\N
327	Operacion_V2_10.OP_CondicionPredioTipo	\N	9	Via	\N	f	Vía	\N
328	Operacion_V2_10.OP_CondicionPredioTipo	\N	10	Bien_Uso_Publico	\N	f	Bien de uso público	\N
\.


--
-- TOC entry 12649 (class 0 OID 339229)
-- Dependencies: 2215
-- Data for Name: op_construccion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_construccion (t_id, t_ili_tid, identificador, tipo_construccion, tipo_dominio, numero_pisos, numero_sotanos, numero_mezanines, numero_semisotanos, codigo_edificacion, area_construccion, altura, avaluo_construccion, dimension, etiqueta, relacion_superficie, geometria, comienzo_vida_util_version, fin_vida_util_version, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12650 (class 0 OID 339245)
-- Dependencies: 2216
-- Data for Name: op_construccionplantatipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_construccionplantatipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
117	Operacion_V2_10.OP_ConstruccionPlantaTipo	\N	0	Piso	\N	f	Piso	\N
118	Operacion_V2_10.OP_ConstruccionPlantaTipo	\N	1	Mezanine	\N	f	Mezanine	\N
119	Operacion_V2_10.OP_ConstruccionPlantaTipo	\N	2	Sotano	\N	f	Sótano	\N
120	Operacion_V2_10.OP_ConstruccionPlantaTipo	\N	3	Semisotano	\N	f	Semisótano	\N
121	Operacion_V2_10.OP_ConstruccionPlantaTipo	\N	4	Subterraneo	\N	f	Subterráneo	\N
\.


--
-- TOC entry 12651 (class 0 OID 339252)
-- Dependencies: 2217
-- Data for Name: op_construcciontipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_construcciontipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
104	Operacion_V2_10.OP_ConstruccionTipo	\N	0	Convencional	\N	f	Convencional	\N
105	Operacion_V2_10.OP_ConstruccionTipo	\N	1	No_Convencional	\N	f	No convencional	\N
\.


--
-- TOC entry 12652 (class 0 OID 339259)
-- Dependencies: 2218
-- Data for Name: op_datos_ph_condominio; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_datos_ph_condominio (t_id, t_ili_tid, area_total_terreno, area_total_terreno_privada, area_total_terreno_comun, area_total_construida, area_total_construida_privada, area_total_construida_comun, torre_no, total_pisos_torre, total_unidades_privadas, total_sotanos, total_unidades_sotanos, op_predio) FROM stdin;
\.


--
-- TOC entry 12653 (class 0 OID 339274)
-- Dependencies: 2219
-- Data for Name: op_derecho; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_derecho (t_id, t_ili_tid, tipo, descripcion, comprobacion_comparte, uso_efectivo, interesado_op_interesado, interesado_op_agrupacion_interesados, unidad, comienzo_vida_util_version, fin_vida_util_version, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12654 (class 0 OID 339282)
-- Dependencies: 2220
-- Data for Name: op_derechotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_derechotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
76	Operacion_V2_10.OP_DerechoTipo	\N	0	Dominio	\N	f	Dominio	Derecho de dominio o propiedad
77	Operacion_V2_10.OP_DerechoTipo	\N	1	Ocupacion	\N	f	Ocupación	\N
78	Operacion_V2_10.OP_DerechoTipo	\N	2	Posesion	\N	f	Posesión	\N
79	Operacion_V2_10.OP_DerechoTipo	\N	3	Derecho_Propiedad_Colectiva	\N	f	Derecho de propiedad colectiva	\N
80	Operacion_V2_10.OP_DerechoTipo	\N	4	Nuda_Propiedad	\N	f	Nuda propiedad	\N
81	Operacion_V2_10.OP_DerechoTipo	\N	5	Usufructo	\N	f	Usufructo	\N
82	Operacion_V2_10.OP_DerechoTipo	\N	6	Tenencia	\N	f	Tenencia	\N
83	Operacion_V2_10.OP_DerechoTipo	\N	7	Minero	\N	f	Minero	\N
\.


--
-- TOC entry 12655 (class 0 OID 339289)
-- Dependencies: 2221
-- Data for Name: op_dominioconstrucciontipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_dominioconstrucciontipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
113	Operacion_V2_10.OP_DominioConstruccionTipo	\N	0	Comun	\N	f	Común	\N
114	Operacion_V2_10.OP_DominioConstruccionTipo	\N	1	Privado	\N	f	Privado	\N
\.


--
-- TOC entry 12656 (class 0 OID 339296)
-- Dependencies: 2222
-- Data for Name: op_fotoidentificaciontipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_fotoidentificaciontipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
106	Operacion_V2_10.OP_FotoidentificacionTipo	\N	0	Visible	\N	f	Visible	\N
107	Operacion_V2_10.OP_FotoidentificacionTipo	\N	1	Estimado	\N	f	Estimado	\N
\.


--
-- TOC entry 12657 (class 0 OID 339303)
-- Dependencies: 2223
-- Data for Name: op_fuenteadministrativa; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_fuenteadministrativa (t_id, t_ili_tid, tipo, ente_emisor, observacion, numero_fuente, estado_disponibilidad, tipo_principal, fecha_documento_fuente, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12658 (class 0 OID 339311)
-- Dependencies: 2224
-- Data for Name: op_fuenteadministrativatipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_fuenteadministrativatipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
141	Operacion_V2_10.OP_FuenteAdministrativaTipo	\N	0	Escritura_Publica	\N	f	Escritura pública	\N
142	Operacion_V2_10.OP_FuenteAdministrativaTipo	\N	1	Sentencia_Judicial	\N	f	Sentencia judicial	\N
143	Operacion_V2_10.OP_FuenteAdministrativaTipo	\N	2	Acto_Administrativo	\N	f	Acto administrativo	\N
144	Operacion_V2_10.OP_FuenteAdministrativaTipo	\N	3	Documento_Privado	\N	f	Documento privado	\N
145	Operacion_V2_10.OP_FuenteAdministrativaTipo	\N	4	Sin_Documento	\N	f	Sin documento	\N
\.


--
-- TOC entry 12659 (class 0 OID 339318)
-- Dependencies: 2225
-- Data for Name: op_fuenteespacial; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_fuenteespacial (t_id, t_ili_tid, nombre, tipo, descripcion, metadato, estado_disponibilidad, tipo_principal, fecha_documento_fuente, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12660 (class 0 OID 339326)
-- Dependencies: 2226
-- Data for Name: op_grupoetnicotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_grupoetnicotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
65	Operacion_V2_10.OP_GrupoEtnicoTipo	\N	0	Indigena	\N	f	Indígena	\N
66	Operacion_V2_10.OP_GrupoEtnicoTipo	\N	1	Rrom	\N	f	Rrom	\N
67	Operacion_V2_10.OP_GrupoEtnicoTipo	\N	2	Raizal	\N	f	Raizal	\N
68	Operacion_V2_10.OP_GrupoEtnicoTipo	\N	3	Palenquero	\N	f	Palenquero	\N
69	Operacion_V2_10.OP_GrupoEtnicoTipo	\N	4	Negro	\N	f	Negro	\N
70	Operacion_V2_10.OP_GrupoEtnicoTipo	\N	5	Afrocolombiano	\N	f	Afrocolombiano	\N
71	Operacion_V2_10.OP_GrupoEtnicoTipo	\N	6	Ninguno	\N	f	Ninguno	\N
\.


--
-- TOC entry 12661 (class 0 OID 339333)
-- Dependencies: 2227
-- Data for Name: op_interesado; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_interesado (t_id, t_ili_tid, tipo, tipo_documento, documento_identidad, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, sexo, grupo_etnico, razon_social, nombre, comienzo_vida_util_version, fin_vida_util_version, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12662 (class 0 OID 339341)
-- Dependencies: 2228
-- Data for Name: op_interesado_contacto; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_interesado_contacto (t_id, t_ili_tid, telefono1, telefono2, domicilio_notificacion, direccion_residencia, correo_electronico, autoriza_notificacion_correo, departamento, municipio, vereda, corregimiento, op_interesado) FROM stdin;
\.


--
-- TOC entry 12663 (class 0 OID 339349)
-- Dependencies: 2229
-- Data for Name: op_interesadodocumentotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_interesadodocumentotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
45	Operacion_V2_10.OP_InteresadoDocumentoTipo	\N	0	Cedula_Ciudadania	\N	f	Cédula de ciudadanía	\N
46	Operacion_V2_10.OP_InteresadoDocumentoTipo	\N	1	Cedula_Extranjeria	\N	f	Cédula de estranjería	\N
47	Operacion_V2_10.OP_InteresadoDocumentoTipo	\N	2	NIT	\N	f	NIT	\N
48	Operacion_V2_10.OP_InteresadoDocumentoTipo	\N	3	Pasaporte	\N	f	Pasaporte	\N
49	Operacion_V2_10.OP_InteresadoDocumentoTipo	\N	4	Tarjeta_Identidad	\N	f	Tarjeta de identidad	\N
50	Operacion_V2_10.OP_InteresadoDocumentoTipo	\N	5	Libreta_Militar	\N	f	Libreta militar	\N
51	Operacion_V2_10.OP_InteresadoDocumentoTipo	\N	6	Registro_Civil	\N	f	Registro civil	\N
52	Operacion_V2_10.OP_InteresadoDocumentoTipo	\N	7	Cedula_Militar	\N	f	Cédula militar	\N
53	Operacion_V2_10.OP_InteresadoDocumentoTipo	\N	8	NUIP	\N	f	NUIP	\N
\.


--
-- TOC entry 12664 (class 0 OID 339356)
-- Dependencies: 2230
-- Data for Name: op_interesadotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_interesadotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
43	Operacion_V2_10.OP_InteresadoTipo	\N	0	Persona_Natural	\N	f	Persona natural	\N
44	Operacion_V2_10.OP_InteresadoTipo	\N	1	Persona_Juridica	\N	f	Persona jurídica	\N
\.


--
-- TOC entry 12665 (class 0 OID 339363)
-- Dependencies: 2231
-- Data for Name: op_lindero; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_lindero (t_id, t_ili_tid, longitud, geometria, localizacion_textual, comienzo_vida_util_version, fin_vida_util_version, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12666 (class 0 OID 339372)
-- Dependencies: 2232
-- Data for Name: op_predio; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_predio (t_id, t_ili_tid, departamento, municipio, id_operacion, tiene_fmi, codigo_orip, matricula_inmobiliaria, numero_predial, numero_predial_anterior, avaluo_catastral, condicion_predio, direccion, nombre, tipo, comienzo_vida_util_version, fin_vida_util_version, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12667 (class 0 OID 339381)
-- Dependencies: 2233
-- Data for Name: op_predio_copropiedad; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_predio_copropiedad (t_id, predio, copropiedad) FROM stdin;
\.


--
-- TOC entry 12668 (class 0 OID 339385)
-- Dependencies: 2234
-- Data for Name: op_predio_insumos_operacion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_predio_insumos_operacion (t_id, t_ili_tid, ini_predio_insumos, op_predio) FROM stdin;
\.


--
-- TOC entry 12669 (class 0 OID 339389)
-- Dependencies: 2235
-- Data for Name: op_puntocontrol; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_puntocontrol (t_id, t_ili_tid, id_punto_control, puntotipo, tipo_punto_control, exactitud_horizontal, exactitud_vertical, posicion_interpolacion, metodoproduccion, geometria, ue_op_construccion, ue_op_terreno, ue_op_servidumbretransito, ue_op_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12670 (class 0 OID 339399)
-- Dependencies: 2236
-- Data for Name: op_puntocontroltipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_puntocontroltipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
192	Operacion_V2_10.OP_PuntoControlTipo	\N	0	Control	\N	f	Control	\N
193	Operacion_V2_10.OP_PuntoControlTipo	\N	1	Apoyo	\N	f	Apoyo	\N
\.


--
-- TOC entry 12671 (class 0 OID 339406)
-- Dependencies: 2237
-- Data for Name: op_puntolevantamiento; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_puntolevantamiento (t_id, t_ili_tid, id_punto_levantamiento, puntotipo, tipo_punto_levantamiento, fotoidentificacion, exactitud_horizontal, exactitud_vertical, posicion_interpolacion, metodoproduccion, geometria, ue_op_construccion, ue_op_terreno, ue_op_servidumbretransito, ue_op_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12672 (class 0 OID 339416)
-- Dependencies: 2238
-- Data for Name: op_puntolevtipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_puntolevtipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
189	Operacion_V2_10.OP_PuntoLevTipo	\N	0	Auxiliar	\N	f	Auxiliar	\N
190	Operacion_V2_10.OP_PuntoLevTipo	\N	1	Construccion	\N	f	Construcción	\N
191	Operacion_V2_10.OP_PuntoLevTipo	\N	2	Servidumbre	\N	f	Servidumbre	\N
\.


--
-- TOC entry 12673 (class 0 OID 339423)
-- Dependencies: 2239
-- Data for Name: op_puntolindero; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_puntolindero (t_id, t_ili_tid, id_punto_lindero, puntotipo, acuerdo, fotoidentificacion, ubicacion_punto, exactitud_horizontal, exactitud_vertical, posicion_interpolacion, metodoproduccion, geometria, ue_op_construccion, ue_op_terreno, ue_op_servidumbretransito, ue_op_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12674 (class 0 OID 339433)
-- Dependencies: 2240
-- Data for Name: op_puntotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_puntotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
281	Operacion_V2_10.OP_PuntoTipo	\N	0	Poste	\N	f	Poste	\N
282	Operacion_V2_10.OP_PuntoTipo	\N	1	Construccion	\N	f	Construcción	\N
283	Operacion_V2_10.OP_PuntoTipo	\N	2	Punto_Dinamico	\N	f	Punto dinámico	Punto referido a los puntos limitantes con elementos hidrográficos
284	Operacion_V2_10.OP_PuntoTipo	\N	3	Elemento_Natural	\N	f	elemento natural	\N
285	Operacion_V2_10.OP_PuntoTipo	\N	4	Piedra	\N	f	Piedra	\N
286	Operacion_V2_10.OP_PuntoTipo	\N	5	Sin_Materializacion	\N	f	Sin materialización	\N
287	Operacion_V2_10.OP_PuntoTipo	\N	6	Mojon	\N	f	Mojón	\N
288	Operacion_V2_10.OP_PuntoTipo	\N	7	Incrustacion	\N	f	Incrustación	\N
289	Operacion_V2_10.OP_PuntoTipo	\N	8	Pilastra	\N	f	Pilastra	\N
\.


--
-- TOC entry 12675 (class 0 OID 339440)
-- Dependencies: 2241
-- Data for Name: op_restriccion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_restriccion (t_id, t_ili_tid, tipo, descripcion, comprobacion_comparte, uso_efectivo, interesado_op_interesado, interesado_op_agrupacion_interesados, unidad, comienzo_vida_util_version, fin_vida_util_version, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12676 (class 0 OID 339448)
-- Dependencies: 2242
-- Data for Name: op_restricciontipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_restricciontipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
3	Operacion_V2_10.OP_RestriccionTipo	\N	0	Servidumbre.Transito	\N	f	(Servidumbre) Tránsito	\N
4	Operacion_V2_10.OP_RestriccionTipo	\N	1	Servidumbre.Aguas_Negras	\N	f	(Servidumbre) Aguas negras	\N
5	Operacion_V2_10.OP_RestriccionTipo	\N	2	Servidumbre.Aire	\N	f	(Servidumbre) Aire	\N
6	Operacion_V2_10.OP_RestriccionTipo	\N	3	Servidumbre.Energia_Electrica	\N	f	(Servidumbre) Energía eléctrica	\N
7	Operacion_V2_10.OP_RestriccionTipo	\N	4	Servidumbre.Gasoducto	\N	f	(Servidumbre) Gasoducto	\N
8	Operacion_V2_10.OP_RestriccionTipo	\N	5	Servidumbre.Luz	\N	f	(Servidumbre) Luz	\N
9	Operacion_V2_10.OP_RestriccionTipo	\N	6	Servidumbre.Oleoducto	\N	f	(Servidumbre) Oleoducto	\N
10	Operacion_V2_10.OP_RestriccionTipo	\N	7	Servidumbre.Agua	\N	f	(Servidumbre) Agua	\N
11	Operacion_V2_10.OP_RestriccionTipo	\N	8	Servidumbre.Minera	\N	f	(Servidumbre) Minera	\N
12	Operacion_V2_10.OP_RestriccionTipo	\N	9	Servidumbre.Legal_Hidrocarburos	\N	f	(Servidumbre) Legal de hidrocarburos	\N
13	Operacion_V2_10.OP_RestriccionTipo	\N	10	Servidumbre.Catenaria	\N	f	(Servidumbre) Catenaria (decreto 738 de 2014, ley 1682 de 2013)	\N
14	Operacion_V2_10.OP_RestriccionTipo	\N	11	Servidumbre.Alcantarillado	\N	f	(Servidumbre) Alcantarillado	\N
15	Operacion_V2_10.OP_RestriccionTipo	\N	12	Servidumbre.Acueducto	\N	f	(Servidumbre) Acueducto	\N
\.


--
-- TOC entry 12677 (class 0 OID 339455)
-- Dependencies: 2243
-- Data for Name: op_servidumbretransito; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_servidumbretransito (t_id, t_ili_tid, area_servidumbre, dimension, etiqueta, relacion_superficie, geometria, comienzo_vida_util_version, fin_vida_util_version, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12678 (class 0 OID 339464)
-- Dependencies: 2244
-- Data for Name: op_sexotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_sexotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
115	Operacion_V2_10.OP_SexoTipo	\N	0	Masculino	\N	f	Masculino	\N
116	Operacion_V2_10.OP_SexoTipo	\N	1	Femenino	\N	f	Femenino	\N
\.


--
-- TOC entry 12679 (class 0 OID 339471)
-- Dependencies: 2245
-- Data for Name: op_terreno; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_terreno (t_id, t_ili_tid, area_terreno, avaluo_terreno, manzana_vereda_codigo, numero_subterraneos, geometria, dimension, etiqueta, relacion_superficie, comienzo_vida_util_version, fin_vida_util_version, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12680 (class 0 OID 339482)
-- Dependencies: 2246
-- Data for Name: op_ubicacionpuntotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_ubicacionpuntotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
166	Operacion_V2_10.OP_UbicacionPuntoTipo	\N	0	Esquinero	\N	f	Esquinero	\N
167	Operacion_V2_10.OP_UbicacionPuntoTipo	\N	1	Medianero	\N	f	Medianero	\N
\.


--
-- TOC entry 12681 (class 0 OID 339489)
-- Dependencies: 2247
-- Data for Name: op_unidadconstruccion; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_unidadconstruccion (t_id, t_ili_tid, identificador, tipo_dominio, tipo_construccion, tipo_unidad_construccion, tipo_planta, planta_ubicacion, total_habitaciones, total_banios, total_locales, total_pisos, uso, anio_construccion, avaluo_construccion, area_construida, area_privada_construida, altura, observaciones, op_construccion, dimension, etiqueta, relacion_superficie, geometria, comienzo_vida_util_version, fin_vida_util_version, espacio_de_nombres, local_id) FROM stdin;
\.


--
-- TOC entry 12682 (class 0 OID 339507)
-- Dependencies: 2248
-- Data for Name: op_unidadconstrucciontipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_unidadconstrucciontipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
329	Operacion_V2_10.OP_UnidadConstruccionTipo	\N	0	Residencial	\N	f	Residencial	\N
330	Operacion_V2_10.OP_UnidadConstruccionTipo	\N	1	Comercial	\N	f	Comercial	\N
331	Operacion_V2_10.OP_UnidadConstruccionTipo	\N	2	Industrial	\N	f	Industrial	\N
332	Operacion_V2_10.OP_UnidadConstruccionTipo	\N	3	Anexo	\N	f	Anexo	\N
\.


--
-- TOC entry 12683 (class 0 OID 339514)
-- Dependencies: 2249
-- Data for Name: op_usouconstipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_usouconstipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
194	Operacion_V2_10.OP_UsoUConsTipo	\N	0	Vivienda_Hasta_3_Pisos	\N	f	Vivienda de hasta 3 pisos	\N
195	Operacion_V2_10.OP_UsoUConsTipo	\N	1	Ramadas_Cobertizos_Caneyes	\N	f	Ramadas, cobertizos o caneyes	\N
196	Operacion_V2_10.OP_UsoUConsTipo	\N	2	Galpones_Gallineros	\N	f	Galpones o gallineros	\N
197	Operacion_V2_10.OP_UsoUConsTipo	\N	3	Establos_Pesebreras_Caballerizas	\N	f	Establos, pesebreras o caballerizas	\N
198	Operacion_V2_10.OP_UsoUConsTipo	\N	4	Cocheras_Banieras_Porquerizas	\N	f	Cocheras, bañeras o porquerizas	\N
199	Operacion_V2_10.OP_UsoUConsTipo	\N	5	Bodega_Casa_Bomba	\N	f	Bodega casa bomba	\N
200	Operacion_V2_10.OP_UsoUConsTipo	\N	6	Industrias	\N	f	Industrias	\N
201	Operacion_V2_10.OP_UsoUConsTipo	\N	7	Silos	\N	f	Silos	\N
202	Operacion_V2_10.OP_UsoUConsTipo	\N	8	Piscinas	\N	f	Piscinas	\N
203	Operacion_V2_10.OP_UsoUConsTipo	\N	9	Tanques	\N	f	Tanques	\N
204	Operacion_V2_10.OP_UsoUConsTipo	\N	10	Beneficiaderos	\N	f	Beneficiaderos	\N
205	Operacion_V2_10.OP_UsoUConsTipo	\N	11	Colegios_Y_Universidades	\N	f	Colegios y universidades	\N
206	Operacion_V2_10.OP_UsoUConsTipo	\N	12	Bibliotecas	\N	f	Bibliotecas	\N
207	Operacion_V2_10.OP_UsoUConsTipo	\N	13	Garajes_Cubiertos	\N	f	Garajes cubiertos	\N
208	Operacion_V2_10.OP_UsoUConsTipo	\N	14	Bodegas_Comerciales_Grandes_Almacenes	\N	f	Bodegas comerciales, grandes almacenes	\N
209	Operacion_V2_10.OP_UsoUConsTipo	\N	15	Secaderos	\N	f	Secaderos	\N
210	Operacion_V2_10.OP_UsoUConsTipo	\N	16	Clinicas_Hospitales_Centros_Medicos	\N	f	Centros hospitales, centros médicos	\N
211	Operacion_V2_10.OP_UsoUConsTipo	\N	17	Pozos	\N	f	Pozos	\N
212	Operacion_V2_10.OP_UsoUConsTipo	\N	18	Kioskos	\N	f	Kioskos	\N
213	Operacion_V2_10.OP_UsoUConsTipo	\N	19	Albercas_Baniaderas	\N	f	Albercas o bañaderas	\N
214	Operacion_V2_10.OP_UsoUConsTipo	\N	20	Hoteles_En_PH	\N	f	Hoteles en propiedad horizontal	\N
215	Operacion_V2_10.OP_UsoUConsTipo	\N	21	Corrales	\N	f	Corrales	\N
216	Operacion_V2_10.OP_UsoUConsTipo	\N	22	Casa_Elbas	\N	f	Casa de elbas	\N
217	Operacion_V2_10.OP_UsoUConsTipo	\N	23	Comercio	\N	f	Comercio	\N
218	Operacion_V2_10.OP_UsoUConsTipo	\N	24	Iglesias	\N	f	Iglesias	\N
219	Operacion_V2_10.OP_UsoUConsTipo	\N	25	Hoteles	\N	f	Hoteles	\N
220	Operacion_V2_10.OP_UsoUConsTipo	\N	26	Clubes_Casinos	\N	f	Clubes o casinos	\N
221	Operacion_V2_10.OP_UsoUConsTipo	\N	27	Oficinas_Consultorios	\N	f	Oficinas o consultorios	\N
222	Operacion_V2_10.OP_UsoUConsTipo	\N	28	Apartamentos_Mas_De_4_Pisos	\N	f	Apartamentos de más de 4 pisos	\N
223	Operacion_V2_10.OP_UsoUConsTipo	\N	29	Restaurante	\N	f	Restaurante	\N
224	Operacion_V2_10.OP_UsoUConsTipo	\N	30	Pensiones_Residencias	\N	f	Pensiones o residencias	\N
225	Operacion_V2_10.OP_UsoUConsTipo	\N	31	Puesto_De_Salud	\N	f	Puesto de salud	\N
226	Operacion_V2_10.OP_UsoUConsTipo	\N	32	Parqueaderos	\N	f	Parqueaderos	\N
227	Operacion_V2_10.OP_UsoUConsTipo	\N	33	Barracas	\N	f	Barracas	\N
228	Operacion_V2_10.OP_UsoUConsTipo	\N	34	Teatro_Cinemas	\N	f	Teatro o cinemas	\N
229	Operacion_V2_10.OP_UsoUConsTipo	\N	35	Aulas_De_Clase	\N	f	Aulas de clase	\N
230	Operacion_V2_10.OP_UsoUConsTipo	\N	36	Coliseos	\N	f	Coliseos	\N
231	Operacion_V2_10.OP_UsoUConsTipo	\N	37	Casas_De_Culto	\N	f	Casas de culto	\N
232	Operacion_V2_10.OP_UsoUConsTipo	\N	38	Talleres	\N	f	Talleres	\N
233	Operacion_V2_10.OP_UsoUConsTipo	\N	39	Jardin_Infantil_En_Casa	\N	f	Jardín infantil en casa	\N
234	Operacion_V2_10.OP_UsoUConsTipo	\N	40	Torres_De_Enfriamiento	\N	f	Torres de enfriamiento	\N
235	Operacion_V2_10.OP_UsoUConsTipo	\N	41	Muelles	\N	f	Muelles	\N
236	Operacion_V2_10.OP_UsoUConsTipo	\N	42	Estacion_De_Bombeo	\N	f	Estación de bombeo	\N
237	Operacion_V2_10.OP_UsoUConsTipo	\N	43	Estadio_Plaza_De_Toros	\N	f	Estadio, plaza de toros	\N
238	Operacion_V2_10.OP_UsoUConsTipo	\N	44	Carceles	\N	f	Cárceles	\N
239	Operacion_V2_10.OP_UsoUConsTipo	\N	45	Parque_Cementerio	\N	f	Parque cementerio	\N
240	Operacion_V2_10.OP_UsoUConsTipo	\N	46	Vivienda_Colonial	\N	f	Vivienda colonial	\N
241	Operacion_V2_10.OP_UsoUConsTipo	\N	47	Comercio_Colonial	\N	f	Comercio colonial	\N
242	Operacion_V2_10.OP_UsoUConsTipo	\N	48	Oficinas_Consultorios_Colonial	\N	f	Oficinas o consultorios colonial	\N
243	Operacion_V2_10.OP_UsoUConsTipo	\N	49	Aptos_En_Edificios_4_5_Pisos	\N	f	Apartamentos en edificios de 4 o 5 pisos	\N
244	Operacion_V2_10.OP_UsoUConsTipo	\N	50	Centros_Comerciales	\N	f	Centros comerciales	\N
245	Operacion_V2_10.OP_UsoUConsTipo	\N	51	Canchas_De_Tenis	\N	f	Canchas de tenis	\N
246	Operacion_V2_10.OP_UsoUConsTipo	\N	52	Toboganes	\N	f	Toboganes	\N
247	Operacion_V2_10.OP_UsoUConsTipo	\N	53	Vivienda_Recreacional	\N	f	Vivienda recreacional	\N
248	Operacion_V2_10.OP_UsoUConsTipo	\N	54	Camaroneras	\N	f	Camaroneras	\N
249	Operacion_V2_10.OP_UsoUConsTipo	\N	55	Fuertes_Y_Castillos	\N	f	Fuertes y castillos	\N
250	Operacion_V2_10.OP_UsoUConsTipo	\N	56	Murallas	\N	f	Murallas	\N
251	Operacion_V2_10.OP_UsoUConsTipo	\N	57	Vivienda_Hasta_3_Pisos_En_PH	\N	f	Vivienda de hasta 3 pisos	\N
252	Operacion_V2_10.OP_UsoUConsTipo	\N	58	Apartamentos_4_Y_Mas_Pisos_En_PH	\N	f	Apartamentos de 4 y más pisos en propiedad horizontal	\N
253	Operacion_V2_10.OP_UsoUConsTipo	\N	59	Vivienda_Recreacional_En_PH	\N	f	Vivienda recreacional en propiedad horizontal	\N
254	Operacion_V2_10.OP_UsoUConsTipo	\N	60	Bodega_Casa_Bomba_En_PH	\N	f	Bodega casa bomba en propiedad horizontal	\N
255	Operacion_V2_10.OP_UsoUConsTipo	\N	61	Bodega_Comercial_En_PH	\N	f	Bodega comercial en propiedad horizontal	\N
256	Operacion_V2_10.OP_UsoUConsTipo	\N	62	Comercio_En_PH	\N	f	Comercio en propiedad horizontal	\N
257	Operacion_V2_10.OP_UsoUConsTipo	\N	63	Centros_Comerciales_En_PH	\N	f	Centros comerciales en propiedad horizontal	\N
258	Operacion_V2_10.OP_UsoUConsTipo	\N	64	Oficinas_Consultorios_En_PH	\N	f	Oficinas o consultorios en propiedad horizontal	\N
259	Operacion_V2_10.OP_UsoUConsTipo	\N	65	Parqueaderos_En_PH	\N	f	Parqueaderos en propiedad horizontal	\N
260	Operacion_V2_10.OP_UsoUConsTipo	\N	66	Garajes_En_PH	\N	f	Garajes en propiedad horizontal	\N
261	Operacion_V2_10.OP_UsoUConsTipo	\N	67	Industria_En_PH	\N	f	Industria en propiedad horizontal	\N
262	Operacion_V2_10.OP_UsoUConsTipo	\N	68	Marquesinas_Patios_Cubiertos	\N	f	Marquesinas, patios o cubiertos	\N
263	Operacion_V2_10.OP_UsoUConsTipo	\N	69	Lagunas_De_Oxidacion	\N	f	Lagunas de oxidación	\N
264	Operacion_V2_10.OP_UsoUConsTipo	\N	70	Via_Ferrea	\N	f	Vía férrea	\N
265	Operacion_V2_10.OP_UsoUConsTipo	\N	71	Carretera	\N	f	Carretera	\N
266	Operacion_V2_10.OP_UsoUConsTipo	\N	72	Teatro_Cinema_En_PH	\N	f	Teatro o cinema en propiedad horizontal	\N
267	Operacion_V2_10.OP_UsoUConsTipo	\N	73	Iglesia_En_PH	\N	f	Iglesia en propiedad horizontal	\N
268	Operacion_V2_10.OP_UsoUConsTipo	\N	74	Restaurante_En_PH	\N	f	Restaurante en propiedad horizontal	\N
269	Operacion_V2_10.OP_UsoUConsTipo	\N	75	Hotel_Colonial	\N	f	Hotel colonial	\N
270	Operacion_V2_10.OP_UsoUConsTipo	\N	76	Restaurante_Colonial	\N	f	Restaurante colonial	\N
271	Operacion_V2_10.OP_UsoUConsTipo	\N	77	Entidad_Educativa_Colonial_Colegio_Colonial	\N	f	Entidad educativa colonial o colegio colonial	\N
272	Operacion_V2_10.OP_UsoUConsTipo	\N	78	Cimientos_Estructura_Muros_Y_Placa_Base	\N	f	Cimientos de estructura, muros y placa base	\N
\.


--
-- TOC entry 12684 (class 0 OID 339521)
-- Dependencies: 2250
-- Data for Name: op_viatipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.op_viatipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
84	Operacion_V2_10.OP_ViaTipo	\N	0	Arteria	\N	f	Arteria	\N
85	Operacion_V2_10.OP_ViaTipo	\N	1	Autopista	\N	f	Autopista	\N
86	Operacion_V2_10.OP_ViaTipo	\N	2	Carreteable	\N	f	Carreteable	\N
87	Operacion_V2_10.OP_ViaTipo	\N	3	Cicloruta	\N	f	Ciclorruta	\N
88	Operacion_V2_10.OP_ViaTipo	\N	4	Colectora	\N	f	Colectora	\N
89	Operacion_V2_10.OP_ViaTipo	\N	5	Departamental	\N	f	Departamental	\N
90	Operacion_V2_10.OP_ViaTipo	\N	6	Ferrea	\N	f	Férrea	\N
91	Operacion_V2_10.OP_ViaTipo	\N	7	Local	\N	f	Local	\N
92	Operacion_V2_10.OP_ViaTipo	\N	8	Metro_o_Metrovia	\N	f	Metro o metrovía	\N
93	Operacion_V2_10.OP_ViaTipo	\N	9	Nacional	\N	f	Nacional	\N
94	Operacion_V2_10.OP_ViaTipo	\N	10	Ordinaria	\N	f	Ordinaria	\N
95	Operacion_V2_10.OP_ViaTipo	\N	11	Peatonal	\N	f	Peatonal	\N
96	Operacion_V2_10.OP_ViaTipo	\N	12	Principal	\N	f	Principal	\N
97	Operacion_V2_10.OP_ViaTipo	\N	13	Privada	\N	f	Privada	\N
98	Operacion_V2_10.OP_ViaTipo	\N	14	Secundaria	\N	f	Secundaria	\N
99	Operacion_V2_10.OP_ViaTipo	\N	15	Troncal	\N	f	Troncal	\N
\.


--
-- TOC entry 12685 (class 0 OID 339528)
-- Dependencies: 2251
-- Data for Name: snr_calidadderechotipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.snr_calidadderechotipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
54	Datos_SNR_V2_10.SNR_CalidadDerechoTipo	\N	0	Dominio	\N	f	Dominio	\N
55	Datos_SNR_V2_10.SNR_CalidadDerechoTipo	\N	1	Falsa_Tradicion	\N	f	Falsa tradición	\N
56	Datos_SNR_V2_10.SNR_CalidadDerechoTipo	\N	2	Nuda_Propiedad	\N	f	Nuda propiedad	\N
57	Datos_SNR_V2_10.SNR_CalidadDerechoTipo	\N	3	Propiedad_Colectiva	\N	f	Propiedad colectiva	\N
58	Datos_SNR_V2_10.SNR_CalidadDerechoTipo	\N	4	Usufructo	\N	f	Usufructo	\N
\.


--
-- TOC entry 12686 (class 0 OID 339535)
-- Dependencies: 2252
-- Data for Name: snr_derecho; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.snr_derecho (t_id, t_ili_tid, calidad_derecho_registro, codigo_naturaleza_juridica, snr_fuente_derecho, snr_predio_registro) FROM stdin;
\.


--
-- TOC entry 12687 (class 0 OID 339539)
-- Dependencies: 2253
-- Data for Name: snr_documentotitulartipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.snr_documentotitulartipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
146	Datos_SNR_V2_10.SNR_DocumentoTitularTipo	\N	0	Cedula_Ciudadania	\N	f	Cédula de ciudadanía	\N
147	Datos_SNR_V2_10.SNR_DocumentoTitularTipo	\N	1	Cedula_Extranjeria	\N	f	Cédula de extranjería	\N
148	Datos_SNR_V2_10.SNR_DocumentoTitularTipo	\N	2	NIT	\N	f	NIT	\N
149	Datos_SNR_V2_10.SNR_DocumentoTitularTipo	\N	3	Pasaporte	\N	f	Pasaporte	\N
150	Datos_SNR_V2_10.SNR_DocumentoTitularTipo	\N	4	Tarjeta_Identidad	\N	f	Tarjeta de identidad	\N
151	Datos_SNR_V2_10.SNR_DocumentoTitularTipo	\N	5	Libreta_Militar	\N	f	Libreta militar	\N
152	Datos_SNR_V2_10.SNR_DocumentoTitularTipo	\N	6	Registro_Civil	\N	f	Registro civil	\N
153	Datos_SNR_V2_10.SNR_DocumentoTitularTipo	\N	7	Cedula_Militar	\N	f	Cédula militar	\N
154	Datos_SNR_V2_10.SNR_DocumentoTitularTipo	\N	8	NUIP	\N	f	NUIP	\N
155	Datos_SNR_V2_10.SNR_DocumentoTitularTipo	\N	9	Secuencial_SNR	\N	f	Secuencial SNR	\N
\.


--
-- TOC entry 12688 (class 0 OID 339546)
-- Dependencies: 2254
-- Data for Name: snr_fuente_cabidalinderos; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.snr_fuente_cabidalinderos (t_id, t_ili_tid, tipo_documento, numero_documento, fecha_documento, ente_emisor, ciudad_emisora) FROM stdin;
\.


--
-- TOC entry 12689 (class 0 OID 339553)
-- Dependencies: 2255
-- Data for Name: snr_fuente_derecho; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.snr_fuente_derecho (t_id, t_ili_tid, tipo_documento, numero_documento, fecha_documento, ente_emisor, ciudad_emisora) FROM stdin;
\.


--
-- TOC entry 12690 (class 0 OID 339560)
-- Dependencies: 2256
-- Data for Name: snr_fuentetipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.snr_fuentetipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
133	Datos_SNR_V2_10.SNR_FuenteTipo	\N	0	Acto_Administrativo	\N	f	Acto administrativo	\N
134	Datos_SNR_V2_10.SNR_FuenteTipo	\N	1	Escritura_Publica	\N	f	Escritura pública	\N
135	Datos_SNR_V2_10.SNR_FuenteTipo	\N	2	Sentencia_Judicial	\N	f	Sentencia judicial	\N
\.


--
-- TOC entry 12691 (class 0 OID 339567)
-- Dependencies: 2257
-- Data for Name: snr_personatitulartipo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.snr_personatitulartipo (t_id, thisclass, baseclass, itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
38	Datos_SNR_V2_10.SNR_PersonaTitularTipo	\N	0	Persona_Natural	\N	f	Persona natural	\N
39	Datos_SNR_V2_10.SNR_PersonaTitularTipo	\N	1	Persona_Juridica	\N	f	Persona jurídica	\N
\.


--
-- TOC entry 12692 (class 0 OID 339574)
-- Dependencies: 2258
-- Data for Name: snr_predio_registro; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.snr_predio_registro (t_id, t_ili_tid, codigo_orip, matricula_inmobiliaria, numero_predial_nuevo_en_fmi, numero_predial_anterior_en_fmi, cabida_linderos, matricula_inmobiliaria_matriz, fecha_datos, snr_fuente_cabidalinderos) FROM stdin;
\.


--
-- TOC entry 12693 (class 0 OID 339581)
-- Dependencies: 2259
-- Data for Name: snr_titular; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.snr_titular (t_id, t_ili_tid, tipo_persona, tipo_documento, numero_documento, nombres, primer_apellido, segundo_apellido, razon_social) FROM stdin;
\.


--
-- TOC entry 12694 (class 0 OID 339588)
-- Dependencies: 2260
-- Data for Name: snr_titular_derecho; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.snr_titular_derecho (t_id, t_ili_tid, snr_titular, snr_derecho, porcentaje_participacion) FROM stdin;
\.


--
-- TOC entry 12695 (class 0 OID 339593)
-- Dependencies: 2261
-- Data for Name: t_ili2db_attrname; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.t_ili2db_attrname (iliname, sqlname, colowner, target) FROM stdin;
LADM_COL_V1_6.LADM_Nucleo.col_menosCl.ue_menos	ue_menos_op_terreno	col_menoscl	op_terreno
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia.ue	ue_op_construccion	op_puntolindero	op_construccion
Operacion_V2_10.Operacion.OP_Terreno.Numero_Subterraneos	numero_subterraneos	op_terreno	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado	op_puntolevantamiento_transformacion_y_resultado	col_transformacion	op_puntolevantamiento
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	op_puntolindero_procedencia	anystructure	op_puntolindero
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	op_unidadconstruccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_menosCl.ue_menos	ue_menos_op_unidadconstruccion	col_menoscl	op_unidadconstruccion
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda.Codigo_Sector	codigo_sector	gc_vereda	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente	fecha_documento_fuente	op_fuenteespacial	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia.ue	ue_op_servidumbretransito	op_puntolindero	op_servidumbretransito
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos.Archivo	snr_fuente_cabidlndros_archivo	extarchivo	snr_fuente_cabidalinderos
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Numero_Pisos	numero_pisos	gc_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Urbano.Geometria	geometria	gc_sector_urbano	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Matricula_Inmobiliaria_Catastro	matricula_inmobiliaria_catastro	gc_predio_catastro	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro.Tipo_Avaluo	tipo_avaluo	gc_perimetro	\N
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Area_Total_Terreno_Privada	area_total_terreno_privada	op_datos_ph_condominio	\N
LADM_COL_V1_6.LADM_Nucleo.COL_DRR.Comprobacion_Comparte	comprobacion_comparte	op_derecho	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Municipio	codigo_municipio	gc_perimetro	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Unidades_Sotano	total_unidades_sotano	gc_datos_ph_condiminio	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital	area_terreno_digital	gc_terreno	\N
Operacion_V2_10.Operacion.OP_Interesado.Documento_Identidad	documento_identidad	op_interesado	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Etiqueta	etiqueta	op_construccion	\N
Operacion_V2_10.Operacion.OP_PuntoControl.ID_Punto_Control	id_punto_control	op_puntocontrol	\N
Operacion_V2_10.Operacion.OP_PuntoLevantamiento.Tipo_Punto_Levantamiento	tipo_punto_levantamiento	op_puntolevantamiento	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_unidadconstruccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Codigo_Terreno	codigo_terreno	gc_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Condicion_Predio	condicion_predio	gc_predio_catastro	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Area_Privada	area_privada	gc_unidad_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_copropiedad.gc_matriz	gc_matriz	gc_copropiedad	gc_predio_catastro
Operacion_V2_10.Operacion.OP_Interesado.Grupo_Etnico	grupo_etnico	op_interesado	\N
LADM_COL_V1_6.LADM_Nucleo.col_rrrInteresado.interesado	interesado_op_agrupacion_interesados	op_derecho	op_agrupacion_interesados
LADM_COL_V1_6.LADM_Nucleo.COL_VolumenValor.Volumen_Medicion	volumen_medicion	col_volumenvalor	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Pisos	total_pisos	gc_unidad_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Etiqueta	etiqueta	op_unidadconstruccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Locales	total_locales	gc_unidad_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoCcl.punto	punto_op_puntocontrol	col_puntoccl	op_puntocontrol
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Fecha_Datos	fecha_datos	gc_predio_catastro	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Interesado.ext_PID	op_agrupacion_intrsdos_ext_pid	extinteresado	op_agrupacion_interesados
Datos_SNR_V2_10.Datos_SNR.snr_fuente_cabidalinderos.snr_fuente_cabidalinderos	snr_fuente_cabidalinderos	snr_predio_registro	snr_fuente_cabidalinderos
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie	relacion_superficie	op_servidumbretransito	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_interesado	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia.ue	ue_op_unidadconstruccion	op_puntolindero	op_unidadconstruccion
LADM_COL_V1_6.LADM_Nucleo.col_masCcl.ue_mas	ue_mas_op_unidadconstruccion	col_masccl	op_unidadconstruccion
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Letra_Via_Generadora	letra_via_generadora	extdireccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.Geometria	geometria	op_puntocontrol	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_restriccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_responsableFuente.interesado	interesado_op_interesado	col_responsablefuente	op_interesado
LADM_COL_V1_6.LADM_Nucleo.CC_MetodoOperacion.Ddimensiones_Objetivo	ddimensiones_objetivo	cc_metodooperacion	\N
Operacion_V2_10.Operacion.OP_Interesado.Tipo	tipo	op_interesado	\N
LADM_COL_V1_6.LADM_Nucleo.col_baunitComoInteresado.interesado	interesado_op_agrupacion_interesados	col_baunitcomointeresado	op_agrupacion_interesados
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	op_interesado	\N
Operacion_V2_10.Operacion.op_predio_copropiedad.predio	predio	op_predio_copropiedad	op_predio
Operacion_V2_10.Operacion.OP_Interesado.Segundo_Apellido	segundo_apellido	op_interesado	\N
ISO19107_PLANAS_V1.GM_Surface2DListValue.value	avalue	gm_surface2dlistvalue	\N
Operacion_V2_10.Operacion.OP_Predio.Codigo_ORIP	codigo_orip	op_predio	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Predio	tipo_predio	gc_predio_catastro	\N
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Complemento	complemento	extdireccion	\N
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Numero_Predio	numero_predio	extdireccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Identificador	identificador	gc_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Etiqueta	etiqueta	gc_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativa.Numero_Fuente	numero_fuente	op_fuenteadministrativa	\N
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Total_Pisos	total_pisos	op_unidadconstruccion	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	op_restriccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_construccion_predio.gc_predio	gc_predio	gc_construccion	gc_predio_catastro
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho.Ente_Emisor	ente_emisor	snr_fuente_derecho	\N
Operacion_V2_10.Operacion.OP_PuntoLindero.Fotoidentificacion	fotoidentificacion	op_puntolindero	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro.Nombre_Geografico	nombre_geografico	gc_perimetro	\N
LADM_COL_V1_6.LADM_Nucleo.COL_BAUnit.Nombre	nombre	op_predio	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_fuenteespacial	\N
LADM_COL_V1_6.LADM_Nucleo.COL_BAUnit.Tipo	tipo	op_predio	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueFuente.ue	ue_op_unidadconstruccion	col_uefuente	op_unidadconstruccion
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie	relacion_superficie	op_terreno	\N
Datos_SNR_V2_10.Datos_SNR.snr_derecho_predio.snr_predio_registro	snr_predio_registro	snr_derecho	snr_predio_registro
LADM_COL_V1_6.LADM_Nucleo.col_puntoFuente.punto	punto_op_puntolindero	col_puntofuente	op_puntolindero
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Manzana.Codigo	codigo	gc_manzana	\N
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Fecha_Grabacion	fecha_grabacion	extarchivo	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Terreno_Comun	area_total_terreno_comun	gc_datos_ph_condiminio	\N
Operacion_V2_10.Operacion.OP_PuntoLevantamiento.Fotoidentificacion	fotoidentificacion	op_puntolevantamiento	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Etiqueta	etiqueta	op_servidumbretransito	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda.Codigo	codigo	gc_vereda	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Etiqueta	etiqueta	op_terreno	\N
LADM_COL_V1_6.LADM_Nucleo.col_relacionFuenteUespacial.fuente_espacial	fuente_espacial	col_relacionfuenteuespacial	op_fuenteespacial
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Area_Privada_Construida	area_privada_construida	op_unidadconstruccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Etiqueta	etiqueta	gc_unidad_construccion	\N
Operacion_V2_10.Operacion.OP_Construccion.Tipo_Dominio	tipo_dominio	op_construccion	\N
Operacion_V2_10.Operacion.OP_Construccion.Numero_Mezanines	numero_mezanines	op_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoCcl.punto	punto_op_puntolevantamiento	col_puntoccl	op_puntolevantamiento
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_terreno	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Geometria	geometria	gc_comisiones_unidad_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Rural.Geometria	geometria	gc_sector_rural	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Planta	planta	gc_unidad_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Catastro	tipo_catastro	gc_predio_catastro	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Estado_Alerta	estado_alerta	gc_predio_catastro	\N
Operacion_V2_10.Operacion.op_predio_insumos_operacion.op_predio	op_predio	op_predio_insumos_operacion	op_predio
LADM_COL_V1_6.LADM_Nucleo.col_baunitFuente.unidad	unidad	col_baunitfuente	op_predio
LADM_COL_V1_6.LADM_Nucleo.col_puntoCl.punto	punto_op_puntolindero	col_puntocl	op_puntolindero
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Departamento	codigo_departamento	gc_perimetro	\N
LADM_COL_V1_6.LADM_Nucleo.col_topografoFuente.topografo	topografo_op_agrupacion_interesados	col_topografofuente	op_agrupacion_interesados
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Fecha_Alerta	fecha_alerta	gc_predio_catastro	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_fuenteadministrativa	\N
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Area_Construida	area_construida	op_unidadconstruccion	\N
Operacion_V2_10.Operacion.op_predio_insumos_operacion.ini_predio_insumos	ini_predio_insumos	op_predio_insumos_operacion	ini_predio_insumos
Operacion_V2_10.Operacion.OP_PuntoLindero.PuntoTipo	puntotipo	op_puntolindero	\N
LADM_COL_V1_6.LADM_Nucleo.col_menosCl.ue_menos	ue_menos_op_construccion	col_menoscl	op_construccion
LADM_COL_V1_6.LADM_Nucleo.col_miembros.interesado	interesado_op_agrupacion_interesados	col_miembros	op_agrupacion_interesados
Operacion_V2_10.Operacion.OP_PuntoLindero.Exactitud_Horizontal	exactitud_horizontal	op_puntolindero	\N
LADM_COL_V1_6.LADM_Nucleo.col_masCcl.ue_mas	ue_mas_op_terreno	col_masccl	op_terreno
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Nombre	codigo_nombre	gc_perimetro	\N
LADM_COL_V1_6.LADM_Nucleo.ExtRedServiciosFisica.Ext_Interesado_Administrador_ID	extredserviciosfisica_ext_interesado_administrador_id	extinteresado	extredserviciosfisica
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	op_servidumbretransito	\N
Operacion_V2_10.Operacion.OP_PuntoLindero.Ubicacion_Punto	ubicacion_punto	op_puntolindero	\N
LADM_COL_V1_6.LADM_Nucleo.col_menosCl.ue_menos	ue_menos_op_servidumbretransito	col_menoscl	op_servidumbretransito
Datos_SNR_V2_10.Datos_SNR.snr_titular_derecho.snr_derecho	snr_derecho	snr_titular_derecho	snr_derecho
Operacion_V2_10.Operacion.OP_PuntoLevantamiento.PuntoTipo	puntotipo	op_puntolevantamiento	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Barrio.Codigo_Sector	codigo_sector	gc_barrio	\N
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Total_Locales	total_locales	op_unidadconstruccion	\N
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Tipo_Direccion	tipo_direccion	extdireccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro.Geometria	geometria	gc_perimetro	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_puntolevantamiento	\N
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Total_Sotanos	total_sotanos	op_datos_ph_condominio	\N
Operacion_V2_10.Operacion.OP_Predio.Municipio	municipio	op_predio	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	op_construccion	\N
Operacion_V2_10.Operacion.OP_ServidumbreTransito.Area_Servidumbre	area_servidumbre	op_servidumbretransito	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID	op_fuenteadministrtiva_ext_archivo_id	extarchivo	op_fuenteadministrativa
Operacion_V2_10.Operacion.OP_Predio.Direccion	direccion	op_predio	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_predio	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueFuente.ue	ue_op_servidumbretransito	col_uefuente	op_servidumbretransito
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie	relacion_superficie	op_construccion	\N
Operacion_V2_10.Operacion.OP_PuntoControl.PuntoTipo	puntotipo	op_puntocontrol	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	op_unidadconstruccion_calidad	anystructure	op_unidadconstruccion
LADM_COL_V1_6.LADM_Nucleo.col_puntoCcl.ccl	ccl	col_puntoccl	op_lindero
ISO19107_PLANAS_V1.GM_MultiSurface2D.geometry	gm_multisurface2d_geometry	gm_surface2dlistvalue	gm_multisurface2d
LADM_COL_V1_6.LADM_Nucleo.col_ueUeGrupo.parte	parte_op_unidadconstruccion	col_ueuegrupo	op_unidadconstruccion
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie	relacion_superficie	op_unidadconstruccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Transformacion.Localizacion_Transformada	localizacion_transformada	col_transformacion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno.Numero_Subterraneos	numero_subterraneos	gc_terreno	\N
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Municipio	municipio	op_interesado_contacto	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueUeGrupo.parte	parte_op_terreno	col_ueuegrupo	op_terreno
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Geometria	geometria	gc_unidad_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Localizacion	localizacion	extdireccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_cclFuente.ccl	ccl	col_cclfuente	op_lindero
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Identificador	identificador	op_unidadconstruccion	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho.Ciudad_Emisora	ciudad_emisora	snr_fuente_derecho	\N
Operacion_V2_10.Operacion.op_ph_predio.op_predio	op_predio	op_datos_ph_condominio	op_predio
LADM_COL_V1_6.LADM_Nucleo.Imagen.uri	uri	imagen	\N
LADM_COL_V1_6.LADM_Nucleo.COL_DRR.Descripcion	descripcion	op_restriccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Interesado.Nombre	nombre	op_interesado	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	op_restriccion_procedencia	anystructure	op_restriccion
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID	op_unidadconstruccion_ext_direccion_id	extdireccion	op_unidadconstruccion
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia.ue	ue_op_terreno	op_puntocontrol	op_terreno
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Segundo_Apellido	segundo_apellido	gc_propietario	\N
Operacion_V2_10.Operacion.OP_FuenteAdministrativa.Ente_Emisor	ente_emisor	op_fuenteadministrativa	\N
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Tipo_Planta	tipo_planta	op_unidadconstruccion	\N
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Domicilio_Notificacion	domicilio_notificacion	op_interesado_contacto	\N
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Tipo_Dominio	tipo_dominio	op_unidadconstruccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_menosCcl.ue_menos	ue_menos_op_servidumbretransito	col_menosccl	op_servidumbretransito
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos.Fecha_Documento	fecha_documento	snr_fuente_cabidalinderos	\N
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Ciudad	sector_ciudad	extdireccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_copropiedad.gc_unidad	gc_unidad	gc_copropiedad	gc_predio_catastro
Operacion_V2_10.Operacion.OP_Interesado.Razon_Social	razon_social	op_interesado	\N
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Autoriza_Notificacion_Correo	autoriza_notificacion_correo	op_interesado_contacto	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID	op_fuenteespacial_ext_archivo_id	extarchivo	op_fuenteespacial
Operacion_V2_10.Operacion.op_predio_copropiedad.coeficiente	op_predio_copropiedad_coeficiente	fraccion	op_predio_copropiedad
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Urbano.Codigo	codigo	gc_sector_urbano	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Volumen	op_unidadconstruccion_volumen	col_volumenvalor	op_unidadconstruccion
Datos_SNR_V2_10.Datos_SNR.snr_titular_derecho.snr_titular	snr_titular	snr_titular_derecho	snr_titular
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Tipo_Dominio	tipo_dominio	gc_unidad_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Dimension	dimension	op_construccion	\N
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Altura	altura	op_unidadconstruccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_ph_predio.gc_predio	gc_predio	gc_datos_ph_condiminio	gc_predio_catastro
Datos_SNR_V2_10.Datos_SNR.snr_titular_derecho.Porcentaje_Participacion	porcentaje_participacion	snr_titular_derecho	\N
Operacion_V2_10.Operacion.OP_Predio.Numero_Predial	numero_predial	op_predio	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	op_predio_procedencia	anystructure	op_predio
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	op_puntolindero_calidad	anystructure	op_puntolindero
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Segundo_Apellido	segundo_apellido	snr_titular	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.Posicion_Interpolacion	posicion_interpolacion	op_puntocontrol	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	op_unidadconstruccion	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Fecha_Datos	fecha_datos	snr_predio_registro	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Primer_Apellido	primer_apellido	gc_propietario	\N
Operacion_V2_10.Operacion.OP_Construccion.Numero_Pisos	numero_pisos	op_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_DRR.Descripcion	descripcion	op_derecho	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Matricula_Inmobiliaria_Matriz	matricula_inmobiliaria_matriz	snr_predio_registro	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Tipo_Documento	tipo_documento	gc_propietario	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Geometria	geometria	gc_construccion	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Codigo_ORIP	codigo_orip	snr_predio_registro	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_agrupacion_interesados	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	op_terreno	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Transformacion.Transformacion	col_transformacion_transformacion	cc_metodooperacion	col_transformacion
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_copropiedad.Coeficiente_Copropiedad	coeficiente_copropiedad	gc_copropiedad	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueBaunit.ue	ue_op_servidumbretransito	col_uebaunit	op_servidumbretransito
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda.Geometria	geometria	gc_vereda	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia.ue	ue_op_terreno	op_puntolevantamiento	op_terreno
Operacion_V2_10.Operacion.OP_PuntoControl.Exactitud_Vertical	exactitud_vertical	op_puntocontrol	\N
LADM_COL_V1_6.LADM_Nucleo.COL_DRR.Uso_Efectivo	uso_efectivo	op_restriccion	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_puntolindero	\N
LADM_COL_V1_6.LADM_Nucleo.col_miembros.participacion	col_miembros_participacion	fraccion	col_miembros
LADM_COL_V1_6.LADM_Nucleo.Fraccion.Denominador	denominador	fraccion	\N
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Tipo_Unidad_Construccion	tipo_unidad_construccion	op_unidadconstruccion	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	op_construccion_calidad	anystructure	op_construccion
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	op_puntolindero	\N
Operacion_V2_10.Operacion.OP_PuntoLevantamiento.Exactitud_Vertical	exactitud_vertical	op_puntolevantamiento	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	op_agrupacion_intrsdos_calidad	anystructure	op_agrupacion_interesados
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Area	op_construccion_area	col_areavalor	op_construccion
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	op_agrupacion_interesados	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	op_puntolevantamiento	\N
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Nombre_Predio	nombre_predio	extdireccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Barrio.Codigo	codigo	gc_barrio	\N
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Uso	uso	op_unidadconstruccion	\N
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Tipo_Construccion	tipo_construccion	op_unidadconstruccion	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Cabida_Linderos	cabida_linderos	snr_predio_registro	\N
Operacion_V2_10.Operacion.OP_Terreno.Avaluo_Terreno	avaluo_terreno	op_terreno	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_propietario_predio.gc_predio_catastro	gc_predio_catastro	gc_propietario	gc_predio_catastro
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Area_Total_Terreno_Comun	area_total_terreno_comun	op_datos_ph_condominio	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueFuente.fuente_espacial	fuente_espacial	col_uefuente	op_fuenteespacial
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Area_Construida	area_construida	gc_unidad_construccion	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos.Ciudad_Emisora	ciudad_emisora	snr_fuente_cabidalinderos	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.Posicion_Interpolacion	posicion_interpolacion	op_puntolindero	\N
Operacion_V2_10.Operacion.OP_Interesado.Primer_Apellido	primer_apellido	op_interesado	\N
LADM_COL_V1_6.LADM_Nucleo.col_masCcl.ue_mas	ue_mas_op_servidumbretransito	col_masccl	op_servidumbretransito
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Anio_Construccion	anio_construccion	gc_unidad_construccion	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Numero_Predial_Anterior_en_FMI	numero_predial_anterior_en_fmi	snr_predio_registro	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_puntolevantamiento	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	op_unidadconstruccion_procedencia	anystructure	op_unidadconstruccion
LADM_COL_V1_6.LADM_Nucleo.col_unidadFuente.fuente_administrativa	fuente_administrativa	col_unidadfuente	op_fuenteadministrativa
LADM_COL_V1_6.LADM_Nucleo.COL_AreaValor.type	atype	col_areavalor	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Numero_Predial_Nuevo_en_FMI	numero_predial_nuevo_en_fmi	snr_predio_registro	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Area	op_unidadconstruccion_area	col_areavalor	op_unidadconstruccion
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_servidumbretransito	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	op_construccion_procedencia	anystructure	op_construccion
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	op_agrupacion_intrsdos_procedencia	anystructure	op_agrupacion_interesados
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID	op_construccion_ext_direccion_id	extdireccion	op_construccion
LADM_COL_V1_6.LADM_Nucleo.col_puntoCl.punto	punto_op_puntocontrol	col_puntocl	op_puntocontrol
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Geometria	geometria	op_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_terreno_predio.gc_predio	gc_predio	gc_terreno	gc_predio_catastro
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Extraccion	extraccion	extarchivo	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueUeGrupo.parte	parte_op_construccion	col_ueuegrupo	op_construccion
LADM_COL_V1_6.LADM_Nucleo.col_puntoCl.punto	punto_op_puntolevantamiento	col_puntocl	op_puntolevantamiento
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia.ue	ue_op_terreno	op_puntolindero	op_terreno
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Construida_Comun	area_total_construida_comun	gc_datos_ph_condiminio	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Tipo_Persona	tipo_persona	snr_titular	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Torre_No	torre_no	gc_datos_ph_condiminio	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Geometria	geometria	op_servidumbretransito	\N
Operacion_V2_10.Operacion.OP_Construccion.Area_Construccion	area_construccion	op_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	op_lindero	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	op_restriccion_calidad	anystructure	op_restriccion
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.Posicion_Interpolacion	posicion_interpolacion	op_puntolevantamiento	\N
LADM_COL_V1_6.LADM_Nucleo.ExtRedServiciosFisica.Orientada	orientada	extredserviciosfisica	\N
LADM_COL_V1_6.LADM_Nucleo.col_relacionFuente.fuente_administrativa	fuente_administrativa	col_relacionfuente	op_fuenteadministrativa
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Matricula_Inmobiliaria	matricula_inmobiliaria	snr_predio_registro	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente	fecha_documento_fuente	op_fuenteadministrativa	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Uso	uso	gc_unidad_construccion	\N
Operacion_V2_10.Operacion.OP_Predio.Avaluo_Catastral	avaluo_catastral	op_predio	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Entidad_Emisora_Alerta	entidad_emisora_alerta	gc_predio_catastro	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Numero_Mezanines	numero_mezanines	gc_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Destinacion_Economica	destinacion_economica	gc_predio_catastro	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoFuente.punto	punto_op_puntolevantamiento	col_puntofuente	op_puntolevantamiento
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Area_Total_Construida_Comun	area_total_construida_comun	op_datos_ph_condominio	\N
Operacion_V2_10.Operacion.OP_Construccion.Avaluo_Construccion	avaluo_construccion	op_construccion	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos.Numero_Documento	numero_documento	snr_fuente_cabidalinderos	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	op_predio_calidad	anystructure	op_predio
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Dimension	dimension	op_servidumbretransito	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	op_puntocontrol	\N
LADM_COL_V1_6.LADM_Nucleo.col_masCcl.ccl_mas	ccl_mas	col_masccl	op_lindero
Operacion_V2_10.Operacion.OP_Interesado.Primer_Nombre	primer_nombre	op_interesado	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia.ue	ue_op_servidumbretransito	op_puntolevantamiento	op_servidumbretransito
LADM_COL_V1_6.LADM_Nucleo.COL_AreaValor.areaSize	areasize	col_areavalor	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	op_terreno	\N
Operacion_V2_10.Operacion.OP_Construccion.Identificador	identificador	op_construccion	\N
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Telefono2	telefono2	op_interesado_contacto	\N
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Fecha_Aceptacion	fecha_aceptacion	extarchivo	\N
Operacion_V2_10.Operacion.OP_PuntoControl.Tipo_Punto_Control	tipo_punto_control	op_puntocontrol	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Numero_Documento	numero_documento	gc_propietario	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno.Geometria	geometria	gc_terreno	\N
Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos.ini_predio_integracion_snr.snr_predio_juridico	snr_predio_juridico	ini_predio_insumos	snr_predio_registro
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	op_derecho	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia.ue	ue_op_construccion	op_puntolevantamiento	op_construccion
Datos_Gestor_Catastral_V2_10.GC_Direccion.Valor	valor	gc_direccion	\N
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Total_Banios	total_banios	op_unidadconstruccion	\N
Operacion_V2_10.Operacion.OP_Interesado.Sexo	sexo	op_interesado	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial_Anterior	numero_predial_anterior	gc_predio_catastro	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_puntolindero	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_terreno	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Barrio.Nombre	nombre	gc_barrio	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_construccion_unidad.gc_construccion	gc_construccion	gc_unidad_construccion	gc_construccion
LADM_COL_V1_6.LADM_Nucleo.COL_Interesado.ext_PID	op_interesado_ext_pid	extinteresado	op_interesado
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Dimension	dimension	op_terreno	\N
LADM_COL_V1_6.LADM_Nucleo.col_miembros.agrupacion	agrupacion	col_miembros	op_agrupacion_interesados
Operacion_V2_10.Operacion.op_interesado_contacto.op_interesado	op_interesado	op_interesado_contacto	op_interesado
Operacion_V2_10.Operacion.OP_Interesado.Segundo_Nombre	segundo_nombre	op_interesado	\N
LADM_COL_V1_6.LADM_Nucleo.ExtInteresado.Huella_Dactilar	extinteresado_huella_dactilar	imagen	extinteresado
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_derecho	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Numero_Documento	numero_documento	snr_titular	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_puntocontrol	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	op_restriccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoFuente.punto	punto_op_puntocontrol	col_puntofuente	op_puntocontrol
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Terreno	area_total_terreno	gc_datos_ph_condiminio	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	op_puntolindero	\N
Operacion_V2_10.Operacion.OP_Construccion.Altura	altura	op_construccion	\N
Operacion_V2_10.Operacion.OP_Derecho.Tipo	tipo	op_derecho	\N
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Total_Pisos_Torre	total_pisos_torre	op_datos_ph_condominio	\N
LADM_COL_V1_6.LADM_Nucleo.col_baunitComoInteresado.interesado	interesado_op_interesado	col_baunitcomointeresado	op_interesado
LADM_COL_V1_6.LADM_Nucleo.COL_Agrupacion_Interesados.Tipo	tipo	op_agrupacion_interesados	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_restriccion	\N
Operacion_V2_10.Operacion.OP_Terreno.Area_Terreno	area_terreno	op_terreno	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Area	op_terreno_area	col_areavalor	op_terreno
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Letra_Via_Principal	letra_via_principal	extdireccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_masCl.ue_mas	ue_mas_op_unidadconstruccion	col_mascl	op_unidadconstruccion
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	op_puntolevantamiento_calidad	anystructure	op_puntolevantamiento
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Total_Unidades_Privadas	total_unidades_privadas	op_datos_ph_condominio	\N
LADM_COL_V1_6.LADM_Nucleo.ExtInteresado.Firma	extinteresado_firma	imagen	extinteresado
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	op_interesado_procedencia	anystructure	op_interesado
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Espacio_De_Nombres	espacio_de_nombres	extarchivo	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Manzana.Codigo_Anterior	codigo_anterior	gc_manzana	\N
LADM_COL_V1_6.LADM_Nucleo.col_unidadFuente.unidad	unidad	col_unidadfuente	op_predio
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Datos	datos	extarchivo	\N
LADM_COL_V1_6.LADM_Nucleo.col_rrrFuente.rrr	rrr_op_derecho	col_rrrfuente	op_derecho
Operacion_V2_10.Operacion.op_construccion_unidadconstruccion.op_construccion	op_construccion	op_unidadconstruccion	op_construccion
LADM_COL_V1_6.LADM_Nucleo.col_puntoCcl.punto	punto_op_puntolindero	col_puntoccl	op_puntolindero
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Area_Construida	area_construida	gc_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueBaunit.ue	ue_op_terreno	col_uebaunit	op_terreno
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Local_Id	local_id	extarchivo	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Direcciones	gc_predio_catastro_direcciones	gc_direccion	gc_predio_catastro
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Fecha_Entrega	fecha_entrega	extarchivo	\N
LADM_COL_V1_6.LADM_Nucleo.col_clFuente.fuente_espacial	fuente_espacial	col_clfuente	op_fuenteespacial
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Valor_Via_Principal	valor_via_principal	extdireccion	\N
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Area_Total_Construida	area_total_construida	op_datos_ph_condominio	\N
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacial.Nombre	nombre	op_fuenteespacial	\N
LADM_COL_V1_6.LADM_Nucleo.col_menosCcl.ue_menos	ue_menos_op_unidadconstruccion	col_menosccl	op_unidadconstruccion
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Geometria	geometria	gc_comisiones_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_DRR.Comprobacion_Comparte	comprobacion_comparte	op_restriccion	\N
LADM_COL_V1_6.LADM_Nucleo.ExtInteresado.Fotografia	extinteresado_fotografia	imagen	extinteresado
LADM_COL_V1_6.LADM_Nucleo.col_cclFuente.fuente_espacial	fuente_espacial	col_cclfuente	op_fuenteespacial
LADM_COL_V1_6.LADM_Nucleo.col_menosCcl.ue_menos	ue_menos_op_terreno	col_menosccl	op_terreno
ISO19107_PLANAS_V1.GM_Surface3DListValue.value	avalue	gm_surface3dlistvalue	\N
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Correo_Electronico	correo_electronico	op_interesado_contacto	\N
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Observaciones	observaciones	op_unidadconstruccion	\N
Operacion_V2_10.Operacion.OP_Construccion.Numero_Semisotanos	numero_semisotanos	op_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	op_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda.Codigo_Anterior	codigo_anterior	gc_vereda	\N
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Area_Total_Terreno	area_total_terreno	op_datos_ph_condominio	\N
Operacion_V2_10.Operacion.OP_Terreno.Geometria	geometria	op_terreno	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia.ue	ue_op_construccion	op_puntocontrol	op_construccion
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Barrio.Geometria	geometria	gc_barrio	\N
LADM_COL_V1_6.LADM_Nucleo.col_topografoFuente.topografo	topografo_op_interesado	col_topografofuente	op_interesado
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Valor_Via_Generadora	valor_via_generadora	extdireccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado	op_puntolindero_transformacion_y_resultado	col_transformacion	op_puntolindero
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Departamento	departamento	op_interesado_contacto	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Volumen	op_servidumbretransito_volumen	col_volumenvalor	op_servidumbretransito
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	op_terreno_procedencia	anystructure	op_terreno
Operacion_V2_10.Operacion.OP_Predio.Numero_Predial_Anterior	numero_predial_anterior	op_predio	\N
Operacion_V2_10.Operacion.OP_PuntoLevantamiento.ID_Punto_Levantamiento	id_punto_levantamiento	op_puntolevantamiento	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_agrupacion_interesados	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	op_predio	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Geometria	geometria	op_unidadconstruccion	\N
LADM_COL_V1_6.LADM_Nucleo.ExtUnidadEdificacionFisica.Ext_Direccion_ID	extunidadedificcnfsica_ext_direccion_id	extdireccion	extunidadedificacionfisica
LADM_COL_V1_6.LADM_Nucleo.col_baunitRrr.unidad	unidad	op_restriccion	op_predio
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho.Numero_Documento	numero_documento	snr_fuente_derecho	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Manzana.Codigo_Barrio	codigo_barrio	gc_manzana	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Codigo_Terreno	codigo_terreno	gc_unidad_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacial.Tipo	tipo	op_fuenteespacial	\N
LADM_COL_V1_6.LADM_Nucleo.col_rrrFuente.fuente_administrativa	fuente_administrativa	col_rrrfuente	op_fuenteadministrativa
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad	estado_disponibilidad	op_fuenteadministrativa	\N
LADM_COL_V1_6.LADM_Nucleo.col_topografoFuente.fuente_espacial	fuente_espacial	col_topografofuente	op_fuenteespacial
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacial.Descripcion	descripcion	op_fuenteespacial	\N
Operacion_V2_10.Operacion.OP_Predio.Matricula_Inmobiliaria	matricula_inmobiliaria	op_predio	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica	area_terreno_alfanumerica	gc_terreno	\N
LADM_COL_V1_6.LADM_Nucleo.col_miembros.interesado	interesado_op_interesado	col_miembros	op_interesado
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_lindero	\N
LADM_COL_V1_6.LADM_Nucleo.ExtInteresado.Ext_Direccion_ID	extinteresado_ext_direccion_id	extdireccion	extinteresado
LADM_COL_V1_6.LADM_Nucleo.col_masCl.ue_mas	ue_mas_op_servidumbretransito	col_mascl	op_servidumbretransito
Operacion_V2_10.Operacion.OP_PuntoControl.Exactitud_Horizontal	exactitud_horizontal	op_puntocontrol	\N
Operacion_V2_10.Operacion.OP_Construccion.Numero_Sotanos	numero_sotanos	op_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	op_servidumbretransito	\N
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Torre_No	torre_no	op_datos_ph_condominio	\N
Operacion_V2_10.Operacion.OP_FuenteAdministrativa.Tipo	tipo	op_fuenteadministrativa	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad	estado_disponibilidad	op_fuenteespacial	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Construida	area_total_construida	gc_datos_ph_condiminio	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.MetodoProduccion	metodoproduccion	op_puntolevantamiento	\N
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Telefono1	telefono1	op_interesado_contacto	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Unidades_Privadas	total_unidades_privadas	gc_datos_ph_condiminio	\N
LADM_COL_V1_6.LADM_Nucleo.col_baunitFuente.fuente_espacial	fuente_espacial	col_baunitfuente	op_fuenteespacial
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Terreno.Geometria	geometria	gc_comisiones_terreno	\N
Operacion_V2_10.Operacion.OP_Terreno.Manzana_Vereda_Codigo	manzana_vereda_codigo	op_terreno	\N
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Total_Habitaciones	total_habitaciones	op_unidadconstruccion	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Primer_Apellido	primer_apellido	snr_titular	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Volumen	op_construccion_volumen	col_volumenvalor	op_construccion
Operacion_V2_10.Operacion.op_predio_copropiedad.copropiedad	copropiedad	op_predio_copropiedad	op_predio
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia.ue	ue_op_servidumbretransito	op_puntocontrol	op_servidumbretransito
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Construida_Privada	area_total_construida_privada	gc_datos_ph_condiminio	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Banios	total_banios	gc_unidad_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Rural.Codigo	codigo	gc_sector_rural	\N
Operacion_V2_10.Operacion.OP_PuntoLindero.ID_Punto_Lindero	id_punto_lindero	op_puntolindero	\N
LADM_COL_V1_6.LADM_Nucleo.Fraccion.Numerador	numerador	fraccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_rrrInteresado.interesado	interesado_op_agrupacion_interesados	op_restriccion	op_agrupacion_interesados
LADM_COL_V1_6.LADM_Nucleo.ExtInteresado.Nombre	nombre	extinteresado	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Numero_Semisotanos	numero_semisotanos	gc_construccion	\N
Operacion_V2_10.Operacion.OP_PuntoLevantamiento.Exactitud_Horizontal	exactitud_horizontal	op_puntolevantamiento	\N
LADM_COL_V1_6.LADM_Nucleo.col_masCl.ue_mas	ue_mas_op_construccion	col_mascl	op_construccion
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Dimension	dimension	op_unidadconstruccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente.Tipo_Principal	tipo_principal	op_fuenteadministrativa	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	op_predio	\N
Operacion_V2_10.Operacion.OP_Predio.Tiene_FMI	tiene_fmi	op_predio	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Sotanos	total_sotanos	gc_datos_ph_condiminio	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno.Manzana_Vereda_Codigo	manzana_vereda_codigo	gc_terreno	\N
Datos_SNR_V2_10.Datos_SNR.snr_fuente_derecho.snr_fuente_derecho	snr_fuente_derecho	snr_derecho	snr_fuente_derecho
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	op_terreno_calidad	anystructure	op_terreno
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	op_interesado_calidad	anystructure	op_interesado
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_fuenteespacial	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado	op_puntocontrol_transformacion_y_resultado	col_transformacion	op_puntocontrol
LADM_COL_V1_6.LADM_Nucleo.COL_DRR.Uso_Efectivo	uso_efectivo	op_derecho	\N
LADM_COL_V1_6.LADM_Nucleo.col_menosCcl.ccl_menos	ccl_menos	col_menosccl	op_lindero
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Corregimiento	corregimiento	op_interesado_contacto	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Tipo_Documento	tipo_documento	snr_titular	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_interesado	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial	numero_predial	gc_predio_catastro	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos.Tipo_Documento	tipo_documento	snr_fuente_cabidalinderos	\N
Datos_Gestor_Catastral_V2_10.GC_Direccion.Geometria_Referencia	geometria_referencia	gc_direccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueBaunit.baunit	baunit	col_uebaunit	op_predio
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Planta_Ubicacion	planta_ubicacion	op_unidadconstruccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_CadenaCarasLimite.Geometria	geometria	op_lindero	\N
Operacion_V2_10.Operacion.OP_Restriccion.Tipo	tipo	op_restriccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Numero_Sotanos	numero_sotanos	gc_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Digito_Verificacion	digito_verificacion	gc_propietario	\N
ISO19107_PLANAS_V1.GM_MultiSurface3D.geometry	gm_multisurface3d_geometry	gm_surface3dlistvalue	gm_multisurface3d
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.MetodoProduccion	metodoproduccion	op_puntocontrol	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia.ue	ue_op_unidadconstruccion	op_puntocontrol	op_unidadconstruccion
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Manzana.Geometria	geometria	gc_manzana	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID	op_terreno_ext_direccion_id	extdireccion	op_terreno
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Razon_Social	razon_social	snr_titular	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueFuente.ue	ue_op_construccion	col_uefuente	op_construccion
LADM_COL_V1_6.LADM_Nucleo.CC_MetodoOperacion.Dimensiones_Origen	dimensiones_origen	cc_metodooperacion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Identificador	identificador	gc_unidad_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Segundo_Nombre	segundo_nombre	gc_propietario	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoFuente.fuente_espacial	fuente_espacial	col_puntofuente	op_fuenteespacial
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	op_agrupacion_interesados	\N
LADM_COL_V1_6.LADM_Nucleo.col_rrrInteresado.interesado	interesado_op_interesado	op_restriccion	op_interesado
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_lindero	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.MetodoProduccion	metodoproduccion	op_puntolindero	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	op_lindero_procedencia	anystructure	op_lindero
Operacion_V2_10.Operacion.OP_Lindero.Longitud	longitud	op_lindero	\N
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Total_Unidades_Sotanos	total_unidades_sotanos	op_datos_ph_condominio	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Interesado.Nombre	nombre	op_agrupacion_interesados	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueUeGrupo.parte	parte_op_servidumbretransito	col_ueuegrupo	op_servidumbretransito
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Sistema_Procedencia_Datos	sistema_procedencia_datos	gc_predio_catastro	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Derecho.Calidad_Derecho_Registro	calidad_derecho_registro	snr_derecho	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_fuenteadministrativa	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	op_puntocontrol_calidad	anystructure	op_puntocontrol
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	op_lindero_calidad	anystructure	op_lindero
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	op_puntocontrol	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_servidumbretransito	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	op_interesado	\N
LADM_COL_V1_6.LADM_Nucleo.col_baunitRrr.unidad	unidad	op_derecho	op_predio
Datos_Gestor_Catastral_V2_10.GC_Direccion.Principal	principal	gc_direccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_rrrInteresado.interesado	interesado_op_interesado	op_derecho	op_interesado
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Anio_Construccion	anio_construccion	op_unidadconstruccion	\N
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Predio	sector_predio	extdireccion	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	op_puntocontrol_procedencia	anystructure	op_puntocontrol
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Puntaje	puntaje	gc_unidad_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Codigo_Edificacion	codigo_edificacion	gc_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Terreno_Privada	area_total_terreno_privada	gc_datos_ph_condiminio	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Tipo_Construccion	tipo_construccion	gc_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Pisos_Torre	total_pisos_torre	gc_datos_ph_condiminio	\N
Operacion_V2_10.Operacion.OP_Predio.Id_Operacion	id_operacion	op_predio	\N
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Area_Total_Construida_Privada	area_total_construida_privada	op_datos_ph_condominio	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	local_id	op_derecho	\N
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_puntocontrol	\N
LADM_COL_V1_6.LADM_Nucleo.col_rrrFuente.rrr	rrr_op_restriccion	col_rrrfuente	op_restriccion
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_unidadconstruccion	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Derecho.Codigo_Naturaleza_Juridica	codigo_naturaleza_juridica	snr_derecho	\N
LADM_COL_V1_6.LADM_Nucleo.COL_CadenaCarasLimite.Localizacion_Textual	localizacion_textual	op_lindero	\N
Operacion_V2_10.Operacion.OP_PuntoLindero.Exactitud_Vertical	exactitud_vertical	op_puntolindero	\N
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Clase_Via_Principal	clase_via_principal	extdireccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativa.Observacion	observacion	op_fuenteadministrativa	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia.ue	ue_op_unidadconstruccion	op_puntolevantamiento	op_unidadconstruccion
LADM_COL_V1_6.LADM_Nucleo.COL_VolumenValor.Tipo	tipo	col_volumenvalor	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Nombres	nombres	snr_titular	\N
Operacion_V2_10.Operacion.OP_Predio.Condicion_Predio	condicion_predio	op_predio	\N
Operacion_V2_10.Operacion.OP_Predio.Departamento	departamento	op_predio	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	op_servidumbretransito_calidad	anystructure	op_servidumbretransito
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Primer_Nombre	primer_nombre	gc_propietario	\N
Operacion_V2_10.Operacion.OP_Construccion.Tipo_Construccion	tipo_construccion	op_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Circulo_Registral	circulo_registral	gc_predio_catastro	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueBaunit.ue	ue_op_construccion	col_uebaunit	op_construccion
LADM_COL_V1_6.LADM_Nucleo.col_baunitComoInteresado.unidad	unidad	col_baunitcomointeresado	op_predio
LADM_COL_V1_6.LADM_Nucleo.col_ueFuente.ue	ue_op_terreno	col_uefuente	op_terreno
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho.Fecha_Documento	fecha_documento	snr_fuente_derecho	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente.Tipo_Principal	tipo_principal	op_fuenteespacial	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	op_puntolevantamiento_procedencia	anystructure	op_puntolevantamiento
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Avaluo_Construccion	avaluo_construccion	op_unidadconstruccion	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	op_derecho_procedencia	anystructure	op_derecho
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	espacio_de_nombres	op_predio	\N
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Direccion_Residencia	direccion_residencia	op_interesado_contacto	\N
Operacion_V2_10.Operacion.OP_PuntoLindero.Acuerdo	acuerdo	op_puntolindero	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Tipo_Dominio	tipo_dominio	gc_construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Habitaciones	total_habitaciones	gc_unidad_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Codigo_Postal	codigo_postal	extdireccion	\N
LADM_COL_V1_6.LADM_Nucleo.CC_MetodoOperacion.Formula	formula	cc_metodooperacion	\N
Operacion_V2_10.Operacion.OP_Construccion.Codigo_Edificacion	codigo_edificacion	op_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Volumen	op_terreno_volumen	col_volumenvalor	op_terreno
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	op_servidumbretransito_procedencia	anystructure	op_servidumbretransito
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	op_derecho	\N
LADM_COL_V1_6.LADM_Nucleo.col_masCcl.ue_mas	ue_mas_op_construccion	col_masccl	op_construccion
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Es_Direccion_Principal	es_direccion_principal	extdireccion	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	op_puntolevantamiento	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.Geometria	geometria	op_puntolevantamiento	\N
LADM_COL_V1_6.LADM_Nucleo.col_responsableFuente.interesado	interesado_op_agrupacion_interesados	col_responsablefuente	op_agrupacion_interesados
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.Geometria	geometria	op_puntolindero	\N
LADM_COL_V1_6.LADM_Nucleo.col_responsableFuente.fuente_administrativa	fuente_administrativa	col_responsablefuente	op_fuenteadministrativa
Operacion_V2_10.Operacion.OP_Interesado.Tipo_Documento	tipo_documento	op_interesado	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda.Nombre	nombre	gc_vereda	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	op_derecho_calidad	anystructure	op_derecho
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Razon_Social	razon_social	gc_propietario	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho.Tipo_Documento	tipo_documento	snr_fuente_derecho	\N
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacial.Metadato	metadato	op_fuenteespacial	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Area	op_servidumbretransito_area	col_areavalor	op_servidumbretransito
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos.Ente_Emisor	ente_emisor	snr_fuente_cabidalinderos	\N
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Vereda	vereda	op_interesado_contacto	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Tipo_Construccion	tipo_construccion	gc_unidad_construccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_masCl.ue_mas	ue_mas_op_terreno	col_mascl	op_terreno
LADM_COL_V1_6.LADM_Nucleo.col_menosCcl.ue_menos	ue_menos_op_construccion	col_menosccl	op_construccion
LADM_COL_V1_6.LADM_Nucleo.col_ueBaunit.ue	ue_op_unidadconstruccion	col_uebaunit	op_unidadconstruccion
Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos.ini_predio_integracion_gc.gc_predio_catastro	gc_predio_catastro	ini_predio_insumos	gc_predio_catastro
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	op_lindero	\N
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID	op_servidumbretransito_ext_direccion_id	extdireccion	op_servidumbretransito
\.


--
-- TOC entry 12696 (class 0 OID 339599)
-- Dependencies: 2262
-- Data for Name: t_ili2db_basket; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.t_ili2db_basket (t_id, dataset, topic, t_ili_tid, attachmentkey, domains) FROM stdin;
\.


--
-- TOC entry 12697 (class 0 OID 339605)
-- Dependencies: 2263
-- Data for Name: t_ili2db_classname; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.t_ili2db_classname (iliname, sqlname) FROM stdin;
LADM_COL_V1_6.LADM_Nucleo.COL_BAUnit	col_baunit
Datos_Gestor_Catastral_V2_10.GC_Direccion	gc_direccion
Datos_Gestor_Catastral_V2_10.GC_CondicionPredioTipo	gc_condicionprediotipo
LADM_COL_V1_6.LADM_Nucleo.COL_CadenaCarasLimite	col_cadenacaraslimite
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Urbano	gc_sector_urbano
Operacion_V2_10.OP_CondicionPredioTipo	op_condicionprediotipo
LADM_COL_V1_6.LADM_Nucleo.COL_DimensionTipo	col_dimensiontipo
Operacion_V2_10.Operacion.OP_Predio	op_predio
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Clase_Via_Principal	extdireccion_clase_via_principal
Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos.ini_predio_integracion_gc	ini_predio_integracion_gc
Operacion_V2_10.Operacion.OP_Agrupacion_Interesados	op_agrupacion_interesados
LADM_COL_V1_6.LADM_Nucleo.col_ueNivel	col_uenivel
LADM_COL_V1_6.LADM_Nucleo.col_baunitFuente	col_baunitfuente
Operacion_V2_10.Operacion.op_predio_copropiedad	op_predio_copropiedad
LADM_COL_V1_6.LADM_Nucleo.COL_EstructuraTipo	col_estructuratipo
Datos_SNR_V2_10.Datos_SNR.SNR_Titular	snr_titular
LADM_COL_V1_6.LADM_Nucleo.Fraccion	fraccion
LADM_COL_V1_6.LADM_Nucleo.col_menosCcl	col_menosccl
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho	snr_fuente_derecho
LADM_COL_V1_6.LADM_Nucleo.ExtInteresado	extinteresado
LADM_COL_V1_6.LADM_Nucleo.col_unidadFuente	col_unidadfuente
Operacion_V2_10.Operacion.OP_Derecho	op_derecho
Datos_SNR_V2_10.Datos_SNR.SNR_Derecho	snr_derecho
LADM_COL_V1_6.LADM_Nucleo.col_clFuente	col_clfuente
LADM_COL_V1_6.LADM_Nucleo.COL_VolumenValor	col_volumenvalor
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_construccion_unidad	gc_construccion_unidad
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda	gc_vereda
Operacion_V2_10.Operacion.OP_Terreno	op_terreno
LADM_COL_V1_6.LADM_Nucleo.COL_InterpolacionTipo	col_interpolaciontipo
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativa	col_fuenteadministrativa
LADM_COL_V1_6.LADM_Nucleo.col_miembros	col_miembros
Operacion_V2_10.OP_FuenteAdministrativaTipo	op_fuenteadministrativatipo
LADM_COL_V1_6.LADM_Nucleo.COL_VolumenTipo	col_volumentipo
Operacion_V2_10.OP_UsoUConsTipo	op_usouconstipo
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativaTipo	col_fuenteadministrativatipo
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial	col_unidadespacial
Operacion_V2_10.Operacion.OP_Lindero	op_lindero
Operacion_V2_10.OP_UbicacionPuntoTipo	op_ubicacionpuntotipo
LADM_COL_V1_6.LADM_Nucleo.COL_MetodoProduccionTipo	col_metodoproducciontipo
Datos_Gestor_Catastral_V2_10.GC_UnidadConstruccionTipo	gc_unidadconstrucciontipo
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente	col_fuente
Operacion_V2_10.Operacion.op_ph_predio	op_ph_predio
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEdificacionTipo	col_unidadedificaciontipo
LADM_COL_V1_6.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales	col_agrupacionunidadesespaciales
Datos_SNR_V2_10.SNR_CalidadDerechoTipo	snr_calidadderechotipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_propietario_predio	gc_propietario_predio
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos	snr_fuente_cabidalinderos
Operacion_V2_10.OP_PuntoControlTipo	op_puntocontroltipo
LADM_COL_V1_6.LADM_Nucleo.COL_PuntoTipo	col_puntotipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno	gc_terreno
ISO19107_PLANAS_V1.GM_MultiSurface2D	gm_multisurface2d
LADM_COL_V1_6.LADM_Nucleo.COL_Nivel	col_nivel
LADM_COL_V1_6.LADM_Nucleo.col_menosCl	col_menoscl
LADM_COL_V1_6.LADM_Nucleo.col_rrrInteresado	col_rrrinteresado
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion	extdireccion
LADM_COL_V1_6.LADM_Nucleo.col_ueFuente	col_uefuente
Operacion_V2_10.OP_InteresadoTipo	op_interesadotipo
Operacion_V2_10.OP_PuntoTipo	op_puntotipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Rural	gc_sector_rural
LADM_COL_V1_6.LADM_Nucleo.COL_RelacionSuperficieTipo	col_relacionsuperficietipo
Operacion_V2_10.OP_DerechoTipo	op_derechotipo
LADM_COL_V1_6.LADM_Nucleo.CC_MetodoOperacion	cc_metodooperacion
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Construccion	gc_comisiones_construccion
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Predio	extdireccion_sector_predio
Operacion_V2_10.OP_RestriccionTipo	op_restricciontipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_construccion_predio	gc_construccion_predio
Operacion_V2_10.Operacion.OP_PuntoLevantamiento	op_puntolevantamiento
Operacion_V2_10.Operacion.OP_UnidadConstruccion	op_unidadconstruccion
LADM_COL_V1_6.LADM_Nucleo.COL_ISO19125_Tipo	col_iso19125_tipo
Operacion_V2_10.Operacion.OP_Construccion	op_construccion
LADM_COL_V1_6.LADM_Nucleo.col_relacionFuenteUespacial	col_relacionfuenteuespacial
Datos_SNR_V2_10.Datos_SNR.snr_titular_derecho	snr_titular_derecho
LADM_COL_V1_6.LADM_Nucleo.COL_AreaValor	col_areavalor
LADM_COL_V1_6.LADM_Nucleo.Oid	oid
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro	snr_predio_registro
Operacion_V2_10.OP_ConstruccionTipo	op_construcciontipo
Operacion_V2_10.OP_UnidadConstruccionTipo	op_unidadconstrucciontipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro	gc_perimetro
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Terreno	gc_comisiones_terreno
Operacion_V2_10.OP_InteresadoDocumentoTipo	op_interesadodocumentotipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Barrio	gc_barrio
LADM_COL_V1_6.LADM_Nucleo.COL_RedServiciosTipo	col_redserviciostipo
Datos_SNR_V2_10.Datos_SNR.snr_derecho_predio	snr_derecho_predio
Operacion_V2_10.Operacion.op_construccion_unidadconstruccion	op_construccion_unidadconstruccion
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro	gc_predio_catastro
Datos_SNR_V2_10.SNR_DocumentoTitularTipo	snr_documentotitulartipo
LADM_COL_V1_6.LADM_Nucleo.col_topografoFuente	col_topografofuente
LADM_COL_V1_6.LADM_Nucleo.COL_DRR	col_drr
Operacion_V2_10.Operacion.op_interesado_contacto	operacin_v2_10operacion_op_interesado_contacto
LADM_COL_V1_6.LADM_Nucleo.col_masCl	col_mascl
LADM_COL_V1_6.LADM_Nucleo.CI_Forma_Presentacion_Codigo	ci_forma_presentacion_codigo
LADM_COL_V1_6.LADM_Nucleo.ExtUnidadEdificacionFisica	extunidadedificacionfisica
Operacion_V2_10.OP_AcuerdoTipo	op_acuerdotipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_terreno_predio	gc_terreno_predio
Operacion_V2_10.Operacion.OP_FuenteEspacial	op_fuenteespacial
Operacion_V2_10.Operacion.OP_PuntoControl	op_puntocontrol
LADM_COL_V1_6.LADM_Nucleo.col_ueJerarquiaGrupo	col_uejerarquiagrupo
ISO19107_PLANAS_V1.GM_Surface3DListValue	gm_surface3dlistvalue
LADM_COL_V1_6.LADM_Nucleo.col_masCcl	col_masccl
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio	op_datos_ph_condominio
LADM_COL_V1_6.LADM_Nucleo.Imagen	imagen
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacialTipo	col_fuenteespacialtipo
LADM_COL_V1_6.LADM_Nucleo.ExtRedServiciosFisica	extredserviciosfisica
ISO19107_PLANAS_V1.GM_Surface2DListValue	gm_surface2dlistvalue
LADM_COL_V1_6.LADM_Nucleo.COL_Agrupacion_Interesados	col_agrupacion_interesados
LADM_COL_V1_6.LADM_Nucleo.COL_Transformacion	col_transformacion
LADM_COL_V1_6.LADM_Nucleo.COL_Interesado	col_interesado
ISO19107_PLANAS_V1.GM_MultiSurface3D	gm_multisurface3d
Operacion_V2_10.OP_FotoidentificacionTipo	op_fotoidentificaciontipo
Operacion_V2_10.Operacion.OP_Interesado	op_interesado
LADM_COL_V1_6.LADM_Nucleo.COL_EspacioJuridicoRedServicios	col_espaciojuridicoredservicios
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Ciudad	extdireccion_sector_ciudad
LADM_COL_V1_6.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion	col_espaciojuridicounidadedificacion
LADM_COL_V1_6.LADM_Nucleo.col_relacionFuente	col_relacionfuente
Operacion_V2_10.OP_GrupoEtnicoTipo	op_grupoetnicotipo
LADM_COL_V1_6.LADM_Nucleo.COL_BAUnitTipo	col_baunittipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion	gc_comisiones_unidad_construccion
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacial	col_fuenteespacial
LADM_COL_V1_6.LADM_Nucleo.col_baunitComoInteresado	col_baunitcomointeresado
LADM_COL_V1_6.LADM_Nucleo.COL_EstadoRedServiciosTipo	col_estadoredserviciostipo
LADM_COL_V1_6.LADM_Nucleo.col_ueUeGrupo	col_ueuegrupo
Operacion_V2_10.Operacion.OP_ServidumbreTransito	op_servidumbretransito
Operacion_V2_10.Operacion.OP_Restriccion	op_restriccion
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_ph_predio	gc_ph_predio
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Tipo_Direccion	extdireccion_tipo_direccion
LADM_COL_V1_6.LADM_Nucleo.col_cclFuente	col_cclfuente
LADM_COL_V1_6.LADM_Nucleo.COL_RelacionNecesariaBAUnits	col_relacionnecesariabaunits
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_copropiedad	gc_copropiedad
LADM_COL_V1_6.LADM_Nucleo.COL_ContenidoNivelTipo	col_contenidoniveltipo
Operacion_V2_10.OP_DominioConstruccionTipo	op_dominioconstrucciontipo
LADM_COL_V1_6.LADM_Nucleo.col_ueBaunit	col_uebaunit
Datos_SNR_V2_10.SNR_PersonaTitularTipo	snr_personatitulartipo
LADM_COL_V1_6.LADM_Nucleo.COL_CarasLindero	col_caraslindero
Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos.INI_Predio_Insumos	ini_predio_insumos
LADM_COL_V1_6.LADM_Nucleo.col_rrrFuente	col_rrrfuente
Datos_SNR_V2_10.Datos_SNR.snr_fuente_derecho	dats_snr_v2_10datos_snr_snr_fuente_derecho
INTERLIS.ANYSTRUCTURE	anystructure
LADM_COL_V1_6.LADM_Nucleo.col_puntoCcl	col_puntoccl
LADM_COL_V1_6.LADM_Nucleo.COL_EstadoDisponibilidadTipo	col_estadodisponibilidadtipo
LADM_COL_V1_6.LADM_Nucleo.COL_RelacionNecesariaUnidadesEspaciales	col_relacionnecesariaunidadesespaciales
LADM_COL_V1_6.LADM_Nucleo.col_baunitRrr	col_baunitrrr
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia	col_puntoreferencia
LADM_COL_V1_6.LADM_Nucleo.col_puntoCl	col_puntocl
Operacion_V2_10.Operacion.op_predio_insumos_operacion	op_predio_insumos_operacion
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo	extarchivo
Operacion_V2_10.OP_SexoTipo	op_sexotipo
LADM_COL_V1_6.LADM_Nucleo.COL_RegistroTipo	col_registrotipo
Operacion_V2_10.Operacion.OP_Interesado_Contacto	op_interesado_contacto
LADM_COL_V1_6.LADM_Nucleo.col_puntoFuente	col_puntofuente
LADM_COL_V1_6.LADM_Nucleo.COL_AreaTipo	col_areatipo
LADM_COL_V1_6.LADM_Nucleo.col_responsableFuente	col_responsablefuente
Operacion_V2_10.OP_PuntoLevTipo	op_puntolevtipo
Operacion_V2_10.OP_ViaTipo	op_viatipo
Datos_SNR_V2_10.SNR_FuenteTipo	snr_fuentetipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario	gc_propietario
LADM_COL_V1_6.LADM_Nucleo.COL_GrupoInteresadoTipo	col_grupointeresadotipo
Operacion_V2_10.OP_ConstruccionPlantaTipo	op_construccionplantatipo
Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos.ini_predio_integracion_snr	ini_predio_integracion_snr
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio	gc_datos_ph_condiminio
Datos_SNR_V2_10.Datos_SNR.snr_fuente_cabidalinderos	dats_snr_v2_10datos_snr_snr_fuente_cabidalinderos
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion	gc_construccion
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Manzana	gc_manzana
Operacion_V2_10.Operacion.OP_PuntoLindero	op_puntolindero
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion	gc_unidad_construccion
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado	objetoversionado
Operacion_V2_10.Operacion.OP_FuenteAdministrativa	op_fuenteadministrativa
Datos_Gestor_Catastral_V2_10.GC_SistemaProcedenciaDatosTipo	gc_sistemaprocedenciadatostipo
LADM_COL_V1_6.LADM_Nucleo.COL_Punto	col_punto
\.


--
-- TOC entry 12698 (class 0 OID 339611)
-- Dependencies: 2264
-- Data for Name: t_ili2db_column_prop; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.t_ili2db_column_prop (tablename, subtype, columnname, tag, setting) FROM stdin;
op_puntolindero	\N	local_id	ch.ehi.ili2db.dispName	Local ID
op_fuenteespacial	\N	nombre	ch.ehi.ili2db.dispName	Nombre
gc_propietario	\N	razon_social	ch.ehi.ili2db.dispName	Razón social
op_construccion	\N	dimension	ch.ehi.ili2db.foreignKey	col_dimensiontipo
op_construccion	\N	dimension	ch.ehi.ili2db.dispName	Dimensión
anystructure	\N	op_predio_procedencia	ch.ehi.ili2db.foreignKey	op_predio
col_topografofuente	\N	topografo_op_agrupacion_interesados	ch.ehi.ili2db.foreignKey	op_agrupacion_interesados
op_derecho	\N	interesado_op_agrupacion_interesados	ch.ehi.ili2db.foreignKey	op_agrupacion_interesados
op_servidumbretransito	\N	dimension	ch.ehi.ili2db.foreignKey	col_dimensiontipo
op_servidumbretransito	\N	dimension	ch.ehi.ili2db.dispName	Dimensión
op_unidadconstruccion	\N	uso	ch.ehi.ili2db.foreignKey	op_usouconstipo
op_unidadconstruccion	\N	uso	ch.ehi.ili2db.dispName	Uso
op_construccion	\N	altura	ch.ehi.ili2db.unit	m
op_construccion	\N	altura	ch.ehi.ili2db.dispName	Altura
op_fuenteadministrativa	\N	observacion	ch.ehi.ili2db.dispName	Observación
col_mascl	\N	ue_mas_op_construccion	ch.ehi.ili2db.foreignKey	op_construccion
snr_fuente_cabidalinderos	\N	ciudad_emisora	ch.ehi.ili2db.dispName	Ciudad emisora
col_ueuegrupo	\N	parte_op_servidumbretransito	ch.ehi.ili2db.foreignKey	op_servidumbretransito
gc_datos_ph_condiminio	\N	area_total_terreno_comun	ch.ehi.ili2db.unit	m2
gc_datos_ph_condiminio	\N	area_total_terreno_comun	ch.ehi.ili2db.dispName	Área total de terreno común
gc_copropiedad	\N	gc_unidad	ch.ehi.ili2db.foreignKey	gc_predio_catastro
cc_metodooperacion	\N	col_transformacion_transformacion	ch.ehi.ili2db.foreignKey	col_transformacion
gc_predio_catastro	\N	destinacion_economica	ch.ehi.ili2db.dispName	Destinación económica
extdireccion	\N	op_terreno_ext_direccion_id	ch.ehi.ili2db.foreignKey	op_terreno
op_puntocontrol	\N	id_punto_control	ch.ehi.ili2db.dispName	ID del punto de control
anystructure	\N	op_puntolevantamiento_procedencia	ch.ehi.ili2db.foreignKey	op_puntolevantamiento
anystructure	\N	op_agrupacion_intrsdos_procedencia	ch.ehi.ili2db.foreignKey	op_agrupacion_interesados
ini_predio_insumos	\N	snr_predio_juridico	ch.ehi.ili2db.foreignKey	snr_predio_registro
snr_titular	\N	nombres	ch.ehi.ili2db.dispName	Nombres
op_interesado	\N	documento_identidad	ch.ehi.ili2db.dispName	Documento de identidad
gc_construccion	\N	tipo_construccion	ch.ehi.ili2db.foreignKey	gc_unidadconstrucciontipo
gc_construccion	\N	tipo_construccion	ch.ehi.ili2db.dispName	Tipo de construcción
col_uebaunit	\N	ue_op_servidumbretransito	ch.ehi.ili2db.foreignKey	op_servidumbretransito
op_unidadconstruccion	\N	tipo_planta	ch.ehi.ili2db.foreignKey	op_construccionplantatipo
op_unidadconstruccion	\N	tipo_planta	ch.ehi.ili2db.dispName	Tipo de planta
op_unidadconstruccion	\N	area_construida	ch.ehi.ili2db.unit	m2
op_unidadconstruccion	\N	area_construida	ch.ehi.ili2db.dispName	Área construida
extdireccion	\N	op_servidumbretransito_ext_direccion_id	ch.ehi.ili2db.foreignKey	op_servidumbretransito
op_puntolindero	\N	fotoidentificacion	ch.ehi.ili2db.foreignKey	op_fotoidentificaciontipo
op_puntolindero	\N	fotoidentificacion	ch.ehi.ili2db.dispName	Fotoidentificación
op_puntolevantamiento	\N	tipo_punto_levantamiento	ch.ehi.ili2db.foreignKey	op_puntolevtipo
op_puntolevantamiento	\N	tipo_punto_levantamiento	ch.ehi.ili2db.dispName	Tipo de punto de levantamiento
col_miembros	\N	interesado_op_agrupacion_interesados	ch.ehi.ili2db.foreignKey	op_agrupacion_interesados
snr_predio_registro	\N	snr_fuente_cabidalinderos	ch.ehi.ili2db.foreignKey	snr_fuente_cabidalinderos
op_lindero	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
gc_comisiones_construccion	\N	geometria	ch.ehi.ili2db.coordDimension	3
gc_comisiones_construccion	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
gc_comisiones_construccion	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
gc_comisiones_construccion	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
gc_comisiones_construccion	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
gc_comisiones_construccion	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
gc_comisiones_construccion	\N	geometria	ch.ehi.ili2db.c3Min	-5000.000
gc_comisiones_construccion	\N	geometria	ch.ehi.ili2db.c3Max	6000.000
gc_comisiones_construccion	\N	geometria	ch.ehi.ili2db.srid	4326
gc_comisiones_construccion	\N	geometria	ch.ehi.ili2db.dispName	Geometría
op_unidadconstruccion	\N	avaluo_construccion	ch.ehi.ili2db.unit	COP
op_unidadconstruccion	\N	avaluo_construccion	ch.ehi.ili2db.dispName	Avalúo de la construcción
op_puntolindero	\N	comienzo_vida_util_version	ch.ehi.ili2db.dispName	Versión de comienzo de vida útil
gc_predio_catastro	\N	fecha_alerta	ch.ehi.ili2db.dispName	Fecha de alerta
op_derecho	\N	unidad	ch.ehi.ili2db.foreignKey	op_predio
op_restriccion	\N	fin_vida_util_version	ch.ehi.ili2db.dispName	Versión de fin de vida útil
op_servidumbretransito	\N	fin_vida_util_version	ch.ehi.ili2db.dispName	Versión de fin de vida útil
col_areavalor	\N	op_unidadconstruccion_area	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
col_menosccl	\N	ue_menos_op_terreno	ch.ehi.ili2db.foreignKey	op_terreno
gc_terreno	\N	numero_subterraneos	ch.ehi.ili2db.dispName	Número de subterráneos
op_predio	\N	direccion	ch.ehi.ili2db.dispName	Dirección
col_miembros	\N	agrupacion	ch.ehi.ili2db.foreignKey	op_agrupacion_interesados
gc_construccion	\N	area_construida	ch.ehi.ili2db.unit	m2
gc_construccion	\N	area_construida	ch.ehi.ili2db.dispName	Área construida
col_masccl	\N	ue_mas_op_construccion	ch.ehi.ili2db.foreignKey	op_construccion
extarchivo	\N	snr_fuente_cabidlndros_archivo	ch.ehi.ili2db.foreignKey	snr_fuente_cabidalinderos
op_unidadconstruccion	\N	anio_construccion	ch.ehi.ili2db.dispName	Año de construcción
op_agrupacion_interesados	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
op_predio	\N	nombre	ch.ehi.ili2db.dispName	Nombre
extinteresado	\N	op_interesado_ext_pid	ch.ehi.ili2db.foreignKey	op_interesado
extarchivo	\N	datos	ch.ehi.ili2db.dispName	Datos
gc_predio_catastro	\N	tipo_catastro	ch.ehi.ili2db.dispName	Tipo de catastro
op_puntolevantamiento	\N	geometria	ch.ehi.ili2db.coordDimension	3
op_puntolevantamiento	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
op_puntolevantamiento	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
op_puntolevantamiento	\N	geometria	ch.ehi.ili2db.geomType	POINT
op_puntolevantamiento	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
op_puntolevantamiento	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
op_puntolevantamiento	\N	geometria	ch.ehi.ili2db.c3Min	-5000.000
op_puntolevantamiento	\N	geometria	ch.ehi.ili2db.c3Max	6000.000
op_puntolevantamiento	\N	geometria	ch.ehi.ili2db.srid	4326
op_puntolevantamiento	\N	geometria	ch.ehi.ili2db.dispName	Geometría
gc_construccion	\N	numero_semisotanos	ch.ehi.ili2db.dispName	Número de semisótanos
col_uefuente	\N	ue_op_servidumbretransito	ch.ehi.ili2db.foreignKey	op_servidumbretransito
gc_perimetro	\N	geometria	ch.ehi.ili2db.coordDimension	2
gc_perimetro	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
gc_perimetro	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
gc_perimetro	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
gc_perimetro	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
gc_perimetro	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
gc_perimetro	\N	geometria	ch.ehi.ili2db.srid	4326
gc_perimetro	\N	geometria	ch.ehi.ili2db.dispName	Geometría
gc_unidad_construccion	\N	gc_construccion	ch.ehi.ili2db.foreignKey	gc_construccion
col_areavalor	\N	op_construccion_area	ch.ehi.ili2db.foreignKey	op_construccion
op_derecho	\N	comienzo_vida_util_version	ch.ehi.ili2db.dispName	Versión de comienzo de vida útil
op_interesado_contacto	\N	departamento	ch.ehi.ili2db.dispName	Departamento
gc_comisiones_terreno	\N	geometria	ch.ehi.ili2db.coordDimension	2
gc_comisiones_terreno	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
gc_comisiones_terreno	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
gc_comisiones_terreno	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
gc_comisiones_terreno	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
gc_comisiones_terreno	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
gc_comisiones_terreno	\N	geometria	ch.ehi.ili2db.srid	4326
gc_comisiones_terreno	\N	geometria	ch.ehi.ili2db.dispName	Geometría
col_areavalor	\N	op_servidumbretransito_area	ch.ehi.ili2db.foreignKey	op_servidumbretransito
snr_derecho	\N	snr_fuente_derecho	ch.ehi.ili2db.foreignKey	snr_fuente_derecho
col_rrrfuente	\N	fuente_administrativa	ch.ehi.ili2db.foreignKey	op_fuenteadministrativa
extdireccion	\N	tipo_direccion	ch.ehi.ili2db.foreignKey	extdireccion_tipo_direccion
extdireccion	\N	tipo_direccion	ch.ehi.ili2db.dispName	Tipo de dirección
anystructure	\N	op_agrupacion_intrsdos_calidad	ch.ehi.ili2db.foreignKey	op_agrupacion_interesados
gm_surface3dlistvalue	\N	gm_multisurface3d_geometry	ch.ehi.ili2db.foreignKey	gm_multisurface3d
col_topografofuente	\N	fuente_espacial	ch.ehi.ili2db.foreignKey	op_fuenteespacial
snr_fuente_cabidalinderos	\N	numero_documento	ch.ehi.ili2db.dispName	Número de documento
col_puntocl	\N	punto_op_puntolevantamiento	ch.ehi.ili2db.foreignKey	op_puntolevantamiento
op_puntocontrol	\N	metodoproduccion	ch.ehi.ili2db.foreignKey	col_metodoproducciontipo
op_puntocontrol	\N	metodoproduccion	ch.ehi.ili2db.dispName	Método de producción
op_construccion	\N	avaluo_construccion	ch.ehi.ili2db.unit	COP
op_construccion	\N	avaluo_construccion	ch.ehi.ili2db.dispName	Ávaluo de construcción
op_interesado	\N	tipo_documento	ch.ehi.ili2db.foreignKey	op_interesadodocumentotipo
op_interesado	\N	tipo_documento	ch.ehi.ili2db.dispName	Tipo de documento
op_interesado	\N	nombre	ch.ehi.ili2db.dispName	Nombre
op_unidadconstruccion	\N	altura	ch.ehi.ili2db.unit	m
op_unidadconstruccion	\N	altura	ch.ehi.ili2db.dispName	Altura
op_derecho	\N	local_id	ch.ehi.ili2db.dispName	Local ID
op_datos_ph_condominio	\N	total_unidades_sotanos	ch.ehi.ili2db.dispName	Total de únidades de sótanos
op_lindero	\N	geometria	ch.ehi.ili2db.coordDimension	3
op_lindero	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
op_lindero	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
op_lindero	\N	geometria	ch.ehi.ili2db.geomType	LINESTRING
op_lindero	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
op_lindero	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
op_lindero	\N	geometria	ch.ehi.ili2db.c3Min	-5000.000
op_lindero	\N	geometria	ch.ehi.ili2db.c3Max	6000.000
op_lindero	\N	geometria	ch.ehi.ili2db.srid	4326
op_lindero	\N	geometria	ch.ehi.ili2db.dispName	Geometría
col_areavalor	\N	atype	ch.ehi.ili2db.foreignKey	col_areatipo
col_areavalor	\N	atype	ch.ehi.ili2db.dispName	Tipo
gc_construccion	\N	numero_pisos	ch.ehi.ili2db.dispName	Número de pisos
op_construccion	\N	numero_sotanos	ch.ehi.ili2db.dispName	Número de sótanos
col_cclfuente	\N	fuente_espacial	ch.ehi.ili2db.foreignKey	op_fuenteespacial
op_puntolindero	\N	exactitud_horizontal	ch.ehi.ili2db.unit	cm
op_puntolindero	\N	exactitud_horizontal	ch.ehi.ili2db.dispName	Exactitud horizontal
col_volumenvalor	\N	tipo	ch.ehi.ili2db.foreignKey	col_volumentipo
col_volumenvalor	\N	tipo	ch.ehi.ili2db.dispName	Tipo
op_servidumbretransito	\N	area_servidumbre	ch.ehi.ili2db.unit	m2
op_servidumbretransito	\N	area_servidumbre	ch.ehi.ili2db.dispName	Área de la servidumbre
col_transformacion	\N	op_puntolevantamiento_transformacion_y_resultado	ch.ehi.ili2db.foreignKey	op_puntolevantamiento
gc_unidad_construccion	\N	puntaje	ch.ehi.ili2db.dispName	Puntaje
col_unidadfuente	\N	unidad	ch.ehi.ili2db.foreignKey	op_predio
gc_terreno	\N	gc_predio	ch.ehi.ili2db.foreignKey	gc_predio_catastro
op_construccion	\N	tipo_dominio	ch.ehi.ili2db.foreignKey	op_dominioconstrucciontipo
op_construccion	\N	tipo_dominio	ch.ehi.ili2db.dispName	Tipo de dominio
anystructure	\N	op_unidadconstruccion_calidad	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
col_puntoccl	\N	punto_op_puntolevantamiento	ch.ehi.ili2db.foreignKey	op_puntolevantamiento
op_puntocontrol	\N	ue_op_terreno	ch.ehi.ili2db.foreignKey	op_terreno
op_puntolindero	\N	acuerdo	ch.ehi.ili2db.foreignKey	op_acuerdotipo
op_puntolindero	\N	acuerdo	ch.ehi.ili2db.dispName	Acuerdo
snr_titular	\N	primer_apellido	ch.ehi.ili2db.dispName	Primer apellido
anystructure	\N	op_puntolevantamiento_calidad	ch.ehi.ili2db.foreignKey	op_puntolevantamiento
op_interesado	\N	segundo_nombre	ch.ehi.ili2db.dispName	Segundo nombre
op_interesado_contacto	\N	municipio	ch.ehi.ili2db.dispName	Municipio
col_ueuegrupo	\N	parte_op_construccion	ch.ehi.ili2db.foreignKey	op_construccion
gc_unidad_construccion	\N	total_banios	ch.ehi.ili2db.dispName	Total de baños
op_puntocontrol	\N	puntotipo	ch.ehi.ili2db.foreignKey	op_puntotipo
op_puntocontrol	\N	puntotipo	ch.ehi.ili2db.dispName	Tipo de punto
anystructure	\N	op_servidumbretransito_procedencia	ch.ehi.ili2db.foreignKey	op_servidumbretransito
op_predio	\N	avaluo_catastral	ch.ehi.ili2db.unit	COP
op_predio	\N	avaluo_catastral	ch.ehi.ili2db.dispName	Avalúo catastral
op_construccion	\N	codigo_edificacion	ch.ehi.ili2db.dispName	Código de edificación
gc_propietario	\N	primer_nombre	ch.ehi.ili2db.dispName	Primer nombre
gc_propietario	\N	digito_verificacion	ch.ehi.ili2db.dispName	Dígito de verificación
extinteresado	\N	extredserviciosfisica_ext_interesado_administrador_id	ch.ehi.ili2db.foreignKey	extredserviciosfisica
gc_manzana	\N	geometria	ch.ehi.ili2db.coordDimension	2
gc_manzana	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
gc_manzana	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
gc_manzana	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
gc_manzana	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
gc_manzana	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
gc_manzana	\N	geometria	ch.ehi.ili2db.srid	4326
gc_manzana	\N	geometria	ch.ehi.ili2db.dispName	Geometría
op_interesado	\N	primer_apellido	ch.ehi.ili2db.dispName	Primer apellido
gc_datos_ph_condiminio	\N	total_unidades_sotano	ch.ehi.ili2db.dispName	Total de unidades de sótano
op_datos_ph_condominio	\N	area_total_construida	ch.ehi.ili2db.unit	m2
op_datos_ph_condominio	\N	area_total_construida	ch.ehi.ili2db.dispName	Área total construida
anystructure	\N	op_puntolindero_calidad	ch.ehi.ili2db.foreignKey	op_puntolindero
col_menoscl	\N	ue_menos_op_terreno	ch.ehi.ili2db.foreignKey	op_terreno
extarchivo	\N	fecha_entrega	ch.ehi.ili2db.dispName	Fecha de entrega
op_unidadconstruccion	\N	total_pisos	ch.ehi.ili2db.dispName	Total de pisos
gc_construccion	\N	numero_sotanos	ch.ehi.ili2db.dispName	Número de sótanos
anystructure	\N	op_derecho_procedencia	ch.ehi.ili2db.foreignKey	op_derecho
op_terreno	\N	fin_vida_util_version	ch.ehi.ili2db.dispName	Versión de fin de vida útil
op_construccion	\N	numero_pisos	ch.ehi.ili2db.dispName	Número de pisos
col_uefuente	\N	ue_op_terreno	ch.ehi.ili2db.foreignKey	op_terreno
op_derecho	\N	tipo	ch.ehi.ili2db.foreignKey	op_derechotipo
op_derecho	\N	tipo	ch.ehi.ili2db.dispName	Tipo
extdireccion	\N	complemento	ch.ehi.ili2db.dispName	Complemento
gc_construccion	\N	codigo_edificacion	ch.ehi.ili2db.dispName	Código de edificación
op_restriccion	\N	tipo	ch.ehi.ili2db.foreignKey	op_restricciontipo
op_restriccion	\N	tipo	ch.ehi.ili2db.dispName	Tipo
gc_construccion	\N	tipo_dominio	ch.ehi.ili2db.dispName	Tipo de dominio
gc_construccion	\N	codigo_terreno	ch.ehi.ili2db.dispName	Código de terreno
anystructure	\N	op_predio_calidad	ch.ehi.ili2db.foreignKey	op_predio
imagen	\N	extinteresado_firma	ch.ehi.ili2db.foreignKey	extinteresado
gc_datos_ph_condiminio	\N	area_total_terreno_privada	ch.ehi.ili2db.unit	m2
gc_datos_ph_condiminio	\N	area_total_terreno_privada	ch.ehi.ili2db.dispName	Área total de terreno privada
op_puntolindero	\N	id_punto_lindero	ch.ehi.ili2db.dispName	ID del punto de lindero
op_agrupacion_interesados	\N	nombre	ch.ehi.ili2db.dispName	Nombre
op_puntolindero	\N	metodoproduccion	ch.ehi.ili2db.foreignKey	col_metodoproducciontipo
op_puntolindero	\N	metodoproduccion	ch.ehi.ili2db.dispName	Método de producción
op_unidadconstruccion	\N	total_locales	ch.ehi.ili2db.dispName	Total de locales
col_relacionfuente	\N	fuente_administrativa	ch.ehi.ili2db.foreignKey	op_fuenteadministrativa
op_puntolindero	\N	ue_op_unidadconstruccion	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
snr_fuente_derecho	\N	numero_documento	ch.ehi.ili2db.dispName	Número de documento
op_derecho	\N	uso_efectivo	ch.ehi.ili2db.dispName	Uso efectivo
op_puntolindero	\N	fin_vida_util_version	ch.ehi.ili2db.dispName	Versión de fin de vida útil
op_construccion	\N	numero_mezanines	ch.ehi.ili2db.dispName	Número de mezanines
op_fuenteespacial	\N	tipo	ch.ehi.ili2db.foreignKey	col_fuenteespacialtipo
op_fuenteespacial	\N	tipo	ch.ehi.ili2db.dispName	Tipo
op_puntolevantamiento	\N	posicion_interpolacion	ch.ehi.ili2db.foreignKey	col_interpolaciontipo
op_puntolevantamiento	\N	posicion_interpolacion	ch.ehi.ili2db.dispName	Posición interpolación
col_volumenvalor	\N	volumen_medicion	ch.ehi.ili2db.unit	m
col_volumenvalor	\N	volumen_medicion	ch.ehi.ili2db.dispName	Volumen medición
col_rrrfuente	\N	rrr_op_restriccion	ch.ehi.ili2db.foreignKey	op_restriccion
col_ueuegrupo	\N	parte_op_terreno	ch.ehi.ili2db.foreignKey	op_terreno
col_volumenvalor	\N	op_construccion_volumen	ch.ehi.ili2db.foreignKey	op_construccion
op_terreno	\N	geometria	ch.ehi.ili2db.coordDimension	3
op_terreno	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
op_terreno	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
op_terreno	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
op_terreno	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
op_terreno	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
op_terreno	\N	geometria	ch.ehi.ili2db.c3Min	-5000.000
op_terreno	\N	geometria	ch.ehi.ili2db.c3Max	6000.000
op_terreno	\N	geometria	ch.ehi.ili2db.srid	4326
op_terreno	\N	geometria	ch.ehi.ili2db.dispName	Geometría
col_responsablefuente	\N	interesado_op_interesado	ch.ehi.ili2db.foreignKey	op_interesado
gc_perimetro	\N	codigo_departamento	ch.ehi.ili2db.dispName	Código del departamento
gc_manzana	\N	codigo	ch.ehi.ili2db.dispName	Código
anystructure	\N	op_servidumbretransito_calidad	ch.ehi.ili2db.foreignKey	op_servidumbretransito
gc_construccion	\N	identificador	ch.ehi.ili2db.dispName	Identificador
snr_fuente_cabidalinderos	\N	tipo_documento	ch.ehi.ili2db.foreignKey	snr_fuentetipo
snr_fuente_cabidalinderos	\N	tipo_documento	ch.ehi.ili2db.dispName	Tipo de documento
op_unidadconstruccion	\N	observaciones	ch.ehi.ili2db.dispName	Observaciones
op_unidadconstruccion	\N	tipo_dominio	ch.ehi.ili2db.foreignKey	op_dominioconstrucciontipo
op_unidadconstruccion	\N	tipo_dominio	ch.ehi.ili2db.dispName	Tipo de dominio
extdireccion	\N	valor_via_generadora	ch.ehi.ili2db.dispName	Valor de vía generadora
extdireccion	\N	sector_predio	ch.ehi.ili2db.foreignKey	extdireccion_sector_predio
extdireccion	\N	sector_predio	ch.ehi.ili2db.dispName	Sector del predio
col_topografofuente	\N	topografo_op_interesado	ch.ehi.ili2db.foreignKey	op_interesado
extdireccion	\N	localizacion	ch.ehi.ili2db.coordDimension	3
extdireccion	\N	localizacion	ch.ehi.ili2db.c1Max	1806900.000
extdireccion	\N	localizacion	ch.ehi.ili2db.c2Max	1984900.000
extdireccion	\N	localizacion	ch.ehi.ili2db.geomType	POINT
extdireccion	\N	localizacion	ch.ehi.ili2db.c1Min	165000.000
extdireccion	\N	localizacion	ch.ehi.ili2db.c2Min	23000.000
extdireccion	\N	localizacion	ch.ehi.ili2db.c3Min	-5000.000
extdireccion	\N	localizacion	ch.ehi.ili2db.c3Max	6000.000
extdireccion	\N	localizacion	ch.ehi.ili2db.srid	4326
extdireccion	\N	localizacion	ch.ehi.ili2db.dispName	Localización
snr_titular	\N	segundo_apellido	ch.ehi.ili2db.dispName	Segundo apellido
op_servidumbretransito	\N	comienzo_vida_util_version	ch.ehi.ili2db.dispName	Versión de comienzo de vida útil
col_mascl	\N	ue_mas_op_terreno	ch.ehi.ili2db.foreignKey	op_terreno
op_puntolindero	\N	exactitud_vertical	ch.ehi.ili2db.unit	cm
op_puntolindero	\N	exactitud_vertical	ch.ehi.ili2db.dispName	Exactitud vertical
gc_predio_catastro	\N	entidad_emisora_alerta	ch.ehi.ili2db.dispName	Entidad emisora de la alerta
gc_unidad_construccion	\N	etiqueta	ch.ehi.ili2db.dispName	Etiqueta
col_uebaunit	\N	ue_op_terreno	ch.ehi.ili2db.foreignKey	op_terreno
col_relacionfuenteuespacial	\N	fuente_espacial	ch.ehi.ili2db.foreignKey	op_fuenteespacial
col_volumenvalor	\N	op_servidumbretransito_volumen	ch.ehi.ili2db.foreignKey	op_servidumbretransito
imagen	\N	uri	ch.ehi.ili2db.dispName	uri
gc_direccion	\N	valor	ch.ehi.ili2db.dispName	Valor
extdireccion	\N	numero_predio	ch.ehi.ili2db.dispName	Número del predio
gc_unidad_construccion	\N	geometria	ch.ehi.ili2db.coordDimension	3
gc_unidad_construccion	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
gc_unidad_construccion	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
gc_unidad_construccion	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
gc_unidad_construccion	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
gc_unidad_construccion	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
gc_unidad_construccion	\N	geometria	ch.ehi.ili2db.c3Min	-5000.000
gc_unidad_construccion	\N	geometria	ch.ehi.ili2db.c3Max	6000.000
gc_unidad_construccion	\N	geometria	ch.ehi.ili2db.srid	4326
gc_unidad_construccion	\N	geometria	ch.ehi.ili2db.dispName	Geometría
op_servidumbretransito	\N	local_id	ch.ehi.ili2db.dispName	Local ID
op_predio	\N	municipio	ch.ehi.ili2db.dispName	Municipio
op_puntocontrol	\N	exactitud_horizontal	ch.ehi.ili2db.unit	cm
op_puntocontrol	\N	exactitud_horizontal	ch.ehi.ili2db.dispName	Exactitud horizontal
op_puntolevantamiento	\N	ue_op_terreno	ch.ehi.ili2db.foreignKey	op_terreno
gc_propietario	\N	segundo_apellido	ch.ehi.ili2db.dispName	Segundo apellido
gc_datos_ph_condiminio	\N	area_total_terreno	ch.ehi.ili2db.unit	m2
gc_datos_ph_condiminio	\N	area_total_terreno	ch.ehi.ili2db.dispName	Área total de terreno
op_predio_copropiedad	\N	predio	ch.ehi.ili2db.foreignKey	op_predio
ini_predio_insumos	\N	gc_predio_catastro	ch.ehi.ili2db.foreignKey	gc_predio_catastro
extarchivo	\N	extraccion	ch.ehi.ili2db.dispName	Extracción
anystructure	\N	op_terreno_procedencia	ch.ehi.ili2db.foreignKey	op_terreno
col_volumenvalor	\N	op_unidadconstruccion_volumen	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
anystructure	\N	op_puntocontrol_calidad	ch.ehi.ili2db.foreignKey	op_puntocontrol
op_terreno	\N	avaluo_terreno	ch.ehi.ili2db.unit	COP
op_terreno	\N	avaluo_terreno	ch.ehi.ili2db.dispName	Avalúo de terreno
gm_surface2dlistvalue	\N	avalue	ch.ehi.ili2db.coordDimension	2
gm_surface2dlistvalue	\N	avalue	ch.ehi.ili2db.c1Max	1806900.000
gm_surface2dlistvalue	\N	avalue	ch.ehi.ili2db.c2Max	1984900.000
gm_surface2dlistvalue	\N	avalue	ch.ehi.ili2db.geomType	POLYGON
gm_surface2dlistvalue	\N	avalue	ch.ehi.ili2db.c1Min	165000.000
gm_surface2dlistvalue	\N	avalue	ch.ehi.ili2db.c2Min	23000.000
gm_surface2dlistvalue	\N	avalue	ch.ehi.ili2db.srid	4326
snr_predio_registro	\N	cabida_linderos	ch.ehi.ili2db.textKind	MTEXT
snr_predio_registro	\N	cabida_linderos	ch.ehi.ili2db.dispName	Cabida y linderos
op_unidadconstruccion	\N	planta_ubicacion	ch.ehi.ili2db.dispName	Planta ubicación
extarchivo	\N	fecha_aceptacion	ch.ehi.ili2db.dispName	Fecha de aceptación
op_unidadconstruccion	\N	fin_vida_util_version	ch.ehi.ili2db.dispName	Versión de fin de vida útil
op_interesado_contacto	\N	direccion_residencia	ch.ehi.ili2db.dispName	Dirección de residencia
op_unidadconstruccion	\N	relacion_superficie	ch.ehi.ili2db.foreignKey	col_relacionsuperficietipo
op_unidadconstruccion	\N	relacion_superficie	ch.ehi.ili2db.dispName	Relación superficie
gc_copropiedad	\N	gc_matriz	ch.ehi.ili2db.foreignKey	gc_predio_catastro
gc_sector_urbano	\N	codigo	ch.ehi.ili2db.dispName	Código
gc_unidad_construccion	\N	planta	ch.ehi.ili2db.dispName	Planta
col_baunitcomointeresado	\N	interesado_op_agrupacion_interesados	ch.ehi.ili2db.foreignKey	op_agrupacion_interesados
cc_metodooperacion	\N	formula	ch.ehi.ili2db.dispName	Fórmula
snr_derecho	\N	codigo_naturaleza_juridica	ch.ehi.ili2db.dispName	Código naturaleza jurídica
op_fuenteadministrativa	\N	ente_emisor	ch.ehi.ili2db.dispName	Ente emisor
op_terreno	\N	manzana_vereda_codigo	ch.ehi.ili2db.dispName	Código de manzana vereda
op_puntolevantamiento	\N	ue_op_servidumbretransito	ch.ehi.ili2db.foreignKey	op_servidumbretransito
op_puntolindero	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
gc_direccion	\N	geometria_referencia	ch.ehi.ili2db.coordDimension	3
gc_direccion	\N	geometria_referencia	ch.ehi.ili2db.c1Max	1806900.000
gc_direccion	\N	geometria_referencia	ch.ehi.ili2db.c2Max	1984900.000
gc_direccion	\N	geometria_referencia	ch.ehi.ili2db.geomType	LINESTRING
gc_direccion	\N	geometria_referencia	ch.ehi.ili2db.c1Min	165000.000
gc_direccion	\N	geometria_referencia	ch.ehi.ili2db.c2Min	23000.000
gc_direccion	\N	geometria_referencia	ch.ehi.ili2db.c3Min	-5000.000
gc_direccion	\N	geometria_referencia	ch.ehi.ili2db.c3Max	6000.000
gc_direccion	\N	geometria_referencia	ch.ehi.ili2db.srid	4326
gc_direccion	\N	geometria_referencia	ch.ehi.ili2db.dispName	Geometría de referencia
gc_perimetro	\N	codigo_nombre	ch.ehi.ili2db.dispName	Código nombre
gc_propietario	\N	primer_apellido	ch.ehi.ili2db.dispName	Primer apellido
op_interesado_contacto	\N	domicilio_notificacion	ch.ehi.ili2db.dispName	Domicilio notificación
op_restriccion	\N	interesado_op_agrupacion_interesados	ch.ehi.ili2db.foreignKey	op_agrupacion_interesados
op_servidumbretransito	\N	geometria	ch.ehi.ili2db.coordDimension	3
op_servidumbretransito	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
op_servidumbretransito	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
op_servidumbretransito	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
op_servidumbretransito	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
op_servidumbretransito	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
op_servidumbretransito	\N	geometria	ch.ehi.ili2db.c3Min	-5000.000
op_servidumbretransito	\N	geometria	ch.ehi.ili2db.c3Max	6000.000
op_servidumbretransito	\N	geometria	ch.ehi.ili2db.srid	4326
op_servidumbretransito	\N	geometria	ch.ehi.ili2db.dispName	Geometría
op_unidadconstruccion	\N	tipo_construccion	ch.ehi.ili2db.foreignKey	op_construcciontipo
op_unidadconstruccion	\N	tipo_construccion	ch.ehi.ili2db.dispName	Tipo de construcción
gc_predio_catastro	\N	numero_predial_anterior	ch.ehi.ili2db.dispName	Número predial anterior
gm_surface2dlistvalue	\N	gm_multisurface2d_geometry	ch.ehi.ili2db.foreignKey	gm_multisurface2d
gc_construccion	\N	geometria	ch.ehi.ili2db.coordDimension	3
gc_construccion	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
gc_construccion	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
gc_construccion	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
gc_construccion	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
gc_construccion	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
gc_construccion	\N	geometria	ch.ehi.ili2db.c3Min	-5000.000
gc_construccion	\N	geometria	ch.ehi.ili2db.c3Max	6000.000
gc_construccion	\N	geometria	ch.ehi.ili2db.srid	4326
gc_construccion	\N	geometria	ch.ehi.ili2db.dispName	Geometría
gc_vereda	\N	nombre	ch.ehi.ili2db.dispName	Nombre
snr_titular	\N	tipo_documento	ch.ehi.ili2db.foreignKey	snr_documentotitulartipo
snr_titular	\N	tipo_documento	ch.ehi.ili2db.dispName	Tipo de documento
op_puntolevantamiento	\N	local_id	ch.ehi.ili2db.dispName	Local ID
op_puntocontrol	\N	ue_op_servidumbretransito	ch.ehi.ili2db.foreignKey	op_servidumbretransito
col_puntofuente	\N	punto_op_puntolindero	ch.ehi.ili2db.foreignKey	op_puntolindero
op_puntocontrol	\N	tipo_punto_control	ch.ehi.ili2db.foreignKey	op_puntocontroltipo
op_puntocontrol	\N	tipo_punto_control	ch.ehi.ili2db.dispName	Tipo de punto de control
snr_fuente_derecho	\N	ciudad_emisora	ch.ehi.ili2db.dispName	Ciudad emisora
imagen	\N	extinteresado_huella_dactilar	ch.ehi.ili2db.foreignKey	extinteresado
extredserviciosfisica	\N	orientada	ch.ehi.ili2db.dispName	Orientada
col_masccl	\N	ue_mas_op_unidadconstruccion	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
op_interesado_contacto	\N	autoriza_notificacion_correo	ch.ehi.ili2db.dispName	Autoriza notificación correo
op_terreno	\N	dimension	ch.ehi.ili2db.foreignKey	col_dimensiontipo
op_terreno	\N	dimension	ch.ehi.ili2db.dispName	Dimensión
op_lindero	\N	local_id	ch.ehi.ili2db.dispName	Local ID
gc_manzana	\N	codigo_anterior	ch.ehi.ili2db.dispName	Código anterior
col_menosccl	\N	ccl_menos	ch.ehi.ili2db.foreignKey	op_lindero
snr_fuente_derecho	\N	fecha_documento	ch.ehi.ili2db.dispName	Fecha del documento
op_unidadconstruccion	\N	area_privada_construida	ch.ehi.ili2db.unit	m2
op_unidadconstruccion	\N	area_privada_construida	ch.ehi.ili2db.dispName	Área privada construida
op_puntolindero	\N	ue_op_construccion	ch.ehi.ili2db.foreignKey	op_construccion
col_puntofuente	\N	fuente_espacial	ch.ehi.ili2db.foreignKey	op_fuenteespacial
op_predio	\N	numero_predial_anterior	ch.ehi.ili2db.dispName	Número predial anterior
op_datos_ph_condominio	\N	area_total_construida_privada	ch.ehi.ili2db.unit	m2
op_datos_ph_condominio	\N	area_total_construida_privada	ch.ehi.ili2db.dispName	Área total construida privada
gc_direccion	\N	gc_predio_catastro_direcciones	ch.ehi.ili2db.foreignKey	gc_predio_catastro
op_agrupacion_interesados	\N	fin_vida_util_version	ch.ehi.ili2db.dispName	Versión de fin de vida útil
op_construccion	\N	fin_vida_util_version	ch.ehi.ili2db.dispName	Versión de fin de vida útil
op_interesado	\N	local_id	ch.ehi.ili2db.dispName	Local ID
snr_titular_derecho	\N	snr_derecho	ch.ehi.ili2db.foreignKey	snr_derecho
extdireccion	\N	op_construccion_ext_direccion_id	ch.ehi.ili2db.foreignKey	op_construccion
op_unidadconstruccion	\N	tipo_unidad_construccion	ch.ehi.ili2db.foreignKey	op_unidadconstrucciontipo
op_unidadconstruccion	\N	tipo_unidad_construccion	ch.ehi.ili2db.dispName	Tipo de unidad de construcción
col_menoscl	\N	ue_menos_op_unidadconstruccion	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
op_restriccion	\N	descripcion	ch.ehi.ili2db.dispName	Descripción
op_fuenteespacial	\N	tipo_principal	ch.ehi.ili2db.foreignKey	ci_forma_presentacion_codigo
op_fuenteespacial	\N	tipo_principal	ch.ehi.ili2db.dispName	Tipo principal
op_puntolindero	\N	puntotipo	ch.ehi.ili2db.foreignKey	op_puntotipo
op_puntolindero	\N	puntotipo	ch.ehi.ili2db.dispName	Tipo de punto
cc_metodooperacion	\N	dimensiones_origen	ch.ehi.ili2db.dispName	Dimensiones origen
op_unidadconstruccion	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
col_responsablefuente	\N	fuente_administrativa	ch.ehi.ili2db.foreignKey	op_fuenteadministrativa
extdireccion	\N	codigo_postal	ch.ehi.ili2db.dispName	Código postal
op_restriccion	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
op_fuenteadministrativa	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
op_puntocontrol	\N	local_id	ch.ehi.ili2db.dispName	Local ID
gc_construccion	\N	etiqueta	ch.ehi.ili2db.dispName	Etiqueta
gc_datos_ph_condiminio	\N	total_unidades_privadas	ch.ehi.ili2db.dispName	Total de unidades privadas
gc_datos_ph_condiminio	\N	gc_predio	ch.ehi.ili2db.foreignKey	gc_predio_catastro
op_servidumbretransito	\N	etiqueta	ch.ehi.ili2db.dispName	Etiqueta
col_menosccl	\N	ue_menos_op_construccion	ch.ehi.ili2db.foreignKey	op_construccion
op_puntolevantamiento	\N	exactitud_horizontal	ch.ehi.ili2db.unit	cm
op_puntolevantamiento	\N	exactitud_horizontal	ch.ehi.ili2db.dispName	Exactitud horizontal
col_menoscl	\N	ue_menos_op_servidumbretransito	ch.ehi.ili2db.foreignKey	op_servidumbretransito
gc_datos_ph_condiminio	\N	total_pisos_torre	ch.ehi.ili2db.dispName	Total pisos de torre
op_interesado	\N	sexo	ch.ehi.ili2db.foreignKey	op_sexotipo
op_interesado	\N	sexo	ch.ehi.ili2db.dispName	Sexo
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.coordDimension	3
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.c1Max	1806900.000
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.c2Max	1984900.000
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.geomType	POLYGON
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.c1Min	165000.000
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.c2Min	23000.000
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.c3Min	-5000.000
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.c3Max	6000.000
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.srid	4326
op_terreno	\N	comienzo_vida_util_version	ch.ehi.ili2db.dispName	Versión de comienzo de vida útil
gc_unidad_construccion	\N	identificador	ch.ehi.ili2db.dispName	Identificador
op_predio	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
op_construccion	\N	tipo_construccion	ch.ehi.ili2db.foreignKey	op_construcciontipo
op_construccion	\N	tipo_construccion	ch.ehi.ili2db.dispName	Tipo de construcción
gc_propietario	\N	tipo_documento	ch.ehi.ili2db.dispName	Tipo de documento
extdireccion	\N	es_direccion_principal	ch.ehi.ili2db.dispName	Es dirección principal
gc_predio_catastro	\N	sistema_procedencia_datos	ch.ehi.ili2db.foreignKey	gc_sistemaprocedenciadatostipo
gc_predio_catastro	\N	sistema_procedencia_datos	ch.ehi.ili2db.dispName	Sistema procedencia de los datos
col_transformacion	\N	op_puntolindero_transformacion_y_resultado	ch.ehi.ili2db.foreignKey	op_puntolindero
anystructure	\N	op_lindero_calidad	ch.ehi.ili2db.foreignKey	op_lindero
op_interesado_contacto	\N	corregimiento	ch.ehi.ili2db.dispName	Corregimiento
op_unidadconstruccion	\N	total_habitaciones	ch.ehi.ili2db.dispName	Total de habitaciones
col_areavalor	\N	areasize	ch.ehi.ili2db.unit	m2
col_areavalor	\N	areasize	ch.ehi.ili2db.dispName	Área
gc_unidad_construccion	\N	codigo_terreno	ch.ehi.ili2db.dispName	Código terreno
op_agrupacion_interesados	\N	tipo	ch.ehi.ili2db.foreignKey	col_grupointeresadotipo
op_agrupacion_interesados	\N	tipo	ch.ehi.ili2db.dispName	Tipo
op_fuenteespacial	\N	fecha_documento_fuente	ch.ehi.ili2db.dispName	Fecha de documento fuente
op_puntocontrol	\N	posicion_interpolacion	ch.ehi.ili2db.foreignKey	col_interpolaciontipo
op_puntocontrol	\N	posicion_interpolacion	ch.ehi.ili2db.dispName	Posición interpolación
op_interesado	\N	primer_nombre	ch.ehi.ili2db.dispName	Primer nombre
col_mascl	\N	ue_mas_op_servidumbretransito	ch.ehi.ili2db.foreignKey	op_servidumbretransito
col_transformacion	\N	op_puntocontrol_transformacion_y_resultado	ch.ehi.ili2db.foreignKey	op_puntocontrol
fraccion	\N	op_predio_copropiedad_coeficiente	ch.ehi.ili2db.foreignKey	op_predio_copropiedad
op_derecho	\N	interesado_op_interesado	ch.ehi.ili2db.foreignKey	op_interesado
snr_titular_derecho	\N	snr_titular	ch.ehi.ili2db.foreignKey	snr_titular
op_predio	\N	departamento	ch.ehi.ili2db.dispName	Departamento
op_datos_ph_condominio	\N	area_total_terreno_comun	ch.ehi.ili2db.unit	m2
op_datos_ph_condominio	\N	area_total_terreno_comun	ch.ehi.ili2db.dispName	Área total de terreno común
col_puntoccl	\N	punto_op_puntolindero	ch.ehi.ili2db.foreignKey	op_puntolindero
anystructure	\N	op_lindero_procedencia	ch.ehi.ili2db.foreignKey	op_lindero
op_lindero	\N	localizacion_textual	ch.ehi.ili2db.dispName	Localización textual
gc_vereda	\N	codigo	ch.ehi.ili2db.dispName	Código
op_fuenteadministrativa	\N	estado_disponibilidad	ch.ehi.ili2db.foreignKey	col_estadodisponibilidadtipo
op_fuenteadministrativa	\N	estado_disponibilidad	ch.ehi.ili2db.dispName	Estado de disponibilidad
gc_unidad_construccion	\N	anio_construccion	ch.ehi.ili2db.dispName	Año de construcción
op_puntocontrol	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
extarchivo	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
op_lindero	\N	longitud	ch.ehi.ili2db.unit	m
op_lindero	\N	longitud	ch.ehi.ili2db.dispName	Longitud
gc_perimetro	\N	tipo_avaluo	ch.ehi.ili2db.dispName	Tipo de avalúo
gc_vereda	\N	geometria	ch.ehi.ili2db.coordDimension	2
gc_vereda	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
gc_vereda	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
gc_vereda	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
gc_vereda	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
gc_vereda	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
gc_vereda	\N	geometria	ch.ehi.ili2db.srid	4326
gc_vereda	\N	geometria	ch.ehi.ili2db.dispName	Geometría
anystructure	\N	op_restriccion_calidad	ch.ehi.ili2db.foreignKey	op_restriccion
extinteresado	\N	op_agrupacion_intrsdos_ext_pid	ch.ehi.ili2db.foreignKey	op_agrupacion_interesados
anystructure	\N	op_restriccion_procedencia	ch.ehi.ili2db.foreignKey	op_restriccion
col_uefuente	\N	ue_op_unidadconstruccion	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
gc_construccion	\N	gc_predio	ch.ehi.ili2db.foreignKey	gc_predio_catastro
snr_titular	\N	razon_social	ch.ehi.ili2db.textKind	MTEXT
snr_titular	\N	razon_social	ch.ehi.ili2db.dispName	Razón social
op_construccion	\N	etiqueta	ch.ehi.ili2db.dispName	Etiqueta
col_uebaunit	\N	ue_op_unidadconstruccion	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
col_masccl	\N	ue_mas_op_servidumbretransito	ch.ehi.ili2db.foreignKey	op_servidumbretransito
op_puntolevantamiento	\N	puntotipo	ch.ehi.ili2db.foreignKey	op_puntotipo
op_puntolevantamiento	\N	puntotipo	ch.ehi.ili2db.dispName	Tipo de punto
op_interesado_contacto	\N	op_interesado	ch.ehi.ili2db.foreignKey	op_interesado
gc_datos_ph_condiminio	\N	area_total_construida	ch.ehi.ili2db.unit	m2
gc_datos_ph_condiminio	\N	area_total_construida	ch.ehi.ili2db.dispName	Área total construida
gc_datos_ph_condiminio	\N	area_total_construida_privada	ch.ehi.ili2db.unit	m2
gc_datos_ph_condiminio	\N	area_total_construida_privada	ch.ehi.ili2db.dispName	Área total construida privada
snr_predio_registro	\N	codigo_orip	ch.ehi.ili2db.dispName	Código ORIP
op_construccion	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
op_fuenteespacial	\N	descripcion	ch.ehi.ili2db.textKind	MTEXT
op_fuenteespacial	\N	descripcion	ch.ehi.ili2db.dispName	Descripción
col_puntocl	\N	punto_op_puntolindero	ch.ehi.ili2db.foreignKey	op_puntolindero
snr_fuente_cabidalinderos	\N	ente_emisor	ch.ehi.ili2db.dispName	Ente emisor
gc_vereda	\N	codigo_anterior	ch.ehi.ili2db.dispName	Código anterior
op_fuenteadministrativa	\N	fecha_documento_fuente	ch.ehi.ili2db.dispName	Fecha de documento fuente
op_fuenteespacial	\N	local_id	ch.ehi.ili2db.dispName	Local ID
op_servidumbretransito	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
op_terreno	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
col_miembros	\N	interesado_op_interesado	ch.ehi.ili2db.foreignKey	op_interesado
gc_unidad_construccion	\N	area_construida	ch.ehi.ili2db.unit	m2
gc_unidad_construccion	\N	area_construida	ch.ehi.ili2db.dispName	Área construida
op_terreno	\N	numero_subterraneos	ch.ehi.ili2db.dispName	Número de subterráneos
gc_comisiones_unidad_construccion	\N	geometria	ch.ehi.ili2db.coordDimension	3
gc_comisiones_unidad_construccion	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
gc_comisiones_unidad_construccion	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
gc_comisiones_unidad_construccion	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
gc_comisiones_unidad_construccion	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
gc_comisiones_unidad_construccion	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
gc_comisiones_unidad_construccion	\N	geometria	ch.ehi.ili2db.c3Min	-5000.000
gc_comisiones_unidad_construccion	\N	geometria	ch.ehi.ili2db.c3Max	6000.000
gc_comisiones_unidad_construccion	\N	geometria	ch.ehi.ili2db.srid	4326
gc_comisiones_unidad_construccion	\N	geometria	ch.ehi.ili2db.dispName	Geometría
gc_perimetro	\N	codigo_municipio	ch.ehi.ili2db.dispName	Código del municipio
op_interesado_contacto	\N	telefono1	ch.ehi.ili2db.dispName	Teléfono 1
op_predio_copropiedad	\N	copropiedad	ch.ehi.ili2db.foreignKey	op_predio
op_unidadconstruccion	\N	total_banios	ch.ehi.ili2db.dispName	Total de baños
op_interesado	\N	grupo_etnico	ch.ehi.ili2db.foreignKey	op_grupoetnicotipo
op_interesado	\N	grupo_etnico	ch.ehi.ili2db.dispName	Grupo étnico
imagen	\N	extinteresado_fotografia	ch.ehi.ili2db.foreignKey	extinteresado
op_interesado_contacto	\N	vereda	ch.ehi.ili2db.dispName	Vereda
op_fuenteespacial	\N	estado_disponibilidad	ch.ehi.ili2db.foreignKey	col_estadodisponibilidadtipo
op_fuenteespacial	\N	estado_disponibilidad	ch.ehi.ili2db.dispName	Estado de disponibilidad
gc_direccion	\N	principal	ch.ehi.ili2db.dispName	Principal
gc_unidad_construccion	\N	total_pisos	ch.ehi.ili2db.dispName	Total de pisos
op_unidadconstruccion	\N	comienzo_vida_util_version	ch.ehi.ili2db.dispName	Versión de comienzo de vida útil
op_datos_ph_condominio	\N	total_sotanos	ch.ehi.ili2db.dispName	Total de sótanos
fraccion	\N	denominador	ch.ehi.ili2db.dispName	Denominador
op_interesado	\N	comienzo_vida_util_version	ch.ehi.ili2db.dispName	Versión de comienzo de vida útil
op_puntocontrol	\N	exactitud_vertical	ch.ehi.ili2db.unit	cm
op_puntocontrol	\N	exactitud_vertical	ch.ehi.ili2db.dispName	Exactitud vertical
op_terreno	\N	etiqueta	ch.ehi.ili2db.dispName	Etiqueta
col_uebaunit	\N	baunit	ch.ehi.ili2db.foreignKey	op_predio
col_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.coordDimension	3
col_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.c1Max	1806900.000
col_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.c2Max	1984900.000
col_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.geomType	POINT
col_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.c1Min	165000.000
col_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.c2Min	23000.000
col_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.c3Min	-5000.000
col_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.c3Max	6000.000
col_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.srid	4326
col_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.dispName	Localización transformada
op_unidadconstruccion	\N	identificador	ch.ehi.ili2db.dispName	Identificador
gc_datos_ph_condiminio	\N	area_total_construida_comun	ch.ehi.ili2db.unit	m2
gc_datos_ph_condiminio	\N	area_total_construida_comun	ch.ehi.ili2db.dispName	Área total construida común
snr_predio_registro	\N	matricula_inmobiliaria	ch.ehi.ili2db.dispName	Matrícula inmobiliaria
op_predio	\N	tipo	ch.ehi.ili2db.foreignKey	col_baunittipo
op_predio	\N	tipo	ch.ehi.ili2db.dispName	Tipo
op_puntolevantamiento	\N	metodoproduccion	ch.ehi.ili2db.foreignKey	col_metodoproducciontipo
op_puntolevantamiento	\N	metodoproduccion	ch.ehi.ili2db.dispName	Método de producción
gc_predio_catastro	\N	circulo_registral	ch.ehi.ili2db.dispName	Círculo registral
op_fuenteadministrativa	\N	tipo_principal	ch.ehi.ili2db.foreignKey	ci_forma_presentacion_codigo
op_fuenteadministrativa	\N	tipo_principal	ch.ehi.ili2db.dispName	Tipo principal
op_datos_ph_condominio	\N	torre_no	ch.ehi.ili2db.dispName	Torre número
op_predio	\N	fin_vida_util_version	ch.ehi.ili2db.dispName	Versión de fin de vida útil
op_restriccion	\N	interesado_op_interesado	ch.ehi.ili2db.foreignKey	op_interesado
op_puntocontrol	\N	ue_op_construccion	ch.ehi.ili2db.foreignKey	op_construccion
op_puntocontrol	\N	geometria	ch.ehi.ili2db.coordDimension	3
op_puntocontrol	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
op_puntocontrol	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
op_puntocontrol	\N	geometria	ch.ehi.ili2db.geomType	POINT
op_puntocontrol	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
op_puntocontrol	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
op_puntocontrol	\N	geometria	ch.ehi.ili2db.c3Min	-5000.000
op_puntocontrol	\N	geometria	ch.ehi.ili2db.c3Max	6000.000
op_puntocontrol	\N	geometria	ch.ehi.ili2db.srid	4326
op_puntocontrol	\N	geometria	ch.ehi.ili2db.dispName	Geometría
col_baunitfuente	\N	unidad	ch.ehi.ili2db.foreignKey	op_predio
op_interesado_contacto	\N	telefono2	ch.ehi.ili2db.dispName	Teléfono 2
op_predio	\N	matricula_inmobiliaria	ch.ehi.ili2db.dispName	Matrícula inmobiliaria
gc_predio_catastro	\N	estado_alerta	ch.ehi.ili2db.dispName	Estado alerta
op_unidadconstruccion	\N	local_id	ch.ehi.ili2db.dispName	Local ID
col_masccl	\N	ue_mas_op_terreno	ch.ehi.ili2db.foreignKey	op_terreno
op_terreno	\N	area_terreno	ch.ehi.ili2db.unit	m2
op_terreno	\N	area_terreno	ch.ehi.ili2db.dispName	Área de terreno
op_terreno	\N	local_id	ch.ehi.ili2db.dispName	Local ID
extarchivo	\N	local_id	ch.ehi.ili2db.dispName	Local ID
snr_derecho	\N	calidad_derecho_registro	ch.ehi.ili2db.foreignKey	snr_calidadderechotipo
snr_derecho	\N	calidad_derecho_registro	ch.ehi.ili2db.dispName	Calidad derecho registro
op_interesado	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
gc_predio_catastro	\N	fecha_datos	ch.ehi.ili2db.dispName	Fecha de los datos
gc_unidad_construccion	\N	area_privada	ch.ehi.ili2db.unit	m2
gc_unidad_construccion	\N	area_privada	ch.ehi.ili2db.dispName	Área privada
anystructure	\N	op_construccion_procedencia	ch.ehi.ili2db.foreignKey	op_construccion
op_interesado	\N	razon_social	ch.ehi.ili2db.dispName	Razón social
col_cclfuente	\N	ccl	ch.ehi.ili2db.foreignKey	op_lindero
gc_predio_catastro	\N	matricula_inmobiliaria_catastro	ch.ehi.ili2db.dispName	Matrícula inmobiliaria catastro
snr_titular	\N	numero_documento	ch.ehi.ili2db.dispName	Número de documento
col_baunitfuente	\N	fuente_espacial	ch.ehi.ili2db.foreignKey	op_fuenteespacial
extdireccion	\N	letra_via_principal	ch.ehi.ili2db.dispName	Letra vía principal
gc_barrio	\N	nombre	ch.ehi.ili2db.dispName	Nombre
op_derecho	\N	comprobacion_comparte	ch.ehi.ili2db.dispName	Comprobación si comparte
op_construccion	\N	relacion_superficie	ch.ehi.ili2db.foreignKey	col_relacionsuperficietipo
op_construccion	\N	relacion_superficie	ch.ehi.ili2db.dispName	Relación superficie
op_predio	\N	local_id	ch.ehi.ili2db.dispName	Local ID
col_puntocl	\N	punto_op_puntocontrol	ch.ehi.ili2db.foreignKey	op_puntocontrol
gc_sector_urbano	\N	geometria	ch.ehi.ili2db.coordDimension	2
gc_sector_urbano	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
gc_sector_urbano	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
gc_sector_urbano	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
gc_sector_urbano	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
gc_sector_urbano	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
gc_sector_urbano	\N	geometria	ch.ehi.ili2db.srid	4326
gc_sector_urbano	\N	geometria	ch.ehi.ili2db.dispName	Geometría
op_fuenteadministrativa	\N	tipo	ch.ehi.ili2db.foreignKey	op_fuenteadministrativatipo
op_fuenteadministrativa	\N	tipo	ch.ehi.ili2db.dispName	Tipo
op_unidadconstruccion	\N	op_construccion	ch.ehi.ili2db.foreignKey	op_construccion
col_mascl	\N	ue_mas_op_unidadconstruccion	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
op_interesado_contacto	\N	correo_electronico	ch.ehi.ili2db.dispName	Correo electrónico
op_restriccion	\N	comprobacion_comparte	ch.ehi.ili2db.dispName	Comprobación si comparte
snr_predio_registro	\N	fecha_datos	ch.ehi.ili2db.dispName	Fecha de datos
op_fuenteadministrativa	\N	local_id	ch.ehi.ili2db.dispName	Local ID
op_puntolevantamiento	\N	ue_op_construccion	ch.ehi.ili2db.foreignKey	op_construccion
op_puntolevantamiento	\N	comienzo_vida_util_version	ch.ehi.ili2db.dispName	Versión de comienzo de vida útil
anystructure	\N	op_interesado_calidad	ch.ehi.ili2db.foreignKey	op_interesado
anystructure	\N	op_interesado_procedencia	ch.ehi.ili2db.foreignKey	op_interesado
op_predio	\N	tiene_fmi	ch.ehi.ili2db.dispName	Tiene FMI
op_puntolevantamiento	\N	fotoidentificacion	ch.ehi.ili2db.foreignKey	op_fotoidentificaciontipo
op_puntolevantamiento	\N	fotoidentificacion	ch.ehi.ili2db.dispName	Fotoidentificación
col_puntoccl	\N	punto_op_puntocontrol	ch.ehi.ili2db.foreignKey	op_puntocontrol
gc_unidad_construccion	\N	tipo_construccion	ch.ehi.ili2db.foreignKey	gc_unidadconstrucciontipo
gc_unidad_construccion	\N	tipo_construccion	ch.ehi.ili2db.dispName	Tipo de construcción
op_construccion	\N	comienzo_vida_util_version	ch.ehi.ili2db.dispName	Versión de comienzo de vida útil
op_construccion	\N	identificador	ch.ehi.ili2db.dispName	Identificador
col_uebaunit	\N	ue_op_construccion	ch.ehi.ili2db.foreignKey	op_construccion
col_uefuente	\N	ue_op_construccion	ch.ehi.ili2db.foreignKey	op_construccion
gc_vereda	\N	codigo_sector	ch.ehi.ili2db.dispName	Código del sector
extdireccion	\N	clase_via_principal	ch.ehi.ili2db.foreignKey	extdireccion_clase_via_principal
extdireccion	\N	clase_via_principal	ch.ehi.ili2db.dispName	Clase de vía principal
extdireccion	\N	extunidadedificcnfsica_ext_direccion_id	ch.ehi.ili2db.foreignKey	extunidadedificacionfisica
gc_manzana	\N	codigo_barrio	ch.ehi.ili2db.dispName	Código de barrio
op_terreno	\N	relacion_superficie	ch.ehi.ili2db.foreignKey	col_relacionsuperficietipo
op_terreno	\N	relacion_superficie	ch.ehi.ili2db.dispName	Relación superficie
snr_predio_registro	\N	numero_predial_anterior_en_fmi	ch.ehi.ili2db.dispName	Número predial anterior en FMI
op_unidadconstruccion	\N	geometria	ch.ehi.ili2db.coordDimension	3
op_unidadconstruccion	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
op_unidadconstruccion	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
op_unidadconstruccion	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
op_unidadconstruccion	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
op_unidadconstruccion	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
op_unidadconstruccion	\N	geometria	ch.ehi.ili2db.c3Min	-5000.000
op_unidadconstruccion	\N	geometria	ch.ehi.ili2db.c3Max	6000.000
op_unidadconstruccion	\N	geometria	ch.ehi.ili2db.srid	4326
op_unidadconstruccion	\N	geometria	ch.ehi.ili2db.dispName	Geometría
gc_perimetro	\N	nombre_geografico	ch.ehi.ili2db.dispName	Nombre geográfico
col_menosccl	\N	ue_menos_op_servidumbretransito	ch.ehi.ili2db.foreignKey	op_servidumbretransito
extdireccion	\N	extinteresado_ext_direccion_id	ch.ehi.ili2db.foreignKey	extinteresado
anystructure	\N	op_terreno_calidad	ch.ehi.ili2db.foreignKey	op_terreno
extdireccion	\N	sector_ciudad	ch.ehi.ili2db.foreignKey	extdireccion_sector_ciudad
extdireccion	\N	sector_ciudad	ch.ehi.ili2db.dispName	Sector de la ciudad
col_baunitcomointeresado	\N	interesado_op_interesado	ch.ehi.ili2db.foreignKey	op_interesado
op_agrupacion_interesados	\N	comienzo_vida_util_version	ch.ehi.ili2db.dispName	Versión de comienzo de vida útil
op_fuenteespacial	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
op_lindero	\N	comienzo_vida_util_version	ch.ehi.ili2db.dispName	Versión de comienzo de vida útil
gc_construccion	\N	numero_mezanines	ch.ehi.ili2db.dispName	Número de mezanines
extarchivo	\N	op_fuenteadministrtiva_ext_archivo_id	ch.ehi.ili2db.foreignKey	op_fuenteadministrativa
op_restriccion	\N	local_id	ch.ehi.ili2db.dispName	Local ID
gc_terreno	\N	area_terreno_alfanumerica	ch.ehi.ili2db.unit	m2
gc_terreno	\N	area_terreno_alfanumerica	ch.ehi.ili2db.dispName	Área terreno alfanumérica
snr_derecho	\N	snr_predio_registro	ch.ehi.ili2db.foreignKey	snr_predio_registro
snr_fuente_derecho	\N	ente_emisor	ch.ehi.ili2db.textKind	MTEXT
snr_fuente_derecho	\N	ente_emisor	ch.ehi.ili2db.dispName	Ente emisor
op_puntocontrol	\N	comienzo_vida_util_version	ch.ehi.ili2db.dispName	Versión de comienzo de vida útil
extdireccion	\N	nombre_predio	ch.ehi.ili2db.dispName	Nombre del predio
gc_terreno	\N	area_terreno_digital	ch.ehi.ili2db.unit	m2
gc_terreno	\N	area_terreno_digital	ch.ehi.ili2db.dispName	Área terreno digital
op_fuenteespacial	\N	metadato	ch.ehi.ili2db.textKind	MTEXT
op_fuenteespacial	\N	metadato	ch.ehi.ili2db.dispName	Metadato
gc_terreno	\N	manzana_vereda_codigo	ch.ehi.ili2db.dispName	Código de manzana vereda
op_datos_ph_condominio	\N	area_total_terreno_privada	ch.ehi.ili2db.unit	m2
op_datos_ph_condominio	\N	area_total_terreno_privada	ch.ehi.ili2db.dispName	Área total de terreno privada
op_construccion	\N	area_construccion	ch.ehi.ili2db.unit	m2
op_construccion	\N	area_construccion	ch.ehi.ili2db.dispName	Área de construcción
col_puntofuente	\N	punto_op_puntolevantamiento	ch.ehi.ili2db.foreignKey	op_puntolevantamiento
op_derecho	\N	fin_vida_util_version	ch.ehi.ili2db.dispName	Versión de fin de vida útil
cc_metodooperacion	\N	ddimensiones_objetivo	ch.ehi.ili2db.dispName	Ddimensiones objetivo
op_puntolindero	\N	posicion_interpolacion	ch.ehi.ili2db.foreignKey	col_interpolaciontipo
op_puntolindero	\N	posicion_interpolacion	ch.ehi.ili2db.dispName	Posición interpolación
gc_unidad_construccion	\N	total_locales	ch.ehi.ili2db.dispName	Total de locales
op_construccion	\N	local_id	ch.ehi.ili2db.dispName	Local ID
op_servidumbretransito	\N	relacion_superficie	ch.ehi.ili2db.foreignKey	col_relacionsuperficietipo
op_servidumbretransito	\N	relacion_superficie	ch.ehi.ili2db.dispName	Relación superficie
op_puntolevantamiento	\N	id_punto_levantamiento	ch.ehi.ili2db.dispName	ID del punto de levantamiento
gc_barrio	\N	geometria	ch.ehi.ili2db.coordDimension	2
gc_barrio	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
gc_barrio	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
gc_barrio	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
gc_barrio	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
gc_barrio	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
gc_barrio	\N	geometria	ch.ehi.ili2db.srid	4326
gc_barrio	\N	geometria	ch.ehi.ili2db.dispName	Geometría
col_rrrfuente	\N	rrr_op_derecho	ch.ehi.ili2db.foreignKey	op_derecho
op_restriccion	\N	unidad	ch.ehi.ili2db.foreignKey	op_predio
op_puntolindero	\N	ue_op_servidumbretransito	ch.ehi.ili2db.foreignKey	op_servidumbretransito
snr_predio_registro	\N	numero_predial_nuevo_en_fmi	ch.ehi.ili2db.dispName	Número predial nuevo en FMI
gc_propietario	\N	numero_documento	ch.ehi.ili2db.dispName	Número de documento
op_construccion	\N	geometria	ch.ehi.ili2db.coordDimension	3
op_construccion	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
op_construccion	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
op_construccion	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
op_construccion	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
op_construccion	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
op_construccion	\N	geometria	ch.ehi.ili2db.c3Min	-5000.000
op_construccion	\N	geometria	ch.ehi.ili2db.c3Max	6000.000
op_construccion	\N	geometria	ch.ehi.ili2db.srid	4326
op_construccion	\N	geometria	ch.ehi.ili2db.dispName	Geometría
op_fuenteadministrativa	\N	numero_fuente	ch.ehi.ili2db.dispName	Número de fuente
op_puntolevantamiento	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
op_agrupacion_interesados	\N	local_id	ch.ehi.ili2db.dispName	Local ID
op_datos_ph_condominio	\N	area_total_construida_comun	ch.ehi.ili2db.unit	m2
op_datos_ph_condominio	\N	area_total_construida_comun	ch.ehi.ili2db.dispName	Área total construida común
anystructure	\N	op_derecho_calidad	ch.ehi.ili2db.foreignKey	op_derecho
op_predio	\N	codigo_orip	ch.ehi.ili2db.dispName	Código ORIP
col_puntofuente	\N	punto_op_puntocontrol	ch.ehi.ili2db.foreignKey	op_puntocontrol
col_puntoccl	\N	ccl	ch.ehi.ili2db.foreignKey	op_lindero
col_baunitcomointeresado	\N	unidad	ch.ehi.ili2db.foreignKey	op_predio
anystructure	\N	op_construccion_calidad	ch.ehi.ili2db.foreignKey	op_construccion
col_unidadfuente	\N	fuente_administrativa	ch.ehi.ili2db.foreignKey	op_fuenteadministrativa
gc_sector_rural	\N	codigo	ch.ehi.ili2db.dispName	Código
op_datos_ph_condominio	\N	total_unidades_privadas	ch.ehi.ili2db.dispName	Total de unidades privadas
extarchivo	\N	op_fuenteespacial_ext_archivo_id	ch.ehi.ili2db.foreignKey	op_fuenteespacial
op_predio	\N	id_operacion	ch.ehi.ili2db.dispName	Identificador único de operación
op_restriccion	\N	comienzo_vida_util_version	ch.ehi.ili2db.dispName	Versión de comienzo de vida útil
col_menosccl	\N	ue_menos_op_unidadconstruccion	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
op_unidadconstruccion	\N	etiqueta	ch.ehi.ili2db.dispName	Etiqueta
col_menoscl	\N	ue_menos_op_construccion	ch.ehi.ili2db.foreignKey	op_construccion
op_predio	\N	numero_predial	ch.ehi.ili2db.dispName	Número predial
op_predio	\N	condicion_predio	ch.ehi.ili2db.foreignKey	op_condicionprediotipo
op_predio	\N	condicion_predio	ch.ehi.ili2db.dispName	Condición del predio
op_datos_ph_condominio	\N	total_pisos_torre	ch.ehi.ili2db.dispName	Total pisos de torre
op_predio	\N	comienzo_vida_util_version	ch.ehi.ili2db.dispName	Versión de comienzo de vida útil
snr_predio_registro	\N	matricula_inmobiliaria_matriz	ch.ehi.ili2db.dispName	Matrícula inmobiliaria matriz
op_puntocontrol	\N	ue_op_unidadconstruccion	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
op_puntolevantamiento	\N	exactitud_vertical	ch.ehi.ili2db.unit	cm
op_puntolevantamiento	\N	exactitud_vertical	ch.ehi.ili2db.dispName	Exactitud vertical
op_puntolevantamiento	\N	ue_op_unidadconstruccion	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
op_interesado	\N	tipo	ch.ehi.ili2db.foreignKey	op_interesadotipo
op_interesado	\N	tipo	ch.ehi.ili2db.dispName	Tipo
op_restriccion	\N	uso_efectivo	ch.ehi.ili2db.dispName	Uso efectivo
gc_predio_catastro	\N	tipo_predio	ch.ehi.ili2db.dispName	Tipo de predio
gc_propietario	\N	segundo_nombre	ch.ehi.ili2db.dispName	Segundo nombre
col_clfuente	\N	fuente_espacial	ch.ehi.ili2db.foreignKey	op_fuenteespacial
op_unidadconstruccion	\N	dimension	ch.ehi.ili2db.foreignKey	col_dimensiontipo
op_unidadconstruccion	\N	dimension	ch.ehi.ili2db.dispName	Dimensión
extdireccion	\N	letra_via_generadora	ch.ehi.ili2db.dispName	Letra de vía generadora
fraccion	\N	col_miembros_participacion	ch.ehi.ili2db.foreignKey	col_miembros
extdireccion	\N	valor_via_principal	ch.ehi.ili2db.dispName	Valor vía principal
gc_unidad_construccion	\N	tipo_dominio	ch.ehi.ili2db.dispName	Tipo de dominio
col_volumenvalor	\N	op_terreno_volumen	ch.ehi.ili2db.foreignKey	op_terreno
gc_datos_ph_condiminio	\N	torre_no	ch.ehi.ili2db.dispName	Torre número
gc_unidad_construccion	\N	uso	ch.ehi.ili2db.dispName	Uso
gc_datos_ph_condiminio	\N	total_sotanos	ch.ehi.ili2db.dispName	Total de sótanos
gc_predio_catastro	\N	numero_predial	ch.ehi.ili2db.dispName	Número predial
snr_titular	\N	tipo_persona	ch.ehi.ili2db.foreignKey	snr_personatitulartipo
snr_titular	\N	tipo_persona	ch.ehi.ili2db.dispName	Tipo de persona
gc_barrio	\N	codigo_sector	ch.ehi.ili2db.dispName	Código sector
fraccion	\N	numerador	ch.ehi.ili2db.dispName	Numerador
op_construccion	\N	numero_semisotanos	ch.ehi.ili2db.dispName	Número de semisótanos
extarchivo	\N	fecha_grabacion	ch.ehi.ili2db.dispName	Fecha de grabación
gc_unidad_construccion	\N	total_habitaciones	ch.ehi.ili2db.dispName	Total de habitaciones
op_lindero	\N	fin_vida_util_version	ch.ehi.ili2db.dispName	Versión de fin de vida útil
op_datos_ph_condominio	\N	area_total_terreno	ch.ehi.ili2db.unit	m2
op_datos_ph_condominio	\N	area_total_terreno	ch.ehi.ili2db.dispName	Área total de terreno
extinteresado	\N	nombre	ch.ehi.ili2db.dispName	Nombre
gc_terreno	\N	geometria	ch.ehi.ili2db.coordDimension	2
gc_terreno	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
gc_terreno	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
gc_terreno	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
gc_terreno	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
gc_terreno	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
gc_terreno	\N	geometria	ch.ehi.ili2db.srid	4326
gc_terreno	\N	geometria	ch.ehi.ili2db.dispName	Geometría
op_puntocontrol	\N	fin_vida_util_version	ch.ehi.ili2db.dispName	Versión de fin de vida útil
snr_fuente_derecho	\N	tipo_documento	ch.ehi.ili2db.foreignKey	snr_fuentetipo
snr_fuente_derecho	\N	tipo_documento	ch.ehi.ili2db.dispName	Tipo de documento
op_puntolindero	\N	geometria	ch.ehi.ili2db.coordDimension	3
op_puntolindero	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
op_puntolindero	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
op_puntolindero	\N	geometria	ch.ehi.ili2db.geomType	POINT
op_puntolindero	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
op_puntolindero	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
op_puntolindero	\N	geometria	ch.ehi.ili2db.c3Min	-5000.000
op_puntolindero	\N	geometria	ch.ehi.ili2db.c3Max	6000.000
op_puntolindero	\N	geometria	ch.ehi.ili2db.srid	4326
op_puntolindero	\N	geometria	ch.ehi.ili2db.dispName	Geometría
op_derecho	\N	descripcion	ch.ehi.ili2db.dispName	Descripción
anystructure	\N	op_puntocontrol_procedencia	ch.ehi.ili2db.foreignKey	op_puntocontrol
op_puntolevantamiento	\N	fin_vida_util_version	ch.ehi.ili2db.dispName	Versión de fin de vida útil
op_puntolindero	\N	ue_op_terreno	ch.ehi.ili2db.foreignKey	op_terreno
anystructure	\N	op_unidadconstruccion_procedencia	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
op_derecho	\N	espacio_de_nombres	ch.ehi.ili2db.dispName	Espacio de nombres
gc_predio_catastro	\N	condicion_predio	ch.ehi.ili2db.foreignKey	gc_condicionprediotipo
gc_predio_catastro	\N	condicion_predio	ch.ehi.ili2db.dispName	Condición del predio
gc_propietario	\N	gc_predio_catastro	ch.ehi.ili2db.foreignKey	gc_predio_catastro
anystructure	\N	op_puntolindero_procedencia	ch.ehi.ili2db.foreignKey	op_puntolindero
gc_sector_rural	\N	geometria	ch.ehi.ili2db.coordDimension	2
gc_sector_rural	\N	geometria	ch.ehi.ili2db.c1Max	1806900.000
gc_sector_rural	\N	geometria	ch.ehi.ili2db.c2Max	1984900.000
gc_sector_rural	\N	geometria	ch.ehi.ili2db.geomType	MULTIPOLYGON
gc_sector_rural	\N	geometria	ch.ehi.ili2db.c1Min	165000.000
gc_sector_rural	\N	geometria	ch.ehi.ili2db.c2Min	23000.000
gc_sector_rural	\N	geometria	ch.ehi.ili2db.srid	4326
gc_sector_rural	\N	geometria	ch.ehi.ili2db.dispName	Geometría
op_interesado	\N	fin_vida_util_version	ch.ehi.ili2db.dispName	Versión de fin de vida útil
col_uefuente	\N	fuente_espacial	ch.ehi.ili2db.foreignKey	op_fuenteespacial
op_predio_insumos_operacion	\N	op_predio	ch.ehi.ili2db.foreignKey	op_predio
col_responsablefuente	\N	interesado_op_agrupacion_interesados	ch.ehi.ili2db.foreignKey	op_agrupacion_interesados
col_areavalor	\N	op_terreno_area	ch.ehi.ili2db.foreignKey	op_terreno
snr_fuente_cabidalinderos	\N	fecha_documento	ch.ehi.ili2db.dispName	Fecha de documento
col_masccl	\N	ccl_mas	ch.ehi.ili2db.foreignKey	op_lindero
op_puntolindero	\N	ubicacion_punto	ch.ehi.ili2db.foreignKey	op_ubicacionpuntotipo
op_puntolindero	\N	ubicacion_punto	ch.ehi.ili2db.dispName	Ubicación del punto
col_ueuegrupo	\N	parte_op_unidadconstruccion	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
op_datos_ph_condominio	\N	op_predio	ch.ehi.ili2db.foreignKey	op_predio
gc_barrio	\N	codigo	ch.ehi.ili2db.dispName	Código
extdireccion	\N	op_unidadconstruccion_ext_direccion_id	ch.ehi.ili2db.foreignKey	op_unidadconstruccion
op_predio_insumos_operacion	\N	ini_predio_insumos	ch.ehi.ili2db.foreignKey	ini_predio_insumos
op_interesado	\N	segundo_apellido	ch.ehi.ili2db.dispName	Segundo apellido
\.


--
-- TOC entry 12699 (class 0 OID 339617)
-- Dependencies: 2265
-- Data for Name: t_ili2db_dataset; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.t_ili2db_dataset (t_id, datasetname) FROM stdin;
\.


--
-- TOC entry 12700 (class 0 OID 339620)
-- Dependencies: 2266
-- Data for Name: t_ili2db_inheritance; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.t_ili2db_inheritance (thisclass, baseclass) FROM stdin;
LADM_COL_V1_6.LADM_Nucleo.COL_Nivel	LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Barrio	\N
LADM_COL_V1_6.LADM_Nucleo.COL_BAUnit	LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado
LADM_COL_V1_6.LADM_Nucleo.COL_RelacionNecesariaBAUnits	LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro	\N
LADM_COL_V1_6.LADM_Nucleo.COL_RelacionNecesariaUnidadesEspaciales	LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Terreno	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoCl	\N
Operacion_V2_10.Operacion.OP_Derecho	LADM_COL_V1_6.LADM_Nucleo.COL_DRR
LADM_COL_V1_6.LADM_Nucleo.col_baunitFuente	\N
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Agrupacion_Interesados	LADM_COL_V1_6.LADM_Nucleo.COL_Interesado
LADM_COL_V1_6.LADM_Nucleo.col_baunitRrr	\N
Operacion_V2_10.Operacion.OP_UnidadConstruccion	LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial
Operacion_V2_10.Operacion.OP_Predio	LADM_COL_V1_6.LADM_Nucleo.COL_BAUnit
Operacion_V2_10.Operacion.op_construccion_unidadconstruccion	\N
LADM_COL_V1_6.LADM_Nucleo.Fraccion	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Punto	LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_terreno_predio	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Interesado	LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado
Datos_SNR_V2_10.Datos_SNR.snr_fuente_cabidalinderos	\N
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Construccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_menosCcl	\N
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacial	LADM_COL_V1_6.LADM_Nucleo.COL_Fuente
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno	\N
Operacion_V2_10.Operacion.OP_Terreno	LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial
LADM_COL_V1_6.LADM_Nucleo.COL_AreaValor	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoCcl	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_propietario_predio	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueFuente	\N
LADM_COL_V1_6.LADM_Nucleo.col_responsableFuente	\N
Datos_SNR_V2_10.Datos_SNR.snr_derecho_predio	\N
Operacion_V2_10.Operacion.op_ph_predio	\N
LADM_COL_V1_6.LADM_Nucleo.col_relacionFuente	\N
LADM_COL_V1_6.LADM_Nucleo.COL_CarasLindero	LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado
LADM_COL_V1_6.LADM_Nucleo.COL_DRR	LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_construccion_unidad	\N
Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos.ini_predio_integracion_snr	\N
Operacion_V2_10.Operacion.OP_ServidumbreTransito	LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial
Operacion_V2_10.Operacion.OP_Interesado_Contacto	\N
LADM_COL_V1_6.LADM_Nucleo.col_menosCl	\N
LADM_COL_V1_6.LADM_Nucleo.ExtRedServiciosFisica	\N
LADM_COL_V1_6.LADM_Nucleo.Imagen	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_copropiedad	\N
LADM_COL_V1_6.LADM_Nucleo.COL_VolumenValor	\N
Operacion_V2_10.Operacion.OP_Lindero	LADM_COL_V1_6.LADM_Nucleo.COL_CadenaCarasLimite
Operacion_V2_10.Operacion.op_interesado_contacto	\N
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente	LADM_COL_V1_6.LADM_Nucleo.Oid
Operacion_V2_10.Operacion.OP_Agrupacion_Interesados	LADM_COL_V1_6.LADM_Nucleo.COL_Agrupacion_Interesados
Operacion_V2_10.Operacion.OP_PuntoLevantamiento	LADM_COL_V1_6.LADM_Nucleo.COL_Punto
ISO19107_PLANAS_V1.GM_MultiSurface3D	\N
LADM_COL_V1_6.LADM_Nucleo.col_miembros	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos	\N
Operacion_V2_10.Operacion.OP_Construccion	LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial
LADM_COL_V1_6.LADM_Nucleo.COL_Transformacion	\N
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado	LADM_COL_V1_6.LADM_Nucleo.Oid
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion	\N
Datos_SNR_V2_10.Datos_SNR.snr_fuente_derecho	\N
Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos.ini_predio_integracion_gc	\N
LADM_COL_V1_6.LADM_Nucleo.col_clFuente	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Rural	\N
LADM_COL_V1_6.LADM_Nucleo.COL_CadenaCarasLimite	LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado
LADM_COL_V1_6.LADM_Nucleo.col_baunitComoInteresado	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro	\N
Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos.INI_Predio_Insumos	\N
LADM_COL_V1_6.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion	LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial
Operacion_V2_10.Operacion.OP_PuntoControl	LADM_COL_V1_6.LADM_Nucleo.COL_Punto
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Manzana	\N
LADM_COL_V1_6.LADM_Nucleo.col_topografoFuente	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueUeGrupo	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueNivel	\N
Operacion_V2_10.Operacion.OP_PuntoLindero	LADM_COL_V1_6.LADM_Nucleo.COL_Punto
LADM_COL_V1_6.LADM_Nucleo.Oid	\N
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativa	LADM_COL_V1_6.LADM_Nucleo.COL_Fuente
Operacion_V2_10.Operacion.OP_FuenteEspacial	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacial
LADM_COL_V1_6.LADM_Nucleo.col_masCcl	\N
Operacion_V2_10.Operacion.OP_FuenteAdministrativa	LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativa
INTERLIS.ANYSTRUCTURE	\N
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion	\N
Datos_Gestor_Catastral_V2_10.GC_Direccion	\N
LADM_COL_V1_6.LADM_Nucleo.col_relacionFuenteUespacial	\N
ISO19107_PLANAS_V1.GM_MultiSurface2D	\N
Datos_SNR_V2_10.Datos_SNR.snr_titular_derecho	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Derecho	\N
Datos_SNR_V2_10.Datos_SNR.SNR_Titular	\N
LADM_COL_V1_6.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales	LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro	\N
Operacion_V2_10.Operacion.OP_Restriccion	LADM_COL_V1_6.LADM_Nucleo.COL_DRR
LADM_COL_V1_6.LADM_Nucleo.col_ueJerarquiaGrupo	\N
LADM_COL_V1_6.LADM_Nucleo.col_rrrFuente	\N
LADM_COL_V1_6.LADM_Nucleo.col_rrrInteresado	\N
LADM_COL_V1_6.LADM_Nucleo.COL_EspacioJuridicoRedServicios	LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial
ISO19107_PLANAS_V1.GM_Surface2DListValue	\N
LADM_COL_V1_6.LADM_Nucleo.col_puntoFuente	\N
Operacion_V2_10.Operacion.OP_Interesado	LADM_COL_V1_6.LADM_Nucleo.COL_Interesado
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial	LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Urbano	\N
LADM_COL_V1_6.LADM_Nucleo.col_ueBaunit	\N
Operacion_V2_10.Operacion.op_predio_copropiedad	\N
Operacion_V2_10.Operacion.op_predio_insumos_operacion	\N
LADM_COL_V1_6.LADM_Nucleo.CC_MetodoOperacion	\N
LADM_COL_V1_6.LADM_Nucleo.ExtInteresado	\N
LADM_COL_V1_6.LADM_Nucleo.col_unidadFuente	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_construccion_predio	\N
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_ph_predio	\N
ISO19107_PLANAS_V1.GM_Surface3DListValue	\N
LADM_COL_V1_6.LADM_Nucleo.ExtUnidadEdificacionFisica	\N
LADM_COL_V1_6.LADM_Nucleo.col_masCl	\N
LADM_COL_V1_6.LADM_Nucleo.col_cclFuente	\N
\.


--
-- TOC entry 12701 (class 0 OID 339626)
-- Dependencies: 2267
-- Data for Name: t_ili2db_meta_attrs; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.t_ili2db_meta_attrs (ilielement, attr_name, attr_value) FROM stdin;
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Total_Sotanos	ili2db.dispName	Total de sótanos
LADM_COL_V1_6.LADM_Nucleo.COL_Agrupacion_Interesados.Tipo	ili2db.dispName	Tipo
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Total_Locales	ili2db.dispName	Total de locales
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Codigo_Postal	ili2db.dispName	Código postal
Datos_Gestor_Catastral_V2_10.GC_Direccion	ili2db.dispName	(GC) Dirección
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Numero_Pisos	ili2db.dispName	Número de pisos
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Primer_Apellido	ili2db.dispName	Primer apellido
LADM_COL_V1_6.LADM_Nucleo.COL_VolumenValor.Tipo	ili2db.dispName	Tipo
Operacion_V2_10.Operacion.OP_Construccion.Altura	ili2db.dispName	Altura
Operacion_V2_10.Operacion.OP_Terreno.Avaluo_Terreno	ili2db.dispName	Avalúo de terreno
LADM_COL_V1_6.LADM_Nucleo.COL_Interesado.ext_PID	ili2db.dispName	Ext PID
LADM_COL_V1_6.LADM_Nucleo.COL_EspacioJuridicoRedServicios.Estado	ili2db.dispName	Estado
Operacion_V2_10.Operacion.OP_PuntoLindero.Fotoidentificacion	ili2db.dispName	Fotoidentificación
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Manzana.Geometria	ili2db.dispName	Geometría
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Area_Construida	ili2db.dispName	Área construida
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Calidad	ili2db.dispName	Calidad
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Segundo_Apellido	ili2db.dispName	Segundo apellido
Operacion_V2_10.Operacion.OP_Predio	ili2db.dispName	Predio
Operacion_V2_10.Operacion.OP_Agrupacion_Interesados	ili2db.dispName	Agrupación de Interesados
Operacion_V2_10.Operacion.OP_Construccion.Tipo_Dominio	ili2db.dispName	Tipo de dominio
Operacion_V2_10.Operacion.OP_Interesado.Segundo_Nombre	ili2db.dispName	Segundo nombre
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Construida_Comun	ili2db.dispName	Área total construida común
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Area_Total_Construida_Privada	ili2db.dispName	Área total construida privada
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Planta_Ubicacion	ili2db.dispName	Planta ubicación
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Volumen	ili2db.dispName	Volumen
Datos_SNR_V2_10.Datos_SNR.SNR_Titular	ili2db.dispName	(SNR) Titular
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Domicilio_Notificacion	ili2db.dispName	Domicilio notificación
LADM_COL_V1_6.LADM_Nucleo.Imagen.uri	ili2db.dispName	uri
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Uso	ili2db.dispName	Uso
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Area_Construida	ili2db.dispName	Área construida
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente	ili2db.dispName	Fecha de documento fuente
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno.Geometria	ili2db.dispName	Geometría
Operacion_V2_10.Operacion.OP_Derecho.Tipo	ili2db.dispName	Tipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Manzana.Codigo_Anterior	ili2db.dispName	Código anterior
Operacion_V2_10.Operacion.OP_Predio.Condicion_Predio	ili2db.dispName	Condición del predio
Operacion_V2_10.Operacion.OP_Interesado.Tipo_Documento	ili2db.dispName	Tipo de documento
Operacion_V2_10.Operacion.OP_PuntoControl.PuntoTipo	ili2db.dispName	Tipo de punto
LADM_COL_V1_6.LADM_Nucleo.CC_MetodoOperacion.Dimensiones_Origen	ili2db.dispName	Dimensiones origen
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos.Numero_Documento	ili2db.dispName	Número de documento
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Geometria	ili2db.dispName	Geometría
Operacion_V2_10.Operacion.OP_Terreno	ili2db.dispName	Terreno
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Codigo_Terreno	ili2db.dispName	Código terreno
LADM_COL_V1_6.LADM_Nucleo.COL_Nivel.Tipo	ili2db.dispName	Tipo
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.PuntoTipo	ili2db.dispName	Tipo de punto
Operacion_V2_10.Operacion.OP_Predio.Numero_Predial_Anterior	ili2db.dispName	Número predial anterior
Operacion_V2_10.Operacion.OP_Terreno.Area_Terreno	ili2db.dispName	Área de terreno
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Area_Total_Terreno_Comun	ili2db.dispName	Área total de terreno común
Datos_Gestor_Catastral_V2_10.GC_Direccion.Geometria_Referencia	ili2db.dispName	Geometría de referencia
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Fecha_Alerta	ili2db.dispName	Fecha de alerta
Operacion_V2_10.Operacion.OP_Lindero	ili2db.dispName	Lindero
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Banios	ili2db.dispName	Total de baños
Operacion_V2_10.Operacion.OP_PuntoLindero.Exactitud_Horizontal	ili2db.dispName	Exactitud horizontal
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Cabida_Linderos	ili2db.dispName	Cabida y linderos
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Puntaje	ili2db.dispName	Puntaje
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Autoriza_Notificacion_Correo	ili2db.dispName	Autoriza notificación correo
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Localizacion	ili2db.dispName	Localización
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.Posicion_Interpolacion	ili2db.dispName	Posición interpolación
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Tipo_Dominio	ili2db.dispName	Tipo de dominio
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Direccion_Residencia	ili2db.dispName	Dirección de residencia
Operacion_V2_10.Operacion.OP_PuntoLindero.ID_Punto_Lindero	ili2db.dispName	ID del punto de lindero
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Area_Privada	ili2db.dispName	Área privada
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Numero_Mezanines	ili2db.dispName	Número de mezanines
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno	ili2db.dispName	(GC) Terreno
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Valor_Via_Generadora	ili2db.dispName	Valor de vía generadora
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Terreno_Comun	ili2db.dispName	Área total de terreno común
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Barrio.Codigo_Sector	ili2db.dispName	Código sector
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion	ili2db.dispName	Dirección
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Tipo_Planta	ili2db.dispName	Tipo de planta
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente.Tipo_Principal	ili2db.dispName	Tipo principal
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Matricula_Inmobiliaria	ili2db.dispName	Matrícula inmobiliaria
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Fecha_Aceptacion	ili2db.dispName	Fecha de aceptación
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho.Ciudad_Emisora	ili2db.dispName	Ciudad emisora
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno.Manzana_Vereda_Codigo	ili2db.dispName	Código de manzana vereda
Operacion_V2_10.Operacion.OP_Terreno.Manzana_Vereda_Codigo	ili2db.dispName	Código de manzana vereda
LADM_COL_V1_6.LADM_Nucleo.CC_MetodoOperacion.Formula	ili2db.dispName	Fórmula
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Fecha_Datos	ili2db.dispName	Fecha de los datos
LADM_COL_V1_6.LADM_Nucleo.COL_CarasLindero.Localizacion_Textual	ili2db.dispName	Localización textual
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Numero_Documento	ili2db.dispName	Número de documento
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Corregimiento	ili2db.dispName	Corregimiento
LADM_COL_V1_6.LADM_Nucleo.COL_EspacioJuridicoRedServicios.Tipo	ili2db.dispName	Tipo
Operacion_V2_10.Operacion.OP_Construccion.Numero_Mezanines	ili2db.dispName	Número de mezanines
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Area_Total_Construida_Comun	ili2db.dispName	Área total construida común
Operacion_V2_10.Operacion.OP_PuntoLevantamiento	ili2db.dispName	Punto Levantamiento
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Total_Banios	ili2db.dispName	Total de baños
LADM_COL_V1_6.LADM_Nucleo.ExtInteresado.Firma	ili2db.dispName	Firma
Operacion_V2_10.Operacion.OP_Interesado.Razon_Social	ili2db.dispName	Razón social
Operacion_V2_10.Operacion.OP_Construccion	ili2db.dispName	Construcción
Operacion_V2_10.Operacion.OP_Interesado.Grupo_Etnico	ili2db.dispName	Grupo étnico
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Primer_Apellido	ili2db.dispName	Primer apellido
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacial.Descripcion	ili2db.dispName	Descripción
Operacion_V2_10.Operacion.OP_Interesado.Primer_Nombre	ili2db.dispName	Primer nombre
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Tipo_Documento	ili2db.dispName	Tipo de documento
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Area_Total_Terreno	ili2db.dispName	Área total de terreno
LADM_COL_V1_6.LADM_Nucleo.COL_Interesado.Nombre	ili2db.dispName	Nombre
Operacion_V2_10.Operacion.OP_Interesado.Segundo_Apellido	ili2db.dispName	Segundo apellido
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Tipo_Construccion	ili2db.dispName	Tipo de construcción
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Torre_No	ili2db.dispName	Torre número
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro	ili2db.dispName	(GC) Perímetro
LADM_COL_V1_6.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Nivel_Jerarquico	ili2db.dispName	Nivel jerárquico
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Tipo_Persona	ili2db.dispName	Tipo de persona
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Fecha_Grabacion	ili2db.dispName	Fecha de grabación
LADM_COL_V1_6.LADM_Nucleo.ExtInteresado.Ext_Direccion_ID	ili2db.dispName	Ext dirección id
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho.Tipo_Documento	ili2db.dispName	Tipo de documento
Operacion_V2_10.Operacion.OP_PuntoControl.Tipo_Punto_Control	ili2db.dispName	Tipo de punto de control
Operacion_V2_10.Operacion.OP_Predio.Tiene_FMI	ili2db.dispName	Tiene FMI
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Anio_Construccion	ili2db.dispName	Año de construcción
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Digito_Verificacion	ili2db.dispName	Dígito de verificación
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Municipio	ili2db.dispName	Código del municipio
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Segundo_Nombre	ili2db.dispName	Segundo nombre
Operacion_V2_10.Operacion.OP_Terreno.Geometria	ili2db.dispName	Geometría
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Departamento	ili2db.dispName	Departamento
Operacion_V2_10.Operacion.OP_Predio.Avaluo_Catastral	ili2db.dispName	Avalúo catastral
Operacion_V2_10.Operacion.OP_Terreno.Numero_Subterraneos	ili2db.dispName	Número de subterráneos
Operacion_V2_10.Operacion.OP_PuntoControl	ili2db.dispName	Punto Control
LADM_COL_V1_6.LADM_Nucleo.COL_DRR.Uso_Efectivo	ili2db.dispName	Uso efectivo
LADM_COL_V1_6.LADM_Nucleo.Fraccion.Numerador	ili2db.dispName	Numerador
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID	ili2db.dispName	Ext archivo id
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos.Fecha_Documento	ili2db.dispName	Fecha de documento
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Nombres	ili2db.dispName	Nombres
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda.Nombre	ili2db.dispName	Nombre
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Area_Total_Construida	ili2db.dispName	Área total construida
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Etiqueta	ili2db.dispName	Etiqueta
LADM_COL_V1_6.LADM_Nucleo.COL_EspacioJuridicoRedServicios.ext_ID_Red_Fisica	ili2db.dispName	Ext id red física
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio	ili2db.dispName	Datos PH Condominio
LADM_COL_V1_6.LADM_Nucleo.ExtRedServiciosFisica.Ext_Interesado_Administrador_ID	ili2db.dispName	Ext interesado administrador id
LADM_COL_V1_6.LADM_Nucleo.COL_BAUnit.Nombre	ili2db.dispName	Nombre
Operacion_V2_10.Operacion.OP_Predio.Codigo_ORIP	ili2db.dispName	Código ORIP
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Dimension	ili2db.dispName	Dimensión
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativa.Tipo	ili2db.dispName	Tipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Urbano.Geometria	ili2db.dispName	Geometría
LADM_COL_V1_6.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion.Tipo	ili2db.dispName	Tipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion	ili2db.dispName	(GC) Comisiones Unidad Construcción
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Razon_Social	ili2db.dispName	Razón social
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Uso	ili2db.dispName	Uso
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Avaluo_Construccion	ili2db.dispName	Avalúo de la construcción
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Area_Construida	ili2db.dispName	Área construida
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Vereda	ili2db.dispName	Vereda
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Anio_Construccion	ili2db.dispName	Año de construcción
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Identificador	ili2db.dispName	Identificador
Operacion_V2_10.Operacion.OP_Restriccion	ili2db.dispName	Restricción
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Datos	ili2db.dispName	Datos
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Unidades_Sotano	ili2db.dispName	Total de unidades de sótano
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Telefono1	ili2db.dispName	Teléfono 1
Operacion_V2_10.Operacion.OP_Interesado.Primer_Apellido	ili2db.dispName	Primer apellido
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Telefono2	ili2db.dispName	Teléfono 2
Operacion_V2_10.Operacion.OP_Predio.Numero_Predial	ili2db.dispName	Número predial
LADM_COL_V1_6.LADM_Nucleo.COL_DRR.Comprobacion_Comparte	ili2db.dispName	Comprobación si comparte
LADM_COL_V1_6.LADM_Nucleo.Oid.Local_Id	ili2db.dispName	Local ID
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Tipo_Construccion	ili2db.dispName	Tipo de construcción
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Manzana.Codigo	ili2db.dispName	Código
Datos_Gestor_Catastral_V2_10.GC_Direccion.Principal	ili2db.dispName	Principal
LADM_COL_V1_6.LADM_Nucleo.CC_MetodoOperacion.Ddimensiones_Objetivo	ili2db.dispName	Ddimensiones objetivo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Planta	ili2db.dispName	Planta
LADM_COL_V1_6.LADM_Nucleo.COL_VolumenValor.Volumen_Medicion	ili2db.dispName	Volumen medición
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro.Geometria	ili2db.dispName	Geometría
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho.Fecha_Documento	ili2db.dispName	Fecha del documento
LADM_COL_V1_6.LADM_Nucleo.COL_CadenaCarasLimite.Localizacion_Textual	ili2db.dispName	Localización textual
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	ili2db.dispName	Versión de comienzo de vida útil
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Sotanos	ili2db.dispName	Total de sótanos
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda.Codigo_Anterior	ili2db.dispName	Código anterior
LADM_COL_V1_6.LADM_Nucleo.ExtRedServiciosFisica.Orientada	ili2db.dispName	Orientada
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda.Codigo_Sector	ili2db.dispName	Código del sector
Operacion_V2_10.Operacion.OP_Construccion.Numero_Semisotanos	ili2db.dispName	Número de semisótanos
Operacion_V2_10.Operacion.OP_Predio.Municipio	ili2db.dispName	Municipio
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Unidades_Privadas	ili2db.dispName	Total de unidades privadas
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Codigo_Terreno	ili2db.dispName	Código de terreno
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Total_Unidades_Privadas	ili2db.dispName	Total de unidades privadas
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital	ili2db.dispName	Área terreno digital
Operacion_V2_10.Operacion.OP_Interesado_Contacto	ili2db.dispName	Interesado Contacto
Operacion_V2_10.Operacion.OP_Predio.Matricula_Inmobiliaria	ili2db.dispName	Matrícula inmobiliaria
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Tipo_Documento	ili2db.dispName	Tipo de documento
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario	ili2db.dispName	(GC) Propietario
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos.Tipo_Documento	ili2db.dispName	Tipo de documento
Operacion_V2_10.Operacion.OP_FuenteAdministrativa.Tipo	ili2db.dispName	Tipo
LADM_COL_V1_6.LADM_Nucleo.ExtInteresado.Fotografia	ili2db.dispName	Fotografía
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Extraccion	ili2db.dispName	Extracción
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Tipo_Dominio	ili2db.dispName	Tipo de dominio
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio	ili2db.dispName	(GC) Datos Propiedad Horizontal Condominio
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda.Codigo	ili2db.dispName	Código
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Procedencia	ili2db.dispName	Procedencia
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion	ili2db.dispName	(GC) Unidad Construcción
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Local_Id	ili2db.dispName	Local ID
LADM_COL_V1_6.LADM_Nucleo.COL_RelacionNecesariaBAUnits.Relacion	ili2db.dispName	Relación
Operacion_V2_10.Operacion.OP_FuenteAdministrativa	ili2db.dispName	Fuente Administrativa
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacial.Nombre	ili2db.dispName	Nombre
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Altura	ili2db.dispName	Altura
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Pisos_Torre	ili2db.dispName	Total pisos de torre
Datos_SNR_V2_10.Datos_SNR.SNR_Derecho.Codigo_Naturaleza_Juridica	ili2db.dispName	Código naturaleza jurídica
LADM_COL_V1_6.LADM_Nucleo.COL_CadenaCarasLimite.Geometria	ili2db.dispName	Geometría
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Numero_Predial_Nuevo_en_FMI	ili2db.dispName	Número predial nuevo en FMI
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Departamento	ili2db.dispName	Código del departamento
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Geometria	ili2db.dispName	Geometría
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Torre_No	ili2db.dispName	Torre número
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Barrio.Codigo	ili2db.dispName	Código
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Predio	ili2db.dispName	Tipo de predio
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica	ili2db.dispName	Área terreno alfanumérica
Operacion_V2_10.Operacion.OP_PuntoLindero.Acuerdo	ili2db.dispName	Acuerdo
Operacion_V2_10.Operacion.OP_PuntoLindero.Ubicacion_Punto	ili2db.dispName	Ubicación del punto
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Urbano	ili2db.dispName	(GC) Sector Urbano
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Rural.Codigo	ili2db.dispName	Código
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Clase_Via_Principal	ili2db.dispName	Clase de vía principal
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno.Numero_Subterraneos	ili2db.dispName	Número de subterráneos
Operacion_V2_10.Operacion.OP_Interesado.Tipo	ili2db.dispName	Tipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Locales	ili2db.dispName	Total de locales
LADM_COL_V1_6.LADM_Nucleo.COL_BAUnit.Tipo	ili2db.dispName	Tipo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial	ili2db.dispName	Número predial
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho	ili2db.dispName	(SNR) Fuente Derecho
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Espacio_De_Nombres	ili2db.dispName	Espacio de nombres
Operacion_V2_10.Operacion.OP_Derecho	ili2db.dispName	Derecho
LADM_COL_V1_6.LADM_Nucleo.COL_Transformacion.Localizacion_Transformada	ili2db.dispName	Localización transformada
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Destinacion_Economica	ili2db.dispName	Destinación económica
Datos_SNR_V2_10.Datos_SNR.SNR_Derecho	ili2db.dispName	(SNR) Derecho
Datos_Gestor_Catastral_V2_10.GC_Direccion.Valor	ili2db.dispName	Valor
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda	ili2db.dispName	(GC) Vereda
Operacion_V2_10.Operacion.OP_PuntoLevantamiento.Exactitud_Vertical	ili2db.dispName	Exactitud vertical
Operacion_V2_10.Operacion.OP_ServidumbreTransito.Area_Servidumbre	ili2db.dispName	Área de la servidumbre
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Numero_Semisotanos	ili2db.dispName	Número de semisótanos
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos.Archivo	ili2db.dispName	Archivo
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado	ili2db.dispName	Transformación y resultado
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Nombre	ili2db.dispName	Código nombre
Operacion_V2_10.Operacion.OP_PuntoLindero.PuntoTipo	ili2db.dispName	Tipo de punto
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Circulo_Registral	ili2db.dispName	Círculo registral
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Nombre_Predio	ili2db.dispName	Nombre del predio
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Habitaciones	ili2db.dispName	Total de habitaciones
Operacion_V2_10.Operacion.OP_Construccion.Codigo_Edificacion	ili2db.dispName	Código de edificación
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Fecha_Datos	ili2db.dispName	Fecha de datos
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial_Anterior	ili2db.dispName	Número predial anterior
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Etiqueta	ili2db.dispName	Etiqueta
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos	ili2db.dispName	(SNR) Fuente Cabida Linderos
LADM_COL_V1_6.LADM_Nucleo.COL_CarasLindero.Geometria	ili2db.dispName	Geometría
LADM_COL_V1_6.LADM_Nucleo.ExtInteresado.Nombre	ili2db.dispName	Nombre
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Identificador	ili2db.dispName	Identificador
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Numero_Predial_Anterior_en_FMI	ili2db.dispName	Número predial anterior en FMI
LADM_COL_V1_6.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Etiqueta	ili2db.dispName	Etiqueta
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Segundo_Apellido	ili2db.dispName	Segundo apellido
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Catastro	ili2db.dispName	Tipo de catastro
Operacion_V2_10.Operacion.OP_PuntoLindero.Exactitud_Vertical	ili2db.dispName	Exactitud vertical
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad	ili2db.dispName	Estado de disponibilidad
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Construida	ili2db.dispName	Área total construida
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Estado_Alerta	ili2db.dispName	Estado alerta
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Rural	ili2db.dispName	(GC) Sector Rural
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Total_Unidades_Sotanos	ili2db.dispName	Total de únidades de sótanos
LADM_COL_V1_6.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion.Ext_Unidad_Edificacion_Fisica_ID	ili2db.dispName	Ext unidad edificación física id
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Predio	ili2db.dispName	Sector del predio
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Construccion	ili2db.dispName	(GC) Comisiones Construcción
Operacion_V2_10.Operacion.OP_Construccion.Numero_Sotanos	ili2db.dispName	Número de sótanos
LADM_COL_V1_6.LADM_Nucleo.ExtUnidadEdificacionFisica.Ext_Direccion_ID	ili2db.dispName	Ext dirección id
Operacion_V2_10.Operacion.OP_UnidadConstruccion	ili2db.dispName	Unidad de Construcción
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Geometria	ili2db.dispName	Geometría
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Identificador	ili2db.dispName	Identificador
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Razon_Social	ili2db.dispName	Razón social
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Correo_Electronico	ili2db.dispName	Correo electrónico
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID	ili2db.dispName	Ext dirección id
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Geometria	ili2db.dispName	Geometría
Operacion_V2_10.Operacion.OP_Restriccion.Tipo	ili2db.dispName	Tipo
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Area_Privada_Construida	ili2db.dispName	Área privada construida
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Direcciones	ili2db.dispName	Direcciones
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Area	ili2db.dispName	Área
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Area_Total_Terreno_Privada	ili2db.dispName	Área total de terreno privada
Operacion_V2_10.Operacion.OP_PuntoControl.Exactitud_Vertical	ili2db.dispName	Exactitud vertical
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativa.Numero_Fuente	ili2db.dispName	Número de fuente
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Terreno.Geometria	ili2db.dispName	Geometría
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro	ili2db.dispName	(SNR) Predio Registro
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Terreno_Privada	ili2db.dispName	Área total de terreno privada
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie	ili2db.dispName	Relación superficie
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Tipo_Construccion	ili2db.dispName	Tipo de construcción
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Terreno	ili2db.dispName	(GC) Comisiones Terreno
LADM_COL_V1_6.LADM_Nucleo.Oid.Espacio_De_Nombres	ili2db.dispName	Espacio de nombres
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Barrio	ili2db.dispName	(GC) Barrio
Operacion_V2_10.Operacion.OP_Construccion.Numero_Pisos	ili2db.dispName	Número de pisos
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Barrio.Nombre	ili2db.dispName	Nombre
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro	ili2db.dispName	(GC) Predio Catastro
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacial.Metadato	ili2db.dispName	Metadato
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro.Nombre_Geografico	ili2db.dispName	Nombre geográfico
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Rural.Geometria	ili2db.dispName	Geometría
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos.Ciudad_Emisora	ili2db.dispName	Ciudad emisora
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Letra_Via_Principal	ili2db.dispName	Letra vía principal
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.Geometria	ili2db.dispName	Geometría
LADM_COL_V1_6.LADM_Nucleo.COL_DRR.Descripcion	ili2db.dispName	Descripción
Operacion_V2_10.Operacion.OP_PuntoLevantamiento.PuntoTipo	ili2db.dispName	Tipo de punto
LADM_COL_V1_6.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Nombre	ili2db.dispName	Nombre
Operacion_V2_10.Operacion.OP_FuenteEspacial	ili2db.dispName	Fuente Espacial
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Codigo_ORIP	ili2db.dispName	Código ORIP
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Tipo_Dominio	ili2db.dispName	Tipo de dominio
LADM_COL_V1_6.LADM_Nucleo.COL_Nivel.Registro_Tipo	ili2db.dispName	Tipo de registro
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo.Fecha_Entrega	ili2db.dispName	Fecha de entrega
Operacion_V2_10.Operacion.OP_Construccion.Area_Construccion	ili2db.dispName	Área de construcción
LADM_COL_V1_6.LADM_Nucleo.ExtInteresado.Huella_Dactilar	ili2db.dispName	Huella dactilar
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Numero_Predio	ili2db.dispName	Número del predio
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Complemento	ili2db.dispName	Complemento
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Tipo_Unidad_Construccion	ili2db.dispName	Tipo de unidad de construcción
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Geometria	ili2db.dispName	Geometría
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Sistema_Procedencia_Datos	ili2db.dispName	Sistema procedencia de los datos
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Barrio.Geometria	ili2db.dispName	Geometría
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Codigo_Edificacion	ili2db.dispName	Código de edificación
Datos_SNR_V2_10.Datos_SNR.SNR_Titular.Numero_Documento	ili2db.dispName	Número de documento
Operacion_V2_10.Operacion.OP_Predio.Departamento	ili2db.dispName	Departamento
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho.Numero_Documento	ili2db.dispName	Número de documento
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio.Total_Pisos_Torre	ili2db.dispName	Total pisos de torre
Operacion_V2_10.Operacion.OP_PuntoLevantamiento.Exactitud_Horizontal	ili2db.dispName	Exactitud horizontal
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativa.Observacion	ili2db.dispName	Observación
Operacion_V2_10.Operacion.OP_Interesado	ili2db.dispName	Interesado
Operacion_V2_10.Operacion.OP_PuntoControl.Exactitud_Horizontal	ili2db.dispName	Exactitud horizontal
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Sector_Ciudad	ili2db.dispName	Sector de la ciudad
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Terreno	ili2db.dispName	Área total de terreno
Operacion_V2_10.Operacion.OP_PuntoControl.ID_Punto_Control	ili2db.dispName	ID del punto de control
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Matricula_Inmobiliaria_Catastro	ili2db.dispName	Matrícula inmobiliaria catastro
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Total_Habitaciones	ili2db.dispName	Total de habitaciones
LADM_COL_V1_6.LADM_Nucleo.COL_Nivel.Estructura	ili2db.dispName	Estructura
LADM_COL_V1_6.LADM_Nucleo.COL_RelacionNecesariaUnidadesEspaciales.Relacion	ili2db.dispName	Relación
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario.Primer_Nombre	ili2db.dispName	Primer nombre
LADM_COL_V1_6.LADM_Nucleo.COL_Nivel.Nombre	ili2db.dispName	Nombre
Operacion_V2_10.Operacion.OP_Interesado.Sexo	ili2db.dispName	Sexo
Operacion_V2_10.Operacion.OP_ServidumbreTransito	ili2db.dispName	Servidumbre de Tránsito
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Tipo_Direccion	ili2db.dispName	Tipo de dirección
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Manzana.Codigo_Barrio	ili2db.dispName	Código de barrio
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Numero_Sotanos	ili2db.dispName	Número de sótanos
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho.Ente_Emisor	ili2db.dispName	Ente emisor
Operacion_V2_10.Operacion.OP_Construccion.Tipo_Construccion	ili2db.dispName	Tipo de construcción
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	ili2db.dispName	Versión de fin de vida útil
Operacion_V2_10.Operacion.OP_Predio.Id_Operacion	ili2db.dispName	Identificador único de operación
Operacion_V2_10.Operacion.OP_PuntoLevantamiento.Tipo_Punto_Levantamiento	ili2db.dispName	Tipo de punto de levantamiento
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Urbano.Codigo	ili2db.dispName	Código
Operacion_V2_10.Operacion.OP_PuntoLevantamiento.ID_Punto_Levantamiento	ili2db.dispName	ID del punto de levantamiento
Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos.INI_Predio_Insumos	ili2db.dispName	(Integración Insumos) Predio Insumos
Operacion_V2_10.Operacion.OP_Construccion.Identificador	ili2db.dispName	Identificador
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Observaciones	ili2db.dispName	Observaciones
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro.Tipo_Avaluo	ili2db.dispName	Tipo de avalúo
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Entidad_Emisora_Alerta	ili2db.dispName	Entidad emisora de la alerta
Operacion_V2_10.Operacion.OP_Predio.Direccion	ili2db.dispName	Dirección
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Valor_Via_Principal	ili2db.dispName	Valor vía principal
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Construida_Privada	ili2db.dispName	Área total construida privada
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Etiqueta	ili2db.dispName	Etiqueta
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Es_Direccion_Principal	ili2db.dispName	Es dirección principal
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro.Condicion_Predio	ili2db.dispName	Condición del predio
Operacion_V2_10.Operacion.OP_UnidadConstruccion.Total_Pisos	ili2db.dispName	Total de pisos
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo	ili2db.dispName	Archivo fuente
LADM_COL_V1_6.LADM_Nucleo.COL_Punto.MetodoProduccion	ili2db.dispName	Método de producción
Operacion_V2_10.Operacion.OP_Lindero.Longitud	ili2db.dispName	Longitud
LADM_COL_V1_6.LADM_Nucleo.COL_AreaValor.areaSize	ili2db.dispName	Área
LADM_COL_V1_6.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales.Punto_Referencia	ili2db.dispName	Punto de referencia
Operacion_V2_10.Operacion.OP_PuntoLevantamiento.Fotoidentificacion	ili2db.dispName	Fotoidentificación
Datos_SNR_V2_10.Datos_SNR.SNR_Derecho.Calidad_Derecho_Registro	ili2db.dispName	Calidad derecho registro
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacial.Tipo	ili2db.dispName	Tipo
Operacion_V2_10.Operacion.OP_Interesado_Contacto.Municipio	ili2db.dispName	Municipio
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion.Letra_Via_Generadora	ili2db.dispName	Letra de vía generadora
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro.Matricula_Inmobiliaria_Matriz	ili2db.dispName	Matrícula inmobiliaria matriz
Operacion_V2_10.Operacion.OP_Interesado.Documento_Identidad	ili2db.dispName	Documento de identidad
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion	ili2db.dispName	(GC) Construcción
Operacion_V2_10.Operacion.OP_FuenteAdministrativa.Ente_Emisor	ili2db.dispName	Ente emisor
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Manzana	ili2db.dispName	(GC) Manzana
Operacion_V2_10.Operacion.OP_PuntoLindero	ili2db.dispName	Punto Lindero
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos.Ente_Emisor	ili2db.dispName	Ente emisor
LADM_COL_V1_6.LADM_Nucleo.COL_Transformacion.Transformacion	ili2db.dispName	Transformación
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Pisos	ili2db.dispName	Total de pisos
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda.Geometria	ili2db.dispName	Geometría
LADM_COL_V1_6.LADM_Nucleo.COL_AreaValor.type	ili2db.dispName	Tipo
LADM_COL_V1_6.LADM_Nucleo.Fraccion.Denominador	ili2db.dispName	Denominador
Operacion_V2_10.Operacion.OP_Construccion.Avaluo_Construccion	ili2db.dispName	Ávaluo de construcción
\.


--
-- TOC entry 12702 (class 0 OID 339632)
-- Dependencies: 2268
-- Data for Name: t_ili2db_model; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.t_ili2db_model (filename, iliversion, modelname, content, importdate) FROM stdin;
Operacion_V2_10.ili	2.3	Operacion_V2_10{ Datos_Integracion_Insumos_V2_10 ISO19107_PLANAS_V1 LADM_COL_V1_6}	INTERLIS 2.3;\n\n/** ISO 19152 LADM country profile COL modeled with INTERLIS 2.\n * \n * -----------------------------------------------------------\n * revision history\n * -----------------------------------------------------------\n * \n * 10.05.2016/mg: EJEMPLO INTERLIS POR OFERTAS\n * 16.06.2016/mg: Taller IGAC/SNR\n * 23.08.2016/mg: Relaciones\n * 15.09.2016/mg: Comentarios Modelo\n * 20.11.2016/aa: Topic Ficha\n * 25.11.2016/aa: Ajustes FichaPredio\n * 02.12.2016/ss: Nuevas clases, atributos y tipos\n * 15.12.2016/lj: Ajuste tipos (IGAC/SNR), BAUnit GM_surface\n * 31.03.2017/fm: Simplificación de herencia\n * 25.05.2017/fm: Se elimina la relacion HipotecaDerecho, se elimina la clase InteresadoBAUnit, se elimina marca abstract en las clases derivadas de RRR\n * 26.05.2017/fm: Se cambian las clases terreno servidumbre de paso y construccion al paquete de unidades espaciales. Se acorta el nombre del Modelo. ajuste al diseño del diagrama de clases. Se elimina InteresadoNacion\n * 09.06.2017/vm: Referido al modelo LADM traducido al español\n * 09.06.2017/vm: cambio de version a 2.1.1, incluye cambios por LADM en español y de  nombres de atributo por no seguir las convenciones adoptadas.\n * 15.06.2017/fm: cambio de version a 2.1.2, se quita el atributo geometría de la clase predio. se reemplaza el atributo OID por los atributos atributos namespace y localId. Se añaden atributos folio matriz y segregados al predio. se elimina el dominio transaccion_registral_tipo\n * 20.06.2017/fm: Ajuste a nombres de las clases y atributos LA_\n * 04.07.2017/sr: Ajuste de nombres de clases y atributos, creacion de relaciones, ajuste subdominios\n * 04.07.2017/fm: Se unifican los modelos LADM_ES y Catastro_COL, se eliminan las clases que extienden de responsabilidad, restriccion, derecho, hipoteca, fuente_administrativa y fuente espacial. eliminan atributos opcionales no usados de la clase hipoteca\n * 11.07.2017/fm: se adiciona el atributo poligono_creado\n * 12.07.2017/fm: se adiciona el atributo Estado_Nupre en la clase predio\n * 17.07.2017/fm: poligono creado debe ser obligatorio para la clase terreno.\n * 28.09.2017/fm : Cambio del nombre en la clase alerta por publicidad, Publicidad Extiende de objeto versionado, se elimita atributo fecha de vigencia. Ajuste al atributo plantacion comercial de la clase terreno. Se extraen los atributos de la clase predio e interesados a los modelos extendidos de ficha y registro. version 2.2.0\n * 20.10.2017/ag : Ajustes a atributos de la clase terreno, cambio a dominio multivalorado, se crean dominios, col_servidumbre, col_afectacion, col_explotacion, col_territorioAgricula, col_cuerpoAgua, se elimina la obligatoriedad del rol responsable en las relaciones responsableFuente y topografoFuente\n * 28.10.2017/gc : Soporte de geometrías multi-parte para LA_UnidadEspacial (y las clases que la extienden) y Terreno.\n * 02.11.2017/ : Cambio del nombre del modelo de Catastro_COL_ES a Catastro_Registro_Nucleo\n * 07.11.2017/fm: Cambio de nombre a la clase CadenaCarasLindero a CadenaCarasLimite \n * 14.11.2017/fm : taducción del dominio COL_BuildingUnitTipo\n * 14.12.2017/fm : definicion de extends entre topics catastro registro nucleo y Ladm_nucleo\n * 30.01.2018/fm : Cambio del tipo de dato del atributo Ext_Direccion de la clase Unidad Espacial a ExtDireccion; atributo ext_PID de la calse LA_Interesado cambia de OID a ExtInteresado; Cambio de cardinalidad en relacion miembros entre LA_Interesado y LA_Agrupacion_Interesados de 0..1 a 0..*\n * 19.02.2018/fm : Cambio en longitud de atributo DocumentoIdentidad de 10 a 12 posiciones\n * 17.07.2018/fm : cambio en cardinalidad asociación ConstruccionUnidadConstruccion de 1..* a 0..*; ampliación del tamaño para campo de nombre en Interesado Natural; se incluyen los valores nuip, cedula militar, registro civil, cedula militar, secuencial SRN y secuencial IGAC al dominio COL_InteresadoDocumentoTipo\n * 30.07.2018/fm : Cambio obligatoriedad atributo area_registral de clase terreno de 1 a 0..1\n * 31.07.2018/fm: Creación de la clase COL_Interesado integrando los atributos de interesado natural e interesado jurídico; se agrega area en la clase construcción; se adiciona valor Carta_Venta al dominio COL_FuenteAdministrativaTipo; inclusion de atributo nombre en la clase COL_FuenteAdministrativa\n * 10.08.2018/fm: Eliminado clase Interesado Natural e Interesado Juridico\n * 28.08.2018/fm: Ajuste a cardinalidad en la composición predio_copropiedad, se elimina el requerido.\n * 28.08.2018/fm-at: Se incluye el tipo de predio conforme a la resolucion 070 de 2011; Se elimina el atributo tipo_construccion de la clase Unidad_Construcción ya que el dominio hace referencia a tipos de predios y no a tipos de construcciones\n * 10.09.2018/fm-at: Ajuste a los tipos de Predio conforme a la resolucion 070\n * 21.09.2018/at: Se agrega el valor "Hipoteca" al dominio COL_RestriccionTipo, se ajusta la longitud del atributo Codigo_Registral en las clases especializadas de LA_RRR de 3 a 4 caracteres\n * 25.09.2018/at: Se ajusta la longitud del atributo Codigo_Registral en las clases especializadas de LA_RRR a 5 caracteres de acuerdo a la Resolución 3973 de 2018\n * 18.10.2018/at: Se agregan los atributos p_Espacio_De_Nombres y p_Local_Id a la clase Publicidad\n * 29.10.2018/fm: se amplia el tamaño de campo FMI en la clase predio para almacenar cadenas como 'LIBRO 2 TOMO 1/961 FOLIO 37/46 PARTIDA N 58'\n * -----------------------------------------------------------\n * \n * (c) IGAC y SNR con apoyo de la Cooperacion Suiza\n * \n * -----------------------------------------------------------\n */\nCONTRACTED MODEL Operacion_V2_10 (es)\nAT "http://www.proadmintierra.info/"\nVERSION "V2.2.1"  // 2018-02-19 // =\n  IMPORTS ISO19107_PLANAS_V1,LADM_COL_V1_6,Datos_Integracion_Insumos_V2_10;\n\n  DOMAIN\n\n    /** Valores para indicar el nivel de acuerdo\n     */\n    OP_AcuerdoTipo = (\n      /** Existe un acuerdo sobre la posición del punto\n       */\n      !!@ ili2db.dispName = "Acuerdo"\n      Acuerdo,\n      /** Existe un desacuerdo sobre la posición del punto\n       */\n      !!@ ili2db.dispName = "Desacuerdo"\n      Desacuerdo\n    );\n\n    /** Valores para indicar el tipo de condición de predio\n     */\n    OP_CondicionPredioTipo = (\n      !!@ ili2db.dispName = "No propiedad horizontal"\n      NPH,\n      !!@ ili2db.dispName = "Propiedad horizontal"\n      PH(\n        !!@ ili2db.dispName = "(Propiedad horizontal) Matriz"\n        Matriz,\n        !!@ ili2db.dispName = "(Propiedad horizontal) Unidad Predial"\n        Unidad_Predial\n      ),\n      !!@ ili2db.dispName = "Condominio"\n      Condominio(\n        !!@ ili2db.dispName = "(Condominio) Matriz"\n        Matriz,\n        !!@ ili2db.dispName = "(Condominio) Unidad predial"\n        Unidad_Predial\n      ),\n      !!@ ili2db.dispName = "Mejora"\n      Mejora(\n        !!@ ili2db.dispName = "(Mejora) Propiedad horizontal"\n        PH,\n        !!@ ili2db.dispName = "(Mejora) No propiedad horizontal"\n        NPH\n      ),\n      !!@ ili2db.dispName = "Parque cementerio"\n      Parque_Cementerio(\n        !!@ ili2db.dispName = "(Parque cementerio) Matriz"\n        Matriz,\n        !!@ ili2db.dispName = "(Parque Cementerio) Unidad predial"\n        Unidad_Predial\n      ),\n      !!@ ili2db.dispName = "Vía"\n      Via,\n      !!@ ili2db.dispName = "Bien de uso público"\n      Bien_Uso_Publico\n    );\n\n    OP_ConstruccionPlantaTipo = (\n      !!@ ili2db.dispName = "Piso"\n      Piso,\n      !!@ ili2db.dispName = "Mezanine"\n      Mezanine,\n      !!@ ili2db.dispName = "Sótano"\n      Sotano,\n      !!@ ili2db.dispName = "Semisótano"\n      Semisotano,\n      !!@ ili2db.dispName = "Subterráneo"\n      Subterraneo\n    );\n\n    OP_ConstruccionTipo = (\n      !!@ ili2db.dispName = "Convencional"\n      Convencional,\n      !!@ ili2db.dispName = "No convencional"\n      No_Convencional\n    );\n\n    OP_DerechoTipo = (\n      /** Derecho de dominio o propiedad\n       */\n      !!@ ili2db.dispName = "Dominio"\n      Dominio,\n      !!@ ili2db.dispName = "Ocupación"\n      Ocupacion,\n      !!@ ili2db.dispName = "Posesión"\n      Posesion,\n      !!@ ili2db.dispName = "Derecho de propiedad colectiva"\n      Derecho_Propiedad_Colectiva,\n      !!@ ili2db.dispName = "Nuda propiedad"\n      Nuda_Propiedad,\n      !!@ ili2db.dispName = "Usufructo"\n      Usufructo,\n      !!@ ili2db.dispName = "Tenencia"\n      Tenencia,\n      !!@ ili2db.dispName = "Minero"\n      Minero\n    );\n\n    OP_DominioConstruccionTipo = (\n      !!@ ili2db.dispName = "Común"\n      Comun,\n      !!@ ili2db.dispName = "Privado"\n      Privado\n    );\n\n    OP_FotoidentificacionTipo = (\n      !!@ ili2db.dispName = "Visible"\n      Visible,\n      !!@ ili2db.dispName = "Estimado"\n      Estimado\n    );\n\n    OP_FuenteAdministrativaTipo = (\n      !!@ ili2db.dispName = "Escritura pública"\n      Escritura_Publica,\n      !!@ ili2db.dispName = "Sentencia judicial"\n      Sentencia_Judicial,\n      !!@ ili2db.dispName = "Acto administrativo"\n      Acto_Administrativo,\n      !!@ ili2db.dispName = "Documento privado"\n      Documento_Privado,\n      !!@ ili2db.dispName = "Sin documento"\n      Sin_Documento\n    );\n\n    OP_GrupoEtnicoTipo = (\n      !!@ ili2db.dispName = "Indígena"\n      Indigena,\n      !!@ ili2db.dispName = "Rrom"\n      Rrom,\n      !!@ ili2db.dispName = "Raizal"\n      Raizal,\n      !!@ ili2db.dispName = "Palenquero"\n      Palenquero,\n      !!@ ili2db.dispName = "Negro"\n      Negro,\n      !!@ ili2db.dispName = "Afrocolombiano"\n      Afrocolombiano,\n      !!@ ili2db.dispName = "Ninguno"\n      Ninguno\n    );\n\n    OP_InteresadoDocumentoTipo = (\n      !!@ ili2db.dispName = "Cédula de ciudadanía"\n      Cedula_Ciudadania,\n      !!@ ili2db.dispName = "Cédula de estranjería"\n      Cedula_Extranjeria,\n      !!@ ili2db.dispName = "NIT"\n      NIT,\n      !!@ ili2db.dispName = "Pasaporte"\n      Pasaporte,\n      !!@ ili2db.dispName = "Tarjeta de identidad"\n      Tarjeta_Identidad,\n      !!@ ili2db.dispName = "Libreta militar"\n      Libreta_Militar,\n      !!@ ili2db.dispName = "Registro civil"\n      Registro_Civil,\n      !!@ ili2db.dispName = "Cédula militar"\n      Cedula_Militar,\n      !!@ ili2db.dispName = "NUIP"\n      NUIP\n    );\n\n    OP_InteresadoTipo = (\n      !!@ ili2db.dispName = "Persona natural"\n      Persona_Natural,\n      !!@ ili2db.dispName = "Persona jurídica"\n      Persona_Juridica\n    );\n\n    /** Conjunto de valores para indicar si se trata de un punto de control de referencia (un punto principal) o de apoyo (uso para levantamientos locales con estación total)\n     */\n    OP_PuntoControlTipo = (\n      !!@ ili2db.dispName = "Control"\n      Control,\n      !!@ ili2db.dispName = "Apoyo"\n      Apoyo\n    );\n\n    /** Punto de leventamiento planimetrico que se identifican en el marco de la identificación de las construcciones, los linderos o puntos auxiliares levantado para el apoyo en la mediciión\n     */\n    OP_PuntoLevTipo = (\n      !!@ ili2db.dispName = "Auxiliar"\n      Auxiliar,\n      !!@ ili2db.dispName = "Construcción"\n      Construccion,\n      !!@ ili2db.dispName = "Servidumbre"\n      Servidumbre\n    );\n\n    OP_PuntoTipo = (\n      !!@ ili2db.dispName = "Poste"\n      Poste,\n      !!@ ili2db.dispName = "Construcción"\n      Construccion,\n      /** Punto referido a los puntos limitantes con elementos hidrográficos\n       */\n      !!@ ili2db.dispName = "Punto dinámico"\n      Punto_Dinamico,\n      !!@ ili2db.dispName = "elemento natural"\n      Elemento_Natural,\n      !!@ ili2db.dispName = "Piedra"\n      Piedra,\n      !!@ ili2db.dispName = "Sin materialización"\n      Sin_Materializacion,\n      !!@ ili2db.dispName = "Mojón"\n      Mojon,\n      !!@ ili2db.dispName = "Incrustación"\n      Incrustacion,\n      !!@ ili2db.dispName = "Pilastra"\n      Pilastra\n    );\n\n    OP_RestriccionTipo = (\n      !!@ ili2db.dispName = "Servidumbre de paso"\n      Servidumbre(\n        !!@ ili2db.dispName = "(Servidumbre) Tránsito"\n        Transito,\n        !!@ ili2db.dispName = "(Servidumbre) Aguas negras"\n        Aguas_Negras,\n        !!@ ili2db.dispName = "(Servidumbre) Aire"\n        Aire,\n        !!@ ili2db.dispName = "(Servidumbre) Energía eléctrica"\n        Energia_Electrica,\n        !!@ ili2db.dispName = "(Servidumbre) Gasoducto"\n        Gasoducto,\n        !!@ ili2db.dispName = "(Servidumbre) Luz"\n        Luz,\n        !!@ ili2db.dispName = "(Servidumbre) Oleoducto"\n        Oleoducto,\n        !!@ ili2db.dispName = "(Servidumbre) Agua"\n        Agua,\n        !!@ ili2db.dispName = "(Servidumbre) Minera"\n        Minera,\n        !!@ ili2db.dispName = "(Servidumbre) Legal de hidrocarburos"\n        Legal_Hidrocarburos,\n        !!@ ili2db.dispName = "(Servidumbre) Catenaria (decreto 738 de 2014, ley 1682 de 2013)"\n        Catenaria,\n        !!@ ili2db.dispName = "(Servidumbre) Alcantarillado"\n        Alcantarillado,\n        !!@ ili2db.dispName = "(Servidumbre) Acueducto"\n        Acueducto\n      )\n    );\n\n    OP_SexoTipo = (\n      !!@ ili2db.dispName = "Masculino"\n      Masculino,\n      !!@ ili2db.dispName = "Femenino"\n      Femenino\n    );\n\n    OP_UbicacionPuntoTipo = (\n      !!@ ili2db.dispName = "Esquinero"\n      Esquinero,\n      !!@ ili2db.dispName = "Medianero"\n      Medianero\n    );\n\n    /** Valores válidos para indicar el tipo de construcción empleada para levantar una unidad de construcción, con incidencia en su avalúo. REVISAR DOCUMENTACIÓN\n     */\n    OP_UnidadConstruccionTipo = (\n      !!@ ili2db.dispName = "Residencial"\n      Residencial,\n      !!@ ili2db.dispName = "Comercial"\n      Comercial,\n      !!@ ili2db.dispName = "Industrial"\n      Industrial,\n      !!@ ili2db.dispName = "Anexo"\n      Anexo\n    );\n\n    OP_UsoUConsTipo = (\n      !!@ ili2db.dispName = "Vivienda de hasta 3 pisos"\n      Vivienda_Hasta_3_Pisos,\n      !!@ ili2db.dispName = "Ramadas, cobertizos o caneyes"\n      Ramadas_Cobertizos_Caneyes,\n      !!@ ili2db.dispName = "Galpones o gallineros"\n      Galpones_Gallineros,\n      !!@ ili2db.dispName = "Establos, pesebreras o caballerizas"\n      Establos_Pesebreras_Caballerizas,\n      !!@ ili2db.dispName = "Cocheras, bañeras o porquerizas"\n      Cocheras_Banieras_Porquerizas,\n      !!@ ili2db.dispName = "Bodega casa bomba"\n      Bodega_Casa_Bomba,\n      !!@ ili2db.dispName = "Industrias"\n      Industrias,\n      !!@ ili2db.dispName = "Silos"\n      Silos,\n      !!@ ili2db.dispName = "Piscinas"\n      Piscinas,\n      !!@ ili2db.dispName = "Tanques"\n      Tanques,\n      !!@ ili2db.dispName = "Beneficiaderos"\n      Beneficiaderos,\n      !!@ ili2db.dispName = "Colegios y universidades"\n      Colegios_Y_Universidades,\n      !!@ ili2db.dispName = "Bibliotecas"\n      Bibliotecas,\n      !!@ ili2db.dispName = "Garajes cubiertos"\n      Garajes_Cubiertos,\n      !!@ ili2db.dispName = "Bodegas comerciales, grandes almacenes"\n      Bodegas_Comerciales_Grandes_Almacenes,\n      !!@ ili2db.dispName = "Secaderos"\n      Secaderos,\n      !!@ ili2db.dispName = "Centros hospitales, centros médicos"\n      Clinicas_Hospitales_Centros_Medicos,\n      !!@ ili2db.dispName = "Pozos"\n      Pozos,\n      !!@ ili2db.dispName = "Kioskos"\n      Kioskos,\n      !!@ ili2db.dispName = "Albercas o bañaderas"\n      Albercas_Baniaderas,\n      !!@ ili2db.dispName = "Hoteles en propiedad horizontal"\n      Hoteles_En_PH,\n      !!@ ili2db.dispName = "Corrales"\n      Corrales,\n      !!@ ili2db.dispName = "Casa de elbas"\n      Casa_Elbas,\n      !!@ ili2db.dispName = "Comercio"\n      Comercio,\n      !!@ ili2db.dispName = "Iglesias"\n      Iglesias,\n      !!@ ili2db.dispName = "Hoteles"\n      Hoteles,\n      !!@ ili2db.dispName = "Clubes o casinos"\n      Clubes_Casinos,\n      !!@ ili2db.dispName = "Oficinas o consultorios"\n      Oficinas_Consultorios,\n      !!@ ili2db.dispName = "Apartamentos de más de 4 pisos"\n      Apartamentos_Mas_De_4_Pisos,\n      !!@ ili2db.dispName = "Restaurante"\n      Restaurante,\n      !!@ ili2db.dispName = "Pensiones o residencias"\n      Pensiones_Residencias,\n      !!@ ili2db.dispName = "Puesto de salud"\n      Puesto_De_Salud,\n      !!@ ili2db.dispName = "Parqueaderos"\n      Parqueaderos,\n      !!@ ili2db.dispName = "Barracas"\n      Barracas,\n      !!@ ili2db.dispName = "Teatro o cinemas"\n      Teatro_Cinemas,\n      !!@ ili2db.dispName = "Aulas de clase"\n      Aulas_De_Clase,\n      !!@ ili2db.dispName = "Coliseos"\n      Coliseos,\n      !!@ ili2db.dispName = "Casas de culto"\n      Casas_De_Culto,\n      !!@ ili2db.dispName = "Talleres"\n      Talleres,\n      !!@ ili2db.dispName = "Jardín infantil en casa"\n      Jardin_Infantil_En_Casa,\n      !!@ ili2db.dispName = "Torres de enfriamiento"\n      Torres_De_Enfriamiento,\n      !!@ ili2db.dispName = "Muelles"\n      Muelles,\n      !!@ ili2db.dispName = "Estación de bombeo"\n      Estacion_De_Bombeo,\n      !!@ ili2db.dispName = "Estadio, plaza de toros"\n      Estadio_Plaza_De_Toros,\n      !!@ ili2db.dispName = "Cárceles"\n      Carceles,\n      !!@ ili2db.dispName = "Parque cementerio"\n      Parque_Cementerio,\n      !!@ ili2db.dispName = "Vivienda colonial"\n      Vivienda_Colonial,\n      !!@ ili2db.dispName = "Comercio colonial"\n      Comercio_Colonial,\n      !!@ ili2db.dispName = "Oficinas o consultorios colonial"\n      Oficinas_Consultorios_Colonial,\n      !!@ ili2db.dispName = "Apartamentos en edificios de 4 o 5 pisos"\n      Aptos_En_Edificios_4_5_Pisos,\n      !!@ ili2db.dispName = "Centros comerciales"\n      Centros_Comerciales,\n      !!@ ili2db.dispName = "Canchas de tenis"\n      Canchas_De_Tenis,\n      !!@ ili2db.dispName = "Toboganes"\n      Toboganes,\n      !!@ ili2db.dispName = "Vivienda recreacional"\n      Vivienda_Recreacional,\n      !!@ ili2db.dispName = "Camaroneras"\n      Camaroneras,\n      !!@ ili2db.dispName = "Fuertes y castillos"\n      Fuertes_Y_Castillos,\n      !!@ ili2db.dispName = "Murallas"\n      Murallas,\n      !!@ ili2db.dispName = "Vivienda de hasta 3 pisos"\n      Vivienda_Hasta_3_Pisos_En_PH,\n      !!@ ili2db.dispName = "Apartamentos de 4 y más pisos en propiedad horizontal"\n      Apartamentos_4_Y_Mas_Pisos_En_PH,\n      !!@ ili2db.dispName = "Vivienda recreacional en propiedad horizontal"\n      Vivienda_Recreacional_En_PH,\n      !!@ ili2db.dispName = "Bodega casa bomba en propiedad horizontal"\n      Bodega_Casa_Bomba_En_PH,\n      !!@ ili2db.dispName = "Bodega comercial en propiedad horizontal"\n      Bodega_Comercial_En_PH,\n      !!@ ili2db.dispName = "Comercio en propiedad horizontal"\n      Comercio_En_PH,\n      !!@ ili2db.dispName = "Centros comerciales en propiedad horizontal"\n      Centros_Comerciales_En_PH,\n      !!@ ili2db.dispName = "Oficinas o consultorios en propiedad horizontal"\n      Oficinas_Consultorios_En_PH,\n      !!@ ili2db.dispName = "Parqueaderos en propiedad horizontal"\n      Parqueaderos_En_PH,\n      !!@ ili2db.dispName = "Garajes en propiedad horizontal"\n      Garajes_En_PH,\n      !!@ ili2db.dispName = "Industria en propiedad horizontal"\n      Industria_En_PH,\n      !!@ ili2db.dispName = "Marquesinas, patios o cubiertos"\n      Marquesinas_Patios_Cubiertos,\n      !!@ ili2db.dispName = "Lagunas de oxidación"\n      Lagunas_De_Oxidacion,\n      !!@ ili2db.dispName = "Vía férrea"\n      Via_Ferrea,\n      !!@ ili2db.dispName = "Carretera"\n      Carretera,\n      !!@ ili2db.dispName = "Teatro o cinema en propiedad horizontal"\n      Teatro_Cinema_En_PH,\n      !!@ ili2db.dispName = "Iglesia en propiedad horizontal"\n      Iglesia_En_PH,\n      !!@ ili2db.dispName = "Restaurante en propiedad horizontal"\n      Restaurante_En_PH,\n      !!@ ili2db.dispName = "Hotel colonial"\n      Hotel_Colonial,\n      !!@ ili2db.dispName = "Restaurante colonial"\n      Restaurante_Colonial,\n      !!@ ili2db.dispName = "Entidad educativa colonial o colegio colonial"\n      Entidad_Educativa_Colonial_Colegio_Colonial,\n      !!@ ili2db.dispName = "Cimientos de estructura, muros y placa base"\n      Cimientos_Estructura_Muros_Y_Placa_Base\n    );\n\n    OP_ViaTipo = (\n      !!@ ili2db.dispName = "Arteria"\n      Arteria,\n      !!@ ili2db.dispName = "Autopista"\n      Autopista,\n      !!@ ili2db.dispName = "Carreteable"\n      Carreteable,\n      !!@ ili2db.dispName = "Ciclorruta"\n      Cicloruta,\n      !!@ ili2db.dispName = "Colectora"\n      Colectora,\n      !!@ ili2db.dispName = "Departamental"\n      Departamental,\n      !!@ ili2db.dispName = "Férrea"\n      Ferrea,\n      !!@ ili2db.dispName = "Local"\n      Local,\n      !!@ ili2db.dispName = "Metro o metrovía"\n      Metro_o_Metrovia,\n      !!@ ili2db.dispName = "Nacional"\n      Nacional,\n      !!@ ili2db.dispName = "Ordinaria"\n      Ordinaria,\n      !!@ ili2db.dispName = "Peatonal"\n      Peatonal,\n      !!@ ili2db.dispName = "Principal"\n      Principal,\n      !!@ ili2db.dispName = "Privada"\n      Privada,\n      !!@ ili2db.dispName = "Secundaria"\n      Secundaria,\n      !!@ ili2db.dispName = "Troncal"\n      Troncal\n    );\n\n  TOPIC Operacion\n  EXTENDS LADM_COL_V1_6.LADM_Nucleo =\n    OID AS INTERLIS.UUIDOID;\n    DEPENDS ON LADM_COL_V1_6.LADM_Nucleo,Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos;\n\n    !!@ ili2db.dispName = "Agrupación de Interesados"\n    CLASS OP_Agrupacion_Interesados\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_Agrupacion_Interesados =\n    END OP_Agrupacion_Interesados;\n\n    /** Es un tipo de espacio jurídico de la unidad de edificación del modelo LADM que almacena datos específicos del avalúo resultante del mismo.\n     */\n    !!@ ili2db.dispName = "Construcción"\n    CLASS OP_Construccion\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial =\n      !!@ ili2db.dispName = "Identificador"\n      Identificador : TEXT*2;\n      !!@ ili2db.dispName = "Tipo de construcción"\n      Tipo_Construccion : Operacion_V2_10.OP_ConstruccionTipo;\n      !!@ ili2db.dispName = "Tipo de dominio"\n      Tipo_Dominio : Operacion_V2_10.OP_DominioConstruccionTipo;\n      /** Cantidad de plantas que tiene la construcción\n       */\n      !!@ ili2db.dispName = "Número de pisos"\n      Numero_Pisos : MANDATORY 1 .. 100;\n      !!@ ili2db.dispName = "Número de sótanos"\n      Numero_Sotanos : 0 .. 99;\n      !!@ ili2db.dispName = "Número de mezanines"\n      Numero_Mezanines : 0 .. 99;\n      !!@ ili2db.dispName = "Número de semisótanos"\n      Numero_Semisotanos : 0 .. 99;\n      !!@ ili2db.dispName = "Código de edificación"\n      Codigo_Edificacion : 0 .. 10000000000000000000;\n      !!@ ili2db.dispName = "Área de construcción"\n      Area_Construccion : MANDATORY 0.0 .. 99999999999999.9 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Altura"\n      Altura : 1 .. 1000 [INTERLIS.m];\n      /** Rsultado del cálculo de su avalúo mediante la metodología legalmente establecida.\n       */\n      !!@ ili2db.dispName = "Ávaluo de construcción"\n      Avaluo_Construccion : LADM_COL_V1_6.LADM_Nucleo.Peso;\n    END OP_Construccion;\n\n    !!@ ili2db.dispName = "Datos PH Condominio"\n    CLASS OP_Datos_PH_Condominio =\n      !!@ ili2db.dispName = "Área total de terreno"\n      Area_Total_Terreno : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Área total de terreno privada"\n      Area_Total_Terreno_Privada : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Área total de terreno común"\n      Area_Total_Terreno_Comun : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Área total construida"\n      Area_Total_Construida : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Área total construida privada"\n      Area_Total_Construida_Privada : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Área total construida común"\n      Area_Total_Construida_Comun : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Torre número"\n      Torre_No : TEXT*10;\n      !!@ ili2db.dispName = "Total pisos de torre"\n      Total_Pisos_Torre : 0 .. 200;\n      !!@ ili2db.dispName = "Total de unidades privadas"\n      Total_Unidades_Privadas : 0 .. 99999999;\n      !!@ ili2db.dispName = "Total de sótanos"\n      Total_Sotanos : 0 .. 30;\n      !!@ ili2db.dispName = "Total de únidades de sótanos"\n      Total_Unidades_Sotanos : 0 .. 99999999;\n    END OP_Datos_PH_Condominio;\n\n    /** Clase que registra las instancias de los derechos que un interesado ejerce sobre un predio. Es una especialización de la clase LA_RRR del propio modelo.\n     */\n    !!@ ili2db.dispName = "Derecho"\n    CLASS OP_Derecho\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_DRR =\n      /** Derecho que se ejerce.\n       */\n      !!@ ili2db.dispName = "Tipo"\n      Tipo : Operacion_V2_10.OP_DerechoTipo;\n    END OP_Derecho;\n\n    !!@ ili2db.dispName = "Fuente Administrativa"\n    CLASS OP_FuenteAdministrativa\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativa =\n      !!@ ili2db.dispName = "Tipo"\n      Tipo (EXTENDED) : MANDATORY Operacion_V2_10.OP_FuenteAdministrativaTipo;\n      !!@ ili2db.dispName = "Ente emisor"\n      Ente_Emisor : TEXT*255;\n    END OP_FuenteAdministrativa;\n\n    !!@ ili2db.dispName = "Fuente Espacial"\n    CLASS OP_FuenteEspacial\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacial =\n    END OP_FuenteEspacial;\n\n    !!@ ili2db.dispName = "Interesado"\n    CLASS OP_Interesado\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_Interesado =\n      /** Tipo de persona del que se trata\n       */\n      !!@ ili2db.dispName = "Tipo"\n      Tipo : MANDATORY Operacion_V2_10.OP_InteresadoTipo;\n      /** Tipo de documento del que se trata.\n       */\n      !!@ ili2db.dispName = "Tipo de documento"\n      Tipo_Documento : MANDATORY Operacion_V2_10.OP_InteresadoDocumentoTipo;\n      /** Documento de identidad del interesado.\n       */\n      !!@ ili2db.dispName = "Documento de identidad"\n      Documento_Identidad : MANDATORY TEXT*50;\n      /** Primer nombre de la persona física.\n       */\n      !!@ ili2db.dispName = "Primer nombre"\n      Primer_Nombre : TEXT*100;\n      /** Segundo nombre de la persona física.\n       */\n      !!@ ili2db.dispName = "Segundo nombre"\n      Segundo_Nombre : TEXT*100;\n      /** Primer apellido de la persona física.\n       */\n      !!@ ili2db.dispName = "Primer apellido"\n      Primer_Apellido : TEXT*100;\n      /** Segundo apellido de la persona física.\n       */\n      !!@ ili2db.dispName = "Segundo apellido"\n      Segundo_Apellido : TEXT*100;\n      !!@ ili2db.dispName = "Sexo"\n      Sexo : Operacion_V2_10.OP_SexoTipo;\n      !!@ ili2db.dispName = "Grupo étnico"\n      Grupo_Etnico : Operacion_V2_10.OP_GrupoEtnicoTipo;\n      /** Nombre con el que está inscrito.\n       */\n      !!@ ili2db.dispName = "Razón social"\n      Razon_Social : TEXT*255;\n    END OP_Interesado;\n\n    !!@ ili2db.dispName = "Interesado Contacto"\n    CLASS OP_Interesado_Contacto =\n      !!@ ili2db.dispName = "Teléfono 1"\n      Telefono1 : TEXT*20;\n      !!@ ili2db.dispName = "Teléfono 2"\n      Telefono2 : TEXT*20;\n      !!@ ili2db.dispName = "Domicilio notificación"\n      Domicilio_Notificacion : TEXT*500;\n      !!@ ili2db.dispName = "Dirección de residencia"\n      Direccion_Residencia : TEXT*500;\n      !!@ ili2db.dispName = "Correo electrónico"\n      Correo_Electronico : TEXT*100;\n      /** Indica si el interesado autoriza notificación vía correo electrónico\n       */\n      !!@ ili2db.dispName = "Autoriza notificación correo"\n      Autoriza_Notificacion_Correo : BOOLEAN;\n      !!@ ili2db.dispName = "Departamento"\n      Departamento : MANDATORY TEXT*100;\n      !!@ ili2db.dispName = "Municipio"\n      Municipio : MANDATORY TEXT*100;\n      !!@ ili2db.dispName = "Vereda"\n      Vereda : TEXT*100;\n      !!@ ili2db.dispName = "Corregimiento"\n      Corregimiento : TEXT*100;\n    END OP_Interesado_Contacto;\n\n    /** Clase especializada de LA_CadenaCarasLindero que permite registrar los linderos.\n     * Dos linderos no pueden cruzarse ni superponerse.\n     */\n    !!@ ili2db.dispName = "Lindero"\n    CLASS OP_Lindero\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_CadenaCarasLimite =\n      /** Lóngitud en m del lindero.\n       */\n      !!@ ili2db.dispName = "Longitud"\n      Longitud : MANDATORY 0.0 .. 10000.0 [INTERLIS.m];\n    END OP_Lindero;\n\n    /** Clase especializada de BaUnit, que describe la unidad administrativa básica para el caso de Colombia.\n     * El predio es la unidad territorial legal propia de Catastro. Esta formada por el terreno y puede o no tener construcciones asociadas.\n     */\n    !!@ ili2db.dispName = "Predio"\n    CLASS OP_Predio\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_BAUnit =\n      /** Corresponde al codigo del departamento al cual pertenece el predio. Es asignado por DIVIPOLA y tiene 2 dígitos.\n       */\n      !!@ ili2db.dispName = "Departamento"\n      Departamento : MANDATORY TEXT*2;\n      /** Corresponde al codigo del municipio al cual pertenece el predio. Es asignado por DIVIPOLA y tiene 3 dígitos.\n       */\n      !!@ ili2db.dispName = "Municipio"\n      Municipio : MANDATORY TEXT*3;\n      /** Numero Unico de identificación Predial. Es el codigo definido en el proyecto de ley que será el codigo de identificación del predio tanto para catastratro como para Registro.\n       */\n      !!@ ili2db.dispName = "Identificador único de operación"\n      Id_Operacion : MANDATORY TEXT*30;\n      !!@ ili2db.dispName = "Tiene FMI"\n      Tiene_FMI : MANDATORY BOOLEAN;\n      /** Circulo registral\n       */\n      !!@ ili2db.dispName = "Código ORIP"\n      Codigo_ORIP : TEXT*3;\n      /** Matricula inmobiliaria\n       */\n      !!@ ili2db.dispName = "Matrícula inmobiliaria"\n      Matricula_Inmobiliaria : TEXT*80;\n      /** Nuevo código númerico de treinta (30) dígitos, que se le asigna a cada predio y busca localizarlo inequívocamente en los documentos catastrales, según el modelo determinado por el Instituto Geográfico Agustin Codazzi.\n       */\n      !!@ ili2db.dispName = "Número predial"\n      Numero_Predial : TEXT*30;\n      /** Anterior código númerico de veinte (20) digitos, que se le asigna a cada predio y busca localizarlo inequívocamente en los documentos catastrales, según el modelo determinado por el Instituto Geográfico Agustin Codazzi.\n       */\n      !!@ ili2db.dispName = "Número predial anterior"\n      Numero_Predial_Anterior : TEXT*20;\n      /** Valor de cada predio, obtenido mediante investigación y análisis estadistico del mercado inmobiliario y la metodología de aplicación  correspondiente. El avalúo  catastral de cada predio se determina a partir de la adición de los avalúos parciales practicados independientemente para los terrenos y para las edificaciones en el comprendidos.\n       */\n      !!@ ili2db.dispName = "Avalúo catastral"\n      Avaluo_Catastral : LADM_COL_V1_6.LADM_Nucleo.Peso;\n      !!@ ili2db.dispName = "Condición del predio"\n      Condicion_Predio : MANDATORY Operacion_V2_10.OP_CondicionPredioTipo;\n      !!@ ili2db.dispName = "Dirección"\n      Direccion : MANDATORY TEXT*255;\n      UNIQUE Id_Operacion; \n    END OP_Predio;\n\n    /** Clase especializada de LA_Punto que representa puntos de la densificación de la red local, que se utiliza en la operación catastral para el levantamiento de información fisica de los objetos territoriales, como puntos de control.\n     */\n    !!@ ili2db.dispName = "Punto Control"\n    CLASS OP_PuntoControl\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_Punto =\n      /** Nombre que recibe el punto.\n       */\n      !!@ ili2db.dispName = "ID del punto de control"\n      ID_Punto_Control : MANDATORY TEXT*255;\n      !!@ ili2db.dispName = "Tipo de punto"\n      PuntoTipo (EXTENDED) : MANDATORY Operacion_V2_10.OP_PuntoTipo;\n      /** Si se trata deun punto de control o de apoyo.\n       */\n      !!@ ili2db.dispName = "Tipo de punto de control"\n      Tipo_Punto_Control : Operacion_V2_10.OP_PuntoControlTipo;\n      /** Exactitud horizontal de la medición del punto.\n       */\n      !!@ ili2db.dispName = "Exactitud horizontal"\n      Exactitud_Horizontal : MANDATORY 0 .. 1000 [LADM_COL_V1_6.cm];\n      /** Exactitud vertical de la medición del punto.\n       */\n      !!@ ili2db.dispName = "Exactitud vertical"\n      Exactitud_Vertical : MANDATORY 0 .. 1000 [LADM_COL_V1_6.cm];\n    END OP_PuntoControl;\n\n    /** Clase especializada de LA_Punto que almacena puntos que definen un lindero, instancia de la clase LA_CadenaCarasLindero y sus especializaciones.\n     */\n    !!@ ili2db.dispName = "Punto Lindero"\n    CLASS OP_PuntoLindero\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_Punto =\n      /** Nombre o codigo del punto lindero\n       */\n      !!@ ili2db.dispName = "ID del punto de lindero"\n      ID_Punto_Lindero : TEXT*255;\n      !!@ ili2db.dispName = "Tipo de punto"\n      PuntoTipo (EXTENDED) : MANDATORY Operacion_V2_10.OP_PuntoTipo;\n      /** Se Indica si existe acuerdo o no entre los colindantes en relación al punto lindero que se está midiendo.\n       */\n      !!@ ili2db.dispName = "Acuerdo"\n      Acuerdo : MANDATORY Operacion_V2_10.OP_AcuerdoTipo;\n      !!@ ili2db.dispName = "Fotoidentificación"\n      Fotoidentificacion : Operacion_V2_10.OP_FotoidentificacionTipo;\n      !!@ ili2db.dispName = "Ubicación del punto"\n      Ubicacion_Punto : Operacion_V2_10.OP_UbicacionPuntoTipo;\n      /** Corresponde a la exactitud horizontal del punto lindero\n       */\n      !!@ ili2db.dispName = "Exactitud horizontal"\n      Exactitud_Horizontal : MANDATORY 0 .. 1000 [LADM_COL_V1_6.cm];\n      /** Corresponde a la exactitud vertical del punto lindero\n       */\n      !!@ ili2db.dispName = "Exactitud vertical"\n      Exactitud_Vertical : 0 .. 1000 [LADM_COL_V1_6.cm];\n    END OP_PuntoLindero;\n\n    !!@ ili2db.dispName = "Restricción"\n    CLASS OP_Restriccion\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_DRR =\n      !!@ ili2db.dispName = "Tipo"\n      Tipo : MANDATORY Operacion_V2_10.OP_RestriccionTipo;\n    END OP_Restriccion;\n\n    /** Porción de tierra con una extensión geográfica definida.\n     */\n    !!@ ili2db.dispName = "Terreno"\n    CLASS OP_Terreno\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial =\n      /** Área de predio resultado de los calculos realizados en el proceso de levantamiento planimetrico\n       */\n      !!@ ili2db.dispName = "Área de terreno"\n      Area_Terreno : MANDATORY 0.0 .. 99999999999999.9 [LADM_COL_V1_6.m2];\n      /** Valor asignado en el proceso de valoración economica masiva al terreno del predio\n       */\n      !!@ ili2db.dispName = "Avalúo de terreno"\n      Avaluo_Terreno : LADM_COL_V1_6.LADM_Nucleo.Peso;\n      !!@ ili2db.dispName = "Código de manzana vereda"\n      Manzana_Vereda_Codigo : TEXT*17;\n      !!@ ili2db.dispName = "Número de subterráneos"\n      Numero_Subterraneos : 0 .. 999;\n      /** Corresponde a la figura geometrica vectorial poligonal, generada a partir de los linderos del predio.\n       */\n      !!@ ili2db.dispName = "Geometría"\n      Geometria (EXTENDED) : MANDATORY ISO19107_PLANAS_V1.GM_MultiSurface3D;\n    END OP_Terreno;\n\n    /** Clase especializada de LA_Punto que representa puntos demarcados que representan la posición horizontal de un vértice de construcción, servidumbre o auxiliare.\n     */\n    !!@ ili2db.dispName = "Punto Levantamiento"\n    CLASS OP_PuntoLevantamiento\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_Punto =\n      /** Se caracterizan los diferentes tipos de punto levantamiento, estos son punto de construccción, punto de servidumbre o punto auxiliar\n       */\n      !!@ ili2db.dispName = "ID del punto de levantamiento"\n      ID_Punto_Levantamiento : TEXT*255;\n      !!@ ili2db.dispName = "Tipo de punto"\n      PuntoTipo (EXTENDED) : MANDATORY Operacion_V2_10.OP_PuntoTipo;\n      !!@ ili2db.dispName = "Tipo de punto de levantamiento"\n      Tipo_Punto_Levantamiento : Operacion_V2_10.OP_PuntoLevTipo;\n      !!@ ili2db.dispName = "Fotoidentificación"\n      Fotoidentificacion : Operacion_V2_10.OP_FotoidentificacionTipo;\n      /** Corresponde a la exactitud horizontal del punto levantamiento\n       */\n      !!@ ili2db.dispName = "Exactitud horizontal"\n      Exactitud_Horizontal : MANDATORY 0 .. 1000 [LADM_COL_V1_6.cm];\n      /** Corresponde a la exactitud vertical del punto levantamiento\n       */\n      !!@ ili2db.dispName = "Exactitud vertical"\n      Exactitud_Vertical : 0 .. 1000 [LADM_COL_V1_6.cm];\n    END OP_PuntoLevantamiento;\n\n    ASSOCIATION op_interesado_contacto =\n      op_contacto -- {0..*} OP_Interesado_Contacto;\n      op_interesado -- {1} OP_Interesado;\n    END op_interesado_contacto;\n\n    ASSOCIATION op_ph_predio =\n      op_predio -- {1} OP_Predio;\n      op_datos_ph -- {0..1} OP_Datos_PH_Condominio;\n    END op_ph_predio;\n\n    ASSOCIATION op_predio_copropiedad =\n      predio -- {0..*} OP_Predio;\n      copropiedad -<> {0..1} OP_Predio;\n      coeficiente : LADM_COL_V1_6.LADM_Nucleo.Fraccion;\n    END op_predio_copropiedad;\n\n    ASSOCIATION op_predio_insumos_operacion =\n      ini_predio_insumos (EXTERNAL) -- {0..*} Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos.INI_Predio_Insumos;\n      op_predio -- {0..*} OP_Predio;\n    END op_predio_insumos_operacion;\n\n    /** Tipo de unidad espacial que permite la representación de una servidumbre de paso asociada a una LA_BAUnit.\n     */\n    !!@ ili2db.dispName = "Servidumbre de Tránsito"\n    CLASS OP_ServidumbreTransito\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial =\n      /** Fecha de inscripción de la servidumbre en el Catastro.\n       */\n      !!@ ili2db.dispName = "Área de la servidumbre"\n      Area_Servidumbre : MANDATORY 0.0 .. 99999999999999.9 [LADM_COL_V1_6.m2];\n    END OP_ServidumbreTransito;\n\n    /** Es cada conjunto de materiales consolidados dentro de un predio que tiene una caracteristicas especificas en cuanto a elementos constitutivos físicos y usos de los mismos.\n     */\n    !!@ ili2db.dispName = "Unidad de Construcción"\n    CLASS OP_UnidadConstruccion\n    EXTENDS LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial =\n      !!@ ili2db.dispName = "Identificador"\n      Identificador : TEXT*3;\n      !!@ ili2db.dispName = "Tipo de dominio"\n      Tipo_Dominio : Operacion_V2_10.OP_DominioConstruccionTipo;\n      !!@ ili2db.dispName = "Tipo de construcción"\n      Tipo_Construccion : Operacion_V2_10.OP_ConstruccionTipo;\n      !!@ ili2db.dispName = "Tipo de unidad de construcción"\n      Tipo_Unidad_Construccion : Operacion_V2_10.OP_UnidadConstruccionTipo;\n      !!@ ili2db.dispName = "Tipo de planta"\n      Tipo_Planta : Operacion_V2_10.OP_ConstruccionPlantaTipo;\n      !!@ ili2db.dispName = "Planta ubicación"\n      Planta_Ubicacion : 0 .. 500;\n      !!@ ili2db.dispName = "Total de habitaciones"\n      Total_Habitaciones : 0 .. 999999;\n      !!@ ili2db.dispName = "Total de baños"\n      Total_Banios : 0 .. 999999;\n      !!@ ili2db.dispName = "Total de locales"\n      Total_Locales : 0 .. 999999;\n      !!@ ili2db.dispName = "Total de pisos"\n      Total_Pisos : 0 .. 150;\n      !!@ ili2db.dispName = "Uso"\n      Uso : MANDATORY Operacion_V2_10.OP_UsoUConsTipo;\n      !!@ ili2db.dispName = "Año de construcción"\n      Anio_Construccion : 1512 .. 2500;\n      !!@ ili2db.dispName = "Avalúo de la construcción"\n      Avaluo_Construccion : LADM_COL_V1_6.LADM_Nucleo.Peso;\n      /** Area de la unidad de contrucción.\n       */\n      !!@ ili2db.dispName = "Área construida"\n      Area_Construida : MANDATORY 0.0 .. 99999999999999.9 [LADM_COL_V1_6.m2];\n      /** Área privada de la unidad de construcción para el caso en que las construcciones tienen regimen de propiedad horizontal.\n       */\n      !!@ ili2db.dispName = "Área privada construida"\n      Area_Privada_Construida : 0.0 .. 99999999999999.9 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Altura"\n      Altura : 1 .. 1000 [INTERLIS.m];\n      !!@ ili2db.dispName = "Observaciones"\n      Observaciones : TEXT;\n    END OP_UnidadConstruccion;\n\n    ASSOCIATION op_construccion_unidadconstruccion =\n      op_unidadconstruccion -- {0..*} OP_UnidadConstruccion;\n      op_construccion -<> {1} OP_Construccion;\n    END op_construccion_unidadconstruccion;\n\n  END Operacion;\n\nEND Operacion_V2_10.\n	2020-01-28 10:16:55.146
LADM_COL_V1_6.ili	2.3	LADM_COL_V1_6{ ISO19107_PLANAS_V1}	INTERLIS 2.3;\n\n/** ISO 19152 LADM country profile COL Core Model.\n * \n * -----------------------------------------------------------\n * \n * LADM es un modelo conceptual de la realidad que concreta una ontología y establece una semántica para la administración del territorio.\n * \n * -----------------------------------------------------------\n *  revision history\n * -----------------------------------------------------------\n * \n *  30.01.2018/fm : Cambio del tipo de dato del atributo Ext_Direccion de la clase Unidad Espacial a ExtDireccion; atributo ext_PID de la calse LA_Interesado cambia de OID a ExtInteresado; Cambio de cardinalidad en relacion miembros entre LA_Interesado y LA_Agrupacion_Interesados de 0..1 a 0..*\n *  07.02.2018/fm-gc: Ajuste al tipo de dato de la unidad Peso, pasa a tener precision 1 para evitar ser tratado cmo atributo entero y aumentar su tamaño\n *  19.02.2018/fm-gc: ampliación del dominio al tipo de dato Peso\n *  26.02.2018/fm-lj: cambio del nombre del dominio ISO19125_Type a ISO19125_Tipo\n *  19.04.2018/vb fm: Ajuste al constraint Fraccion, denominador mayor a 0\n *  19.04.2018/vb fm: Cambio en la cardinalidad del atributo u_Local_Id de la clase LA_BAUnit de 0..1 a 1\n * 17.07.2018/fm : se incluye escritura en dominio COL_FuenteAdministrativaTipo\n * 10.08.2018/fm : Se eliminan los atributos ai_local_id y ai_espacio_de_nombres de la clase LA_Agrupacion_Interesados\n * 27.08.2018/fm : Ajuste a la cardinalidad de asociacion puntoFuente de 1..* a 0..*\n * 25.09.2018/at: Se ajusta la longitud del atributo Codigo_Registral_Transaccion en la clase COL_FuenteAdministrativa a 5 caracteres de acuerdo a la Resolución 3973 de 2018\n * -----------------------------------------------------------\n * \n *  (c) IGAC y SNR con apoyo de la Cooperacion Suiza\n * \n * -----------------------------------------------------------\n */\nMODEL LADM_COL_V1_6 (es)\nAT "http://www.proadmintierra.info/"\nVERSION "V1.2.0"  // 2019-08-13 // =\n  IMPORTS ISO19107_PLANAS_V1;\n\n  UNIT\n\n    PesoColombiano [COP] EXTENDS INTERLIS.MONEY;\n\n    Area (ABSTRACT) = (INTERLIS.LENGTH * INTERLIS.LENGTH);\n\n    MetroCuadrado [m2] EXTENDS Area = (INTERLIS.m * INTERLIS.m);\n\n    Centrimetro [cm] = 1 / 100 [INTERLIS.m];\n\n  TOPIC LADM_Nucleo(ABSTRACT) =\n\n    DOMAIN\n\n      CharacterString = TEXT*255;\n\n      /** Traducción del dominio CI_PresentationFormCode de la norma ISO 19115:2003. Indica el modo en el que se representan los datos.\n       */\n      CI_Forma_Presentacion_Codigo = (\n        /** Definición en la ISO 19115:2003.\n         */\n        !!@ ili2db.dispName = "Imagen"\n        Imagen,\n        !!@ ili2db.dispName = "Documento"\n        Documento,\n        /** Definición en la ISO 19115:2003.\n         */\n        !!@ ili2db.dispName = "Mapa"\n        Mapa,\n        /** Definición en la ISO 19115:2003.\n         */\n        !!@ ili2db.dispName = "Video"\n        Video,\n        /** Definición en la ISO 19115:2003.\n         */\n        !!@ ili2db.dispName = "Otro"\n        Otro\n      );\n\n      COL_AreaTipo = (\n        !!@ ili2db.dispName = "Área calculada artura local"\n        Area_Calculada_Altura_Local,\n        !!@ ili2db.dispName = "Área calculada altura mar"\n        Area_Calculada_Altura_Mar,\n        !!@ ili2db.dispName = "Área catastral administrativa"\n        Area_Catastral_Administrativa,\n        !!@ ili2db.dispName = "Área estimado construcción"\n        Area_Estimado_Construccion,\n        !!@ ili2db.dispName = "Área no oficial"\n        Area_No_Oficial,\n        !!@ ili2db.dispName = "Área registral"\n        Area_Registral\n      );\n\n      COL_BAUnitTipo = (\n        !!@ ili2db.dispName = "Unidad propiedad básica"\n        Unidad_Propiedad_Basica,\n        !!@ ili2db.dispName = "Unidad derecho"\n        Unidad_Derecho,\n        !!@ ili2db.dispName = "Otro"\n        Otro\n      );\n\n      COL_ContenidoNivelTipo = (\n        !!@ ili2db.dispName = "Construcción convencional"\n        Construccion_Convencional,\n        !!@ ili2db.dispName = "Construcción no convencional"\n        Construccion_No_Convencional,\n        !!@ ili2db.dispName = "Consuetudinario"\n        Consuetudinario,\n        !!@ ili2db.dispName = "Formal"\n        Formal,\n        !!@ ili2db.dispName = "Informal"\n        Informal,\n        !!@ ili2db.dispName = "Responsabilidad"\n        Responsabilidad,\n        !!@ ili2db.dispName = "Restricción derecho público"\n        Restriccion_Derecho_Publico,\n        !!@ ili2db.dispName = "Restricción derecho privado"\n        Restriccion_Derecho_Privado\n      );\n\n      COL_DimensionTipo = (\n        !!@ ili2db.dispName = "Dimensión 2D"\n        Dim2D,\n        !!@ ili2db.dispName = "Dimensión 3D"\n        Dim3D,\n        !!@ ili2db.dispName = "Otro"\n        Otro\n      );\n\n      COL_EstadoRedServiciosTipo = (\n        !!@ ili2db.dispName = "Planeado"\n        Planeado,\n        !!@ ili2db.dispName = "En uso"\n        En_Uso,\n        !!@ ili2db.dispName = "Fuera de servicio"\n        Fuera_De_Servicio,\n        !!@ ili2db.dispName = "Otro"\n        Otro\n      );\n\n      COL_EstructuraTipo = (\n        !!@ ili2db.dispName = "Croquis"\n        Croquis,\n        !!@ ili2db.dispName = "Línea no estructurada"\n        Linea_no_Estructurada,\n        !!@ ili2db.dispName = "Texto"\n        Texto,\n        !!@ ili2db.dispName = "Topológico"\n        Topologico\n      );\n\n      COL_FuenteEspacialTipo = (\n        !!@ ili2db.dispName = "Croquis de campo"\n        Croquis_Campo,\n        !!@ ili2db.dispName = "Datos crudos (GPS, Estación total, LiDAR, etc.)"\n        Datos_Crudos,\n        !!@ ili2db.dispName = "Ortofoto"\n        Ortofoto,\n        !!@ ili2db.dispName = "Informe técnico"\n        Informe_Tecnico,\n        !!@ ili2db.dispName = "Registro fotográfico"\n        Registro_Fotografico\n      );\n\n      COL_GrupoInteresadoTipo = (\n        !!@ ili2db.dispName = "Grupo civil"\n        Grupo_Civil,\n        !!@ ili2db.dispName = "Grupo empresarial"\n        Grupo_Empresarial,\n        !!@ ili2db.dispName = "Grupo étnico"\n        Grupo_Etnico,\n        !!@ ili2db.dispName = "Grupo mixto"\n        Grupo_Mixto\n      );\n\n      /** Si ha sido situado por interpolación, de qué manera se ha hecho.\n       */\n      COL_InterpolacionTipo = (\n        !!@ ili2db.dispName = "Aislado"\n        Aislado,\n        !!@ ili2db.dispName = "Intermedio arco"\n        Intermedio_Arco,\n        !!@ ili2db.dispName = "Intermedio línea"\n        Intermedio_Linea\n      );\n\n      COL_MetodoProduccionTipo = (\n        !!@ ili2db.dispName = "Método directo"\n        Metodo_Directo,\n        !!@ ili2db.dispName = "Método indirecto"\n        Metodo_Indirecto\n      );\n\n      COL_PuntoTipo = (\n        !!@ ili2db.dispName = "Control"\n        Control,\n        !!@ ili2db.dispName = "Catastro"\n        Catastro,\n        !!@ ili2db.dispName = "Otro"\n        Otro\n      );\n\n      COL_RegistroTipo = (\n        !!@ ili2db.dispName = "Rural"\n        Rural,\n        !!@ ili2db.dispName = "Urbano"\n        Urbano,\n        !!@ ili2db.dispName = "Otro"\n        Otro\n      );\n\n      COL_VolumenTipo = (\n        !!@ ili2db.dispName = "Oficial"\n        Oficial,\n        !!@ ili2db.dispName = "Calculado"\n        Calculado,\n        !!@ ili2db.dispName = "Otro"\n        Otro\n      );\n\n      Integer = 0 .. 999999999;\n\n      COL_EstadoDisponibilidadTipo = (\n        !!@ ili2db.dispName = "Convertido"\n        Convertido,\n        !!@ ili2db.dispName = "Desconocido"\n        Desconocido,\n        !!@ ili2db.dispName = "Disponible"\n        Disponible\n      );\n\n      COL_ISO19125_Tipo = (\n        !!@ ili2db.dispName = "Disjunto"\n        Disjunto,\n        !!@ ili2db.dispName = "Toca"\n        Toca,\n        !!@ ili2db.dispName = "Superpone"\n        Superpone,\n        !!@ ili2db.dispName = "Desconocido"\n        Desconocido\n      );\n\n      COL_RelacionSuperficieTipo = (\n        !!@ ili2db.dispName = "En rasante"\n        En_Rasante,\n        !!@ ili2db.dispName = "En vuelo"\n        En_Vuelo,\n        !!@ ili2db.dispName = "En subsuelo"\n        En_Subsuelo,\n        !!@ ili2db.dispName = "Otro"\n        Otro\n      );\n\n      COL_UnidadEdificacionTipo = (\n        !!@ ili2db.dispName = "Compartido"\n        Compartido,\n        !!@ ili2db.dispName = "Individual"\n        Individual\n      );\n\n      Currency = -2000000000.00 .. 2000000000.00;\n\n      Real = 0.000 .. 999999999.999;\n\n    /** Estructura que proviene de la traducción de la clase CC_OperationMethod de la ISO 19111. Indica el método utilizado, mediante un algoritmo o un procedimiento, para realizar operaciones con coordenadas.\n     */\n    STRUCTURE CC_MetodoOperacion =\n      /** Fórmulas o procedimientos utilizadoa por este método de operación de coordenadas. Esto puede ser una referencia a una publicación. Tenga en cuenta que el método de operación puede no ser analítico, en cuyo caso este atributo hace referencia o contiene el procedimiento, no una fórmula analítica.\n       */\n      !!@ ili2db.dispName = "Fórmula"\n      Formula : MANDATORY CharacterString;\n      /** Número de dimensiones en la fuente CRS de este método de operación de coordenadas.\n       */\n      !!@ ili2db.dispName = "Dimensiones origen"\n      Dimensiones_Origen : Integer;\n      /** Número de dimensiones en el CRS de destino de este método de operación de coordenadas.\n       */\n      !!@ ili2db.dispName = "Ddimensiones objetivo"\n      Ddimensiones_Objetivo : Integer;\n    END CC_MetodoOperacion;\n\n    STRUCTURE COL_AreaValor =\n      !!@ ili2db.dispName = "Área"\n      areaSize : MANDATORY 0.0 .. 99999999999999.9 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Tipo"\n      type : MANDATORY COL_AreaTipo;\n    END COL_AreaValor;\n\n    /** Referencia a una clase externa para gestionar direcciones.\n     */\n    !!@ ili2db.dispName = "Dirección"\n    STRUCTURE ExtDireccion =\n      !!@ ili2db.dispName = "Tipo de dirección"\n      Tipo_Direccion : MANDATORY (\n        !!@ ili2db.dispName = "Estructurada"\n        Estructurada,\n        !!@ ili2db.dispName = "No estructurada"\n        No_Estructurada\n      );\n      !!@ ili2db.dispName = "Es dirección principal"\n      Es_Direccion_Principal : BOOLEAN;\n      /** Par de valores georreferenciados (x,y) en la que se encuentra la dirección.\n       */\n      !!@ ili2db.dispName = "Localización"\n      Localizacion : ISO19107_PLANAS_V1.GM_Point3D;\n      !!@ ili2db.dispName = "Código postal"\n      Codigo_Postal : CharacterString;\n      !!@ ili2db.dispName = "Clase de vía principal"\n      Clase_Via_Principal : (\n        !!@ ili2db.dispName = "Avenida calle"\n        Avenida_Calle,\n        !!@ ili2db.dispName = "Avenida carrera"\n        Avenida_Carrera,\n        !!@ ili2db.dispName = "Calle"\n        Calle,\n        !!@ ili2db.dispName = "Carrera"\n        Carrera,\n        !!@ ili2db.dispName = "Diagonal"\n        Diagonal,\n        !!@ ili2db.dispName = "Transversal"\n        Transversal,\n        !!@ ili2db.dispName = "Circular"\n        Circular\n      );\n      !!@ ili2db.dispName = "Valor vía principal"\n      Valor_Via_Principal : TEXT*100;\n      !!@ ili2db.dispName = "Letra vía principal"\n      Letra_Via_Principal : TEXT*20;\n      !!@ ili2db.dispName = "Sector de la ciudad"\n      Sector_Ciudad : (\n        Norte,\n        Sur,\n        Este,\n        Oeste\n      );\n      !!@ ili2db.dispName = "Valor de vía generadora"\n      Valor_Via_Generadora : TEXT*100;\n      !!@ ili2db.dispName = "Letra de vía generadora"\n      Letra_Via_Generadora : TEXT*20;\n      !!@ ili2db.dispName = "Número del predio"\n      Numero_Predio : TEXT*20;\n      !!@ ili2db.dispName = "Sector del predio"\n      Sector_Predio : (\n        Norte,\n        Sur,\n        Este,\n        Oeste\n      );\n      !!@ ili2db.dispName = "Complemento"\n      Complemento : TEXT*255;\n      !!@ ili2db.dispName = "Nombre del predio"\n      Nombre_Predio : TEXT*255;\n      SET CONSTRAINT WHERE Tipo_Direccion == #No_Estructurada: \n        Nombre_Predio <> UNDEFINED;\n    END ExtDireccion;\n\n    /** Estructura para la definición de un tipo de dato personalizado que permite indicar una fracción o quebrado cona serie específica de condiciones.\n     */\n    STRUCTURE Fraccion =\n      /** Parte inferior de la fracción. Debe ser mayor que 0. Debe ser mayor que el numerador.\n       */\n      !!@ ili2db.dispName = "Denominador"\n      Denominador : MANDATORY Integer;\n      /** Parte superior de la fracción. Debe ser mayor que 0. Debe sder menor que el denominador.\n       */\n      !!@ ili2db.dispName = "Numerador"\n      Numerador : MANDATORY Integer;\n      MANDATORY CONSTRAINT\n        Denominador > 0;\n      MANDATORY CONSTRAINT\n        Numerador > 0;\n      MANDATORY CONSTRAINT\n        Denominador >= Numerador;\n    END Fraccion;\n\n    CLASS Oid (ABSTRACT) =\n      !!@ ili2db.dispName = "Espacio de nombres"\n      Espacio_De_Nombres : MANDATORY CharacterString;\n      !!@ ili2db.dispName = "Local ID"\n      Local_Id : MANDATORY CharacterString;\n    END Oid;\n\n    DOMAIN\n\n      COL_FuenteAdministrativaTipo = (\n        !!@ ili2db.dispName = "Escritura"\n        Escritura,\n        !!@ ili2db.dispName = "Certificado"\n        Certificado,\n        !!@ ili2db.dispName = "Contrato"\n        Contrato,\n        !!@ ili2db.dispName = "Documento de identidad"\n        Documento_Identidad,\n        !!@ ili2db.dispName = "Informe"\n        Informe,\n        !!@ ili2db.dispName = "Formulario predial"\n        Formulario_Predial,\n        !!@ ili2db.dispName = "Promesa de compraventa"\n        Promesa_Compraventa,\n        !!@ ili2db.dispName = "Reglamento"\n        Reglamento,\n        !!@ ili2db.dispName = "Resolución"\n        Resolucion,\n        !!@ ili2db.dispName = "Sentencia"\n        Sentencia,\n        !!@ ili2db.dispName = "Solicitud"\n        Solicitud,\n        !!@ ili2db.dispName = "Acta"\n        Acta,\n        !!@ ili2db.dispName = "Acuerdo"\n        Acuerdo,\n        !!@ ili2db.dispName = "Auto"\n        Auto,\n        !!@ ili2db.dispName = "Estatuto social"\n        Estatuto_Social,\n        !!@ ili2db.dispName = "Decreto"\n        Decreto,\n        !!@ ili2db.dispName = "Providencia"\n        Providencia,\n        !!@ ili2db.dispName = "Acta de colindancia"\n        Acta_Colindancia,\n        !!@ ili2db.dispName = "Libros antiguo sistema"\n        Libros_Antiguo_Sistema_Registral,\n        !!@ ili2db.dispName = "Informe de colindancia"\n        Informe_Colindancia,\n        !!@ ili2db.dispName = "Carta vental"\n        Carta_Venta,\n        !!@ ili2db.dispName = "Otro"\n        Otro\n      );\n\n      COL_RedServiciosTipo = (\n        !!@ ili2db.dispName = "Petróleo"\n        Petroleo,\n        !!@ ili2db.dispName = "Químicos"\n        Quimicos,\n        !!@ ili2db.dispName = "Red térmica"\n        Red_Termica,\n        !!@ ili2db.dispName = "Telecomunicación"\n        Telecomunicacion\n      );\n\n      Peso = 0.0 .. 999999999999999.0 [LADM_COL_V1_6.COP];\n\n    /** Registro de la fórmula o procedimiento utilizado en la transformación y de su resultado.\n     */\n    STRUCTURE COL_Transformacion =\n      /** Fórmula o procedimiento utilizado en la transformación.\n       */\n      !!@ ili2db.dispName = "Transformación"\n      Transformacion : MANDATORY LADM_COL_V1_6.LADM_Nucleo.CC_MetodoOperacion;\n      /** Geometría una vez realizado el proceso de transformación.\n       */\n      !!@ ili2db.dispName = "Localización transformada"\n      Localizacion_Transformada : MANDATORY ISO19107_PLANAS_V1.GM_Point3D;\n    END COL_Transformacion;\n\n    /** Control externo de la unidad de edificación física.\n     */\n    STRUCTURE ExtUnidadEdificacionFisica =\n      !!@ ili2db.dispName = "Ext dirección id"\n      Ext_Direccion_ID : LADM_COL_V1_6.LADM_Nucleo.ExtDireccion;\n    END ExtUnidadEdificacionFisica;\n\n    /** Referencia a una imagen mediante su url.\n     */\n    STRUCTURE Imagen =\n      /** url de la imagen.\n       */\n      !!@ ili2db.dispName = "uri"\n      uri : CharacterString;\n    END Imagen;\n\n    /** Clase abstracta que permite gestionar el histórico del conjunto de clases, las cuales heredan de esta, excepto las fuentes.\n     */\n    CLASS ObjetoVersionado (ABSTRACT)\n    EXTENDS Oid =\n      /** Comienzo de la validez actual de la instancia de un objeto.\n       */\n      !!@ ili2db.dispName = "Versión de comienzo de vida útil"\n      Comienzo_Vida_Util_Version : MANDATORY INTERLIS.XMLDateTime;\n      /** Finnzo de la validez actual de la instancia de un objeto.\n       */\n      !!@ ili2db.dispName = "Versión de fin de vida útil"\n      Fin_Vida_Util_Version : INTERLIS.XMLDateTime;\n      /** Metadatos relativos a la calidad de la instancia.\n       */\n      !!@ ili2db.dispName = "Calidad"\n      Calidad : LIST {0..*} OF ANYSTRUCTURE;\n      /** Metadatos corresondientes a la responsabilidad de la instancia.\n       */\n      !!@ ili2db.dispName = "Procedencia"\n      Procedencia : LIST {0..*} OF ANYSTRUCTURE;\n      MANDATORY CONSTRAINT\n        Fin_Vida_Util_Version >= Comienzo_Vida_Util_Version;\n    END ObjetoVersionado;\n\n    /** Referencia a una clase externa para gestionar direcciones.\n     */\n    STRUCTURE ExtInteresado =\n      /** Identificador externo del interesado.\n       */\n      !!@ ili2db.dispName = "Ext dirección id"\n      Ext_Direccion_ID : LADM_COL_V1_6.LADM_Nucleo.ExtDireccion;\n      !!@ ili2db.dispName = "Huella dactilar"\n      Huella_Dactilar : LADM_COL_V1_6.LADM_Nucleo.Imagen;\n      !!@ ili2db.dispName = "Nombre"\n      Nombre : CharacterString;\n      !!@ ili2db.dispName = "Fotografía"\n      Fotografia : LADM_COL_V1_6.LADM_Nucleo.Imagen;\n      !!@ ili2db.dispName = "Firma"\n      Firma : LADM_COL_V1_6.LADM_Nucleo.Imagen;\n    END ExtInteresado;\n\n    /** Referencia a una clase externa para gestionar las redes físicas de servicios.\n     */\n    STRUCTURE ExtRedServiciosFisica =\n      /** Indica si la red de servicios tiene un gradiente o no.\n       */\n      !!@ ili2db.dispName = "Orientada"\n      Orientada : BOOLEAN;\n      /** Identificador de referencia a un interesado externo que es el administrador.\n       */\n      !!@ ili2db.dispName = "Ext interesado administrador id"\n      Ext_Interesado_Administrador_ID : LADM_COL_V1_6.LADM_Nucleo.ExtInteresado;\n    END ExtRedServiciosFisica;\n\n    /** Referencia a clase externa desde donde se gestiona el repositorio de archivos.\n     */\n    !!@ ili2db.dispName = "Archivo fuente"\n    STRUCTURE ExtArchivo =\n      /** Fecha en la que ha sido aceptado el documento.\n       */\n      !!@ ili2db.dispName = "Fecha de aceptación"\n      Fecha_Aceptacion : INTERLIS.XMLDate;\n      /** Datos que contiene el documento.\n       */\n      !!@ ili2db.dispName = "Datos"\n      Datos : CharacterString;\n      /** Última fecha de extracción del documento.\n       */\n      !!@ ili2db.dispName = "Extracción"\n      Extraccion : INTERLIS.XMLDate;\n      /** Fecha en la que el documento es aceptado en el sistema.\n       */\n      !!@ ili2db.dispName = "Fecha de grabación"\n      Fecha_Grabacion : INTERLIS.XMLDate;\n      /** Fecha en la que fue entregado el documento.\n       */\n      !!@ ili2db.dispName = "Fecha de entrega"\n      Fecha_Entrega : INTERLIS.XMLDate;\n      !!@ ili2db.dispName = "Espacio de nombres"\n      Espacio_De_Nombres : MANDATORY CharacterString;\n      !!@ ili2db.dispName = "Local ID"\n      Local_Id : MANDATORY CharacterString;\n    END ExtArchivo;\n\n    /** Clase abstracta. Esta clase es la personalización en el modelo del perfil colombiano de la clase de LADM LA_Source.\n     */\n    CLASS COL_Fuente (ABSTRACT)\n    EXTENDS Oid =\n      /** Indica si la fuente está o no disponible y en qué condiciones. También puede indicar porqué ha dejado de estar disponible, si ha ocurrido.\n       */\n      !!@ ili2db.dispName = "Estado de disponibilidad"\n      Estado_Disponibilidad : MANDATORY COL_EstadoDisponibilidadTipo;\n      /** Identificador del archivo fuente controlado por una clase externa.\n       */\n      !!@ ili2db.dispName = "Ext archivo id"\n      Ext_Archivo_ID : LADM_COL_V1_6.LADM_Nucleo.ExtArchivo;\n      /** Tipo de formato en el que es presentada la fuente, de acuerdo con el registro de metadatos.\n       */\n      !!@ ili2db.dispName = "Tipo principal"\n      Tipo_Principal : CI_Forma_Presentacion_Codigo;\n      !!@ ili2db.dispName = "Fecha de documento fuente"\n      Fecha_Documento_Fuente : INTERLIS.XMLDate;\n    END COL_Fuente;\n\n    /** Estructura para la definición de un tipo de dato personalizado que permite indicar la medición de un volumen y la naturaleza de este.\n     */\n    STRUCTURE COL_VolumenValor =\n      /** Medición del volumen en m3.\n       */\n      !!@ ili2db.dispName = "Volumen medición"\n      Volumen_Medicion : MANDATORY 0.0 .. 99999999999999.9 [INTERLIS.m];\n      /** Indicación de si el volumen es calculado, si figura como oficial o si se da otra circunstancia.\n       */\n      !!@ ili2db.dispName = "Tipo"\n      Tipo : MANDATORY COL_VolumenTipo;\n    END COL_VolumenValor;\n\n    /** Especialización de la clase COL_Fuente para almacenar aquellas fuentes constituidas por documentos (documento hipotecario, documentos notariales, documentos históricos, etc.) que documentan la relación entre instancias de interesados y de predios.\n     */\n    CLASS COL_FuenteAdministrativa (ABSTRACT)\n    EXTENDS COL_Fuente =\n      /** Descripción del documento.\n       */\n      !!@ ili2db.dispName = "Observación"\n      Observacion : CharacterString;\n      /** Tipo de documento de fuente administrativa.\n       */\n      !!@ ili2db.dispName = "Tipo"\n      Tipo : MANDATORY COL_FuenteAdministrativaTipo;\n      /** Identificador del documento, ejemplo: numero de la resolución\n       */\n      !!@ ili2db.dispName = "Número de fuente"\n      Numero_Fuente : TEXT*150;\n    END COL_FuenteAdministrativa;\n\n    /** Traducción al español de la clase LA_SpatialUnit de LADM.\n     */\n    CLASS COL_UnidadEspacial (ABSTRACT)\n    EXTENDS ObjetoVersionado =\n      !!@ ili2db.dispName = "Área"\n      Area : LIST {0..*} OF LADM_COL_V1_6.LADM_Nucleo.COL_AreaValor;\n      !!@ ili2db.dispName = "Dimensión"\n      Dimension : COL_DimensionTipo;\n      /** Corresponde al atributo extAddressID de la clase en LADM.\n       */\n      !!@ ili2db.dispName = "Ext dirección id"\n      Ext_Direccion_ID : LIST {0..*} OF LADM_COL_V1_6.LADM_Nucleo.ExtDireccion;\n      /** Corresponde al atributo label de la clase en LADM.\n       */\n      !!@ ili2db.dispName = "Etiqueta"\n      Etiqueta : CharacterString;\n      /** Corresponde al atributo surfaceRelation de la clase en LADM.\n       */\n      !!@ ili2db.dispName = "Relación superficie"\n      Relacion_Superficie : COL_RelacionSuperficieTipo;\n      /** Corresponde al atributo volume de la clase en LADM.\n       */\n      !!@ ili2db.dispName = "Volumen"\n      Volumen : LIST {0..*} OF LADM_COL_V1_6.LADM_Nucleo.COL_VolumenValor;\n      /** Materializacion del metodo createArea(). Almacena de forma permanente la geometría de tipo poligonal.\n       */\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface3D;\n    END COL_UnidadEspacial;\n\n    /** Agrupa unidades espaciales, es decir, representaciones geográficas de las unidades administrativas básicas (clase LA_BAUnit) para representar otras unidades espaciales que se forman en base a estas, como puede ser el caso de los polígonos catastrales.\n     */\n    CLASS COL_AgrupacionUnidadesEspaciales (ABSTRACT)\n    EXTENDS ObjetoVersionado =\n      /** Nivel jerárquico de la agrupación, dentro del anidamiento de diferentes agrupaciones.\n       */\n      !!@ ili2db.dispName = "Nivel jerárquico"\n      Nivel_Jerarquico : MANDATORY Integer;\n      /** Definición de la agrupación.\n       */\n      !!@ ili2db.dispName = "Etiqueta"\n      Etiqueta : CharacterString;\n      /** Nombre que recibe la agrupación.\n       */\n      !!@ ili2db.dispName = "Nombre"\n      Nombre : CharacterString;\n      /** Punto de referencia de toda la agrupación, a modo de centro de masas.\n       */\n      !!@ ili2db.dispName = "Punto de referencia"\n      Punto_Referencia : ISO19107_PLANAS_V1.GM_Point3D;\n    END COL_AgrupacionUnidadesEspaciales;\n\n    /** Traducción al español de la clase LA_LegalSpaceBuildingUnit. Sus intancias son las unidades de edificación\n     */\n    CLASS COL_EspacioJuridicoUnidadEdificacion (ABSTRACT)\n    EXTENDS COL_UnidadEspacial =\n      /** Identificador de la unidad de edificación.\n       */\n      !!@ ili2db.dispName = "Ext unidad edificación física id"\n      Ext_Unidad_Edificacion_Fisica_ID : LADM_COL_V1_6.LADM_Nucleo.ExtUnidadEdificacionFisica;\n      /** Tipo de unidad de edificación de la que se trata.\n       */\n      !!@ ili2db.dispName = "Tipo"\n      Tipo : COL_UnidadEdificacionTipo;\n    END COL_EspacioJuridicoUnidadEdificacion;\n\n    ASSOCIATION col_ueJerarquiaGrupo =\n      agrupacion -<> {0..1} COL_AgrupacionUnidadesEspaciales;\n      elemento -- {0..*} COL_AgrupacionUnidadesEspaciales;\n    END col_ueJerarquiaGrupo;\n\n    /** Traducción al español de la clase LA_LegalSpaceUtilityNetwork. Representa un tipo de unidad espacial (LA_UNidadEspacial) cuyas instancias son las redes de servicios.\n     */\n    CLASS COL_EspacioJuridicoRedServicios (ABSTRACT)\n    EXTENDS COL_UnidadEspacial =\n      /** Identificador de la red física hacia una referencia externa.\n       */\n      !!@ ili2db.dispName = "Ext id red física"\n      ext_ID_Red_Fisica : LADM_COL_V1_6.LADM_Nucleo.ExtRedServiciosFisica;\n      /** Estado de operatividad de la red.\n       */\n      !!@ ili2db.dispName = "Estado"\n      Estado : COL_EstadoRedServiciosTipo;\n      /** Tipo de servicio que presta.\n       */\n      !!@ ili2db.dispName = "Tipo"\n      Tipo : COL_RedServiciosTipo;\n    END COL_EspacioJuridicoRedServicios;\n\n    ASSOCIATION col_ueUeGrupo =\n      parte -- {0..*} COL_UnidadEspacial;\n      todo -- {0..*} COL_AgrupacionUnidadesEspaciales;\n    END col_ueUeGrupo;\n\n    /** Traducción de la clase LA_Level de LADM.\n     */\n    CLASS COL_Nivel (ABSTRACT)\n    EXTENDS ObjetoVersionado =\n      !!@ ili2db.dispName = "Nombre"\n      Nombre : CharacterString;\n      !!@ ili2db.dispName = "Tipo de registro"\n      Registro_Tipo : COL_RegistroTipo;\n      !!@ ili2db.dispName = "Estructura"\n      Estructura : COL_EstructuraTipo;\n      !!@ ili2db.dispName = "Tipo"\n      Tipo : COL_ContenidoNivelTipo;\n    END COL_Nivel;\n\n    /** Traducción al español de la clase LA_RequiredRelationshipSpatialUnit de LADM.\n     */\n    CLASS COL_RelacionNecesariaUnidadesEspaciales (ABSTRACT)\n    EXTENDS ObjetoVersionado =\n      !!@ ili2db.dispName = "Relación"\n      Relacion : MANDATORY COL_ISO19125_Tipo;\n    END COL_RelacionNecesariaUnidadesEspaciales;\n\n    ASSOCIATION col_ueNivel =\n      ue -- {0..*} COL_UnidadEspacial;\n      nivel -- {0..1} COL_Nivel;\n    END col_ueNivel;\n\n    /** Clase abstracta que agrupa los atributos comunes de las clases para los derechos (rights), las responsabilidades (responsabilities) y las restricciones (restrictions).\n     */\n    CLASS COL_DRR (ABSTRACT)\n    EXTENDS ObjetoVersionado =\n      /** Descripción relatical al derecho, la responsabilidad o la restricción.\n       */\n      !!@ ili2db.dispName = "Descripción"\n      Descripcion : CharacterString;\n      /** Indicación de si se activa el constraint (a+b+...+n=100%) de la fracción Compartido.\n       */\n      !!@ ili2db.dispName = "Comprobación si comparte"\n      Comprobacion_Comparte : BOOLEAN;\n      /** Descripción de cual es el uso efectivo.\n       */\n      !!@ ili2db.dispName = "Uso efectivo"\n      Uso_Efectivo : CharacterString;\n    END COL_DRR;\n\n    /** De forma genérica, representa el objeto territorial legal (Catastro 2014) que se gestiona en el modelo, en este caso, la parcela catastral o predio. Es independiente del conocimiento de su realidad espacial y se centra en su existencia conocida y reconocida.\n     */\n    CLASS COL_BAUnit (ABSTRACT)\n    EXTENDS ObjetoVersionado =\n      /** Nombre que recibe la unidad administrativa básica, en muchos casos toponímico, especialmente en terrenos rústicos.\n       */\n      !!@ ili2db.dispName = "Nombre"\n      Nombre : CharacterString;\n      /** Tipo de derecho que la reconoce.\n       */\n      !!@ ili2db.dispName = "Tipo"\n      Tipo : MANDATORY COL_BAUnitTipo;\n    END COL_BAUnit;\n\n    ASSOCIATION col_rrrFuente =\n      fuente_administrativa -- {1..*} COL_FuenteAdministrativa;\n      rrr -- {0..*} COL_DRR;\n    END col_rrrFuente;\n\n    /** Traducción de la clase LA_RequiredRelationshipBAUnit de LADM.\n     */\n    CLASS COL_RelacionNecesariaBAUnits (ABSTRACT)\n    EXTENDS ObjetoVersionado =\n      !!@ ili2db.dispName = "Relación"\n      Relacion : MANDATORY CharacterString;\n    END COL_RelacionNecesariaBAUnits;\n\n    ASSOCIATION col_baunitRrr =\n      unidad -- {1} COL_BAUnit;\n      rrr -- {1..*} COL_DRR;\n    END col_baunitRrr;\n\n    ASSOCIATION col_ueBaunit =\n      ue (EXTERNAL) -- {0..*} COL_UnidadEspacial;\n      baunit -- {0..*} COL_BAUnit;\n    END col_ueBaunit;\n\n    ASSOCIATION col_relacionFuente =\n      fuente_administrativa -- {0..*} COL_FuenteAdministrativa;\n      relacionrequeridaBaunit -- {0..*} COL_RelacionNecesariaBAUnits;\n    END col_relacionFuente;\n\n    ASSOCIATION col_unidadFuente =\n      fuente_administrativa -- {0..*} COL_FuenteAdministrativa;\n      unidad -- {0..*} COL_BAUnit;\n    END col_unidadFuente;\n\n    /** Traducción al español de la clase LA_Point de LADM.\n     */\n    CLASS COL_Punto (ABSTRACT)\n    EXTENDS ObjetoVersionado =\n      !!@ ili2db.dispName = "Posición interpolación"\n      Posicion_Interpolacion : COL_InterpolacionTipo;\n      !!@ ili2db.dispName = "Tipo de punto"\n      PuntoTipo : MANDATORY COL_PuntoTipo;\n      !!@ ili2db.dispName = "Método de producción"\n      MetodoProduccion : COL_MetodoProduccionTipo;\n      !!@ ili2db.dispName = "Transformación y resultado"\n      Transformacion_Y_Resultado : LIST {0..*} OF LADM_COL_V1_6.LADM_Nucleo.COL_Transformacion;\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : MANDATORY ISO19107_PLANAS_V1.GM_Point3D;\n    END COL_Punto;\n\n    /** Especialización de la clase COL_Fuente para almacenar las fuentes constituidas por datos espaciales (entidades geográficas, imágenes de satélite, vuelos fotogramétricos, listados de coordenadas, mapas, planos antiguos o modernos, descripción de localizaciones, etc.) que documentan técnicamente la relación entre instancias de interesados y de predios\n     */\n    CLASS COL_FuenteEspacial (ABSTRACT)\n    EXTENDS COL_Fuente =\n      !!@ ili2db.dispName = "Nombre"\n      Nombre : MANDATORY TEXT*255;\n      !!@ ili2db.dispName = "Tipo"\n      Tipo : MANDATORY COL_FuenteEspacialTipo;\n      !!@ ili2db.dispName = "Descripción"\n      Descripcion : MANDATORY MTEXT;\n      !!@ ili2db.dispName = "Metadato"\n      Metadato : MTEXT;\n    END COL_FuenteEspacial;\n\n    /** Traducción al español de la clase LA_BoundaryFaceString de LADM. Define los linderos y a su vez puede estar definida por una descrición textual o por dos o más puntos. Puede estar asociada a una fuente espacial o más.\n     */\n    CLASS COL_CadenaCarasLimite (ABSTRACT)\n    EXTENDS ObjetoVersionado =\n      /** Geometría lineal que define el lindero. Puede estar asociada a geometrías de tipo punto que definen sus vértices o ser una entidad lineal independiente.\n       */\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_Curve3D;\n      /** Descripción de la localización, cuando esta se basa en texto.\n       */\n      !!@ ili2db.dispName = "Localización textual"\n      Localizacion_Textual : CharacterString;\n    END COL_CadenaCarasLimite;\n\n    /** Traducción de la clase LA_BoundaryFace de LADM. De forma similar a LA_CadenaCarasLindero, representa los límites, pero en este caso permite representación 3D.\n     */\n    CLASS COL_CarasLindero (ABSTRACT)\n    EXTENDS ObjetoVersionado =\n      /** Geometría en 3D del límite o lindero, asociada a putos o a descripciones textuales.\n       */\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface3D;\n      /** Cuando la localización del límte está dada por una descripción textual, aquí se recoge esta.\n       */\n      !!@ ili2db.dispName = "Localización textual"\n      Localizacion_Textual : CharacterString;\n    END COL_CarasLindero;\n\n    ASSOCIATION col_puntoReferencia =\n      ue (EXTERNAL) -- {0..1} COL_UnidadEspacial;\n      punto -- {0..1} COL_Punto;\n    END col_puntoReferencia;\n\n    ASSOCIATION col_puntoFuente =\n      fuente_espacial -- {0..*} COL_FuenteEspacial;\n      punto -- {0..*} COL_Punto;\n    END col_puntoFuente;\n\n    ASSOCIATION col_ueFuente =\n      ue (EXTERNAL) -- {0..*} COL_UnidadEspacial;\n      fuente_espacial -- {0..*} COL_FuenteEspacial;\n    END col_ueFuente;\n\n    ASSOCIATION col_baunitFuente =\n      fuente_espacial -- {0..*} COL_FuenteEspacial;\n      unidad (EXTERNAL) -- {0..*} COL_BAUnit;\n    END col_baunitFuente;\n\n    ASSOCIATION col_relacionFuenteUespacial =\n      fuente_espacial -- {0..*} COL_FuenteEspacial;\n      relacionrequeridaUe (EXTERNAL) -- {0..*} COL_RelacionNecesariaUnidadesEspaciales;\n    END col_relacionFuenteUespacial;\n\n    ASSOCIATION col_cclFuente =\n      ccl -- {0..*} COL_CadenaCarasLimite;\n      fuente_espacial -- {0..*} COL_FuenteEspacial;\n    END col_cclFuente;\n\n    ASSOCIATION col_menosCcl =\n      ccl_menos -- {0..*} COL_CadenaCarasLimite;\n      ue_menos (EXTERNAL) -- {0..*} COL_UnidadEspacial;\n    END col_menosCcl;\n\n    ASSOCIATION col_masCcl =\n      ccl_mas -- {0..*} COL_CadenaCarasLimite;\n      ue_mas (EXTERNAL) -- {0..*} COL_UnidadEspacial;\n    END col_masCcl;\n\n    ASSOCIATION col_puntoCcl =\n      punto -- {2..*} COL_Punto;\n      ccl -- {0..*} COL_CadenaCarasLimite;\n    END col_puntoCcl;\n\n    ASSOCIATION col_clFuente =\n      cl -- {0..*} COL_CarasLindero;\n      fuente_espacial -- {0..*} COL_FuenteEspacial;\n    END col_clFuente;\n\n    ASSOCIATION col_menosCl =\n      cl_menos -- {0..*} COL_CarasLindero;\n      ue_menos (EXTERNAL) -- {0..*} COL_UnidadEspacial;\n    END col_menosCl;\n\n    ASSOCIATION col_masCl =\n      cl_mas -- {0..*} COL_CarasLindero;\n      ue_mas (EXTERNAL) -- {0..*} COL_UnidadEspacial;\n    END col_masCl;\n\n    ASSOCIATION col_puntoCl =\n      punto -- {3..*} COL_Punto;\n      cl -- {0..*} COL_CarasLindero;\n    END col_puntoCl;\n\n    /** Traducción de la clase LA_Party de LADM. Representa a las personas que ejercen derechos y responsabilidades  o sufren restricciones respecto a una BAUnit.\n     */\n    CLASS COL_Interesado (ABSTRACT)\n    EXTENDS ObjetoVersionado =\n      /** Identificador del interesado.\n       */\n      !!@ ili2db.dispName = "Ext PID"\n      ext_PID : LADM_COL_V1_6.LADM_Nucleo.ExtInteresado;\n      /** Nombre del interesado.\n       */\n      !!@ ili2db.dispName = "Nombre"\n      Nombre : CharacterString;\n    END COL_Interesado;\n\n    /** Registra interesados que representan a grupos de personas. Se registra el grupo en si, independientemete de las personas por separado. Es lo que ocurreo, por ejemplo, con un grupo étnico.\n     */\n    CLASS COL_Agrupacion_Interesados (ABSTRACT)\n    EXTENDS COL_Interesado =\n      /** Indica el tipo de agrupación del que se trata.\n       */\n      !!@ ili2db.dispName = "Tipo"\n      Tipo : MANDATORY COL_GrupoInteresadoTipo;\n    END COL_Agrupacion_Interesados;\n\n    ASSOCIATION col_baunitComoInteresado =\n      interesado -- {0..*} COL_Interesado;\n      unidad (EXTERNAL) -- {0..*} COL_BAUnit;\n    END col_baunitComoInteresado;\n\n    ASSOCIATION col_responsableFuente =\n      fuente_administrativa (EXTERNAL) -- {0..*} COL_FuenteAdministrativa;\n      interesado -- {0..*} COL_Interesado;\n    END col_responsableFuente;\n\n    ASSOCIATION col_rrrInteresado =\n      rrr (EXTERNAL) -- {0..*} COL_DRR;\n      interesado -- {0..1} COL_Interesado;\n    END col_rrrInteresado;\n\n    ASSOCIATION col_topografoFuente =\n      fuente_espacial (EXTERNAL) -- {0..*} COL_FuenteEspacial;\n      topografo -- {0..*} COL_Interesado;\n    END col_topografoFuente;\n\n    ASSOCIATION col_miembros =\n      interesado -- {2..*} COL_Interesado;\n      agrupacion -<> {0..*} COL_Agrupacion_Interesados;\n      participacion : LADM_COL_V1_6.LADM_Nucleo.Fraccion;\n    END col_miembros;\n\n  END LADM_Nucleo;\n\nEND LADM_COL_V1_6.\n	2020-01-28 10:16:55.146
ISO19107_PLANAS_V1.ili	2.3	ISO19107_PLANAS_V1	INTERLIS 2.3;\n\nTYPE MODEL ISO19107_PLANAS_V1 (es)\nAT "http://www.swisslm.ch/models"\nVERSION "2016-03-07"  =\n\n  DOMAIN\n\n    GM_Point2D = COORD 165000.000 .. 1806900.000 [INTERLIS.m], 23000.000 .. 1984900.000 [INTERLIS.m] ,ROTATION 2 -> 1;\n\n    GM_Curve2D = POLYLINE WITH (ARCS,STRAIGHTS) VERTEX GM_Point2D WITHOUT OVERLAPS>0.001;\n\n    GM_Surface2D = SURFACE WITH (ARCS,STRAIGHTS) VERTEX GM_Point2D WITHOUT OVERLAPS>0.001;\n\n    GM_Point3D = COORD 165000.000 .. 1806900.000 [INTERLIS.m], 23000.000 .. 1984900.000 [INTERLIS.m], -5000.000 .. 6000.000 [INTERLIS.m] ,ROTATION 2 -> 1;\n\n    GM_Curve3D = POLYLINE WITH (ARCS,STRAIGHTS) VERTEX GM_Point3D WITHOUT OVERLAPS>0.001;\n\n    GM_Surface3D = SURFACE WITH (ARCS,STRAIGHTS) VERTEX GM_Point3D WITHOUT OVERLAPS>0.001;\n\n  STRUCTURE GM_Geometry2DListValue =\n  END GM_Geometry2DListValue;\n\n  STRUCTURE GM_Curve2DListValue =\n    value : MANDATORY GM_Curve2D;\n  END GM_Curve2DListValue;\n\n  STRUCTURE GM_Surface2DListValue =\n    value : MANDATORY GM_Surface2D;\n  END GM_Surface2DListValue;\n\n  !!@ ili2db.mapping = "MultiLine"\nSTRUCTURE GM_MultiCurve2D =\n    geometry : LIST {1..*} OF ISO19107_PLANAS_V1.GM_Curve2DListValue;\n  END GM_MultiCurve2D;\n\n  !!@ ili2db.mapping = "MultiSurface"\nSTRUCTURE GM_MultiSurface2D =\n    geometry : LIST {1..*} OF ISO19107_PLANAS_V1.GM_Surface2DListValue;\n  END GM_MultiSurface2D;\n\n  STRUCTURE GM_Curve3DListValue =\n    value : MANDATORY GM_Curve3D;\n  END GM_Curve3DListValue;\n\n  STRUCTURE GM_Surface3DListValue =\n    value : MANDATORY GM_Surface3D;\n  END GM_Surface3DListValue;\n\n  !!@ ili2db.mapping = "MultiLine"\nSTRUCTURE GM_MultiCurve3D =\n    geometry : LIST {1..*} OF ISO19107_PLANAS_V1.GM_Curve3DListValue;\n  END GM_MultiCurve3D;\n\n  !!@ ili2db.mapping = "MultiSurface"\nSTRUCTURE GM_MultiSurface3D =\n    geometry : LIST {1..*} OF ISO19107_PLANAS_V1.GM_Surface3DListValue;\n  END GM_MultiSurface3D;\n\nEND ISO19107_PLANAS_V1.\n	2020-01-28 10:16:55.146
Insumos_V2_10.ili	2.3	Datos_Gestor_Catastral_V2_10{ ISO19107_PLANAS_V1 LADM_COL_V1_6} Datos_SNR_V2_10{ LADM_COL_V1_6} Datos_Integracion_Insumos_V2_10{ Datos_SNR_V2_10 Datos_Gestor_Catastral_V2_10}	INTERLIS 2.3;\n\nMODEL Datos_Gestor_Catastral_V2_10 (es)\nAT "mailto:PC4@localhost"\nVERSION "2019-08-01"  =\n  IMPORTS ISO19107_PLANAS_V1,LADM_COL_V1_6;\n\n  DOMAIN\n\n    GC_CondicionPredioTipo = (\n      !!@ ili2db.dispName = "No propiedad horizontal"\n      NPH,\n      !!@ ili2db.dispName = "Propiedad horizontal"\n      PH(\n        Matriz,\n        Unidad_Predial\n      ),\n      !!@ ili2db.dispName = "Condiminio"\n      Condominio(\n        Matriz,\n        Unidad_Predial\n      ),\n      !!@ ili2db.dispName = "Mejora"\n      Mejora(\n        PH,\n        NPH\n      ),\n      !!@ ili2db.dispName = "Parque cementerio"\n      Parque_Cementerio(\n        Matriz,\n        Unidad_Predial\n      ),\n      !!@ ili2db.dispName = "Vía"\n      Via,\n      !!@ ili2db.dispName = "Bien de uso público"\n      Bien_Uso_Publico\n    );\n\n    GC_SistemaProcedenciaDatosTipo = (\n      !!@ ili2db.dispName = "Sistema Nacional Catastral"\n      SNC,\n      !!@ ili2db.dispName = "Cobol"\n      Cobol\n    );\n\n    GC_UnidadConstruccionTipo = (\n      !!@ ili2db.dispName = "Convencional"\n      Convencional,\n      !!@ ili2db.dispName = "No convencional"\n      No_Convencional\n    );\n\n  !!@ ili2db.dispName = "(GC) Dirección"\n  STRUCTURE GC_Direccion =\n    !!@ ili2db.dispName = "Valor"\n    Valor : TEXT*255;\n    !!@ ili2db.dispName = "Principal"\n    Principal : BOOLEAN;\n    !!@ ili2db.dispName = "Geometría de referencia"\n    Geometria_Referencia : ISO19107_PLANAS_V1.GM_Curve3D;\n  END GC_Direccion;\n\n  TOPIC Datos_Gestor_Catastral =\n\n    !!@ ili2db.dispName = "(GC) Barrio"\n    CLASS GC_Barrio =\n      !!@ ili2db.dispName = "Código"\n      Codigo : TEXT*13;\n      !!@ ili2db.dispName = "Nombre"\n      Nombre : TEXT*100;\n      !!@ ili2db.dispName = "Código sector"\n      Codigo_Sector : TEXT*9;\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface2D;\n    END GC_Barrio;\n\n    !!@ ili2db.dispName = "(GC) Comisiones Construcción"\n    CLASS GC_Comisiones_Construccion =\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface3D;\n    END GC_Comisiones_Construccion;\n\n    !!@ ili2db.dispName = "(GC) Comisiones Terreno"\n    CLASS GC_Comisiones_Terreno =\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface2D;\n    END GC_Comisiones_Terreno;\n\n    !!@ ili2db.dispName = "(GC) Comisiones Unidad Construcción"\n    CLASS GC_Comisiones_Unidad_Construccion =\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface3D;\n    END GC_Comisiones_Unidad_Construccion;\n\n    !!@ ili2db.dispName = "(GC) Construcción"\n    CLASS GC_Construccion =\n      !!@ ili2db.dispName = "Identificador"\n      Identificador : TEXT*30;\n      !!@ ili2db.dispName = "Etiqueta"\n      Etiqueta : TEXT*50;\n      !!@ ili2db.dispName = "Tipo de construcción"\n      Tipo_Construccion : Datos_Gestor_Catastral_V2_10.GC_UnidadConstruccionTipo;\n      !!@ ili2db.dispName = "Tipo de dominio"\n      Tipo_Dominio : TEXT*20;\n      !!@ ili2db.dispName = "Número de pisos"\n      Numero_Pisos : 0 .. 200;\n      !!@ ili2db.dispName = "Número de sótanos"\n      Numero_Sotanos : 0 .. 99;\n      !!@ ili2db.dispName = "Número de mezanines"\n      Numero_Mezanines : 0 .. 99;\n      !!@ ili2db.dispName = "Número de semisótanos"\n      Numero_Semisotanos : 0 .. 99;\n      !!@ ili2db.dispName = "Código de edificación"\n      Codigo_Edificacion : 0 .. 10000000000000000000;\n      !!@ ili2db.dispName = "Código de terreno"\n      Codigo_Terreno : TEXT*30;\n      !!@ ili2db.dispName = "Área construida"\n      Area_Construida : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface3D;\n    END GC_Construccion;\n\n    !!@ ili2db.dispName = "(GC) Datos Propiedad Horizontal Condominio"\n    CLASS GC_Datos_PH_Condiminio =\n      !!@ ili2db.dispName = "Área total de terreno"\n      Area_Total_Terreno : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Área total de terreno privada"\n      Area_Total_Terreno_Privada : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Área total de terreno común"\n      Area_Total_Terreno_Comun : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Área total construida"\n      Area_Total_Construida : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Área total construida privada"\n      Area_Total_Construida_Privada : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Área total construida común"\n      Area_Total_Construida_Comun : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Torre número"\n      Torre_No : TEXT*10;\n      !!@ ili2db.dispName = "Total pisos de torre"\n      Total_Pisos_Torre : 0 .. 200;\n      !!@ ili2db.dispName = "Total de unidades privadas"\n      Total_Unidades_Privadas : 0 .. 99999999;\n      !!@ ili2db.dispName = "Total de sótanos"\n      Total_Sotanos : 0 .. 30;\n      !!@ ili2db.dispName = "Total de unidades de sótano"\n      Total_Unidades_Sotano : 0 .. 99999999;\n    END GC_Datos_PH_Condiminio;\n\n    !!@ ili2db.dispName = "(GC) Manzana"\n    CLASS GC_Manzana =\n      !!@ ili2db.dispName = "Código"\n      Codigo : TEXT*17;\n      !!@ ili2db.dispName = "Código anterior"\n      Codigo_Anterior : TEXT*255;\n      !!@ ili2db.dispName = "Código de barrio"\n      Codigo_Barrio : TEXT*13;\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface2D;\n    END GC_Manzana;\n\n    !!@ ili2db.dispName = "(GC) Perímetro"\n    CLASS GC_Perimetro =\n      !!@ ili2db.dispName = "Código del departamento"\n      Codigo_Departamento : TEXT*2;\n      !!@ ili2db.dispName = "Código del municipio"\n      Codigo_Municipio : TEXT*5;\n      !!@ ili2db.dispName = "Tipo de avalúo"\n      Tipo_Avaluo : TEXT*30;\n      !!@ ili2db.dispName = "Nombre geográfico"\n      Nombre_Geografico : TEXT*50;\n      !!@ ili2db.dispName = "Código nombre"\n      Codigo_Nombre : TEXT*255;\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface2D;\n    END GC_Perimetro;\n\n    /** Datos del propietario en catastro\n     */\n    !!@ ili2db.dispName = "(GC) Predio Catastro"\n    CLASS GC_Predio_Catastro =\n      !!@ ili2db.dispName = "Tipo de catastro"\n      Tipo_Catastro : TEXT*255;\n      !!@ ili2db.dispName = "Número predial"\n      Numero_Predial : TEXT*30;\n      !!@ ili2db.dispName = "Número predial anterior"\n      Numero_Predial_Anterior : TEXT*20;\n      !!@ ili2db.dispName = "Círculo registral"\n      Circulo_Registral : TEXT*4;\n      !!@ ili2db.dispName = "Matrícula inmobiliaria catastro"\n      Matricula_Inmobiliaria_Catastro : TEXT*80;\n      !!@ ili2db.dispName = "Direcciones"\n      Direcciones : BAG {0..*} OF Datos_Gestor_Catastral_V2_10.GC_Direccion;\n      !!@ ili2db.dispName = "Tipo de predio"\n      Tipo_Predio : TEXT*100;\n      !!@ ili2db.dispName = "Condición del predio"\n      Condicion_Predio : Datos_Gestor_Catastral_V2_10.GC_CondicionPredioTipo;\n      !!@ ili2db.dispName = "Destinación económica"\n      Destinacion_Economica : TEXT*150;\n      !!@ ili2db.dispName = "Estado alerta"\n      Estado_Alerta : TEXT*30;\n      !!@ ili2db.dispName = "Entidad emisora de la alerta"\n      Entidad_Emisora_Alerta : TEXT*255;\n      !!@ ili2db.dispName = "Fecha de alerta"\n      Fecha_Alerta : INTERLIS.XMLDate;\n      !!@ ili2db.dispName = "Sistema procedencia de los datos"\n      Sistema_Procedencia_Datos : Datos_Gestor_Catastral_V2_10.GC_SistemaProcedenciaDatosTipo;\n      !!@ ili2db.dispName = "Fecha de los datos"\n      Fecha_Datos : MANDATORY INTERLIS.XMLDate;\n    END GC_Predio_Catastro;\n\n    /** Datos del propietario en catastro\n     */\n    !!@ ili2db.dispName = "(GC) Propietario"\n    CLASS GC_Propietario =\n      !!@ ili2db.dispName = "Tipo de documento"\n      Tipo_Documento : TEXT*100;\n      !!@ ili2db.dispName = "Número de documento"\n      Numero_Documento : TEXT*50;\n      !!@ ili2db.dispName = "Dígito de verificación"\n      Digito_Verificacion : TEXT*1;\n      !!@ ili2db.dispName = "Primer nombre"\n      Primer_Nombre : TEXT*255;\n      !!@ ili2db.dispName = "Segundo nombre"\n      Segundo_Nombre : TEXT*255;\n      !!@ ili2db.dispName = "Primer apellido"\n      Primer_Apellido : TEXT*255;\n      !!@ ili2db.dispName = "Segundo apellido"\n      Segundo_Apellido : TEXT*255;\n      !!@ ili2db.dispName = "Razón social"\n      Razon_Social : TEXT*255;\n    END GC_Propietario;\n\n    !!@ ili2db.dispName = "(GC) Sector Rural"\n    CLASS GC_Sector_Rural =\n      !!@ ili2db.dispName = "Código"\n      Codigo : TEXT*9;\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface2D;\n    END GC_Sector_Rural;\n\n    !!@ ili2db.dispName = "(GC) Sector Urbano"\n    CLASS GC_Sector_Urbano =\n      !!@ ili2db.dispName = "Código"\n      Codigo : TEXT*9;\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface2D;\n    END GC_Sector_Urbano;\n\n    /** Datos del terreno, asociado al predio en catastro\n     */\n    !!@ ili2db.dispName = "(GC) Terreno"\n    CLASS GC_Terreno =\n      !!@ ili2db.dispName = "Área terreno alfanumérica"\n      Area_Terreno_Alfanumerica : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Área terreno digital"\n      Area_Terreno_Digital : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Código de manzana vereda"\n      Manzana_Vereda_Codigo : TEXT*17;\n      !!@ ili2db.dispName = "Número de subterráneos"\n      Numero_Subterraneos : 0 .. 999999999999999;\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface2D;\n    END GC_Terreno;\n\n    !!@ ili2db.dispName = "(GC) Unidad Construcción"\n    CLASS GC_Unidad_Construccion =\n      !!@ ili2db.dispName = "Identificador"\n      Identificador : TEXT*2;\n      !!@ ili2db.dispName = "Etiqueta"\n      Etiqueta : TEXT*50;\n      !!@ ili2db.dispName = "Tipo de dominio"\n      Tipo_Dominio : TEXT*20;\n      !!@ ili2db.dispName = "Tipo de construcción"\n      Tipo_Construccion : Datos_Gestor_Catastral_V2_10.GC_UnidadConstruccionTipo;\n      !!@ ili2db.dispName = "Planta"\n      Planta : TEXT*10;\n      !!@ ili2db.dispName = "Total de habitaciones"\n      Total_Habitaciones : 0 .. 999999;\n      !!@ ili2db.dispName = "Total de baños"\n      Total_Banios : 0 .. 999999;\n      !!@ ili2db.dispName = "Total de locales"\n      Total_Locales : 0 .. 999999;\n      !!@ ili2db.dispName = "Total de pisos"\n      Total_Pisos : 0 .. 150;\n      !!@ ili2db.dispName = "Uso"\n      Uso : TEXT*255;\n      !!@ ili2db.dispName = "Año de construcción"\n      Anio_Construccion : 1512 .. 2500;\n      !!@ ili2db.dispName = "Puntaje"\n      Puntaje : 0 .. 200;\n      !!@ ili2db.dispName = "Área construida"\n      Area_Construida : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Área privada"\n      Area_Privada : 0.00 .. 99999999999999.98 [LADM_COL_V1_6.m2];\n      !!@ ili2db.dispName = "Código terreno"\n      Codigo_Terreno : TEXT*30;\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface3D;\n    END GC_Unidad_Construccion;\n\n    !!@ ili2db.dispName = "(GC) Vereda"\n    CLASS GC_Vereda =\n      !!@ ili2db.dispName = "Código"\n      Codigo : TEXT*17;\n      !!@ ili2db.dispName = "Código anterior"\n      Codigo_Anterior : TEXT*13;\n      !!@ ili2db.dispName = "Nombre"\n      Nombre : TEXT*100;\n      !!@ ili2db.dispName = "Código del sector"\n      Codigo_Sector : TEXT*9;\n      !!@ ili2db.dispName = "Geometría"\n      Geometria : ISO19107_PLANAS_V1.GM_MultiSurface2D;\n    END GC_Vereda;\n\n    ASSOCIATION gc_construccion_predio =\n      gc_predio -- {1} GC_Predio_Catastro;\n      gc_construccion -- {0..*} GC_Construccion;\n    END gc_construccion_predio;\n\n    ASSOCIATION gc_construccion_unidad =\n      gc_unidad_construccion -- {0..*} GC_Unidad_Construccion;\n      gc_construccion -- {1} GC_Construccion;\n    END gc_construccion_unidad;\n\n    ASSOCIATION gc_copropiedad =\n      gc_matriz -<> {0..1} GC_Predio_Catastro;\n      gc_unidad -- {0..*} GC_Predio_Catastro;\n      Coeficiente_Copropiedad : 0.0000000 .. 100.0000000;\n    END gc_copropiedad;\n\n    ASSOCIATION gc_ph_predio =\n      gc_predio -- {1} GC_Predio_Catastro;\n      gc_datos_ph -- {0..1} GC_Datos_PH_Condiminio;\n    END gc_ph_predio;\n\n    ASSOCIATION gc_propietario_predio =\n      gc_predio_catastro -- {1} GC_Predio_Catastro;\n      gc_propietario -- {0..*} GC_Propietario;\n    END gc_propietario_predio;\n\n    ASSOCIATION gc_terreno_predio =\n      gc_predio -- {1} GC_Predio_Catastro;\n      gc_terreno -- {0..*} GC_Terreno;\n    END gc_terreno_predio;\n\n  END Datos_Gestor_Catastral;\n\nEND Datos_Gestor_Catastral_V2_10.\n\nMODEL Datos_SNR_V2_10 (es)\nAT "http://www.proadmintierra.info/"\nVERSION "V2.3"  // 2019-07-31 // =\n  IMPORTS LADM_COL_V1_6;\n\n  DOMAIN\n\n    SNR_CalidadDerechoTipo = (\n      !!@ ili2db.dispName = "Dominio"\n      Dominio,\n      !!@ ili2db.dispName = "Falsa tradición"\n      Falsa_Tradicion,\n      !!@ ili2db.dispName = "Nuda propiedad"\n      Nuda_Propiedad,\n      !!@ ili2db.dispName = "Propiedad colectiva"\n      Propiedad_Colectiva,\n      !!@ ili2db.dispName = "Usufructo"\n      Usufructo\n    );\n\n    SNR_DocumentoTitularTipo = (\n      !!@ ili2db.dispName = "Cédula de ciudadanía"\n      Cedula_Ciudadania,\n      !!@ ili2db.dispName = "Cédula de extranjería"\n      Cedula_Extranjeria,\n      !!@ ili2db.dispName = "NIT"\n      NIT,\n      !!@ ili2db.dispName = "Pasaporte"\n      Pasaporte,\n      !!@ ili2db.dispName = "Tarjeta de identidad"\n      Tarjeta_Identidad,\n      !!@ ili2db.dispName = "Libreta militar"\n      Libreta_Militar,\n      !!@ ili2db.dispName = "Registro civil"\n      Registro_Civil,\n      !!@ ili2db.dispName = "Cédula militar"\n      Cedula_Militar,\n      !!@ ili2db.dispName = "NUIP"\n      NUIP,\n      !!@ ili2db.dispName = "Secuencial SNR"\n      Secuencial_SNR\n    );\n\n    SNR_FuenteTipo = (\n      !!@ ili2db.dispName = "Acto administrativo"\n      Acto_Administrativo,\n      !!@ ili2db.dispName = "Escritura pública"\n      Escritura_Publica,\n      !!@ ili2db.dispName = "Sentencia judicial"\n      Sentencia_Judicial\n    );\n\n    SNR_PersonaTitularTipo = (\n      !!@ ili2db.dispName = "Persona natural"\n      Persona_Natural,\n      !!@ ili2db.dispName = "Persona jurídica"\n      Persona_Juridica\n    );\n\n  TOPIC Datos_SNR =\n\n    !!@ ili2db.dispName = "(SNR) Derecho"\n    CLASS SNR_Derecho =\n      /** Calidad de derecho en registro\n       */\n      !!@ ili2db.dispName = "Calidad derecho registro"\n      Calidad_Derecho_Registro : MANDATORY Datos_SNR_V2_10.SNR_CalidadDerechoTipo;\n      !!@ ili2db.dispName = "Código naturaleza jurídica"\n      Codigo_Naturaleza_Juridica : TEXT*5;\n    END SNR_Derecho;\n\n    !!@ ili2db.dispName = "(SNR) Fuente Cabida Linderos"\n    CLASS SNR_Fuente_CabidaLinderos =\n      !!@ ili2db.dispName = "Tipo de documento"\n      Tipo_Documento : Datos_SNR_V2_10.SNR_FuenteTipo;\n      !!@ ili2db.dispName = "Número de documento"\n      Numero_Documento : TEXT*255;\n      !!@ ili2db.dispName = "Fecha de documento"\n      Fecha_Documento : INTERLIS.XMLDate;\n      !!@ ili2db.dispName = "Ente emisor"\n      Ente_Emisor : TEXT*255;\n      !!@ ili2db.dispName = "Ciudad emisora"\n      Ciudad_Emisora : TEXT*255;\n      !!@ ili2db.dispName = "Archivo"\n      Archivo : LADM_COL_V1_6.LADM_Nucleo.ExtArchivo;\n    END SNR_Fuente_CabidaLinderos;\n\n    /** Datos del documento que soporta el derecho\n     */\n    !!@ ili2db.dispName = "(SNR) Fuente Derecho"\n    CLASS SNR_Fuente_Derecho =\n      !!@ ili2db.dispName = "Tipo de documento"\n      Tipo_Documento : Datos_SNR_V2_10.SNR_FuenteTipo;\n      !!@ ili2db.dispName = "Número de documento"\n      Numero_Documento : TEXT*255;\n      !!@ ili2db.dispName = "Fecha del documento"\n      Fecha_Documento : INTERLIS.XMLDate;\n      !!@ ili2db.dispName = "Ente emisor"\n      Ente_Emisor : MTEXT*255;\n      !!@ ili2db.dispName = "Ciudad emisora"\n      Ciudad_Emisora : TEXT*255;\n    END SNR_Fuente_Derecho;\n\n    /** Datos del predio entregados por registro\n     */\n    !!@ ili2db.dispName = "(SNR) Predio Registro"\n    CLASS SNR_Predio_Registro =\n      !!@ ili2db.dispName = "Código ORIP"\n      Codigo_ORIP : TEXT*3;\n      !!@ ili2db.dispName = "Matrícula inmobiliaria"\n      Matricula_Inmobiliaria : TEXT*80;\n      !!@ ili2db.dispName = "Número predial nuevo en FMI"\n      Numero_Predial_Nuevo_en_FMI : TEXT*30;\n      !!@ ili2db.dispName = "Número predial anterior en FMI"\n      Numero_Predial_Anterior_en_FMI : TEXT*30;\n      !!@ ili2db.dispName = "Cabida y linderos"\n      Cabida_Linderos : MTEXT;\n      /** Matricula inmobiliaria matriz, cuando aplique\n       */\n      !!@ ili2db.dispName = "Matrícula inmobiliaria matriz"\n      Matricula_Inmobiliaria_Matriz : TEXT*80;\n      !!@ ili2db.dispName = "Fecha de datos"\n      Fecha_Datos : MANDATORY INTERLIS.XMLDate;\n    END SNR_Predio_Registro;\n\n    /** Datos de titulares de derecho en registro\n     */\n    !!@ ili2db.dispName = "(SNR) Titular"\n    CLASS SNR_Titular =\n      /** Tipo de persona\n       */\n      !!@ ili2db.dispName = "Tipo de persona"\n      Tipo_Persona : Datos_SNR_V2_10.SNR_PersonaTitularTipo;\n      !!@ ili2db.dispName = "Tipo de documento"\n      Tipo_Documento : Datos_SNR_V2_10.SNR_DocumentoTitularTipo;\n      !!@ ili2db.dispName = "Número de documento"\n      Numero_Documento : MANDATORY TEXT*50;\n      !!@ ili2db.dispName = "Nombres"\n      Nombres : TEXT*500;\n      !!@ ili2db.dispName = "Primer apellido"\n      Primer_Apellido : TEXT*255;\n      !!@ ili2db.dispName = "Segundo apellido"\n      Segundo_Apellido : TEXT*255;\n      !!@ ili2db.dispName = "Razón social"\n      Razon_Social : MTEXT*255;\n    END SNR_Titular;\n\n    ASSOCIATION snr_derecho_predio =\n      snr_predio_registro -- {1} SNR_Predio_Registro;\n      snr_derecho -- {1..*} SNR_Derecho;\n    END snr_derecho_predio;\n\n    ASSOCIATION snr_fuente_cabidalinderos =\n      snr_predio_registro -- {0..*} SNR_Predio_Registro;\n      snr_fuente_cabidalinderos -- {0..1} SNR_Fuente_CabidaLinderos;\n    END snr_fuente_cabidalinderos;\n\n    ASSOCIATION snr_fuente_derecho =\n      snr_derecho -- {1..*} SNR_Derecho;\n      snr_fuente_derecho -- {1} SNR_Fuente_Derecho;\n    END snr_fuente_derecho;\n\n    ASSOCIATION snr_titular_derecho =\n      snr_titular -- {1..*} SNR_Titular;\n      snr_derecho -- {1..*} SNR_Derecho;\n      Porcentaje_Participacion : 0 .. 100;\n    END snr_titular_derecho;\n\n  END Datos_SNR;\n\nEND Datos_SNR_V2_10.\n\nMODEL Datos_Integracion_Insumos_V2_10 (es)\nAT "mailto:PC4@localhost"\nVERSION "2019-09-06"  =\n  IMPORTS Datos_Gestor_Catastral_V2_10,Datos_SNR_V2_10;\n\n  TOPIC Datos_Integracion_Insumos =\n    DEPENDS ON Datos_SNR_V2_10.Datos_SNR,Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral;\n\n    !!@ ili2db.dispName = "(Integración Insumos) Predio Insumos"\n    CLASS INI_Predio_Insumos =\n    END INI_Predio_Insumos;\n\n    ASSOCIATION ini_predio_integracion_gc =\n      gc_predio_catastro (EXTERNAL) -- {0..1} Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro;\n      ini_predio_insumos -- {0..*} INI_Predio_Insumos;\n    END ini_predio_integracion_gc;\n\n    ASSOCIATION ini_predio_integracion_snr =\n      snr_predio_juridico (EXTERNAL) -- {0..1} Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro;\n      ini_predio -- {0..*} INI_Predio_Insumos;\n    END ini_predio_integracion_snr;\n\n  END Datos_Integracion_Insumos;\n\nEND Datos_Integracion_Insumos_V2_10.\n	2020-01-28 10:16:55.146
\.


--
-- TOC entry 12703 (class 0 OID 339638)
-- Dependencies: 2269
-- Data for Name: t_ili2db_settings; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.t_ili2db_settings (tag, setting) FROM stdin;
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
ch.interlis.ili2c.ilidirs	/home/ai/Desktop/LADM_COL/Catastro_Multiproposito/Operacion;/home/ai/Desktop/LADM_COL/ISO
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
-- TOC entry 12704 (class 0 OID 339644)
-- Dependencies: 2270
-- Data for Name: t_ili2db_table_prop; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.t_ili2db_table_prop (tablename, tag, setting) FROM stdin;
col_puntotipo	ch.ehi.ili2db.tableKind	ENUM
extdireccion	ch.ehi.ili2db.tableKind	STRUCTURE
extdireccion	ch.ehi.ili2db.dispName	Dirección
col_fuenteadministrativatipo	ch.ehi.ili2db.tableKind	ENUM
ini_predio_insumos	ch.ehi.ili2db.tableKind	CLASS
ini_predio_insumos	ch.ehi.ili2db.dispName	(Integración Insumos) Predio Insumos
gc_unidadconstrucciontipo	ch.ehi.ili2db.tableKind	ENUM
col_contenidoniveltipo	ch.ehi.ili2db.tableKind	ENUM
col_mascl	ch.ehi.ili2db.tableKind	ASSOCIATION
op_predio	ch.ehi.ili2db.tableKind	CLASS
op_predio	ch.ehi.ili2db.dispName	Predio
col_unidadedificaciontipo	ch.ehi.ili2db.tableKind	ENUM
op_predio_insumos_operacion	ch.ehi.ili2db.tableKind	ASSOCIATION
col_baunitcomointeresado	ch.ehi.ili2db.tableKind	ASSOCIATION
op_interesado	ch.ehi.ili2db.tableKind	CLASS
op_interesado	ch.ehi.ili2db.dispName	Interesado
col_baunittipo	ch.ehi.ili2db.tableKind	ENUM
col_metodoproducciontipo	ch.ehi.ili2db.tableKind	ENUM
op_fuenteadministrativa	ch.ehi.ili2db.tableKind	CLASS
op_fuenteadministrativa	ch.ehi.ili2db.dispName	Fuente Administrativa
snr_predio_registro	ch.ehi.ili2db.tableKind	CLASS
snr_predio_registro	ch.ehi.ili2db.dispName	(SNR) Predio Registro
ci_forma_presentacion_codigo	ch.ehi.ili2db.tableKind	ENUM
col_unidadfuente	ch.ehi.ili2db.tableKind	ASSOCIATION
col_responsablefuente	ch.ehi.ili2db.tableKind	ASSOCIATION
gm_surface2dlistvalue	ch.ehi.ili2db.tableKind	STRUCTURE
imagen	ch.ehi.ili2db.tableKind	STRUCTURE
col_volumenvalor	ch.ehi.ili2db.tableKind	STRUCTURE
op_restricciontipo	ch.ehi.ili2db.tableKind	ENUM
col_baunitfuente	ch.ehi.ili2db.tableKind	ASSOCIATION
col_uefuente	ch.ehi.ili2db.tableKind	ASSOCIATION
snr_titular	ch.ehi.ili2db.tableKind	CLASS
snr_titular	ch.ehi.ili2db.dispName	(SNR) Titular
gc_sector_urbano	ch.ehi.ili2db.tableKind	CLASS
gc_sector_urbano	ch.ehi.ili2db.dispName	(GC) Sector Urbano
col_transformacion	ch.ehi.ili2db.tableKind	STRUCTURE
gc_barrio	ch.ehi.ili2db.tableKind	CLASS
gc_barrio	ch.ehi.ili2db.dispName	(GC) Barrio
col_menoscl	ch.ehi.ili2db.tableKind	ASSOCIATION
col_estadodisponibilidadtipo	ch.ehi.ili2db.tableKind	ENUM
col_registrotipo	ch.ehi.ili2db.tableKind	ENUM
col_miembros	ch.ehi.ili2db.tableKind	ASSOCIATION
col_estadoredserviciostipo	ch.ehi.ili2db.tableKind	ENUM
extdireccion_sector_predio	ch.ehi.ili2db.tableKind	ENUM
extredserviciosfisica	ch.ehi.ili2db.tableKind	STRUCTURE
op_restriccion	ch.ehi.ili2db.tableKind	CLASS
op_restriccion	ch.ehi.ili2db.dispName	Restricción
snr_fuentetipo	ch.ehi.ili2db.tableKind	ENUM
op_derecho	ch.ehi.ili2db.tableKind	CLASS
op_derecho	ch.ehi.ili2db.dispName	Derecho
gc_direccion	ch.ehi.ili2db.tableKind	STRUCTURE
gc_direccion	ch.ehi.ili2db.dispName	(GC) Dirección
op_derechotipo	ch.ehi.ili2db.tableKind	ENUM
extdireccion_sector_ciudad	ch.ehi.ili2db.tableKind	ENUM
op_predio_copropiedad	ch.ehi.ili2db.tableKind	ASSOCIATION
op_construcciontipo	ch.ehi.ili2db.tableKind	ENUM
op_fuenteadministrativatipo	ch.ehi.ili2db.tableKind	ENUM
gc_comisiones_construccion	ch.ehi.ili2db.tableKind	CLASS
gc_comisiones_construccion	ch.ehi.ili2db.dispName	(GC) Comisiones Construcción
gc_propietario	ch.ehi.ili2db.tableKind	CLASS
gc_propietario	ch.ehi.ili2db.dispName	(GC) Propietario
op_fuenteespacial	ch.ehi.ili2db.tableKind	CLASS
op_fuenteespacial	ch.ehi.ili2db.dispName	Fuente Espacial
op_construccionplantatipo	ch.ehi.ili2db.tableKind	ENUM
snr_calidadderechotipo	ch.ehi.ili2db.tableKind	ENUM
op_dominioconstrucciontipo	ch.ehi.ili2db.tableKind	ENUM
col_puntoccl	ch.ehi.ili2db.tableKind	ASSOCIATION
col_estructuratipo	ch.ehi.ili2db.tableKind	ENUM
op_grupoetnicotipo	ch.ehi.ili2db.tableKind	ENUM
col_grupointeresadotipo	ch.ehi.ili2db.tableKind	ENUM
gc_condicionprediotipo	ch.ehi.ili2db.tableKind	ENUM
extdireccion_tipo_direccion	ch.ehi.ili2db.tableKind	ENUM
col_volumentipo	ch.ehi.ili2db.tableKind	ENUM
op_unidadconstruccion	ch.ehi.ili2db.tableKind	CLASS
op_unidadconstruccion	ch.ehi.ili2db.dispName	Unidad de Construcción
op_acuerdotipo	ch.ehi.ili2db.tableKind	ENUM
gc_manzana	ch.ehi.ili2db.tableKind	CLASS
gc_manzana	ch.ehi.ili2db.dispName	(GC) Manzana
col_uebaunit	ch.ehi.ili2db.tableKind	ASSOCIATION
col_relacionfuente	ch.ehi.ili2db.tableKind	ASSOCIATION
op_usouconstipo	ch.ehi.ili2db.tableKind	ENUM
snr_personatitulartipo	ch.ehi.ili2db.tableKind	ENUM
gc_datos_ph_condiminio	ch.ehi.ili2db.tableKind	CLASS
gc_datos_ph_condiminio	ch.ehi.ili2db.dispName	(GC) Datos Propiedad Horizontal Condominio
snr_fuente_derecho	ch.ehi.ili2db.tableKind	CLASS
snr_fuente_derecho	ch.ehi.ili2db.dispName	(SNR) Fuente Derecho
op_interesado_contacto	ch.ehi.ili2db.tableKind	CLASS
op_interesado_contacto	ch.ehi.ili2db.dispName	Interesado Contacto
gc_sistemaprocedenciadatostipo	ch.ehi.ili2db.tableKind	ENUM
col_menosccl	ch.ehi.ili2db.tableKind	ASSOCIATION
extinteresado	ch.ehi.ili2db.tableKind	STRUCTURE
col_iso19125_tipo	ch.ehi.ili2db.tableKind	ENUM
extunidadedificacionfisica	ch.ehi.ili2db.tableKind	STRUCTURE
col_topografofuente	ch.ehi.ili2db.tableKind	ASSOCIATION
col_clfuente	ch.ehi.ili2db.tableKind	ASSOCIATION
op_condicionprediotipo	ch.ehi.ili2db.tableKind	ENUM
gm_multisurface2d	ch.ehi.ili2db.tableKind	STRUCTURE
col_redserviciostipo	ch.ehi.ili2db.tableKind	ENUM
gc_copropiedad	ch.ehi.ili2db.tableKind	ASSOCIATION
gc_comisiones_terreno	ch.ehi.ili2db.tableKind	CLASS
gc_comisiones_terreno	ch.ehi.ili2db.dispName	(GC) Comisiones Terreno
op_servidumbretransito	ch.ehi.ili2db.tableKind	CLASS
op_servidumbretransito	ch.ehi.ili2db.dispName	Servidumbre de Tránsito
gc_construccion	ch.ehi.ili2db.tableKind	CLASS
gc_construccion	ch.ehi.ili2db.dispName	(GC) Construcción
op_puntolindero	ch.ehi.ili2db.tableKind	CLASS
op_puntolindero	ch.ehi.ili2db.dispName	Punto Lindero
op_puntocontroltipo	ch.ehi.ili2db.tableKind	ENUM
col_puntocl	ch.ehi.ili2db.tableKind	ASSOCIATION
col_ueuegrupo	ch.ehi.ili2db.tableKind	ASSOCIATION
snr_fuente_cabidalinderos	ch.ehi.ili2db.tableKind	CLASS
snr_fuente_cabidalinderos	ch.ehi.ili2db.dispName	(SNR) Fuente Cabida Linderos
gc_sector_rural	ch.ehi.ili2db.tableKind	CLASS
gc_sector_rural	ch.ehi.ili2db.dispName	(GC) Sector Rural
col_rrrfuente	ch.ehi.ili2db.tableKind	ASSOCIATION
op_puntolevtipo	ch.ehi.ili2db.tableKind	ENUM
op_fotoidentificaciontipo	ch.ehi.ili2db.tableKind	ENUM
op_puntolevantamiento	ch.ehi.ili2db.tableKind	CLASS
op_puntolevantamiento	ch.ehi.ili2db.dispName	Punto Levantamiento
op_interesadodocumentotipo	ch.ehi.ili2db.tableKind	ENUM
col_dimensiontipo	ch.ehi.ili2db.tableKind	ENUM
gm_surface3dlistvalue	ch.ehi.ili2db.tableKind	STRUCTURE
op_puntocontrol	ch.ehi.ili2db.tableKind	CLASS
op_puntocontrol	ch.ehi.ili2db.dispName	Punto Control
op_interesadotipo	ch.ehi.ili2db.tableKind	ENUM
op_ubicacionpuntotipo	ch.ehi.ili2db.tableKind	ENUM
snr_documentotitulartipo	ch.ehi.ili2db.tableKind	ENUM
col_fuenteespacialtipo	ch.ehi.ili2db.tableKind	ENUM
gc_comisiones_unidad_construccion	ch.ehi.ili2db.tableKind	CLASS
gc_comisiones_unidad_construccion	ch.ehi.ili2db.dispName	(GC) Comisiones Unidad Construcción
gc_terreno	ch.ehi.ili2db.tableKind	CLASS
gc_terreno	ch.ehi.ili2db.dispName	(GC) Terreno
gc_predio_catastro	ch.ehi.ili2db.tableKind	CLASS
gc_predio_catastro	ch.ehi.ili2db.dispName	(GC) Predio Catastro
cc_metodooperacion	ch.ehi.ili2db.tableKind	STRUCTURE
op_datos_ph_condominio	ch.ehi.ili2db.tableKind	CLASS
op_datos_ph_condominio	ch.ehi.ili2db.dispName	Datos PH Condominio
gc_vereda	ch.ehi.ili2db.tableKind	CLASS
gc_vereda	ch.ehi.ili2db.dispName	(GC) Vereda
op_agrupacion_interesados	ch.ehi.ili2db.tableKind	CLASS
op_agrupacion_interesados	ch.ehi.ili2db.dispName	Agrupación de Interesados
op_lindero	ch.ehi.ili2db.tableKind	CLASS
op_lindero	ch.ehi.ili2db.dispName	Lindero
op_viatipo	ch.ehi.ili2db.tableKind	ENUM
fraccion	ch.ehi.ili2db.tableKind	STRUCTURE
op_unidadconstrucciontipo	ch.ehi.ili2db.tableKind	ENUM
gc_unidad_construccion	ch.ehi.ili2db.tableKind	CLASS
gc_unidad_construccion	ch.ehi.ili2db.dispName	(GC) Unidad Construcción
col_areatipo	ch.ehi.ili2db.tableKind	ENUM
op_sexotipo	ch.ehi.ili2db.tableKind	ENUM
gc_perimetro	ch.ehi.ili2db.tableKind	CLASS
gc_perimetro	ch.ehi.ili2db.dispName	(GC) Perímetro
snr_titular_derecho	ch.ehi.ili2db.tableKind	ASSOCIATION
col_masccl	ch.ehi.ili2db.tableKind	ASSOCIATION
col_puntofuente	ch.ehi.ili2db.tableKind	ASSOCIATION
col_relacionsuperficietipo	ch.ehi.ili2db.tableKind	ENUM
op_construccion	ch.ehi.ili2db.tableKind	CLASS
op_construccion	ch.ehi.ili2db.dispName	Construcción
anystructure	ch.ehi.ili2db.tableKind	STRUCTURE
col_relacionfuenteuespacial	ch.ehi.ili2db.tableKind	ASSOCIATION
col_areavalor	ch.ehi.ili2db.tableKind	STRUCTURE
extdireccion_clase_via_principal	ch.ehi.ili2db.tableKind	ENUM
extarchivo	ch.ehi.ili2db.tableKind	STRUCTURE
extarchivo	ch.ehi.ili2db.dispName	Archivo fuente
op_terreno	ch.ehi.ili2db.tableKind	CLASS
op_terreno	ch.ehi.ili2db.dispName	Terreno
op_puntotipo	ch.ehi.ili2db.tableKind	ENUM
col_interpolaciontipo	ch.ehi.ili2db.tableKind	ENUM
gm_multisurface3d	ch.ehi.ili2db.tableKind	STRUCTURE
snr_derecho	ch.ehi.ili2db.tableKind	CLASS
snr_derecho	ch.ehi.ili2db.dispName	(SNR) Derecho
col_cclfuente	ch.ehi.ili2db.tableKind	ASSOCIATION
\.


--
-- TOC entry 12705 (class 0 OID 339650)
-- Dependencies: 2271
-- Data for Name: t_ili2db_trafo; Type: TABLE DATA; Schema: ladm_col_210; Owner: postgres
--

COPY ladm_col_210.t_ili2db_trafo (iliname, tag, setting) FROM stdin;
LADM_COL_V1_6.LADM_Nucleo.COL_BAUnit	ch.ehi.ili2db.inheritance	subClass
Datos_Gestor_Catastral_V2_10.GC_Direccion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
LADM_COL_V1_6.LADM_Nucleo.COL_CadenaCarasLimite	ch.ehi.ili2db.inheritance	subClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Urbano	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Manzana.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
Operacion_V2_10.Operacion.OP_Predio	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos.ini_predio_integracion_gc	ch.ehi.ili2db.inheritance	embedded
Operacion_V2_10.Operacion.OP_Agrupacion_Interesados	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_ueNivel	ch.ehi.ili2db.inheritance	embedded
LADM_COL_V1_6.LADM_Nucleo.col_baunitFuente	ch.ehi.ili2db.inheritance	newAndSubClass
Operacion_V2_10.Operacion.op_predio_copropiedad	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_SNR_V2_10.Datos_SNR.SNR_Titular	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.Fraccion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_menosCcl	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_Derecho	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.ExtInteresado	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_unidadFuente	ch.ehi.ili2db.inheritance	newAndSubClass
Operacion_V2_10.Operacion.OP_Derecho	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
Datos_SNR_V2_10.Datos_SNR.SNR_Derecho	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_clFuente	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.COL_VolumenValor	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_construccion_unidad	ch.ehi.ili2db.inheritance	embedded
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda	ch.ehi.ili2db.inheritance	newAndSubClass
Operacion_V2_10.Operacion.OP_Terreno	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteAdministrativa	ch.ehi.ili2db.inheritance	subClass
LADM_COL_V1_6.LADM_Nucleo.col_miembros	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.COL_UnidadEspacial	ch.ehi.ili2db.inheritance	subClass
Operacion_V2_10.Operacion.OP_Lindero	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.COL_Fuente	ch.ehi.ili2db.inheritance	subClass
Operacion_V2_10.Operacion.op_ph_predio	ch.ehi.ili2db.inheritance	embedded
LADM_COL_V1_6.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales	ch.ehi.ili2db.inheritance	subClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_propietario_predio	ch.ehi.ili2db.inheritance	embedded
Datos_SNR_V2_10.Datos_SNR.SNR_Fuente_CabidaLinderos	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Terreno	ch.ehi.ili2db.inheritance	newAndSubClass
ISO19107_PLANAS_V1.GM_MultiSurface2D	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.COL_Nivel	ch.ehi.ili2db.inheritance	subClass
LADM_COL_V1_6.LADM_Nucleo.col_menosCl	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_rrrInteresado	ch.ehi.ili2db.inheritance	embedded
LADM_COL_V1_6.LADM_Nucleo.ExtDireccion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_ueFuente	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Rural	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.CC_MetodoOperacion	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Construccion	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_construccion_predio	ch.ehi.ili2db.inheritance	embedded
Operacion_V2_10.Operacion.OP_PuntoLevantamiento	ch.ehi.ili2db.inheritance	newAndSubClass
Operacion_V2_10.Operacion.OP_UnidadConstruccion	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
Operacion_V2_10.Operacion.OP_Construccion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_relacionFuenteUespacial	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_SNR_V2_10.Datos_SNR.snr_titular_derecho	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
LADM_COL_V1_6.LADM_Nucleo.COL_AreaValor	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.Oid	ch.ehi.ili2db.inheritance	subClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Terreno.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
Datos_SNR_V2_10.Datos_SNR.SNR_Predio_Registro	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Terreno	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Barrio	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_SNR_V2_10.Datos_SNR.snr_derecho_predio	ch.ehi.ili2db.inheritance	embedded
Operacion_V2_10.Operacion.op_construccion_unidadconstruccion	ch.ehi.ili2db.inheritance	embedded
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Predio_Catastro	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_topografoFuente	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.COL_DRR	ch.ehi.ili2db.inheritance	subClass
Operacion_V2_10.Operacion.op_interesado_contacto	ch.ehi.ili2db.inheritance	embedded
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Rural.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
LADM_COL_V1_6.LADM_Nucleo.col_masCl	ch.ehi.ili2db.inheritance	newAndSubClass
Operacion_V2_10.Operacion.OP_Terreno.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
LADM_COL_V1_6.LADM_Nucleo.ExtUnidadEdificacionFisica	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_terreno_predio	ch.ehi.ili2db.inheritance	embedded
Operacion_V2_10.Operacion.OP_FuenteEspacial	ch.ehi.ili2db.inheritance	newAndSubClass
Operacion_V2_10.Operacion.OP_PuntoControl	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_ueJerarquiaGrupo	ch.ehi.ili2db.inheritance	embedded
ISO19107_PLANAS_V1.GM_Surface3DListValue	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_masCcl	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
Operacion_V2_10.Operacion.OP_Datos_PH_Condominio	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.Imagen	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Barrio.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
LADM_COL_V1_6.LADM_Nucleo.ExtRedServiciosFisica	ch.ehi.ili2db.inheritance	newAndSubClass
ISO19107_PLANAS_V1.GM_Surface2DListValue	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.COL_Agrupacion_Interesados	ch.ehi.ili2db.inheritance	subClass
LADM_COL_V1_6.LADM_Nucleo.COL_Transformacion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.COL_Interesado	ch.ehi.ili2db.inheritance	subClass
ISO19107_PLANAS_V1.GM_MultiSurface3D	ch.ehi.ili2db.inheritance	newAndSubClass
Operacion_V2_10.Operacion.OP_Interesado	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Sector_Urbano.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
LADM_COL_V1_6.LADM_Nucleo.COL_EspacioJuridicoRedServicios	ch.ehi.ili2db.inheritance	subClass
LADM_COL_V1_6.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion	ch.ehi.ili2db.inheritance	subClass
LADM_COL_V1_6.LADM_Nucleo.col_relacionFuente	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.COL_FuenteEspacial	ch.ehi.ili2db.inheritance	subClass
LADM_COL_V1_6.LADM_Nucleo.col_baunitComoInteresado	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_ueUeGrupo	ch.ehi.ili2db.inheritance	newAndSubClass
Operacion_V2_10.Operacion.OP_ServidumbreTransito	ch.ehi.ili2db.inheritance	newAndSubClass
Operacion_V2_10.Operacion.OP_Restriccion	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_ph_predio	ch.ehi.ili2db.inheritance	embedded
LADM_COL_V1_6.LADM_Nucleo.col_cclFuente	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.COL_RelacionNecesariaBAUnits	ch.ehi.ili2db.inheritance	subClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.gc_copropiedad	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_ueBaunit	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.COL_CarasLindero	ch.ehi.ili2db.inheritance	subClass
Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos.INI_Predio_Insumos	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_rrrFuente	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Perimetro.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
Datos_SNR_V2_10.Datos_SNR.snr_fuente_derecho	ch.ehi.ili2db.inheritance	embedded
INTERLIS.ANYSTRUCTURE	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_puntoCcl	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.COL_RelacionNecesariaUnidadesEspaciales	ch.ehi.ili2db.inheritance	subClass
LADM_COL_V1_6.LADM_Nucleo.col_baunitRrr	ch.ehi.ili2db.inheritance	embedded
LADM_COL_V1_6.LADM_Nucleo.col_puntoReferencia	ch.ehi.ili2db.inheritance	embedded
LADM_COL_V1_6.LADM_Nucleo.col_puntoCl	ch.ehi.ili2db.inheritance	newAndSubClass
Operacion_V2_10.Operacion.op_predio_insumos_operacion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.ExtArchivo	ch.ehi.ili2db.inheritance	newAndSubClass
Operacion_V2_10.Operacion.OP_Interesado_Contacto	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_puntoFuente	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.col_responsableFuente	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Propietario	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Integracion_Insumos_V2_10.Datos_Integracion_Insumos.ini_predio_integracion_snr	ch.ehi.ili2db.inheritance	embedded
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_SNR_V2_10.Datos_SNR.snr_fuente_cabidalinderos	ch.ehi.ili2db.inheritance	embedded
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Construccion	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Manzana	ch.ehi.ili2db.inheritance	newAndSubClass
Operacion_V2_10.Operacion.OP_PuntoLindero	ch.ehi.ili2db.inheritance	newAndSubClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Unidad_Construccion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.ObjetoVersionado	ch.ehi.ili2db.inheritance	subClass
Datos_Gestor_Catastral_V2_10.Datos_Gestor_Catastral.GC_Vereda.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
Operacion_V2_10.Operacion.OP_FuenteAdministrativa	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_6.LADM_Nucleo.COL_Punto	ch.ehi.ili2db.inheritance	subClass
\.


--
-- TOC entry 12891 (class 0 OID 0)
-- Dependencies: 2129
-- Name: t_ili2db_seq; Type: SEQUENCE SET; Schema: ladm_col_210; Owner: postgres
--

SELECT pg_catalog.setval('ladm_col_210.t_ili2db_seq', 332, true);


--
-- TOC entry 11708 (class 2606 OID 339660)
-- Name: anystructure anystructure_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11711 (class 2606 OID 339662)
-- Name: cc_metodooperacion cc_metodooperacion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.cc_metodooperacion
    ADD CONSTRAINT cc_metodooperacion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11713 (class 2606 OID 339664)
-- Name: ci_forma_presentacion_codigo ci_forma_presentacion_codigo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.ci_forma_presentacion_codigo
    ADD CONSTRAINT ci_forma_presentacion_codigo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11715 (class 2606 OID 339666)
-- Name: col_areatipo col_areatipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_areatipo
    ADD CONSTRAINT col_areatipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11722 (class 2606 OID 339668)
-- Name: col_areavalor col_areavalor_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_areavalor
    ADD CONSTRAINT col_areavalor_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11726 (class 2606 OID 339670)
-- Name: col_baunitcomointeresado col_baunitcomointeresado_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_baunitcomointeresado
    ADD CONSTRAINT col_baunitcomointeresado_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11730 (class 2606 OID 339672)
-- Name: col_baunitfuente col_baunitfuente_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_baunitfuente
    ADD CONSTRAINT col_baunitfuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11733 (class 2606 OID 339674)
-- Name: col_baunittipo col_baunittipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_baunittipo
    ADD CONSTRAINT col_baunittipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11737 (class 2606 OID 339676)
-- Name: col_cclfuente col_cclfuente_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_cclfuente
    ADD CONSTRAINT col_cclfuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11740 (class 2606 OID 339678)
-- Name: col_clfuente col_clfuente_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_clfuente
    ADD CONSTRAINT col_clfuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11742 (class 2606 OID 339680)
-- Name: col_contenidoniveltipo col_contenidoniveltipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_contenidoniveltipo
    ADD CONSTRAINT col_contenidoniveltipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11744 (class 2606 OID 339682)
-- Name: col_dimensiontipo col_dimensiontipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_dimensiontipo
    ADD CONSTRAINT col_dimensiontipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11746 (class 2606 OID 339684)
-- Name: col_estadodisponibilidadtipo col_estadodisponibilidadtipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_estadodisponibilidadtipo
    ADD CONSTRAINT col_estadodisponibilidadtipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11748 (class 2606 OID 339686)
-- Name: col_estadoredserviciostipo col_estadoredserviciostipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_estadoredserviciostipo
    ADD CONSTRAINT col_estadoredserviciostipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11750 (class 2606 OID 339688)
-- Name: col_estructuratipo col_estructuratipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_estructuratipo
    ADD CONSTRAINT col_estructuratipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11752 (class 2606 OID 339690)
-- Name: col_fuenteadministrativatipo col_fuenteadministrativatipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_fuenteadministrativatipo
    ADD CONSTRAINT col_fuenteadministrativatipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11754 (class 2606 OID 339692)
-- Name: col_fuenteespacialtipo col_fuenteespacialtipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_fuenteespacialtipo
    ADD CONSTRAINT col_fuenteespacialtipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11756 (class 2606 OID 339694)
-- Name: col_grupointeresadotipo col_grupointeresadotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_grupointeresadotipo
    ADD CONSTRAINT col_grupointeresadotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11758 (class 2606 OID 339696)
-- Name: col_interpolaciontipo col_interpolaciontipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_interpolaciontipo
    ADD CONSTRAINT col_interpolaciontipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11760 (class 2606 OID 339698)
-- Name: col_iso19125_tipo col_iso19125_tipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_iso19125_tipo
    ADD CONSTRAINT col_iso19125_tipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11763 (class 2606 OID 339700)
-- Name: col_masccl col_masccl_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_masccl
    ADD CONSTRAINT col_masccl_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11769 (class 2606 OID 339702)
-- Name: col_mascl col_mascl_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_mascl
    ADD CONSTRAINT col_mascl_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11776 (class 2606 OID 339704)
-- Name: col_menosccl col_menosccl_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_menosccl
    ADD CONSTRAINT col_menosccl_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11782 (class 2606 OID 339706)
-- Name: col_menoscl col_menoscl_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_menoscl
    ADD CONSTRAINT col_menoscl_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11788 (class 2606 OID 339708)
-- Name: col_metodoproducciontipo col_metodoproducciontipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_metodoproducciontipo
    ADD CONSTRAINT col_metodoproducciontipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11793 (class 2606 OID 339710)
-- Name: col_miembros col_miembros_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_miembros
    ADD CONSTRAINT col_miembros_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11796 (class 2606 OID 339712)
-- Name: col_puntoccl col_puntoccl_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntoccl
    ADD CONSTRAINT col_puntoccl_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11801 (class 2606 OID 339714)
-- Name: col_puntocl col_puntocl_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntocl
    ADD CONSTRAINT col_puntocl_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11807 (class 2606 OID 339716)
-- Name: col_puntofuente col_puntofuente_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntofuente
    ADD CONSTRAINT col_puntofuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11812 (class 2606 OID 339718)
-- Name: col_puntotipo col_puntotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntotipo
    ADD CONSTRAINT col_puntotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11814 (class 2606 OID 339720)
-- Name: col_redserviciostipo col_redserviciostipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_redserviciostipo
    ADD CONSTRAINT col_redserviciostipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11816 (class 2606 OID 339722)
-- Name: col_registrotipo col_registrotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_registrotipo
    ADD CONSTRAINT col_registrotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11819 (class 2606 OID 339724)
-- Name: col_relacionfuente col_relacionfuente_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_relacionfuente
    ADD CONSTRAINT col_relacionfuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11821 (class 2606 OID 339726)
-- Name: col_relacionfuenteuespacial col_relacionfuenteuespacial_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_relacionfuenteuespacial
    ADD CONSTRAINT col_relacionfuenteuespacial_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11824 (class 2606 OID 339728)
-- Name: col_relacionsuperficietipo col_relacionsuperficietipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_relacionsuperficietipo
    ADD CONSTRAINT col_relacionsuperficietipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11829 (class 2606 OID 339730)
-- Name: col_responsablefuente col_responsablefuente_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_responsablefuente
    ADD CONSTRAINT col_responsablefuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11832 (class 2606 OID 339732)
-- Name: col_rrrfuente col_rrrfuente_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_rrrfuente
    ADD CONSTRAINT col_rrrfuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11837 (class 2606 OID 339734)
-- Name: col_topografofuente col_topografofuente_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_topografofuente
    ADD CONSTRAINT col_topografofuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11845 (class 2606 OID 339736)
-- Name: col_transformacion col_transformacion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_transformacion
    ADD CONSTRAINT col_transformacion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11848 (class 2606 OID 339738)
-- Name: col_uebaunit col_uebaunit_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_uebaunit
    ADD CONSTRAINT col_uebaunit_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11855 (class 2606 OID 339740)
-- Name: col_uefuente col_uefuente_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_uefuente
    ADD CONSTRAINT col_uefuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11865 (class 2606 OID 339742)
-- Name: col_ueuegrupo col_ueuegrupo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_ueuegrupo
    ADD CONSTRAINT col_ueuegrupo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11867 (class 2606 OID 339744)
-- Name: col_unidadedificaciontipo col_unidadedificaciontipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_unidadedificaciontipo
    ADD CONSTRAINT col_unidadedificaciontipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11870 (class 2606 OID 339746)
-- Name: col_unidadfuente col_unidadfuente_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_unidadfuente
    ADD CONSTRAINT col_unidadfuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11873 (class 2606 OID 339748)
-- Name: col_volumentipo col_volumentipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_volumentipo
    ADD CONSTRAINT col_volumentipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11879 (class 2606 OID 339750)
-- Name: col_volumenvalor col_volumenvalor_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_volumenvalor
    ADD CONSTRAINT col_volumenvalor_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11884 (class 2606 OID 339752)
-- Name: extarchivo extarchivo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extarchivo
    ADD CONSTRAINT extarchivo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11900 (class 2606 OID 339754)
-- Name: extdireccion_clase_via_principal extdireccion_clase_via_principal_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion_clase_via_principal
    ADD CONSTRAINT extdireccion_clase_via_principal_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11895 (class 2606 OID 339756)
-- Name: extdireccion extdireccion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion
    ADD CONSTRAINT extdireccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11902 (class 2606 OID 339758)
-- Name: extdireccion_sector_ciudad extdireccion_sector_ciudad_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion_sector_ciudad
    ADD CONSTRAINT extdireccion_sector_ciudad_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11904 (class 2606 OID 339760)
-- Name: extdireccion_sector_predio extdireccion_sector_predio_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion_sector_predio
    ADD CONSTRAINT extdireccion_sector_predio_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11906 (class 2606 OID 339762)
-- Name: extdireccion_tipo_direccion extdireccion_tipo_direccion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion_tipo_direccion
    ADD CONSTRAINT extdireccion_tipo_direccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11911 (class 2606 OID 339764)
-- Name: extinteresado extinteresado_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extinteresado
    ADD CONSTRAINT extinteresado_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11913 (class 2606 OID 339766)
-- Name: extredserviciosfisica extredserviciosfisica_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extredserviciosfisica
    ADD CONSTRAINT extredserviciosfisica_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11915 (class 2606 OID 339768)
-- Name: extunidadedificacionfisica extunidadedificacionfisica_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extunidadedificacionfisica
    ADD CONSTRAINT extunidadedificacionfisica_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11919 (class 2606 OID 339770)
-- Name: fraccion fraccion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.fraccion
    ADD CONSTRAINT fraccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11922 (class 2606 OID 339772)
-- Name: gc_barrio gc_barrio_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_barrio
    ADD CONSTRAINT gc_barrio_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11925 (class 2606 OID 339774)
-- Name: gc_comisiones_construccion gc_comisiones_construccion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_comisiones_construccion
    ADD CONSTRAINT gc_comisiones_construccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11928 (class 2606 OID 339776)
-- Name: gc_comisiones_terreno gc_comisiones_terreno_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_comisiones_terreno
    ADD CONSTRAINT gc_comisiones_terreno_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11931 (class 2606 OID 339778)
-- Name: gc_comisiones_unidad_construccion gc_comisiones_unidad_construccion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_comisiones_unidad_construccion
    ADD CONSTRAINT gc_comisiones_unidad_construccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11933 (class 2606 OID 339780)
-- Name: gc_condicionprediotipo gc_condicionprediotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_condicionprediotipo
    ADD CONSTRAINT gc_condicionprediotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11937 (class 2606 OID 339782)
-- Name: gc_construccion gc_construccion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_construccion
    ADD CONSTRAINT gc_construccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11943 (class 2606 OID 339784)
-- Name: gc_copropiedad gc_copropiedad_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_copropiedad
    ADD CONSTRAINT gc_copropiedad_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11946 (class 2606 OID 339786)
-- Name: gc_datos_ph_condiminio gc_datos_ph_condiminio_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_datos_ph_condiminio
    ADD CONSTRAINT gc_datos_ph_condiminio_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11950 (class 2606 OID 339788)
-- Name: gc_direccion gc_direccion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_direccion
    ADD CONSTRAINT gc_direccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11953 (class 2606 OID 339790)
-- Name: gc_manzana gc_manzana_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_manzana
    ADD CONSTRAINT gc_manzana_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11956 (class 2606 OID 339792)
-- Name: gc_perimetro gc_perimetro_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_perimetro
    ADD CONSTRAINT gc_perimetro_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11959 (class 2606 OID 339794)
-- Name: gc_predio_catastro gc_predio_catastro_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_predio_catastro
    ADD CONSTRAINT gc_predio_catastro_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11963 (class 2606 OID 339796)
-- Name: gc_propietario gc_propietario_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_propietario
    ADD CONSTRAINT gc_propietario_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11966 (class 2606 OID 339798)
-- Name: gc_sector_rural gc_sector_rural_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_sector_rural
    ADD CONSTRAINT gc_sector_rural_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11969 (class 2606 OID 339800)
-- Name: gc_sector_urbano gc_sector_urbano_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_sector_urbano
    ADD CONSTRAINT gc_sector_urbano_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11971 (class 2606 OID 339802)
-- Name: gc_sistemaprocedenciadatostipo gc_sistemaprocedenciadatostipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_sistemaprocedenciadatostipo
    ADD CONSTRAINT gc_sistemaprocedenciadatostipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11975 (class 2606 OID 339804)
-- Name: gc_terreno gc_terreno_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_terreno
    ADD CONSTRAINT gc_terreno_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11979 (class 2606 OID 339806)
-- Name: gc_unidad_construccion gc_unidad_construccion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_unidad_construccion
    ADD CONSTRAINT gc_unidad_construccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11982 (class 2606 OID 339808)
-- Name: gc_unidadconstrucciontipo gc_unidadconstrucciontipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_unidadconstrucciontipo
    ADD CONSTRAINT gc_unidadconstrucciontipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11985 (class 2606 OID 339810)
-- Name: gc_vereda gc_vereda_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_vereda
    ADD CONSTRAINT gc_vereda_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11987 (class 2606 OID 339812)
-- Name: gm_multisurface2d gm_multisurface2d_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gm_multisurface2d
    ADD CONSTRAINT gm_multisurface2d_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11989 (class 2606 OID 339814)
-- Name: gm_multisurface3d gm_multisurface3d_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gm_multisurface3d
    ADD CONSTRAINT gm_multisurface3d_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11993 (class 2606 OID 339816)
-- Name: gm_surface2dlistvalue gm_surface2dlistvalue_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gm_surface2dlistvalue
    ADD CONSTRAINT gm_surface2dlistvalue_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11997 (class 2606 OID 339818)
-- Name: gm_surface3dlistvalue gm_surface3dlistvalue_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gm_surface3dlistvalue
    ADD CONSTRAINT gm_surface3dlistvalue_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12002 (class 2606 OID 339820)
-- Name: imagen imagen_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.imagen
    ADD CONSTRAINT imagen_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12005 (class 2606 OID 339822)
-- Name: ini_predio_insumos ini_predio_insumos_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.ini_predio_insumos
    ADD CONSTRAINT ini_predio_insumos_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12008 (class 2606 OID 339824)
-- Name: op_acuerdotipo op_acuerdotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_acuerdotipo
    ADD CONSTRAINT op_acuerdotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12010 (class 2606 OID 339826)
-- Name: op_agrupacion_interesados op_agrupacion_interesados_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_agrupacion_interesados
    ADD CONSTRAINT op_agrupacion_interesados_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12013 (class 2606 OID 339828)
-- Name: op_condicionprediotipo op_condicionprediotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_condicionprediotipo
    ADD CONSTRAINT op_condicionprediotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12017 (class 2606 OID 339830)
-- Name: op_construccion op_construccion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_construccion
    ADD CONSTRAINT op_construccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12022 (class 2606 OID 339832)
-- Name: op_construccionplantatipo op_construccionplantatipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_construccionplantatipo
    ADD CONSTRAINT op_construccionplantatipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12024 (class 2606 OID 339834)
-- Name: op_construcciontipo op_construcciontipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_construcciontipo
    ADD CONSTRAINT op_construcciontipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12027 (class 2606 OID 339836)
-- Name: op_datos_ph_condominio op_datos_ph_condominio_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_datos_ph_condominio
    ADD CONSTRAINT op_datos_ph_condominio_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12031 (class 2606 OID 339838)
-- Name: op_derecho op_derecho_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_derecho
    ADD CONSTRAINT op_derecho_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12035 (class 2606 OID 339840)
-- Name: op_derechotipo op_derechotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_derechotipo
    ADD CONSTRAINT op_derechotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12037 (class 2606 OID 339842)
-- Name: op_dominioconstrucciontipo op_dominioconstrucciontipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_dominioconstrucciontipo
    ADD CONSTRAINT op_dominioconstrucciontipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12039 (class 2606 OID 339844)
-- Name: op_fotoidentificaciontipo op_fotoidentificaciontipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_fotoidentificaciontipo
    ADD CONSTRAINT op_fotoidentificaciontipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12042 (class 2606 OID 339846)
-- Name: op_fuenteadministrativa op_fuenteadministrativa_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_fuenteadministrativa
    ADD CONSTRAINT op_fuenteadministrativa_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12046 (class 2606 OID 339848)
-- Name: op_fuenteadministrativatipo op_fuenteadministrativatipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_fuenteadministrativatipo
    ADD CONSTRAINT op_fuenteadministrativatipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12049 (class 2606 OID 339850)
-- Name: op_fuenteespacial op_fuenteespacial_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_fuenteespacial
    ADD CONSTRAINT op_fuenteespacial_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12053 (class 2606 OID 339852)
-- Name: op_grupoetnicotipo op_grupoetnicotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_grupoetnicotipo
    ADD CONSTRAINT op_grupoetnicotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12062 (class 2606 OID 339854)
-- Name: op_interesado_contacto op_interesado_contacto_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_interesado_contacto
    ADD CONSTRAINT op_interesado_contacto_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12056 (class 2606 OID 339856)
-- Name: op_interesado op_interesado_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_interesado
    ADD CONSTRAINT op_interesado_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12064 (class 2606 OID 339858)
-- Name: op_interesadodocumentotipo op_interesadodocumentotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_interesadodocumentotipo
    ADD CONSTRAINT op_interesadodocumentotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12066 (class 2606 OID 339860)
-- Name: op_interesadotipo op_interesadotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_interesadotipo
    ADD CONSTRAINT op_interesadotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12069 (class 2606 OID 339862)
-- Name: op_lindero op_lindero_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_lindero
    ADD CONSTRAINT op_lindero_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12076 (class 2606 OID 339864)
-- Name: op_predio_copropiedad op_predio_copropiedad_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_predio_copropiedad
    ADD CONSTRAINT op_predio_copropiedad_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12080 (class 2606 OID 339866)
-- Name: op_predio_insumos_operacion op_predio_insumos_operacion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_predio_insumos_operacion
    ADD CONSTRAINT op_predio_insumos_operacion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12072 (class 2606 OID 339868)
-- Name: op_predio op_predio_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_predio
    ADD CONSTRAINT op_predio_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12086 (class 2606 OID 339870)
-- Name: op_puntocontrol op_puntocontrol_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntocontrol
    ADD CONSTRAINT op_puntocontrol_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12095 (class 2606 OID 339872)
-- Name: op_puntocontroltipo op_puntocontroltipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntocontroltipo
    ADD CONSTRAINT op_puntocontroltipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12100 (class 2606 OID 339874)
-- Name: op_puntolevantamiento op_puntolevantamiento_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolevantamiento
    ADD CONSTRAINT op_puntolevantamiento_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12109 (class 2606 OID 339876)
-- Name: op_puntolevtipo op_puntolevtipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolevtipo
    ADD CONSTRAINT op_puntolevtipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12115 (class 2606 OID 339878)
-- Name: op_puntolindero op_puntolindero_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolindero
    ADD CONSTRAINT op_puntolindero_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12124 (class 2606 OID 339880)
-- Name: op_puntotipo op_puntotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntotipo
    ADD CONSTRAINT op_puntotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12128 (class 2606 OID 339882)
-- Name: op_restriccion op_restriccion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_restriccion
    ADD CONSTRAINT op_restriccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12132 (class 2606 OID 339884)
-- Name: op_restricciontipo op_restricciontipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_restricciontipo
    ADD CONSTRAINT op_restricciontipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12136 (class 2606 OID 339886)
-- Name: op_servidumbretransito op_servidumbretransito_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_servidumbretransito
    ADD CONSTRAINT op_servidumbretransito_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12139 (class 2606 OID 339888)
-- Name: op_sexotipo op_sexotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_sexotipo
    ADD CONSTRAINT op_sexotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12143 (class 2606 OID 339890)
-- Name: op_terreno op_terreno_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_terreno
    ADD CONSTRAINT op_terreno_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12146 (class 2606 OID 339892)
-- Name: op_ubicacionpuntotipo op_ubicacionpuntotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_ubicacionpuntotipo
    ADD CONSTRAINT op_ubicacionpuntotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12151 (class 2606 OID 339894)
-- Name: op_unidadconstruccion op_unidadconstruccion_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_unidadconstruccion
    ADD CONSTRAINT op_unidadconstruccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12159 (class 2606 OID 339896)
-- Name: op_unidadconstrucciontipo op_unidadconstrucciontipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_unidadconstrucciontipo
    ADD CONSTRAINT op_unidadconstrucciontipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12161 (class 2606 OID 339898)
-- Name: op_usouconstipo op_usouconstipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_usouconstipo
    ADD CONSTRAINT op_usouconstipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12163 (class 2606 OID 339900)
-- Name: op_viatipo op_viatipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_viatipo
    ADD CONSTRAINT op_viatipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12165 (class 2606 OID 339902)
-- Name: snr_calidadderechotipo snr_calidadderechotipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_calidadderechotipo
    ADD CONSTRAINT snr_calidadderechotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12168 (class 2606 OID 339904)
-- Name: snr_derecho snr_derecho_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_derecho
    ADD CONSTRAINT snr_derecho_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12172 (class 2606 OID 339906)
-- Name: snr_documentotitulartipo snr_documentotitulartipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_documentotitulartipo
    ADD CONSTRAINT snr_documentotitulartipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12174 (class 2606 OID 339908)
-- Name: snr_fuente_cabidalinderos snr_fuente_cabidalinderos_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_fuente_cabidalinderos
    ADD CONSTRAINT snr_fuente_cabidalinderos_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12177 (class 2606 OID 339910)
-- Name: snr_fuente_derecho snr_fuente_derecho_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_fuente_derecho
    ADD CONSTRAINT snr_fuente_derecho_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12180 (class 2606 OID 339912)
-- Name: snr_fuentetipo snr_fuentetipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_fuentetipo
    ADD CONSTRAINT snr_fuentetipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12182 (class 2606 OID 339914)
-- Name: snr_personatitulartipo snr_personatitulartipo_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_personatitulartipo
    ADD CONSTRAINT snr_personatitulartipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12184 (class 2606 OID 339916)
-- Name: snr_predio_registro snr_predio_registro_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_predio_registro
    ADD CONSTRAINT snr_predio_registro_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12191 (class 2606 OID 339918)
-- Name: snr_titular_derecho snr_titular_derecho_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_titular_derecho
    ADD CONSTRAINT snr_titular_derecho_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12187 (class 2606 OID 339920)
-- Name: snr_titular snr_titular_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_titular
    ADD CONSTRAINT snr_titular_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12195 (class 2606 OID 339922)
-- Name: t_ili2db_attrname t_ili2db_attrname_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.t_ili2db_attrname
    ADD CONSTRAINT t_ili2db_attrname_pkey PRIMARY KEY (sqlname, colowner);


--
-- TOC entry 12199 (class 2606 OID 339924)
-- Name: t_ili2db_basket t_ili2db_basket_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.t_ili2db_basket
    ADD CONSTRAINT t_ili2db_basket_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12201 (class 2606 OID 339926)
-- Name: t_ili2db_classname t_ili2db_classname_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.t_ili2db_classname
    ADD CONSTRAINT t_ili2db_classname_pkey PRIMARY KEY (iliname);


--
-- TOC entry 12204 (class 2606 OID 339928)
-- Name: t_ili2db_dataset t_ili2db_dataset_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.t_ili2db_dataset
    ADD CONSTRAINT t_ili2db_dataset_pkey PRIMARY KEY (t_id);


--
-- TOC entry 12206 (class 2606 OID 339930)
-- Name: t_ili2db_inheritance t_ili2db_inheritance_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.t_ili2db_inheritance
    ADD CONSTRAINT t_ili2db_inheritance_pkey PRIMARY KEY (thisclass);


--
-- TOC entry 12209 (class 2606 OID 339932)
-- Name: t_ili2db_model t_ili2db_model_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.t_ili2db_model
    ADD CONSTRAINT t_ili2db_model_pkey PRIMARY KEY (iliversion, modelname);


--
-- TOC entry 12211 (class 2606 OID 339934)
-- Name: t_ili2db_settings t_ili2db_settings_pkey; Type: CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.t_ili2db_settings
    ADD CONSTRAINT t_ili2db_settings_pkey PRIMARY KEY (tag);


--
-- TOC entry 11681 (class 1259 OID 339935)
-- Name: anystructure_op_agrupacion_ntrsds_cldad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_agrupacion_ntrsds_cldad_idx ON ladm_col_210.anystructure USING btree (op_agrupacion_intrsdos_calidad);


--
-- TOC entry 11682 (class 1259 OID 339936)
-- Name: anystructure_op_agrupcn_ntrsds_prcdncia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_agrupcn_ntrsds_prcdncia_idx ON ladm_col_210.anystructure USING btree (op_agrupacion_intrsdos_procedencia);


--
-- TOC entry 11683 (class 1259 OID 339937)
-- Name: anystructure_op_construccion_calidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_construccion_calidad_idx ON ladm_col_210.anystructure USING btree (op_construccion_calidad);


--
-- TOC entry 11684 (class 1259 OID 339938)
-- Name: anystructure_op_construccion_procedncia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_construccion_procedncia_idx ON ladm_col_210.anystructure USING btree (op_construccion_procedencia);


--
-- TOC entry 11685 (class 1259 OID 339939)
-- Name: anystructure_op_derecho_calidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_derecho_calidad_idx ON ladm_col_210.anystructure USING btree (op_derecho_calidad);


--
-- TOC entry 11686 (class 1259 OID 339940)
-- Name: anystructure_op_derecho_procedencia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_derecho_procedencia_idx ON ladm_col_210.anystructure USING btree (op_derecho_procedencia);


--
-- TOC entry 11687 (class 1259 OID 339941)
-- Name: anystructure_op_interesado_calidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_interesado_calidad_idx ON ladm_col_210.anystructure USING btree (op_interesado_calidad);


--
-- TOC entry 11688 (class 1259 OID 339942)
-- Name: anystructure_op_interesado_procedencia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_interesado_procedencia_idx ON ladm_col_210.anystructure USING btree (op_interesado_procedencia);


--
-- TOC entry 11689 (class 1259 OID 339943)
-- Name: anystructure_op_lindero_calidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_lindero_calidad_idx ON ladm_col_210.anystructure USING btree (op_lindero_calidad);


--
-- TOC entry 11690 (class 1259 OID 339944)
-- Name: anystructure_op_lindero_procedencia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_lindero_procedencia_idx ON ladm_col_210.anystructure USING btree (op_lindero_procedencia);


--
-- TOC entry 11691 (class 1259 OID 339945)
-- Name: anystructure_op_predio_calidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_predio_calidad_idx ON ladm_col_210.anystructure USING btree (op_predio_calidad);


--
-- TOC entry 11692 (class 1259 OID 339946)
-- Name: anystructure_op_predio_procedencia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_predio_procedencia_idx ON ladm_col_210.anystructure USING btree (op_predio_procedencia);


--
-- TOC entry 11693 (class 1259 OID 339947)
-- Name: anystructure_op_puntocontrol_calidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_puntocontrol_calidad_idx ON ladm_col_210.anystructure USING btree (op_puntocontrol_calidad);


--
-- TOC entry 11694 (class 1259 OID 339948)
-- Name: anystructure_op_puntocontrol_procedncia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_puntocontrol_procedncia_idx ON ladm_col_210.anystructure USING btree (op_puntocontrol_procedencia);


--
-- TOC entry 11695 (class 1259 OID 339949)
-- Name: anystructure_op_puntolevantamient_cldad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_puntolevantamient_cldad_idx ON ladm_col_210.anystructure USING btree (op_puntolevantamiento_calidad);


--
-- TOC entry 11696 (class 1259 OID 339950)
-- Name: anystructure_op_puntolevantmnt_prcdncia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_puntolevantmnt_prcdncia_idx ON ladm_col_210.anystructure USING btree (op_puntolevantamiento_procedencia);


--
-- TOC entry 11697 (class 1259 OID 339951)
-- Name: anystructure_op_puntolindero_calidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_puntolindero_calidad_idx ON ladm_col_210.anystructure USING btree (op_puntolindero_calidad);


--
-- TOC entry 11698 (class 1259 OID 339952)
-- Name: anystructure_op_puntolindero_procedncia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_puntolindero_procedncia_idx ON ladm_col_210.anystructure USING btree (op_puntolindero_procedencia);


--
-- TOC entry 11699 (class 1259 OID 339953)
-- Name: anystructure_op_restriccion_calidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_restriccion_calidad_idx ON ladm_col_210.anystructure USING btree (op_restriccion_calidad);


--
-- TOC entry 11700 (class 1259 OID 339954)
-- Name: anystructure_op_restriccion_procedencia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_restriccion_procedencia_idx ON ladm_col_210.anystructure USING btree (op_restriccion_procedencia);


--
-- TOC entry 11701 (class 1259 OID 339955)
-- Name: anystructure_op_servidmbrtrnst_prcdncia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_servidmbrtrnst_prcdncia_idx ON ladm_col_210.anystructure USING btree (op_servidumbretransito_procedencia);


--
-- TOC entry 11702 (class 1259 OID 339956)
-- Name: anystructure_op_servidumbretranst_cldad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_servidumbretranst_cldad_idx ON ladm_col_210.anystructure USING btree (op_servidumbretransito_calidad);


--
-- TOC entry 11703 (class 1259 OID 339957)
-- Name: anystructure_op_terreno_calidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_terreno_calidad_idx ON ladm_col_210.anystructure USING btree (op_terreno_calidad);


--
-- TOC entry 11704 (class 1259 OID 339958)
-- Name: anystructure_op_terreno_procedencia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_terreno_procedencia_idx ON ladm_col_210.anystructure USING btree (op_terreno_procedencia);


--
-- TOC entry 11705 (class 1259 OID 339959)
-- Name: anystructure_op_unidadcnstrccn_prcdncia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_unidadcnstrccn_prcdncia_idx ON ladm_col_210.anystructure USING btree (op_unidadconstruccion_procedencia);


--
-- TOC entry 11706 (class 1259 OID 339960)
-- Name: anystructure_op_unidadconstruccin_cldad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX anystructure_op_unidadconstruccin_cldad_idx ON ladm_col_210.anystructure USING btree (op_unidadconstruccion_calidad);


--
-- TOC entry 11709 (class 1259 OID 339961)
-- Name: cc_metodooperacion_col_transfrmcn_trnsfrmcion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX cc_metodooperacion_col_transfrmcn_trnsfrmcion_idx ON ladm_col_210.cc_metodooperacion USING btree (col_transformacion_transformacion);


--
-- TOC entry 11716 (class 1259 OID 339962)
-- Name: col_areavalor_atype_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_areavalor_atype_idx ON ladm_col_210.col_areavalor USING btree (atype);


--
-- TOC entry 11717 (class 1259 OID 339963)
-- Name: col_areavalor_op_construccion_area_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_areavalor_op_construccion_area_idx ON ladm_col_210.col_areavalor USING btree (op_construccion_area);


--
-- TOC entry 11718 (class 1259 OID 339964)
-- Name: col_areavalor_op_servidumbretransito_rea_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_areavalor_op_servidumbretransito_rea_idx ON ladm_col_210.col_areavalor USING btree (op_servidumbretransito_area);


--
-- TOC entry 11719 (class 1259 OID 339965)
-- Name: col_areavalor_op_terreno_area_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_areavalor_op_terreno_area_idx ON ladm_col_210.col_areavalor USING btree (op_terreno_area);


--
-- TOC entry 11720 (class 1259 OID 339966)
-- Name: col_areavalor_op_unidadconstruccion_area_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_areavalor_op_unidadconstruccion_area_idx ON ladm_col_210.col_areavalor USING btree (op_unidadconstruccion_area);


--
-- TOC entry 11723 (class 1259 OID 339967)
-- Name: col_baunitcomointeresado_interesado_op_interesado_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_baunitcomointeresado_interesado_op_interesado_idx ON ladm_col_210.col_baunitcomointeresado USING btree (interesado_op_interesado);


--
-- TOC entry 11724 (class 1259 OID 339968)
-- Name: col_baunitcomointeresado_interesado_p_grpcn_ntrsdos_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_baunitcomointeresado_interesado_p_grpcn_ntrsdos_idx ON ladm_col_210.col_baunitcomointeresado USING btree (interesado_op_agrupacion_interesados);


--
-- TOC entry 11727 (class 1259 OID 339969)
-- Name: col_baunitcomointeresado_unidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_baunitcomointeresado_unidad_idx ON ladm_col_210.col_baunitcomointeresado USING btree (unidad);


--
-- TOC entry 11728 (class 1259 OID 339970)
-- Name: col_baunitfuente_fuente_espacial_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_baunitfuente_fuente_espacial_idx ON ladm_col_210.col_baunitfuente USING btree (fuente_espacial);


--
-- TOC entry 11731 (class 1259 OID 339971)
-- Name: col_baunitfuente_unidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_baunitfuente_unidad_idx ON ladm_col_210.col_baunitfuente USING btree (unidad);


--
-- TOC entry 11734 (class 1259 OID 339972)
-- Name: col_cclfuente_ccl_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_cclfuente_ccl_idx ON ladm_col_210.col_cclfuente USING btree (ccl);


--
-- TOC entry 11735 (class 1259 OID 339973)
-- Name: col_cclfuente_fuente_espacial_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_cclfuente_fuente_espacial_idx ON ladm_col_210.col_cclfuente USING btree (fuente_espacial);


--
-- TOC entry 11738 (class 1259 OID 339974)
-- Name: col_clfuente_fuente_espacial_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_clfuente_fuente_espacial_idx ON ladm_col_210.col_clfuente USING btree (fuente_espacial);


--
-- TOC entry 11761 (class 1259 OID 339975)
-- Name: col_masccl_ccl_mas_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_masccl_ccl_mas_idx ON ladm_col_210.col_masccl USING btree (ccl_mas);


--
-- TOC entry 11764 (class 1259 OID 339976)
-- Name: col_masccl_ue_mas_op_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_masccl_ue_mas_op_construccion_idx ON ladm_col_210.col_masccl USING btree (ue_mas_op_construccion);


--
-- TOC entry 11765 (class 1259 OID 339977)
-- Name: col_masccl_ue_mas_op_servidmbrtrnsito_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_masccl_ue_mas_op_servidmbrtrnsito_idx ON ladm_col_210.col_masccl USING btree (ue_mas_op_servidumbretransito);


--
-- TOC entry 11766 (class 1259 OID 339978)
-- Name: col_masccl_ue_mas_op_terreno_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_masccl_ue_mas_op_terreno_idx ON ladm_col_210.col_masccl USING btree (ue_mas_op_terreno);


--
-- TOC entry 11767 (class 1259 OID 339979)
-- Name: col_masccl_ue_mas_op_unidadcnstrccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_masccl_ue_mas_op_unidadcnstrccion_idx ON ladm_col_210.col_masccl USING btree (ue_mas_op_unidadconstruccion);


--
-- TOC entry 11770 (class 1259 OID 339980)
-- Name: col_mascl_ue_mas_op_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_mascl_ue_mas_op_construccion_idx ON ladm_col_210.col_mascl USING btree (ue_mas_op_construccion);


--
-- TOC entry 11771 (class 1259 OID 339981)
-- Name: col_mascl_ue_mas_op_servidmbrtrnsito_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_mascl_ue_mas_op_servidmbrtrnsito_idx ON ladm_col_210.col_mascl USING btree (ue_mas_op_servidumbretransito);


--
-- TOC entry 11772 (class 1259 OID 339982)
-- Name: col_mascl_ue_mas_op_terreno_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_mascl_ue_mas_op_terreno_idx ON ladm_col_210.col_mascl USING btree (ue_mas_op_terreno);


--
-- TOC entry 11773 (class 1259 OID 339983)
-- Name: col_mascl_ue_mas_op_unidadcnstrccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_mascl_ue_mas_op_unidadcnstrccion_idx ON ladm_col_210.col_mascl USING btree (ue_mas_op_unidadconstruccion);


--
-- TOC entry 11774 (class 1259 OID 339984)
-- Name: col_menosccl_ccl_menos_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_menosccl_ccl_menos_idx ON ladm_col_210.col_menosccl USING btree (ccl_menos);


--
-- TOC entry 11777 (class 1259 OID 339985)
-- Name: col_menosccl_ue_menos_op_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_menosccl_ue_menos_op_construccion_idx ON ladm_col_210.col_menosccl USING btree (ue_menos_op_construccion);


--
-- TOC entry 11778 (class 1259 OID 339986)
-- Name: col_menosccl_ue_menos_op_srvdmbrtrnsito_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_menosccl_ue_menos_op_srvdmbrtrnsito_idx ON ladm_col_210.col_menosccl USING btree (ue_menos_op_servidumbretransito);


--
-- TOC entry 11779 (class 1259 OID 339987)
-- Name: col_menosccl_ue_menos_op_terreno_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_menosccl_ue_menos_op_terreno_idx ON ladm_col_210.col_menosccl USING btree (ue_menos_op_terreno);


--
-- TOC entry 11780 (class 1259 OID 339988)
-- Name: col_menosccl_ue_menos_op_unddcnstrccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_menosccl_ue_menos_op_unddcnstrccion_idx ON ladm_col_210.col_menosccl USING btree (ue_menos_op_unidadconstruccion);


--
-- TOC entry 11783 (class 1259 OID 339989)
-- Name: col_menoscl_ue_menos_op_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_menoscl_ue_menos_op_construccion_idx ON ladm_col_210.col_menoscl USING btree (ue_menos_op_construccion);


--
-- TOC entry 11784 (class 1259 OID 339990)
-- Name: col_menoscl_ue_menos_op_srvdmbrtrnsito_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_menoscl_ue_menos_op_srvdmbrtrnsito_idx ON ladm_col_210.col_menoscl USING btree (ue_menos_op_servidumbretransito);


--
-- TOC entry 11785 (class 1259 OID 339991)
-- Name: col_menoscl_ue_menos_op_terreno_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_menoscl_ue_menos_op_terreno_idx ON ladm_col_210.col_menoscl USING btree (ue_menos_op_terreno);


--
-- TOC entry 11786 (class 1259 OID 339992)
-- Name: col_menoscl_ue_menos_op_unddcnstrccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_menoscl_ue_menos_op_unddcnstrccion_idx ON ladm_col_210.col_menoscl USING btree (ue_menos_op_unidadconstruccion);


--
-- TOC entry 11789 (class 1259 OID 339993)
-- Name: col_miembros_agrupacion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_miembros_agrupacion_idx ON ladm_col_210.col_miembros USING btree (agrupacion);


--
-- TOC entry 11790 (class 1259 OID 339994)
-- Name: col_miembros_interesado_op_interesado_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_miembros_interesado_op_interesado_idx ON ladm_col_210.col_miembros USING btree (interesado_op_interesado);


--
-- TOC entry 11791 (class 1259 OID 339995)
-- Name: col_miembros_interesado_p_grpcn_ntrsdos_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_miembros_interesado_p_grpcn_ntrsdos_idx ON ladm_col_210.col_miembros USING btree (interesado_op_agrupacion_interesados);


--
-- TOC entry 11794 (class 1259 OID 339996)
-- Name: col_puntoccl_ccl_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_puntoccl_ccl_idx ON ladm_col_210.col_puntoccl USING btree (ccl);


--
-- TOC entry 11797 (class 1259 OID 339997)
-- Name: col_puntoccl_punto_op_puntocontrol_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_puntoccl_punto_op_puntocontrol_idx ON ladm_col_210.col_puntoccl USING btree (punto_op_puntocontrol);


--
-- TOC entry 11798 (class 1259 OID 339998)
-- Name: col_puntoccl_punto_op_puntolevantaminto_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_puntoccl_punto_op_puntolevantaminto_idx ON ladm_col_210.col_puntoccl USING btree (punto_op_puntolevantamiento);


--
-- TOC entry 11799 (class 1259 OID 339999)
-- Name: col_puntoccl_punto_op_puntolindero_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_puntoccl_punto_op_puntolindero_idx ON ladm_col_210.col_puntoccl USING btree (punto_op_puntolindero);


--
-- TOC entry 11802 (class 1259 OID 340000)
-- Name: col_puntocl_punto_op_puntocontrol_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_puntocl_punto_op_puntocontrol_idx ON ladm_col_210.col_puntocl USING btree (punto_op_puntocontrol);


--
-- TOC entry 11803 (class 1259 OID 340001)
-- Name: col_puntocl_punto_op_puntolevantaminto_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_puntocl_punto_op_puntolevantaminto_idx ON ladm_col_210.col_puntocl USING btree (punto_op_puntolevantamiento);


--
-- TOC entry 11804 (class 1259 OID 340002)
-- Name: col_puntocl_punto_op_puntolindero_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_puntocl_punto_op_puntolindero_idx ON ladm_col_210.col_puntocl USING btree (punto_op_puntolindero);


--
-- TOC entry 11805 (class 1259 OID 340003)
-- Name: col_puntofuente_fuente_espacial_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_puntofuente_fuente_espacial_idx ON ladm_col_210.col_puntofuente USING btree (fuente_espacial);


--
-- TOC entry 11808 (class 1259 OID 340004)
-- Name: col_puntofuente_punto_op_puntocontrol_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_puntofuente_punto_op_puntocontrol_idx ON ladm_col_210.col_puntofuente USING btree (punto_op_puntocontrol);


--
-- TOC entry 11809 (class 1259 OID 340005)
-- Name: col_puntofuente_punto_op_puntolevantaminto_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_puntofuente_punto_op_puntolevantaminto_idx ON ladm_col_210.col_puntofuente USING btree (punto_op_puntolevantamiento);


--
-- TOC entry 11810 (class 1259 OID 340006)
-- Name: col_puntofuente_punto_op_puntolindero_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_puntofuente_punto_op_puntolindero_idx ON ladm_col_210.col_puntofuente USING btree (punto_op_puntolindero);


--
-- TOC entry 11817 (class 1259 OID 340007)
-- Name: col_relacionfuente_fuente_administrativa_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_relacionfuente_fuente_administrativa_idx ON ladm_col_210.col_relacionfuente USING btree (fuente_administrativa);


--
-- TOC entry 11822 (class 1259 OID 340008)
-- Name: col_relacionfuenteuespcial_fuente_espacial_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_relacionfuenteuespcial_fuente_espacial_idx ON ladm_col_210.col_relacionfuenteuespacial USING btree (fuente_espacial);


--
-- TOC entry 11825 (class 1259 OID 340009)
-- Name: col_responsablefuente_fuente_administrativa_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_responsablefuente_fuente_administrativa_idx ON ladm_col_210.col_responsablefuente USING btree (fuente_administrativa);


--
-- TOC entry 11826 (class 1259 OID 340010)
-- Name: col_responsablefuente_interesado_op_interesado_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_responsablefuente_interesado_op_interesado_idx ON ladm_col_210.col_responsablefuente USING btree (interesado_op_interesado);


--
-- TOC entry 11827 (class 1259 OID 340011)
-- Name: col_responsablefuente_interesado_p_grpcn_ntrsdos_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_responsablefuente_interesado_p_grpcn_ntrsdos_idx ON ladm_col_210.col_responsablefuente USING btree (interesado_op_agrupacion_interesados);


--
-- TOC entry 11830 (class 1259 OID 340012)
-- Name: col_rrrfuente_fuente_administrativa_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_rrrfuente_fuente_administrativa_idx ON ladm_col_210.col_rrrfuente USING btree (fuente_administrativa);


--
-- TOC entry 11833 (class 1259 OID 340013)
-- Name: col_rrrfuente_rrr_op_derecho_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_rrrfuente_rrr_op_derecho_idx ON ladm_col_210.col_rrrfuente USING btree (rrr_op_derecho);


--
-- TOC entry 11834 (class 1259 OID 340014)
-- Name: col_rrrfuente_rrr_op_restriccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_rrrfuente_rrr_op_restriccion_idx ON ladm_col_210.col_rrrfuente USING btree (rrr_op_restriccion);


--
-- TOC entry 11835 (class 1259 OID 340015)
-- Name: col_topografofuente_fuente_espacial_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_topografofuente_fuente_espacial_idx ON ladm_col_210.col_topografofuente USING btree (fuente_espacial);


--
-- TOC entry 11838 (class 1259 OID 340016)
-- Name: col_topografofuente_topografo_op_grpcn_ntrsdos_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_topografofuente_topografo_op_grpcn_ntrsdos_idx ON ladm_col_210.col_topografofuente USING btree (topografo_op_agrupacion_interesados);


--
-- TOC entry 11839 (class 1259 OID 340017)
-- Name: col_topografofuente_topografo_op_interesado_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_topografofuente_topografo_op_interesado_idx ON ladm_col_210.col_topografofuente USING btree (topografo_op_interesado);


--
-- TOC entry 11840 (class 1259 OID 340018)
-- Name: col_transformacion_localizacion_transformada_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_transformacion_localizacion_transformada_idx ON ladm_col_210.col_transformacion USING gist (localizacion_transformada);


--
-- TOC entry 11841 (class 1259 OID 340019)
-- Name: col_transformacion_op_pntcntrl_tmcn_y_rsltado_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_transformacion_op_pntcntrl_tmcn_y_rsltado_idx ON ladm_col_210.col_transformacion USING btree (op_puntocontrol_transformacion_y_resultado);


--
-- TOC entry 11842 (class 1259 OID 340020)
-- Name: col_transformacion_op_pntlndr_trmcn_y_rsltado_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_transformacion_op_pntlndr_trmcn_y_rsltado_idx ON ladm_col_210.col_transformacion USING btree (op_puntolindero_transformacion_y_resultado);


--
-- TOC entry 11843 (class 1259 OID 340021)
-- Name: col_transformacion_op_pntlvntmntmcn_y_rsltado_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_transformacion_op_pntlvntmntmcn_y_rsltado_idx ON ladm_col_210.col_transformacion USING btree (op_puntolevantamiento_transformacion_y_resultado);


--
-- TOC entry 11846 (class 1259 OID 340022)
-- Name: col_uebaunit_baunit_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_uebaunit_baunit_idx ON ladm_col_210.col_uebaunit USING btree (baunit);


--
-- TOC entry 11849 (class 1259 OID 340023)
-- Name: col_uebaunit_ue_op_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_uebaunit_ue_op_construccion_idx ON ladm_col_210.col_uebaunit USING btree (ue_op_construccion);


--
-- TOC entry 11850 (class 1259 OID 340024)
-- Name: col_uebaunit_ue_op_servidumbretransito_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_uebaunit_ue_op_servidumbretransito_idx ON ladm_col_210.col_uebaunit USING btree (ue_op_servidumbretransito);


--
-- TOC entry 11851 (class 1259 OID 340025)
-- Name: col_uebaunit_ue_op_terreno_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_uebaunit_ue_op_terreno_idx ON ladm_col_210.col_uebaunit USING btree (ue_op_terreno);


--
-- TOC entry 11852 (class 1259 OID 340026)
-- Name: col_uebaunit_ue_op_unidadconstruccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_uebaunit_ue_op_unidadconstruccion_idx ON ladm_col_210.col_uebaunit USING btree (ue_op_unidadconstruccion);


--
-- TOC entry 11853 (class 1259 OID 340027)
-- Name: col_uefuente_fuente_espacial_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_uefuente_fuente_espacial_idx ON ladm_col_210.col_uefuente USING btree (fuente_espacial);


--
-- TOC entry 11856 (class 1259 OID 340028)
-- Name: col_uefuente_ue_op_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_uefuente_ue_op_construccion_idx ON ladm_col_210.col_uefuente USING btree (ue_op_construccion);


--
-- TOC entry 11857 (class 1259 OID 340029)
-- Name: col_uefuente_ue_op_servidumbretransito_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_uefuente_ue_op_servidumbretransito_idx ON ladm_col_210.col_uefuente USING btree (ue_op_servidumbretransito);


--
-- TOC entry 11858 (class 1259 OID 340030)
-- Name: col_uefuente_ue_op_terreno_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_uefuente_ue_op_terreno_idx ON ladm_col_210.col_uefuente USING btree (ue_op_terreno);


--
-- TOC entry 11859 (class 1259 OID 340031)
-- Name: col_uefuente_ue_op_unidadconstruccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_uefuente_ue_op_unidadconstruccion_idx ON ladm_col_210.col_uefuente USING btree (ue_op_unidadconstruccion);


--
-- TOC entry 11860 (class 1259 OID 340032)
-- Name: col_ueuegrupo_parte_op_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_ueuegrupo_parte_op_construccion_idx ON ladm_col_210.col_ueuegrupo USING btree (parte_op_construccion);


--
-- TOC entry 11861 (class 1259 OID 340033)
-- Name: col_ueuegrupo_parte_op_servidumbrtrnsito_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_ueuegrupo_parte_op_servidumbrtrnsito_idx ON ladm_col_210.col_ueuegrupo USING btree (parte_op_servidumbretransito);


--
-- TOC entry 11862 (class 1259 OID 340034)
-- Name: col_ueuegrupo_parte_op_terreno_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_ueuegrupo_parte_op_terreno_idx ON ladm_col_210.col_ueuegrupo USING btree (parte_op_terreno);


--
-- TOC entry 11863 (class 1259 OID 340035)
-- Name: col_ueuegrupo_parte_op_unidadconstrccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_ueuegrupo_parte_op_unidadconstrccion_idx ON ladm_col_210.col_ueuegrupo USING btree (parte_op_unidadconstruccion);


--
-- TOC entry 11868 (class 1259 OID 340036)
-- Name: col_unidadfuente_fuente_administrativa_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_unidadfuente_fuente_administrativa_idx ON ladm_col_210.col_unidadfuente USING btree (fuente_administrativa);


--
-- TOC entry 11871 (class 1259 OID 340037)
-- Name: col_unidadfuente_unidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_unidadfuente_unidad_idx ON ladm_col_210.col_unidadfuente USING btree (unidad);


--
-- TOC entry 11874 (class 1259 OID 340038)
-- Name: col_volumenvalor_op_construccion_volumen_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_volumenvalor_op_construccion_volumen_idx ON ladm_col_210.col_volumenvalor USING btree (op_construccion_volumen);


--
-- TOC entry 11875 (class 1259 OID 340039)
-- Name: col_volumenvalor_op_servidumbretranst_vlmen_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_volumenvalor_op_servidumbretranst_vlmen_idx ON ladm_col_210.col_volumenvalor USING btree (op_servidumbretransito_volumen);


--
-- TOC entry 11876 (class 1259 OID 340040)
-- Name: col_volumenvalor_op_terreno_volumen_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_volumenvalor_op_terreno_volumen_idx ON ladm_col_210.col_volumenvalor USING btree (op_terreno_volumen);


--
-- TOC entry 11877 (class 1259 OID 340041)
-- Name: col_volumenvalor_op_unidadconstruccin_vlmen_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_volumenvalor_op_unidadconstruccin_vlmen_idx ON ladm_col_210.col_volumenvalor USING btree (op_unidadconstruccion_volumen);


--
-- TOC entry 11880 (class 1259 OID 340042)
-- Name: col_volumenvalor_tipo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX col_volumenvalor_tipo_idx ON ladm_col_210.col_volumenvalor USING btree (tipo);


--
-- TOC entry 11881 (class 1259 OID 340043)
-- Name: extarchivo_op_fuenteespacl_xt_rchv_id_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extarchivo_op_fuenteespacl_xt_rchv_id_idx ON ladm_col_210.extarchivo USING btree (op_fuenteespacial_ext_archivo_id);


--
-- TOC entry 11882 (class 1259 OID 340044)
-- Name: extarchivo_op_funtdmnstrtv_xt_rchv_id_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extarchivo_op_funtdmnstrtv_xt_rchv_id_idx ON ladm_col_210.extarchivo USING btree (op_fuenteadministrtiva_ext_archivo_id);


--
-- TOC entry 11885 (class 1259 OID 340045)
-- Name: extarchivo_snr_fuente_cbdlndrs_rchivo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extarchivo_snr_fuente_cbdlndrs_rchivo_idx ON ladm_col_210.extarchivo USING btree (snr_fuente_cabidlndros_archivo);


--
-- TOC entry 11886 (class 1259 OID 340046)
-- Name: extdireccion_clase_via_principal_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extdireccion_clase_via_principal_idx ON ladm_col_210.extdireccion USING btree (clase_via_principal);


--
-- TOC entry 11887 (class 1259 OID 340047)
-- Name: extdireccion_extinteresado_ext_drccn_id_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extdireccion_extinteresado_ext_drccn_id_idx ON ladm_col_210.extdireccion USING btree (extinteresado_ext_direccion_id);


--
-- TOC entry 11888 (class 1259 OID 340048)
-- Name: extdireccion_extndddfccnfsc_xt_drccn_id_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extdireccion_extndddfccnfsc_xt_drccn_id_idx ON ladm_col_210.extdireccion USING btree (extunidadedificcnfsica_ext_direccion_id);


--
-- TOC entry 11889 (class 1259 OID 340049)
-- Name: extdireccion_localizacion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extdireccion_localizacion_idx ON ladm_col_210.extdireccion USING gist (localizacion);


--
-- TOC entry 11890 (class 1259 OID 340050)
-- Name: extdireccion_op_construccin_xt_drccn_id_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extdireccion_op_construccin_xt_drccn_id_idx ON ladm_col_210.extdireccion USING btree (op_construccion_ext_direccion_id);


--
-- TOC entry 11891 (class 1259 OID 340051)
-- Name: extdireccion_op_nddcnstrccn_xt_drccn_id_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extdireccion_op_nddcnstrccn_xt_drccn_id_idx ON ladm_col_210.extdireccion USING btree (op_unidadconstruccion_ext_direccion_id);


--
-- TOC entry 11892 (class 1259 OID 340052)
-- Name: extdireccion_op_srvdmbrtrnt_xt_drccn_id_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extdireccion_op_srvdmbrtrnt_xt_drccn_id_idx ON ladm_col_210.extdireccion USING btree (op_servidumbretransito_ext_direccion_id);


--
-- TOC entry 11893 (class 1259 OID 340053)
-- Name: extdireccion_op_terreno_ext_direccin_id_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extdireccion_op_terreno_ext_direccin_id_idx ON ladm_col_210.extdireccion USING btree (op_terreno_ext_direccion_id);


--
-- TOC entry 11896 (class 1259 OID 340054)
-- Name: extdireccion_sector_ciudad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extdireccion_sector_ciudad_idx ON ladm_col_210.extdireccion USING btree (sector_ciudad);


--
-- TOC entry 11897 (class 1259 OID 340055)
-- Name: extdireccion_sector_predio_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extdireccion_sector_predio_idx ON ladm_col_210.extdireccion USING btree (sector_predio);


--
-- TOC entry 11898 (class 1259 OID 340056)
-- Name: extdireccion_tipo_direccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extdireccion_tipo_direccion_idx ON ladm_col_210.extdireccion USING btree (tipo_direccion);


--
-- TOC entry 11907 (class 1259 OID 340057)
-- Name: extinteresado_extrdsrvcsfscd_dmnstrdr_id_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extinteresado_extrdsrvcsfscd_dmnstrdr_id_idx ON ladm_col_210.extinteresado USING btree (extredserviciosfisica_ext_interesado_administrador_id);


--
-- TOC entry 11908 (class 1259 OID 340058)
-- Name: extinteresado_op_agrupacin_ntrsds_xt_pid_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extinteresado_op_agrupacin_ntrsds_xt_pid_idx ON ladm_col_210.extinteresado USING btree (op_agrupacion_intrsdos_ext_pid);


--
-- TOC entry 11909 (class 1259 OID 340059)
-- Name: extinteresado_op_interesado_ext_pid_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX extinteresado_op_interesado_ext_pid_idx ON ladm_col_210.extinteresado USING btree (op_interesado_ext_pid);


--
-- TOC entry 11916 (class 1259 OID 340060)
-- Name: fraccion_col_miembros_participacion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX fraccion_col_miembros_participacion_idx ON ladm_col_210.fraccion USING btree (col_miembros_participacion);


--
-- TOC entry 11917 (class 1259 OID 340061)
-- Name: fraccion_op_predio_copropidd_cfcnte_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX fraccion_op_predio_copropidd_cfcnte_idx ON ladm_col_210.fraccion USING btree (op_predio_copropiedad_coeficiente);


--
-- TOC entry 11920 (class 1259 OID 340062)
-- Name: gc_barrio_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_barrio_geometria_idx ON ladm_col_210.gc_barrio USING gist (geometria);


--
-- TOC entry 11929 (class 1259 OID 340063)
-- Name: gc_comisins_ndd_cnstrccion_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_comisins_ndd_cnstrccion_geometria_idx ON ladm_col_210.gc_comisiones_unidad_construccion USING gist (geometria);


--
-- TOC entry 11923 (class 1259 OID 340064)
-- Name: gc_comisiones_construccion_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_comisiones_construccion_geometria_idx ON ladm_col_210.gc_comisiones_construccion USING gist (geometria);


--
-- TOC entry 11926 (class 1259 OID 340065)
-- Name: gc_comisiones_terreno_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_comisiones_terreno_geometria_idx ON ladm_col_210.gc_comisiones_terreno USING gist (geometria);


--
-- TOC entry 11934 (class 1259 OID 340066)
-- Name: gc_construccion_gc_predio_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_construccion_gc_predio_idx ON ladm_col_210.gc_construccion USING btree (gc_predio);


--
-- TOC entry 11935 (class 1259 OID 340067)
-- Name: gc_construccion_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_construccion_geometria_idx ON ladm_col_210.gc_construccion USING gist (geometria);


--
-- TOC entry 11938 (class 1259 OID 340068)
-- Name: gc_construccion_tipo_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_construccion_tipo_construccion_idx ON ladm_col_210.gc_construccion USING btree (tipo_construccion);


--
-- TOC entry 11939 (class 1259 OID 340069)
-- Name: gc_copropiedad_gc_matriz_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_copropiedad_gc_matriz_idx ON ladm_col_210.gc_copropiedad USING btree (gc_matriz);


--
-- TOC entry 11940 (class 1259 OID 340070)
-- Name: gc_copropiedad_gc_unidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_copropiedad_gc_unidad_idx ON ladm_col_210.gc_copropiedad USING btree (gc_unidad);


--
-- TOC entry 11941 (class 1259 OID 340071)
-- Name: gc_copropiedad_gc_unidad_key; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE UNIQUE INDEX gc_copropiedad_gc_unidad_key ON ladm_col_210.gc_copropiedad USING btree (gc_unidad);


--
-- TOC entry 11944 (class 1259 OID 340072)
-- Name: gc_datos_ph_condiminio_gc_predio_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_datos_ph_condiminio_gc_predio_idx ON ladm_col_210.gc_datos_ph_condiminio USING btree (gc_predio);


--
-- TOC entry 11947 (class 1259 OID 340073)
-- Name: gc_direccion_gc_predio_catastro_drccnes_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_direccion_gc_predio_catastro_drccnes_idx ON ladm_col_210.gc_direccion USING btree (gc_predio_catastro_direcciones);


--
-- TOC entry 11948 (class 1259 OID 340074)
-- Name: gc_direccion_geometria_referencia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_direccion_geometria_referencia_idx ON ladm_col_210.gc_direccion USING gist (geometria_referencia);


--
-- TOC entry 11951 (class 1259 OID 340075)
-- Name: gc_manzana_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_manzana_geometria_idx ON ladm_col_210.gc_manzana USING gist (geometria);


--
-- TOC entry 11954 (class 1259 OID 340076)
-- Name: gc_perimetro_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_perimetro_geometria_idx ON ladm_col_210.gc_perimetro USING gist (geometria);


--
-- TOC entry 11957 (class 1259 OID 340077)
-- Name: gc_predio_catastro_condicion_predio_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_predio_catastro_condicion_predio_idx ON ladm_col_210.gc_predio_catastro USING btree (condicion_predio);


--
-- TOC entry 11960 (class 1259 OID 340078)
-- Name: gc_predio_catastro_sistema_procedencia_datos_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_predio_catastro_sistema_procedencia_datos_idx ON ladm_col_210.gc_predio_catastro USING btree (sistema_procedencia_datos);


--
-- TOC entry 11961 (class 1259 OID 340079)
-- Name: gc_propietario_gc_predio_catastro_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_propietario_gc_predio_catastro_idx ON ladm_col_210.gc_propietario USING btree (gc_predio_catastro);


--
-- TOC entry 11964 (class 1259 OID 340080)
-- Name: gc_sector_rural_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_sector_rural_geometria_idx ON ladm_col_210.gc_sector_rural USING gist (geometria);


--
-- TOC entry 11967 (class 1259 OID 340081)
-- Name: gc_sector_urbano_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_sector_urbano_geometria_idx ON ladm_col_210.gc_sector_urbano USING gist (geometria);


--
-- TOC entry 11972 (class 1259 OID 340082)
-- Name: gc_terreno_gc_predio_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_terreno_gc_predio_idx ON ladm_col_210.gc_terreno USING btree (gc_predio);


--
-- TOC entry 11973 (class 1259 OID 340083)
-- Name: gc_terreno_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_terreno_geometria_idx ON ladm_col_210.gc_terreno USING gist (geometria);


--
-- TOC entry 11976 (class 1259 OID 340084)
-- Name: gc_unidad_construccion_gc_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_unidad_construccion_gc_construccion_idx ON ladm_col_210.gc_unidad_construccion USING btree (gc_construccion);


--
-- TOC entry 11977 (class 1259 OID 340085)
-- Name: gc_unidad_construccion_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_unidad_construccion_geometria_idx ON ladm_col_210.gc_unidad_construccion USING gist (geometria);


--
-- TOC entry 11980 (class 1259 OID 340086)
-- Name: gc_unidad_construccion_tipo_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_unidad_construccion_tipo_construccion_idx ON ladm_col_210.gc_unidad_construccion USING btree (tipo_construccion);


--
-- TOC entry 11983 (class 1259 OID 340087)
-- Name: gc_vereda_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gc_vereda_geometria_idx ON ladm_col_210.gc_vereda USING gist (geometria);


--
-- TOC entry 11990 (class 1259 OID 340088)
-- Name: gm_surface2dlistvalue_avalue_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gm_surface2dlistvalue_avalue_idx ON ladm_col_210.gm_surface2dlistvalue USING gist (avalue);


--
-- TOC entry 11991 (class 1259 OID 340089)
-- Name: gm_surface2dlistvalue_gm_multisurface2d_geometry_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gm_surface2dlistvalue_gm_multisurface2d_geometry_idx ON ladm_col_210.gm_surface2dlistvalue USING btree (gm_multisurface2d_geometry);


--
-- TOC entry 11994 (class 1259 OID 340090)
-- Name: gm_surface3dlistvalue_avalue_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gm_surface3dlistvalue_avalue_idx ON ladm_col_210.gm_surface3dlistvalue USING gist (avalue);


--
-- TOC entry 11995 (class 1259 OID 340091)
-- Name: gm_surface3dlistvalue_gm_multisurface3d_geometry_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX gm_surface3dlistvalue_gm_multisurface3d_geometry_idx ON ladm_col_210.gm_surface3dlistvalue USING btree (gm_multisurface3d_geometry);


--
-- TOC entry 11998 (class 1259 OID 340092)
-- Name: imagen_extinteresado_firma_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX imagen_extinteresado_firma_idx ON ladm_col_210.imagen USING btree (extinteresado_firma);


--
-- TOC entry 11999 (class 1259 OID 340093)
-- Name: imagen_extinteresado_fotografia_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX imagen_extinteresado_fotografia_idx ON ladm_col_210.imagen USING btree (extinteresado_fotografia);


--
-- TOC entry 12000 (class 1259 OID 340094)
-- Name: imagen_extinteresado_huell_dctlar_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX imagen_extinteresado_huell_dctlar_idx ON ladm_col_210.imagen USING btree (extinteresado_huella_dactilar);


--
-- TOC entry 12003 (class 1259 OID 340095)
-- Name: ini_predio_insumos_gc_predio_catastro_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX ini_predio_insumos_gc_predio_catastro_idx ON ladm_col_210.ini_predio_insumos USING btree (gc_predio_catastro);


--
-- TOC entry 12006 (class 1259 OID 340096)
-- Name: ini_predio_insumos_snr_predio_juridico_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX ini_predio_insumos_snr_predio_juridico_idx ON ladm_col_210.ini_predio_insumos USING btree (snr_predio_juridico);


--
-- TOC entry 12011 (class 1259 OID 340097)
-- Name: op_agrupacion_interesados_tipo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_agrupacion_interesados_tipo_idx ON ladm_col_210.op_agrupacion_interesados USING btree (tipo);


--
-- TOC entry 12014 (class 1259 OID 340098)
-- Name: op_construccion_dimension_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_construccion_dimension_idx ON ladm_col_210.op_construccion USING btree (dimension);


--
-- TOC entry 12015 (class 1259 OID 340099)
-- Name: op_construccion_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_construccion_geometria_idx ON ladm_col_210.op_construccion USING gist (geometria);


--
-- TOC entry 12018 (class 1259 OID 340100)
-- Name: op_construccion_relacion_superficie_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_construccion_relacion_superficie_idx ON ladm_col_210.op_construccion USING btree (relacion_superficie);


--
-- TOC entry 12019 (class 1259 OID 340101)
-- Name: op_construccion_tipo_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_construccion_tipo_construccion_idx ON ladm_col_210.op_construccion USING btree (tipo_construccion);


--
-- TOC entry 12020 (class 1259 OID 340102)
-- Name: op_construccion_tipo_dominio_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_construccion_tipo_dominio_idx ON ladm_col_210.op_construccion USING btree (tipo_dominio);


--
-- TOC entry 12025 (class 1259 OID 340103)
-- Name: op_datos_ph_condominio_op_predio_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_datos_ph_condominio_op_predio_idx ON ladm_col_210.op_datos_ph_condominio USING btree (op_predio);


--
-- TOC entry 12028 (class 1259 OID 340104)
-- Name: op_derecho_interesado_op_interesado_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_derecho_interesado_op_interesado_idx ON ladm_col_210.op_derecho USING btree (interesado_op_interesado);


--
-- TOC entry 12029 (class 1259 OID 340105)
-- Name: op_derecho_interesado_p_grpcn_ntrsdos_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_derecho_interesado_p_grpcn_ntrsdos_idx ON ladm_col_210.op_derecho USING btree (interesado_op_agrupacion_interesados);


--
-- TOC entry 12032 (class 1259 OID 340106)
-- Name: op_derecho_tipo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_derecho_tipo_idx ON ladm_col_210.op_derecho USING btree (tipo);


--
-- TOC entry 12033 (class 1259 OID 340107)
-- Name: op_derecho_unidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_derecho_unidad_idx ON ladm_col_210.op_derecho USING btree (unidad);


--
-- TOC entry 12040 (class 1259 OID 340108)
-- Name: op_fuenteadministrativa_estado_disponibilidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_fuenteadministrativa_estado_disponibilidad_idx ON ladm_col_210.op_fuenteadministrativa USING btree (estado_disponibilidad);


--
-- TOC entry 12043 (class 1259 OID 340109)
-- Name: op_fuenteadministrativa_tipo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_fuenteadministrativa_tipo_idx ON ladm_col_210.op_fuenteadministrativa USING btree (tipo);


--
-- TOC entry 12044 (class 1259 OID 340110)
-- Name: op_fuenteadministrativa_tipo_principal_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_fuenteadministrativa_tipo_principal_idx ON ladm_col_210.op_fuenteadministrativa USING btree (tipo_principal);


--
-- TOC entry 12047 (class 1259 OID 340111)
-- Name: op_fuenteespacial_estado_disponibilidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_fuenteespacial_estado_disponibilidad_idx ON ladm_col_210.op_fuenteespacial USING btree (estado_disponibilidad);


--
-- TOC entry 12050 (class 1259 OID 340112)
-- Name: op_fuenteespacial_tipo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_fuenteespacial_tipo_idx ON ladm_col_210.op_fuenteespacial USING btree (tipo);


--
-- TOC entry 12051 (class 1259 OID 340113)
-- Name: op_fuenteespacial_tipo_principal_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_fuenteespacial_tipo_principal_idx ON ladm_col_210.op_fuenteespacial USING btree (tipo_principal);


--
-- TOC entry 12060 (class 1259 OID 340114)
-- Name: op_interesado_contacto_op_interesado_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_interesado_contacto_op_interesado_idx ON ladm_col_210.op_interesado_contacto USING btree (op_interesado);


--
-- TOC entry 12054 (class 1259 OID 340115)
-- Name: op_interesado_grupo_etnico_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_interesado_grupo_etnico_idx ON ladm_col_210.op_interesado USING btree (grupo_etnico);


--
-- TOC entry 12057 (class 1259 OID 340116)
-- Name: op_interesado_sexo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_interesado_sexo_idx ON ladm_col_210.op_interesado USING btree (sexo);


--
-- TOC entry 12058 (class 1259 OID 340117)
-- Name: op_interesado_tipo_documento_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_interesado_tipo_documento_idx ON ladm_col_210.op_interesado USING btree (tipo_documento);


--
-- TOC entry 12059 (class 1259 OID 340118)
-- Name: op_interesado_tipo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_interesado_tipo_idx ON ladm_col_210.op_interesado USING btree (tipo);


--
-- TOC entry 12067 (class 1259 OID 340119)
-- Name: op_lindero_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_lindero_geometria_idx ON ladm_col_210.op_lindero USING gist (geometria);


--
-- TOC entry 12070 (class 1259 OID 340120)
-- Name: op_predio_condicion_predio_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_predio_condicion_predio_idx ON ladm_col_210.op_predio USING btree (condicion_predio);


--
-- TOC entry 12074 (class 1259 OID 340121)
-- Name: op_predio_copropiedad_copropiedad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_predio_copropiedad_copropiedad_idx ON ladm_col_210.op_predio_copropiedad USING btree (copropiedad);


--
-- TOC entry 12077 (class 1259 OID 340122)
-- Name: op_predio_copropiedad_predio_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_predio_copropiedad_predio_idx ON ladm_col_210.op_predio_copropiedad USING btree (predio);


--
-- TOC entry 12078 (class 1259 OID 340123)
-- Name: op_predio_copropiedad_predio_key; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE UNIQUE INDEX op_predio_copropiedad_predio_key ON ladm_col_210.op_predio_copropiedad USING btree (predio);


--
-- TOC entry 12081 (class 1259 OID 340124)
-- Name: op_predio_insumos_opercion_ini_predio_insumos_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_predio_insumos_opercion_ini_predio_insumos_idx ON ladm_col_210.op_predio_insumos_operacion USING btree (ini_predio_insumos);


--
-- TOC entry 12082 (class 1259 OID 340125)
-- Name: op_predio_insumos_opercion_op_predio_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_predio_insumos_opercion_op_predio_idx ON ladm_col_210.op_predio_insumos_operacion USING btree (op_predio);


--
-- TOC entry 12073 (class 1259 OID 340126)
-- Name: op_predio_tipo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_predio_tipo_idx ON ladm_col_210.op_predio USING btree (tipo);


--
-- TOC entry 12083 (class 1259 OID 340127)
-- Name: op_puntocontrol_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntocontrol_geometria_idx ON ladm_col_210.op_puntocontrol USING gist (geometria);


--
-- TOC entry 12084 (class 1259 OID 340128)
-- Name: op_puntocontrol_metodoproduccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntocontrol_metodoproduccion_idx ON ladm_col_210.op_puntocontrol USING btree (metodoproduccion);


--
-- TOC entry 12087 (class 1259 OID 340129)
-- Name: op_puntocontrol_posicion_interpolacion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntocontrol_posicion_interpolacion_idx ON ladm_col_210.op_puntocontrol USING btree (posicion_interpolacion);


--
-- TOC entry 12088 (class 1259 OID 340130)
-- Name: op_puntocontrol_puntotipo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntocontrol_puntotipo_idx ON ladm_col_210.op_puntocontrol USING btree (puntotipo);


--
-- TOC entry 12089 (class 1259 OID 340131)
-- Name: op_puntocontrol_tipo_punto_control_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntocontrol_tipo_punto_control_idx ON ladm_col_210.op_puntocontrol USING btree (tipo_punto_control);


--
-- TOC entry 12090 (class 1259 OID 340132)
-- Name: op_puntocontrol_ue_op_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntocontrol_ue_op_construccion_idx ON ladm_col_210.op_puntocontrol USING btree (ue_op_construccion);


--
-- TOC entry 12091 (class 1259 OID 340133)
-- Name: op_puntocontrol_ue_op_servidumbretransito_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntocontrol_ue_op_servidumbretransito_idx ON ladm_col_210.op_puntocontrol USING btree (ue_op_servidumbretransito);


--
-- TOC entry 12092 (class 1259 OID 340134)
-- Name: op_puntocontrol_ue_op_terreno_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntocontrol_ue_op_terreno_idx ON ladm_col_210.op_puntocontrol USING btree (ue_op_terreno);


--
-- TOC entry 12093 (class 1259 OID 340135)
-- Name: op_puntocontrol_ue_op_unidadconstruccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntocontrol_ue_op_unidadconstruccion_idx ON ladm_col_210.op_puntocontrol USING btree (ue_op_unidadconstruccion);


--
-- TOC entry 12096 (class 1259 OID 340136)
-- Name: op_puntolevantamiento_fotoidentificacion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolevantamiento_fotoidentificacion_idx ON ladm_col_210.op_puntolevantamiento USING btree (fotoidentificacion);


--
-- TOC entry 12097 (class 1259 OID 340137)
-- Name: op_puntolevantamiento_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolevantamiento_geometria_idx ON ladm_col_210.op_puntolevantamiento USING gist (geometria);


--
-- TOC entry 12098 (class 1259 OID 340138)
-- Name: op_puntolevantamiento_metodoproduccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolevantamiento_metodoproduccion_idx ON ladm_col_210.op_puntolevantamiento USING btree (metodoproduccion);


--
-- TOC entry 12101 (class 1259 OID 340139)
-- Name: op_puntolevantamiento_posicion_interpolacion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolevantamiento_posicion_interpolacion_idx ON ladm_col_210.op_puntolevantamiento USING btree (posicion_interpolacion);


--
-- TOC entry 12102 (class 1259 OID 340140)
-- Name: op_puntolevantamiento_puntotipo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolevantamiento_puntotipo_idx ON ladm_col_210.op_puntolevantamiento USING btree (puntotipo);


--
-- TOC entry 12103 (class 1259 OID 340141)
-- Name: op_puntolevantamiento_tipo_punto_levantamiento_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolevantamiento_tipo_punto_levantamiento_idx ON ladm_col_210.op_puntolevantamiento USING btree (tipo_punto_levantamiento);


--
-- TOC entry 12104 (class 1259 OID 340142)
-- Name: op_puntolevantamiento_ue_op_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolevantamiento_ue_op_construccion_idx ON ladm_col_210.op_puntolevantamiento USING btree (ue_op_construccion);


--
-- TOC entry 12105 (class 1259 OID 340143)
-- Name: op_puntolevantamiento_ue_op_servidumbretransito_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolevantamiento_ue_op_servidumbretransito_idx ON ladm_col_210.op_puntolevantamiento USING btree (ue_op_servidumbretransito);


--
-- TOC entry 12106 (class 1259 OID 340144)
-- Name: op_puntolevantamiento_ue_op_terreno_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolevantamiento_ue_op_terreno_idx ON ladm_col_210.op_puntolevantamiento USING btree (ue_op_terreno);


--
-- TOC entry 12107 (class 1259 OID 340145)
-- Name: op_puntolevantamiento_ue_op_unidadconstruccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolevantamiento_ue_op_unidadconstruccion_idx ON ladm_col_210.op_puntolevantamiento USING btree (ue_op_unidadconstruccion);


--
-- TOC entry 12110 (class 1259 OID 340146)
-- Name: op_puntolindero_acuerdo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolindero_acuerdo_idx ON ladm_col_210.op_puntolindero USING btree (acuerdo);


--
-- TOC entry 12111 (class 1259 OID 340147)
-- Name: op_puntolindero_fotoidentificacion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolindero_fotoidentificacion_idx ON ladm_col_210.op_puntolindero USING btree (fotoidentificacion);


--
-- TOC entry 12112 (class 1259 OID 340148)
-- Name: op_puntolindero_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolindero_geometria_idx ON ladm_col_210.op_puntolindero USING gist (geometria);


--
-- TOC entry 12113 (class 1259 OID 340149)
-- Name: op_puntolindero_metodoproduccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolindero_metodoproduccion_idx ON ladm_col_210.op_puntolindero USING btree (metodoproduccion);


--
-- TOC entry 12116 (class 1259 OID 340150)
-- Name: op_puntolindero_posicion_interpolacion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolindero_posicion_interpolacion_idx ON ladm_col_210.op_puntolindero USING btree (posicion_interpolacion);


--
-- TOC entry 12117 (class 1259 OID 340151)
-- Name: op_puntolindero_puntotipo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolindero_puntotipo_idx ON ladm_col_210.op_puntolindero USING btree (puntotipo);


--
-- TOC entry 12118 (class 1259 OID 340152)
-- Name: op_puntolindero_ubicacion_punto_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolindero_ubicacion_punto_idx ON ladm_col_210.op_puntolindero USING btree (ubicacion_punto);


--
-- TOC entry 12119 (class 1259 OID 340153)
-- Name: op_puntolindero_ue_op_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolindero_ue_op_construccion_idx ON ladm_col_210.op_puntolindero USING btree (ue_op_construccion);


--
-- TOC entry 12120 (class 1259 OID 340154)
-- Name: op_puntolindero_ue_op_servidumbretransito_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolindero_ue_op_servidumbretransito_idx ON ladm_col_210.op_puntolindero USING btree (ue_op_servidumbretransito);


--
-- TOC entry 12121 (class 1259 OID 340155)
-- Name: op_puntolindero_ue_op_terreno_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolindero_ue_op_terreno_idx ON ladm_col_210.op_puntolindero USING btree (ue_op_terreno);


--
-- TOC entry 12122 (class 1259 OID 340156)
-- Name: op_puntolindero_ue_op_unidadconstruccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_puntolindero_ue_op_unidadconstruccion_idx ON ladm_col_210.op_puntolindero USING btree (ue_op_unidadconstruccion);


--
-- TOC entry 12125 (class 1259 OID 340157)
-- Name: op_restriccion_interesado_op_interesado_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_restriccion_interesado_op_interesado_idx ON ladm_col_210.op_restriccion USING btree (interesado_op_interesado);


--
-- TOC entry 12126 (class 1259 OID 340158)
-- Name: op_restriccion_interesado_p_grpcn_ntrsdos_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_restriccion_interesado_p_grpcn_ntrsdos_idx ON ladm_col_210.op_restriccion USING btree (interesado_op_agrupacion_interesados);


--
-- TOC entry 12129 (class 1259 OID 340159)
-- Name: op_restriccion_tipo_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_restriccion_tipo_idx ON ladm_col_210.op_restriccion USING btree (tipo);


--
-- TOC entry 12130 (class 1259 OID 340160)
-- Name: op_restriccion_unidad_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_restriccion_unidad_idx ON ladm_col_210.op_restriccion USING btree (unidad);


--
-- TOC entry 12133 (class 1259 OID 340161)
-- Name: op_servidumbretransito_dimension_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_servidumbretransito_dimension_idx ON ladm_col_210.op_servidumbretransito USING btree (dimension);


--
-- TOC entry 12134 (class 1259 OID 340162)
-- Name: op_servidumbretransito_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_servidumbretransito_geometria_idx ON ladm_col_210.op_servidumbretransito USING gist (geometria);


--
-- TOC entry 12137 (class 1259 OID 340163)
-- Name: op_servidumbretransito_relacion_superficie_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_servidumbretransito_relacion_superficie_idx ON ladm_col_210.op_servidumbretransito USING btree (relacion_superficie);


--
-- TOC entry 12140 (class 1259 OID 340164)
-- Name: op_terreno_dimension_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_terreno_dimension_idx ON ladm_col_210.op_terreno USING btree (dimension);


--
-- TOC entry 12141 (class 1259 OID 340165)
-- Name: op_terreno_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_terreno_geometria_idx ON ladm_col_210.op_terreno USING gist (geometria);


--
-- TOC entry 12144 (class 1259 OID 340166)
-- Name: op_terreno_relacion_superficie_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_terreno_relacion_superficie_idx ON ladm_col_210.op_terreno USING btree (relacion_superficie);


--
-- TOC entry 12147 (class 1259 OID 340167)
-- Name: op_unidadconstruccion_dimension_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_unidadconstruccion_dimension_idx ON ladm_col_210.op_unidadconstruccion USING btree (dimension);


--
-- TOC entry 12148 (class 1259 OID 340168)
-- Name: op_unidadconstruccion_geometria_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_unidadconstruccion_geometria_idx ON ladm_col_210.op_unidadconstruccion USING gist (geometria);


--
-- TOC entry 12149 (class 1259 OID 340169)
-- Name: op_unidadconstruccion_op_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_unidadconstruccion_op_construccion_idx ON ladm_col_210.op_unidadconstruccion USING btree (op_construccion);


--
-- TOC entry 12152 (class 1259 OID 340170)
-- Name: op_unidadconstruccion_relacion_superficie_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_unidadconstruccion_relacion_superficie_idx ON ladm_col_210.op_unidadconstruccion USING btree (relacion_superficie);


--
-- TOC entry 12153 (class 1259 OID 340171)
-- Name: op_unidadconstruccion_tipo_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_unidadconstruccion_tipo_construccion_idx ON ladm_col_210.op_unidadconstruccion USING btree (tipo_construccion);


--
-- TOC entry 12154 (class 1259 OID 340172)
-- Name: op_unidadconstruccion_tipo_dominio_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_unidadconstruccion_tipo_dominio_idx ON ladm_col_210.op_unidadconstruccion USING btree (tipo_dominio);


--
-- TOC entry 12155 (class 1259 OID 340173)
-- Name: op_unidadconstruccion_tipo_planta_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_unidadconstruccion_tipo_planta_idx ON ladm_col_210.op_unidadconstruccion USING btree (tipo_planta);


--
-- TOC entry 12156 (class 1259 OID 340174)
-- Name: op_unidadconstruccion_tipo_unidad_construccion_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_unidadconstruccion_tipo_unidad_construccion_idx ON ladm_col_210.op_unidadconstruccion USING btree (tipo_unidad_construccion);


--
-- TOC entry 12157 (class 1259 OID 340175)
-- Name: op_unidadconstruccion_uso_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX op_unidadconstruccion_uso_idx ON ladm_col_210.op_unidadconstruccion USING btree (uso);


--
-- TOC entry 12166 (class 1259 OID 340176)
-- Name: snr_derecho_calidad_derecho_registro_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX snr_derecho_calidad_derecho_registro_idx ON ladm_col_210.snr_derecho USING btree (calidad_derecho_registro);


--
-- TOC entry 12169 (class 1259 OID 340177)
-- Name: snr_derecho_snr_fuente_derecho_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX snr_derecho_snr_fuente_derecho_idx ON ladm_col_210.snr_derecho USING btree (snr_fuente_derecho);


--
-- TOC entry 12170 (class 1259 OID 340178)
-- Name: snr_derecho_snr_predio_registro_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX snr_derecho_snr_predio_registro_idx ON ladm_col_210.snr_derecho USING btree (snr_predio_registro);


--
-- TOC entry 12175 (class 1259 OID 340179)
-- Name: snr_fuente_cabidalinderos_tipo_documento_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX snr_fuente_cabidalinderos_tipo_documento_idx ON ladm_col_210.snr_fuente_cabidalinderos USING btree (tipo_documento);


--
-- TOC entry 12178 (class 1259 OID 340180)
-- Name: snr_fuente_derecho_tipo_documento_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX snr_fuente_derecho_tipo_documento_idx ON ladm_col_210.snr_fuente_derecho USING btree (tipo_documento);


--
-- TOC entry 12185 (class 1259 OID 340181)
-- Name: snr_predio_registro_snr_fuente_cabidalinderos_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX snr_predio_registro_snr_fuente_cabidalinderos_idx ON ladm_col_210.snr_predio_registro USING btree (snr_fuente_cabidalinderos);


--
-- TOC entry 12192 (class 1259 OID 340182)
-- Name: snr_titular_derecho_snr_derecho_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX snr_titular_derecho_snr_derecho_idx ON ladm_col_210.snr_titular_derecho USING btree (snr_derecho);


--
-- TOC entry 12193 (class 1259 OID 340183)
-- Name: snr_titular_derecho_snr_titular_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX snr_titular_derecho_snr_titular_idx ON ladm_col_210.snr_titular_derecho USING btree (snr_titular);


--
-- TOC entry 12188 (class 1259 OID 340184)
-- Name: snr_titular_tipo_documento_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX snr_titular_tipo_documento_idx ON ladm_col_210.snr_titular USING btree (tipo_documento);


--
-- TOC entry 12189 (class 1259 OID 340185)
-- Name: snr_titular_tipo_persona_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX snr_titular_tipo_persona_idx ON ladm_col_210.snr_titular USING btree (tipo_persona);


--
-- TOC entry 12196 (class 1259 OID 340186)
-- Name: t_ili2db_attrname_sqlname_colowner_key; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE UNIQUE INDEX t_ili2db_attrname_sqlname_colowner_key ON ladm_col_210.t_ili2db_attrname USING btree (sqlname, colowner);


--
-- TOC entry 12197 (class 1259 OID 340187)
-- Name: t_ili2db_basket_dataset_idx; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE INDEX t_ili2db_basket_dataset_idx ON ladm_col_210.t_ili2db_basket USING btree (dataset);


--
-- TOC entry 12202 (class 1259 OID 340188)
-- Name: t_ili2db_dataset_datasetname_key; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE UNIQUE INDEX t_ili2db_dataset_datasetname_key ON ladm_col_210.t_ili2db_dataset USING btree (datasetname);


--
-- TOC entry 12207 (class 1259 OID 340189)
-- Name: t_ili2db_model_iliversion_modelname_key; Type: INDEX; Schema: ladm_col_210; Owner: postgres
--

CREATE UNIQUE INDEX t_ili2db_model_iliversion_modelname_key ON ladm_col_210.t_ili2db_model USING btree (iliversion, modelname);


--
-- TOC entry 12212 (class 2606 OID 340190)
-- Name: anystructure anystructure_op_agrupacion_ntrsds_cldad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_agrupacion_ntrsds_cldad_fkey FOREIGN KEY (op_agrupacion_intrsdos_calidad) REFERENCES ladm_col_210.op_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12213 (class 2606 OID 340195)
-- Name: anystructure anystructure_op_agrupcn_ntrsds_prcdncia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_agrupcn_ntrsds_prcdncia_fkey FOREIGN KEY (op_agrupacion_intrsdos_procedencia) REFERENCES ladm_col_210.op_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12214 (class 2606 OID 340200)
-- Name: anystructure anystructure_op_construccion_calidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_construccion_calidad_fkey FOREIGN KEY (op_construccion_calidad) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12215 (class 2606 OID 340205)
-- Name: anystructure anystructure_op_construccion_procedncia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_construccion_procedncia_fkey FOREIGN KEY (op_construccion_procedencia) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12216 (class 2606 OID 340210)
-- Name: anystructure anystructure_op_derecho_calidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_derecho_calidad_fkey FOREIGN KEY (op_derecho_calidad) REFERENCES ladm_col_210.op_derecho(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12217 (class 2606 OID 340215)
-- Name: anystructure anystructure_op_derecho_procedencia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_derecho_procedencia_fkey FOREIGN KEY (op_derecho_procedencia) REFERENCES ladm_col_210.op_derecho(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12218 (class 2606 OID 340220)
-- Name: anystructure anystructure_op_interesado_calidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_interesado_calidad_fkey FOREIGN KEY (op_interesado_calidad) REFERENCES ladm_col_210.op_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12219 (class 2606 OID 340225)
-- Name: anystructure anystructure_op_interesado_procedencia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_interesado_procedencia_fkey FOREIGN KEY (op_interesado_procedencia) REFERENCES ladm_col_210.op_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12220 (class 2606 OID 340230)
-- Name: anystructure anystructure_op_lindero_calidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_lindero_calidad_fkey FOREIGN KEY (op_lindero_calidad) REFERENCES ladm_col_210.op_lindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12221 (class 2606 OID 340235)
-- Name: anystructure anystructure_op_lindero_procedencia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_lindero_procedencia_fkey FOREIGN KEY (op_lindero_procedencia) REFERENCES ladm_col_210.op_lindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12222 (class 2606 OID 340240)
-- Name: anystructure anystructure_op_predio_calidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_predio_calidad_fkey FOREIGN KEY (op_predio_calidad) REFERENCES ladm_col_210.op_predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12223 (class 2606 OID 340245)
-- Name: anystructure anystructure_op_predio_procedencia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_predio_procedencia_fkey FOREIGN KEY (op_predio_procedencia) REFERENCES ladm_col_210.op_predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12224 (class 2606 OID 340250)
-- Name: anystructure anystructure_op_puntocontrol_calidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_puntocontrol_calidad_fkey FOREIGN KEY (op_puntocontrol_calidad) REFERENCES ladm_col_210.op_puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12225 (class 2606 OID 340255)
-- Name: anystructure anystructure_op_puntocontrol_procedncia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_puntocontrol_procedncia_fkey FOREIGN KEY (op_puntocontrol_procedencia) REFERENCES ladm_col_210.op_puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12226 (class 2606 OID 340260)
-- Name: anystructure anystructure_op_puntolevantamient_cldad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_puntolevantamient_cldad_fkey FOREIGN KEY (op_puntolevantamiento_calidad) REFERENCES ladm_col_210.op_puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12227 (class 2606 OID 340265)
-- Name: anystructure anystructure_op_puntolevantmnt_prcdncia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_puntolevantmnt_prcdncia_fkey FOREIGN KEY (op_puntolevantamiento_procedencia) REFERENCES ladm_col_210.op_puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12228 (class 2606 OID 340270)
-- Name: anystructure anystructure_op_puntolindero_calidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_puntolindero_calidad_fkey FOREIGN KEY (op_puntolindero_calidad) REFERENCES ladm_col_210.op_puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12229 (class 2606 OID 340275)
-- Name: anystructure anystructure_op_puntolindero_procedncia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_puntolindero_procedncia_fkey FOREIGN KEY (op_puntolindero_procedencia) REFERENCES ladm_col_210.op_puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12230 (class 2606 OID 340280)
-- Name: anystructure anystructure_op_restriccion_calidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_restriccion_calidad_fkey FOREIGN KEY (op_restriccion_calidad) REFERENCES ladm_col_210.op_restriccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12231 (class 2606 OID 340285)
-- Name: anystructure anystructure_op_restriccion_procedencia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_restriccion_procedencia_fkey FOREIGN KEY (op_restriccion_procedencia) REFERENCES ladm_col_210.op_restriccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12232 (class 2606 OID 340290)
-- Name: anystructure anystructure_op_servidmbrtrnst_prcdncia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_servidmbrtrnst_prcdncia_fkey FOREIGN KEY (op_servidumbretransito_procedencia) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12233 (class 2606 OID 340295)
-- Name: anystructure anystructure_op_servidumbretranst_cldad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_servidumbretranst_cldad_fkey FOREIGN KEY (op_servidumbretransito_calidad) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12234 (class 2606 OID 340300)
-- Name: anystructure anystructure_op_terreno_calidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_terreno_calidad_fkey FOREIGN KEY (op_terreno_calidad) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12235 (class 2606 OID 340305)
-- Name: anystructure anystructure_op_terreno_procedencia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_terreno_procedencia_fkey FOREIGN KEY (op_terreno_procedencia) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12236 (class 2606 OID 340310)
-- Name: anystructure anystructure_op_unidadcnstrccn_prcdncia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_unidadcnstrccn_prcdncia_fkey FOREIGN KEY (op_unidadconstruccion_procedencia) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12237 (class 2606 OID 340315)
-- Name: anystructure anystructure_op_unidadconstruccin_cldad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.anystructure
    ADD CONSTRAINT anystructure_op_unidadconstruccin_cldad_fkey FOREIGN KEY (op_unidadconstruccion_calidad) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12238 (class 2606 OID 340320)
-- Name: cc_metodooperacion cc_metodooperacion_col_transfrmcn_trnsfrmcion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.cc_metodooperacion
    ADD CONSTRAINT cc_metodooperacion_col_transfrmcn_trnsfrmcion_fkey FOREIGN KEY (col_transformacion_transformacion) REFERENCES ladm_col_210.col_transformacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12239 (class 2606 OID 340325)
-- Name: col_areavalor col_areavalor_atype_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_areavalor
    ADD CONSTRAINT col_areavalor_atype_fkey FOREIGN KEY (atype) REFERENCES ladm_col_210.col_areatipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12240 (class 2606 OID 340330)
-- Name: col_areavalor col_areavalor_op_construccion_area_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_areavalor
    ADD CONSTRAINT col_areavalor_op_construccion_area_fkey FOREIGN KEY (op_construccion_area) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12241 (class 2606 OID 340335)
-- Name: col_areavalor col_areavalor_op_servidumbretransito_rea_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_areavalor
    ADD CONSTRAINT col_areavalor_op_servidumbretransito_rea_fkey FOREIGN KEY (op_servidumbretransito_area) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12242 (class 2606 OID 340340)
-- Name: col_areavalor col_areavalor_op_terreno_area_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_areavalor
    ADD CONSTRAINT col_areavalor_op_terreno_area_fkey FOREIGN KEY (op_terreno_area) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12243 (class 2606 OID 340345)
-- Name: col_areavalor col_areavalor_op_unidadconstruccion_area_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_areavalor
    ADD CONSTRAINT col_areavalor_op_unidadconstruccion_area_fkey FOREIGN KEY (op_unidadconstruccion_area) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12244 (class 2606 OID 340350)
-- Name: col_baunitcomointeresado col_baunitcomointeresado_interesado_op_interesado_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_baunitcomointeresado
    ADD CONSTRAINT col_baunitcomointeresado_interesado_op_interesado_fkey FOREIGN KEY (interesado_op_interesado) REFERENCES ladm_col_210.op_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12245 (class 2606 OID 340355)
-- Name: col_baunitcomointeresado col_baunitcomointeresado_interesado_p_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_baunitcomointeresado
    ADD CONSTRAINT col_baunitcomointeresado_interesado_p_grpcn_ntrsdos_fkey FOREIGN KEY (interesado_op_agrupacion_interesados) REFERENCES ladm_col_210.op_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12246 (class 2606 OID 340360)
-- Name: col_baunitcomointeresado col_baunitcomointeresado_unidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_baunitcomointeresado
    ADD CONSTRAINT col_baunitcomointeresado_unidad_fkey FOREIGN KEY (unidad) REFERENCES ladm_col_210.op_predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12247 (class 2606 OID 340365)
-- Name: col_baunitfuente col_baunitfuente_fuente_espacial_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_baunitfuente
    ADD CONSTRAINT col_baunitfuente_fuente_espacial_fkey FOREIGN KEY (fuente_espacial) REFERENCES ladm_col_210.op_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12248 (class 2606 OID 340370)
-- Name: col_baunitfuente col_baunitfuente_unidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_baunitfuente
    ADD CONSTRAINT col_baunitfuente_unidad_fkey FOREIGN KEY (unidad) REFERENCES ladm_col_210.op_predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12249 (class 2606 OID 340375)
-- Name: col_cclfuente col_cclfuente_ccl_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_cclfuente
    ADD CONSTRAINT col_cclfuente_ccl_fkey FOREIGN KEY (ccl) REFERENCES ladm_col_210.op_lindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12250 (class 2606 OID 340380)
-- Name: col_cclfuente col_cclfuente_fuente_espacial_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_cclfuente
    ADD CONSTRAINT col_cclfuente_fuente_espacial_fkey FOREIGN KEY (fuente_espacial) REFERENCES ladm_col_210.op_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12251 (class 2606 OID 340385)
-- Name: col_clfuente col_clfuente_fuente_espacial_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_clfuente
    ADD CONSTRAINT col_clfuente_fuente_espacial_fkey FOREIGN KEY (fuente_espacial) REFERENCES ladm_col_210.op_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12252 (class 2606 OID 340390)
-- Name: col_masccl col_masccl_ccl_mas_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_masccl
    ADD CONSTRAINT col_masccl_ccl_mas_fkey FOREIGN KEY (ccl_mas) REFERENCES ladm_col_210.op_lindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12253 (class 2606 OID 340395)
-- Name: col_masccl col_masccl_ue_mas_op_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_masccl
    ADD CONSTRAINT col_masccl_ue_mas_op_construccion_fkey FOREIGN KEY (ue_mas_op_construccion) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12254 (class 2606 OID 340400)
-- Name: col_masccl col_masccl_ue_mas_op_servidmbrtrnsito_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_masccl
    ADD CONSTRAINT col_masccl_ue_mas_op_servidmbrtrnsito_fkey FOREIGN KEY (ue_mas_op_servidumbretransito) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12255 (class 2606 OID 340405)
-- Name: col_masccl col_masccl_ue_mas_op_terreno_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_masccl
    ADD CONSTRAINT col_masccl_ue_mas_op_terreno_fkey FOREIGN KEY (ue_mas_op_terreno) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12256 (class 2606 OID 340410)
-- Name: col_masccl col_masccl_ue_mas_op_unidadcnstrccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_masccl
    ADD CONSTRAINT col_masccl_ue_mas_op_unidadcnstrccion_fkey FOREIGN KEY (ue_mas_op_unidadconstruccion) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12257 (class 2606 OID 340415)
-- Name: col_mascl col_mascl_ue_mas_op_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_mascl
    ADD CONSTRAINT col_mascl_ue_mas_op_construccion_fkey FOREIGN KEY (ue_mas_op_construccion) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12258 (class 2606 OID 340420)
-- Name: col_mascl col_mascl_ue_mas_op_servidmbrtrnsito_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_mascl
    ADD CONSTRAINT col_mascl_ue_mas_op_servidmbrtrnsito_fkey FOREIGN KEY (ue_mas_op_servidumbretransito) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12259 (class 2606 OID 340425)
-- Name: col_mascl col_mascl_ue_mas_op_terreno_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_mascl
    ADD CONSTRAINT col_mascl_ue_mas_op_terreno_fkey FOREIGN KEY (ue_mas_op_terreno) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12260 (class 2606 OID 340430)
-- Name: col_mascl col_mascl_ue_mas_op_unidadcnstrccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_mascl
    ADD CONSTRAINT col_mascl_ue_mas_op_unidadcnstrccion_fkey FOREIGN KEY (ue_mas_op_unidadconstruccion) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12261 (class 2606 OID 340435)
-- Name: col_menosccl col_menosccl_ccl_menos_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_menosccl
    ADD CONSTRAINT col_menosccl_ccl_menos_fkey FOREIGN KEY (ccl_menos) REFERENCES ladm_col_210.op_lindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12262 (class 2606 OID 340440)
-- Name: col_menosccl col_menosccl_ue_menos_op_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_menosccl
    ADD CONSTRAINT col_menosccl_ue_menos_op_construccion_fkey FOREIGN KEY (ue_menos_op_construccion) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12263 (class 2606 OID 340445)
-- Name: col_menosccl col_menosccl_ue_menos_op_srvdmbrtrnsito_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_menosccl
    ADD CONSTRAINT col_menosccl_ue_menos_op_srvdmbrtrnsito_fkey FOREIGN KEY (ue_menos_op_servidumbretransito) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12264 (class 2606 OID 340450)
-- Name: col_menosccl col_menosccl_ue_menos_op_terreno_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_menosccl
    ADD CONSTRAINT col_menosccl_ue_menos_op_terreno_fkey FOREIGN KEY (ue_menos_op_terreno) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12265 (class 2606 OID 340455)
-- Name: col_menosccl col_menosccl_ue_menos_op_unddcnstrccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_menosccl
    ADD CONSTRAINT col_menosccl_ue_menos_op_unddcnstrccion_fkey FOREIGN KEY (ue_menos_op_unidadconstruccion) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12266 (class 2606 OID 340460)
-- Name: col_menoscl col_menoscl_ue_menos_op_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_menoscl
    ADD CONSTRAINT col_menoscl_ue_menos_op_construccion_fkey FOREIGN KEY (ue_menos_op_construccion) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12267 (class 2606 OID 340465)
-- Name: col_menoscl col_menoscl_ue_menos_op_srvdmbrtrnsito_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_menoscl
    ADD CONSTRAINT col_menoscl_ue_menos_op_srvdmbrtrnsito_fkey FOREIGN KEY (ue_menos_op_servidumbretransito) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12268 (class 2606 OID 340470)
-- Name: col_menoscl col_menoscl_ue_menos_op_terreno_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_menoscl
    ADD CONSTRAINT col_menoscl_ue_menos_op_terreno_fkey FOREIGN KEY (ue_menos_op_terreno) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12269 (class 2606 OID 340475)
-- Name: col_menoscl col_menoscl_ue_menos_op_unddcnstrccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_menoscl
    ADD CONSTRAINT col_menoscl_ue_menos_op_unddcnstrccion_fkey FOREIGN KEY (ue_menos_op_unidadconstruccion) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12270 (class 2606 OID 340480)
-- Name: col_miembros col_miembros_agrupacion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_miembros
    ADD CONSTRAINT col_miembros_agrupacion_fkey FOREIGN KEY (agrupacion) REFERENCES ladm_col_210.op_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12271 (class 2606 OID 340485)
-- Name: col_miembros col_miembros_interesado_op_interesado_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_miembros
    ADD CONSTRAINT col_miembros_interesado_op_interesado_fkey FOREIGN KEY (interesado_op_interesado) REFERENCES ladm_col_210.op_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12272 (class 2606 OID 340490)
-- Name: col_miembros col_miembros_interesado_p_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_miembros
    ADD CONSTRAINT col_miembros_interesado_p_grpcn_ntrsdos_fkey FOREIGN KEY (interesado_op_agrupacion_interesados) REFERENCES ladm_col_210.op_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12273 (class 2606 OID 340495)
-- Name: col_puntoccl col_puntoccl_ccl_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntoccl
    ADD CONSTRAINT col_puntoccl_ccl_fkey FOREIGN KEY (ccl) REFERENCES ladm_col_210.op_lindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12274 (class 2606 OID 340500)
-- Name: col_puntoccl col_puntoccl_punto_op_puntocontrol_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntoccl
    ADD CONSTRAINT col_puntoccl_punto_op_puntocontrol_fkey FOREIGN KEY (punto_op_puntocontrol) REFERENCES ladm_col_210.op_puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12275 (class 2606 OID 340505)
-- Name: col_puntoccl col_puntoccl_punto_op_puntolevantaminto_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntoccl
    ADD CONSTRAINT col_puntoccl_punto_op_puntolevantaminto_fkey FOREIGN KEY (punto_op_puntolevantamiento) REFERENCES ladm_col_210.op_puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12276 (class 2606 OID 340510)
-- Name: col_puntoccl col_puntoccl_punto_op_puntolindero_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntoccl
    ADD CONSTRAINT col_puntoccl_punto_op_puntolindero_fkey FOREIGN KEY (punto_op_puntolindero) REFERENCES ladm_col_210.op_puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12277 (class 2606 OID 340515)
-- Name: col_puntocl col_puntocl_punto_op_puntocontrol_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntocl
    ADD CONSTRAINT col_puntocl_punto_op_puntocontrol_fkey FOREIGN KEY (punto_op_puntocontrol) REFERENCES ladm_col_210.op_puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12278 (class 2606 OID 340520)
-- Name: col_puntocl col_puntocl_punto_op_puntolevantaminto_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntocl
    ADD CONSTRAINT col_puntocl_punto_op_puntolevantaminto_fkey FOREIGN KEY (punto_op_puntolevantamiento) REFERENCES ladm_col_210.op_puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12279 (class 2606 OID 340525)
-- Name: col_puntocl col_puntocl_punto_op_puntolindero_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntocl
    ADD CONSTRAINT col_puntocl_punto_op_puntolindero_fkey FOREIGN KEY (punto_op_puntolindero) REFERENCES ladm_col_210.op_puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12280 (class 2606 OID 340530)
-- Name: col_puntofuente col_puntofuente_fuente_espacial_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntofuente
    ADD CONSTRAINT col_puntofuente_fuente_espacial_fkey FOREIGN KEY (fuente_espacial) REFERENCES ladm_col_210.op_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12281 (class 2606 OID 340535)
-- Name: col_puntofuente col_puntofuente_punto_op_puntocontrol_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntofuente
    ADD CONSTRAINT col_puntofuente_punto_op_puntocontrol_fkey FOREIGN KEY (punto_op_puntocontrol) REFERENCES ladm_col_210.op_puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12282 (class 2606 OID 340540)
-- Name: col_puntofuente col_puntofuente_punto_op_puntolevantaminto_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntofuente
    ADD CONSTRAINT col_puntofuente_punto_op_puntolevantaminto_fkey FOREIGN KEY (punto_op_puntolevantamiento) REFERENCES ladm_col_210.op_puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12283 (class 2606 OID 340545)
-- Name: col_puntofuente col_puntofuente_punto_op_puntolindero_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_puntofuente
    ADD CONSTRAINT col_puntofuente_punto_op_puntolindero_fkey FOREIGN KEY (punto_op_puntolindero) REFERENCES ladm_col_210.op_puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12284 (class 2606 OID 340550)
-- Name: col_relacionfuente col_relacionfuente_fuente_administrativa_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_relacionfuente
    ADD CONSTRAINT col_relacionfuente_fuente_administrativa_fkey FOREIGN KEY (fuente_administrativa) REFERENCES ladm_col_210.op_fuenteadministrativa(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12285 (class 2606 OID 340555)
-- Name: col_relacionfuenteuespacial col_relacionfuenteuespcial_fuente_espacial_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_relacionfuenteuespacial
    ADD CONSTRAINT col_relacionfuenteuespcial_fuente_espacial_fkey FOREIGN KEY (fuente_espacial) REFERENCES ladm_col_210.op_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12286 (class 2606 OID 340560)
-- Name: col_responsablefuente col_responsablefuente_fuente_administrativa_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_responsablefuente
    ADD CONSTRAINT col_responsablefuente_fuente_administrativa_fkey FOREIGN KEY (fuente_administrativa) REFERENCES ladm_col_210.op_fuenteadministrativa(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12287 (class 2606 OID 340565)
-- Name: col_responsablefuente col_responsablefuente_interesado_op_interesado_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_responsablefuente
    ADD CONSTRAINT col_responsablefuente_interesado_op_interesado_fkey FOREIGN KEY (interesado_op_interesado) REFERENCES ladm_col_210.op_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12288 (class 2606 OID 340570)
-- Name: col_responsablefuente col_responsablefuente_interesado_p_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_responsablefuente
    ADD CONSTRAINT col_responsablefuente_interesado_p_grpcn_ntrsdos_fkey FOREIGN KEY (interesado_op_agrupacion_interesados) REFERENCES ladm_col_210.op_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12289 (class 2606 OID 340575)
-- Name: col_rrrfuente col_rrrfuente_fuente_administrativa_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_rrrfuente
    ADD CONSTRAINT col_rrrfuente_fuente_administrativa_fkey FOREIGN KEY (fuente_administrativa) REFERENCES ladm_col_210.op_fuenteadministrativa(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12290 (class 2606 OID 340580)
-- Name: col_rrrfuente col_rrrfuente_rrr_op_derecho_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_rrrfuente
    ADD CONSTRAINT col_rrrfuente_rrr_op_derecho_fkey FOREIGN KEY (rrr_op_derecho) REFERENCES ladm_col_210.op_derecho(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12291 (class 2606 OID 340585)
-- Name: col_rrrfuente col_rrrfuente_rrr_op_restriccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_rrrfuente
    ADD CONSTRAINT col_rrrfuente_rrr_op_restriccion_fkey FOREIGN KEY (rrr_op_restriccion) REFERENCES ladm_col_210.op_restriccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12292 (class 2606 OID 340590)
-- Name: col_topografofuente col_topografofuente_fuente_espacial_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_topografofuente
    ADD CONSTRAINT col_topografofuente_fuente_espacial_fkey FOREIGN KEY (fuente_espacial) REFERENCES ladm_col_210.op_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12293 (class 2606 OID 340595)
-- Name: col_topografofuente col_topografofuente_topografo_op_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_topografofuente
    ADD CONSTRAINT col_topografofuente_topografo_op_grpcn_ntrsdos_fkey FOREIGN KEY (topografo_op_agrupacion_interesados) REFERENCES ladm_col_210.op_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12294 (class 2606 OID 340600)
-- Name: col_topografofuente col_topografofuente_topografo_op_interesado_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_topografofuente
    ADD CONSTRAINT col_topografofuente_topografo_op_interesado_fkey FOREIGN KEY (topografo_op_interesado) REFERENCES ladm_col_210.op_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12295 (class 2606 OID 340605)
-- Name: col_transformacion col_transformacion_op_pntcntrl_tmcn_y_rsltado_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_transformacion
    ADD CONSTRAINT col_transformacion_op_pntcntrl_tmcn_y_rsltado_fkey FOREIGN KEY (op_puntocontrol_transformacion_y_resultado) REFERENCES ladm_col_210.op_puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12296 (class 2606 OID 340610)
-- Name: col_transformacion col_transformacion_op_pntlndr_trmcn_y_rsltado_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_transformacion
    ADD CONSTRAINT col_transformacion_op_pntlndr_trmcn_y_rsltado_fkey FOREIGN KEY (op_puntolindero_transformacion_y_resultado) REFERENCES ladm_col_210.op_puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12297 (class 2606 OID 340615)
-- Name: col_transformacion col_transformacion_op_pntlvntmntmcn_y_rsltado_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_transformacion
    ADD CONSTRAINT col_transformacion_op_pntlvntmntmcn_y_rsltado_fkey FOREIGN KEY (op_puntolevantamiento_transformacion_y_resultado) REFERENCES ladm_col_210.op_puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12298 (class 2606 OID 340620)
-- Name: col_uebaunit col_uebaunit_baunit_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_uebaunit
    ADD CONSTRAINT col_uebaunit_baunit_fkey FOREIGN KEY (baunit) REFERENCES ladm_col_210.op_predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12299 (class 2606 OID 340625)
-- Name: col_uebaunit col_uebaunit_ue_op_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_uebaunit
    ADD CONSTRAINT col_uebaunit_ue_op_construccion_fkey FOREIGN KEY (ue_op_construccion) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12300 (class 2606 OID 340630)
-- Name: col_uebaunit col_uebaunit_ue_op_servidumbretransito_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_uebaunit
    ADD CONSTRAINT col_uebaunit_ue_op_servidumbretransito_fkey FOREIGN KEY (ue_op_servidumbretransito) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12301 (class 2606 OID 340635)
-- Name: col_uebaunit col_uebaunit_ue_op_terreno_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_uebaunit
    ADD CONSTRAINT col_uebaunit_ue_op_terreno_fkey FOREIGN KEY (ue_op_terreno) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12302 (class 2606 OID 340640)
-- Name: col_uebaunit col_uebaunit_ue_op_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_uebaunit
    ADD CONSTRAINT col_uebaunit_ue_op_unidadconstruccion_fkey FOREIGN KEY (ue_op_unidadconstruccion) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12303 (class 2606 OID 340645)
-- Name: col_uefuente col_uefuente_fuente_espacial_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_uefuente
    ADD CONSTRAINT col_uefuente_fuente_espacial_fkey FOREIGN KEY (fuente_espacial) REFERENCES ladm_col_210.op_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12304 (class 2606 OID 340650)
-- Name: col_uefuente col_uefuente_ue_op_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_uefuente
    ADD CONSTRAINT col_uefuente_ue_op_construccion_fkey FOREIGN KEY (ue_op_construccion) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12305 (class 2606 OID 340655)
-- Name: col_uefuente col_uefuente_ue_op_servidumbretransito_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_uefuente
    ADD CONSTRAINT col_uefuente_ue_op_servidumbretransito_fkey FOREIGN KEY (ue_op_servidumbretransito) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12306 (class 2606 OID 340660)
-- Name: col_uefuente col_uefuente_ue_op_terreno_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_uefuente
    ADD CONSTRAINT col_uefuente_ue_op_terreno_fkey FOREIGN KEY (ue_op_terreno) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12307 (class 2606 OID 340665)
-- Name: col_uefuente col_uefuente_ue_op_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_uefuente
    ADD CONSTRAINT col_uefuente_ue_op_unidadconstruccion_fkey FOREIGN KEY (ue_op_unidadconstruccion) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12308 (class 2606 OID 340670)
-- Name: col_ueuegrupo col_ueuegrupo_parte_op_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_ueuegrupo
    ADD CONSTRAINT col_ueuegrupo_parte_op_construccion_fkey FOREIGN KEY (parte_op_construccion) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12309 (class 2606 OID 340675)
-- Name: col_ueuegrupo col_ueuegrupo_parte_op_servidumbrtrnsito_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_ueuegrupo
    ADD CONSTRAINT col_ueuegrupo_parte_op_servidumbrtrnsito_fkey FOREIGN KEY (parte_op_servidumbretransito) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12310 (class 2606 OID 340680)
-- Name: col_ueuegrupo col_ueuegrupo_parte_op_terreno_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_ueuegrupo
    ADD CONSTRAINT col_ueuegrupo_parte_op_terreno_fkey FOREIGN KEY (parte_op_terreno) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12311 (class 2606 OID 340685)
-- Name: col_ueuegrupo col_ueuegrupo_parte_op_unidadconstrccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_ueuegrupo
    ADD CONSTRAINT col_ueuegrupo_parte_op_unidadconstrccion_fkey FOREIGN KEY (parte_op_unidadconstruccion) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12312 (class 2606 OID 340690)
-- Name: col_unidadfuente col_unidadfuente_fuente_administrativa_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_unidadfuente
    ADD CONSTRAINT col_unidadfuente_fuente_administrativa_fkey FOREIGN KEY (fuente_administrativa) REFERENCES ladm_col_210.op_fuenteadministrativa(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12313 (class 2606 OID 340695)
-- Name: col_unidadfuente col_unidadfuente_unidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_unidadfuente
    ADD CONSTRAINT col_unidadfuente_unidad_fkey FOREIGN KEY (unidad) REFERENCES ladm_col_210.op_predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12314 (class 2606 OID 340700)
-- Name: col_volumenvalor col_volumenvalor_op_construccion_volumen_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_volumenvalor
    ADD CONSTRAINT col_volumenvalor_op_construccion_volumen_fkey FOREIGN KEY (op_construccion_volumen) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12315 (class 2606 OID 340705)
-- Name: col_volumenvalor col_volumenvalor_op_servidumbretranst_vlmen_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_volumenvalor
    ADD CONSTRAINT col_volumenvalor_op_servidumbretranst_vlmen_fkey FOREIGN KEY (op_servidumbretransito_volumen) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12316 (class 2606 OID 340710)
-- Name: col_volumenvalor col_volumenvalor_op_terreno_volumen_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_volumenvalor
    ADD CONSTRAINT col_volumenvalor_op_terreno_volumen_fkey FOREIGN KEY (op_terreno_volumen) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12317 (class 2606 OID 340715)
-- Name: col_volumenvalor col_volumenvalor_op_unidadconstruccin_vlmen_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_volumenvalor
    ADD CONSTRAINT col_volumenvalor_op_unidadconstruccin_vlmen_fkey FOREIGN KEY (op_unidadconstruccion_volumen) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12318 (class 2606 OID 340720)
-- Name: col_volumenvalor col_volumenvalor_tipo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.col_volumenvalor
    ADD CONSTRAINT col_volumenvalor_tipo_fkey FOREIGN KEY (tipo) REFERENCES ladm_col_210.col_volumentipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12319 (class 2606 OID 340725)
-- Name: extarchivo extarchivo_op_fuenteespacl_xt_rchv_id_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extarchivo
    ADD CONSTRAINT extarchivo_op_fuenteespacl_xt_rchv_id_fkey FOREIGN KEY (op_fuenteespacial_ext_archivo_id) REFERENCES ladm_col_210.op_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12320 (class 2606 OID 340730)
-- Name: extarchivo extarchivo_op_funtdmnstrtv_xt_rchv_id_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extarchivo
    ADD CONSTRAINT extarchivo_op_funtdmnstrtv_xt_rchv_id_fkey FOREIGN KEY (op_fuenteadministrtiva_ext_archivo_id) REFERENCES ladm_col_210.op_fuenteadministrativa(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12321 (class 2606 OID 340735)
-- Name: extarchivo extarchivo_snr_fuente_cbdlndrs_rchivo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extarchivo
    ADD CONSTRAINT extarchivo_snr_fuente_cbdlndrs_rchivo_fkey FOREIGN KEY (snr_fuente_cabidlndros_archivo) REFERENCES ladm_col_210.snr_fuente_cabidalinderos(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12322 (class 2606 OID 340740)
-- Name: extdireccion extdireccion_clase_via_principal_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion
    ADD CONSTRAINT extdireccion_clase_via_principal_fkey FOREIGN KEY (clase_via_principal) REFERENCES ladm_col_210.extdireccion_clase_via_principal(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12323 (class 2606 OID 340745)
-- Name: extdireccion extdireccion_extinteresado_ext_drccn_id_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion
    ADD CONSTRAINT extdireccion_extinteresado_ext_drccn_id_fkey FOREIGN KEY (extinteresado_ext_direccion_id) REFERENCES ladm_col_210.extinteresado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12324 (class 2606 OID 340750)
-- Name: extdireccion extdireccion_extndddfccnfsc_xt_drccn_id_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion
    ADD CONSTRAINT extdireccion_extndddfccnfsc_xt_drccn_id_fkey FOREIGN KEY (extunidadedificcnfsica_ext_direccion_id) REFERENCES ladm_col_210.extunidadedificacionfisica(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12325 (class 2606 OID 340755)
-- Name: extdireccion extdireccion_op_construccin_xt_drccn_id_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion
    ADD CONSTRAINT extdireccion_op_construccin_xt_drccn_id_fkey FOREIGN KEY (op_construccion_ext_direccion_id) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12326 (class 2606 OID 340760)
-- Name: extdireccion extdireccion_op_nddcnstrccn_xt_drccn_id_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion
    ADD CONSTRAINT extdireccion_op_nddcnstrccn_xt_drccn_id_fkey FOREIGN KEY (op_unidadconstruccion_ext_direccion_id) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12327 (class 2606 OID 340765)
-- Name: extdireccion extdireccion_op_srvdmbrtrnt_xt_drccn_id_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion
    ADD CONSTRAINT extdireccion_op_srvdmbrtrnt_xt_drccn_id_fkey FOREIGN KEY (op_servidumbretransito_ext_direccion_id) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12328 (class 2606 OID 340770)
-- Name: extdireccion extdireccion_op_terreno_ext_direccin_id_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion
    ADD CONSTRAINT extdireccion_op_terreno_ext_direccin_id_fkey FOREIGN KEY (op_terreno_ext_direccion_id) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12329 (class 2606 OID 340775)
-- Name: extdireccion extdireccion_sector_ciudad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion
    ADD CONSTRAINT extdireccion_sector_ciudad_fkey FOREIGN KEY (sector_ciudad) REFERENCES ladm_col_210.extdireccion_sector_ciudad(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12330 (class 2606 OID 340780)
-- Name: extdireccion extdireccion_sector_predio_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion
    ADD CONSTRAINT extdireccion_sector_predio_fkey FOREIGN KEY (sector_predio) REFERENCES ladm_col_210.extdireccion_sector_predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12331 (class 2606 OID 340785)
-- Name: extdireccion extdireccion_tipo_direccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extdireccion
    ADD CONSTRAINT extdireccion_tipo_direccion_fkey FOREIGN KEY (tipo_direccion) REFERENCES ladm_col_210.extdireccion_tipo_direccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12332 (class 2606 OID 340790)
-- Name: extinteresado extinteresado_extrdsrvcsfscd_dmnstrdr_id_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extinteresado
    ADD CONSTRAINT extinteresado_extrdsrvcsfscd_dmnstrdr_id_fkey FOREIGN KEY (extredserviciosfisica_ext_interesado_administrador_id) REFERENCES ladm_col_210.extredserviciosfisica(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12333 (class 2606 OID 340795)
-- Name: extinteresado extinteresado_op_agrupacin_ntrsds_xt_pid_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extinteresado
    ADD CONSTRAINT extinteresado_op_agrupacin_ntrsds_xt_pid_fkey FOREIGN KEY (op_agrupacion_intrsdos_ext_pid) REFERENCES ladm_col_210.op_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12334 (class 2606 OID 340800)
-- Name: extinteresado extinteresado_op_interesado_ext_pid_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.extinteresado
    ADD CONSTRAINT extinteresado_op_interesado_ext_pid_fkey FOREIGN KEY (op_interesado_ext_pid) REFERENCES ladm_col_210.op_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12335 (class 2606 OID 340805)
-- Name: fraccion fraccion_col_miembros_participacion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.fraccion
    ADD CONSTRAINT fraccion_col_miembros_participacion_fkey FOREIGN KEY (col_miembros_participacion) REFERENCES ladm_col_210.col_miembros(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12336 (class 2606 OID 340810)
-- Name: fraccion fraccion_op_predio_copropidd_cfcnte_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.fraccion
    ADD CONSTRAINT fraccion_op_predio_copropidd_cfcnte_fkey FOREIGN KEY (op_predio_copropiedad_coeficiente) REFERENCES ladm_col_210.op_predio_copropiedad(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12337 (class 2606 OID 340815)
-- Name: gc_construccion gc_construccion_gc_predio_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_construccion
    ADD CONSTRAINT gc_construccion_gc_predio_fkey FOREIGN KEY (gc_predio) REFERENCES ladm_col_210.gc_predio_catastro(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12338 (class 2606 OID 340820)
-- Name: gc_construccion gc_construccion_tipo_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_construccion
    ADD CONSTRAINT gc_construccion_tipo_construccion_fkey FOREIGN KEY (tipo_construccion) REFERENCES ladm_col_210.gc_unidadconstrucciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12339 (class 2606 OID 340825)
-- Name: gc_copropiedad gc_copropiedad_gc_matriz_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_copropiedad
    ADD CONSTRAINT gc_copropiedad_gc_matriz_fkey FOREIGN KEY (gc_matriz) REFERENCES ladm_col_210.gc_predio_catastro(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12340 (class 2606 OID 340830)
-- Name: gc_copropiedad gc_copropiedad_gc_unidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_copropiedad
    ADD CONSTRAINT gc_copropiedad_gc_unidad_fkey FOREIGN KEY (gc_unidad) REFERENCES ladm_col_210.gc_predio_catastro(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12341 (class 2606 OID 340835)
-- Name: gc_datos_ph_condiminio gc_datos_ph_condiminio_gc_predio_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_datos_ph_condiminio
    ADD CONSTRAINT gc_datos_ph_condiminio_gc_predio_fkey FOREIGN KEY (gc_predio) REFERENCES ladm_col_210.gc_predio_catastro(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12342 (class 2606 OID 340840)
-- Name: gc_direccion gc_direccion_gc_predio_catastro_drccnes_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_direccion
    ADD CONSTRAINT gc_direccion_gc_predio_catastro_drccnes_fkey FOREIGN KEY (gc_predio_catastro_direcciones) REFERENCES ladm_col_210.gc_predio_catastro(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12343 (class 2606 OID 340845)
-- Name: gc_predio_catastro gc_predio_catastro_condicion_predio_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_predio_catastro
    ADD CONSTRAINT gc_predio_catastro_condicion_predio_fkey FOREIGN KEY (condicion_predio) REFERENCES ladm_col_210.gc_condicionprediotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12344 (class 2606 OID 340850)
-- Name: gc_predio_catastro gc_predio_catastro_sistema_procedencia_datos_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_predio_catastro
    ADD CONSTRAINT gc_predio_catastro_sistema_procedencia_datos_fkey FOREIGN KEY (sistema_procedencia_datos) REFERENCES ladm_col_210.gc_sistemaprocedenciadatostipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12345 (class 2606 OID 340855)
-- Name: gc_propietario gc_propietario_gc_predio_catastro_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_propietario
    ADD CONSTRAINT gc_propietario_gc_predio_catastro_fkey FOREIGN KEY (gc_predio_catastro) REFERENCES ladm_col_210.gc_predio_catastro(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12346 (class 2606 OID 340860)
-- Name: gc_terreno gc_terreno_gc_predio_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_terreno
    ADD CONSTRAINT gc_terreno_gc_predio_fkey FOREIGN KEY (gc_predio) REFERENCES ladm_col_210.gc_predio_catastro(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12347 (class 2606 OID 340865)
-- Name: gc_unidad_construccion gc_unidad_construccion_gc_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_unidad_construccion
    ADD CONSTRAINT gc_unidad_construccion_gc_construccion_fkey FOREIGN KEY (gc_construccion) REFERENCES ladm_col_210.gc_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12348 (class 2606 OID 340870)
-- Name: gc_unidad_construccion gc_unidad_construccion_tipo_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gc_unidad_construccion
    ADD CONSTRAINT gc_unidad_construccion_tipo_construccion_fkey FOREIGN KEY (tipo_construccion) REFERENCES ladm_col_210.gc_unidadconstrucciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12349 (class 2606 OID 340875)
-- Name: gm_surface2dlistvalue gm_surface2dlistvalue_gm_multisurface2d_geometry_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gm_surface2dlistvalue
    ADD CONSTRAINT gm_surface2dlistvalue_gm_multisurface2d_geometry_fkey FOREIGN KEY (gm_multisurface2d_geometry) REFERENCES ladm_col_210.gm_multisurface2d(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12350 (class 2606 OID 340880)
-- Name: gm_surface3dlistvalue gm_surface3dlistvalue_gm_multisurface3d_geometry_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.gm_surface3dlistvalue
    ADD CONSTRAINT gm_surface3dlistvalue_gm_multisurface3d_geometry_fkey FOREIGN KEY (gm_multisurface3d_geometry) REFERENCES ladm_col_210.gm_multisurface3d(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12351 (class 2606 OID 340885)
-- Name: imagen imagen_extinteresado_firma_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.imagen
    ADD CONSTRAINT imagen_extinteresado_firma_fkey FOREIGN KEY (extinteresado_firma) REFERENCES ladm_col_210.extinteresado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12352 (class 2606 OID 340890)
-- Name: imagen imagen_extinteresado_fotografia_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.imagen
    ADD CONSTRAINT imagen_extinteresado_fotografia_fkey FOREIGN KEY (extinteresado_fotografia) REFERENCES ladm_col_210.extinteresado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12353 (class 2606 OID 340895)
-- Name: imagen imagen_extinteresado_huell_dctlar_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.imagen
    ADD CONSTRAINT imagen_extinteresado_huell_dctlar_fkey FOREIGN KEY (extinteresado_huella_dactilar) REFERENCES ladm_col_210.extinteresado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12354 (class 2606 OID 340900)
-- Name: ini_predio_insumos ini_predio_insumos_gc_predio_catastro_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.ini_predio_insumos
    ADD CONSTRAINT ini_predio_insumos_gc_predio_catastro_fkey FOREIGN KEY (gc_predio_catastro) REFERENCES ladm_col_210.gc_predio_catastro(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12355 (class 2606 OID 340905)
-- Name: ini_predio_insumos ini_predio_insumos_snr_predio_juridico_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.ini_predio_insumos
    ADD CONSTRAINT ini_predio_insumos_snr_predio_juridico_fkey FOREIGN KEY (snr_predio_juridico) REFERENCES ladm_col_210.snr_predio_registro(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12356 (class 2606 OID 340910)
-- Name: op_agrupacion_interesados op_agrupacion_interesados_tipo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_agrupacion_interesados
    ADD CONSTRAINT op_agrupacion_interesados_tipo_fkey FOREIGN KEY (tipo) REFERENCES ladm_col_210.col_grupointeresadotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12357 (class 2606 OID 340915)
-- Name: op_construccion op_construccion_dimension_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_construccion
    ADD CONSTRAINT op_construccion_dimension_fkey FOREIGN KEY (dimension) REFERENCES ladm_col_210.col_dimensiontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12358 (class 2606 OID 340920)
-- Name: op_construccion op_construccion_relacion_superficie_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_construccion
    ADD CONSTRAINT op_construccion_relacion_superficie_fkey FOREIGN KEY (relacion_superficie) REFERENCES ladm_col_210.col_relacionsuperficietipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12359 (class 2606 OID 340925)
-- Name: op_construccion op_construccion_tipo_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_construccion
    ADD CONSTRAINT op_construccion_tipo_construccion_fkey FOREIGN KEY (tipo_construccion) REFERENCES ladm_col_210.op_construcciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12360 (class 2606 OID 340930)
-- Name: op_construccion op_construccion_tipo_dominio_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_construccion
    ADD CONSTRAINT op_construccion_tipo_dominio_fkey FOREIGN KEY (tipo_dominio) REFERENCES ladm_col_210.op_dominioconstrucciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12361 (class 2606 OID 340935)
-- Name: op_datos_ph_condominio op_datos_ph_condominio_op_predio_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_datos_ph_condominio
    ADD CONSTRAINT op_datos_ph_condominio_op_predio_fkey FOREIGN KEY (op_predio) REFERENCES ladm_col_210.op_predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12362 (class 2606 OID 340940)
-- Name: op_derecho op_derecho_interesado_op_interesado_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_derecho
    ADD CONSTRAINT op_derecho_interesado_op_interesado_fkey FOREIGN KEY (interesado_op_interesado) REFERENCES ladm_col_210.op_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12363 (class 2606 OID 340945)
-- Name: op_derecho op_derecho_interesado_p_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_derecho
    ADD CONSTRAINT op_derecho_interesado_p_grpcn_ntrsdos_fkey FOREIGN KEY (interesado_op_agrupacion_interesados) REFERENCES ladm_col_210.op_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12364 (class 2606 OID 340950)
-- Name: op_derecho op_derecho_tipo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_derecho
    ADD CONSTRAINT op_derecho_tipo_fkey FOREIGN KEY (tipo) REFERENCES ladm_col_210.op_derechotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12365 (class 2606 OID 340955)
-- Name: op_derecho op_derecho_unidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_derecho
    ADD CONSTRAINT op_derecho_unidad_fkey FOREIGN KEY (unidad) REFERENCES ladm_col_210.op_predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12366 (class 2606 OID 340960)
-- Name: op_fuenteadministrativa op_fuenteadministrativa_estado_disponibilidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_fuenteadministrativa
    ADD CONSTRAINT op_fuenteadministrativa_estado_disponibilidad_fkey FOREIGN KEY (estado_disponibilidad) REFERENCES ladm_col_210.col_estadodisponibilidadtipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12367 (class 2606 OID 340965)
-- Name: op_fuenteadministrativa op_fuenteadministrativa_tipo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_fuenteadministrativa
    ADD CONSTRAINT op_fuenteadministrativa_tipo_fkey FOREIGN KEY (tipo) REFERENCES ladm_col_210.op_fuenteadministrativatipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12368 (class 2606 OID 340970)
-- Name: op_fuenteadministrativa op_fuenteadministrativa_tipo_principal_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_fuenteadministrativa
    ADD CONSTRAINT op_fuenteadministrativa_tipo_principal_fkey FOREIGN KEY (tipo_principal) REFERENCES ladm_col_210.ci_forma_presentacion_codigo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12369 (class 2606 OID 340975)
-- Name: op_fuenteespacial op_fuenteespacial_estado_disponibilidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_fuenteespacial
    ADD CONSTRAINT op_fuenteespacial_estado_disponibilidad_fkey FOREIGN KEY (estado_disponibilidad) REFERENCES ladm_col_210.col_estadodisponibilidadtipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12370 (class 2606 OID 340980)
-- Name: op_fuenteespacial op_fuenteespacial_tipo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_fuenteespacial
    ADD CONSTRAINT op_fuenteespacial_tipo_fkey FOREIGN KEY (tipo) REFERENCES ladm_col_210.col_fuenteespacialtipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12371 (class 2606 OID 340985)
-- Name: op_fuenteespacial op_fuenteespacial_tipo_principal_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_fuenteespacial
    ADD CONSTRAINT op_fuenteespacial_tipo_principal_fkey FOREIGN KEY (tipo_principal) REFERENCES ladm_col_210.ci_forma_presentacion_codigo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12376 (class 2606 OID 340990)
-- Name: op_interesado_contacto op_interesado_contacto_op_interesado_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_interesado_contacto
    ADD CONSTRAINT op_interesado_contacto_op_interesado_fkey FOREIGN KEY (op_interesado) REFERENCES ladm_col_210.op_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12372 (class 2606 OID 340995)
-- Name: op_interesado op_interesado_grupo_etnico_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_interesado
    ADD CONSTRAINT op_interesado_grupo_etnico_fkey FOREIGN KEY (grupo_etnico) REFERENCES ladm_col_210.op_grupoetnicotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12373 (class 2606 OID 341000)
-- Name: op_interesado op_interesado_sexo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_interesado
    ADD CONSTRAINT op_interesado_sexo_fkey FOREIGN KEY (sexo) REFERENCES ladm_col_210.op_sexotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12374 (class 2606 OID 341005)
-- Name: op_interesado op_interesado_tipo_documento_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_interesado
    ADD CONSTRAINT op_interesado_tipo_documento_fkey FOREIGN KEY (tipo_documento) REFERENCES ladm_col_210.op_interesadodocumentotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12375 (class 2606 OID 341010)
-- Name: op_interesado op_interesado_tipo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_interesado
    ADD CONSTRAINT op_interesado_tipo_fkey FOREIGN KEY (tipo) REFERENCES ladm_col_210.op_interesadotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12377 (class 2606 OID 341015)
-- Name: op_predio op_predio_condicion_predio_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_predio
    ADD CONSTRAINT op_predio_condicion_predio_fkey FOREIGN KEY (condicion_predio) REFERENCES ladm_col_210.op_condicionprediotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12379 (class 2606 OID 341020)
-- Name: op_predio_copropiedad op_predio_copropiedad_copropiedad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_predio_copropiedad
    ADD CONSTRAINT op_predio_copropiedad_copropiedad_fkey FOREIGN KEY (copropiedad) REFERENCES ladm_col_210.op_predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12380 (class 2606 OID 341025)
-- Name: op_predio_copropiedad op_predio_copropiedad_predio_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_predio_copropiedad
    ADD CONSTRAINT op_predio_copropiedad_predio_fkey FOREIGN KEY (predio) REFERENCES ladm_col_210.op_predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12381 (class 2606 OID 341030)
-- Name: op_predio_insumos_operacion op_predio_insumos_opercion_ini_predio_insumos_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_predio_insumos_operacion
    ADD CONSTRAINT op_predio_insumos_opercion_ini_predio_insumos_fkey FOREIGN KEY (ini_predio_insumos) REFERENCES ladm_col_210.ini_predio_insumos(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12382 (class 2606 OID 341035)
-- Name: op_predio_insumos_operacion op_predio_insumos_opercion_op_predio_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_predio_insumos_operacion
    ADD CONSTRAINT op_predio_insumos_opercion_op_predio_fkey FOREIGN KEY (op_predio) REFERENCES ladm_col_210.op_predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12378 (class 2606 OID 341040)
-- Name: op_predio op_predio_tipo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_predio
    ADD CONSTRAINT op_predio_tipo_fkey FOREIGN KEY (tipo) REFERENCES ladm_col_210.col_baunittipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12383 (class 2606 OID 341045)
-- Name: op_puntocontrol op_puntocontrol_metodoproduccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntocontrol
    ADD CONSTRAINT op_puntocontrol_metodoproduccion_fkey FOREIGN KEY (metodoproduccion) REFERENCES ladm_col_210.col_metodoproducciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12384 (class 2606 OID 341050)
-- Name: op_puntocontrol op_puntocontrol_posicion_interpolacion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntocontrol
    ADD CONSTRAINT op_puntocontrol_posicion_interpolacion_fkey FOREIGN KEY (posicion_interpolacion) REFERENCES ladm_col_210.col_interpolaciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12385 (class 2606 OID 341055)
-- Name: op_puntocontrol op_puntocontrol_puntotipo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntocontrol
    ADD CONSTRAINT op_puntocontrol_puntotipo_fkey FOREIGN KEY (puntotipo) REFERENCES ladm_col_210.op_puntotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12386 (class 2606 OID 341060)
-- Name: op_puntocontrol op_puntocontrol_tipo_punto_control_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntocontrol
    ADD CONSTRAINT op_puntocontrol_tipo_punto_control_fkey FOREIGN KEY (tipo_punto_control) REFERENCES ladm_col_210.op_puntocontroltipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12387 (class 2606 OID 341065)
-- Name: op_puntocontrol op_puntocontrol_ue_op_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntocontrol
    ADD CONSTRAINT op_puntocontrol_ue_op_construccion_fkey FOREIGN KEY (ue_op_construccion) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12388 (class 2606 OID 341070)
-- Name: op_puntocontrol op_puntocontrol_ue_op_servidumbretransito_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntocontrol
    ADD CONSTRAINT op_puntocontrol_ue_op_servidumbretransito_fkey FOREIGN KEY (ue_op_servidumbretransito) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12389 (class 2606 OID 341075)
-- Name: op_puntocontrol op_puntocontrol_ue_op_terreno_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntocontrol
    ADD CONSTRAINT op_puntocontrol_ue_op_terreno_fkey FOREIGN KEY (ue_op_terreno) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12390 (class 2606 OID 341080)
-- Name: op_puntocontrol op_puntocontrol_ue_op_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntocontrol
    ADD CONSTRAINT op_puntocontrol_ue_op_unidadconstruccion_fkey FOREIGN KEY (ue_op_unidadconstruccion) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12391 (class 2606 OID 341085)
-- Name: op_puntolevantamiento op_puntolevantamiento_fotoidentificacion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolevantamiento
    ADD CONSTRAINT op_puntolevantamiento_fotoidentificacion_fkey FOREIGN KEY (fotoidentificacion) REFERENCES ladm_col_210.op_fotoidentificaciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12392 (class 2606 OID 341090)
-- Name: op_puntolevantamiento op_puntolevantamiento_metodoproduccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolevantamiento
    ADD CONSTRAINT op_puntolevantamiento_metodoproduccion_fkey FOREIGN KEY (metodoproduccion) REFERENCES ladm_col_210.col_metodoproducciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12393 (class 2606 OID 341095)
-- Name: op_puntolevantamiento op_puntolevantamiento_posicion_interpolacion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolevantamiento
    ADD CONSTRAINT op_puntolevantamiento_posicion_interpolacion_fkey FOREIGN KEY (posicion_interpolacion) REFERENCES ladm_col_210.col_interpolaciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12394 (class 2606 OID 341100)
-- Name: op_puntolevantamiento op_puntolevantamiento_puntotipo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolevantamiento
    ADD CONSTRAINT op_puntolevantamiento_puntotipo_fkey FOREIGN KEY (puntotipo) REFERENCES ladm_col_210.op_puntotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12395 (class 2606 OID 341105)
-- Name: op_puntolevantamiento op_puntolevantamiento_tipo_punto_levantamiento_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolevantamiento
    ADD CONSTRAINT op_puntolevantamiento_tipo_punto_levantamiento_fkey FOREIGN KEY (tipo_punto_levantamiento) REFERENCES ladm_col_210.op_puntolevtipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12396 (class 2606 OID 341110)
-- Name: op_puntolevantamiento op_puntolevantamiento_ue_op_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolevantamiento
    ADD CONSTRAINT op_puntolevantamiento_ue_op_construccion_fkey FOREIGN KEY (ue_op_construccion) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12397 (class 2606 OID 341115)
-- Name: op_puntolevantamiento op_puntolevantamiento_ue_op_servidumbretransito_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolevantamiento
    ADD CONSTRAINT op_puntolevantamiento_ue_op_servidumbretransito_fkey FOREIGN KEY (ue_op_servidumbretransito) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12398 (class 2606 OID 341120)
-- Name: op_puntolevantamiento op_puntolevantamiento_ue_op_terreno_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolevantamiento
    ADD CONSTRAINT op_puntolevantamiento_ue_op_terreno_fkey FOREIGN KEY (ue_op_terreno) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12399 (class 2606 OID 341125)
-- Name: op_puntolevantamiento op_puntolevantamiento_ue_op_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolevantamiento
    ADD CONSTRAINT op_puntolevantamiento_ue_op_unidadconstruccion_fkey FOREIGN KEY (ue_op_unidadconstruccion) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12400 (class 2606 OID 341130)
-- Name: op_puntolindero op_puntolindero_acuerdo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolindero
    ADD CONSTRAINT op_puntolindero_acuerdo_fkey FOREIGN KEY (acuerdo) REFERENCES ladm_col_210.op_acuerdotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12401 (class 2606 OID 341135)
-- Name: op_puntolindero op_puntolindero_fotoidentificacion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolindero
    ADD CONSTRAINT op_puntolindero_fotoidentificacion_fkey FOREIGN KEY (fotoidentificacion) REFERENCES ladm_col_210.op_fotoidentificaciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12402 (class 2606 OID 341140)
-- Name: op_puntolindero op_puntolindero_metodoproduccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolindero
    ADD CONSTRAINT op_puntolindero_metodoproduccion_fkey FOREIGN KEY (metodoproduccion) REFERENCES ladm_col_210.col_metodoproducciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12403 (class 2606 OID 341145)
-- Name: op_puntolindero op_puntolindero_posicion_interpolacion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolindero
    ADD CONSTRAINT op_puntolindero_posicion_interpolacion_fkey FOREIGN KEY (posicion_interpolacion) REFERENCES ladm_col_210.col_interpolaciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12404 (class 2606 OID 341150)
-- Name: op_puntolindero op_puntolindero_puntotipo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolindero
    ADD CONSTRAINT op_puntolindero_puntotipo_fkey FOREIGN KEY (puntotipo) REFERENCES ladm_col_210.op_puntotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12405 (class 2606 OID 341155)
-- Name: op_puntolindero op_puntolindero_ubicacion_punto_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolindero
    ADD CONSTRAINT op_puntolindero_ubicacion_punto_fkey FOREIGN KEY (ubicacion_punto) REFERENCES ladm_col_210.op_ubicacionpuntotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12406 (class 2606 OID 341160)
-- Name: op_puntolindero op_puntolindero_ue_op_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolindero
    ADD CONSTRAINT op_puntolindero_ue_op_construccion_fkey FOREIGN KEY (ue_op_construccion) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12407 (class 2606 OID 341165)
-- Name: op_puntolindero op_puntolindero_ue_op_servidumbretransito_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolindero
    ADD CONSTRAINT op_puntolindero_ue_op_servidumbretransito_fkey FOREIGN KEY (ue_op_servidumbretransito) REFERENCES ladm_col_210.op_servidumbretransito(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12408 (class 2606 OID 341170)
-- Name: op_puntolindero op_puntolindero_ue_op_terreno_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolindero
    ADD CONSTRAINT op_puntolindero_ue_op_terreno_fkey FOREIGN KEY (ue_op_terreno) REFERENCES ladm_col_210.op_terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12409 (class 2606 OID 341175)
-- Name: op_puntolindero op_puntolindero_ue_op_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_puntolindero
    ADD CONSTRAINT op_puntolindero_ue_op_unidadconstruccion_fkey FOREIGN KEY (ue_op_unidadconstruccion) REFERENCES ladm_col_210.op_unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12410 (class 2606 OID 341180)
-- Name: op_restriccion op_restriccion_interesado_op_interesado_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_restriccion
    ADD CONSTRAINT op_restriccion_interesado_op_interesado_fkey FOREIGN KEY (interesado_op_interesado) REFERENCES ladm_col_210.op_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12411 (class 2606 OID 341185)
-- Name: op_restriccion op_restriccion_interesado_p_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_restriccion
    ADD CONSTRAINT op_restriccion_interesado_p_grpcn_ntrsdos_fkey FOREIGN KEY (interesado_op_agrupacion_interesados) REFERENCES ladm_col_210.op_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12412 (class 2606 OID 341190)
-- Name: op_restriccion op_restriccion_tipo_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_restriccion
    ADD CONSTRAINT op_restriccion_tipo_fkey FOREIGN KEY (tipo) REFERENCES ladm_col_210.op_restricciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12413 (class 2606 OID 341195)
-- Name: op_restriccion op_restriccion_unidad_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_restriccion
    ADD CONSTRAINT op_restriccion_unidad_fkey FOREIGN KEY (unidad) REFERENCES ladm_col_210.op_predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12414 (class 2606 OID 341200)
-- Name: op_servidumbretransito op_servidumbretransito_dimension_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_servidumbretransito
    ADD CONSTRAINT op_servidumbretransito_dimension_fkey FOREIGN KEY (dimension) REFERENCES ladm_col_210.col_dimensiontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12415 (class 2606 OID 341205)
-- Name: op_servidumbretransito op_servidumbretransito_relacion_superficie_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_servidumbretransito
    ADD CONSTRAINT op_servidumbretransito_relacion_superficie_fkey FOREIGN KEY (relacion_superficie) REFERENCES ladm_col_210.col_relacionsuperficietipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12416 (class 2606 OID 341210)
-- Name: op_terreno op_terreno_dimension_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_terreno
    ADD CONSTRAINT op_terreno_dimension_fkey FOREIGN KEY (dimension) REFERENCES ladm_col_210.col_dimensiontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12417 (class 2606 OID 341215)
-- Name: op_terreno op_terreno_relacion_superficie_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_terreno
    ADD CONSTRAINT op_terreno_relacion_superficie_fkey FOREIGN KEY (relacion_superficie) REFERENCES ladm_col_210.col_relacionsuperficietipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12418 (class 2606 OID 341220)
-- Name: op_unidadconstruccion op_unidadconstruccion_dimension_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_unidadconstruccion
    ADD CONSTRAINT op_unidadconstruccion_dimension_fkey FOREIGN KEY (dimension) REFERENCES ladm_col_210.col_dimensiontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12419 (class 2606 OID 341225)
-- Name: op_unidadconstruccion op_unidadconstruccion_op_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_unidadconstruccion
    ADD CONSTRAINT op_unidadconstruccion_op_construccion_fkey FOREIGN KEY (op_construccion) REFERENCES ladm_col_210.op_construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12420 (class 2606 OID 341230)
-- Name: op_unidadconstruccion op_unidadconstruccion_relacion_superficie_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_unidadconstruccion
    ADD CONSTRAINT op_unidadconstruccion_relacion_superficie_fkey FOREIGN KEY (relacion_superficie) REFERENCES ladm_col_210.col_relacionsuperficietipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12421 (class 2606 OID 341235)
-- Name: op_unidadconstruccion op_unidadconstruccion_tipo_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_unidadconstruccion
    ADD CONSTRAINT op_unidadconstruccion_tipo_construccion_fkey FOREIGN KEY (tipo_construccion) REFERENCES ladm_col_210.op_construcciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12422 (class 2606 OID 341240)
-- Name: op_unidadconstruccion op_unidadconstruccion_tipo_dominio_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_unidadconstruccion
    ADD CONSTRAINT op_unidadconstruccion_tipo_dominio_fkey FOREIGN KEY (tipo_dominio) REFERENCES ladm_col_210.op_dominioconstrucciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12423 (class 2606 OID 341245)
-- Name: op_unidadconstruccion op_unidadconstruccion_tipo_planta_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_unidadconstruccion
    ADD CONSTRAINT op_unidadconstruccion_tipo_planta_fkey FOREIGN KEY (tipo_planta) REFERENCES ladm_col_210.op_construccionplantatipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12424 (class 2606 OID 341250)
-- Name: op_unidadconstruccion op_unidadconstruccion_tipo_unidad_construccion_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_unidadconstruccion
    ADD CONSTRAINT op_unidadconstruccion_tipo_unidad_construccion_fkey FOREIGN KEY (tipo_unidad_construccion) REFERENCES ladm_col_210.op_unidadconstrucciontipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12425 (class 2606 OID 341255)
-- Name: op_unidadconstruccion op_unidadconstruccion_uso_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.op_unidadconstruccion
    ADD CONSTRAINT op_unidadconstruccion_uso_fkey FOREIGN KEY (uso) REFERENCES ladm_col_210.op_usouconstipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12426 (class 2606 OID 341260)
-- Name: snr_derecho snr_derecho_calidad_derecho_registro_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_derecho
    ADD CONSTRAINT snr_derecho_calidad_derecho_registro_fkey FOREIGN KEY (calidad_derecho_registro) REFERENCES ladm_col_210.snr_calidadderechotipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12427 (class 2606 OID 341265)
-- Name: snr_derecho snr_derecho_snr_fuente_derecho_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_derecho
    ADD CONSTRAINT snr_derecho_snr_fuente_derecho_fkey FOREIGN KEY (snr_fuente_derecho) REFERENCES ladm_col_210.snr_fuente_derecho(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12428 (class 2606 OID 341270)
-- Name: snr_derecho snr_derecho_snr_predio_registro_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_derecho
    ADD CONSTRAINT snr_derecho_snr_predio_registro_fkey FOREIGN KEY (snr_predio_registro) REFERENCES ladm_col_210.snr_predio_registro(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12429 (class 2606 OID 341275)
-- Name: snr_fuente_cabidalinderos snr_fuente_cabidalinderos_tipo_documento_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_fuente_cabidalinderos
    ADD CONSTRAINT snr_fuente_cabidalinderos_tipo_documento_fkey FOREIGN KEY (tipo_documento) REFERENCES ladm_col_210.snr_fuentetipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12430 (class 2606 OID 341280)
-- Name: snr_fuente_derecho snr_fuente_derecho_tipo_documento_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_fuente_derecho
    ADD CONSTRAINT snr_fuente_derecho_tipo_documento_fkey FOREIGN KEY (tipo_documento) REFERENCES ladm_col_210.snr_fuentetipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12431 (class 2606 OID 341285)
-- Name: snr_predio_registro snr_predio_registro_snr_fuente_cabidalinderos_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_predio_registro
    ADD CONSTRAINT snr_predio_registro_snr_fuente_cabidalinderos_fkey FOREIGN KEY (snr_fuente_cabidalinderos) REFERENCES ladm_col_210.snr_fuente_cabidalinderos(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12434 (class 2606 OID 341290)
-- Name: snr_titular_derecho snr_titular_derecho_snr_derecho_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_titular_derecho
    ADD CONSTRAINT snr_titular_derecho_snr_derecho_fkey FOREIGN KEY (snr_derecho) REFERENCES ladm_col_210.snr_derecho(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12435 (class 2606 OID 341295)
-- Name: snr_titular_derecho snr_titular_derecho_snr_titular_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_titular_derecho
    ADD CONSTRAINT snr_titular_derecho_snr_titular_fkey FOREIGN KEY (snr_titular) REFERENCES ladm_col_210.snr_titular(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12432 (class 2606 OID 341300)
-- Name: snr_titular snr_titular_tipo_documento_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_titular
    ADD CONSTRAINT snr_titular_tipo_documento_fkey FOREIGN KEY (tipo_documento) REFERENCES ladm_col_210.snr_documentotitulartipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12433 (class 2606 OID 341305)
-- Name: snr_titular snr_titular_tipo_persona_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.snr_titular
    ADD CONSTRAINT snr_titular_tipo_persona_fkey FOREIGN KEY (tipo_persona) REFERENCES ladm_col_210.snr_personatitulartipo(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12436 (class 2606 OID 341310)
-- Name: t_ili2db_basket t_ili2db_basket_dataset_fkey; Type: FK CONSTRAINT; Schema: ladm_col_210; Owner: postgres
--

ALTER TABLE ONLY ladm_col_210.t_ili2db_basket
    ADD CONSTRAINT t_ili2db_basket_dataset_fkey FOREIGN KEY (dataset) REFERENCES ladm_col_210.t_ili2db_dataset(t_id) DEFERRABLE INITIALLY DEFERRED;


-- Completed on 2020-07-15 12:42:41 -05

--
-- PostgreSQL database dump complete
--

