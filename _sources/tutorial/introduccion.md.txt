# Introducción

Este tutorial te permite hacer uso de las funcionalidades del *plugin* “Asistente LADM-COL”, incluyendo herramientas para apoyar los procesos captura, revisión, validación y consolidación de datos resultado del barrido predial masivo (levantamiento catastral) en el marco de la política pública de catastro multipropósito en Colombia.

Para ello, el tutorial utiliza un conjunto de datos de prueba y comprende las siguientes secciones:

- [Crear Estructura LADM-COL](crear_estructura_ladm_col.html#crear-estructura-ladm-col)

- [Captura y Estructuración de Datos](captura_y_estructuracion_de_datos.html#captura-y-estructuracion-de-datos)

- [Reglas de Calidad](reglas_de_calidad.html#reglas-de-calidad)

- [Consulta de Información](consulta_de_informacion.html#consulta-de-informacion)

- [Generación de Reportes](generacion_de_reportes.html#generacion-de-reportes)

- [Exportar e Importar Datos](exportar_importar_datos.html#exportar-e-importar-datos)

- [Gestión de Insumos](gestion_de_insumos.html#gestion-de-insumos)

## ¿Que se necesita para empezar?

Para desarrollar el tutorial se requieren los siguientes insumos:

**Software**

Software **QGIS versión 3.14.x** o superior, instalado en el equipo de trabajo. QGIS es software libre y se puede descargar desde [este enlace](https://qgis.org/en/site/forusers/download.html).

Complemento **Asistente LADM-COL**, que se descarga y se activa dentro del software QGIS en el menú “Complementos”, opción “Administrar e instalar complementos”. Una vez allí, se busca por términos clave en el campo de búsquedas y se instala dando clic en el botón `Instalar complemento`.

**Datos**

*Repositorio de datos*

Se debe contar con una base de datos configurada en el software PostgreSQL 9.5 o superior en la cual se tengan permisos de creación de esquemas. Durante la sección [Administración de datos](administracion_de_datos.html) del tutorial, se creará un esquema con la estructura del modelo LADM-COL.

 *Conjunto de datos de ejemplo*

En la siguiente [URL](http://nas-swissphoto.quickconnect.to/d/f/620702901595062139) se puede descargar un archivo comprimido en formato ZIP con el nombre “Datos”.

Este archivo contiene lo siguiente: 

**Insumos_cobol.zip:** Datos en formato COBOL utilizados para importación de insumos en el Asistente LADM-COL.

**Soportes:** Soportes para las fuentes administrativas. Esta carpeta contiene las escrituras públicas que soportan los derechos de dominio descritos durante el tutorial.

**taller_asistente.gpkg:** Archivo de base de datos en formato GeoPackage que tiene la información entregada por un topógrafo al realizar un barrido predial masivo.

**topo_punto_control.csv:** Archivo CSV que tiene la información asociada a los puntos de control utilizados por el topógrafo durante el levantamiento predial masivo.