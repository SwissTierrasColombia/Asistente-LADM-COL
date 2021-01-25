# Barra de herramientas

Así es como se ve la barra de herramientas:

<img src="_static/barra_de_herramientas/ladm_col_toolbar.png" alt="Barra de herramientas Asistente LADM-COL" />

Si la barra de herramientas no aparece en la interfaz de QGIS, puedes hacer que se vea
con la siguiente interacción: click derecho en la región gris en QGIS y clickeando
en "Herramientas LADM-COL" o como en el siguiente gif:

<img src="_static/barra_de_herramientas/show_ladm_col_toolbar.gif" alt="Mostrar barra de herramientas Asistente LADM-COL" style="height:500px;width:800px" />



## Construir linderos

## Mover nodos

## Llenar PuntosCCL


Puedes llenar la tabla de topología PuntosCCL usando el botón Llenar PuntosCCL en la barra
de herramientas de LADM_COL el cual hace este trabajo de forma automática y más rápido.

Estas son las tablas que se relacionan con esta función:
- puntosccl –> puntolindero y lindero

<img src="_static/barra_de_herramientas/fill_points_bfs.gif" alt="Llenar puntos CCL" style="height:500px;width:800px" />



## Llenar más y menos CCL

Puedes llenar la tabla de topología más CCL y menos usando el botón Llenar más CCL y menos
usando la barra de herramientas de LADM_COL el cual hace este trabajo de forma automática y más rápido.

Estas son las tablas que se relacionan con esta función:

- masccl –> terreno y lindero
- menos –> terreno y lindero (agujeros o anillos internos)

<img src="_static/barra_de_herramientas/fill_more_and_less_bfs.gif" alt="Llenar más y menos CCL" style="height:500px;width:800px" />



## Llenar relaciones de Servidumbre de paso

Debes seleccionar una **Servidumbre de Paso**, uno o más **Terreno(s)** que serán beneficiados
con la servidumbre de paso, y una o más **Fuentes Administrativa(s)** que soporte(n) la servidumbre de paso.
El plugin automáticamente crea la relación entre los predios beneficados y las relaciones.
Es importante saber que debes tener las relaciones entre los predios y
los terrenos para evitar inconvenientes con esta función.

<img src="_static/barra_de_herramientas/fill_relations_right_of_way.gif" alt="Llenar relaciones de Servidumbre de paso" style="height:500px;width:800px" />

