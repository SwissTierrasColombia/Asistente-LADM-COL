# Captura y estructuración de datos

## Topografía y representación

### Crear Punto Lindero

Elige esta opción para cargar puntos a la capa **Punto Lindero** del modelo *LADM-COL*.

**Punto Lindero** es una clase especializada de *COL_Punto* que almacena los puntos que definen un lindero.

#### Desde un archivo CSV con la estructura requerida

Agrega un archivo de valores separados por coma (CSV), seleccionando el delimitador y los campos que contienen las coordenadas de los puntos.

<a class="" data-lightbox="Crear punto lindero" href="_static/captura_y_estructura_de_datos/create_point_boundary.gif" title="Crear punto lindero" data-title="Crear punto lindero"><img src="_static/captura_y_estructura_de_datos/create_point_boundary.gif" class="align-center" width="800px" alt="Crear punto lindero"/></a>

#### Desde otra capa de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **puntolindero** de *LADM_COL*.

Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

### Crear Punto Levantamiento

Elige esta opción para cargar puntos a la capa **Punto Levantamiento** del modelo *LADM-COL*.

**Punto Levantamiento** es una clase especializada de *COL_Punto* que representa la posición horizontal de un vértice de construcción, servidumbre o auxiliares.

#### Desde un archivo CSV con la estructura requerida

Agrega un archivo de valores separados por coma (CSV), seleccionando el delimitador y los campos que contienen las coordenadas de los puntos.

#### Desde otra capa de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **lindero** de *LADM-COL*.

Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

### Crear Punto de Control

Elige esta opción para cargar puntos a la capa **Punto de Control** del modelo *LADM-COL*.

**Punto de Control** es una clase especializada de *COL_Punto* que representa puntos de la densificación de la red local, que se utiliza en la operación catastral para el levantamiento de información física de los objetos territoriales.

#### Desde un archivo CSV con la estructura requerida

Agrega un archivo de valores separados por coma (CSV), seleccionando el delimitador y los campos que contienen las coordenadas de los puntos.

<a class="" data-lightbox="Crear punto controlo" href="_static/captura_y_estructura_de_datos/create_control_point.gif" title="Crear punto control" data-title="Crear punto control"><img src="_static/captura_y_estructura_de_datos/create_control_point.gif" class="align-center" width="800px" alt="Crear punto control"/></a>

