Importar desde estructura intermedia
*************************************
Esta seccion exponen el procedimiento a seguir para poder realizar la importación de datos masivamente desde archivos con formato de hoja de calculo a una base de datos con la estructura del modelo LADM_COL.

Requerimientos previos:

1. Datos coincidentes con la estructura intermedia, como se muestra en las imagenes:

- Estructura de Agrupación de interesados:

.. image:: ../_static/importar_desde_estructura_intermedia/group_party.png
    :height: 500
    :width: 800
    :alt: Estructura de Agrupación de interesados
    :download: true
    :title: Estructura de Agrupación de interesados

- Estructura de derecho:

.. image:: ../_static/importar_desde_estructura_intermedia/right.png
    :height: 500
    :width: 800
    :alt: Estructura de derecho
    :download: true
    :title: Estructura de derecho

- Estructura de interesado:

.. image:: ../_static/importar_desde_estructura_intermedia/party.png
    :height: 500
    :width: 800
    :alt: Estructura de interesado
    :download: true
    :title: Estructura de interesado

- Estructura de predio:

.. image:: ../_static/importar_desde_estructura_intermedia/parcel.png
    :height: 500
    :width: 800
    :alt: Estructura de predio
    :download: true
    :title: Estructura de predio

`Plantilla en blanco de estructura intermedia. <../_static/importar_desde_estructura_intermedia/data_templates/estructura_vacia.xlsx>`_
`Datos de ejemplo según la estructura intermedia. <../_static/importar_desde_estructura_intermedia/data_templates/estructura.xlsx>`_

El procedimiento es el siguiente:

1. En la barra de herramientas dar click en el boton que dice: «Importar desde estructura intermedia»
2. Seleccione el archivo con formato de hoja de calculo donde se encuentra almacenada la información a ser cargada
3. Aceptar el diálogo y esperar por el resultado.
4. Confirmar que en QGIS se crearon las tablas intermedias y que las tablas del modelo implicadas quedaron con nuevos datos.

La ejecución del modelo con los datos de ejemplo debe genberar el siguiente resultado:

- Tablas intermedias:

.. image:: ../_static/importar_desde_estructura_intermedia/intermediate_tables.png
    :alt: Tablas intermedias
    :download: true
    :title: Tablas intermedias

- Tablas del modelo implicadas:

.. image:: ../_static/importar_desde_estructura_intermedia/relate_table.png
    :alt: Tablas del modelo implicadas
    :download: true
    :title: Tablas del modelo implicadas

- Un ejemplo del procedimiento haciendo uso de los datos de ejemplo:

.. image:: ../_static/importar_desde_estructura_intermedia/import_intermediate_structure.gif
    :height: 500
    :width: 800
    :alt: Importar desde estructura intermedia
    :download: true
    :title: Importar desde estructura intermedia
