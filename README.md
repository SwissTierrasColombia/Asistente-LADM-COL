[![License](https://img.shields.io/github/license/AgenciaImplementacion/Asistente-LADM_COL.svg)](https://tldrlegal.com/license/gnu-general-public-license-v3-%28gpl-3%29)
[![Release](https://img.shields.io/github/release/AgenciaImplementacion/asistente-ladm_col.svg)](https://github.com/AgenciaImplementacion/asistente-ladm_col/releases)
[![Build Status](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL.svg?branch=master)](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL)

You can read the docs in [English](README_en.md).

# Asistente LADM_COL
Plugin de [QGIS](http://qgis.org) que ayuda a capturar y mantener datos conformes con [LADM_COL](https://github.com/AgenciaImplementacion/LADM_COL) y a generar archivos de intercambio de [INTERLIS](http://www.interlis.ch/index_e.htm) (.XTF).

Licencia: [GNU General Public License v3.0](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/LICENSE)


Un proyecto de: [Agencia de Implementación](https://www.proadmintierra.info/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE S.A.S](http://www.incige.com/))



## Funcionalidades

La versión actual (0.0.4) del Asistente LADM_COL depende del plugin [Project Generator](https://github.com/opengisch/projectgenerator/) [v2.0.1.1](https://github.com/AgenciaImplementacion/projectgenerator/releases/tag/2.0.1.1) y permite:

 - Capturar datos para el modelo LADM_COL v2.2.1.
 - Agregar puntos a las capas `Punto Lindero` y `Punto Levantamiento` desde archivo CSV.
   - Validar para evitar insertar puntos superpuestos.
 - Definir `Linderos` digitalizando sobre el mapa.
   - Ayudas para la digitalización:
     - Configuración automática de snapping y de valores predeterminados para campos.
     - Partir líneas seleccionadas por segmento.
     - Unir líneas seleccionadas.
 - Crear `Terrenos`:
   - A partir de linderos seleccionados.
   - A partir de una capa fuente con la misma estructura de campos.
 - Llenar automáticamente tablas de topología:
   - `PuntosCCL` (relaciona `Punto Lindero` y `Lindero`)
   - `MasCCL`    (relaciona `Lindero` y `Terreno`)
   - `Menos`     (relaciona `Terreno` y sus anillos/huecos internos)
 - Crear `Predios` a partir de `Terrrenos` existentes.
 - Revisar segmentos de linderos muy largos (que superen una tolerancia dada).
 - Usar el plugin 'Project Generator' (una dependencia) para cargar capas con formularios y relaciones configuradas.
 - Usar estilos preconfigurados para asignarlos a las capas cargadas.

## Pruebas automatizadas al software

Esta se ejecutan automáticamente en cada commit realizado al repositorio y los resultados de estos están disponibles en:

- Linux: https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL
- Windows: http://portal.proadmintierra.info:18000/

Para ejecutar las pruebas localmente se necesita tener instalado *docker* y *docker-compose*.
Se recomienda:
- Descargar *docker* desde el [sitio oficial](https://www.docker.com/community-edition#/download). Por ejemplo, para Ubuntu/Linux_Mint pueden seguirse los pasos descritos en [Install using the convenience script](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-convenience-script).
- Instalar *docker-compose* usando los [binarios](https://github.com/docker/compose/releases/tag/1.18.0).

El comando para ejecutar las pruebas es:
```sh
docker-compose run --rm qgis
```

## Pasos para traducir al español

 + Si se han agregado archivos .py o .ui al código fuente, actualizar el archivo `asistente_ladm_col/i18n/Asistente-LADM_COL.pro`.
 + En la terminal de comandos, y desde la carpeta *Asistente-LADM_COL*, ejecutar
`lupdate asistente_ladm_col/i18n/Asistente-LADM_COL.pro` (lo cual actualiza el archivo de cadenas de traducción `asistente_ladm_col/i18n/Asistente-LADM_COL_es.ts`)
 + Abrir el programa *Qt-Linguist* y cargar el archivo  `asistente_ladm_col/i18n/Asistente-LADM_COL_es.ts`
 + Editar las cadenas de texto traducibles y guardar el archivo.
 + Ir a la carpeta *asistente_ladm_col* y ejecutar:
 `make` (esto ejecuta a su vez el comando `lrelease`, el cual genera un archivo binario con extensión .qm)

NOTA: El archivo .qm no se versiona, pero hará parte del release del plugin.
