Configuración
==============

.. image:: _static/configuracion/settings.gif
    :height: 500
    :width: 800
    :alt: Configuración básica
    :download: true
    :title: Configuración básica

Conexión a Base de Datos
**************************

En esta pestaña, se definen los parámetros para conectarse con la base de datos que almacena el modelo físico de LADM_COL.

Estos parámetros son:

**Parámetros comunes**

- **Fuente**: Define el origen de los datos, esta puede ser una base de datos espacial PostgreSQL, GeoPackage o MSSQL (Experimental).

Párametros de PostgreSQL/PostGIS
---------------------------------

- **Usuario**: Nombre del Usuario que tiene permiso sobre la base de datos
- **Contraseña**: Contraseña de Usuario
- **Host**: dirección donde la base de datos es almacenada localhost es equivalente a 127.0.0.
- **Puerto**: Número del puerto de escucha para la base de datos
- **Base de Datos**:Nombre de la base de datos que contiene o contendrá el modelo físico de LADM_COL
- **Esquema**: Nombre del esquema que almacena los objetos del modelo físico de LADM_COL

.. image:: _static/configuracion/db_connection_settings.gif
    :height: 500
    :width: 800
    :alt: Configuración básica
    :download: true
    :title: Configuración básica

**Nota**: Puede crear su base de datos y su esquema. Pero los nombres no deben contener caracteres especiales.

Parámetros de GeoPackage
-------------------------

- **Archivo de Base de Datos**: Ubicación en disco del archivo Geopackage que contiene la base de datos.

El botón Probar Conexión se usa para saber si los parámetros ingresados son correctos y permiten la conexión a la base de datos

Modelos
********

En esta pestaña, puede seleccionar si desea utilizar el repositorio de modelos locales o remotos.

.. image:: _static/configuracion/set_custom_models_directories.gif
    :height: 500
    :width: 800
    :alt: Establecer directorios de modelos personalizados
    :download: true
    :title: Establecer directorios de modelos personalizados

Calidad
*********
En esta pestaña se definen parámetros para validaciones de calidad. Por ejemplo, se establece el límite de tolerancia permitido para segmentos de linderos demasiado largos, el cual debe estar definido en metros.

Valores automáticos
*********************

La mayoría de las clases en LADM_COL tiene dos atributos que combinados deben ser únicos en todo el `esquema/base de datos`. Se denominan **espacio_de_nombres** y **local_id**. Para hacer más fácil el llenado de estos atributos, el asistente LADM_COL puede configurarse con valores automáticos para ellos.

Concretamente, **espacio_de_nombres** corresponderá a un prefijo opcional (p.e., MI_ORGANIZACION) más el nombre de la clase (p.e., LINDERO): MI_ORGANIZATION_LINDERO.

Por otra parte , **local_id** correspondera al ID del registro en la base de datos.

Si deseas llenar esos valores por tu cuenta desmarca las siguientes opciones en este formulario.

.. image:: _static/configuracion/automatic_values_settings.gif
    :height: 500
    :width: 800
    :alt: Configuración de valores automáticos
    :download: true
    :title: Configuración de valores automáticos

Fuentes
********

Es posible configurar a través de un repositorio de datos una ruta de acceso URL para subir fuentes administrativas y fuentes espaciales asociadas a la información recolectada en LADM-COL.

.. image:: _static/configuracion/source_settings.gif
    :height: 500
    :width: 800
    :alt: Fuentes
    :download: true
    :title: Fuentes
