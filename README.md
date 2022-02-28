[![License](https://img.shields.io/github/license/SwissTierrasColombia/Asistente-LADM-COL.svg)](https://tldrlegal.com/license/gnu-general-public-license-v3-%28gpl-3%29)
[![Release](https://img.shields.io/github/release/SwissTierrasColombia/Asistente-LADM-COL.svg)](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/releases)
[![Continuous integration](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/actions/workflows/main.yml/badge.svg)](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/actions/workflows/main.yml)

You can read the docs in [English](README_en.md).

# Asistente LADM-COL
Complemento para [QGIS](http://qgis.org) que permite crear y mantener datos conformes con [LADM-COL](https://github.com/SwissTierrasColombia/LADM-COL), así  como importar, visualizar, capturar, consultar, transformar (mediante  ETLs), validar y generar archivos de intercambio de [INTERLIS](http://www.interlis.ch/index_e.htm) (.XTF). Se integra al Sistema de Transición para realizar tareas que requieren análisis y validación de datos espaciales.

Licencia: [GNU General Public License v3.0](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/blob/master/LICENSE)

Enlaces de interés: [Documentación](https://swisstierrascolombia.github.io/Asistente-LADM-COL), [Galería](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/blob/master/README.md#galería)

Un proyecto de: [SwissTierras Colombia](https://swisstierrascolombia.com/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE S.A.S](http://www.incige.com/))


:arrow_right: Con la versión actual del Asistente LADM-COL, te sugerimos utilizar QGIS v3.22.0 o superior, disponibles en https://qgis.org/downloads/

## Soporte de funcionalidades por motor de base de datos

La versión actual ([4.0.0-beta](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/releases/tag/4.0.0-beta)) del Asistente LADM-COL soporta los motores de Base de Datos PostgreSQL/PostGIS, GeoPackage y SQL Server.

Este es el soporte funcional para cada motor: 

| Módulos                                                      | PostgreSQL/PostGIS |        GeoPackage        |        MS SQL Server        |
| ------------------------------------------------------------ | :----------------: | :----------------------: | :-------------------------: |
| [Administración de datos](https://github.com/SwissTierrasColombia/Asistente-LADM-COL#administraci%C3%B3n-de-datos) | :heavy_check_mark: |    :heavy_check_mark:    |     :heavy_check_mark:      |
| [Captura y estructuración de datos](https://github.com/SwissTierrasColombia/Asistente-LADM-COL#captura-y-estructuraci%C3%B3n-de-datos) | :heavy_check_mark: |    :heavy_check_mark:    | :heavy_check_mark::warning: |
| [Cargar capas](https://github.com/SwissTierrasColombia/Asistente-LADM-COL#cargar-capas) | :heavy_check_mark: |    :heavy_check_mark:    |     :heavy_check_mark:      |
| [Gestión de insumos](https://github.com/SwissTierrasColombia/Asistente-LADM-COL#gesti%C3%B3n-de-insumos) | :heavy_check_mark: |    :heavy_check_mark:    |  :heavy_multiplication_x:   |
| [Validaciones de calidad](https://github.com/SwissTierrasColombia/Asistente-LADM-COL#validaciones-de-calidad) | :heavy_check_mark: |    :heavy_check_mark:    |     :heavy_check_mark:      |
| [Consultas](https://github.com/SwissTierrasColombia/Asistente-LADM-COL#consultas) | :heavy_check_mark: |    :heavy_check_mark:    |     :heavy_check_mark:      |
| [Reportes](https://github.com/SwissTierrasColombia/Asistente-LADM-COL#reportes) | :heavy_check_mark: | :heavy_multiplication_x: |  :heavy_multiplication_x:   |
| [Identificación de novedades](https://github.com/SwissTierrasColombia/Asistente-LADM-COL#identificaci%C3%B3n-de-novedades) | :heavy_check_mark: |    :heavy_check_mark:    | :heavy_check_mark::warning: |
| [Sistema de Transición](https://github.com/SwissTierrasColombia/Asistente-LADM-COL#sistema-de-transici%C3%B3n) | :heavy_check_mark: |    :heavy_check_mark:    |     :heavy_check_mark:      |

## Requerimientos mínimos

Para usar el Asistente LADM-COL se requiere:

 - Sistema Operativo:
   - Windows 10
   - GNU/Linux
   - macOS (soporte limitado)
 - Software base:
   - QGIS v3.22.0 - Białowieża o superior ([descargar](https://qgis.org/downloads/)).
   - Java v1.8
   - PostgreSQL 9.5 o superior (funciona con PostgreSQL 10, 11 ó 12).
   - PostGIS 2.4 o superior.
   - (Opcional) SQL Server 2012 o superior.
 - Complementos de QGIS (al instalar el Asistente LADM-COL usando el Administrador de Complementos de QGIS, las dependencias se instalarán automáticamente):
   - MapSwipe Tool v1.2
   - Invisible layers and groups v2.1

## Galería

+ Reglas de Calidad

  https://user-images.githubusercontent.com/652785/154091679-73e9e847-af89-4179-b4a8-48b2d9cf1f56.mp4

+ Consultas

  ![Consultas](https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6290636/query_25.gif)

+ Reportes

  ![Reportes](https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6290657/report_25.gif)

+ Identificación de Novedades

  ![Identificación de Novedades](https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6293473/novedades_short_40_slides.gif)

+ Integración con el Sistema de Transición

  ![insumos](https://user-images.githubusercontent.com/27906888/83693002-b6f17900-a5ba-11ea-8d62-0ed25b2a7cfe.gif)

## Funcionalidades

#### Administración de datos

  - Crear estructura de base de datos conforme al modelo LADM-COL v3.1, usando la proyección Origen Nacional (EPSG:9377).
  - Importar datos desde archivo de transferencia (.XTF).
  - Exportar datos a archivo de transferencia (.XTF).
  - Importar/exportar datos desde y hacia archivos de transferencia (.XTF) desactivando la validación de los mismos. 
  - Soporte de tres motores para manejar datos de LADM-COL:
    - :elephant: PostgreSQL/PostGIS: Soporte total.
    - :package: GeoPackage: Soporte total, exceptuando el módulo de reportes.
    - :copyright: SQL Server: Soporte parcial. Gestión de insumos y reportes no están soportados.

#### Captura y estructuración de datos

+ Capturar datos para el modelo de aplicación de Levantamiento Catastral v1.2.

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
   
  - Configurar valores automáticos para campos `t_ili_tid`, `espacio_de_nombres` y `local_id`.
  - Usar estilos preconfigurados en archivos QML para asignarlos a las capas cargadas.

#### Cargar capas

+ Seleccionar en un diálogo las capas a cargar de cualquier modelo de la base de datos o esquema.
+ Cargar capas con formularios, relaciones y dominios configurados.
+ Cargar conjuntos de capas preconfigurados.


#### Gestión de Insumos

- ETL para generar insumos catastrales a partir de datos del IGAC (fuente SNC).
- ETL para generar insumos catastrales a partir de datos del IGAC (fuente Cobol).

 - Generar reporte de Omisiones y Comisiones.

#### Validaciones de calidad

 - Realizar revisiones de calidad (topología) configurando opcionalmente una tolerancia:
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
   - Revisar que las `Unidades de Construcción` estén dentro de su `Construcción` correspondiente.
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

#### Consultas

 - Consultar datos LADM-COL por componentes:
   - Información Básica.
   - Información Jurídica.
   - Información de Ficha Predial.
   - Información Física.
   - Información Económica.

#### Reportes

 - Generar Informes de Colindancia con base en `Terrenos` seleccionados (Anexo 17).
 - Generar reporte 'Plano ANT' con base en `Terrenos` seleccionados.

#### Identificación de Novedades

 - Identificar novedades:

   - Comparar base de datos del barrido contra datos de insumos y evidenciar diferencias masivas y por predio tanto en el componente alfanumérico como geográfico.


#### Sistema de Transición

 - Integración con el Sistema de Transición:
   - Autenticación.
   - Gestión de tareas: consulta, iniciación, cancelación y finalización.
   - Tareas de generación de insumos catastrales.
     - ETL para generar insumos catastrales a partir de datos del IGAC (fuente SNC).
     - ETL para generar insumos catastrales a partir de datos del IGAC (fuente Cobol).
 - Soporte de roles y generación de interfaz de usuario para cada rol.

## Pruebas automatizadas y asistidas al software

### Pruebas unitarias

Éstas se ejecutan automáticamente luego de cada commit realizado al repositorio y los resultados están disponibles en:

- GNU/Linux: https://travis-ci.org/SwissTierrasColombia/Asistente-LADM-COL
- Windows: http://portal.proadmintierra.info:18000/

Para ejecutar las pruebas localmente se necesita tener instalado *docker* y *docker-compose*.
Se recomienda:
- Descargar *docker* desde el [sitio oficial](https://hub.docker.com/search/?type=edition&offering=community). Por ejemplo, para Ubuntu/Linux_Mint pueden seguirse los pasos descritos en [Install using the convenience script](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-convenience-script).
- Instalar *docker-compose* usando los [binarios](https://github.com/docker/compose/releases).
- NOTA: La [instalación](https://www.how2shout.com/how-to/how-to-install-docker-ce-on-ubuntu-20-04-lts-focal-fossa.html) en el SO Ubuntu 20.04 es más sencilla.

Antes de ejecutar las pruebas unitarias, necesitas definir estas dos variables de entorno (asegúrate de usar tu propia ruta a la raíz del repositorio para la primera variable; la segunda variable corresponde a un tag del Docker Hub oficial de QGIS):

```sh
export GITHUB_WORKSPACE=/home/Asistente-LADM-COL
export QGIS_TEST_VERSION="final-3_22_1"
```

El comando para ejecutar las pruebas es (ejecutar desde la raíz del repositorio):
```sh
docker-compose -f .docker/docker-compose.yml run --rm qgis
```

En caso de requerir recrear la imagen de docker se puede ejecutar:
```sh
docker-compose -f .docker/docker-compose.yml down --rmi local && docker-compose -f .docker/docker-compose.yml build
```

### Pruebas asistidas (para la interfaz de usuario)

El plugin Asistente LADM-COL utiliza el plugin *QGIS Tester* para soportar pruebas asistidas para funcionalidades de Interfaz de Usuario. 

Prerrequisitos:

Para correr pruebas asistidas se requiere: 

- Plugin *QGIS Tester* (disponible en: https://github.com/planetfederal/qgis-tester-plugin).
- Librería *qgiscommons*: ```pip install qgiscommons```

Revisa [la documentación](https://github.com/planetfederal/qgis-tester-plugin/blob/master/docs/source/usage.rst) para instrucciones de uso.

Si los prerrequisitos no se cumplen, el plugin Asistente LADM-COL continuará su ejecución de forma normal y dejará un mensaje de advertencia en el log de QGIS.


## Pasos para traducir al español

 + Si se han agregado archivos .py o .ui al código fuente, actualizar el archivo `asistente_ladm_col/i18n/Asistente-LADM-COL.pro`.
 + Ir a la carpeta *asistente_ladm_col* y ejecutar:
`make update_translations` (lo cual actualiza el archivo de cadenas de traducción `asistente_ladm_col/i18n/Asistente-LADM-COL_es.ts`)
 + Abrir el programa *Qt-Linguist* y cargar el archivo  `asistente_ladm_col/i18n/Asistente-LADM-COL_es.ts`
 + Editar las cadenas de texto traducibles y guardar el archivo.
 + Ir a la carpeta *asistente_ladm_col* y ejecutar:
 `make` (esto ejecuta a su vez el comando `lrelease`, el cual genera un archivo binario con extensión .qm)

NOTA: El archivo .qm no se versiona, pero hará parte del release del plugin.

## ¿Cómo recibir notificaciones de nuevas versiones del Asistente LADM-COL?

 + Si tienes cuenta de GitHub o si puedes crear una, ve a https://github.com/SwissTierrasColombia/Asistente-LADM-COL/ y haz clic en el botón `Watch` de la parte superior de la página web para seguir las novedades del repositorio.

 + Si no tienes cuenta de GitHub, tienes dos opciones:

   a) Subscríbete al *feed* de lanzamientos: https://github.com/SwissTierrasColombia/Asistente-LADM-COL/releases.atom

   b) Usa gitpunch!

      + Ve a la página https://gitpunch.com/
      + Espera a que termine la animación o haz clic en `Skip` (en la parte inferior de la página).
      + Regístrate usando tu correo electrónico.
      + Busca por "Asistente LADM-COL" y elige el repositorio `SwissTierrasColombia/Asistente-LADM-COL`.
      + Eso es todo. Después de recibir un correo que te notifique una nueva versión del plugin, pasarán unas horas hasta que el mismo esté disponible en el repositorio oficial de plugins de QGIS.
   
   