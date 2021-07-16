# Cargar capas

El Asistente LADM-COL tiene una herramienta para cargar capas conservando las características del modelo .ili con el que se generó la base de datos.

Esta herramienta permite acceder a un listado completo de capas de la base de datos, permitiendo seleccionar aquellas que se quieren cargar a QGIS. Dicha selección puede hacerse manualmente en el listado de capas o haciendo uso de conjuntos de capas por temática, como se mostrará en breve.

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>La herramienta "Cargar Capas" del Asistente LADM-COL, realiza de forma automática la configuración de dominios,  relaciones, formularios de edición y simbología para las capas de una base de datos LADM-COL.</p>
</div>

Después de haber creado la [estructura LADM-COL](administracion_de_datos.html#crear-estructura-ladm-col) en la base de datos donde se guardarán los datos, y luego de haber realizado bien sea la importación de estos a partir del archivo XTF del conjunto de datos (como se describe en la sección [Importar datos](administracion_de_datos.html#importar-datos)), o la generación manual de datos (como se explica en [Captura y estructuración de datos](captura_y_estructura_de_datos.html#captura-y-estructuracion-de-datos)), se procede a cargar capas a QGIS con el fin de explorar los datos, como se ilustra en la siguiente animación.

<a class="" data-lightbox="Cargar capas" href="_static/cargar_capas/load_layers.gif" title="Cargar capas" data-title="Cargar capas"><img src="_static/cargar_capas/load_layers.gif" class="align-center" width="800px" alt="Cargar capas"/></a>



Las capas se muestran en grupos, según el modelo LADM-COL al cual pertenezcan. En la parte inferior de la ventana interna hay tres _check boxes_ (cajas de chequeo) que permiten ver u ocultar en el listado de capas, los dominios, estructuras y asociaciones que contenga la base de datos. No se despliegan por defecto, con el fin de que el usuario pueda manipular las capas básicas de forma más clara. Los tres *check boxes* son:

* **Mostrar dominios**: Muestra los diferentes dominios del modelo. Ejemplo: *LC_CondicionPredioTipo*.
* **Mostrar estructuras**: Muestra las tablas de tipo "Estructura" del modelo. Ejemplo: *Dirección*.
* **Mostrar asociaciones**: Muestra las tablas de paso originadas por relaciones muchos a muchos (M:N) entre tablas y/o capas geográficas. Ejemplo: *COL_UEBAUnit*.

<a class="" data-lightbox="Cajas de chequeo" href="_static/cargar_capas/Cajas_seleccion.png" title="Cajas de chequeo" data-title="Cajas de chequeo"><img src="_static/cargar_capas/Cajas_seleccion.png" class="align-center" width="800px" alt="Cajas de chequeo"/></a>

En la parte inferior de la ventana *Cargar Capas* existe un menú desplegable llamado "**Seleccionar tablas predefinida para**", que permite seleccionar un conjunto de capas previamente asociados por temática, sin tener que seleccionar una a una, como son los datos de interesados, los datos de derechos y los datos de Punto Lindero, Lindero y Terreno.

Al seleccionar una de las opciones se observa que en el listado de capas aparecen capas seleccionadas por temática. Al dar clic en Aceptar, dichas capas se cargan al panel de capas y al mapa de QGIS, como se aprecia en la siguiente animación.

<a class="" data-lightbox="Conjuntos predefinidos de capas" href="_static/cargar_capas/tablas_predefinidas.gif" title="Conjuntos predefinidos de capas" data-title="Conjuntos predefinidos de capas"><img src="_static/cargar_capas/tablas_predefinidas.gif" class="align-center" width="800px" alt="Conjuntos predefinidos de capas"/></a>

