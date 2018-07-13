[![License](https://img.shields.io/github/license/AgenciaImplementacion/Asistente-LADM_COL.svg)](https://tldrlegal.com/license/gnu-general-public-license-v3-%28gpl-3%29)
[![Release](https://img.shields.io/github/release/AgenciaImplementacion/asistente-ladm_col.svg)](https://github.com/AgenciaImplementacion/asistente-ladm_col/releases)
[![Build Status](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL.svg?branch=master)](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL)
[![Build Status](http://portal.proadmintierra.info:18000/status.svg?branch=master)](http://portal.proadmintierra.info:18000)

You can read the docs in [English](README_en.md).

# Asistente LADM_COL
Plugin de [QGIS](http://qgis.org) que ayuda a capturar y mantener datos conformes con [LADM_COL](https://github.com/AgenciaImplementacion/LADM_COL) y a generar archivos de intercambio de [INTERLIS](http://www.interlis.ch/index_e.htm) (.XTF).

Licencia: [GNU General Public License v3.0](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/LICENSE)


Un proyecto de: [Agencia de Implementación](https://www.proadmintierra.info/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE S.A.S](http://www.incige.com/))

 :arrow_right: Se recomienda utilizar la versión de QGIS más reciente, disponible en https://qgis.org/downloads/weekly/


## Funcionalidades

La versión actual ([0.5.0](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/releases/tag/0.5.0)) del Asistente LADM_COL depende del plugin [Project Generator](https://github.com/opengisch/projectgenerator/) v3.2.3 (o superior) y permite:

 - Capturar datos para el modelo LADM_COL v2.2.1.
 - Preprocesar puntos: Medición controlada.
   - Agrupamiento de puntos por cercanía.
   - Cálculo de posición promediada para puntos del mismo grupo.
 - Agregar puntos a las capas `Punto Lindero`, `Punto Levantamiento` y `Punto Control`:
   - Desde archivo CSV con la estructura requerida.
     - Validar para evitar insertar puntos superpuestos.
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
 - Agregar `Linderos`:
   - Digitalizando sobre el mapa.
     - Ayudas para la digitalización:
       - Configuración automática de snapping y de valores predeterminados para campos.
       - Partir líneas seleccionadas por segmento.
       - Unir líneas seleccionadas.
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Terrenos`:
   - A partir de linderos seleccionados.
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
 - Llenar automáticamente tablas de topología:
   - `PuntosCCL` (relaciona `Punto Lindero` y `Lindero`)
   - `MasCCL`    (relaciona `Lindero` y `Terreno`)
   - `Menos`     (relaciona `Terreno` y sus anillos/huecos internos)
 - Crear `Construcciones` y `Ùnidades de Construcción`:
   - Digitalizando sobre el mapa.
     - Ayudas para la digitalización:
       - Configuración automática de snapping y de valores predeterminados para campos.
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Predios`:
   - A partir de `Terrenos` existentes.
   - Desde otra tabla con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Interesados Naturales` e `Interesados Jurídicos`:
   - Usando formularios preconfigurados.
   - Desde otra tabla con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Fuente Espacial` y `Fuente Administrativa`:
   - Usando formularios preconfigurados.
     - Y relacionando la nueva `Fuente Espacial` a `Terrenos`, `Linderos` o `Puntos` previamente seleccionados.
   - Desde otra tabla con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Archivos Fuente`:
   - Asociar fuentes a archivos fuente.
   - Almacenar archivos fuente en servidor en el momento de guardar cambios o
     posteriormente, de forma masiva.
 - Crear `Derechos`, `Restricciones` y `Responsabilidades` (`RRR`):
   - Usando formularios preconfigurados (relacionando el nuevo objeto a `Fuentes Administrativas` previamente seleccionadas).
   - Desde otra tabla con cualquier estructura, definiendo un mapeo de campos.
 - Seleccionar en un diálogo las capas a cargar de cualquier modelo de la base de datos o esquema:
   - Usar el plugin 'Project Generator' para cargar capas con formularios, relaciones y dominios configurados.
   - Cargar conjuntos de capas preconfigurados.
 - Realizar revisiones de calidad:
   - Revisar segmentos de linderos muy largos (que superen una tolerancia dada).
   - Revisar superposiciones en `Punto Lindero`.
   - Revisar superposiciones en `Punto de Control`.
   - Revisar superposiciones en `Lindero`.
   - Revisar superposiciones en `Terreno`.
   - Revisar nodos de `Lindero` sin `Punto Lindero` asociado.
   - Revisar nodos de `Lindero` no conectados.
   - Revisar nodos de `Construcción` sin `Punto Levantamiento` asociado.
 - Configurar valores automáticos para campos `espacio_de_nombres` y `local_id`.
 - Usar estilos preconfigurados en archivos QML para asignarlos a las capas cargadas.
 - Visualizar GIFs ilustrativos en la ayuda online del plugin o descargarlos para trabajo offline.

## Pruebas automatizadas al software

Éstas se ejecutan automáticamente luego de cada commit realizado al repositorio y los resultados están disponibles en:

- GNU/Linux: https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL
- Windows: http://portal.proadmintierra.info:18000/

Para ejecutar las pruebas localmente se necesita tener instalado *docker* y *docker-compose*.
Se recomienda:
- Descargar *docker* desde el [sitio oficial](https://www.docker.com/community-edition#/download). Por ejemplo, para Ubuntu/Linux_Mint pueden seguirse los pasos descritos en [Install using the convenience script](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-convenience-script).
- Instalar *docker-compose* usando los [binarios](https://github.com/docker/compose/releases/tag/1.18.0).

El comando para ejecutar las pruebas es (ejecutar desde la raíz del repositorio):
```sh
docker-compose run --rm qgis
```

En caso de requerir recrear la imagen de docker se puede ejecutar:
```sh
docker-compose down --rmi local && docker-compose build
```

## Pasos para traducir al español

 + Si se han agregado archivos .py o .ui al código fuente, actualizar el archivo `asistente_ladm_col/i18n/Asistente-LADM_COL.pro`.
 + Ir a la carpeta *asistente_ladm_col* y ejecutar:
`make update_translations` (lo cual actualiza el archivo de cadenas de traducción `asistente_ladm_col/i18n/Asistente-LADM_COL_es.ts`)
 + Abrir el programa *Qt-Linguist* y cargar el archivo  `asistente_ladm_col/i18n/Asistente-LADM_COL_es.ts`
 + Editar las cadenas de texto traducibles y guardar el archivo.
 + Ir a la carpeta *asistente_ladm_col* y ejecutar:
 `make` (esto ejecuta a su vez el comando `lrelease`, el cual genera un archivo binario con extensión .qm)

NOTA: El archivo .qm no se versiona, pero hará parte del release del plugin.
