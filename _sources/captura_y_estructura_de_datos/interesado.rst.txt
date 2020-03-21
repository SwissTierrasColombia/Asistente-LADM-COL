Interesado
===========

Crear Interesado
------------------

1. Ingresando datos manualmente en un formulario

  Elige esta opción si deseas agregar un **Interesado** con un formulario.

  **Interesado** es una Persona natural o no natural que tiene derechos o a la
  que le recaen restricciones o responsabilidades referidas a uno o más *predios*.

  .. image:: ../_static/captura_y_estructura_de_datos/create_party.gif
     :height: 500
     :width: 800
     :alt: Create Party

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una
  tabla fuente hacia la tabla **col_interesado** de *LADM_COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir
  un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa este ENLACE_.

Agrupación de Interesados
--------------------------

1. Ingresando datos manualmente en un formulario

  Elige esta opción si deseas agregar una **Agrupación de Interesados** con un formulario.

  **Agrupación de Interesados** registra interesados que representan a
  grupos de personas. Se registra el grupo en sí, independientemente de las personas
  por separado. Es lo que ocurre, por ejemplo, con un grupo étnico o un groupo civil.

  Esta **Agrupación de Interesados** tiene derechos o a la que le recaen
  restricciones o responsabilidades referidas a uno o más predios.

  Puedes insertar fracciones para tener el porcentade de correspondencia
  en la **Agrupación de Interesados**, la suma de numeradores dividida por la suma de
  denominadores debe ser igual a 1, de lo contrario la creación de la agrupación no será
  permitida.

  .. image:: ../_static/captura_y_estructura_de_datos/group_party.gif
     :height: 500
     :width: 800
     :alt: Crear agrupación de interesados

.. _ENLACE: ../captura_y_estructura_de_datos/preprocesamiento.html#usar-mapeo-de-campos