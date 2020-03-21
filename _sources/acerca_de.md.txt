# Acerca de

Plugin de [QGIS](http://qgis.org) que ayuda a capturar y mantener datos conformes con [LADM_COL](https://github.com/AgenciaImplementacion/LADM_COL) y a generar archivos de intercambio de [INTERLIS](http://www.interlis.ch/index_e.htm) (.XTF).

Licencia: [GNU General Public License v3.0](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/LICENSE)

Enlaces de interés: [Documentación](https://agenciaimplementacion.github.io/Asistente-LADM_COL), [Galería](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/README.md#galería)

Un proyecto de: [Agencia de Implementación](https://www.proadmintierra.info/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE S.A.S](http://www.incige.com/))

 Se recomienda utilizar la versión 3.10.x de QGIS, disponible en https://qgis.org/downloads/


## Funcionalidades

La versión actual ([2.99.1](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/releases/tag/2.99.1)) del Asistente LADM_COL depende del plugin [QGIS Model Baker v6.0.0](https://github.com/opengisch/QgisModelBaker/releases/download/v6.0.0/qgis-model-baker.v6.0.0.zip) y permite:

 - Integración con el Sistema de Transición:
   - Autenticación.
   - Gestión de tareas: consulta, iniciación, cancelación y finalización.
   - Tareas de generación de insumos catastrales e integración asistida de insumos (soporte parcial).
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
 - ETL para generar insumos catastrales a partir de datos del IGAC (fuente Cobol).
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
