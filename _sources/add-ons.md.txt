# Add-ons

Los add-ons son complementos de QGIS que permiten extender las funcionalidades del Asistente LADM-COL, agregándole nuevos modelos LADM-COL, nuevos roles, interfaces (menús y barras de herramientas) propias para esos nuevos roles y nuevos módulos y funcionalidades.

Los add-ons pueden ser instalados desde el administrador de complementos de QGIS y siempre necesitarán tener instalado el Asistente LADM-COL.

Los add-ons permiten que otras organizaciones o sectores ofrezcan sus propias funcionalidades para datos LADM-COL, reutilizando el núcleo del Asistente LADM-COL.

**Add-ons disponibles**

+ [Add-on de ambiente](#add-on-de-ambiente).

## Add-on de ambiente

### Prerrequisitos

- QGIS version [3.22.x](https://qgis.org/downloads/QGIS-OSGeo4W-3.22.0-3.msi) o superior 
- Datos de reservas:
  - Reservas Ley Segunda
  - Sustracciones
  - Compensaciones

### Instalando el add-on en QGIS

Para realizar la instalación es necesario abrir QGIS ir al menú `Complementos → Administrar e instalar complementos`.

Una vez se abra la ventana de complementos, es necesario ir a `Configuración` y activar la opción de `Mostrar también los complementos experimentales`:

<a class="" data-lightbox="Complementos experimentales" href="_static/add_ons/screenshot_01.png" title="Complementos experimentales" data-title="Complementos experimentales"><img src="_static/add_ons/screenshot_01.png" class="align-center" width="800px" alt="Complementos experimentales"/></a>

Una vez activada la opción de mostrar complementos experimentales se regresa al menú `Todos` y se busca "Asistente LADM-COL" o simplemente "LADM".

<a class="" data-lightbox="Complementos LADM-COL" href="_static/add_ons/screenshot_02.png" title="Complementos LADM-COL" data-title="Complementos LADM-COL"><img src="_static/add_ons/screenshot_02.png" class="align-center" width="800px" alt="Complementos LADM-COL"/></a>

Se procederá a instalar tanto el Asistente LADM-COL, cómo el Add-on de ambiente, en ese orden. Se debe instalar el Asistente LADM-COL en su versión experimental.

Al instalar el Asistente LADM-COL, se abrirá un diálogo de dependencias. Se debe dar clic en `Aceptar` dejando marcadas las opciones por defecto. Al terminar la primera instalación se obtendrá el siguiente menú.

<a class="" data-lightbox="Seleccionar rol" href="_static/add_ons/screenshot_03.png" title="Seleccionar rol" data-title="Seleccionar rol"><img src="_static/add_ons/screenshot_03.png" class="align-center" width="800px" alt="Seleccionar rol"/></a>

Aquí se seleccionará temporalmente la opción `Básico` y se dará clic en `Aceptar`.

Luego se instala el Add-on de Ambiente, el cual no requiere ningún paso adicional. Una vez instalado se debe cerrar la ventana de complementos, tras lo cual se podrá observar el siguiente menú dentro de QGIS:

<a class="" data-lightbox="Menú LADM-COL Ambiente" href="_static/add_ons/screenshot_04.png" title="Menú LADM-COL Ambiente" data-title="Menú LADM-COL Ambiente"><img src="_static/add_ons/screenshot_04.png" class="align-center" width="400px" alt="Menú LADM-COL Ambiente"/></a>

El siguiente paso será cargar las capas que servirán de insumo para estructurar datos en la base de datos de ambiente:

<a class="" data-lightbox="Cargar capas insumo" href="_static/add_ons/screenshot_05.png" title="Cargar capas insumo" data-title="Cargar capas insumo"><img src="_static/add_ons/screenshot_05.png" class="align-center" width="800px" alt="Cargar capas insumo"/></a>

Lo siguiente es crear la estructura de base de datos:

<a class="" data-lightbox="Crear estructura de base de datos" href="_static/add_ons/screenshot_06.png" title="Crear estructura de base de datos" data-title="Crear estructura de base de datos"><img src="_static/add_ons/screenshot_06.png" class="align-center" width="800px" alt="Crear estructura de base de datos"/></a>

Se procede a configurar la base de datos a utilizar, la cual puede ser GeoPackage o PostgreSQL/PostGIS.

<a class="" data-lightbox="Elegir motor de base de datos" href="_static/add_ons/screenshot_07.png" title="Elegir motor de base de datos" data-title="Elegir motor de base de datos"><img src="_static/add_ons/screenshot_07.png" class="align-center" width="800px" alt="Elegir motor de base de datos"/></a>

Se escogerá en este caso GeoPackage, y posteriormente se dará la ruta donde se localizará la base de datos:

<a class="" data-lightbox="Ruta a base de datos" href="_static/add_ons/screenshot_08.png" title="Ruta a base de datos" data-title="Ruta a base de datos"><img src="_static/add_ons/screenshot_08.png" class="align-center" width="800px" alt="Ruta a base de datos"/></a>

Una vez configurado el archivo de la base de datos, se regresa a la ventana de crear estructura LADM-COL y lo siguiente será dar clic al botón de `Crear estructura LADM-COL`.

<a class="" data-lightbox="Ejecutar Crer estructura LADM-COL" href="_static/add_ons/screenshot_09.png" title="Ejecutar Crer estructura LADM-COL" data-title="Ejecutar Crer estructura LADM-COL"><img src="_static/add_ons/screenshot_09.png" class="align-center" width="800px" alt="Ejecutar Crer estructura LADM-COL"/></a>

La herramienta descargará automáticamente una librería llamada `ili2gpkg` y creará el esquema de base de datos. Al finalizar se mostrará el siguiente mensaje:

<a class="" data-lightbox="Creación exitosa estructura LADM-COL" href="_static/add_ons/screenshot_10.png" title="Creación exitosa estructura LADM-COL" data-title="Creación exitosa estructura LADM-COL"><img src="_static/add_ons/screenshot_10.png" class="align-center" width="800px" alt="Creación exitosa estructura LADM-COL"/></a>

Lo siguiente será dar clic en el botón `Cerrar`. Si se vuelve a dar clic en el menú de LADM-COL Ambiente, aparecerán nuevas funcionalidades, debido a que ahora se dispone de una base de datos con la estructura del modelo de ambiente:

<a class="" data-lightbox="Nuevas funcionalidades disponibles" href="_static/add_ons/screenshot_11.png" title="Nuevas funcionalidades disponibles" data-title="Nuevas funcionalidades disponibles"><img src="_static/add_ons/screenshot_11.png" class="align-center" width="400px" alt="Nuevas funcionalidades disponibles"/></a>

Lo siguiente será dar clic en la opción `Ejecutar ETL Ley 2da`, lo cual cargará de forma automática las capas de salida a la ventana de la ETL y sólo será necesario mapear las capas de entrada que corresponden a los datos de insumos (esto es, reserva ley 2da, sustracción y compensación):

<a class="" data-lightbox="ETL, capas de entrada" href="_static/add_ons/screenshot_12.png" title="ETL, capas de entrada" data-title="ETL, capas de entrada"><img src="_static/add_ons/screenshot_12.png" class="align-center" width="800px" alt="ETL, capas de entrada"/></a>

Así quedarían mapeadas las capas:

<a class="" data-lightbox="ETL, capas de entrada configuradas" href="_static/add_ons/screenshot_13.png" title="ETL, capas de entrada configuradas" data-title="ETL, capas de entrada configuradas"><img src="_static/add_ons/screenshot_13.png" class="align-center" width="800px" alt="ETL, capas de entrada configuradas"/></a>

Lo siguiente será dar clic en `Ejecutar` (este proceso tarda alrededor de 5 minutos o menos), el Asistente LADM-COL ejecutará una serie de geoprocesos para transformar la información de las capas hacia el modelo de Reservas de Ley 2da, el resultado será el siguiente:

<a class="" data-lightbox="Resultado ETL" href="_static/add_ons/screenshot_14.png" title="Resultado ETL" data-title="Resultado ETL"><img src="_static/add_ons/screenshot_14.png" class="align-center" width="800px" alt="Resultado ETL"/></a>

Una vez cargada la información, será posible revisar los datos cargados dentro de cada una de las capas, e incluso será posible hacer consultas a través de SQL.

<a class="" data-lightbox="Datos estructurados en LADM-COL" href="_static/add_ons/screenshot_15.png" title="Datos estructurados en LADM-COL" data-title="Datos estructurados en LADM-COL"><img src="_static/add_ons/screenshot_15.png" class="align-center" width="800px" alt="Datos estructurados en LADM-COL"/></a>

Finalmente, será posible exportar un archivo XTF entrando al menú `LADM-COL AMBIENTE → Administración de datos → Exportar datos`.

<a class="" data-lightbox="Menú exportar datos" href="_static/add_ons/screenshot_16.png" title="Menú exportar datos" data-title="Menú exportar datos"><img src="_static/add_ons/screenshot_16.png" class="align-center" width="800px" alt="Menú exportar datos"/></a>

Es posible que salga una ventana como esta, la cual se puede ignorar:

<a class="" data-lightbox="Ignorar certificados no encontrados" href="_static/add_ons/screenshot_17.png" title="Ignorar certificados no encontrados" data-title="Ignorar certificados no encontrados"><img src="_static/add_ons/screenshot_17.png" class="align-center" width="600px" alt="Ignorar certificados no encontrados"/></a>

La ventana que tiene relevancia en este caso será la siguiente:

<a class="" data-lightbox="Exportar datos a XTF" href="_static/add_ons/screenshot_18.png" title="Exportar datos a XTF" data-title="Exportar datos a XTF"><img src="_static/add_ons/screenshot_18.png" class="align-center" width="600px" alt="Exportar datos a XTF"/></a>

Aquí se deberá seleccionar la ruta al archivo de transferencia XTF para realizar la exportación.

<a class="" data-lightbox="Ruta al XTF" href="_static/add_ons/screenshot_19.png" title="Ruta al XTF" data-title="Ruta al XTF"><img src="_static/add_ons/screenshot_19.png" class="align-center" width="600px" alt="Ruta al XTF"/></a>

Una vez señalado el archivo de destino se dará clic en el botón `Exportar datos` y empezará el proceso de generación del XTF. Este proceso puede ser un poco largo (alrededor de 45 minutos).

<a class="" data-lightbox="XTF exportado exitósamente" href="_static/add_ons/screenshot_20.png" title="XTF exportado exitósamente" data-title="XTF exportado exitósamente"><img src="_static/add_ons/screenshot_20.png" class="align-center" width="600px" alt="XTF exportado exitósamente"/></a>

Al terminar el proceso, el resultado será un `export done` y se tendrá un archivo XTF válido para el modelo de Reservas de Ley 2da. El archivo obtenido es un poco pesado, debido a la cantidad de vértices que contienen las geometrías, así que si se desea abrir como texto plano (pues es un archivo XML), puede que tarde un poco. 

El archivo XTF es un archivo de transferencia de datos, que se puede comprimir para compartir con otros actores, quienes podran importarlo a su propia base de datos.

<a class="" data-lightbox="Contenido del XTF" href="_static/add_ons/screenshot_21.png" title="Contenido del XTF" data-title="Contenido del XTF"><img src="_static/add_ons/screenshot_21.png" class="align-center" width="800px" alt="Contenido del XTF"/></a>