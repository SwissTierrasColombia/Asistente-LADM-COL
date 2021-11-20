# Barra de herramientas

La barra de herramientas del Asistente LADM-COL ofrece varios grupos de funcionalidades que se ordenan de acuerdo al módulo al que pertenecen.

Así luce la barra de herramientas del Asistente LADM-COL (rol Avanzado):

<a class="" data-lightbox="Barra de herramientas para el rol avanzado" href="./_static/barra_de_herramientas/ladm_col_toolbar.png" title="Barra de herramientas para el rol avanzado" data-title="Barra de herramientas para el rol avanzado"><img src="./_static/barra_de_herramientas/ladm_col_toolbar.png" class="align-center" width="800px" alt="Barra de herramientas para el rol avanzado"/></a>

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>Si la barra de herramientas no aparece en la interfaz de QGIS, puedes hacer que se vea de la siguiente manera: dar clic derecho en una sección libre de las barras de herramientas de QGIS y seleccionar <i>Herramientas LADM-COL</i>, como se muestra en el siguiente GIF.</p>
</div>

<a class="" data-lightbox="Mostrar barra de herramientas Asistente LADM-COL" href="./_static/barra_de_herramientas/show_ladm_col_toolbar.gif" title=" Mostrar barra de herramientas Asistente LADM-COL " data-title=" Mostrar barra de herramientas Asistente LADM-COL "><img src="./_static/barra_de_herramientas/show_ladm_col_toolbar.gif" class="align-center" width="800px" alt=" Mostrar barra de herramientas Asistente LADM-COL "/></a>

<div class="warning">
<p class="admonition-title">ADVERTENCIA</p>
<p>La barra de herramientas no es visible en la interfaz de QGIS si el Asistente LADM-COL no tiene una conexión válida a una base de datos.<br><br> Esto sucede justo después de la primera instalación del plugin, pero puede ocurrir incluso después de instalado. Por ejemplo, si se define una conexión a una base de datos GeoPackge, se cierra QGIS, se borra o mueve el archivo de base de datos y se vuelve a abrir QGIS. El Asistente reconocerá que no hay conexión válida y evitará mostrr la barra de herramientas.</p>
</div>


Los grupos de funcionalidades son los siguientes:
## Sistema de transición (1)
<a class="" data-lightbox="Sistema de Transición" href="./_static/barra_de_herramientas/toolbar_ST.png" title="Sistema de Transición" data-title="Sistema de Transición"><img src="./_static/barra_de_herramientas/toolbar_ST.png" class="align-center" width="200px" alt="Sistema de Transición"/></a>

## Crear objetos de levantamiento (2)
<a class="" data-lightbox="Crear objetos de Levantamiento" href="./_static/barra_de_herramientas/crear_objetos_lev.png" title="Crear objetos de Levantamiento" data-title="Crear objetos de Levantamiento"><img src="./_static/barra_de_herramientas/crear_objetos_lev.png" class="align-center" width="200px" alt="Crear objetos de Levantamiento"/></a>

## Cargar capas (3)
<a class="" data-lightbox="Cargar capas" href="./_static/barra_de_herramientas/cargar_capas.png" title="Cargar capas" data-title="Cargar capas"><img src="./_static/barra_de_herramientas/cargar_capas.png" class="align-center" width="60px" alt="Cargar capas"/></a>

## Construir linderos (4)

<a class="" data-lightbox="Construir linderos" href="./_static/barra_de_herramientas/build_boudaries.gif" title="Construir linderos" data-title="Construir linderos"><img src="./_static/barra_de_herramientas/build_boudaries.gif" class="align-center" width="800px" alt="Construir linderos"/></a>

## Mover nodos (5)

<a class="" data-lightbox="Mover nodos" href="./_static/barra_de_herramientas/mover_nodos.gif" title="Mover nodos" data-title="Mover nodos"><img src="./_static/barra_de_herramientas/mover_nodos.gif" class="align-center" width="800px" alt="Mover nodos"/></a>

## Llenar PuntosCCL (6)

La tabla de topología `PuntosCCL` puede llenarse de forma automática usando el botón `Llenar PuntosCCL`  de la barra de herramientas del Asistente LADM-COL.

La tabla `PuntosCCL` relaciona Puntos de Lindero con sus Linderos correspondientes.

<a class="" data-lightbox="Llenar puntos CCL" href="./_static/barra_de_herramientas/fill_points_bfs.gif" title="Llenar puntos CCL" data-title="Llenar puntos CCL"><img src="./_static/barra_de_herramientas/fill_points_bfs.gif" class="align-center" width="800px" alt="Llenar puntos CCL"/></a>

## Llenar más y menos CCL (7)

Las tablas de topología `Más CCL` y `Menos` pueden ser llenadas de forma automática usando el botón `Llenar más CCL y menos` de la barra de herramientas del Asistente LADM-COL.

La tabla `MásCCL` relaciona un Terreno con sus Linderos (externos) correspondientes, mientras que la tabla `Menos` relaciona los agujeros de un Terreno con sus Linderos (internos) correspondientes.

<a class="" data-lightbox="Llenar más y menos CCL" href="./_static/barra_de_herramientas/fill_more_and_less_bfs.gif" title="Llenar más y menos CCL" data-title="Llenar más y menos CCL"><img src="./_static/barra_de_herramientas/fill_more_and_less_bfs.gif" class="align-center" width="800px" alt="Llenar más y menos CCL"/></a>

## Configuración (8)
<a class="" data-lightbox="Configuración" href="./_static/barra_de_herramientas/configuracion.png" title="Configuración" data-title="Configuración"><img src="./_static/barra_de_herramientas/configuracion.png" class="align-center" width="60px" alt="Configuración"/></a>

Al dar clic en este botón tendrás acceso a la ventana de [Configuración](configuracion.html#configuracion) del Asistente LADM-COL.

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
    <p>La barra de herramientas depende del rol activo del Asistente LADM-COL, que se puede definir en la pestaña "Avanzado" de la ventana de configuración.</p> La sección <a href="configuracion.html#funcionalidades-por-rol">Funcionalidades por rol</a> muestra las diferentes configuraciones de la barra de herramientas según el rol activo.
</div>

