# Captura y estructuración de datos


## Levantamiento Catastral

### Topografía y representación

#### Crear Punto

##### Punto lindero

Elige esta opción para cargar puntos a la capa **Punto Lindero** del modelo *LADM-COL*.

**Punto Lindero** es una clase especializada de *LA_Punto* que almacena puntos que definen un lindero.
Lindero es una instancia de la clase *LA_BoundaryFaceString* y sus especializaciones.

1. Desde un archivo CSV con la estructura requerida

  Agrega un archivo de valores separados por coma (CSV), seleccionando el delimitador y los campos que contienen las coordenadas de los puntos.

  <img src="_static/captura_y_estructura_de_datos/create_point_boundary.gif" alt="Crear punto lindero" style="width:800px" />

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **puntolindero** de *LADM_COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

##### Punto Levantamiento

Elige esta opción para cargar puntos a la capa **Punto Levantamiento** del modelo *LADM-COL*.

**Punto Levantamiento** es una clase especializada de *LA_Punto* que representa la posición horizontal de un vértice de construcción, servidumbre o auxiliares.

1. Desde un archivo CSV con la estructura requerida

  Agrega un archivo de valores separados por coma (CSV), seleccionando el delimitador y los campos que contienen las coordenadas de los puntos.

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **lindero** de *LADM-COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

##### Punto de Control

Elige esta opción para cargar puntos a la capa **Punto de Control** del modelo *LADM-COL*.

**Punto de Control** es una clase especializada de *LA_Punto* que representa puntos de la densificación de la red local, que se utiliza en la operación catastral para el levantamiento de información fisica de los objetos territoriales.

1. Desde un archivo CSV con la estructura requerida

  Agrega un archivo de valores separados por coma (CSV), seleccionando el delimitador y los campos que contienen las coordenadas de los puntos.

  <img src="_static/captura_y_estructura_de_datos/create_control_point.gif" alt="Crear punto control" style="width:800px" />

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **puntocontrol** de *LADM-COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)


#### Crear Lindero

1. Digitalizando

  Elige esta opción si deseas agregar un **Lindero** usando las herramientas
  de digitalización de QGIS.

  **Lindero** es una clase especializada de *LA_CadenaCarasLindero* que permite registrar los linderos. Dos linderos no pueden cruzarse ni superponerse.

  <img src="_static/captura_y_estructura_de_datos/create_boundary.gif" alt="Crear lindero" style="width:800px" />

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **lindero** de *LADM-COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

 


### Unidad Espacial

#### Crear Terreno

1. Seleccionando linderos existentes

  Elige esta opción si deseas crear un **Terreno** a partir de *Linderos* existentes.

  **Terreno** es una porción de tierra con una extensión geográfica definida.

  <img src="_static/captura_y_estructura_de_datos/create_plot.gif" alt="Crear terreno" style="width:800px" />

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente hacia la capa **terreno** de LADM-COL.

  Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

#### Crear Construcción

1. Digitalizando

  Elige esta opción si deseas crear una **Construcción** a partir de *Puntos de Levantamiento* existentes.

  **Construcción** es un tipo de espacio jurídico de la unidad de edificación del modelo LADM que almacena datos específicos del avalúo resultante del mismo.

  <img src="_static/captura_y_estructura_de_datos/create_building.gif" alt="Crear construcción" style="width:800px" />

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente hacia la capa **construcción** de *LADM-COL*.

  Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

#### Crear Unidad de Construcción

1. Digitalizando

  Elige esta opción si deseas crear una **Unidad de Construcción** a partir
  de *Puntos de Levantamiento* existentes.

  **Unidad de Construcción** es cada conjunto de materiales consolidados dentro de un Predio que tiene unas caracteristicas específicas en cuanto a elementos constitutivos físicos y usos de los mismos.

  <img src="_static/captura_y_estructura_de_datos/create_building_unit.gif" alt="Crear unidad de construcción" style="width:800px" />

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente hacia la capa *unidad de construccion* de *LADM_COL*.

  Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

#### Crear Servidumbre de tránsito

