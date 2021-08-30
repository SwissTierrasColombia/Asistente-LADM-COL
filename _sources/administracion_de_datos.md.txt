# Administración de datos

Este modulo del Asistente LADM-COL permite gestionar bases de datos y datos conformes con el modelo LADM-COL. Para ello emplea herramientas que trabajan con el lenguaje INTERLIS. En particular, permite:

1. [Crear una estructura](#crear-estructura-ladm-col) en base de datos conforme con el modelo LADM-COL y con sus modelos extendidos. Esto es, lleva de modelos conceptuales a modelos físicos.
2. [Importar datos](#importar-datos) a una base de datos LADM-COL desde archivos de transferencia de INTERLIS, con extensión .XTF.
3. [Exportar datos](#exportar-datos) desde una base de datos LADM-COL hacia archivos de transferencia de INTERLIS, con extensión .XTF.

## Crear estructura LADM-COL

Esta funcionalidad permite crear esquemas de base de datos (si se utiliza PostgreSQL/PostGIS o SQL Server) o archivos de base de datos (si se utiliza GeoPackage) conformes con el modelo LADM-COL y con sus modelos extendidos.

<a class="" data-lightbox="Crear estructura LADM-COL" href="_static/administracion_de_datos/create_schema_ladm_qgismodelbaker.gif" title="Crear estructura LADM-COL" data-title="Crear estructura LADM-COL"><img src="_static/administracion_de_datos/create_schema_ladm_qgismodelbaker.gif" class="align-center" width="800px" alt="Crear estructura LADM-COL"/></a>

<div class="warning">
<p class="admonition-title">ADVERTENCIA</p>
<p>Para bases de datos PostgreSQL/PostGIS o SQL Server, el nombre del esquema de base de datos debe estar en minúsculas y no debe contener caracteres especiales.</p>
</div>


## Importar datos

Esta funcionalidad permite importar datos desde un archivo de transferencia (en formato .XTF) a un esquema de base de datos (si se utiliza PostgreSQL/PostGIS o SQL Server) o a un archivo de base de datos con extensión .GPKG (si se utiliza GeoPackage).

La estructura de los datos y la estructura de la base de datos de destino deben coincidir, y deben ser conformes con el modelo LADM-COL o con sus modelos extendidos.

<a class="" data-lightbox="Importar datos desde un archivo XTF" href="_static/administracion_de_datos/import_data_qgismodelbaker.gif" title="Importar datos desde un archivo XTF" data-title="Importar datos desde un archivo XTF"><img src="_static/administracion_de_datos/import_data_qgismodelbaker.gif" class="align-center" width="800px" alt="Importar datos desde un archivo XTF"/></a>

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>Durante la importación de datos .XTF se llevan a cabo validaciones de los datos, según el modelo con el cuál sean conformes. Por ejemplo, se valida que los valores de dominios presentes en los datos, correspondan a los valores de dominios definidos en los modelos LADM-COL.</p>
</div>

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>En algunas ocasiones puede ser útil deshabilitar temporalmente las validaciones sobre los datos con el fin de poder importar un archivo XTF. Por ejemplo, puede que en una misma entidad varias personas quieran compartise estados intermedios (no finalizados, y por tanto, aún no necesariamente válidos) de un conjunto de datos. Para ello, ver la sección <a href="configuracion.html#modelos">Configuración -> Modelos</a> de la documentación.</p>
</div>

## Exportar datos

Esta funcionalidad permite exportar desde un esquema de base de datos (si se utiliza PostgreSQL/PostGIS o SQL Server) o desde un archivo de base de datos con extensión .GPKG (si se utiliza GeoPackage), hacia un archivo de transferencia, con extensión .XTF.

<a class="" data-lightbox="Exportar datos a un archivo XTF" href="_static/administracion_de_datos/export_data_qgismodelbaker.gif" title="Exportar datos a un archivo XTF" data-title="Exportar datos a un archivo XTF"><img src="_static/administracion_de_datos/export_data_qgismodelbaker.gif" class="align-center" width="800px" alt="Exportar datos a un archivo XTF"/></a>

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>Durante la exportación de datos a .XTF se llevan a cabo validaciones de los datos, según el modelo con el cuál sean conformes. Por ejemplo, se valida que los valores de dominios presentes en los datos, correspondan a los valores de dominios definidos en los modelos LADM-COL.</p>
</div>

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>En algunas ocasiones puede ser útil deshabilitar temporalmente las validaciones sobre los datos con el fin de poder obtener un archivo XTF que se pueda intercambiar. Por ejemplo, puede que en una misma entidad varias personas quieran compartise estados intermedios (no finalizados, y por tanto, aún no necesariamente válidos) de un conjunto de datos. Para ello, ver la sección <a href="configuracion.html#modelos">Configuración -> Modelos</a> de la documentación.</p>
</div>