# Captura y Estructuración de Datos

## Alistamiento de insumos

La primera parte de tutorial corresponde a la descarga e importación de datos en QGIS.  Para llevar a cabo cada uno de los pasos, es necesario que descargues el [material de práctica](http://nas-swissphoto.quickconnect.to/d/f/620702901595062139) y sigas las instrucciones del tutorial.

<div class="seealso">
<p class="admonition-title">TIP</p>
<p> Si deseas agregar otras fuentes de información como referencia a la información proporcionada, puedes hacerlo haciendo uso de QGIS y sus diferentes funcionalidades. </p>
</div>

### Paso 1: Conexión a la base de datos 

Para empezar, se debe definir la conexión a la base de datos. Para realizar este proceso, dirígete al panel "**Navegador**" ubicado a la izquierda de la interfaz de QGIS, en el árbol que se despliega ubica la sección **Geopackage**, haz clic derecho sobre esta sección y selecciona la opción de **Conexión nueva**. Una vez se despliega el panel de navegación, deberás ubicar la base de datos **taller_asistente.gpkg** (disponible en los datos del tutorial) y dar clic en el botón **Abrir** para configurar la conexión a la base de datos.

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p> Como resultado de este proceso se tendrá conexión a una base de datos que posee diversa información, de la cual se hará uso a medida que se avance en las secciones de este tutorial. </p>
</div>

<a class="" data-lightbox="Paso 1: Conexión a la base de datos" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos1.gif" title=" Paso 1: Conexión a la base de datos " data-title=" Paso 1: Conexión a la base de datos "><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos1.gif" class="align-center" width="800px" alt=" Paso 1: Conexión a la base de datos "/></a>

<div class="seealso">
<p class="admonition-title">TIP</p>
<p> Con el fin de tener una mejor referencia de la zona de trabajo, se recomienda instalar el complemento <b>QuickMapServices</b>, que proporciona un conjunto de servicios Web que pueden ser utilizados como mapas base. Por ejemplo, algunos permiten desplegar imágenes satelitales sobre el mapa. </p>
</div>

<a class="" data-lightbox="Paso 1: QuickMapService" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos2.gif" title="Paso 1: QuickMapService" data-title="Paso 1: QuickMapService"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos2.gif" class="align-center" width="800px" alt="Paso 1: QuickMapService"/></a>

## Consulta de dominios

### Paso 1: Tabla de atributos

Para proceder a la consulta de dominios debes dirigirte al grupo "**domains**" ubicado en el panel de capas de QGIS, abrir el grupo y buscar el dominio de interés. Sobre éste debes dar clic derecho y seleccionar la opción **Abrir tabla de atributos** en el menú de contexto que se despliega.

El ejemplo que se muestra a continuación se desarrolla con la capa **lc\_puntotipo**.

<a class="" data-lightbox="Paso 1: Tabla de atributos" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos9.png" title="Paso 1: Tabla de atributos" data-title="Paso 1: Tabla de atributos"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos9.png" class="align-center" width="400px" alt="Paso 1: Tabla de atributos"/></a>

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>Puedes acceder a la tabla de atributos de la capa de interés, ubicándote sobre la misma en el panel de capas y tecleando <b>F6</b>.</p>
</div>

### Paso 2: Identificación del T_Id

Se desplegará un diálogo con el listado de los valores del dominio seleccionado. De esta manera es posible identificar el número correspondiente al campo de descripción del elemento requerido, ubicado en la columna **t_id**.

<a class="" data-lightbox="Paso 2: Identificación del T_Id" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos10.png" title="Paso 2: Identificación del T_Id" data-title="Paso 2: Identificación del T_Id"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos10.png" class="align-center" width="1200px" alt="Paso 2: Identificación del T_Id"/></a>

## Paquete de topografía y representación

### Puntos de lindero

### Puntos de levantamiento

### Puntos de Control

### Linderos

### Construcción De Linderos

### Relación Entre Puntos y Linderos

## Unidad Espacial

### Creación De Terrenos y Sus Relaciones

#### Creación De Relación Entre Los Linderos y Los Terrenos

### Creación De Construcciones

### Creación De Unidades De Construcción

## Unidad Básica Administrativa

### Crear Predio

## Interesados

### Crear Agrupación De Interesados

## Fuentes

## RRR

### Crear Derecho