1. Digitalizando eje

  Elige esta opción si deseas crear una **Servidumbre de tránsito** digitalizando el eje a partir de *Puntos de Levantamiento* existentes y dando un valor de ancho.

  **Servidumbre de tránsito** es un tipo de unidad espacial del modelo LADM que premite la representación de servidumbres de tránsito asociadas a una *LA_BAUnit*.

  <img src="_static/captura_y_estructura_de_datos/create_right_of_way_line.gif" alt="Crear servidumbre de tránsito digitalizando línea" style="width:800px" />

2. Digitalizando Polígono

  Elige esta opción si deseas crear una **Servidumbre de tránsito** digitalizando un polígono a partir de *Puntos de Levantamiento* existentes.

  **Servidumbre de tránsito** es un tipo de unidad espacial del modelo LADM que premite la representación de servidumbres de paso asociadas a una *LA_BAUnit*.

  <img src="_static/captura_y_estructura_de_datos/create_right_of_way_polygon.gif" alt="Crear servidumbre de paso digitalizando polígono" style="width:800px" />

3. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente hacia la
  capa **Servidumbre de tránsito** de *LADM_COL*.

  Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

#### Llenar relaciones de servidumbre de tránsito

Ver [Barra de herramientas](barra_de_herramientas.html#llenar-relaciones-de-servidumbre-de-paso).

#### Relacionar dirección

Para asociar una dirección a una unidad espacial (terreno, construcción o unidad de construcción) existen dos opciones:

1. Ingresando datos manualmente en un formulario

  Tenemos dos formas de relacionar una dirección a crear mediante formulario:

  a. **Seleccionando en el mapa**: Aquí seleccionas una *Unidad Espacial* e inmediatamente este regresará al wizard activando el botón para crear la relación.

  <img src="_static/captura_y_estructura_de_datos/associate_extaddress_select_by_map.gif" alt="Relacionar dirección seleccionando en el mapa" style="width:800px" />

  b. **Seleccionando por expresión**: aquí seleccionas una Unidad Espacial usando una expresión. La expresión debe ser válida y debe tomar solo un objeto espacial. Si la expresión toma dos o más objetos espaciales, el botón para crear la relación no se activará.

  <img src="_static/captura_y_estructura_de_datos/associate_extaddress_select_by_expression.gif" alt="Relacionar dirección seleccionando por expresión" style="width:800px" />

  2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una capa fuente  hacia la capa Dirección de *LADM-COL*.

  Si la estructura de campos de las capas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)




### Unidad Administrativa Básica

#### Crear Predio

1. Basado en un terreno existente

  Elige esta opción si deseas crear un **Predio** basado en terrenos existentes.

  **Predio** es una clase *BA Unit* especializada, que describe la unidad administrativa básica del catastro colombiano. El **Predio** es la unidad jurídica territorial, que está formada por el terreno y puede o no tener construcciones asociadas.

  <img src="_static/captura_y_estructura_de_datos/create_parcel.gif" alt="Crear predio" style="width:800px" />

2. Desde otra tabla/capa de QGIS (configurando un mapeo de campos)

  Elige esta opción para abrir una ventana que te permita importar datos de una tabla fuente en la tabla *LADM-COL* **predio**.

  Si la estructura del campo de entrada y el campo de salida difieren, puedes establecer un mapeo de campos para definir las transformaciones y correspondencias.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)


### Interesado

#### Crear interesado

1. Ingresando datos manualmente en un formulario

  Elige esta opción si deseas agregar un **Interesado** llenando un formulario.

  **Interesado** es una persona natural o no natural que tiene derechos o a la
  que le recaen restricciones referidas a uno o más *predios*.

  <img src="_static/captura_y_estructura_de_datos/create_party.gif" alt="Crear interesado" style="width:800px" />

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **col_interesado** de *LADM-COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

#### Crear agrupación de interesados

