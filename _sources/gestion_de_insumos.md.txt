# Gestión de insumos

## Ejecutar ETL de Insumos

Las ETLs (Extracción, Transformación y Cargue) que llevan los datos desde SNC (Sistema Nacional Catastral) o COBOL (**CO**mmon **B**usiness-**O**riented **L**anguage) al submodelo de insumos se pueden ejecutar desde un wizard en el Asistente LADM-COL.

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>Se recomienda ejecutar la ETL que lleva los datos desde COBOL o SNC al submodelo de insumos desde el perfil de <b>Proveedor de Insumos</b> del Asistente LADM-COL.</p>
</div>

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>Antes de ejecutar la ETL de COBOL o SNC al submodelo de insumos, <a href="https://swisstierrascolombia.github.io/Asistente-LADM-COL/administracion_de_datos.html#crear-estructura-ladm-col">crea la estructura de base de datos</a> desde Administración de datos --> Crear estructura</p>
</div>

### ETL SNC al Submodelo de insumos

Para Ejecutar la ETL SNC es necesario que del sistema SNC se extraigan los siguientes archivos para la zona de trabajo de interés: 

|                    |     **Alfanuméricos**     |                                |
| ------------------ | ------------------------- | ------------------------------ |
| predio_bloqueo.csv | persona_predio.csv *      | unidad_construccion_comp.csv * |
| persona.csv *      | direccion.csv *           | ficha_matriz.csv               |
| predio.csv *       | unidad_construccion.csv * | ficha_matriz_predio.csv        |
| ficha_matriz_torre.csv |                           |                                |

|   **Geográficos**   |
| ------------------- |
| GDB (Geodatabase) * |

\* *Archivo obligatorio para ejecutar el ETL.*

<div class="warning">
<p class="admonition-title">ADVERTENCIA</p>
<p>Antes de ejecutar el ETL de SNC, se debe verificar la configuración de la conexión a la base de datos destino para evitar sobreescribir datos a una estructura incorrecta.</p>
</div>

<a class="" data-lightbox="ETL SNC" href="_static/gestion_de_insumos/etl_snc.gif" title="ETL SNC" data-title="ETL SNC"><img src="_static/gestion_de_insumos/etl_snc.gif" class="align-center" width="800px" height="500px" alt="ETL SNC">
</a>

### ETL COBOL a submodelo de insumos

Para Ejecutar la ETL COBOL es necesario que del sistema COBOL se extraigan los siguiente archivos para la zona de trabajo de interés:

|           | **Alfanuméricos** |           |
| --------- | :---------------: | --------- |
| blo.lis   |     uni.lis *     | ter.lis * |
| pro.lis * |                   |           |

|   **Geográficos**   |
| ------------------- |
| GDB (Geodatabase) * |

\* *Archivo obligatorio para ejecutar el ETL.*

<div class="warning">
<p class="admonition-title">ADVERTENCIA</p>
<p>Antes de ejecutar la ETL de COBOL, se debe verificar la configuración de la conexión a la base de datos destino para evitar sobreescribir datos a una estructura incorrecta.</p>
</div>

<a class="" data-lightbox="ETL Cobol" href="_static/gestion_de_insumos/etl_cobol.gif" title="ETL Cobol" data-title="ETL Cobol"><img src="_static/gestion_de_insumos/etl_cobol.gif" class="align-center" width="800px" height="500px" alt="ETL Cobol">
</a>

## Reporte de Omisiones y Comisiones

Esta funcionalidad facilita la generación del reporte de omisiones y comisiones para los datos de **COBOL** y **SNC**, este reporte nos permite identificar las inconsistencias de completitud del dato, y depurar el error tanto en la información gráfica como alfanumérica. Para esto es necesario contar con la información asociada al predio que se encuentra en el archivo **uni.lis** para el caso de **COBOL**, y para el caso **SNC** se encuentra en el archivo **predio.csv**. La información geográfica para ambos casos se encuentra en el archivo con formato **GDB**. 

Despues de ejecutar el reporte, las capas geográficas resultantes se almacenarán en un archivo con formato **GeoPackage (GPKG)** y la estadistica de los datos se almacenará en un archivo en formato **Excel (XLS)** a los cuales se les podrá asígnar un nombre y quedarán en la carpeta seleccionada en el momento de ejecutar el reporte.

### Reporte Omisiones y Comisiones - COBOL

<a class="" data-lightbox="Omisiones y Comisiones Cobol" href="_static/gestion_de_insumos/omisiones_comisiones_cobol.gif" title="Omisiones y Comisiones Cobol" data-title="Omisiones y Comisiones Cobol"><img src="_static/gestion_de_insumos/omisiones_comisiones_cobol.gif" class="align-center" width="800px" height="500px" alt="Omisiones y Comisiones Cobol">
</a>

### Reporte Omisiones y Comisiones - SNC

<a class="" data-lightbox="Omisiones y Comisiones SNC" href="_static/gestion_de_insumos/omisiones_comisiones_snc.gif" title="Omisiones y Comisiones SNC" data-title="Omisiones y Comisiones SNC"><img src="_static/gestion_de_insumos/omisiones_comisiones_snc.gif" class="align-center" width="800px" height="500px" alt="Omisiones y Comisiones SNC">
</a>
