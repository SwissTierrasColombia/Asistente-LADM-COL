# Consulta de datos

El Asistente LADM-COL permite consultar bases de datos conformes con el modelo LADM-COL. Las consultas pueden realizarse de dos maneras:

+ [Consulta alfanumérica](#consulta-alfanumerica): Por número predial, número predial anterior o folio de matrícula inmobiliaria (FMI).
+ [Consulta espacial](#consulta-espacial): Seleccionando un terreno en el mapa.

El resultado de las consultas es un árbol interactivo de datos relacionados, correspondientes a cuatro componentes temáticos:

+ [Consulta básica](#consulta-basica).
+ [Consulta jurídica](#consulta-juridica).
+ [Consulta física](#consulta-fisica).
+ [Consulta económica](#consulta-economica).

En la siguiente animación se puede observar la manera de activar el módulo de consultas. Nótese que al activar este módulo, el Asistente LADM-COL automátcamente carga las capas requeridas para llevar a cabo las consultas.

<a class="" data-lightbox="Consulta de datos" href="_static/consulta_de_datos/Consulta_información_ladm.gif" title="Consulta de datos" data-title="Consulta de datos"><img src="_static/consulta_de_datos/Consulta_información_ladm.gif" class="align-center" width="800px" alt="Consulta de datos">
</a>

## Consulta alfanumérica
Para realizar una consulta alfanumérica se debe activar la pestaña `Consulta alfanumérica` del panel de consultas, elegir el criterio o atributo por el cuál se realizará la consulta, e ingresar el valor a buscar.

<a class="" data-lightbox="Consulta alfanúmerica" href="_static/consulta_de_datos/Consulta_información_alfanúmerica_ladm.gif" title="Consulta alfanúmerica" data-title="Consulta alfanúmerica"><img src="_static/consulta_de_datos/Consulta_información_alfanúmerica_ladm.gif" class="align-center" width="800px" alt="Consulta alfanúmerica">
</a>

## Consulta espacial
Para realizar una consulta espacial se debe activar la pestaña `Consulta espacial` del panel de consultas, dar clic sobre el botón `Identificar` y finalmente dar clic sobre uno de los terrenos desplegados en el mapa.

<a class="" data-lightbox="Consulta espacial" href="_static/consulta_de_datos/Consulta_información_espacial_ladm.gif" title="Consulta espacial" data-title="Consulta espacial"><img src="_static/consulta_de_datos/Consulta_información_espacial_ladm.gif" class="align-center" width="800px" alt="Consulta espacial">
</a>

## Resultados de las consultas

### Consulta básica
Muestra los datos básicos de los objetos relacionados con el terreno, como predios, construcciones y unidades de construcción.

<a class="" data-lightbox="Consulta básica" href="_static/consulta_de_datos/Consulta_basica.png" title="Consulta básica" data-title="Consulta básica"><img src="_static/consulta_de_datos/Consulta_basica.png" class="align-center" width="400px" alt="Consulta básica">
</a>

### Consulta jurídica

Muestra los datos jurídicos asociados al terreno como los predios, derechos, fuentes administrativas, interesados, restricciones, responsabilidades y gravámenes a la propiedad como hipotecas, servidumbres, usufructos, etc.

<a class="" data-lightbox="Consulta jurídica" href="_static/consulta_de_datos/Consulta_juridica.png" title="Consulta jurídica" data-title="Consulta jurídica"><img src="_static/consulta_de_datos/Consulta_juridica.png" class="align-center" width="400px" alt="Consulta jurídica">
</a>

### Consulta física
Muestra los datos físicos del predio, como linderos y puntos de linderos que están asociados al terreno correspondiente, así como puntos de levantamiento y fuentes espaciales si están disponibles en el modelo LADM-COL.

<a class="" data-lightbox="Consulta física" href="_static/consulta_de_datos/Consulta_fisica.png" title="Consulta física" data-title="Consulta física"><img src="_static/consulta_de_datos/Consulta_fisica.png" class="align-center" width="400px" alt="Consulta física">
</a>

### Consulta económica
Muestra la información económica (avalúos, zonas homogéneas, etc.) de los objetos relacionados al terreno como predios, construcciones y unidades de construcción, así como datos del modelo extendido de avalúos de LADM-COL para estos objetos. 

<a class="" data-lightbox="Consulta económica" href="_static/consulta_de_datos/Consulta_economica.png" title="Consulta económica" data-title="Consulta económica"><img src="_static/consulta_de_datos/Consulta_economica.png" class="align-center" width="400px" alt="Consulta económica">
</a>

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>Los datos desplegados en el panel de resultados, se encuentran organizados (anidados) de acuerdo a sus relaciones. Por ejemplo, un terreno puede tener un predio relacionado, que a su vez puede estar relacionado con una o más construcciones, que a su vez pueden estar relacionadas con una o más unidades constructivas.</p>
</div>


### Resultados interactivos
Una vez desplegados los resultados de una consulta, los objetos listados ofrecen un menú contextual, que se activa al dar clic derecho sobre los mismos (por ejemplo, sobre los registros en negrita `t_id`), permitiendo acceder a funcionalidades específicas para esos objetos de la base de datos, como se aprecia en la siguiente animación.

<a class="" data-lightbox="Resultados interactivos" href="_static/consulta_de_datos/despliegue_menu_contextual.gif" title="Resultados interactivos" data-title="Resultados interactivos"><img src="_static/consulta_de_datos/despliegue_menu_contextual.gif" class="align-center" width="800px" alt="Resultados interactivos"></a>

Las herramientas que se ofrecen son:

* **Copiar valor**: Copia el valor del atributo al portapapeles.
* **Zoom a objeto geográfico**: Hace un acercamiento en el mapa encuadrando el objeto de interés.
* **Zoom a terreno asociado** (solo para objetos tipo predio): Hace un acercamiento en el mapa encuadrando el terreno asociado al predio de interés.
* **Abrir formulario para el objeto**: despliega el formulario del objeto seleccionado para visualizar todos sus atributos.

<div class="seealso">
<p class="admonition-title">TIP</p>
    Al abrir el formulario de un objeto desde el menú contextual del panel de resultados, los valores de los atributos del objeto pueden ser editados, siempre y cuando la sesión de edición de la capa correspondiente esté iniciada. Dicha edición estará sujeta al cumplimiento de <i>constraints</i> de la base de datos, que se validan al ingresar/editar atributos o al guardar la edición.
</div>