1. Ingresando datos manualmente en un formulario

  Elige esta opción si deseas agregar una **Agrupación de Interesados** usando un formulario.

  **Agrupación de Interesados** registra interesados que representan a grupos de personas. Se registra el grupo en sí, independientemente de las personas por separado. Es lo que ocurre, por ejemplo, con un grupo étnico o un groupo civil.

  Esta **Agrupación de Interesados** tiene derechos o a la que le recaen restricciones referidas a uno o más predios.

  Puedes insertar fracciones para tener el porcentaje de correspondencia en la **Agrupación de Interesados**, la suma de las fracciones debe ser igual a 1, de lo contrario la creación de la agrupación no será permitida.

  <img src="_static/captura_y_estructura_de_datos/group_party.gif" alt="Crear agrupación de interesados" style="width:800px" />




### RRR

#### Crear derecho

1. Ingresando datos manualmente en un formulario

  Elige esta opción si has creado previamente por lo menos una Fuente Administrativa y deseas relacionarla a un nuevo **Derecho** que estás a punto de crear usando un formulario.

  **COL_Derecho** es una clase que registra las instancias de los derechos que un interesado ejerce sobre un predio. Es una especialización de la clase *LA_RRR* del propio modelo.

  <img src="_static/captura_y_estructura_de_datos/create_right.gif" alt="Crear derecho" style="width:800px" />

2. Desde otra tabla de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **col_derecho** de *LADM-COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

#### Crear restricción

1. Ingresando datos manualmente en un formulario

  Elige esta opción si has creado previamente por lo menos una Fuente Administrativa y deseas relacionarla a una nueva **Restricción** que estás a punto de crear usando un formulario.

  **COL_Restricción** almacena las restricciones a las que está sometido un
  predio y que inciden sobre los derechos que pueden ejercerse sobre él.

  <img src="_static/captura_y_estructura_de_datos/create_restriction.gif" alt="Crear restricción" style="width:800px" />

2. Desde otra tabla de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos
  desde una tabla fuente hacia la tabla **col_restriccion** de LADM-COL.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)


### Fuentes

#### Crear fuente administrativa

1. Ingresando datos manualmente en un formulario

  Elige esta opción si deseas agregar una **Fuente administrativa** usando un formulario.

  **Fuente administrativa** es una especialización de la clase *COL_Fuente* para almacenar aquellas fuentes constituidas por documentos (documento hipotecario, documentos notariales, documentos históricos, etc.) que documentan la relación entre instancias de interesados y de predios.

  <img src="_static/captura_y_estructura_de_datos/create_admin_source.gif" alt="Crear fuente administrativa" style="width:800px" />

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **col_fuenteadministrativa** de *LADM-COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)

#### Crear fuente espacial

1. Ingresando datos manualmente en un formulario

  Elige esta opción si deseas agregar una **Fuente Espacial** usando un formulario.

  **Fuente espacial** es una especialización de la clase *COL_Fuente* para almacenar las fuentes constituidas por datos espaciales (entidades geográficas, imágenes de satélite, vuelos fotogramétricos, listados de coordenadas, mapas, planos antiguos o modernos, descripción de localizaciones, etc.) que documentan técnicamente la relación entre instancias de interesados y de predios.

  <img src="_static/captura_y_estructura_de_datos/create_spatial_source.gif" alt="Crear fuente espacial" style="width:800px" />

2. Desde otra capa de QGIS (definiendo un mapeo de campos)

  Elige esta opción para abrir una ventana que te permite importar datos desde una tabla fuente hacia la tabla **col_fuenteespacial** de *LADM_COL*.

  Si la estructura de campos de las tablas de entrada y salida difiere, puedes definir un mapeo para transformar campos y establecer correspondencias entre ellos.

  Para usar esta función revisa [¿Cómo usar el mapeo de campos?](#como-usar-el-mapeo-de-campos)


## Subir archivos fuentes pendientes

## Arreglar relaciones LADM-COL

## ¿Cómo usar el mapeo de campos?

Puedes definir un mapeo para transofrmar campos y establecer correspondencias entre ellos, esto te permite importar los datos directamente en la base de datos desde otra capa o tabla cargada en QGIS.

Es posible elegir el mapeo a utilizar de una lista de mapeos recientes.

  <img src="_static/captura_y_estructura_de_datos/example_refactor_fields.gif" alt="Mapeo de campos" style="width:800px" />