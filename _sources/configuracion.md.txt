# Configuración

El diálogo de configuración permite definir configuraciones generales para el funcionamiento del Asistente LADM-COL. Se compone de las siguientes secciones:

+ [Conexión a Base de Datos](#conexion-a-base-de-datos)
+ [Modelos](#modelos)
+ [Calidad](#calidad)
+ [Valores Automáticos](#valores-automaticos)
+ [Servicios](#servicios)
+ [Avanzado](#avanzado)

<a class="" data-lightbox="Configuración" href="_static/configuracion/settings.gif" title="Configuración" data-title="Configuración"><img src="_static/configuracion/settings.gif" class="align-center" width="800px" alt="Configuración"/></a>

## Conexión a Base de Datos

En esta pestaña se definen los parámetros para conectarse con la base de datos que almacena el modelo físico basado en LADM-COL, sobre el cual se trabajará. La elección de la base de datos a conectar determinará cuáles funcionalidades del Asistente LADM-COL están disponibles, de acuerdo al [rol activo](introduccion.html#dialogo-de-bienvenida).

Se tienen tres opciones de motores de base de datos para realizar la conexión:

+ [PostgreSQL/PostGIS](#conexion-a-postgresql-postgis)
+ [GeoPackage](#conexion-a-geopackage)
+ [SQL Server](#conexion-a-sql-server)

El listado desplegable **Fuente** permite elegir el motor de base de datos de interés.

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>Revisa el soporte de funcionalidades por motor de base de datos en la sección de <a href="introduccion.html#soporte-de-funcionalidades-por-motor-de-base-de-datos">Introducción</a>.</p>
</div>

### Conexión a PostgreSQL/PostGIS

- **Host**: Dirección IP para acceder a la base de datos. Si la base de datos es local, puede usarse `localhost` como valor del parámetro `Host`.
- **Puerto**: Número del puerto de escucha para la base de datos.
- **Usuario**: Nombre del usuario que tiene permiso sobre la base de datos.
- **Contraseña**: Contraseña de usuario.
- **Base de Datos**: Nombre de la base de datos que contiene o contendrá el modelo físico de LADM-COL.
- **Esquema**: Nombre del esquema que almacena los objetos del modelo físico de LADM-COL.
- **Probar conexión**: Permite conocer si se puede establecer conexión con el servidor de PostgreSQL/PostGIS al cual apuntan los parámetros de conexión.
- **Probar estructura LADM-COL**: Permite conocer si el esquema seleccionado tiene una estructura de tablas y relaciones que corresponda a los modelos soportados, basados en LADM-COL.

<a class="" data-lightbox="Conexión a Base de Datos" href="_static/configuracion/conexion_base_de_datos.png" title="Conexión a Base de Datos" data-title="Conexión a Base de Datos"><img src="_static/configuracion/conexion_base_de_datos.png" class="align-center" alt="Conexión a Base de Datos"/></a>

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>Desde la pestaña de conexión a PostgreSQL/PostGIS puedes crear tu base de datos y tu esquema de trabajo.</p>
</div>
<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>Revisa las versiones soportadas de PostgreSQL/PostGIS en la sección de <a href="introduccion.html#requerimientos-minimos">Introducción</a>.</p>
</div>


<div class="seealso">
<p class="admonition-title">TIP</p>
<p>Es posible configurar la conexión a la base de datos utilizando un usuario que tenga permisos de creación (`CREATE`) o de uso (`USAGE`) sobre el esquema de trabajo. El permiso de uso (`USAGE`) es más limitado, pero es útil cuando se quiere restringir la creación/modificación/borrado de objetos del esquema, como tablas y relaciones, y a la vez permitir la edición de datos espaciales y alfanuméricos. Ver <a href="https://github.com/SwissTierrasColombia/Asistente-LADM-COL/issues/384#issuecomment-716250604" target="_blank">ejemplo de configuración de permisos limitados para un usuario del Asistente LADM-COL</a>.</p>
</div>

### Conexión a GeoPackage

- **Archivo de Base de Datos**: Ubicación en disco del archivo Geopackage (.gpkg) que contiene la base de datos.
- **Probar conexión**: Permite conocer si el archivo GeoPackage (.gpkg) especificado existe y puede ser accedido correctamente.
- **Probar estructura LADM-COL**: Permite conocer si el archivo seleccionado tiene una estructura de tablas y relaciones que corresponda a los modelos soportados, basados en LADM-COL.

<a class="" data-lightbox="Conexión a Base de Datos GeoPackage" href="_static/configuracion/conexion_base_de_datos_gpkg.png" title="Conexión a Base de Datos GeoPackage" data-title="Conexión a Base de Datos GeoPackage"><img src="_static/configuracion/conexion_base_de_datos_gpkg.png" class="align-center"  alt="Conexión a Base de Datos GeoPackage"/></a>

### Conexión a SQL Server

<a class="" data-lightbox="Conexión a Base de Datos SQL Server" href="_static/configuracion/conexion_base_de_datos_mssql.png" title="Conexión a Base de Datos SQL Server" data-title="Conexión a Base de Datos SQL Server"><img src="_static/configuracion/conexion_base_de_datos_mssql.png" class="align-center" alt="Conexión a Base de Datos SQL Server"/></a>

## Modelos

En esta pestaña se puede seleccionar el repositorio de modelos locales a utilizar, así como definir si se quieren deshabilitar las validaciones (por ejemplo, validaciones de estructura y de relaciones) sobre las operaciones de importar y exportar archivos XTF (ver sección [Adminninstración de datos](administracion_de_datos.html)).

<a class="" data-lightbox="Configuración de acceso a modelos" href="_static/configuracion/modelos.png" title="Configuración de acceso a modelos" data-title="Configuración de acceso a modelos"><img src="_static/configuracion/modelos.png" class="align-center" alt="Configuración de acceso a modelos"/></a>

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>La versión instalada del Asistente LADM-COL incluye una carpeta con los modelos soportados por esa versión. De manera predeterminada, los modelos a los que accede el Asistente LADM-COL se encuentran en dicha carpeta.</p>
</div>

## Calidad

En esta pestaña se definen parámetros generales para validaciones de calidad. 

 - **Tolerancia**: Se puede configurar el valor de tolerancia (en milímetros) para la ejecución de reglas de calidad. Los vértices separados por una distancia menos o igual a la tolerancia, serán considerados como superpuestos.
 - **Tener en cuenta vías**: En la validación de huecos entre terrenos, se pueden incluir como errores los espacios entre cuadras (de esta forma, se estarían teniendo en cuenta las vías) o se pueden omitir (y de esta forma, no se estarían teniendo en cuenta las vías).

<a class="" data-lightbox="Parámetros generales para reglas de calidad" href="_static/configuracion/calidad.png" title="Parámetros generales para reglas de calidad" data-title="Parámetros generales para reglas de calidad"><img src="_static/configuracion/calidad.png" class="align-center" alt="Parámetros generales para reglas de calidad"/></a>

## Valores automáticos

La mayoría de las clases en LADM_COL tiene dos atributos que combinados deben ser únicos en todo el `esquema/base de datos`. Se denominan `espacio_de_nombres` y `local_id`. Para hacer más fácil el llenado de estos atributos, el asistente LADM_COL puede configurarse con valores automáticos para ellos.

Concretamente, `espacio_de_nombres` corresponderá a un prefijo opcional (p.e., MI_ORGANIZACION) más el nombre de la clase (p.e., LC_LINDERO): MI_ORGANIZATION_LINDERO.

Por otra parte , `local_id` correspondera al ID del registro en la base de datos.

Si deseas llenar esos valores por tu cuenta desmarca las siguientes opciones en este formulario.

<a class="" data-lightbox="Configuración de valores automáticos" href="_static/configuracion/valores_automaticos.png" title="Configuración de valores automáticos" data-title="Configuración de valores automáticos"><img src="_static/configuracion/valores_automaticos.png" class="align-center" alt="Configuración de valores automáticos"/></a>

## Servicios

En esta sección se configuran un par de servicios web que el Asistente LADM-COL puede emplear para conectarse al [Sistema de Transición](sistema_de_transicion.html) y para subir archivos de fuentes administrativas y espaciales. 

La configuración de estos servicios es opcional, pues solo se requiere cuando se utilizará alguna de las dos funcionalidades mencionadas, pero no interfiere en el uso normal del complemento.

<a class="" data-lightbox="Parámetros de conexión a servicios" href="_static/configuracion/servicios.png" title="Parámetros de conexión a servicios" data-title="Parámetros de conexión a servicios"><img src="_static/configuracion/servicios.png" class="align-center" alt="Parámetros de conexión a servicios"/></a>


## Avanzado

En esta sección se define cuál es el rol activo para el Asistente LADM-COL. Ver la sección de [Introducción](introduccion.html#dialogo-de-bienvenida) para más detalles.

<a class="" data-lightbox="Configuración del rol activo" href="_static/configuracion/roles.png" title="Configuración del rol activo" data-title="Configuración del rol activo"><img src="_static/configuracion/roles.png" class="align-center" alt="Configuración del rol activo"/></a>