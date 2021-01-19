--
-- PostgreSQL database dump
--

-- Dumped from database version 11.8 (Ubuntu 11.8-1.pgdg20.04+1)
-- Dumped by pg_dump version 12.3 (Ubuntu 12.3-1.pgdg20.04+1)

-- Started on 2020-07-15 12:37:29 -05

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
-- TOC entry 22 (class 2615 OID 335182)
-- Name: interlis_ili2db3_ladm; Type: SCHEMA; Schema: -; Owner: postgres
--

DROP SCHEMA IF EXISTS interlis_ili2db3_ladm CASCADE;
CREATE SCHEMA interlis_ili2db3_ladm;
CREATE EXTENSION IF NOT EXISTS postgis;


ALTER SCHEMA interlis_ili2db3_ladm OWNER TO postgres;

--
-- TOC entry 1963 (class 1259 OID 335183)
-- Name: t_ili2db_seq; Type: SEQUENCE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE SEQUENCE interlis_ili2db3_ladm.t_ili2db_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_seq OWNER TO postgres;

SET default_tablespace = '';

--
-- TOC entry 1964 (class 1259 OID 335185)
-- Name: baunitcomointeresado; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.baunitcomointeresado (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    interesado_la_agrupacion_interesados bigint,
    interesado_col_interesado bigint,
    unidad_la_baunit bigint,
    unidad_predio bigint
);


ALTER TABLE interlis_ili2db3_ladm.baunitcomointeresado OWNER TO postgres;

--
-- TOC entry 12448 (class 0 OID 0)
-- Dependencies: 1964
-- Name: TABLE baunitcomointeresado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.baunitcomointeresado IS '@iliname LADM_COL_V1_1.LADM_Nucleo.baunitComoInteresado';


--
-- TOC entry 1965 (class 1259 OID 335189)
-- Name: baunitfuente; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.baunitfuente (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    bfuente bigint NOT NULL,
    unidad_la_baunit bigint,
    unidad_predio bigint
);


ALTER TABLE interlis_ili2db3_ladm.baunitfuente OWNER TO postgres;

--
-- TOC entry 12449 (class 0 OID 0)
-- Dependencies: 1965
-- Name: TABLE baunitfuente; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.baunitfuente IS '@iliname LADM_COL_V1_1.LADM_Nucleo.baunitFuente';


--
-- TOC entry 1966 (class 1259 OID 335193)
-- Name: cc_metodooperacion; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.cc_metodooperacion (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    formula character varying(255) NOT NULL,
    dimensiones_origen integer,
    ddimensiones_objetivo integer,
    la_transformacion_transformacion bigint,
    CONSTRAINT cc_metodooperacion_ddimensiones_objetivo_check CHECK (((ddimensiones_objetivo >= 0) AND (ddimensiones_objetivo <= 999999999))),
    CONSTRAINT cc_metodooperacion_dimensiones_origen_check CHECK (((dimensiones_origen >= 0) AND (dimensiones_origen <= 999999999)))
);


ALTER TABLE interlis_ili2db3_ladm.cc_metodooperacion OWNER TO postgres;

--
-- TOC entry 12450 (class 0 OID 0)
-- Dependencies: 1966
-- Name: TABLE cc_metodooperacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.cc_metodooperacion IS 'Estructura que proviene de la traducción de la clase CC_OperationMethod de la ISO 19111. Indica el método utilizado, mediante un algoritmo o un procedimiento, para realizar operaciones con coordenadas.
@iliname LADM_COL_V1_1.LADM_Nucleo.CC_MetodoOperacion';


--
-- TOC entry 12451 (class 0 OID 0)
-- Dependencies: 1966
-- Name: COLUMN cc_metodooperacion.formula; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.cc_metodooperacion.formula IS 'Fórmulas o procedimientos utilizadoa por este método de operación de coordenadas. Esto puede ser una referencia a una publicación. Tenga en cuenta que el método de operación puede no ser analítico, en cuyo caso este atributo hace referencia o contiene el procedimiento, no una fórmula analítica.
@iliname Formula';


--
-- TOC entry 12452 (class 0 OID 0)
-- Dependencies: 1966
-- Name: COLUMN cc_metodooperacion.dimensiones_origen; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.cc_metodooperacion.dimensiones_origen IS 'Número de dimensiones en la fuente CRS de este método de operación de coordenadas.
@iliname Dimensiones_Origen';


--
-- TOC entry 12453 (class 0 OID 0)
-- Dependencies: 1966
-- Name: COLUMN cc_metodooperacion.ddimensiones_objetivo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.cc_metodooperacion.ddimensiones_objetivo IS 'Número de dimensiones en el CRS de destino de este método de operación de coordenadas.
@iliname Ddimensiones_Objetivo';


--
-- TOC entry 12454 (class 0 OID 0)
-- Dependencies: 1966
-- Name: COLUMN cc_metodooperacion.la_transformacion_transformacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.cc_metodooperacion.la_transformacion_transformacion IS 'Fórmula o procedimiento utilizado en la transformación.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Transformacion.Transformacion';


--
-- TOC entry 1967 (class 1259 OID 335199)
-- Name: cclfuente; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.cclfuente (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ccl_la_cadenacaraslimite bigint,
    ccl_lindero bigint,
    lfuente bigint NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.cclfuente OWNER TO postgres;

--
-- TOC entry 12455 (class 0 OID 0)
-- Dependencies: 1967
-- Name: TABLE cclfuente; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.cclfuente IS '@iliname LADM_COL_V1_1.LADM_Nucleo.cclFuente';


--
-- TOC entry 1968 (class 1259 OID 335203)
-- Name: ci_codigotarea; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.ci_codigotarea (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.ci_codigotarea OWNER TO postgres;

--
-- TOC entry 1969 (class 1259 OID 335209)
-- Name: ci_contacto; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.ci_contacto (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    telefono character varying(255),
    direccion character varying(255),
    fuente_en_linea character varying(255),
    horario_de_atencion character varying(255),
    instrucciones_contacto character varying(255),
    ci_parteresponsable_informacion_contacto bigint
);


ALTER TABLE interlis_ili2db3_ladm.ci_contacto OWNER TO postgres;

--
-- TOC entry 12456 (class 0 OID 0)
-- Dependencies: 1969
-- Name: TABLE ci_contacto; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.ci_contacto IS 'Clase traducida CI_Contact de la ISO 19115.
Almacena la información requerida para permitir el contacto con la persona responsable y la organización.
@iliname LADM_COL_V1_1.LADM_Nucleo.CI_Contacto';


--
-- TOC entry 12457 (class 0 OID 0)
-- Dependencies: 1969
-- Name: COLUMN ci_contacto.telefono; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_contacto.telefono IS 'Números de teléfono en los que la organización o el individuo pueden ser contactados.
@iliname Telefono';


--
-- TOC entry 12458 (class 0 OID 0)
-- Dependencies: 1969
-- Name: COLUMN ci_contacto.direccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_contacto.direccion IS 'Dirección física y de correo electrónico en la que se puede contactar a la organización o al individuo.
@iliname Direccion';


--
-- TOC entry 12459 (class 0 OID 0)
-- Dependencies: 1969
-- Name: COLUMN ci_contacto.fuente_en_linea; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_contacto.fuente_en_linea IS 'Información en línea que se puede usar para contactar al individuo o a la organización.
@iliname Fuente_En_Linea';


--
-- TOC entry 12460 (class 0 OID 0)
-- Dependencies: 1969
-- Name: COLUMN ci_contacto.horario_de_atencion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_contacto.horario_de_atencion IS 'Período de tiempo, incluida la zona horaria, en el que la organización o el individuo pueden ser contactados.
@iliname Horario_De_Atencion';


--
-- TOC entry 12461 (class 0 OID 0)
-- Dependencies: 1969
-- Name: COLUMN ci_contacto.instrucciones_contacto; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_contacto.instrucciones_contacto IS 'Instrucciones complementarias sobre cómo o cuándo contactar al individuo o a la organización.
@iliname Instrucciones_Contacto';


--
-- TOC entry 12462 (class 0 OID 0)
-- Dependencies: 1969
-- Name: COLUMN ci_contacto.ci_parteresponsable_informacion_contacto; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_contacto.ci_parteresponsable_informacion_contacto IS 'Ver clase CI_Contacto.
@iliname LADM_COL_V1_1.LADM_Nucleo.CI_ParteResponsable.Informacion_Contacto';


--
-- TOC entry 1970 (class 1259 OID 335216)
-- Name: ci_forma_presentacion_codigo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.ci_forma_presentacion_codigo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.ci_forma_presentacion_codigo OWNER TO postgres;

--
-- TOC entry 1971 (class 1259 OID 335222)
-- Name: ci_parteresponsable; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.ci_parteresponsable (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    nombre_individual character varying(255),
    nombre_organizacion character varying(255),
    posicion character varying(255),
    funcion character varying(255),
    col_fuenteadminstrtiva_procedencia bigint,
    la_unidadespacial_procedencia bigint,
    la_agrupacinnddsspcles_procedencia bigint,
    la_espacjrdcndddfccion_procedencia bigint,
    la_espacijrdcrdsrvcios_procedencia bigint,
    la_nivel_procedencia bigint,
    la_relcnncsrnddsspcles_procedencia bigint,
    la_baunit_procedencia bigint,
    la_relacionnecesrbnits_procedencia bigint,
    la_punto_procedencia bigint,
    col_fuenteespacial_procedencia bigint,
    la_cadenacaraslimite_procedencia bigint,
    la_caraslindero_procedencia bigint,
    la_agrupacion_intrsdos_procedencia bigint,
    col_derecho_procedencia bigint,
    col_interesado_procedencia bigint,
    construccion_procedencia bigint,
    lindero_procedencia bigint,
    predio_procedencia bigint,
    publicidad_procedencia bigint,
    puntocontrol_procedencia bigint,
    puntolindero_procedencia bigint,
    terreno_procedencia bigint,
    col_restriccion_procedencia bigint,
    puntolevantamiento_procedencia bigint,
    col_responsabilidad_procedencia bigint,
    servidumbrepaso_procedencia bigint,
    col_hipoteca_procedencia bigint,
    unidadconstruccion_procedencia bigint
);


ALTER TABLE interlis_ili2db3_ladm.ci_parteresponsable OWNER TO postgres;

--
-- TOC entry 12463 (class 0 OID 0)
-- Dependencies: 1971
-- Name: TABLE ci_parteresponsable; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.ci_parteresponsable IS 'Clase traducida CI_ResponsibleParty de la ISO 19115:2003. Identificación de los responsables del recurso y el papel de la parte en el recurso.
@iliname LADM_COL_V1_1.LADM_Nucleo.CI_ParteResponsable';


--
-- TOC entry 12464 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.nombre_individual; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.nombre_individual IS 'Nombre individual del responsable. Se proporciona si la organización o la posición no son proporcionados.
@iliname Nombre_Individual';


--
-- TOC entry 12465 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.nombre_organizacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.nombre_organizacion IS 'Nombre de la organización responsable. Se proporciona si el nombre individual o la posición no se provén.
@iliname Nombre_Organizacion';


--
-- TOC entry 12466 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.posicion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.posicion IS 'Posición de la persona responsable. Se proporcionará si NombreIndividual o Organizacion no son
proporcionados.
@iliname Posicion';


--
-- TOC entry 12467 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.funcion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.funcion IS 'Función realizada por la parte responsable.
@iliname Funcion';


--
-- TOC entry 12468 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.col_fuenteadminstrtiva_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.col_fuenteadminstrtiva_procedencia IS 'Parte responsable de la aceptación, con todos los metadatos gestionados por la clase CI_ParteResponsable, que hace referencia a la norma ISO 19115:2003.
@iliname LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Procedencia';


--
-- TOC entry 12469 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.la_unidadespacial_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.la_unidadespacial_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12470 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.la_agrupacinnddsspcles_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.la_agrupacinnddsspcles_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12471 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.la_espacjrdcndddfccion_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.la_espacjrdcndddfccion_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12472 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.la_espacijrdcrdsrvcios_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.la_espacijrdcrdsrvcios_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12473 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.la_nivel_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.la_nivel_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12474 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.la_relcnncsrnddsspcles_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.la_relcnncsrnddsspcles_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12475 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.la_baunit_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.la_baunit_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12476 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.la_relacionnecesrbnits_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.la_relacionnecesrbnits_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12477 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.la_punto_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.la_punto_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12478 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.col_fuenteespacial_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.col_fuenteespacial_procedencia IS 'Parte responsable de la aceptación, con todos los metadatos gestionados por la clase CI_ParteResponsable, que hace referencia a la norma ISO 19115:2003.
@iliname LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Procedencia';


--
-- TOC entry 12479 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.la_cadenacaraslimite_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.la_cadenacaraslimite_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12480 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.la_caraslindero_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.la_caraslindero_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12481 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.la_agrupacion_intrsdos_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.la_agrupacion_intrsdos_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12482 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.col_derecho_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.col_derecho_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12483 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.col_interesado_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.col_interesado_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12484 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.construccion_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.construccion_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12485 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.lindero_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.lindero_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12486 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.predio_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.predio_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12487 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.publicidad_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.publicidad_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12488 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.puntocontrol_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.puntocontrol_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12489 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.puntolindero_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.puntolindero_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12490 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.terreno_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.terreno_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12491 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.col_restriccion_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.col_restriccion_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12492 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.puntolevantamiento_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.puntolevantamiento_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12493 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.col_responsabilidad_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.col_responsabilidad_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12494 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.servidumbrepaso_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.servidumbrepaso_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12495 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.col_hipoteca_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.col_hipoteca_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 12496 (class 0 OID 0)
-- Dependencies: 1971
-- Name: COLUMN ci_parteresponsable.unidadconstruccion_procedencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.ci_parteresponsable.unidadconstruccion_procedencia IS 'Metadatos corresondientes a la responsabilidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia';


--
-- TOC entry 1972 (class 1259 OID 335229)
-- Name: clfuente; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.clfuente (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    cl bigint NOT NULL,
    cfuente bigint NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.clfuente OWNER TO postgres;

--
-- TOC entry 12497 (class 0 OID 0)
-- Dependencies: 1972
-- Name: TABLE clfuente; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.clfuente IS '@iliname LADM_COL_V1_1.LADM_Nucleo.clFuente';


--
-- TOC entry 1973 (class 1259 OID 335233)
-- Name: col_acuerdotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_acuerdotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_acuerdotipo OWNER TO postgres;

--
-- TOC entry 1974 (class 1259 OID 335239)
-- Name: col_afectacion; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_afectacion (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_afectacion OWNER TO postgres;

--
-- TOC entry 1975 (class 1259 OID 335245)
-- Name: col_afectacion_terreno_afectacion; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_afectacion_terreno_afectacion (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    avalue character varying(255) NOT NULL,
    terreno_afectacion bigint
);


ALTER TABLE interlis_ili2db3_ladm.col_afectacion_terreno_afectacion OWNER TO postgres;

--
-- TOC entry 12498 (class 0 OID 0)
-- Dependencies: 1975
-- Name: TABLE col_afectacion_terreno_afectacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_afectacion_terreno_afectacion IS '@iliname Catastro_Registro_Nucleo_V2_2_1.COL_Afectacion_Terreno_Afectacion';


--
-- TOC entry 12499 (class 0 OID 0)
-- Dependencies: 1975
-- Name: COLUMN col_afectacion_terreno_afectacion.avalue; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_afectacion_terreno_afectacion.avalue IS '@iliname value';


--
-- TOC entry 12500 (class 0 OID 0)
-- Dependencies: 1975
-- Name: COLUMN col_afectacion_terreno_afectacion.terreno_afectacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_afectacion_terreno_afectacion.terreno_afectacion IS 'Se describe si en el predio existe alguna afectación natural de tipo inundación o de remoción en masa, corresponde a la pregunta 5.7 del anexo 5.1 de los estandares de catastro multiproposito versión 2.1.1
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Afectacion';


--
-- TOC entry 1976 (class 1259 OID 335249)
-- Name: col_areatipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_areatipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_areatipo OWNER TO postgres;

--
-- TOC entry 1977 (class 1259 OID 335255)
-- Name: col_areavalor; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_areavalor (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    areasize numeric(15,1) NOT NULL,
    atype character varying(255) NOT NULL,
    la_unidadespacial_area bigint,
    la_espacjrdcndddfccion_area bigint,
    la_espacijrdcrdsrvcios_area bigint,
    construccion_area bigint,
    terreno_area bigint,
    servidumbrepaso_area bigint,
    unidadconstruccion_area bigint,
    CONSTRAINT col_areavalor_areasize_check CHECK (((areasize >= 0.0) AND (areasize <= 99999999999999.9)))
);


ALTER TABLE interlis_ili2db3_ladm.col_areavalor OWNER TO postgres;

--
-- TOC entry 12501 (class 0 OID 0)
-- Dependencies: 1977
-- Name: TABLE col_areavalor; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_areavalor IS '@iliname LADM_COL_V1_1.LADM_Nucleo.COL_AreaValor';


--
-- TOC entry 12502 (class 0 OID 0)
-- Dependencies: 1977
-- Name: COLUMN col_areavalor.areasize; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_areavalor.areasize IS '@iliname areaSize';


--
-- TOC entry 12503 (class 0 OID 0)
-- Dependencies: 1977
-- Name: COLUMN col_areavalor.atype; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_areavalor.atype IS '@iliname type';


--
-- TOC entry 12504 (class 0 OID 0)
-- Dependencies: 1977
-- Name: COLUMN col_areavalor.la_unidadespacial_area; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_areavalor.la_unidadespacial_area IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area';


--
-- TOC entry 12505 (class 0 OID 0)
-- Dependencies: 1977
-- Name: COLUMN col_areavalor.la_espacjrdcndddfccion_area; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_areavalor.la_espacjrdcndddfccion_area IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area';


--
-- TOC entry 12506 (class 0 OID 0)
-- Dependencies: 1977
-- Name: COLUMN col_areavalor.la_espacijrdcrdsrvcios_area; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_areavalor.la_espacijrdcrdsrvcios_area IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area';


--
-- TOC entry 12507 (class 0 OID 0)
-- Dependencies: 1977
-- Name: COLUMN col_areavalor.construccion_area; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_areavalor.construccion_area IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area';


--
-- TOC entry 12508 (class 0 OID 0)
-- Dependencies: 1977
-- Name: COLUMN col_areavalor.terreno_area; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_areavalor.terreno_area IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area';


--
-- TOC entry 12509 (class 0 OID 0)
-- Dependencies: 1977
-- Name: COLUMN col_areavalor.servidumbrepaso_area; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_areavalor.servidumbrepaso_area IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area';


--
-- TOC entry 12510 (class 0 OID 0)
-- Dependencies: 1977
-- Name: COLUMN col_areavalor.unidadconstruccion_area; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_areavalor.unidadconstruccion_area IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area';


--
-- TOC entry 1978 (class 1259 OID 335260)
-- Name: col_bosqueareasemi; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_bosqueareasemi (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_bosqueareasemi OWNER TO postgres;

--
-- TOC entry 1979 (class 1259 OID 335266)
-- Name: col_bosqueareasemi_terreno_bosque_area_seminaturale; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_bosqueareasemi_terreno_bosque_area_seminaturale (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    avalue character varying(255) NOT NULL,
    terreno_bosque_area_seminaturale bigint
);


ALTER TABLE interlis_ili2db3_ladm.col_bosqueareasemi_terreno_bosque_area_seminaturale OWNER TO postgres;

--
-- TOC entry 12511 (class 0 OID 0)
-- Dependencies: 1979
-- Name: TABLE col_bosqueareasemi_terreno_bosque_area_seminaturale; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_bosqueareasemi_terreno_bosque_area_seminaturale IS '@iliname Catastro_Registro_Nucleo_V2_2_1.COL_BosqueAreaSemi_Terreno_Bosque_Area_Seminaturale';


--
-- TOC entry 12512 (class 0 OID 0)
-- Dependencies: 1979
-- Name: COLUMN col_bosqueareasemi_terreno_bosque_area_seminaturale.avalue; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_bosqueareasemi_terreno_bosque_area_seminaturale.avalue IS '@iliname value';


--
-- TOC entry 12513 (class 0 OID 0)
-- Dependencies: 1979
-- Name: COLUMN col_bosqueareasemi_terreno_bosque_area_seminaturale.terreno_bosque_area_seminaturale; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_bosqueareasemi_terreno_bosque_area_seminaturale.terreno_bosque_area_seminaturale IS 'Se describe si en el predio existe presencia de bosques o áreas seminaturales, corresponde a la pregunta 5.4 del anexo 5.1 de los estandares de catastro multiproposito versión 2.1.1
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Bosque_Area_Seminaturale';


--
-- TOC entry 1980 (class 1259 OID 335270)
-- Name: col_cuerpoagua; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_cuerpoagua (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_cuerpoagua OWNER TO postgres;

--
-- TOC entry 1981 (class 1259 OID 335276)
-- Name: col_cuerpoagua_terreno_evidencia_cuerpo_agua; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_cuerpoagua_terreno_evidencia_cuerpo_agua (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    avalue character varying(255) NOT NULL,
    terreno_evidencia_cuerpo_agua bigint
);


ALTER TABLE interlis_ili2db3_ladm.col_cuerpoagua_terreno_evidencia_cuerpo_agua OWNER TO postgres;

--
-- TOC entry 12514 (class 0 OID 0)
-- Dependencies: 1981
-- Name: TABLE col_cuerpoagua_terreno_evidencia_cuerpo_agua; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_cuerpoagua_terreno_evidencia_cuerpo_agua IS '@iliname Catastro_Registro_Nucleo_V2_2_1.COL_CuerpoAgua_Terreno_Evidencia_Cuerpo_Agua';


--
-- TOC entry 12515 (class 0 OID 0)
-- Dependencies: 1981
-- Name: COLUMN col_cuerpoagua_terreno_evidencia_cuerpo_agua.avalue; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_cuerpoagua_terreno_evidencia_cuerpo_agua.avalue IS '@iliname value';


--
-- TOC entry 12516 (class 0 OID 0)
-- Dependencies: 1981
-- Name: COLUMN col_cuerpoagua_terreno_evidencia_cuerpo_agua.terreno_evidencia_cuerpo_agua; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_cuerpoagua_terreno_evidencia_cuerpo_agua.terreno_evidencia_cuerpo_agua IS 'En esta clase se identifican los valores de la pregunta 5.5. Especifique si evidencia en el terreno del Anexo 5, Versión 2.1.1 de Catastro Multiproposito
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Evidencia_Cuerpo_Agua';


--
-- TOC entry 1982 (class 1259 OID 335280)
-- Name: col_defpuntotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_defpuntotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_defpuntotipo OWNER TO postgres;

--
-- TOC entry 1983 (class 1259 OID 335286)
-- Name: col_derecho; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_derecho (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    tipo character varying(255) NOT NULL,
    codigo_registral_derecho character varying(5),
    descripcion character varying(255),
    comprobacion_comparte boolean,
    uso_efectivo character varying(255),
    r_espacio_de_nombres character varying(255) NOT NULL,
    r_local_id character varying(255) NOT NULL,
    interesado_la_agrupacion_interesados bigint,
    interesado_col_interesado bigint,
    unidad_la_baunit bigint,
    unidad_predio bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone
);


ALTER TABLE interlis_ili2db3_ladm.col_derecho OWNER TO postgres;

--
-- TOC entry 12517 (class 0 OID 0)
-- Dependencies: 1983
-- Name: TABLE col_derecho; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_derecho IS 'Clase que registra las instancias de los derechos que un interesado ejerce sobre un predio. Es una especialización de la clase LA_RRR del propio modelo.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Derecho';


--
-- TOC entry 12518 (class 0 OID 0)
-- Dependencies: 1983
-- Name: COLUMN col_derecho.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_derecho.tipo IS 'Derecho que se ejerce.
@iliname Tipo';


--
-- TOC entry 12519 (class 0 OID 0)
-- Dependencies: 1983
-- Name: COLUMN col_derecho.codigo_registral_derecho; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_derecho.codigo_registral_derecho IS 'Código con el que el derecho se registra en el Registro de la Propiedad.
@iliname Codigo_Registral_Derecho';


--
-- TOC entry 12520 (class 0 OID 0)
-- Dependencies: 1983
-- Name: COLUMN col_derecho.descripcion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_derecho.descripcion IS 'Descripción relatical al derecho, la responsabilidad o la restricción.
@iliname Descripcion';


--
-- TOC entry 12521 (class 0 OID 0)
-- Dependencies: 1983
-- Name: COLUMN col_derecho.comprobacion_comparte; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_derecho.comprobacion_comparte IS 'Indicación de si comparte o no.
@iliname Comprobacion_Comparte';


--
-- TOC entry 12522 (class 0 OID 0)
-- Dependencies: 1983
-- Name: COLUMN col_derecho.uso_efectivo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_derecho.uso_efectivo IS 'Descripción de cual es el uso efectivo.
@iliname Uso_Efectivo';


--
-- TOC entry 12523 (class 0 OID 0)
-- Dependencies: 1983
-- Name: COLUMN col_derecho.r_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_derecho.r_espacio_de_nombres IS 'Identificador global único.
@iliname r_Espacio_De_Nombres';


--
-- TOC entry 12524 (class 0 OID 0)
-- Dependencies: 1983
-- Name: COLUMN col_derecho.r_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_derecho.r_local_id IS 'Identificador único local.
@iliname r_Local_Id';


--
-- TOC entry 12525 (class 0 OID 0)
-- Dependencies: 1983
-- Name: COLUMN col_derecho.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_derecho.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12526 (class 0 OID 0)
-- Dependencies: 1983
-- Name: COLUMN col_derecho.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_derecho.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 1984 (class 1259 OID 335293)
-- Name: col_derechotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_derechotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_derechotipo OWNER TO postgres;

--
-- TOC entry 1985 (class 1259 OID 335299)
-- Name: col_descripcionpuntotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_descripcionpuntotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_descripcionpuntotipo OWNER TO postgres;

--
-- TOC entry 1986 (class 1259 OID 335305)
-- Name: col_estadodisponibilidadtipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_estadodisponibilidadtipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_estadodisponibilidadtipo OWNER TO postgres;

--
-- TOC entry 1987 (class 1259 OID 335311)
-- Name: col_estructuratipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_estructuratipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_estructuratipo OWNER TO postgres;

--
-- TOC entry 1988 (class 1259 OID 335317)
-- Name: col_explotaciontipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_explotaciontipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_explotaciontipo OWNER TO postgres;

--
-- TOC entry 1989 (class 1259 OID 335323)
-- Name: col_explotaciontipo_terreno_explotacion; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_explotaciontipo_terreno_explotacion (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    avalue character varying(255) NOT NULL,
    terreno_explotacion bigint
);


ALTER TABLE interlis_ili2db3_ladm.col_explotaciontipo_terreno_explotacion OWNER TO postgres;

--
-- TOC entry 12527 (class 0 OID 0)
-- Dependencies: 1989
-- Name: TABLE col_explotaciontipo_terreno_explotacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_explotaciontipo_terreno_explotacion IS '@iliname Catastro_Registro_Nucleo_V2_2_1.COL_ExplotacionTipo_Terreno_Explotacion';


--
-- TOC entry 12528 (class 0 OID 0)
-- Dependencies: 1989
-- Name: COLUMN col_explotaciontipo_terreno_explotacion.avalue; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_explotaciontipo_terreno_explotacion.avalue IS '@iliname value';


--
-- TOC entry 12529 (class 0 OID 0)
-- Dependencies: 1989
-- Name: COLUMN col_explotaciontipo_terreno_explotacion.terreno_explotacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_explotaciontipo_terreno_explotacion.terreno_explotacion IS 'Se caracteriza si en el predio existe algún tipo de explotación, corresponde a la pregunta 5.6 del anexo 5.1 de los estandares de catastro multiproposito versión 2.1.1
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Explotacion';


--
-- TOC entry 1990 (class 1259 OID 335327)
-- Name: col_fuenteadministrativa; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_fuenteadministrativa (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    texto character varying(255),
    tipo character varying(255) NOT NULL,
    codigo_registral_transaccion character varying(5),
    nombre character varying(50),
    fecha_aceptacion timestamp without time zone,
    estado_disponibilidad character varying(255) NOT NULL,
    sello_inicio_validez timestamp without time zone,
    tipo_principal character varying(255),
    fecha_grabacion timestamp without time zone,
    fecha_entrega timestamp without time zone,
    s_espacio_de_nombres character varying(255) NOT NULL,
    s_local_id character varying(255) NOT NULL,
    oficialidad boolean
);


ALTER TABLE interlis_ili2db3_ladm.col_fuenteadministrativa OWNER TO postgres;

--
-- TOC entry 12530 (class 0 OID 0)
-- Dependencies: 1990
-- Name: TABLE col_fuenteadministrativa; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_fuenteadministrativa IS 'Especialización de la clase COL_Fuente para almacenar aquellas fuentes constituidas por documentos (documento hipotecario, documentos notariales, documentos históricos, etc.) que documentan la relación entre instancias de interesados y de predios.
@iliname LADM_COL_V1_1.LADM_Nucleo.COL_FuenteAdministrativa';


--
-- TOC entry 12531 (class 0 OID 0)
-- Dependencies: 1990
-- Name: COLUMN col_fuenteadministrativa.texto; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteadministrativa.texto IS 'Descripción del documento.
@iliname Texto';


--
-- TOC entry 12532 (class 0 OID 0)
-- Dependencies: 1990
-- Name: COLUMN col_fuenteadministrativa.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteadministrativa.tipo IS 'Tipo de documento de fuente administrativa.
@iliname Tipo';


--
-- TOC entry 12533 (class 0 OID 0)
-- Dependencies: 1990
-- Name: COLUMN col_fuenteadministrativa.codigo_registral_transaccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteadministrativa.codigo_registral_transaccion IS 'Código registral de la transacción que se documenta.
@iliname Codigo_Registral_Transaccion';


--
-- TOC entry 12534 (class 0 OID 0)
-- Dependencies: 1990
-- Name: COLUMN col_fuenteadministrativa.nombre; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteadministrativa.nombre IS 'Identificador del documento, ejemplo: numero de la resolución
@iliname Nombre';


--
-- TOC entry 12535 (class 0 OID 0)
-- Dependencies: 1990
-- Name: COLUMN col_fuenteadministrativa.fecha_aceptacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteadministrativa.fecha_aceptacion IS '@iliname Fecha_Aceptacion';


--
-- TOC entry 12536 (class 0 OID 0)
-- Dependencies: 1990
-- Name: COLUMN col_fuenteadministrativa.estado_disponibilidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteadministrativa.estado_disponibilidad IS 'Indica si la fuente está o no disponible y en qué condiciones. También puede indicar porqué ha dejado de estar disponible, si ha ocurrido.
@iliname Estado_Disponibilidad';


--
-- TOC entry 12537 (class 0 OID 0)
-- Dependencies: 1990
-- Name: COLUMN col_fuenteadministrativa.sello_inicio_validez; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteadministrativa.sello_inicio_validez IS 'Fecha de inicio de validez de la fuente.
@iliname Sello_Inicio_Validez';


--
-- TOC entry 12538 (class 0 OID 0)
-- Dependencies: 1990
-- Name: COLUMN col_fuenteadministrativa.tipo_principal; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteadministrativa.tipo_principal IS 'Tipo de formato en el que es presentada la fuente, de acuerdo con el registro de metadatos.
@iliname Tipo_Principal';


--
-- TOC entry 12539 (class 0 OID 0)
-- Dependencies: 1990
-- Name: COLUMN col_fuenteadministrativa.fecha_grabacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteadministrativa.fecha_grabacion IS 'Fecha en la que es almacenado el documento fuente.
@iliname Fecha_Grabacion';


--
-- TOC entry 12540 (class 0 OID 0)
-- Dependencies: 1990
-- Name: COLUMN col_fuenteadministrativa.fecha_entrega; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteadministrativa.fecha_entrega IS 'Fecha en la que se entrega la fuente.
@iliname Fecha_Entrega';


--
-- TOC entry 12541 (class 0 OID 0)
-- Dependencies: 1990
-- Name: COLUMN col_fuenteadministrativa.s_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteadministrativa.s_espacio_de_nombres IS 'Identificación inéquivoca de la fuente en el sistema.
@iliname s_Espacio_De_Nombres';


--
-- TOC entry 12542 (class 0 OID 0)
-- Dependencies: 1990
-- Name: COLUMN col_fuenteadministrativa.s_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteadministrativa.s_local_id IS 'Identificador de la fuente en el sistema local.
@iliname s_Local_Id';


--
-- TOC entry 12543 (class 0 OID 0)
-- Dependencies: 1990
-- Name: COLUMN col_fuenteadministrativa.oficialidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteadministrativa.oficialidad IS 'Indica si se trata de un documento oficial o no.
@iliname Oficialidad';


--
-- TOC entry 1991 (class 1259 OID 335334)
-- Name: col_fuenteadministrativatipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_fuenteadministrativatipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_fuenteadministrativatipo OWNER TO postgres;

--
-- TOC entry 1992 (class 1259 OID 335340)
-- Name: col_fuenteespacial; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_fuenteespacial (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    tipo character varying(255) NOT NULL,
    fecha_aceptacion timestamp without time zone,
    estado_disponibilidad character varying(255) NOT NULL,
    sello_inicio_validez timestamp without time zone,
    tipo_principal character varying(255),
    fecha_grabacion timestamp without time zone,
    fecha_entrega timestamp without time zone,
    s_espacio_de_nombres character varying(255) NOT NULL,
    s_local_id character varying(255) NOT NULL,
    oficialidad boolean
);


ALTER TABLE interlis_ili2db3_ladm.col_fuenteespacial OWNER TO postgres;

--
-- TOC entry 12544 (class 0 OID 0)
-- Dependencies: 1992
-- Name: TABLE col_fuenteespacial; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_fuenteespacial IS 'Especialización de la clase COL_Fuente para almacenar las fuentes constituidas por datos espaciales (entidades geográficas, imágenes de satélite, vuelos fotogramétricos, listados de coordenadas, mapas, planos antiguos o modernos, descripción de localizaciones, etc.) que documentan técnicamente la relación entre instancias de interesados y de predios
@iliname LADM_COL_V1_1.LADM_Nucleo.COL_FuenteEspacial';


--
-- TOC entry 12545 (class 0 OID 0)
-- Dependencies: 1992
-- Name: COLUMN col_fuenteespacial.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteespacial.tipo IS '@iliname Tipo';


--
-- TOC entry 12546 (class 0 OID 0)
-- Dependencies: 1992
-- Name: COLUMN col_fuenteespacial.fecha_aceptacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteespacial.fecha_aceptacion IS '@iliname Fecha_Aceptacion';


--
-- TOC entry 12547 (class 0 OID 0)
-- Dependencies: 1992
-- Name: COLUMN col_fuenteespacial.estado_disponibilidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteespacial.estado_disponibilidad IS 'Indica si la fuente está o no disponible y en qué condiciones. También puede indicar porqué ha dejado de estar disponible, si ha ocurrido.
@iliname Estado_Disponibilidad';


--
-- TOC entry 12548 (class 0 OID 0)
-- Dependencies: 1992
-- Name: COLUMN col_fuenteespacial.sello_inicio_validez; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteespacial.sello_inicio_validez IS 'Fecha de inicio de validez de la fuente.
@iliname Sello_Inicio_Validez';


--
-- TOC entry 12549 (class 0 OID 0)
-- Dependencies: 1992
-- Name: COLUMN col_fuenteespacial.tipo_principal; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteespacial.tipo_principal IS 'Tipo de formato en el que es presentada la fuente, de acuerdo con el registro de metadatos.
@iliname Tipo_Principal';


--
-- TOC entry 12550 (class 0 OID 0)
-- Dependencies: 1992
-- Name: COLUMN col_fuenteespacial.fecha_grabacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteespacial.fecha_grabacion IS 'Fecha en la que es almacenado el documento fuente.
@iliname Fecha_Grabacion';


--
-- TOC entry 12551 (class 0 OID 0)
-- Dependencies: 1992
-- Name: COLUMN col_fuenteespacial.fecha_entrega; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteespacial.fecha_entrega IS 'Fecha en la que se entrega la fuente.
@iliname Fecha_Entrega';


--
-- TOC entry 12552 (class 0 OID 0)
-- Dependencies: 1992
-- Name: COLUMN col_fuenteespacial.s_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteespacial.s_espacio_de_nombres IS 'Identificación inéquivoca de la fuente en el sistema.
@iliname s_Espacio_De_Nombres';


--
-- TOC entry 12553 (class 0 OID 0)
-- Dependencies: 1992
-- Name: COLUMN col_fuenteespacial.s_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteespacial.s_local_id IS 'Identificador de la fuente en el sistema local.
@iliname s_Local_Id';


--
-- TOC entry 12554 (class 0 OID 0)
-- Dependencies: 1992
-- Name: COLUMN col_fuenteespacial.oficialidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_fuenteespacial.oficialidad IS 'Indica si se trata de un documento oficial o no.
@iliname Oficialidad';


--
-- TOC entry 1993 (class 1259 OID 335347)
-- Name: col_fuenteespacialtipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_fuenteespacialtipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_fuenteespacialtipo OWNER TO postgres;

--
-- TOC entry 1994 (class 1259 OID 335353)
-- Name: col_funcioninteresadotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_funcioninteresadotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_funcioninteresadotipo OWNER TO postgres;

--
-- TOC entry 1995 (class 1259 OID 335359)
-- Name: col_generotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_generotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_generotipo OWNER TO postgres;

--
-- TOC entry 1996 (class 1259 OID 335365)
-- Name: col_grupointeresadotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_grupointeresadotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_grupointeresadotipo OWNER TO postgres;

--
-- TOC entry 1997 (class 1259 OID 335371)
-- Name: col_hipoteca; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_hipoteca (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    h_tipo character varying(255),
    codigo_registral_hipoteca character varying(5),
    interesado_requerido boolean,
    tipo character varying(255) NOT NULL,
    codigo_registral_restriccion character varying(5),
    descripcion character varying(255),
    comprobacion_comparte boolean,
    uso_efectivo character varying(255),
    r_espacio_de_nombres character varying(255) NOT NULL,
    r_local_id character varying(255) NOT NULL,
    interesado_la_agrupacion_interesados bigint,
    interesado_col_interesado bigint,
    unidad_la_baunit bigint,
    unidad_predio bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone
);


ALTER TABLE interlis_ili2db3_ladm.col_hipoteca OWNER TO postgres;

--
-- TOC entry 12555 (class 0 OID 0)
-- Dependencies: 1997
-- Name: TABLE col_hipoteca; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_hipoteca IS 'Clase que representa un tipo de restricción heredando de COL_Restricción, asociada a un derecho y que permite gestionar las hipotecas constituídas sobre un bien inmueble, considerando las cuestiones legales nacionales.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Hipoteca';


--
-- TOC entry 12556 (class 0 OID 0)
-- Dependencies: 1997
-- Name: COLUMN col_hipoteca.h_tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_hipoteca.h_tipo IS 'Tipo de hipoteca constituida, conforme a la legislación colombiana.
@iliname h_Tipo';


--
-- TOC entry 12557 (class 0 OID 0)
-- Dependencies: 1997
-- Name: COLUMN col_hipoteca.codigo_registral_hipoteca; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_hipoteca.codigo_registral_hipoteca IS 'Código con el que la hipoteca se registra en el Registro de la Propiedad Inmobiliaria en el momento de ser constituida.
@iliname Codigo_Registral_Hipoteca';


--
-- TOC entry 12558 (class 0 OID 0)
-- Dependencies: 1997
-- Name: COLUMN col_hipoteca.interesado_requerido; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_hipoteca.interesado_requerido IS 'Indica si es preciso o no que un interesado esté asociado a la restricción.
@iliname Interesado_Requerido';


--
-- TOC entry 12559 (class 0 OID 0)
-- Dependencies: 1997
-- Name: COLUMN col_hipoteca.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_hipoteca.tipo IS 'Define el tipo de restricción.
@iliname Tipo';


--
-- TOC entry 12560 (class 0 OID 0)
-- Dependencies: 1997
-- Name: COLUMN col_hipoteca.codigo_registral_restriccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_hipoteca.codigo_registral_restriccion IS 'Código con el que la responsabilidad se registra en el Registro de la Propiedad.
@iliname Codigo_Registral_Restriccion';


--
-- TOC entry 12561 (class 0 OID 0)
-- Dependencies: 1997
-- Name: COLUMN col_hipoteca.descripcion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_hipoteca.descripcion IS 'Descripción relatical al derecho, la responsabilidad o la restricción.
@iliname Descripcion';


--
-- TOC entry 12562 (class 0 OID 0)
-- Dependencies: 1997
-- Name: COLUMN col_hipoteca.comprobacion_comparte; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_hipoteca.comprobacion_comparte IS 'Indicación de si comparte o no.
@iliname Comprobacion_Comparte';


--
-- TOC entry 12563 (class 0 OID 0)
-- Dependencies: 1997
-- Name: COLUMN col_hipoteca.uso_efectivo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_hipoteca.uso_efectivo IS 'Descripción de cual es el uso efectivo.
@iliname Uso_Efectivo';


--
-- TOC entry 12564 (class 0 OID 0)
-- Dependencies: 1997
-- Name: COLUMN col_hipoteca.r_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_hipoteca.r_espacio_de_nombres IS 'Identificador global único.
@iliname r_Espacio_De_Nombres';


--
-- TOC entry 12565 (class 0 OID 0)
-- Dependencies: 1997
-- Name: COLUMN col_hipoteca.r_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_hipoteca.r_local_id IS 'Identificador único local.
@iliname r_Local_Id';


--
-- TOC entry 12566 (class 0 OID 0)
-- Dependencies: 1997
-- Name: COLUMN col_hipoteca.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_hipoteca.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12567 (class 0 OID 0)
-- Dependencies: 1997
-- Name: COLUMN col_hipoteca.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_hipoteca.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 1998 (class 1259 OID 335378)
-- Name: col_hipotecatipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_hipotecatipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_hipotecatipo OWNER TO postgres;

--
-- TOC entry 1999 (class 1259 OID 335384)
-- Name: col_instituciontipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_instituciontipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_instituciontipo OWNER TO postgres;

--
-- TOC entry 2000 (class 1259 OID 335390)
-- Name: col_interesado; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_interesado (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    documento_identidad character varying(12) NOT NULL,
    tipo_documento character varying(255) NOT NULL,
    organo_emisor character varying(20),
    fecha_emision date,
    primer_apellido character varying(100),
    primer_nombre character varying(100),
    segundo_apellido character varying(100),
    segundo_nombre character varying(100),
    razon_social character varying(250),
    genero character varying(255),
    tipo_interesado_juridico character varying(255),
    nombre character varying(255),
    tipo character varying(255) NOT NULL,
    p_espacio_de_nombres character varying(255) NOT NULL,
    p_local_id character varying(255) NOT NULL,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone
);


ALTER TABLE interlis_ili2db3_ladm.col_interesado OWNER TO postgres;

--
-- TOC entry 12568 (class 0 OID 0)
-- Dependencies: 2000
-- Name: TABLE col_interesado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_interesado IS '@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado';


--
-- TOC entry 12569 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.documento_identidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.documento_identidad IS 'Documento de identidad del interesado.
@iliname Documento_Identidad';


--
-- TOC entry 12570 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.tipo_documento; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.tipo_documento IS 'Tipo de documento del que se trata.
@iliname Tipo_Documento';


--
-- TOC entry 12571 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.organo_emisor; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.organo_emisor IS 'Quien ha emitido el documento de identidad.
@iliname Organo_Emisor';


--
-- TOC entry 12572 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.fecha_emision; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.fecha_emision IS 'Fecha de emisión del documento de identidad.
@iliname Fecha_Emision';


--
-- TOC entry 12573 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.primer_apellido; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.primer_apellido IS 'Primer apellido de la persona física.
@iliname Primer_Apellido';


--
-- TOC entry 12574 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.primer_nombre; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.primer_nombre IS 'Primer nombre de la persona física.
@iliname Primer_Nombre';


--
-- TOC entry 12575 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.segundo_apellido; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.segundo_apellido IS 'Segundo apellido de la persona física.
@iliname Segundo_Apellido';


--
-- TOC entry 12576 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.segundo_nombre; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.segundo_nombre IS 'Segundo nombre de la persona física.
@iliname Segundo_Nombre';


--
-- TOC entry 12577 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.razon_social; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.razon_social IS 'Nombre con el que está inscrito.
@iliname Razon_Social';


--
-- TOC entry 12578 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.genero; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.genero IS '@iliname Genero';


--
-- TOC entry 12579 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.tipo_interesado_juridico; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.tipo_interesado_juridico IS '@iliname Tipo_Interesado_Juridico';


--
-- TOC entry 12580 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.nombre; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.nombre IS 'Nombre del interesado.
@iliname Nombre';


--
-- TOC entry 12581 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.tipo IS 'Tipo de persona del que se trata.
@iliname Tipo';


--
-- TOC entry 12582 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.p_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.p_espacio_de_nombres IS 'Identificador único global.
@iliname p_Espacio_De_Nombres';


--
-- TOC entry 12583 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.p_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.p_local_id IS 'Identificador único local.
@iliname p_Local_Id';


--
-- TOC entry 12584 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12585 (class 0 OID 0)
-- Dependencies: 2000
-- Name: COLUMN col_interesado.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_interesado.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 2001 (class 1259 OID 335397)
-- Name: col_interesadodocumentotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_interesadodocumentotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_interesadodocumentotipo OWNER TO postgres;

--
-- TOC entry 2002 (class 1259 OID 335403)
-- Name: col_interesadojuridicotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_interesadojuridicotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_interesadojuridicotipo OWNER TO postgres;

--
-- TOC entry 2003 (class 1259 OID 335409)
-- Name: col_interpolaciontipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_interpolaciontipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_interpolaciontipo OWNER TO postgres;

--
-- TOC entry 2004 (class 1259 OID 335415)
-- Name: col_levelcontenttipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_levelcontenttipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_levelcontenttipo OWNER TO postgres;

--
-- TOC entry 2005 (class 1259 OID 335421)
-- Name: col_monumentaciontipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_monumentaciontipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_monumentaciontipo OWNER TO postgres;

--
-- TOC entry 2006 (class 1259 OID 335427)
-- Name: col_prediotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_prediotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_prediotipo OWNER TO postgres;

--
-- TOC entry 2007 (class 1259 OID 335433)
-- Name: col_publicidadtipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_publicidadtipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_publicidadtipo OWNER TO postgres;

--
-- TOC entry 2008 (class 1259 OID 335439)
-- Name: col_puntocontroltipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_puntocontroltipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_puntocontroltipo OWNER TO postgres;

--
-- TOC entry 2009 (class 1259 OID 335445)
-- Name: col_puntolevtipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_puntolevtipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_puntolevtipo OWNER TO postgres;

--
-- TOC entry 2010 (class 1259 OID 335451)
-- Name: col_redserviciostipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_redserviciostipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_redserviciostipo OWNER TO postgres;

--
-- TOC entry 2011 (class 1259 OID 335457)
-- Name: col_responsabilidad; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_responsabilidad (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    tipo character varying(255) NOT NULL,
    codigo_registral_responsabilidad character varying(5),
    descripcion character varying(255),
    comprobacion_comparte boolean,
    uso_efectivo character varying(255),
    r_espacio_de_nombres character varying(255) NOT NULL,
    r_local_id character varying(255) NOT NULL,
    interesado_la_agrupacion_interesados bigint,
    interesado_col_interesado bigint,
    unidad_la_baunit bigint,
    unidad_predio bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone
);


ALTER TABLE interlis_ili2db3_ladm.col_responsabilidad OWNER TO postgres;

--
-- TOC entry 12586 (class 0 OID 0)
-- Dependencies: 2011
-- Name: TABLE col_responsabilidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_responsabilidad IS 'Clase de tipo LA_RRR que registra las responsabilidades que las instancias de los interesados tienen sobre los predios.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Responsabilidad';


--
-- TOC entry 12587 (class 0 OID 0)
-- Dependencies: 2011
-- Name: COLUMN col_responsabilidad.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_responsabilidad.tipo IS 'Definición del tipo de responsabilidad que se tiene.
@iliname Tipo';


--
-- TOC entry 12588 (class 0 OID 0)
-- Dependencies: 2011
-- Name: COLUMN col_responsabilidad.codigo_registral_responsabilidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_responsabilidad.codigo_registral_responsabilidad IS 'Código con el que la responsabilidad se registra en el Registro de la Propiedad.
@iliname Codigo_Registral_Responsabilidad';


--
-- TOC entry 12589 (class 0 OID 0)
-- Dependencies: 2011
-- Name: COLUMN col_responsabilidad.descripcion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_responsabilidad.descripcion IS 'Descripción relatical al derecho, la responsabilidad o la restricción.
@iliname Descripcion';


--
-- TOC entry 12590 (class 0 OID 0)
-- Dependencies: 2011
-- Name: COLUMN col_responsabilidad.comprobacion_comparte; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_responsabilidad.comprobacion_comparte IS 'Indicación de si comparte o no.
@iliname Comprobacion_Comparte';


--
-- TOC entry 12591 (class 0 OID 0)
-- Dependencies: 2011
-- Name: COLUMN col_responsabilidad.uso_efectivo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_responsabilidad.uso_efectivo IS 'Descripción de cual es el uso efectivo.
@iliname Uso_Efectivo';


--
-- TOC entry 12592 (class 0 OID 0)
-- Dependencies: 2011
-- Name: COLUMN col_responsabilidad.r_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_responsabilidad.r_espacio_de_nombres IS 'Identificador global único.
@iliname r_Espacio_De_Nombres';


--
-- TOC entry 12593 (class 0 OID 0)
-- Dependencies: 2011
-- Name: COLUMN col_responsabilidad.r_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_responsabilidad.r_local_id IS 'Identificador único local.
@iliname r_Local_Id';


--
-- TOC entry 12594 (class 0 OID 0)
-- Dependencies: 2011
-- Name: COLUMN col_responsabilidad.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_responsabilidad.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12595 (class 0 OID 0)
-- Dependencies: 2011
-- Name: COLUMN col_responsabilidad.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_responsabilidad.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 2012 (class 1259 OID 335464)
-- Name: col_responsabilidadtipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_responsabilidadtipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_responsabilidadtipo OWNER TO postgres;

--
-- TOC entry 2013 (class 1259 OID 335470)
-- Name: col_restriccion; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_restriccion (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    interesado_requerido boolean,
    tipo character varying(255) NOT NULL,
    codigo_registral_restriccion character varying(5),
    descripcion character varying(255),
    comprobacion_comparte boolean,
    uso_efectivo character varying(255),
    r_espacio_de_nombres character varying(255) NOT NULL,
    r_local_id character varying(255) NOT NULL,
    interesado_la_agrupacion_interesados bigint,
    interesado_col_interesado bigint,
    unidad_la_baunit bigint,
    unidad_predio bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone
);


ALTER TABLE interlis_ili2db3_ladm.col_restriccion OWNER TO postgres;

--
-- TOC entry 12596 (class 0 OID 0)
-- Dependencies: 2013
-- Name: TABLE col_restriccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_restriccion IS 'Restricciones a las que está sometido un predio y que inciden sobre los derechos que pueden ejercerse sobre él.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Restriccion';


--
-- TOC entry 12597 (class 0 OID 0)
-- Dependencies: 2013
-- Name: COLUMN col_restriccion.interesado_requerido; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_restriccion.interesado_requerido IS 'Indica si es preciso o no que un interesado esté asociado a la restricción.
@iliname Interesado_Requerido';


--
-- TOC entry 12598 (class 0 OID 0)
-- Dependencies: 2013
-- Name: COLUMN col_restriccion.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_restriccion.tipo IS 'Define el tipo de restricción.
@iliname Tipo';


--
-- TOC entry 12599 (class 0 OID 0)
-- Dependencies: 2013
-- Name: COLUMN col_restriccion.codigo_registral_restriccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_restriccion.codigo_registral_restriccion IS 'Código con el que la responsabilidad se registra en el Registro de la Propiedad.
@iliname Codigo_Registral_Restriccion';


--
-- TOC entry 12600 (class 0 OID 0)
-- Dependencies: 2013
-- Name: COLUMN col_restriccion.descripcion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_restriccion.descripcion IS 'Descripción relatical al derecho, la responsabilidad o la restricción.
@iliname Descripcion';


--
-- TOC entry 12601 (class 0 OID 0)
-- Dependencies: 2013
-- Name: COLUMN col_restriccion.comprobacion_comparte; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_restriccion.comprobacion_comparte IS 'Indicación de si comparte o no.
@iliname Comprobacion_Comparte';


--
-- TOC entry 12602 (class 0 OID 0)
-- Dependencies: 2013
-- Name: COLUMN col_restriccion.uso_efectivo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_restriccion.uso_efectivo IS 'Descripción de cual es el uso efectivo.
@iliname Uso_Efectivo';


--
-- TOC entry 12603 (class 0 OID 0)
-- Dependencies: 2013
-- Name: COLUMN col_restriccion.r_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_restriccion.r_espacio_de_nombres IS 'Identificador global único.
@iliname r_Espacio_De_Nombres';


--
-- TOC entry 12604 (class 0 OID 0)
-- Dependencies: 2013
-- Name: COLUMN col_restriccion.r_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_restriccion.r_local_id IS 'Identificador único local.
@iliname r_Local_Id';


--
-- TOC entry 12605 (class 0 OID 0)
-- Dependencies: 2013
-- Name: COLUMN col_restriccion.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_restriccion.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12606 (class 0 OID 0)
-- Dependencies: 2013
-- Name: COLUMN col_restriccion.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_restriccion.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 2014 (class 1259 OID 335477)
-- Name: col_restricciontipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_restricciontipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_restricciontipo OWNER TO postgres;

--
-- TOC entry 2015 (class 1259 OID 335483)
-- Name: col_servidumbretipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_servidumbretipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_servidumbretipo OWNER TO postgres;

--
-- TOC entry 2016 (class 1259 OID 335489)
-- Name: col_servidumbretipo_terreno_servidumbre; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_servidumbretipo_terreno_servidumbre (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    avalue character varying(255) NOT NULL,
    terreno_servidumbre bigint
);


ALTER TABLE interlis_ili2db3_ladm.col_servidumbretipo_terreno_servidumbre OWNER TO postgres;

--
-- TOC entry 12607 (class 0 OID 0)
-- Dependencies: 2016
-- Name: TABLE col_servidumbretipo_terreno_servidumbre; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_servidumbretipo_terreno_servidumbre IS '@iliname Catastro_Registro_Nucleo_V2_2_1.COL_ServidumbreTipo_Terreno_Servidumbre';


--
-- TOC entry 12608 (class 0 OID 0)
-- Dependencies: 2016
-- Name: COLUMN col_servidumbretipo_terreno_servidumbre.avalue; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_servidumbretipo_terreno_servidumbre.avalue IS '@iliname value';


--
-- TOC entry 12609 (class 0 OID 0)
-- Dependencies: 2016
-- Name: COLUMN col_servidumbretipo_terreno_servidumbre.terreno_servidumbre; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_servidumbretipo_terreno_servidumbre.terreno_servidumbre IS 'Tipo de derecho que limita el dominio de una porción del predio, corresponde a la pregunta 5.8 del anexo 5.1 de los estandares de catastro multiproposito versión 2.1.1
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Servidumbre';


--
-- TOC entry 2017 (class 1259 OID 335493)
-- Name: col_territorioagricola; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_territorioagricola (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_territorioagricola OWNER TO postgres;

--
-- TOC entry 2018 (class 1259 OID 335499)
-- Name: col_territorioagricola_terreno_territorio_agricola; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_territorioagricola_terreno_territorio_agricola (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    avalue character varying(255) NOT NULL,
    terreno_territorio_agricola bigint
);


ALTER TABLE interlis_ili2db3_ladm.col_territorioagricola_terreno_territorio_agricola OWNER TO postgres;

--
-- TOC entry 12610 (class 0 OID 0)
-- Dependencies: 2018
-- Name: TABLE col_territorioagricola_terreno_territorio_agricola; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.col_territorioagricola_terreno_territorio_agricola IS '@iliname Catastro_Registro_Nucleo_V2_2_1.COL_TerritorioAgricola_Terreno_Territorio_Agricola';


--
-- TOC entry 12611 (class 0 OID 0)
-- Dependencies: 2018
-- Name: COLUMN col_territorioagricola_terreno_territorio_agricola.avalue; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_territorioagricola_terreno_territorio_agricola.avalue IS '@iliname value';


--
-- TOC entry 12612 (class 0 OID 0)
-- Dependencies: 2018
-- Name: COLUMN col_territorioagricola_terreno_territorio_agricola.terreno_territorio_agricola; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.col_territorioagricola_terreno_territorio_agricola.terreno_territorio_agricola IS 'se caracterizan los diferentes tipos de cultivos o territorios agricolas que conforman el predio, corresponde a la pregunta 5.3 del anexo 5.1 de los estandares de catastro multiproposito versión 2.1.1
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Territorio_Agricola';


--
-- TOC entry 2019 (class 1259 OID 335503)
-- Name: col_tipoconstrucciontipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_tipoconstrucciontipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_tipoconstrucciontipo OWNER TO postgres;

--
-- TOC entry 2020 (class 1259 OID 335509)
-- Name: col_unidadedificaciontipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_unidadedificaciontipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_unidadedificaciontipo OWNER TO postgres;

--
-- TOC entry 2021 (class 1259 OID 335515)
-- Name: col_viatipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_viatipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_viatipo OWNER TO postgres;

--
-- TOC entry 2022 (class 1259 OID 335521)
-- Name: col_zonatipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.col_zonatipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.col_zonatipo OWNER TO postgres;

--
-- TOC entry 2023 (class 1259 OID 335527)
-- Name: construccion; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.construccion (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    avaluo_construccion numeric(16,1) NOT NULL,
    area_construccion numeric(15,1),
    tipo character varying(255),
    dimension character varying(255),
    etiqueta character varying(255),
    relacion_superficie character varying(255),
    su_espacio_de_nombres character varying(255) NOT NULL,
    su_local_id character varying(255) NOT NULL,
    nivel bigint,
    uej2_la_unidadespacial bigint,
    uej2_la_espaciojuridicoredservicios bigint,
    uej2_la_espaciojuridicounidadedificacion bigint,
    uej2_servidumbrepaso bigint,
    uej2_terreno bigint,
    uej2_construccion bigint,
    uej2_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    punto_referencia public.geometry(Point,3116),
    poligono_creado public.geometry(MultiPolygon,3116),
    CONSTRAINT construccion_area_construccion_check CHECK (((area_construccion >= 0.0) AND (area_construccion <= 99999999999999.9))),
    CONSTRAINT construccion_avaluo_construccion_check CHECK (((avaluo_construccion >= 0.0) AND (avaluo_construccion <= '999999999999999'::numeric)))
);


ALTER TABLE interlis_ili2db3_ladm.construccion OWNER TO postgres;

--
-- TOC entry 12613 (class 0 OID 0)
-- Dependencies: 2023
-- Name: TABLE construccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.construccion IS 'Es un tipo de espacio jurídico de la unidad de edificación del modelo LADM que almacena datos específicos del avalúo resultante del mismo.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Construccion';


--
-- TOC entry 12614 (class 0 OID 0)
-- Dependencies: 2023
-- Name: COLUMN construccion.avaluo_construccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.construccion.avaluo_construccion IS 'Rsultado del cálculo de su avalúo mediante la metodología legalmente establecida.
@iliname Avaluo_Construccion';


--
-- TOC entry 12615 (class 0 OID 0)
-- Dependencies: 2023
-- Name: COLUMN construccion.area_construccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.construccion.area_construccion IS '@iliname Area_Construccion';


--
-- TOC entry 12616 (class 0 OID 0)
-- Dependencies: 2023
-- Name: COLUMN construccion.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.construccion.tipo IS 'Tipo de unidad de edificación de la que se trata.
@iliname Tipo';


--
-- TOC entry 12617 (class 0 OID 0)
-- Dependencies: 2023
-- Name: COLUMN construccion.dimension; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.construccion.dimension IS '@iliname Dimension';


--
-- TOC entry 12618 (class 0 OID 0)
-- Dependencies: 2023
-- Name: COLUMN construccion.etiqueta; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.construccion.etiqueta IS 'Corresponde al atributo label de la clase en LADM.
@iliname Etiqueta';


--
-- TOC entry 12619 (class 0 OID 0)
-- Dependencies: 2023
-- Name: COLUMN construccion.relacion_superficie; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.construccion.relacion_superficie IS 'Corresponde al atributo surfaceRelation de la clase en LADM.
@iliname Relacion_Superficie';


--
-- TOC entry 12620 (class 0 OID 0)
-- Dependencies: 2023
-- Name: COLUMN construccion.su_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.construccion.su_espacio_de_nombres IS 'Identificador único global. Corresponde al atributo suID de la clase en LADM.
@iliname su_Espacio_De_Nombres';


--
-- TOC entry 12621 (class 0 OID 0)
-- Dependencies: 2023
-- Name: COLUMN construccion.su_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.construccion.su_local_id IS 'Identificador único local.
@iliname su_Local_Id';


--
-- TOC entry 12622 (class 0 OID 0)
-- Dependencies: 2023
-- Name: COLUMN construccion.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.construccion.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12623 (class 0 OID 0)
-- Dependencies: 2023
-- Name: COLUMN construccion.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.construccion.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 12624 (class 0 OID 0)
-- Dependencies: 2023
-- Name: COLUMN construccion.punto_referencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.construccion.punto_referencia IS 'Corresponde al atributo referencePoint de la clase en LADM.
@iliname Punto_Referencia';


--
-- TOC entry 12625 (class 0 OID 0)
-- Dependencies: 2023
-- Name: COLUMN construccion.poligono_creado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.construccion.poligono_creado IS 'Materializacion del metodo createArea(). Almacena de forma permanente la geometría de tipo poligonal.';


--
-- TOC entry 2024 (class 1259 OID 335536)
-- Name: dq_absoluteexternalpositionalaccuracy; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    atributo1 character varying(255),
    atributo21 character varying(255),
    nombre_medida character varying(255),
    identificacion_medida character varying(255),
    descripcion_medida character varying(255),
    metodo_evaluacion character varying(255),
    descripcion_metodo_evaluacion character varying(255),
    procedimiento_evaluacion character varying(255),
    fecha_hora timestamp without time zone,
    resultado character varying(255)
);


ALTER TABLE interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy OWNER TO postgres;

--
-- TOC entry 12626 (class 0 OID 0)
-- Dependencies: 2024
-- Name: TABLE dq_absoluteexternalpositionalaccuracy; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy IS 'DEFINIR y DOCUMENTAR. Se hace necesaria para su uso por ObjetoVersionado.
@iliname LADM_COL_V1_1.LADM_Nucleo.DQ_AbsoluteExternalPositionalAccuracy';


--
-- TOC entry 12627 (class 0 OID 0)
-- Dependencies: 2024
-- Name: COLUMN dq_absoluteexternalpositionalaccuracy.atributo1; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy.atributo1 IS 'DEFINIR';


--
-- TOC entry 12628 (class 0 OID 0)
-- Dependencies: 2024
-- Name: COLUMN dq_absoluteexternalpositionalaccuracy.atributo21; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy.atributo21 IS 'MODELAR.';


--
-- TOC entry 12629 (class 0 OID 0)
-- Dependencies: 2024
-- Name: COLUMN dq_absoluteexternalpositionalaccuracy.nombre_medida; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy.nombre_medida IS 'Nombre de la prueba aplicada a los datos. Proviene de la agregación de la clase DQ_MeasureReference a DQ_Element.
@iliname Nombre_Medida';


--
-- TOC entry 12630 (class 0 OID 0)
-- Dependencies: 2024
-- Name: COLUMN dq_absoluteexternalpositionalaccuracy.identificacion_medida; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy.identificacion_medida IS 'Identificador de la medida, valor que identifica de manera única la medida dentro de un espacio de nombres. Proviene de la agregación de la clase DQ_MeasureReference a DQ_Element.
@iliname Identificacion_Medida';


--
-- TOC entry 12631 (class 0 OID 0)
-- Dependencies: 2024
-- Name: COLUMN dq_absoluteexternalpositionalaccuracy.descripcion_medida; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy.descripcion_medida IS 'Descripción. Proviene de la agregación de la clase DQ_MeasureReference a DQ_Element.
@iliname Descripcion_Medida';


--
-- TOC entry 12632 (class 0 OID 0)
-- Dependencies: 2024
-- Name: COLUMN dq_absoluteexternalpositionalaccuracy.metodo_evaluacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy.metodo_evaluacion IS 'Método utilizado para evaluar la calidad de los datos. Proviene de la agregación de la clase DQ_EvaluationMethod a DQ_Element.
@iliname Metodo_Evaluacion';


--
-- TOC entry 12633 (class 0 OID 0)
-- Dependencies: 2024
-- Name: COLUMN dq_absoluteexternalpositionalaccuracy.descripcion_metodo_evaluacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy.descripcion_metodo_evaluacion IS 'Descripción del método de evaluación. Proviene de la agregación de la clase DQ_EvaluationMethod a DQ_Element.
@iliname Descripcion_Metodo_Evaluacion';


--
-- TOC entry 12634 (class 0 OID 0)
-- Dependencies: 2024
-- Name: COLUMN dq_absoluteexternalpositionalaccuracy.procedimiento_evaluacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy.procedimiento_evaluacion IS 'Referencia a la información del procedimiento. Proviene de la agregación de la clase DQ_MeasureReference a DQ_Element.
@iliname Procedimiento_Evaluacion';


--
-- TOC entry 12635 (class 0 OID 0)
-- Dependencies: 2024
-- Name: COLUMN dq_absoluteexternalpositionalaccuracy.fecha_hora; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy.fecha_hora IS 'Fecha y hora en la que se generan los resultados. Proviene de la agregación de la clase DQ_Result a DQ_Element.
@iliname Fecha_Hora';


--
-- TOC entry 12636 (class 0 OID 0)
-- Dependencies: 2024
-- Name: COLUMN dq_absoluteexternalpositionalaccuracy.resultado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy.resultado IS 'Alcance del resultado de la prueba de calidad. Proviene de la agregación de la clase DQ_Result a DQ_Element.
@iliname Resultado';


--
-- TOC entry 2025 (class 1259 OID 335543)
-- Name: dq_element; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.dq_element (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    nombre_medida character varying(255),
    identificacion_medida character varying(255),
    descripcion_medida character varying(255),
    metodo_evaluacion character varying(255),
    descripcion_metodo_evaluacion character varying(255),
    procedimiento_evaluacion character varying(255),
    fecha_hora timestamp without time zone,
    resultado character varying(255),
    om_observacion_resultado_calidad bigint,
    col_fuenteadminstrtiva_calidad bigint,
    la_unidadespacial_calidad bigint,
    la_agrupacinnddsspcles_calidad bigint,
    la_espacjrdcndddfccion_calidad bigint,
    la_espacijrdcrdsrvcios_calidad bigint,
    la_nivel_calidad bigint,
    la_relcnncsrnddsspcles_calidad bigint,
    la_baunit_calidad bigint,
    la_relacionnecesrbnits_calidad bigint,
    la_punto_calidad bigint,
    col_fuenteespacial_calidad bigint,
    la_cadenacaraslimite_calidad bigint,
    la_caraslindero_calidad bigint,
    la_agrupacion_intrsdos_calidad bigint,
    col_derecho_calidad bigint,
    col_interesado_calidad bigint,
    construccion_calidad bigint,
    lindero_calidad bigint,
    predio_calidad bigint,
    publicidad_calidad bigint,
    puntocontrol_calidad bigint,
    puntolindero_calidad bigint,
    terreno_calidad bigint,
    col_restriccion_calidad bigint,
    puntolevantamiento_calidad bigint,
    col_responsabilidad_calidad bigint,
    servidumbrepaso_calidad bigint,
    col_hipoteca_calidad bigint,
    unidadconstruccion_calidad bigint
);


ALTER TABLE interlis_ili2db3_ladm.dq_element OWNER TO postgres;

--
-- TOC entry 12637 (class 0 OID 0)
-- Dependencies: 2025
-- Name: TABLE dq_element; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.dq_element IS 'Clase traducida a partir de DQ_Element de la norma ISO 19157.
Contiene los aspectos de la información de calidad cuantitativa. REVISAR MODELADO
@iliname LADM_COL_V1_1.LADM_Nucleo.DQ_Element';


--
-- TOC entry 12638 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.nombre_medida; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.nombre_medida IS 'Nombre de la prueba aplicada a los datos. Proviene de la agregación de la clase DQ_MeasureReference a DQ_Element.
@iliname Nombre_Medida';


--
-- TOC entry 12639 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.identificacion_medida; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.identificacion_medida IS 'Identificador de la medida, valor que identifica de manera única la medida dentro de un espacio de nombres. Proviene de la agregación de la clase DQ_MeasureReference a DQ_Element.
@iliname Identificacion_Medida';


--
-- TOC entry 12640 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.descripcion_medida; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.descripcion_medida IS 'Descripción. Proviene de la agregación de la clase DQ_MeasureReference a DQ_Element.
@iliname Descripcion_Medida';


--
-- TOC entry 12641 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.metodo_evaluacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.metodo_evaluacion IS 'Método utilizado para evaluar la calidad de los datos. Proviene de la agregación de la clase DQ_EvaluationMethod a DQ_Element.
@iliname Metodo_Evaluacion';


--
-- TOC entry 12642 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.descripcion_metodo_evaluacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.descripcion_metodo_evaluacion IS 'Descripción del método de evaluación. Proviene de la agregación de la clase DQ_EvaluationMethod a DQ_Element.
@iliname Descripcion_Metodo_Evaluacion';


--
-- TOC entry 12643 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.procedimiento_evaluacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.procedimiento_evaluacion IS 'Referencia a la información del procedimiento. Proviene de la agregación de la clase DQ_MeasureReference a DQ_Element.
@iliname Procedimiento_Evaluacion';


--
-- TOC entry 12644 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.fecha_hora; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.fecha_hora IS 'Fecha y hora en la que se generan los resultados. Proviene de la agregación de la clase DQ_Result a DQ_Element.
@iliname Fecha_Hora';


--
-- TOC entry 12645 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.resultado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.resultado IS 'Alcance del resultado de la prueba de calidad. Proviene de la agregación de la clase DQ_Result a DQ_Element.
@iliname Resultado';


--
-- TOC entry 12646 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.om_observacion_resultado_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.om_observacion_resultado_calidad IS 'Resultado del proceso de calidad, conforme a DQ_Element.
@iliname LADM_COL_V1_1.LADM_Nucleo.OM_Observacion.Resultado_Calidad';


--
-- TOC entry 12647 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.col_fuenteadminstrtiva_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.col_fuenteadminstrtiva_calidad IS 'Descripción de la calidad del documento de acuerdo a los metadatos del objeto DQ_Element, clase de la norma ISO 19157 que se refiere a aspectos de la información de calidad cuantitativa de la instancia referenciada.
@iliname LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Calidad';


--
-- TOC entry 12648 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.la_unidadespacial_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.la_unidadespacial_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12649 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.la_agrupacinnddsspcles_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.la_agrupacinnddsspcles_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12650 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.la_espacjrdcndddfccion_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.la_espacjrdcndddfccion_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12651 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.la_espacijrdcrdsrvcios_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.la_espacijrdcrdsrvcios_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12652 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.la_nivel_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.la_nivel_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12653 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.la_relcnncsrnddsspcles_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.la_relcnncsrnddsspcles_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12654 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.la_baunit_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.la_baunit_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12655 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.la_relacionnecesrbnits_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.la_relacionnecesrbnits_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12656 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.la_punto_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.la_punto_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12657 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.col_fuenteespacial_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.col_fuenteespacial_calidad IS 'Descripción de la calidad del documento de acuerdo a los metadatos del objeto DQ_Element, clase de la norma ISO 19157 que se refiere a aspectos de la información de calidad cuantitativa de la instancia referenciada.
@iliname LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Calidad';


--
-- TOC entry 12658 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.la_cadenacaraslimite_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.la_cadenacaraslimite_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12659 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.la_caraslindero_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.la_caraslindero_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12660 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.la_agrupacion_intrsdos_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.la_agrupacion_intrsdos_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12661 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.col_derecho_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.col_derecho_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12662 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.col_interesado_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.col_interesado_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12663 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.construccion_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.construccion_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12664 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.lindero_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.lindero_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12665 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.predio_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.predio_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12666 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.publicidad_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.publicidad_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12667 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.puntocontrol_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.puntocontrol_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12668 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.puntolindero_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.puntolindero_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12669 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.terreno_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.terreno_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12670 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.col_restriccion_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.col_restriccion_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12671 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.puntolevantamiento_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.puntolevantamiento_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12672 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.col_responsabilidad_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.col_responsabilidad_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12673 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.servidumbrepaso_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.servidumbrepaso_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12674 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.col_hipoteca_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.col_hipoteca_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 12675 (class 0 OID 0)
-- Dependencies: 2025
-- Name: COLUMN dq_element.unidadconstruccion_calidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_element.unidadconstruccion_calidad IS 'Metadatos relativos a la calidad de la instancia.
@iliname LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad';


--
-- TOC entry 2026 (class 1259 OID 335550)
-- Name: dq_metodo_evaluacion_codigo_tipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.dq_metodo_evaluacion_codigo_tipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.dq_metodo_evaluacion_codigo_tipo OWNER TO postgres;

--
-- TOC entry 2027 (class 1259 OID 335556)
-- Name: dq_positionalaccuracy; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.dq_positionalaccuracy (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    atributo21 character varying(255),
    nombre_medida character varying(255),
    identificacion_medida character varying(255),
    descripcion_medida character varying(255),
    metodo_evaluacion character varying(255),
    descripcion_metodo_evaluacion character varying(255),
    procedimiento_evaluacion character varying(255),
    fecha_hora timestamp without time zone,
    resultado character varying(255),
    la_punto_exactitud_estimada bigint,
    puntocontrol_exactitud_estimada bigint,
    puntolindero_exactitud_estimada bigint,
    puntolevantamiento_exactitud_estimada bigint
);


ALTER TABLE interlis_ili2db3_ladm.dq_positionalaccuracy OWNER TO postgres;

--
-- TOC entry 12676 (class 0 OID 0)
-- Dependencies: 2027
-- Name: TABLE dq_positionalaccuracy; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.dq_positionalaccuracy IS 'estructura no utilizada, se materializa sobre los atributos Extactitud horizontal y vertical
@iliname LADM_COL_V1_1.LADM_Nucleo.DQ_PositionalAccuracy';


--
-- TOC entry 12677 (class 0 OID 0)
-- Dependencies: 2027
-- Name: COLUMN dq_positionalaccuracy.atributo21; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_positionalaccuracy.atributo21 IS 'MODELAR.';


--
-- TOC entry 12678 (class 0 OID 0)
-- Dependencies: 2027
-- Name: COLUMN dq_positionalaccuracy.nombre_medida; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_positionalaccuracy.nombre_medida IS 'Nombre de la prueba aplicada a los datos. Proviene de la agregación de la clase DQ_MeasureReference a DQ_Element.
@iliname Nombre_Medida';


--
-- TOC entry 12679 (class 0 OID 0)
-- Dependencies: 2027
-- Name: COLUMN dq_positionalaccuracy.identificacion_medida; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_positionalaccuracy.identificacion_medida IS 'Identificador de la medida, valor que identifica de manera única la medida dentro de un espacio de nombres. Proviene de la agregación de la clase DQ_MeasureReference a DQ_Element.
@iliname Identificacion_Medida';


--
-- TOC entry 12680 (class 0 OID 0)
-- Dependencies: 2027
-- Name: COLUMN dq_positionalaccuracy.descripcion_medida; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_positionalaccuracy.descripcion_medida IS 'Descripción. Proviene de la agregación de la clase DQ_MeasureReference a DQ_Element.
@iliname Descripcion_Medida';


--
-- TOC entry 12681 (class 0 OID 0)
-- Dependencies: 2027
-- Name: COLUMN dq_positionalaccuracy.metodo_evaluacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_positionalaccuracy.metodo_evaluacion IS 'Método utilizado para evaluar la calidad de los datos. Proviene de la agregación de la clase DQ_EvaluationMethod a DQ_Element.
@iliname Metodo_Evaluacion';


--
-- TOC entry 12682 (class 0 OID 0)
-- Dependencies: 2027
-- Name: COLUMN dq_positionalaccuracy.descripcion_metodo_evaluacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_positionalaccuracy.descripcion_metodo_evaluacion IS 'Descripción del método de evaluación. Proviene de la agregación de la clase DQ_EvaluationMethod a DQ_Element.
@iliname Descripcion_Metodo_Evaluacion';


--
-- TOC entry 12683 (class 0 OID 0)
-- Dependencies: 2027
-- Name: COLUMN dq_positionalaccuracy.procedimiento_evaluacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_positionalaccuracy.procedimiento_evaluacion IS 'Referencia a la información del procedimiento. Proviene de la agregación de la clase DQ_MeasureReference a DQ_Element.
@iliname Procedimiento_Evaluacion';


--
-- TOC entry 12684 (class 0 OID 0)
-- Dependencies: 2027
-- Name: COLUMN dq_positionalaccuracy.fecha_hora; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_positionalaccuracy.fecha_hora IS 'Fecha y hora en la que se generan los resultados. Proviene de la agregación de la clase DQ_Result a DQ_Element.
@iliname Fecha_Hora';


--
-- TOC entry 12685 (class 0 OID 0)
-- Dependencies: 2027
-- Name: COLUMN dq_positionalaccuracy.resultado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_positionalaccuracy.resultado IS 'Alcance del resultado de la prueba de calidad. Proviene de la agregación de la clase DQ_Result a DQ_Element.
@iliname Resultado';


--
-- TOC entry 12686 (class 0 OID 0)
-- Dependencies: 2027
-- Name: COLUMN dq_positionalaccuracy.la_punto_exactitud_estimada; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_positionalaccuracy.la_punto_exactitud_estimada IS 'Atributo no usado, se materializa sobre los atributos Extactitud horizontal y vertical
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Exactitud_Estimada';


--
-- TOC entry 12687 (class 0 OID 0)
-- Dependencies: 2027
-- Name: COLUMN dq_positionalaccuracy.puntocontrol_exactitud_estimada; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_positionalaccuracy.puntocontrol_exactitud_estimada IS 'Atributo no usado, se materializa sobre los atributos Extactitud horizontal y vertical
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Exactitud_Estimada';


--
-- TOC entry 12688 (class 0 OID 0)
-- Dependencies: 2027
-- Name: COLUMN dq_positionalaccuracy.puntolindero_exactitud_estimada; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_positionalaccuracy.puntolindero_exactitud_estimada IS 'Atributo no usado, se materializa sobre los atributos Extactitud horizontal y vertical
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Exactitud_Estimada';


--
-- TOC entry 12689 (class 0 OID 0)
-- Dependencies: 2027
-- Name: COLUMN dq_positionalaccuracy.puntolevantamiento_exactitud_estimada; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.dq_positionalaccuracy.puntolevantamiento_exactitud_estimada IS 'Atributo no usado, se materializa sobre los atributos Extactitud horizontal y vertical
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Exactitud_Estimada';


--
-- TOC entry 2028 (class 1259 OID 335563)
-- Name: extarchivo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.extarchivo (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    fecha_aceptacion date,
    datos character varying(255),
    extraccion date,
    fecha_grabacion date,
    fecha_entrega date,
    s_espacio_de_nombres character varying(255) NOT NULL,
    s_local_id character varying(255) NOT NULL,
    col_fuenteadminstrtiva_ext_archivo_id bigint,
    col_fuenteespacial_ext_archivo_id bigint
);


ALTER TABLE interlis_ili2db3_ladm.extarchivo OWNER TO postgres;

--
-- TOC entry 12690 (class 0 OID 0)
-- Dependencies: 2028
-- Name: TABLE extarchivo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.extarchivo IS 'Referencia a clase externa desde donde se gestiona el repositorio de archivos.
@iliname LADM_COL_V1_1.LADM_Nucleo.ExtArchivo';


--
-- TOC entry 12691 (class 0 OID 0)
-- Dependencies: 2028
-- Name: COLUMN extarchivo.fecha_aceptacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extarchivo.fecha_aceptacion IS 'Fecha en la que ha sido aceptado el documento.
@iliname Fecha_Aceptacion';


--
-- TOC entry 12692 (class 0 OID 0)
-- Dependencies: 2028
-- Name: COLUMN extarchivo.datos; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extarchivo.datos IS 'Datos que contiene el documento.
@iliname Datos';


--
-- TOC entry 12693 (class 0 OID 0)
-- Dependencies: 2028
-- Name: COLUMN extarchivo.extraccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extarchivo.extraccion IS 'Última fecha de extracción del documento.
@iliname Extraccion';


--
-- TOC entry 12694 (class 0 OID 0)
-- Dependencies: 2028
-- Name: COLUMN extarchivo.fecha_grabacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extarchivo.fecha_grabacion IS 'Fecha en la que el documento es aceptado en el sistema.
@iliname Fecha_Grabacion';


--
-- TOC entry 12695 (class 0 OID 0)
-- Dependencies: 2028
-- Name: COLUMN extarchivo.fecha_entrega; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extarchivo.fecha_entrega IS 'Fecha en la que fue entregado el documento.
@iliname Fecha_Entrega';


--
-- TOC entry 12696 (class 0 OID 0)
-- Dependencies: 2028
-- Name: COLUMN extarchivo.s_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extarchivo.s_espacio_de_nombres IS 'Definición del identificador único global del documento.
@iliname s_Espacio_De_Nombres';


--
-- TOC entry 12697 (class 0 OID 0)
-- Dependencies: 2028
-- Name: COLUMN extarchivo.s_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extarchivo.s_local_id IS 'Identificador local del documento.
@iliname s_Local_Id';


--
-- TOC entry 12698 (class 0 OID 0)
-- Dependencies: 2028
-- Name: COLUMN extarchivo.col_fuenteadminstrtiva_ext_archivo_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extarchivo.col_fuenteadminstrtiva_ext_archivo_id IS 'Identificador del archivo fuente controlado por una clase externa.
@iliname LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID';


--
-- TOC entry 12699 (class 0 OID 0)
-- Dependencies: 2028
-- Name: COLUMN extarchivo.col_fuenteespacial_ext_archivo_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extarchivo.col_fuenteespacial_ext_archivo_id IS 'Identificador del archivo fuente controlado por una clase externa.
@iliname LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID';


--
-- TOC entry 2029 (class 1259 OID 335570)
-- Name: extdireccion; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.extdireccion (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    nombre_area_direccion character varying(255),
    nombre_edificio character varying(255),
    numero_edificio character varying(255),
    ciudad character varying(255),
    pais character varying(255),
    codigo_postal character varying(255),
    apartado_correo character varying(255),
    departamento character varying(255),
    nombre_calle character varying(255),
    extunidadedificcnfsica_ext_direccion_id bigint,
    extinteresado_ext_direccion_id bigint,
    la_unidadespacial_ext_direccion_id bigint,
    la_espacjrdcndddfccion_ext_direccion_id bigint,
    la_espacijrdcrdsrvcios_ext_direccion_id bigint,
    construccion_ext_direccion_id bigint,
    terreno_ext_direccion_id bigint,
    servidumbrepaso_ext_direccion_id bigint,
    unidadconstruccion_ext_direccion_id bigint,
    coordenada_direccion public.geometry(Point,3116)
);


ALTER TABLE interlis_ili2db3_ladm.extdireccion OWNER TO postgres;

--
-- TOC entry 12700 (class 0 OID 0)
-- Dependencies: 2029
-- Name: TABLE extdireccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.extdireccion IS 'Referencia a una clase externa para gestionar direcciones.
@iliname LADM_COL_V1_1.LADM_Nucleo.ExtDireccion';


--
-- TOC entry 12701 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.nombre_area_direccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.nombre_area_direccion IS 'Nombre del área en la que se encuentra la dirección.
@iliname Nombre_Area_Direccion';


--
-- TOC entry 12702 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.nombre_edificio; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.nombre_edificio IS 'Nombre del edificio.
@iliname Nombre_Edificio';


--
-- TOC entry 12703 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.numero_edificio; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.numero_edificio IS 'Número de edificio.
@iliname Numero_Edificio';


--
-- TOC entry 12704 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.ciudad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.ciudad IS '@iliname Ciudad';


--
-- TOC entry 12705 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.pais; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.pais IS '@iliname Pais';


--
-- TOC entry 12706 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.codigo_postal; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.codigo_postal IS '@iliname Codigo_Postal';


--
-- TOC entry 12707 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.apartado_correo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.apartado_correo IS '@iliname Apartado_Correo';


--
-- TOC entry 12708 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.departamento; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.departamento IS '@iliname Departamento';


--
-- TOC entry 12709 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.nombre_calle; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.nombre_calle IS 'Nombre de la calle.
@iliname Nombre_Calle';


--
-- TOC entry 12710 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.extunidadedificcnfsica_ext_direccion_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.extunidadedificcnfsica_ext_direccion_id IS '@iliname LADM_COL_V1_1.LADM_Nucleo.ExtUnidadEdificacionFisica.Ext_Direccion_ID';


--
-- TOC entry 12711 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.extinteresado_ext_direccion_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.extinteresado_ext_direccion_id IS 'Identificador externo del interesado.
@iliname LADM_COL_V1_1.LADM_Nucleo.ExtInteresado.Ext_Direccion_ID';


--
-- TOC entry 12712 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.la_unidadespacial_ext_direccion_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.la_unidadespacial_ext_direccion_id IS 'Corresponde al atributo extAddressID de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID';


--
-- TOC entry 12713 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.la_espacjrdcndddfccion_ext_direccion_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.la_espacjrdcndddfccion_ext_direccion_id IS 'Corresponde al atributo extAddressID de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID';


--
-- TOC entry 12714 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.la_espacijrdcrdsrvcios_ext_direccion_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.la_espacijrdcrdsrvcios_ext_direccion_id IS 'Corresponde al atributo extAddressID de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID';


--
-- TOC entry 12715 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.construccion_ext_direccion_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.construccion_ext_direccion_id IS 'Corresponde al atributo extAddressID de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID';


--
-- TOC entry 12716 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.terreno_ext_direccion_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.terreno_ext_direccion_id IS 'Corresponde al atributo extAddressID de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID';


--
-- TOC entry 12717 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.servidumbrepaso_ext_direccion_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.servidumbrepaso_ext_direccion_id IS 'Corresponde al atributo extAddressID de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID';


--
-- TOC entry 12718 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.unidadconstruccion_ext_direccion_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.unidadconstruccion_ext_direccion_id IS 'Corresponde al atributo extAddressID de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID';


--
-- TOC entry 12719 (class 0 OID 0)
-- Dependencies: 2029
-- Name: COLUMN extdireccion.coordenada_direccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extdireccion.coordenada_direccion IS 'Par de valores georreferenciados (x,y) en la que se encuentra la dirección.
@iliname Coordenada_Direccion';


--
-- TOC entry 2030 (class 1259 OID 335577)
-- Name: extinteresado; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.extinteresado (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    nombre character varying(255),
    extredserviciosfisica_ext_interesado_administrador_id bigint,
    la_agrupacion_intrsdos_ext_pid bigint,
    col_interesado_ext_pid bigint
);


ALTER TABLE interlis_ili2db3_ladm.extinteresado OWNER TO postgres;

--
-- TOC entry 12720 (class 0 OID 0)
-- Dependencies: 2030
-- Name: TABLE extinteresado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.extinteresado IS 'Referencia a una clase externa para gestionar direcciones.
@iliname LADM_COL_V1_1.LADM_Nucleo.ExtInteresado';


--
-- TOC entry 12721 (class 0 OID 0)
-- Dependencies: 2030
-- Name: COLUMN extinteresado.nombre; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extinteresado.nombre IS '@iliname Nombre';


--
-- TOC entry 12722 (class 0 OID 0)
-- Dependencies: 2030
-- Name: COLUMN extinteresado.extredserviciosfisica_ext_interesado_administrador_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extinteresado.extredserviciosfisica_ext_interesado_administrador_id IS 'Identificador de referencia a un interesado externo que es el administrador.
@iliname LADM_COL_V1_1.LADM_Nucleo.ExtRedServiciosFisica.Ext_Interesado_Administrador_ID';


--
-- TOC entry 12723 (class 0 OID 0)
-- Dependencies: 2030
-- Name: COLUMN extinteresado.la_agrupacion_intrsdos_ext_pid; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extinteresado.la_agrupacion_intrsdos_ext_pid IS 'Identificador del interesado.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.ext_PID';


--
-- TOC entry 12724 (class 0 OID 0)
-- Dependencies: 2030
-- Name: COLUMN extinteresado.col_interesado_ext_pid; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extinteresado.col_interesado_ext_pid IS 'Identificador del interesado.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.ext_PID';


--
-- TOC entry 2031 (class 1259 OID 335581)
-- Name: extredserviciosfisica; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.extredserviciosfisica (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    orientada boolean,
    la_espacijrdcrdsrvcios_ext_id_red_fisica bigint
);


ALTER TABLE interlis_ili2db3_ladm.extredserviciosfisica OWNER TO postgres;

--
-- TOC entry 12725 (class 0 OID 0)
-- Dependencies: 2031
-- Name: TABLE extredserviciosfisica; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.extredserviciosfisica IS 'Referencia a una clase externa para gestionar las redes físicas de servicios.
@iliname LADM_COL_V1_1.LADM_Nucleo.ExtRedServiciosFisica';


--
-- TOC entry 12726 (class 0 OID 0)
-- Dependencies: 2031
-- Name: COLUMN extredserviciosfisica.orientada; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extredserviciosfisica.orientada IS 'Indica si la red de servicios tiene un gradiente o no.
@iliname Orientada';


--
-- TOC entry 12727 (class 0 OID 0)
-- Dependencies: 2031
-- Name: COLUMN extredserviciosfisica.la_espacijrdcrdsrvcios_ext_id_red_fisica; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extredserviciosfisica.la_espacijrdcrdsrvcios_ext_id_red_fisica IS 'Identificador de la red física hacia una referencia externa.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoRedServicios.ext_ID_Red_Fisica';


--
-- TOC entry 2032 (class 1259 OID 335585)
-- Name: extunidadedificacionfisica; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.extunidadedificacionfisica (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    la_espacjrdcndddfccion_ext_unidad_edificacion_fisic_id bigint,
    construccion_ext_unidad_edificacion_fisica_id bigint,
    unidadconstruccion_ext_unidad_edificacion_fisica_id bigint
);


ALTER TABLE interlis_ili2db3_ladm.extunidadedificacionfisica OWNER TO postgres;

--
-- TOC entry 12728 (class 0 OID 0)
-- Dependencies: 2032
-- Name: TABLE extunidadedificacionfisica; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.extunidadedificacionfisica IS 'Control externo de la unidad de edificación física.
@iliname LADM_COL_V1_1.LADM_Nucleo.ExtUnidadEdificacionFisica';


--
-- TOC entry 12729 (class 0 OID 0)
-- Dependencies: 2032
-- Name: COLUMN extunidadedificacionfisica.la_espacjrdcndddfccion_ext_unidad_edificacion_fisic_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extunidadedificacionfisica.la_espacjrdcndddfccion_ext_unidad_edificacion_fisic_id IS 'Identificador de la unidad de edificación.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion.Ext_Unidad_Edificacion_Fisica_ID';


--
-- TOC entry 12730 (class 0 OID 0)
-- Dependencies: 2032
-- Name: COLUMN extunidadedificacionfisica.construccion_ext_unidad_edificacion_fisica_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extunidadedificacionfisica.construccion_ext_unidad_edificacion_fisica_id IS 'Identificador de la unidad de edificación.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion.Ext_Unidad_Edificacion_Fisica_ID';


--
-- TOC entry 12731 (class 0 OID 0)
-- Dependencies: 2032
-- Name: COLUMN extunidadedificacionfisica.unidadconstruccion_ext_unidad_edificacion_fisica_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.extunidadedificacionfisica.unidadconstruccion_ext_unidad_edificacion_fisica_id IS 'Identificador de la unidad de edificación.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion.Ext_Unidad_Edificacion_Fisica_ID';


--
-- TOC entry 2033 (class 1259 OID 335589)
-- Name: fraccion; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.fraccion (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    denominador integer NOT NULL,
    numerador integer NOT NULL,
    miembros_participacion bigint,
    col_derecho_compartido bigint,
    col_restriccion_compartido bigint,
    predio_copropiedad_coeficiente bigint,
    col_responsabilidad_compartido bigint,
    col_hipoteca_compartido bigint,
    CONSTRAINT fraccion_denominador_check CHECK (((denominador >= 0) AND (denominador <= 999999999))),
    CONSTRAINT fraccion_numerador_check CHECK (((numerador >= 0) AND (numerador <= 999999999)))
);


ALTER TABLE interlis_ili2db3_ladm.fraccion OWNER TO postgres;

--
-- TOC entry 12732 (class 0 OID 0)
-- Dependencies: 2033
-- Name: TABLE fraccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.fraccion IS 'Estructura para la definición de un tipo de dato personalizado que permite indicar una fracción o quebrado cona serie específica de condiciones.
@iliname LADM_COL_V1_1.LADM_Nucleo.Fraccion';


--
-- TOC entry 12733 (class 0 OID 0)
-- Dependencies: 2033
-- Name: COLUMN fraccion.denominador; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.fraccion.denominador IS 'Parte inferior de la fracción. Debe ser mayor que 0. Debe ser mayor que el numerador.
@iliname Denominador';


--
-- TOC entry 12734 (class 0 OID 0)
-- Dependencies: 2033
-- Name: COLUMN fraccion.numerador; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.fraccion.numerador IS 'Parte superior de la fracción. Debe ser mayor que 0. Debe sder menor que el denominador.
@iliname Numerador';


--
-- TOC entry 12735 (class 0 OID 0)
-- Dependencies: 2033
-- Name: COLUMN fraccion.miembros_participacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.fraccion.miembros_participacion IS '@iliname LADM_COL_V1_1.LADM_Nucleo.miembros.participacion';


--
-- TOC entry 12736 (class 0 OID 0)
-- Dependencies: 2033
-- Name: COLUMN fraccion.col_derecho_compartido; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.fraccion.col_derecho_compartido IS 'Participación, en modo de fracción, en la subclase LA_Derecho, LA_Responsabilidad o LA_Restriccion.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Compartido';


--
-- TOC entry 12737 (class 0 OID 0)
-- Dependencies: 2033
-- Name: COLUMN fraccion.col_restriccion_compartido; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.fraccion.col_restriccion_compartido IS 'Participación, en modo de fracción, en la subclase LA_Derecho, LA_Responsabilidad o LA_Restriccion.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Compartido';


--
-- TOC entry 12738 (class 0 OID 0)
-- Dependencies: 2033
-- Name: COLUMN fraccion.predio_copropiedad_coeficiente; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.fraccion.predio_copropiedad_coeficiente IS '@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.predio_copropiedad.coeficiente';


--
-- TOC entry 12739 (class 0 OID 0)
-- Dependencies: 2033
-- Name: COLUMN fraccion.col_responsabilidad_compartido; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.fraccion.col_responsabilidad_compartido IS 'Participación, en modo de fracción, en la subclase LA_Derecho, LA_Responsabilidad o LA_Restriccion.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Compartido';


--
-- TOC entry 12740 (class 0 OID 0)
-- Dependencies: 2033
-- Name: COLUMN fraccion.col_hipoteca_compartido; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.fraccion.col_hipoteca_compartido IS 'Participación, en modo de fracción, en la subclase LA_Derecho, LA_Responsabilidad o LA_Restriccion.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Compartido';


--
-- TOC entry 2034 (class 1259 OID 335595)
-- Name: gm_multisurface2d; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.gm_multisurface2d (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint
);


ALTER TABLE interlis_ili2db3_ladm.gm_multisurface2d OWNER TO postgres;

--
-- TOC entry 12741 (class 0 OID 0)
-- Dependencies: 2034
-- Name: TABLE gm_multisurface2d; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.gm_multisurface2d IS '@iliname ISO19107_V1_MAGNABOG.GM_MultiSurface2D';


--
-- TOC entry 2035 (class 1259 OID 335599)
-- Name: gm_multisurface3d; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.gm_multisurface3d (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint
);


ALTER TABLE interlis_ili2db3_ladm.gm_multisurface3d OWNER TO postgres;

--
-- TOC entry 12742 (class 0 OID 0)
-- Dependencies: 2035
-- Name: TABLE gm_multisurface3d; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.gm_multisurface3d IS '@iliname ISO19107_V1_MAGNABOG.GM_MultiSurface3D';


--
-- TOC entry 2036 (class 1259 OID 335603)
-- Name: gm_surface2dlistvalue; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.gm_surface2dlistvalue (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    gm_multisurface2d_geometry bigint,
    avalue public.geometry(Polygon,3116)
);


ALTER TABLE interlis_ili2db3_ladm.gm_surface2dlistvalue OWNER TO postgres;

--
-- TOC entry 12743 (class 0 OID 0)
-- Dependencies: 2036
-- Name: TABLE gm_surface2dlistvalue; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.gm_surface2dlistvalue IS '@iliname ISO19107_V1_MAGNABOG.GM_Surface2DListValue';


--
-- TOC entry 12744 (class 0 OID 0)
-- Dependencies: 2036
-- Name: COLUMN gm_surface2dlistvalue.gm_multisurface2d_geometry; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.gm_surface2dlistvalue.gm_multisurface2d_geometry IS '@iliname ISO19107_V1_MAGNABOG.GM_MultiSurface2D.geometry';


--
-- TOC entry 12745 (class 0 OID 0)
-- Dependencies: 2036
-- Name: COLUMN gm_surface2dlistvalue.avalue; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.gm_surface2dlistvalue.avalue IS '@iliname value';


--
-- TOC entry 2037 (class 1259 OID 335610)
-- Name: gm_surface3dlistvalue; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.gm_surface3dlistvalue (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    gm_multisurface3d_geometry bigint,
    avalue public.geometry(PolygonZ,3116)
);


ALTER TABLE interlis_ili2db3_ladm.gm_surface3dlistvalue OWNER TO postgres;

--
-- TOC entry 12746 (class 0 OID 0)
-- Dependencies: 2037
-- Name: TABLE gm_surface3dlistvalue; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.gm_surface3dlistvalue IS '@iliname ISO19107_V1_MAGNABOG.GM_Surface3DListValue';


--
-- TOC entry 12747 (class 0 OID 0)
-- Dependencies: 2037
-- Name: COLUMN gm_surface3dlistvalue.gm_multisurface3d_geometry; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.gm_surface3dlistvalue.gm_multisurface3d_geometry IS '@iliname ISO19107_V1_MAGNABOG.GM_MultiSurface3D.geometry';


--
-- TOC entry 12748 (class 0 OID 0)
-- Dependencies: 2037
-- Name: COLUMN gm_surface3dlistvalue.avalue; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.gm_surface3dlistvalue.avalue IS '@iliname value';


--
-- TOC entry 2038 (class 1259 OID 335617)
-- Name: hipotecaderecho; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.hipotecaderecho (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    hipoteca bigint NOT NULL,
    derecho bigint NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.hipotecaderecho OWNER TO postgres;

--
-- TOC entry 12749 (class 0 OID 0)
-- Dependencies: 2038
-- Name: TABLE hipotecaderecho; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.hipotecaderecho IS '@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.hipotecaDerecho';


--
-- TOC entry 2039 (class 1259 OID 335621)
-- Name: imagen; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.imagen (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    uri character varying(255),
    extinteresado_huella_dactilar bigint,
    extinteresado_fotografia bigint,
    extinteresado_firma bigint
);


ALTER TABLE interlis_ili2db3_ladm.imagen OWNER TO postgres;

--
-- TOC entry 12750 (class 0 OID 0)
-- Dependencies: 2039
-- Name: TABLE imagen; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.imagen IS 'Referencia a una imagen mediante su url.
@iliname LADM_COL_V1_1.LADM_Nucleo.Imagen';


--
-- TOC entry 12751 (class 0 OID 0)
-- Dependencies: 2039
-- Name: COLUMN imagen.uri; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.imagen.uri IS 'url de la imagen.';


--
-- TOC entry 12752 (class 0 OID 0)
-- Dependencies: 2039
-- Name: COLUMN imagen.extinteresado_huella_dactilar; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.imagen.extinteresado_huella_dactilar IS '@iliname LADM_COL_V1_1.LADM_Nucleo.ExtInteresado.Huella_Dactilar';


--
-- TOC entry 12753 (class 0 OID 0)
-- Dependencies: 2039
-- Name: COLUMN imagen.extinteresado_fotografia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.imagen.extinteresado_fotografia IS '@iliname LADM_COL_V1_1.LADM_Nucleo.ExtInteresado.Fotografia';


--
-- TOC entry 12754 (class 0 OID 0)
-- Dependencies: 2039
-- Name: COLUMN imagen.extinteresado_firma; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.imagen.extinteresado_firma IS '@iliname LADM_COL_V1_1.LADM_Nucleo.ExtInteresado.Firma';


--
-- TOC entry 2040 (class 1259 OID 335625)
-- Name: interesado_contacto; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.interesado_contacto (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    telefono1 character varying(20),
    telefono2 character varying(20),
    domicilio_notificacion character varying(500),
    correo_electronico character varying(100),
    origen_datos character varying(255),
    interesado bigint NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.interesado_contacto OWNER TO postgres;

--
-- TOC entry 12755 (class 0 OID 0)
-- Dependencies: 2040
-- Name: TABLE interesado_contacto; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.interesado_contacto IS '@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Interesado_Contacto';


--
-- TOC entry 12756 (class 0 OID 0)
-- Dependencies: 2040
-- Name: COLUMN interesado_contacto.telefono1; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.interesado_contacto.telefono1 IS '@iliname Telefono1';


--
-- TOC entry 12757 (class 0 OID 0)
-- Dependencies: 2040
-- Name: COLUMN interesado_contacto.telefono2; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.interesado_contacto.telefono2 IS '@iliname Telefono2';


--
-- TOC entry 12758 (class 0 OID 0)
-- Dependencies: 2040
-- Name: COLUMN interesado_contacto.domicilio_notificacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.interesado_contacto.domicilio_notificacion IS '@iliname Domicilio_Notificacion';


--
-- TOC entry 12759 (class 0 OID 0)
-- Dependencies: 2040
-- Name: COLUMN interesado_contacto.correo_electronico; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.interesado_contacto.correo_electronico IS '@iliname Correo_Electronico';


--
-- TOC entry 12760 (class 0 OID 0)
-- Dependencies: 2040
-- Name: COLUMN interesado_contacto.origen_datos; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.interesado_contacto.origen_datos IS '@iliname Origen_Datos';


--
-- TOC entry 2041 (class 1259 OID 335632)
-- Name: iso19125_tipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.iso19125_tipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.iso19125_tipo OWNER TO postgres;

--
-- TOC entry 2042 (class 1259 OID 335638)
-- Name: la_agrupacion_interesados; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_agrupacion_interesados (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ai_tipo character varying(255) NOT NULL,
    nombre character varying(255),
    tipo character varying(255) NOT NULL,
    p_espacio_de_nombres character varying(255) NOT NULL,
    p_local_id character varying(255) NOT NULL,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone
);


ALTER TABLE interlis_ili2db3_ladm.la_agrupacion_interesados OWNER TO postgres;

--
-- TOC entry 12761 (class 0 OID 0)
-- Dependencies: 2042
-- Name: TABLE la_agrupacion_interesados; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_agrupacion_interesados IS 'Registra interesados que representan a grupos de personas. Se registra el grupo en si, independientemete de las personas por separado. Es lo que ocurreo, por ejemplo, con un grupo étnico.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Agrupacion_Interesados';


--
-- TOC entry 12762 (class 0 OID 0)
-- Dependencies: 2042
-- Name: COLUMN la_agrupacion_interesados.ai_tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacion_interesados.ai_tipo IS 'Indica el tipo de agrupación del que se trata.
@iliname ai_Tipo';


--
-- TOC entry 12763 (class 0 OID 0)
-- Dependencies: 2042
-- Name: COLUMN la_agrupacion_interesados.nombre; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacion_interesados.nombre IS 'Nombre del interesado.
@iliname Nombre';


--
-- TOC entry 12764 (class 0 OID 0)
-- Dependencies: 2042
-- Name: COLUMN la_agrupacion_interesados.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacion_interesados.tipo IS 'Tipo de persona del que se trata.
@iliname Tipo';


--
-- TOC entry 12765 (class 0 OID 0)
-- Dependencies: 2042
-- Name: COLUMN la_agrupacion_interesados.p_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacion_interesados.p_espacio_de_nombres IS 'Identificador único global.
@iliname p_Espacio_De_Nombres';


--
-- TOC entry 12766 (class 0 OID 0)
-- Dependencies: 2042
-- Name: COLUMN la_agrupacion_interesados.p_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacion_interesados.p_local_id IS 'Identificador único local.
@iliname p_Local_Id';


--
-- TOC entry 12767 (class 0 OID 0)
-- Dependencies: 2042
-- Name: COLUMN la_agrupacion_interesados.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacion_interesados.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12768 (class 0 OID 0)
-- Dependencies: 2042
-- Name: COLUMN la_agrupacion_interesados.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacion_interesados.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 2043 (class 1259 OID 335645)
-- Name: la_agrupacion_interesados_tipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_agrupacion_interesados_tipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_agrupacion_interesados_tipo OWNER TO postgres;

--
-- TOC entry 2044 (class 1259 OID 335651)
-- Name: la_agrupacionunidadesespaciales; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_agrupacionunidadesespaciales (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    nivel_jerarquico integer NOT NULL,
    etiqueta character varying(255),
    nombre character varying(255),
    sug_espacio_de_nombres character varying(255) NOT NULL,
    sug_local_id character varying(255) NOT NULL,
    aset bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    punto_referencia public.geometry(Point,3116),
    CONSTRAINT la_agrupacionuniddsspcles_nivel_jerarquico_check CHECK (((nivel_jerarquico >= 0) AND (nivel_jerarquico <= 999999999)))
);


ALTER TABLE interlis_ili2db3_ladm.la_agrupacionunidadesespaciales OWNER TO postgres;

--
-- TOC entry 12769 (class 0 OID 0)
-- Dependencies: 2044
-- Name: TABLE la_agrupacionunidadesespaciales; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_agrupacionunidadesespaciales IS 'Agrupa unidades espaciales, es decir, representaciones geográficas de las unidades administrativas básicas (clase LA_BAUnit) para representar otras unidades espaciales que se forman en base a estas, como puede ser el caso de los polígonos catastrales.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_AgrupacionUnidadesEspaciales';


--
-- TOC entry 12770 (class 0 OID 0)
-- Dependencies: 2044
-- Name: COLUMN la_agrupacionunidadesespaciales.nivel_jerarquico; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacionunidadesespaciales.nivel_jerarquico IS 'Nivel jerárquico de la agrupación, dentro del anidamiento de diferentes agrupaciones.
@iliname Nivel_Jerarquico';


--
-- TOC entry 12771 (class 0 OID 0)
-- Dependencies: 2044
-- Name: COLUMN la_agrupacionunidadesespaciales.etiqueta; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacionunidadesespaciales.etiqueta IS 'Definición de la agrupación.
@iliname Etiqueta';


--
-- TOC entry 12772 (class 0 OID 0)
-- Dependencies: 2044
-- Name: COLUMN la_agrupacionunidadesespaciales.nombre; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacionunidadesespaciales.nombre IS 'Nombre que recibe la agrupación.
@iliname Nombre';


--
-- TOC entry 12773 (class 0 OID 0)
-- Dependencies: 2044
-- Name: COLUMN la_agrupacionunidadesespaciales.sug_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacionunidadesespaciales.sug_espacio_de_nombres IS 'Identificar único global de la agrupación.
@iliname sug_Espacio_De_Nombres';


--
-- TOC entry 12774 (class 0 OID 0)
-- Dependencies: 2044
-- Name: COLUMN la_agrupacionunidadesespaciales.sug_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacionunidadesespaciales.sug_local_id IS 'Identificador único local de la agrupación.
@iliname sug_Local_Id';


--
-- TOC entry 12775 (class 0 OID 0)
-- Dependencies: 2044
-- Name: COLUMN la_agrupacionunidadesespaciales.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacionunidadesespaciales.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12776 (class 0 OID 0)
-- Dependencies: 2044
-- Name: COLUMN la_agrupacionunidadesespaciales.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacionunidadesespaciales.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 12777 (class 0 OID 0)
-- Dependencies: 2044
-- Name: COLUMN la_agrupacionunidadesespaciales.punto_referencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_agrupacionunidadesespaciales.punto_referencia IS 'Punto de referencia de toda la agrupación, a modo de centro de masas.
@iliname Punto_Referencia';


--
-- TOC entry 2045 (class 1259 OID 335659)
-- Name: la_baunit; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_baunit (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    nombre character varying(255),
    tipo character varying(255) NOT NULL,
    u_espacio_de_nombres character varying(255) NOT NULL,
    u_local_id character varying(255) NOT NULL,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone
);


ALTER TABLE interlis_ili2db3_ladm.la_baunit OWNER TO postgres;

--
-- TOC entry 12778 (class 0 OID 0)
-- Dependencies: 2045
-- Name: TABLE la_baunit; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_baunit IS 'De forma genérica, representa el objeto territorial legal (Catastro 2014) que se gestiona en el modelo, en este caso, la parcela catastral o predio. Es independiente del conocimiento de su realidad espacial y se centra en su existencia conocida y reconocida.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit';


--
-- TOC entry 12779 (class 0 OID 0)
-- Dependencies: 2045
-- Name: COLUMN la_baunit.nombre; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_baunit.nombre IS 'Nombre que recibe la unidad administrativa básica, en muchos casos toponímico, especialmente en terrenos rústicos.
@iliname Nombre';


--
-- TOC entry 12780 (class 0 OID 0)
-- Dependencies: 2045
-- Name: COLUMN la_baunit.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_baunit.tipo IS 'Tipo de derecho que la reconoce.
@iliname Tipo';


--
-- TOC entry 12781 (class 0 OID 0)
-- Dependencies: 2045
-- Name: COLUMN la_baunit.u_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_baunit.u_espacio_de_nombres IS 'Identificador único global.
@iliname u_Espacio_De_Nombres';


--
-- TOC entry 12782 (class 0 OID 0)
-- Dependencies: 2045
-- Name: COLUMN la_baunit.u_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_baunit.u_local_id IS 'Identificador único local.
@iliname u_Local_Id';


--
-- TOC entry 12783 (class 0 OID 0)
-- Dependencies: 2045
-- Name: COLUMN la_baunit.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_baunit.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12784 (class 0 OID 0)
-- Dependencies: 2045
-- Name: COLUMN la_baunit.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_baunit.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 2046 (class 1259 OID 335666)
-- Name: la_baunittipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_baunittipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_baunittipo OWNER TO postgres;

--
-- TOC entry 2047 (class 1259 OID 335672)
-- Name: la_cadenacaraslimite; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_cadenacaraslimite (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    localizacion_textual character varying(255),
    ccl_espacio_de_nombres character varying(255) NOT NULL,
    ccl_local_id character varying(255) NOT NULL,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    geometria public.geometry(LineString,3116)
);


ALTER TABLE interlis_ili2db3_ladm.la_cadenacaraslimite OWNER TO postgres;

--
-- TOC entry 12785 (class 0 OID 0)
-- Dependencies: 2047
-- Name: TABLE la_cadenacaraslimite; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_cadenacaraslimite IS 'Traducción al español de la clase LA_BoundaryFaceString de LADM. Define los linderos y a su vez puede estar definida por una descrición textual o por dos o más puntos. Puede estar asociada a una fuente espacial o más.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite';


--
-- TOC entry 12786 (class 0 OID 0)
-- Dependencies: 2047
-- Name: COLUMN la_cadenacaraslimite.localizacion_textual; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_cadenacaraslimite.localizacion_textual IS 'Descripción de la localización, cuando esta se basa en texto.
@iliname Localizacion_Textual';


--
-- TOC entry 12787 (class 0 OID 0)
-- Dependencies: 2047
-- Name: COLUMN la_cadenacaraslimite.ccl_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_cadenacaraslimite.ccl_espacio_de_nombres IS 'Identificador único global de la cadena de caras lindero.
@iliname ccl_Espacio_De_Nombres';


--
-- TOC entry 12788 (class 0 OID 0)
-- Dependencies: 2047
-- Name: COLUMN la_cadenacaraslimite.ccl_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_cadenacaraslimite.ccl_local_id IS 'Identificador local de la cadena de caras lindero.
@iliname ccl_Local_Id';


--
-- TOC entry 12789 (class 0 OID 0)
-- Dependencies: 2047
-- Name: COLUMN la_cadenacaraslimite.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_cadenacaraslimite.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12790 (class 0 OID 0)
-- Dependencies: 2047
-- Name: COLUMN la_cadenacaraslimite.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_cadenacaraslimite.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 12791 (class 0 OID 0)
-- Dependencies: 2047
-- Name: COLUMN la_cadenacaraslimite.geometria; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_cadenacaraslimite.geometria IS 'Geometría lineal que define el lindero. Puede estar asociada a geometrías de tipo punto que definen sus vértices o ser una entidad lineal independiente.
@iliname Geometria';


--
-- TOC entry 2048 (class 1259 OID 335679)
-- Name: la_caraslindero; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_caraslindero (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    localizacion_textual character varying(255),
    cl_espacio_de_nombres character varying(255) NOT NULL,
    cl_local_id character varying(255) NOT NULL,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    geometria public.geometry(MultiPolygonZ,3116)
);


ALTER TABLE interlis_ili2db3_ladm.la_caraslindero OWNER TO postgres;

--
-- TOC entry 12792 (class 0 OID 0)
-- Dependencies: 2048
-- Name: TABLE la_caraslindero; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_caraslindero IS 'Traducción de la clase LA_BoundaryFace de LADM. De forma similar a LA_CadenaCarasLindero, representa los límites, pero en este caso permite representación 3D.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_CarasLindero';


--
-- TOC entry 12793 (class 0 OID 0)
-- Dependencies: 2048
-- Name: COLUMN la_caraslindero.localizacion_textual; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_caraslindero.localizacion_textual IS 'Cuando la localización del límte está dada por una descripción textual, aquí se recoge esta.
@iliname Localizacion_Textual';


--
-- TOC entry 12794 (class 0 OID 0)
-- Dependencies: 2048
-- Name: COLUMN la_caraslindero.cl_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_caraslindero.cl_espacio_de_nombres IS 'Identificador único global.
@iliname cl_Espacio_De_Nombres';


--
-- TOC entry 12795 (class 0 OID 0)
-- Dependencies: 2048
-- Name: COLUMN la_caraslindero.cl_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_caraslindero.cl_local_id IS 'Identificador único local.
@iliname cl_Local_Id';


--
-- TOC entry 12796 (class 0 OID 0)
-- Dependencies: 2048
-- Name: COLUMN la_caraslindero.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_caraslindero.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12797 (class 0 OID 0)
-- Dependencies: 2048
-- Name: COLUMN la_caraslindero.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_caraslindero.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 12798 (class 0 OID 0)
-- Dependencies: 2048
-- Name: COLUMN la_caraslindero.geometria; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_caraslindero.geometria IS 'Geometría en 3D del límite o lindero, asociada a putos o a descripciones textuales.
@iliname Geometria';


--
-- TOC entry 2049 (class 1259 OID 335686)
-- Name: la_contenidoniveltipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_contenidoniveltipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_contenidoniveltipo OWNER TO postgres;

--
-- TOC entry 2050 (class 1259 OID 335692)
-- Name: la_derechotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_derechotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_derechotipo OWNER TO postgres;

--
-- TOC entry 2051 (class 1259 OID 335698)
-- Name: la_dimensiontipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_dimensiontipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_dimensiontipo OWNER TO postgres;

--
-- TOC entry 2052 (class 1259 OID 335704)
-- Name: la_espaciojuridicoredservicios; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_espaciojuridicoredservicios (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    estado character varying(255),
    tipo character varying(255),
    dimension character varying(255),
    etiqueta character varying(255),
    relacion_superficie character varying(255),
    su_espacio_de_nombres character varying(255) NOT NULL,
    su_local_id character varying(255) NOT NULL,
    nivel bigint,
    uej2_la_unidadespacial bigint,
    uej2_la_espaciojuridicoredservicios bigint,
    uej2_la_espaciojuridicounidadedificacion bigint,
    uej2_servidumbrepaso bigint,
    uej2_terreno bigint,
    uej2_construccion bigint,
    uej2_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    punto_referencia public.geometry(Point,3116),
    poligono_creado public.geometry(MultiPolygon,3116)
);


ALTER TABLE interlis_ili2db3_ladm.la_espaciojuridicoredservicios OWNER TO postgres;

--
-- TOC entry 12799 (class 0 OID 0)
-- Dependencies: 2052
-- Name: TABLE la_espaciojuridicoredservicios; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_espaciojuridicoredservicios IS 'Traducción al español de la clase LA_LegalSpaceUtilityNetwork. Representa un tipo de unidad espacial (LA_UNidadEspacial) cuyas instancias son las redes de servicios.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoRedServicios';


--
-- TOC entry 12800 (class 0 OID 0)
-- Dependencies: 2052
-- Name: COLUMN la_espaciojuridicoredservicios.estado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicoredservicios.estado IS 'Estado de operatividad de la red.
@iliname Estado';


--
-- TOC entry 12801 (class 0 OID 0)
-- Dependencies: 2052
-- Name: COLUMN la_espaciojuridicoredservicios.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicoredservicios.tipo IS 'Tipo de servicio que presta.
@iliname Tipo';


--
-- TOC entry 12802 (class 0 OID 0)
-- Dependencies: 2052
-- Name: COLUMN la_espaciojuridicoredservicios.dimension; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicoredservicios.dimension IS '@iliname Dimension';


--
-- TOC entry 12803 (class 0 OID 0)
-- Dependencies: 2052
-- Name: COLUMN la_espaciojuridicoredservicios.etiqueta; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicoredservicios.etiqueta IS 'Corresponde al atributo label de la clase en LADM.
@iliname Etiqueta';


--
-- TOC entry 12804 (class 0 OID 0)
-- Dependencies: 2052
-- Name: COLUMN la_espaciojuridicoredservicios.relacion_superficie; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicoredservicios.relacion_superficie IS 'Corresponde al atributo surfaceRelation de la clase en LADM.
@iliname Relacion_Superficie';


--
-- TOC entry 12805 (class 0 OID 0)
-- Dependencies: 2052
-- Name: COLUMN la_espaciojuridicoredservicios.su_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicoredservicios.su_espacio_de_nombres IS 'Identificador único global. Corresponde al atributo suID de la clase en LADM.
@iliname su_Espacio_De_Nombres';


--
-- TOC entry 12806 (class 0 OID 0)
-- Dependencies: 2052
-- Name: COLUMN la_espaciojuridicoredservicios.su_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicoredservicios.su_local_id IS 'Identificador único local.
@iliname su_Local_Id';


--
-- TOC entry 12807 (class 0 OID 0)
-- Dependencies: 2052
-- Name: COLUMN la_espaciojuridicoredservicios.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicoredservicios.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12808 (class 0 OID 0)
-- Dependencies: 2052
-- Name: COLUMN la_espaciojuridicoredservicios.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicoredservicios.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 12809 (class 0 OID 0)
-- Dependencies: 2052
-- Name: COLUMN la_espaciojuridicoredservicios.punto_referencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicoredservicios.punto_referencia IS 'Corresponde al atributo referencePoint de la clase en LADM.
@iliname Punto_Referencia';


--
-- TOC entry 12810 (class 0 OID 0)
-- Dependencies: 2052
-- Name: COLUMN la_espaciojuridicoredservicios.poligono_creado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicoredservicios.poligono_creado IS 'Materializacion del metodo createArea(). Almacena de forma permanente la geometría de tipo poligonal.';


--
-- TOC entry 2053 (class 1259 OID 335711)
-- Name: la_espaciojuridicounidadedificacion; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    tipo character varying(255),
    dimension character varying(255),
    etiqueta character varying(255),
    relacion_superficie character varying(255),
    su_espacio_de_nombres character varying(255) NOT NULL,
    su_local_id character varying(255) NOT NULL,
    nivel bigint,
    uej2_la_unidadespacial bigint,
    uej2_la_espaciojuridicoredservicios bigint,
    uej2_la_espaciojuridicounidadedificacion bigint,
    uej2_servidumbrepaso bigint,
    uej2_terreno bigint,
    uej2_construccion bigint,
    uej2_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    punto_referencia public.geometry(Point,3116),
    poligono_creado public.geometry(MultiPolygon,3116)
);


ALTER TABLE interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion OWNER TO postgres;

--
-- TOC entry 12811 (class 0 OID 0)
-- Dependencies: 2053
-- Name: TABLE la_espaciojuridicounidadedificacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion IS 'Traducción al español de la clase LA_LegalSpaceBuildingUnit. Sus intancias son las unidades de edificación
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion';


--
-- TOC entry 12812 (class 0 OID 0)
-- Dependencies: 2053
-- Name: COLUMN la_espaciojuridicounidadedificacion.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion.tipo IS 'Tipo de unidad de edificación de la que se trata.
@iliname Tipo';


--
-- TOC entry 12813 (class 0 OID 0)
-- Dependencies: 2053
-- Name: COLUMN la_espaciojuridicounidadedificacion.dimension; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion.dimension IS '@iliname Dimension';


--
-- TOC entry 12814 (class 0 OID 0)
-- Dependencies: 2053
-- Name: COLUMN la_espaciojuridicounidadedificacion.etiqueta; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion.etiqueta IS 'Corresponde al atributo label de la clase en LADM.
@iliname Etiqueta';


--
-- TOC entry 12815 (class 0 OID 0)
-- Dependencies: 2053
-- Name: COLUMN la_espaciojuridicounidadedificacion.relacion_superficie; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion.relacion_superficie IS 'Corresponde al atributo surfaceRelation de la clase en LADM.
@iliname Relacion_Superficie';


--
-- TOC entry 12816 (class 0 OID 0)
-- Dependencies: 2053
-- Name: COLUMN la_espaciojuridicounidadedificacion.su_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion.su_espacio_de_nombres IS 'Identificador único global. Corresponde al atributo suID de la clase en LADM.
@iliname su_Espacio_De_Nombres';


--
-- TOC entry 12817 (class 0 OID 0)
-- Dependencies: 2053
-- Name: COLUMN la_espaciojuridicounidadedificacion.su_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion.su_local_id IS 'Identificador único local.
@iliname su_Local_Id';


--
-- TOC entry 12818 (class 0 OID 0)
-- Dependencies: 2053
-- Name: COLUMN la_espaciojuridicounidadedificacion.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12819 (class 0 OID 0)
-- Dependencies: 2053
-- Name: COLUMN la_espaciojuridicounidadedificacion.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 12820 (class 0 OID 0)
-- Dependencies: 2053
-- Name: COLUMN la_espaciojuridicounidadedificacion.punto_referencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion.punto_referencia IS 'Corresponde al atributo referencePoint de la clase en LADM.
@iliname Punto_Referencia';


--
-- TOC entry 12821 (class 0 OID 0)
-- Dependencies: 2053
-- Name: COLUMN la_espaciojuridicounidadedificacion.poligono_creado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion.poligono_creado IS 'Materializacion del metodo createArea(). Almacena de forma permanente la geometría de tipo poligonal.';


--
-- TOC entry 2054 (class 1259 OID 335718)
-- Name: la_estadodisponibilidadtipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_estadodisponibilidadtipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_estadodisponibilidadtipo OWNER TO postgres;

--
-- TOC entry 2055 (class 1259 OID 335724)
-- Name: la_estadoredserviciostipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_estadoredserviciostipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_estadoredserviciostipo OWNER TO postgres;

--
-- TOC entry 2056 (class 1259 OID 335730)
-- Name: la_estructuratipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_estructuratipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_estructuratipo OWNER TO postgres;

--
-- TOC entry 2057 (class 1259 OID 335736)
-- Name: la_fuenteadministrativatipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_fuenteadministrativatipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_fuenteadministrativatipo OWNER TO postgres;

--
-- TOC entry 2058 (class 1259 OID 335742)
-- Name: la_fuenteespacialtipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_fuenteespacialtipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_fuenteespacialtipo OWNER TO postgres;

--
-- TOC entry 2059 (class 1259 OID 335748)
-- Name: la_hipotecatipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_hipotecatipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_hipotecatipo OWNER TO postgres;

--
-- TOC entry 2060 (class 1259 OID 335754)
-- Name: la_interesadotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_interesadotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_interesadotipo OWNER TO postgres;

--
-- TOC entry 2061 (class 1259 OID 335760)
-- Name: la_interpolaciontipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_interpolaciontipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_interpolaciontipo OWNER TO postgres;

--
-- TOC entry 2062 (class 1259 OID 335766)
-- Name: la_monumentaciontipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_monumentaciontipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_monumentaciontipo OWNER TO postgres;

--
-- TOC entry 2063 (class 1259 OID 335772)
-- Name: la_nivel; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_nivel (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    nombre character varying(255),
    registro_tipo character varying(255),
    estructura character varying(255),
    tipo character varying(255),
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone
);


ALTER TABLE interlis_ili2db3_ladm.la_nivel OWNER TO postgres;

--
-- TOC entry 12822 (class 0 OID 0)
-- Dependencies: 2063
-- Name: TABLE la_nivel; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_nivel IS 'Traducción de la calse LA_Level de LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Nivel';


--
-- TOC entry 12823 (class 0 OID 0)
-- Dependencies: 2063
-- Name: COLUMN la_nivel.nombre; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_nivel.nombre IS '@iliname Nombre';


--
-- TOC entry 12824 (class 0 OID 0)
-- Dependencies: 2063
-- Name: COLUMN la_nivel.registro_tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_nivel.registro_tipo IS '@iliname Registro_Tipo';


--
-- TOC entry 12825 (class 0 OID 0)
-- Dependencies: 2063
-- Name: COLUMN la_nivel.estructura; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_nivel.estructura IS '@iliname Estructura';


--
-- TOC entry 12826 (class 0 OID 0)
-- Dependencies: 2063
-- Name: COLUMN la_nivel.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_nivel.tipo IS '@iliname Tipo';


--
-- TOC entry 12827 (class 0 OID 0)
-- Dependencies: 2063
-- Name: COLUMN la_nivel.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_nivel.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12828 (class 0 OID 0)
-- Dependencies: 2063
-- Name: COLUMN la_nivel.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_nivel.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 2064 (class 1259 OID 335779)
-- Name: la_punto; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_punto (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    posicion_interpolacion character varying(255),
    monumentacion character varying(255),
    puntotipo character varying(255) NOT NULL,
    p_espacio_de_nombres character varying(255) NOT NULL,
    p_local_id character varying(255) NOT NULL,
    ue_la_unidadespacial bigint,
    ue_la_espaciojuridicoredservicios bigint,
    ue_la_espaciojuridicounidadedificacion bigint,
    ue_servidumbrepaso bigint,
    ue_terreno bigint,
    ue_construccion bigint,
    ue_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    localizacion_original public.geometry(Point,3116)
);


ALTER TABLE interlis_ili2db3_ladm.la_punto OWNER TO postgres;

--
-- TOC entry 12829 (class 0 OID 0)
-- Dependencies: 2064
-- Name: TABLE la_punto; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_punto IS 'Traducción al español de la clase LA_Point de LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Punto';


--
-- TOC entry 12830 (class 0 OID 0)
-- Dependencies: 2064
-- Name: COLUMN la_punto.posicion_interpolacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_punto.posicion_interpolacion IS '@iliname Posicion_Interpolacion';


--
-- TOC entry 12831 (class 0 OID 0)
-- Dependencies: 2064
-- Name: COLUMN la_punto.monumentacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_punto.monumentacion IS '@iliname Monumentacion';


--
-- TOC entry 12832 (class 0 OID 0)
-- Dependencies: 2064
-- Name: COLUMN la_punto.puntotipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_punto.puntotipo IS '@iliname PuntoTipo';


--
-- TOC entry 12833 (class 0 OID 0)
-- Dependencies: 2064
-- Name: COLUMN la_punto.p_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_punto.p_espacio_de_nombres IS '@iliname p_Espacio_De_Nombres';


--
-- TOC entry 12834 (class 0 OID 0)
-- Dependencies: 2064
-- Name: COLUMN la_punto.p_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_punto.p_local_id IS '@iliname p_Local_Id';


--
-- TOC entry 12835 (class 0 OID 0)
-- Dependencies: 2064
-- Name: COLUMN la_punto.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_punto.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12836 (class 0 OID 0)
-- Dependencies: 2064
-- Name: COLUMN la_punto.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_punto.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 12837 (class 0 OID 0)
-- Dependencies: 2064
-- Name: COLUMN la_punto.localizacion_original; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_punto.localizacion_original IS '@iliname Localizacion_Original';


--
-- TOC entry 2065 (class 1259 OID 335786)
-- Name: la_puntotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_puntotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_puntotipo OWNER TO postgres;

--
-- TOC entry 2066 (class 1259 OID 335792)
-- Name: la_redserviciostipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_redserviciostipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_redserviciostipo OWNER TO postgres;

--
-- TOC entry 2067 (class 1259 OID 335798)
-- Name: la_registrotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_registrotipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_registrotipo OWNER TO postgres;

--
-- TOC entry 2068 (class 1259 OID 335804)
-- Name: la_relacionnecesariabaunits; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_relacionnecesariabaunits (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    relacion character varying(255) NOT NULL,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone
);


ALTER TABLE interlis_ili2db3_ladm.la_relacionnecesariabaunits OWNER TO postgres;

--
-- TOC entry 12838 (class 0 OID 0)
-- Dependencies: 2068
-- Name: TABLE la_relacionnecesariabaunits; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_relacionnecesariabaunits IS 'Traducción de la clase LA_RequiredRelationshipBAUnit de LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_RelacionNecesariaBAUnits';


--
-- TOC entry 12839 (class 0 OID 0)
-- Dependencies: 2068
-- Name: COLUMN la_relacionnecesariabaunits.relacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_relacionnecesariabaunits.relacion IS '@iliname Relacion';


--
-- TOC entry 12840 (class 0 OID 0)
-- Dependencies: 2068
-- Name: COLUMN la_relacionnecesariabaunits.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_relacionnecesariabaunits.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12841 (class 0 OID 0)
-- Dependencies: 2068
-- Name: COLUMN la_relacionnecesariabaunits.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_relacionnecesariabaunits.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 2069 (class 1259 OID 335808)
-- Name: la_relacionnecesariaunidadesespaciales; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_relacionnecesariaunidadesespaciales (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    relacion character varying(255) NOT NULL,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone
);


ALTER TABLE interlis_ili2db3_ladm.la_relacionnecesariaunidadesespaciales OWNER TO postgres;

--
-- TOC entry 12842 (class 0 OID 0)
-- Dependencies: 2069
-- Name: TABLE la_relacionnecesariaunidadesespaciales; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_relacionnecesariaunidadesespaciales IS 'Traducción al español de la clase LA_RequiredRelationshipSpatialUnit de LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_RelacionNecesariaUnidadesEspaciales';


--
-- TOC entry 12843 (class 0 OID 0)
-- Dependencies: 2069
-- Name: COLUMN la_relacionnecesariaunidadesespaciales.relacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_relacionnecesariaunidadesespaciales.relacion IS '@iliname Relacion';


--
-- TOC entry 12844 (class 0 OID 0)
-- Dependencies: 2069
-- Name: COLUMN la_relacionnecesariaunidadesespaciales.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_relacionnecesariaunidadesespaciales.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12845 (class 0 OID 0)
-- Dependencies: 2069
-- Name: COLUMN la_relacionnecesariaunidadesespaciales.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_relacionnecesariaunidadesespaciales.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 2070 (class 1259 OID 335812)
-- Name: la_relacionsuperficietipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_relacionsuperficietipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_relacionsuperficietipo OWNER TO postgres;

--
-- TOC entry 2071 (class 1259 OID 335818)
-- Name: la_responsabilidadtipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_responsabilidadtipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_responsabilidadtipo OWNER TO postgres;

--
-- TOC entry 2072 (class 1259 OID 335824)
-- Name: la_restricciontipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_restricciontipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_restricciontipo OWNER TO postgres;

--
-- TOC entry 2073 (class 1259 OID 335830)
-- Name: la_tareainteresadotipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_tareainteresadotipo (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    tipo character varying(255),
    la_agrupacion_intrsdos_tarea bigint,
    col_interesado_tarea bigint
);


ALTER TABLE interlis_ili2db3_ladm.la_tareainteresadotipo OWNER TO postgres;

--
-- TOC entry 12846 (class 0 OID 0)
-- Dependencies: 2073
-- Name: TABLE la_tareainteresadotipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_tareainteresadotipo IS 'Estructura que define los diferentes tipos de interesados que pueden darse.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_TareaInteresadoTipo';


--
-- TOC entry 12847 (class 0 OID 0)
-- Dependencies: 2073
-- Name: COLUMN la_tareainteresadotipo.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_tareainteresadotipo.tipo IS '@iliname Tipo';


--
-- TOC entry 12848 (class 0 OID 0)
-- Dependencies: 2073
-- Name: COLUMN la_tareainteresadotipo.la_agrupacion_intrsdos_tarea; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_tareainteresadotipo.la_agrupacion_intrsdos_tarea IS 'Función o tarea que realiza el interesado dentro del marco de derechos, obligaciones y restricciones.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.Tarea';


--
-- TOC entry 12849 (class 0 OID 0)
-- Dependencies: 2073
-- Name: COLUMN la_tareainteresadotipo.col_interesado_tarea; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_tareainteresadotipo.col_interesado_tarea IS 'Función o tarea que realiza el interesado dentro del marco de derechos, obligaciones y restricciones.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.Tarea';


--
-- TOC entry 2074 (class 1259 OID 335834)
-- Name: la_tareainteresadotipo_tipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_tareainteresadotipo_tipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_tareainteresadotipo_tipo OWNER TO postgres;

--
-- TOC entry 2075 (class 1259 OID 335840)
-- Name: la_transformacion; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_transformacion (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    la_punto_transformacion_y_resultado bigint,
    puntocontrol_transformacion_y_resultado bigint,
    puntolindero_transformacion_y_resultado bigint,
    puntolevantamiento_transformacion_y_resultado bigint,
    localizacion_transformada public.geometry(Point,3116)
);


ALTER TABLE interlis_ili2db3_ladm.la_transformacion OWNER TO postgres;

--
-- TOC entry 12850 (class 0 OID 0)
-- Dependencies: 2075
-- Name: TABLE la_transformacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_transformacion IS 'Registro de la fórmula o procedimiento utilizado en la transformación y de su resultado.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Transformacion';


--
-- TOC entry 12851 (class 0 OID 0)
-- Dependencies: 2075
-- Name: COLUMN la_transformacion.la_punto_transformacion_y_resultado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_transformacion.la_punto_transformacion_y_resultado IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Transformacion_Y_Resultado';


--
-- TOC entry 12852 (class 0 OID 0)
-- Dependencies: 2075
-- Name: COLUMN la_transformacion.puntocontrol_transformacion_y_resultado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_transformacion.puntocontrol_transformacion_y_resultado IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Transformacion_Y_Resultado';


--
-- TOC entry 12853 (class 0 OID 0)
-- Dependencies: 2075
-- Name: COLUMN la_transformacion.puntolindero_transformacion_y_resultado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_transformacion.puntolindero_transformacion_y_resultado IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Transformacion_Y_Resultado';


--
-- TOC entry 12854 (class 0 OID 0)
-- Dependencies: 2075
-- Name: COLUMN la_transformacion.puntolevantamiento_transformacion_y_resultado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_transformacion.puntolevantamiento_transformacion_y_resultado IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Transformacion_Y_Resultado';


--
-- TOC entry 12855 (class 0 OID 0)
-- Dependencies: 2075
-- Name: COLUMN la_transformacion.localizacion_transformada; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_transformacion.localizacion_transformada IS 'Geometría una vez realizado el proceso de transformación.
@iliname Localizacion_Transformada';


--
-- TOC entry 2076 (class 1259 OID 335847)
-- Name: la_unidadedificaciontipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_unidadedificaciontipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_unidadedificaciontipo OWNER TO postgres;

--
-- TOC entry 2077 (class 1259 OID 335853)
-- Name: la_unidadespacial; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_unidadespacial (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    dimension character varying(255),
    etiqueta character varying(255),
    relacion_superficie character varying(255),
    su_espacio_de_nombres character varying(255) NOT NULL,
    su_local_id character varying(255) NOT NULL,
    nivel bigint,
    uej2_la_unidadespacial bigint,
    uej2_la_espaciojuridicoredservicios bigint,
    uej2_la_espaciojuridicounidadedificacion bigint,
    uej2_servidumbrepaso bigint,
    uej2_terreno bigint,
    uej2_construccion bigint,
    uej2_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    punto_referencia public.geometry(Point,3116),
    poligono_creado public.geometry(MultiPolygon,3116)
);


ALTER TABLE interlis_ili2db3_ladm.la_unidadespacial OWNER TO postgres;

--
-- TOC entry 12856 (class 0 OID 0)
-- Dependencies: 2077
-- Name: TABLE la_unidadespacial; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_unidadespacial IS 'Traducción al español de la clase LA_SpatialUnit de LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial';


--
-- TOC entry 12857 (class 0 OID 0)
-- Dependencies: 2077
-- Name: COLUMN la_unidadespacial.dimension; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_unidadespacial.dimension IS '@iliname Dimension';


--
-- TOC entry 12858 (class 0 OID 0)
-- Dependencies: 2077
-- Name: COLUMN la_unidadespacial.etiqueta; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_unidadespacial.etiqueta IS 'Corresponde al atributo label de la clase en LADM.
@iliname Etiqueta';


--
-- TOC entry 12859 (class 0 OID 0)
-- Dependencies: 2077
-- Name: COLUMN la_unidadespacial.relacion_superficie; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_unidadespacial.relacion_superficie IS 'Corresponde al atributo surfaceRelation de la clase en LADM.
@iliname Relacion_Superficie';


--
-- TOC entry 12860 (class 0 OID 0)
-- Dependencies: 2077
-- Name: COLUMN la_unidadespacial.su_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_unidadespacial.su_espacio_de_nombres IS 'Identificador único global. Corresponde al atributo suID de la clase en LADM.
@iliname su_Espacio_De_Nombres';


--
-- TOC entry 12861 (class 0 OID 0)
-- Dependencies: 2077
-- Name: COLUMN la_unidadespacial.su_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_unidadespacial.su_local_id IS 'Identificador único local.
@iliname su_Local_Id';


--
-- TOC entry 12862 (class 0 OID 0)
-- Dependencies: 2077
-- Name: COLUMN la_unidadespacial.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_unidadespacial.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12863 (class 0 OID 0)
-- Dependencies: 2077
-- Name: COLUMN la_unidadespacial.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_unidadespacial.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 12864 (class 0 OID 0)
-- Dependencies: 2077
-- Name: COLUMN la_unidadespacial.punto_referencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_unidadespacial.punto_referencia IS 'Corresponde al atributo referencePoint de la clase en LADM.
@iliname Punto_Referencia';


--
-- TOC entry 12865 (class 0 OID 0)
-- Dependencies: 2077
-- Name: COLUMN la_unidadespacial.poligono_creado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_unidadespacial.poligono_creado IS 'Materializacion del metodo createArea(). Almacena de forma permanente la geometría de tipo poligonal.';


--
-- TOC entry 2078 (class 1259 OID 335860)
-- Name: la_volumentipo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_volumentipo (
    itfcode integer NOT NULL,
    ilicode character varying(1024) NOT NULL,
    seq integer,
    inactive boolean NOT NULL,
    dispname character varying(250) NOT NULL,
    description character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.la_volumentipo OWNER TO postgres;

--
-- TOC entry 2079 (class 1259 OID 335866)
-- Name: la_volumenvalor; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.la_volumenvalor (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    volumen_medicion numeric(15,1) NOT NULL,
    tipo character varying(255) NOT NULL,
    la_unidadespacial_volumen bigint,
    la_espacjrdcndddfccion_volumen bigint,
    la_espacijrdcrdsrvcios_volumen bigint,
    construccion_volumen bigint,
    terreno_volumen bigint,
    servidumbrepaso_volumen bigint,
    unidadconstruccion_volumen bigint,
    CONSTRAINT la_volumenvalor_volumen_medicion_check CHECK (((volumen_medicion >= 0.0) AND (volumen_medicion <= 99999999999999.9)))
);


ALTER TABLE interlis_ili2db3_ladm.la_volumenvalor OWNER TO postgres;

--
-- TOC entry 12866 (class 0 OID 0)
-- Dependencies: 2079
-- Name: TABLE la_volumenvalor; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.la_volumenvalor IS 'Estructura para la definición de un tipo de dato personalizado que permite indicar la medición de un volumen y la naturaleza de este.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_VolumenValor';


--
-- TOC entry 12867 (class 0 OID 0)
-- Dependencies: 2079
-- Name: COLUMN la_volumenvalor.volumen_medicion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_volumenvalor.volumen_medicion IS 'Medición del volumen en m3.
@iliname Volumen_Medicion';


--
-- TOC entry 12868 (class 0 OID 0)
-- Dependencies: 2079
-- Name: COLUMN la_volumenvalor.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_volumenvalor.tipo IS 'Indicación de si el volumen es calculado, si figura como oficial o si se da otra circunstancia.
@iliname Tipo';


--
-- TOC entry 12869 (class 0 OID 0)
-- Dependencies: 2079
-- Name: COLUMN la_volumenvalor.la_unidadespacial_volumen; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_volumenvalor.la_unidadespacial_volumen IS 'Corresponde al atributo volume de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen';


--
-- TOC entry 12870 (class 0 OID 0)
-- Dependencies: 2079
-- Name: COLUMN la_volumenvalor.la_espacjrdcndddfccion_volumen; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_volumenvalor.la_espacjrdcndddfccion_volumen IS 'Corresponde al atributo volume de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen';


--
-- TOC entry 12871 (class 0 OID 0)
-- Dependencies: 2079
-- Name: COLUMN la_volumenvalor.la_espacijrdcrdsrvcios_volumen; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_volumenvalor.la_espacijrdcrdsrvcios_volumen IS 'Corresponde al atributo volume de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen';


--
-- TOC entry 12872 (class 0 OID 0)
-- Dependencies: 2079
-- Name: COLUMN la_volumenvalor.construccion_volumen; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_volumenvalor.construccion_volumen IS 'Corresponde al atributo volume de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen';


--
-- TOC entry 12873 (class 0 OID 0)
-- Dependencies: 2079
-- Name: COLUMN la_volumenvalor.terreno_volumen; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_volumenvalor.terreno_volumen IS 'Corresponde al atributo volume de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen';


--
-- TOC entry 12874 (class 0 OID 0)
-- Dependencies: 2079
-- Name: COLUMN la_volumenvalor.servidumbrepaso_volumen; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_volumenvalor.servidumbrepaso_volumen IS 'Corresponde al atributo volume de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen';


--
-- TOC entry 12875 (class 0 OID 0)
-- Dependencies: 2079
-- Name: COLUMN la_volumenvalor.unidadconstruccion_volumen; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.la_volumenvalor.unidadconstruccion_volumen IS 'Corresponde al atributo volume de la clase en LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen';


--
-- TOC entry 2080 (class 1259 OID 335871)
-- Name: li_lineaje; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.li_lineaje (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    astatement character varying(255),
    la_punto_metodoproduccion bigint,
    puntocontrol_metodoproduccion bigint,
    puntolindero_metodoproduccion bigint,
    puntolevantamiento_metodoproduccion bigint
);


ALTER TABLE interlis_ili2db3_ladm.li_lineaje OWNER TO postgres;

--
-- TOC entry 12876 (class 0 OID 0)
-- Dependencies: 2080
-- Name: TABLE li_lineaje; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.li_lineaje IS 'Estructura que da soporte a los metadatos que documentan el linaje, información concerniente a las fuentes y a los procesos de producción, y procedente de la norma ISO 19115. Con respecto a la clase de dicha norma, presenta sólo el atributo statement.
@iliname LADM_COL_V1_1.LADM_Nucleo.LI_Lineaje';


--
-- TOC entry 12877 (class 0 OID 0)
-- Dependencies: 2080
-- Name: COLUMN li_lineaje.astatement; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.li_lineaje.astatement IS 'Explicación general del conocimiento del productor de datos sobre el linaje de un recurso.
@iliname Statement';


--
-- TOC entry 12878 (class 0 OID 0)
-- Dependencies: 2080
-- Name: COLUMN li_lineaje.la_punto_metodoproduccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.li_lineaje.la_punto_metodoproduccion IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Punto.MetodoProduccion';


--
-- TOC entry 12879 (class 0 OID 0)
-- Dependencies: 2080
-- Name: COLUMN li_lineaje.puntocontrol_metodoproduccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.li_lineaje.puntocontrol_metodoproduccion IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Punto.MetodoProduccion';


--
-- TOC entry 12880 (class 0 OID 0)
-- Dependencies: 2080
-- Name: COLUMN li_lineaje.puntolindero_metodoproduccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.li_lineaje.puntolindero_metodoproduccion IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Punto.MetodoProduccion';


--
-- TOC entry 12881 (class 0 OID 0)
-- Dependencies: 2080
-- Name: COLUMN li_lineaje.puntolevantamiento_metodoproduccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.li_lineaje.puntolevantamiento_metodoproduccion IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Punto.MetodoProduccion';


--
-- TOC entry 2081 (class 1259 OID 335875)
-- Name: lindero; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.lindero (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    longitud numeric(6,1) NOT NULL,
    localizacion_textual character varying(255),
    ccl_espacio_de_nombres character varying(255) NOT NULL,
    ccl_local_id character varying(255) NOT NULL,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    geometria public.geometry(LineString,3116),
    CONSTRAINT lindero_longitud_check CHECK (((longitud >= 0.0) AND (longitud <= 10000.0)))
);


ALTER TABLE interlis_ili2db3_ladm.lindero OWNER TO postgres;

--
-- TOC entry 12882 (class 0 OID 0)
-- Dependencies: 2081
-- Name: TABLE lindero; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.lindero IS 'Clase especializada de LA_CadenaCarasLindero que permite registrar los linderos.
Dos linderos no pueden cruzarse ni superponerse.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Lindero';


--
-- TOC entry 12883 (class 0 OID 0)
-- Dependencies: 2081
-- Name: COLUMN lindero.longitud; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.lindero.longitud IS 'Lóngitud en m del lindero.
@iliname Longitud';


--
-- TOC entry 12884 (class 0 OID 0)
-- Dependencies: 2081
-- Name: COLUMN lindero.localizacion_textual; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.lindero.localizacion_textual IS 'Descripción de la localización, cuando esta se basa en texto.
@iliname Localizacion_Textual';


--
-- TOC entry 12885 (class 0 OID 0)
-- Dependencies: 2081
-- Name: COLUMN lindero.ccl_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.lindero.ccl_espacio_de_nombres IS 'Identificador único global de la cadena de caras lindero.
@iliname ccl_Espacio_De_Nombres';


--
-- TOC entry 12886 (class 0 OID 0)
-- Dependencies: 2081
-- Name: COLUMN lindero.ccl_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.lindero.ccl_local_id IS 'Identificador local de la cadena de caras lindero.
@iliname ccl_Local_Id';


--
-- TOC entry 12887 (class 0 OID 0)
-- Dependencies: 2081
-- Name: COLUMN lindero.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.lindero.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12888 (class 0 OID 0)
-- Dependencies: 2081
-- Name: COLUMN lindero.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.lindero.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 12889 (class 0 OID 0)
-- Dependencies: 2081
-- Name: COLUMN lindero.geometria; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.lindero.geometria IS 'Geometría lineal que define el lindero. Puede estar asociada a geometrías de tipo punto que definen sus vértices o ser una entidad lineal independiente.
@iliname Geometria';


--
-- TOC entry 2082 (class 1259 OID 335883)
-- Name: mas; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.mas (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    clp bigint NOT NULL,
    uep_la_unidadespacial bigint,
    uep_la_espaciojuridicoredservicios bigint,
    uep_la_espaciojuridicounidadedificacion bigint,
    uep_servidumbrepaso bigint,
    uep_terreno bigint,
    uep_construccion bigint,
    uep_unidadconstruccion bigint
);


ALTER TABLE interlis_ili2db3_ladm.mas OWNER TO postgres;

--
-- TOC entry 12890 (class 0 OID 0)
-- Dependencies: 2082
-- Name: TABLE mas; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.mas IS '@iliname LADM_COL_V1_1.LADM_Nucleo.mas';


--
-- TOC entry 2083 (class 1259 OID 335887)
-- Name: masccl; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.masccl (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    cclp_la_cadenacaraslimite bigint,
    cclp_lindero bigint,
    uep_la_unidadespacial bigint,
    uep_la_espaciojuridicoredservicios bigint,
    uep_la_espaciojuridicounidadedificacion bigint,
    uep_servidumbrepaso bigint,
    uep_terreno bigint,
    uep_construccion bigint,
    uep_unidadconstruccion bigint
);


ALTER TABLE interlis_ili2db3_ladm.masccl OWNER TO postgres;

--
-- TOC entry 12891 (class 0 OID 0)
-- Dependencies: 2083
-- Name: TABLE masccl; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.masccl IS '@iliname LADM_COL_V1_1.LADM_Nucleo.masCcl';


--
-- TOC entry 2084 (class 1259 OID 335891)
-- Name: menos; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.menos (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ccl_la_cadenacaraslimite bigint,
    ccl_lindero bigint,
    eu_la_unidadespacial bigint,
    eu_la_espaciojuridicoredservicios bigint,
    eu_la_espaciojuridicounidadedificacion bigint,
    eu_servidumbrepaso bigint,
    eu_terreno bigint,
    eu_construccion bigint,
    eu_unidadconstruccion bigint
);


ALTER TABLE interlis_ili2db3_ladm.menos OWNER TO postgres;

--
-- TOC entry 12892 (class 0 OID 0)
-- Dependencies: 2084
-- Name: TABLE menos; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.menos IS '@iliname LADM_COL_V1_1.LADM_Nucleo.menos';


--
-- TOC entry 2085 (class 1259 OID 335895)
-- Name: menosf; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.menosf (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    cl bigint NOT NULL,
    ue_la_unidadespacial bigint,
    ue_la_espaciojuridicoredservicios bigint,
    ue_la_espaciojuridicounidadedificacion bigint,
    ue_servidumbrepaso bigint,
    ue_terreno bigint,
    ue_construccion bigint,
    ue_unidadconstruccion bigint
);


ALTER TABLE interlis_ili2db3_ladm.menosf OWNER TO postgres;

--
-- TOC entry 12893 (class 0 OID 0)
-- Dependencies: 2085
-- Name: TABLE menosf; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.menosf IS '@iliname LADM_COL_V1_1.LADM_Nucleo.menosf';


--
-- TOC entry 2086 (class 1259 OID 335899)
-- Name: miembros; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.miembros (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    interesados_la_agrupacion_interesados bigint,
    interesados_col_interesado bigint,
    agrupacion bigint NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.miembros OWNER TO postgres;

--
-- TOC entry 12894 (class 0 OID 0)
-- Dependencies: 2086
-- Name: TABLE miembros; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.miembros IS '@iliname LADM_COL_V1_1.LADM_Nucleo.miembros';


--
-- TOC entry 2087 (class 1259 OID 335903)
-- Name: oid; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.oid (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    localid character varying(255) NOT NULL,
    espaciodenombres character varying(255) NOT NULL,
    extdireccion_direccion_id bigint,
    extinteresado_interesado_id bigint,
    la_nivel_n_id bigint
);


ALTER TABLE interlis_ili2db3_ladm.oid OWNER TO postgres;

--
-- TOC entry 12895 (class 0 OID 0)
-- Dependencies: 2087
-- Name: TABLE oid; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.oid IS 'Estructura que permite definir el Oid o identificadores de objeto. Viene marcado en la propia norma ISO 19152:2012, LADM.
@iliname LADM_COL_V1_1.LADM_Nucleo.Oid';


--
-- TOC entry 12896 (class 0 OID 0)
-- Dependencies: 2087
-- Name: COLUMN oid.localid; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.oid.localid IS 'Identificador local asignado por el proveedor de los datos.
@iliname localId';


--
-- TOC entry 12897 (class 0 OID 0)
-- Dependencies: 2087
-- Name: COLUMN oid.espaciodenombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.oid.espaciodenombres IS 'Identificador de la fuente de datos del objeto.
@iliname espacioDeNombres';


--
-- TOC entry 12898 (class 0 OID 0)
-- Dependencies: 2087
-- Name: COLUMN oid.extdireccion_direccion_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.oid.extdireccion_direccion_id IS 'Identificador local de la dirección.
@iliname LADM_COL_V1_1.LADM_Nucleo.ExtDireccion.Direccion_ID';


--
-- TOC entry 12899 (class 0 OID 0)
-- Dependencies: 2087
-- Name: COLUMN oid.extinteresado_interesado_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.oid.extinteresado_interesado_id IS 'Identificador local del interesado.
@iliname LADM_COL_V1_1.LADM_Nucleo.ExtInteresado.Interesado_ID';


--
-- TOC entry 12900 (class 0 OID 0)
-- Dependencies: 2087
-- Name: COLUMN oid.la_nivel_n_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.oid.la_nivel_n_id IS '@iliname LADM_COL_V1_1.LADM_Nucleo.LA_Nivel.n_ID';


--
-- TOC entry 2088 (class 1259 OID 335910)
-- Name: om_observacion; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.om_observacion (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    col_fuenteespacial_mediciones bigint
);


ALTER TABLE interlis_ili2db3_ladm.om_observacion OWNER TO postgres;

--
-- TOC entry 12901 (class 0 OID 0)
-- Dependencies: 2088
-- Name: TABLE om_observacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.om_observacion IS 'Estructura que pone a disposición del modelo la clase OM_Observation de la ISO 19156 y de la que sólo implementa un atributo de los cinco que tiene la clase origina: resultQuality.
@iliname LADM_COL_V1_1.LADM_Nucleo.OM_Observacion';


--
-- TOC entry 12902 (class 0 OID 0)
-- Dependencies: 2088
-- Name: COLUMN om_observacion.col_fuenteespacial_mediciones; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.om_observacion.col_fuenteespacial_mediciones IS '@iliname LADM_COL_V1_1.LADM_Nucleo.COL_FuenteEspacial.Mediciones';


--
-- TOC entry 2089 (class 1259 OID 335914)
-- Name: om_proceso; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.om_proceso (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_seq bigint,
    col_fuenteespacial_procedimiento bigint
);


ALTER TABLE interlis_ili2db3_ladm.om_proceso OWNER TO postgres;

--
-- TOC entry 12903 (class 0 OID 0)
-- Dependencies: 2089
-- Name: TABLE om_proceso; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.om_proceso IS 'Estructura que pone a disposición del modelo la clase OM_Process de la ISO 19156. No desarrollado, debe ser definido por los pilotos
@iliname LADM_COL_V1_1.LADM_Nucleo.OM_Proceso';


--
-- TOC entry 12904 (class 0 OID 0)
-- Dependencies: 2089
-- Name: COLUMN om_proceso.col_fuenteespacial_procedimiento; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.om_proceso.col_fuenteespacial_procedimiento IS 'No desarrollado, debe ser definido por los pilotos
@iliname LADM_COL_V1_1.LADM_Nucleo.COL_FuenteEspacial.Procedimiento';


--
-- TOC entry 2090 (class 1259 OID 335918)
-- Name: predio; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.predio (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    departamento character varying(2),
    municipio character varying(3),
    zona character varying(2),
    nupre character varying(20) NOT NULL,
    fmi character varying(80),
    numero_predial character varying(30),
    numero_predial_anterior character varying(20),
    avaluo_predio numeric(16,1),
    copropiedad bigint,
    nombre character varying(255),
    tipo character varying(255) NOT NULL,
    u_espacio_de_nombres character varying(255) NOT NULL,
    u_local_id character varying(255) NOT NULL,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    CONSTRAINT predio_avaluo_predio_check CHECK (((avaluo_predio >= 0.0) AND (avaluo_predio <= '999999999999999'::numeric)))
);


ALTER TABLE interlis_ili2db3_ladm.predio OWNER TO postgres;

--
-- TOC entry 12905 (class 0 OID 0)
-- Dependencies: 2090
-- Name: TABLE predio; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.predio IS 'Clase especializada de BaUnit, que describe la unidad administrativa básica para el caso de Colombia.
El predio es la unidad territorial legal propia de Catastro. Esta formada por el terreno y puede o no tener construcciones asociadas.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Predio';


--
-- TOC entry 12906 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.departamento; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.departamento IS 'Corresponde al codigo del departamento al cual pertenece el predio. Es asignado por DIVIPOLA y tiene 2 dígitos.
@iliname Departamento';


--
-- TOC entry 12907 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.municipio; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.municipio IS 'Corresponde al codigo del municipio al cual pertenece el predio. Es asignado por DIVIPOLA y tiene 3 dígitos.
@iliname Municipio';


--
-- TOC entry 12908 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.zona; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.zona IS 'Corresponde a la zona castrastral, definida para optimizar las actividades catastrales. Es un codigo de 2 dígitos.
@iliname Zona';


--
-- TOC entry 12909 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.nupre; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.nupre IS 'Numero Unico de identificación Predial. Es el codigo definido en el proyecto de ley que será el codigo de identificación del predio tanto para catastratro como para Registro.
@iliname NUPRE';


--
-- TOC entry 12910 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.fmi; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.fmi IS 'Folio de Matricula Inmobilidaria. Codigo único de identificación asignado al documento registral en la oficina de registro de instrumentos públicos.
@iliname FMI';


--
-- TOC entry 12911 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.numero_predial; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.numero_predial IS 'Nuevo código númerico de treinta (30) dígitos, que se le asigna a cada predio y busca localizarlo inequívocamente en los documentos catastrales, según el modelo determinado por el Instituto Geográfico Agustin Codazzi.
@iliname Numero_Predial';


--
-- TOC entry 12912 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.numero_predial_anterior; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.numero_predial_anterior IS 'Anterior código númerico de veinte (20) digitos, que se le asigna a cada predio y busca localizarlo inequívocamente en los documentos catastrales, según el modelo determinado por el Instituto Geográfico Agustin Codazzi.
@iliname Numero_Predial_Anterior';


--
-- TOC entry 12913 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.avaluo_predio; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.avaluo_predio IS 'Valor de cada predio, obtenido mediante investigación y análisis estadistico del mercado inmobiliario y la metodología de aplicación  correspondiente. El avalúo  catastral de cada predio se determina a partir de la adición de los avalúos parciales practicados independientemente para los terrenos y para las edificaciones en el comprendidos.
@iliname Avaluo_Predio';


--
-- TOC entry 12914 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.nombre; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.nombre IS 'Nombre que recibe la unidad administrativa básica, en muchos casos toponímico, especialmente en terrenos rústicos.
@iliname Nombre';


--
-- TOC entry 12915 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.tipo IS 'Tipo de derecho que la reconoce.
@iliname Tipo';


--
-- TOC entry 12916 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.u_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.u_espacio_de_nombres IS 'Identificador único global.
@iliname u_Espacio_De_Nombres';


--
-- TOC entry 12917 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.u_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.u_local_id IS 'Identificador único local.
@iliname u_Local_Id';


--
-- TOC entry 12918 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12919 (class 0 OID 0)
-- Dependencies: 2090
-- Name: COLUMN predio.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.predio.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 2091 (class 1259 OID 335926)
-- Name: predio_copropiedad; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.predio_copropiedad (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200)
);


ALTER TABLE interlis_ili2db3_ladm.predio_copropiedad OWNER TO postgres;

--
-- TOC entry 12920 (class 0 OID 0)
-- Dependencies: 2091
-- Name: TABLE predio_copropiedad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.predio_copropiedad IS '@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.predio_copropiedad';


--
-- TOC entry 2092 (class 1259 OID 335930)
-- Name: publicidad; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.publicidad (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    tipo character varying(255) NOT NULL,
    codigo_registral_publicidad character varying(5) NOT NULL,
    p_espacio_de_nombres character varying(255) NOT NULL,
    p_local_id character varying(255) NOT NULL,
    baunit_la_baunit bigint,
    baunit_predio bigint,
    interesado_la_agrupacion_interesados bigint,
    interesado_col_interesado bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone
);


ALTER TABLE interlis_ili2db3_ladm.publicidad OWNER TO postgres;

--
-- TOC entry 12921 (class 0 OID 0)
-- Dependencies: 2092
-- Name: TABLE publicidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.publicidad IS 'Clase especial del perfil colombiano de la norma ISO 19152:2012. Pretenden generar publicidad sobre el predio a partir del almacenamiento de los codigos registrales que se inscriben el FMI. No se genera ningún tipo de derecho, ni limita la propiedad.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Publicidad';


--
-- TOC entry 12922 (class 0 OID 0)
-- Dependencies: 2092
-- Name: COLUMN publicidad.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.publicidad.tipo IS 'Indica la característica por la que se hace público.
@iliname Tipo';


--
-- TOC entry 12923 (class 0 OID 0)
-- Dependencies: 2092
-- Name: COLUMN publicidad.codigo_registral_publicidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.publicidad.codigo_registral_publicidad IS 'Código registral del FMI que se hace público.
@iliname Codigo_Registral_Publicidad';


--
-- TOC entry 12924 (class 0 OID 0)
-- Dependencies: 2092
-- Name: COLUMN publicidad.p_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.publicidad.p_espacio_de_nombres IS 'Identificador global único.
@iliname p_Espacio_De_Nombres';


--
-- TOC entry 12925 (class 0 OID 0)
-- Dependencies: 2092
-- Name: COLUMN publicidad.p_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.publicidad.p_local_id IS 'Identificador único local.
@iliname p_Local_Id';


--
-- TOC entry 12926 (class 0 OID 0)
-- Dependencies: 2092
-- Name: COLUMN publicidad.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.publicidad.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12927 (class 0 OID 0)
-- Dependencies: 2092
-- Name: COLUMN publicidad.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.publicidad.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 2093 (class 1259 OID 335937)
-- Name: publicidadfuente; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.publicidadfuente (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    publicidad bigint NOT NULL,
    fuente bigint NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.publicidadfuente OWNER TO postgres;

--
-- TOC entry 12928 (class 0 OID 0)
-- Dependencies: 2093
-- Name: TABLE publicidadfuente; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.publicidadfuente IS '@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadFuente';


--
-- TOC entry 2094 (class 1259 OID 335941)
-- Name: puntoccl; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.puntoccl (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    punto_la_punto bigint,
    punto_puntocontrol bigint,
    punto_puntolindero bigint,
    punto_puntolevantamiento bigint,
    ccl_la_cadenacaraslimite bigint,
    ccl_lindero bigint
);


ALTER TABLE interlis_ili2db3_ladm.puntoccl OWNER TO postgres;

--
-- TOC entry 12929 (class 0 OID 0)
-- Dependencies: 2094
-- Name: TABLE puntoccl; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.puntoccl IS '@iliname LADM_COL_V1_1.LADM_Nucleo.puntoCcl';


--
-- TOC entry 2095 (class 1259 OID 335945)
-- Name: puntocl; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.puntocl (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    punto_la_punto bigint,
    punto_puntocontrol bigint,
    punto_puntolindero bigint,
    punto_puntolevantamiento bigint,
    cl bigint NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.puntocl OWNER TO postgres;

--
-- TOC entry 12930 (class 0 OID 0)
-- Dependencies: 2095
-- Name: TABLE puntocl; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.puntocl IS '@iliname LADM_COL_V1_1.LADM_Nucleo.puntoCl';


--
-- TOC entry 2096 (class 1259 OID 335949)
-- Name: puntocontrol; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.puntocontrol (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    nombre_punto character varying(20) NOT NULL,
    exactitud_vertical integer NOT NULL,
    exactitud_horizontal integer NOT NULL,
    tipo_punto_control character varying(255),
    confiabilidad boolean,
    posicion_interpolacion character varying(255),
    monumentacion character varying(255),
    puntotipo character varying(255) NOT NULL,
    p_espacio_de_nombres character varying(255) NOT NULL,
    p_local_id character varying(255) NOT NULL,
    ue_la_unidadespacial bigint,
    ue_la_espaciojuridicoredservicios bigint,
    ue_la_espaciojuridicounidadedificacion bigint,
    ue_servidumbrepaso bigint,
    ue_terreno bigint,
    ue_construccion bigint,
    ue_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    localizacion_original public.geometry(Point,3116),
    CONSTRAINT puntocontrol_exactitud_horizontal_check CHECK (((exactitud_horizontal >= 0) AND (exactitud_horizontal <= 1000))),
    CONSTRAINT puntocontrol_exactitud_vertical_check CHECK (((exactitud_vertical >= 0) AND (exactitud_vertical <= 1000)))
);


ALTER TABLE interlis_ili2db3_ladm.puntocontrol OWNER TO postgres;

--
-- TOC entry 12931 (class 0 OID 0)
-- Dependencies: 2096
-- Name: TABLE puntocontrol; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.puntocontrol IS 'Clase especializada de LA_Punto que representa puntos de la densificación de la red local, que se utiliza en la operación catastral para el levantamiento de información fisica de los objetos territoriales, como puntos de control.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoControl';


--
-- TOC entry 12932 (class 0 OID 0)
-- Dependencies: 2096
-- Name: COLUMN puntocontrol.nombre_punto; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntocontrol.nombre_punto IS 'Nombre que recibe el punto.
@iliname Nombre_Punto';


--
-- TOC entry 12933 (class 0 OID 0)
-- Dependencies: 2096
-- Name: COLUMN puntocontrol.exactitud_vertical; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntocontrol.exactitud_vertical IS 'Exactitud vertical de la medición del punto.
@iliname Exactitud_Vertical';


--
-- TOC entry 12934 (class 0 OID 0)
-- Dependencies: 2096
-- Name: COLUMN puntocontrol.exactitud_horizontal; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntocontrol.exactitud_horizontal IS 'Exactitud horizontal de la medición del punto.
@iliname Exactitud_Horizontal';


--
-- TOC entry 12935 (class 0 OID 0)
-- Dependencies: 2096
-- Name: COLUMN puntocontrol.tipo_punto_control; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntocontrol.tipo_punto_control IS 'Si se trata deun punto de control o de apoyo.
@iliname Tipo_Punto_Control';


--
-- TOC entry 12936 (class 0 OID 0)
-- Dependencies: 2096
-- Name: COLUMN puntocontrol.confiabilidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntocontrol.confiabilidad IS 'Si el punto es o no fiable.
@iliname Confiabilidad';


--
-- TOC entry 12937 (class 0 OID 0)
-- Dependencies: 2096
-- Name: COLUMN puntocontrol.posicion_interpolacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntocontrol.posicion_interpolacion IS '@iliname Posicion_Interpolacion';


--
-- TOC entry 12938 (class 0 OID 0)
-- Dependencies: 2096
-- Name: COLUMN puntocontrol.monumentacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntocontrol.monumentacion IS '@iliname Monumentacion';


--
-- TOC entry 12939 (class 0 OID 0)
-- Dependencies: 2096
-- Name: COLUMN puntocontrol.puntotipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntocontrol.puntotipo IS '@iliname PuntoTipo';


--
-- TOC entry 12940 (class 0 OID 0)
-- Dependencies: 2096
-- Name: COLUMN puntocontrol.p_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntocontrol.p_espacio_de_nombres IS '@iliname p_Espacio_De_Nombres';


--
-- TOC entry 12941 (class 0 OID 0)
-- Dependencies: 2096
-- Name: COLUMN puntocontrol.p_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntocontrol.p_local_id IS '@iliname p_Local_Id';


--
-- TOC entry 12942 (class 0 OID 0)
-- Dependencies: 2096
-- Name: COLUMN puntocontrol.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntocontrol.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12943 (class 0 OID 0)
-- Dependencies: 2096
-- Name: COLUMN puntocontrol.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntocontrol.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 12944 (class 0 OID 0)
-- Dependencies: 2096
-- Name: COLUMN puntocontrol.localizacion_original; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntocontrol.localizacion_original IS '@iliname Localizacion_Original';


--
-- TOC entry 2097 (class 1259 OID 335958)
-- Name: puntofuente; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.puntofuente (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    pfuente bigint NOT NULL,
    punto_la_punto bigint,
    punto_puntocontrol bigint,
    punto_puntolindero bigint,
    punto_puntolevantamiento bigint
);


ALTER TABLE interlis_ili2db3_ladm.puntofuente OWNER TO postgres;

--
-- TOC entry 12945 (class 0 OID 0)
-- Dependencies: 2097
-- Name: TABLE puntofuente; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.puntofuente IS '@iliname LADM_COL_V1_1.LADM_Nucleo.puntoFuente';


--
-- TOC entry 2098 (class 1259 OID 335962)
-- Name: puntolevantamiento; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.puntolevantamiento (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    tipo_punto_levantamiento character varying(255),
    definicion_punto character varying(255) NOT NULL,
    exactitud_vertical integer,
    exactitud_horizontal integer,
    nombre_punto character varying(10),
    posicion_interpolacion character varying(255),
    monumentacion character varying(255),
    puntotipo character varying(255) NOT NULL,
    p_espacio_de_nombres character varying(255) NOT NULL,
    p_local_id character varying(255) NOT NULL,
    ue_la_unidadespacial bigint,
    ue_la_espaciojuridicoredservicios bigint,
    ue_la_espaciojuridicounidadedificacion bigint,
    ue_servidumbrepaso bigint,
    ue_terreno bigint,
    ue_construccion bigint,
    ue_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    localizacion_original public.geometry(Point,3116),
    CONSTRAINT puntolevantamiento_exactitud_horizontal_check CHECK (((exactitud_horizontal >= 0) AND (exactitud_horizontal <= 1000))),
    CONSTRAINT puntolevantamiento_exactitud_vertical_check CHECK (((exactitud_vertical >= 0) AND (exactitud_vertical <= 1000)))
);


ALTER TABLE interlis_ili2db3_ladm.puntolevantamiento OWNER TO postgres;

--
-- TOC entry 12946 (class 0 OID 0)
-- Dependencies: 2098
-- Name: TABLE puntolevantamiento; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.puntolevantamiento IS 'Clase especializada de LA_Punto que representa puntos demarcados que representan la posición horizontal de un vértice de construcción, servidumbre o auxiliare.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLevantamiento';


--
-- TOC entry 12947 (class 0 OID 0)
-- Dependencies: 2098
-- Name: COLUMN puntolevantamiento.tipo_punto_levantamiento; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolevantamiento.tipo_punto_levantamiento IS 'Se caracterizan los diferentes tipos de punto levantamiento, estos son punto de construccción, punto de servidumbre o punto auxiliar
@iliname Tipo_Punto_Levantamiento';


--
-- TOC entry 12948 (class 0 OID 0)
-- Dependencies: 2098
-- Name: COLUMN puntolevantamiento.definicion_punto; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolevantamiento.definicion_punto IS 'Se caracteriza si el punto de levantamiento corresponde a un punto bien definido o no bien definido
@iliname Definicion_Punto';


--
-- TOC entry 12949 (class 0 OID 0)
-- Dependencies: 2098
-- Name: COLUMN puntolevantamiento.exactitud_vertical; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolevantamiento.exactitud_vertical IS 'Corresponde a la exactitud vertical del punto levantamiento
@iliname Exactitud_Vertical';


--
-- TOC entry 12950 (class 0 OID 0)
-- Dependencies: 2098
-- Name: COLUMN puntolevantamiento.exactitud_horizontal; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolevantamiento.exactitud_horizontal IS 'Corresponde a la exactitud horizontal del punto levantamiento
@iliname Exactitud_Horizontal';


--
-- TOC entry 12951 (class 0 OID 0)
-- Dependencies: 2098
-- Name: COLUMN puntolevantamiento.nombre_punto; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolevantamiento.nombre_punto IS 'Nombre que recibe el punto.
@iliname Nombre_Punto';


--
-- TOC entry 12952 (class 0 OID 0)
-- Dependencies: 2098
-- Name: COLUMN puntolevantamiento.posicion_interpolacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolevantamiento.posicion_interpolacion IS '@iliname Posicion_Interpolacion';


--
-- TOC entry 12953 (class 0 OID 0)
-- Dependencies: 2098
-- Name: COLUMN puntolevantamiento.monumentacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolevantamiento.monumentacion IS '@iliname Monumentacion';


--
-- TOC entry 12954 (class 0 OID 0)
-- Dependencies: 2098
-- Name: COLUMN puntolevantamiento.puntotipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolevantamiento.puntotipo IS '@iliname PuntoTipo';


--
-- TOC entry 12955 (class 0 OID 0)
-- Dependencies: 2098
-- Name: COLUMN puntolevantamiento.p_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolevantamiento.p_espacio_de_nombres IS '@iliname p_Espacio_De_Nombres';


--
-- TOC entry 12956 (class 0 OID 0)
-- Dependencies: 2098
-- Name: COLUMN puntolevantamiento.p_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolevantamiento.p_local_id IS '@iliname p_Local_Id';


--
-- TOC entry 12957 (class 0 OID 0)
-- Dependencies: 2098
-- Name: COLUMN puntolevantamiento.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolevantamiento.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12958 (class 0 OID 0)
-- Dependencies: 2098
-- Name: COLUMN puntolevantamiento.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolevantamiento.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 12959 (class 0 OID 0)
-- Dependencies: 2098
-- Name: COLUMN puntolevantamiento.localizacion_original; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolevantamiento.localizacion_original IS '@iliname Localizacion_Original';


--
-- TOC entry 2099 (class 1259 OID 335971)
-- Name: puntolindero; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.puntolindero (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    acuerdo character varying(255) NOT NULL,
    definicion_punto character varying(255) NOT NULL,
    descripcion_punto character varying(255),
    exactitud_vertical integer,
    exactitud_horizontal integer NOT NULL,
    confiabilidad boolean,
    nombre_punto character varying(10),
    posicion_interpolacion character varying(255),
    monumentacion character varying(255),
    puntotipo character varying(255) NOT NULL,
    p_espacio_de_nombres character varying(255) NOT NULL,
    p_local_id character varying(255) NOT NULL,
    ue_la_unidadespacial bigint,
    ue_la_espaciojuridicoredservicios bigint,
    ue_la_espaciojuridicounidadedificacion bigint,
    ue_servidumbrepaso bigint,
    ue_terreno bigint,
    ue_construccion bigint,
    ue_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    localizacion_original public.geometry(Point,3116),
    CONSTRAINT puntolindero_exactitud_horizontal_check CHECK (((exactitud_horizontal >= 0) AND (exactitud_horizontal <= 1000))),
    CONSTRAINT puntolindero_exactitud_vertical_check CHECK (((exactitud_vertical >= 0) AND (exactitud_vertical <= 1000)))
);


ALTER TABLE interlis_ili2db3_ladm.puntolindero OWNER TO postgres;

--
-- TOC entry 12960 (class 0 OID 0)
-- Dependencies: 2099
-- Name: TABLE puntolindero; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.puntolindero IS 'Clase especializada de LA_Punto que almacena puntos que definen un lindero, instancia de la clase LA_CadenaCarasLindero y sus especializaciones.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLindero';


--
-- TOC entry 12961 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.acuerdo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.acuerdo IS 'Se Indica si existe acuerdo o no entre los colindantes en relación al punto lindero que se está midiendo.
@iliname Acuerdo';


--
-- TOC entry 12962 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.definicion_punto; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.definicion_punto IS 'Se caracteriza si el punto de levantamiento corresponde a un punto bien definido o no bien definido
@iliname Definicion_Punto';


--
-- TOC entry 12963 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.descripcion_punto; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.descripcion_punto IS 'Es la descripción del tipo de punto lindero y las caracteristicas del vertice
@iliname Descripcion_Punto';


--
-- TOC entry 12964 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.exactitud_vertical; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.exactitud_vertical IS 'Corresponde a la exactitud vertical del punto lindero
@iliname Exactitud_Vertical';


--
-- TOC entry 12965 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.exactitud_horizontal; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.exactitud_horizontal IS 'Corresponde a la exactitud horizontal del punto lindero
@iliname Exactitud_Horizontal';


--
-- TOC entry 12966 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.confiabilidad; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.confiabilidad IS 'Indica si es o no fiable.
@iliname Confiabilidad';


--
-- TOC entry 12967 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.nombre_punto; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.nombre_punto IS 'Nombre o codigo del punto lindero
@iliname Nombre_Punto';


--
-- TOC entry 12968 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.posicion_interpolacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.posicion_interpolacion IS '@iliname Posicion_Interpolacion';


--
-- TOC entry 12969 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.monumentacion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.monumentacion IS '@iliname Monumentacion';


--
-- TOC entry 12970 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.puntotipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.puntotipo IS '@iliname PuntoTipo';


--
-- TOC entry 12971 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.p_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.p_espacio_de_nombres IS '@iliname p_Espacio_De_Nombres';


--
-- TOC entry 12972 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.p_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.p_local_id IS '@iliname p_Local_Id';


--
-- TOC entry 12973 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12974 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 12975 (class 0 OID 0)
-- Dependencies: 2099
-- Name: COLUMN puntolindero.localizacion_original; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.puntolindero.localizacion_original IS '@iliname Localizacion_Original';


--
-- TOC entry 2100 (class 1259 OID 335980)
-- Name: relacionbaunit; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.relacionbaunit (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    unidad1_la_baunit bigint,
    unidad1_predio bigint,
    unidad2_la_baunit bigint,
    unidad2_predio bigint
);


ALTER TABLE interlis_ili2db3_ladm.relacionbaunit OWNER TO postgres;

--
-- TOC entry 12976 (class 0 OID 0)
-- Dependencies: 2100
-- Name: TABLE relacionbaunit; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.relacionbaunit IS '@iliname LADM_COL_V1_1.LADM_Nucleo.relacionBaunit';


--
-- TOC entry 2101 (class 1259 OID 335984)
-- Name: relacionfuente; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.relacionfuente (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    refuente bigint NOT NULL,
    relacionrequeridabaunit bigint NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.relacionfuente OWNER TO postgres;

--
-- TOC entry 12977 (class 0 OID 0)
-- Dependencies: 2101
-- Name: TABLE relacionfuente; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.relacionfuente IS '@iliname LADM_COL_V1_1.LADM_Nucleo.relacionFuente';


--
-- TOC entry 2102 (class 1259 OID 335988)
-- Name: relacionfuenteuespacial; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.relacionfuenteuespacial (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    rfuente bigint NOT NULL,
    relacionrequeridaue bigint NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.relacionfuenteuespacial OWNER TO postgres;

--
-- TOC entry 12978 (class 0 OID 0)
-- Dependencies: 2102
-- Name: TABLE relacionfuenteuespacial; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.relacionfuenteuespacial IS '@iliname LADM_COL_V1_1.LADM_Nucleo.relacionFuenteUespacial';


--
-- TOC entry 2103 (class 1259 OID 335992)
-- Name: relacionue; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.relacionue (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    rue1_la_unidadespacial bigint,
    rue1_la_espaciojuridicoredservicios bigint,
    rue1_la_espaciojuridicounidadedificacion bigint,
    rue1_servidumbrepaso bigint,
    rue1_terreno bigint,
    rue1_construccion bigint,
    rue1_unidadconstruccion bigint,
    rue2_la_unidadespacial bigint,
    rue2_la_espaciojuridicoredservicios bigint,
    rue2_la_espaciojuridicounidadedificacion bigint,
    rue2_servidumbrepaso bigint,
    rue2_terreno bigint,
    rue2_construccion bigint,
    rue2_unidadconstruccion bigint
);


ALTER TABLE interlis_ili2db3_ladm.relacionue OWNER TO postgres;

--
-- TOC entry 12979 (class 0 OID 0)
-- Dependencies: 2103
-- Name: TABLE relacionue; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.relacionue IS '@iliname LADM_COL_V1_1.LADM_Nucleo.relacionUe';


--
-- TOC entry 2104 (class 1259 OID 335996)
-- Name: responsablefuente; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.responsablefuente (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    cfuente bigint NOT NULL,
    notario_la_agrupacion_interesados bigint,
    notario_col_interesado bigint
);


ALTER TABLE interlis_ili2db3_ladm.responsablefuente OWNER TO postgres;

--
-- TOC entry 12980 (class 0 OID 0)
-- Dependencies: 2104
-- Name: TABLE responsablefuente; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.responsablefuente IS '@iliname LADM_COL_V1_1.LADM_Nucleo.responsableFuente';


--
-- TOC entry 2105 (class 1259 OID 336000)
-- Name: rrrfuente; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.rrrfuente (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    rfuente bigint NOT NULL,
    rrr_col_responsabilidad bigint,
    rrr_col_derecho bigint,
    rrr_col_restriccion bigint,
    rrr_col_hipoteca bigint
);


ALTER TABLE interlis_ili2db3_ladm.rrrfuente OWNER TO postgres;

--
-- TOC entry 12981 (class 0 OID 0)
-- Dependencies: 2105
-- Name: TABLE rrrfuente; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.rrrfuente IS '@iliname LADM_COL_V1_1.LADM_Nucleo.rrrFuente';


--
-- TOC entry 2106 (class 1259 OID 336004)
-- Name: servidumbrepaso; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.servidumbrepaso (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    identificador character varying(20) NOT NULL,
    fecha_inscripcion_catastral date,
    dimension character varying(255),
    etiqueta character varying(255),
    relacion_superficie character varying(255),
    su_espacio_de_nombres character varying(255) NOT NULL,
    su_local_id character varying(255) NOT NULL,
    nivel bigint,
    uej2_la_unidadespacial bigint,
    uej2_la_espaciojuridicoredservicios bigint,
    uej2_la_espaciojuridicounidadedificacion bigint,
    uej2_servidumbrepaso bigint,
    uej2_terreno bigint,
    uej2_construccion bigint,
    uej2_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    punto_referencia public.geometry(Point,3116),
    poligono_creado public.geometry(MultiPolygon,3116)
);


ALTER TABLE interlis_ili2db3_ladm.servidumbrepaso OWNER TO postgres;

--
-- TOC entry 12982 (class 0 OID 0)
-- Dependencies: 2106
-- Name: TABLE servidumbrepaso; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.servidumbrepaso IS 'Tipo de unidad espacial que permite la representación de una servidumbre de paso asociada a una LA_BAUnit.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.ServidumbrePaso';


--
-- TOC entry 12983 (class 0 OID 0)
-- Dependencies: 2106
-- Name: COLUMN servidumbrepaso.identificador; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.servidumbrepaso.identificador IS '@iliname Identificador';


--
-- TOC entry 12984 (class 0 OID 0)
-- Dependencies: 2106
-- Name: COLUMN servidumbrepaso.fecha_inscripcion_catastral; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.servidumbrepaso.fecha_inscripcion_catastral IS 'Fecha de inscripción de la servidumbre en el Catastro.
@iliname Fecha_Inscripcion_Catastral';


--
-- TOC entry 12985 (class 0 OID 0)
-- Dependencies: 2106
-- Name: COLUMN servidumbrepaso.dimension; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.servidumbrepaso.dimension IS '@iliname Dimension';


--
-- TOC entry 12986 (class 0 OID 0)
-- Dependencies: 2106
-- Name: COLUMN servidumbrepaso.etiqueta; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.servidumbrepaso.etiqueta IS 'Corresponde al atributo label de la clase en LADM.
@iliname Etiqueta';


--
-- TOC entry 12987 (class 0 OID 0)
-- Dependencies: 2106
-- Name: COLUMN servidumbrepaso.relacion_superficie; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.servidumbrepaso.relacion_superficie IS 'Corresponde al atributo surfaceRelation de la clase en LADM.
@iliname Relacion_Superficie';


--
-- TOC entry 12988 (class 0 OID 0)
-- Dependencies: 2106
-- Name: COLUMN servidumbrepaso.su_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.servidumbrepaso.su_espacio_de_nombres IS 'Identificador único global. Corresponde al atributo suID de la clase en LADM.
@iliname su_Espacio_De_Nombres';


--
-- TOC entry 12989 (class 0 OID 0)
-- Dependencies: 2106
-- Name: COLUMN servidumbrepaso.su_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.servidumbrepaso.su_local_id IS 'Identificador único local.
@iliname su_Local_Id';


--
-- TOC entry 12990 (class 0 OID 0)
-- Dependencies: 2106
-- Name: COLUMN servidumbrepaso.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.servidumbrepaso.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 12991 (class 0 OID 0)
-- Dependencies: 2106
-- Name: COLUMN servidumbrepaso.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.servidumbrepaso.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 12992 (class 0 OID 0)
-- Dependencies: 2106
-- Name: COLUMN servidumbrepaso.punto_referencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.servidumbrepaso.punto_referencia IS 'Corresponde al atributo referencePoint de la clase en LADM.
@iliname Punto_Referencia';


--
-- TOC entry 12993 (class 0 OID 0)
-- Dependencies: 2106
-- Name: COLUMN servidumbrepaso.poligono_creado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.servidumbrepaso.poligono_creado IS 'Materializacion del metodo createArea(). Almacena de forma permanente la geometría de tipo poligonal.';


--
-- TOC entry 2107 (class 1259 OID 336011)
-- Name: t_ili2db_attrname; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_attrname (
    iliname character varying(1024) NOT NULL,
    sqlname character varying(1024) NOT NULL,
    owner character varying(1024) NOT NULL,
    target character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_attrname OWNER TO postgres;

--
-- TOC entry 2108 (class 1259 OID 336017)
-- Name: t_ili2db_basket; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_basket (
    t_id bigint NOT NULL,
    dataset bigint,
    topic character varying(200) NOT NULL,
    t_ili_tid character varying(200),
    attachmentkey character varying(200) NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_basket OWNER TO postgres;

--
-- TOC entry 2109 (class 1259 OID 336023)
-- Name: t_ili2db_classname; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_classname (
    iliname character varying(1024) NOT NULL,
    sqlname character varying(1024) NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_classname OWNER TO postgres;

--
-- TOC entry 2110 (class 1259 OID 336029)
-- Name: t_ili2db_column_prop; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_column_prop (
    tablename character varying(255) NOT NULL,
    subtype character varying(255),
    columnname character varying(255) NOT NULL,
    tag character varying(1024) NOT NULL,
    setting character varying(1024) NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_column_prop OWNER TO postgres;

--
-- TOC entry 2111 (class 1259 OID 336035)
-- Name: t_ili2db_dataset; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_dataset (
    t_id bigint NOT NULL,
    datasetname character varying(200)
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_dataset OWNER TO postgres;

--
-- TOC entry 2112 (class 1259 OID 336038)
-- Name: t_ili2db_import; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_import (
    t_id bigint NOT NULL,
    dataset bigint NOT NULL,
    importdate timestamp without time zone NOT NULL,
    importuser character varying(40) NOT NULL,
    importfile character varying(200)
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_import OWNER TO postgres;

--
-- TOC entry 12994 (class 0 OID 0)
-- Dependencies: 2112
-- Name: TABLE t_ili2db_import; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.t_ili2db_import IS 'DEPRECATED, do not use';


--
-- TOC entry 2113 (class 1259 OID 336041)
-- Name: t_ili2db_import_basket; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_import_basket (
    t_id bigint NOT NULL,
    import bigint NOT NULL,
    basket bigint NOT NULL,
    objectcount integer,
    start_t_id bigint,
    end_t_id bigint
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_import_basket OWNER TO postgres;

--
-- TOC entry 12995 (class 0 OID 0)
-- Dependencies: 2113
-- Name: TABLE t_ili2db_import_basket; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.t_ili2db_import_basket IS 'DEPRECATED, do not use';


--
-- TOC entry 2114 (class 1259 OID 336044)
-- Name: t_ili2db_import_object; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_import_object (
    t_id bigint NOT NULL,
    import_basket bigint NOT NULL,
    class character varying(200) NOT NULL,
    objectcount integer,
    start_t_id bigint,
    end_t_id bigint
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_import_object OWNER TO postgres;

--
-- TOC entry 12996 (class 0 OID 0)
-- Dependencies: 2114
-- Name: TABLE t_ili2db_import_object; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.t_ili2db_import_object IS 'DEPRECATED, do not use';


--
-- TOC entry 2115 (class 1259 OID 336047)
-- Name: t_ili2db_inheritance; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_inheritance (
    thisclass character varying(1024) NOT NULL,
    baseclass character varying(1024)
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_inheritance OWNER TO postgres;

--
-- TOC entry 2116 (class 1259 OID 336053)
-- Name: t_ili2db_meta_attrs; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_meta_attrs (
    ilielement character varying(255) NOT NULL,
    attr_name character varying(1024) NOT NULL,
    attr_value character varying(1024) NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_meta_attrs OWNER TO postgres;

--
-- TOC entry 2117 (class 1259 OID 336059)
-- Name: t_ili2db_model; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_model (
    file character varying(250) NOT NULL,
    iliversion character varying(3) NOT NULL,
    modelname text NOT NULL,
    content text NOT NULL,
    importdate timestamp without time zone NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_model OWNER TO postgres;

--
-- TOC entry 2118 (class 1259 OID 336065)
-- Name: t_ili2db_settings; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_settings (
    tag character varying(60) NOT NULL,
    setting character varying(255)
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_settings OWNER TO postgres;

--
-- TOC entry 2119 (class 1259 OID 336068)
-- Name: t_ili2db_table_prop; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_table_prop (
    tablename character varying(255) NOT NULL,
    tag character varying(1024) NOT NULL,
    setting character varying(1024) NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_table_prop OWNER TO postgres;

--
-- TOC entry 2120 (class 1259 OID 336074)
-- Name: t_ili2db_trafo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.t_ili2db_trafo (
    iliname character varying(1024) NOT NULL,
    tag character varying(1024) NOT NULL,
    setting character varying(1024) NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.t_ili2db_trafo OWNER TO postgres;

--
-- TOC entry 2121 (class 1259 OID 336080)
-- Name: terreno; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.terreno (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    area_registral numeric(15,1),
    area_calculada numeric(15,1) NOT NULL,
    avaluo_terreno numeric(16,1) NOT NULL,
    dimension character varying(255),
    etiqueta character varying(255),
    relacion_superficie character varying(255),
    su_espacio_de_nombres character varying(255) NOT NULL,
    su_local_id character varying(255) NOT NULL,
    nivel bigint,
    uej2_la_unidadespacial bigint,
    uej2_la_espaciojuridicoredservicios bigint,
    uej2_la_espaciojuridicounidadedificacion bigint,
    uej2_servidumbrepaso bigint,
    uej2_terreno bigint,
    uej2_construccion bigint,
    uej2_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    punto_referencia public.geometry(Point,3116),
    poligono_creado public.geometry(MultiPolygon,3116),
    CONSTRAINT terreno_area_calculada_check CHECK (((area_calculada >= 0.0) AND (area_calculada <= 99999999999999.9))),
    CONSTRAINT terreno_area_registral_check CHECK (((area_registral >= 0.0) AND (area_registral <= 99999999999999.9))),
    CONSTRAINT terreno_avaluo_terreno_check CHECK (((avaluo_terreno >= 0.0) AND (avaluo_terreno <= '999999999999999'::numeric)))
);


ALTER TABLE interlis_ili2db3_ladm.terreno OWNER TO postgres;

--
-- TOC entry 12997 (class 0 OID 0)
-- Dependencies: 2121
-- Name: TABLE terreno; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.terreno IS 'Porción de tierra con una extensión geográfica definida.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno';


--
-- TOC entry 12998 (class 0 OID 0)
-- Dependencies: 2121
-- Name: COLUMN terreno.area_registral; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.terreno.area_registral IS 'Área del predio que se encuentra inscrita en el Folio de Matricula Inmobiliaria
@iliname Area_Registral';


--
-- TOC entry 12999 (class 0 OID 0)
-- Dependencies: 2121
-- Name: COLUMN terreno.area_calculada; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.terreno.area_calculada IS 'Área de predio resultado de los calculos realizados en el proceso de levantamiento planimetrico
@iliname Area_Calculada';


--
-- TOC entry 13000 (class 0 OID 0)
-- Dependencies: 2121
-- Name: COLUMN terreno.avaluo_terreno; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.terreno.avaluo_terreno IS 'Valor asignado en el proceso de valoración economica masiva al terreno del predio
@iliname Avaluo_Terreno';


--
-- TOC entry 13001 (class 0 OID 0)
-- Dependencies: 2121
-- Name: COLUMN terreno.dimension; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.terreno.dimension IS '@iliname Dimension';


--
-- TOC entry 13002 (class 0 OID 0)
-- Dependencies: 2121
-- Name: COLUMN terreno.etiqueta; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.terreno.etiqueta IS 'Corresponde al atributo label de la clase en LADM.
@iliname Etiqueta';


--
-- TOC entry 13003 (class 0 OID 0)
-- Dependencies: 2121
-- Name: COLUMN terreno.relacion_superficie; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.terreno.relacion_superficie IS 'Corresponde al atributo surfaceRelation de la clase en LADM.
@iliname Relacion_Superficie';


--
-- TOC entry 13004 (class 0 OID 0)
-- Dependencies: 2121
-- Name: COLUMN terreno.su_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.terreno.su_espacio_de_nombres IS 'Identificador único global. Corresponde al atributo suID de la clase en LADM.
@iliname su_Espacio_De_Nombres';


--
-- TOC entry 13005 (class 0 OID 0)
-- Dependencies: 2121
-- Name: COLUMN terreno.su_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.terreno.su_local_id IS 'Identificador único local.
@iliname su_Local_Id';


--
-- TOC entry 13006 (class 0 OID 0)
-- Dependencies: 2121
-- Name: COLUMN terreno.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.terreno.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 13007 (class 0 OID 0)
-- Dependencies: 2121
-- Name: COLUMN terreno.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.terreno.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 13008 (class 0 OID 0)
-- Dependencies: 2121
-- Name: COLUMN terreno.punto_referencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.terreno.punto_referencia IS 'Corresponde al atributo referencePoint de la clase en LADM.
@iliname Punto_Referencia';


--
-- TOC entry 13009 (class 0 OID 0)
-- Dependencies: 2121
-- Name: COLUMN terreno.poligono_creado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.terreno.poligono_creado IS 'Materializacion del metodo createArea(). Almacena de forma permanente la geometría de tipo poligonal.';


--
-- TOC entry 2122 (class 1259 OID 336090)
-- Name: topografofuente; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.topografofuente (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    sfuente bigint NOT NULL,
    topografo_la_agrupacion_interesados bigint,
    topografo_col_interesado bigint
);


ALTER TABLE interlis_ili2db3_ladm.topografofuente OWNER TO postgres;

--
-- TOC entry 13010 (class 0 OID 0)
-- Dependencies: 2122
-- Name: TABLE topografofuente; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.topografofuente IS '@iliname LADM_COL_V1_1.LADM_Nucleo.topografoFuente';


--
-- TOC entry 2123 (class 1259 OID 336094)
-- Name: uebaunit; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.uebaunit (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ue_la_unidadespacial bigint,
    ue_la_espaciojuridicoredservicios bigint,
    ue_la_espaciojuridicounidadedificacion bigint,
    ue_servidumbrepaso bigint,
    ue_terreno bigint,
    ue_construccion bigint,
    ue_unidadconstruccion bigint,
    baunit_la_baunit bigint,
    baunit_predio bigint
);


ALTER TABLE interlis_ili2db3_ladm.uebaunit OWNER TO postgres;

--
-- TOC entry 13011 (class 0 OID 0)
-- Dependencies: 2123
-- Name: TABLE uebaunit; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.uebaunit IS '@iliname LADM_COL_V1_1.LADM_Nucleo.ueBaunit';


--
-- TOC entry 2124 (class 1259 OID 336098)
-- Name: uefuente; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.uefuente (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ue_la_unidadespacial bigint,
    ue_la_espaciojuridicoredservicios bigint,
    ue_la_espaciojuridicounidadedificacion bigint,
    ue_servidumbrepaso bigint,
    ue_terreno bigint,
    ue_construccion bigint,
    ue_unidadconstruccion bigint,
    pfuente bigint NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.uefuente OWNER TO postgres;

--
-- TOC entry 13012 (class 0 OID 0)
-- Dependencies: 2124
-- Name: TABLE uefuente; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.uefuente IS '@iliname LADM_COL_V1_1.LADM_Nucleo.ueFuente';


--
-- TOC entry 2125 (class 1259 OID 336102)
-- Name: ueuegrupo; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.ueuegrupo (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    parte_la_unidadespacial bigint,
    parte_la_espaciojuridicoredservicios bigint,
    parte_la_espaciojuridicounidadedificacion bigint,
    parte_servidumbrepaso bigint,
    parte_terreno bigint,
    parte_construccion bigint,
    parte_unidadconstruccion bigint,
    todo bigint NOT NULL
);


ALTER TABLE interlis_ili2db3_ladm.ueuegrupo OWNER TO postgres;

--
-- TOC entry 13013 (class 0 OID 0)
-- Dependencies: 2125
-- Name: TABLE ueuegrupo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.ueuegrupo IS '@iliname LADM_COL_V1_1.LADM_Nucleo.ueUeGrupo';


--
-- TOC entry 2126 (class 1259 OID 336106)
-- Name: unidadconstruccion; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.unidadconstruccion (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    avaluo_unidad_construccion numeric(16,1),
    numero_pisos integer NOT NULL,
    area_construida numeric(15,1),
    area_privada_construida numeric(15,1),
    construccion bigint NOT NULL,
    tipo character varying(255),
    dimension character varying(255),
    etiqueta character varying(255),
    relacion_superficie character varying(255),
    su_espacio_de_nombres character varying(255) NOT NULL,
    su_local_id character varying(255) NOT NULL,
    nivel bigint,
    uej2_la_unidadespacial bigint,
    uej2_la_espaciojuridicoredservicios bigint,
    uej2_la_espaciojuridicounidadedificacion bigint,
    uej2_servidumbrepaso bigint,
    uej2_terreno bigint,
    uej2_construccion bigint,
    uej2_unidadconstruccion bigint,
    comienzo_vida_util_version timestamp without time zone NOT NULL,
    fin_vida_util_version timestamp without time zone,
    punto_referencia public.geometry(Point,3116),
    poligono_creado public.geometry(MultiPolygon,3116),
    CONSTRAINT unidadconstruccion_area_construida_check CHECK (((area_construida >= 0.0) AND (area_construida <= 99999999999999.9))),
    CONSTRAINT unidadconstruccion_area_privada_construida_check CHECK (((area_privada_construida >= 0.0) AND (area_privada_construida <= 99999999999999.9))),
    CONSTRAINT unidadconstruccion_avaluo_unidad_constrccion_check CHECK (((avaluo_unidad_construccion >= 0.0) AND (avaluo_unidad_construccion <= '999999999999999'::numeric))),
    CONSTRAINT unidadconstruccion_numero_pisos_check CHECK (((numero_pisos >= 1) AND (numero_pisos <= 100)))
);


ALTER TABLE interlis_ili2db3_ladm.unidadconstruccion OWNER TO postgres;

--
-- TOC entry 13014 (class 0 OID 0)
-- Dependencies: 2126
-- Name: TABLE unidadconstruccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.unidadconstruccion IS 'Es cada conjunto de materiales consolidados dentro de un predio que tiene una caracteristicas especificas en cuanto a elementos constitutivos físicos y usos de los mismos.
@iliname Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.UnidadConstruccion';


--
-- TOC entry 13015 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.avaluo_unidad_construccion; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.avaluo_unidad_construccion IS 'Corresponde al valor catastral determinado mediante el metodo economico definido, para cada unidad de contrucción del predio
@iliname Avaluo_Unidad_Construccion';


--
-- TOC entry 13016 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.numero_pisos; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.numero_pisos IS 'Número de pisos que constituyen la unidad de construcción.
@iliname Numero_Pisos';


--
-- TOC entry 13017 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.area_construida; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.area_construida IS 'Area de la unidad de contrucción.
@iliname Area_Construida';


--
-- TOC entry 13018 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.area_privada_construida; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.area_privada_construida IS 'Área privada de la unidad de construcción para el caso en que las construcciones tienen regimen de propiedad horizontal.
@iliname Area_Privada_Construida';


--
-- TOC entry 13019 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.tipo; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.tipo IS 'Tipo de unidad de edificación de la que se trata.
@iliname Tipo';


--
-- TOC entry 13020 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.dimension; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.dimension IS '@iliname Dimension';


--
-- TOC entry 13021 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.etiqueta; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.etiqueta IS 'Corresponde al atributo label de la clase en LADM.
@iliname Etiqueta';


--
-- TOC entry 13022 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.relacion_superficie; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.relacion_superficie IS 'Corresponde al atributo surfaceRelation de la clase en LADM.
@iliname Relacion_Superficie';


--
-- TOC entry 13023 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.su_espacio_de_nombres; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.su_espacio_de_nombres IS 'Identificador único global. Corresponde al atributo suID de la clase en LADM.
@iliname su_Espacio_De_Nombres';


--
-- TOC entry 13024 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.su_local_id; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.su_local_id IS 'Identificador único local.
@iliname su_Local_Id';


--
-- TOC entry 13025 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.comienzo_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.comienzo_vida_util_version IS 'Comienzo de la validez actual de la instancia de un objeto.
@iliname Comienzo_Vida_Util_Version';


--
-- TOC entry 13026 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.fin_vida_util_version; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.fin_vida_util_version IS 'Finnzo de la validez actual de la instancia de un objeto.
@iliname Fin_Vida_Util_Version';


--
-- TOC entry 13027 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.punto_referencia; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.punto_referencia IS 'Corresponde al atributo referencePoint de la clase en LADM.
@iliname Punto_Referencia';


--
-- TOC entry 13028 (class 0 OID 0)
-- Dependencies: 2126
-- Name: COLUMN unidadconstruccion.poligono_creado; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON COLUMN interlis_ili2db3_ladm.unidadconstruccion.poligono_creado IS 'Materializacion del metodo createArea(). Almacena de forma permanente la geometría de tipo poligonal.';


--
-- TOC entry 2127 (class 1259 OID 336117)
-- Name: unidadfuente; Type: TABLE; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE TABLE interlis_ili2db3_ladm.unidadfuente (
    t_id bigint DEFAULT nextval('interlis_ili2db3_ladm.t_ili2db_seq'::regclass) NOT NULL,
    t_ili_tid character varying(200),
    ufuente bigint NOT NULL,
    unidad_la_baunit bigint,
    unidad_predio bigint
);


ALTER TABLE interlis_ili2db3_ladm.unidadfuente OWNER TO postgres;

--
-- TOC entry 13029 (class 0 OID 0)
-- Dependencies: 2127
-- Name: TABLE unidadfuente; Type: COMMENT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COMMENT ON TABLE interlis_ili2db3_ladm.unidadfuente IS '@iliname LADM_COL_V1_1.LADM_Nucleo.unidadFuente';


--
-- TOC entry 12279 (class 0 OID 335185)
-- Dependencies: 1964
-- Data for Name: baunitcomointeresado; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.baunitcomointeresado (t_id, t_ili_tid, interesado_la_agrupacion_interesados, interesado_col_interesado, unidad_la_baunit, unidad_predio) FROM stdin;
\.


--
-- TOC entry 12280 (class 0 OID 335189)
-- Dependencies: 1965
-- Data for Name: baunitfuente; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.baunitfuente (t_id, t_ili_tid, bfuente, unidad_la_baunit, unidad_predio) FROM stdin;
\.


--
-- TOC entry 12281 (class 0 OID 335193)
-- Dependencies: 1966
-- Data for Name: cc_metodooperacion; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.cc_metodooperacion (t_id, t_seq, formula, dimensiones_origen, ddimensiones_objetivo, la_transformacion_transformacion) FROM stdin;
\.


--
-- TOC entry 12282 (class 0 OID 335199)
-- Dependencies: 1967
-- Data for Name: cclfuente; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.cclfuente (t_id, t_ili_tid, ccl_la_cadenacaraslimite, ccl_lindero, lfuente) FROM stdin;
\.


--
-- TOC entry 12283 (class 0 OID 335203)
-- Dependencies: 1968
-- Data for Name: ci_codigotarea; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.ci_codigotarea (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Proveedor_De_Recursos	\N	f	Proveedor De Recursos	\N
1	Custodio	\N	f	Custodio	\N
2	Propietario	\N	f	Propietario	\N
3	Usuario	\N	f	Usuario	\N
4	Distribuidor	\N	f	Distribuidor	\N
5	Creador	\N	f	Creador	\N
6	Punto_De_Contacto	\N	f	Punto De Contacto	\N
7	Investigador_Principal	\N	f	Investigador Principal	\N
8	Procesador	\N	f	Procesador	\N
9	Editor	\N	f	Editor	\N
10	Autor	\N	f	Autor	\N
\.


--
-- TOC entry 12284 (class 0 OID 335209)
-- Dependencies: 1969
-- Data for Name: ci_contacto; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.ci_contacto (t_id, t_seq, telefono, direccion, fuente_en_linea, horario_de_atencion, instrucciones_contacto, ci_parteresponsable_informacion_contacto) FROM stdin;
\.


--
-- TOC entry 12285 (class 0 OID 335216)
-- Dependencies: 1970
-- Data for Name: ci_forma_presentacion_codigo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.ci_forma_presentacion_codigo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Imagen	\N	f	Imagen	Definición en la ISO 19115:2003.
1	Mapa	\N	f	Mapa	Definición en la ISO 19115:2003.
2	Modelo	\N	f	Modelo	Definición en la ISO 19115:2003.
3	Perfil	\N	f	Perfil	Definición en la ISO 19115:2003.
4	Tabla	\N	f	Tabla	Definición en la ISO 19115:2003.
5	Video	\N	f	Video	Definición en la ISO 19115:2003.
6	Audio	\N	f	Audio	Definición en la ISO 19115:2003.
7	Diagrama	\N	f	Diagrama	Definición en la ISO 19115:2003.
8	Multimedia	\N	f	Multimedia	Definición en la ISO 19115:2003.
9	Muestra_Fisica	\N	f	Muestra Fisica	Definición en la ISO 19115:2003.
10	Otro	\N	f	Otro	Definición en la ISO 19115:2003.
\.


--
-- TOC entry 12286 (class 0 OID 335222)
-- Dependencies: 1971
-- Data for Name: ci_parteresponsable; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.ci_parteresponsable (t_id, t_seq, nombre_individual, nombre_organizacion, posicion, funcion, col_fuenteadminstrtiva_procedencia, la_unidadespacial_procedencia, la_agrupacinnddsspcles_procedencia, la_espacjrdcndddfccion_procedencia, la_espacijrdcrdsrvcios_procedencia, la_nivel_procedencia, la_relcnncsrnddsspcles_procedencia, la_baunit_procedencia, la_relacionnecesrbnits_procedencia, la_punto_procedencia, col_fuenteespacial_procedencia, la_cadenacaraslimite_procedencia, la_caraslindero_procedencia, la_agrupacion_intrsdos_procedencia, col_derecho_procedencia, col_interesado_procedencia, construccion_procedencia, lindero_procedencia, predio_procedencia, publicidad_procedencia, puntocontrol_procedencia, puntolindero_procedencia, terreno_procedencia, col_restriccion_procedencia, puntolevantamiento_procedencia, col_responsabilidad_procedencia, servidumbrepaso_procedencia, col_hipoteca_procedencia, unidadconstruccion_procedencia) FROM stdin;
\.


--
-- TOC entry 12287 (class 0 OID 335229)
-- Dependencies: 1972
-- Data for Name: clfuente; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.clfuente (t_id, t_ili_tid, cl, cfuente) FROM stdin;
\.


--
-- TOC entry 12288 (class 0 OID 335233)
-- Dependencies: 1973
-- Data for Name: col_acuerdotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_acuerdotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Acuerdo	\N	f	Acuerdo	Existe un acuerdo sobre la posición del punto
1	Desacuerdo	\N	f	Desacuerdo	Existe un desacuerdo sobre la posición del punto
\.


--
-- TOC entry 12289 (class 0 OID 335239)
-- Dependencies: 1974
-- Data for Name: col_afectacion; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_afectacion (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Inundacion	\N	f	Inundacion	\N
1	RemocionMasa	\N	f	RemocionMasa	Remocion en Masa
2	Otra	\N	f	Otra	\N
\.


--
-- TOC entry 12290 (class 0 OID 335245)
-- Dependencies: 1975
-- Data for Name: col_afectacion_terreno_afectacion; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_afectacion_terreno_afectacion (t_id, t_seq, avalue, terreno_afectacion) FROM stdin;
\.


--
-- TOC entry 12291 (class 0 OID 335249)
-- Dependencies: 1976
-- Data for Name: col_areatipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_areatipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Area_Calculada_Altura_Local	\N	f	Area Calculada Altura Local	\N
1	Area_Calculada_Altura_Mar	\N	f	Area Calculada Altura Mar	\N
2	Area_Catastral_Administrativa	\N	f	Area Catastral Administrativa	\N
3	Area_Estimado_Construccion	\N	f	Area Estimado Construccion	\N
4	Area_No_Oficial	\N	f	Area No Oficial	\N
5	Area_Registral	\N	f	Area Registral	\N
\.


--
-- TOC entry 12292 (class 0 OID 335255)
-- Dependencies: 1977
-- Data for Name: col_areavalor; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_areavalor (t_id, t_seq, areasize, atype, la_unidadespacial_area, la_espacjrdcndddfccion_area, la_espacijrdcrdsrvcios_area, construccion_area, terreno_area, servidumbrepaso_area, unidadconstruccion_area) FROM stdin;
\.


--
-- TOC entry 12293 (class 0 OID 335260)
-- Dependencies: 1978
-- Data for Name: col_bosqueareasemi; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_bosqueareasemi (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	AreaBoscosa	\N	f	AreaBoscosa	Área Boscosa
1	PlantaForestal	\N	f	PlantaForestal	Plantación Forestal
\.


--
-- TOC entry 12294 (class 0 OID 335266)
-- Dependencies: 1979
-- Data for Name: col_bosqueareasemi_terreno_bosque_area_seminaturale; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_bosqueareasemi_terreno_bosque_area_seminaturale (t_id, t_seq, avalue, terreno_bosque_area_seminaturale) FROM stdin;
\.


--
-- TOC entry 12295 (class 0 OID 335270)
-- Dependencies: 1980
-- Data for Name: col_cuerpoagua; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_cuerpoagua (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	NacimientoAgua	\N	f	NacimientoAgua	\N
1	CuerpoAgua	\N	f	CuerpoAgua	Cuerpo de agua natural o artificial
2	ZonaPantanosa	\N	f	ZonaPantanosa	\N
\.


--
-- TOC entry 12296 (class 0 OID 335276)
-- Dependencies: 1981
-- Data for Name: col_cuerpoagua_terreno_evidencia_cuerpo_agua; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_cuerpoagua_terreno_evidencia_cuerpo_agua (t_id, t_seq, avalue, terreno_evidencia_cuerpo_agua) FROM stdin;
\.


--
-- TOC entry 12297 (class 0 OID 335280)
-- Dependencies: 1982
-- Data for Name: col_defpuntotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_defpuntotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Bien_Definido	\N	f	Bien Definido	\N
1	No_Bien_Definido	\N	f	No Bien Definido	\N
\.


--
-- TOC entry 12298 (class 0 OID 335286)
-- Dependencies: 1983
-- Data for Name: col_derecho; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_derecho (t_id, t_ili_tid, tipo, codigo_registral_derecho, descripcion, comprobacion_comparte, uso_efectivo, r_espacio_de_nombres, r_local_id, interesado_la_agrupacion_interesados, interesado_col_interesado, unidad_la_baunit, unidad_predio, comienzo_vida_util_version, fin_vida_util_version) FROM stdin;
\.


--
-- TOC entry 12299 (class 0 OID 335293)
-- Dependencies: 1984
-- Data for Name: col_derechotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_derechotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Derecho_Propiedad_Colectiva	\N	f	Derecho Propiedad Colectiva	\N
1	Mineria_Derecho	\N	f	Mineria Derecho	\N
2	Nuda_Propiedad	\N	f	Nuda Propiedad	\N
3	Ocupacion	\N	f	Ocupacion	\N
4	Posesion	\N	f	Posesion	\N
5	Tenencia	\N	f	Tenencia	\N
6	Usufructo	\N	f	Usufructo	\N
7	Dominio	\N	f	Dominio	Derecho de dominio o propiedad
\.


--
-- TOC entry 12300 (class 0 OID 335299)
-- Dependencies: 1985
-- Data for Name: col_descripcionpuntotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_descripcionpuntotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Esquina_Construccion	\N	f	Esquina Construccion	\N
1	Interseccion_Cerca_De_Piedra	\N	f	Interseccion Cerca De Piedra	\N
2	Interseccion_Cerca_Viva	\N	f	Interseccion Cerca Viva	\N
3	Poste_de_Cerca	\N	f	Poste de Cerca	\N
4	Otros	\N	f	Otros	!! por definir durante pilotos
\.


--
-- TOC entry 12301 (class 0 OID 335305)
-- Dependencies: 1986
-- Data for Name: col_estadodisponibilidadtipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_estadodisponibilidadtipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Convertido	\N	f	Convertido	\N
1	Desconocido	\N	f	Desconocido	\N
2	Disponible	\N	f	Disponible	\N
\.


--
-- TOC entry 12302 (class 0 OID 335311)
-- Dependencies: 1987
-- Data for Name: col_estructuratipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_estructuratipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Croquis	\N	f	Croquis	\N
1	Linea_no_Estructurada	\N	f	Linea no Estructurada	\N
2	Texto	\N	f	Texto	\N
3	Topologico	\N	f	Topologico	\N
\.


--
-- TOC entry 12303 (class 0 OID 335317)
-- Dependencies: 1988
-- Data for Name: col_explotaciontipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_explotaciontipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Minera	\N	f	Minera	\N
1	Hidrocarburo	\N	f	Hidrocarburo	\N
2	Otra	\N	f	Otra	\N
\.


--
-- TOC entry 12304 (class 0 OID 335323)
-- Dependencies: 1989
-- Data for Name: col_explotaciontipo_terreno_explotacion; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_explotaciontipo_terreno_explotacion (t_id, t_seq, avalue, terreno_explotacion) FROM stdin;
\.


--
-- TOC entry 12305 (class 0 OID 335327)
-- Dependencies: 1990
-- Data for Name: col_fuenteadministrativa; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_fuenteadministrativa (t_id, t_ili_tid, texto, tipo, codigo_registral_transaccion, nombre, fecha_aceptacion, estado_disponibilidad, sello_inicio_validez, tipo_principal, fecha_grabacion, fecha_entrega, s_espacio_de_nombres, s_local_id, oficialidad) FROM stdin;
\.


--
-- TOC entry 12306 (class 0 OID 335334)
-- Dependencies: 1991
-- Data for Name: col_fuenteadministrativatipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_fuenteadministrativatipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Escritura	\N	f	Escritura	\N
1	Certificado	\N	f	Certificado	\N
2	Contrato	\N	f	Contrato	\N
3	Documento_Identidad	\N	f	Documento Identidad	\N
4	Informe	\N	f	Informe	\N
5	Formulario_Predial	\N	f	Formulario Predial	\N
6	Promesa_Compraventa	\N	f	Promesa Compraventa	\N
7	Reglamento	\N	f	Reglamento	\N
8	Resolucion	\N	f	Resolucion	\N
9	Sentencia	\N	f	Sentencia	\N
10	Solicitud	\N	f	Solicitud	\N
11	Acta	\N	f	Acta	\N
12	Acuerdo	\N	f	Acuerdo	\N
13	Auto	\N	f	Auto	\N
14	Estatuto_Social	\N	f	Estatuto Social	\N
15	Decreto	\N	f	Decreto	\N
16	Providencia	\N	f	Providencia	\N
17	Acta_Colindancia	\N	f	Acta Colindancia	\N
18	Libros_Antiguo_Sistema_Registral	\N	f	Libros Antiguo Sistema Registral	\N
19	Informe_Colindancia	\N	f	Informe Colindancia	\N
20	Carta_Venta	\N	f	Carta Venta	\N
\.


--
-- TOC entry 12307 (class 0 OID 335340)
-- Dependencies: 1992
-- Data for Name: col_fuenteespacial; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_fuenteespacial (t_id, t_ili_tid, tipo, fecha_aceptacion, estado_disponibilidad, sello_inicio_validez, tipo_principal, fecha_grabacion, fecha_entrega, s_espacio_de_nombres, s_local_id, oficialidad) FROM stdin;
\.


--
-- TOC entry 12308 (class 0 OID 335347)
-- Dependencies: 1993
-- Data for Name: col_fuenteespacialtipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_fuenteespacialtipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Croquis_Campo	\N	f	Croquis Campo	\N
1	Protocolo_Posicionamiento	\N	f	Protocolo Posicionamiento	\N
2	Informe_Calculo	\N	f	Informe Calculo	\N
3	Datos_Crudos	\N	f	Datos Crudos	\N
\.


--
-- TOC entry 12309 (class 0 OID 335353)
-- Dependencies: 1994
-- Data for Name: col_funcioninteresadotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_funcioninteresadotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Abogado_Demandas	\N	f	Abogado Demandas	\N
1	Administrador_Estado	\N	f	Administrador Estado	\N
2	Banco	\N	f	Banco	\N
3	Ciudadano	\N	f	Ciudadano	\N
4	Juez	\N	f	Juez	\N
5	Notario	\N	f	Notario	\N
6	Reconocedor_Agrimensor	\N	f	Reconocedor Agrimensor	\N
\.


--
-- TOC entry 12310 (class 0 OID 335359)
-- Dependencies: 1995
-- Data for Name: col_generotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_generotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Femenino	\N	f	Femenino	\N
1	Masculino	\N	f	Masculino	\N
2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12311 (class 0 OID 335365)
-- Dependencies: 1996
-- Data for Name: col_grupointeresadotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_grupointeresadotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Grupo_BAUnit	\N	f	Grupo BAUnit	\N
1	Grupo_Civil	\N	f	Grupo Civil	\N
2	Grupo_Empresarial	\N	f	Grupo Empresarial	\N
3	Grupo_Etnico	\N	f	Grupo Etnico	\N
\.


--
-- TOC entry 12312 (class 0 OID 335371)
-- Dependencies: 1997
-- Data for Name: col_hipoteca; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_hipoteca (t_id, t_ili_tid, h_tipo, codigo_registral_hipoteca, interesado_requerido, tipo, codigo_registral_restriccion, descripcion, comprobacion_comparte, uso_efectivo, r_espacio_de_nombres, r_local_id, interesado_la_agrupacion_interesados, interesado_col_interesado, unidad_la_baunit, unidad_predio, comienzo_vida_util_version, fin_vida_util_version) FROM stdin;
\.


--
-- TOC entry 12313 (class 0 OID 335378)
-- Dependencies: 1998
-- Data for Name: col_hipotecatipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_hipotecatipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Abierta	\N	f	Abierta	\N
1	Cerrada	\N	f	Cerrada	\N
\.


--
-- TOC entry 12314 (class 0 OID 335384)
-- Dependencies: 1999
-- Data for Name: col_instituciontipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_instituciontipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Registraduria_Nacional	\N	f	Registraduria Nacional	\N
1	Registro_Propiedad	\N	f	Registro Propiedad	\N
2	Catastro_IGAC	\N	f	Catastro IGAC	\N
3	Catastro_Descentralizado	\N	f	Catastro Descentralizado	\N
4	URT	\N	f	URT	\N
5	ANT	\N	f	ANT	\N
\.


--
-- TOC entry 12315 (class 0 OID 335390)
-- Dependencies: 2000
-- Data for Name: col_interesado; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_interesado (t_id, t_ili_tid, documento_identidad, tipo_documento, organo_emisor, fecha_emision, primer_apellido, primer_nombre, segundo_apellido, segundo_nombre, razon_social, genero, tipo_interesado_juridico, nombre, tipo, p_espacio_de_nombres, p_local_id, comienzo_vida_util_version, fin_vida_util_version) FROM stdin;
\.


--
-- TOC entry 12316 (class 0 OID 335397)
-- Dependencies: 2001
-- Data for Name: col_interesadodocumentotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_interesadodocumentotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Cedula_Ciudadania	\N	f	Cedula Ciudadania	\N
1	Cedula_Extranjeria	\N	f	Cedula Extranjeria	\N
2	NIT	\N	f	NIT	\N
3	Pasaporte	\N	f	Pasaporte	\N
4	Tarjeta_Identidad	\N	f	Tarjeta Identidad	\N
5	Libreta_Militar	\N	f	Libreta Militar	\N
6	Registro_Civil	\N	f	Registro Civil	\N
7	Cedula_Militar	\N	f	Cedula Militar	\N
8	NUIP	\N	f	NUIP	\N
9	Secuencial_SNR	\N	f	Secuencial SNR	\N
10	Secuencial_IGAC	\N	f	Secuencial IGAC	\N
\.


--
-- TOC entry 12317 (class 0 OID 335403)
-- Dependencies: 2002
-- Data for Name: col_interesadojuridicotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_interesadojuridicotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Publico	\N	f	Publico	\N
1	Privado	\N	f	Privado	\N
2	Mixto	\N	f	Mixto	\N
\.


--
-- TOC entry 12318 (class 0 OID 335409)
-- Dependencies: 2003
-- Data for Name: col_interpolaciontipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_interpolaciontipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Aislado	\N	f	Aislado	\N
1	Intermedio_Arco	\N	f	Intermedio Arco	\N
2	Intermedio_Linea	\N	f	Intermedio Linea	\N
\.


--
-- TOC entry 12319 (class 0 OID 335415)
-- Dependencies: 2004
-- Data for Name: col_levelcontenttipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_levelcontenttipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Construccion_Convencional	\N	f	Construccion Convencional	\N
1	Construccion_No_Convencional	\N	f	Construccion No Convencional	\N
2	Consuetudinario	\N	f	Consuetudinario	\N
3	Formal	\N	f	Formal	\N
4	Informal	\N	f	Informal	\N
5	Responsabilidad	\N	f	Responsabilidad	\N
6	Restriccion_Derecho_Publico	\N	f	Restriccion Derecho Publico	\N
7	Restriction_Derecho_Privado	\N	f	Restriction Derecho Privado	\N
\.


--
-- TOC entry 12320 (class 0 OID 335421)
-- Dependencies: 2005
-- Data for Name: col_monumentaciontipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_monumentaciontipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Incrustacion	\N	f	Incrustacion	\N
1	Mojon	\N	f	Mojon	\N
2	No_Materializado	\N	f	No Materializado	\N
3	Otros	\N	f	Otros	\N
4	Pilastra	\N	f	Pilastra	\N
\.


--
-- TOC entry 12321 (class 0 OID 335427)
-- Dependencies: 2006
-- Data for Name: col_prediotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_prediotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	NPH	\N	f	NPH	\N
1	PropiedadHorizontal.Matriz	\N	f	PropiedadHorizontal.Matriz	\N
2	PropiedadHorizontal.UnidadPredial	\N	f	PropiedadHorizontal.UnidadPredial	\N
3	Condominio.Matriz	\N	f	Condominio.Matriz	\N
4	Condominio.UnidadPredial	\N	f	Condominio.UnidadPredial	\N
5	Mejora	\N	f	Mejora	\N
6	ParqueCementerio.Matriz	\N	f	ParqueCementerio.Matriz	\N
7	ParqueCementerio.UnidadPrivada	\N	f	ParqueCementerio.UnidadPrivada	\N
8	Via	\N	f	Via	\N
9	BienUsoPublico	\N	f	BienUsoPublico	\N
10	Deposito	\N	f	Deposito	\N
11	Parqueadero	\N	f	Parqueadero	\N
12	Bodega	\N	f	Bodega	\N
\.


--
-- TOC entry 12322 (class 0 OID 335433)
-- Dependencies: 2007
-- Data for Name: col_publicidadtipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_publicidadtipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Demanda	\N	f	Demanda	\N
1	Inicio_de_Proceso_Administrativo	\N	f	Inicio de Proceso Administrativo	\N
2	Cancelacion	\N	f	Cancelacion	\N
3	Desplazamiento_Forzado	\N	f	Desplazamiento Forzado	\N
4	Victima_o_Restitucion	\N	f	Victima o Restitucion	\N
5	Publicidad_de_Acto_Juridico	\N	f	Publicidad de Acto Juridico	\N
\.


--
-- TOC entry 12323 (class 0 OID 335439)
-- Dependencies: 2008
-- Data for Name: col_puntocontroltipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_puntocontroltipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Control	\N	f	Control	\N
1	Apoyo	\N	f	Apoyo	\N
\.


--
-- TOC entry 12324 (class 0 OID 335445)
-- Dependencies: 2009
-- Data for Name: col_puntolevtipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_puntolevtipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Auxiliar	\N	f	Auxiliar	\N
1	Construccion	\N	f	Construccion	\N
2	Servidumbre	\N	f	Servidumbre	\N
\.


--
-- TOC entry 12325 (class 0 OID 335451)
-- Dependencies: 2010
-- Data for Name: col_redserviciostipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_redserviciostipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Petroleo	\N	f	Petroleo	\N
1	Quimicos	\N	f	Quimicos	\N
2	Red_Termica	\N	f	Red Termica	\N
3	Telecomunicacion	\N	f	Telecomunicacion	\N
\.


--
-- TOC entry 12326 (class 0 OID 335457)
-- Dependencies: 2011
-- Data for Name: col_responsabilidad; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_responsabilidad (t_id, t_ili_tid, tipo, codigo_registral_responsabilidad, descripcion, comprobacion_comparte, uso_efectivo, r_espacio_de_nombres, r_local_id, interesado_la_agrupacion_interesados, interesado_col_interesado, unidad_la_baunit, unidad_predio, comienzo_vida_util_version, fin_vida_util_version) FROM stdin;
\.


--
-- TOC entry 12327 (class 0 OID 335464)
-- Dependencies: 2012
-- Data for Name: col_responsabilidadtipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_responsabilidadtipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Constitucional	\N	f	Constitucional	\N
1	Legal	\N	f	Legal	\N
2	Contractual	\N	f	Contractual	\N
3	Administrativa	\N	f	Administrativa	\N
4	Judicial	\N	f	Judicial	\N
5	Otros	\N	f	Otros	\N
\.


--
-- TOC entry 12328 (class 0 OID 335470)
-- Dependencies: 2013
-- Data for Name: col_restriccion; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_restriccion (t_id, t_ili_tid, interesado_requerido, tipo, codigo_registral_restriccion, descripcion, comprobacion_comparte, uso_efectivo, r_espacio_de_nombres, r_local_id, interesado_la_agrupacion_interesados, interesado_col_interesado, unidad_la_baunit, unidad_predio, comienzo_vida_util_version, fin_vida_util_version) FROM stdin;
\.


--
-- TOC entry 12329 (class 0 OID 335477)
-- Dependencies: 2014
-- Data for Name: col_restricciontipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_restricciontipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Afectaciones_Interes_General	\N	f	Afectaciones Interes General	\N
1	Ambientales	\N	f	Ambientales	\N
2	Desplazamiento_Forzado_Restitucion	\N	f	Desplazamiento Forzado Restitucion	\N
3	Embargo	\N	f	Embargo	\N
4	Hipoteca	\N	f	Hipoteca	\N
5	Propiedad_Horizontal_y_Urbanismo	\N	f	Propiedad Horizontal y Urbanismo	\N
6	Prohibiciones_Expresas	\N	f	Prohibiciones Expresas	\N
7	Proteccion_Familia	\N	f	Proteccion Familia	\N
8	Servidumbre	\N	f	Servidumbre	\N
9	No_Registrada	\N	f	No Registrada	\N
\.


--
-- TOC entry 12330 (class 0 OID 335483)
-- Dependencies: 2015
-- Data for Name: col_servidumbretipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_servidumbretipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Vial	\N	f	Vial	\N
1	Petrolera	\N	f	Petrolera	\N
2	Electrica	\N	f	Electrica	\N
3	Otra	\N	f	Otra	\N
\.


--
-- TOC entry 12331 (class 0 OID 335489)
-- Dependencies: 2016
-- Data for Name: col_servidumbretipo_terreno_servidumbre; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_servidumbretipo_terreno_servidumbre (t_id, t_seq, avalue, terreno_servidumbre) FROM stdin;
\.


--
-- TOC entry 12332 (class 0 OID 335493)
-- Dependencies: 2017
-- Data for Name: col_territorioagricola; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_territorioagricola (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	CultTransitorio	\N	f	CultTransitorio	\N
1	CultPermanente	\N	f	CultPermanente	\N
2	Confinado	\N	f	Confinado	\N
3	TierraPrepodesc	\N	f	TierraPrepodesc	Tierra en preparacion o descanso
4	AreaAgriHetero	\N	f	AreaAgriHetero	\N
5	Pasto	\N	f	Pasto	\N
\.


--
-- TOC entry 12333 (class 0 OID 335499)
-- Dependencies: 2018
-- Data for Name: col_territorioagricola_terreno_territorio_agricola; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_territorioagricola_terreno_territorio_agricola (t_id, t_seq, avalue, terreno_territorio_agricola) FROM stdin;
\.


--
-- TOC entry 12334 (class 0 OID 335503)
-- Dependencies: 2019
-- Data for Name: col_tipoconstrucciontipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_tipoconstrucciontipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Anexo	\N	f	Anexo	\N
1	No_PH	\N	f	No PH	\N
2	Parque_Cementerio	\N	f	Parque Cementerio	\N
3	PH	\N	f	PH	\N
\.


--
-- TOC entry 12335 (class 0 OID 335509)
-- Dependencies: 2020
-- Data for Name: col_unidadedificaciontipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_unidadedificaciontipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Compartido	\N	f	Compartido	\N
1	individual	\N	f	individual	\N
\.


--
-- TOC entry 12336 (class 0 OID 335515)
-- Dependencies: 2021
-- Data for Name: col_viatipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_viatipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Arteria	\N	f	Arteria	\N
1	Autopista	\N	f	Autopista	\N
2	Carreteable	\N	f	Carreteable	\N
3	Cicloruta	\N	f	Cicloruta	\N
4	Colectora	\N	f	Colectora	\N
5	Departamental	\N	f	Departamental	\N
6	Ferrea	\N	f	Ferrea	\N
7	Local	\N	f	Local	\N
8	Metro_o_Metrovia	\N	f	Metro o Metrovia	\N
9	Nacional	\N	f	Nacional	\N
10	Ordinaria	\N	f	Ordinaria	\N
11	Peatonal	\N	f	Peatonal	\N
12	Principal	\N	f	Principal	\N
13	Privada	\N	f	Privada	\N
14	Secundaria	\N	f	Secundaria	\N
15	Troncal	\N	f	Troncal	\N
\.


--
-- TOC entry 12337 (class 0 OID 335521)
-- Dependencies: 2022
-- Data for Name: col_zonatipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.col_zonatipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Perimetro_Urbano	\N	f	Perimetro Urbano	\N
1	Rural	\N	f	Rural	\N
2	Corregimiento	\N	f	Corregimiento	\N
3	Caserios	\N	f	Caserios	\N
4	Inspecion_Policia	\N	f	Inspecion Policia	\N
\.


--
-- TOC entry 12338 (class 0 OID 335527)
-- Dependencies: 2023
-- Data for Name: construccion; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.construccion (t_id, t_ili_tid, avaluo_construccion, area_construccion, tipo, dimension, etiqueta, relacion_superficie, su_espacio_de_nombres, su_local_id, nivel, uej2_la_unidadespacial, uej2_la_espaciojuridicoredservicios, uej2_la_espaciojuridicounidadedificacion, uej2_servidumbrepaso, uej2_terreno, uej2_construccion, uej2_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, punto_referencia, poligono_creado) FROM stdin;
\.


--
-- TOC entry 12339 (class 0 OID 335536)
-- Dependencies: 2024
-- Data for Name: dq_absoluteexternalpositionalaccuracy; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy (t_id, t_seq, atributo1, atributo21, nombre_medida, identificacion_medida, descripcion_medida, metodo_evaluacion, descripcion_metodo_evaluacion, procedimiento_evaluacion, fecha_hora, resultado) FROM stdin;
\.


--
-- TOC entry 12340 (class 0 OID 335543)
-- Dependencies: 2025
-- Data for Name: dq_element; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.dq_element (t_id, t_seq, nombre_medida, identificacion_medida, descripcion_medida, metodo_evaluacion, descripcion_metodo_evaluacion, procedimiento_evaluacion, fecha_hora, resultado, om_observacion_resultado_calidad, col_fuenteadminstrtiva_calidad, la_unidadespacial_calidad, la_agrupacinnddsspcles_calidad, la_espacjrdcndddfccion_calidad, la_espacijrdcrdsrvcios_calidad, la_nivel_calidad, la_relcnncsrnddsspcles_calidad, la_baunit_calidad, la_relacionnecesrbnits_calidad, la_punto_calidad, col_fuenteespacial_calidad, la_cadenacaraslimite_calidad, la_caraslindero_calidad, la_agrupacion_intrsdos_calidad, col_derecho_calidad, col_interesado_calidad, construccion_calidad, lindero_calidad, predio_calidad, publicidad_calidad, puntocontrol_calidad, puntolindero_calidad, terreno_calidad, col_restriccion_calidad, puntolevantamiento_calidad, col_responsabilidad_calidad, servidumbrepaso_calidad, col_hipoteca_calidad, unidadconstruccion_calidad) FROM stdin;
\.


--
-- TOC entry 12341 (class 0 OID 335550)
-- Dependencies: 2026
-- Data for Name: dq_metodo_evaluacion_codigo_tipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.dq_metodo_evaluacion_codigo_tipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Interno_Directo	\N	f	Interno Directo	\N
1	Externo_Directo	\N	f	Externo Directo	\N
2	Indirecto	\N	f	Indirecto	\N
\.


--
-- TOC entry 12342 (class 0 OID 335556)
-- Dependencies: 2027
-- Data for Name: dq_positionalaccuracy; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.dq_positionalaccuracy (t_id, t_seq, atributo21, nombre_medida, identificacion_medida, descripcion_medida, metodo_evaluacion, descripcion_metodo_evaluacion, procedimiento_evaluacion, fecha_hora, resultado, la_punto_exactitud_estimada, puntocontrol_exactitud_estimada, puntolindero_exactitud_estimada, puntolevantamiento_exactitud_estimada) FROM stdin;
\.


--
-- TOC entry 12343 (class 0 OID 335563)
-- Dependencies: 2028
-- Data for Name: extarchivo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.extarchivo (t_id, t_seq, fecha_aceptacion, datos, extraccion, fecha_grabacion, fecha_entrega, s_espacio_de_nombres, s_local_id, col_fuenteadminstrtiva_ext_archivo_id, col_fuenteespacial_ext_archivo_id) FROM stdin;
\.


--
-- TOC entry 12344 (class 0 OID 335570)
-- Dependencies: 2029
-- Data for Name: extdireccion; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.extdireccion (t_id, t_seq, nombre_area_direccion, nombre_edificio, numero_edificio, ciudad, pais, codigo_postal, apartado_correo, departamento, nombre_calle, extunidadedificcnfsica_ext_direccion_id, extinteresado_ext_direccion_id, la_unidadespacial_ext_direccion_id, la_espacjrdcndddfccion_ext_direccion_id, la_espacijrdcrdsrvcios_ext_direccion_id, construccion_ext_direccion_id, terreno_ext_direccion_id, servidumbrepaso_ext_direccion_id, unidadconstruccion_ext_direccion_id, coordenada_direccion) FROM stdin;
\.


--
-- TOC entry 12345 (class 0 OID 335577)
-- Dependencies: 2030
-- Data for Name: extinteresado; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.extinteresado (t_id, t_seq, nombre, extredserviciosfisica_ext_interesado_administrador_id, la_agrupacion_intrsdos_ext_pid, col_interesado_ext_pid) FROM stdin;
\.


--
-- TOC entry 12346 (class 0 OID 335581)
-- Dependencies: 2031
-- Data for Name: extredserviciosfisica; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.extredserviciosfisica (t_id, t_seq, orientada, la_espacijrdcrdsrvcios_ext_id_red_fisica) FROM stdin;
\.


--
-- TOC entry 12347 (class 0 OID 335585)
-- Dependencies: 2032
-- Data for Name: extunidadedificacionfisica; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.extunidadedificacionfisica (t_id, t_seq, la_espacjrdcndddfccion_ext_unidad_edificacion_fisic_id, construccion_ext_unidad_edificacion_fisica_id, unidadconstruccion_ext_unidad_edificacion_fisica_id) FROM stdin;
\.


--
-- TOC entry 12348 (class 0 OID 335589)
-- Dependencies: 2033
-- Data for Name: fraccion; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.fraccion (t_id, t_seq, denominador, numerador, miembros_participacion, col_derecho_compartido, col_restriccion_compartido, predio_copropiedad_coeficiente, col_responsabilidad_compartido, col_hipoteca_compartido) FROM stdin;
\.


--
-- TOC entry 12349 (class 0 OID 335595)
-- Dependencies: 2034
-- Data for Name: gm_multisurface2d; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.gm_multisurface2d (t_id, t_seq) FROM stdin;
\.


--
-- TOC entry 12350 (class 0 OID 335599)
-- Dependencies: 2035
-- Data for Name: gm_multisurface3d; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.gm_multisurface3d (t_id, t_seq) FROM stdin;
\.


--
-- TOC entry 12351 (class 0 OID 335603)
-- Dependencies: 2036
-- Data for Name: gm_surface2dlistvalue; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.gm_surface2dlistvalue (t_id, t_seq, gm_multisurface2d_geometry, avalue) FROM stdin;
\.


--
-- TOC entry 12352 (class 0 OID 335610)
-- Dependencies: 2037
-- Data for Name: gm_surface3dlistvalue; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.gm_surface3dlistvalue (t_id, t_seq, gm_multisurface3d_geometry, avalue) FROM stdin;
\.


--
-- TOC entry 12353 (class 0 OID 335617)
-- Dependencies: 2038
-- Data for Name: hipotecaderecho; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.hipotecaderecho (t_id, t_ili_tid, hipoteca, derecho) FROM stdin;
\.


--
-- TOC entry 12354 (class 0 OID 335621)
-- Dependencies: 2039
-- Data for Name: imagen; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.imagen (t_id, t_seq, uri, extinteresado_huella_dactilar, extinteresado_fotografia, extinteresado_firma) FROM stdin;
\.


--
-- TOC entry 12355 (class 0 OID 335625)
-- Dependencies: 2040
-- Data for Name: interesado_contacto; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.interesado_contacto (t_id, t_ili_tid, telefono1, telefono2, domicilio_notificacion, correo_electronico, origen_datos, interesado) FROM stdin;
\.


--
-- TOC entry 12356 (class 0 OID 335632)
-- Dependencies: 2041
-- Data for Name: iso19125_tipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.iso19125_tipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Disjunto	\N	f	Disjunto	\N
1	Toca	\N	f	Toca	\N
2	Superpone	\N	f	Superpone	\N
3	Desconocido	\N	f	Desconocido	\N
\.


--
-- TOC entry 12357 (class 0 OID 335638)
-- Dependencies: 2042
-- Data for Name: la_agrupacion_interesados; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_agrupacion_interesados (t_id, t_ili_tid, ai_tipo, nombre, tipo, p_espacio_de_nombres, p_local_id, comienzo_vida_util_version, fin_vida_util_version) FROM stdin;
\.


--
-- TOC entry 12358 (class 0 OID 335645)
-- Dependencies: 2043
-- Data for Name: la_agrupacion_interesados_tipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_agrupacion_interesados_tipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Asociacion	\N	f	Asociacion	\N
1	Familia	\N	f	Familia	\N
2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12359 (class 0 OID 335651)
-- Dependencies: 2044
-- Data for Name: la_agrupacionunidadesespaciales; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_agrupacionunidadesespaciales (t_id, t_ili_tid, nivel_jerarquico, etiqueta, nombre, sug_espacio_de_nombres, sug_local_id, aset, comienzo_vida_util_version, fin_vida_util_version, punto_referencia) FROM stdin;
\.


--
-- TOC entry 12360 (class 0 OID 335659)
-- Dependencies: 2045
-- Data for Name: la_baunit; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_baunit (t_id, t_ili_tid, nombre, tipo, u_espacio_de_nombres, u_local_id, comienzo_vida_util_version, fin_vida_util_version) FROM stdin;
\.


--
-- TOC entry 12361 (class 0 OID 335666)
-- Dependencies: 2046
-- Data for Name: la_baunittipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_baunittipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Unidad_Propiedad_Basica	\N	f	Unidad Propiedad Basica	\N
1	Unidad_Derecho	\N	f	Unidad Derecho	\N
2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12362 (class 0 OID 335672)
-- Dependencies: 2047
-- Data for Name: la_cadenacaraslimite; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_cadenacaraslimite (t_id, t_ili_tid, localizacion_textual, ccl_espacio_de_nombres, ccl_local_id, comienzo_vida_util_version, fin_vida_util_version, geometria) FROM stdin;
\.


--
-- TOC entry 12363 (class 0 OID 335679)
-- Dependencies: 2048
-- Data for Name: la_caraslindero; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_caraslindero (t_id, t_ili_tid, localizacion_textual, cl_espacio_de_nombres, cl_local_id, comienzo_vida_util_version, fin_vida_util_version, geometria) FROM stdin;
\.


--
-- TOC entry 12364 (class 0 OID 335686)
-- Dependencies: 2049
-- Data for Name: la_contenidoniveltipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_contenidoniveltipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Derecho_Primario	\N	f	Derecho Primario	\N
1	Consuetudinario	\N	f	Consuetudinario	\N
2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12365 (class 0 OID 335692)
-- Dependencies: 2050
-- Data for Name: la_derechotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_derechotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Propiedad	\N	f	Propiedad	\N
1	Consuetudinario	\N	f	Consuetudinario	\N
2	Arrendamiento	\N	f	Arrendamiento	\N
3	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12366 (class 0 OID 335698)
-- Dependencies: 2051
-- Data for Name: la_dimensiontipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_dimensiontipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Dim2D	\N	f	Dim2D	\N
1	Dim3D	\N	f	Dim3D	\N
2	otro	\N	f	otro	\N
\.


--
-- TOC entry 12367 (class 0 OID 335704)
-- Dependencies: 2052
-- Data for Name: la_espaciojuridicoredservicios; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_espaciojuridicoredservicios (t_id, t_ili_tid, estado, tipo, dimension, etiqueta, relacion_superficie, su_espacio_de_nombres, su_local_id, nivel, uej2_la_unidadespacial, uej2_la_espaciojuridicoredservicios, uej2_la_espaciojuridicounidadedificacion, uej2_servidumbrepaso, uej2_terreno, uej2_construccion, uej2_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, punto_referencia, poligono_creado) FROM stdin;
\.


--
-- TOC entry 12368 (class 0 OID 335711)
-- Dependencies: 2053
-- Data for Name: la_espaciojuridicounidadedificacion; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion (t_id, t_ili_tid, tipo, dimension, etiqueta, relacion_superficie, su_espacio_de_nombres, su_local_id, nivel, uej2_la_unidadespacial, uej2_la_espaciojuridicoredservicios, uej2_la_espaciojuridicounidadedificacion, uej2_servidumbrepaso, uej2_terreno, uej2_construccion, uej2_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, punto_referencia, poligono_creado) FROM stdin;
\.


--
-- TOC entry 12369 (class 0 OID 335718)
-- Dependencies: 2054
-- Data for Name: la_estadodisponibilidadtipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_estadodisponibilidadtipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Original	\N	f	Original	\N
1	Destruido	\N	f	Destruido	\N
2	Incompleto	\N	f	Incompleto	\N
3	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12370 (class 0 OID 335724)
-- Dependencies: 2055
-- Data for Name: la_estadoredserviciostipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_estadoredserviciostipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Planeado	\N	f	Planeado	\N
1	En_Uso	\N	f	En Uso	\N
2	Fuera_De_Servicio	\N	f	Fuera De Servicio	\N
3	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12371 (class 0 OID 335730)
-- Dependencies: 2056
-- Data for Name: la_estructuratipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_estructuratipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Punto	\N	f	Punto	\N
1	Linea	\N	f	Linea	\N
2	Poligono	\N	f	Poligono	\N
3	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12372 (class 0 OID 335736)
-- Dependencies: 2057
-- Data for Name: la_fuenteadministrativatipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_fuenteadministrativatipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Escritura	\N	f	Escritura	\N
1	Titulo	\N	f	Titulo	\N
2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12373 (class 0 OID 335742)
-- Dependencies: 2058
-- Data for Name: la_fuenteespacialtipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_fuenteespacialtipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Topografia	\N	f	Topografia	\N
1	Plano	\N	f	Plano	\N
2	Fotografia_Aerea	\N	f	Fotografia Aerea	\N
3	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12374 (class 0 OID 335748)
-- Dependencies: 2059
-- Data for Name: la_hipotecatipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_hipotecatipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Lineal	\N	f	Lineal	\N
1	Micro_Credito	\N	f	Micro Credito	\N
2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12375 (class 0 OID 335754)
-- Dependencies: 2060
-- Data for Name: la_interesadotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_interesadotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Persona_Natural	\N	f	Persona Natural	\N
1	Persona_No_Natural	\N	f	Persona No Natural	\N
2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12376 (class 0 OID 335760)
-- Dependencies: 2061
-- Data for Name: la_interpolaciontipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_interpolaciontipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Inicio	\N	f	Inicio	\N
1	Final	\N	f	Final	\N
2	Centro_Arco	\N	f	Centro Arco	\N
3	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12377 (class 0 OID 335766)
-- Dependencies: 2062
-- Data for Name: la_monumentaciontipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_monumentaciontipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Baliza	\N	f	Baliza	\N
1	Poste	\N	f	Poste	\N
2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12378 (class 0 OID 335772)
-- Dependencies: 2063
-- Data for Name: la_nivel; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_nivel (t_id, t_ili_tid, nombre, registro_tipo, estructura, tipo, comienzo_vida_util_version, fin_vida_util_version) FROM stdin;
\.


--
-- TOC entry 12379 (class 0 OID 335779)
-- Dependencies: 2064
-- Data for Name: la_punto; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_punto (t_id, t_ili_tid, posicion_interpolacion, monumentacion, puntotipo, p_espacio_de_nombres, p_local_id, ue_la_unidadespacial, ue_la_espaciojuridicoredservicios, ue_la_espaciojuridicounidadedificacion, ue_servidumbrepaso, ue_terreno, ue_construccion, ue_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, localizacion_original) FROM stdin;
\.


--
-- TOC entry 12380 (class 0 OID 335786)
-- Dependencies: 2065
-- Data for Name: la_puntotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_puntotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Control	\N	f	Control	\N
1	Catastro	\N	f	Catastro	\N
2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12381 (class 0 OID 335792)
-- Dependencies: 2066
-- Data for Name: la_redserviciostipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_redserviciostipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Electricidad	\N	f	Electricidad	\N
1	Gas	\N	f	Gas	\N
2	Agua	\N	f	Agua	\N
3	Alcantarillado	\N	f	Alcantarillado	\N
4	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12382 (class 0 OID 335798)
-- Dependencies: 2067
-- Data for Name: la_registrotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_registrotipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Rural	\N	f	Rural	\N
1	Urbano	\N	f	Urbano	\N
2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12383 (class 0 OID 335804)
-- Dependencies: 2068
-- Data for Name: la_relacionnecesariabaunits; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_relacionnecesariabaunits (t_id, t_ili_tid, relacion, comienzo_vida_util_version, fin_vida_util_version) FROM stdin;
\.


--
-- TOC entry 12384 (class 0 OID 335808)
-- Dependencies: 2069
-- Data for Name: la_relacionnecesariaunidadesespaciales; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_relacionnecesariaunidadesespaciales (t_id, t_ili_tid, relacion, comienzo_vida_util_version, fin_vida_util_version) FROM stdin;
\.


--
-- TOC entry 12385 (class 0 OID 335812)
-- Dependencies: 2070
-- Data for Name: la_relacionsuperficietipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_relacionsuperficietipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	En_Rasante	\N	f	En Rasante	\N
1	En_Vuelo	\N	f	En Vuelo	\N
2	En_Subsuelo	\N	f	En Subsuelo	\N
3	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12386 (class 0 OID 335818)
-- Dependencies: 2071
-- Data for Name: la_responsabilidadtipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_responsabilidadtipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Policia_Areas_Inundables	\N	f	Policia Areas Inundables	\N
1	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12387 (class 0 OID 335824)
-- Dependencies: 2072
-- Data for Name: la_restricciontipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_restricciontipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Servidumbres	\N	f	Servidumbres	\N
1	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12388 (class 0 OID 335830)
-- Dependencies: 2073
-- Data for Name: la_tareainteresadotipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_tareainteresadotipo (t_id, t_seq, tipo, la_agrupacion_intrsdos_tarea, col_interesado_tarea) FROM stdin;
\.


--
-- TOC entry 12389 (class 0 OID 335834)
-- Dependencies: 2074
-- Data for Name: la_tareainteresadotipo_tipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_tareainteresadotipo_tipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	topografo	\N	f	topografo	\N
1	notario	\N	f	notario	\N
2	otro	\N	f	otro	\N
\.


--
-- TOC entry 12390 (class 0 OID 335840)
-- Dependencies: 2075
-- Data for Name: la_transformacion; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_transformacion (t_id, t_seq, la_punto_transformacion_y_resultado, puntocontrol_transformacion_y_resultado, puntolindero_transformacion_y_resultado, puntolevantamiento_transformacion_y_resultado, localizacion_transformada) FROM stdin;
\.


--
-- TOC entry 12391 (class 0 OID 335847)
-- Dependencies: 2076
-- Data for Name: la_unidadedificaciontipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_unidadedificaciontipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Privado	\N	f	Privado	\N
1	Comercial	\N	f	Comercial	\N
2	Estado	\N	f	Estado	\N
3	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12392 (class 0 OID 335853)
-- Dependencies: 2077
-- Data for Name: la_unidadespacial; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_unidadespacial (t_id, t_ili_tid, dimension, etiqueta, relacion_superficie, su_espacio_de_nombres, su_local_id, nivel, uej2_la_unidadespacial, uej2_la_espaciojuridicoredservicios, uej2_la_espaciojuridicounidadedificacion, uej2_servidumbrepaso, uej2_terreno, uej2_construccion, uej2_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, punto_referencia, poligono_creado) FROM stdin;
\.


--
-- TOC entry 12393 (class 0 OID 335860)
-- Dependencies: 2078
-- Data for Name: la_volumentipo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_volumentipo (itfcode, ilicode, seq, inactive, dispname, description) FROM stdin;
0	Oficial	\N	f	Oficial	\N
1	Calculado	\N	f	Calculado	\N
2	Otro	\N	f	Otro	\N
\.


--
-- TOC entry 12394 (class 0 OID 335866)
-- Dependencies: 2079
-- Data for Name: la_volumenvalor; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.la_volumenvalor (t_id, t_seq, volumen_medicion, tipo, la_unidadespacial_volumen, la_espacjrdcndddfccion_volumen, la_espacijrdcrdsrvcios_volumen, construccion_volumen, terreno_volumen, servidumbrepaso_volumen, unidadconstruccion_volumen) FROM stdin;
\.


--
-- TOC entry 12395 (class 0 OID 335871)
-- Dependencies: 2080
-- Data for Name: li_lineaje; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.li_lineaje (t_id, t_seq, astatement, la_punto_metodoproduccion, puntocontrol_metodoproduccion, puntolindero_metodoproduccion, puntolevantamiento_metodoproduccion) FROM stdin;
\.


--
-- TOC entry 12396 (class 0 OID 335875)
-- Dependencies: 2081
-- Data for Name: lindero; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.lindero (t_id, t_ili_tid, longitud, localizacion_textual, ccl_espacio_de_nombres, ccl_local_id, comienzo_vida_util_version, fin_vida_util_version, geometria) FROM stdin;
\.


--
-- TOC entry 12397 (class 0 OID 335883)
-- Dependencies: 2082
-- Data for Name: mas; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.mas (t_id, t_ili_tid, clp, uep_la_unidadespacial, uep_la_espaciojuridicoredservicios, uep_la_espaciojuridicounidadedificacion, uep_servidumbrepaso, uep_terreno, uep_construccion, uep_unidadconstruccion) FROM stdin;
\.


--
-- TOC entry 12398 (class 0 OID 335887)
-- Dependencies: 2083
-- Data for Name: masccl; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.masccl (t_id, t_ili_tid, cclp_la_cadenacaraslimite, cclp_lindero, uep_la_unidadespacial, uep_la_espaciojuridicoredservicios, uep_la_espaciojuridicounidadedificacion, uep_servidumbrepaso, uep_terreno, uep_construccion, uep_unidadconstruccion) FROM stdin;
\.


--
-- TOC entry 12399 (class 0 OID 335891)
-- Dependencies: 2084
-- Data for Name: menos; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.menos (t_id, t_ili_tid, ccl_la_cadenacaraslimite, ccl_lindero, eu_la_unidadespacial, eu_la_espaciojuridicoredservicios, eu_la_espaciojuridicounidadedificacion, eu_servidumbrepaso, eu_terreno, eu_construccion, eu_unidadconstruccion) FROM stdin;
\.


--
-- TOC entry 12400 (class 0 OID 335895)
-- Dependencies: 2085
-- Data for Name: menosf; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.menosf (t_id, t_ili_tid, cl, ue_la_unidadespacial, ue_la_espaciojuridicoredservicios, ue_la_espaciojuridicounidadedificacion, ue_servidumbrepaso, ue_terreno, ue_construccion, ue_unidadconstruccion) FROM stdin;
\.


--
-- TOC entry 12401 (class 0 OID 335899)
-- Dependencies: 2086
-- Data for Name: miembros; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.miembros (t_id, t_ili_tid, interesados_la_agrupacion_interesados, interesados_col_interesado, agrupacion) FROM stdin;
\.


--
-- TOC entry 12402 (class 0 OID 335903)
-- Dependencies: 2087
-- Data for Name: oid; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.oid (t_id, t_seq, localid, espaciodenombres, extdireccion_direccion_id, extinteresado_interesado_id, la_nivel_n_id) FROM stdin;
\.


--
-- TOC entry 12403 (class 0 OID 335910)
-- Dependencies: 2088
-- Data for Name: om_observacion; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.om_observacion (t_id, t_seq, col_fuenteespacial_mediciones) FROM stdin;
\.


--
-- TOC entry 12404 (class 0 OID 335914)
-- Dependencies: 2089
-- Data for Name: om_proceso; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.om_proceso (t_id, t_seq, col_fuenteespacial_procedimiento) FROM stdin;
\.


--
-- TOC entry 12405 (class 0 OID 335918)
-- Dependencies: 2090
-- Data for Name: predio; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.predio (t_id, t_ili_tid, departamento, municipio, zona, nupre, fmi, numero_predial, numero_predial_anterior, avaluo_predio, copropiedad, nombre, tipo, u_espacio_de_nombres, u_local_id, comienzo_vida_util_version, fin_vida_util_version) FROM stdin;
\.


--
-- TOC entry 12406 (class 0 OID 335926)
-- Dependencies: 2091
-- Data for Name: predio_copropiedad; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.predio_copropiedad (t_id, t_ili_tid) FROM stdin;
\.


--
-- TOC entry 12407 (class 0 OID 335930)
-- Dependencies: 2092
-- Data for Name: publicidad; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.publicidad (t_id, t_ili_tid, tipo, codigo_registral_publicidad, p_espacio_de_nombres, p_local_id, baunit_la_baunit, baunit_predio, interesado_la_agrupacion_interesados, interesado_col_interesado, comienzo_vida_util_version, fin_vida_util_version) FROM stdin;
\.


--
-- TOC entry 12408 (class 0 OID 335937)
-- Dependencies: 2093
-- Data for Name: publicidadfuente; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.publicidadfuente (t_id, t_ili_tid, publicidad, fuente) FROM stdin;
\.


--
-- TOC entry 12409 (class 0 OID 335941)
-- Dependencies: 2094
-- Data for Name: puntoccl; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.puntoccl (t_id, t_ili_tid, punto_la_punto, punto_puntocontrol, punto_puntolindero, punto_puntolevantamiento, ccl_la_cadenacaraslimite, ccl_lindero) FROM stdin;
\.


--
-- TOC entry 12410 (class 0 OID 335945)
-- Dependencies: 2095
-- Data for Name: puntocl; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.puntocl (t_id, t_ili_tid, punto_la_punto, punto_puntocontrol, punto_puntolindero, punto_puntolevantamiento, cl) FROM stdin;
\.


--
-- TOC entry 12411 (class 0 OID 335949)
-- Dependencies: 2096
-- Data for Name: puntocontrol; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.puntocontrol (t_id, t_ili_tid, nombre_punto, exactitud_vertical, exactitud_horizontal, tipo_punto_control, confiabilidad, posicion_interpolacion, monumentacion, puntotipo, p_espacio_de_nombres, p_local_id, ue_la_unidadespacial, ue_la_espaciojuridicoredservicios, ue_la_espaciojuridicounidadedificacion, ue_servidumbrepaso, ue_terreno, ue_construccion, ue_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, localizacion_original) FROM stdin;
\.


--
-- TOC entry 12412 (class 0 OID 335958)
-- Dependencies: 2097
-- Data for Name: puntofuente; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.puntofuente (t_id, t_ili_tid, pfuente, punto_la_punto, punto_puntocontrol, punto_puntolindero, punto_puntolevantamiento) FROM stdin;
\.


--
-- TOC entry 12413 (class 0 OID 335962)
-- Dependencies: 2098
-- Data for Name: puntolevantamiento; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.puntolevantamiento (t_id, t_ili_tid, tipo_punto_levantamiento, definicion_punto, exactitud_vertical, exactitud_horizontal, nombre_punto, posicion_interpolacion, monumentacion, puntotipo, p_espacio_de_nombres, p_local_id, ue_la_unidadespacial, ue_la_espaciojuridicoredservicios, ue_la_espaciojuridicounidadedificacion, ue_servidumbrepaso, ue_terreno, ue_construccion, ue_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, localizacion_original) FROM stdin;
\.


--
-- TOC entry 12414 (class 0 OID 335971)
-- Dependencies: 2099
-- Data for Name: puntolindero; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.puntolindero (t_id, t_ili_tid, acuerdo, definicion_punto, descripcion_punto, exactitud_vertical, exactitud_horizontal, confiabilidad, nombre_punto, posicion_interpolacion, monumentacion, puntotipo, p_espacio_de_nombres, p_local_id, ue_la_unidadespacial, ue_la_espaciojuridicoredservicios, ue_la_espaciojuridicounidadedificacion, ue_servidumbrepaso, ue_terreno, ue_construccion, ue_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, localizacion_original) FROM stdin;
\.


--
-- TOC entry 12415 (class 0 OID 335980)
-- Dependencies: 2100
-- Data for Name: relacionbaunit; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.relacionbaunit (t_id, t_ili_tid, unidad1_la_baunit, unidad1_predio, unidad2_la_baunit, unidad2_predio) FROM stdin;
\.


--
-- TOC entry 12416 (class 0 OID 335984)
-- Dependencies: 2101
-- Data for Name: relacionfuente; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.relacionfuente (t_id, t_ili_tid, refuente, relacionrequeridabaunit) FROM stdin;
\.


--
-- TOC entry 12417 (class 0 OID 335988)
-- Dependencies: 2102
-- Data for Name: relacionfuenteuespacial; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.relacionfuenteuespacial (t_id, t_ili_tid, rfuente, relacionrequeridaue) FROM stdin;
\.


--
-- TOC entry 12418 (class 0 OID 335992)
-- Dependencies: 2103
-- Data for Name: relacionue; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.relacionue (t_id, t_ili_tid, rue1_la_unidadespacial, rue1_la_espaciojuridicoredservicios, rue1_la_espaciojuridicounidadedificacion, rue1_servidumbrepaso, rue1_terreno, rue1_construccion, rue1_unidadconstruccion, rue2_la_unidadespacial, rue2_la_espaciojuridicoredservicios, rue2_la_espaciojuridicounidadedificacion, rue2_servidumbrepaso, rue2_terreno, rue2_construccion, rue2_unidadconstruccion) FROM stdin;
\.


--
-- TOC entry 12419 (class 0 OID 335996)
-- Dependencies: 2104
-- Data for Name: responsablefuente; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.responsablefuente (t_id, t_ili_tid, cfuente, notario_la_agrupacion_interesados, notario_col_interesado) FROM stdin;
\.


--
-- TOC entry 12420 (class 0 OID 336000)
-- Dependencies: 2105
-- Data for Name: rrrfuente; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.rrrfuente (t_id, t_ili_tid, rfuente, rrr_col_responsabilidad, rrr_col_derecho, rrr_col_restriccion, rrr_col_hipoteca) FROM stdin;
\.


--
-- TOC entry 12421 (class 0 OID 336004)
-- Dependencies: 2106
-- Data for Name: servidumbrepaso; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.servidumbrepaso (t_id, t_ili_tid, identificador, fecha_inscripcion_catastral, dimension, etiqueta, relacion_superficie, su_espacio_de_nombres, su_local_id, nivel, uej2_la_unidadespacial, uej2_la_espaciojuridicoredservicios, uej2_la_espaciojuridicounidadedificacion, uej2_servidumbrepaso, uej2_terreno, uej2_construccion, uej2_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, punto_referencia, poligono_creado) FROM stdin;
\.


--
-- TOC entry 12422 (class 0 OID 336011)
-- Dependencies: 2107
-- Data for Name: t_ili2db_attrname; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_attrname (iliname, sqlname, owner, target) FROM stdin;
LADM_COL_V1_1.LADM_Nucleo.puntoCl.punto	punto_puntolindero	puntocl	puntolindero
LADM_COL_V1_1.LADM_Nucleo.miembros.interesados	interesados_la_agrupacion_interesados	miembros	la_agrupacion_interesados
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Restriccion.Codigo_Registral_Restriccion	codigo_registral_restriccion	col_hipoteca	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Descripcion_Metodo_Evaluacion	descripcion_metodo_evaluacion	dq_element	\N
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoRedServicios.ext_ID_Red_Fisica	la_espacijrdcrdsrvcios_ext_id_red_fisica	extredserviciosfisica	la_espaciojuridicoredservicios
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.predio_copropiedad.copropiedad	copropiedad	predio	predio
LADM_COL_V1_1.LADM_Nucleo.LA_TareaInteresadoTipo.Tipo	tipo	la_tareainteresadotipo	\N
LADM_COL_V1_1.LADM_Nucleo.ExtRedServiciosFisica.Orientada	orientada	extredserviciosfisica	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Descripcion	descripcion	col_derecho	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Restriccion.Interesado_Requerido	interesado_requerido	col_restriccion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Espacio_De_Nombres	su_espacio_de_nombres	unidadconstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_unidadconstruccion	puntolevantamiento	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.poligono_creado	poligono_creado	la_unidadespacial	\N
LADM_COL_V1_1.LADM_Nucleo.ueUeGrupo.parte	parte_construccion	ueuegrupo	construccion
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_unidadconstruccion	la_punto	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	la_cadenacaraslimite_calidad	dq_element	la_cadenacaraslimite
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.poligono_creado	poligono_creado	construccion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID	servidumbrepaso_ext_direccion_id	extdireccion	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.relacionBaunit.unidad1	unidad1_predio	relacionbaunit	predio
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion.Departamento	departamento	extdireccion	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Predio.Municipio	municipio	predio	\N
LADM_COL_V1_1.LADM_Nucleo.puntoFuente.punto	punto_puntolevantamiento	puntofuente	puntolevantamiento
LADM_COL_V1_1.LADM_Nucleo.miembros.interesados	interesados_col_interesado	miembros	col_interesado
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	la_agrupacion_interesados	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicounidadedificacion	construccion	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion.Apartado_Correo	apartado_correo	extdireccion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Uso_Efectivo	uso_efectivo	col_hipoteca	\N
LADM_COL_V1_1.LADM_Nucleo.rrrFuente.rrr	rrr_col_derecho	rrrfuente	col_derecho
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Posicion_Interpolacion	posicion_interpolacion	puntocontrol	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Uso_Efectivo	uso_efectivo	col_restriccion	\N
LADM_COL_V1_1.LADM_Nucleo.mas.ueP	uep_terreno	mas	terreno
LADM_COL_V1_1.LADM_Nucleo.CI_ParteResponsable.Nombre_Individual	nombre_individual	ci_parteresponsable	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Fecha_Hora	fecha_hora	dq_positionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.p_Local_Id	p_local_id	col_interesado	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Restriccion.Interesado_Requerido	interesado_requerido	col_hipoteca	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Relacion_Superficie	relacion_superficie	unidadconstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.menosf.ue	ue_la_espaciojuridicounidadedificacion	menosf	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Localizacion_Original	localizacion_original	puntocontrol	\N
LADM_COL_V1_1.LADM_Nucleo.ueUeGrupo.parte	parte_la_unidadespacial	ueuegrupo	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	la_cadenacaraslimite_procedencia	ci_parteresponsable	la_cadenacaraslimite
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	col_hipoteca	\N
LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit.Nombre	nombre	predio	\N
LADM_COL_V1_1.LADM_Nucleo.LA_AgrupacionUnidadesEspaciales.Nombre	nombre	la_agrupacionunidadesespaciales	\N
LADM_COL_V1_1.LADM_Nucleo.CI_Contacto.Telefono	telefono	ci_contacto	\N
LADM_COL_V1_1.LADM_Nucleo.CI_ParteResponsable.Funcion	funcion	ci_parteresponsable	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_terreno	puntocontrol	terreno
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_unidadespacial	servidumbrepaso	la_unidadespacial
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLindero.Definicion_Punto	definicion_punto	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_construccion	servidumbrepaso	construccion
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.s_Local_Id	s_local_id	col_fuenteadministrativa	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicounidadedificacion	la_espaciojuridicoredservicios	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.puntoFuente.pfuente	pfuente	puntofuente	col_fuenteespacial
LADM_COL_V1_1.LADM_Nucleo.baunitComoInteresado.unidad	unidad_predio	baunitcomointeresado	predio
LADM_COL_V1_1.LADM_Nucleo.ExtInteresado.Interesado_ID	extinteresado_interesado_id	oid	extinteresado
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	la_espacijrdcrdsrvcios_procedencia	ci_parteresponsable	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Descripcion_Medida	descripcion_medida	dq_element	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Identificacion_Medida	identificacion_medida	dq_element	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Explotacion	terreno_explotacion	col_explotaciontipo_terreno_explotacion	terreno
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue2	rue2_unidadconstruccion	relacionue	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen	servidumbrepaso_volumen	la_volumenvalor	servidumbrepaso
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.ConstruccionUnidadConstruccion.construccion	construccion	unidadconstruccion	construccion
LADM_COL_V1_1.LADM_Nucleo.menosf.ue	ue_la_unidadespacial	menosf	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion.Tipo	tipo	construccion	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.UnidadConstruccion.Avaluo_Unidad_Construccion	avaluo_unidad_construccion	unidadconstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	col_restriccion	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	servidumbrepaso_procedencia	ci_parteresponsable	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.ueFuente.ue	ue_servidumbrepaso	uefuente	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	construccion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.r_Espacio_De_Nombres	r_espacio_de_nombres	col_restriccion	\N
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Sello_Inicio_Validez	sello_inicio_validez	col_fuenteespacial	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.r_Espacio_De_Nombres	r_espacio_de_nombres	col_hipoteca	\N
LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit.u_Espacio_De_Nombres	u_espacio_de_nombres	la_baunit	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLindero.Exactitud_Horizontal	exactitud_horizontal	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.relacionFuente.refuente	refuente	relacionfuente	col_fuenteadministrativa
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado.Organo_Emisor	organo_emisor	col_interesado	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_construccion	la_punto	construccion
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Publicidad.p_Espacio_De_Nombres	p_espacio_de_nombres	publicidad	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_unidadconstruccion	puntolindero	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	la_espacijrdcrdsrvcios_calidad	dq_element	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	puntolevantamiento_calidad	dq_element	puntolevantamiento
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	la_espaciojuridicounidadedificacion	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_servidumbrepaso	unidadconstruccion	servidumbrepaso
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLevantamiento.Nombre_Punto	nombre_punto	puntolevantamiento	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	la_nivel	\N
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion.Tipo	tipo	la_espaciojuridicounidadedificacion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.poligono_creado	poligono_creado	la_espaciojuridicoredservicios	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicounidadedificacion	la_unidadespacial	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	terreno	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area	unidadconstruccion_area	col_areavalor	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.LA_Nivel.Tipo	tipo	la_nivel	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Comprobacion_Comparte	comprobacion_comparte	col_hipoteca	\N
LADM_COL_V1_1.LADM_Nucleo.menos.eu	eu_unidadconstruccion	menos	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Comprobacion_Comparte	comprobacion_comparte	col_restriccion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area	la_unidadespacial_area	col_areavalor	la_unidadespacial
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Publicidad.Codigo_Registral_Publicidad	codigo_registral_publicidad	publicidad	\N
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion.Ext_Unidad_Edificacion_Fisica_ID	unidadconstruccion_ext_unidad_edificacion_fisica_id	extunidadedificacionfisica	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.LA_VolumenValor.Tipo	tipo	la_volumenvalor	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID	terreno_ext_direccion_id	extdireccion	terreno
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.s_Local_Id	s_local_id	col_fuenteespacial	\N
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue1	rue1_unidadconstruccion	relacionue	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_unidadconstruccion	servidumbrepaso	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Nombre_Medida	nombre_medida	dq_absoluteexternalpositionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area	la_espacjrdcndddfccion_area	col_areavalor	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_construccion	construccion	construccion
LADM_COL_V1_1.LADM_Nucleo.rrrInteresado.interesado	interesado_col_interesado	col_hipoteca	col_interesado
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_la_unidadespacial	la_punto	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.MetodoProduccion	puntolindero_metodoproduccion	li_lineaje	puntolindero
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	col_hipoteca_calidad	dq_element	col_hipoteca
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Area_Registral	area_registral	terreno	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	la_cadenacaraslimite	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	terreno_calidad	dq_element	terreno
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Nombre_Medida	nombre_medida	dq_element	\N
LADM_COL_V1_1.LADM_Nucleo.baunitComoInteresado.unidad	unidad_la_baunit	baunitcomointeresado	la_baunit
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_la_espaciojuridicoredservicios	puntolindero	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.s_Espacio_De_Nombres	s_espacio_de_nombres	col_fuenteadministrativa	\N
LADM_COL_V1_1.LADM_Nucleo.CI_ParteResponsable.Informacion_Contacto	ci_parteresponsable_informacion_contacto	ci_contacto	ci_parteresponsable
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Dimension	dimension	la_unidadespacial	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Compartido	col_restriccion_compartido	fraccion	col_restriccion
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.poligono_creado	poligono_creado	la_espaciojuridicounidadedificacion	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLevantamiento.Definicion_Punto	definicion_punto	puntolevantamiento	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	terreno	\N
LADM_COL_V1_1.LADM_Nucleo.ueNivel.nivel	nivel	terreno	la_nivel
LADM_COL_V1_1.LADM_Nucleo.ueUeGrupo.parte	parte_unidadconstruccion	ueuegrupo	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.ueFuente.ue	ue_terreno	uefuente	terreno
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_construccion	la_espaciojuridicoredservicios	construccion
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoControl.Confiabilidad	confiabilidad	puntocontrol	\N
LADM_COL_V1_1.LADM_Nucleo.rrrInteresado.interesado	interesado_col_interesado	col_restriccion	col_interesado
Catastro_Registro_Nucleo_V2_2_1.COL_CuerpoAgua_Terreno_Evidencia_Cuerpo_Agua.value	avalue	col_cuerpoagua_terreno_evidencia_cuerpo_agua	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Transformacion_Y_Resultado	puntolindero_transformacion_y_resultado	la_transformacion	puntolindero
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicounidadedificacion	servidumbrepaso	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.Fraccion.Numerador	numerador	fraccion	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_unidadespacial	construccion	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	la_baunit_procedencia	ci_parteresponsable	la_baunit
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado.Documento_Identidad	documento_identidad	col_interesado	\N
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion.Numero_Edificio	numero_edificio	extdireccion	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Afectacion	terreno_afectacion	col_afectacion_terreno_afectacion	terreno
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.PuntoTipo	puntotipo	puntolevantamiento	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	la_relacionnecesrbnits_calidad	dq_element	la_relacionnecesariabaunits
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	col_hipoteca_procedencia	ci_parteresponsable	col_hipoteca
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	la_agrupacionunidadesespaciales	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_construccion	puntolevantamiento	construccion
LADM_COL_V1_1.LADM_Nucleo.rrrInteresado.interesado	interesado_la_agrupacion_interesados	col_hipoteca	la_agrupacion_interesados
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoRedServicios.Estado	estado	la_espaciojuridicoredservicios	\N
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue2	rue2_la_espaciojuridicoredservicios	relacionue	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.menos.eu	eu_la_espaciojuridicoredservicios	menos	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.masCcl.ueP	uep_la_espaciojuridicoredservicios	masccl	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.p_Local_Id	p_local_id	puntolevantamiento	\N
LADM_COL_V1_1.LADM_Nucleo.rrrInteresado.interesado	interesado_la_agrupacion_interesados	col_restriccion	la_agrupacion_interesados
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID	col_fuenteespacial_ext_archivo_id	extarchivo	col_fuenteespacial
LADM_COL_V1_1.LADM_Nucleo.relacionFuenteUespacial.rfuente	rfuente	relacionfuenteuespacial	col_fuenteespacial
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion.Direccion_ID	extdireccion_direccion_id	oid	extdireccion
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_unidadconstruccion	la_espaciojuridicoredservicios	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.poligono_creado	poligono_creado	terreno	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_la_espaciojuridicounidadedificacion	puntolevantamiento	la_espaciojuridicounidadedificacion
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadFuente.fuente	fuente	publicidadfuente	col_fuenteadministrativa
LADM_COL_V1_1.LADM_Nucleo.rrrFuente.rfuente	rfuente	rrrfuente	col_fuenteadministrativa
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadBAUnit.baunit	baunit_predio	publicidad	predio
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion.Coordenada_Direccion	coordenada_direccion	extdireccion	\N
LADM_COL_V1_1.LADM_Nucleo.relacionBaunit.unidad2	unidad2_predio	relacionbaunit	predio
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoRedServicios.Tipo	tipo	la_espaciojuridicoredservicios	\N
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion.Ext_Unidad_Edificacion_Fisica_ID	construccion_ext_unidad_edificacion_fisica_id	extunidadedificacionfisica	construccion
LADM_COL_V1_1.LADM_Nucleo.mas.ueP	uep_servidumbrepaso	mas	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite.ccl_Espacio_De_Nombres	ccl_espacio_de_nombres	lindero	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	col_restriccion_procedencia	ci_parteresponsable	col_restriccion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	la_baunit_calidad	dq_element	la_baunit
LADM_COL_V1_1.LADM_Nucleo.CC_MetodoOperacion.Ddimensiones_Objetivo	ddimensiones_objetivo	cc_metodooperacion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Etiqueta	etiqueta	terreno	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Restriccion.Codigo_Registral_Restriccion	codigo_registral_restriccion	col_restriccion	\N
ISO19107_V1_MAGNABOG.GM_Surface2DListValue.value	avalue	gm_surface2dlistvalue	\N
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion.Ciudad	ciudad	extdireccion	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	lindero	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.menosf.cl	cl	menosf	la_caraslindero
LADM_COL_V1_1.LADM_Nucleo.masCcl.cclP	cclp_la_cadenacaraslimite	masccl	la_cadenacaraslimite
LADM_COL_V1_1.LADM_Nucleo.LA_AgrupacionUnidadesEspaciales.sug_Espacio_De_Nombres	sug_espacio_de_nombres	la_agrupacionunidadesespaciales	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Interesado_Contacto.Telefono2	telefono2	interesado_contacto	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.UnidadConstruccion.Numero_Pisos	numero_pisos	unidadconstruccion	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Derecho.Codigo_Registral_Derecho	codigo_registral_derecho	col_derecho	\N
LADM_COL_V1_1.LADM_Nucleo.ueNivel.nivel	nivel	la_espaciojuridicounidadedificacion	la_nivel
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	la_espaciojuridicounidadedificacion	\N
LADM_COL_V1_1.LADM_Nucleo.baunitRrr.unidad	unidad_la_baunit	col_responsabilidad	la_baunit
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoControl.Tipo_Punto_Control	tipo_punto_control	puntocontrol	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_unidadespacial	la_unidadespacial	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue1	rue1_la_espaciojuridicoredservicios	relacionue	la_espaciojuridicoredservicios
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Bosque_Area_Seminaturale	terreno_bosque_area_seminaturale	col_bosqueareasemi_terreno_bosque_area_seminaturale	terreno
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	servidumbrepaso	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	la_espaciojuridicoredservicios	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area	construccion_area	col_areavalor	construccion
LADM_COL_V1_1.LADM_Nucleo.masCcl.ueP	uep_unidadconstruccion	masccl	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	la_relacionnecesrbnits_procedencia	ci_parteresponsable	la_relacionnecesariabaunits
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID	la_espacijrdcrdsrvcios_ext_direccion_id	extdireccion	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	la_cadenacaraslimite	\N
LADM_COL_V1_1.LADM_Nucleo.ueFuente.ue	ue_la_espaciojuridicoredservicios	uefuente	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.Nombre	nombre	la_agrupacion_interesados	\N
LADM_COL_V1_1.LADM_Nucleo.responsableFuente.cfuente	cfuente	responsablefuente	col_fuenteadministrativa
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Sello_Inicio_Validez	sello_inicio_validez	col_fuenteadministrativa	\N
LADM_COL_V1_1.LADM_Nucleo.baunitRrr.unidad	unidad_predio	col_responsabilidad	predio
LADM_COL_V1_1.LADM_Nucleo.rrrFuente.rrr	rrr_col_hipoteca	rrrfuente	col_hipoteca
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLindero.Descripcion_Punto	descripcion_punto	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.puntoFuente.punto	punto_puntocontrol	puntofuente	puntocontrol
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Publicidad.Tipo	tipo	publicidad	\N
ISO19107_V1_MAGNABOG.GM_MultiSurface2D.geometry	gm_multisurface2d_geometry	gm_surface2dlistvalue	gm_multisurface2d
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Fecha_Entrega	fecha_entrega	col_fuenteadministrativa	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.p_Local_Id	p_local_id	la_agrupacion_interesados	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	col_restriccion_calidad	dq_element	col_restriccion
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_la_espaciojuridicounidadedificacion	puntolindero	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	unidadconstruccion_calidad	dq_element	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	la_punto_procedencia	ci_parteresponsable	la_punto
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_unidadconstruccion	unidadconstruccion	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.relacionFuenteUespacial.relacionrequeridaUe	relacionrequeridaue	relacionfuenteuespacial	la_relacionnecesariaunidadesespaciales
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Interesado_Contacto.Correo_Electronico	correo_electronico	interesado_contacto	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado.Fecha_Emision	fecha_emision	col_interesado	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.predio_copropiedad.coeficiente	predio_copropiedad_coeficiente	fraccion	predio_copropiedad
LADM_COL_V1_1.LADM_Nucleo.ueFuente.ue	ue_unidadconstruccion	uefuente	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteEspacial.Procedimiento	col_fuenteespacial_procedimiento	om_proceso	col_fuenteespacial
LADM_COL_V1_1.LADM_Nucleo.menos.ccl	ccl_lindero	menos	lindero
LADM_COL_V1_1.LADM_Nucleo.puntoCcl.punto	punto_puntolindero	puntoccl	puntolindero
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue1	rue1_construccion	relacionue	construccion
LADM_COL_V1_1.LADM_Nucleo.relacionBaunit.unidad2	unidad2_la_baunit	relacionbaunit	la_baunit
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_unidadconstruccion	construccion	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.masCcl.ueP	uep_servidumbrepaso	masccl	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit.Tipo	tipo	la_baunit	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Nombre_Medida	nombre_medida	dq_positionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.p_Espacio_De_Nombres	p_espacio_de_nombres	la_punto	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_unidadespacial	terreno	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Compartido	col_hipoteca_compartido	fraccion	col_hipoteca
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_terreno	la_espaciojuridicounidadedificacion	terreno
LADM_COL_V1_1.LADM_Nucleo.ueFuente.pfuente	pfuente	uefuente	col_fuenteespacial
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	puntocontrol_procedencia	ci_parteresponsable	puntocontrol
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue1	rue1_la_unidadespacial	relacionue	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.ueFuente.ue	ue_construccion	uefuente	construccion
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado.Segundo_Nombre	segundo_nombre	col_interesado	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	col_interesado	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID	unidadconstruccion_ext_direccion_id	extdireccion	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue2	rue2_la_unidadespacial	relacionue	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Procedencia	col_fuenteadminstrtiva_procedencia	ci_parteresponsable	col_fuenteadministrativa
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_la_espaciojuridicoredservicios	puntolevantamiento	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion.Nombre_Area_Direccion	nombre_area_direccion	extdireccion	\N
LADM_COL_V1_1.LADM_Nucleo.ueUeGrupo.todo	todo	ueuegrupo	la_agrupacionunidadesespaciales
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLindero.Acuerdo	acuerdo	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_servidumbrepaso	terreno	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.LA_VolumenValor.Volumen_Medicion	volumen_medicion	la_volumenvalor	\N
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteEspacial.Mediciones	col_fuenteespacial_mediciones	om_observacion	col_fuenteespacial
LADM_COL_V1_1.LADM_Nucleo.ueBaunit.ue	ue_servidumbrepaso	uebaunit	servidumbrepaso
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Predio.Zona	zona	predio	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.p_Espacio_De_Nombres	p_espacio_de_nombres	puntolevantamiento	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen	terreno_volumen	la_volumenvalor	terreno
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen	la_unidadespacial_volumen	la_volumenvalor	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.puntoCcl.punto	punto_puntolevantamiento	puntoccl	puntolevantamiento
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	puntocontrol	\N
LADM_COL_V1_1.LADM_Nucleo.unidadFuente.ufuente	ufuente	unidadfuente	col_fuenteadministrativa
LADM_COL_V1_1.LADM_Nucleo.menos.ccl	ccl_la_cadenacaraslimite	menos	la_cadenacaraslimite
LADM_COL_V1_1.LADM_Nucleo.ueBaunit.ue	ue_la_espaciojuridicounidadedificacion	uebaunit	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.rrrInteresado.interesado	interesado_col_interesado	col_derecho	col_interesado
LADM_COL_V1_1.LADM_Nucleo.baunitRrr.unidad	unidad_predio	col_restriccion	predio
LADM_COL_V1_1.LADM_Nucleo.menos.eu	eu_servidumbrepaso	menos	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	la_caraslindero_calidad	dq_element	la_caraslindero
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_terreno	puntolindero	terreno
LADM_COL_V1_1.LADM_Nucleo.ExtInteresado.Firma	extinteresado_firma	imagen	extinteresado
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue2	rue2_servidumbrepaso	relacionue	servidumbrepaso
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Interesado_Contacto.Origen_Datos	origen_datos	interesado_contacto	\N
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Tipo_Principal	tipo_principal	col_fuenteespacial	\N
LADM_COL_V1_1.LADM_Nucleo.rrrFuente.rrr	rrr_col_responsabilidad	rrrfuente	col_responsabilidad
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	col_derecho_calidad	dq_element	col_derecho
LADM_COL_V1_1.LADM_Nucleo.miembros.participacion	miembros_participacion	fraccion	miembros
LADM_COL_V1_1.LADM_Nucleo.responsableFuente.notario	notario_la_agrupacion_interesados	responsablefuente	la_agrupacion_interesados
LADM_COL_V1_1.LADM_Nucleo.relacionBaunit.unidad1	unidad1_la_baunit	relacionbaunit	la_baunit
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	terreno_procedencia	ci_parteresponsable	terreno
LADM_COL_V1_1.LADM_Nucleo.baunitFuente.bfuente	bfuente	baunitfuente	col_fuenteespacial
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	la_agrupacion_interesados	\N
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Oficialidad	oficialidad	col_fuenteadministrativa	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	publicidad_procedencia	ci_parteresponsable	publicidad
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicoredservicios	servidumbrepaso	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Descripcion_Medida	descripcion_medida	dq_absoluteexternalpositionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.r_Local_Id	r_local_id	col_derecho	\N
LADM_COL_V1_1.LADM_Nucleo.mas.ueP	uep_la_espaciojuridicoredservicios	mas	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.ueUeGrupo.parte	parte_servidumbrepaso	ueuegrupo	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicoredservicios	la_espaciojuridicoredservicios	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	la_unidadespacial_procedencia	ci_parteresponsable	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Calidad	col_fuenteespacial_calidad	dq_element	col_fuenteespacial
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Espacio_De_Nombres	su_espacio_de_nombres	terreno	\N
LADM_COL_V1_1.LADM_Nucleo.masCcl.ueP	uep_construccion	masccl	construccion
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_construccion	la_unidadespacial	construccion
LADM_COL_V1_1.LADM_Nucleo.menos.eu	eu_la_unidadespacial	menos	la_unidadespacial
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Territorio_Agricola	terreno_territorio_agricola	col_territorioagricola_terreno_territorio_agricola	terreno
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicounidadedificacion	la_espaciojuridicounidadedificacion	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.p_Espacio_De_Nombres	p_espacio_de_nombres	col_interesado	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Predio.Avaluo_Predio	avaluo_predio	predio	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Predio.Numero_Predial	numero_predial	predio	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	predio	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Nivel.Registro_Tipo	registro_tipo	la_nivel	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	col_responsabilidad	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicoredservicios	construccion	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue1	rue1_servidumbrepaso	relacionue	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.LA_CarasLindero.Geometria	geometria	la_caraslindero	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.poligono_creado	poligono_creado	servidumbrepaso	\N
LADM_COL_V1_1.LADM_Nucleo.COL_AreaValor.areaSize	areasize	col_areavalor	\N
LADM_COL_V1_1.LADM_Nucleo.Imagen.uri	uri	imagen	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.ServidumbrePaso.Fecha_Inscripcion_Catastral	fecha_inscripcion_catastral	servidumbrepaso	\N
LADM_COL_V1_1.LADM_Nucleo.baunitRrr.unidad	unidad_predio	col_hipoteca	predio
LADM_COL_V1_1.LADM_Nucleo.mas.ueP	uep_unidadconstruccion	mas	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area	servidumbrepaso_area	col_areavalor	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.PuntoTipo	puntotipo	la_punto	\N
LADM_COL_V1_1.LADM_Nucleo.CC_MetodoOperacion.Formula	formula	cc_metodooperacion	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	la_nivel	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Hipoteca.h_Tipo	h_tipo	col_hipoteca	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Agrupacion_Interesados.ai_Tipo	ai_tipo	la_agrupacion_interesados	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.ext_PID	la_agrupacion_intrsdos_ext_pid	extinteresado	la_agrupacion_interesados
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_la_espaciojuridicoredservicios	la_punto	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Punto_Referencia	punto_referencia	terreno	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	predio_calidad	dq_element	predio
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Tipo_Principal	tipo_principal	col_fuenteadministrativa	\N
LADM_COL_V1_1.LADM_Nucleo.puntoCl.punto	punto_la_punto	puntocl	la_punto
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_construccion	terreno	construccion
LADM_COL_V1_1.LADM_Nucleo.ExtArchivo.Extraccion	extraccion	extarchivo	\N
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Oficialidad	oficialidad	col_fuenteespacial	\N
LADM_COL_V1_1.LADM_Nucleo.mas.ueP	uep_construccion	mas	construccion
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_la_espaciojuridicounidadedificacion	puntocontrol	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	la_relacionnecesariabaunits	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID	construccion_ext_direccion_id	extdireccion	construccion
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID	la_unidadespacial_ext_direccion_id	extdireccion	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	puntolevantamiento	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	la_unidadespacial	\N
LADM_COL_V1_1.LADM_Nucleo.ueFuente.ue	ue_la_unidadespacial	uefuente	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	puntolindero_procedencia	ci_parteresponsable	puntolindero
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicoredservicios	la_unidadespacial	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.puntoCcl.punto	punto_puntocontrol	puntoccl	puntocontrol
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicoredservicios	unidadconstruccion	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	col_derecho	\N
LADM_COL_V1_1.LADM_Nucleo.OM_Observacion.Resultado_Calidad	om_observacion_resultado_calidad	dq_element	om_observacion
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.Tarea	la_agrupacion_intrsdos_tarea	la_tareainteresadotipo	la_agrupacion_interesados
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	col_restriccion	\N
LADM_COL_V1_1.LADM_Nucleo.ExtArchivo.Fecha_Grabacion	fecha_grabacion	extarchivo	\N
LADM_COL_V1_1.LADM_Nucleo.CI_Contacto.Horario_De_Atencion	horario_de_atencion	ci_contacto	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	la_agrupacinnddsspcles_calidad	dq_element	la_agrupacionunidadesespaciales
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	puntolevantamiento_procedencia	ci_parteresponsable	puntolevantamiento
LADM_COL_V1_1.LADM_Nucleo.ueBaunit.ue	ue_terreno	uebaunit	terreno
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Evidencia_Cuerpo_Agua	terreno_evidencia_cuerpo_agua	col_cuerpoagua_terreno_evidencia_cuerpo_agua	terreno
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.p_Local_Id	p_local_id	la_punto	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Localizacion_Original	localizacion_original	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue2	rue2_construccion	relacionue	construccion
LADM_COL_V1_1.LADM_Nucleo.LA_AgrupacionUnidadesEspaciales.Punto_Referencia	punto_referencia	la_agrupacionunidadesespaciales	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Area_Calculada	area_calculada	terreno	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Construccion.Area_Construccion	area_construccion	construccion	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	col_hipoteca	\N
LADM_COL_V1_1.LADM_Nucleo.ExtInteresado.Nombre	nombre	extinteresado	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadBAUnit.baunit	baunit_la_baunit	publicidad	la_baunit
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.poligono_creado	poligono_creado	unidadconstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.mas.clP	clp	mas	la_caraslindero
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Resultado	resultado	dq_positionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	la_relacionnecesariaunidadesespaciales	\N
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Fecha_Aceptacion	fecha_aceptacion	col_fuenteespacial	\N
LADM_COL_V1_1.LADM_Nucleo.puntoCl.punto	punto_puntolevantamiento	puntocl	puntolevantamiento
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Responsabilidad.Codigo_Registral_Responsabilidad	codigo_registral_responsabilidad	col_responsabilidad	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.hipotecaDerecho.derecho	derecho	hipotecaderecho	col_derecho
LADM_COL_V1_1.LADM_Nucleo.menos.eu	eu_construccion	menos	construccion
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_unidadconstruccion	la_unidadespacial	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.masCcl.ueP	uep_la_unidadespacial	masccl	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit.u_Local_Id	u_local_id	predio	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	la_nivel_calidad	dq_element	la_nivel
LADM_COL_V1_1.LADM_Nucleo.LA_CarasLindero.Localizacion_Textual	localizacion_textual	la_caraslindero	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.MetodoProduccion	la_punto_metodoproduccion	li_lineaje	la_punto
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion.Codigo_Postal	codigo_postal	extdireccion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Etiqueta	etiqueta	servidumbrepaso	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_servidumbrepaso	la_unidadespacial	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Compartido	col_derecho_compartido	fraccion	col_derecho
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Relacion_Superficie	relacion_superficie	construccion	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado.Genero	genero	col_interesado	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	publicidad	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Transformacion_Y_Resultado	la_punto_transformacion_y_resultado	la_transformacion	la_punto
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_servidumbrepaso	construccion	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	col_interesado	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Construccion.Avaluo_Construccion	avaluo_construccion	construccion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Monumentacion	monumentacion	la_punto	\N
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion.Tipo	tipo	unidadconstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteAdministrativa.Nombre	nombre	col_fuenteadministrativa	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Interesado_Contacto.Domicilio_Notificacion	domicilio_notificacion	interesado_contacto	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Relacion_Superficie	relacion_superficie	la_unidadespacial	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Nivel.Estructura	estructura	la_nivel	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	la_relacionnecesariaunidadesespaciales	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Comprobacion_Comparte	comprobacion_comparte	col_derecho	\N
LADM_COL_V1_1.LADM_Nucleo.ueUeGrupo.parte	parte_terreno	ueuegrupo	terreno
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	unidadconstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	la_espacjrdcndddfccion_calidad	dq_element	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	lindero_calidad	dq_element	lindero
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.r_Espacio_De_Nombres	r_espacio_de_nombres	col_responsabilidad	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_PositionalAccuracy.atributo21	atributo21	dq_absoluteexternalpositionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Espacio_De_Nombres	su_espacio_de_nombres	la_unidadespacial	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Lindero.Longitud	longitud	lindero	\N
LADM_COL_V1_1.LADM_Nucleo.CI_ParteResponsable.Nombre_Organizacion	nombre_organizacion	ci_parteresponsable	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	la_nivel_procedencia	ci_parteresponsable	la_nivel
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Procedencia	col_fuenteespacial_procedencia	ci_parteresponsable	col_fuenteespacial
LADM_COL_V1_1.LADM_Nucleo.ExtRedServiciosFisica.Ext_Interesado_Administrador_ID	extredserviciosfisica_ext_interesado_administrador_id	extinteresado	extredserviciosfisica
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_la_unidadespacial	puntocontrol	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	puntocontrol	\N
LADM_COL_V1_1.LADM_Nucleo.mas.ueP	uep_la_unidadespacial	mas	la_unidadespacial
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.UnidadConstruccion.Area_Construida	area_construida	unidadconstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Ext_Direccion_ID	la_espacjrdcndddfccion_ext_direccion_id	extdireccion	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	col_interesado_calidad	dq_element	col_interesado
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Local_Id	su_local_id	la_espaciojuridicounidadedificacion	\N
LADM_COL_V1_1.LADM_Nucleo.ueBaunit.baunit	baunit_predio	uebaunit	predio
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_construccion	puntocontrol	construccion
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado.Segundo_Apellido	segundo_apellido	col_interesado	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Localizacion_Original	localizacion_original	puntolevantamiento	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_terreno	servidumbrepaso	terreno
LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit.u_Local_Id	u_local_id	la_baunit	\N
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Fecha_Entrega	fecha_entrega	col_fuenteespacial	\N
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion.Nombre_Edificio	nombre_edificio	extdireccion	\N
LADM_COL_V1_1.LADM_Nucleo.unidadFuente.unidad	unidad_la_baunit	unidadfuente	la_baunit
LADM_COL_V1_1.LADM_Nucleo.menosf.ue	ue_terreno	menosf	terreno
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	lindero_procedencia	ci_parteresponsable	lindero
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Espacio_De_Nombres	su_espacio_de_nombres	la_espaciojuridicounidadedificacion	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoControl.Exactitud_Vertical	exactitud_vertical	puntocontrol	\N
LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite.Geometria	geometria	la_cadenacaraslimite	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Relacion_Superficie	relacion_superficie	la_espaciojuridicoredservicios	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Servidumbre	terreno_servidumbre	col_servidumbretipo_terreno_servidumbre	terreno
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	servidumbrepaso	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	la_baunit	\N
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad	estado_disponibilidad	col_fuenteespacial	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Espacio_De_Nombres	su_espacio_de_nombres	construccion	\N
LADM_COL_V1_1.LADM_Nucleo.topografoFuente.topografo	topografo_la_agrupacion_interesados	topografofuente	la_agrupacion_interesados
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.Tipo	tipo	col_interesado	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Posicion_Interpolacion	posicion_interpolacion	puntolevantamiento	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Localizacion_Original	localizacion_original	la_punto	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLevantamiento.Tipo_Punto_Levantamiento	tipo_punto_levantamiento	puntolevantamiento	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Uso_Efectivo	uso_efectivo	col_responsabilidad	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite.ccl_Local_Id	ccl_local_id	lindero	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	col_interesado_procedencia	ci_parteresponsable	col_interesado
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Local_Id	su_local_id	la_unidadespacial	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Resultado	resultado	dq_absoluteexternalpositionalaccuracy	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Derecho.Tipo	tipo	col_derecho	\N
LADM_COL_V1_1.LADM_Nucleo.topografoFuente.topografo	topografo_col_interesado	topografofuente	col_interesado
LADM_COL_V1_1.LADM_Nucleo.ExtArchivo.Fecha_Entrega	fecha_entrega	extarchivo	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	la_agrupacion_intrsdos_procedencia	ci_parteresponsable	la_agrupacion_interesados
LADM_COL_V1_1.LADM_Nucleo.LA_CarasLindero.cl_Espacio_De_Nombres	cl_espacio_de_nombres	la_caraslindero	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoControl.Nombre_Punto	nombre_punto	puntocontrol	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Monumentacion	monumentacion	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Monumentacion	monumentacion	puntolevantamiento	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Uso_Efectivo	uso_efectivo	col_derecho	\N
LADM_COL_V1_1.LADM_Nucleo.ueNivel.nivel	nivel	servidumbrepaso	la_nivel
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	col_responsabilidad_calidad	dq_element	col_responsabilidad
LADM_COL_V1_1.LADM_Nucleo.rrrInteresado.interesado	interesado_col_interesado	col_responsabilidad	col_interesado
LADM_COL_V1_1.LADM_Nucleo.relacionFuente.relacionrequeridaBaunit	relacionrequeridabaunit	relacionfuente	la_relacionnecesariabaunits
LADM_COL_V1_1.LADM_Nucleo.baunitComoInteresado.interesado	interesado_la_agrupacion_interesados	baunitcomointeresado	la_agrupacion_interesados
LADM_COL_V1_1.LADM_Nucleo.baunitComoInteresado.interesado	interesado_col_interesado	baunitcomointeresado	col_interesado
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Etiqueta	etiqueta	la_espaciojuridicoredservicios	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area	terreno_area	col_areavalor	terreno
LADM_COL_V1_1.LADM_Nucleo.rrrInteresado.interesado	interesado_la_agrupacion_interesados	col_responsabilidad	la_agrupacion_interesados
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Descripcion_Metodo_Evaluacion	descripcion_metodo_evaluacion	dq_positionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.ExtUnidadEdificacionFisica.Ext_Direccion_ID	extunidadedificcnfsica_ext_direccion_id	extdireccion	extunidadedificacionfisica
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	la_caraslindero	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Responsabilidad.Tipo	tipo	col_responsabilidad	\N
LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite.ccl_Espacio_De_Nombres	ccl_espacio_de_nombres	la_cadenacaraslimite	\N
LADM_COL_V1_1.LADM_Nucleo.rrrFuente.rrr	rrr_col_restriccion	rrrfuente	col_restriccion
LADM_COL_V1_1.LADM_Nucleo.ExtArchivo.s_Espacio_De_Nombres	s_espacio_de_nombres	extarchivo	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	la_caraslindero	\N
LADM_COL_V1_1.LADM_Nucleo.cclFuente.lfuente	lfuente	cclfuente	col_fuenteespacial
LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit.Tipo	tipo	predio	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.UnidadConstruccion.Area_Privada_Construida	area_privada_construida	unidadconstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Relacion_Superficie	relacion_superficie	servidumbrepaso	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLevantamiento.Exactitud_Vertical	exactitud_vertical	puntolevantamiento	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Procedimiento_Evaluacion	procedimiento_evaluacion	dq_element	\N
LADM_COL_V1_1.LADM_Nucleo.ExtArchivo.Fecha_Aceptacion	fecha_aceptacion	extarchivo	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Relacion_Superficie	relacion_superficie	la_espaciojuridicounidadedificacion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.p_Espacio_De_Nombres	p_espacio_de_nombres	puntocontrol	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	la_punto	\N
LADM_COL_V1_1.LADM_Nucleo.ueNivel.nivel	nivel	la_espaciojuridicoredservicios	la_nivel
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	la_espaciojuridicoredservicios	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	construccion_calidad	dq_element	construccion
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Local_Id	su_local_id	terreno	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen	la_espacjrdcndddfccion_volumen	la_volumenvalor	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.LA_Nivel.n_ID	la_nivel_n_id	oid	la_nivel
LADM_COL_V1_1.LADM_Nucleo.puntoCl.punto	punto_puntocontrol	puntocl	puntocontrol
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_unidadconstruccion	terreno	unidadconstruccion
Catastro_Registro_Nucleo_V2_2_1.COL_ServidumbreTipo_Terreno_Servidumbre.value	avalue	col_servidumbretipo_terreno_servidumbre	\N
Catastro_Registro_Nucleo_V2_2_1.COL_TerritorioAgricola_Terreno_Territorio_Agricola.value	avalue	col_territorioagricola_terreno_territorio_agricola	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Predio.FMI	fmi	predio	\N
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad	estado_disponibilidad	col_fuenteadministrativa	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_PositionalAccuracy.atributo21	atributo21	dq_positionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.p_Espacio_De_Nombres	p_espacio_de_nombres	la_agrupacion_interesados	\N
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteEspacial.Tipo	tipo	col_fuenteespacial	\N
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID	col_fuenteadminstrtiva_ext_archivo_id	extarchivo	col_fuenteadministrativa
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Fecha_Grabacion	fecha_grabacion	col_fuenteadministrativa	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Dimension	dimension	terreno	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Posicion_Interpolacion	posicion_interpolacion	la_punto	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.p_Local_Id	p_local_id	puntocontrol	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Transformacion.Transformacion	la_transformacion_transformacion	cc_metodooperacion	la_transformacion
LADM_COL_V1_1.LADM_Nucleo.puntoCcl.punto	punto_la_punto	puntoccl	la_punto
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Resultado	resultado	dq_element	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_AbsoluteExternalPositionalAccuracy.atributo1	atributo1	dq_absoluteexternalpositionalaccuracy	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoControl.Exactitud_Horizontal	exactitud_horizontal	puntocontrol	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_unidadconstruccion	la_espaciojuridicounidadedificacion	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Procedimiento_Evaluacion	procedimiento_evaluacion	dq_absoluteexternalpositionalaccuracy	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado.Razon_Social	razon_social	col_interesado	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_unidadconstruccion	puntocontrol	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_terreno	puntolevantamiento	terreno
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	la_relcnncsrnddsspcles_calidad	dq_element	la_relacionnecesariaunidadesespaciales
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Comprobacion_Comparte	comprobacion_comparte	col_responsabilidad	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Descripcion_Medida	descripcion_medida	dq_positionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	la_relcnncsrnddsspcles_procedencia	ci_parteresponsable	la_relacionnecesariaunidadesespaciales
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	la_agrupacion_intrsdos_calidad	dq_element	la_agrupacion_interesados
LADM_COL_V1_1.LADM_Nucleo.LI_Lineaje.Statement	astatement	li_lineaje	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_construccion	unidadconstruccion	construccion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	la_espacjrdcndddfccion_procedencia	ci_parteresponsable	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.masCcl.cclP	cclp_lindero	masccl	lindero
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Relacion_Superficie	relacion_superficie	terreno	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLindero.Exactitud_Vertical	exactitud_vertical	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_terreno	la_espaciojuridicoredservicios	terreno
LADM_COL_V1_1.LADM_Nucleo.LA_AgrupacionUnidadesEspaciales.Nivel_Jerarquico	nivel_jerarquico	la_agrupacionunidadesespaciales	\N
LADM_COL_V1_1.LADM_Nucleo.menosf.ue	ue_servidumbrepaso	menosf	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.CI_ParteResponsable.Posicion	posicion	ci_parteresponsable	\N
LADM_COL_V1_1.LADM_Nucleo.ueBaunit.ue	ue_la_unidadespacial	uebaunit	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.clFuente.cl	cl	clfuente	la_caraslindero
LADM_COL_V1_1.LADM_Nucleo.Oid.localId	localid	oid	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	puntocontrol_calidad	dq_element	puntocontrol
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Fecha_Aceptacion	fecha_aceptacion	col_fuenteadministrativa	\N
LADM_COL_V1_1.LADM_Nucleo.ueBaunit.baunit	baunit_la_baunit	uebaunit	la_baunit
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Publicidad.p_Local_Id	p_local_id	publicidad	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	publicidad_calidad	dq_element	publicidad
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion.Ext_Unidad_Edificacion_Fisica_ID	la_espacjrdcndddfccion_ext_unidad_edificacion_fisic_id	extunidadedificacionfisica	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Transformacion_Y_Resultado	puntolevantamiento_transformacion_y_resultado	la_transformacion	puntolevantamiento
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.InteresadoContacto.interesado	interesado	interesado_contacto	col_interesado
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicounidadedificacion	unidadconstruccion	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Punto_Referencia	punto_referencia	la_unidadespacial	\N
LADM_COL_V1_1.LADM_Nucleo.CC_MetodoOperacion.Dimensiones_Origen	dimensiones_origen	cc_metodooperacion	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadInteresado.interesado	interesado_col_interesado	publicidad	col_interesado
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicoredservicios	terreno	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.CI_Contacto.Fuente_En_Linea	fuente_en_linea	ci_contacto	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadInteresado.interesado	interesado_la_agrupacion_interesados	publicidad	la_agrupacion_interesados
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Etiqueta	etiqueta	la_espaciojuridicounidadedificacion	\N
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion.Nombre_Calle	nombre_calle	extdireccion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RelacionNecesariaUnidadesEspaciales.Relacion	relacion	la_relacionnecesariaunidadesespaciales	\N
LADM_COL_V1_1.LADM_Nucleo.ueUeGrupo.parte	parte_la_espaciojuridicoredservicios	ueuegrupo	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.baunitRrr.unidad	unidad_la_baunit	col_derecho	la_baunit
LADM_COL_V1_1.LADM_Nucleo.Fraccion.Denominador	denominador	fraccion	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicoredservicios	la_espaciojuridicounidadedificacion	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.masCcl.ueP	uep_terreno	masccl	terreno
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Exactitud_Estimada	puntocontrol_exactitud_estimada	dq_positionalaccuracy	puntocontrol
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_la_espaciojuridicoredservicios	puntocontrol	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	construccion_procedencia	ci_parteresponsable	construccion
LADM_COL_V1_1.LADM_Nucleo.CI_Contacto.Direccion	direccion	ci_contacto	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_construccion	la_espaciojuridicounidadedificacion	construccion
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Area	la_espacijrdcrdsrvcios_area	col_areavalor	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	publicidad	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadFuente.publicidad	publicidad	publicidadfuente	publicidad
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Punto_Referencia	punto_referencia	unidadconstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.p_Espacio_De_Nombres	p_espacio_de_nombres	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Metodo_Evaluacion	metodo_evaluacion	dq_element	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Descripcion_Metodo_Evaluacion	descripcion_metodo_evaluacion	dq_absoluteexternalpositionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Compartido	col_responsabilidad_compartido	fraccion	col_responsabilidad
LADM_COL_V1_1.LADM_Nucleo.cclFuente.ccl	ccl_la_cadenacaraslimite	cclfuente	la_cadenacaraslimite
LADM_COL_V1_1.LADM_Nucleo.LA_RelacionNecesariaBAUnits.Relacion	relacion	la_relacionnecesariabaunits	\N
LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite.Localizacion_Textual	localizacion_textual	la_cadenacaraslimite	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Dimension	dimension	la_espaciojuridicounidadedificacion	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_servidumbrepaso	puntolevantamiento	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.Nombre	nombre	col_interesado	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.PuntoTipo	puntotipo	puntocontrol	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.r_Local_Id	r_local_id	col_hipoteca	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.r_Local_Id	r_local_id	col_restriccion	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	la_punto_calidad	dq_element	la_punto
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.ServidumbrePaso.Identificador	identificador	servidumbrepaso	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_unidadespacial	la_espaciojuridicounidadedificacion	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen	construccion_volumen	la_volumenvalor	construccion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	lindero	\N
LADM_COL_V1_1.LADM_Nucleo.ueNivel.nivel	nivel	unidadconstruccion	la_nivel
LADM_COL_V1_1.LADM_Nucleo.baunitFuente.unidad	unidad_predio	baunitfuente	predio
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Predio.NUPRE	nupre	predio	\N
LADM_COL_V1_1.LADM_Nucleo.baunitRrr.unidad	unidad_la_baunit	col_hipoteca	la_baunit
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	la_caraslindero_procedencia	ci_parteresponsable	la_caraslindero
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Predio.Numero_Predial_Anterior	numero_predial_anterior	predio	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_terreno	terreno	terreno
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Punto_Referencia	punto_referencia	construccion	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Interesado_Contacto.Telefono1	telefono1	interesado_contacto	\N
LADM_COL_V1_1.LADM_Nucleo.ExtArchivo.s_Local_Id	s_local_id	extarchivo	\N
LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite.Geometria	geometria	lindero	\N
LADM_COL_V1_1.LADM_Nucleo.Oid.espacioDeNombres	espaciodenombres	oid	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_servidumbrepaso	la_punto	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite.ccl_Local_Id	ccl_local_id	la_cadenacaraslimite	\N
LADM_COL_V1_1.LADM_Nucleo.topografoFuente.sfuente	sfuente	topografofuente	col_fuenteespacial
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Avaluo_Terreno	avaluo_terreno	terreno	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_espaciojuridicounidadedificacion	terreno	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen	unidadconstruccion_volumen	la_volumenvalor	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Local_Id	su_local_id	servidumbrepaso	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	unidadconstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Procedimiento_Evaluacion	procedimiento_evaluacion	dq_positionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.Tipo	tipo	la_agrupacion_interesados	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_servidumbrepaso	puntolindero	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue1	rue1_terreno	relacionue	terreno
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado.Primer_Apellido	primer_apellido	col_interesado	\N
LADM_COL_V1_1.LADM_Nucleo.baunitRrr.unidad	unidad_la_baunit	col_restriccion	la_baunit
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Hipoteca.Codigo_Registral_Hipoteca	codigo_registral_hipoteca	col_hipoteca	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.MetodoProduccion	puntolevantamiento_metodoproduccion	li_lineaje	puntolevantamiento
LADM_COL_V1_1.LADM_Nucleo.LA_AgrupacionUnidadesEspaciales.Etiqueta	etiqueta	la_agrupacionunidadesespaciales	\N
LADM_COL_V1_1.LADM_Nucleo.menosf.ue	ue_unidadconstruccion	menosf	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.ExtArchivo.Datos	datos	extarchivo	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	col_derecho	\N
LADM_COL_V1_1.LADM_Nucleo.unidadFuente.unidad	unidad_predio	unidadfuente	predio
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.r_Local_Id	r_local_id	col_responsabilidad	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Exactitud_Estimada	puntolevantamiento_exactitud_estimada	dq_positionalaccuracy	puntolevantamiento
LADM_COL_V1_1.LADM_Nucleo.responsableFuente.notario	notario_col_interesado	responsablefuente	col_interesado
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Identificacion_Medida	identificacion_medida	dq_absoluteexternalpositionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Transformacion.Localizacion_Transformada	localizacion_transformada	la_transformacion	\N
LADM_COL_V1_1.LADM_Nucleo.rrrInteresado.interesado	interesado_la_agrupacion_interesados	col_derecho	la_agrupacion_interesados
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.p_Local_Id	p_local_id	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.ueBaunit.ue	ue_construccion	uebaunit	construccion
ISO19107_V1_MAGNABOG.GM_Surface3DListValue.value	avalue	gm_surface3dlistvalue	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Predio.Departamento	departamento	predio	\N
Catastro_Registro_Nucleo_V2_2_1.COL_BosqueAreaSemi_Terreno_Bosque_Area_Seminaturale.value	avalue	col_bosqueareasemi_terreno_bosque_area_seminaturale	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_la_unidadespacial	puntolindero	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_unidadespacial	unidadconstruccion	la_unidadespacial
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Restriccion.Tipo	tipo	col_restriccion	\N
LADM_COL_V1_1.LADM_Nucleo.ExtInteresado.Fotografia	extinteresado_fotografia	imagen	extinteresado
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_la_espaciojuridicounidadedificacion	la_punto	la_espaciojuridicounidadedificacion
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLindero.Nombre_Punto	nombre_punto	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_servidumbrepaso	puntocontrol	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.menosf.ue	ue_la_espaciojuridicoredservicios	menosf	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteAdministrativa.Codigo_Registral_Transaccion	codigo_registral_transaccion	col_fuenteadministrativa	\N
LADM_COL_V1_1.LADM_Nucleo.LA_CarasLindero.cl_Local_Id	cl_local_id	la_caraslindero	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Dimension	dimension	construccion	\N
LADM_COL_V1_1.LADM_Nucleo.masCcl.ueP	uep_la_espaciojuridicounidadedificacion	masccl	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.menos.eu	eu_terreno	menos	terreno
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Metodo_Evaluacion	metodo_evaluacion	dq_positionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue2	rue2_terreno	relacionue	terreno
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Restriccion.Tipo	tipo	col_hipoteca	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	unidadconstruccion_procedencia	ci_parteresponsable	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteAdministrativa.Tipo	tipo	col_fuenteadministrativa	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	la_unidadespacial_calidad	dq_element	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Posicion_Interpolacion	posicion_interpolacion	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	la_punto	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_construccion	puntolindero	construccion
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_terreno	la_punto	terreno
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado.Tipo_Documento	tipo_documento	col_interesado	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	col_responsabilidad	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Local_Id	su_local_id	la_espaciojuridicoredservicios	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.ext_PID	col_interesado_ext_pid	extinteresado	col_interesado
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	predio	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.PuntoTipo	puntotipo	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Descripcion	descripcion	col_restriccion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Exactitud_Estimada	la_punto_exactitud_estimada	dq_positionalaccuracy	la_punto
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_terreno	unidadconstruccion	terreno
LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit.Nombre	nombre	la_baunit	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Espacio_De_Nombres	su_espacio_de_nombres	servidumbrepaso	\N
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteAdministrativa.Texto	texto	col_fuenteadministrativa	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_servidumbrepaso	servidumbrepaso	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	puntolevantamiento	\N
LADM_COL_V1_1.LADM_Nucleo.clFuente.cfuente	cfuente	clfuente	col_fuenteespacial
LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit.u_Espacio_De_Nombres	u_espacio_de_nombres	predio	\N
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Calidad	col_fuenteadminstrtiva_calidad	dq_element	col_fuenteadministrativa
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_servidumbrepaso	la_espaciojuridicounidadedificacion	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Fecha_Hora	fecha_hora	dq_element	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Etiqueta	etiqueta	unidadconstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.CI_Contacto.Instrucciones_Contacto	instrucciones_contacto	ci_contacto	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Etiqueta	etiqueta	la_unidadespacial	\N
LADM_COL_V1_1.LADM_Nucleo.menosf.ue	ue_construccion	menosf	construccion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	la_agrupacionunidadesespaciales	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Dimension	dimension	la_espaciojuridicoredservicios	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Local_Id	su_local_id	construccion	\N
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue1	rue1_la_espaciojuridicounidadedificacion	relacionue	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_terreno	construccion	terreno
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Descripcion	descripcion	col_hipoteca	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Fecha_Hora	fecha_hora	dq_absoluteexternalpositionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.miembros.agrupacion	agrupacion	miembros	la_agrupacion_interesados
LADM_COL_V1_1.LADM_Nucleo.ueUeGrupo.parte	parte_la_espaciojuridicounidadedificacion	ueuegrupo	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.ueFuente.ue	ue_la_espaciojuridicounidadedificacion	uefuente	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia.ue	ue_la_unidadespacial	puntolevantamiento	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.ExtInteresado.Ext_Direccion_ID	extinteresado_ext_direccion_id	extdireccion	extinteresado
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Punto_Referencia	punto_referencia	servidumbrepaso	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLindero.Confiabilidad	confiabilidad	puntolindero	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Punto_Referencia	punto_referencia	la_espaciojuridicounidadedificacion	\N
Catastro_Registro_Nucleo_V2_2_1.COL_Afectacion_Terreno_Afectacion.value	avalue	col_afectacion_terreno_afectacion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Dimension	dimension	unidadconstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Transformacion_Y_Resultado	puntocontrol_transformacion_y_resultado	la_transformacion	puntocontrol
LADM_COL_V1_1.LADM_Nucleo.COL_AreaValor.type	atype	col_areavalor	\N
LADM_COL_V1_1.LADM_Nucleo.baunitRrr.unidad	unidad_predio	col_derecho	predio
LADM_COL_V1_1.LADM_Nucleo.menos.eu	eu_la_espaciojuridicounidadedificacion	menos	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.Descripcion	descripcion	col_responsabilidad	\N
LADM_COL_V1_1.LADM_Nucleo.ueNivel.nivel	nivel	la_unidadespacial	la_nivel
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	col_derecho_procedencia	ci_parteresponsable	col_derecho
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.s_Espacio_De_Nombres	s_espacio_de_nombres	col_fuenteespacial	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Punto_Referencia	punto_referencia	la_espaciojuridicoredservicios	\N
LADM_COL_V1_1.LADM_Nucleo.mas.ueP	uep_la_espaciojuridicounidadedificacion	mas	la_espaciojuridicounidadedificacion
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.hipotecaDerecho.hipoteca	hipoteca	hipotecaderecho	col_hipoteca
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_la_unidadespacial	la_espaciojuridicoredservicios	la_unidadespacial
LADM_COL_V1_1.LADM_Nucleo.puntoCcl.ccl	ccl_la_cadenacaraslimite	puntoccl	la_cadenacaraslimite
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Identificacion_Medida	identificacion_medida	dq_positionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado.Tarea	col_interesado_tarea	la_tareainteresadotipo	col_interesado
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Local_Id	su_local_id	unidadconstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.ExtInteresado.Huella_Dactilar	extinteresado_huella_dactilar	imagen	extinteresado
LADM_COL_V1_1.LADM_Nucleo.LA_Nivel.Nombre	nombre	la_nivel	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	la_unidadespacial	\N
ISO19107_V1_MAGNABOG.GM_MultiSurface3D.geometry	gm_multisurface3d_geometry	gm_surface3dlistvalue	gm_multisurface3d
LADM_COL_V1_1.LADM_Nucleo.ueJerarquiaGrupo.set	aset	la_agrupacionunidadesespaciales	la_agrupacionunidadesespaciales
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Dimension	dimension	servidumbrepaso	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	la_relacionnecesariabaunits	\N
LADM_COL_V1_1.LADM_Nucleo.puntoFuente.punto	punto_la_punto	puntofuente	la_punto
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	predio_procedencia	ci_parteresponsable	predio
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLevantamiento.Exactitud_Horizontal	exactitud_horizontal	puntolevantamiento	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	col_responsabilidad_procedencia	ci_parteresponsable	col_responsabilidad
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Procedencia	la_agrupacinnddsspcles_procedencia	ci_parteresponsable	la_agrupacionunidadesespaciales
LADM_COL_V1_1.LADM_Nucleo.LA_AgrupacionUnidadesEspaciales.sug_Local_Id	sug_local_id	la_agrupacionunidadesespaciales	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Monumentacion	monumentacion	puntocontrol	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado.Tipo_Interesado_Juridico	tipo_interesado_juridico	col_interesado	\N
LADM_COL_V1_1.LADM_Nucleo.ueBaunit.ue	ue_la_espaciojuridicoredservicios	uebaunit	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Etiqueta	etiqueta	construccion	\N
LADM_COL_V1_1.LADM_Nucleo.ueBaunit.ue	ue_unidadconstruccion	uebaunit	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.LA_RRR.r_Espacio_De_Nombres	r_espacio_de_nombres	col_derecho	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado.Primer_Nombre	primer_nombre	col_interesado	\N
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente.Fecha_Grabacion	fecha_grabacion	col_fuenteespacial	\N
LADM_COL_V1_1.LADM_Nucleo.puntoCl.cl	cl	puntocl	la_caraslindero
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.Volumen	la_espacijrdcrdsrvcios_volumen	la_volumenvalor	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version	fin_vida_util_version	la_baunit	\N
LADM_COL_V1_1.LADM_Nucleo.relacionUe.rue2	rue2_la_espaciojuridicounidadedificacion	relacionue	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	puntolindero_calidad	dq_element	puntolindero
LADM_COL_V1_1.LADM_Nucleo.DQ_Element.Metodo_Evaluacion	metodo_evaluacion	dq_absoluteexternalpositionalaccuracy	\N
LADM_COL_V1_1.LADM_Nucleo.puntoCcl.ccl	ccl_lindero	puntoccl	lindero
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion.Pais	pais	extdireccion	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_servidumbrepaso	la_espaciojuridicoredservicios	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.baunitFuente.unidad	unidad_la_baunit	baunitfuente	la_baunit
Catastro_Registro_Nucleo_V2_2_1.COL_ExplotacionTipo_Terreno_Explotacion.value	avalue	col_explotaciontipo_terreno_explotacion	\N
LADM_COL_V1_1.LADM_Nucleo.cclFuente.ccl	ccl_lindero	cclfuente	lindero
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.MetodoProduccion	puntocontrol_metodoproduccion	li_lineaje	puntocontrol
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Calidad	servidumbrepaso_calidad	dq_element	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia.uej2	uej2_terreno	la_unidadespacial	terreno
LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite.Localizacion_Textual	localizacion_textual	lindero	\N
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.su_Espacio_De_Nombres	su_espacio_de_nombres	la_espaciojuridicoredservicios	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto.Exactitud_Estimada	puntolindero_exactitud_estimada	dq_positionalaccuracy	puntolindero
LADM_COL_V1_1.LADM_Nucleo.puntoFuente.punto	punto_puntolindero	puntofuente	puntolindero
LADM_COL_V1_1.LADM_Nucleo.ueNivel.nivel	nivel	construccion	la_nivel
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version	comienzo_vida_util_version	construccion	\N
\.


--
-- TOC entry 12423 (class 0 OID 336017)
-- Dependencies: 2108
-- Data for Name: t_ili2db_basket; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_basket (t_id, dataset, topic, t_ili_tid, attachmentkey) FROM stdin;
\.


--
-- TOC entry 12424 (class 0 OID 336023)
-- Dependencies: 2109
-- Data for Name: t_ili2db_classname; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_classname (iliname, sqlname) FROM stdin;
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia	uejerarquia
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.ServidumbrePaso	servidumbrepaso
LADM_COL_V1_1.LADM_Nucleo.LA_VolumenValor	la_volumenvalor
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoControl	puntocontrol
LADM_COL_V1_1.LADM_Nucleo.ISO19125_Tipo	iso19125_tipo
Catastro_Registro_Nucleo_V2_2_1.COL_TerritorioAgricola	col_territorioagricola
LADM_COL_V1_1.LADM_Nucleo.CI_Contacto	ci_contacto
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.hipotecaDerecho	hipotecaderecho
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion	extdireccion
LADM_COL_V1_1.LADM_Nucleo.Oid	oid
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno	terreno
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia	puntoreferencia
LADM_COL_V1_1.LADM_Nucleo.ExtInteresado	extinteresado
LADM_COL_V1_1.LADM_Nucleo.LA_InterpolacionTipo	la_interpolaciontipo
LADM_COL_V1_1.LADM_Nucleo.LA_RelacionNecesariaBAUnits	la_relacionnecesariabaunits
LADM_COL_V1_1.LADM_Nucleo.menos	menos
LADM_COL_V1_1.LADM_Nucleo.LA_RelacionSuperficieTipo	la_relacionsuperficietipo
Catastro_Registro_Nucleo_V2_2_1.COL_CuerpoAgua_Terreno_Evidencia_Cuerpo_Agua	col_cuerpoagua_terreno_evidencia_cuerpo_agua
Catastro_Registro_Nucleo_V2_2_1.COL_PredioTipo	col_prediotipo
LADM_COL_V1_1.LADM_Nucleo.responsableFuente	responsablefuente
Catastro_Registro_Nucleo_V2_2_1.COL_BosqueAreaSemi_Terreno_Bosque_Area_Seminaturale	col_bosqueareasemi_terreno_bosque_area_seminaturale
LADM_COL_V1_1.LADM_Nucleo.relacionFuenteUespacial	relacionfuenteuespacial
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial	la_unidadespacial
ISO19107_V1_MAGNABOG.GM_Surface2DListValue	gm_surface2dlistvalue
LADM_COL_V1_1.LADM_Nucleo.LA_PuntoTipo	la_puntotipo
Catastro_Registro_Nucleo_V2_2_1.COL_UnidadEdificacionTipo	col_unidadedificaciontipo
LADM_COL_V1_1.LADM_Nucleo.LA_RegistroTipo	la_registrotipo
LADM_COL_V1_1.LADM_Nucleo.ExtRedServiciosFisica	extredserviciosfisica
Catastro_Registro_Nucleo_V2_2_1.COL_DefPuntoTipo	col_defpuntotipo
LADM_COL_V1_1.LADM_Nucleo.LA_DimensionTipo	la_dimensiontipo
LADM_COL_V1_1.LADM_Nucleo.baunitFuente	baunitfuente
LADM_COL_V1_1.LADM_Nucleo.COL_AreaTipo	col_areatipo
LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite	la_cadenacaraslimite
LADM_COL_V1_1.LADM_Nucleo.ueUeGrupo	ueuegrupo
LADM_COL_V1_1.LADM_Nucleo.CI_Forma_Presentacion_Codigo	ci_forma_presentacion_codigo
Catastro_Registro_Nucleo_V2_2_1.COL_MonumentacionTipo	col_monumentaciontipo
LADM_COL_V1_1.LADM_Nucleo.LA_EstructuraTipo	la_estructuratipo
Catastro_Registro_Nucleo_V2_2_1.COL_InteresadoJuridicoTipo	col_interesadojuridicotipo
LADM_COL_V1_1.LADM_Nucleo.LA_HipotecaTipo	la_hipotecatipo
LADM_COL_V1_1.LADM_Nucleo.LI_Lineaje	li_lineaje
LADM_COL_V1_1.LADM_Nucleo.ueBaunit	uebaunit
Catastro_Registro_Nucleo_V2_2_1.COL_ResponsabilidadTipo	col_responsabilidadtipo
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Responsabilidad	col_responsabilidad
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.InteresadoContacto	interesadocontacto
Catastro_Registro_Nucleo_V2_2_1.COL_Afectacion_Terreno_Afectacion	col_afectacion_terreno_afectacion
LADM_COL_V1_1.LADM_Nucleo.LA_Agrupacion_Interesados_Tipo	la_agrupacion_interesados_tipo
LADM_COL_V1_1.LADM_Nucleo.unidadFuente	unidadfuente
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado	col_interesado
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteEspacialTipo	col_fuenteespacialtipo
Catastro_Registro_Nucleo_V2_2_1.COL_InterpolacionTipo	col_interpolaciontipo
LADM_COL_V1_1.LADM_Nucleo.LA_Transformacion	la_transformacion
LADM_COL_V1_1.LADM_Nucleo.COL_FuncionInteresadoTipo	col_funcioninteresadotipo
Catastro_Registro_Nucleo_V2_2_1.COL_ZonaTipo	col_zonatipo
Catastro_Registro_Nucleo_V2_2_1.COL_BosqueAreaSemi	col_bosqueareasemi
LADM_COL_V1_1.LADM_Nucleo.LA_ContenidoNivelTipo	la_contenidoniveltipo
LADM_COL_V1_1.LADM_Nucleo.ueJerarquiaGrupo	uejerarquiagrupo
LADM_COL_V1_1.LADM_Nucleo.relacionBaunit	relacionbaunit
ISO19107_V1_MAGNABOG.GM_Surface3DListValue	gm_surface3dlistvalue
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Lindero	lindero
Catastro_Registro_Nucleo_V2_2_1.COL_CuerpoAgua	col_cuerpoagua
LADM_COL_V1_1.LADM_Nucleo.LA_MonumentacionTipo	la_monumentaciontipo
LADM_COL_V1_1.LADM_Nucleo.LA_CarasLindero	la_caraslindero
LADM_COL_V1_1.LADM_Nucleo.relacionFuente	relacionfuente
LADM_COL_V1_1.LADM_Nucleo.relacionUe	relacionue
LADM_COL_V1_1.LADM_Nucleo.DQ_Metodo_Evaluacion_Codigo_Tipo	dq_metodo_evaluacion_codigo_tipo
LADM_COL_V1_1.LADM_Nucleo.Imagen	imagen
LADM_COL_V1_1.LADM_Nucleo.DQ_Element	dq_element
LADM_COL_V1_1.LADM_Nucleo.baunitComoInteresado	baunitcomointeresado
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente	col_fuente
LADM_COL_V1_1.LADM_Nucleo.LA_FuenteEspacialTipo	la_fuenteespacialtipo
LADM_COL_V1_1.LADM_Nucleo.LA_AgrupacionUnidadesEspaciales	la_agrupacionunidadesespaciales
LADM_COL_V1_1.LADM_Nucleo.CI_CodigoTarea	ci_codigotarea
Catastro_Registro_Nucleo_V2_2_1.COL_PublicidadTipo	col_publicidadtipo
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLevantamiento	puntolevantamiento
LADM_COL_V1_1.LADM_Nucleo.COL_LevelContentTipo	col_levelcontenttipo
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado	objetoversionado
LADM_COL_V1_1.LADM_Nucleo.DQ_PositionalAccuracy	dq_positionalaccuracy
LADM_COL_V1_1.LADM_Nucleo.LA_RedServiciosTipo	la_redserviciostipo
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.ConstruccionUnidadConstruccion	construccionunidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteAdministrativa	col_fuenteadministrativa
LADM_COL_V1_1.LADM_Nucleo.rrrInteresado	rrrinteresado
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.UnidadConstruccion	unidadconstruccion
LADM_COL_V1_1.LADM_Nucleo.COL_EstadoDisponibilidadTipo	col_estadodisponibilidadtipo
Catastro_Registro_Nucleo_V2_2_1.COL_ViaTipo	col_viatipo
LADM_COL_V1_1.LADM_Nucleo.LA_RestriccionTipo	la_restricciontipo
LADM_COL_V1_1.LADM_Nucleo.puntoCcl	puntoccl
LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit	la_baunit
LADM_COL_V1_1.LADM_Nucleo.LA_EstadoRedServiciosTipo	la_estadoredserviciostipo
LADM_COL_V1_1.LADM_Nucleo.menosf	menosf
LADM_COL_V1_1.LADM_Nucleo.LA_InteresadoTipo	la_interesadotipo
Catastro_Registro_Nucleo_V2_2_1.COL_ServidumbreTipo	col_servidumbretipo
LADM_COL_V1_1.LADM_Nucleo.clFuente	clfuente
Catastro_Registro_Nucleo_V2_2_1.COL_ServidumbreTipo_Terreno_Servidumbre	col_servidumbretipo_terreno_servidumbre
LADM_COL_V1_1.LADM_Nucleo.ueNivel	uenivel
LADM_COL_V1_1.LADM_Nucleo.masCcl	masccl
LADM_COL_V1_1.LADM_Nucleo.LA_ResponsabilidadTipo	la_responsabilidadtipo
LADM_COL_V1_1.LADM_Nucleo.ExtArchivo	extarchivo
LADM_COL_V1_1.LADM_Nucleo.LA_Nivel	la_nivel
Catastro_Registro_Nucleo_V2_2_1.COL_ExplotacionTipo_Terreno_Explotacion	col_explotaciontipo_terreno_explotacion
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion	la_espaciojuridicounidadedificacion
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEdificacionTipo	la_unidadedificaciontipo
LADM_COL_V1_1.LADM_Nucleo.LA_DerechoTipo	la_derechotipo
Catastro_Registro_Nucleo_V2_2_1.COL_PuntoControlTipo	col_puntocontroltipo
Catastro_Registro_Nucleo_V2_2_1.COL_GeneroTipo	col_generotipo
ISO19107_V1_MAGNABOG.GM_MultiSurface2D	gm_multisurface2d
Catastro_Registro_Nucleo_V2_2_1.COL_HipotecaTipo	col_hipotecatipo
LADM_COL_V1_1.LADM_Nucleo.Fraccion	fraccion
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Construccion	construccion
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Hipoteca	col_hipoteca
LADM_COL_V1_1.LADM_Nucleo.LA_EstadoDisponibilidadTipo	la_estadodisponibilidadtipo
LADM_COL_V1_1.LADM_Nucleo.baunitRrr	baunitrrr
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado	la_interesado
LADM_COL_V1_1.LADM_Nucleo.miembros	miembros
Catastro_Registro_Nucleo_V2_2_1.COL_Afectacion	col_afectacion
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Predio	predio
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Derecho	col_derecho
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Restriccion	col_restriccion
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadBAUnit	publicidadbaunit
Catastro_Registro_Nucleo_V2_2_1.COL_PuntoLevTipo	col_puntolevtipo
LADM_COL_V1_1.LADM_Nucleo.puntoFuente	puntofuente
LADM_COL_V1_1.LADM_Nucleo.CI_ParteResponsable	ci_parteresponsable
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Publicidad	publicidad
LADM_COL_V1_1.LADM_Nucleo.OM_Observacion	om_observacion
LADM_COL_V1_1.LADM_Nucleo.LA_Punto	la_punto
LADM_COL_V1_1.LADM_Nucleo.LA_TareaInteresadoTipo.Tipo	la_tareainteresadotipo_tipo
ISO19107_V1_MAGNABOG.GM_MultiSurface3D	gm_multisurface3d
LADM_COL_V1_1.LADM_Nucleo.DQ_AbsoluteExternalPositionalAccuracy	dq_absoluteexternalpositionalaccuracy
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadInteresado	publicidadinteresado
LADM_COL_V1_1.LADM_Nucleo.LA_BAUnitTipo	la_baunittipo
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLindero	puntolindero
LADM_COL_V1_1.LADM_Nucleo.COL_GrupoInteresadoTipo	col_grupointeresadotipo
Catastro_Registro_Nucleo_V2_2_1.COL_InteresadoDocumentoTipo	col_interesadodocumentotipo
Catastro_Registro_Nucleo_V2_2_1.COL_AcuerdoTipo	col_acuerdotipo
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoRedServicios	la_espaciojuridicoredservicios
LADM_COL_V1_1.LADM_Nucleo.topografoFuente	topografofuente
LADM_COL_V1_1.LADM_Nucleo.LA_FuenteAdministrativaTipo	la_fuenteadministrativatipo
Catastro_Registro_Nucleo_V2_2_1.COL_RestriccionTipo	col_restricciontipo
Catastro_Registro_Nucleo_V2_2_1.COL_DescripcionPuntoTipo	col_descripcionpuntotipo
LADM_COL_V1_1.LADM_Nucleo.LA_TareaInteresadoTipo	la_tareainteresadotipo
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.predio_copropiedad	predio_copropiedad
LADM_COL_V1_1.LADM_Nucleo.CC_MetodoOperacion	cc_metodooperacion
LADM_COL_V1_1.LADM_Nucleo.mas	mas
Catastro_Registro_Nucleo_V2_2_1.COL_TipoConstruccionTipo	col_tipoconstrucciontipo
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadFuente	publicidadfuente
Catastro_Registro_Nucleo_V2_2_1.COL_EstructuraTipo	col_estructuratipo
Catastro_Registro_Nucleo_V2_2_1.COL_InstitucionTipo	col_instituciontipo
LADM_COL_V1_1.LADM_Nucleo.COL_AreaValor	col_areavalor
LADM_COL_V1_1.LADM_Nucleo.cclFuente	cclfuente
LADM_COL_V1_1.LADM_Nucleo.rrrFuente	rrrfuente
Catastro_Registro_Nucleo_V2_2_1.COL_ExplotacionTipo	col_explotaciontipo
LADM_COL_V1_1.LADM_Nucleo.OM_Proceso	om_proceso
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Interesado_Contacto	interesado_contacto
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteAdministrativaTipo	col_fuenteadministrativatipo
LADM_COL_V1_1.LADM_Nucleo.LA_RelacionNecesariaUnidadesEspaciales	la_relacionnecesariaunidadesespaciales
LADM_COL_V1_1.LADM_Nucleo.LA_Agrupacion_Interesados	la_agrupacion_interesados
Catastro_Registro_Nucleo_V2_2_1.COL_DerechoTipo	col_derechotipo
LADM_COL_V1_1.LADM_Nucleo.ueFuente	uefuente
Catastro_Registro_Nucleo_V2_2_1.COL_TerritorioAgricola_Terreno_Territorio_Agricola	col_territorioagricola_terreno_territorio_agricola
Catastro_Registro_Nucleo_V2_2_1.COL_RedServiciosTipo	col_redserviciostipo
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteEspacial	col_fuenteespacial
LADM_COL_V1_1.LADM_Nucleo.puntoCl	puntocl
LADM_COL_V1_1.LADM_Nucleo.LA_VolumenTipo	la_volumentipo
LADM_COL_V1_1.LADM_Nucleo.LA_RRR	la_rrr
LADM_COL_V1_1.LADM_Nucleo.ExtUnidadEdificacionFisica	extunidadedificacionfisica
\.


--
-- TOC entry 12425 (class 0 OID 336029)
-- Dependencies: 2110
-- Data for Name: t_ili2db_column_prop; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_column_prop (tablename, subtype, columnname, tag, setting) FROM stdin;
col_areavalor	\N	areasize	ch.ehi.ili2db.unit	m2
la_unidadespacial	\N	poligono_creado	ch.ehi.ili2db.c1Max	1806900.0
terreno	\N	punto_referencia	ch.ehi.ili2db.c2Min	23000.0
terreno	\N	poligono_creado	ch.ehi.ili2db.c2Min	23000.0
la_punto	\N	localizacion_original	ch.ehi.ili2db.c1Max	1806900.0
predio	\N	avaluo_predio	ch.ehi.ili2db.unit	COP
lindero	\N	geometria	ch.ehi.ili2db.c1Min	165000.0
gm_surface2dlistvalue	\N	avalue	ch.ehi.ili2db.c2Min	23000.0
la_espaciojuridicounidadedificacion	\N	punto_referencia	ch.ehi.ili2db.c2Max	1984900.0
lindero	\N	geometria	ch.ehi.ili2db.c2Max	1984900.0
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.c1Max	1806900.0
la_caraslindero	\N	geometria	ch.ehi.ili2db.c3Max	6000.0
la_caraslindero	\N	geometria	ch.ehi.ili2db.c2Min	23000.0
terreno	\N	punto_referencia	ch.ehi.ili2db.c1Min	165000.0
lindero	\N	longitud	ch.ehi.ili2db.unit	m
puntolindero	\N	localizacion_original	ch.ehi.ili2db.c2Min	23000.0
terreno	\N	poligono_creado	ch.ehi.ili2db.c1Max	1806900.0
terreno	\N	poligono_creado	ch.ehi.ili2db.c1Min	165000.0
la_volumenvalor	\N	volumen_medicion	ch.ehi.ili2db.unit	m
la_cadenacaraslimite	\N	geometria	ch.ehi.ili2db.c1Min	165000.0
construccion	\N	poligono_creado	ch.ehi.ili2db.c2Max	1984900.0
la_espaciojuridicoredservicios	\N	poligono_creado	ch.ehi.ili2db.c1Max	1806900.0
lindero	\N	geometria	ch.ehi.ili2db.c1Max	1806900.0
gm_surface2dlistvalue	\N	avalue	ch.ehi.ili2db.c2Max	1984900.0
la_unidadespacial	\N	poligono_creado	ch.ehi.ili2db.c1Min	165000.0
la_espaciojuridicoredservicios	\N	poligono_creado	ch.ehi.ili2db.c1Min	165000.0
terreno	\N	punto_referencia	ch.ehi.ili2db.c2Max	1984900.0
la_espaciojuridicoredservicios	\N	punto_referencia	ch.ehi.ili2db.c1Max	1806900.0
gm_surface2dlistvalue	\N	avalue	ch.ehi.ili2db.c1Min	165000.0
la_punto	\N	localizacion_original	ch.ehi.ili2db.c2Min	23000.0
gm_surface2dlistvalue	\N	avalue	ch.ehi.ili2db.c1Max	1806900.0
la_caraslindero	\N	geometria	ch.ehi.ili2db.c1Min	165000.0
la_espaciojuridicoredservicios	\N	poligono_creado	ch.ehi.ili2db.c2Min	23000.0
la_caraslindero	\N	geometria	ch.ehi.ili2db.c1Max	1806900.0
la_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.c1Min	165000.0
construccion	\N	punto_referencia	ch.ehi.ili2db.c1Max	1806900.0
la_espaciojuridicounidadedificacion	\N	punto_referencia	ch.ehi.ili2db.c1Min	165000.0
la_agrupacionunidadesespaciales	\N	punto_referencia	ch.ehi.ili2db.c2Max	1984900.0
servidumbrepaso	\N	poligono_creado	ch.ehi.ili2db.c1Max	1806900.0
puntolevantamiento	\N	localizacion_original	ch.ehi.ili2db.c1Max	1806900.0
unidadconstruccion	\N	punto_referencia	ch.ehi.ili2db.c1Min	165000.0
construccion	\N	poligono_creado	ch.ehi.ili2db.c1Max	1806900.0
puntolevantamiento	\N	localizacion_original	ch.ehi.ili2db.c2Min	23000.0
la_espaciojuridicoredservicios	\N	poligono_creado	ch.ehi.ili2db.c2Max	1984900.0
puntolindero	\N	localizacion_original	ch.ehi.ili2db.c1Max	1806900.0
extdireccion	\N	coordenada_direccion	ch.ehi.ili2db.c1Min	165000.0
la_unidadespacial	\N	punto_referencia	ch.ehi.ili2db.c2Min	23000.0
unidadconstruccion	\N	avaluo_unidad_construccion	ch.ehi.ili2db.unit	COP
la_caraslindero	\N	geometria	ch.ehi.ili2db.c3Min	-1000.0
la_agrupacionunidadesespaciales	\N	punto_referencia	ch.ehi.ili2db.c1Max	1806900.0
terreno	\N	area_registral	ch.ehi.ili2db.unit	m2
la_espaciojuridicoredservicios	\N	punto_referencia	ch.ehi.ili2db.c2Min	23000.0
la_espaciojuridicounidadedificacion	\N	poligono_creado	ch.ehi.ili2db.c1Max	1806900.0
puntolindero	\N	exactitud_horizontal	ch.ehi.ili2db.unit	cm
puntolevantamiento	\N	exactitud_horizontal	ch.ehi.ili2db.unit	cm
la_cadenacaraslimite	\N	geometria	ch.ehi.ili2db.c2Min	23000.0
terreno	\N	avaluo_terreno	ch.ehi.ili2db.unit	COP
puntolindero	\N	localizacion_original	ch.ehi.ili2db.c2Max	1984900.0
la_agrupacionunidadesespaciales	\N	punto_referencia	ch.ehi.ili2db.c2Min	23000.0
construccion	\N	poligono_creado	ch.ehi.ili2db.c1Min	165000.0
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.c2Max	1984900.0
unidadconstruccion	\N	punto_referencia	ch.ehi.ili2db.c2Min	23000.0
construccion	\N	avaluo_construccion	ch.ehi.ili2db.unit	COP
la_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.c2Max	1984900.0
servidumbrepaso	\N	punto_referencia	ch.ehi.ili2db.c2Min	23000.0
extdireccion	\N	coordenada_direccion	ch.ehi.ili2db.c1Max	1806900.0
la_caraslindero	\N	geometria	ch.ehi.ili2db.c2Max	1984900.0
lindero	\N	geometria	ch.ehi.ili2db.c2Min	23000.0
servidumbrepaso	\N	poligono_creado	ch.ehi.ili2db.c2Min	23000.0
la_cadenacaraslimite	\N	geometria	ch.ehi.ili2db.c2Max	1984900.0
puntocontrol	\N	localizacion_original	ch.ehi.ili2db.c1Max	1806900.0
puntolindero	\N	exactitud_vertical	ch.ehi.ili2db.unit	cm
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.c3Max	6000.0
la_espaciojuridicounidadedificacion	\N	punto_referencia	ch.ehi.ili2db.c2Min	23000.0
construccion	\N	poligono_creado	ch.ehi.ili2db.c2Min	23000.0
la_espaciojuridicoredservicios	\N	punto_referencia	ch.ehi.ili2db.c2Max	1984900.0
extdireccion	\N	coordenada_direccion	ch.ehi.ili2db.c2Max	1984900.0
servidumbrepaso	\N	punto_referencia	ch.ehi.ili2db.c1Max	1806900.0
unidadconstruccion	\N	poligono_creado	ch.ehi.ili2db.c2Max	1984900.0
unidadconstruccion	\N	punto_referencia	ch.ehi.ili2db.c1Max	1806900.0
puntocontrol	\N	localizacion_original	ch.ehi.ili2db.c2Max	1984900.0
terreno	\N	punto_referencia	ch.ehi.ili2db.c1Max	1806900.0
terreno	\N	poligono_creado	ch.ehi.ili2db.c2Max	1984900.0
la_unidadespacial	\N	punto_referencia	ch.ehi.ili2db.c2Max	1984900.0
puntolindero	\N	localizacion_original	ch.ehi.ili2db.c1Min	165000.0
la_espaciojuridicounidadedificacion	\N	poligono_creado	ch.ehi.ili2db.c2Min	23000.0
puntolevantamiento	\N	exactitud_vertical	ch.ehi.ili2db.unit	cm
la_punto	\N	localizacion_original	ch.ehi.ili2db.c2Max	1984900.0
la_unidadespacial	\N	poligono_creado	ch.ehi.ili2db.c2Max	1984900.0
la_unidadespacial	\N	punto_referencia	ch.ehi.ili2db.c1Min	165000.0
unidadconstruccion	\N	poligono_creado	ch.ehi.ili2db.c1Max	1806900.0
puntocontrol	\N	exactitud_vertical	ch.ehi.ili2db.unit	cm
la_espaciojuridicounidadedificacion	\N	poligono_creado	ch.ehi.ili2db.c1Min	165000.0
construccion	\N	punto_referencia	ch.ehi.ili2db.c2Min	23000.0
la_unidadespacial	\N	poligono_creado	ch.ehi.ili2db.c2Min	23000.0
la_unidadespacial	\N	punto_referencia	ch.ehi.ili2db.c1Max	1806900.0
la_espaciojuridicounidadedificacion	\N	punto_referencia	ch.ehi.ili2db.c1Max	1806900.0
unidadconstruccion	\N	area_construida	ch.ehi.ili2db.unit	m2
servidumbrepaso	\N	poligono_creado	ch.ehi.ili2db.c1Min	165000.0
servidumbrepaso	\N	punto_referencia	ch.ehi.ili2db.c2Max	1984900.0
puntocontrol	\N	localizacion_original	ch.ehi.ili2db.c1Min	165000.0
la_espaciojuridicounidadedificacion	\N	poligono_creado	ch.ehi.ili2db.c2Max	1984900.0
la_espaciojuridicoredservicios	\N	punto_referencia	ch.ehi.ili2db.c1Min	165000.0
unidadconstruccion	\N	poligono_creado	ch.ehi.ili2db.c1Min	165000.0
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.c2Min	23000.0
la_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.c1Max	1806900.0
la_transformacion	\N	localizacion_transformada	ch.ehi.ili2db.c2Min	23000.0
construccion	\N	punto_referencia	ch.ehi.ili2db.c1Min	165000.0
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.c3Min	-1000.0
la_punto	\N	localizacion_original	ch.ehi.ili2db.c1Min	165000.0
puntolevantamiento	\N	localizacion_original	ch.ehi.ili2db.c2Max	1984900.0
servidumbrepaso	\N	punto_referencia	ch.ehi.ili2db.c1Min	165000.0
unidadconstruccion	\N	poligono_creado	ch.ehi.ili2db.c2Min	23000.0
unidadconstruccion	\N	punto_referencia	ch.ehi.ili2db.c2Max	1984900.0
extdireccion	\N	coordenada_direccion	ch.ehi.ili2db.c2Min	23000.0
la_agrupacionunidadesespaciales	\N	punto_referencia	ch.ehi.ili2db.c1Min	165000.0
gm_surface3dlistvalue	\N	avalue	ch.ehi.ili2db.c1Min	165000.0
construccion	\N	punto_referencia	ch.ehi.ili2db.c2Max	1984900.0
la_cadenacaraslimite	\N	geometria	ch.ehi.ili2db.c1Max	1806900.0
puntolevantamiento	\N	localizacion_original	ch.ehi.ili2db.c1Min	165000.0
puntocontrol	\N	localizacion_original	ch.ehi.ili2db.c2Min	23000.0
servidumbrepaso	\N	poligono_creado	ch.ehi.ili2db.c2Max	1984900.0
puntocontrol	\N	exactitud_horizontal	ch.ehi.ili2db.unit	cm
terreno	\N	area_calculada	ch.ehi.ili2db.unit	m2
unidadconstruccion	\N	area_privada_construida	ch.ehi.ili2db.unit	m2
\.


--
-- TOC entry 12426 (class 0 OID 336035)
-- Dependencies: 2111
-- Data for Name: t_ili2db_dataset; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_dataset (t_id, datasetname) FROM stdin;
\.


--
-- TOC entry 12427 (class 0 OID 336038)
-- Dependencies: 2112
-- Data for Name: t_ili2db_import; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_import (t_id, dataset, importdate, importuser, importfile) FROM stdin;
\.


--
-- TOC entry 12428 (class 0 OID 336041)
-- Dependencies: 2113
-- Data for Name: t_ili2db_import_basket; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_import_basket (t_id, import, basket, objectcount, start_t_id, end_t_id) FROM stdin;
\.


--
-- TOC entry 12429 (class 0 OID 336044)
-- Dependencies: 2114
-- Data for Name: t_ili2db_import_object; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_import_object (t_id, import_basket, class, objectcount, start_t_id, end_t_id) FROM stdin;
\.


--
-- TOC entry 12430 (class 0 OID 336047)
-- Dependencies: 2115
-- Data for Name: t_ili2db_inheritance; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_inheritance (thisclass, baseclass) FROM stdin;
ISO19107_V1_MAGNABOG.GM_Surface3DListValue	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Punto	LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado
LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite	LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado
LADM_COL_V1_1.LADM_Nucleo.CC_MetodoOperacion	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RRR	LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado
LADM_COL_V1_1.LADM_Nucleo.LA_RelacionNecesariaUnidadesEspaciales	LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado
LADM_COL_V1_1.LADM_Nucleo.baunitFuente	\N
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Predio	LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion	\N
ISO19107_V1_MAGNABOG.GM_Surface2DListValue	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquiaGrupo	\N
LADM_COL_V1_1.LADM_Nucleo.ueBaunit	\N
ISO19107_V1_MAGNABOG.GM_MultiSurface2D	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_AbsoluteExternalPositionalAccuracy	LADM_COL_V1_1.LADM_Nucleo.DQ_PositionalAccuracy
Catastro_Registro_Nucleo_V2_2_1.COL_TerritorioAgricola_Terreno_Territorio_Agricola	\N
Catastro_Registro_Nucleo_V2_2_1.COL_Afectacion_Terreno_Afectacion	\N
LADM_COL_V1_1.LADM_Nucleo.relacionFuenteUespacial	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.UnidadConstruccion	LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion
LADM_COL_V1_1.LADM_Nucleo.Fraccion	\N
LADM_COL_V1_1.LADM_Nucleo.ueFuente	\N
LADM_COL_V1_1.LADM_Nucleo.COL_AreaValor	\N
LADM_COL_V1_1.LADM_Nucleo.miembros	\N
LADM_COL_V1_1.LADM_Nucleo.puntoFuente	\N
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente	\N
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteEspacial	LADM_COL_V1_1.LADM_Nucleo.COL_Fuente
LADM_COL_V1_1.LADM_Nucleo.ueNivel	\N
Catastro_Registro_Nucleo_V2_2_1.COL_ExplotacionTipo_Terreno_Explotacion	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoControl	LADM_COL_V1_1.LADM_Nucleo.LA_Punto
LADM_COL_V1_1.LADM_Nucleo.menos	\N
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion	LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial
LADM_COL_V1_1.LADM_Nucleo.LI_Lineaje	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Nivel	LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Publicidad	LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado
ISO19107_V1_MAGNABOG.GM_MultiSurface3D	\N
LADM_COL_V1_1.LADM_Nucleo.Oid	\N
LADM_COL_V1_1.LADM_Nucleo.relacionFuente	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Transformacion	\N
LADM_COL_V1_1.LADM_Nucleo.ueUeGrupo	\N
LADM_COL_V1_1.LADM_Nucleo.DQ_Element	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLevantamiento	LADM_COL_V1_1.LADM_Nucleo.LA_Punto
LADM_COL_V1_1.LADM_Nucleo.LA_CarasLindero	LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado
LADM_COL_V1_1.LADM_Nucleo.relacionUe	\N
LADM_COL_V1_1.LADM_Nucleo.cclFuente	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Lindero	LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite
LADM_COL_V1_1.LADM_Nucleo.ExtArchivo	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Restriccion	LADM_COL_V1_1.LADM_Nucleo.LA_RRR
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteAdministrativa	LADM_COL_V1_1.LADM_Nucleo.COL_Fuente
LADM_COL_V1_1.LADM_Nucleo.unidadFuente	\N
LADM_COL_V1_1.LADM_Nucleo.LA_RelacionNecesariaBAUnits	LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado
LADM_COL_V1_1.LADM_Nucleo.rrrInteresado	\N
LADM_COL_V1_1.LADM_Nucleo.baunitRrr	\N
LADM_COL_V1_1.LADM_Nucleo.menosf	\N
LADM_COL_V1_1.LADM_Nucleo.baunitComoInteresado	\N
Catastro_Registro_Nucleo_V2_2_1.COL_BosqueAreaSemi_Terreno_Bosque_Area_Seminaturale	\N
LADM_COL_V1_1.LADM_Nucleo.Imagen	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadInteresado	\N
LADM_COL_V1_1.LADM_Nucleo.puntoCcl	\N
Catastro_Registro_Nucleo_V2_2_1.COL_CuerpoAgua_Terreno_Evidencia_Cuerpo_Agua	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Hipoteca	Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Restriccion
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.ServidumbrePaso	LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Interesado_Contacto	\N
LADM_COL_V1_1.LADM_Nucleo.LA_TareaInteresadoTipo	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Derecho	LADM_COL_V1_1.LADM_Nucleo.LA_RRR
LADM_COL_V1_1.LADM_Nucleo.mas	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.InteresadoContacto	\N
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado	LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado
LADM_COL_V1_1.LADM_Nucleo.ExtUnidadEdificacionFisica	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLindero	LADM_COL_V1_1.LADM_Nucleo.LA_Punto
LADM_COL_V1_1.LADM_Nucleo.OM_Proceso	\N
LADM_COL_V1_1.LADM_Nucleo.CI_ParteResponsable	\N
LADM_COL_V1_1.LADM_Nucleo.clFuente	\N
Catastro_Registro_Nucleo_V2_2_1.COL_ServidumbreTipo_Terreno_Servidumbre	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado	LADM_COL_V1_1.LADM_Nucleo.LA_Interesado
LADM_COL_V1_1.LADM_Nucleo.CI_Contacto	\N
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.predio_copropiedad	\N
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoRedServicios	LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial
LADM_COL_V1_1.LADM_Nucleo.LA_Agrupacion_Interesados	LADM_COL_V1_1.LADM_Nucleo.LA_Interesado
LADM_COL_V1_1.LADM_Nucleo.topografoFuente	\N
LADM_COL_V1_1.LADM_Nucleo.rrrFuente	\N
LADM_COL_V1_1.LADM_Nucleo.relacionBaunit	\N
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno	LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.hipotecaDerecho	\N
LADM_COL_V1_1.LADM_Nucleo.responsableFuente	\N
LADM_COL_V1_1.LADM_Nucleo.masCcl	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadFuente	\N
LADM_COL_V1_1.LADM_Nucleo.OM_Observacion	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.ConstruccionUnidadConstruccion	\N
LADM_COL_V1_1.LADM_Nucleo.ExtRedServiciosFisica	\N
LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit	LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Construccion	LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion
LADM_COL_V1_1.LADM_Nucleo.DQ_PositionalAccuracy	LADM_COL_V1_1.LADM_Nucleo.DQ_Element
LADM_COL_V1_1.LADM_Nucleo.ExtInteresado	\N
LADM_COL_V1_1.LADM_Nucleo.LA_VolumenValor	\N
LADM_COL_V1_1.LADM_Nucleo.LA_AgrupacionUnidadesEspaciales	LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado
LADM_COL_V1_1.LADM_Nucleo.puntoCl	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadBAUnit	\N
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Responsabilidad	LADM_COL_V1_1.LADM_Nucleo.LA_RRR
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial	LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado
\.


--
-- TOC entry 12431 (class 0 OID 336053)
-- Dependencies: 2116
-- Data for Name: t_ili2db_meta_attrs; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_meta_attrs (ilielement, attr_name, attr_value) FROM stdin;
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Lindero.no_overlaps	name	no_overlaps
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLindero.no_overlaps	name	no_overlaps
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Validar Area	ilivalid.msg	el objeto {su_Espacio_De_Nombres} - {su_Local_Id} no forma un area continua y sin superposisciones
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.Validar Area	name	Validar Area
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno.no_overlaps	name	no_overlaps
\.


--
-- TOC entry 12432 (class 0 OID 336059)
-- Dependencies: 2117
-- Data for Name: t_ili2db_model; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_model (file, iliversion, modelname, content, importdate) FROM stdin;
LADM_COL_V1_1.ili	2.3	LADM_COL_V1_1{ ISO19107_V1_MAGNABOG}	INTERLIS 2.3;\n\n/** ISO 19152 LADM country profile COL Core Model.\n * \n * -----------------------------------------------------------\n * \n * LADM es un modelo conceptual de la realidad que concreta una ontolog�a y establece una sem�ntica para la administraci�n del territorio.\n * \n * -----------------------------------------------------------\n *  revision history\n * -----------------------------------------------------------\n * \n *  30.01.2018/fm : Cambio del tipo de dato del atributo Ext_Direccion de la clase Unidad Espacial a ExtDireccion; atributo ext_PID de la calse LA_Interesado cambia de OID a ExtInteresado; Cambio de cardinalidad en relacion miembros entre LA_Interesado y LA_Agrupacion_Interesados de 0..1 a 0..*\n *  07.02.2018/fm-gc: Ajuste al tipo de dato de la unidad Peso, pasa a tener precision 1 para evitar ser tratado cmo atributo entero y aumentar su tama�o\n *  19.02.2018/fm-gc: ampliaci�n del dominio al tipo de dato Peso\n *  26.02.2018/fm-lj: cambio del nombre del dominio ISO19125_Type a ISO19125_Tipo\n *  19.04.2018/vb fm: Ajuste al constraint Fraccion, denominador mayor a 0\n *  19.04.2018/vb fm: Cambio en la cardinalidad del atributo u_Local_Id de la clase LA_BAUnit de 0..1 a 1\n * 17.07.2018/fm : se incluye escritura en dominio COL_FuenteAdministrativaTipo\n * 10.08.2018/fm : Se eliminan los atributos ai_local_id y ai_espacio_de_nombres de la clase LA_Agrupacion_Interesados\n * 27.08.2018/fm : Ajuste a la cardinalidad de asociacion puntoFuente de 1..* a 0..*\n * 25.09.2018/at: Se ajusta la longitud del atributo Codigo_Registral_Transaccion en la clase COL_FuenteAdministrativa a 5 caracteres de acuerdo a la Resoluci�n 3973 de 2018\n * -----------------------------------------------------------\n * \n *  (c) IGAC y SNR con apoyo de la Cooperacion Suiza\n * \n * -----------------------------------------------------------\n */\nMODEL LADM_COL_V1_1 (es)\nAT "http://www.proadmintierra.info/"\nVERSION "V1.1.0"  // 2018-04-19 // =\n  IMPORTS ISO19107_V1_MAGNABOG;\n\n  UNIT\n\n    PesoColombiano [COP] EXTENDS INTERLIS.MONEY;\n\n    Area (ABSTRACT) = (INTERLIS.LENGTH * INTERLIS.LENGTH);\n\n    MetroCuadrado [m2] EXTENDS Area = (INTERLIS.m * INTERLIS.m);\n\n    Centrimetro [cm] = 1 / 100 [INTERLIS.m];\n\n  TOPIC LADM_Nucleo(ABSTRACT) =\n\n    DOMAIN\n\n      CharacterString = TEXT*255;\n\n      COL_AreaTipo = (\n        Area_Calculada_Altura_Local,\n        Area_Calculada_Altura_Mar,\n        Area_Catastral_Administrativa,\n        Area_Estimado_Construccion,\n        Area_No_Oficial,\n        Area_Registral\n      );\n\n      COL_FuenteEspacialTipo = (\n        Croquis_Campo,\n        Protocolo_Posicionamiento,\n        Informe_Calculo,\n        Datos_Crudos\n      );\n\n      COL_FuncionInteresadoTipo = (\n        Abogado_Demandas,\n        Administrador_Estado,\n        Banco,\n        Ciudadano,\n        Juez,\n        Notario,\n        Reconocedor_Agrimensor\n      );\n\n      COL_GrupoInteresadoTipo = (\n        Grupo_BAUnit,\n        Grupo_Civil,\n        Grupo_Empresarial,\n        Grupo_Etnico\n      );\n\n      COL_LevelContentTipo = (\n        Construccion_Convencional,\n        Construccion_No_Convencional,\n        Consuetudinario,\n        Formal,\n        Informal,\n        Responsabilidad,\n        Restriccion_Derecho_Publico,\n        Restriction_Derecho_Privado\n      );\n\n      Integer = 0 .. 999999999;\n\n      LA_VolumenTipo = (\n        Oficial,\n        Calculado,\n        Otro\n      );\n\n      COL_EstadoDisponibilidadTipo = (\n        Convertido,\n        Desconocido,\n        Disponible\n      );\n\n      Currency = -2000000000.00 .. 2000000000.00;\n\n      LA_FuenteEspacialTipo = (\n        Topografia,\n        Plano,\n        Fotografia_Aerea,\n        Otro\n      );\n\n      Real = 0.000 .. 999999999.999;\n\n    STRUCTURE COL_AreaValor =\n      areaSize : MANDATORY 0.0 .. 99999999999999.9 [LADM_COL_V1_1.m2];\n      type : MANDATORY COL_AreaTipo;\n    END COL_AreaValor;\n\n    DOMAIN\n\n      COL_FuenteAdministrativaTipo = (\n        Escritura,\n        Certificado,\n        Contrato,\n        Documento_Identidad,\n        Informe,\n        Formulario_Predial,\n        Promesa_Compraventa,\n        Reglamento,\n        Resolucion,\n        Sentencia,\n        Solicitud,\n        Acta,\n        Acuerdo,\n        Auto,\n        Estatuto_Social,\n        Decreto,\n        Providencia,\n        Acta_Colindancia,\n        Libros_Antiguo_Sistema_Registral,\n        Informe_Colindancia,\n        Carta_Venta\n      );\n\n      LA_DimensionTipo = (\n        Dim2D,\n        Dim3D,\n        otro\n      );\n\n      LA_EstadoDisponibilidadTipo = (\n        Original,\n        Destruido,\n        Incompleto,\n        Otro\n      );\n\n      Peso = 0.0 .. 999999999999999.0 [LADM_COL_V1_1.COP];\n\n      LA_Agrupacion_Interesados_Tipo = (\n        Asociacion,\n        Familia,\n        Otro\n      );\n\n      LA_RelacionSuperficieTipo = (\n        En_Rasante,\n        En_Vuelo,\n        En_Subsuelo,\n        Otro\n      );\n\n      LA_InteresadoTipo = (\n        Persona_Natural,\n        Persona_No_Natural,\n        Otro\n      );\n\n      LA_UnidadEdificacionTipo = (\n        Privado,\n        Comercial,\n        Estado,\n        Otro\n      );\n\n      LA_BAUnitTipo = (\n        Unidad_Propiedad_Basica,\n        Unidad_Derecho,\n        Otro\n      );\n\n      LA_EstadoRedServiciosTipo = (\n        Planeado,\n        En_Uso,\n        Fuera_De_Servicio,\n        Otro\n      );\n\n      LA_DerechoTipo = (\n        Propiedad,\n        Consuetudinario,\n        Arrendamiento,\n        Otro\n      );\n\n      LA_RedServiciosTipo = (\n        Electricidad,\n        Gas,\n        Agua,\n        Alcantarillado,\n        Otro\n      );\n\n      LA_RegistroTipo = (\n        Rural,\n        Urbano,\n        Otro\n      );\n\n      LA_RestriccionTipo = (\n        Servidumbres,\n        Otro\n      );\n\n      LA_EstructuraTipo = (\n        Punto,\n        Linea,\n        Poligono,\n        Otro\n      );\n\n      LA_ResponsabilidadTipo = (\n        Policia_Areas_Inundables,\n        Otro\n      );\n\n      LA_ContenidoNivelTipo = (\n        Derecho_Primario,\n        Consuetudinario,\n        Otro\n      );\n\n      LA_HipotecaTipo = (\n        Lineal,\n        Micro_Credito,\n        Otro\n      );\n\n      LA_FuenteAdministrativaTipo = (\n        Escritura,\n        Titulo,\n        Otro\n      );\n\n      LA_InterpolacionTipo = (\n        Inicio,\n        Final,\n        Centro_Arco,\n        Otro\n      );\n\n      LA_MonumentacionTipo = (\n        Baliza,\n        Poste,\n        Otro\n      );\n\n      LA_PuntoTipo = (\n        Control,\n        Catastro,\n        Otro\n      );\n\n      ISO19125_Tipo = (\n        Disjunto,\n        Toca,\n        Superpone,\n        Desconocido\n      );\n\n      DQ_Metodo_Evaluacion_Codigo_Tipo = (\n        Interno_Directo,\n        Externo_Directo,\n        Indirecto\n      );\n\n      /** Dominio que proviene de la traducci�n de CI_RoleCode de la norma ISO 19115:2003. Da los valores de dominio v�lidos para la funci�n realizada por la parte responsable.\n       */\n      CI_CodigoTarea = (\n        Proveedor_De_Recursos,\n        Custodio,\n        Propietario,\n        Usuario,\n        Distribuidor,\n        Creador,\n        Punto_De_Contacto,\n        Investigador_Principal,\n        Procesador,\n        Editor,\n        Autor\n      );\n\n      /** Traducci�n del dominio CI_PresentationFormCode de la norma ISO 19115:2003. Indica el modo en el que se representan los datos.\n       */\n      CI_Forma_Presentacion_Codigo = (\n        /** Definici�n en la ISO 19115:2003.\n         */\n        Imagen,\n        /** Definici�n en la ISO 19115:2003.\n         */\n        Mapa,\n        /** Definici�n en la ISO 19115:2003.\n         */\n        Modelo,\n        /** Definici�n en la ISO 19115:2003.\n         */\n        Perfil,\n        /** Definici�n en la ISO 19115:2003.\n         */\n        Tabla,\n        /** Definici�n en la ISO 19115:2003.\n         */\n        Video,\n        /** Definici�n en la ISO 19115:2003.\n         */\n        Audio,\n        /** Definici�n en la ISO 19115:2003.\n         */\n        Diagrama,\n        /** Definici�n en la ISO 19115:2003.\n         */\n        Multimedia,\n        /** Definici�n en la ISO 19115:2003.\n         */\n        Muestra_Fisica,\n        /** Definici�n en la ISO 19115:2003.\n         */\n        Otro\n      );\n\n    /** Estructura que permite definir el Oid o identificadores de objeto. Viene marcado en la propia norma ISO 19152:2012, LADM.\n     */\n    STRUCTURE Oid =\n      /** Identificador local asignado por el proveedor de los datos.\n       */\n      localId : MANDATORY CharacterString;\n      /** Identificador de la fuente de datos del objeto.\n       */\n      espacioDeNombres : MANDATORY CharacterString;\n    END Oid;\n\n    /** Estructura para la definici�n de un tipo de dato personalizado que permite indicar una fracci�n o quebrado cona serie espec�fica de condiciones.\n     */\n    STRUCTURE Fraccion =\n      /** Parte inferior de la fracci�n. Debe ser mayor que 0. Debe ser mayor que el numerador.\n       */\n      Denominador : MANDATORY Integer;\n      /** Parte superior de la fracci�n. Debe ser mayor que 0. Debe sder menor que el denominador.\n       */\n      Numerador : MANDATORY Integer;\n      MANDATORY CONSTRAINT\n        Denominador > 0;\n      MANDATORY CONSTRAINT\n        Numerador > 0;\n      MANDATORY CONSTRAINT\n        Denominador >= Numerador;\n    END Fraccion;\n\n    /** Referencia a una imagen mediante su url.\n     */\n    STRUCTURE Imagen =\n      /** url de la imagen.\n       */\n      uri : CharacterString;\n    END Imagen;\n\n    /** Clase traducida a partir de DQ_Element de la norma ISO 19157.\n     * Contiene los aspectos de la informaci�n de calidad cuantitativa. REVISAR MODELADO\n     */\n    STRUCTURE DQ_Element =\n      /** Nombre de la prueba aplicada a los datos. Proviene de la agregaci�n de la clase DQ_MeasureReference a DQ_Element.\n       */\n      Nombre_Medida : CharacterString;\n      /** Identificador de la medida, valor que identifica de manera �nica la medida dentro de un espacio de nombres. Proviene de la agregaci�n de la clase DQ_MeasureReference a DQ_Element.\n       */\n      Identificacion_Medida : CharacterString;\n      /** Descripci�n. Proviene de la agregaci�n de la clase DQ_MeasureReference a DQ_Element.\n       */\n      Descripcion_Medida : CharacterString;\n      /** M�todo utilizado para evaluar la calidad de los datos. Proviene de la agregaci�n de la clase DQ_EvaluationMethod a DQ_Element.\n       */\n      Metodo_Evaluacion : DQ_Metodo_Evaluacion_Codigo_Tipo;\n      /** Descripci�n del m�todo de evaluaci�n. Proviene de la agregaci�n de la clase DQ_EvaluationMethod a DQ_Element.\n       */\n      Descripcion_Metodo_Evaluacion : CharacterString;\n      /** Referencia a la informaci�n del procedimiento. Proviene de la agregaci�n de la clase DQ_MeasureReference a DQ_Element.\n       */\n      Procedimiento_Evaluacion : CharacterString;\n      /** Fecha y hora en la que se generan los resultados. Proviene de la agregaci�n de la clase DQ_Result a DQ_Element.\n       */\n      Fecha_Hora : INTERLIS.XMLDateTime;\n      /** Alcance del resultado de la prueba de calidad. Proviene de la agregaci�n de la clase DQ_Result a DQ_Element.\n       */\n      Resultado : CharacterString;\n    END DQ_Element;\n\n    /** estructura no utilizada, se materializa sobre los atributos Extactitud horizontal y vertical\n     */\n    STRUCTURE DQ_PositionalAccuracy\n    EXTENDS DQ_Element =\n      /** MODELAR.\n       */\n      atributo21 : CharacterString;\n    END DQ_PositionalAccuracy;\n\n    /** DEFINIR y DOCUMENTAR. Se hace necesaria para su uso por ObjetoVersionado.\n     */\n    STRUCTURE DQ_AbsoluteExternalPositionalAccuracy\n    EXTENDS DQ_PositionalAccuracy =\n      /** DEFINIR\n       */\n      atributo1 : CharacterString;\n    END DQ_AbsoluteExternalPositionalAccuracy;\n\n    /** Estructura que da soporte a los metadatos que documentan el linaje, informaci�n concerniente a las fuentes y a los procesos de producci�n, y procedente de la norma ISO 19115. Con respecto a la clase de dicha norma, presenta s�lo el atributo statement.\n     */\n    STRUCTURE LI_Lineaje =\n      /** Explicaci�n general del conocimiento del productor de datos sobre el linaje de un recurso.\n       */\n      Statement : CharacterString;\n    END LI_Lineaje;\n\n    /** Clase traducida CI_Contact de la ISO 19115.\n     * Almacena la informaci�n requerida para permitir el contacto con la persona responsable y la organizaci�n.\n     */\n    STRUCTURE CI_Contacto =\n      /** N�meros de tel�fono en los que la organizaci�n o el individuo pueden ser contactados.\n       */\n      Telefono : CharacterString;\n      /** Direcci�n f�sica y de correo electr�nico en la que se puede contactar a la organizaci�n o al individuo.\n       */\n      Direccion : CharacterString;\n      /** Informaci�n en l�nea que se puede usar para contactar al individuo o a la organizaci�n.\n       */\n      Fuente_En_Linea : CharacterString;\n      /** Per�odo de tiempo, incluida la zona horaria, en el que la organizaci�n o el individuo pueden ser contactados.\n       */\n      Horario_De_Atencion : CharacterString;\n      /** Instrucciones complementarias sobre c�mo o cu�ndo contactar al individuo o a la organizaci�n.\n       */\n      Instrucciones_Contacto : CharacterString;\n    END CI_Contacto;\n\n    /** Clase traducida CI_ResponsibleParty de la ISO 19115:2003. Identificaci�n de los responsables del recurso y el papel de la parte en el recurso.\n     */\n    STRUCTURE CI_ParteResponsable =\n      /** Nombre individual del responsable. Se proporciona si la organizaci�n o la posici�n no son proporcionados.\n       */\n      Nombre_Individual : CharacterString;\n      /** Nombre de la organizaci�n responsable. Se proporciona si el nombre individual o la posici�n no se prov�n.\n       */\n      Nombre_Organizacion : CharacterString;\n      /** Posici�n de la persona responsable. Se proporcionar� si NombreIndividual o Organizacion no son\n       * proporcionados.\n       */\n      Posicion : CharacterString;\n      /** Ver clase CI_Contacto.\n       */\n      Informacion_Contacto : LADM_COL_V1_1.LADM_Nucleo.CI_Contacto;\n      /** Funci�n realizada por la parte responsable.\n       */\n      Funcion : CI_CodigoTarea;\n    END CI_ParteResponsable;\n\n    /** Estructura que proviene de la traducci�n de la clase CC_OperationMethod de la ISO 19111. Indica el m�todo utilizado, mediante un algoritmo o un procedimiento, para realizar operaciones con coordenadas.\n     */\n    STRUCTURE CC_MetodoOperacion =\n      /** F�rmulas o procedimientos utilizadoa por este m�todo de operaci�n de coordenadas. Esto puede ser una referencia a una publicaci�n. Tenga en cuenta que el m�todo de operaci�n puede no ser anal�tico, en cuyo caso este atributo hace referencia o contiene el procedimiento, no una f�rmula anal�tica.\n       */\n      Formula : MANDATORY CharacterString;\n      /** N�mero de dimensiones en la fuente CRS de este m�todo de operaci�n de coordenadas.\n       */\n      Dimensiones_Origen : Integer;\n      /** N�mero de dimensiones en el CRS de destino de este m�todo de operaci�n de coordenadas.\n       */\n      Ddimensiones_Objetivo : Integer;\n    END CC_MetodoOperacion;\n\n    /** Registro de la f�rmula o procedimiento utilizado en la transformaci�n y de su resultado.\n     */\n    STRUCTURE LA_Transformacion =\n      /** F�rmula o procedimiento utilizado en la transformaci�n.\n       */\n      Transformacion : MANDATORY LADM_COL_V1_1.LADM_Nucleo.CC_MetodoOperacion;\n      /** Geometr�a una vez realizado el proceso de transformaci�n.\n       */\n      Localizacion_Transformada : MANDATORY ISO19107_V1_MAGNABOG.GM_Point2D;\n    END LA_Transformacion;\n\n    /** Estructura que pone a disposici�n del modelo la clase OM_Observation de la ISO 19156 y de la que s�lo implementa un atributo de los cinco que tiene la clase origina: resultQuality.\n     */\n    STRUCTURE OM_Observacion =\n      /** Resultado del proceso de calidad, conforme a DQ_Element.\n       */\n      Resultado_Calidad : LADM_COL_V1_1.LADM_Nucleo.DQ_Element;\n    END OM_Observacion;\n\n    /** Estructura que define los diferentes tipos de interesados que pueden darse.\n     */\n    STRUCTURE LA_TareaInteresadoTipo =\n      Tipo : (\n        topografo,\n        notario,\n        otro\n      );\n    END LA_TareaInteresadoTipo;\n\n    /** Estructura que pone a disposici�n del modelo la clase OM_Process de la ISO 19156. No desarrollado, debe ser definido por los pilotos\n     */\n    STRUCTURE OM_Proceso =\n    END OM_Proceso;\n\n    /** Referencia a una clase externa para gestionar direcciones.\n     */\n    STRUCTURE ExtDireccion =\n      /** Nombre del �rea en la que se encuentra la direcci�n.\n       */\n      Nombre_Area_Direccion : CharacterString;\n      /** Par de valores georreferenciados (x,y) en la que se encuentra la direcci�n.\n       */\n      Coordenada_Direccion : ISO19107_V1_MAGNABOG.GM_Point2D;\n      /** Identificador local de la direcci�n.\n       */\n      Direccion_ID : MANDATORY LADM_COL_V1_1.LADM_Nucleo.Oid;\n      /** Nombre del edificio.\n       */\n      Nombre_Edificio : CharacterString;\n      /** N�mero de edificio.\n       */\n      Numero_Edificio : CharacterString;\n      Ciudad : CharacterString;\n      Pais : CharacterString;\n      Codigo_Postal : CharacterString;\n      Apartado_Correo : CharacterString;\n      Departamento : CharacterString;\n      /** Nombre de la calle.\n       */\n      Nombre_Calle : CharacterString;\n    END ExtDireccion;\n\n    /** Clase abstracta que permite gestionar el hist�rico del conjunto de clases, las cuales heredan de esta, excepto las fuentes.\n     */\n    CLASS ObjetoVersionado (ABSTRACT) =\n      /** Comienzo de la validez actual de la instancia de un objeto.\n       */\n      Comienzo_Vida_Util_Version : MANDATORY INTERLIS.XMLDateTime;\n      /** Finnzo de la validez actual de la instancia de un objeto.\n       */\n      Fin_Vida_Util_Version : INTERLIS.XMLDateTime;\n      /** Metadatos relativos a la calidad de la instancia.\n       */\n      Calidad : LIST {0..*} OF LADM_COL_V1_1.LADM_Nucleo.DQ_Element;\n      /** Metadatos corresondientes a la responsabilidad de la instancia.\n       */\n      Procedencia : LIST {0..*} OF LADM_COL_V1_1.LADM_Nucleo.CI_ParteResponsable;\n      MANDATORY CONSTRAINT\n        Fin_Vida_Util_Version >= Comienzo_Vida_Util_Version;\n    END ObjetoVersionado;\n\n    /** Control externo de la unidad de edificaci�n f�sica.\n     */\n    STRUCTURE ExtUnidadEdificacionFisica =\n      Ext_Direccion_ID : LADM_COL_V1_1.LADM_Nucleo.ExtDireccion;\n    END ExtUnidadEdificacionFisica;\n\n    /** Referencia a una clase externa para gestionar direcciones.\n     */\n    STRUCTURE ExtInteresado =\n      /** Identificador externo del interesado.\n       */\n      Ext_Direccion_ID : LADM_COL_V1_1.LADM_Nucleo.ExtDireccion;\n      Huella_Dactilar : LADM_COL_V1_1.LADM_Nucleo.Imagen;\n      Nombre : CharacterString;\n      /** Identificador local del interesado.\n       */\n      Interesado_ID : LADM_COL_V1_1.LADM_Nucleo.Oid;\n      Fotografia : LADM_COL_V1_1.LADM_Nucleo.Imagen;\n      Firma : LADM_COL_V1_1.LADM_Nucleo.Imagen;\n    END ExtInteresado;\n\n    /** Referencia a una clase externa para gestionar las redes f�sicas de servicios.\n     */\n    STRUCTURE ExtRedServiciosFisica =\n      /** Indica si la red de servicios tiene un gradiente o no.\n       */\n      Orientada : BOOLEAN;\n      /** Identificador de referencia a un interesado externo que es el administrador.\n       */\n      Ext_Interesado_Administrador_ID : LADM_COL_V1_1.LADM_Nucleo.ExtInteresado;\n    END ExtRedServiciosFisica;\n\n    /** Referencia a clase externa desde donde se gestiona el repositorio de archivos.\n     */\n    STRUCTURE ExtArchivo =\n      /** Fecha en la que ha sido aceptado el documento.\n       */\n      Fecha_Aceptacion : INTERLIS.XMLDate;\n      /** Datos que contiene el documento.\n       */\n      Datos : CharacterString;\n      /** �ltima fecha de extracci�n del documento.\n       */\n      Extraccion : INTERLIS.XMLDate;\n      /** Fecha en la que el documento es aceptado en el sistema.\n       */\n      Fecha_Grabacion : INTERLIS.XMLDate;\n      /** Fecha en la que fue entregado el documento.\n       */\n      Fecha_Entrega : INTERLIS.XMLDate;\n      /** Definici�n del identificador �nico global del documento.\n       */\n      s_Espacio_De_Nombres : MANDATORY CharacterString;\n      /** Identificador local del documento.\n       */\n      s_Local_Id : MANDATORY CharacterString;\n    END ExtArchivo;\n\n    /** Clase abstracta. Esta clase es la personalizaci�n en el modelo del perfil colombiano de la clase de LADM LA_Source.\n     */\n    CLASS COL_Fuente (ABSTRACT) =\n      Fecha_Aceptacion : INTERLIS.XMLDateTime;\n      /** Indica si la fuente est� o no disponible y en qu� condiciones. Tambi�n puede indicar porqu� ha dejado de estar disponible, si ha ocurrido.\n       */\n      Estado_Disponibilidad : MANDATORY COL_EstadoDisponibilidadTipo;\n      /** Identificador del archivo fuente controlado por una clase externa.\n       */\n      Ext_Archivo_ID : LADM_COL_V1_1.LADM_Nucleo.ExtArchivo;\n      /** Fecha de inicio de validez de la fuente.\n       */\n      Sello_Inicio_Validez : INTERLIS.XMLDateTime;\n      /** Tipo de formato en el que es presentada la fuente, de acuerdo con el registro de metadatos.\n       */\n      Tipo_Principal : CI_Forma_Presentacion_Codigo;\n      /** Descripci�n de la calidad del documento de acuerdo a los metadatos del objeto DQ_Element, clase de la norma ISO 19157 que se refiere a aspectos de la informaci�n de calidad cuantitativa de la instancia referenciada.\n       */\n      Calidad : LIST {0..*} OF LADM_COL_V1_1.LADM_Nucleo.DQ_Element;\n      /** Fecha en la que es almacenado el documento fuente.\n       */\n      Fecha_Grabacion : INTERLIS.XMLDateTime;\n      /** Parte responsable de la aceptaci�n, con todos los metadatos gestionados por la clase CI_ParteResponsable, que hace referencia a la norma ISO 19115:2003.\n       */\n      Procedencia : LIST {0..*} OF LADM_COL_V1_1.LADM_Nucleo.CI_ParteResponsable;\n      /** Fecha en la que se entrega la fuente.\n       */\n      Fecha_Entrega : INTERLIS.XMLDateTime;\n      /** Identificaci�n in�quivoca de la fuente en el sistema.\n       */\n      s_Espacio_De_Nombres : MANDATORY CharacterString;\n      /** Identificador de la fuente en el sistema local.\n       */\n      s_Local_Id : MANDATORY CharacterString;\n      /** Indica si se trata de un documento oficial o no.\n       */\n      Oficialidad : BOOLEAN;\n    END COL_Fuente;\n\n    /** Estructura para la definici�n de un tipo de dato personalizado que permite indicar la medici�n de un volumen y la naturaleza de este.\n     */\n    STRUCTURE LA_VolumenValor =\n      /** Medici�n del volumen en m3.\n       */\n      Volumen_Medicion : MANDATORY 0.0 .. 99999999999999.9 [INTERLIS.m];\n      /** Indicaci�n de si el volumen es calculado, si figura como oficial o si se da otra circunstancia.\n       */\n      Tipo : MANDATORY LA_VolumenTipo;\n    END LA_VolumenValor;\n\n    /** Especializaci�n de la clase COL_Fuente para almacenar aquellas fuentes constituidas por documentos (documento hipotecario, documentos notariales, documentos hist�ricos, etc.) que documentan la relaci�n entre instancias de interesados y de predios.\n     */\n    CLASS COL_FuenteAdministrativa\n    EXTENDS COL_Fuente =\n      /** Descripci�n del documento.\n       */\n      Texto : CharacterString;\n      /** Tipo de documento de fuente administrativa.\n       */\n      Tipo : MANDATORY COL_FuenteAdministrativaTipo;\n      /** C�digo registral de la transacci�n que se documenta.\n       */\n      Codigo_Registral_Transaccion : TEXT*5;\n      /** Identificador del documento, ejemplo: numero de la resoluci�n\n       */\n      Nombre : TEXT*50;\n    END COL_FuenteAdministrativa;\n\n    /** Traducci�n al espa�ol de la clase LA_SpatialUnit de LADM.\n     */\n    CLASS LA_UnidadEspacial\n    EXTENDS ObjetoVersionado =\n      Area : LIST {0..*} OF LADM_COL_V1_1.LADM_Nucleo.COL_AreaValor;\n      Dimension : LA_DimensionTipo;\n      /** Corresponde al atributo extAddressID de la clase en LADM.\n       */\n      Ext_Direccion_ID : LIST {0..*} OF LADM_COL_V1_1.LADM_Nucleo.ExtDireccion;\n      /** Corresponde al atributo label de la clase en LADM.\n       */\n      Etiqueta : CharacterString;\n      /** Corresponde al atributo referencePoint de la clase en LADM.\n       */\n      Punto_Referencia : ISO19107_V1_MAGNABOG.GM_Point2D;\n      /** Corresponde al atributo surfaceRelation de la clase en LADM.\n       */\n      Relacion_Superficie : LA_RelacionSuperficieTipo;\n      /** Corresponde al atributo volume de la clase en LADM.\n       */\n      Volumen : LIST {0..*} OF LADM_COL_V1_1.LADM_Nucleo.LA_VolumenValor;\n      /** Identificador �nico global. Corresponde al atributo suID de la clase en LADM.\n       */\n      su_Espacio_De_Nombres : MANDATORY CharacterString;\n      /** Identificador �nico local.\n       */\n      su_Local_Id : MANDATORY CharacterString;\n      /** Materializacion del metodo createArea(). Almacena de forma permanente la geometr�a de tipo poligonal.\n       */\n      poligono_creado : ISO19107_V1_MAGNABOG.GM_MultiSurface2D;\n    END LA_UnidadEspacial;\n\n    /** Agrupa unidades espaciales, es decir, representaciones geogr�ficas de las unidades administrativas b�sicas (clase LA_BAUnit) para representar otras unidades espaciales que se forman en base a estas, como puede ser el caso de los pol�gonos catastrales.\n     */\n    CLASS LA_AgrupacionUnidadesEspaciales\n    EXTENDS ObjetoVersionado =\n      /** Nivel jer�rquico de la agrupaci�n, dentro del anidamiento de diferentes agrupaciones.\n       */\n      Nivel_Jerarquico : MANDATORY Integer;\n      /** Definici�n de la agrupaci�n.\n       */\n      Etiqueta : CharacterString;\n      /** Nombre que recibe la agrupaci�n.\n       */\n      Nombre : CharacterString;\n      /** Punto de referencia de toda la agrupaci�n, a modo de centro de masas.\n       */\n      Punto_Referencia : ISO19107_V1_MAGNABOG.GM_Point2D;\n      /** Identificar �nico global de la agrupaci�n.\n       */\n      sug_Espacio_De_Nombres : MANDATORY CharacterString;\n      /** Identificador �nico local de la agrupaci�n.\n       */\n      sug_Local_Id : MANDATORY CharacterString;\n    END LA_AgrupacionUnidadesEspaciales;\n\n    /** Traducci�n al espa�ol de la clase LA_LegalSpaceBuildingUnit. Sus intancias son las unidades de edificaci�n\n     */\n    CLASS LA_EspacioJuridicoUnidadEdificacion\n    EXTENDS LA_UnidadEspacial =\n      /** Identificador de la unidad de edificaci�n.\n       */\n      Ext_Unidad_Edificacion_Fisica_ID : LADM_COL_V1_1.LADM_Nucleo.ExtUnidadEdificacionFisica;\n      /** Tipo de unidad de edificaci�n de la que se trata.\n       */\n      Tipo : LA_UnidadEdificacionTipo;\n    END LA_EspacioJuridicoUnidadEdificacion;\n\n    /** Traducci�n al espa�ol de la clase LA_LegalSpaceUtilityNetwork. Representa un tipo de unidad espacial (LA_UNidadEspacial) cuyas instancias son las redes de servicios.\n     */\n    CLASS LA_EspacioJuridicoRedServicios\n    EXTENDS LA_UnidadEspacial =\n      /** Identificador de la red f�sica hacia una referencia externa.\n       */\n      ext_ID_Red_Fisica : LADM_COL_V1_1.LADM_Nucleo.ExtRedServiciosFisica;\n      /** Estado de operatividad de la red.\n       */\n      Estado : LA_EstadoRedServiciosTipo;\n      /** Tipo de servicio que presta.\n       */\n      Tipo : LA_RedServiciosTipo;\n    END LA_EspacioJuridicoRedServicios;\n\n    /** Traducci�n de la calse LA_Level de LADM.\n     */\n    CLASS LA_Nivel\n    EXTENDS ObjetoVersionado =\n      n_ID : MANDATORY LADM_COL_V1_1.LADM_Nucleo.Oid;\n      Nombre : CharacterString;\n      Registro_Tipo : LA_RegistroTipo;\n      Estructura : LA_EstructuraTipo;\n      Tipo : LA_ContenidoNivelTipo;\n    END LA_Nivel;\n\n    /** Traducci�n al espa�ol de la clase LA_RequiredRelationshipSpatialUnit de LADM.\n     */\n    CLASS LA_RelacionNecesariaUnidadesEspaciales\n    EXTENDS ObjetoVersionado =\n      Relacion : MANDATORY ISO19125_Tipo;\n    END LA_RelacionNecesariaUnidadesEspaciales;\n\n    ASSOCIATION relacionUe =\n      rue1 -- {0..*} LA_UnidadEspacial;\n      rue2 -- {0..*} LA_UnidadEspacial;\n    END relacionUe;\n\n    ASSOCIATION ueJerarquia =\n      uej1 -- {0..*} LA_UnidadEspacial;\n      uej2 -<> {0..1} LA_UnidadEspacial;\n    END ueJerarquia;\n\n    ASSOCIATION ueJerarquiaGrupo =\n      set -<> {0..1} LA_AgrupacionUnidadesEspaciales;\n      element -- {0..*} LA_AgrupacionUnidadesEspaciales;\n    END ueJerarquiaGrupo;\n\n    ASSOCIATION ueUeGrupo =\n      parte -- {0..*} LA_UnidadEspacial;\n      todo -- {0..*} LA_AgrupacionUnidadesEspaciales;\n    END ueUeGrupo;\n\n    ASSOCIATION ueNivel =\n      ue -- {0..*} LA_UnidadEspacial;\n      nivel -- {0..1} LA_Nivel;\n    END ueNivel;\n\n    /** Clase abstracta que agrupa los atributos comunes de las clases para los derechos (rights), las responsabilidades (responsabilities) y las restricciones (restrictions).\n     */\n    CLASS LA_RRR (ABSTRACT)\n    EXTENDS ObjetoVersionado =\n      /** Descripci�n relatical al derecho, la responsabilidad o la restricci�n.\n       */\n      Descripcion : CharacterString;\n      /** Participaci�n, en modo de fracci�n, en la subclase LA_Derecho, LA_Responsabilidad o LA_Restriccion.\n       */\n      Compartido : LADM_COL_V1_1.LADM_Nucleo.Fraccion;\n      /** Indicaci�n de si comparte o no.\n       */\n      Comprobacion_Comparte : BOOLEAN;\n      /** Descripci�n de cual es el uso efectivo.\n       */\n      Uso_Efectivo : CharacterString;\n      /** Identificador global �nico.\n       */\n      r_Espacio_De_Nombres : MANDATORY CharacterString;\n      /** Identificador �nico local.\n       */\n      r_Local_Id : MANDATORY CharacterString;\n    END LA_RRR;\n\n    /** De forma gen�rica, representa el objeto territorial legal (Catastro 2014) que se gestiona en el modelo, en este caso, la parcela catastral o predio. Es independiente del conocimiento de su realidad espacial y se centra en su existencia conocida y reconocida.\n     */\n    CLASS LA_BAUnit\n    EXTENDS ObjetoVersionado =\n      /** Nombre que recibe la unidad administrativa b�sica, en muchos casos topon�mico, especialmente en terrenos r�sticos.\n       */\n      Nombre : CharacterString;\n      /** Tipo de derecho que la reconoce.\n       */\n      Tipo : MANDATORY LA_BAUnitTipo;\n      /** Identificador �nico global.\n       */\n      u_Espacio_De_Nombres : MANDATORY CharacterString;\n      /** Identificador �nico local.\n       */\n      u_Local_Id : MANDATORY CharacterString;\n    END LA_BAUnit;\n\n    ASSOCIATION rrrFuente =\n      rfuente -- {1..*} COL_FuenteAdministrativa;\n      rrr -- {0..*} LA_RRR;\n    END rrrFuente;\n\n    /** Traducci�n de la clase LA_RequiredRelationshipBAUnit de LADM.\n     */\n    CLASS LA_RelacionNecesariaBAUnits\n    EXTENDS ObjetoVersionado =\n      Relacion : MANDATORY CharacterString;\n    END LA_RelacionNecesariaBAUnits;\n\n    ASSOCIATION ueBaunit =\n      ue (EXTERNAL) -- {0..*} LA_UnidadEspacial;\n      baunit -- {0..*} LA_BAUnit;\n    END ueBaunit;\n\n    ASSOCIATION relacionBaunit =\n      unidad1 -- {0..*} LA_BAUnit;\n      unidad2 -- {0..*} LA_BAUnit;\n    END relacionBaunit;\n\n    ASSOCIATION relacionFuente =\n      refuente -- {0..*} COL_FuenteAdministrativa;\n      relacionrequeridaBaunit -- {0..*} LA_RelacionNecesariaBAUnits;\n    END relacionFuente;\n\n    ASSOCIATION baunitRrr =\n      unidad -- {1} LA_BAUnit;\n      rrr -- {1..*} LA_RRR;\n    END baunitRrr;\n\n    ASSOCIATION unidadFuente =\n      ufuente -- {0..*} COL_FuenteAdministrativa;\n      unidad -- {0..*} LA_BAUnit;\n    END unidadFuente;\n\n    /** Traducci�n al espa�ol de la clase LA_Point de LADM.\n     */\n    CLASS LA_Punto\n    EXTENDS ObjetoVersionado =\n      /** Atributo no usado, se materializa sobre los atributos Extactitud horizontal y vertical\n       */\n      Exactitud_Estimada : LADM_COL_V1_1.LADM_Nucleo.DQ_PositionalAccuracy;\n      Posicion_Interpolacion : LA_InterpolacionTipo;\n      Monumentacion : LA_MonumentacionTipo;\n      Localizacion_Original : MANDATORY ISO19107_V1_MAGNABOG.GM_Point2D;\n      PuntoTipo : MANDATORY LA_PuntoTipo;\n      MetodoProduccion : LADM_COL_V1_1.LADM_Nucleo.LI_Lineaje;\n      Transformacion_Y_Resultado : LIST {0..*} OF LADM_COL_V1_1.LADM_Nucleo.LA_Transformacion;\n      p_Espacio_De_Nombres : MANDATORY CharacterString;\n      p_Local_Id : MANDATORY CharacterString;\n    END LA_Punto;\n\n    /** Especializaci�n de la clase COL_Fuente para almacenar las fuentes constituidas por datos espaciales (entidades geogr�ficas, im�genes de sat�lite, vuelos fotogram�tricos, listados de coordenadas, mapas, planos antiguos o modernos, descripci�n de localizaciones, etc.) que documentan t�cnicamente la relaci�n entre instancias de interesados y de predios\n     */\n    CLASS COL_FuenteEspacial\n    EXTENDS COL_Fuente =\n      Mediciones : LIST {0..*} OF LADM_COL_V1_1.LADM_Nucleo.OM_Observacion;\n      /** No desarrollado, debe ser definido por los pilotos\n       */\n      Procedimiento : LADM_COL_V1_1.LADM_Nucleo.OM_Proceso;\n      Tipo : MANDATORY COL_FuenteEspacialTipo;\n    END COL_FuenteEspacial;\n\n    /** Traducci�n al espa�ol de la clase LA_BoundaryFaceString de LADM. Define los linderos y a su vez puede estar definida por una descrici�n textual o por dos o m�s puntos. Puede estar asociada a una fuente espacial o m�s.\n     */\n    CLASS LA_CadenaCarasLimite\n    EXTENDS ObjetoVersionado =\n      /** Geometr�a lineal que define el lindero. Puede estar asociada a geometr�as de tipo punto que definen sus v�rtices o ser una entidad lineal independiente.\n       */\n      Geometria : ISO19107_V1_MAGNABOG.GM_Curve2D;\n      /** Descripci�n de la localizaci�n, cuando esta se basa en texto.\n       */\n      Localizacion_Textual : CharacterString;\n      /** Identificador �nico global de la cadena de caras lindero.\n       */\n      ccl_Espacio_De_Nombres : MANDATORY CharacterString;\n      /** Identificador local de la cadena de caras lindero.\n       */\n      ccl_Local_Id : MANDATORY CharacterString;\n    END LA_CadenaCarasLimite;\n\n    /** Traducci�n de la clase LA_BoundaryFace de LADM. De forma similar a LA_CadenaCarasLindero, representa los l�mites, pero en este caso permite representaci�n 3D.\n     */\n    CLASS LA_CarasLindero\n    EXTENDS ObjetoVersionado =\n      /** Geometr�a en 3D del l�mite o lindero, asociada a putos o a descripciones textuales.\n       */\n      Geometria : ISO19107_V1_MAGNABOG.GM_MultiSurface3D;\n      /** Cuando la localizaci�n del l�mte est� dada por una descripci�n textual, aqu� se recoge esta.\n       */\n      Localizacion_Textual : CharacterString;\n      /** Identificador �nico global.\n       */\n      cl_Espacio_De_Nombres : MANDATORY CharacterString;\n      /** Identificador �nico local.\n       */\n      cl_Local_Id : MANDATORY CharacterString;\n    END LA_CarasLindero;\n\n    ASSOCIATION puntoReferencia =\n      ue (EXTERNAL) -- {0..1} LA_UnidadEspacial;\n      punto -- {0..1} LA_Punto;\n    END puntoReferencia;\n\n    ASSOCIATION puntoFuente =\n      pfuente -- {0..*} COL_FuenteEspacial;\n      punto -- {0..*} LA_Punto;\n    END puntoFuente;\n\n    ASSOCIATION ueFuente =\n      ue (EXTERNAL) -- {0..*} LA_UnidadEspacial;\n      pfuente -- {0..*} COL_FuenteEspacial;\n    END ueFuente;\n\n    ASSOCIATION baunitFuente =\n      bfuente -- {0..*} COL_FuenteEspacial;\n      unidad (EXTERNAL) -- {0..*} LA_BAUnit;\n    END baunitFuente;\n\n    ASSOCIATION relacionFuenteUespacial =\n      rfuente -- {0..*} COL_FuenteEspacial;\n      relacionrequeridaUe (EXTERNAL) -- {0..*} LA_RelacionNecesariaUnidadesEspaciales;\n    END relacionFuenteUespacial;\n\n    ASSOCIATION cclFuente =\n      ccl -- {0..*} LA_CadenaCarasLimite;\n      lfuente -- {0..*} COL_FuenteEspacial;\n    END cclFuente;\n\n    ASSOCIATION menos =\n      ccl -- {0..*} LA_CadenaCarasLimite;\n      eu (EXTERNAL) -- {0..*} LA_UnidadEspacial;\n    END menos;\n\n    ASSOCIATION masCcl =\n      cclP -- {0..*} LA_CadenaCarasLimite;\n      ueP (EXTERNAL) -- {0..*} LA_UnidadEspacial;\n    END masCcl;\n\n    ASSOCIATION puntoCcl =\n      punto -- {2..*} LA_Punto;\n      ccl -- {0..*} LA_CadenaCarasLimite;\n    END puntoCcl;\n\n    ASSOCIATION clFuente =\n      cl -- {0..*} LA_CarasLindero;\n      cfuente -- {0..*} COL_FuenteEspacial;\n    END clFuente;\n\n    ASSOCIATION menosf =\n      cl -- {0..*} LA_CarasLindero;\n      ue (EXTERNAL) -- {0..*} LA_UnidadEspacial;\n    END menosf;\n\n    ASSOCIATION mas =\n      clP -- {0..*} LA_CarasLindero;\n      ueP (EXTERNAL) -- {0..*} LA_UnidadEspacial;\n    END mas;\n\n    ASSOCIATION puntoCl =\n      punto -- {3..*} LA_Punto;\n      cl -- {0..*} LA_CarasLindero;\n    END puntoCl;\n\n    /** Traducci�n de la clase LA_Party de LADM. Representa a las personas que ejercen derechos y responsabilidades  o sufren restricciones respecto a una BAUnit.\n     */\n    CLASS LA_Interesado (ABSTRACT)\n    EXTENDS ObjetoVersionado =\n      /** Identificador del interesado.\n       */\n      ext_PID : LADM_COL_V1_1.LADM_Nucleo.ExtInteresado;\n      /** Nombre del interesado.\n       */\n      Nombre : CharacterString;\n      /** Funci�n o tarea que realiza el interesado dentro del marco de derechos, obligaciones y restricciones.\n       */\n      Tarea : LIST {0..*} OF LADM_COL_V1_1.LADM_Nucleo.LA_TareaInteresadoTipo;\n      /** Tipo de persona del que se trata.\n       */\n      Tipo : MANDATORY LA_InteresadoTipo;\n      /** Identificador �nico global.\n       */\n      p_Espacio_De_Nombres : MANDATORY CharacterString;\n      /** Identificador �nico local.\n       */\n      p_Local_Id : MANDATORY CharacterString;\n    END LA_Interesado;\n\n    /** Registra interesados que representan a grupos de personas. Se registra el grupo en si, independientemete de las personas por separado. Es lo que ocurreo, por ejemplo, con un grupo �tnico.\n     */\n    CLASS LA_Agrupacion_Interesados\n    EXTENDS LA_Interesado =\n      /** Indica el tipo de agrupaci�n del que se trata.\n       */\n      ai_Tipo : MANDATORY COL_GrupoInteresadoTipo;\n    END LA_Agrupacion_Interesados;\n\n    ASSOCIATION baunitComoInteresado =\n      interesado -- {0..*} LA_Interesado;\n      unidad (EXTERNAL) -- {0..*} LA_BAUnit;\n    END baunitComoInteresado;\n\n    ASSOCIATION responsableFuente =\n      cfuente (EXTERNAL) -- {0..*} COL_FuenteAdministrativa;\n      notario -- {0..*} LA_Interesado;\n    END responsableFuente;\n\n    ASSOCIATION rrrInteresado =\n      rrr (EXTERNAL) -- {0..*} LA_RRR;\n      interesado -- {0..1} LA_Interesado;\n    END rrrInteresado;\n\n    ASSOCIATION topografoFuente =\n      sfuente (EXTERNAL) -- {0..*} COL_FuenteEspacial;\n      topografo -- {0..*} LA_Interesado;\n    END topografoFuente;\n\n    ASSOCIATION miembros =\n      interesados -- {2..*} LA_Interesado;\n      agrupacion -<> {0..*} LA_Agrupacion_Interesados;\n      participacion : LADM_COL_V1_1.LADM_Nucleo.Fraccion;\n    END miembros;\n\n  END LADM_Nucleo;\n\nEND LADM_COL_V1_1.\n	2020-01-28 09:28:30.079
ISO19107_V1_MAGNABOG.ili	2.3	ISO19107_V1_MAGNABOG	INTERLIS 2.3;\n\nTYPE MODEL ISO19107_V1_MAGNABOG (en)\nAT "http://www.swisslm.ch/models"\nVERSION "2016-03-07"  =\n\n  DOMAIN\n\n    GM_Point2D = COORD 165000.000 .. 1806900.000 [INTERLIS.m], 23000.000 .. 1984900.000 [INTERLIS.m] ,ROTATION 2 -> 1;\n\n    GM_Curve2D = POLYLINE WITH (ARCS,STRAIGHTS) VERTEX GM_Point2D WITHOUT OVERLAPS>0.001;\n\n    GM_Surface2D = SURFACE WITH (ARCS,STRAIGHTS) VERTEX GM_Point2D WITHOUT OVERLAPS>0.001;\n\n    GM_Point3D = COORD 165000.000 .. 1806900.000 [INTERLIS.m], 23000.000 .. 1984900.000 [INTERLIS.m], -1000.000 .. 6000.000 [INTERLIS.m] ,ROTATION 2 -> 1;\n\n    GM_Curve3D = POLYLINE WITH (ARCS,STRAIGHTS) VERTEX GM_Point3D WITHOUT OVERLAPS>0.001;\n\n    GM_Surface3D = SURFACE WITH (ARCS,STRAIGHTS) VERTEX GM_Point3D WITHOUT OVERLAPS>0.001;\n\n  STRUCTURE GM_Geometry2DListValue (ABSTRACT) =\n  END GM_Geometry2DListValue;\n\n  STRUCTURE GM_Curve2DListValue =\n    value : MANDATORY GM_Curve2D;\n  END GM_Curve2DListValue;\n\n  STRUCTURE GM_Surface2DListValue =\n    value : MANDATORY GM_Surface2D;\n  END GM_Surface2DListValue;\n\n  !!@ ili2db.mapping = "MultiLine"\nSTRUCTURE GM_MultiCurve2D =\n    geometry : LIST {1..*} OF ISO19107_V1_MAGNABOG.GM_Curve2DListValue;\n  END GM_MultiCurve2D;\n\n  !!@ ili2db.mapping = "MultiSurface"\nSTRUCTURE GM_MultiSurface2D =\n    geometry : LIST {1..*} OF ISO19107_V1_MAGNABOG.GM_Surface2DListValue;\n  END GM_MultiSurface2D;\n\n  STRUCTURE GM_Curve3DListValue =\n    value : MANDATORY GM_Curve3D;\n  END GM_Curve3DListValue;\n\n  STRUCTURE GM_Surface3DListValue =\n    value : MANDATORY GM_Surface3D;\n  END GM_Surface3DListValue;\n\n  !!@ ili2db.mapping = "MultiLine"\nSTRUCTURE GM_MultiCurve3D =\n    geometry : LIST {1..*} OF ISO19107_V1_MAGNABOG.GM_Curve3DListValue;\n  END GM_MultiCurve3D;\n\n  !!@ ili2db.mapping = "MultiSurface"\nSTRUCTURE GM_MultiSurface3D =\n    geometry : LIST {1..*} OF ISO19107_V1_MAGNABOG.GM_Surface3DListValue;\n  END GM_MultiSurface3D;\n\nEND ISO19107_V1_MAGNABOG.\n	2020-01-28 09:28:30.079
Catastro_Registro_Nucleo_V2_2_1.ili	2.3	Catastro_Registro_Nucleo_V2_2_1{ ISO19107_V1_MAGNABOG LADM_COL_V1_1}	INTERLIS 2.3;\n\n/** ISO 19152 LADM country profile COL modeled with INTERLIS 2.\n * \n * -----------------------------------------------------------\n * revision history\n * -----------------------------------------------------------\n * \n * 10.05.2016/mg: EJEMPLO INTERLIS POR OFERTAS\n * 16.06.2016/mg: Taller IGAC/SNR\n * 23.08.2016/mg: Relaciones\n * 15.09.2016/mg: Comentarios Modelo\n * 20.11.2016/aa: Topic Ficha\n * 25.11.2016/aa: Ajustes FichaPredio\n * 02.12.2016/ss: Nuevas clases, atributos y tipos\n * 15.12.2016/lj: Ajuste tipos (IGAC/SNR), BAUnit GM_surface\n * 31.03.2017/fm: Simplificaci�n de herencia\n * 25.05.2017/fm: Se elimina la relacion HipotecaDerecho, se elimina la clase InteresadoBAUnit, se elimina marca abstract en las clases derivadas de RRR\n * 26.05.2017/fm: Se cambian las clases terreno servidumbre de paso y construccion al paquete de unidades espaciales. Se acorta el nombre del Modelo. ajuste al dise�o del diagrama de clases. Se elimina InteresadoNacion\n * 09.06.2017/vm: Referido al modelo LADM traducido al espa�ol\n * 09.06.2017/vm: cambio de version a 2.1.1, incluye cambios por LADM en espa�ol y de  nombres de atributo por no seguir las convenciones adoptadas.\n * 15.06.2017/fm: cambio de version a 2.1.2, se quita el atributo geometr�a de la clase predio. se reemplaza el atributo OID por los atributos atributos namespace y localId. Se a�aden atributos folio matriz y segregados al predio. se elimina el dominio transaccion_registral_tipo\n * 20.06.2017/fm: Ajuste a nombres de las clases y atributos LA_\n * 04.07.2017/sr: Ajuste de nombres de clases y atributos, creacion de relaciones, ajuste subdominios\n * 04.07.2017/fm: Se unifican los modelos LADM_ES y Catastro_COL, se eliminan las clases que extienden de responsabilidad, restriccion, derecho, hipoteca, fuente_administrativa y fuente espacial. eliminan atributos opcionales no usados de la clase hipoteca\n * 11.07.2017/fm: se adiciona el atributo poligono_creado\n * 12.07.2017/fm: se adiciona el atributo Estado_Nupre en la clase predio\n * 17.07.2017/fm: poligono creado debe ser obligatorio para la clase terreno.\n * 28.09.2017/fm : Cambio del nombre en la clase alerta por publicidad, Publicidad Extiende de objeto versionado, se elimita atributo fecha de vigencia. Ajuste al atributo plantacion comercial de la clase terreno. Se extraen los atributos de la clase predio e interesados a los modelos extendidos de ficha y registro. version 2.2.0\n * 20.10.2017/ag : Ajustes a atributos de la clase terreno, cambio a dominio multivalorado, se crean dominios, col_servidumbre, col_afectacion, col_explotacion, col_territorioAgricula, col_cuerpoAgua, se elimina la obligatoriedad del rol responsable en las relaciones responsableFuente y topografoFuente\n * 28.10.2017/gc : Soporte de geometr�as multi-parte para LA_UnidadEspacial (y las clases que la extienden) y Terreno.\n * 02.11.2017/ : Cambio del nombre del modelo de Catastro_COL_ES a Catastro_Registro_Nucleo\n * 07.11.2017/fm: Cambio de nombre a la clase CadenaCarasLindero a CadenaCarasLimite \n * 14.11.2017/fm : taducci�n del dominio COL_BuildingUnitTipo\n * 14.12.2017/fm : definicion de extends entre topics catastro registro nucleo y Ladm_nucleo\n * 30.01.2018/fm : Cambio del tipo de dato del atributo Ext_Direccion de la clase Unidad Espacial a ExtDireccion; atributo ext_PID de la calse LA_Interesado cambia de OID a ExtInteresado; Cambio de cardinalidad en relacion miembros entre LA_Interesado y LA_Agrupacion_Interesados de 0..1 a 0..*\n * 19.02.2018/fm : Cambio en longitud de atributo DocumentoIdentidad de 10 a 12 posiciones\n * 17.07.2018/fm : cambio en cardinalidad asociaci�n ConstruccionUnidadConstruccion de 1..* a 0..*; ampliaci�n del tama�o para campo de nombre en Interesado Natural; se incluyen los valores nuip, cedula militar, registro civil, cedula militar, secuencial SRN y secuencial IGAC al dominio COL_InteresadoDocumentoTipo\n * 30.07.2018/fm : Cambio obligatoriedad atributo area_registral de clase terreno de 1 a 0..1\n * 31.07.2018/fm: Creaci�n de la clase COL_Interesado integrando los atributos de interesado natural e interesado jur�dico; se agrega area en la clase construcci�n; se adiciona valor Carta_Venta al dominio COL_FuenteAdministrativaTipo; inclusion de atributo nombre en la clase COL_FuenteAdministrativa\n * 10.08.2018/fm: Eliminado clase Interesado Natural e Interesado Juridico\n * 28.08.2018/fm: Ajuste a cardinalidad en la composici�n predio_copropiedad, se elimina el requerido.\n * 28.08.2018/fm-at: Se incluye el tipo de predio conforme a la resolucion 070 de 2011; Se elimina el atributo tipo_construccion de la clase Unidad_Construcci�n ya que el dominio hace referencia a tipos de predios y no a tipos de construcciones\n * 10.09.2018/fm-at: Ajuste a los tipos de Predio conforme a la resolucion 070\n * 21.09.2018/at: Se agrega el valor "Hipoteca" al dominio COL_RestriccionTipo, se ajusta la longitud del atributo Codigo_Registral en las clases especializadas de LA_RRR de 3 a 4 caracteres\n * 25.09.2018/at: Se ajusta la longitud del atributo Codigo_Registral en las clases especializadas de LA_RRR a 5 caracteres de acuerdo a la Resoluci�n 3973 de 2018\n * 18.10.2018/at: Se agregan los atributos p_Espacio_De_Nombres y p_Local_Id a la clase Publicidad\n * 29.10.2018/fm: se amplia el tama�o de campo FMI en la clase predio para almacenar cadenas como 'LIBRO 2 TOMO 1/961 FOLIO 37/46 PARTIDA N 58'\n * -----------------------------------------------------------\n * \n * (c) IGAC y SNR con apoyo de la Cooperacion Suiza\n * \n * -----------------------------------------------------------\n */\nCONTRACTED MODEL Catastro_Registro_Nucleo_V2_2_1 (es)\nAT "http://www.proadmintierra.info/"\nVERSION "V2.2.1"  // 2018-02-19 // =\n  IMPORTS ISO19107_V1_MAGNABOG,LADM_COL_V1_1;\n\n  FUNCTION no_overlaps(Objects: OBJECTS OF ANYCLASS; SurfaceAttr : ATTRIBUTE OF @ Objects RESTRICTION ( SURFACE )): BOOLEAN;\n\n  DOMAIN\n\n    /** !! ajustar en el Catalogo de Objetos\n     */\n    COL_AcuerdoTipo = (\n      /** Existe un acuerdo sobre la posici�n del punto\n       */\n      Acuerdo,\n      /** Existe un desacuerdo sobre la posici�n del punto\n       */\n      Desacuerdo\n    );\n\n    COL_Afectacion = (\n      Inundacion,\n      /** Remocion en Masa\n       */\n      RemocionMasa,\n      Otra\n    );\n\n    COL_BosqueAreaSemi = (\n      /** �rea Boscosa\n       */\n      AreaBoscosa,\n      /** Plantaci�n Forestal\n       */\n      PlantaForestal\n    );\n\n    COL_CuerpoAgua = (\n      NacimientoAgua,\n      /** Cuerpo de agua natural o artificial\n       */\n      CuerpoAgua,\n      ZonaPantanosa\n    );\n\n    COL_DerechoTipo = (\n      Derecho_Propiedad_Colectiva,\n      Mineria_Derecho,\n      Nuda_Propiedad,\n      Ocupacion,\n      Posesion,\n      Tenencia,\n      Usufructo,\n      /** Derecho de dominio o propiedad\n       */\n      Dominio\n    );\n\n    COL_EstructuraTipo = (\n      Croquis,\n      Linea_no_Estructurada,\n      Texto,\n      Topologico\n    );\n\n    COL_ExplotacionTipo = (\n      Minera,\n      Hidrocarburo,\n      Otra\n    );\n\n    COL_GeneroTipo = (\n      Femenino,\n      Masculino,\n      Otro\n    );\n\n    COL_InteresadoDocumentoTipo = (\n      Cedula_Ciudadania,\n      Cedula_Extranjeria,\n      NIT,\n      Pasaporte,\n      Tarjeta_Identidad,\n      Libreta_Militar,\n      Registro_Civil,\n      Cedula_Militar,\n      NUIP,\n      Secuencial_SNR,\n      Secuencial_IGAC\n    );\n\n    COL_MonumentacionTipo = (\n      Incrustacion,\n      Mojon,\n      No_Materializado,\n      Otros,\n      Pilastra\n    );\n\n    /** Tipos de predios de acuerdo a la resolucion 070 de 2011\n     */\n    COL_PredioTipo = (\n      NPH,\n      PropiedadHorizontal(\n        Matriz,\n        UnidadPredial\n      ),\n      Condominio(\n        Matriz,\n        UnidadPredial\n      ),\n      Mejora,\n      ParqueCementerio(\n        Matriz,\n        UnidadPrivada\n      ),\n      Via,\n      BienUsoPublico,\n      Deposito,\n      Parqueadero,\n      Bodega\n    );\n\n    COL_ServidumbreTipo = (\n      Vial,\n      Petrolera,\n      Electrica,\n      Otra\n    );\n\n    COL_TerritorioAgricola = (\n      CultTransitorio,\n      CultPermanente,\n      Confinado,\n      /** Tierra en preparacion o descanso\n       */\n      TierraPrepodesc,\n      AreaAgriHetero,\n      Pasto\n    );\n\n    COL_UnidadEdificacionTipo = (\n      Compartido,\n      individual\n    );\n\n    COL_DefPuntoTipo = (\n      Bien_Definido,\n      No_Bien_Definido\n    );\n\n    COL_InstitucionTipo = (\n      Registraduria_Nacional,\n      Registro_Propiedad,\n      Catastro_IGAC,\n      Catastro_Descentralizado,\n      URT,\n      ANT\n    );\n\n    COL_InteresadoJuridicoTipo = (\n      Publico,\n      Privado,\n      Mixto\n    );\n\n    /** Conjunto de valores para indicar si se trata de un punto de control de referencia (un punto principal) o de apoyo (uso para levantamientos locales con estaci�n total)\n     */\n    COL_PuntoControlTipo = (\n      Control,\n      Apoyo\n    );\n\n    COL_RedServiciosTipo = (\n      Petroleo,\n      Quimicos,\n      Red_Termica,\n      Telecomunicacion\n    );\n\n    COL_ResponsabilidadTipo = (\n      Constitucional,\n      Legal,\n      Contractual,\n      Administrativa,\n      Judicial,\n      Otros\n    );\n\n    COL_DescripcionPuntoTipo = (\n      Esquina_Construccion,\n      Interseccion_Cerca_De_Piedra,\n      Interseccion_Cerca_Viva,\n      Poste_de_Cerca,\n      /** !! por definir durante pilotos\n       */\n      Otros\n    );\n\n    /** Punto de leventamiento planimetrico que se identifican en el marco de la identificaci�n de las construcciones, los linderos o puntos auxiliares levantado para el apoyo en la medicii�n\n     */\n    COL_PuntoLevTipo = (\n      Auxiliar,\n      Construccion,\n      Servidumbre\n    );\n\n    COL_RestriccionTipo = (\n      Afectaciones_Interes_General,\n      Ambientales,\n      Desplazamiento_Forzado_Restitucion,\n      Embargo,\n      Hipoteca,\n      Propiedad_Horizontal_y_Urbanismo,\n      Prohibiciones_Expresas,\n      Proteccion_Familia,\n      Servidumbre,\n      No_Registrada\n    );\n\n    COL_ViaTipo = (\n      Arteria,\n      Autopista,\n      Carreteable,\n      Cicloruta,\n      Colectora,\n      Departamental,\n      Ferrea,\n      Local,\n      Metro_o_Metrovia,\n      Nacional,\n      Ordinaria,\n      Peatonal,\n      Principal,\n      Privada,\n      Secundaria,\n      Troncal\n    );\n\n    COL_HipotecaTipo = (\n      Abierta,\n      Cerrada\n    );\n\n    /** Si ha sido situado por interpolaci�n, de qu� manera se ha hecho.\n     */\n    COL_InterpolacionTipo = (\n      Aislado,\n      Intermedio_Arco,\n      Intermedio_Linea\n    );\n\n    COL_ZonaTipo = (\n      Perimetro_Urbano,\n      Rural,\n      Corregimiento,\n      Caserios,\n      Inspecion_Policia\n    );\n\n    /** Dominio con la descripci�n de la tipologia de los codigos registrales que se inscriben y que publicitan alguna caracteristica especial del predio\n     */\n    COL_PublicidadTipo = (\n      Demanda,\n      Inicio_de_Proceso_Administrativo,\n      Cancelacion,\n      Desplazamiento_Forzado,\n      Victima_o_Restitucion,\n      Publicidad_de_Acto_Juridico\n    );\n\n    COL_TipoConstruccionTipo = (\n      Anexo,\n      No_PH,\n      Parque_Cementerio,\n      PH\n    );\n  STRUCTURE COL_Afectacion_Terreno_Afectacion = value : MANDATORY COL_Afectacion; END COL_Afectacion_Terreno_Afectacion;\n  STRUCTURE COL_BosqueAreaSemi_Terreno_Bosque_Area_Seminaturale = value : MANDATORY COL_BosqueAreaSemi; END COL_BosqueAreaSemi_Terreno_Bosque_Area_Seminaturale;\n  STRUCTURE COL_CuerpoAgua_Terreno_Evidencia_Cuerpo_Agua = value : MANDATORY COL_CuerpoAgua; END COL_CuerpoAgua_Terreno_Evidencia_Cuerpo_Agua;\n  STRUCTURE COL_ExplotacionTipo_Terreno_Explotacion = value : MANDATORY COL_ExplotacionTipo; END COL_ExplotacionTipo_Terreno_Explotacion;\n  STRUCTURE COL_ServidumbreTipo_Terreno_Servidumbre = value : MANDATORY COL_ServidumbreTipo; END COL_ServidumbreTipo_Terreno_Servidumbre;\n  STRUCTURE COL_TerritorioAgricola_Terreno_Territorio_Agricola = value : MANDATORY COL_TerritorioAgricola; END COL_TerritorioAgricola_Terreno_Territorio_Agricola;\n\n  TOPIC Catastro_Registro\n  EXTENDS LADM_COL_V1_1.LADM_Nucleo =\n    DEPENDS ON LADM_COL_V1_1.LADM_Nucleo;\n\n    /** Clase que registra las instancias de los derechos que un interesado ejerce sobre un predio. Es una especializaci�n de la clase LA_RRR del propio modelo.\n     */\n    CLASS COL_Derecho\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.LA_RRR =\n      /** Derecho que se ejerce.\n       */\n      Tipo : MANDATORY Catastro_Registro_Nucleo_V2_2_1.COL_DerechoTipo;\n      /** C�digo con el que el derecho se registra en el Registro de la Propiedad.\n       */\n      Codigo_Registral_Derecho : TEXT*5;\n    END COL_Derecho;\n\n    CLASS COL_Interesado\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.LA_Interesado =\n      /** Documento de identidad del interesado.\n       */\n      Documento_Identidad : MANDATORY TEXT*12;\n      /** Tipo de documento del que se trata.\n       */\n      Tipo_Documento : MANDATORY Catastro_Registro_Nucleo_V2_2_1.COL_InteresadoDocumentoTipo;\n      /** Quien ha emitido el documento de identidad.\n       */\n      Organo_Emisor : TEXT*20;\n      /** Fecha de emisi�n del documento de identidad.\n       */\n      Fecha_Emision : INTERLIS.XMLDate;\n      /** Primer apellido de la persona f�sica.\n       */\n      Primer_Apellido : TEXT*100;\n      /** Primer nombre de la persona f�sica.\n       */\n      Primer_Nombre : TEXT*100;\n      /** Segundo apellido de la persona f�sica.\n       */\n      Segundo_Apellido : TEXT*100;\n      /** Segundo nombre de la persona f�sica.\n       */\n      Segundo_Nombre : TEXT*100;\n      /** Nombre con el que est� inscrito.\n       */\n      Razon_Social : TEXT*250;\n      Genero : Catastro_Registro_Nucleo_V2_2_1.COL_GeneroTipo;\n      Tipo_Interesado_Juridico : Catastro_Registro_Nucleo_V2_2_1.COL_InteresadoJuridicoTipo;\n    END COL_Interesado;\n\n    /** Es un tipo de espacio jur�dico de la unidad de edificaci�n del modelo LADM que almacena datos espec�ficos del aval�o resultante del mismo.\n     */\n    CLASS Construccion\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion =\n      /** Rsultado del c�lculo de su aval�o mediante la metodolog�a legalmente establecida.\n       */\n      Avaluo_Construccion : MANDATORY LADM_COL_V1_1.LADM_Nucleo.Peso;\n      Area_Construccion : 0.0 .. 99999999999999.9;\n    END Construccion;\n\n    CLASS Interesado_Contacto =\n      Telefono1 : TEXT*20;\n      Telefono2 : TEXT*20;\n      Domicilio_Notificacion : TEXT*500;\n      Correo_Electronico : TEXT*100;\n      Origen_Datos : Catastro_Registro_Nucleo_V2_2_1.COL_InstitucionTipo;\n    END Interesado_Contacto;\n\n    /** Clase especializada de LA_CadenaCarasLindero que permite registrar los linderos.\n     * Dos linderos no pueden cruzarse ni superponerse.\n     */\n    CLASS Lindero\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite =\n      /** L�ngitud en m del lindero.\n       */\n      Longitud : MANDATORY 0.0 .. 10000.0 [INTERLIS.m];\n      !!@name="no_overlaps"\n      SET CONSTRAINT no_overlaps(ALL,>> Geometria);\n    END Lindero;\n\n    /** Clase especializada de BaUnit, que describe la unidad administrativa b�sica para el caso de Colombia.\n     * El predio es la unidad territorial legal propia de Catastro. Esta formada por el terreno y puede o no tener construcciones asociadas.\n     */\n    CLASS Predio\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit =\n      /** Corresponde al codigo del departamento al cual pertenece el predio. Es asignado por DIVIPOLA y tiene 2 d�gitos.\n       */\n      Departamento : TEXT*2;\n      /** Corresponde al codigo del municipio al cual pertenece el predio. Es asignado por DIVIPOLA y tiene 3 d�gitos.\n       */\n      Municipio : TEXT*3;\n      /** Corresponde a la zona castrastral, definida para optimizar las actividades catastrales. Es un codigo de 2 d�gitos.\n       */\n      Zona : TEXT*2;\n      /** Numero Unico de identificaci�n Predial. Es el codigo definido en el proyecto de ley que ser� el codigo de identificaci�n del predio tanto para catastratro como para Registro.\n       */\n      NUPRE : MANDATORY TEXT*20;\n      /** Folio de Matricula Inmobilidaria. Codigo �nico de identificaci�n asignado al documento registral en la oficina de registro de instrumentos p�blicos.\n       */\n      FMI : TEXT*80;\n      /** Nuevo c�digo n�merico de treinta (30) d�gitos, que se le asigna a cada predio y busca localizarlo inequ�vocamente en los documentos catastrales, seg�n el modelo determinado por el Instituto Geogr�fico Agustin Codazzi.\n       */\n      Numero_Predial : TEXT*30;\n      /** Anterior c�digo n�merico de veinte (20) digitos, que se le asigna a cada predio y busca localizarlo inequ�vocamente en los documentos catastrales, seg�n el modelo determinado por el Instituto Geogr�fico Agustin Codazzi.\n       */\n      Numero_Predial_Anterior : TEXT*20;\n      /** Valor de cada predio, obtenido mediante investigaci�n y an�lisis estadistico del mercado inmobiliario y la metodolog�a de aplicaci�n  correspondiente. El aval�o  catastral de cada predio se determina a partir de la adici�n de los aval�os parciales practicados independientemente para los terrenos y para las edificaciones en el comprendidos.\n       */\n      Avaluo_Predio : LADM_COL_V1_1.LADM_Nucleo.Peso;\n      Tipo (EXTENDED) : MANDATORY Catastro_Registro_Nucleo_V2_2_1.COL_PredioTipo;\n      UNIQUE NUPRE; \n    END Predio;\n\n    /** Clase especial del perfil colombiano de la norma ISO 19152:2012. Pretenden generar publicidad sobre el predio a partir del almacenamiento de los codigos registrales que se inscriben el FMI. No se genera ning�n tipo de derecho, ni limita la propiedad.\n     */\n    CLASS Publicidad\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado =\n      /** Indica la caracter�stica por la que se hace p�blico.\n       */\n      Tipo : MANDATORY Catastro_Registro_Nucleo_V2_2_1.COL_PublicidadTipo;\n      /** C�digo registral del FMI que se hace p�blico.\n       */\n      Codigo_Registral_Publicidad : MANDATORY TEXT*5;\n      /** Identificador global �nico.\n       */\n      p_Espacio_De_Nombres : MANDATORY LADM_COL_V1_1.LADM_Nucleo.CharacterString;\n      /** Identificador �nico local.\n       */\n      p_Local_Id : MANDATORY LADM_COL_V1_1.LADM_Nucleo.CharacterString;\n    END Publicidad;\n\n    /** Clase especializada de LA_Punto que representa puntos de la densificaci�n de la red local, que se utiliza en la operaci�n catastral para el levantamiento de informaci�n fisica de los objetos territoriales, como puntos de control.\n     */\n    CLASS PuntoControl\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.LA_Punto =\n      /** Nombre que recibe el punto.\n       */\n      Nombre_Punto : MANDATORY TEXT*20;\n      /** Exactitud vertical de la medici�n del punto.\n       */\n      Exactitud_Vertical : MANDATORY 0 .. 1000 [LADM_COL_V1_1.cm];\n      /** Exactitud horizontal de la medici�n del punto.\n       */\n      Exactitud_Horizontal : MANDATORY 0 .. 1000 [LADM_COL_V1_1.cm];\n      /** Se describe la posici�n del punto con relaci�n a su estructura, si es un punto aislado, o si hace parte de un Arco o de una linea.\n       */\n      Posicion_Interpolacion (EXTENDED) : Catastro_Registro_Nucleo_V2_2_1.COL_InterpolacionTipo;\n      Monumentacion (EXTENDED) : MANDATORY Catastro_Registro_Nucleo_V2_2_1.COL_MonumentacionTipo;\n      /** Si se trata deun punto de control o de apoyo.\n       */\n      Tipo_Punto_Control : Catastro_Registro_Nucleo_V2_2_1.COL_PuntoControlTipo;\n      /** Si el punto es o no fiable.\n       */\n      Confiabilidad : BOOLEAN;\n    END PuntoControl;\n\n    /** Clase especializada de LA_Punto que almacena puntos que definen un lindero, instancia de la clase LA_CadenaCarasLindero y sus especializaciones.\n     */\n    CLASS PuntoLindero\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.LA_Punto =\n      /** Se Indica si existe acuerdo o no entre los colindantes en relaci�n al punto lindero que se est� midiendo.\n       */\n      Acuerdo : MANDATORY Catastro_Registro_Nucleo_V2_2_1.COL_AcuerdoTipo;\n      /** Se caracteriza si el punto de levantamiento corresponde a un punto bien definido o no bien definido\n       */\n      Definicion_Punto : MANDATORY Catastro_Registro_Nucleo_V2_2_1.COL_DefPuntoTipo;\n      /** Es la descripci�n del tipo de punto lindero y las caracteristicas del vertice\n       */\n      Descripcion_Punto : Catastro_Registro_Nucleo_V2_2_1.COL_DescripcionPuntoTipo;\n      /** Corresponde a la exactitud vertical del punto lindero\n       */\n      Exactitud_Vertical : 0 .. 1000 [LADM_COL_V1_1.cm];\n      /** Corresponde a la exactitud horizontal del punto lindero\n       */\n      Exactitud_Horizontal : MANDATORY 0 .. 1000 [LADM_COL_V1_1.cm];\n      /** Indica si es o no fiable.\n       */\n      Confiabilidad : BOOLEAN;\n      /** Se describe la posici�n del punto con relaci�n a su estructura, si es un punto aislado, o si hace parte de un Arco o de una linea.\n       */\n      Posicion_Interpolacion (EXTENDED) : Catastro_Registro_Nucleo_V2_2_1.COL_InterpolacionTipo;\n      /** Si se trata de un monumento geod�sico, el tipo.\n       */\n      Monumentacion (EXTENDED) : MANDATORY Catastro_Registro_Nucleo_V2_2_1.COL_MonumentacionTipo;\n      /** Nombre o codigo del punto lindero\n       */\n      Nombre_Punto : TEXT*10;\n      !!@name="no_overlaps"\n      SET CONSTRAINT no_overlaps(ALL,>> Localizacion_Original);\n    END PuntoLindero;\n\n    /** Porci�n de tierra con una extensi�n geogr�fica definida.\n     */\n    CLASS Terreno\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial =\n      /** �rea del predio que se encuentra inscrita en el Folio de Matricula Inmobiliaria\n       */\n      Area_Registral : 0.0 .. 99999999999999.9 [LADM_COL_V1_1.m2];\n      /** �rea de predio resultado de los calculos realizados en el proceso de levantamiento planimetrico\n       */\n      Area_Calculada : MANDATORY 0.0 .. 99999999999999.9 [LADM_COL_V1_1.m2];\n      /** Valor asignado en el proceso de valoraci�n economica masiva al terreno del predio\n       */\n      Avaluo_Terreno : MANDATORY LADM_COL_V1_1.LADM_Nucleo.Peso;\n      /** se caracterizan los diferentes tipos de cultivos o territorios agricolas que conforman el predio, corresponde a la pregunta 5.3 del anexo 5.1 de los estandares de catastro multiproposito versi�n 2.1.1\n       */\n      Territorio_Agricola : BAG {0..*} OF Catastro_Registro_Nucleo_V2_2_1.COL_TerritorioAgricola_Terreno_Territorio_Agricola;\n      /** Se describe si en el predio existe presencia de bosques o �reas seminaturales, corresponde a la pregunta 5.4 del anexo 5.1 de los estandares de catastro multiproposito versi�n 2.1.1\n       */\n      Bosque_Area_Seminaturale : BAG {0..*} OF Catastro_Registro_Nucleo_V2_2_1.COL_BosqueAreaSemi_Terreno_Bosque_Area_Seminaturale;\n      /** En esta clase se identifican los valores de la pregunta 5.5. Especifique si evidencia en el terreno del Anexo 5, Versi�n 2.1.1 de Catastro Multiproposito\n       */\n      Evidencia_Cuerpo_Agua : BAG {0..*} OF Catastro_Registro_Nucleo_V2_2_1.COL_CuerpoAgua_Terreno_Evidencia_Cuerpo_Agua;\n      /** Se caracteriza si en el predio existe alg�n tipo de explotaci�n, corresponde a la pregunta 5.6 del anexo 5.1 de los estandares de catastro multiproposito versi�n 2.1.1\n       */\n      Explotacion : BAG {0..*} OF Catastro_Registro_Nucleo_V2_2_1.COL_ExplotacionTipo_Terreno_Explotacion;\n      /** Se describe si en el predio existe alguna afectaci�n natural de tipo inundaci�n o de remoci�n en masa, corresponde a la pregunta 5.7 del anexo 5.1 de los estandares de catastro multiproposito versi�n 2.1.1\n       */\n      Afectacion : BAG {0..*} OF Catastro_Registro_Nucleo_V2_2_1.COL_Afectacion_Terreno_Afectacion;\n      /** Tipo de derecho que limita el dominio de una porci�n del predio, corresponde a la pregunta 5.8 del anexo 5.1 de los estandares de catastro multiproposito versi�n 2.1.1\n       */\n      Servidumbre : BAG {0..*} OF Catastro_Registro_Nucleo_V2_2_1.COL_ServidumbreTipo_Terreno_Servidumbre;\n      /** Corresponde a la figura geometrica vectorial poligonal, generada a partir de los linderos del predio.\n       */\n      poligono_creado (EXTENDED) : MANDATORY ISO19107_V1_MAGNABOG.GM_MultiSurface2D;\n      !!@name="Validar Area"\n      !!@ilivalid.msg="el objeto {su_Espacio_De_Nombres} - {su_Local_Id} no forma un area continua y sin superposisciones"\n      SET CONSTRAINT INTERLIS.areAreas(ALL, UNDEFINED, >> poligono_creado);\n      !!@name="no_overlaps"\n      SET CONSTRAINT no_overlaps(ALL,>> poligono_creado);\n    END Terreno;\n\n    /** Restricciones a las que est� sometido un predio y que inciden sobre los derechos que pueden ejercerse sobre �l.\n     */\n    CLASS COL_Restriccion\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.LA_RRR =\n      /** Indica si es preciso o no que un interesado est� asociado a la restricci�n.\n       */\n      Interesado_Requerido : BOOLEAN;\n      /** Define el tipo de restricci�n.\n       */\n      Tipo : MANDATORY Catastro_Registro_Nucleo_V2_2_1.COL_RestriccionTipo;\n      /** C�digo con el que la responsabilidad se registra en el Registro de la Propiedad.\n       */\n      Codigo_Registral_Restriccion : TEXT*5;\n    END COL_Restriccion;\n\n    /** Clase especializada de LA_Punto que representa puntos demarcados que representan la posici�n horizontal de un v�rtice de construcci�n, servidumbre o auxiliare.\n     */\n    CLASS PuntoLevantamiento\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.LA_Punto =\n      /** Se caracterizan los diferentes tipos de punto levantamiento, estos son punto de construccci�n, punto de servidumbre o punto auxiliar\n       */\n      Tipo_Punto_Levantamiento : Catastro_Registro_Nucleo_V2_2_1.COL_PuntoLevTipo;\n      /** Se caracteriza si el punto de levantamiento corresponde a un punto bien definido o no bien definido\n       */\n      Definicion_Punto : MANDATORY Catastro_Registro_Nucleo_V2_2_1.COL_DefPuntoTipo;\n      /** Corresponde a la exactitud vertical del punto levantamiento\n       */\n      Exactitud_Vertical : 0 .. 1000 [LADM_COL_V1_1.cm];\n      /** Corresponde a la exactitud horizontal del punto levantamiento\n       */\n      Exactitud_Horizontal : 0 .. 1000 [LADM_COL_V1_1.cm];\n      /** Se describe la posici�n del punto con relaci�n a su estructura, si es un punto aislado, o si hace parte de un Arco o de una linea.\n       */\n      Posicion_Interpolacion (EXTENDED) : Catastro_Registro_Nucleo_V2_2_1.COL_InterpolacionTipo;\n      /** Definici�n sobre si el punto de levantamiento se encuentra monumentado o no y los tipos de monumentaci�n especificos para el perfil nacional\n       */\n      Monumentacion (EXTENDED) : MANDATORY Catastro_Registro_Nucleo_V2_2_1.COL_MonumentacionTipo;\n      /** Nombre que recibe el punto.\n       */\n      Nombre_Punto : TEXT*10;\n    END PuntoLevantamiento;\n\n    ASSOCIATION InteresadoContacto =\n      contacto -- {0..*} Interesado_Contacto;\n      interesado -- {1} COL_Interesado;\n    END InteresadoContacto;\n\n    ASSOCIATION predio_copropiedad =\n      predio -- {0..*} Predio;\n      copropiedad -<> {0..1} Predio;\n      coeficiente : LADM_COL_V1_1.LADM_Nucleo.Fraccion;\n    END predio_copropiedad;\n\n    ASSOCIATION PublicidadBAUnit =\n      pubicidad -- {0..*} Publicidad;\n      baunit (EXTERNAL) -- {1} LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit;\n    END PublicidadBAUnit;\n\n    ASSOCIATION PublicidadFuente =\n      publicidad -- {0..1} Publicidad;\n      fuente (EXTERNAL) -- {1..*} LADM_COL_V1_1.LADM_Nucleo.COL_FuenteAdministrativa;\n    END PublicidadFuente;\n\n    ASSOCIATION PublicidadInteresado =\n      publicidad -- {0..*} Publicidad;\n      interesado (EXTERNAL) -- {0..1} LADM_COL_V1_1.LADM_Nucleo.LA_Interesado;\n    END PublicidadInteresado;\n\n    /** Clase de tipo LA_RRR que registra las responsabilidades que las instancias de los interesados tienen sobre los predios.\n     */\n    CLASS COL_Responsabilidad\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.LA_RRR =\n      /** Definici�n del tipo de responsabilidad que se tiene.\n       */\n      Tipo : MANDATORY Catastro_Registro_Nucleo_V2_2_1.COL_ResponsabilidadTipo;\n      /** C�digo con el que la responsabilidad se registra en el Registro de la Propiedad.\n       */\n      Codigo_Registral_Responsabilidad : TEXT*5;\n    END COL_Responsabilidad;\n\n    /** Tipo de unidad espacial que permite la representaci�n de una servidumbre de paso asociada a una LA_BAUnit.\n     */\n    CLASS ServidumbrePaso\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial =\n      Identificador : MANDATORY TEXT*20;\n      /** Fecha de inscripci�n de la servidumbre en el Catastro.\n       */\n      Fecha_Inscripcion_Catastral : INTERLIS.XMLDate;\n    END ServidumbrePaso;\n\n    /** Clase que representa un tipo de restricci�n heredando de COL_Restricci�n, asociada a un derecho y que permite gestionar las hipotecas constitu�das sobre un bien inmueble, considerando las cuestiones legales nacionales.\n     */\n    CLASS COL_Hipoteca\n    EXTENDS COL_Restriccion =\n      /** Tipo de hipoteca constituida, conforme a la legislaci�n colombiana.\n       */\n      h_Tipo : Catastro_Registro_Nucleo_V2_2_1.COL_HipotecaTipo;\n      /** C�digo con el que la hipoteca se registra en el Registro de la Propiedad Inmobiliaria en el momento de ser constituida.\n       */\n      Codigo_Registral_Hipoteca : TEXT*5;\n    END COL_Hipoteca;\n\n    /** Es cada conjunto de materiales consolidados dentro de un predio que tiene una caracteristicas especificas en cuanto a elementos constitutivos f�sicos y usos de los mismos.\n     */\n    CLASS UnidadConstruccion\n    EXTENDS LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion =\n      /** Corresponde al valor catastral determinado mediante el metodo economico definido, para cada unidad de contrucci�n del predio\n       */\n      Avaluo_Unidad_Construccion : LADM_COL_V1_1.LADM_Nucleo.Peso;\n      /** N�mero de pisos que constituyen la unidad de construcci�n.\n       */\n      Numero_Pisos : MANDATORY 1 .. 100;\n      /** Area de la unidad de contrucci�n.\n       */\n      Area_Construida : 0.0 .. 99999999999999.9 [LADM_COL_V1_1.m2];\n      /** �rea privada de la unidad de construcci�n para el caso en que las construcciones tienen regimen de propiedad horizontal.\n       */\n      Area_Privada_Construida : 0.0 .. 99999999999999.9 [LADM_COL_V1_1.m2];\n    END UnidadConstruccion;\n\n    ASSOCIATION ConstruccionUnidadConstruccion =\n      unidadconstruccion -- {0..*} UnidadConstruccion;\n      construccion -<> {1} Construccion;\n    END ConstruccionUnidadConstruccion;\n\n    ASSOCIATION hipotecaDerecho =\n      hipoteca -- {0..*} COL_Hipoteca;\n      derecho -- {0..*} COL_Derecho;\n    END hipotecaDerecho;\n\n  END Catastro_Registro;\n\nEND Catastro_Registro_Nucleo_V2_2_1.\n	2020-01-28 09:28:30.079
\.


--
-- TOC entry 12433 (class 0 OID 336065)
-- Dependencies: 2118
-- Data for Name: t_ili2db_settings; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_settings (tag, setting) FROM stdin;
ch.ehi.ili2db.createMetaInfo	True
ch.ehi.ili2db.beautifyEnumDispName	underscore
ch.interlis.ili2c.ilidirs	%ILI_FROM_DB;%XTF_DIR;http://models.interlis.ch/;%JAR_DIR
ch.ehi.ili2db.arrayTrafo	coalesce
ch.ehi.ili2db.TidHandling	property
ch.ehi.ili2db.createForeignKeyIndex	yes
ch.ehi.ili2db.numericCheckConstraints	create
ch.ehi.ili2db.sender	ili2pg-3.11.2-20180208
ch.ehi.ili2db.createForeignKey	yes
ch.ehi.sqlgen.createGeomIndex	True
ch.ehi.ili2db.defaultSrsAuthority	EPSG
ch.ehi.ili2db.defaultSrsCode	3116
ch.ehi.ili2db.createEnumDefs	multiTable
ch.ehi.ili2db.uniqueConstraints	create
ch.ehi.ili2db.maxSqlNameLength	60
ch.ehi.ili2db.uuidDefaultValue	uuid_generate_v4()
ch.ehi.ili2db.inheritanceTrafo	smart2
ch.ehi.ili2db.catalogueRefTrafo	coalesce
ch.ehi.ili2db.multiPointTrafo	coalesce
ch.ehi.ili2db.StrokeArcs	enable
ch.ehi.ili2db.multiLineTrafo	coalesce
ch.ehi.ili2db.multiSurfaceTrafo	coalesce
ch.ehi.ili2db.multilingualTrafo	expand
\.


--
-- TOC entry 12434 (class 0 OID 336068)
-- Dependencies: 2119
-- Data for Name: t_ili2db_table_prop; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_table_prop (tablename, tag, setting) FROM stdin;
col_derechotipo	ch.ehi.ili2db.tableKind	ENUM
extdireccion	ch.ehi.ili2db.tableKind	STRUCTURE
col_generotipo	ch.ehi.ili2db.tableKind	ENUM
col_fuenteadministrativatipo	ch.ehi.ili2db.tableKind	ENUM
la_estadodisponibilidadtipo	ch.ehi.ili2db.tableKind	ENUM
puntocl	ch.ehi.ili2db.tableKind	ASSOCIATION
la_unidadedificaciontipo	ch.ehi.ili2db.tableKind	ENUM
li_lineaje	ch.ehi.ili2db.tableKind	STRUCTURE
publicidadfuente	ch.ehi.ili2db.tableKind	ASSOCIATION
col_afectacion_terreno_afectacion	ch.ehi.ili2db.tableKind	STRUCTURE
hipotecaderecho	ch.ehi.ili2db.tableKind	ASSOCIATION
la_monumentaciontipo	ch.ehi.ili2db.tableKind	ENUM
col_unidadedificaciontipo	ch.ehi.ili2db.tableKind	ENUM
col_viatipo	ch.ehi.ili2db.tableKind	ENUM
om_proceso	ch.ehi.ili2db.tableKind	STRUCTURE
menos	ch.ehi.ili2db.tableKind	ASSOCIATION
col_explotaciontipo_terreno_explotacion	ch.ehi.ili2db.tableKind	STRUCTURE
col_zonatipo	ch.ehi.ili2db.tableKind	ENUM
la_baunittipo	ch.ehi.ili2db.tableKind	ENUM
dq_element	ch.ehi.ili2db.tableKind	STRUCTURE
ci_forma_presentacion_codigo	ch.ehi.ili2db.tableKind	ENUM
la_estadoredserviciostipo	ch.ehi.ili2db.tableKind	ENUM
col_bosqueareasemi_terreno_bosque_area_seminaturale	ch.ehi.ili2db.tableKind	STRUCTURE
relacionue	ch.ehi.ili2db.tableKind	ASSOCIATION
gm_surface2dlistvalue	ch.ehi.ili2db.tableKind	STRUCTURE
imagen	ch.ehi.ili2db.tableKind	STRUCTURE
col_servidumbretipo_terreno_servidumbre	ch.ehi.ili2db.tableKind	STRUCTURE
la_interpolaciontipo	ch.ehi.ili2db.tableKind	ENUM
ci_contacto	ch.ehi.ili2db.tableKind	STRUCTURE
la_redserviciostipo	ch.ehi.ili2db.tableKind	ENUM
dq_metodo_evaluacion_codigo_tipo	ch.ehi.ili2db.tableKind	ENUM
la_volumentipo	ch.ehi.ili2db.tableKind	ENUM
rrrfuente	ch.ehi.ili2db.tableKind	ASSOCIATION
col_puntolevtipo	ch.ehi.ili2db.tableKind	ENUM
clfuente	ch.ehi.ili2db.tableKind	ASSOCIATION
col_publicidadtipo	ch.ehi.ili2db.tableKind	ENUM
la_responsabilidadtipo	ch.ehi.ili2db.tableKind	ENUM
iso19125_tipo	ch.ehi.ili2db.tableKind	ENUM
puntoccl	ch.ehi.ili2db.tableKind	ASSOCIATION
col_estadodisponibilidadtipo	ch.ehi.ili2db.tableKind	ENUM
col_interesadodocumentotipo	ch.ehi.ili2db.tableKind	ENUM
la_interesadotipo	ch.ehi.ili2db.tableKind	ENUM
extredserviciosfisica	ch.ehi.ili2db.tableKind	STRUCTURE
la_relacionsuperficietipo	ch.ehi.ili2db.tableKind	ENUM
uebaunit	ch.ehi.ili2db.tableKind	ASSOCIATION
la_dimensiontipo	ch.ehi.ili2db.tableKind	ENUM
la_restricciontipo	ch.ehi.ili2db.tableKind	ENUM
mas	ch.ehi.ili2db.tableKind	ASSOCIATION
col_acuerdotipo	ch.ehi.ili2db.tableKind	ENUM
col_estructuratipo	ch.ehi.ili2db.tableKind	ENUM
col_grupointeresadotipo	ch.ehi.ili2db.tableKind	ENUM
dq_positionalaccuracy	ch.ehi.ili2db.tableKind	STRUCTURE
la_agrupacion_interesados_tipo	ch.ehi.ili2db.tableKind	ENUM
col_interesadojuridicotipo	ch.ehi.ili2db.tableKind	ENUM
col_restricciontipo	ch.ehi.ili2db.tableKind	ENUM
la_tareainteresadotipo_tipo	ch.ehi.ili2db.tableKind	ENUM
cclfuente	ch.ehi.ili2db.tableKind	ASSOCIATION
col_tipoconstrucciontipo	ch.ehi.ili2db.tableKind	ENUM
la_fuenteespacialtipo	ch.ehi.ili2db.tableKind	ENUM
col_instituciontipo	ch.ehi.ili2db.tableKind	ENUM
la_transformacion	ch.ehi.ili2db.tableKind	STRUCTURE
la_estructuratipo	ch.ehi.ili2db.tableKind	ENUM
extinteresado	ch.ehi.ili2db.tableKind	STRUCTURE
col_puntocontroltipo	ch.ehi.ili2db.tableKind	ENUM
extunidadedificacionfisica	ch.ehi.ili2db.tableKind	STRUCTURE
predio_copropiedad	ch.ehi.ili2db.tableKind	ASSOCIATION
responsablefuente	ch.ehi.ili2db.tableKind	ASSOCIATION
col_cuerpoagua_terreno_evidencia_cuerpo_agua	ch.ehi.ili2db.tableKind	STRUCTURE
relacionfuenteuespacial	ch.ehi.ili2db.tableKind	ASSOCIATION
col_bosqueareasemi	ch.ehi.ili2db.tableKind	ENUM
gm_multisurface2d	ch.ehi.ili2db.tableKind	STRUCTURE
la_contenidoniveltipo	ch.ehi.ili2db.tableKind	ENUM
col_redserviciostipo	ch.ehi.ili2db.tableKind	ENUM
col_prediotipo	ch.ehi.ili2db.tableKind	ENUM
la_volumenvalor	ch.ehi.ili2db.tableKind	STRUCTURE
ci_parteresponsable	ch.ehi.ili2db.tableKind	STRUCTURE
miembros	ch.ehi.ili2db.tableKind	ASSOCIATION
menosf	ch.ehi.ili2db.tableKind	ASSOCIATION
col_servidumbretipo	ch.ehi.ili2db.tableKind	ENUM
la_derechotipo	ch.ehi.ili2db.tableKind	ENUM
dq_absoluteexternalpositionalaccuracy	ch.ehi.ili2db.tableKind	STRUCTURE
col_hipotecatipo	ch.ehi.ili2db.tableKind	ENUM
unidadfuente	ch.ehi.ili2db.tableKind	ASSOCIATION
col_afectacion	ch.ehi.ili2db.tableKind	ENUM
masccl	ch.ehi.ili2db.tableKind	ASSOCIATION
col_territorioagricola	ch.ehi.ili2db.tableKind	ENUM
ci_codigotarea	ch.ehi.ili2db.tableKind	ENUM
gm_surface3dlistvalue	ch.ehi.ili2db.tableKind	STRUCTURE
la_tareainteresadotipo	ch.ehi.ili2db.tableKind	STRUCTURE
la_puntotipo	ch.ehi.ili2db.tableKind	ENUM
col_fuenteespacialtipo	ch.ehi.ili2db.tableKind	ENUM
cc_metodooperacion	ch.ehi.ili2db.tableKind	STRUCTURE
oid	ch.ehi.ili2db.tableKind	STRUCTURE
col_explotaciontipo	ch.ehi.ili2db.tableKind	ENUM
baunitfuente	ch.ehi.ili2db.tableKind	ASSOCIATION
la_fuenteadministrativatipo	ch.ehi.ili2db.tableKind	ENUM
relacionfuente	ch.ehi.ili2db.tableKind	ASSOCIATION
uefuente	ch.ehi.ili2db.tableKind	ASSOCIATION
fraccion	ch.ehi.ili2db.tableKind	STRUCTURE
la_hipotecatipo	ch.ehi.ili2db.tableKind	ENUM
col_defpuntotipo	ch.ehi.ili2db.tableKind	ENUM
ueuegrupo	ch.ehi.ili2db.tableKind	ASSOCIATION
col_territorioagricola_terreno_territorio_agricola	ch.ehi.ili2db.tableKind	STRUCTURE
col_areatipo	ch.ehi.ili2db.tableKind	ENUM
topografofuente	ch.ehi.ili2db.tableKind	ASSOCIATION
om_observacion	ch.ehi.ili2db.tableKind	STRUCTURE
col_responsabilidadtipo	ch.ehi.ili2db.tableKind	ENUM
col_levelcontenttipo	ch.ehi.ili2db.tableKind	ENUM
col_funcioninteresadotipo	ch.ehi.ili2db.tableKind	ENUM
col_monumentaciontipo	ch.ehi.ili2db.tableKind	ENUM
relacionbaunit	ch.ehi.ili2db.tableKind	ASSOCIATION
col_descripcionpuntotipo	ch.ehi.ili2db.tableKind	ENUM
col_areavalor	ch.ehi.ili2db.tableKind	STRUCTURE
la_registrotipo	ch.ehi.ili2db.tableKind	ENUM
baunitcomointeresado	ch.ehi.ili2db.tableKind	ASSOCIATION
extarchivo	ch.ehi.ili2db.tableKind	STRUCTURE
col_cuerpoagua	ch.ehi.ili2db.tableKind	ENUM
col_interpolaciontipo	ch.ehi.ili2db.tableKind	ENUM
gm_multisurface3d	ch.ehi.ili2db.tableKind	STRUCTURE
puntofuente	ch.ehi.ili2db.tableKind	ASSOCIATION
\.


--
-- TOC entry 12435 (class 0 OID 336074)
-- Dependencies: 2120
-- Data for Name: t_ili2db_trafo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.t_ili2db_trafo (iliname, tag, setting) FROM stdin;
LADM_COL_V1_1.LADM_Nucleo.ueJerarquia	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.ServidumbrePaso	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_VolumenValor	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoControl	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.CI_Contacto	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.hipotecaDerecho	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.ExtDireccion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.Oid	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Terreno	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.puntoReferencia	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.ExtInteresado	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_RelacionNecesariaBAUnits	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.menos	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.COL_CuerpoAgua_Terreno_Evidencia_Cuerpo_Agua	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.responsableFuente	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.COL_BosqueAreaSemi_Terreno_Bosque_Area_Seminaturale	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.relacionFuenteUespacial	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial	ch.ehi.ili2db.inheritance	newAndSubClass
ISO19107_V1_MAGNABOG.GM_Surface2DListValue	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.ExtRedServiciosFisica	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.baunitFuente	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_CadenaCarasLimite	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.ueUeGrupo	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LI_Lineaje	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.ueBaunit	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Responsabilidad	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.InteresadoContacto	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.COL_Afectacion_Terreno_Afectacion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.unidadFuente	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Interesado	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_Transformacion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.ueJerarquiaGrupo	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.relacionBaunit	ch.ehi.ili2db.inheritance	newAndSubClass
ISO19107_V1_MAGNABOG.GM_Surface3DListValue	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Lindero	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_CarasLindero	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.relacionFuente	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.relacionUe	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.Imagen	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.DQ_Element	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.baunitComoInteresado	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.COL_Fuente	ch.ehi.ili2db.inheritance	subClass
LADM_COL_V1_1.LADM_Nucleo.LA_AgrupacionUnidadesEspaciales	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLevantamiento	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.ObjetoVersionado	ch.ehi.ili2db.inheritance	subClass
LADM_COL_V1_1.LADM_Nucleo.DQ_PositionalAccuracy	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.ConstruccionUnidadConstruccion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteAdministrativa	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.rrrInteresado	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.UnidadConstruccion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.puntoCcl	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_BAUnit	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.menosf	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.clFuente	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.COL_ServidumbreTipo_Terreno_Servidumbre	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.ueNivel	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.masCcl	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.ExtArchivo	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_Nivel	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.COL_ExplotacionTipo_Terreno_Explotacion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoUnidadEdificacion	ch.ehi.ili2db.inheritance	newAndSubClass
ISO19107_V1_MAGNABOG.GM_MultiSurface2D	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.Fraccion	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Construccion	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Hipoteca	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.baunitRrr	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_CarasLindero.Geometria	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
LADM_COL_V1_1.LADM_Nucleo.LA_Interesado	ch.ehi.ili2db.inheritance	subClass
LADM_COL_V1_1.LADM_Nucleo.miembros	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Predio	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Derecho	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.COL_Restriccion	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadBAUnit	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.puntoFuente	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.CI_ParteResponsable	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Publicidad	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.OM_Observacion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_Punto	ch.ehi.ili2db.inheritance	newAndSubClass
ISO19107_V1_MAGNABOG.GM_MultiSurface3D	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.DQ_AbsoluteExternalPositionalAccuracy	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadInteresado	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PuntoLindero	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_EspacioJuridicoRedServicios	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.topografoFuente	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_UnidadEspacial.poligono_creado	ch.ehi.ili2db.multiSurfaceTrafo	coalesce
LADM_COL_V1_1.LADM_Nucleo.LA_TareaInteresadoTipo	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.predio_copropiedad	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.CC_MetodoOperacion	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.mas	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.PublicidadFuente	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.COL_AreaValor	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.cclFuente	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.rrrFuente	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.OM_Proceso	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.Catastro_Registro.Interesado_Contacto	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_RelacionNecesariaUnidadesEspaciales	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_Agrupacion_Interesados	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.ueFuente	ch.ehi.ili2db.inheritance	newAndSubClass
Catastro_Registro_Nucleo_V2_2_1.COL_TerritorioAgricola_Terreno_Territorio_Agricola	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.COL_FuenteEspacial	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.puntoCl	ch.ehi.ili2db.inheritance	newAndSubClass
LADM_COL_V1_1.LADM_Nucleo.LA_RRR	ch.ehi.ili2db.inheritance	subClass
LADM_COL_V1_1.LADM_Nucleo.ExtUnidadEdificacionFisica	ch.ehi.ili2db.inheritance	newAndSubClass
\.


--
-- TOC entry 12436 (class 0 OID 336080)
-- Dependencies: 2121
-- Data for Name: terreno; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.terreno (t_id, t_ili_tid, area_registral, area_calculada, avaluo_terreno, dimension, etiqueta, relacion_superficie, su_espacio_de_nombres, su_local_id, nivel, uej2_la_unidadespacial, uej2_la_espaciojuridicoredservicios, uej2_la_espaciojuridicounidadedificacion, uej2_servidumbrepaso, uej2_terreno, uej2_construccion, uej2_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, punto_referencia, poligono_creado) FROM stdin;
\.


--
-- TOC entry 12437 (class 0 OID 336090)
-- Dependencies: 2122
-- Data for Name: topografofuente; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.topografofuente (t_id, t_ili_tid, sfuente, topografo_la_agrupacion_interesados, topografo_col_interesado) FROM stdin;
\.


--
-- TOC entry 12438 (class 0 OID 336094)
-- Dependencies: 2123
-- Data for Name: uebaunit; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.uebaunit (t_id, t_ili_tid, ue_la_unidadespacial, ue_la_espaciojuridicoredservicios, ue_la_espaciojuridicounidadedificacion, ue_servidumbrepaso, ue_terreno, ue_construccion, ue_unidadconstruccion, baunit_la_baunit, baunit_predio) FROM stdin;
\.


--
-- TOC entry 12439 (class 0 OID 336098)
-- Dependencies: 2124
-- Data for Name: uefuente; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.uefuente (t_id, t_ili_tid, ue_la_unidadespacial, ue_la_espaciojuridicoredservicios, ue_la_espaciojuridicounidadedificacion, ue_servidumbrepaso, ue_terreno, ue_construccion, ue_unidadconstruccion, pfuente) FROM stdin;
\.


--
-- TOC entry 12440 (class 0 OID 336102)
-- Dependencies: 2125
-- Data for Name: ueuegrupo; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.ueuegrupo (t_id, t_ili_tid, parte_la_unidadespacial, parte_la_espaciojuridicoredservicios, parte_la_espaciojuridicounidadedificacion, parte_servidumbrepaso, parte_terreno, parte_construccion, parte_unidadconstruccion, todo) FROM stdin;
\.


--
-- TOC entry 12441 (class 0 OID 336106)
-- Dependencies: 2126
-- Data for Name: unidadconstruccion; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.unidadconstruccion (t_id, t_ili_tid, avaluo_unidad_construccion, numero_pisos, area_construida, area_privada_construida, construccion, tipo, dimension, etiqueta, relacion_superficie, su_espacio_de_nombres, su_local_id, nivel, uej2_la_unidadespacial, uej2_la_espaciojuridicoredservicios, uej2_la_espaciojuridicounidadedificacion, uej2_servidumbrepaso, uej2_terreno, uej2_construccion, uej2_unidadconstruccion, comienzo_vida_util_version, fin_vida_util_version, punto_referencia, poligono_creado) FROM stdin;
\.


--
-- TOC entry 12442 (class 0 OID 336117)
-- Dependencies: 2127
-- Data for Name: unidadfuente; Type: TABLE DATA; Schema: interlis_ili2db3_ladm; Owner: postgres
--

COPY interlis_ili2db3_ladm.unidadfuente (t_id, t_ili_tid, ufuente, unidad_la_baunit, unidad_predio) FROM stdin;
\.


--
-- TOC entry 13030 (class 0 OID 0)
-- Dependencies: 1963
-- Name: t_ili2db_seq; Type: SEQUENCE SET; Schema: interlis_ili2db3_ladm; Owner: postgres
--

SELECT pg_catalog.setval('interlis_ili2db3_ladm.t_ili2db_seq', 1, false);


--
-- TOC entry 11064 (class 2606 OID 336124)
-- Name: baunitcomointeresado baunitcomointeresado_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.baunitcomointeresado
    ADD CONSTRAINT baunitcomointeresado_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11069 (class 2606 OID 336126)
-- Name: baunitfuente baunitfuente_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.baunitfuente
    ADD CONSTRAINT baunitfuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11074 (class 2606 OID 336128)
-- Name: cc_metodooperacion cc_metodooperacion_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.cc_metodooperacion
    ADD CONSTRAINT cc_metodooperacion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11079 (class 2606 OID 336130)
-- Name: cclfuente cclfuente_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.cclfuente
    ADD CONSTRAINT cclfuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11081 (class 2606 OID 336132)
-- Name: ci_codigotarea ci_codigotarea_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_codigotarea
    ADD CONSTRAINT ci_codigotarea_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11084 (class 2606 OID 336134)
-- Name: ci_contacto ci_contacto_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_contacto
    ADD CONSTRAINT ci_contacto_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11086 (class 2606 OID 336136)
-- Name: ci_forma_presentacion_codigo ci_forma_presentacion_codigo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_forma_presentacion_codigo
    ADD CONSTRAINT ci_forma_presentacion_codigo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11109 (class 2606 OID 336138)
-- Name: ci_parteresponsable ci_parteresponsable_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11121 (class 2606 OID 336140)
-- Name: clfuente clfuente_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.clfuente
    ADD CONSTRAINT clfuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11123 (class 2606 OID 336142)
-- Name: col_acuerdotipo col_acuerdotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_acuerdotipo
    ADD CONSTRAINT col_acuerdotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11125 (class 2606 OID 336144)
-- Name: col_afectacion col_afectacion_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_afectacion
    ADD CONSTRAINT col_afectacion_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11128 (class 2606 OID 336146)
-- Name: col_afectacion_terreno_afectacion col_afectacion_terreno_afectacion_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_afectacion_terreno_afectacion
    ADD CONSTRAINT col_afectacion_terreno_afectacion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11130 (class 2606 OID 336148)
-- Name: col_areatipo col_areatipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_areatipo
    ADD CONSTRAINT col_areatipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11136 (class 2606 OID 336150)
-- Name: col_areavalor col_areavalor_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_areavalor
    ADD CONSTRAINT col_areavalor_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11141 (class 2606 OID 336152)
-- Name: col_bosqueareasemi col_bosqueareasemi_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_bosqueareasemi
    ADD CONSTRAINT col_bosqueareasemi_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11143 (class 2606 OID 336154)
-- Name: col_bosqueareasemi_terreno_bosque_area_seminaturale col_bosqueareasemi_terreno_bosque_area_seminaturale_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_bosqueareasemi_terreno_bosque_area_seminaturale
    ADD CONSTRAINT col_bosqueareasemi_terreno_bosque_area_seminaturale_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11146 (class 2606 OID 336156)
-- Name: col_cuerpoagua col_cuerpoagua_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_cuerpoagua
    ADD CONSTRAINT col_cuerpoagua_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11149 (class 2606 OID 336158)
-- Name: col_cuerpoagua_terreno_evidencia_cuerpo_agua col_cuerpoagua_terreno_evidencia_cuerpo_agua_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_cuerpoagua_terreno_evidencia_cuerpo_agua
    ADD CONSTRAINT col_cuerpoagua_terreno_evidencia_cuerpo_agua_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11151 (class 2606 OID 336160)
-- Name: col_defpuntotipo col_defpuntotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_defpuntotipo
    ADD CONSTRAINT col_defpuntotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11155 (class 2606 OID 336162)
-- Name: col_derecho col_derecho_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_derecho
    ADD CONSTRAINT col_derecho_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11159 (class 2606 OID 336164)
-- Name: col_derechotipo col_derechotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_derechotipo
    ADD CONSTRAINT col_derechotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11161 (class 2606 OID 336166)
-- Name: col_descripcionpuntotipo col_descripcionpuntotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_descripcionpuntotipo
    ADD CONSTRAINT col_descripcionpuntotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11163 (class 2606 OID 336168)
-- Name: col_estadodisponibilidadtipo col_estadodisponibilidadtipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_estadodisponibilidadtipo
    ADD CONSTRAINT col_estadodisponibilidadtipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11165 (class 2606 OID 336170)
-- Name: col_estructuratipo col_estructuratipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_estructuratipo
    ADD CONSTRAINT col_estructuratipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11167 (class 2606 OID 336172)
-- Name: col_explotaciontipo col_explotaciontipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_explotaciontipo
    ADD CONSTRAINT col_explotaciontipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11169 (class 2606 OID 336174)
-- Name: col_explotaciontipo_terreno_explotacion col_explotaciontipo_terreno_explotacion_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_explotaciontipo_terreno_explotacion
    ADD CONSTRAINT col_explotaciontipo_terreno_explotacion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11172 (class 2606 OID 336176)
-- Name: col_fuenteadministrativa col_fuenteadministrativa_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_fuenteadministrativa
    ADD CONSTRAINT col_fuenteadministrativa_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11174 (class 2606 OID 336178)
-- Name: col_fuenteadministrativatipo col_fuenteadministrativatipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_fuenteadministrativatipo
    ADD CONSTRAINT col_fuenteadministrativatipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11176 (class 2606 OID 336180)
-- Name: col_fuenteespacial col_fuenteespacial_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_fuenteespacial
    ADD CONSTRAINT col_fuenteespacial_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11178 (class 2606 OID 336182)
-- Name: col_fuenteespacialtipo col_fuenteespacialtipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_fuenteespacialtipo
    ADD CONSTRAINT col_fuenteespacialtipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11180 (class 2606 OID 336184)
-- Name: col_funcioninteresadotipo col_funcioninteresadotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_funcioninteresadotipo
    ADD CONSTRAINT col_funcioninteresadotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11182 (class 2606 OID 336186)
-- Name: col_generotipo col_generotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_generotipo
    ADD CONSTRAINT col_generotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11184 (class 2606 OID 336188)
-- Name: col_grupointeresadotipo col_grupointeresadotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_grupointeresadotipo
    ADD CONSTRAINT col_grupointeresadotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11188 (class 2606 OID 336190)
-- Name: col_hipoteca col_hipoteca_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_hipoteca
    ADD CONSTRAINT col_hipoteca_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11192 (class 2606 OID 336192)
-- Name: col_hipotecatipo col_hipotecatipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_hipotecatipo
    ADD CONSTRAINT col_hipotecatipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11194 (class 2606 OID 336194)
-- Name: col_instituciontipo col_instituciontipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_instituciontipo
    ADD CONSTRAINT col_instituciontipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11196 (class 2606 OID 336196)
-- Name: col_interesado col_interesado_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_interesado
    ADD CONSTRAINT col_interesado_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11198 (class 2606 OID 336198)
-- Name: col_interesadodocumentotipo col_interesadodocumentotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_interesadodocumentotipo
    ADD CONSTRAINT col_interesadodocumentotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11200 (class 2606 OID 336200)
-- Name: col_interesadojuridicotipo col_interesadojuridicotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_interesadojuridicotipo
    ADD CONSTRAINT col_interesadojuridicotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11202 (class 2606 OID 336202)
-- Name: col_interpolaciontipo col_interpolaciontipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_interpolaciontipo
    ADD CONSTRAINT col_interpolaciontipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11204 (class 2606 OID 336204)
-- Name: col_levelcontenttipo col_levelcontenttipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_levelcontenttipo
    ADD CONSTRAINT col_levelcontenttipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11206 (class 2606 OID 336206)
-- Name: col_monumentaciontipo col_monumentaciontipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_monumentaciontipo
    ADD CONSTRAINT col_monumentaciontipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11208 (class 2606 OID 336208)
-- Name: col_prediotipo col_prediotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_prediotipo
    ADD CONSTRAINT col_prediotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11210 (class 2606 OID 336210)
-- Name: col_publicidadtipo col_publicidadtipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_publicidadtipo
    ADD CONSTRAINT col_publicidadtipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11212 (class 2606 OID 336212)
-- Name: col_puntocontroltipo col_puntocontroltipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_puntocontroltipo
    ADD CONSTRAINT col_puntocontroltipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11214 (class 2606 OID 336214)
-- Name: col_puntolevtipo col_puntolevtipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_puntolevtipo
    ADD CONSTRAINT col_puntolevtipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11216 (class 2606 OID 336216)
-- Name: col_redserviciostipo col_redserviciostipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_redserviciostipo
    ADD CONSTRAINT col_redserviciostipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11220 (class 2606 OID 336218)
-- Name: col_responsabilidad col_responsabilidad_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_responsabilidad
    ADD CONSTRAINT col_responsabilidad_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11224 (class 2606 OID 336220)
-- Name: col_responsabilidadtipo col_responsabilidadtipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_responsabilidadtipo
    ADD CONSTRAINT col_responsabilidadtipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11228 (class 2606 OID 336222)
-- Name: col_restriccion col_restriccion_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_restriccion
    ADD CONSTRAINT col_restriccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11232 (class 2606 OID 336224)
-- Name: col_restricciontipo col_restricciontipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_restricciontipo
    ADD CONSTRAINT col_restricciontipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11234 (class 2606 OID 336226)
-- Name: col_servidumbretipo col_servidumbretipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_servidumbretipo
    ADD CONSTRAINT col_servidumbretipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11236 (class 2606 OID 336228)
-- Name: col_servidumbretipo_terreno_servidumbre col_servidumbretipo_terreno_servidumbre_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_servidumbretipo_terreno_servidumbre
    ADD CONSTRAINT col_servidumbretipo_terreno_servidumbre_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11239 (class 2606 OID 336230)
-- Name: col_territorioagricola col_territorioagricola_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_territorioagricola
    ADD CONSTRAINT col_territorioagricola_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11241 (class 2606 OID 336232)
-- Name: col_territorioagricola_terreno_territorio_agricola col_territorioagricola_terreno_territorio_agricola_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_territorioagricola_terreno_territorio_agricola
    ADD CONSTRAINT col_territorioagricola_terreno_territorio_agricola_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11244 (class 2606 OID 336234)
-- Name: col_tipoconstrucciontipo col_tipoconstrucciontipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_tipoconstrucciontipo
    ADD CONSTRAINT col_tipoconstrucciontipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11246 (class 2606 OID 336236)
-- Name: col_unidadedificaciontipo col_unidadedificaciontipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_unidadedificaciontipo
    ADD CONSTRAINT col_unidadedificaciontipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11248 (class 2606 OID 336238)
-- Name: col_viatipo col_viatipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_viatipo
    ADD CONSTRAINT col_viatipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11250 (class 2606 OID 336240)
-- Name: col_zonatipo col_zonatipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_zonatipo
    ADD CONSTRAINT col_zonatipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11253 (class 2606 OID 336242)
-- Name: construccion construccion_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.construccion
    ADD CONSTRAINT construccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11264 (class 2606 OID 336244)
-- Name: dq_absoluteexternalpositionalaccuracy dq_absoluteexternalpositionalaccuracy_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_absoluteexternalpositionalaccuracy
    ADD CONSTRAINT dq_absoluteexternalpositionalaccuracy_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11288 (class 2606 OID 336246)
-- Name: dq_element dq_element_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11298 (class 2606 OID 336248)
-- Name: dq_metodo_evaluacion_codigo_tipo dq_metodo_evaluacion_codigo_tipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_metodo_evaluacion_codigo_tipo
    ADD CONSTRAINT dq_metodo_evaluacion_codigo_tipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11301 (class 2606 OID 336250)
-- Name: dq_positionalaccuracy dq_positionalaccuracy_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_positionalaccuracy
    ADD CONSTRAINT dq_positionalaccuracy_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11308 (class 2606 OID 336252)
-- Name: extarchivo extarchivo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extarchivo
    ADD CONSTRAINT extarchivo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11317 (class 2606 OID 336254)
-- Name: extdireccion extdireccion_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extdireccion
    ADD CONSTRAINT extdireccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11325 (class 2606 OID 336256)
-- Name: extinteresado extinteresado_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extinteresado
    ADD CONSTRAINT extinteresado_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11328 (class 2606 OID 336258)
-- Name: extredserviciosfisica extredserviciosfisica_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extredserviciosfisica
    ADD CONSTRAINT extredserviciosfisica_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11332 (class 2606 OID 336260)
-- Name: extunidadedificacionfisica extunidadedificacionfisica_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extunidadedificacionfisica
    ADD CONSTRAINT extunidadedificacionfisica_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11340 (class 2606 OID 336262)
-- Name: fraccion fraccion_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.fraccion
    ADD CONSTRAINT fraccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11343 (class 2606 OID 336264)
-- Name: gm_multisurface2d gm_multisurface2d_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.gm_multisurface2d
    ADD CONSTRAINT gm_multisurface2d_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11345 (class 2606 OID 336266)
-- Name: gm_multisurface3d gm_multisurface3d_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.gm_multisurface3d
    ADD CONSTRAINT gm_multisurface3d_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11349 (class 2606 OID 336268)
-- Name: gm_surface2dlistvalue gm_surface2dlistvalue_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.gm_surface2dlistvalue
    ADD CONSTRAINT gm_surface2dlistvalue_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11353 (class 2606 OID 336270)
-- Name: gm_surface3dlistvalue gm_surface3dlistvalue_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.gm_surface3dlistvalue
    ADD CONSTRAINT gm_surface3dlistvalue_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11357 (class 2606 OID 336272)
-- Name: hipotecaderecho hipotecaderecho_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.hipotecaderecho
    ADD CONSTRAINT hipotecaderecho_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11362 (class 2606 OID 336274)
-- Name: imagen imagen_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.imagen
    ADD CONSTRAINT imagen_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11365 (class 2606 OID 336276)
-- Name: interesado_contacto interesado_contacto_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.interesado_contacto
    ADD CONSTRAINT interesado_contacto_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11367 (class 2606 OID 336278)
-- Name: iso19125_tipo iso19125_tipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.iso19125_tipo
    ADD CONSTRAINT iso19125_tipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11369 (class 2606 OID 336280)
-- Name: la_agrupacion_interesados la_agrupacion_interesados_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_agrupacion_interesados
    ADD CONSTRAINT la_agrupacion_interesados_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11371 (class 2606 OID 336282)
-- Name: la_agrupacion_interesados_tipo la_agrupacion_interesados_tipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_agrupacion_interesados_tipo
    ADD CONSTRAINT la_agrupacion_interesados_tipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11373 (class 2606 OID 336284)
-- Name: la_agrupacionunidadesespaciales la_agrupacionunidadesespaciales_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_agrupacionunidadesespaciales
    ADD CONSTRAINT la_agrupacionunidadesespaciales_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11377 (class 2606 OID 336286)
-- Name: la_baunit la_baunit_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_baunit
    ADD CONSTRAINT la_baunit_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11379 (class 2606 OID 336288)
-- Name: la_baunittipo la_baunittipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_baunittipo
    ADD CONSTRAINT la_baunittipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11382 (class 2606 OID 336290)
-- Name: la_cadenacaraslimite la_cadenacaraslimite_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_cadenacaraslimite
    ADD CONSTRAINT la_cadenacaraslimite_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11385 (class 2606 OID 336292)
-- Name: la_caraslindero la_caraslindero_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_caraslindero
    ADD CONSTRAINT la_caraslindero_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11387 (class 2606 OID 336294)
-- Name: la_contenidoniveltipo la_contenidoniveltipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_contenidoniveltipo
    ADD CONSTRAINT la_contenidoniveltipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11389 (class 2606 OID 336296)
-- Name: la_derechotipo la_derechotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_derechotipo
    ADD CONSTRAINT la_derechotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11391 (class 2606 OID 336298)
-- Name: la_dimensiontipo la_dimensiontipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_dimensiontipo
    ADD CONSTRAINT la_dimensiontipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11393 (class 2606 OID 336300)
-- Name: la_espaciojuridicoredservicios la_espaciojuridicoredservicios_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicoredservicios
    ADD CONSTRAINT la_espaciojuridicoredservicios_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11415 (class 2606 OID 336302)
-- Name: la_espaciojuridicounidadedificacion la_espaciojuridicounidadedificacion_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion
    ADD CONSTRAINT la_espaciojuridicounidadedificacion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11417 (class 2606 OID 336304)
-- Name: la_estadodisponibilidadtipo la_estadodisponibilidadtipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_estadodisponibilidadtipo
    ADD CONSTRAINT la_estadodisponibilidadtipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11419 (class 2606 OID 336306)
-- Name: la_estadoredserviciostipo la_estadoredserviciostipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_estadoredserviciostipo
    ADD CONSTRAINT la_estadoredserviciostipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11421 (class 2606 OID 336308)
-- Name: la_estructuratipo la_estructuratipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_estructuratipo
    ADD CONSTRAINT la_estructuratipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11423 (class 2606 OID 336310)
-- Name: la_fuenteadministrativatipo la_fuenteadministrativatipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_fuenteadministrativatipo
    ADD CONSTRAINT la_fuenteadministrativatipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11425 (class 2606 OID 336312)
-- Name: la_fuenteespacialtipo la_fuenteespacialtipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_fuenteespacialtipo
    ADD CONSTRAINT la_fuenteespacialtipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11427 (class 2606 OID 336314)
-- Name: la_hipotecatipo la_hipotecatipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_hipotecatipo
    ADD CONSTRAINT la_hipotecatipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11429 (class 2606 OID 336316)
-- Name: la_interesadotipo la_interesadotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_interesadotipo
    ADD CONSTRAINT la_interesadotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11431 (class 2606 OID 336318)
-- Name: la_interpolaciontipo la_interpolaciontipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_interpolaciontipo
    ADD CONSTRAINT la_interpolaciontipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11433 (class 2606 OID 336322)
-- Name: la_monumentaciontipo la_monumentaciontipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_monumentaciontipo
    ADD CONSTRAINT la_monumentaciontipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11435 (class 2606 OID 336324)
-- Name: la_nivel la_nivel_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_nivel
    ADD CONSTRAINT la_nivel_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11438 (class 2606 OID 336326)
-- Name: la_punto la_punto_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_punto
    ADD CONSTRAINT la_punto_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11447 (class 2606 OID 336328)
-- Name: la_puntotipo la_puntotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_puntotipo
    ADD CONSTRAINT la_puntotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11449 (class 2606 OID 336330)
-- Name: la_redserviciostipo la_redserviciostipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_redserviciostipo
    ADD CONSTRAINT la_redserviciostipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11451 (class 2606 OID 336332)
-- Name: la_registrotipo la_registrotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_registrotipo
    ADD CONSTRAINT la_registrotipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11453 (class 2606 OID 336334)
-- Name: la_relacionnecesariabaunits la_relacionnecesariabaunits_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_relacionnecesariabaunits
    ADD CONSTRAINT la_relacionnecesariabaunits_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11455 (class 2606 OID 336336)
-- Name: la_relacionnecesariaunidadesespaciales la_relacionnecesariaunidadesespaciales_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_relacionnecesariaunidadesespaciales
    ADD CONSTRAINT la_relacionnecesariaunidadesespaciales_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11457 (class 2606 OID 336338)
-- Name: la_relacionsuperficietipo la_relacionsuperficietipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_relacionsuperficietipo
    ADD CONSTRAINT la_relacionsuperficietipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11459 (class 2606 OID 336340)
-- Name: la_responsabilidadtipo la_responsabilidadtipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_responsabilidadtipo
    ADD CONSTRAINT la_responsabilidadtipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11461 (class 2606 OID 336342)
-- Name: la_restricciontipo la_restricciontipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_restricciontipo
    ADD CONSTRAINT la_restricciontipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11465 (class 2606 OID 336344)
-- Name: la_tareainteresadotipo la_tareainteresadotipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_tareainteresadotipo
    ADD CONSTRAINT la_tareainteresadotipo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11467 (class 2606 OID 336346)
-- Name: la_tareainteresadotipo_tipo la_tareainteresadotipo_tipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_tareainteresadotipo_tipo
    ADD CONSTRAINT la_tareainteresadotipo_tipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11471 (class 2606 OID 336348)
-- Name: la_transformacion la_transformacion_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_transformacion
    ADD CONSTRAINT la_transformacion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11476 (class 2606 OID 336350)
-- Name: la_unidadedificaciontipo la_unidadedificaciontipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_unidadedificaciontipo
    ADD CONSTRAINT la_unidadedificaciontipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11479 (class 2606 OID 336352)
-- Name: la_unidadespacial la_unidadespacial_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_unidadespacial
    ADD CONSTRAINT la_unidadespacial_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11490 (class 2606 OID 336354)
-- Name: la_volumentipo la_volumentipo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_volumentipo
    ADD CONSTRAINT la_volumentipo_pkey PRIMARY KEY (itfcode);


--
-- TOC entry 11496 (class 2606 OID 336356)
-- Name: la_volumenvalor la_volumenvalor_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_volumenvalor
    ADD CONSTRAINT la_volumenvalor_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11502 (class 2606 OID 336358)
-- Name: li_lineaje li_lineaje_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.li_lineaje
    ADD CONSTRAINT li_lineaje_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11508 (class 2606 OID 336360)
-- Name: lindero lindero_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.lindero
    ADD CONSTRAINT lindero_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11511 (class 2606 OID 336362)
-- Name: mas mas_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.mas
    ADD CONSTRAINT mas_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11522 (class 2606 OID 336364)
-- Name: masccl masccl_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.masccl
    ADD CONSTRAINT masccl_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11540 (class 2606 OID 336366)
-- Name: menos menos_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menos
    ADD CONSTRAINT menos_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11543 (class 2606 OID 336368)
-- Name: menosf menosf_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menosf
    ADD CONSTRAINT menosf_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11555 (class 2606 OID 336370)
-- Name: miembros miembros_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.miembros
    ADD CONSTRAINT miembros_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11560 (class 2606 OID 336372)
-- Name: oid oid_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.oid
    ADD CONSTRAINT oid_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11563 (class 2606 OID 336374)
-- Name: om_observacion om_observacion_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.om_observacion
    ADD CONSTRAINT om_observacion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11566 (class 2606 OID 336376)
-- Name: om_proceso om_proceso_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.om_proceso
    ADD CONSTRAINT om_proceso_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11572 (class 2606 OID 336378)
-- Name: predio_copropiedad predio_copropiedad_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.predio_copropiedad
    ADD CONSTRAINT predio_copropiedad_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11570 (class 2606 OID 336380)
-- Name: predio predio_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.predio
    ADD CONSTRAINT predio_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11578 (class 2606 OID 336382)
-- Name: publicidad publicidad_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.publicidad
    ADD CONSTRAINT publicidad_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11581 (class 2606 OID 336384)
-- Name: publicidadfuente publicidadfuente_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.publicidadfuente
    ADD CONSTRAINT publicidadfuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11586 (class 2606 OID 336386)
-- Name: puntoccl puntoccl_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntoccl
    ADD CONSTRAINT puntoccl_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11593 (class 2606 OID 336388)
-- Name: puntocl puntocl_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocl
    ADD CONSTRAINT puntocl_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11600 (class 2606 OID 336390)
-- Name: puntocontrol puntocontrol_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocontrol
    ADD CONSTRAINT puntocontrol_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11610 (class 2606 OID 336392)
-- Name: puntofuente puntofuente_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntofuente
    ADD CONSTRAINT puntofuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11617 (class 2606 OID 336394)
-- Name: puntolevantamiento puntolevantamiento_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolevantamiento
    ADD CONSTRAINT puntolevantamiento_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11627 (class 2606 OID 336396)
-- Name: puntolindero puntolindero_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolindero
    ADD CONSTRAINT puntolindero_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11636 (class 2606 OID 336398)
-- Name: relacionbaunit relacionbaunit_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionbaunit
    ADD CONSTRAINT relacionbaunit_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11642 (class 2606 OID 336400)
-- Name: relacionfuente relacionfuente_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionfuente
    ADD CONSTRAINT relacionfuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11646 (class 2606 OID 336402)
-- Name: relacionfuenteuespacial relacionfuenteuespacial_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionfuenteuespacial
    ADD CONSTRAINT relacionfuenteuespacial_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11650 (class 2606 OID 336404)
-- Name: relacionue relacionue_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11669 (class 2606 OID 336406)
-- Name: responsablefuente responsablefuente_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.responsablefuente
    ADD CONSTRAINT responsablefuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11671 (class 2606 OID 336408)
-- Name: rrrfuente rrrfuente_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.rrrfuente
    ADD CONSTRAINT rrrfuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11679 (class 2606 OID 336410)
-- Name: servidumbrepaso servidumbrepaso_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.servidumbrepaso
    ADD CONSTRAINT servidumbrepaso_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11690 (class 2606 OID 336412)
-- Name: t_ili2db_attrname t_ili2db_attrname_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.t_ili2db_attrname
    ADD CONSTRAINT t_ili2db_attrname_pkey PRIMARY KEY (sqlname, owner);


--
-- TOC entry 11694 (class 2606 OID 336414)
-- Name: t_ili2db_basket t_ili2db_basket_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.t_ili2db_basket
    ADD CONSTRAINT t_ili2db_basket_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11696 (class 2606 OID 336416)
-- Name: t_ili2db_classname t_ili2db_classname_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.t_ili2db_classname
    ADD CONSTRAINT t_ili2db_classname_pkey PRIMARY KEY (iliname);


--
-- TOC entry 11699 (class 2606 OID 336418)
-- Name: t_ili2db_dataset t_ili2db_dataset_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.t_ili2db_dataset
    ADD CONSTRAINT t_ili2db_dataset_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11706 (class 2606 OID 336420)
-- Name: t_ili2db_import_basket t_ili2db_import_basket_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.t_ili2db_import_basket
    ADD CONSTRAINT t_ili2db_import_basket_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11708 (class 2606 OID 336422)
-- Name: t_ili2db_import_object t_ili2db_import_object_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.t_ili2db_import_object
    ADD CONSTRAINT t_ili2db_import_object_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11702 (class 2606 OID 336424)
-- Name: t_ili2db_import t_ili2db_import_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.t_ili2db_import
    ADD CONSTRAINT t_ili2db_import_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11710 (class 2606 OID 336426)
-- Name: t_ili2db_inheritance t_ili2db_inheritance_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.t_ili2db_inheritance
    ADD CONSTRAINT t_ili2db_inheritance_pkey PRIMARY KEY (thisclass);


--
-- TOC entry 11713 (class 2606 OID 336428)
-- Name: t_ili2db_model t_ili2db_model_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.t_ili2db_model
    ADD CONSTRAINT t_ili2db_model_pkey PRIMARY KEY (iliversion, modelname);


--
-- TOC entry 11715 (class 2606 OID 336430)
-- Name: t_ili2db_settings t_ili2db_settings_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.t_ili2db_settings
    ADD CONSTRAINT t_ili2db_settings_pkey PRIMARY KEY (tag);


--
-- TOC entry 11718 (class 2606 OID 336432)
-- Name: terreno terreno_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.terreno
    ADD CONSTRAINT terreno_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11729 (class 2606 OID 336434)
-- Name: topografofuente topografofuente_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.topografofuente
    ADD CONSTRAINT topografofuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11736 (class 2606 OID 336436)
-- Name: uebaunit uebaunit_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uebaunit
    ADD CONSTRAINT uebaunit_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11746 (class 2606 OID 336438)
-- Name: uefuente uefuente_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uefuente
    ADD CONSTRAINT uefuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11762 (class 2606 OID 336440)
-- Name: ueuegrupo ueuegrupo_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ueuegrupo
    ADD CONSTRAINT ueuegrupo_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11767 (class 2606 OID 336442)
-- Name: unidadconstruccion unidadconstruccion_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadconstruccion
    ADD CONSTRAINT unidadconstruccion_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11778 (class 2606 OID 336444)
-- Name: unidadfuente unidadfuente_pkey; Type: CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadfuente
    ADD CONSTRAINT unidadfuente_pkey PRIMARY KEY (t_id);


--
-- TOC entry 11061 (class 1259 OID 336445)
-- Name: baunitcomointeresado_interesado_col_interesado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX baunitcomointeresado_interesado_col_interesado_idx ON interlis_ili2db3_ladm.baunitcomointeresado USING btree (interesado_col_interesado);


--
-- TOC entry 11062 (class 1259 OID 336446)
-- Name: baunitcomointeresado_interesado_l_grpcn_ntrsdos_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX baunitcomointeresado_interesado_l_grpcn_ntrsdos_idx ON interlis_ili2db3_ladm.baunitcomointeresado USING btree (interesado_la_agrupacion_interesados);


--
-- TOC entry 11065 (class 1259 OID 336447)
-- Name: baunitcomointeresado_unidad_la_baunit_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX baunitcomointeresado_unidad_la_baunit_idx ON interlis_ili2db3_ladm.baunitcomointeresado USING btree (unidad_la_baunit);


--
-- TOC entry 11066 (class 1259 OID 336448)
-- Name: baunitcomointeresado_unidad_predio_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX baunitcomointeresado_unidad_predio_idx ON interlis_ili2db3_ladm.baunitcomointeresado USING btree (unidad_predio);


--
-- TOC entry 11067 (class 1259 OID 336449)
-- Name: baunitfuente_bfuente_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX baunitfuente_bfuente_idx ON interlis_ili2db3_ladm.baunitfuente USING btree (bfuente);


--
-- TOC entry 11070 (class 1259 OID 336450)
-- Name: baunitfuente_unidad_la_baunit_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX baunitfuente_unidad_la_baunit_idx ON interlis_ili2db3_ladm.baunitfuente USING btree (unidad_la_baunit);


--
-- TOC entry 11071 (class 1259 OID 336451)
-- Name: baunitfuente_unidad_predio_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX baunitfuente_unidad_predio_idx ON interlis_ili2db3_ladm.baunitfuente USING btree (unidad_predio);


--
-- TOC entry 11072 (class 1259 OID 336452)
-- Name: cc_metodooperacion_la_transformcn_trnsfrmcion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX cc_metodooperacion_la_transformcn_trnsfrmcion_idx ON interlis_ili2db3_ladm.cc_metodooperacion USING btree (la_transformacion_transformacion);


--
-- TOC entry 11075 (class 1259 OID 336453)
-- Name: cclfuente_ccl_la_cadenacaraslimite_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX cclfuente_ccl_la_cadenacaraslimite_idx ON interlis_ili2db3_ladm.cclfuente USING btree (ccl_la_cadenacaraslimite);


--
-- TOC entry 11076 (class 1259 OID 336454)
-- Name: cclfuente_ccl_lindero_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX cclfuente_ccl_lindero_idx ON interlis_ili2db3_ladm.cclfuente USING btree (ccl_lindero);


--
-- TOC entry 11077 (class 1259 OID 336455)
-- Name: cclfuente_lfuente_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX cclfuente_lfuente_idx ON interlis_ili2db3_ladm.cclfuente USING btree (lfuente);


--
-- TOC entry 11082 (class 1259 OID 336456)
-- Name: ci_contacto_ci_prtrspnsblnfrmcn_cntcto_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_contacto_ci_prtrspnsblnfrmcn_cntcto_idx ON interlis_ili2db3_ladm.ci_contacto USING btree (ci_parteresponsable_informacion_contacto);


--
-- TOC entry 11087 (class 1259 OID 336457)
-- Name: ci_parteresponsable_col_derecho_procedencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_col_derecho_procedencia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (col_derecho_procedencia);


--
-- TOC entry 11088 (class 1259 OID 336458)
-- Name: ci_parteresponsable_col_fuentdmnstrtv_prcdncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_col_fuentdmnstrtv_prcdncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (col_fuenteadminstrtiva_procedencia);


--
-- TOC entry 11089 (class 1259 OID 336459)
-- Name: ci_parteresponsable_col_fuenteespacil_prcdncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_col_fuenteespacil_prcdncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (col_fuenteespacial_procedencia);


--
-- TOC entry 11090 (class 1259 OID 336460)
-- Name: ci_parteresponsable_col_hipoteca_procedencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_col_hipoteca_procedencia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (col_hipoteca_procedencia);


--
-- TOC entry 11091 (class 1259 OID 336461)
-- Name: ci_parteresponsable_col_interesado_procedencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_col_interesado_procedencia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (col_interesado_procedencia);


--
-- TOC entry 11092 (class 1259 OID 336462)
-- Name: ci_parteresponsable_col_responsabildd_prcdncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_col_responsabildd_prcdncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (col_responsabilidad_procedencia);


--
-- TOC entry 11093 (class 1259 OID 336463)
-- Name: ci_parteresponsable_col_restriccion_procedncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_col_restriccion_procedncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (col_restriccion_procedencia);


--
-- TOC entry 11094 (class 1259 OID 336464)
-- Name: ci_parteresponsable_construccion_procedencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_construccion_procedencia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (construccion_procedencia);


--
-- TOC entry 11095 (class 1259 OID 336465)
-- Name: ci_parteresponsable_la_agrupcn_ntrsds_prcdncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_la_agrupcn_ntrsds_prcdncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (la_agrupacion_intrsdos_procedencia);


--
-- TOC entry 11096 (class 1259 OID 336466)
-- Name: ci_parteresponsable_la_baunit_procedencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_la_baunit_procedencia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (la_baunit_procedencia);


--
-- TOC entry 11097 (class 1259 OID 336467)
-- Name: ci_parteresponsable_la_cadenacaraslmt_prcdncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_la_cadenacaraslmt_prcdncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (la_cadenacaraslimite_procedencia);


--
-- TOC entry 11098 (class 1259 OID 336468)
-- Name: ci_parteresponsable_la_caraslindero_procedncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_la_caraslindero_procedncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (la_caraslindero_procedencia);


--
-- TOC entry 11099 (class 1259 OID 336469)
-- Name: ci_parteresponsable_la_grpcnnddsspcls_prcdncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_la_grpcnnddsspcls_prcdncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (la_agrupacinnddsspcles_procedencia);


--
-- TOC entry 11100 (class 1259 OID 336470)
-- Name: ci_parteresponsable_la_nivel_procedencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_la_nivel_procedencia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (la_nivel_procedencia);


--
-- TOC entry 11101 (class 1259 OID 336471)
-- Name: ci_parteresponsable_la_punto_procedencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_la_punto_procedencia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (la_punto_procedencia);


--
-- TOC entry 11102 (class 1259 OID 336472)
-- Name: ci_parteresponsable_la_relacnncsrbnts_prcdncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_la_relacnncsrbnts_prcdncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (la_relacionnecesrbnits_procedencia);


--
-- TOC entry 11103 (class 1259 OID 336473)
-- Name: ci_parteresponsable_la_rlcnncsrndpcls_prcdncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_la_rlcnncsrndpcls_prcdncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (la_relcnncsrnddsspcles_procedencia);


--
-- TOC entry 11104 (class 1259 OID 336474)
-- Name: ci_parteresponsable_la_spcjrdcnddfccn_prcdncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_la_spcjrdcnddfccn_prcdncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (la_espacjrdcndddfccion_procedencia);


--
-- TOC entry 11105 (class 1259 OID 336475)
-- Name: ci_parteresponsable_la_spcjrdcrdsrvcs_prcdncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_la_spcjrdcrdsrvcs_prcdncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (la_espacijrdcrdsrvcios_procedencia);


--
-- TOC entry 11106 (class 1259 OID 336476)
-- Name: ci_parteresponsable_la_unidadespacial_prcdncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_la_unidadespacial_prcdncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (la_unidadespacial_procedencia);


--
-- TOC entry 11107 (class 1259 OID 336477)
-- Name: ci_parteresponsable_lindero_procedencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_lindero_procedencia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (lindero_procedencia);


--
-- TOC entry 11110 (class 1259 OID 336478)
-- Name: ci_parteresponsable_predio_procedencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_predio_procedencia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (predio_procedencia);


--
-- TOC entry 11111 (class 1259 OID 336479)
-- Name: ci_parteresponsable_publicidad_procedencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_publicidad_procedencia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (publicidad_procedencia);


--
-- TOC entry 11112 (class 1259 OID 336480)
-- Name: ci_parteresponsable_puntocontrol_procedencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_puntocontrol_procedencia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (puntocontrol_procedencia);


--
-- TOC entry 11113 (class 1259 OID 336481)
-- Name: ci_parteresponsable_puntolevantamient_prcdncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_puntolevantamient_prcdncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (puntolevantamiento_procedencia);


--
-- TOC entry 11114 (class 1259 OID 336482)
-- Name: ci_parteresponsable_puntolindero_procedencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_puntolindero_procedencia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (puntolindero_procedencia);


--
-- TOC entry 11115 (class 1259 OID 336483)
-- Name: ci_parteresponsable_servidumbrepaso_procedncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_servidumbrepaso_procedncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (servidumbrepaso_procedencia);


--
-- TOC entry 11116 (class 1259 OID 336484)
-- Name: ci_parteresponsable_terreno_procedencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_terreno_procedencia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (terreno_procedencia);


--
-- TOC entry 11117 (class 1259 OID 336485)
-- Name: ci_parteresponsable_unidadconstruccin_prcdncia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ci_parteresponsable_unidadconstruccin_prcdncia_idx ON interlis_ili2db3_ladm.ci_parteresponsable USING btree (unidadconstruccion_procedencia);


--
-- TOC entry 11118 (class 1259 OID 336486)
-- Name: clfuente_cfuente_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX clfuente_cfuente_idx ON interlis_ili2db3_ladm.clfuente USING btree (cfuente);


--
-- TOC entry 11119 (class 1259 OID 336487)
-- Name: clfuente_cl_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX clfuente_cl_idx ON interlis_ili2db3_ladm.clfuente USING btree (cl);


--
-- TOC entry 11126 (class 1259 OID 336488)
-- Name: col_afectacin_trrn_fctcion_terreno_afectacion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_afectacin_trrn_fctcion_terreno_afectacion_idx ON interlis_ili2db3_ladm.col_afectacion_terreno_afectacion USING btree (terreno_afectacion);


--
-- TOC entry 11131 (class 1259 OID 336489)
-- Name: col_areavalor_construccion_area_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_areavalor_construccion_area_idx ON interlis_ili2db3_ladm.col_areavalor USING btree (construccion_area);


--
-- TOC entry 11132 (class 1259 OID 336490)
-- Name: col_areavalor_la_espacijrdcrdsrvcios_rea_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_areavalor_la_espacijrdcrdsrvcios_rea_idx ON interlis_ili2db3_ladm.col_areavalor USING btree (la_espacijrdcrdsrvcios_area);


--
-- TOC entry 11133 (class 1259 OID 336491)
-- Name: col_areavalor_la_espacjrdcndddfccion_rea_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_areavalor_la_espacjrdcndddfccion_rea_idx ON interlis_ili2db3_ladm.col_areavalor USING btree (la_espacjrdcndddfccion_area);


--
-- TOC entry 11134 (class 1259 OID 336492)
-- Name: col_areavalor_la_unidadespacial_area_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_areavalor_la_unidadespacial_area_idx ON interlis_ili2db3_ladm.col_areavalor USING btree (la_unidadespacial_area);


--
-- TOC entry 11137 (class 1259 OID 336493)
-- Name: col_areavalor_servidumbrepaso_area_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_areavalor_servidumbrepaso_area_idx ON interlis_ili2db3_ladm.col_areavalor USING btree (servidumbrepaso_area);


--
-- TOC entry 11138 (class 1259 OID 336494)
-- Name: col_areavalor_terreno_area_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_areavalor_terreno_area_idx ON interlis_ili2db3_ladm.col_areavalor USING btree (terreno_area);


--
-- TOC entry 11139 (class 1259 OID 336495)
-- Name: col_areavalor_unidadconstruccion_area_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_areavalor_unidadconstruccion_area_idx ON interlis_ili2db3_ladm.col_areavalor USING btree (unidadconstruccion_area);


--
-- TOC entry 11144 (class 1259 OID 336496)
-- Name: col_bsqrsm_trsq_r_smntrale_terreno_bosque_ar_smntrale_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_bsqrsm_trsq_r_smntrale_terreno_bosque_ar_smntrale_idx ON interlis_ili2db3_ladm.col_bosqueareasemi_terreno_bosque_area_seminaturale USING btree (terreno_bosque_area_seminaturale);


--
-- TOC entry 11147 (class 1259 OID 336497)
-- Name: col_crpg_trrn_vdnc_crp_gua_terreno_evidencia_curp_gua_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_crpg_trrn_vdnc_crp_gua_terreno_evidencia_curp_gua_idx ON interlis_ili2db3_ladm.col_cuerpoagua_terreno_evidencia_cuerpo_agua USING btree (terreno_evidencia_cuerpo_agua);


--
-- TOC entry 11152 (class 1259 OID 336498)
-- Name: col_derecho_interesado_col_interesado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_derecho_interesado_col_interesado_idx ON interlis_ili2db3_ladm.col_derecho USING btree (interesado_col_interesado);


--
-- TOC entry 11153 (class 1259 OID 336499)
-- Name: col_derecho_interesado_l_grpcn_ntrsdos_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_derecho_interesado_l_grpcn_ntrsdos_idx ON interlis_ili2db3_ladm.col_derecho USING btree (interesado_la_agrupacion_interesados);


--
-- TOC entry 11156 (class 1259 OID 336500)
-- Name: col_derecho_unidad_la_baunit_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_derecho_unidad_la_baunit_idx ON interlis_ili2db3_ladm.col_derecho USING btree (unidad_la_baunit);


--
-- TOC entry 11157 (class 1259 OID 336501)
-- Name: col_derecho_unidad_predio_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_derecho_unidad_predio_idx ON interlis_ili2db3_ladm.col_derecho USING btree (unidad_predio);


--
-- TOC entry 11185 (class 1259 OID 336502)
-- Name: col_hipoteca_interesado_col_interesado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_hipoteca_interesado_col_interesado_idx ON interlis_ili2db3_ladm.col_hipoteca USING btree (interesado_col_interesado);


--
-- TOC entry 11186 (class 1259 OID 336503)
-- Name: col_hipoteca_interesado_l_grpcn_ntrsdos_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_hipoteca_interesado_l_grpcn_ntrsdos_idx ON interlis_ili2db3_ladm.col_hipoteca USING btree (interesado_la_agrupacion_interesados);


--
-- TOC entry 11189 (class 1259 OID 336504)
-- Name: col_hipoteca_unidad_la_baunit_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_hipoteca_unidad_la_baunit_idx ON interlis_ili2db3_ladm.col_hipoteca USING btree (unidad_la_baunit);


--
-- TOC entry 11190 (class 1259 OID 336505)
-- Name: col_hipoteca_unidad_predio_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_hipoteca_unidad_predio_idx ON interlis_ili2db3_ladm.col_hipoteca USING btree (unidad_predio);


--
-- TOC entry 11217 (class 1259 OID 336506)
-- Name: col_responsabilidad_interesado_col_interesado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_responsabilidad_interesado_col_interesado_idx ON interlis_ili2db3_ladm.col_responsabilidad USING btree (interesado_col_interesado);


--
-- TOC entry 11218 (class 1259 OID 336507)
-- Name: col_responsabilidad_interesado_l_grpcn_ntrsdos_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_responsabilidad_interesado_l_grpcn_ntrsdos_idx ON interlis_ili2db3_ladm.col_responsabilidad USING btree (interesado_la_agrupacion_interesados);


--
-- TOC entry 11221 (class 1259 OID 336508)
-- Name: col_responsabilidad_unidad_la_baunit_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_responsabilidad_unidad_la_baunit_idx ON interlis_ili2db3_ladm.col_responsabilidad USING btree (unidad_la_baunit);


--
-- TOC entry 11222 (class 1259 OID 336509)
-- Name: col_responsabilidad_unidad_predio_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_responsabilidad_unidad_predio_idx ON interlis_ili2db3_ladm.col_responsabilidad USING btree (unidad_predio);


--
-- TOC entry 11225 (class 1259 OID 336510)
-- Name: col_restriccion_interesado_col_interesado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_restriccion_interesado_col_interesado_idx ON interlis_ili2db3_ladm.col_restriccion USING btree (interesado_col_interesado);


--
-- TOC entry 11226 (class 1259 OID 336511)
-- Name: col_restriccion_interesado_l_grpcn_ntrsdos_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_restriccion_interesado_l_grpcn_ntrsdos_idx ON interlis_ili2db3_ladm.col_restriccion USING btree (interesado_la_agrupacion_interesados);


--
-- TOC entry 11229 (class 1259 OID 336512)
-- Name: col_restriccion_unidad_la_baunit_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_restriccion_unidad_la_baunit_idx ON interlis_ili2db3_ladm.col_restriccion USING btree (unidad_la_baunit);


--
-- TOC entry 11230 (class 1259 OID 336513)
-- Name: col_restriccion_unidad_predio_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_restriccion_unidad_predio_idx ON interlis_ili2db3_ladm.col_restriccion USING btree (unidad_predio);


--
-- TOC entry 11237 (class 1259 OID 336514)
-- Name: col_srvdmbrtptrrn_srvdmbre_terreno_servidumbre_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_srvdmbrtptrrn_srvdmbre_terreno_servidumbre_idx ON interlis_ili2db3_ladm.col_servidumbretipo_terreno_servidumbre USING btree (terreno_servidumbre);


--
-- TOC entry 11242 (class 1259 OID 336515)
-- Name: col_trrtrgrcl_trrtr_grcola_terreno_territorio_agrcola_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_trrtrgrcl_trrtr_grcola_terreno_territorio_agrcola_idx ON interlis_ili2db3_ladm.col_territorioagricola_terreno_territorio_agricola USING btree (terreno_territorio_agricola);


--
-- TOC entry 11170 (class 1259 OID 336516)
-- Name: col_xpltcntp_trrn_xpltcion_terreno_explotacion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX col_xpltcntp_trrn_xpltcion_terreno_explotacion_idx ON interlis_ili2db3_ladm.col_explotaciontipo_terreno_explotacion USING btree (terreno_explotacion);


--
-- TOC entry 11251 (class 1259 OID 336517)
-- Name: construccion_nivel_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX construccion_nivel_idx ON interlis_ili2db3_ladm.construccion USING btree (nivel);


--
-- TOC entry 11254 (class 1259 OID 336518)
-- Name: construccion_poligono_creado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX construccion_poligono_creado_idx ON interlis_ili2db3_ladm.construccion USING gist (poligono_creado);


--
-- TOC entry 11255 (class 1259 OID 336519)
-- Name: construccion_punto_referencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX construccion_punto_referencia_idx ON interlis_ili2db3_ladm.construccion USING gist (punto_referencia);


--
-- TOC entry 11256 (class 1259 OID 336520)
-- Name: construccion_uej2_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX construccion_uej2_construccion_idx ON interlis_ili2db3_ladm.construccion USING btree (uej2_construccion);


--
-- TOC entry 11257 (class 1259 OID 336521)
-- Name: construccion_uej2_la_espacjrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX construccion_uej2_la_espacjrdcrdsrvcios_idx ON interlis_ili2db3_ladm.construccion USING btree (uej2_la_espaciojuridicoredservicios);


--
-- TOC entry 11258 (class 1259 OID 336522)
-- Name: construccion_uej2_la_espcjrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX construccion_uej2_la_espcjrdcndddfccion_idx ON interlis_ili2db3_ladm.construccion USING btree (uej2_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11259 (class 1259 OID 336523)
-- Name: construccion_uej2_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX construccion_uej2_la_unidadespacial_idx ON interlis_ili2db3_ladm.construccion USING btree (uej2_la_unidadespacial);


--
-- TOC entry 11260 (class 1259 OID 336524)
-- Name: construccion_uej2_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX construccion_uej2_servidumbrepaso_idx ON interlis_ili2db3_ladm.construccion USING btree (uej2_servidumbrepaso);


--
-- TOC entry 11261 (class 1259 OID 336525)
-- Name: construccion_uej2_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX construccion_uej2_terreno_idx ON interlis_ili2db3_ladm.construccion USING btree (uej2_terreno);


--
-- TOC entry 11262 (class 1259 OID 336526)
-- Name: construccion_uej2_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX construccion_uej2_unidadconstruccion_idx ON interlis_ili2db3_ladm.construccion USING btree (uej2_unidadconstruccion);


--
-- TOC entry 11265 (class 1259 OID 336527)
-- Name: dq_element_col_derecho_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_col_derecho_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (col_derecho_calidad);


--
-- TOC entry 11266 (class 1259 OID 336528)
-- Name: dq_element_col_fuenteadminstrtv_cldad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_col_fuenteadminstrtv_cldad_idx ON interlis_ili2db3_ladm.dq_element USING btree (col_fuenteadminstrtiva_calidad);


--
-- TOC entry 11267 (class 1259 OID 336529)
-- Name: dq_element_col_fuenteespacial_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_col_fuenteespacial_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (col_fuenteespacial_calidad);


--
-- TOC entry 11268 (class 1259 OID 336530)
-- Name: dq_element_col_hipoteca_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_col_hipoteca_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (col_hipoteca_calidad);


--
-- TOC entry 11269 (class 1259 OID 336531)
-- Name: dq_element_col_interesado_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_col_interesado_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (col_interesado_calidad);


--
-- TOC entry 11270 (class 1259 OID 336532)
-- Name: dq_element_col_responsabilidad_caldad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_col_responsabilidad_caldad_idx ON interlis_ili2db3_ladm.dq_element USING btree (col_responsabilidad_calidad);


--
-- TOC entry 11271 (class 1259 OID 336533)
-- Name: dq_element_col_restriccion_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_col_restriccion_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (col_restriccion_calidad);


--
-- TOC entry 11272 (class 1259 OID 336534)
-- Name: dq_element_construccion_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_construccion_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (construccion_calidad);


--
-- TOC entry 11273 (class 1259 OID 336535)
-- Name: dq_element_la_agrupacion_ntrsds_cldad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_la_agrupacion_ntrsds_cldad_idx ON interlis_ili2db3_ladm.dq_element USING btree (la_agrupacion_intrsdos_calidad);


--
-- TOC entry 11274 (class 1259 OID 336536)
-- Name: dq_element_la_agrupacnnddsspcls_cldad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_la_agrupacnnddsspcls_cldad_idx ON interlis_ili2db3_ladm.dq_element USING btree (la_agrupacinnddsspcles_calidad);


--
-- TOC entry 11275 (class 1259 OID 336537)
-- Name: dq_element_la_baunit_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_la_baunit_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (la_baunit_calidad);


--
-- TOC entry 11276 (class 1259 OID 336538)
-- Name: dq_element_la_cadenacaraslimite_cldad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_la_cadenacaraslimite_cldad_idx ON interlis_ili2db3_ladm.dq_element USING btree (la_cadenacaraslimite_calidad);


--
-- TOC entry 11277 (class 1259 OID 336539)
-- Name: dq_element_la_caraslindero_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_la_caraslindero_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (la_caraslindero_calidad);


--
-- TOC entry 11278 (class 1259 OID 336540)
-- Name: dq_element_la_espacijrdcrdsrvcs_cldad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_la_espacijrdcrdsrvcs_cldad_idx ON interlis_ili2db3_ladm.dq_element USING btree (la_espacijrdcrdsrvcios_calidad);


--
-- TOC entry 11279 (class 1259 OID 336541)
-- Name: dq_element_la_espacjrdcndddfccn_cldad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_la_espacjrdcndddfccn_cldad_idx ON interlis_ili2db3_ladm.dq_element USING btree (la_espacjrdcndddfccion_calidad);


--
-- TOC entry 11280 (class 1259 OID 336542)
-- Name: dq_element_la_nivel_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_la_nivel_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (la_nivel_calidad);


--
-- TOC entry 11281 (class 1259 OID 336543)
-- Name: dq_element_la_punto_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_la_punto_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (la_punto_calidad);


--
-- TOC entry 11282 (class 1259 OID 336544)
-- Name: dq_element_la_relacionnecsrbnts_cldad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_la_relacionnecsrbnts_cldad_idx ON interlis_ili2db3_ladm.dq_element USING btree (la_relacionnecesrbnits_calidad);


--
-- TOC entry 11283 (class 1259 OID 336545)
-- Name: dq_element_la_rlcnncsrnddsspcls_cldad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_la_rlcnncsrnddsspcls_cldad_idx ON interlis_ili2db3_ladm.dq_element USING btree (la_relcnncsrnddsspcles_calidad);


--
-- TOC entry 11284 (class 1259 OID 336546)
-- Name: dq_element_la_unidadespacial_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_la_unidadespacial_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (la_unidadespacial_calidad);


--
-- TOC entry 11285 (class 1259 OID 336547)
-- Name: dq_element_lindero_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_lindero_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (lindero_calidad);


--
-- TOC entry 11286 (class 1259 OID 336548)
-- Name: dq_element_om_observacion_rsltd_cldad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_om_observacion_rsltd_cldad_idx ON interlis_ili2db3_ladm.dq_element USING btree (om_observacion_resultado_calidad);


--
-- TOC entry 11289 (class 1259 OID 336549)
-- Name: dq_element_predio_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_predio_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (predio_calidad);


--
-- TOC entry 11290 (class 1259 OID 336550)
-- Name: dq_element_publicidad_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_publicidad_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (publicidad_calidad);


--
-- TOC entry 11291 (class 1259 OID 336551)
-- Name: dq_element_puntocontrol_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_puntocontrol_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (puntocontrol_calidad);


--
-- TOC entry 11292 (class 1259 OID 336552)
-- Name: dq_element_puntolevantamiento_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_puntolevantamiento_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (puntolevantamiento_calidad);


--
-- TOC entry 11293 (class 1259 OID 336553)
-- Name: dq_element_puntolindero_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_puntolindero_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (puntolindero_calidad);


--
-- TOC entry 11294 (class 1259 OID 336554)
-- Name: dq_element_servidumbrepaso_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_servidumbrepaso_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (servidumbrepaso_calidad);


--
-- TOC entry 11295 (class 1259 OID 336555)
-- Name: dq_element_terreno_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_terreno_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (terreno_calidad);


--
-- TOC entry 11296 (class 1259 OID 336556)
-- Name: dq_element_unidadconstruccion_calidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_element_unidadconstruccion_calidad_idx ON interlis_ili2db3_ladm.dq_element USING btree (unidadconstruccion_calidad);


--
-- TOC entry 11299 (class 1259 OID 336557)
-- Name: dq_positionalaccuracy_la_punto_exactitud_estmada_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_positionalaccuracy_la_punto_exactitud_estmada_idx ON interlis_ili2db3_ladm.dq_positionalaccuracy USING btree (la_punto_exactitud_estimada);


--
-- TOC entry 11302 (class 1259 OID 336558)
-- Name: dq_positionalaccuracy_puntocontrol_excttd_stmada_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_positionalaccuracy_puntocontrol_excttd_stmada_idx ON interlis_ili2db3_ladm.dq_positionalaccuracy USING btree (puntocontrol_exactitud_estimada);


--
-- TOC entry 11303 (class 1259 OID 336559)
-- Name: dq_positionalaccuracy_puntolevntmnt_xcttd_stmada_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_positionalaccuracy_puntolevntmnt_xcttd_stmada_idx ON interlis_ili2db3_ladm.dq_positionalaccuracy USING btree (puntolevantamiento_exactitud_estimada);


--
-- TOC entry 11304 (class 1259 OID 336560)
-- Name: dq_positionalaccuracy_puntolindero_excttd_stmada_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX dq_positionalaccuracy_puntolindero_excttd_stmada_idx ON interlis_ili2db3_ladm.dq_positionalaccuracy USING btree (puntolindero_exactitud_estimada);


--
-- TOC entry 11305 (class 1259 OID 336561)
-- Name: extarchivo_col_fntdmnstrtv_xt_rchv_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extarchivo_col_fntdmnstrtv_xt_rchv_id_idx ON interlis_ili2db3_ladm.extarchivo USING btree (col_fuenteadminstrtiva_ext_archivo_id);


--
-- TOC entry 11306 (class 1259 OID 336562)
-- Name: extarchivo_col_fuenteespcl_xt_rchv_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extarchivo_col_fuenteespcl_xt_rchv_id_idx ON interlis_ili2db3_ladm.extarchivo USING btree (col_fuenteespacial_ext_archivo_id);


--
-- TOC entry 11309 (class 1259 OID 336563)
-- Name: extdireccion_construccion_ext_dirccn_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extdireccion_construccion_ext_dirccn_id_idx ON interlis_ili2db3_ladm.extdireccion USING btree (construccion_ext_direccion_id);


--
-- TOC entry 11310 (class 1259 OID 336564)
-- Name: extdireccion_coordenada_direccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extdireccion_coordenada_direccion_idx ON interlis_ili2db3_ladm.extdireccion USING gist (coordenada_direccion);


--
-- TOC entry 11311 (class 1259 OID 336565)
-- Name: extdireccion_extinteresado_ext_drccn_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extdireccion_extinteresado_ext_drccn_id_idx ON interlis_ili2db3_ladm.extdireccion USING btree (extinteresado_ext_direccion_id);


--
-- TOC entry 11312 (class 1259 OID 336566)
-- Name: extdireccion_extndddfccnfsc_xt_drccn_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extdireccion_extndddfccnfsc_xt_drccn_id_idx ON interlis_ili2db3_ladm.extdireccion USING btree (extunidadedificcnfsica_ext_direccion_id);


--
-- TOC entry 11313 (class 1259 OID 336567)
-- Name: extdireccion_la_spcjrdcnddn_xt_drccn_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extdireccion_la_spcjrdcnddn_xt_drccn_id_idx ON interlis_ili2db3_ladm.extdireccion USING btree (la_espacjrdcndddfccion_ext_direccion_id);


--
-- TOC entry 11314 (class 1259 OID 336568)
-- Name: extdireccion_la_spcjrdcrdss_xt_drccn_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extdireccion_la_spcjrdcrdss_xt_drccn_id_idx ON interlis_ili2db3_ladm.extdireccion USING btree (la_espacijrdcrdsrvcios_ext_direccion_id);


--
-- TOC entry 11315 (class 1259 OID 336569)
-- Name: extdireccion_la_unidadespcl_xt_drccn_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extdireccion_la_unidadespcl_xt_drccn_id_idx ON interlis_ili2db3_ladm.extdireccion USING btree (la_unidadespacial_ext_direccion_id);


--
-- TOC entry 11318 (class 1259 OID 336570)
-- Name: extdireccion_servidumbrepas_xt_drccn_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extdireccion_servidumbrepas_xt_drccn_id_idx ON interlis_ili2db3_ladm.extdireccion USING btree (servidumbrepaso_ext_direccion_id);


--
-- TOC entry 11319 (class 1259 OID 336571)
-- Name: extdireccion_terreno_ext_direccion_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extdireccion_terreno_ext_direccion_id_idx ON interlis_ili2db3_ladm.extdireccion USING btree (terreno_ext_direccion_id);


--
-- TOC entry 11320 (class 1259 OID 336572)
-- Name: extdireccion_unidadcnstrccn_xt_drccn_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extdireccion_unidadcnstrccn_xt_drccn_id_idx ON interlis_ili2db3_ladm.extdireccion USING btree (unidadconstruccion_ext_direccion_id);


--
-- TOC entry 11321 (class 1259 OID 336573)
-- Name: extinteresado_col_interesado_ext_pid_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extinteresado_col_interesado_ext_pid_idx ON interlis_ili2db3_ladm.extinteresado USING btree (col_interesado_ext_pid);


--
-- TOC entry 11322 (class 1259 OID 336574)
-- Name: extinteresado_extrdsrvcsfscd_dmnstrdr_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extinteresado_extrdsrvcsfscd_dmnstrdr_id_idx ON interlis_ili2db3_ladm.extinteresado USING btree (extredserviciosfisica_ext_interesado_administrador_id);


--
-- TOC entry 11323 (class 1259 OID 336575)
-- Name: extinteresado_la_agrupacin_ntrsds_xt_pid_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extinteresado_la_agrupacin_ntrsds_xt_pid_idx ON interlis_ili2db3_ladm.extinteresado USING btree (la_agrupacion_intrsdos_ext_pid);


--
-- TOC entry 11326 (class 1259 OID 336576)
-- Name: extredserviciosfisica_la_spcjrdcrdsxt_d_rd_fsica_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extredserviciosfisica_la_spcjrdcrdsxt_d_rd_fsica_idx ON interlis_ili2db3_ladm.extredserviciosfisica USING btree (la_espacijrdcrdsrvcios_ext_id_red_fisica);


--
-- TOC entry 11329 (class 1259 OID 336577)
-- Name: extunidadedificacionfisica_constrccn_xt__dfccn_fsc_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extunidadedificacionfisica_constrccn_xt__dfccn_fsc_id_idx ON interlis_ili2db3_ladm.extunidadedificacionfisica USING btree (construccion_ext_unidad_edificacion_fisica_id);


--
-- TOC entry 11330 (class 1259 OID 336578)
-- Name: extunidadedificacionfisica_la_spcjrdcndd_dfccn_fsc_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extunidadedificacionfisica_la_spcjrdcndd_dfccn_fsc_id_idx ON interlis_ili2db3_ladm.extunidadedificacionfisica USING btree (la_espacjrdcndddfccion_ext_unidad_edificacion_fisic_id);


--
-- TOC entry 11333 (class 1259 OID 336579)
-- Name: extunidadedificacionfisica_uniddcnstrccn_dfccn_fsc_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX extunidadedificacionfisica_uniddcnstrccn_dfccn_fsc_id_idx ON interlis_ili2db3_ladm.extunidadedificacionfisica USING btree (unidadconstruccion_ext_unidad_edificacion_fisica_id);


--
-- TOC entry 11334 (class 1259 OID 336580)
-- Name: fraccion_col_derecho_compartido_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX fraccion_col_derecho_compartido_idx ON interlis_ili2db3_ladm.fraccion USING btree (col_derecho_compartido);


--
-- TOC entry 11335 (class 1259 OID 336581)
-- Name: fraccion_col_hipoteca_compartido_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX fraccion_col_hipoteca_compartido_idx ON interlis_ili2db3_ladm.fraccion USING btree (col_hipoteca_compartido);


--
-- TOC entry 11336 (class 1259 OID 336582)
-- Name: fraccion_col_responsabildd_cmprtido_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX fraccion_col_responsabildd_cmprtido_idx ON interlis_ili2db3_ladm.fraccion USING btree (col_responsabilidad_compartido);


--
-- TOC entry 11337 (class 1259 OID 336583)
-- Name: fraccion_col_restriccion_compartido_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX fraccion_col_restriccion_compartido_idx ON interlis_ili2db3_ladm.fraccion USING btree (col_restriccion_compartido);


--
-- TOC entry 11338 (class 1259 OID 336584)
-- Name: fraccion_miembros_participacion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX fraccion_miembros_participacion_idx ON interlis_ili2db3_ladm.fraccion USING btree (miembros_participacion);


--
-- TOC entry 11341 (class 1259 OID 336585)
-- Name: fraccion_predio_copropiedad_cofcnte_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX fraccion_predio_copropiedad_cofcnte_idx ON interlis_ili2db3_ladm.fraccion USING btree (predio_copropiedad_coeficiente);


--
-- TOC entry 11346 (class 1259 OID 336586)
-- Name: gm_surface2dlistvalue_avalue_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX gm_surface2dlistvalue_avalue_idx ON interlis_ili2db3_ladm.gm_surface2dlistvalue USING gist (avalue);


--
-- TOC entry 11347 (class 1259 OID 336587)
-- Name: gm_surface2dlistvalue_gm_multisurface2d_geometry_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX gm_surface2dlistvalue_gm_multisurface2d_geometry_idx ON interlis_ili2db3_ladm.gm_surface2dlistvalue USING btree (gm_multisurface2d_geometry);


--
-- TOC entry 11350 (class 1259 OID 336588)
-- Name: gm_surface3dlistvalue_avalue_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX gm_surface3dlistvalue_avalue_idx ON interlis_ili2db3_ladm.gm_surface3dlistvalue USING gist (avalue);


--
-- TOC entry 11351 (class 1259 OID 336589)
-- Name: gm_surface3dlistvalue_gm_multisurface3d_geometry_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX gm_surface3dlistvalue_gm_multisurface3d_geometry_idx ON interlis_ili2db3_ladm.gm_surface3dlistvalue USING btree (gm_multisurface3d_geometry);


--
-- TOC entry 11354 (class 1259 OID 336590)
-- Name: hipotecaderecho_derecho_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX hipotecaderecho_derecho_idx ON interlis_ili2db3_ladm.hipotecaderecho USING btree (derecho);


--
-- TOC entry 11355 (class 1259 OID 336591)
-- Name: hipotecaderecho_hipoteca_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX hipotecaderecho_hipoteca_idx ON interlis_ili2db3_ladm.hipotecaderecho USING btree (hipoteca);


--
-- TOC entry 11358 (class 1259 OID 336592)
-- Name: imagen_extinteresado_firma_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX imagen_extinteresado_firma_idx ON interlis_ili2db3_ladm.imagen USING btree (extinteresado_firma);


--
-- TOC entry 11359 (class 1259 OID 336593)
-- Name: imagen_extinteresado_fotografia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX imagen_extinteresado_fotografia_idx ON interlis_ili2db3_ladm.imagen USING btree (extinteresado_fotografia);


--
-- TOC entry 11360 (class 1259 OID 336594)
-- Name: imagen_extinteresado_huell_dctlar_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX imagen_extinteresado_huell_dctlar_idx ON interlis_ili2db3_ladm.imagen USING btree (extinteresado_huella_dactilar);


--
-- TOC entry 11363 (class 1259 OID 336595)
-- Name: interesado_contacto_interesado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX interesado_contacto_interesado_idx ON interlis_ili2db3_ladm.interesado_contacto USING btree (interesado);


--
-- TOC entry 11374 (class 1259 OID 336596)
-- Name: la_agrupacionunidadsspcles_aset_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_agrupacionunidadsspcles_aset_idx ON interlis_ili2db3_ladm.la_agrupacionunidadesespaciales USING btree (aset);


--
-- TOC entry 11375 (class 1259 OID 336597)
-- Name: la_agrupacionunidadsspcles_punto_referencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_agrupacionunidadsspcles_punto_referencia_idx ON interlis_ili2db3_ladm.la_agrupacionunidadesespaciales USING gist (punto_referencia);


--
-- TOC entry 11380 (class 1259 OID 336598)
-- Name: la_cadenacaraslimite_geometria_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_cadenacaraslimite_geometria_idx ON interlis_ili2db3_ladm.la_cadenacaraslimite USING gist (geometria);


--
-- TOC entry 11383 (class 1259 OID 336599)
-- Name: la_caraslindero_geometria_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_caraslindero_geometria_idx ON interlis_ili2db3_ladm.la_caraslindero USING gist (geometria);


--
-- TOC entry 11404 (class 1259 OID 336600)
-- Name: la_espaciojuridcndddfccion_nivel_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridcndddfccion_nivel_idx ON interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion USING btree (nivel);


--
-- TOC entry 11405 (class 1259 OID 336601)
-- Name: la_espaciojuridcndddfccion_poligono_creado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridcndddfccion_poligono_creado_idx ON interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion USING gist (poligono_creado);


--
-- TOC entry 11406 (class 1259 OID 336602)
-- Name: la_espaciojuridcndddfccion_punto_referencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridcndddfccion_punto_referencia_idx ON interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion USING gist (punto_referencia);


--
-- TOC entry 11407 (class 1259 OID 336603)
-- Name: la_espaciojuridcndddfccion_uej2_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridcndddfccion_uej2_construccion_idx ON interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion USING btree (uej2_construccion);


--
-- TOC entry 11408 (class 1259 OID 336604)
-- Name: la_espaciojuridcndddfccion_uej2_la_espacjrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridcndddfccion_uej2_la_espacjrdcrdsrvcios_idx ON interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion USING btree (uej2_la_espaciojuridicoredservicios);


--
-- TOC entry 11409 (class 1259 OID 336605)
-- Name: la_espaciojuridcndddfccion_uej2_la_espcjrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridcndddfccion_uej2_la_espcjrdcndddfccion_idx ON interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion USING btree (uej2_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11410 (class 1259 OID 336606)
-- Name: la_espaciojuridcndddfccion_uej2_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridcndddfccion_uej2_la_unidadespacial_idx ON interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion USING btree (uej2_la_unidadespacial);


--
-- TOC entry 11411 (class 1259 OID 336607)
-- Name: la_espaciojuridcndddfccion_uej2_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridcndddfccion_uej2_servidumbrepaso_idx ON interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion USING btree (uej2_servidumbrepaso);


--
-- TOC entry 11412 (class 1259 OID 336608)
-- Name: la_espaciojuridcndddfccion_uej2_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridcndddfccion_uej2_terreno_idx ON interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion USING btree (uej2_terreno);


--
-- TOC entry 11413 (class 1259 OID 336609)
-- Name: la_espaciojuridcndddfccion_uej2_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridcndddfccion_uej2_unidadconstruccion_idx ON interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion USING btree (uej2_unidadconstruccion);


--
-- TOC entry 11394 (class 1259 OID 336610)
-- Name: la_espaciojuridicrdsrvcios_nivel_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridicrdsrvcios_nivel_idx ON interlis_ili2db3_ladm.la_espaciojuridicoredservicios USING btree (nivel);


--
-- TOC entry 11395 (class 1259 OID 336611)
-- Name: la_espaciojuridicrdsrvcios_poligono_creado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridicrdsrvcios_poligono_creado_idx ON interlis_ili2db3_ladm.la_espaciojuridicoredservicios USING gist (poligono_creado);


--
-- TOC entry 11396 (class 1259 OID 336612)
-- Name: la_espaciojuridicrdsrvcios_punto_referencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridicrdsrvcios_punto_referencia_idx ON interlis_ili2db3_ladm.la_espaciojuridicoredservicios USING gist (punto_referencia);


--
-- TOC entry 11397 (class 1259 OID 336613)
-- Name: la_espaciojuridicrdsrvcios_uej2_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridicrdsrvcios_uej2_construccion_idx ON interlis_ili2db3_ladm.la_espaciojuridicoredservicios USING btree (uej2_construccion);


--
-- TOC entry 11398 (class 1259 OID 336614)
-- Name: la_espaciojuridicrdsrvcios_uej2_la_espacjrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridicrdsrvcios_uej2_la_espacjrdcrdsrvcios_idx ON interlis_ili2db3_ladm.la_espaciojuridicoredservicios USING btree (uej2_la_espaciojuridicoredservicios);


--
-- TOC entry 11399 (class 1259 OID 336615)
-- Name: la_espaciojuridicrdsrvcios_uej2_la_espcjrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridicrdsrvcios_uej2_la_espcjrdcndddfccion_idx ON interlis_ili2db3_ladm.la_espaciojuridicoredservicios USING btree (uej2_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11400 (class 1259 OID 336616)
-- Name: la_espaciojuridicrdsrvcios_uej2_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridicrdsrvcios_uej2_la_unidadespacial_idx ON interlis_ili2db3_ladm.la_espaciojuridicoredservicios USING btree (uej2_la_unidadespacial);


--
-- TOC entry 11401 (class 1259 OID 336617)
-- Name: la_espaciojuridicrdsrvcios_uej2_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridicrdsrvcios_uej2_servidumbrepaso_idx ON interlis_ili2db3_ladm.la_espaciojuridicoredservicios USING btree (uej2_servidumbrepaso);


--
-- TOC entry 11402 (class 1259 OID 336618)
-- Name: la_espaciojuridicrdsrvcios_uej2_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridicrdsrvcios_uej2_terreno_idx ON interlis_ili2db3_ladm.la_espaciojuridicoredservicios USING btree (uej2_terreno);


--
-- TOC entry 11403 (class 1259 OID 336619)
-- Name: la_espaciojuridicrdsrvcios_uej2_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_espaciojuridicrdsrvcios_uej2_unidadconstruccion_idx ON interlis_ili2db3_ladm.la_espaciojuridicoredservicios USING btree (uej2_unidadconstruccion);


--
-- TOC entry 11436 (class 1259 OID 336620)
-- Name: la_punto_localizacion_original_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_punto_localizacion_original_idx ON interlis_ili2db3_ladm.la_punto USING gist (localizacion_original);


--
-- TOC entry 11439 (class 1259 OID 336621)
-- Name: la_punto_ue_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_punto_ue_construccion_idx ON interlis_ili2db3_ladm.la_punto USING btree (ue_construccion);


--
-- TOC entry 11440 (class 1259 OID 336622)
-- Name: la_punto_ue_la_espacijrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_punto_ue_la_espacijrdcndddfccion_idx ON interlis_ili2db3_ladm.la_punto USING btree (ue_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11441 (class 1259 OID 336623)
-- Name: la_punto_ue_la_espaciojrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_punto_ue_la_espaciojrdcrdsrvcios_idx ON interlis_ili2db3_ladm.la_punto USING btree (ue_la_espaciojuridicoredservicios);


--
-- TOC entry 11442 (class 1259 OID 336624)
-- Name: la_punto_ue_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_punto_ue_la_unidadespacial_idx ON interlis_ili2db3_ladm.la_punto USING btree (ue_la_unidadespacial);


--
-- TOC entry 11443 (class 1259 OID 336625)
-- Name: la_punto_ue_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_punto_ue_servidumbrepaso_idx ON interlis_ili2db3_ladm.la_punto USING btree (ue_servidumbrepaso);


--
-- TOC entry 11444 (class 1259 OID 336626)
-- Name: la_punto_ue_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_punto_ue_terreno_idx ON interlis_ili2db3_ladm.la_punto USING btree (ue_terreno);


--
-- TOC entry 11445 (class 1259 OID 336627)
-- Name: la_punto_ue_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_punto_ue_unidadconstruccion_idx ON interlis_ili2db3_ladm.la_punto USING btree (ue_unidadconstruccion);


--
-- TOC entry 11462 (class 1259 OID 336628)
-- Name: la_tareainteresadotipo_col_interesado_tarea_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_tareainteresadotipo_col_interesado_tarea_idx ON interlis_ili2db3_ladm.la_tareainteresadotipo USING btree (col_interesado_tarea);


--
-- TOC entry 11463 (class 1259 OID 336629)
-- Name: la_tareainteresadotipo_la_agrupacion_intrsds_trea_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_tareainteresadotipo_la_agrupacion_intrsds_trea_idx ON interlis_ili2db3_ladm.la_tareainteresadotipo USING btree (la_agrupacion_intrsdos_tarea);


--
-- TOC entry 11468 (class 1259 OID 336630)
-- Name: la_transformacion_la_pnt_trnsfrmcn_y_rsltado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_transformacion_la_pnt_trnsfrmcn_y_rsltado_idx ON interlis_ili2db3_ladm.la_transformacion USING btree (la_punto_transformacion_y_resultado);


--
-- TOC entry 11469 (class 1259 OID 336631)
-- Name: la_transformacion_localizacion_transformada_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_transformacion_localizacion_transformada_idx ON interlis_ili2db3_ladm.la_transformacion USING gist (localizacion_transformada);


--
-- TOC entry 11472 (class 1259 OID 336632)
-- Name: la_transformacion_puntcntrl_trnmcn_y_rsltado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_transformacion_puntcntrl_trnmcn_y_rsltado_idx ON interlis_ili2db3_ladm.la_transformacion USING btree (puntocontrol_transformacion_y_resultado);


--
-- TOC entry 11473 (class 1259 OID 336633)
-- Name: la_transformacion_puntlndr_trnsmcn_y_rsltado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_transformacion_puntlndr_trnsmcn_y_rsltado_idx ON interlis_ili2db3_ladm.la_transformacion USING btree (puntolindero_transformacion_y_resultado);


--
-- TOC entry 11474 (class 1259 OID 336634)
-- Name: la_transformacion_puntlvntmnt_tmcn_y_rsltado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_transformacion_puntlvntmnt_tmcn_y_rsltado_idx ON interlis_ili2db3_ladm.la_transformacion USING btree (puntolevantamiento_transformacion_y_resultado);


--
-- TOC entry 11477 (class 1259 OID 336635)
-- Name: la_unidadespacial_nivel_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_unidadespacial_nivel_idx ON interlis_ili2db3_ladm.la_unidadespacial USING btree (nivel);


--
-- TOC entry 11480 (class 1259 OID 336636)
-- Name: la_unidadespacial_poligono_creado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_unidadespacial_poligono_creado_idx ON interlis_ili2db3_ladm.la_unidadespacial USING gist (poligono_creado);


--
-- TOC entry 11481 (class 1259 OID 336637)
-- Name: la_unidadespacial_punto_referencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_unidadespacial_punto_referencia_idx ON interlis_ili2db3_ladm.la_unidadespacial USING gist (punto_referencia);


--
-- TOC entry 11482 (class 1259 OID 336638)
-- Name: la_unidadespacial_uej2_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_unidadespacial_uej2_construccion_idx ON interlis_ili2db3_ladm.la_unidadespacial USING btree (uej2_construccion);


--
-- TOC entry 11483 (class 1259 OID 336639)
-- Name: la_unidadespacial_uej2_la_espacjrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_unidadespacial_uej2_la_espacjrdcrdsrvcios_idx ON interlis_ili2db3_ladm.la_unidadespacial USING btree (uej2_la_espaciojuridicoredservicios);


--
-- TOC entry 11484 (class 1259 OID 336640)
-- Name: la_unidadespacial_uej2_la_espcjrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_unidadespacial_uej2_la_espcjrdcndddfccion_idx ON interlis_ili2db3_ladm.la_unidadespacial USING btree (uej2_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11485 (class 1259 OID 336641)
-- Name: la_unidadespacial_uej2_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_unidadespacial_uej2_la_unidadespacial_idx ON interlis_ili2db3_ladm.la_unidadespacial USING btree (uej2_la_unidadespacial);


--
-- TOC entry 11486 (class 1259 OID 336642)
-- Name: la_unidadespacial_uej2_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_unidadespacial_uej2_servidumbrepaso_idx ON interlis_ili2db3_ladm.la_unidadespacial USING btree (uej2_servidumbrepaso);


--
-- TOC entry 11487 (class 1259 OID 336643)
-- Name: la_unidadespacial_uej2_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_unidadespacial_uej2_terreno_idx ON interlis_ili2db3_ladm.la_unidadespacial USING btree (uej2_terreno);


--
-- TOC entry 11488 (class 1259 OID 336644)
-- Name: la_unidadespacial_uej2_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_unidadespacial_uej2_unidadconstruccion_idx ON interlis_ili2db3_ladm.la_unidadespacial USING btree (uej2_unidadconstruccion);


--
-- TOC entry 11491 (class 1259 OID 336645)
-- Name: la_volumenvalor_construccion_volumen_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_volumenvalor_construccion_volumen_idx ON interlis_ili2db3_ladm.la_volumenvalor USING btree (construccion_volumen);


--
-- TOC entry 11492 (class 1259 OID 336646)
-- Name: la_volumenvalor_la_espacijrdcrdsrvcs_vlmen_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_volumenvalor_la_espacijrdcrdsrvcs_vlmen_idx ON interlis_ili2db3_ladm.la_volumenvalor USING btree (la_espacijrdcrdsrvcios_volumen);


--
-- TOC entry 11493 (class 1259 OID 336647)
-- Name: la_volumenvalor_la_espacjrdcndddfccn_vlmen_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_volumenvalor_la_espacjrdcndddfccn_vlmen_idx ON interlis_ili2db3_ladm.la_volumenvalor USING btree (la_espacjrdcndddfccion_volumen);


--
-- TOC entry 11494 (class 1259 OID 336648)
-- Name: la_volumenvalor_la_unidadespacial_volumen_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_volumenvalor_la_unidadespacial_volumen_idx ON interlis_ili2db3_ladm.la_volumenvalor USING btree (la_unidadespacial_volumen);


--
-- TOC entry 11497 (class 1259 OID 336649)
-- Name: la_volumenvalor_servidumbrepaso_volumen_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_volumenvalor_servidumbrepaso_volumen_idx ON interlis_ili2db3_ladm.la_volumenvalor USING btree (servidumbrepaso_volumen);


--
-- TOC entry 11498 (class 1259 OID 336650)
-- Name: la_volumenvalor_terreno_volumen_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_volumenvalor_terreno_volumen_idx ON interlis_ili2db3_ladm.la_volumenvalor USING btree (terreno_volumen);


--
-- TOC entry 11499 (class 1259 OID 336651)
-- Name: la_volumenvalor_unidadconstruccion_volumen_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX la_volumenvalor_unidadconstruccion_volumen_idx ON interlis_ili2db3_ladm.la_volumenvalor USING btree (unidadconstruccion_volumen);


--
-- TOC entry 11500 (class 1259 OID 336652)
-- Name: li_lineaje_la_punto_metodoproduccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX li_lineaje_la_punto_metodoproduccion_idx ON interlis_ili2db3_ladm.li_lineaje USING btree (la_punto_metodoproduccion);


--
-- TOC entry 11503 (class 1259 OID 336653)
-- Name: li_lineaje_puntocontrol_metodprdccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX li_lineaje_puntocontrol_metodprdccion_idx ON interlis_ili2db3_ladm.li_lineaje USING btree (puntocontrol_metodoproduccion);


--
-- TOC entry 11504 (class 1259 OID 336654)
-- Name: li_lineaje_puntolevantmnt_mtdprdccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX li_lineaje_puntolevantmnt_mtdprdccion_idx ON interlis_ili2db3_ladm.li_lineaje USING btree (puntolevantamiento_metodoproduccion);


--
-- TOC entry 11505 (class 1259 OID 336655)
-- Name: li_lineaje_puntolindero_metodprdccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX li_lineaje_puntolindero_metodprdccion_idx ON interlis_ili2db3_ladm.li_lineaje USING btree (puntolindero_metodoproduccion);


--
-- TOC entry 11506 (class 1259 OID 336656)
-- Name: lindero_geometria_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX lindero_geometria_idx ON interlis_ili2db3_ladm.lindero USING gist (geometria);


--
-- TOC entry 11509 (class 1259 OID 336657)
-- Name: mas_clp_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX mas_clp_idx ON interlis_ili2db3_ladm.mas USING btree (clp);


--
-- TOC entry 11512 (class 1259 OID 336658)
-- Name: mas_uep_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX mas_uep_construccion_idx ON interlis_ili2db3_ladm.mas USING btree (uep_construccion);


--
-- TOC entry 11513 (class 1259 OID 336659)
-- Name: mas_uep_la_espacijrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX mas_uep_la_espacijrdcrdsrvcios_idx ON interlis_ili2db3_ladm.mas USING btree (uep_la_espaciojuridicoredservicios);


--
-- TOC entry 11514 (class 1259 OID 336660)
-- Name: mas_uep_la_espacjrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX mas_uep_la_espacjrdcndddfccion_idx ON interlis_ili2db3_ladm.mas USING btree (uep_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11515 (class 1259 OID 336661)
-- Name: mas_uep_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX mas_uep_la_unidadespacial_idx ON interlis_ili2db3_ladm.mas USING btree (uep_la_unidadespacial);


--
-- TOC entry 11516 (class 1259 OID 336662)
-- Name: mas_uep_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX mas_uep_servidumbrepaso_idx ON interlis_ili2db3_ladm.mas USING btree (uep_servidumbrepaso);


--
-- TOC entry 11517 (class 1259 OID 336663)
-- Name: mas_uep_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX mas_uep_terreno_idx ON interlis_ili2db3_ladm.mas USING btree (uep_terreno);


--
-- TOC entry 11518 (class 1259 OID 336664)
-- Name: mas_uep_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX mas_uep_unidadconstruccion_idx ON interlis_ili2db3_ladm.mas USING btree (uep_unidadconstruccion);


--
-- TOC entry 11519 (class 1259 OID 336665)
-- Name: masccl_cclp_la_cadenacaraslimite_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX masccl_cclp_la_cadenacaraslimite_idx ON interlis_ili2db3_ladm.masccl USING btree (cclp_la_cadenacaraslimite);


--
-- TOC entry 11520 (class 1259 OID 336666)
-- Name: masccl_cclp_lindero_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX masccl_cclp_lindero_idx ON interlis_ili2db3_ladm.masccl USING btree (cclp_lindero);


--
-- TOC entry 11523 (class 1259 OID 336667)
-- Name: masccl_uep_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX masccl_uep_construccion_idx ON interlis_ili2db3_ladm.masccl USING btree (uep_construccion);


--
-- TOC entry 11524 (class 1259 OID 336668)
-- Name: masccl_uep_la_espacijrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX masccl_uep_la_espacijrdcrdsrvcios_idx ON interlis_ili2db3_ladm.masccl USING btree (uep_la_espaciojuridicoredservicios);


--
-- TOC entry 11525 (class 1259 OID 336669)
-- Name: masccl_uep_la_espacjrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX masccl_uep_la_espacjrdcndddfccion_idx ON interlis_ili2db3_ladm.masccl USING btree (uep_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11526 (class 1259 OID 336670)
-- Name: masccl_uep_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX masccl_uep_la_unidadespacial_idx ON interlis_ili2db3_ladm.masccl USING btree (uep_la_unidadespacial);


--
-- TOC entry 11527 (class 1259 OID 336671)
-- Name: masccl_uep_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX masccl_uep_servidumbrepaso_idx ON interlis_ili2db3_ladm.masccl USING btree (uep_servidumbrepaso);


--
-- TOC entry 11528 (class 1259 OID 336672)
-- Name: masccl_uep_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX masccl_uep_terreno_idx ON interlis_ili2db3_ladm.masccl USING btree (uep_terreno);


--
-- TOC entry 11529 (class 1259 OID 336673)
-- Name: masccl_uep_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX masccl_uep_unidadconstruccion_idx ON interlis_ili2db3_ladm.masccl USING btree (uep_unidadconstruccion);


--
-- TOC entry 11530 (class 1259 OID 336674)
-- Name: menos_ccl_la_cadenacaraslimite_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menos_ccl_la_cadenacaraslimite_idx ON interlis_ili2db3_ladm.menos USING btree (ccl_la_cadenacaraslimite);


--
-- TOC entry 11531 (class 1259 OID 336675)
-- Name: menos_ccl_lindero_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menos_ccl_lindero_idx ON interlis_ili2db3_ladm.menos USING btree (ccl_lindero);


--
-- TOC entry 11532 (class 1259 OID 336676)
-- Name: menos_eu_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menos_eu_construccion_idx ON interlis_ili2db3_ladm.menos USING btree (eu_construccion);


--
-- TOC entry 11533 (class 1259 OID 336677)
-- Name: menos_eu_la_espacijrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menos_eu_la_espacijrdcndddfccion_idx ON interlis_ili2db3_ladm.menos USING btree (eu_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11534 (class 1259 OID 336678)
-- Name: menos_eu_la_espaciojrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menos_eu_la_espaciojrdcrdsrvcios_idx ON interlis_ili2db3_ladm.menos USING btree (eu_la_espaciojuridicoredservicios);


--
-- TOC entry 11535 (class 1259 OID 336679)
-- Name: menos_eu_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menos_eu_la_unidadespacial_idx ON interlis_ili2db3_ladm.menos USING btree (eu_la_unidadespacial);


--
-- TOC entry 11536 (class 1259 OID 336680)
-- Name: menos_eu_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menos_eu_servidumbrepaso_idx ON interlis_ili2db3_ladm.menos USING btree (eu_servidumbrepaso);


--
-- TOC entry 11537 (class 1259 OID 336681)
-- Name: menos_eu_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menos_eu_terreno_idx ON interlis_ili2db3_ladm.menos USING btree (eu_terreno);


--
-- TOC entry 11538 (class 1259 OID 336682)
-- Name: menos_eu_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menos_eu_unidadconstruccion_idx ON interlis_ili2db3_ladm.menos USING btree (eu_unidadconstruccion);


--
-- TOC entry 11541 (class 1259 OID 336683)
-- Name: menosf_cl_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menosf_cl_idx ON interlis_ili2db3_ladm.menosf USING btree (cl);


--
-- TOC entry 11544 (class 1259 OID 336684)
-- Name: menosf_ue_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menosf_ue_construccion_idx ON interlis_ili2db3_ladm.menosf USING btree (ue_construccion);


--
-- TOC entry 11545 (class 1259 OID 336685)
-- Name: menosf_ue_la_espacijrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menosf_ue_la_espacijrdcndddfccion_idx ON interlis_ili2db3_ladm.menosf USING btree (ue_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11546 (class 1259 OID 336686)
-- Name: menosf_ue_la_espaciojrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menosf_ue_la_espaciojrdcrdsrvcios_idx ON interlis_ili2db3_ladm.menosf USING btree (ue_la_espaciojuridicoredservicios);


--
-- TOC entry 11547 (class 1259 OID 336687)
-- Name: menosf_ue_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menosf_ue_la_unidadespacial_idx ON interlis_ili2db3_ladm.menosf USING btree (ue_la_unidadespacial);


--
-- TOC entry 11548 (class 1259 OID 336688)
-- Name: menosf_ue_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menosf_ue_servidumbrepaso_idx ON interlis_ili2db3_ladm.menosf USING btree (ue_servidumbrepaso);


--
-- TOC entry 11549 (class 1259 OID 336689)
-- Name: menosf_ue_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menosf_ue_terreno_idx ON interlis_ili2db3_ladm.menosf USING btree (ue_terreno);


--
-- TOC entry 11550 (class 1259 OID 336690)
-- Name: menosf_ue_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX menosf_ue_unidadconstruccion_idx ON interlis_ili2db3_ladm.menosf USING btree (ue_unidadconstruccion);


--
-- TOC entry 11551 (class 1259 OID 336691)
-- Name: miembros_agrupacion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX miembros_agrupacion_idx ON interlis_ili2db3_ladm.miembros USING btree (agrupacion);


--
-- TOC entry 11552 (class 1259 OID 336692)
-- Name: miembros_interesados_col_interesado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX miembros_interesados_col_interesado_idx ON interlis_ili2db3_ladm.miembros USING btree (interesados_col_interesado);


--
-- TOC entry 11553 (class 1259 OID 336693)
-- Name: miembros_interesads_l_grpcn_ntrsdos_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX miembros_interesads_l_grpcn_ntrsdos_idx ON interlis_ili2db3_ladm.miembros USING btree (interesados_la_agrupacion_interesados);


--
-- TOC entry 11556 (class 1259 OID 336694)
-- Name: oid_extdireccion_direccion_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX oid_extdireccion_direccion_id_idx ON interlis_ili2db3_ladm.oid USING btree (extdireccion_direccion_id);


--
-- TOC entry 11557 (class 1259 OID 336695)
-- Name: oid_extinteresado_interesad_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX oid_extinteresado_interesad_id_idx ON interlis_ili2db3_ladm.oid USING btree (extinteresado_interesado_id);


--
-- TOC entry 11558 (class 1259 OID 336696)
-- Name: oid_la_nivel_n_id_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX oid_la_nivel_n_id_idx ON interlis_ili2db3_ladm.oid USING btree (la_nivel_n_id);


--
-- TOC entry 11561 (class 1259 OID 336697)
-- Name: om_observacion_col_fuenteespacial_medcnes_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX om_observacion_col_fuenteespacial_medcnes_idx ON interlis_ili2db3_ladm.om_observacion USING btree (col_fuenteespacial_mediciones);


--
-- TOC entry 11564 (class 1259 OID 336698)
-- Name: om_proceso_col_fuenteespacil_prcdmnto_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX om_proceso_col_fuenteespacil_prcdmnto_idx ON interlis_ili2db3_ladm.om_proceso USING btree (col_fuenteespacial_procedimiento);


--
-- TOC entry 11567 (class 1259 OID 336699)
-- Name: predio_copropiedad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX predio_copropiedad_idx ON interlis_ili2db3_ladm.predio USING btree (copropiedad);


--
-- TOC entry 11568 (class 1259 OID 336700)
-- Name: predio_nupre_key; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE UNIQUE INDEX predio_nupre_key ON interlis_ili2db3_ladm.predio USING btree (nupre);


--
-- TOC entry 11573 (class 1259 OID 336701)
-- Name: publicidad_baunit_la_baunit_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX publicidad_baunit_la_baunit_idx ON interlis_ili2db3_ladm.publicidad USING btree (baunit_la_baunit);


--
-- TOC entry 11574 (class 1259 OID 336702)
-- Name: publicidad_baunit_predio_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX publicidad_baunit_predio_idx ON interlis_ili2db3_ladm.publicidad USING btree (baunit_predio);


--
-- TOC entry 11575 (class 1259 OID 336703)
-- Name: publicidad_interesado_col_interesado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX publicidad_interesado_col_interesado_idx ON interlis_ili2db3_ladm.publicidad USING btree (interesado_col_interesado);


--
-- TOC entry 11576 (class 1259 OID 336704)
-- Name: publicidad_interesado_l_grpcn_ntrsdos_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX publicidad_interesado_l_grpcn_ntrsdos_idx ON interlis_ili2db3_ladm.publicidad USING btree (interesado_la_agrupacion_interesados);


--
-- TOC entry 11579 (class 1259 OID 336705)
-- Name: publicidadfuente_fuente_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX publicidadfuente_fuente_idx ON interlis_ili2db3_ladm.publicidadfuente USING btree (fuente);


--
-- TOC entry 11582 (class 1259 OID 336706)
-- Name: publicidadfuente_publicidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX publicidadfuente_publicidad_idx ON interlis_ili2db3_ladm.publicidadfuente USING btree (publicidad);


--
-- TOC entry 11583 (class 1259 OID 336707)
-- Name: puntoccl_ccl_la_cadenacaraslimite_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntoccl_ccl_la_cadenacaraslimite_idx ON interlis_ili2db3_ladm.puntoccl USING btree (ccl_la_cadenacaraslimite);


--
-- TOC entry 11584 (class 1259 OID 336708)
-- Name: puntoccl_ccl_lindero_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntoccl_ccl_lindero_idx ON interlis_ili2db3_ladm.puntoccl USING btree (ccl_lindero);


--
-- TOC entry 11587 (class 1259 OID 336709)
-- Name: puntoccl_punto_la_punto_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntoccl_punto_la_punto_idx ON interlis_ili2db3_ladm.puntoccl USING btree (punto_la_punto);


--
-- TOC entry 11588 (class 1259 OID 336710)
-- Name: puntoccl_punto_puntocontrol_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntoccl_punto_puntocontrol_idx ON interlis_ili2db3_ladm.puntoccl USING btree (punto_puntocontrol);


--
-- TOC entry 11589 (class 1259 OID 336711)
-- Name: puntoccl_punto_puntolevantamiento_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntoccl_punto_puntolevantamiento_idx ON interlis_ili2db3_ladm.puntoccl USING btree (punto_puntolevantamiento);


--
-- TOC entry 11590 (class 1259 OID 336712)
-- Name: puntoccl_punto_puntolindero_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntoccl_punto_puntolindero_idx ON interlis_ili2db3_ladm.puntoccl USING btree (punto_puntolindero);


--
-- TOC entry 11591 (class 1259 OID 336713)
-- Name: puntocl_cl_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntocl_cl_idx ON interlis_ili2db3_ladm.puntocl USING btree (cl);


--
-- TOC entry 11594 (class 1259 OID 336714)
-- Name: puntocl_punto_la_punto_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntocl_punto_la_punto_idx ON interlis_ili2db3_ladm.puntocl USING btree (punto_la_punto);


--
-- TOC entry 11595 (class 1259 OID 336715)
-- Name: puntocl_punto_puntocontrol_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntocl_punto_puntocontrol_idx ON interlis_ili2db3_ladm.puntocl USING btree (punto_puntocontrol);


--
-- TOC entry 11596 (class 1259 OID 336716)
-- Name: puntocl_punto_puntolevantamiento_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntocl_punto_puntolevantamiento_idx ON interlis_ili2db3_ladm.puntocl USING btree (punto_puntolevantamiento);


--
-- TOC entry 11597 (class 1259 OID 336717)
-- Name: puntocl_punto_puntolindero_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntocl_punto_puntolindero_idx ON interlis_ili2db3_ladm.puntocl USING btree (punto_puntolindero);


--
-- TOC entry 11598 (class 1259 OID 336718)
-- Name: puntocontrol_localizacion_original_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntocontrol_localizacion_original_idx ON interlis_ili2db3_ladm.puntocontrol USING gist (localizacion_original);


--
-- TOC entry 11601 (class 1259 OID 336719)
-- Name: puntocontrol_ue_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntocontrol_ue_construccion_idx ON interlis_ili2db3_ladm.puntocontrol USING btree (ue_construccion);


--
-- TOC entry 11602 (class 1259 OID 336720)
-- Name: puntocontrol_ue_la_espacijrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntocontrol_ue_la_espacijrdcndddfccion_idx ON interlis_ili2db3_ladm.puntocontrol USING btree (ue_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11603 (class 1259 OID 336721)
-- Name: puntocontrol_ue_la_espaciojrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntocontrol_ue_la_espaciojrdcrdsrvcios_idx ON interlis_ili2db3_ladm.puntocontrol USING btree (ue_la_espaciojuridicoredservicios);


--
-- TOC entry 11604 (class 1259 OID 336722)
-- Name: puntocontrol_ue_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntocontrol_ue_la_unidadespacial_idx ON interlis_ili2db3_ladm.puntocontrol USING btree (ue_la_unidadespacial);


--
-- TOC entry 11605 (class 1259 OID 336723)
-- Name: puntocontrol_ue_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntocontrol_ue_servidumbrepaso_idx ON interlis_ili2db3_ladm.puntocontrol USING btree (ue_servidumbrepaso);


--
-- TOC entry 11606 (class 1259 OID 336724)
-- Name: puntocontrol_ue_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntocontrol_ue_terreno_idx ON interlis_ili2db3_ladm.puntocontrol USING btree (ue_terreno);


--
-- TOC entry 11607 (class 1259 OID 336725)
-- Name: puntocontrol_ue_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntocontrol_ue_unidadconstruccion_idx ON interlis_ili2db3_ladm.puntocontrol USING btree (ue_unidadconstruccion);


--
-- TOC entry 11608 (class 1259 OID 336726)
-- Name: puntofuente_pfuente_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntofuente_pfuente_idx ON interlis_ili2db3_ladm.puntofuente USING btree (pfuente);


--
-- TOC entry 11611 (class 1259 OID 336727)
-- Name: puntofuente_punto_la_punto_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntofuente_punto_la_punto_idx ON interlis_ili2db3_ladm.puntofuente USING btree (punto_la_punto);


--
-- TOC entry 11612 (class 1259 OID 336728)
-- Name: puntofuente_punto_puntocontrol_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntofuente_punto_puntocontrol_idx ON interlis_ili2db3_ladm.puntofuente USING btree (punto_puntocontrol);


--
-- TOC entry 11613 (class 1259 OID 336729)
-- Name: puntofuente_punto_puntolevantamiento_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntofuente_punto_puntolevantamiento_idx ON interlis_ili2db3_ladm.puntofuente USING btree (punto_puntolevantamiento);


--
-- TOC entry 11614 (class 1259 OID 336730)
-- Name: puntofuente_punto_puntolindero_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntofuente_punto_puntolindero_idx ON interlis_ili2db3_ladm.puntofuente USING btree (punto_puntolindero);


--
-- TOC entry 11615 (class 1259 OID 336731)
-- Name: puntolevantamiento_localizacion_original_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolevantamiento_localizacion_original_idx ON interlis_ili2db3_ladm.puntolevantamiento USING gist (localizacion_original);


--
-- TOC entry 11618 (class 1259 OID 336732)
-- Name: puntolevantamiento_ue_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolevantamiento_ue_construccion_idx ON interlis_ili2db3_ladm.puntolevantamiento USING btree (ue_construccion);


--
-- TOC entry 11619 (class 1259 OID 336733)
-- Name: puntolevantamiento_ue_la_espacijrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolevantamiento_ue_la_espacijrdcndddfccion_idx ON interlis_ili2db3_ladm.puntolevantamiento USING btree (ue_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11620 (class 1259 OID 336734)
-- Name: puntolevantamiento_ue_la_espaciojrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolevantamiento_ue_la_espaciojrdcrdsrvcios_idx ON interlis_ili2db3_ladm.puntolevantamiento USING btree (ue_la_espaciojuridicoredservicios);


--
-- TOC entry 11621 (class 1259 OID 336735)
-- Name: puntolevantamiento_ue_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolevantamiento_ue_la_unidadespacial_idx ON interlis_ili2db3_ladm.puntolevantamiento USING btree (ue_la_unidadespacial);


--
-- TOC entry 11622 (class 1259 OID 336736)
-- Name: puntolevantamiento_ue_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolevantamiento_ue_servidumbrepaso_idx ON interlis_ili2db3_ladm.puntolevantamiento USING btree (ue_servidumbrepaso);


--
-- TOC entry 11623 (class 1259 OID 336737)
-- Name: puntolevantamiento_ue_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolevantamiento_ue_terreno_idx ON interlis_ili2db3_ladm.puntolevantamiento USING btree (ue_terreno);


--
-- TOC entry 11624 (class 1259 OID 336738)
-- Name: puntolevantamiento_ue_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolevantamiento_ue_unidadconstruccion_idx ON interlis_ili2db3_ladm.puntolevantamiento USING btree (ue_unidadconstruccion);


--
-- TOC entry 11625 (class 1259 OID 336739)
-- Name: puntolindero_localizacion_original_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolindero_localizacion_original_idx ON interlis_ili2db3_ladm.puntolindero USING gist (localizacion_original);


--
-- TOC entry 11628 (class 1259 OID 336740)
-- Name: puntolindero_ue_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolindero_ue_construccion_idx ON interlis_ili2db3_ladm.puntolindero USING btree (ue_construccion);


--
-- TOC entry 11629 (class 1259 OID 336741)
-- Name: puntolindero_ue_la_espacijrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolindero_ue_la_espacijrdcndddfccion_idx ON interlis_ili2db3_ladm.puntolindero USING btree (ue_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11630 (class 1259 OID 336742)
-- Name: puntolindero_ue_la_espaciojrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolindero_ue_la_espaciojrdcrdsrvcios_idx ON interlis_ili2db3_ladm.puntolindero USING btree (ue_la_espaciojuridicoredservicios);


--
-- TOC entry 11631 (class 1259 OID 336743)
-- Name: puntolindero_ue_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolindero_ue_la_unidadespacial_idx ON interlis_ili2db3_ladm.puntolindero USING btree (ue_la_unidadespacial);


--
-- TOC entry 11632 (class 1259 OID 336744)
-- Name: puntolindero_ue_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolindero_ue_servidumbrepaso_idx ON interlis_ili2db3_ladm.puntolindero USING btree (ue_servidumbrepaso);


--
-- TOC entry 11633 (class 1259 OID 336745)
-- Name: puntolindero_ue_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolindero_ue_terreno_idx ON interlis_ili2db3_ladm.puntolindero USING btree (ue_terreno);


--
-- TOC entry 11634 (class 1259 OID 336746)
-- Name: puntolindero_ue_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX puntolindero_ue_unidadconstruccion_idx ON interlis_ili2db3_ladm.puntolindero USING btree (ue_unidadconstruccion);


--
-- TOC entry 11637 (class 1259 OID 336747)
-- Name: relacionbaunit_unidad1_la_baunit_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionbaunit_unidad1_la_baunit_idx ON interlis_ili2db3_ladm.relacionbaunit USING btree (unidad1_la_baunit);


--
-- TOC entry 11638 (class 1259 OID 336748)
-- Name: relacionbaunit_unidad1_predio_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionbaunit_unidad1_predio_idx ON interlis_ili2db3_ladm.relacionbaunit USING btree (unidad1_predio);


--
-- TOC entry 11639 (class 1259 OID 336749)
-- Name: relacionbaunit_unidad2_la_baunit_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionbaunit_unidad2_la_baunit_idx ON interlis_ili2db3_ladm.relacionbaunit USING btree (unidad2_la_baunit);


--
-- TOC entry 11640 (class 1259 OID 336750)
-- Name: relacionbaunit_unidad2_predio_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionbaunit_unidad2_predio_idx ON interlis_ili2db3_ladm.relacionbaunit USING btree (unidad2_predio);


--
-- TOC entry 11643 (class 1259 OID 336751)
-- Name: relacionfuente_refuente_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionfuente_refuente_idx ON interlis_ili2db3_ladm.relacionfuente USING btree (refuente);


--
-- TOC entry 11644 (class 1259 OID 336752)
-- Name: relacionfuente_relacionrequeridabaunit_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionfuente_relacionrequeridabaunit_idx ON interlis_ili2db3_ladm.relacionfuente USING btree (relacionrequeridabaunit);


--
-- TOC entry 11647 (class 1259 OID 336753)
-- Name: relacionfuenteuespacial_relacionrequeridaue_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionfuenteuespacial_relacionrequeridaue_idx ON interlis_ili2db3_ladm.relacionfuenteuespacial USING btree (relacionrequeridaue);


--
-- TOC entry 11648 (class 1259 OID 336754)
-- Name: relacionfuenteuespacial_rfuente_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionfuenteuespacial_rfuente_idx ON interlis_ili2db3_ladm.relacionfuenteuespacial USING btree (rfuente);


--
-- TOC entry 11651 (class 1259 OID 336755)
-- Name: relacionue_rue1_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue1_construccion_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue1_construccion);


--
-- TOC entry 11652 (class 1259 OID 336756)
-- Name: relacionue_rue1_la_espacjrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue1_la_espacjrdcrdsrvcios_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue1_la_espaciojuridicoredservicios);


--
-- TOC entry 11653 (class 1259 OID 336757)
-- Name: relacionue_rue1_la_espcjrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue1_la_espcjrdcndddfccion_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue1_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11654 (class 1259 OID 336758)
-- Name: relacionue_rue1_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue1_la_unidadespacial_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue1_la_unidadespacial);


--
-- TOC entry 11655 (class 1259 OID 336759)
-- Name: relacionue_rue1_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue1_servidumbrepaso_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue1_servidumbrepaso);


--
-- TOC entry 11656 (class 1259 OID 336760)
-- Name: relacionue_rue1_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue1_terreno_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue1_terreno);


--
-- TOC entry 11657 (class 1259 OID 336761)
-- Name: relacionue_rue1_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue1_unidadconstruccion_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue1_unidadconstruccion);


--
-- TOC entry 11658 (class 1259 OID 336762)
-- Name: relacionue_rue2_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue2_construccion_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue2_construccion);


--
-- TOC entry 11659 (class 1259 OID 336763)
-- Name: relacionue_rue2_la_espacjrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue2_la_espacjrdcrdsrvcios_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue2_la_espaciojuridicoredservicios);


--
-- TOC entry 11660 (class 1259 OID 336764)
-- Name: relacionue_rue2_la_espcjrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue2_la_espcjrdcndddfccion_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue2_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11661 (class 1259 OID 336765)
-- Name: relacionue_rue2_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue2_la_unidadespacial_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue2_la_unidadespacial);


--
-- TOC entry 11662 (class 1259 OID 336766)
-- Name: relacionue_rue2_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue2_servidumbrepaso_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue2_servidumbrepaso);


--
-- TOC entry 11663 (class 1259 OID 336767)
-- Name: relacionue_rue2_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue2_terreno_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue2_terreno);


--
-- TOC entry 11664 (class 1259 OID 336768)
-- Name: relacionue_rue2_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX relacionue_rue2_unidadconstruccion_idx ON interlis_ili2db3_ladm.relacionue USING btree (rue2_unidadconstruccion);


--
-- TOC entry 11665 (class 1259 OID 336769)
-- Name: responsablefuente_cfuente_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX responsablefuente_cfuente_idx ON interlis_ili2db3_ladm.responsablefuente USING btree (cfuente);


--
-- TOC entry 11666 (class 1259 OID 336770)
-- Name: responsablefuente_notario_col_interesado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX responsablefuente_notario_col_interesado_idx ON interlis_ili2db3_ladm.responsablefuente USING btree (notario_col_interesado);


--
-- TOC entry 11667 (class 1259 OID 336771)
-- Name: responsablefuente_notario_la_agrupcn_ntrsdos_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX responsablefuente_notario_la_agrupcn_ntrsdos_idx ON interlis_ili2db3_ladm.responsablefuente USING btree (notario_la_agrupacion_interesados);


--
-- TOC entry 11672 (class 1259 OID 336772)
-- Name: rrrfuente_rfuente_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX rrrfuente_rfuente_idx ON interlis_ili2db3_ladm.rrrfuente USING btree (rfuente);


--
-- TOC entry 11673 (class 1259 OID 336773)
-- Name: rrrfuente_rrr_col_derecho_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX rrrfuente_rrr_col_derecho_idx ON interlis_ili2db3_ladm.rrrfuente USING btree (rrr_col_derecho);


--
-- TOC entry 11674 (class 1259 OID 336774)
-- Name: rrrfuente_rrr_col_hipoteca_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX rrrfuente_rrr_col_hipoteca_idx ON interlis_ili2db3_ladm.rrrfuente USING btree (rrr_col_hipoteca);


--
-- TOC entry 11675 (class 1259 OID 336775)
-- Name: rrrfuente_rrr_col_responsabilidad_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX rrrfuente_rrr_col_responsabilidad_idx ON interlis_ili2db3_ladm.rrrfuente USING btree (rrr_col_responsabilidad);


--
-- TOC entry 11676 (class 1259 OID 336776)
-- Name: rrrfuente_rrr_col_restriccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX rrrfuente_rrr_col_restriccion_idx ON interlis_ili2db3_ladm.rrrfuente USING btree (rrr_col_restriccion);


--
-- TOC entry 11677 (class 1259 OID 336777)
-- Name: servidumbrepaso_nivel_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX servidumbrepaso_nivel_idx ON interlis_ili2db3_ladm.servidumbrepaso USING btree (nivel);


--
-- TOC entry 11680 (class 1259 OID 336778)
-- Name: servidumbrepaso_poligono_creado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX servidumbrepaso_poligono_creado_idx ON interlis_ili2db3_ladm.servidumbrepaso USING gist (poligono_creado);


--
-- TOC entry 11681 (class 1259 OID 336779)
-- Name: servidumbrepaso_punto_referencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX servidumbrepaso_punto_referencia_idx ON interlis_ili2db3_ladm.servidumbrepaso USING gist (punto_referencia);


--
-- TOC entry 11682 (class 1259 OID 336780)
-- Name: servidumbrepaso_uej2_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX servidumbrepaso_uej2_construccion_idx ON interlis_ili2db3_ladm.servidumbrepaso USING btree (uej2_construccion);


--
-- TOC entry 11683 (class 1259 OID 336781)
-- Name: servidumbrepaso_uej2_la_espacjrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX servidumbrepaso_uej2_la_espacjrdcrdsrvcios_idx ON interlis_ili2db3_ladm.servidumbrepaso USING btree (uej2_la_espaciojuridicoredservicios);


--
-- TOC entry 11684 (class 1259 OID 336782)
-- Name: servidumbrepaso_uej2_la_espcjrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX servidumbrepaso_uej2_la_espcjrdcndddfccion_idx ON interlis_ili2db3_ladm.servidumbrepaso USING btree (uej2_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11685 (class 1259 OID 336783)
-- Name: servidumbrepaso_uej2_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX servidumbrepaso_uej2_la_unidadespacial_idx ON interlis_ili2db3_ladm.servidumbrepaso USING btree (uej2_la_unidadespacial);


--
-- TOC entry 11686 (class 1259 OID 336784)
-- Name: servidumbrepaso_uej2_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX servidumbrepaso_uej2_servidumbrepaso_idx ON interlis_ili2db3_ladm.servidumbrepaso USING btree (uej2_servidumbrepaso);


--
-- TOC entry 11687 (class 1259 OID 336785)
-- Name: servidumbrepaso_uej2_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX servidumbrepaso_uej2_terreno_idx ON interlis_ili2db3_ladm.servidumbrepaso USING btree (uej2_terreno);


--
-- TOC entry 11688 (class 1259 OID 336786)
-- Name: servidumbrepaso_uej2_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX servidumbrepaso_uej2_unidadconstruccion_idx ON interlis_ili2db3_ladm.servidumbrepaso USING btree (uej2_unidadconstruccion);


--
-- TOC entry 11691 (class 1259 OID 336787)
-- Name: t_ili2db_attrname_sqlname_owner_key; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE UNIQUE INDEX t_ili2db_attrname_sqlname_owner_key ON interlis_ili2db3_ladm.t_ili2db_attrname USING btree (sqlname, owner);


--
-- TOC entry 11692 (class 1259 OID 336788)
-- Name: t_ili2db_basket_dataset_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX t_ili2db_basket_dataset_idx ON interlis_ili2db3_ladm.t_ili2db_basket USING btree (dataset);


--
-- TOC entry 11697 (class 1259 OID 336789)
-- Name: t_ili2db_dataset_datasetname_key; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE UNIQUE INDEX t_ili2db_dataset_datasetname_key ON interlis_ili2db3_ladm.t_ili2db_dataset USING btree (datasetname);


--
-- TOC entry 11703 (class 1259 OID 336790)
-- Name: t_ili2db_import_basket_basket_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX t_ili2db_import_basket_basket_idx ON interlis_ili2db3_ladm.t_ili2db_import_basket USING btree (basket);


--
-- TOC entry 11704 (class 1259 OID 336791)
-- Name: t_ili2db_import_basket_import_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX t_ili2db_import_basket_import_idx ON interlis_ili2db3_ladm.t_ili2db_import_basket USING btree (import);


--
-- TOC entry 11700 (class 1259 OID 336792)
-- Name: t_ili2db_import_dataset_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX t_ili2db_import_dataset_idx ON interlis_ili2db3_ladm.t_ili2db_import USING btree (dataset);


--
-- TOC entry 11711 (class 1259 OID 336793)
-- Name: t_ili2db_model_iliversion_modelname_key; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE UNIQUE INDEX t_ili2db_model_iliversion_modelname_key ON interlis_ili2db3_ladm.t_ili2db_model USING btree (iliversion, modelname);


--
-- TOC entry 11716 (class 1259 OID 336794)
-- Name: terreno_nivel_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX terreno_nivel_idx ON interlis_ili2db3_ladm.terreno USING btree (nivel);


--
-- TOC entry 11719 (class 1259 OID 336795)
-- Name: terreno_poligono_creado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX terreno_poligono_creado_idx ON interlis_ili2db3_ladm.terreno USING gist (poligono_creado);


--
-- TOC entry 11720 (class 1259 OID 336796)
-- Name: terreno_punto_referencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX terreno_punto_referencia_idx ON interlis_ili2db3_ladm.terreno USING gist (punto_referencia);


--
-- TOC entry 11721 (class 1259 OID 336797)
-- Name: terreno_uej2_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX terreno_uej2_construccion_idx ON interlis_ili2db3_ladm.terreno USING btree (uej2_construccion);


--
-- TOC entry 11722 (class 1259 OID 336798)
-- Name: terreno_uej2_la_espacjrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX terreno_uej2_la_espacjrdcrdsrvcios_idx ON interlis_ili2db3_ladm.terreno USING btree (uej2_la_espaciojuridicoredservicios);


--
-- TOC entry 11723 (class 1259 OID 336799)
-- Name: terreno_uej2_la_espcjrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX terreno_uej2_la_espcjrdcndddfccion_idx ON interlis_ili2db3_ladm.terreno USING btree (uej2_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11724 (class 1259 OID 336800)
-- Name: terreno_uej2_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX terreno_uej2_la_unidadespacial_idx ON interlis_ili2db3_ladm.terreno USING btree (uej2_la_unidadespacial);


--
-- TOC entry 11725 (class 1259 OID 336801)
-- Name: terreno_uej2_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX terreno_uej2_servidumbrepaso_idx ON interlis_ili2db3_ladm.terreno USING btree (uej2_servidumbrepaso);


--
-- TOC entry 11726 (class 1259 OID 336802)
-- Name: terreno_uej2_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX terreno_uej2_terreno_idx ON interlis_ili2db3_ladm.terreno USING btree (uej2_terreno);


--
-- TOC entry 11727 (class 1259 OID 336803)
-- Name: terreno_uej2_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX terreno_uej2_unidadconstruccion_idx ON interlis_ili2db3_ladm.terreno USING btree (uej2_unidadconstruccion);


--
-- TOC entry 11730 (class 1259 OID 336804)
-- Name: topografofuente_sfuente_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX topografofuente_sfuente_idx ON interlis_ili2db3_ladm.topografofuente USING btree (sfuente);


--
-- TOC entry 11731 (class 1259 OID 336805)
-- Name: topografofuente_topografo_col_interesado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX topografofuente_topografo_col_interesado_idx ON interlis_ili2db3_ladm.topografofuente USING btree (topografo_col_interesado);


--
-- TOC entry 11732 (class 1259 OID 336806)
-- Name: topografofuente_topografo_la_grpcn_ntrsdos_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX topografofuente_topografo_la_grpcn_ntrsdos_idx ON interlis_ili2db3_ladm.topografofuente USING btree (topografo_la_agrupacion_interesados);


--
-- TOC entry 11733 (class 1259 OID 336807)
-- Name: uebaunit_baunit_la_baunit_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uebaunit_baunit_la_baunit_idx ON interlis_ili2db3_ladm.uebaunit USING btree (baunit_la_baunit);


--
-- TOC entry 11734 (class 1259 OID 336808)
-- Name: uebaunit_baunit_predio_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uebaunit_baunit_predio_idx ON interlis_ili2db3_ladm.uebaunit USING btree (baunit_predio);


--
-- TOC entry 11737 (class 1259 OID 336809)
-- Name: uebaunit_ue_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uebaunit_ue_construccion_idx ON interlis_ili2db3_ladm.uebaunit USING btree (ue_construccion);


--
-- TOC entry 11738 (class 1259 OID 336810)
-- Name: uebaunit_ue_la_espacijrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uebaunit_ue_la_espacijrdcndddfccion_idx ON interlis_ili2db3_ladm.uebaunit USING btree (ue_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11739 (class 1259 OID 336811)
-- Name: uebaunit_ue_la_espaciojrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uebaunit_ue_la_espaciojrdcrdsrvcios_idx ON interlis_ili2db3_ladm.uebaunit USING btree (ue_la_espaciojuridicoredservicios);


--
-- TOC entry 11740 (class 1259 OID 336812)
-- Name: uebaunit_ue_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uebaunit_ue_la_unidadespacial_idx ON interlis_ili2db3_ladm.uebaunit USING btree (ue_la_unidadespacial);


--
-- TOC entry 11741 (class 1259 OID 336813)
-- Name: uebaunit_ue_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uebaunit_ue_servidumbrepaso_idx ON interlis_ili2db3_ladm.uebaunit USING btree (ue_servidumbrepaso);


--
-- TOC entry 11742 (class 1259 OID 336814)
-- Name: uebaunit_ue_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uebaunit_ue_terreno_idx ON interlis_ili2db3_ladm.uebaunit USING btree (ue_terreno);


--
-- TOC entry 11743 (class 1259 OID 336815)
-- Name: uebaunit_ue_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uebaunit_ue_unidadconstruccion_idx ON interlis_ili2db3_ladm.uebaunit USING btree (ue_unidadconstruccion);


--
-- TOC entry 11744 (class 1259 OID 336816)
-- Name: uefuente_pfuente_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uefuente_pfuente_idx ON interlis_ili2db3_ladm.uefuente USING btree (pfuente);


--
-- TOC entry 11747 (class 1259 OID 336817)
-- Name: uefuente_ue_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uefuente_ue_construccion_idx ON interlis_ili2db3_ladm.uefuente USING btree (ue_construccion);


--
-- TOC entry 11748 (class 1259 OID 336818)
-- Name: uefuente_ue_la_espacijrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uefuente_ue_la_espacijrdcndddfccion_idx ON interlis_ili2db3_ladm.uefuente USING btree (ue_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11749 (class 1259 OID 336819)
-- Name: uefuente_ue_la_espaciojrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uefuente_ue_la_espaciojrdcrdsrvcios_idx ON interlis_ili2db3_ladm.uefuente USING btree (ue_la_espaciojuridicoredservicios);


--
-- TOC entry 11750 (class 1259 OID 336820)
-- Name: uefuente_ue_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uefuente_ue_la_unidadespacial_idx ON interlis_ili2db3_ladm.uefuente USING btree (ue_la_unidadespacial);


--
-- TOC entry 11751 (class 1259 OID 336821)
-- Name: uefuente_ue_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uefuente_ue_servidumbrepaso_idx ON interlis_ili2db3_ladm.uefuente USING btree (ue_servidumbrepaso);


--
-- TOC entry 11752 (class 1259 OID 336822)
-- Name: uefuente_ue_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uefuente_ue_terreno_idx ON interlis_ili2db3_ladm.uefuente USING btree (ue_terreno);


--
-- TOC entry 11753 (class 1259 OID 336823)
-- Name: uefuente_ue_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX uefuente_ue_unidadconstruccion_idx ON interlis_ili2db3_ladm.uefuente USING btree (ue_unidadconstruccion);


--
-- TOC entry 11754 (class 1259 OID 336824)
-- Name: ueuegrupo_parte_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ueuegrupo_parte_construccion_idx ON interlis_ili2db3_ladm.ueuegrupo USING btree (parte_construccion);


--
-- TOC entry 11755 (class 1259 OID 336825)
-- Name: ueuegrupo_parte_la_espcjrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ueuegrupo_parte_la_espcjrdcrdsrvcios_idx ON interlis_ili2db3_ladm.ueuegrupo USING btree (parte_la_espaciojuridicoredservicios);


--
-- TOC entry 11756 (class 1259 OID 336826)
-- Name: ueuegrupo_parte_la_spcjrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ueuegrupo_parte_la_spcjrdcndddfccion_idx ON interlis_ili2db3_ladm.ueuegrupo USING btree (parte_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11757 (class 1259 OID 336827)
-- Name: ueuegrupo_parte_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ueuegrupo_parte_la_unidadespacial_idx ON interlis_ili2db3_ladm.ueuegrupo USING btree (parte_la_unidadespacial);


--
-- TOC entry 11758 (class 1259 OID 336828)
-- Name: ueuegrupo_parte_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ueuegrupo_parte_servidumbrepaso_idx ON interlis_ili2db3_ladm.ueuegrupo USING btree (parte_servidumbrepaso);


--
-- TOC entry 11759 (class 1259 OID 336829)
-- Name: ueuegrupo_parte_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ueuegrupo_parte_terreno_idx ON interlis_ili2db3_ladm.ueuegrupo USING btree (parte_terreno);


--
-- TOC entry 11760 (class 1259 OID 336830)
-- Name: ueuegrupo_parte_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ueuegrupo_parte_unidadconstruccion_idx ON interlis_ili2db3_ladm.ueuegrupo USING btree (parte_unidadconstruccion);


--
-- TOC entry 11763 (class 1259 OID 336831)
-- Name: ueuegrupo_todo_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX ueuegrupo_todo_idx ON interlis_ili2db3_ladm.ueuegrupo USING btree (todo);


--
-- TOC entry 11764 (class 1259 OID 336832)
-- Name: unidadconstruccion_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadconstruccion_construccion_idx ON interlis_ili2db3_ladm.unidadconstruccion USING btree (construccion);


--
-- TOC entry 11765 (class 1259 OID 336833)
-- Name: unidadconstruccion_nivel_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadconstruccion_nivel_idx ON interlis_ili2db3_ladm.unidadconstruccion USING btree (nivel);


--
-- TOC entry 11768 (class 1259 OID 336834)
-- Name: unidadconstruccion_poligono_creado_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadconstruccion_poligono_creado_idx ON interlis_ili2db3_ladm.unidadconstruccion USING gist (poligono_creado);


--
-- TOC entry 11769 (class 1259 OID 336835)
-- Name: unidadconstruccion_punto_referencia_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadconstruccion_punto_referencia_idx ON interlis_ili2db3_ladm.unidadconstruccion USING gist (punto_referencia);


--
-- TOC entry 11770 (class 1259 OID 336836)
-- Name: unidadconstruccion_uej2_construccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadconstruccion_uej2_construccion_idx ON interlis_ili2db3_ladm.unidadconstruccion USING btree (uej2_construccion);


--
-- TOC entry 11771 (class 1259 OID 336837)
-- Name: unidadconstruccion_uej2_la_espacjrdcrdsrvcios_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadconstruccion_uej2_la_espacjrdcrdsrvcios_idx ON interlis_ili2db3_ladm.unidadconstruccion USING btree (uej2_la_espaciojuridicoredservicios);


--
-- TOC entry 11772 (class 1259 OID 336838)
-- Name: unidadconstruccion_uej2_la_espcjrdcndddfccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadconstruccion_uej2_la_espcjrdcndddfccion_idx ON interlis_ili2db3_ladm.unidadconstruccion USING btree (uej2_la_espaciojuridicounidadedificacion);


--
-- TOC entry 11773 (class 1259 OID 336839)
-- Name: unidadconstruccion_uej2_la_unidadespacial_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadconstruccion_uej2_la_unidadespacial_idx ON interlis_ili2db3_ladm.unidadconstruccion USING btree (uej2_la_unidadespacial);


--
-- TOC entry 11774 (class 1259 OID 336840)
-- Name: unidadconstruccion_uej2_servidumbrepaso_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadconstruccion_uej2_servidumbrepaso_idx ON interlis_ili2db3_ladm.unidadconstruccion USING btree (uej2_servidumbrepaso);


--
-- TOC entry 11775 (class 1259 OID 336841)
-- Name: unidadconstruccion_uej2_terreno_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadconstruccion_uej2_terreno_idx ON interlis_ili2db3_ladm.unidadconstruccion USING btree (uej2_terreno);


--
-- TOC entry 11776 (class 1259 OID 336842)
-- Name: unidadconstruccion_uej2_unidadconstruccion_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadconstruccion_uej2_unidadconstruccion_idx ON interlis_ili2db3_ladm.unidadconstruccion USING btree (uej2_unidadconstruccion);


--
-- TOC entry 11779 (class 1259 OID 336843)
-- Name: unidadfuente_ufuente_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadfuente_ufuente_idx ON interlis_ili2db3_ladm.unidadfuente USING btree (ufuente);


--
-- TOC entry 11780 (class 1259 OID 336844)
-- Name: unidadfuente_unidad_la_baunit_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadfuente_unidad_la_baunit_idx ON interlis_ili2db3_ladm.unidadfuente USING btree (unidad_la_baunit);


--
-- TOC entry 11781 (class 1259 OID 336845)
-- Name: unidadfuente_unidad_predio_idx; Type: INDEX; Schema: interlis_ili2db3_ladm; Owner: postgres
--

CREATE INDEX unidadfuente_unidad_predio_idx ON interlis_ili2db3_ladm.unidadfuente USING btree (unidad_predio);


--
-- TOC entry 11782 (class 2606 OID 336846)
-- Name: baunitcomointeresado baunitcomointeresado_interesado_col_interesado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.baunitcomointeresado
    ADD CONSTRAINT baunitcomointeresado_interesado_col_interesado_fkey FOREIGN KEY (interesado_col_interesado) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11783 (class 2606 OID 336851)
-- Name: baunitcomointeresado baunitcomointeresado_interesado_l_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.baunitcomointeresado
    ADD CONSTRAINT baunitcomointeresado_interesado_l_grpcn_ntrsdos_fkey FOREIGN KEY (interesado_la_agrupacion_interesados) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11784 (class 2606 OID 336856)
-- Name: baunitcomointeresado baunitcomointeresado_unidad_la_baunit_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.baunitcomointeresado
    ADD CONSTRAINT baunitcomointeresado_unidad_la_baunit_fkey FOREIGN KEY (unidad_la_baunit) REFERENCES interlis_ili2db3_ladm.la_baunit(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11785 (class 2606 OID 336861)
-- Name: baunitcomointeresado baunitcomointeresado_unidad_predio_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.baunitcomointeresado
    ADD CONSTRAINT baunitcomointeresado_unidad_predio_fkey FOREIGN KEY (unidad_predio) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11786 (class 2606 OID 336866)
-- Name: baunitfuente baunitfuente_bfuente_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.baunitfuente
    ADD CONSTRAINT baunitfuente_bfuente_fkey FOREIGN KEY (bfuente) REFERENCES interlis_ili2db3_ladm.col_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11787 (class 2606 OID 336871)
-- Name: baunitfuente baunitfuente_unidad_la_baunit_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.baunitfuente
    ADD CONSTRAINT baunitfuente_unidad_la_baunit_fkey FOREIGN KEY (unidad_la_baunit) REFERENCES interlis_ili2db3_ladm.la_baunit(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11788 (class 2606 OID 336876)
-- Name: baunitfuente baunitfuente_unidad_predio_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.baunitfuente
    ADD CONSTRAINT baunitfuente_unidad_predio_fkey FOREIGN KEY (unidad_predio) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11789 (class 2606 OID 336881)
-- Name: cc_metodooperacion cc_metodooperacion_la_transformcn_trnsfrmcion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.cc_metodooperacion
    ADD CONSTRAINT cc_metodooperacion_la_transformcn_trnsfrmcion_fkey FOREIGN KEY (la_transformacion_transformacion) REFERENCES interlis_ili2db3_ladm.la_transformacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11790 (class 2606 OID 336886)
-- Name: cclfuente cclfuente_ccl_la_cadenacaraslimite_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.cclfuente
    ADD CONSTRAINT cclfuente_ccl_la_cadenacaraslimite_fkey FOREIGN KEY (ccl_la_cadenacaraslimite) REFERENCES interlis_ili2db3_ladm.la_cadenacaraslimite(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11791 (class 2606 OID 336891)
-- Name: cclfuente cclfuente_ccl_lindero_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.cclfuente
    ADD CONSTRAINT cclfuente_ccl_lindero_fkey FOREIGN KEY (ccl_lindero) REFERENCES interlis_ili2db3_ladm.lindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11792 (class 2606 OID 336896)
-- Name: cclfuente cclfuente_lfuente_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.cclfuente
    ADD CONSTRAINT cclfuente_lfuente_fkey FOREIGN KEY (lfuente) REFERENCES interlis_ili2db3_ladm.col_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11793 (class 2606 OID 336901)
-- Name: ci_contacto ci_contacto_ci_prtrspnsblnfrmcn_cntcto_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_contacto
    ADD CONSTRAINT ci_contacto_ci_prtrspnsblnfrmcn_cntcto_fkey FOREIGN KEY (ci_parteresponsable_informacion_contacto) REFERENCES interlis_ili2db3_ladm.ci_parteresponsable(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11794 (class 2606 OID 336906)
-- Name: ci_parteresponsable ci_parteresponsable_col_derecho_procedencia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_col_derecho_procedencia_fkey FOREIGN KEY (col_derecho_procedencia) REFERENCES interlis_ili2db3_ladm.col_derecho(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11795 (class 2606 OID 336911)
-- Name: ci_parteresponsable ci_parteresponsable_col_fuentdmnstrtv_prcdncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_col_fuentdmnstrtv_prcdncia_fkey FOREIGN KEY (col_fuenteadminstrtiva_procedencia) REFERENCES interlis_ili2db3_ladm.col_fuenteadministrativa(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11796 (class 2606 OID 336916)
-- Name: ci_parteresponsable ci_parteresponsable_col_fuenteespacil_prcdncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_col_fuenteespacil_prcdncia_fkey FOREIGN KEY (col_fuenteespacial_procedencia) REFERENCES interlis_ili2db3_ladm.col_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11797 (class 2606 OID 336921)
-- Name: ci_parteresponsable ci_parteresponsable_col_hipoteca_procedencia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_col_hipoteca_procedencia_fkey FOREIGN KEY (col_hipoteca_procedencia) REFERENCES interlis_ili2db3_ladm.col_hipoteca(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11798 (class 2606 OID 336926)
-- Name: ci_parteresponsable ci_parteresponsable_col_interesado_procedencia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_col_interesado_procedencia_fkey FOREIGN KEY (col_interesado_procedencia) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11799 (class 2606 OID 336931)
-- Name: ci_parteresponsable ci_parteresponsable_col_responsabildd_prcdncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_col_responsabildd_prcdncia_fkey FOREIGN KEY (col_responsabilidad_procedencia) REFERENCES interlis_ili2db3_ladm.col_responsabilidad(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11800 (class 2606 OID 336936)
-- Name: ci_parteresponsable ci_parteresponsable_col_restriccion_procedncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_col_restriccion_procedncia_fkey FOREIGN KEY (col_restriccion_procedencia) REFERENCES interlis_ili2db3_ladm.col_restriccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11801 (class 2606 OID 336941)
-- Name: ci_parteresponsable ci_parteresponsable_construccion_procedencia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_construccion_procedencia_fkey FOREIGN KEY (construccion_procedencia) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11802 (class 2606 OID 336946)
-- Name: ci_parteresponsable ci_parteresponsable_la_agrupcn_ntrsds_prcdncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_la_agrupcn_ntrsds_prcdncia_fkey FOREIGN KEY (la_agrupacion_intrsdos_procedencia) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11803 (class 2606 OID 336951)
-- Name: ci_parteresponsable ci_parteresponsable_la_baunit_procedencia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_la_baunit_procedencia_fkey FOREIGN KEY (la_baunit_procedencia) REFERENCES interlis_ili2db3_ladm.la_baunit(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11804 (class 2606 OID 336956)
-- Name: ci_parteresponsable ci_parteresponsable_la_cadenacaraslmt_prcdncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_la_cadenacaraslmt_prcdncia_fkey FOREIGN KEY (la_cadenacaraslimite_procedencia) REFERENCES interlis_ili2db3_ladm.la_cadenacaraslimite(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11805 (class 2606 OID 336961)
-- Name: ci_parteresponsable ci_parteresponsable_la_caraslindero_procedncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_la_caraslindero_procedncia_fkey FOREIGN KEY (la_caraslindero_procedencia) REFERENCES interlis_ili2db3_ladm.la_caraslindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11806 (class 2606 OID 336966)
-- Name: ci_parteresponsable ci_parteresponsable_la_grpcnnddsspcls_prcdncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_la_grpcnnddsspcls_prcdncia_fkey FOREIGN KEY (la_agrupacinnddsspcles_procedencia) REFERENCES interlis_ili2db3_ladm.la_agrupacionunidadesespaciales(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11807 (class 2606 OID 336971)
-- Name: ci_parteresponsable ci_parteresponsable_la_nivel_procedencia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_la_nivel_procedencia_fkey FOREIGN KEY (la_nivel_procedencia) REFERENCES interlis_ili2db3_ladm.la_nivel(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11808 (class 2606 OID 336976)
-- Name: ci_parteresponsable ci_parteresponsable_la_punto_procedencia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_la_punto_procedencia_fkey FOREIGN KEY (la_punto_procedencia) REFERENCES interlis_ili2db3_ladm.la_punto(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11809 (class 2606 OID 336981)
-- Name: ci_parteresponsable ci_parteresponsable_la_relacnncsrbnts_prcdncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_la_relacnncsrbnts_prcdncia_fkey FOREIGN KEY (la_relacionnecesrbnits_procedencia) REFERENCES interlis_ili2db3_ladm.la_relacionnecesariabaunits(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11810 (class 2606 OID 336986)
-- Name: ci_parteresponsable ci_parteresponsable_la_rlcnncsrndpcls_prcdncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_la_rlcnncsrndpcls_prcdncia_fkey FOREIGN KEY (la_relcnncsrnddsspcles_procedencia) REFERENCES interlis_ili2db3_ladm.la_relacionnecesariaunidadesespaciales(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11811 (class 2606 OID 336991)
-- Name: ci_parteresponsable ci_parteresponsable_la_spcjrdcnddfccn_prcdncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_la_spcjrdcnddfccn_prcdncia_fkey FOREIGN KEY (la_espacjrdcndddfccion_procedencia) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11812 (class 2606 OID 336996)
-- Name: ci_parteresponsable ci_parteresponsable_la_spcjrdcrdsrvcs_prcdncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_la_spcjrdcrdsrvcs_prcdncia_fkey FOREIGN KEY (la_espacijrdcrdsrvcios_procedencia) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11813 (class 2606 OID 337001)
-- Name: ci_parteresponsable ci_parteresponsable_la_unidadespacial_prcdncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_la_unidadespacial_prcdncia_fkey FOREIGN KEY (la_unidadespacial_procedencia) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11814 (class 2606 OID 337006)
-- Name: ci_parteresponsable ci_parteresponsable_lindero_procedencia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_lindero_procedencia_fkey FOREIGN KEY (lindero_procedencia) REFERENCES interlis_ili2db3_ladm.lindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11815 (class 2606 OID 337011)
-- Name: ci_parteresponsable ci_parteresponsable_predio_procedencia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_predio_procedencia_fkey FOREIGN KEY (predio_procedencia) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11816 (class 2606 OID 337016)
-- Name: ci_parteresponsable ci_parteresponsable_publicidad_procedencia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_publicidad_procedencia_fkey FOREIGN KEY (publicidad_procedencia) REFERENCES interlis_ili2db3_ladm.publicidad(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11817 (class 2606 OID 337021)
-- Name: ci_parteresponsable ci_parteresponsable_puntocontrol_procedencia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_puntocontrol_procedencia_fkey FOREIGN KEY (puntocontrol_procedencia) REFERENCES interlis_ili2db3_ladm.puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11818 (class 2606 OID 337026)
-- Name: ci_parteresponsable ci_parteresponsable_puntolevantamient_prcdncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_puntolevantamient_prcdncia_fkey FOREIGN KEY (puntolevantamiento_procedencia) REFERENCES interlis_ili2db3_ladm.puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11819 (class 2606 OID 337031)
-- Name: ci_parteresponsable ci_parteresponsable_puntolindero_procedencia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_puntolindero_procedencia_fkey FOREIGN KEY (puntolindero_procedencia) REFERENCES interlis_ili2db3_ladm.puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11820 (class 2606 OID 337036)
-- Name: ci_parteresponsable ci_parteresponsable_servidumbrepaso_procedncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_servidumbrepaso_procedncia_fkey FOREIGN KEY (servidumbrepaso_procedencia) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11821 (class 2606 OID 337041)
-- Name: ci_parteresponsable ci_parteresponsable_terreno_procedencia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_terreno_procedencia_fkey FOREIGN KEY (terreno_procedencia) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11822 (class 2606 OID 337046)
-- Name: ci_parteresponsable ci_parteresponsable_unidadconstruccin_prcdncia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ci_parteresponsable
    ADD CONSTRAINT ci_parteresponsable_unidadconstruccin_prcdncia_fkey FOREIGN KEY (unidadconstruccion_procedencia) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11823 (class 2606 OID 337051)
-- Name: clfuente clfuente_cfuente_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.clfuente
    ADD CONSTRAINT clfuente_cfuente_fkey FOREIGN KEY (cfuente) REFERENCES interlis_ili2db3_ladm.col_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11824 (class 2606 OID 337056)
-- Name: clfuente clfuente_cl_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.clfuente
    ADD CONSTRAINT clfuente_cl_fkey FOREIGN KEY (cl) REFERENCES interlis_ili2db3_ladm.la_caraslindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11825 (class 2606 OID 337061)
-- Name: col_afectacion_terreno_afectacion col_afectacin_trrn_fctcion_terreno_afectacion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_afectacion_terreno_afectacion
    ADD CONSTRAINT col_afectacin_trrn_fctcion_terreno_afectacion_fkey FOREIGN KEY (terreno_afectacion) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11826 (class 2606 OID 337066)
-- Name: col_areavalor col_areavalor_construccion_area_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_areavalor
    ADD CONSTRAINT col_areavalor_construccion_area_fkey FOREIGN KEY (construccion_area) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11827 (class 2606 OID 337071)
-- Name: col_areavalor col_areavalor_la_espacijrdcrdsrvcios_rea_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_areavalor
    ADD CONSTRAINT col_areavalor_la_espacijrdcrdsrvcios_rea_fkey FOREIGN KEY (la_espacijrdcrdsrvcios_area) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11828 (class 2606 OID 337076)
-- Name: col_areavalor col_areavalor_la_espacjrdcndddfccion_rea_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_areavalor
    ADD CONSTRAINT col_areavalor_la_espacjrdcndddfccion_rea_fkey FOREIGN KEY (la_espacjrdcndddfccion_area) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11829 (class 2606 OID 337081)
-- Name: col_areavalor col_areavalor_la_unidadespacial_area_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_areavalor
    ADD CONSTRAINT col_areavalor_la_unidadespacial_area_fkey FOREIGN KEY (la_unidadespacial_area) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11830 (class 2606 OID 337086)
-- Name: col_areavalor col_areavalor_servidumbrepaso_area_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_areavalor
    ADD CONSTRAINT col_areavalor_servidumbrepaso_area_fkey FOREIGN KEY (servidumbrepaso_area) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11831 (class 2606 OID 337091)
-- Name: col_areavalor col_areavalor_terreno_area_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_areavalor
    ADD CONSTRAINT col_areavalor_terreno_area_fkey FOREIGN KEY (terreno_area) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11832 (class 2606 OID 337096)
-- Name: col_areavalor col_areavalor_unidadconstruccion_area_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_areavalor
    ADD CONSTRAINT col_areavalor_unidadconstruccion_area_fkey FOREIGN KEY (unidadconstruccion_area) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11833 (class 2606 OID 337101)
-- Name: col_bosqueareasemi_terreno_bosque_area_seminaturale col_bsqrsm_trsq_r_smntrale_terreno_bosque_ar_smntrale_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_bosqueareasemi_terreno_bosque_area_seminaturale
    ADD CONSTRAINT col_bsqrsm_trsq_r_smntrale_terreno_bosque_ar_smntrale_fkey FOREIGN KEY (terreno_bosque_area_seminaturale) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11834 (class 2606 OID 337106)
-- Name: col_cuerpoagua_terreno_evidencia_cuerpo_agua col_crpg_trrn_vdnc_crp_gua_terreno_evidencia_curp_gua_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_cuerpoagua_terreno_evidencia_cuerpo_agua
    ADD CONSTRAINT col_crpg_trrn_vdnc_crp_gua_terreno_evidencia_curp_gua_fkey FOREIGN KEY (terreno_evidencia_cuerpo_agua) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11835 (class 2606 OID 337111)
-- Name: col_derecho col_derecho_interesado_col_interesado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_derecho
    ADD CONSTRAINT col_derecho_interesado_col_interesado_fkey FOREIGN KEY (interesado_col_interesado) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11836 (class 2606 OID 337116)
-- Name: col_derecho col_derecho_interesado_l_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_derecho
    ADD CONSTRAINT col_derecho_interesado_l_grpcn_ntrsdos_fkey FOREIGN KEY (interesado_la_agrupacion_interesados) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11837 (class 2606 OID 337121)
-- Name: col_derecho col_derecho_unidad_la_baunit_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_derecho
    ADD CONSTRAINT col_derecho_unidad_la_baunit_fkey FOREIGN KEY (unidad_la_baunit) REFERENCES interlis_ili2db3_ladm.la_baunit(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11838 (class 2606 OID 337126)
-- Name: col_derecho col_derecho_unidad_predio_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_derecho
    ADD CONSTRAINT col_derecho_unidad_predio_fkey FOREIGN KEY (unidad_predio) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11840 (class 2606 OID 337131)
-- Name: col_hipoteca col_hipoteca_interesado_col_interesado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_hipoteca
    ADD CONSTRAINT col_hipoteca_interesado_col_interesado_fkey FOREIGN KEY (interesado_col_interesado) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11841 (class 2606 OID 337136)
-- Name: col_hipoteca col_hipoteca_interesado_l_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_hipoteca
    ADD CONSTRAINT col_hipoteca_interesado_l_grpcn_ntrsdos_fkey FOREIGN KEY (interesado_la_agrupacion_interesados) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11842 (class 2606 OID 337141)
-- Name: col_hipoteca col_hipoteca_unidad_la_baunit_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_hipoteca
    ADD CONSTRAINT col_hipoteca_unidad_la_baunit_fkey FOREIGN KEY (unidad_la_baunit) REFERENCES interlis_ili2db3_ladm.la_baunit(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11843 (class 2606 OID 337146)
-- Name: col_hipoteca col_hipoteca_unidad_predio_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_hipoteca
    ADD CONSTRAINT col_hipoteca_unidad_predio_fkey FOREIGN KEY (unidad_predio) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11844 (class 2606 OID 337151)
-- Name: col_responsabilidad col_responsabilidad_interesado_col_interesado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_responsabilidad
    ADD CONSTRAINT col_responsabilidad_interesado_col_interesado_fkey FOREIGN KEY (interesado_col_interesado) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11845 (class 2606 OID 337156)
-- Name: col_responsabilidad col_responsabilidad_interesado_l_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_responsabilidad
    ADD CONSTRAINT col_responsabilidad_interesado_l_grpcn_ntrsdos_fkey FOREIGN KEY (interesado_la_agrupacion_interesados) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11846 (class 2606 OID 337161)
-- Name: col_responsabilidad col_responsabilidad_unidad_la_baunit_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_responsabilidad
    ADD CONSTRAINT col_responsabilidad_unidad_la_baunit_fkey FOREIGN KEY (unidad_la_baunit) REFERENCES interlis_ili2db3_ladm.la_baunit(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11847 (class 2606 OID 337166)
-- Name: col_responsabilidad col_responsabilidad_unidad_predio_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_responsabilidad
    ADD CONSTRAINT col_responsabilidad_unidad_predio_fkey FOREIGN KEY (unidad_predio) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11848 (class 2606 OID 337171)
-- Name: col_restriccion col_restriccion_interesado_col_interesado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_restriccion
    ADD CONSTRAINT col_restriccion_interesado_col_interesado_fkey FOREIGN KEY (interesado_col_interesado) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11849 (class 2606 OID 337176)
-- Name: col_restriccion col_restriccion_interesado_l_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_restriccion
    ADD CONSTRAINT col_restriccion_interesado_l_grpcn_ntrsdos_fkey FOREIGN KEY (interesado_la_agrupacion_interesados) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11850 (class 2606 OID 337181)
-- Name: col_restriccion col_restriccion_unidad_la_baunit_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_restriccion
    ADD CONSTRAINT col_restriccion_unidad_la_baunit_fkey FOREIGN KEY (unidad_la_baunit) REFERENCES interlis_ili2db3_ladm.la_baunit(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11851 (class 2606 OID 337186)
-- Name: col_restriccion col_restriccion_unidad_predio_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_restriccion
    ADD CONSTRAINT col_restriccion_unidad_predio_fkey FOREIGN KEY (unidad_predio) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11852 (class 2606 OID 337191)
-- Name: col_servidumbretipo_terreno_servidumbre col_srvdmbrtptrrn_srvdmbre_terreno_servidumbre_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_servidumbretipo_terreno_servidumbre
    ADD CONSTRAINT col_srvdmbrtptrrn_srvdmbre_terreno_servidumbre_fkey FOREIGN KEY (terreno_servidumbre) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11853 (class 2606 OID 337196)
-- Name: col_territorioagricola_terreno_territorio_agricola col_trrtrgrcl_trrtr_grcola_terreno_territorio_agrcola_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_territorioagricola_terreno_territorio_agricola
    ADD CONSTRAINT col_trrtrgrcl_trrtr_grcola_terreno_territorio_agrcola_fkey FOREIGN KEY (terreno_territorio_agricola) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11839 (class 2606 OID 337201)
-- Name: col_explotaciontipo_terreno_explotacion col_xpltcntp_trrn_xpltcion_terreno_explotacion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.col_explotaciontipo_terreno_explotacion
    ADD CONSTRAINT col_xpltcntp_trrn_xpltcion_terreno_explotacion_fkey FOREIGN KEY (terreno_explotacion) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11854 (class 2606 OID 337206)
-- Name: construccion construccion_nivel_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.construccion
    ADD CONSTRAINT construccion_nivel_fkey FOREIGN KEY (nivel) REFERENCES interlis_ili2db3_ladm.la_nivel(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11855 (class 2606 OID 337211)
-- Name: construccion construccion_uej2_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.construccion
    ADD CONSTRAINT construccion_uej2_construccion_fkey FOREIGN KEY (uej2_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11856 (class 2606 OID 337216)
-- Name: construccion construccion_uej2_la_espacjrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.construccion
    ADD CONSTRAINT construccion_uej2_la_espacjrdcrdsrvcios_fkey FOREIGN KEY (uej2_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11857 (class 2606 OID 337221)
-- Name: construccion construccion_uej2_la_espcjrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.construccion
    ADD CONSTRAINT construccion_uej2_la_espcjrdcndddfccion_fkey FOREIGN KEY (uej2_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11858 (class 2606 OID 337226)
-- Name: construccion construccion_uej2_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.construccion
    ADD CONSTRAINT construccion_uej2_la_unidadespacial_fkey FOREIGN KEY (uej2_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11859 (class 2606 OID 337231)
-- Name: construccion construccion_uej2_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.construccion
    ADD CONSTRAINT construccion_uej2_servidumbrepaso_fkey FOREIGN KEY (uej2_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11860 (class 2606 OID 337236)
-- Name: construccion construccion_uej2_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.construccion
    ADD CONSTRAINT construccion_uej2_terreno_fkey FOREIGN KEY (uej2_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11861 (class 2606 OID 337241)
-- Name: construccion construccion_uej2_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.construccion
    ADD CONSTRAINT construccion_uej2_unidadconstruccion_fkey FOREIGN KEY (uej2_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11862 (class 2606 OID 337246)
-- Name: dq_element dq_element_col_derecho_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_col_derecho_calidad_fkey FOREIGN KEY (col_derecho_calidad) REFERENCES interlis_ili2db3_ladm.col_derecho(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11863 (class 2606 OID 337251)
-- Name: dq_element dq_element_col_fuenteadminstrtv_cldad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_col_fuenteadminstrtv_cldad_fkey FOREIGN KEY (col_fuenteadminstrtiva_calidad) REFERENCES interlis_ili2db3_ladm.col_fuenteadministrativa(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11864 (class 2606 OID 337256)
-- Name: dq_element dq_element_col_fuenteespacial_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_col_fuenteespacial_calidad_fkey FOREIGN KEY (col_fuenteespacial_calidad) REFERENCES interlis_ili2db3_ladm.col_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11865 (class 2606 OID 337261)
-- Name: dq_element dq_element_col_hipoteca_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_col_hipoteca_calidad_fkey FOREIGN KEY (col_hipoteca_calidad) REFERENCES interlis_ili2db3_ladm.col_hipoteca(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11866 (class 2606 OID 337266)
-- Name: dq_element dq_element_col_interesado_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_col_interesado_calidad_fkey FOREIGN KEY (col_interesado_calidad) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11867 (class 2606 OID 337271)
-- Name: dq_element dq_element_col_responsabilidad_caldad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_col_responsabilidad_caldad_fkey FOREIGN KEY (col_responsabilidad_calidad) REFERENCES interlis_ili2db3_ladm.col_responsabilidad(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11868 (class 2606 OID 337276)
-- Name: dq_element dq_element_col_restriccion_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_col_restriccion_calidad_fkey FOREIGN KEY (col_restriccion_calidad) REFERENCES interlis_ili2db3_ladm.col_restriccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11869 (class 2606 OID 337281)
-- Name: dq_element dq_element_construccion_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_construccion_calidad_fkey FOREIGN KEY (construccion_calidad) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11870 (class 2606 OID 337286)
-- Name: dq_element dq_element_la_agrupacion_ntrsds_cldad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_la_agrupacion_ntrsds_cldad_fkey FOREIGN KEY (la_agrupacion_intrsdos_calidad) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11871 (class 2606 OID 337291)
-- Name: dq_element dq_element_la_agrupacnnddsspcls_cldad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_la_agrupacnnddsspcls_cldad_fkey FOREIGN KEY (la_agrupacinnddsspcles_calidad) REFERENCES interlis_ili2db3_ladm.la_agrupacionunidadesespaciales(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11872 (class 2606 OID 337296)
-- Name: dq_element dq_element_la_baunit_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_la_baunit_calidad_fkey FOREIGN KEY (la_baunit_calidad) REFERENCES interlis_ili2db3_ladm.la_baunit(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11873 (class 2606 OID 337301)
-- Name: dq_element dq_element_la_cadenacaraslimite_cldad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_la_cadenacaraslimite_cldad_fkey FOREIGN KEY (la_cadenacaraslimite_calidad) REFERENCES interlis_ili2db3_ladm.la_cadenacaraslimite(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11874 (class 2606 OID 337306)
-- Name: dq_element dq_element_la_caraslindero_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_la_caraslindero_calidad_fkey FOREIGN KEY (la_caraslindero_calidad) REFERENCES interlis_ili2db3_ladm.la_caraslindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11875 (class 2606 OID 337311)
-- Name: dq_element dq_element_la_espacijrdcrdsrvcs_cldad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_la_espacijrdcrdsrvcs_cldad_fkey FOREIGN KEY (la_espacijrdcrdsrvcios_calidad) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11876 (class 2606 OID 337316)
-- Name: dq_element dq_element_la_espacjrdcndddfccn_cldad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_la_espacjrdcndddfccn_cldad_fkey FOREIGN KEY (la_espacjrdcndddfccion_calidad) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11877 (class 2606 OID 337321)
-- Name: dq_element dq_element_la_nivel_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_la_nivel_calidad_fkey FOREIGN KEY (la_nivel_calidad) REFERENCES interlis_ili2db3_ladm.la_nivel(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11878 (class 2606 OID 337326)
-- Name: dq_element dq_element_la_punto_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_la_punto_calidad_fkey FOREIGN KEY (la_punto_calidad) REFERENCES interlis_ili2db3_ladm.la_punto(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11879 (class 2606 OID 337331)
-- Name: dq_element dq_element_la_relacionnecsrbnts_cldad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_la_relacionnecsrbnts_cldad_fkey FOREIGN KEY (la_relacionnecesrbnits_calidad) REFERENCES interlis_ili2db3_ladm.la_relacionnecesariabaunits(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11880 (class 2606 OID 337336)
-- Name: dq_element dq_element_la_rlcnncsrnddsspcls_cldad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_la_rlcnncsrnddsspcls_cldad_fkey FOREIGN KEY (la_relcnncsrnddsspcles_calidad) REFERENCES interlis_ili2db3_ladm.la_relacionnecesariaunidadesespaciales(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11881 (class 2606 OID 337341)
-- Name: dq_element dq_element_la_unidadespacial_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_la_unidadespacial_calidad_fkey FOREIGN KEY (la_unidadespacial_calidad) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11882 (class 2606 OID 337346)
-- Name: dq_element dq_element_lindero_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_lindero_calidad_fkey FOREIGN KEY (lindero_calidad) REFERENCES interlis_ili2db3_ladm.lindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11883 (class 2606 OID 337351)
-- Name: dq_element dq_element_om_observacion_rsltd_cldad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_om_observacion_rsltd_cldad_fkey FOREIGN KEY (om_observacion_resultado_calidad) REFERENCES interlis_ili2db3_ladm.om_observacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11884 (class 2606 OID 337356)
-- Name: dq_element dq_element_predio_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_predio_calidad_fkey FOREIGN KEY (predio_calidad) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11885 (class 2606 OID 337361)
-- Name: dq_element dq_element_publicidad_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_publicidad_calidad_fkey FOREIGN KEY (publicidad_calidad) REFERENCES interlis_ili2db3_ladm.publicidad(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11886 (class 2606 OID 337366)
-- Name: dq_element dq_element_puntocontrol_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_puntocontrol_calidad_fkey FOREIGN KEY (puntocontrol_calidad) REFERENCES interlis_ili2db3_ladm.puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11887 (class 2606 OID 337371)
-- Name: dq_element dq_element_puntolevantamiento_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_puntolevantamiento_calidad_fkey FOREIGN KEY (puntolevantamiento_calidad) REFERENCES interlis_ili2db3_ladm.puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11888 (class 2606 OID 337376)
-- Name: dq_element dq_element_puntolindero_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_puntolindero_calidad_fkey FOREIGN KEY (puntolindero_calidad) REFERENCES interlis_ili2db3_ladm.puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11889 (class 2606 OID 337381)
-- Name: dq_element dq_element_servidumbrepaso_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_servidumbrepaso_calidad_fkey FOREIGN KEY (servidumbrepaso_calidad) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11890 (class 2606 OID 337386)
-- Name: dq_element dq_element_terreno_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_terreno_calidad_fkey FOREIGN KEY (terreno_calidad) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11891 (class 2606 OID 337391)
-- Name: dq_element dq_element_unidadconstruccion_calidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_element
    ADD CONSTRAINT dq_element_unidadconstruccion_calidad_fkey FOREIGN KEY (unidadconstruccion_calidad) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11892 (class 2606 OID 337396)
-- Name: dq_positionalaccuracy dq_positionalaccuracy_la_punto_exactitud_estmada_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_positionalaccuracy
    ADD CONSTRAINT dq_positionalaccuracy_la_punto_exactitud_estmada_fkey FOREIGN KEY (la_punto_exactitud_estimada) REFERENCES interlis_ili2db3_ladm.la_punto(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11893 (class 2606 OID 337401)
-- Name: dq_positionalaccuracy dq_positionalaccuracy_puntocontrol_excttd_stmada_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_positionalaccuracy
    ADD CONSTRAINT dq_positionalaccuracy_puntocontrol_excttd_stmada_fkey FOREIGN KEY (puntocontrol_exactitud_estimada) REFERENCES interlis_ili2db3_ladm.puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11894 (class 2606 OID 337406)
-- Name: dq_positionalaccuracy dq_positionalaccuracy_puntolevntmnt_xcttd_stmada_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_positionalaccuracy
    ADD CONSTRAINT dq_positionalaccuracy_puntolevntmnt_xcttd_stmada_fkey FOREIGN KEY (puntolevantamiento_exactitud_estimada) REFERENCES interlis_ili2db3_ladm.puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11895 (class 2606 OID 337411)
-- Name: dq_positionalaccuracy dq_positionalaccuracy_puntolindero_excttd_stmada_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.dq_positionalaccuracy
    ADD CONSTRAINT dq_positionalaccuracy_puntolindero_excttd_stmada_fkey FOREIGN KEY (puntolindero_exactitud_estimada) REFERENCES interlis_ili2db3_ladm.puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11896 (class 2606 OID 337416)
-- Name: extarchivo extarchivo_col_fntdmnstrtv_xt_rchv_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extarchivo
    ADD CONSTRAINT extarchivo_col_fntdmnstrtv_xt_rchv_id_fkey FOREIGN KEY (col_fuenteadminstrtiva_ext_archivo_id) REFERENCES interlis_ili2db3_ladm.col_fuenteadministrativa(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11897 (class 2606 OID 337421)
-- Name: extarchivo extarchivo_col_fuenteespcl_xt_rchv_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extarchivo
    ADD CONSTRAINT extarchivo_col_fuenteespcl_xt_rchv_id_fkey FOREIGN KEY (col_fuenteespacial_ext_archivo_id) REFERENCES interlis_ili2db3_ladm.col_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11898 (class 2606 OID 337426)
-- Name: extdireccion extdireccion_construccion_ext_dirccn_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extdireccion
    ADD CONSTRAINT extdireccion_construccion_ext_dirccn_id_fkey FOREIGN KEY (construccion_ext_direccion_id) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11899 (class 2606 OID 337431)
-- Name: extdireccion extdireccion_extinteresado_ext_drccn_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extdireccion
    ADD CONSTRAINT extdireccion_extinteresado_ext_drccn_id_fkey FOREIGN KEY (extinteresado_ext_direccion_id) REFERENCES interlis_ili2db3_ladm.extinteresado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11900 (class 2606 OID 337436)
-- Name: extdireccion extdireccion_extndddfccnfsc_xt_drccn_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extdireccion
    ADD CONSTRAINT extdireccion_extndddfccnfsc_xt_drccn_id_fkey FOREIGN KEY (extunidadedificcnfsica_ext_direccion_id) REFERENCES interlis_ili2db3_ladm.extunidadedificacionfisica(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11901 (class 2606 OID 337441)
-- Name: extdireccion extdireccion_la_spcjrdcnddn_xt_drccn_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extdireccion
    ADD CONSTRAINT extdireccion_la_spcjrdcnddn_xt_drccn_id_fkey FOREIGN KEY (la_espacjrdcndddfccion_ext_direccion_id) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11902 (class 2606 OID 337446)
-- Name: extdireccion extdireccion_la_spcjrdcrdss_xt_drccn_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extdireccion
    ADD CONSTRAINT extdireccion_la_spcjrdcrdss_xt_drccn_id_fkey FOREIGN KEY (la_espacijrdcrdsrvcios_ext_direccion_id) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11903 (class 2606 OID 337451)
-- Name: extdireccion extdireccion_la_unidadespcl_xt_drccn_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extdireccion
    ADD CONSTRAINT extdireccion_la_unidadespcl_xt_drccn_id_fkey FOREIGN KEY (la_unidadespacial_ext_direccion_id) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11904 (class 2606 OID 337456)
-- Name: extdireccion extdireccion_servidumbrepas_xt_drccn_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extdireccion
    ADD CONSTRAINT extdireccion_servidumbrepas_xt_drccn_id_fkey FOREIGN KEY (servidumbrepaso_ext_direccion_id) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11905 (class 2606 OID 337461)
-- Name: extdireccion extdireccion_terreno_ext_direccion_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extdireccion
    ADD CONSTRAINT extdireccion_terreno_ext_direccion_id_fkey FOREIGN KEY (terreno_ext_direccion_id) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11906 (class 2606 OID 337466)
-- Name: extdireccion extdireccion_unidadcnstrccn_xt_drccn_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extdireccion
    ADD CONSTRAINT extdireccion_unidadcnstrccn_xt_drccn_id_fkey FOREIGN KEY (unidadconstruccion_ext_direccion_id) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11907 (class 2606 OID 337471)
-- Name: extinteresado extinteresado_col_interesado_ext_pid_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extinteresado
    ADD CONSTRAINT extinteresado_col_interesado_ext_pid_fkey FOREIGN KEY (col_interesado_ext_pid) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11908 (class 2606 OID 337476)
-- Name: extinteresado extinteresado_extrdsrvcsfscd_dmnstrdr_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extinteresado
    ADD CONSTRAINT extinteresado_extrdsrvcsfscd_dmnstrdr_id_fkey FOREIGN KEY (extredserviciosfisica_ext_interesado_administrador_id) REFERENCES interlis_ili2db3_ladm.extredserviciosfisica(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11909 (class 2606 OID 337481)
-- Name: extinteresado extinteresado_la_agrupacin_ntrsds_xt_pid_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extinteresado
    ADD CONSTRAINT extinteresado_la_agrupacin_ntrsds_xt_pid_fkey FOREIGN KEY (la_agrupacion_intrsdos_ext_pid) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11910 (class 2606 OID 337486)
-- Name: extredserviciosfisica extredserviciosfisica_la_spcjrdcrdsxt_d_rd_fsica_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extredserviciosfisica
    ADD CONSTRAINT extredserviciosfisica_la_spcjrdcrdsxt_d_rd_fsica_fkey FOREIGN KEY (la_espacijrdcrdsrvcios_ext_id_red_fisica) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11911 (class 2606 OID 337491)
-- Name: extunidadedificacionfisica extunidadedificacionfisica_constrccn_xt__dfccn_fsc_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extunidadedificacionfisica
    ADD CONSTRAINT extunidadedificacionfisica_constrccn_xt__dfccn_fsc_id_fkey FOREIGN KEY (construccion_ext_unidad_edificacion_fisica_id) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11912 (class 2606 OID 337496)
-- Name: extunidadedificacionfisica extunidadedificacionfisica_la_spcjrdcndd_dfccn_fsc_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extunidadedificacionfisica
    ADD CONSTRAINT extunidadedificacionfisica_la_spcjrdcndd_dfccn_fsc_id_fkey FOREIGN KEY (la_espacjrdcndddfccion_ext_unidad_edificacion_fisic_id) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11913 (class 2606 OID 337501)
-- Name: extunidadedificacionfisica extunidadedificacionfisica_uniddcnstrccn_dfccn_fsc_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.extunidadedificacionfisica
    ADD CONSTRAINT extunidadedificacionfisica_uniddcnstrccn_dfccn_fsc_id_fkey FOREIGN KEY (unidadconstruccion_ext_unidad_edificacion_fisica_id) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11914 (class 2606 OID 337506)
-- Name: fraccion fraccion_col_derecho_compartido_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.fraccion
    ADD CONSTRAINT fraccion_col_derecho_compartido_fkey FOREIGN KEY (col_derecho_compartido) REFERENCES interlis_ili2db3_ladm.col_derecho(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11915 (class 2606 OID 337511)
-- Name: fraccion fraccion_col_hipoteca_compartido_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.fraccion
    ADD CONSTRAINT fraccion_col_hipoteca_compartido_fkey FOREIGN KEY (col_hipoteca_compartido) REFERENCES interlis_ili2db3_ladm.col_hipoteca(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11916 (class 2606 OID 337516)
-- Name: fraccion fraccion_col_responsabildd_cmprtido_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.fraccion
    ADD CONSTRAINT fraccion_col_responsabildd_cmprtido_fkey FOREIGN KEY (col_responsabilidad_compartido) REFERENCES interlis_ili2db3_ladm.col_responsabilidad(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11917 (class 2606 OID 337521)
-- Name: fraccion fraccion_col_restriccion_compartido_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.fraccion
    ADD CONSTRAINT fraccion_col_restriccion_compartido_fkey FOREIGN KEY (col_restriccion_compartido) REFERENCES interlis_ili2db3_ladm.col_restriccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11918 (class 2606 OID 337526)
-- Name: fraccion fraccion_miembros_participacion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.fraccion
    ADD CONSTRAINT fraccion_miembros_participacion_fkey FOREIGN KEY (miembros_participacion) REFERENCES interlis_ili2db3_ladm.miembros(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11919 (class 2606 OID 337531)
-- Name: fraccion fraccion_predio_copropiedad_cofcnte_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.fraccion
    ADD CONSTRAINT fraccion_predio_copropiedad_cofcnte_fkey FOREIGN KEY (predio_copropiedad_coeficiente) REFERENCES interlis_ili2db3_ladm.predio_copropiedad(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11920 (class 2606 OID 337536)
-- Name: gm_surface2dlistvalue gm_surface2dlistvalue_gm_multisurface2d_geometry_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.gm_surface2dlistvalue
    ADD CONSTRAINT gm_surface2dlistvalue_gm_multisurface2d_geometry_fkey FOREIGN KEY (gm_multisurface2d_geometry) REFERENCES interlis_ili2db3_ladm.gm_multisurface2d(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11921 (class 2606 OID 337541)
-- Name: gm_surface3dlistvalue gm_surface3dlistvalue_gm_multisurface3d_geometry_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.gm_surface3dlistvalue
    ADD CONSTRAINT gm_surface3dlistvalue_gm_multisurface3d_geometry_fkey FOREIGN KEY (gm_multisurface3d_geometry) REFERENCES interlis_ili2db3_ladm.gm_multisurface3d(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11922 (class 2606 OID 337546)
-- Name: hipotecaderecho hipotecaderecho_derecho_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.hipotecaderecho
    ADD CONSTRAINT hipotecaderecho_derecho_fkey FOREIGN KEY (derecho) REFERENCES interlis_ili2db3_ladm.col_derecho(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11923 (class 2606 OID 337551)
-- Name: hipotecaderecho hipotecaderecho_hipoteca_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.hipotecaderecho
    ADD CONSTRAINT hipotecaderecho_hipoteca_fkey FOREIGN KEY (hipoteca) REFERENCES interlis_ili2db3_ladm.col_hipoteca(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11924 (class 2606 OID 337556)
-- Name: imagen imagen_extinteresado_firma_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.imagen
    ADD CONSTRAINT imagen_extinteresado_firma_fkey FOREIGN KEY (extinteresado_firma) REFERENCES interlis_ili2db3_ladm.extinteresado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11925 (class 2606 OID 337561)
-- Name: imagen imagen_extinteresado_fotografia_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.imagen
    ADD CONSTRAINT imagen_extinteresado_fotografia_fkey FOREIGN KEY (extinteresado_fotografia) REFERENCES interlis_ili2db3_ladm.extinteresado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11926 (class 2606 OID 337566)
-- Name: imagen imagen_extinteresado_huell_dctlar_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.imagen
    ADD CONSTRAINT imagen_extinteresado_huell_dctlar_fkey FOREIGN KEY (extinteresado_huella_dactilar) REFERENCES interlis_ili2db3_ladm.extinteresado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11927 (class 2606 OID 337571)
-- Name: interesado_contacto interesado_contacto_interesado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.interesado_contacto
    ADD CONSTRAINT interesado_contacto_interesado_fkey FOREIGN KEY (interesado) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11928 (class 2606 OID 337576)
-- Name: la_agrupacionunidadesespaciales la_agrupacionunidadsspcles_aset_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_agrupacionunidadesespaciales
    ADD CONSTRAINT la_agrupacionunidadsspcles_aset_fkey FOREIGN KEY (aset) REFERENCES interlis_ili2db3_ladm.la_agrupacionunidadesespaciales(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11937 (class 2606 OID 337581)
-- Name: la_espaciojuridicounidadedificacion la_espaciojuridcndddfccion_nivel_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion
    ADD CONSTRAINT la_espaciojuridcndddfccion_nivel_fkey FOREIGN KEY (nivel) REFERENCES interlis_ili2db3_ladm.la_nivel(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11938 (class 2606 OID 337586)
-- Name: la_espaciojuridicounidadedificacion la_espaciojuridcndddfccion_uej2_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion
    ADD CONSTRAINT la_espaciojuridcndddfccion_uej2_construccion_fkey FOREIGN KEY (uej2_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11939 (class 2606 OID 337591)
-- Name: la_espaciojuridicounidadedificacion la_espaciojuridcndddfccion_uej2_la_espacjrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion
    ADD CONSTRAINT la_espaciojuridcndddfccion_uej2_la_espacjrdcrdsrvcios_fkey FOREIGN KEY (uej2_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11940 (class 2606 OID 337596)
-- Name: la_espaciojuridicounidadedificacion la_espaciojuridcndddfccion_uej2_la_espcjrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion
    ADD CONSTRAINT la_espaciojuridcndddfccion_uej2_la_espcjrdcndddfccion_fkey FOREIGN KEY (uej2_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11941 (class 2606 OID 337601)
-- Name: la_espaciojuridicounidadedificacion la_espaciojuridcndddfccion_uej2_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion
    ADD CONSTRAINT la_espaciojuridcndddfccion_uej2_la_unidadespacial_fkey FOREIGN KEY (uej2_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11942 (class 2606 OID 337606)
-- Name: la_espaciojuridicounidadedificacion la_espaciojuridcndddfccion_uej2_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion
    ADD CONSTRAINT la_espaciojuridcndddfccion_uej2_servidumbrepaso_fkey FOREIGN KEY (uej2_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11943 (class 2606 OID 337611)
-- Name: la_espaciojuridicounidadedificacion la_espaciojuridcndddfccion_uej2_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion
    ADD CONSTRAINT la_espaciojuridcndddfccion_uej2_terreno_fkey FOREIGN KEY (uej2_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11944 (class 2606 OID 337616)
-- Name: la_espaciojuridicounidadedificacion la_espaciojuridcndddfccion_uej2_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion
    ADD CONSTRAINT la_espaciojuridcndddfccion_uej2_unidadconstruccion_fkey FOREIGN KEY (uej2_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11929 (class 2606 OID 337621)
-- Name: la_espaciojuridicoredservicios la_espaciojuridicrdsrvcios_nivel_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicoredservicios
    ADD CONSTRAINT la_espaciojuridicrdsrvcios_nivel_fkey FOREIGN KEY (nivel) REFERENCES interlis_ili2db3_ladm.la_nivel(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11930 (class 2606 OID 337626)
-- Name: la_espaciojuridicoredservicios la_espaciojuridicrdsrvcios_uej2_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicoredservicios
    ADD CONSTRAINT la_espaciojuridicrdsrvcios_uej2_construccion_fkey FOREIGN KEY (uej2_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11931 (class 2606 OID 337631)
-- Name: la_espaciojuridicoredservicios la_espaciojuridicrdsrvcios_uej2_la_espacjrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicoredservicios
    ADD CONSTRAINT la_espaciojuridicrdsrvcios_uej2_la_espacjrdcrdsrvcios_fkey FOREIGN KEY (uej2_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11932 (class 2606 OID 337636)
-- Name: la_espaciojuridicoredservicios la_espaciojuridicrdsrvcios_uej2_la_espcjrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicoredservicios
    ADD CONSTRAINT la_espaciojuridicrdsrvcios_uej2_la_espcjrdcndddfccion_fkey FOREIGN KEY (uej2_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11933 (class 2606 OID 337641)
-- Name: la_espaciojuridicoredservicios la_espaciojuridicrdsrvcios_uej2_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicoredservicios
    ADD CONSTRAINT la_espaciojuridicrdsrvcios_uej2_la_unidadespacial_fkey FOREIGN KEY (uej2_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11934 (class 2606 OID 337646)
-- Name: la_espaciojuridicoredservicios la_espaciojuridicrdsrvcios_uej2_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicoredservicios
    ADD CONSTRAINT la_espaciojuridicrdsrvcios_uej2_servidumbrepaso_fkey FOREIGN KEY (uej2_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11935 (class 2606 OID 337651)
-- Name: la_espaciojuridicoredservicios la_espaciojuridicrdsrvcios_uej2_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicoredservicios
    ADD CONSTRAINT la_espaciojuridicrdsrvcios_uej2_terreno_fkey FOREIGN KEY (uej2_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11936 (class 2606 OID 337656)
-- Name: la_espaciojuridicoredservicios la_espaciojuridicrdsrvcios_uej2_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_espaciojuridicoredservicios
    ADD CONSTRAINT la_espaciojuridicrdsrvcios_uej2_unidadconstruccion_fkey FOREIGN KEY (uej2_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11945 (class 2606 OID 337661)
-- Name: la_punto la_punto_ue_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_punto
    ADD CONSTRAINT la_punto_ue_construccion_fkey FOREIGN KEY (ue_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11946 (class 2606 OID 337666)
-- Name: la_punto la_punto_ue_la_espacijrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_punto
    ADD CONSTRAINT la_punto_ue_la_espacijrdcndddfccion_fkey FOREIGN KEY (ue_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11947 (class 2606 OID 337671)
-- Name: la_punto la_punto_ue_la_espaciojrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_punto
    ADD CONSTRAINT la_punto_ue_la_espaciojrdcrdsrvcios_fkey FOREIGN KEY (ue_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11948 (class 2606 OID 337676)
-- Name: la_punto la_punto_ue_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_punto
    ADD CONSTRAINT la_punto_ue_la_unidadespacial_fkey FOREIGN KEY (ue_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11949 (class 2606 OID 337681)
-- Name: la_punto la_punto_ue_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_punto
    ADD CONSTRAINT la_punto_ue_servidumbrepaso_fkey FOREIGN KEY (ue_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11950 (class 2606 OID 337686)
-- Name: la_punto la_punto_ue_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_punto
    ADD CONSTRAINT la_punto_ue_terreno_fkey FOREIGN KEY (ue_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11951 (class 2606 OID 337691)
-- Name: la_punto la_punto_ue_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_punto
    ADD CONSTRAINT la_punto_ue_unidadconstruccion_fkey FOREIGN KEY (ue_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11952 (class 2606 OID 337696)
-- Name: la_tareainteresadotipo la_tareainteresadotipo_col_interesado_tarea_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_tareainteresadotipo
    ADD CONSTRAINT la_tareainteresadotipo_col_interesado_tarea_fkey FOREIGN KEY (col_interesado_tarea) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11953 (class 2606 OID 337701)
-- Name: la_tareainteresadotipo la_tareainteresadotipo_la_agrupacion_intrsds_trea_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_tareainteresadotipo
    ADD CONSTRAINT la_tareainteresadotipo_la_agrupacion_intrsds_trea_fkey FOREIGN KEY (la_agrupacion_intrsdos_tarea) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11954 (class 2606 OID 337706)
-- Name: la_transformacion la_transformacion_la_pnt_trnsfrmcn_y_rsltado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_transformacion
    ADD CONSTRAINT la_transformacion_la_pnt_trnsfrmcn_y_rsltado_fkey FOREIGN KEY (la_punto_transformacion_y_resultado) REFERENCES interlis_ili2db3_ladm.la_punto(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11955 (class 2606 OID 337711)
-- Name: la_transformacion la_transformacion_puntcntrl_trnmcn_y_rsltado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_transformacion
    ADD CONSTRAINT la_transformacion_puntcntrl_trnmcn_y_rsltado_fkey FOREIGN KEY (puntocontrol_transformacion_y_resultado) REFERENCES interlis_ili2db3_ladm.puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11956 (class 2606 OID 337716)
-- Name: la_transformacion la_transformacion_puntlndr_trnsmcn_y_rsltado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_transformacion
    ADD CONSTRAINT la_transformacion_puntlndr_trnsmcn_y_rsltado_fkey FOREIGN KEY (puntolindero_transformacion_y_resultado) REFERENCES interlis_ili2db3_ladm.puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11957 (class 2606 OID 337721)
-- Name: la_transformacion la_transformacion_puntlvntmnt_tmcn_y_rsltado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_transformacion
    ADD CONSTRAINT la_transformacion_puntlvntmnt_tmcn_y_rsltado_fkey FOREIGN KEY (puntolevantamiento_transformacion_y_resultado) REFERENCES interlis_ili2db3_ladm.puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11958 (class 2606 OID 337726)
-- Name: la_unidadespacial la_unidadespacial_nivel_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_unidadespacial
    ADD CONSTRAINT la_unidadespacial_nivel_fkey FOREIGN KEY (nivel) REFERENCES interlis_ili2db3_ladm.la_nivel(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11959 (class 2606 OID 337731)
-- Name: la_unidadespacial la_unidadespacial_uej2_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_unidadespacial
    ADD CONSTRAINT la_unidadespacial_uej2_construccion_fkey FOREIGN KEY (uej2_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11960 (class 2606 OID 337736)
-- Name: la_unidadespacial la_unidadespacial_uej2_la_espacjrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_unidadespacial
    ADD CONSTRAINT la_unidadespacial_uej2_la_espacjrdcrdsrvcios_fkey FOREIGN KEY (uej2_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11961 (class 2606 OID 337741)
-- Name: la_unidadespacial la_unidadespacial_uej2_la_espcjrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_unidadespacial
    ADD CONSTRAINT la_unidadespacial_uej2_la_espcjrdcndddfccion_fkey FOREIGN KEY (uej2_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11962 (class 2606 OID 337746)
-- Name: la_unidadespacial la_unidadespacial_uej2_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_unidadespacial
    ADD CONSTRAINT la_unidadespacial_uej2_la_unidadespacial_fkey FOREIGN KEY (uej2_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11963 (class 2606 OID 337751)
-- Name: la_unidadespacial la_unidadespacial_uej2_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_unidadespacial
    ADD CONSTRAINT la_unidadespacial_uej2_servidumbrepaso_fkey FOREIGN KEY (uej2_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11964 (class 2606 OID 337756)
-- Name: la_unidadespacial la_unidadespacial_uej2_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_unidadespacial
    ADD CONSTRAINT la_unidadespacial_uej2_terreno_fkey FOREIGN KEY (uej2_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11965 (class 2606 OID 337761)
-- Name: la_unidadespacial la_unidadespacial_uej2_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_unidadespacial
    ADD CONSTRAINT la_unidadespacial_uej2_unidadconstruccion_fkey FOREIGN KEY (uej2_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11966 (class 2606 OID 337766)
-- Name: la_volumenvalor la_volumenvalor_construccion_volumen_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_volumenvalor
    ADD CONSTRAINT la_volumenvalor_construccion_volumen_fkey FOREIGN KEY (construccion_volumen) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11967 (class 2606 OID 337771)
-- Name: la_volumenvalor la_volumenvalor_la_espacijrdcrdsrvcs_vlmen_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_volumenvalor
    ADD CONSTRAINT la_volumenvalor_la_espacijrdcrdsrvcs_vlmen_fkey FOREIGN KEY (la_espacijrdcrdsrvcios_volumen) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11968 (class 2606 OID 337776)
-- Name: la_volumenvalor la_volumenvalor_la_espacjrdcndddfccn_vlmen_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_volumenvalor
    ADD CONSTRAINT la_volumenvalor_la_espacjrdcndddfccn_vlmen_fkey FOREIGN KEY (la_espacjrdcndddfccion_volumen) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11969 (class 2606 OID 337781)
-- Name: la_volumenvalor la_volumenvalor_la_unidadespacial_volumen_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_volumenvalor
    ADD CONSTRAINT la_volumenvalor_la_unidadespacial_volumen_fkey FOREIGN KEY (la_unidadespacial_volumen) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11970 (class 2606 OID 337786)
-- Name: la_volumenvalor la_volumenvalor_servidumbrepaso_volumen_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_volumenvalor
    ADD CONSTRAINT la_volumenvalor_servidumbrepaso_volumen_fkey FOREIGN KEY (servidumbrepaso_volumen) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11971 (class 2606 OID 337791)
-- Name: la_volumenvalor la_volumenvalor_terreno_volumen_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_volumenvalor
    ADD CONSTRAINT la_volumenvalor_terreno_volumen_fkey FOREIGN KEY (terreno_volumen) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11972 (class 2606 OID 337796)
-- Name: la_volumenvalor la_volumenvalor_unidadconstruccion_volumen_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.la_volumenvalor
    ADD CONSTRAINT la_volumenvalor_unidadconstruccion_volumen_fkey FOREIGN KEY (unidadconstruccion_volumen) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11973 (class 2606 OID 337801)
-- Name: li_lineaje li_lineaje_la_punto_metodoproduccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.li_lineaje
    ADD CONSTRAINT li_lineaje_la_punto_metodoproduccion_fkey FOREIGN KEY (la_punto_metodoproduccion) REFERENCES interlis_ili2db3_ladm.la_punto(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11974 (class 2606 OID 337806)
-- Name: li_lineaje li_lineaje_puntocontrol_metodprdccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.li_lineaje
    ADD CONSTRAINT li_lineaje_puntocontrol_metodprdccion_fkey FOREIGN KEY (puntocontrol_metodoproduccion) REFERENCES interlis_ili2db3_ladm.puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11975 (class 2606 OID 337811)
-- Name: li_lineaje li_lineaje_puntolevantmnt_mtdprdccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.li_lineaje
    ADD CONSTRAINT li_lineaje_puntolevantmnt_mtdprdccion_fkey FOREIGN KEY (puntolevantamiento_metodoproduccion) REFERENCES interlis_ili2db3_ladm.puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11976 (class 2606 OID 337816)
-- Name: li_lineaje li_lineaje_puntolindero_metodprdccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.li_lineaje
    ADD CONSTRAINT li_lineaje_puntolindero_metodprdccion_fkey FOREIGN KEY (puntolindero_metodoproduccion) REFERENCES interlis_ili2db3_ladm.puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11977 (class 2606 OID 337821)
-- Name: mas mas_clp_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.mas
    ADD CONSTRAINT mas_clp_fkey FOREIGN KEY (clp) REFERENCES interlis_ili2db3_ladm.la_caraslindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11978 (class 2606 OID 337826)
-- Name: mas mas_uep_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.mas
    ADD CONSTRAINT mas_uep_construccion_fkey FOREIGN KEY (uep_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11979 (class 2606 OID 337831)
-- Name: mas mas_uep_la_espacijrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.mas
    ADD CONSTRAINT mas_uep_la_espacijrdcrdsrvcios_fkey FOREIGN KEY (uep_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11980 (class 2606 OID 337836)
-- Name: mas mas_uep_la_espacjrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.mas
    ADD CONSTRAINT mas_uep_la_espacjrdcndddfccion_fkey FOREIGN KEY (uep_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11981 (class 2606 OID 337841)
-- Name: mas mas_uep_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.mas
    ADD CONSTRAINT mas_uep_la_unidadespacial_fkey FOREIGN KEY (uep_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11982 (class 2606 OID 337846)
-- Name: mas mas_uep_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.mas
    ADD CONSTRAINT mas_uep_servidumbrepaso_fkey FOREIGN KEY (uep_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11983 (class 2606 OID 337851)
-- Name: mas mas_uep_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.mas
    ADD CONSTRAINT mas_uep_terreno_fkey FOREIGN KEY (uep_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11984 (class 2606 OID 337856)
-- Name: mas mas_uep_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.mas
    ADD CONSTRAINT mas_uep_unidadconstruccion_fkey FOREIGN KEY (uep_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11985 (class 2606 OID 337861)
-- Name: masccl masccl_cclp_la_cadenacaraslimite_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.masccl
    ADD CONSTRAINT masccl_cclp_la_cadenacaraslimite_fkey FOREIGN KEY (cclp_la_cadenacaraslimite) REFERENCES interlis_ili2db3_ladm.la_cadenacaraslimite(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11986 (class 2606 OID 337866)
-- Name: masccl masccl_cclp_lindero_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.masccl
    ADD CONSTRAINT masccl_cclp_lindero_fkey FOREIGN KEY (cclp_lindero) REFERENCES interlis_ili2db3_ladm.lindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11987 (class 2606 OID 337871)
-- Name: masccl masccl_uep_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.masccl
    ADD CONSTRAINT masccl_uep_construccion_fkey FOREIGN KEY (uep_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11988 (class 2606 OID 337876)
-- Name: masccl masccl_uep_la_espacijrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.masccl
    ADD CONSTRAINT masccl_uep_la_espacijrdcrdsrvcios_fkey FOREIGN KEY (uep_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11989 (class 2606 OID 337881)
-- Name: masccl masccl_uep_la_espacjrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.masccl
    ADD CONSTRAINT masccl_uep_la_espacjrdcndddfccion_fkey FOREIGN KEY (uep_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11990 (class 2606 OID 337886)
-- Name: masccl masccl_uep_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.masccl
    ADD CONSTRAINT masccl_uep_la_unidadespacial_fkey FOREIGN KEY (uep_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11991 (class 2606 OID 337891)
-- Name: masccl masccl_uep_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.masccl
    ADD CONSTRAINT masccl_uep_servidumbrepaso_fkey FOREIGN KEY (uep_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11992 (class 2606 OID 337896)
-- Name: masccl masccl_uep_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.masccl
    ADD CONSTRAINT masccl_uep_terreno_fkey FOREIGN KEY (uep_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11993 (class 2606 OID 337901)
-- Name: masccl masccl_uep_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.masccl
    ADD CONSTRAINT masccl_uep_unidadconstruccion_fkey FOREIGN KEY (uep_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11994 (class 2606 OID 337906)
-- Name: menos menos_ccl_la_cadenacaraslimite_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menos
    ADD CONSTRAINT menos_ccl_la_cadenacaraslimite_fkey FOREIGN KEY (ccl_la_cadenacaraslimite) REFERENCES interlis_ili2db3_ladm.la_cadenacaraslimite(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11995 (class 2606 OID 337911)
-- Name: menos menos_ccl_lindero_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menos
    ADD CONSTRAINT menos_ccl_lindero_fkey FOREIGN KEY (ccl_lindero) REFERENCES interlis_ili2db3_ladm.lindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11996 (class 2606 OID 337916)
-- Name: menos menos_eu_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menos
    ADD CONSTRAINT menos_eu_construccion_fkey FOREIGN KEY (eu_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11997 (class 2606 OID 337921)
-- Name: menos menos_eu_la_espacijrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menos
    ADD CONSTRAINT menos_eu_la_espacijrdcndddfccion_fkey FOREIGN KEY (eu_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11998 (class 2606 OID 337926)
-- Name: menos menos_eu_la_espaciojrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menos
    ADD CONSTRAINT menos_eu_la_espaciojrdcrdsrvcios_fkey FOREIGN KEY (eu_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 11999 (class 2606 OID 337931)
-- Name: menos menos_eu_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menos
    ADD CONSTRAINT menos_eu_la_unidadespacial_fkey FOREIGN KEY (eu_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12000 (class 2606 OID 337936)
-- Name: menos menos_eu_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menos
    ADD CONSTRAINT menos_eu_servidumbrepaso_fkey FOREIGN KEY (eu_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12001 (class 2606 OID 337941)
-- Name: menos menos_eu_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menos
    ADD CONSTRAINT menos_eu_terreno_fkey FOREIGN KEY (eu_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12002 (class 2606 OID 337946)
-- Name: menos menos_eu_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menos
    ADD CONSTRAINT menos_eu_unidadconstruccion_fkey FOREIGN KEY (eu_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12003 (class 2606 OID 337951)
-- Name: menosf menosf_cl_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menosf
    ADD CONSTRAINT menosf_cl_fkey FOREIGN KEY (cl) REFERENCES interlis_ili2db3_ladm.la_caraslindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12004 (class 2606 OID 337956)
-- Name: menosf menosf_ue_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menosf
    ADD CONSTRAINT menosf_ue_construccion_fkey FOREIGN KEY (ue_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12005 (class 2606 OID 337961)
-- Name: menosf menosf_ue_la_espacijrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menosf
    ADD CONSTRAINT menosf_ue_la_espacijrdcndddfccion_fkey FOREIGN KEY (ue_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12006 (class 2606 OID 337966)
-- Name: menosf menosf_ue_la_espaciojrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menosf
    ADD CONSTRAINT menosf_ue_la_espaciojrdcrdsrvcios_fkey FOREIGN KEY (ue_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12007 (class 2606 OID 337971)
-- Name: menosf menosf_ue_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menosf
    ADD CONSTRAINT menosf_ue_la_unidadespacial_fkey FOREIGN KEY (ue_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12008 (class 2606 OID 337976)
-- Name: menosf menosf_ue_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menosf
    ADD CONSTRAINT menosf_ue_servidumbrepaso_fkey FOREIGN KEY (ue_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12009 (class 2606 OID 337981)
-- Name: menosf menosf_ue_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menosf
    ADD CONSTRAINT menosf_ue_terreno_fkey FOREIGN KEY (ue_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12010 (class 2606 OID 337986)
-- Name: menosf menosf_ue_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.menosf
    ADD CONSTRAINT menosf_ue_unidadconstruccion_fkey FOREIGN KEY (ue_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12011 (class 2606 OID 337991)
-- Name: miembros miembros_agrupacion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.miembros
    ADD CONSTRAINT miembros_agrupacion_fkey FOREIGN KEY (agrupacion) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12012 (class 2606 OID 337996)
-- Name: miembros miembros_interesados_col_interesado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.miembros
    ADD CONSTRAINT miembros_interesados_col_interesado_fkey FOREIGN KEY (interesados_col_interesado) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12013 (class 2606 OID 338001)
-- Name: miembros miembros_interesads_l_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.miembros
    ADD CONSTRAINT miembros_interesads_l_grpcn_ntrsdos_fkey FOREIGN KEY (interesados_la_agrupacion_interesados) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12014 (class 2606 OID 338006)
-- Name: oid oid_extdireccion_direccion_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.oid
    ADD CONSTRAINT oid_extdireccion_direccion_id_fkey FOREIGN KEY (extdireccion_direccion_id) REFERENCES interlis_ili2db3_ladm.extdireccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12015 (class 2606 OID 338011)
-- Name: oid oid_extinteresado_interesad_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.oid
    ADD CONSTRAINT oid_extinteresado_interesad_id_fkey FOREIGN KEY (extinteresado_interesado_id) REFERENCES interlis_ili2db3_ladm.extinteresado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12016 (class 2606 OID 338016)
-- Name: oid oid_la_nivel_n_id_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.oid
    ADD CONSTRAINT oid_la_nivel_n_id_fkey FOREIGN KEY (la_nivel_n_id) REFERENCES interlis_ili2db3_ladm.la_nivel(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12017 (class 2606 OID 338021)
-- Name: om_observacion om_observacion_col_fuenteespacial_medcnes_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.om_observacion
    ADD CONSTRAINT om_observacion_col_fuenteespacial_medcnes_fkey FOREIGN KEY (col_fuenteespacial_mediciones) REFERENCES interlis_ili2db3_ladm.col_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12018 (class 2606 OID 338026)
-- Name: om_proceso om_proceso_col_fuenteespacil_prcdmnto_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.om_proceso
    ADD CONSTRAINT om_proceso_col_fuenteespacil_prcdmnto_fkey FOREIGN KEY (col_fuenteespacial_procedimiento) REFERENCES interlis_ili2db3_ladm.col_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12019 (class 2606 OID 338031)
-- Name: predio predio_copropiedad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.predio
    ADD CONSTRAINT predio_copropiedad_fkey FOREIGN KEY (copropiedad) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12020 (class 2606 OID 338036)
-- Name: publicidad publicidad_baunit_la_baunit_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.publicidad
    ADD CONSTRAINT publicidad_baunit_la_baunit_fkey FOREIGN KEY (baunit_la_baunit) REFERENCES interlis_ili2db3_ladm.la_baunit(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12021 (class 2606 OID 338041)
-- Name: publicidad publicidad_baunit_predio_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.publicidad
    ADD CONSTRAINT publicidad_baunit_predio_fkey FOREIGN KEY (baunit_predio) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12022 (class 2606 OID 338046)
-- Name: publicidad publicidad_interesado_col_interesado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.publicidad
    ADD CONSTRAINT publicidad_interesado_col_interesado_fkey FOREIGN KEY (interesado_col_interesado) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12023 (class 2606 OID 338051)
-- Name: publicidad publicidad_interesado_l_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.publicidad
    ADD CONSTRAINT publicidad_interesado_l_grpcn_ntrsdos_fkey FOREIGN KEY (interesado_la_agrupacion_interesados) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12024 (class 2606 OID 338056)
-- Name: publicidadfuente publicidadfuente_fuente_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.publicidadfuente
    ADD CONSTRAINT publicidadfuente_fuente_fkey FOREIGN KEY (fuente) REFERENCES interlis_ili2db3_ladm.col_fuenteadministrativa(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12025 (class 2606 OID 338061)
-- Name: publicidadfuente publicidadfuente_publicidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.publicidadfuente
    ADD CONSTRAINT publicidadfuente_publicidad_fkey FOREIGN KEY (publicidad) REFERENCES interlis_ili2db3_ladm.publicidad(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12026 (class 2606 OID 338066)
-- Name: puntoccl puntoccl_ccl_la_cadenacaraslimite_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntoccl
    ADD CONSTRAINT puntoccl_ccl_la_cadenacaraslimite_fkey FOREIGN KEY (ccl_la_cadenacaraslimite) REFERENCES interlis_ili2db3_ladm.la_cadenacaraslimite(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12027 (class 2606 OID 338071)
-- Name: puntoccl puntoccl_ccl_lindero_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntoccl
    ADD CONSTRAINT puntoccl_ccl_lindero_fkey FOREIGN KEY (ccl_lindero) REFERENCES interlis_ili2db3_ladm.lindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12028 (class 2606 OID 338076)
-- Name: puntoccl puntoccl_punto_la_punto_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntoccl
    ADD CONSTRAINT puntoccl_punto_la_punto_fkey FOREIGN KEY (punto_la_punto) REFERENCES interlis_ili2db3_ladm.la_punto(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12029 (class 2606 OID 338081)
-- Name: puntoccl puntoccl_punto_puntocontrol_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntoccl
    ADD CONSTRAINT puntoccl_punto_puntocontrol_fkey FOREIGN KEY (punto_puntocontrol) REFERENCES interlis_ili2db3_ladm.puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12030 (class 2606 OID 338086)
-- Name: puntoccl puntoccl_punto_puntolevantamiento_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntoccl
    ADD CONSTRAINT puntoccl_punto_puntolevantamiento_fkey FOREIGN KEY (punto_puntolevantamiento) REFERENCES interlis_ili2db3_ladm.puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12031 (class 2606 OID 338091)
-- Name: puntoccl puntoccl_punto_puntolindero_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntoccl
    ADD CONSTRAINT puntoccl_punto_puntolindero_fkey FOREIGN KEY (punto_puntolindero) REFERENCES interlis_ili2db3_ladm.puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12032 (class 2606 OID 338096)
-- Name: puntocl puntocl_cl_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocl
    ADD CONSTRAINT puntocl_cl_fkey FOREIGN KEY (cl) REFERENCES interlis_ili2db3_ladm.la_caraslindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12033 (class 2606 OID 338101)
-- Name: puntocl puntocl_punto_la_punto_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocl
    ADD CONSTRAINT puntocl_punto_la_punto_fkey FOREIGN KEY (punto_la_punto) REFERENCES interlis_ili2db3_ladm.la_punto(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12034 (class 2606 OID 338106)
-- Name: puntocl puntocl_punto_puntocontrol_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocl
    ADD CONSTRAINT puntocl_punto_puntocontrol_fkey FOREIGN KEY (punto_puntocontrol) REFERENCES interlis_ili2db3_ladm.puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12035 (class 2606 OID 338111)
-- Name: puntocl puntocl_punto_puntolevantamiento_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocl
    ADD CONSTRAINT puntocl_punto_puntolevantamiento_fkey FOREIGN KEY (punto_puntolevantamiento) REFERENCES interlis_ili2db3_ladm.puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12036 (class 2606 OID 338116)
-- Name: puntocl puntocl_punto_puntolindero_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocl
    ADD CONSTRAINT puntocl_punto_puntolindero_fkey FOREIGN KEY (punto_puntolindero) REFERENCES interlis_ili2db3_ladm.puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12037 (class 2606 OID 338121)
-- Name: puntocontrol puntocontrol_ue_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocontrol
    ADD CONSTRAINT puntocontrol_ue_construccion_fkey FOREIGN KEY (ue_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12038 (class 2606 OID 338126)
-- Name: puntocontrol puntocontrol_ue_la_espacijrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocontrol
    ADD CONSTRAINT puntocontrol_ue_la_espacijrdcndddfccion_fkey FOREIGN KEY (ue_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12039 (class 2606 OID 338131)
-- Name: puntocontrol puntocontrol_ue_la_espaciojrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocontrol
    ADD CONSTRAINT puntocontrol_ue_la_espaciojrdcrdsrvcios_fkey FOREIGN KEY (ue_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12040 (class 2606 OID 338136)
-- Name: puntocontrol puntocontrol_ue_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocontrol
    ADD CONSTRAINT puntocontrol_ue_la_unidadespacial_fkey FOREIGN KEY (ue_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12041 (class 2606 OID 338141)
-- Name: puntocontrol puntocontrol_ue_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocontrol
    ADD CONSTRAINT puntocontrol_ue_servidumbrepaso_fkey FOREIGN KEY (ue_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12042 (class 2606 OID 338146)
-- Name: puntocontrol puntocontrol_ue_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocontrol
    ADD CONSTRAINT puntocontrol_ue_terreno_fkey FOREIGN KEY (ue_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12043 (class 2606 OID 338151)
-- Name: puntocontrol puntocontrol_ue_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntocontrol
    ADD CONSTRAINT puntocontrol_ue_unidadconstruccion_fkey FOREIGN KEY (ue_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12044 (class 2606 OID 338156)
-- Name: puntofuente puntofuente_pfuente_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntofuente
    ADD CONSTRAINT puntofuente_pfuente_fkey FOREIGN KEY (pfuente) REFERENCES interlis_ili2db3_ladm.col_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12045 (class 2606 OID 338161)
-- Name: puntofuente puntofuente_punto_la_punto_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntofuente
    ADD CONSTRAINT puntofuente_punto_la_punto_fkey FOREIGN KEY (punto_la_punto) REFERENCES interlis_ili2db3_ladm.la_punto(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12046 (class 2606 OID 338166)
-- Name: puntofuente puntofuente_punto_puntocontrol_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntofuente
    ADD CONSTRAINT puntofuente_punto_puntocontrol_fkey FOREIGN KEY (punto_puntocontrol) REFERENCES interlis_ili2db3_ladm.puntocontrol(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12047 (class 2606 OID 338171)
-- Name: puntofuente puntofuente_punto_puntolevantamiento_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntofuente
    ADD CONSTRAINT puntofuente_punto_puntolevantamiento_fkey FOREIGN KEY (punto_puntolevantamiento) REFERENCES interlis_ili2db3_ladm.puntolevantamiento(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12048 (class 2606 OID 338176)
-- Name: puntofuente puntofuente_punto_puntolindero_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntofuente
    ADD CONSTRAINT puntofuente_punto_puntolindero_fkey FOREIGN KEY (punto_puntolindero) REFERENCES interlis_ili2db3_ladm.puntolindero(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12049 (class 2606 OID 338181)
-- Name: puntolevantamiento puntolevantamiento_ue_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolevantamiento
    ADD CONSTRAINT puntolevantamiento_ue_construccion_fkey FOREIGN KEY (ue_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12050 (class 2606 OID 338186)
-- Name: puntolevantamiento puntolevantamiento_ue_la_espacijrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolevantamiento
    ADD CONSTRAINT puntolevantamiento_ue_la_espacijrdcndddfccion_fkey FOREIGN KEY (ue_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12051 (class 2606 OID 338191)
-- Name: puntolevantamiento puntolevantamiento_ue_la_espaciojrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolevantamiento
    ADD CONSTRAINT puntolevantamiento_ue_la_espaciojrdcrdsrvcios_fkey FOREIGN KEY (ue_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12052 (class 2606 OID 338196)
-- Name: puntolevantamiento puntolevantamiento_ue_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolevantamiento
    ADD CONSTRAINT puntolevantamiento_ue_la_unidadespacial_fkey FOREIGN KEY (ue_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12053 (class 2606 OID 338201)
-- Name: puntolevantamiento puntolevantamiento_ue_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolevantamiento
    ADD CONSTRAINT puntolevantamiento_ue_servidumbrepaso_fkey FOREIGN KEY (ue_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12054 (class 2606 OID 338206)
-- Name: puntolevantamiento puntolevantamiento_ue_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolevantamiento
    ADD CONSTRAINT puntolevantamiento_ue_terreno_fkey FOREIGN KEY (ue_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12055 (class 2606 OID 338211)
-- Name: puntolevantamiento puntolevantamiento_ue_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolevantamiento
    ADD CONSTRAINT puntolevantamiento_ue_unidadconstruccion_fkey FOREIGN KEY (ue_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12056 (class 2606 OID 338216)
-- Name: puntolindero puntolindero_ue_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolindero
    ADD CONSTRAINT puntolindero_ue_construccion_fkey FOREIGN KEY (ue_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12057 (class 2606 OID 338221)
-- Name: puntolindero puntolindero_ue_la_espacijrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolindero
    ADD CONSTRAINT puntolindero_ue_la_espacijrdcndddfccion_fkey FOREIGN KEY (ue_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12058 (class 2606 OID 338226)
-- Name: puntolindero puntolindero_ue_la_espaciojrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolindero
    ADD CONSTRAINT puntolindero_ue_la_espaciojrdcrdsrvcios_fkey FOREIGN KEY (ue_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12059 (class 2606 OID 338231)
-- Name: puntolindero puntolindero_ue_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolindero
    ADD CONSTRAINT puntolindero_ue_la_unidadespacial_fkey FOREIGN KEY (ue_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12060 (class 2606 OID 338236)
-- Name: puntolindero puntolindero_ue_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolindero
    ADD CONSTRAINT puntolindero_ue_servidumbrepaso_fkey FOREIGN KEY (ue_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12061 (class 2606 OID 338241)
-- Name: puntolindero puntolindero_ue_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolindero
    ADD CONSTRAINT puntolindero_ue_terreno_fkey FOREIGN KEY (ue_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12062 (class 2606 OID 338246)
-- Name: puntolindero puntolindero_ue_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.puntolindero
    ADD CONSTRAINT puntolindero_ue_unidadconstruccion_fkey FOREIGN KEY (ue_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12063 (class 2606 OID 338251)
-- Name: relacionbaunit relacionbaunit_unidad1_la_baunit_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionbaunit
    ADD CONSTRAINT relacionbaunit_unidad1_la_baunit_fkey FOREIGN KEY (unidad1_la_baunit) REFERENCES interlis_ili2db3_ladm.la_baunit(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12064 (class 2606 OID 338256)
-- Name: relacionbaunit relacionbaunit_unidad1_predio_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionbaunit
    ADD CONSTRAINT relacionbaunit_unidad1_predio_fkey FOREIGN KEY (unidad1_predio) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12065 (class 2606 OID 338261)
-- Name: relacionbaunit relacionbaunit_unidad2_la_baunit_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionbaunit
    ADD CONSTRAINT relacionbaunit_unidad2_la_baunit_fkey FOREIGN KEY (unidad2_la_baunit) REFERENCES interlis_ili2db3_ladm.la_baunit(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12066 (class 2606 OID 338266)
-- Name: relacionbaunit relacionbaunit_unidad2_predio_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionbaunit
    ADD CONSTRAINT relacionbaunit_unidad2_predio_fkey FOREIGN KEY (unidad2_predio) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12067 (class 2606 OID 338271)
-- Name: relacionfuente relacionfuente_refuente_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionfuente
    ADD CONSTRAINT relacionfuente_refuente_fkey FOREIGN KEY (refuente) REFERENCES interlis_ili2db3_ladm.col_fuenteadministrativa(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12068 (class 2606 OID 338276)
-- Name: relacionfuente relacionfuente_relacionrequeridabaunit_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionfuente
    ADD CONSTRAINT relacionfuente_relacionrequeridabaunit_fkey FOREIGN KEY (relacionrequeridabaunit) REFERENCES interlis_ili2db3_ladm.la_relacionnecesariabaunits(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12069 (class 2606 OID 338281)
-- Name: relacionfuenteuespacial relacionfuenteuespacial_relacionrequeridaue_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionfuenteuespacial
    ADD CONSTRAINT relacionfuenteuespacial_relacionrequeridaue_fkey FOREIGN KEY (relacionrequeridaue) REFERENCES interlis_ili2db3_ladm.la_relacionnecesariaunidadesespaciales(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12070 (class 2606 OID 338286)
-- Name: relacionfuenteuespacial relacionfuenteuespacial_rfuente_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionfuenteuespacial
    ADD CONSTRAINT relacionfuenteuespacial_rfuente_fkey FOREIGN KEY (rfuente) REFERENCES interlis_ili2db3_ladm.col_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12071 (class 2606 OID 338291)
-- Name: relacionue relacionue_rue1_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue1_construccion_fkey FOREIGN KEY (rue1_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12072 (class 2606 OID 338296)
-- Name: relacionue relacionue_rue1_la_espacjrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue1_la_espacjrdcrdsrvcios_fkey FOREIGN KEY (rue1_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12073 (class 2606 OID 338301)
-- Name: relacionue relacionue_rue1_la_espcjrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue1_la_espcjrdcndddfccion_fkey FOREIGN KEY (rue1_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12074 (class 2606 OID 338306)
-- Name: relacionue relacionue_rue1_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue1_la_unidadespacial_fkey FOREIGN KEY (rue1_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12075 (class 2606 OID 338311)
-- Name: relacionue relacionue_rue1_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue1_servidumbrepaso_fkey FOREIGN KEY (rue1_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12076 (class 2606 OID 338316)
-- Name: relacionue relacionue_rue1_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue1_terreno_fkey FOREIGN KEY (rue1_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12077 (class 2606 OID 338321)
-- Name: relacionue relacionue_rue1_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue1_unidadconstruccion_fkey FOREIGN KEY (rue1_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12078 (class 2606 OID 338326)
-- Name: relacionue relacionue_rue2_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue2_construccion_fkey FOREIGN KEY (rue2_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12079 (class 2606 OID 338331)
-- Name: relacionue relacionue_rue2_la_espacjrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue2_la_espacjrdcrdsrvcios_fkey FOREIGN KEY (rue2_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12080 (class 2606 OID 338336)
-- Name: relacionue relacionue_rue2_la_espcjrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue2_la_espcjrdcndddfccion_fkey FOREIGN KEY (rue2_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12081 (class 2606 OID 338341)
-- Name: relacionue relacionue_rue2_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue2_la_unidadespacial_fkey FOREIGN KEY (rue2_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12082 (class 2606 OID 338346)
-- Name: relacionue relacionue_rue2_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue2_servidumbrepaso_fkey FOREIGN KEY (rue2_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12083 (class 2606 OID 338351)
-- Name: relacionue relacionue_rue2_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue2_terreno_fkey FOREIGN KEY (rue2_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12084 (class 2606 OID 338356)
-- Name: relacionue relacionue_rue2_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.relacionue
    ADD CONSTRAINT relacionue_rue2_unidadconstruccion_fkey FOREIGN KEY (rue2_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12085 (class 2606 OID 338361)
-- Name: responsablefuente responsablefuente_cfuente_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.responsablefuente
    ADD CONSTRAINT responsablefuente_cfuente_fkey FOREIGN KEY (cfuente) REFERENCES interlis_ili2db3_ladm.col_fuenteadministrativa(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12086 (class 2606 OID 338366)
-- Name: responsablefuente responsablefuente_notario_col_interesado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.responsablefuente
    ADD CONSTRAINT responsablefuente_notario_col_interesado_fkey FOREIGN KEY (notario_col_interesado) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12087 (class 2606 OID 338371)
-- Name: responsablefuente responsablefuente_notario_la_agrupcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.responsablefuente
    ADD CONSTRAINT responsablefuente_notario_la_agrupcn_ntrsdos_fkey FOREIGN KEY (notario_la_agrupacion_interesados) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12088 (class 2606 OID 338376)
-- Name: rrrfuente rrrfuente_rfuente_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.rrrfuente
    ADD CONSTRAINT rrrfuente_rfuente_fkey FOREIGN KEY (rfuente) REFERENCES interlis_ili2db3_ladm.col_fuenteadministrativa(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12089 (class 2606 OID 338381)
-- Name: rrrfuente rrrfuente_rrr_col_derecho_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.rrrfuente
    ADD CONSTRAINT rrrfuente_rrr_col_derecho_fkey FOREIGN KEY (rrr_col_derecho) REFERENCES interlis_ili2db3_ladm.col_derecho(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12090 (class 2606 OID 338386)
-- Name: rrrfuente rrrfuente_rrr_col_hipoteca_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.rrrfuente
    ADD CONSTRAINT rrrfuente_rrr_col_hipoteca_fkey FOREIGN KEY (rrr_col_hipoteca) REFERENCES interlis_ili2db3_ladm.col_hipoteca(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12091 (class 2606 OID 338391)
-- Name: rrrfuente rrrfuente_rrr_col_responsabilidad_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.rrrfuente
    ADD CONSTRAINT rrrfuente_rrr_col_responsabilidad_fkey FOREIGN KEY (rrr_col_responsabilidad) REFERENCES interlis_ili2db3_ladm.col_responsabilidad(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12092 (class 2606 OID 338396)
-- Name: rrrfuente rrrfuente_rrr_col_restriccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.rrrfuente
    ADD CONSTRAINT rrrfuente_rrr_col_restriccion_fkey FOREIGN KEY (rrr_col_restriccion) REFERENCES interlis_ili2db3_ladm.col_restriccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12093 (class 2606 OID 338401)
-- Name: servidumbrepaso servidumbrepaso_nivel_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.servidumbrepaso
    ADD CONSTRAINT servidumbrepaso_nivel_fkey FOREIGN KEY (nivel) REFERENCES interlis_ili2db3_ladm.la_nivel(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12094 (class 2606 OID 338406)
-- Name: servidumbrepaso servidumbrepaso_uej2_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.servidumbrepaso
    ADD CONSTRAINT servidumbrepaso_uej2_construccion_fkey FOREIGN KEY (uej2_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12095 (class 2606 OID 338411)
-- Name: servidumbrepaso servidumbrepaso_uej2_la_espacjrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.servidumbrepaso
    ADD CONSTRAINT servidumbrepaso_uej2_la_espacjrdcrdsrvcios_fkey FOREIGN KEY (uej2_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12096 (class 2606 OID 338416)
-- Name: servidumbrepaso servidumbrepaso_uej2_la_espcjrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.servidumbrepaso
    ADD CONSTRAINT servidumbrepaso_uej2_la_espcjrdcndddfccion_fkey FOREIGN KEY (uej2_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12097 (class 2606 OID 338421)
-- Name: servidumbrepaso servidumbrepaso_uej2_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.servidumbrepaso
    ADD CONSTRAINT servidumbrepaso_uej2_la_unidadespacial_fkey FOREIGN KEY (uej2_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12098 (class 2606 OID 338426)
-- Name: servidumbrepaso servidumbrepaso_uej2_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.servidumbrepaso
    ADD CONSTRAINT servidumbrepaso_uej2_servidumbrepaso_fkey FOREIGN KEY (uej2_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12099 (class 2606 OID 338431)
-- Name: servidumbrepaso servidumbrepaso_uej2_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.servidumbrepaso
    ADD CONSTRAINT servidumbrepaso_uej2_terreno_fkey FOREIGN KEY (uej2_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12100 (class 2606 OID 338436)
-- Name: servidumbrepaso servidumbrepaso_uej2_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.servidumbrepaso
    ADD CONSTRAINT servidumbrepaso_uej2_unidadconstruccion_fkey FOREIGN KEY (uej2_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12101 (class 2606 OID 338441)
-- Name: t_ili2db_basket t_ili2db_basket_dataset_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.t_ili2db_basket
    ADD CONSTRAINT t_ili2db_basket_dataset_fkey FOREIGN KEY (dataset) REFERENCES interlis_ili2db3_ladm.t_ili2db_dataset(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12102 (class 2606 OID 338446)
-- Name: t_ili2db_import_basket t_ili2db_import_basket_basket_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.t_ili2db_import_basket
    ADD CONSTRAINT t_ili2db_import_basket_basket_fkey FOREIGN KEY (basket) REFERENCES interlis_ili2db3_ladm.t_ili2db_basket(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12103 (class 2606 OID 338451)
-- Name: t_ili2db_import_basket t_ili2db_import_basket_import_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.t_ili2db_import_basket
    ADD CONSTRAINT t_ili2db_import_basket_import_fkey FOREIGN KEY (import) REFERENCES interlis_ili2db3_ladm.t_ili2db_import(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12104 (class 2606 OID 338456)
-- Name: terreno terreno_nivel_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.terreno
    ADD CONSTRAINT terreno_nivel_fkey FOREIGN KEY (nivel) REFERENCES interlis_ili2db3_ladm.la_nivel(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12105 (class 2606 OID 338461)
-- Name: terreno terreno_uej2_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.terreno
    ADD CONSTRAINT terreno_uej2_construccion_fkey FOREIGN KEY (uej2_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12106 (class 2606 OID 338466)
-- Name: terreno terreno_uej2_la_espacjrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.terreno
    ADD CONSTRAINT terreno_uej2_la_espacjrdcrdsrvcios_fkey FOREIGN KEY (uej2_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12107 (class 2606 OID 338471)
-- Name: terreno terreno_uej2_la_espcjrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.terreno
    ADD CONSTRAINT terreno_uej2_la_espcjrdcndddfccion_fkey FOREIGN KEY (uej2_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12108 (class 2606 OID 338476)
-- Name: terreno terreno_uej2_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.terreno
    ADD CONSTRAINT terreno_uej2_la_unidadespacial_fkey FOREIGN KEY (uej2_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12109 (class 2606 OID 338481)
-- Name: terreno terreno_uej2_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.terreno
    ADD CONSTRAINT terreno_uej2_servidumbrepaso_fkey FOREIGN KEY (uej2_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12110 (class 2606 OID 338486)
-- Name: terreno terreno_uej2_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.terreno
    ADD CONSTRAINT terreno_uej2_terreno_fkey FOREIGN KEY (uej2_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12111 (class 2606 OID 338491)
-- Name: terreno terreno_uej2_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.terreno
    ADD CONSTRAINT terreno_uej2_unidadconstruccion_fkey FOREIGN KEY (uej2_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12112 (class 2606 OID 338496)
-- Name: topografofuente topografofuente_sfuente_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.topografofuente
    ADD CONSTRAINT topografofuente_sfuente_fkey FOREIGN KEY (sfuente) REFERENCES interlis_ili2db3_ladm.col_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12113 (class 2606 OID 338501)
-- Name: topografofuente topografofuente_topografo_col_interesado_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.topografofuente
    ADD CONSTRAINT topografofuente_topografo_col_interesado_fkey FOREIGN KEY (topografo_col_interesado) REFERENCES interlis_ili2db3_ladm.col_interesado(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12114 (class 2606 OID 338506)
-- Name: topografofuente topografofuente_topografo_la_grpcn_ntrsdos_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.topografofuente
    ADD CONSTRAINT topografofuente_topografo_la_grpcn_ntrsdos_fkey FOREIGN KEY (topografo_la_agrupacion_interesados) REFERENCES interlis_ili2db3_ladm.la_agrupacion_interesados(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12115 (class 2606 OID 338511)
-- Name: uebaunit uebaunit_baunit_la_baunit_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uebaunit
    ADD CONSTRAINT uebaunit_baunit_la_baunit_fkey FOREIGN KEY (baunit_la_baunit) REFERENCES interlis_ili2db3_ladm.la_baunit(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12116 (class 2606 OID 338516)
-- Name: uebaunit uebaunit_baunit_predio_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uebaunit
    ADD CONSTRAINT uebaunit_baunit_predio_fkey FOREIGN KEY (baunit_predio) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12117 (class 2606 OID 338521)
-- Name: uebaunit uebaunit_ue_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uebaunit
    ADD CONSTRAINT uebaunit_ue_construccion_fkey FOREIGN KEY (ue_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12118 (class 2606 OID 338526)
-- Name: uebaunit uebaunit_ue_la_espacijrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uebaunit
    ADD CONSTRAINT uebaunit_ue_la_espacijrdcndddfccion_fkey FOREIGN KEY (ue_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12119 (class 2606 OID 338531)
-- Name: uebaunit uebaunit_ue_la_espaciojrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uebaunit
    ADD CONSTRAINT uebaunit_ue_la_espaciojrdcrdsrvcios_fkey FOREIGN KEY (ue_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12120 (class 2606 OID 338536)
-- Name: uebaunit uebaunit_ue_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uebaunit
    ADD CONSTRAINT uebaunit_ue_la_unidadespacial_fkey FOREIGN KEY (ue_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12121 (class 2606 OID 338541)
-- Name: uebaunit uebaunit_ue_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uebaunit
    ADD CONSTRAINT uebaunit_ue_servidumbrepaso_fkey FOREIGN KEY (ue_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12122 (class 2606 OID 338546)
-- Name: uebaunit uebaunit_ue_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uebaunit
    ADD CONSTRAINT uebaunit_ue_terreno_fkey FOREIGN KEY (ue_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12123 (class 2606 OID 338551)
-- Name: uebaunit uebaunit_ue_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uebaunit
    ADD CONSTRAINT uebaunit_ue_unidadconstruccion_fkey FOREIGN KEY (ue_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12124 (class 2606 OID 338556)
-- Name: uefuente uefuente_pfuente_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uefuente
    ADD CONSTRAINT uefuente_pfuente_fkey FOREIGN KEY (pfuente) REFERENCES interlis_ili2db3_ladm.col_fuenteespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12125 (class 2606 OID 338561)
-- Name: uefuente uefuente_ue_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uefuente
    ADD CONSTRAINT uefuente_ue_construccion_fkey FOREIGN KEY (ue_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12126 (class 2606 OID 338566)
-- Name: uefuente uefuente_ue_la_espacijrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uefuente
    ADD CONSTRAINT uefuente_ue_la_espacijrdcndddfccion_fkey FOREIGN KEY (ue_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12127 (class 2606 OID 338571)
-- Name: uefuente uefuente_ue_la_espaciojrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uefuente
    ADD CONSTRAINT uefuente_ue_la_espaciojrdcrdsrvcios_fkey FOREIGN KEY (ue_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12128 (class 2606 OID 338576)
-- Name: uefuente uefuente_ue_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uefuente
    ADD CONSTRAINT uefuente_ue_la_unidadespacial_fkey FOREIGN KEY (ue_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12129 (class 2606 OID 338581)
-- Name: uefuente uefuente_ue_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uefuente
    ADD CONSTRAINT uefuente_ue_servidumbrepaso_fkey FOREIGN KEY (ue_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12130 (class 2606 OID 338586)
-- Name: uefuente uefuente_ue_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uefuente
    ADD CONSTRAINT uefuente_ue_terreno_fkey FOREIGN KEY (ue_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12131 (class 2606 OID 338591)
-- Name: uefuente uefuente_ue_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.uefuente
    ADD CONSTRAINT uefuente_ue_unidadconstruccion_fkey FOREIGN KEY (ue_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12132 (class 2606 OID 338596)
-- Name: ueuegrupo ueuegrupo_parte_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ueuegrupo
    ADD CONSTRAINT ueuegrupo_parte_construccion_fkey FOREIGN KEY (parte_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12133 (class 2606 OID 338601)
-- Name: ueuegrupo ueuegrupo_parte_la_espcjrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ueuegrupo
    ADD CONSTRAINT ueuegrupo_parte_la_espcjrdcrdsrvcios_fkey FOREIGN KEY (parte_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12134 (class 2606 OID 338606)
-- Name: ueuegrupo ueuegrupo_parte_la_spcjrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ueuegrupo
    ADD CONSTRAINT ueuegrupo_parte_la_spcjrdcndddfccion_fkey FOREIGN KEY (parte_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12135 (class 2606 OID 338611)
-- Name: ueuegrupo ueuegrupo_parte_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ueuegrupo
    ADD CONSTRAINT ueuegrupo_parte_la_unidadespacial_fkey FOREIGN KEY (parte_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12136 (class 2606 OID 338616)
-- Name: ueuegrupo ueuegrupo_parte_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ueuegrupo
    ADD CONSTRAINT ueuegrupo_parte_servidumbrepaso_fkey FOREIGN KEY (parte_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12137 (class 2606 OID 338621)
-- Name: ueuegrupo ueuegrupo_parte_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ueuegrupo
    ADD CONSTRAINT ueuegrupo_parte_terreno_fkey FOREIGN KEY (parte_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12138 (class 2606 OID 338626)
-- Name: ueuegrupo ueuegrupo_parte_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ueuegrupo
    ADD CONSTRAINT ueuegrupo_parte_unidadconstruccion_fkey FOREIGN KEY (parte_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12139 (class 2606 OID 338631)
-- Name: ueuegrupo ueuegrupo_todo_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.ueuegrupo
    ADD CONSTRAINT ueuegrupo_todo_fkey FOREIGN KEY (todo) REFERENCES interlis_ili2db3_ladm.la_agrupacionunidadesespaciales(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12140 (class 2606 OID 338636)
-- Name: unidadconstruccion unidadconstruccion_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadconstruccion
    ADD CONSTRAINT unidadconstruccion_construccion_fkey FOREIGN KEY (construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12141 (class 2606 OID 338641)
-- Name: unidadconstruccion unidadconstruccion_nivel_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadconstruccion
    ADD CONSTRAINT unidadconstruccion_nivel_fkey FOREIGN KEY (nivel) REFERENCES interlis_ili2db3_ladm.la_nivel(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12142 (class 2606 OID 338646)
-- Name: unidadconstruccion unidadconstruccion_uej2_construccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadconstruccion
    ADD CONSTRAINT unidadconstruccion_uej2_construccion_fkey FOREIGN KEY (uej2_construccion) REFERENCES interlis_ili2db3_ladm.construccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12143 (class 2606 OID 338651)
-- Name: unidadconstruccion unidadconstruccion_uej2_la_espacjrdcrdsrvcios_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadconstruccion
    ADD CONSTRAINT unidadconstruccion_uej2_la_espacjrdcrdsrvcios_fkey FOREIGN KEY (uej2_la_espaciojuridicoredservicios) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicoredservicios(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12144 (class 2606 OID 338656)
-- Name: unidadconstruccion unidadconstruccion_uej2_la_espcjrdcndddfccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadconstruccion
    ADD CONSTRAINT unidadconstruccion_uej2_la_espcjrdcndddfccion_fkey FOREIGN KEY (uej2_la_espaciojuridicounidadedificacion) REFERENCES interlis_ili2db3_ladm.la_espaciojuridicounidadedificacion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12145 (class 2606 OID 338661)
-- Name: unidadconstruccion unidadconstruccion_uej2_la_unidadespacial_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadconstruccion
    ADD CONSTRAINT unidadconstruccion_uej2_la_unidadespacial_fkey FOREIGN KEY (uej2_la_unidadespacial) REFERENCES interlis_ili2db3_ladm.la_unidadespacial(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12146 (class 2606 OID 338666)
-- Name: unidadconstruccion unidadconstruccion_uej2_servidumbrepaso_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadconstruccion
    ADD CONSTRAINT unidadconstruccion_uej2_servidumbrepaso_fkey FOREIGN KEY (uej2_servidumbrepaso) REFERENCES interlis_ili2db3_ladm.servidumbrepaso(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12147 (class 2606 OID 338671)
-- Name: unidadconstruccion unidadconstruccion_uej2_terreno_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadconstruccion
    ADD CONSTRAINT unidadconstruccion_uej2_terreno_fkey FOREIGN KEY (uej2_terreno) REFERENCES interlis_ili2db3_ladm.terreno(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12148 (class 2606 OID 338676)
-- Name: unidadconstruccion unidadconstruccion_uej2_unidadconstruccion_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadconstruccion
    ADD CONSTRAINT unidadconstruccion_uej2_unidadconstruccion_fkey FOREIGN KEY (uej2_unidadconstruccion) REFERENCES interlis_ili2db3_ladm.unidadconstruccion(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12149 (class 2606 OID 338681)
-- Name: unidadfuente unidadfuente_ufuente_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadfuente
    ADD CONSTRAINT unidadfuente_ufuente_fkey FOREIGN KEY (ufuente) REFERENCES interlis_ili2db3_ladm.col_fuenteadministrativa(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12150 (class 2606 OID 338686)
-- Name: unidadfuente unidadfuente_unidad_la_baunit_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadfuente
    ADD CONSTRAINT unidadfuente_unidad_la_baunit_fkey FOREIGN KEY (unidad_la_baunit) REFERENCES interlis_ili2db3_ladm.la_baunit(t_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 12151 (class 2606 OID 338691)
-- Name: unidadfuente unidadfuente_unidad_predio_fkey; Type: FK CONSTRAINT; Schema: interlis_ili2db3_ladm; Owner: postgres
--

ALTER TABLE ONLY interlis_ili2db3_ladm.unidadfuente
    ADD CONSTRAINT unidadfuente_unidad_predio_fkey FOREIGN KEY (unidad_predio) REFERENCES interlis_ili2db3_ladm.predio(t_id) DEFERRABLE INITIALLY DEFERRED;


-- Completed on 2020-07-15 12:37:29 -05

--
-- PostgreSQL database dump complete
--

