## Instrucciones de uso del script qr_standalone.py

### 1. ¿Para qué sirve el script?

El script `qr_standalone.py` permite ejecutar un conjunto de reglas de calidad sobre datos que cumplan con el modelo de aplicación de Levantamiento Catastral v1.1, desde la terminal de comandos del sistema. Esto es, **¡sin abrir la interfaz gráfica de QGIS!**

Como resultado de este script obtendrás:

  + Un reporte en **PDF** detallando la validación de cada regla de calidad.
  + (Opcional) Una base de datos **GeoPackage** :package: con los errores encontrados. 

### 2. Prerrequisitos

+ Tener **QGIS** v3.16.x instalado.
+ Tener los plugins **Asistente LADM-COL** y su correspondiente **QGIS Model Baker** instalados.
+ (Opcional) Tener PostgreSQL (9.5-12) y PostGIS instalados.

### 3. Configuración en Windows

##### 3.1 Variables de entorno

Para la ejecución del script se requiere un entorno configurado, en el cual las librerías de QGIS estén accesibles. 

Para Windows, basta con abrir la terminal de comandos OSGeo4W Shell y ejecutar el archivo `python-qgis-ltr.bat` (el sufijo `-ltr` puede o no estar, dependiendo de tu instalación de QGIS).

Por ejemplo:

    C:\\OSGeo4W\\apps\\qgis\\bin\\python-qgis-ltr.bat

Al ejecutar este archivo `.bat`, tu terminal de comandos de OSGeo4W quedará configurada y lista para ejecutar el script `qr_standalone.py`. Pero antes de eso... debes definir tu configuración para el script, que se explica a continuación.

##### 3.2 Configuración del script

En la sección `SET PARAMETERS` del script `qr_standalone.py`, se deben especificar  parámetros de configuración como rutas a plugins, carpeta de salida y tolerancia para la ejecución de las reglas de calidad, así como la conexión a la base de datos. A continuación se explican en detalle:

3.2.1 **QGIS_PREFIX_PATH**: Es la ruta donde QGIS encuentra recursos como proveedores de datos y la base de datos de sistemas de referencia. Para Windows, generalmente está en:

```bash
C:\\OSGeo4W\\apps\\qgis\\
```

