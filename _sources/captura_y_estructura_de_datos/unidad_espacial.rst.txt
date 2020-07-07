Unidad Espacial
================

Crear Terreno
--------------

1. Seleccionando linderos existentes

  Elige esta opción si deseas crear un **Terreno** a partir de *Linderos* existentes.

  **Terreno** es una porción de tierra con una extensión geográfica definida.

  .. image:: ../_static/captura_y_estructura_de_datos/create_plot.gif
     :height: 500
     :width: 800
     :alt: Crear terreno

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente hacia la capa
  **terreno** de LADM_COL.

  Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar campos
  y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

Crear Construcción
-------------------

1. Digitalizando

  Elige esta opción si deseas crear una **Construcción** a partir de *Puntos de Levantamiento* existentes.

  **Construcción** es un tipo de espacio jurídico de la unidad de edificación del modelo LADM que almacena datos
  específicos del avalúo resultante del mismo.

  .. image:: ../_static/captura_y_estructura_de_datos/create_building.gif
     :height: 500
     :width: 800
     :alt: Crear construcción

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente hacia
  la capa **construcción** de *LADM_COL*.

  Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar
  campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

Crear Unidad de Construcción
-----------------------------

1. Digitalizando

  Elige esta opción si deseas crear una **Unidad de Construcción** a partir
  de *Puntos de Levantamiento* existentes.

  **Unidad de Construcción** es cada conjunto de materiales consolidados dentro de un Predio que tiene unas
  caracteristicas específicas en cuanto a elementos constitutivos físicos y usos de los mismos.

  .. image:: ../_static/captura_y_estructura_de_datos/create_building_unit.gif
     :height: 500
     :width: 800
     :alt: Crear unidad de construcción

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente hacia
  la capa *unidad de construccion* de *LADM_COL*.

  Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar
  campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

Crear Servidumbre de Paso
--------------------------

1. Digitalizando eje

  Elige esta opción si deseas crear una **Servidumbre de paso** digitalizando el eje a partir de
  *Puntos de Levantamiento* existentes y dando un valor de ancho.

  **Servidumbre de paso** es un tipo de unidad espacial del modelo LADM que premite la representación de servidumbres
  de paso asociadas a una *LA_BAUnit*.

  .. image:: ../_static/captura_y_estructura_de_datos/create_right_of_way_line.gif
     :height: 500
     :width: 800
     :alt: Crear servidumbre de paso digitalizando línea

2. Digitalizando Polígono

  Elige esta opción si deseas crear una **Servidumbre de paso** digitalizando un polígono a partir
  de *Puntos de Levantamiento* existentes.

  **Servidumbre de paso** es un tipo de unidad espacial del modelo LADM que premite la representación de
  servidumbres de paso asociadas a una *LA_BAUnit*.

  .. image:: ../_static/captura_y_estructura_de_datos/create_right_of_way_polygon.gif
     :height: 500
     :width: 800
     :alt: Crear servidumbre de paso digitalizando polígono

3. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente hacia la
  capa **Servidumbre de paso** de *LADM_COL*.

  Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar
  campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

4. Llenar relaciones de servidumbre de paso

  Para saber como usar esta función dirígete a `Barra de herramientas <../barra_de_herramientas.html#llenar-relaciones-de-servidumbre-de-paso>`_.


Relacionar Extdireccion
------------------------

Para asociar extdireccion existen dos grupos de opciones:

Creando manualmente usando Unidades Espaciales
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. A un Terreno

2. A una Construcción

3. A una Unidad de Construcción

   Para asociar la **Extdireccion** a una *Unidad Espacial* Existente, primero debes seleccionar una de estas opciones.

   Existen dos formas de relacionar

  a. **Seleccionando en el mapa**: Aquí seleccionas una *Unidad Espacial* e inmediatamente este regresará al asistente,
     esto activa el botón para crear la relación

    .. image:: ../_static/captura_y_estructura_de_datos/associate_extaddress_select_by_map.gif
       :height: 500
       :width: 800
       :alt: Extaddress seleccionando en el mapa

  b. **Seleccionando por expresión**: aquí seleccionas una Unidad Espacial usando una expresión, esta debe ser válida
     y la selección debe tomar solo un objeto espacial. Si la expresión toma dos o más objetos espaciales,
     el botón para crear la relación no se activará.

    .. image:: ../_static/captura_y_estructura_de_datos/associate_extaddress_select_by_expression.gif
       :height: 500
       :width: 800
       :alt: Extaddress seleccionando por expresión

Usando un mapeo de campos de una capa existente
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente
  hacia la capa **extdireccion** de *LADM_COL*.

  Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar
  campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

.. _ENLACE: ../captura_y_estructura_de_datos/preprocesamiento.html#usar-mapeo-de-campos