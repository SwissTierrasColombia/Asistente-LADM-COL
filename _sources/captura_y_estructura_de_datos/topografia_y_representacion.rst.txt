Topografía y representación
*****************************

Crear Punto
=============

Punto lindero
--------------

Elige esta opción para cargar puntos a la capa **Punto Lindero** del modelo *LADM_COL*.

**Punto Lindero** es una clase especializada de *LA_Punto* que almacena puntos que definen un lindero.
Lindero es una instancia de la clase *LA_BoundaryFaceString* y sus especializaciones.

1. Desde un archivo CSV con la estructura requerida

  Agrega un archivo de valores separados por coma (CSV), seleccionando el delimitador y los campos que contienen
  las coordenadas de los puntos

  .. image:: ../_static/captura_y_estructura_de_datos/create_point_boundary.gif
     :height: 500
     :width: 800
     :alt: Crear punto lindero

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una tabla
  fuente hacia la tabla **puntolindero** de *LADM_COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo
  para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

Punto Levantamiento
--------------------

Elige esta opción para cargar puntos a la capa **Punto Levantamiento** del modelo *LADM_COL*.

**Punto Levantamiento** es una clase especializada de *LA_Punto* que representa la posición horizontal de un
vértice de construcción, servidumbre o auxiliares.

1. Desde un archivo CSV con la estructura requerida

  Agrega un archivo de valores separados por coma (CSV), seleccionando el delimitador y los campos
  que contienen las coordenadas de los puntos.

  .. image:: ../_static/captura_y_estructura_de_datos/create_point_boundary.gif
     :height: 500
     :width: 800
     :alt: Crear punto levantamiento

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente
  hacia la tabla **lindero** de *LADM_COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar
  campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

Punto de Control
-----------------

Elige esta opción para cargar puntos a la capa **Punto de Control** del modelo *LADM_COL*.

**Punto de Control** es una clase especializada de *LA_Punto* que representa puntos de la densificación de
la red local, que se utiliza en la operación catastral para el levantamiento de información
fisica de los objetos territoriales.

1. Desde un archivo CSV con la estructura requerida

  Agrega un archivo de valores separados por coma (CSV), seleccionando el delimitador y los campos que contienen
  las coordenadas de los puntos.

  .. image:: ../_static/captura_y_estructura_de_datos/create_control_point.gif
     :height: 500
     :width: 800
     :alt: Crear punto control

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente
  hacia la tabla **puntocontrol** de *LADM_COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere,
  puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

Crear Lindero
==============

1. Digitalizando

  Elige esta opción si deseas agregar un **Lindero** usando las herramientas
  de digitalización de QGIS.

  **Lindero** es una clase especializada de *LA_CadenaCarasLindero* que
  permite registrar los linderos. Dos linderos no pueden cruzarse ni superponerse.

  .. image:: ../_static/captura_y_estructura_de_datos/create_boundary.gif
     :height: 500
     :width: 800
     :alt: Crear lindero

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una
  tabla fuente hacia la tabla **lindero** de *LADM_COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo
  para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

  Si necesitas unir o partir por segmentos los linderos, puedes utilizar los botones Unir y Partir por
  segmento en la barra de herramientas de *LADM-COL*.

  .. image:: ../_static/captura_y_estructura_de_datos/build_boundary.gif
     :height: 500
     :width: 800
     :alt: Construir linderos

|

  Puedes llenar la tabla de topología *PuntoCCL* usando el botón Llenar PuntosCCL en barra de herramientas
  de *LADM_COL* que hace más rápido y de forma automática este trabajo. Para usar esta función revisa
  BARRA_DE_HERRAMIENTAS_.

.. _ENLACE: ../captura_y_estructura_de_datos/preprocesamiento.html#usar-mapeo-de-campos
.. _BARRA_DE_HERRAMIENTAS: ../barra_de_herramientas.html