#### Desde otra capa de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **puntocontrol** de *LADM-COL*.

Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función ver [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

### Crear Lindero

#### Digitalizando

Elige esta opción si deseas agregar un **Lindero** usando las herramientas
de digitalización de QGIS.

**Lindero** es una clase especializada de *COL_CadenaCarasLimite* que permite registrar los linderos. Dos linderos no pueden cruzarse ni superponerse.

<a class="" data-lightbox="Crear lindero" href="_static/captura_y_estructura_de_datos/create_boundary.gif" title="Crear lindero" data-title="Crear lindero"><img src="_static/captura_y_estructura_de_datos/create_boundary.gif" class="align-center" width="800px" alt="Crear lindero"/></a>

#### Desde otra capa de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **lindero** de *LADM-COL*.

Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

## Unidad Espacial

### Crear Terreno

#### Seleccionando linderos existentes

Elige esta opción si deseas crear un **Terreno** a partir de *Linderos* existentes.

**Terreno** es una porción de tierra con una extensión geográfica definida.

<a class="" data-lightbox="Crear terreno" href="_static/captura_y_estructura_de_datos/create_plot.gif" title="Crear terreno" data-title="Crear terreno"><img src="_static/captura_y_estructura_de_datos/create_plot.gif" class="align-center" width="800px" alt="Crear terreno"/></a>

#### Desde otra capa de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente hacia la capa **terreno** de LADM-COL.

Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

### Crear Construcción

#### Digitalizando

Elige esta opción si deseas crear una **Construcción** a partir de *Puntos de Levantamiento* existentes.

**Construcción** es un tipo de espacio jurídico de la unidad de edificación del modelo LADM-COL que almacena datos específicos del avalúo resultante del mismo.

<a class="" data-lightbox="Crear construcción" href="_static/captura_y_estructura_de_datos/create_building.gif" title="Crear construcción" data-title="Crear construcción"><img src="_static/captura_y_estructura_de_datos/create_building.gif" class="align-center" width="800px" alt="Crear construcción"/></a>

#### Desde otra capa de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente hacia la capa **construcción** de *LADM-COL*.

Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

### Crear Unidad de Construcción

#### Digitalizando

Elige esta opción si deseas crear una **Unidad de Construcción** a partir
de *Puntos de Levantamiento* existentes.

**Unidad de Construcción** es cada conjunto de materiales consolidados dentro de un Predio que tiene unas características específicas en cuanto a elementos constitutivos físicos y usos de los mismos.

<a class="" data-lightbox="Crear unidad de construcción" href="_static/captura_y_estructura_de_datos/create_building_unit.gif" title="Crear unidad de construcción" data-title="Crear unidad de construcción"><img src="_static/captura_y_estructura_de_datos/create_building_unit.gif" class="align-center" width="800px" alt="Crear unidad de construcción"/></a>

#### Desde otra capa de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente hacia la capa *unidad de construcción* de *LADM_COL*.

Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

### Crear Servidumbre de Tránsito

**Servidumbre de tránsito** es un tipo de unidad espacial del modelo LADM que premite la representación de servidumbres de tránsito asociadas a una *COL_UnidadAdministrativaBasica*.

#### Digitalizando eje

Elige esta opción si deseas crear una **Servidumbre de tránsito** digitalizando el eje a partir de *Puntos de Levantamiento* existentes y dando un valor de ancho.

<a class="" data-lightbox="Crear servidumbre de tránsito digitalizando línea" href="_static/captura_y_estructura_de_datos/create_right_of_way_line.gif" title="Crear servidumbre de tránsito digitalizando línea" data-title="Crear servidumbre de tránsito digitalizando línea"><img src="_static/captura_y_estructura_de_datos/create_right_of_way_line.gif" class="align-center" width="800px" alt="Crear servidumbre de tránsito digitalizando línea"/></a>

#### Digitalizando Polígono

Elige esta opción si deseas crear una **Servidumbre de tránsito** digitalizando un polígono a partir de *Puntos de Levantamiento* existentes.

<a class="" data-lightbox="Crear servidumbre de paso digitalizando polígono" href="_static/captura_y_estructura_de_datos/create_right_of_way_polygon.gif" title="Crear servidumbre de paso digitalizando polígono" data-title="Crear servidumbre de paso digitalizando polígono"><img src="_static/captura_y_estructura_de_datos/create_right_of_way_polygon.gif" class="align-center" width="800px" alt="Crear servidumbre de paso digitalizando polígono"/></a>

#### Desde otra capa de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente hacia la
capa **Servidumbre de tránsito** de *LADM_COL*.

Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

### Llenar relaciones de servidumbre de tránsito

Debes seleccionar una **Servidumbre de tránsito**, uno o más **Terreno(s)** que se benefician con la servidumbre de tránsito, y una o más **Fuentes Administrativas** que soporten la servidumbre de tránsito.

El `Asistente LADM-COL` automáticamente creará las relaciones entre los predios beneficiados, las servidumbres de tránsito y las fuentes administrativas. Dichas relaciones corresponden a las tablas `col_uebaunit` (predio-servidumbre de tránsito) y `col_rrrfuente` (restricción-fuente administrativa) del modelo de aplicación de Levantamiento Catastral.

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>Antes de llenar relaciones de servidumbre de tránsito, las relaciones entre predios y terrenos deben estar correctamente diligenciadas (tabla col_uebaunit). De lo contrario, la herramienta lo advertirá y no podrá continuar con el proceso.</p>
</div>

<a class="" data-lightbox="Llenar relaciones de servidumbre de tránsito" href="_static/captura_y_estructura_de_datos/fill_relations_right_of_way.gif" title="Llenar relaciones de servidumbre de tránsito" data-title="Llenar relaciones de servidumbre de tránsito"><img src="_static/captura_y_estructura_de_datos/fill_relations_right_of_way.gif" class="align-center" width="800px" alt="Llenar relaciones de servidumbre de tránsito"/></a>

### Relacionar dirección

Para asociar una dirección a una unidad espacial (terreno, construcción o unidad de construcción) existen dos opciones:

#### Ingresando datos manualmente en un formulario

Tenemos dos formas de relacionar una dirección a crear mediante formulario:

a. **Seleccionando en el mapa**: Aquí seleccionas una *Unidad Espacial* e inmediatamente este regresará al wizard activando el botón para crear la relación.

<a class="" data-lightbox="Relacionar dirección seleccionando en el mapa" href="_static/captura_y_estructura_de_datos/associate_extaddress_select_by_map.gif" title="Relacionar dirección seleccionando en el mapa" data-title="Relacionar dirección seleccionando en el mapa"><img src="_static/captura_y_estructura_de_datos/associate_extaddress_select_by_map.gif" class="align-center" width="800px" alt="Relacionar dirección seleccionando en el mapa"/></a>

b. **Seleccionando por expresión**: aquí seleccionas una Unidad Espacial usando una expresión. La expresión debe ser válida y debe tomar solo un objeto espacial. Si la expresión toma dos o más objetos espaciales, el botón para crear la relación no se activará.

<a class="" data-lightbox="Relacionar dirección seleccionando por expresión" href="_static/captura_y_estructura_de_datos/associate_extaddress_select_by_expression.gif" title="Relacionar dirección seleccionando por expresión" data-title="Relacionar dirección seleccionando por expresión"><img src="_static/captura_y_estructura_de_datos/associate_extaddress_select_by_expression.gif" class="align-center" width="800px" alt="Relacionar dirección seleccionando por expresión"/></a>

#### Desde otra capa de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente  hacia la capa Dirección de *LADM-COL*.

Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

## Unidad Administrativa Básica

### Crear Predio

#### Basado en un terreno existente

Elige esta opción si deseas crear un **Predio** basado en terrenos existentes.

**Predio** es una especialización de *COL_UnidadAdministrativaBasica*, que describe la unidad administrativa básica del catastro colombiano. El **Predio** es la unidad jurídica territorial, que está formada por el terreno y puede o no tener construcciones asociadas.

<a class="" data-lightbox="Crear predio" href="_static/captura_y_estructura_de_datos/create_parcel.gif" title="Crear predio" data-title="Crear predio"><img src="_static/captura_y_estructura_de_datos/create_parcel.gif" class="align-center" width="800px" alt="Crear predio"/></a>

#### Desde otra tabla/capa de QGIS (configurando un mapeo de campos)

Elige esta opción para abrir una ventana que te permita importar datos de una tabla fuente en la tabla *LADM-COL* **predio**.

Si la estructura del campo de entrada y el campo de salida difieren, puedes establecer un mapeo de campos para definir las transformaciones y correspondencias.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

## Interesado

### Crear interesado

#### Ingresando datos manualmente en un formulario

Elige esta opción si deseas agregar un **Interesado** llenando un formulario.

**Interesado** es una persona natural o jurídica que tiene derechos o a la
que le recaen restricciones referidas a uno o más *predios*.

<a class="" data-lightbox="Crear interesado" href="_static/captura_y_estructura_de_datos/create_party.gif" title="Crear interesado" data-title="Crear interesado"><img src="_static/captura_y_estructura_de_datos/create_party.gif" class="align-center" width="800px" alt="Crear interesado"/></a>

#### Desde otra capa de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **col_interesado** de *LADM-COL*.

Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

### Crear agrupación de interesados

#### Ingresando datos manualmente en un formulario

Elige esta opción si deseas agregar una **Agrupación de Interesados** usando un formulario.

**Agrupación de Interesados** registra interesados que representan a grupos de personas. Se registra el grupo en sí, independientemente de las personas por separado. Es lo que ocurre, por ejemplo, con un grupo étnico o un groupo civil.

Esta **Agrupación de Interesados** tiene derechos o a la que le recaen restricciones referidas a uno o más predios.

Puedes insertar fracciones para tener el porcentaje de correspondencia en la **Agrupación de Interesados**, la suma de las fracciones debe ser igual a 1, de lo contrario la creación de la agrupación no será permitida.

<a class="" data-lightbox="Crear agrupación de interesados" href="_static/captura_y_estructura_de_datos/group_party.gif" title="Crear agrupación de interesados" data-title="Crear agrupación de interesados"><img src="_static/captura_y_estructura_de_datos/group_party.gif" class="align-center" width="800px" alt="Crear agrupación de interesados"/></a>

## RRR

### Crear derecho

#### Ingresando datos manualmente en un formulario

Elige esta opción si has creado previamente por lo menos una Fuente Administrativa y deseas relacionarla a un nuevo **Derecho** que estás a punto de crear usando un formulario.

**COL_Derecho** es una clase que registra las instancias de los derechos que un interesado ejerce sobre un predio. Es una especialización de la clase *COL_DRR* del propio modelo.

<a class="" data-lightbox="Crear derecho" href="_static/captura_y_estructura_de_datos/create_right.gif" title="Crear derecho" data-title="Crear derecho"><img src="_static/captura_y_estructura_de_datos/create_right.gif" class="align-center" width="800px" alt="Crear derecho"/></a>

#### Desde otra tabla de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **col_derecho** de *LADM-COL*.

Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

### Crear restricción

#### Ingresando datos manualmente en un formulario

Elige esta opción si has creado previamente por lo menos una Fuente Administrativa y deseas relacionarla a una nueva **Restricción** que estás a punto de crear usando un formulario.

**COL_Restricción** almacena las restricciones a las que está sometido un
predio y que inciden sobre los derechos que pueden ejercerse sobre él.

<a class="" data-lightbox="Crear restricción" href="_static/captura_y_estructura_de_datos/create_restriction.gif" title="Crear restricción" data-title="Crear restricción"><img src="_static/captura_y_estructura_de_datos/create_restriction.gif" class="align-center" width="800px" alt="Crear restricción"/></a>

#### Desde otra tabla de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos
desde una tabla fuente hacia la tabla **col_restriccion** de LADM-COL.

Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

## Fuentes

### Crear fuente administrativa

#### Ingresando datos manualmente en un formulario

Elige esta opción si deseas agregar una **Fuente administrativa** usando un formulario.

**Fuente administrativa** es una especialización de la clase *COL_Fuente* para almacenar aquellas fuentes constituidas por documentos (documento hipotecario, documentos notariales, documentos históricos, etc.) que documentan la relación entre instancias de interesados y de predios.

<a class="" data-lightbox="Crear fuente administrativa" href="_static/captura_y_estructura_de_datos/create_admin_source.gif" title="Crear fuente administrativa" data-title="Crear fuente administrativa"><img src="_static/captura_y_estructura_de_datos/create_admin_source.gif" class="align-center" width="800px" alt="Crear fuente administrativa"/></a>

#### Desde otra capa de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **col_fuenteadministrativa** de *LADM-COL*.

Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

### Crear fuente espacial

#### Ingresando datos manualmente en un formulario

Elige esta opción si deseas agregar una **Fuente Espacial** usando un formulario.

**Fuente espacial** es una especialización de la clase *COL_Fuente* para almacenar las fuentes constituidas por datos espaciales (entidades geográficas, imágenes de satélite, vuelos fotogramétricos, listados de coordenadas, mapas, planos antiguos o modernos, descripción de localizaciones, etc.) que documentan técnicamente la relación entre instancias de interesados y de predios.

<a class="" data-lightbox="Crear fuente espacial" href="_static/captura_y_estructura_de_datos/create_spatial_source.gif" title="Crear fuente espacial" data-title="Crear fuente espacial"><img src="_static/captura_y_estructura_de_datos/create_spatial_source.gif" class="align-center" width="800px" alt="Crear fuente espacial"/></a>

#### Desde otra capa de QGIS (definiendo un mapeo de campos)

Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **col_fuenteespacial** de *LADM_COL*.

Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

## Subir archivos fuente pendientes

## Arreglar relaciones LADM-COL

## ¿Cómo usar el mapeo de campos?

Para importar datos directamente desde una capa/tabla origen (cargada en QGIS) a tu capa/tabla destino, generalmente necesitarás configurar un emparejamiento (o mapeo) de campos, posiblemente incluyendo transformaciones de los mismos para garantizar que los valores guardados en tu capa/tabla destino correspondan correctamente con su estructura.

<a class="" data-lightbox="Mapeo de campos" href="_static/captura_y_estructura_de_datos/example_refactor_fields.gif" title="Mapeo de campos" data-title="Mapeo de campos"><img src="_static/captura_y_estructura_de_datos/example_refactor_fields.gif" class="align-center" width="800px" alt="Mapeo de campos"/></a>

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>Si has definido mapeos anteriores para la misma capa destino, es posible elegir el mapeo a utilizar de una lista de mapeos recientes.</p>
</div>

<div class="warning">
<p class="admonition-title">ADVERTENCIA</p>
<p>Cuando importas datos usando el mapeo de campos, es muy conveniente deshabilitar cualquier cálculo automático configurado en la capa/tabla de destino. De lo contrario, los datos que provengan de la capa/tabla origen, al llegar a la capa/tabla destino, serán sobreescritos por los valores automáticos mencionados. Ver la sección <a href="configuracion.html#calcular-campos-automaticos-al-cargar-datos-masivamente">Configuración</a>.</p>
</div>
