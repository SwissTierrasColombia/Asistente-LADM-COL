[![Build Status](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL.svg?branch=master)](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL)

You can read the docs in [English](README_en.md).

# Asistente LADM_COL
Plugin de [QGIS](http://qgis.org) que ayuda a capturar y mantener datos conformes con [LADM_COL](https://github.com/AgenciaImplementacion/LADM_COL) y a generar archivos de intercambio de [INTERLIS](http://www.interlis.ch/index_e.htm) (.XTF).

Licencia: [GNU General Public License v3.0](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/LICENSE)


Un proyecto de: [Agencia de Implementación](https://www.proadmintierra.info/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE S.A.S](http://www.incige.com/))



## Funcionalidades

La versión actual (0.0.2) del Asistente LADM_COL permite:

 - Capturar datos para el modelo LADM_COL v2.2.0.
 - Agregar puntos a la capa `Punto Lindero` desde archivo CSV.
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

## Pruebas automatizadas al software

Esta se ejecutan automáticamente en cada commit realizado al repositorio y los resultados de estos están disponibles en:

- Linux: https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL
- Windows: http://portal.proadmintierra.info:18000/

Para ejecutar las pruebas localmente se necesita tener instalado *docker* y *docker-compose*.
- La versión de *docker* qué usamos puede ser descargada de su [sitio oficial](https://www.docker.com/community-edition#/download), para el desarrollo usamos Ubuntu/Linux_Mint de manera qué seguimos los pasos de
[Install using the convenience script](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-convenience-script).
- La versión de *docker-compose* que usamos puede ser instalada usando los [binarios](https://github.com/docker/compose/releases/tag/1.18.0).

El comando para ejecutar las pruebas es:
```sh
docker-compose run --rm qgis
```
