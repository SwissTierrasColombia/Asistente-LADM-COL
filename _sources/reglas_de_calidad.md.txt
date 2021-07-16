# Reglas de calidad

El Asistente LADM-COL incluye un conjunto de reglas para hacer un control de calidad a datos estructurados en el modelo LADM-COL. Estas reglas de calidad permiten revisar datos y detectar inconsistencias espaciales y alfanuméricas. Para acceder a esta herramienta se debe dar clic en el menú del Asistente LADM-COL y seleccionar “Calidad” como se muestra en el siguiente GIF.

<a class="" data-lightbox="Reglas de calidad" href="_static/reglas_de_calidad/quality_rules.gif" title="Reglas de calidad" data-title="Reglas de calidad"><img src="_static/reglas_de_calidad/quality_rules.gif" class="align-center" width="800px" alt="Reglas de calidad"/></a>

El conjunto de reglas disponibles incluye:
+ [Reglas para Puntos.](#reglas-para-puntos)
+ [Reglas para Líneas.](#reglas-para-lineas)
+ [Reglas para Polígonos.](#reglas-para-poligonos)
+ [Reglas de Consistencia Lógica.](#reglas-de-consistencia-logica)

<a class="" data-lightbox="Conjunto de reglas disponibles" href="_static/reglas_de_calidad/rules_list.PNG" title="Conjunto de reglas disponibles" data-title="Conjunto de reglas disponibles"><img src="_static/reglas_de_calidad/rules_list.PNG" class="align-center" width="600px" alt="Conjunto de reglas disponibles"/></a>

Las reglas de calidad se pueden ejecutar sin haber cargado capas en el mapa o habiendo cargado previamente las capas a validar (como se mostró en la sección [Cargar Capas](cargar_capas.html#cargar-capas)). Asimismo, las reglas de calidad se pueden ejecutar una a una, por grupos, o seleccionándolas todas al tiempo. Para este último caso se da clic en el botón “Seleccionar Todas” y luego se da clic en el botón “Aceptar”.

A continuación se realiza una breve descripción de las reglas de calidad por grupos.

## Reglas para Puntos

Este grupo de reglas ayuda a validar que los puntos provenientes de un levantamiento predial no se superpongan, que estén cubiertos por los nodos de un lindero y los nodos de un terreno, entre otras. En los siguientes GIFs se muestra cómo se ejecutan dos de estas reglas y sus resultados desplegados en el mapa.

### Los Puntos de Lindero no deben superponerse

<a class="" data-lightbox="Los Puntos de Lindero no deben superponerse" href="_static/reglas_de_calidad/boundary_points_should_not_overlap.gif" title="Los Puntos de Lindero no deben superponerse" data-title="Los Puntos de Lindero no deben superponerse"><img src="_static/reglas_de_calidad/boundary_points_should_not_overlap.gif" class="align-center" width="600px" alt="Los Puntos de Lindero no deben superponerse"/></a>

### Los Puntos de Control no deben superponerse

<a class="" data-lightbox="Los Puntos de Control no deben superponerse" href="_static/reglas_de_calidad/control_points_should_not_overlap.gif" title="Los Puntos de Control no deben superponerse" data-title="Los Puntos de Control no deben superponerse"><img src="_static/reglas_de_calidad/control_points_should_not_overlap.gif" class="align-center" width="600px" alt="Los Puntos de Control no deben superponerse"/></a>

## Reglas para Líneas

Este grupo de reglas ayuda a validar algunas características que pueden presentar los linderos de un predio; como que estos no se superpongan, que los linderos estén cubiertos por los límites de uno o varios terrenos, que los linderos deben terminar en cambio de colindancia, entre otras. En los siguientes GIFs se observan los resultados al ejecutar estas reglas.

### Los Linderos no deben superponerse

<a class="" data-lightbox="Los Linderos no deben superponerse" href="_static/reglas_de_calidad/boundary_should_not_overlap.gif" title="Los Linderos no deben superponerse" data-title="Los Linderos no deben superponerse"><img src="_static/reglas_de_calidad/boundary_should_not_overlap.gif" class="align-center" width="600px" alt="Los Linderos no deben superponerse"/></a>


### Los nodos de Lindero deben estar cubiertos por Puntos de Lindero

<a class="" data-lightbox="Los nodos de Lindero deben estar cubiertos por Puntos de Lindero" href="_static/reglas_de_calidad/boundary_nodes_should_be_covered_by_boundary_point.gif" title="Los nodos de Lindero deben estar cubiertos por Puntos de Lindero" data-title="Los nodos de Lindero deben estar cubiertos por Puntos de Lindero"><img src="_static/reglas_de_calidad/boundary_nodes_should_be_covered_by_boundary_point.gif" class="align-center" width="600px" alt="Los nodos de Lindero deben estar cubiertos por Puntos de Lindero"/></a>

### Los Linderos no deben tener nodos sin conectar

<a class="" data-lightbox="Los Linderos no deben tener nodos sin conectar" href="_static/reglas_de_calidad/boundary_should_not_have_dangles.gif" title="Los Linderos no deben tener nodos sin conectar" data-title="Los Linderos no deben tener nodos sin conectar"><img src="_static/reglas_de_calidad/boundary_should_not_have_dangles.gif" class="align-center" width="600px" alt="Los Linderos no deben tener nodos sin conectar"/></a>

## Reglas para Polígonos

Este grupo de reglas ayuda a validar diferentes características que deben cumplir los elementos con geometría polígono como son los terrenos, construcciones, servidumbres y unidades de construcción. Al ejecutarlas se pueden identificar errores topológicos de la misma capa o de relaciones con otras capas. Por ejemplo, hay una regla de calidad para validar que una construcción esté contenida dentro de un polígono de terreno.

A continuación algunos ejemplos de reglas de calidad para polígonos.

### Los Terrenos no deben superponerse

<a class="" data-lightbox="Los Terrenos no deben superponerse" href="_static/reglas_de_calidad/plots_should_not_overlap.gif" title="Los Terrenos no deben superponerse" data-title="Los Terrenos no deben superponerse"><img src="_static/reglas_de_calidad/plots_should_not_overlap.gif" class="align-center" width="800px" alt="Los Terrenos no deben superponerse"/></a>

### Las Servidumbres no se deben superponer con Construcciones

<a class="" data-lightbox="Las Servidumbres no se deben superponer con Construcciones" href="_static/reglas_de_calidad/right_of_way_should_not_overlap_buildings.gif" title="Las Servidumbres no se deben superponer con Construcciones" data-title="Las Servidumbres no se deben superponer con Construcciones"><img src="_static/reglas_de_calidad/right_of_way_should_not_overlap_buildings.gif" class="align-center" width="800px" alt="Las Servidumbres no se deben superponer con Construcciones"/></a>

## Reglas de consistencia lógica

Este conjunto de reglas permite hacer validaciones sobre “reglas de negocio” definidas por la autoridad catastral o los gestores catastrales. Estas reglas de consistencia lógica pueden involucrar una o varias tablas del modelo, así:
 + Relaciones entre elementos geográficos y elementos alfanuméricos: Por ejemplo, validar que las unidades espaciales relacionadas con un predio, correspondan al tipo de predio.
 + Relaciones entre elementos alfanuméricos de una tabla con elementos alfanuméricos de otra tabla: Por ejemplo,  validar que los predios tienen asociado un (y un solo) derecho. 
 + Una sola tabla geográfica: Por ejemplo, validar que no hayan puntos de lindero duplicados.
 + Una sola tabla alfanumérica: Por ejemplo, validar una posición específica del número predial en la tabla predio.

A continuación un ejemplo de la ejecución de reglas de consistencia lógica.


<a class="" data-lightbox="Reglas de Consistencia Lógica" href="_static/reglas_de_calidad/Logical_consistency_rules.gif" title="Reglas de Consistencia Lógica" data-title="Reglas de Consistencia Lógica"><img src="_static/reglas_de_calidad/Logical_consistency_rules.gif" class="align-center" width="800px" alt="Reglas de Consistencia Lógica"/></a>

## Interpretación de resultados

En caso de encontrar algún error, el módulo de reglas de calidad generará por lo menos una capa que será cargada al panel de capas de QGIS, dentro del grupo "Errores de validación". La capa generada puede ser alfanumérica o geográfica. En el caso de las capas geográficas, los registros de la capa permitirán ubicar el error en el mapa, dependiendo de la geometría del error encontrado.

Las tablas de atributos de las capas de errores de reglas de calidad, contienen información útil que permite conocer detalles del error encontrado. Concretamente, estas capas de errores suelen incluir un identificador del registro o los registros que tienen errores (tomado del campo `t_ili_tid`, de tipo UUID), así como el código y la descripción del error, como se aprecia en el siguiente GIF.

<a class="" data-lightbox="Interpretación de resultados" href="_static/reglas_de_calidad/Interpretacion_resultados.gif" title="Interpretación de resultados" data-title="Interpretación de resultados"><img src="_static/reglas_de_calidad/Interpretacion_resultados.gif" class="align-center" width="800px" alt="Interpretación de resultados"/></a>

### Generar reporte validación de reglas y base de datos GeoPackage

Una vez se haya ejecutado un conjunto de reglas de calidad sobre datos estructurados en el modelo LADM-COL se generan dos tipos de resultados:

+ Reporte de la validación (puede ser exportado a PDF).
+ (Opcional) Grupo de capas con errores encontrados (puede ser exportado a una base de datos GeoPackage). En caso de no encontrar errores, no se generarán capas para exportar a una base de datos GeoPackage.

La manera de exportar tanto el reporte de la validación como las capas que contienen los errores detectados se puede apreciar en el siguiente GIF.

<a class="" data-lightbox="Exportación de resultados de reglas de calidad" href="_static/reglas_de_calidad/reporte_gpkg.gif" title="Exportación de resultados de reglas de calidad" data-title="Exportación de resultados de reglas de calidad"><img src="_static/reglas_de_calidad/reporte_gpkg.gif" class="align-center" width="800px" alt="Exportación de resultados de reglas de calidad"/></a>
