# Captura de datos en campo

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>El módulo de Captura de datos en campo del Asistente LADM-COL aún no se ha incluido en los lanzamientos oficiales, puesto que se trata de un módulo en desarrollo. Si estás interesado/a en este módulo, puedes contactarnos en <i>administracion [at] swisstierrascolombia [dot] com</i></p>
</div>

La captura en campo corresponde al levantamiento predial en terreno de una zona de interés por parte del Operador catastral. Comprende varias actividades, entre las que destacan:

1. Alistamiento de insumos (ver <a href="https://swisstierrascolombia.github.io/st-docs/user-manual-doc/9-rol-operador.html#gestion-de-insumos" target="_blank">Gestión de insumos en el Sistema de Transición</a>).
2. ETL de Submodelo de Insumos a Modelo de Captura en Campo.
3. [Asignación de zonas de trabajo y predios por parte del Coordinador General](#asignar-predios).
4. [Asignación de zonas de trabajo y predios por parte del Coordinador de Campo](#asignar-predios-coordinador-de-campo).
5. [Levantamiento en campo por parte de los reconocedores](#recoleccion-datos-en-campo).
6. [Sincronización de datos de campo por parte del Coordinador de Campo](#sincronizar-datos-de-campo).
7. [Sincronización de datos por parte del Coordinador General](#sincronizar-datos-coordinador-general).
8. ETL de Modelo de Captura en Campo a Modelo de aplicación Levantamiento Catastral.

El Asistente LADM-COL incluye un rol de Coordinador General y un rol de Coordinador de campo, los cuales permiten ejecutar las actividades mencionadas anteriormente. A continuación se muestra el proceso, ilustrándolo con animaciones.

***
## ETL (Submodelo Insumos - Modelo Captura en Campo) [Aún en desarrollo]

La ETL que lleva los datos del submodelo de Insumos al modelo de Captura en Campo permite estructurar los datos buscando simplificar su actualización y/o captura en campo.
***

## Asignar predios

La asignación de zonas de trabajo y predios parte del Coordinador General, a quien corresponde asignar (o entregar) un grupo de predios del municipio o área de intervención a los Coordinadores de Campo. Estos, a su vez, deben asignar la carga de trabajo a cada uno de sus Reconocedores de Campo, quienes realizarán el levantamiento catastral del total de la zona de trabajo.

#### Asignar predios (Coordinador General)

El Coordinador General está encargado de asignar a los Coordinadores de Campo la captura y gestión de los datos provenientes del Levantamiento Catastral. A continuación se ilustran sus actividades en el Asistente LADM-COL.

Selección del rol Coordinador General  y creación de base de datos maestra.

<a class="" data-lightbox="Creación de BD Coordinador General" href="_static/captura_de_datos_en_campo/0_Coor_general_asignacion_12.gif" title="Creación de BD Coordinador General" data-title="Creación de BD Coordinador General"><img src="_static/captura_de_datos_en_campo/0_Coor_general_asignacion_12.gif" class="align-center" width="800px" alt="Creación de BD Coordinador General"/></a>

Importación de datos insumos (en formato XTF) al modelo de Captura en Campo.

<a class="" data-lightbox="Importación de datos Coordinador General" href="_static/captura_de_datos_en_campo/1_Coor_general_asignacion_3.gif" title="Importación de datos Coordinador General" data-title="Importación de datos Coordinador General"><img src="_static/captura_de_datos_en_campo/1_Coor_general_asignacion_3.gif" class="align-center" width="800px" alt="Importación de datos Coordinador General"/></a>

Creación de Coordinadores de Campo.

<a class="" data-lightbox="Creación usuarios Coordinador General" href="_static/captura_de_datos_en_campo/2_Coor_general_asignacion_45.gif" title="Creación usuarios Coordinador General" data-title="Creación usuarios Coordinador General"><img src="_static/captura_de_datos_en_campo/2_Coor_general_asignacion_45.gif" class="align-center" width="800px" alt="Creación usuarios Coordinador General"/></a>

Asignación de áreas de intervennción y predios a Coordinadores de Campo.

<a class="" data-lightbox="Asignar predios Coordinador General" href="_static/captura_de_datos_en_campo/3_Coor_general_asignacion_6.gif" title="Asignar predios Coordinador General" data-title="Asignar predios Coordinador General"><img src="_static/captura_de_datos_en_campo/3_Coor_general_asignacion_6.gif" class="align-center" width="800px" alt="Asignar predios Coordinador General"/></a>

Exportación de datos (formato XTF) para los Coordinadores de Campo.

<a class="" data-lightbox="Exportar datos Coordinador General" href="_static/captura_de_datos_en_campo/4_Coor_general_asignacion_7.gif" title="Exportar datos Coordinador General" data-title="Exportar datos Coordinador General"><img src="_static/captura_de_datos_en_campo/4_Coor_general_asignacion_7.gif" class="align-center" width="800px" alt="Exportar datos Coordinador General"/></a>

#### Asignar predios (Coordinador de Campo)

El Coordinador de Campo está encargado de gestionar la captura de datos de campo provenientes del Levantamiento Catastral. Tiene a su cargo reconocedores prediales. A continuación se ilustran sus actividades en el Asistente LADM-COL.

Selección del rol Coordinador de Campo.

<a class="" data-lightbox="Selección rol Coordinador de Campo" href="_static/captura_de_datos_en_campo/5_Coor_campo_asignacion_1.gif" title="Selección rol Coordinador de Campo" data-title="Selección rol Coordinador de Campo"><img src="_static/captura_de_datos_en_campo/5_Coor_campo_asignacion_1.gif" class="align-center" width="800px" alt="Selección rol Coordinador de Campo"/></a>

Creación de base de datos con estructura del modelo de Captura en Campo.

<a class="" data-lightbox="Creación de BD Coordinador de Campo" href="_static/captura_de_datos_en_campo/6_Coor_campo_asignacion_2.gif" title="Creación de BD Coordinador de Campo" data-title="Creación de BD Coordinador de Campo"><img src="_static/captura_de_datos_en_campo/6_Coor_campo_asignacion_2.gif" class="align-center" width="800px" alt="Creación de BD Coordinador de Campo"/></a>

Importación de datos en formato XTF con la zona asignada por el Coordinador General.

<a class="" data-lightbox="Importación de datos Coordinador de Campo" href="_static/captura_de_datos_en_campo/7_Coor_campo_asignacion_3.gif" title="Importación de datos Coordinador de Campo" data-title="Importación de datos Coordinador de Campo"><img src="_static/captura_de_datos_en_campo/7_Coor_campo_asignacion_3.gif" class="align-center" width="800px" alt="Importación de datos Coordinador de Campo"/></a>

Cargue de datos de la zona asignada e imagen de referencia al mapa.

<a class="" data-lightbox="Cargue de datos e imagen base" href="_static/captura_de_datos_en_campo/8_Coor_campo_asignacion_45.gif" title="Cargue de datos e imagen base" data-title="Cargue de datos e imagen base"><img src="_static/captura_de_datos_en_campo/8_Coor_campo_asignacion_45.gif" class="align-center" width="800px" alt="Cargue de datos e imagen base"/></a>

Creación de Reconocedores de Campo.

<a class="" data-lightbox="Creación usuarios Coordinador de Campo" href="_static/captura_de_datos_en_campo/9_Coor_campo_asignacion_6.gif" title="Creación usuarios Coordinador de Campo" data-title="Creación usuarios Coordinador de Campo"><img src="_static/captura_de_datos_en_campo/9_Coor_campo_asignacion_6.gif" class="align-center" width="800px" alt="Creación usuarios Coordinador de Campo"/></a>

Asignación de predios a Reconocedores de Campo.

<a class="" data-lightbox="Asignar predios Coordinador de Campo" href="_static/captura_de_datos_en_campo/10_Coor_campo_asignacion_7.gif" title="Asignar predios Coordinador de Campo" data-title="Asignar predios Coordinador de Campo"><img src="_static/captura_de_datos_en_campo/10_Coor_campo_asignacion_7.gif" class="align-center" width="800px" alt="Asignar predios Coordinador de Campo"/></a>

Generación de proyectos listos para cargar a *QField*, para cada uno de los Reconocedores de Campo.

<a class="" data-lightbox="Exportar datos y proyectos QField" href="_static/captura_de_datos_en_campo/11_Coor_campo_asignacion_89.gif" title="Exportar datos y proyectos QField" data-title="Exportar datos y proyectos QField"><img src="_static/captura_de_datos_en_campo/11_Coor_campo_asignacion_89.gif" class="align-center" width="800px" alt="Exportar datos y proyectos QField"/></a>

## Recolección datos en Campo

El Reconocedor carga a su dispositivo móvil uno o varios proyectos que le ha entregado el Coordinador de Campo. En dicho proyecto se incluye la configuración, formularios, imagen de referencia y simbología necesarios para orientarse, identificar predios en terreno y realizar el levantamiento catastral de forma eficiente.

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>Antes de ir a campo, el Reconocedor debe instalar y configurar en su dispositivo la última versión de <i>QField</i>, para poder cargar y vizualizar correctamente los proyectos entregados por el Coordinador de Campo (ver manual de <a href="https://swisstierrascolombia.github.io/QField-LADM-COL-docs/" target="_blank">QField para campo</a>)</p>
</div>

Cabe aclarar que el uso del Asistente LADM-COL es totalmente opcional para el Reconocedor, quien realizará su trabajo enteramente con QField.

#### Reconocedor

Almacenamiento y cargue del proyecto *QField* en el dispositivo móvil.

<a class="" data-lightbox="Cargue del proyecto QField Reconocedor" href="_static/captura_de_datos_en_campo/12_reconocedor_campo_1.gif" title="Cargue del proyecto QField Reconocedor" data-title="Cargue del proyecto QField Reconocedor"><img src="_static/captura_de_datos_en_campo/12_reconocedor_campo_1.gif" class="align-center" width="800px" alt="Cargue del proyecto QField Reconocedor"/></a>

Digitalización de puntos en el dispositivo móvil.

<a class="" data-lightbox="Digitalización de puntos" href="_static/captura_de_datos_en_campo/13_reconocedor_campo_2.gif" title="Digitalización de puntos" data-title="Digitalización de puntos"><img src="_static/captura_de_datos_en_campo/13_reconocedor_campo_2.gif" class="align-center" width="800px" alt="Digitalización de puntos"/></a>

Digitalización de polígonos y edición de formularios.

<a class="" data-lightbox="Digitalización de polígonos" href="_static/captura_de_datos_en_campo/14_reconocedor_campo_3.gif" title="Digitalización de polígonos" data-title="Digitalización de polígonos"><img src="_static/captura_de_datos_en_campo/14_reconocedor_campo_3.gif" class="align-center" width="800px" alt="Digitalización de polígonos"/></a>

## Sincronizar datos de campo

Después de capturar los datos de campo se debe realizar el proceso de sincronización, que permite la consolidación de los datos obtenidos por cada uno de los Reconocedores en la base de datos del Coordinador de Campo. Luego de que los datos son consolidados y posiblemente editados por el Coordinador de Campo, este envía los mismos al Coordinador General, quien ejecuta un proceso de sincronización para consolidar los datos de todos sus Coordinadores de Campo. 

A continuación se muestran los pasos que se realizan en el Asistente LADM-COL para la ejecución de estas actividades.

#### Sincronizar datos de campo (Coordinador de Campo)

Selección de rol y selección de base de datos existente para sincronizar datos de campo.

<a class="" data-lightbox="Selección de BD Coordinador de Campo" href="_static/captura_de_datos_en_campo/15_Coor_campo_sincronizacion_1.gif" title="Selección de BD Coordinador de Campo" data-title="Selección de BD Coordinador de Campo"><img src="_static/captura_de_datos_en_campo/15_Coor_campo_sincronizacion_1.gif" class="align-center" width="800px" alt="Selección de BD Coordinador de Campo"/></a>

Sincronizar los datos provenientes de los Reconocedores (archivos GPKG).

<a class="" data-lightbox="Sincronizar Coordinador de Campo" href="_static/captura_de_datos_en_campo/16_Coor_campo_sincronizacion_2.gif" title="Sincronizar Coordinador de Campo" data-title="Sincronizar Coordinador de Campo"><img src="_static/captura_de_datos_en_campo/16_Coor_campo_sincronizacion_2.gif" class="align-center" width="800px" alt="Sincronizar Coordinador de Campo"/></a>

Verificar reglas de calidad, corregir y generar archivo XTF para entrega a Coordinador General.

<a class="" data-lightbox="Reglas de calidad y generación de XTF Coordinador de Campo" href="_static/captura_de_datos_en_campo/17_Coor_campo_sincronizacion_34.gif" title="Reglas de calidad y generación de XTF Coordinador de Campo" data-title="Reglas de calidad y generación de XTF Coordinador de Campo"><img src="_static/captura_de_datos_en_campo/17_Coor_campo_sincronizacion_34.gif" class="align-center" width="800px" alt="Reglas de calidad y generación de XTF Coordinador de Campo"/></a>

#### Sincronizar datos (Coordinador General)

Selección de rol y de BD maestra para sincronizar datos de Coordinadores de Campo (archivos XTF).

<a class="" data-lightbox="Recepción y sincronización datos de campo Coordinador General" href="_static/captura_de_datos_en_campo/18_Coor_general_sincronizacion_34.gif" title="Recepción y sincronización datos de campo Coordinador General" data-title="Recepción y sincronización datos de campo Coordinador General"><img src="_static/captura_de_datos_en_campo/18_Coor_general_sincronizacion_34.gif" class="align-center" width="800px" alt="Recepción y sincronización datos de campo Coordinador General"/></a>

Al finalizar esta actividad el Coordinador General obtiene un archivo XTF final del levantamiento catastral de la zona asignada aún en la estructura del modelo de Captura en Campo, la cual se llevara al modelo de aplicación Levantamiento Catastral con su respectivo proceso de control de calidad, para luego ser entregada al Gestor.

***
## ETL (Modelo Captura en Campo - Modelo de Aplicación Lev. Catastral) [Aún en desarrollo]

Una vez se tienen consolidados los datos de los diferentes coordinadores de campo, se utiliza esta ETL para llevar los datos al modelo de aplicación Levantamiento Catastral, con el fin de incorporar la información estructurada en oficina y poder ser entregada al Gestor como producto del Levantamiento Catastral realizado por el Operador.
