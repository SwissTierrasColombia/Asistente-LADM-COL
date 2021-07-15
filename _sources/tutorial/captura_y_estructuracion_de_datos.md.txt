# Captura y Estructuración de Datos

## Alistamiento de insumos

La primera parte de tutorial corresponde a la descarga e importación de datos en QGIS.  Para llevar a cabo cada uno de los pasos, es necesario que descargues el [material de práctica](http://nas-swissphoto.quickconnect.to/d/f/620702901595062139) y sigas las instrucciones del tutorial.

<div class="seealso">
<p class="admonition-title">TIP</p>
<p> Si deseas agregar otras fuentes de información como referencia a la información proporcionada, puedes hacerlo haciendo uso de QGIS y sus diferentes funcionalidades. </p>
</div>

### Paso 1: Conexión a la base de datos 

Para empezar, se debe definir la conexión a la base de datos. Para realizar este proceso, dirígete al panel "**Navegador**" ubicado a la izquierda de la interfaz de QGIS, en el árbol que se despliega ubica la sección **GeoPackage**, haz clic derecho sobre esta sección y selecciona la opción de **Conexión nueva**. Una vez se despliega el panel de navegación, deberás ubicar la base de datos **taller_asistente.gpkg** (disponible en los datos del tutorial) y dar clic en el botón **Abrir** para configurar la conexión a la base de datos.

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

#### Paso 1: Cargue de insumos Punto lindero

Inicialmente, se arrastra la capa de insumo llamada **topo_puntos_lindero** al mapa de QGIS.

<a class="" data-lightbox="Paso 1: Cargue de insumos Punto lindero" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos9.gif" title="Paso 1: Cargue de insumos Punto lindero" data-title="Paso 1: Cargue de insumos Punto lindero"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos9.gif" class="align-center" width="800px" alt="Paso 1: Cargue de insumos Punto lindero"/></a>

#### Paso 2: Creación de punto lindero

Entiéndase *'Puntos de lindero'* como aquellos puntos que definen los vértices de un lindero.

Para crear puntos de lindero debes seguir la ruta **LADM-COL -> Captura y estructuración de datos -> Levantamiento Catastral -> Topografía y Representación -> Crear Punto**.

<a class="" data-lightbox="Paso 2: Creación de punto lindero" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos3.png" title="Paso 2: Creación de punto lindero" data-title="Paso 2: Creación de punto lindero"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos3.png" class="align-center" width="800px" alt="Paso 2: Creación de punto lindero"/></a>

#### Paso 3: Selección del tipo de punto

La acción anterior desplegará un cuadro de diálogo con la opción para seleccionar la clase de punto que se desea importar. En este caso, selecciona **Punto Lindero** y luego haz clic en **Siguiente**.

<a class="" data-lightbox="Paso 3: Selección del tipo de punto" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos4.png" title="Paso 3: Selección del tipo de punto" data-title="Paso 3: Selección del tipo de punto"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos4.png" class="align-center" width="600px" alt="Paso 3: Selección del tipo de punto"/></a>

#### Paso 4: Selección de los datos punto lindero

Ahora debes seleccionar el conjunto de datos a importar. La fuente de estos puede ser un archivo separado por comas (CSV) o una capa vectorial.

Para este caso, elige el conjunto de datos que ya está cargado en la interfaz de QGIS, **topo_punto_lindero**, y procede a dar clic en el botón `Importar`.

<a class="" data-lightbox="Paso 4: Selección de los datos punto lindero" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos5.png" title="Paso 4: Selección de los datos punto lindero" data-title="Paso 4: Selección de los datos punto lindero"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos5.png" class="align-center" width="600px" alt="Paso 4: Selección de los datos punto lindero"/></a>

#### Paso 5: Diálogo del mapeo de campos para punto lindero

Tan pronto realices el paso anterior, se abre un cuadro de diálogo en el cual se encuentra el mapeo de la información levantada en campo comparada con la información que requiere el modelo.

 <a class="" data-lightbox="Paso 5: Diálogo del mapeo de campos para punto lindero" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos6.png" title="Paso 5: Diálogo del mapeo de campos para punto lindero" data-title="Paso 5: Diálogo del mapeo de campos para punto lindero"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos6.png" class="align-center" width="600px" alt="Paso 5: Diálogo del mapeo de campos para punto lindero"/></a>

<div class="warning">
<p class="admonition-title">ADVERTENCIA</p>
<p>Resulta de gran importancia esta sección ya que es la base de la importación de información restante.</p>
</div>

#### Paso 6: Definición del mapeo de campos para punto lindero

La capa **lc\_punto\_lindero** cuenta con cinco atributos obligatorios, estos son:

| **Item** | **Entidad**     | **Atributo**         | **Contenido**                |
| -------- | --------------- | -------------------- | ---------------------------- |
| 1        | LC_PuntoLindero | ID_Punto_Lindero     | Cadena de texto              |
| 2        | LC_PuntoLindero | Punto Tipo           | **LC_PuntoTipo**             |
| 3        | LC_PuntoLindero | Acuerdo              | **LC_AcuerdoTipo**           |
| 4        | LC_PuntoLindero | Exactitud Horizontal | Numérico                     |
| 5        | COL_Punto       | Metodo Producción    | **Col_MetodoProduccionTipo** |

Considerando esto, en el cuadro de diálogo del mapeo de campos (imagen anterior) procede a dar clic en el botón **"Generar expresión"** ![Botón generar expresion](../_static/tutorial/captura_y_estructura_de_datos/ICOdialogodeexpressiones.png) para los atributos obligatorios mencionados en la tabla anterior.

Para asignar códigos (**t_id**) de un dominio con base en sus valores, se hace uso de la siguiente función:

```sql
get_domain_code_from_value('Nombre de la tabla del dominio' (Texto), 
                           valor del dominio a buscar (Texto),
                           Indica si el valor es iliCode o no (Booleano),
                           Indica si validar conexión o no (Booleano),)
```

<a class="" data-lightbox="Paso 6a: Definición del mapeo de campos para punto lindero" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos12.png" title="Paso 6a: Definición del mapeo de campos para punto lindero" data-title="Paso 6a: Definición del mapeo de campos para punto lindero"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos12.png" class="align-center" width="800px" alt="Paso 6a: Definición del mapeo de campos para punto lindero"/></a>

Para el caso del mapeo de atributos obligatorios para Punto Lindero, debes asignar las siguientes expresiones:

| Atributo             | Expresión                                                    |
| -------------------- | ------------------------------------------------------------ |
| id_punto_lindero     | id_punto                                                     |
| puntotipo            | get_domain_code_from_value('lc_puntotipo', punto_tipo, True, False) |
| acuerdo              | get_domain_code_from_value('lc_acuerdotipo', acuerdo, True, False) |
| exactitud_horizontal | 1                                                            |
| metodoproduccion     | get_domain_code_from_value('col_metodoproducciontipo', 'Metodo_Directo', True, False) |

<div class="warning">
<p class="admonition-title">ADVERTENCIA</p>
<p>Para el caso del campo <b>metodoproduccion</b>, se utiliza el texto 'Metodo_Directo' ya que los datos iniciales no cuentan con información para este campo.</p>
</div>


Una vez que se diligencian cada uno de los atributos al interior del formulario, se obtiene el siguiente resultado:

<a class="" data-lightbox="Paso 6b: Definición del mapeo de campos para punto lindero" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos13.png" title="Paso 6b: Definición del mapeo de campos para punto lindero" data-title="Paso 6b: Definición del mapeo de campos para punto lindero"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos13.png" class="align-center" width="800px" alt="Paso 6b: Definición del mapeo de campos para punto lindero"/></a>

#### Paso 7: Resultado de la ejecución punto lindero

Una vez terminado el mapeo de campos, debes dar clic en **Ejecutar** y al terminar el proceso podrás visualizar el siguiente mensaje de validación. Puedes leer su contenido (por ejemplo, "146 features copiados") para verificar que la ejecución haya sido exitosa y cerrar el cuadro de diálogo.

<a class="" data-lightbox="Paso 7 Resultado de la ejecución punto lindero" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos15.png" title="Paso 7 Resultado de la ejecución punto lindero" data-title="Paso 7 Resultado de la ejecución punto lindero"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos15.png" class="align-center" width="800px" alt="Paso 7 Resultado de la ejecución punto lindero"/></a>

### Puntos de levantamiento

#### Paso 1: Cargue de insumos punto levantamiento

Inicialmente, se arrastra la capa de insumo llamada **topo_puntos_levantamiento** al menú de capas de QGIS.

<a class="" data-lightbox="Paso 1: Cargue de insumos punto levantamiento" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos16.gif" title="Paso 1: Cargue de insumos punto levantamiento" data-title="Paso 1: Cargue de insumos punto levantamiento"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos16.gif" class="align-center" width="800px" alt="Paso 1: Cargue de insumos punto levantamiento"/></a>

#### Paso 2: Creación de punto levantamiento

Para iniciar con el proceso de importación debes dirigirte a la barra de herramientas del plugin y dar clic en **Crear objetos de levantamiento -> Crear punto**.

<a class="" data-lightbox="Paso 2: Creación de punto levantamiento" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos16.png" title="Paso 2: Creación de punto levantamiento" data-title="Paso 2: Creación de punto levantamiento"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos16.png" class="align-center" width="400px" alt="Paso 2: Creación de punto levantamiento"/></a>

#### Paso 3: Selección de los datos punto levantamiento

Al realizar el paso 2 se desplegará un cuadro de diálogo donde se deberá seleccionar el tipo de punto a insertar, en este caso: **Punto Levantamiento**. Confirma por medio del botón `Siguiente` , y escoge el conjunto de datos fuente para el procesamiento, que para este caso corresponde a la capa **topo_punto\_levantamiento**. Finalmente presiona el botón `Importar`.

<a class="" data-lightbox="Paso 3: Selección de los datos punto levantamiento" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos17.gif" title="Paso 3: Selección de los datos punto levantamiento" data-title="Paso 3: Selección de los datos punto levantamiento"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos17.gif" class="align-center" width="800px" alt="Paso 3: Selección de los datos punto levantamiento"/></a>

#### Paso 4: Mapeo de campos punto levantamiento  

Se recomienda tener en cuenta el [paso 5](#paso-5-definicion-del-mapeo-de-campos-para-punto-lindero) de la sección de punto de lindero. Para este caso, debemos asignar los valores de la siguiente manera:

| Atributo                 | Expresión                                                    |
| ------------------------ | ------------------------------------------------------------ |
| id_punto_levantamiento   | id                                                           |
| puntotipo                | get_domain_code_from_value('lc_puntotipo', punto_tipo, True, False) |
| tipo_punto_levantamiento | get_domain_code_from_value('lc_puntolevtipo', 'Construccion', True, False) |
| exactitud_horizontal     | 1                                                            |
| metodoproduccion         | get_domain_code_from_value('col_metodoproducciontipo', 'Metodo_Directo', True, False) |

<div class="warning">
<p class="admonition-title">ADVERTENCIA</p>
<p>Para el caso del campo <b>metodoproduccion</b>, se utiliza el texto 'Metodo_Directo' ya que los datos iniciales no cuentan con información para este campo.</p>
<p>Para el caso del campo <b>tipo_punto_levantamiento</b>, se utiliza el texto 'Construccion' ya que los datos iniciales no cuentan con información para este campo.</p>
</div>


<a class="" data-lightbox="Paso 4: Mapeo de campos punto levantamiento" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos18.png" title="Paso 4: Mapeo de campos punto levantamiento" data-title="Paso 4: Mapeo de campos punto levantamiento"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos18.png" class="align-center" width="800px" alt="Paso 4: Mapeo de campos punto levantamiento"/></a>

Después, debes ejecutar el proceso de importación de datos dando clic al botón `Ejecutar`, obteniendo el siguiente resultado:

<a class="" data-lightbox="Resultado punto levantamiento" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos19.png" title="Resultado punto levantamiento" data-title="Resultado punto levantamiento"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos19.png" class="align-center" width="800px" alt="Resultado punto levantamiento"/></a>

### Puntos de Control

#### Paso 1: Importación del CSV puntos de control

Los *'Puntos de Control'* se importarán a través de un archivo con extensión \*.csv. Para ello debes abrir el **Administrador de fuentes de datos** de QGIS, el cual despliega una interfaz en donde se debe seleccionar la opción **Texto delimitado**. Luego es necesario seleccionar la opción **CSV (valores separados por coma)** y posteriormente en la casilla del nombre del archivo presionas el botón de los puntos suspensivos para ubicar el archivo **topo_punto_control.csv**, que se encuentra en los insumos suministrados.

<a class="" data-lightbox="Paso 1: Importación del csv puntos de control" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos22.gif" title="Paso 1: Importación del csv puntos de control" data-title="Paso 1: Importación del csv puntos de control"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos22.gif" class="align-center" width="800px" alt="Paso 1: Importación del csv puntos de control"/></a>

#### Paso 2: Definición de la geometría

En la misma interfaz debes dirigirte a desplegar las opciones de **definición de la geometría**. Verifica que en el **campo X** se encuentre el atributo **lon**, que en el **campo Y** esté el atributo **lat** y por último, que en el **SRC de la geometría** se relacione la proyección **9377 - MAGNA-SIRGAS / Origen-Nacional**.

Una vez que se cumpla con estos requisitos, se debe dar clic en el botón `Añadir`.

<a class="" data-lightbox="Paso 2: Definición de la geometría punto control" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos21.gif" title="Paso 2: Definición de la geometría punto control" data-title="Paso 2: Definición de la geometría punto control"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos21.gif" class="align-center" width="800px" alt="Paso 2: Definición de la geometría punto control"/></a>

#### Paso 3: Creación de punto control

Para iniciar con el proceso de importación debes dirigirte a la barra de herramientas del plugin y hacer clic en **Crear objetos de levantamiento -> Crear punto**.

 <a class="" data-lightbox="Paso 3: Creación de punto control" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos16.png" title="Paso 3: Creación de punto control" data-title="Paso 3: Creación de punto control"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos16.png" class="align-center" width="400px" alt="Paso 3: Creación de punto control"/></a>

#### Paso 4: Selección de los datos punto control

Al realizar el paso 2 se desplegará un cuadro de diálogo donde se deberá seleccionar el tipo de punto a insertar, en este caso: **Punto Control**. Confirma por medio del botón `Siguiente`, y escoge el conjunto de datos fuente para el procesamiento, que para este caso corresponde a la capa **topo_punto\_control**. Finalmente presiona el botón `Importar`.

<a class="" data-lightbox="Paso 4: Selección de los datos punto levantamiento" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos23.gif" title="Paso 4: Selección de los datos punto levantamiento" data-title="Paso 4: Selección de los datos punto levantamiento"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos23.gif" class="align-center" width="800px" alt="Paso 4: Selección de los datos punto levantamiento"/></a>

#### Paso 5: Mapeo de campos punto control  

Se recomienda tener en cuenta el [paso 5](#paso-5-definicion-del-mapeo-de-campos-para-punto-lindero) de la sección de punto de lindero. Para este caso, debemos asignar los valores de la siguiente manera:

| Atributo               | Expresión                                                    |
| ---------------------- | ------------------------------------------------------------ |
| id_punto_levantamiento | nombre                                                       |
| puntotipo              | get_domain_code_from_value('lc_puntotipo', punto_tipo, True, False) |
| tipo_punto_control     | get_domain_code_from_value('lc_puntocontroltipo', 'Control', True, False) |
| exactitud_horizontal   | 1                                                            |
| exactitud_vertical     | 1                                                            |
| metodoproduccion       | get_domain_code_from_value('col_metodoproducciontipo', 'Metodo_Directo', True, False) |

<div class="warning">
<p class="admonition-title">ADVERTENCIA</p>
<p>Para el caso del campo <b>metodoproduccion</b>, se utiliza el texto 'Metodo_Directo' ya que los datos iniciales no cuentan con información para este campo.</p>
<p>Para el caso del campo <b>tipo_punto_control</b>, se utiliza el texto 'Control' ya que los datos iniciales no cuentan con información para este campo.</p>
</div>


<a class="" data-lightbox="Paso 5: Mapeo de campos punto control" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos24.png" title="Paso 5: Mapeo de campos punto control" data-title="Paso 5: Mapeo de campos punto control"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos24.png" class="align-center" width="800px" alt="Paso 5: Mapeo de campos punto control"/></a>

Después, debes ejecutar el proceso de importación de datos dando clic al botón `Ejecutar`, obteniendo el siguiente resultado:

<a class="" data-lightbox="Resultado punto control" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos25.png" title="Resultado punto control" data-title="Resultado punto control"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos25.png" class="align-center" width="800px" alt="Resultado punto control"/></a>   

### Linderos

#### Paso 1: Cargue capa topo\_lindero

El proceso de creación de linderos es muy similar a la creación de puntos. Se inicia con la carga de la capa suministrada llamada **topo_lindero**, de la siguiente manera:

  <a class="" data-lightbox="Paso 1: Cargue capa topo lindero" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos27.gif" title="Paso 1: Cargue capa topo lindero" data-title="Paso 1: Cargue capa topo lindero"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos27.gif" class="align-center" width="800px" alt="Paso 1: Cargue capa topo lindero"/></a>

#### Paso 2: Creación de linderos

En la barra de herramientas del Asistente LADM-COL, presiona el botón ``Crear objetos de levantamiento`` y selecciona la opción **Crear lindero**. Esto despliega un nuevo cuadro de diálogo en el cual debes elegir la opción **Desde otra capa de QGIS** y seleccionar la capa recién cargada, llamada **topo_lindero**. Posteriormente, haz clic en el botón ``Importar``.

<a class="" data-lightbox="Paso 2: Creación de linderos" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos28.gif" title="Paso 2: Creación de linderos" data-title="Paso 2: Creación de linderos"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos28.gif" class="align-center" width="800px" alt="Paso 2: Creación de linderos"/></a>

#### Paso 3: Mapeo de campos lindero 

Se recomienda tener en cuenta el [paso 5](#paso-5-definicion-del-mapeo-de-campos-para-punto-lindero) de la sección de punto de lindero. Para este caso, debemos asignar los valores de la siguiente manera:

| Atributo                 | Expresión                                                    |
| ------------------------ | ------------------------------------------------------------ |
| longitud                 | $length                                                      |

<div class="warning">
<p class="admonition-title">ADVERTENCIA</p>
<p>Para el caso del campo <b>longitud</b>, se utiliza la expresión <i>$length</i> ya que los datos iniciales no cuentan con información para este campo.</p>
</div>


<a class="" data-lightbox="Paso 3: Mapeo de campos lindero" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos24.png" title="Paso 3: Mapeo de campos lindero" data-title="Paso 3: Mapeo de campos lindero"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos24.png" class="align-center" width="800px" alt="Paso 3: Mapeo de campos lindero"/></a>

Después, debes ejecutar el proceso de importación de datos dando clic al botón `Ejecutar`, obteniendo el siguiente resultado:

<a class="" data-lightbox="Resultado linderos" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos25.png" title="Resultado linderos" data-title="Resultado linderos"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos25.png" class="align-center" width="800px" alt="Resultado linderos"/></a>

#### Paso 4: Construcción de Linderos

En el paso anterior se generó un conjunto de segmentos de línea a partir de la capa **topo_punto_lindero**. Con el objetivo de crear los linderos correctamente, es necesario que uses la herramienta ``Construir linderos``.

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>Un lindero está bien construido topológicamente si cada uno de sus nodos finales conecta con más de un lindero. En otras palabras, un lindero no puede tener un nodo final que conecte con un solo lindero. Temáticamente, los nodos finales de un lindero marcan un cambio de colindancia.</p>
</div>

Para acceder a esta herramienta, debes dirigirte a la barra de herramientas y dar clic en el botón ``Construir linderos``. Se habilita un cuadro de diálogo en donde se pregunta: *¿Deseas utilizar todos los linderos de la base de datos?*. Debes dar clic en *Sí* y cuando termine el proceso, click en ``Conmutar edición`` y guardar los cambios.

<a class="" data-lightbox="Paso 4: Construcción de Linderos" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos31.gif" title="Paso 4: Construcción de Linderos" data-title="Paso 4: Construcción de Linderos"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos31.gif" class="align-center" width="800px" alt="Paso 4: Construcción de Linderos"/></a>

### Relación entre Puntos de Lindero y Linderos

#### Paso 1: Creación de la relación

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>Los puntos de lindero y los linderos tienen una relación topológica, puesto que los vértices de un lindero corresponden a puntos de lindero y viceversa. Dicha relación se debe almacenar de forma explícita en el modelo LADM-COL, en la tabla <b>col_puntoccl</b>.</p>
</div>

Para llenar la tabla `col_puntoccl` con la relación entre los puntos de lindero y los linderos, se debe dar clic en el botón ``Llenar PuntosCCL`` ubicado en la barra de herramientas. Al hacerlo, se despliega un cuadro de diálogo en donde se pregunta *¿Quieres llenar la tabla 'col_puntoccl' para todos los linderos de la base de datos?* Para este caso debes dar clic en el botón ``Si``.

<a class="" data-lightbox="Paso 1: Creación de la relación" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos34.gif" title="Paso 1: Creación de la relación" data-title="Paso 1: Creación de la relación"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos34.gif" class="align-center" width="800px" alt="Paso 1: Creación de la relación"/></a>


#### Paso 2: Verificación de la relación

Para validar la ejecución exitosa de la herramienta, se puede abrir la tabla de atributos de la capa **col_puntoccl**, la cual se encuentra en el panel de capas dentro del grupo llamado *tables*.

Una vez que te ubiques sobre la capa **col_puntoccl**, debes dar clic en el botón ``Abrir tabla de atributos`` y se visualizará la información registrada.

<a class="" data-lightbox="Paso 2: Verificación de la relación" href="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos35.gif" title="Paso 2: Verificación de la relación" data-title="Paso 2: Verificación de la relación"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap4preinsumos35.gif" class="align-center" width="800px" alt="Paso 2: Verificación de la relación"/></a>

## Unidad Espacial

### Terrenos

#### Paso 1: Creación de terreno

Dirígete al botón `Crear objetos de Levantamiento` (ubicado en la barra de herramientas) y selecciona la opción **Crear Terreno**:

<a class="" data-lightbox="Paso 1: Creación de terreno" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales1.png" title="Paso 1: Creación de terreno" data-title="Paso 1: Creación de terreno"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales1.png" class="align-center" width="400px" alt="Paso 1: Creación de terreno"/></a>

#### Paso 2: Selección de linderos

Se desplegará una ventana en la cual se te consulta *¿Cómo te gustaría crear terrenos?*, allí cuentas con dos opciones: *Seleccionando linderos existentes* ó *Desde otra capa de QGIS (definiendo un mapeo de campos)*.

En este caso, se procede a elegir la opción **Seleccionando linderos existentes** y luego das clic en el botón **Siguiente**. En el cuadro de diálogo que se despliega, encuentras tres opciones que corresponden con: 

1. Seleccionar lindero(s) en el mapa.
2. Seleccionar lindero(s) con base en una expresión.
3. Seleccionar todos los linderos.

Posteriormente, das clic en el botón `Seleccionar todos los linderos` y luego en el botón `Finalizar`.

<a class="" data-lightbox="Paso 2: Selección de linderos" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales2.gif" title="Paso 2: Selección de linderos" data-title="Paso 2: Selección de linderos"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales2.gif" class="align-center" width="800px" alt="Paso 2: Selección de linderos"/></a>

#### Paso 3: Cálculo del área del terreno

Una vez que los terrenos han sido creados, es necesario calcular o en su defecto actualizar el área del terreno. Para ello, debes dar clic en el botón `Abrir tabla de atributos` ubicado en la barra de herramientas. Posteriormente, elijes en el menú desplegable del lado izquierdo el atributo **Área de terreno [m2]** y das clic en el botón *Generar expresión* ![Botón generar expresion](../_static/tutorial/captura_y_estructura_de_datos/ICOdialogodeexpressiones.png), de esta forma se despliega la ventana de *"Diálogo de expresiones"*, en la cual debes emplear la función *area($geometry)*. Luego, basta con dar clic en el botón `Aceptar`. 

Finalmente, al cerrar la ventana emergente debes dar clic en el botón **Actualizar todo**, de inmediato podrás ver que en la columna **Área de terreno** se asignaron los valores de área correspondientes. Para guardar dichos cambios presiona el botón *Guardar edición* ![Botón guardar edición](../_static/tutorial/captura_y_estructura_de_datos/ICOguardarcambios.png), luego, puedes cerrar la ventana.

<a class="" data-lightbox="Paso 3: Cálculo del área del terreno" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales3.gif" title="Paso 3: Cálculo del área del terreno" data-title="Paso 3: Cálculo del área del terreno"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales3.gif" class="align-center" width="800px" alt="Paso 3: Cálculo del área del terreno"/></a>

### Relación entre Linderos y Terrenos

#### Paso 1: Creación de la relación

El diligenciamiento de esta relación se realiza con la herramienta ``Llenar más CCL y menos`` ubicada en la barra de herramientas. Al hacer clic en este botón, emergerá un cuadro de diálogo en el que se te pregunta si deseas ejecutar esta acción para todos los terrenos identificados en la base de datos. En este caso, se procede a dar clic en el botón ``Sí``.

<a class="" data-lightbox="Paso 1: Creación de la relación" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales8.gif" title="Paso 1: Creación de la relación" data-title="Paso 1: Creación de la relación"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales8.gif" class="align-center" width="800px" alt="Paso 1: Creación de la relación"/></a>

#### Paso 2: Verificación de la relación

Para verificar el estado de las relaciones creadas previamente, basta con abrir la tabla de atributos de la tabla **col_masccl**, y en la columna *ccl_mas* corroborar si los campos están diligenciados correctamente. 

<a class="" data-lightbox="Resultado de la relación entre linderos y terrenos" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales10.gif" title="Resultado de la relación entre linderos y terrenos" data-title="Resultado de la relación entre linderos y terrenos"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales10.gif" class="align-center" width="800px" alt="Resultado de la relación entre linderos y terrenos"/></a>

### Construcciones

#### Paso 1: Cargar insumo construcción

En primera medida, debes cargar a tu espacio de trabajo la capa **topo_construcciones**, para esto, debes dirigirte al **Navegador**, seleccionar **GeoPackage -> taller_asistente.gpkg** y arrastrar la capa **topo_construcciones** al mapa, para que ésta sea cargada. 

<a class="" data-lightbox="Paso 1: Cargar insumo construcción" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales11a.gif  " title="Paso 1: Cargar insumo construcción" data-title="Paso 1: Cargar insumo construcción"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales11a.gif" class="align-center" width="800px" alt="Paso 1: Cargar insumo construcción"/></a>

#### Paso 2: Creación de las construcciones

Al desplegar el menú del botón `Crear objetos de Levantamiento` (ubicado en la barra de herramientas) debes seleccionar la opción **Crear Construcción**. Esta acción abrirá una ventana en la cual se te consulta *¿Cómo te gustaría crear construcciones?*, para este caso selecciona la opción *Desde otra capa de QGIS (definiendo un mapeo de campos)*.

En este caso, harás uso de la información registrada en la capa **topo_construcciones**. De manera que luego de definir la fuente mencionada, debes dar clic en el botón `Importar`.

<a class="" data-lightbox="Paso 2: Creación de las construcciones" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales11b.gif  " title="Paso 2: Creación de las construcciones" data-title="Paso 2: Creación de las construcciones"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales11b.gif" class="align-center" width="800px" alt="Paso 2: Creación de las construcciones"/></a>

#### Paso 3: Mapeo de campos

De inmediato, se desplegará la ventana de mapeo de campos, en la cual debes realizar las modificaciones correspondientes hasta obtener un mapeo de campos como el de la siguiente imagen:

<a class="" data-lightbox="Paso 3: Mapeo de campos" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales13.png" title="Paso 3: Mapeo de campos" data-title="Paso 3: Mapeo de campos"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales13.png" class="align-center" width="800px" alt="Paso 3: Mapeo de campos"/></a> 

Se recomienda tener en cuenta el [paso 5](#paso-5-definicion-del-mapeo-de-campos-para-punto-lindero) de la sección de punto de lindero. Para este caso, debemos asignar los valores de la siguiente manera:

| Atributo                 | Expresión              |
| ------------------------ | ---------------------- |
| identificador            | $id                    |
| numero_pisos             | num_pisos              |
| area_construccion        | area($geometry)        |

<div class="warning">
<p class="admonition-title">ADVERTENCIA</p>
<p>Para el caso de <b>identificador</b>, se utiliza la expresión <i>$id</i> ya que los datos iniciales no cuentan con información para este campo.</p>
<p>Para el caso de <b>area_construccion</b>, se utiliza la expresión <i>area($geometry)</i> ya que los datos iniciales no cuentan con información para este campo.</p>
</div>

Después de completar dichas modificaciones, haz clic en el botón ``Ejecutar``. Cuando el proceso termine, puedes verificar los mensajes de la pestaña **Registro** y posteriormente cerrar la ventana.

### Unidades de Construcción

#### Paso 1: Identificación de la construcción

Para iniciar con el proceso de crear las unidades de construcción se debe emplear la herramienta **Identificar**, ubicada en la barra de herramientas de QGIS. Esto se realiza con el propósito de extraer el valor *t_id* asignado al polígono que representa la construcción de interés.

<a class="" data-lightbox="Paso 1: Identificación de la construcción" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales15.gif" title="Paso 1: Identificación de la construcción" data-title="Paso 1: Identificación de la construcción"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales15.gif" class="align-center" width="800px" alt="Paso 1: Identificación de la construcción"/></a>

#### Paso 2: Creación de unidades de construcción

Después de identificar el *t_id* de la construcción, se procede a crear las unidades de construcción. Para ello debes dirigirte a **LADM-COL –> Captura Y Estructuración De Datos –> Levantamiento Catastral –> Unidad Espacial –> Crear Unidad De Construcción**

De inmediato se desplegará un cuadro de diálogo, en el cual se te consulta como generar la unidad de construcción, puedes elegir entre cargar una capa vectorial o digitalizar el contenido. En este caso, se empleará la opción de digitalización, posteriormente das clic en el botón `Crear`.

<a class="" data-lightbox="Paso 2: Creación de unidades de construcción" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales17.gif" title="Paso 2: Creación de unidades de construcción" data-title="Paso 2: Creación de unidades de construcción"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales17.gif" class="align-center" width="800px" alt="Paso 2: Creación de unidades de construcción"/></a>

#### Paso 3: Formulario de la unidad de construcción

Al cerrarse la ventana se activará la herramienta de *Autoensamblado*, la cual ayudará con el proceso de digitalización, apoyándose de los *Puntos levantamiento* para definir la unidad de construcción. Digitaliza el polígono correspondiente. Tan pronto termines, debes dar clic derecho para finalizar este proceso.

Esta acción desplegará un formulario, el cual tiene casillas resaltadas, las cuales indican que es obligatorio diligenciar dichos campos. En la sección **lc_construccion** diligencia el **t_id** de la construcción consultada previamente.

<a class="" data-lightbox="Paso 3: Formulario de la unidad de construcción" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales18.gif" title="Paso 3: Formulario de la unidad de construcción" data-title="Paso 3: Formulario de la unidad de construcción"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales18.gif" class="align-center" width="800px" alt="Paso 3: Formulario de la unidad de construcción"/></a>

#### Paso 4: Resultado de la unidad de construcción

Finalmente, al cerrar el cuadro de diálogo, podrás visualizar un sólido en 2.5D que representa la unidad de construcción:

<a class="" data-lightbox="Paso 4: Resultado de la unidad de construcción" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales22.png" title="Paso 4: Resultado de la unidad de construcción" data-title="Paso 4: Resultado de la unidad de construcción"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales22.png" class="align-center" width="800px" alt="Paso 4: Resultado de la unidad de construcción"/></a>

### Servidumbre de tránsito

#### Paso 1: Creación de Servidumbre de tránsito

Para crear una *Servidumbre de tránsito*, debes dirigirte a la opción **Crear objetos de levantamiento –> Crear Servidumbre de tránsito** en la barra de herramientas.

De inmediato, se desplegará un cuadro de diálogo que habilitará tres (3) opciones: *Digitalizando el eje*, *Digitalizando polígono* y *Desde otra capa de QGIS*. Para este caso, selecciona la segunda opción, posteriormente das clic en el botón `Crear`.

<a class="" data-lightbox="Paso 1: Creación de Servidumbre de tránsito" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales23.gif" title="Paso 1: Creación de Servidumbre de tránsito" data-title="Paso 1: Creación de Servidumbre de tránsito"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales23.gif" class="align-center" width="800px" alt="Paso 1: Creación de Servidumbre de tránsito"/></a>

#### Paso 2: Formulario de la Servidumbre de tránsito

Al cerrar la ventana anterior, se habilitará la opción para digitalizar la *Servidumbre de tránsito* junto con la herramienta de *Autoensamblado*. Grafica el polígono de tu interés y da clic derecho al finalizar la digitalización.

Una vez que termines la digitalización del polígono, se desplegará un formulario que tiene algunas casillas resaltadas, las cuales deben diligenciarse de forma obligatoria.

<a class="" data-lightbox="Paso 2: Formulario de la Servidumbre de tránsito" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales24.gif" title="Paso 2: Formulario de la Servidumbre de tránsito" data-title="Paso 2: Formulario de la Servidumbre de tránsito"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales24.gif" class="align-center" width="800px" alt="Paso 2: Formulario de la Servidumbre de tránsito"/></a>

#### Paso 3: Resultado de la Servidumbre de tránsito

Finalmente, al cerrar el cuadro de diálogo podrás visualizar un polígono que representa la Servidumbre de tránsito.

<a class="" data-lightbox="Paso 3: Resultado de la Servidumbre de tránsito" href="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales25.png" title="Paso 3: Resultado de la Servidumbre de tránsito" data-title="Paso 3: Resultado de la Servidumbre de tránsito"><img src="../_static/tutorial/captura_y_estructura_de_datos/cap5undespaciales25.png" class="align-center" width="800px" alt="Paso 3: Resultado de la Servidumbre de tránsito"/></a>

## Unidad Básica Administrativa

### Crear Predio

## Interesados

### Crear Agrupación De Interesados

## Fuentes

## RRR

### Crear Derecho