Pero debes revisarla, ya que dependiendo de tu instalación, esa última carpeta podría variar. Más detalles en [GIS.SE](https://gis.stackexchange.com/a/155852/4972).

3.2.2 **QGIS_PROCESSING_PLUGIN_DIR**: Es la ruta donde QGIS encuentra al plugin Processing. Para Windows, generalmente está en:

```bash
C:\\OSGeo4W\\apps\\qgis\\
```

Pero debes revisarla, ya que dependiendo de tu instalación, esa última carpeta podría variar.

3.2.3 **QGIS_PROCESSING_PLUGIN_DIR**: Es la ruta donde QGIS encuentra los plugins `Asistente LADM-COL` y `QGIS Model Baker`. Para Windows, generalmente está en:

```bash
C:\\Users\\USER\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins
```

En esa ruta, debes cambiar `USER` por tu propio usuario y tener en cuenta que `default` podría cambiar si has configurado otro perfil dentro de QGIS. Más detalles en [GIS.SE](https://gis.stackexchange.com/a/274312/4972).

3.2.4 **OUTPUT_DIR**: Es la ruta donde el script `qr_standalone.py` escribirá los resultados de la ejecución de las reglas de calidad. Se creará una carpeta que incluye el reporte en PDF y, en caso de haber errores, también una base de datos GeoPackage :package:.

3.2.5 **TOLERANCE**: Corresponde a una distancia en milímetros. Los vértices separados por una distancia menor o igual que la tolerancia definida, serán considerados como superpuestos. 

La tolerancia puede ser 0, en cuyo caso, solo los vértices con coordenadas exactamente iguales serán considerados como superpuestos.

3.2.6 **CONEXIÓN A LA BASE DE DATOS**: El script `qr_standalone.py` soporta conexión a bases de datos GeoPackage :package: y PostgreSQL/PostGIS :elephant:. 

:package: GeoPackage: El siguiente es un ejemplo de configuración de la conexión a una BD GeoPackage.

```python
db_conn = {'dbfile': 'C:\\ruta\\a\\mi_base_de_datos.gpkg'}
```

:elephant: PostgreSQL/PostGIS: El siguiente es un ejemplo de configuración de la conexión a una BD PostgreSQL/PostGIS.

```python
db_conn = {'host': 'localhost',
           'port': '5432',
           'database': 'mi_db',
           'schema': 'mi_esquema',
           'username': 'postgres',
           'password': '123456'}
```

3.2.7 **SELECCIÓN DE REGLAS DE CALIDAD**:  Antes de ejecutar el script puedes elegir cuáles reglas de calidad vas a validar. Para ello solamente debes quitar el comentario de la regla de calidad correspondiente, en el listado ``quality_rules`` que presenta el script.

Por ejemplo, si deseas ejecutar las reglas para puntos, tu listado `quality_rules` dentro del script lucirá así:

```python
quality_rules = [
    ##------------------------------ POINTS --------------------
    '1001',  # Los Puntos de Lindero no deben superponerse
    '1002',  # Los Puntos de Control no deben superponerse
    '1003',  # Los Puntos de Lindero deben estar cubiertos por ...
    '1004',  # Los Puntos de Lindero deben estar cubiertos por ...
    ##------------------------------- LINES -----------------------
    #'2001',  # Los Linderos no deben superponerse
    #'2002',  # Los Linderos deben terminar en cambio de ...
    ...
]
```

Como puedes ver en este ejemplo, las reglas cuyo codigo empieza por '1' (que corresponden a las reglas para puntos) no están comentariadas, pero las que empiezan por '2' (que corresponden a las reglas para líneas) si están como comentarios de Python.

Entonces, asegúrate de dejar como comentario aquellas reglas que no quieres validar, y quita el comentario de las reglas que si quieres validar. ¡Tú elijes!

##### 3.3 Ejecución del script

Luego de configurar tanto las variables de entorno como las variables dentro del script, puedes proceder a ejecutar el script `qr_standalone.py` en la terminal de comandos OSGeo4W shell, así:

    python C:\\ruta\\a\\script\\qr_standalone.py

### 4. Configuración en GNU/Linux

##### 4.1 Variables de entorno

Para la ejecución del script se requiere un entorno configurado, en el cual las librerías de QGIS estén accesibles. En GNU/Linux, basta con definir las variables de entorno `PYTHONPATH` y `LD_LIBRARY_PATH`, así:

    export PYTHONPATH=/usr/share/qgis/python
    export LD_LIBRARY_PATH=/usr/lib/qgis

##### 4.2 Configuración del script

4.2.1 **QGIS_PREFIX_PATH**: Es la ruta donde QGIS encuentra recursos como proveedores de datos y la base de datos de sistemas de referencia. Para GNU/Linux, generalmente está en:

```bash
/usr
```

Pero debes revisarla, ya que dependerá de tu instalación. Más detalles en [GIS.SE](https://gis.stackexchange.com/a/155852/4972).

4.2.3 **QGIS_PROCESSING_PLUGIN_DIR**: Es la ruta donde QGIS encuentra los plugins `Asistente LADM-COL` y `QGIS Model Baker`. Para GNU/Linux, generalmente está en:

```bash
/home/USER/.local/share/QGIS/QGIS3/profiles/default/python/plugins
```

En esa ruta, debes cambiar `USER` por tu propio usuario y tener en cuenta que `default` podría cambiar si has configurado otro perfil dentro de QGIS. Más detalles en [GIS.SE](https://gis.stackexchange.com/a/274312/4972).

4.2.4 **OUTPUT_DIR**: Es la ruta donde el script `qr_standalone.py` escribirá los resultados de la ejecución de las reglas de calidad. Se creará una carpeta que incluye el reporte en PDF y, en caso de haber errores, también una base de datos GeoPackage :package:.

4.2.5 **TOLERANCE**: Corresponde a una distancia en milímetros. Los vértices separados por una distancia menor o igual que la tolerancia definida, serán considerados como superpuestos. 

La tolerancia puede ser 0, en cuyo caso, solo los vértices con coordenadas exactamente iguales serán considerados como superpuestos.

4.2.6 **CONEXIÓN A LA BASE DE DATOS**: El script `qr_standalone.py` soporta conexión a bases de datos GeoPackage :package: y PostgreSQL/PostGIS :elephant:. 

:package: GeoPackage: El siguiente es un ejemplo de configuración de la conexión a una BD GeoPackage.

```python
db_conn = {'dbfile': 'C:\\ruta\\a\\mi_base_de_datos.gpkg'}
```

:elephant: PostgreSQL/PostGIS: El siguiente es un ejemplo de configuración de la conexión a una BD PostgreSQL/PostGIS.

```python
db_conn = {'host': 'localhost',
           'port': '5432',
           'database': 'mi_db',
           'schema': 'mi_esquema',
           'username': 'postgres',
           'password': '123456'}
```

4.2.7 **SELECCIÓN DE REGLAS DE CALIDAD**:  Antes de ejecutar el script puedes elegir cuáles reglas de calidad vas a validar. Para ello solamente debes quitar el comentario de la regla de calidad correspondiente, en el listado ``quality_rules`` que presenta el script.

Por ejemplo, si deseas ejecutar las reglas para puntos, tu listado `quality_rules` dentro del script lucirá así:

```python
quality_rules = [
    ##------------------------------ POINTS --------------------
    '1001',  # Los Puntos de Lindero no deben superponerse
    '1002',  # Los Puntos de Control no deben superponerse
    '1003',  # Los Puntos de Lindero deben estar cubiertos por ...
    '1004',  # Los Puntos de Lindero deben estar cubiertos por ...
    ##------------------------------- LINES -----------------------
    #'2001',  # Los Linderos no deben superponerse
    #'2002',  # Los Linderos deben terminar en cambio de ...
    ...
]
```

Como puedes ver en este ejemplo, las reglas cuyo codigo empieza por '1' (que corresponden a las reglas para puntos) no están comentariadas, pero las que empiezan por '2' (que corresponden a las reglas para líneas) si están como comentarios de Python.

Entonces, asegúrate de dejar como comentario aquellas reglas que no quieres validar, y quita el comentario de las reglas que si quieres validar. ¡Tú elijes!

##### 4.3 Ejecución del script

Luego de configurar tanto las variables de entorno como las variables dentro del script, puedes proceder a ejecutar el script `qr_standalone.py` en la terminal de comandos de GNU/Linux, así:

```bash
$ python3 /ruta/a/script/qr_standalone.py
```