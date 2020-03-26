[![License](https://img.shields.io/github/license/AgenciaImplementacion/Asistente-LADM_COL.svg)](https://tldrlegal.com/license/gnu-general-public-license-v3-%28gpl-3%29)
[![Release](https://img.shields.io/github/release/AgenciaImplementacion/asistente-ladm_col.svg)](https://github.com/AgenciaImplementacion/asistente-ladm_col/releases)
[![Build Status](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL.svg?branch=master)](https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL)
[![Build Status](http://portal.proadmintierra.info:18000/status.svg?branch=master)](http://portal.proadmintierra.info:18000)

You can read the docs in [English](README_en.md).

# Asistente LADM_COL
Plugin de [QGIS](http://qgis.org) que ayuda a capturar y mantener datos conformes con [LADM_COL](https://github.com/AgenciaImplementacion/LADM_COL) y a generar archivos de intercambio de [INTERLIS](http://www.interlis.ch/index_e.htm) (.XTF).

Licencia: [GNU General Public License v3.0](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/LICENSE)

Enlaces de interés: [Documentación](https://agenciaimplementacion.github.io/Asistente-LADM_COL), [Galería](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/README.md#galería)

Un proyecto de: [Agencia de Implementación](https://www.proadmintierra.info/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE S.A.S](http://www.incige.com/))

 :arrow_right: Se recomienda utilizar la versión 3.10.x de QGIS, disponible en https://qgis.org/downloads/


## Funcionalidades

La versión actual ([2.99.2](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/releases/tag/2.99.2)) del Asistente LADM_COL depende del plugin [QGIS Model Baker v6.0.0](https://github.com/opengisch/QgisModelBaker/releases/download/v6.0.0/qgis-model-baker.v6.0.0.zip) y permite:

 - Integración con el Sistema de Transición:
   - Autenticación.
   - Gestión de tareas: consulta, iniciación, cancelación y finalización.
   - Tareas de generación de insumos catastrales e integración asistida de insumos (soporte parcial).
     - ETL para generar insumos catastrales a partir de datos del IGAC (fuente SNC).
     - ETL para generar insumos catastrales a partir de datos del IGAC (fuente Cobol).
 - Soporte de roles y generación de interfaz de usuario para cada rol.
 - Crear estructura de base de datos conforme con el modelo LADM-COL v2.9.6.
 - Soporte de dos motores para manejar datos de LADM-COL:
   - PostgreSQL/PostGIS: Soporte total.
   - GeoPackage: Validaciones de calidad, consultas y reportes no están soportadas.
 - Capturar datos para el modelo `OPERACIÓN v2.9.6` ([descargar](https://github.com/AgenciaImplementacion/LADM_COL/releases/download/2.9.6/LADM_COL-2_9_6.zip)).
 - Importar datos desde archivo de transferencia (.XTF).
 - Exportar datos a archivo de transferencia (.XTF).
 - Importar/exportar datos desde y hacia archivos de transferencia (.XTF) desactivando la validación de los mismos. 
 - Consultar datos LADM_COL por componentes:
   - Información Básica.
   - Información Jurídica.
   - Información de Ficha Predial.
   - Información Física.
   - Información Económica.
 - Agregar puntos a las capas `Punto Lindero`, `Punto Levantamiento` y `Punto Control`:
   - Desde archivo CSV con la estructura requerida.
     - Validar para evitar insertar puntos superpuestos.
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
 - Agregar `Linderos`:
   - Digitalizando sobre el mapa.
     - Ayudas para la digitalización:
       - Configuración automática de snapping y de valores predeterminados para campos.
       - Construir linderos a partir de líneas seleccionadas (partiéndolas automáticamente por cambio de colindancia).
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Terrenos`:
   - A partir de linderos seleccionados.
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
 - Llenar automáticamente tablas de topología:
   - `PuntosCCL` (relaciona `Punto Lindero` y `Lindero`)
   - `MasCCL`    (relaciona `Lindero` y `Terreno`)
   - `Menos`     (relaciona `Terreno` y sus anillos/huecos internos)
 - Crear `Construcciones` y `Unidades de Construcción`:
   - Digitalizando sobre el mapa.
     - Ayudas para la digitalización:
       - Configuración automática de snapping y de valores predeterminados para campos.
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Servidumbres de Paso`:
   - Digitalizando sobre el mapa el polígono de la servidumbre o el eje de la misma con un ancho.
     - Ayudas para la digitalización:
       - Configuración automática de snapping y de valores predeterminados para campos.
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
   - Crear relaciones de restricciones y beneficiados.
 - Asociar direcciones a los `Terrenos`, `Construcciones` y `Unidades de Construcción`.
 - Crear `Predios`:
   - Usando formularios preconfigurados.
     - Y relacionando el nuevo `Predio` con un `Terreno` y/o una o varias `Construcciones` previamente seleccionadas.
   - Desde otra tabla con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Interesados Naturales` e `Interesados Jurídicos`:
   - Usando formularios preconfigurados.
   - Desde otra tabla con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Agrupaciones de Interesados`:
   - Usando un formulario preconfigurado.
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
   - Usar el plugin 'QGIS Model Baker' para cargar capas con formularios, relaciones y dominios configurados.
   - Cargar conjuntos de capas preconfigurados.
 - Realizar revisiones de calidad (topología):
   - Revisar superposiciones en `Punto Lindero`.
   - Revisar superposiciones en `Punto de Control`.
   - Revisar superposiciones en `Lindero`.
   - Revisar superposiciones en `Terreno`.
   - Revisar superposiciones en `Construcción`.
   - Revisar superposiciones en `Servidumbre de Paso`.
   - Revisar `Punto Lindero` sin nodo de `Lindero` asociado o con `Lindero` asociado pero relacionado de forma incorrecta en tabla `PuntoCCL`.
   - Revisar nodos de `Lindero` sin `Punto Lindero` asociado o con `Punto Lindero` asociado pero relacionado de forma incorrecta en tabla `PuntoCCL`.
   - Revisar nodos de `Lindero` no conectados.
   - Revisar que los `Linderos` siempre terminen en cambio de colindancia.
   - Revisar superposiciones entre `Servidumbre de paso` y `Construcción`.
   - Revisar que los `Terrenos` no dejen agujeros entre ellos.
   - Revisar que los límites de `Terrenos` estén cubiertos por `Linderos` y que sus relaciones estén correctamente registradas en las tablas de topología (`MasCCL` y `Menos`).
   - Revisar que los `Linderos` estén cubiertos por límites de `Terrenos` y que sus relaciones estén correctamente registradas en las tablas de topología (`MasCCL` y `Menos`).
   - Revisar geometrías multiparte en `Servidumbre de paso`.
   - Revisar que las `Construcciones` estén dentro de su `Terreno` correspondiente.
   - Revisar que las `Unidades de Construcción` estén dentro de su `Terreno` correspondiente.
 - Realizar revisiones de calidad (consistencia lógica):
   - Los predios deben tener derecho asociado y pueden tener máximo un derecho de tipo Dominio asociado.
   - No deben haber registros duplicados.
   - Las fracciones de las agrupaciones de interesados deben sumar uno (1).
   - Revisar que el campo departamento de la tabla predio tiene dos caracteres numéricos.
   - Revisar que el campo municipio de la tabla predio tiene tres caracteres numéricos.
   - Revisar que el campo zona de la tabla predio tiene dos caracteres numéricos.
   - Revisar que el número_predial tiene 30 caracteres numéricos.
   - Revisar que el número_predial_anterior tiene 20 caracteres numéricos.
   - Revisar que los atributos son apropiados para interesados naturales.
   - Revisar que los atributos son apropiados para interesados jurídicos.
   - Revisar que el tipo de Predio corresponde a la posición 22 del número_predial.
   - Revisar que las Unidades Espaciales asociadas a Predios correspondan al tipo de predio.
 - Generar reporte de revisiones de calidad.
 - Generar Informes de Colindancia con base en `Terrenos` seleccionados (Anexo 17).
 - Generar reporte 'Plano ANT' con base en `Terrenos` seleccionados.
 - Generar reporte de Omisiones y Comisiones.
 - Identificar novedades:
   - Comparar base de datos del barrido contra datos de insumos y mostrar diferencias masivas y por predio.
 - Importar datos alfanuméricos desde [estructura intermedia en Excel](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/asistente_ladm_col/resources/excel/datos_estructura_excel.xlsx).
 - Configurar valores automáticos para campos `espacio_de_nombres` y `local_id`.
 - Usar estilos preconfigurados en archivos QML para asignarlos a las capas cargadas.
 - Ayuda online y offline.

## Requerimientos mínimos

Para usar el Asistente LADM_COL se requiere:

 - Sistema Operativo:
   - Windows 8 o Windows 10
   - GNU/Linux
 - Software base:
   - QGIS v3.10.0-A Coruña o superior
   - Java v1.8
   - PostgreSQL 9.5 o superior (funciona PostgreSQL 10 y PostgreSQL 11). La versión 12 no está soportada aún.
   - PostGIS 2.4 o superior.
 - Complementos de QGIS (al instalar el Asistente LADM_COL usando el Administrador de Complementos de QGIS, las dependencias se instalarán automáticamente):
   - QGIS Model Baker v6.0.0
   - MapSwipe Tool v1.2
 
## Pruebas automatizadas y asistidas al software

### Pruebas unitarias

Éstas se ejecutan automáticamente luego de cada commit realizado al repositorio y los resultados están disponibles en:

- GNU/Linux: https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL
- Windows: http://portal.proadmintierra.info:18000/

Para ejecutar las pruebas localmente se necesita tener instalado *docker* y *docker-compose*.
Se recomienda:
- Descargar *docker* desde el [sitio oficial](https://hub.docker.com/search/?type=edition&offering=community). Por ejemplo, para Ubuntu/Linux_Mint pueden seguirse los pasos descritos en [Install using the convenience script](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-convenience-script).
- Instalar *docker-compose* usando los [binarios](https://github.com/docker/compose/releases).

El comando para ejecutar las pruebas es (ejecutar desde la raíz del repositorio):
```sh
docker-compose run --rm qgis
```

En caso de requerir recrear la imagen de docker se puede ejecutar:
```sh
docker-compose down --rmi local && docker-compose build
```

### Pruebas asistidas (para la interfaz de usuario)

El plugin Asistente LADM_COL utiliza el plugin *QGIS Tester* para soportar pruebas asistidas para funcionalidades de Interfaz de Usuario. 

Prerrequisitos:

Para correr pruebas asistidas se requiere: 

- Plugin *QGIS Tester* (disponible en: https://github.com/planetfederal/qgis-tester-plugin).
- Librería *qgiscommons*: ```pip install qgiscommons```

Revisa [la documentación](https://github.com/planetfederal/qgis-tester-plugin/blob/master/docs/source/usage.rst) para instrucciones de uso.

Si los prerrequisitos no se cumplen, el plugin Asistente LADM_COL continuará su ejecución de forma normal y dejará un mensaje de advertencia en el log de QGIS.


## Pasos para traducir al español

 + Si se han agregado archivos .py o .ui al código fuente, actualizar el archivo `asistente_ladm_col/i18n/Asistente-LADM_COL.pro`.
 + Ir a la carpeta *asistente_ladm_col* y ejecutar:
`make update_translations` (lo cual actualiza el archivo de cadenas de traducción `asistente_ladm_col/i18n/Asistente-LADM_COL_es.ts`)
 + Abrir el programa *Qt-Linguist* y cargar el archivo  `asistente_ladm_col/i18n/Asistente-LADM_COL_es.ts`
 + Editar las cadenas de texto traducibles y guardar el archivo.
 + Ir a la carpeta *asistente_ladm_col* y ejecutar:
 `make` (esto ejecuta a su vez el comando `lrelease`, el cual genera un archivo binario con extensión .qm)

NOTA: El archivo .qm no se versiona, pero hará parte del release del plugin.

## ¿Cómo recibir notificaciones de nuevas versiones del Asistente LADM_COL?

 + Si tienes cuenta de GitHub o si puedes crear una, ve a https://github.com/AgenciaImplementacion/Asistente-LADM_COL/ y haz clic en el botón `Watch` de la parte superior de la página web para seguir las novedades del repositorio.

 + Si no tienes cuenta de GitHub, tienes dos opciones:

   a) Subscríbete al *feed* de lanzamientos: https://github.com/AgenciaImplementacion/Asistente-LADM_COL/releases.atom

   b) Usa gitpunch!

      + Ve a la página https://gitpunch.com/
      + Espera a que termine la animación o haz clic en `Skip` (en la parte inferior de la página).
      + Regístrate usando tu correo electrónico.
      + Busca por "Asistente LADM_COL" y elige el repositorio `AgenciaImplementacion/Asistente-LADM_COL`.
      + Eso es todo. Después de recibir un correo que te notifique una nueva versión del plugin, pasarán unas horas hasta que el mismo esté disponible en el repositorio oficial de plugins de QGIS.
      
      
## Galería

 + Reglas de Calidad:

  ![Reglas de Calidad](https://s3.amazonaws.com/media-p.slid.es/uploads/308098/images/6343636/quality_rules_25-min.gif)

+ Consultas:

  ![Consultas](https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6290636/query_25.gif)

+ Reportes:

  ![Reportes](https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6290657/report_25.gif)

+ Identificación de Novedades:

  ![Identificación de Novedades](https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6293473/novedades_short_40_slides.gif)
      
+ Integración con Sistema de Transición

  ![insumos](https://user-images.githubusercontent.com/27906888/75196661-73b97b80-572a-11ea-8ae0-30cebccd7996.gif)
