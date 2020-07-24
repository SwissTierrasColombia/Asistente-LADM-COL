# Acerca de

Complemento para [QGIS](http://qgis.org) que permite crear y mantener datos conformes con [LADM-COL](https://github.com/SwissTierrasColombia/LADM-COL), así  como importar, visualizar, capturar, consultar, transformar (mediante  ETLs), validar y generar archivos de intercambio de [INTERLIS](http://www.interlis.ch/index_e.htm) (.XTF). Se integra al Sistema de Transición para realizar tareas que requieren análisis y validación de datos espaciales.

Licencia: [GNU General Public License v3.0](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/blob/master/LICENSE)

Enlaces de interés: [Documentación](https://swisstierrascolombia.github.io/Asistente-LADM-COL), [Galería](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/blob/master/README.md#galería)

Un proyecto de: [SwissTierras Colombia](https://swisstierrascolombia.com/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE S.A.S](http://www.incige.com/))

## Soporte de funcionalidades por motor de base de datos

La versión actual ([3.1.0](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/releases/tag/3.1.0)) del Asistente LADM-COL depende del plugin [QGIS Model Baker v6.1.1.4](https://github.com/SwissTierrasColombia/QgisModelBaker/releases/download/v6.1.1.4/QgisModelBaker_6114.zip) y soporta los motores de Base de Datos PostgreSQL/PostGIS, GeoPackage y SQL Server.

Este es el soporte funcional para cada motor:

| Módulos                           | PostgreSQL/PostGIS |        GeoPackage        |        MS SQL Server        |
| --------------------------------- | :----------------: | :----------------------: | :-------------------------: |
| Administración de datos           |         Si         |            Si            |            Si               |
| Captura y estructuración de datos |         Si         |            Si            |            Parcial          |
| Cargar capas                      |         Si         |            Si            |            Si               |
| Gestión de insumos                |         Si         |            Si            |            No               |
| Validaciones de calidad           |         Si         |            Si            |            Si               |
| Consultas                         |         Si         |            Si            |            Si               |
| Reportes                          |         Si         |            No            |            No               |
| Identificación de novedades       |         Si         |            Si            |            Parcial          |
| Sistema de Transición             |         Si         |            Si            |            Si               |

## Funcionalidades

#### Administración de datos

  - Crear estructura de base de datos conforme al modelo LADM-COL v3.0.
  - Importar datos desde archivo de transferencia (.XTF).
  - Exportar datos a archivo de transferencia (.XTF).
  - Importar/exportar datos desde y hacia archivos de transferencia (.XTF) desactivando la validación de los mismos. 
  - Soporte de tres motores para manejar datos de LADM-COL:
    - :elephant: PostgreSQL/PostGIS: Soporte total.
    - :package: GeoPackage: Soporte total, exceptuando el módulo de reportes.
    - SQL Server: Soporte parcial. Gestión de insumos y reportes no están soportados.

#### Captura y estructuración de datos

+ Capturar datos para el modelo de aplicación de Levantamiento Catastral v1.0 ([descargar](https://github.com/SwissTierrasColombia/LADM_COL/releases/download/1.0/Modelo_Aplicacion_LADMCOL_Levantamiento_Catastral_V1_0.zip)).

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
   
  - Importar datos alfanuméricos desde [estructura intermedia en Excel](https://github.com/SwissTierrasColombia/Asistente-LADM-COL/blob/master/asistente_ladm_col/resources/excel/datos_estructura_excel.xlsx).
  - Configurar valores automáticos para campos `t_ili_tid`, `espacio_de_nombres` y `local_id`.
  - Usar estilos preconfigurados en archivos QML para asignarlos a las capas cargadas.

#### Cargar capas

+ Seleccionar en un diálogo las capas a cargar de cualquier modelo de la base de datos o esquema:

- Usar el plugin 'QGIS Model Baker' para cargar capas con formularios, relaciones y dominios configurados.

- Cargar conjuntos de capas preconfigurados.


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

## Galería

 + Reglas de Calidad![Reglas de Calidad](https://s3.amazonaws.com/media-p.slid.es/uploads/308098/images/6343636/quality_rules_25-min.gif)

+ Consultas

  ![Consultas](https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6290636/query_25.gif)

+ Reportes

  ![Reportes](https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6290657/report_25.gif)

+ Identificación de Novedades

  ![Identificación de Novedades](https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6293473/novedades_short_40_slides.gif)

+ Integración con el Sistema de Transición

  ![insumos](https://user-images.githubusercontent.com/27906888/83693002-b6f17900-a5ba-11ea-8d62-0ed25b2a7cfe.gif)
