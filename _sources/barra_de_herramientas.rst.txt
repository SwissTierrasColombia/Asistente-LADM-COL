Barra de herramientas
**********************
Así es como se ve la barra de herramientas:

.. image:: _static/barra_de_herramientas/ladm_col_toolbar.png
    :height: 500
    :width: 800
    :alt: Barra de herramientas Asistente LADM-COL
    :download: true
    :title: Barra de herramientas Asistente LADM-COL

Si la barra de herramientas no aparece en la interfaz de QGIS, puedes hacer que se vea
con la siguiente interacción: click derecho en la región gris en QGIS y clickeando
en «Herramientas LADM-COL» o como en el siguiente gif:

.. image:: _static/barra_de_herramientas/show_ladm_col_toolbar.gif
    :height: 500
    :width: 800
    :alt: Mostar barra de herramientas Asistente LADM-COL
    :download: true
    :title: Mostar barra de herramientas Asistente LADM-COL

Partir por segmento y Unir
---------------------------
Si necesitas unir o explotar por segmentos los linderos puedes utilizar
los botones Unir y Partir por segmento en la barra de herramientas de LADM_COL.

.. image:: _static/barra_de_herramientas/build_boudaries.gif
    :height: 500
    :width: 800
    :alt: Construir linderos
    :download: true
    :title: Construir linderos

Llenar PuntosCCL
-----------------

Puedes llenar la tabla de topología PuntosCCL usando el botón Llenar PuntosCCL en la barra
de herramientas de LADM_COL el cual hace este trabajo de forma automática y más rápido.

Estas son las tablas que se relacionan con esta función:
- puntosccl –> puntolindero y lindero

.. image:: _static/barra_de_herramientas/fill_points_bfs.gif
    :height: 500
    :width: 800
    :alt: Llenar puntos CCL
    :download: true
    :title: Llenar puntos CCL

Llenar más y menos CCL
-----------------------
Puedes llenar la tabla de topología más CCL y menos usando el botón Llenar más CCL y menos
usando la barra de herramientas de LADM_COL el cual hace este trabajo de forma automática y más rápido.

Estas son las tablas que se relacionan con esta función:

- masccl –> terreno y lindero
- menos –> terreno y lindero (agujeros o anillos internos)

.. image:: _static/barra_de_herramientas/fill_more_and_less_bfs.gif
    :height: 500
    :width: 800
    :alt: Llenar más y menos CCL
    :download: true
    :title: Llenar más y menos CCL

Llenar relaciones de Servidumbre de paso
------------------------------------------

Debes seleccionar una **Servidumbre de Paso**, uno o más **Terreno(s)** que serán beneficiados
con la servidumbre de paso, y una o más **Fuentes Administrativa(s)** que soporte(n) la servidumbre de paso.
El plugin automáticamente crea la relación entre los predios beneficados y las relaciones.
Es importante saber que debes tener las relaciones entre los predios y
los terrenos para evitar inconvenientes con esta función

.. image:: _static/barra_de_herramientas/fill_relations_right_of_way.gif
    :height: 500
    :width: 800
    :alt: Llenar relaciones de Servidumbre de paso
    :download: true
    :title: Llenar relaciones de Servidumbre de paso
