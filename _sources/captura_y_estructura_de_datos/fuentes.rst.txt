Fuente
=======

Fuente Administrativa
----------------------

1. Ingresando datos manualmente en un formulario

  Elige esta opción si deseas agregar una **Fuente administrativa** con un formulario.

  **Fuente administrativa** es una especialización de la clase *COL_Fuente* para almacenar
  aquellas fuentes constituidas por documentos (documento hipotecario, documentos notariales,
  documentos históricos, etc.) que documentan la relación entre instancias
  de interesados y de predios.

  .. image:: ../_static/captura_y_estructura_de_datos/create_admin_source.gif
     :height: 500
     :width: 800
     :alt: Crear fuente administrativa

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde
  una tabla fuente hacia la tabla **col_fuenteadministrativa** de *LADM_COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes
  definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

Fuente Espacial
----------------

1. Ingresando datos manualmente en un formulario

  Elige esta opción si deseas agregar una **Fuente Espacial** usando un formulario.
  (Previamente debes haber seleccionado objetos de la tabla terreno, lindero,
  puntolindero, puntolevantamiento, o puntocontro a los cuales se asociará la nueva fuente espacial)

  **Fuente espacial** es una especialización de la clase *COL_Fuente* para almacenar las fuentes
  constituidas por datos espaciales (entidades geográficas, imágenes de satélite, vuelos fotogramétricos,
  listados de coordenadas, mapas, planos antiguos o modernos, descripción de localizaciones, etc.)
  que documentan técnicamente la relación entre instancias de interesados y de predios.

  .. image:: ../_static/captura_y_estructura_de_datos/create_spatial_source.gif
     :height: 500
     :width: 800
     :alt: Create Spatial Source

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia
  la tabla **col_fuenteespacial** de *LADM_COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir
  un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

.. _ENLACE: ../captura_y_estructura_de_datos/preprocesamiento.html#usar-mapeo-de-campos