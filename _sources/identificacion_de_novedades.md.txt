# Identificación de novedades
El Asistente LADM-COL permite comparar la información oficial de la autoridad catastral (insumos) frente a la información producto del levantamiento catastral.

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>Para usar esta funcionalidad es necesario disponer tanto de los datos oficiales (insumos) como de los datos producto del levantamiento catastral, bien sea en la misma base de datos (o esquema) o en dos bases de datos (o esquemas) diferentes.</p>
</div>

## Configuración identificación de novedades

En el menú LADM-COL de QGIS, selecciona `Identificación de novedades` y luego haz clic en `Configurar identificación de novedades` como se apecia en la imagen. Una vez allí, diligencia los parámetros y selecciona la base de datos en donde se encuentra el conjunto de datos del levantamiento catastral.

<a class="" data-lightbox="Configuración identificación de novedades" href="./_static/identificacion_de_novedades/configuracion_identificacion_novedades.gif" title="Configuración identificación de novedades" data-title="Configuración identificación de novedades"><img src="./_static/identificacion_de_novedades/configuracion_identificacion_novedades.gif" class="align-center" width="800px" alt="Configuración identificación de novedades"/></a>

## Uso de identificación de novedades

En el menú de `Identificación de novedades` se encuentran dos funcionalidades: `Consulta por predio` y `Consulta masiva`. En la primera opción se pueden consultar las novedades de un predio especifico, mientras que en la segunda opción se puede obtener un reporte en pantalla de las novedades presentadas en el total de los datos consultados.


A continuación se explican ambas opciones con más detalle.

### Consulta por predio
Al ejecutar esta funcionalidad, automáticamente se cargan al mapa de QGIS las dos fuentes de datos a comparar y se abre un panel en la parte derecha de la interfaz, que permite realizar la consulta de un predio de manera espacial (esto es, haciendo clic sobre uno de los terrenos del mapa) o por alguno de los tres siguientes atributos:
- Número predial.
- Número predial anterior..
- Folio de Matrícula Inmobiliaria.

Una vez realizada la consulta, se abre una tabla comparativa que muestra tanto el dato oficial (insumos) como el dato producto del levantamiento catastral. 

Además, en la vista del mapa se habilita de forma automática una herramienta de comparación gráfica, que permite identificar cambios de forma de la geometría de un terreno.

<a class="" data-lightbox="Consulta por predio" href="./_static/identificacion_de_novedades/consulta_predio.gif" title="Consulta por predio" data-title="Consulta por predio"><img src="./_static/identificacion_de_novedades/consulta_predio.gif" class="align-center" width="800px" alt="Consulta por predio"/></a>

La tabla comparativa del panel de identificación de novedades se compone de cuatro columnas:

+ Atributo por el cual se hace la comparación.

+ Dato de la fuente oficial (insumos).

+ Dato del levantamiento catastral.

+ Estado


El estado corresponde a un color verde si el dato no presenta cambios y a un color rojo si se encuentran cambios entre las dos fuentes de datos.

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>En la parte superior de la tabla de resultados se encuentra una caja de selección que permite alternar entre visualizar todos los predios de la fuente de datos o únicamente el predio consultado.</p>
</div>

### Consulta masiva

Al ejecutar esta funcionalidad se abre un panel en la parte derecha de la interfaz de QGIS, en donde se despliegan diferentes tipos de novedades que se pueden encontrar al realizar la comparación masiva entre las datos oficiales (insumos) y los datos de levantamiento catastral. 

Para cada tipo de novedad se muestra el conteo de cambios identificados en los dos conjuntos de datos, acompañado de un botón para ver la información de los predios que presentan ese tipo de novedad.

Al hacer clic en el botón `Ver predios` se carga un listado de números prediales y su estado. Se puede hacer doble clic sobre alguno de los resultados para observar una tabla comparativa para ese predio.

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>La herramienta de comparación gráfica solo se activa cuando se encuentre el mismo predio tanto en los datos oficiales (insumos) como en los datos de levantamiento catastral, lo cual excluye, por ejemplo, a los tipos de novedad "Altas" y "Bajas".</p>
</div>



<a class="" data-lightbox="Consulta masiva" href="./_static/identificacion_de_novedades/consulta_masiva.gif" title="Consulta masiva" data-title="Consulta masiva"><img src="./_static/identificacion_de_novedades/consulta_masiva.gif" class="align-center" width="800px" alt="Consulta masiva"/></a>

### Tipos de Novedades
A continuación se describe cada tipo de novedad:

- **Altas**: Son predios incorporados en el levantamiento catastral y que no estaban en los datos oficiales (insumos).
- **Bajas**: Son predios que no aparecen en el levantamiento catastral pero si se encuentran en los datos oficiales (insumos).
- **Predios con cambios**: Son predios que reportan algún cambio en los datos alfanuméricos o en su forma geométrica (cambios físicos).
- **Predios sin cambios**: Predios que no reportaron cambios alfanuméricos ni físicos en el levantamiento catastral en comparación a lo registrado en los datos oficiales (insumos).

Se identifican además dos grupos de predios para facilitar el análisis de cambios y/o inconsistencias:

- **Números prediales duplicados**: Identificación de números prediales asignados a predios diferentes en el levantamiento catastral.
- **Números prediales nulos**: Predios a los cuales no se les asignó un número predial.

Finalmente, se muestra un **Total de novedades**, que permite obtener un listado de todos los predios de la base de datos y su correspondiente estado.

<a class="" data-lightbox="Tipos de novedades" href="./_static/identificacion_de_novedades/resumen_novedades_masivo.png" title="Tipos de novedades" data-title="Tipos de novedades"><img src="./_static/identificacion_de_novedades/resumen_novedades_masivo.png" class="align-center" width="400px" alt="Tipos de novedades"/></a>