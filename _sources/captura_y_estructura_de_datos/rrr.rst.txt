RRR
======

Derecho
--------

1. Ingresando datos manualmente en un formulario (necesitas haber seleccionado Fuentes Administrativas)

  Elige esta opción si has seleccionado por lo menos una Fuente Administrativa*
  y deseas relacionar esas fuentes seleccionadas con un nuevo **Derecho** que vas
  a crear usando un formulario.


  **COL_Derecho** es una clase que registra las instancias de los derechos
  que un interesado ejerce sobre un predio. Es una especialización de la clase *LA_RRR* del propio modelo.

  .. image:: ../_static/captura_y_estructura_de_datos/create_right.gif
     :height: 500
     :width: 800
     :alt: Crear derecho

2. Desde otra tabla de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos
  desde una tabla fuente hacia la tabla **col_derecho** de *LADM_COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere,
  puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

Restricción
------------

1. Ingresando datos manualmente en un formulario (necesitas haber seleccionado Fuentes Administrativas)

  Elige esta opción si has seleccionado por lo menos una *Fuente Administrativa*
  y deseas relacionar esas fuentes seleccionadas con una nueva **Restricción** que
  vas a crear usando un formulario.

  **COL_Restricción** almacena las restricciones a las que está sometido un
  predio y que inciden sobre los derechos que pueden ejercerse sobre él.

  .. image:: ../_static/captura_y_estructura_de_datos/create_restriction.gif
     :height: 500
     :width: 800
     :alt: Crear restricción

2. Desde otra tabla de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos
  desde una tabla fuente hacia la tabla **col_restriccion** de LADM_COL.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir
  un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

Responsabilidad
----------------

1. Ingresando datos manualmente en un formulario (necesitas haber seleccionado *Fuentes Administrativas*)

  Elige esta opción si has seleccionado por lo menos una *Fuente Administrativa* y deseas relacionar
  esas fuentes seleccionadas con una nueva **Responsabilidad** que vas a crear usando un formulario.

  **COL_Responsabilidad** es una clase de tipo *LA_RRR* que registra las responsabilidades
  que las instancias de los interesados tienen sobre los predios.

  .. image:: ../_static/captura_y_estructura_de_datos/create_responsibility.gif
     :height: 500
     :width: 800
     :alt: Crear responsabilidad

2. Desde otra tabla de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde
  una tabla fuente hacia la tabla **col_responsabilidad** de *LADM_COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir
  un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

.. _ENLACE: ../captura_y_estructura_de_datos/preprocesamiento.html#usar-mapeo-de-campos