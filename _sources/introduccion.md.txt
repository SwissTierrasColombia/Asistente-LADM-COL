# Introducción

+ [Generalidades](#generalidades)
  + [Soporte de funcionalidades por motor de base de datos](#soporte-de-funcionalidades-por-motor-de-base-de-datos)
  + [Galería](#galeria)
  + [Funcionalidades](#funcionalidades)
  + [Suscríbete a los lanzamientos del Asistente LADM-COL](#suscribete-a-los-lanzamientos-del-asistente-ladm-col)
+ [Instalación](#instalacion)
  + [Requerimientos mínimos](#requerimientos-minimos)
  + [Proceso de instalación](#proceso-de-instalacion)
  + [Habilitar proyección "Origen Nacional"](#habilitar-proyeccion-origen-nacional)
  + [Dialogo de bienvenida](#dialogo-de-bienvenida)



## Generalidades

El Asistente LADM-COL es un complemento para <a href="http://qgis.org" target="_blank">QGIS</a> que permite crear y mantener datos conformes con <a href="https://github.com/SwissTierrasColombia/LADM_COL" target="_blank">LADM-COL</a>, así  como importar, visualizar, capturar, consultar, transformar (mediante  ETLs), validar y generar archivos de intercambio de <a href="https://www.interlis.ch/en" target="_blank">INTERLIS</a> (.XTF). Se integra al Sistema de Transición para realizar tareas que requieren análisis y validación de datos espaciales.

Licencia: <a href="https://github.com/SwissTierrasColombia/Asistente-LADM-COL/blob/master/LICENSE" target="_blank">GNU General Public License v3.0</a>

Un proyecto de: <a href="https://swisstierrascolombia.com" target="_blank">SwissTierras Colombia</a> (<a href="http://bsf-swissphoto.com" target="_blank">BSF-Swissphoto AG</a> - <a href="http://www.incige.com" target="_blank">INCIGE S.A.S</a>)



### Soporte de funcionalidades por motor de base de datos

La versión actual (<a href="https://github.com/SwissTierrasColombia/Asistente-LADM-COL/releases/tag/3.1.10" target="_blank">3.1.10</a>) del Asistente LADM-COL depende del plugin <a href="https://github.com/SwissTierrasColombia/QgisModelBaker/releases/download/v6.1.1.5/QgisModelBaker_6115.zip" target="_blank">QGIS Model Baker v6.1.1.5</a> y soporta los motores de Base de Datos PostgreSQL/PostGIS, GeoPackage y SQL Server.

Este es el soporte funcional para cada motor:

| Módulos                           | PostgreSQL/PostGIS |        GeoPackage        |        MS SQL Server        |
| --------------------------------- | :----------------: | :----------------------: | :-------------------------: |
| Administración de datos           |         Si         |            Si            |            Si               |
| Captura y estructuración de datos |         Si         |            Si            |            Parcial          |
| Cargar capas                      |         Si         |            Si            |            Si               |
| Gestión de insumos                |         Si         |            Si            |            No               |
| Validaciones de calidad           |         Si         |            Si            |            Si               |
| Consultas                         |         Si         |            Si            |            Si               |
| Reportes                          |         Si         |            No            |            No               |
| Identificación de novedades       |         Si         |            Si            |            Parcial          |
| Sistema de Transición             |         Si         |            Si            |            Si               |



### Galería

+ Reglas de Calidad

  <a class="" data-lightbox="Reglas de Calidad" href="https://s3.amazonaws.com/media-p.slid.es/uploads/308098/images/6343636/quality_rules_25-min.gif" title="Reglas de Calidad" data-title="Reglas de Calidad"><img src="https://s3.amazonaws.com/media-p.slid.es/uploads/308098/images/6343636/quality_rules_25-min.gif" class="align-center" width="800px" alt="Reglas de Calidad"/></a>

+ Consultas

  <a class="" data-lightbox="Consultas" href="https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6290636/query_25.gif" title="Consultas" data-title="Consultas"><img src="https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6290636/query_25.gif" class="align-center" width="800px" alt="Consultas"/></a>

+ Reportes

  <a class="" data-lightbox="Reportes" href="https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6290657/report_25.gif" title="Reportes" data-title="Reportes"><img src="https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6290657/report_25.gif" class="align-center" width="800px" alt="Reportes"/></a>

+ Identificación de Novedades

  <a class="" data-lightbox="Identificación de Novedades" href="https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6293473/novedades_short_40_slides.gif" title="Identificación de Novedades" data-title="Identificación de Novedades"><img src="https://s3.amazonaws.com/media-p.slid.es/uploads/1024195/images/6293473/novedades_short_40_slides.gif" class="align-center" width="800px" alt="Identificación de Novedades"/></a>

+ Integración con el Sistema de Transición

  <a class="" data-lightbox="Sistema de Transición" href="https://user-images.githubusercontent.com/27906888/83693002-b6f17900-a5ba-11ea-8d62-0ed25b2a7cfe.gif" title="Sistema de Transición" data-title="Sistema de Transición"><img src="https://user-images.githubusercontent.com/27906888/83693002-b6f17900-a5ba-11ea-8d62-0ed25b2a7cfe.gif" class="align-center" width="800px" alt="Sistema de Transición"/></a>



### Funcionalidades

#### Administración de datos

  - Crear estructura de base de datos conforme al modelo LADM-COL v3.0.
  - Importar datos desde archivo de transferencia (.XTF).
  - Exportar datos a archivo de transferencia (.XTF).
  - Importar/exportar datos desde y hacia archivos de transferencia (.XTF) desactivando la validación de los mismos. 
  - Soporte de tres motores para manejar datos de LADM-COL:
    - PostgreSQL/PostGIS: Soporte total.
    - GeoPackage: Soporte total, exceptuando el módulo de reportes.
    - SQL Server: Soporte parcial. Gestión de insumos y reportes no están soportados.

#### Captura y estructuración de datos

+ Capturar datos para el modelo de aplicación de Levantamiento Catastral v1.0 (<a href="https://github.com/SwissTierrasColombia/LADM_COL/releases/download/1.0/Modelo_Aplicacion_LADMCOL_Levantamiento_Catastral_V1_0.zip" target="_blank">descargar</a>).
 - Agregar puntos a las capas `Punto Lindero`, `Punto Levantamiento` y `Punto Control`:
   - Desde archivo CSV con la estructura requerida.
     - Validar para evitar insertar puntos superpuestos.
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
 - Agregar `Linderos`:
   - Digitalizando sobre el mapa.
     - Ayudas para la digitalización:
       - Configuración automática de snapping y de valores predeterminados para campos.
       - Construir linderos a partir de líneas seleccionadas (partiéndolas automáticamente por cambio de colindancia).
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Terrenos`:
   - A partir de linderos seleccionados.
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
 - Llenar automáticamente tablas de topología:
   - `PuntosCCL` (relaciona `Punto Lindero` y `Lindero`)
   - `MasCCL`    (relaciona `Lindero` y `Terreno`)
   - `Menos`     (relaciona `Terreno` y sus anillos/huecos internos)
 - Crear `Construcciones` y `Unidades de Construcción`:
   - Digitalizando sobre el mapa.
     - Ayudas para la digitalización:
       - Configuración automática de snapping y de valores predeterminados para campos.
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Servidumbres de Paso`:
   - Digitalizando sobre el mapa el polígono de la servidumbre o el eje de la misma con un ancho.
     - Ayudas para la digitalización:
       - Configuración automática de snapping y de valores predeterminados para campos.
   - Desde otra capa con cualquier estructura, definiendo un mapeo de campos.
   - Crear relaciones de restricciones y beneficiados.
 - Asociar direcciones a los `Terrenos`, `Construcciones` y `Unidades de Construcción`.
 - Crear `Predios`:
   - Usando formularios preconfigurados.
     - Y relacionando el nuevo `Predio` con un `Terreno` y/o una o varias `Construcciones` previamente seleccionadas.
   - Desde otra tabla con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Interesados Naturales` e `Interesados Jurídicos`:
   - Usando formularios preconfigurados.
   - Desde otra tabla con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Agrupaciones de Interesados`:
   - Usando un formulario preconfigurado.
 - Crear `Fuente Espacial` y `Fuente Administrativa`:
   - Usando formularios preconfigurados.
     - Y relacionando la nueva `Fuente Espacial` a `Terrenos`, `Linderos` o `Puntos` previamente seleccionados.
   - Desde otra tabla con cualquier estructura, definiendo un mapeo de campos.
 - Crear `Archivos Fuente`:
   - Asociar fuentes a archivos fuente.
   - Almacenar archivos fuente en servidor en el momento de guardar cambios o
     posteriormente, de forma masiva.
 - Crear `Derechos`, `Restricciones` y `Responsabilidades` (`RRR`):
   - Usando formularios preconfigurados (relacionando el nuevo objeto a `Fuentes Administrativas` previamente seleccionadas).
   - Desde otra tabla con cualquier estructura, definiendo un mapeo de campos.
  - Configurar valores automáticos para campos `t_ili_tid`, `espacio_de_nombres` y `local_id`.
  - Usar estilos preconfigurados en archivos QML para asignarlos a las capas cargadas.

#### Cargar capas

+ Seleccionar en un diálogo las capas a cargar de cualquier modelo de la base de datos o esquema:
- Usar el plugin 'QGIS Model Baker' para cargar capas con formularios, relaciones y dominios configurados.
- Cargar conjuntos de capas preconfigurados.

#### Gestión de Insumos

- ETL para generar insumos catastrales a partir de datos del IGAC (fuente SNC).
- ETL para generar insumos catastrales a partir de datos del IGAC (fuente Cobol).
 - Generar reporte de Omisiones y Comisiones.

#### Validaciones de calidad

 - Realizar revisiones de calidad (topología) configurando opcionalmente una tolerancia:
   - Revisar superposiciones en `Punto Lindero`.
   - Revisar superposiciones en `Punto de Control`.
   - Revisar superposiciones en `Lindero`.
   - Revisar superposiciones en `Terreno`.
   - Revisar superposiciones en `Construcción`.
   - Revisar superposiciones en `Servidumbre de Paso`.
   - Revisar `Punto Lindero` sin nodo de `Lindero` asociado o con `Lindero` asociado pero relacionado de forma incorrecta en tabla `PuntoCCL`.
   - Revisar nodos de `Lindero` sin `Punto Lindero` asociado o con `Punto Lindero` asociado pero relacionado de forma incorrecta en tabla `PuntoCCL`.
   - Revisar nodos de `Lindero` no conectados.
   - Revisar que los `Linderos` siempre terminen en cambio de colindancia.
   - Revisar superposiciones entre `Servidumbre de paso` y `Construcción`.
   - Revisar que los `Terrenos` no dejen agujeros entre ellos.
   - Revisar que los límites de `Terrenos` estén cubiertos por `Linderos` y que sus relaciones estén correctamente registradas en las tablas de topología (`MasCCL` y `Menos`).
   - Revisar que los `Linderos` estén cubiertos por límites de `Terrenos` y que sus relaciones estén correctamente registradas en las tablas de topología (`MasCCL` y `Menos`).
   - Revisar geometrías multiparte en `Servidumbre de paso`.
   - Revisar que las `Construcciones` estén dentro de su `Terreno` correspondiente.
   - Revisar que las `Unidades de Construcción` estén dentro de su `Terreno` correspondiente.
   - Revisar que las `Unidades de Construcción` estén dentro de su `Construcción` correspondiente.
 - Realizar revisiones de calidad (consistencia lógica):
   - Los predios deben tener derecho asociado y pueden tener máximo un derecho de tipo Dominio asociado.
   - No deben haber registros duplicados.
   - Las fracciones de las agrupaciones de interesados deben sumar uno (1).
   - Revisar que el campo departamento de la tabla predio tiene dos caracteres numéricos.
   - Revisar que el campo municipio de la tabla predio tiene tres caracteres numéricos.
   - Revisar que el campo zona de la tabla predio tiene dos caracteres numéricos.
   - Revisar que el número_predial tiene 30 caracteres numéricos.
   - Revisar que el número_predial_anterior tiene 20 caracteres numéricos.
   - Revisar que los atributos son apropiados para interesados naturales.
   - Revisar que los atributos son apropiados para interesados jurídicos.
   - Revisar que el tipo de Predio corresponde a la posición 22 del número_predial.
   - Revisar que las Unidades Espaciales asociadas a Predios correspondan al tipo de predio.
 - Generar reporte de revisiones de calidad.

#### Consultas

 - Consultar datos LADM-COL por componentes:
   - Información Básica.
   - Información Jurídica.
   - Información de Ficha Predial.
   - Información Física.
   - Información Económica.

#### Reportes

 - Generar Informes de Colindancia con base en `Terrenos` seleccionados (Anexo 17).
 - Generar reporte 'Plano ANT' con base en `Terrenos` seleccionados.

#### Identificación de Novedades

 - Identificar novedades:
   - Comparar base de datos del barrido contra datos de insumos y evidenciar diferencias masivas y por predio tanto en el componente alfanumérico como geográfico.

#### Sistema de Transición

 - Integración con el Sistema de Transición:
   - Autenticación.
   - Gestión de tareas: consulta, iniciación, cancelación y finalización.
   - Tareas de generación de insumos catastrales.
     - ETL para generar insumos catastrales a partir de datos del IGAC (fuente SNC).
     - ETL para generar insumos catastrales a partir de datos del IGAC (fuente Cobol).
 - Soporte de roles y generación de interfaz de usuario para cada rol.



### Suscríbete a los lanzamientos del Asistente LADM-COL

1. Ingresa al siguiente <a href="https://gitpunch.com" target="_blank">enlace</a>.
2. Busca "Asistente LADM-COL".
3. Selecciona "Ingresar correo electronico" (*enter email*).
4. Inicia sesión o regístrate con tu correo electrónico y contraseña.
5. Listo, estás suscrito a los lanzamientos del Asistente LADM-COL (las notificaciones llegarán a tu correo electrónico).

  <a class="" data-lightbox="Suscribirse al lanzamiento de versiones Asistente LADM-COL" href="_static/instalacion/suscribe_notification_new_release.gif" title="Suscribirse al lanzamiento de versiones Asistente LADM-COL" data-title="Suscribirse al lanzamiento de versiones Asistente LADM-COL"><img src="_static/instalacion/suscribe_notification_new_release.gif" class="align-center" width="800px" alt="Suscribirse al lanzamiento de versiones Asistente LADM-COL"/></a>





## Instalación

### Requerimientos mínimos

Para usar el Asistente LADM-COL se requiere:

 - Sistema Operativo:
   - Windows 10
   - GNU/Linux
   - macOS
 - Software base:
   - QGIS v3.10.0-A Coruña o superior
   - Java v1.8
   - PostgreSQL 9.5 o superior (funciona PostgreSQL 10, 11 ó 12).
   - PostGIS 2.4 o superior.
 - Complementos de QGIS (al instalar el Asistente LADM-COL usando el Administrador de Complementos de QGIS, las dependencias se instalarán automáticamente):
   - QGIS Model Baker v6.1.1.5.
   - MapSwipe Tool v1.2


### Proceso de instalación

- Es necesario tener el Software QGIS versión 3 instalado.

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>Con la versión actual del Asistente LADM-COL, se recomienda usar la versión v3.14.16 de QGIS. Para obtenerla diríjete a <a href="https://qgis.org/downloads/" target="_blank">la página de descargas de QGIS</a></p>
</div>

- El proceso puede ser observado gráficamete en el siguiente GIF:

  <a class="" data-lightbox="Proceso de instalación del plugin" href="_static/instalacion/instalation.gif" title="Proceso de instalación del plugin" data-title="Proceso de instalación del plugin"><img src="_static/instalacion/instalation.gif" class="align-center" width="800px" alt="Proceso de instalación del plugin"/></a>

- En caso de no contar con la versión correcta del plugin QgisModelBaker, el Asistente LADM-COL mostrará un mensaje similar a este:

  <a class="" data-lightbox="Error de dependencia QgisModelBaker" href="_static/instalacion/error_asistente_qgis_model_baker.png" title="Error de dependencia QgisModelBaker" data-title="Error de dependencia QgisModelBaker"><img src="_static/instalacion/error_asistente_qgis_model_baker.png" class="align-center" width="800px" alt="Error de dependencia QgisModelBaker"/></a>
  
- Si tienes un error con el QgisModelBaker requerido, puedes instalar el plugin QgisModelBaker como en el siguiente GIF:

<a class="" data-lightbox="Instalación de QgisModelBaker" href="_static/instalacion/instalation_qgis_model_baker.gif" title="Instalación de QgisModelBaker" data-title="Instalación de QgisModelBaker"><img src="_static/instalacion/instalation_qgis_model_baker.gif" class="align-center" width="800px" alt="Instalación de QgisModelBaker"/></a>


### Habilitar proyección "Origen Nacional"

<a class="" data-lightbox="La proyección Origen Nacional es necesaria" href="_static/instalacion/ctm12_obligatorio.jpg" title="La proyección Origen Nacional es necesaria" data-title="La proyección Origen Nacional es necesaria"><img src="_static/instalacion/ctm12_obligatorio.jpg" class="align-center" alt="La proyección Origen Nacional es necesaria"/></a>

Para poder usar la proyección "Origen Nacional", se debe permitir que el Asistente LADM-COL configure dicha proyección, puesto que esta aún no se encuentra disponible en la base de datos oficial de Sistemas de Referencia de QGIS.

Para ello, basta con otorgar estos dos **permisos de escritura** al usuario con el cual usas QGIS:

  + Al archivo `srs.db`, que corresponde a la base de datos de sistemas de referencia. Ubicado generalmente en la ruta `C:\Program Files\QGIS 3.10\apps\qgis-ltr\resources\srs.db` (si das clic al enlace que te aparece en el diálogo de Advertencia, llegas directamente a la carpeta).
  + A la **carpeta contenedora** `resources`. Ubicada generalmente en la ruta `C:\Program Files\QGIS 3.10\apps\qgis-ltr\resources\` (si das clic al enlace que te aparece en el diálogo de Advertencia, llegas directamente a la carpeta).


#### ¿Cómo dar permiso de escritura a srs.db?

1. Ir a la carpeta `C:\Program Files\QGIS 3.10\apps\qgis-ltr\resources\`
2. Clic derecho sobre el archivo **srs.db** y elegir `Propiedades`.
3. En la ventana `Propiedades de srs.db`, ir a la pestaña `Seguridad` y elegir el usuario apropiado.
    <a class="" data-lightbox="Archivo srs.db, selección de usuario" href="_static/instalacion/file_3.png" title="Archivo srs.db, selección de usuario" data-title="Archivo srs.db, selección de usuario"><img src="_static/instalacion/file_3.png" class="align-center" alt="Archivo srs.db, selección de usuario"/></a>

4. Dar click en el botón `Editar`.
5. En la ventana `Permisos de srs.db`, elegir el usuario apropiado y seleccionar `Escritura` (columna `Permitir`).
    <a class="" data-lightbox="Archivo srs.db, permiso de escritura" href="_static/instalacion/file_5.png" title="Archivo srs.db, permiso de escritura" data-title="Archivo srs.db, permiso de escritura"><img src="_static/instalacion/file_5.png" class="align-center" alt="Archivo srs.db, permiso de escritura"/></a>

6. Dar clic en `Aceptar` en las dos ventanas abiertas.


#### ¿Cómo dar permiso de escritura a la carpeta resources?

1. Ir a la carpeta `C:\Program Files\QGIS 3.10\apps\qgis-ltr\`
2. Clic derecho sobre la carpeta **resources** y elegir `Propiedades`.
3. En la ventana `Propiedades de resources`, ir a la pestaña `Seguridad` y elegir el usuario apropiado.
    <a class="" data-lightbox="Carpeta resources, selección de usuario" href="_static/instalacion/folder_3.png" title="Carpeta resources, selección de usuario" data-title="Carpeta resources, selección de usuario"><img src="_static/instalacion/folder_3.png" class="align-center" alt="Carpeta resources, selección de usuario"/></a>

4. Dar click en el botón `Editar`.
5. En la ventana `Permisos de resources`, elegir el usuario apropiado y seleccionar `Escritura` (columna `Permitir`).
    <a class="" data-lightbox="Carpeta resources, permiso de escritura" href="_static/instalacion/folder_5.png" title="Carpeta resources, permiso de escritura" data-title="Carpeta resources, permiso de escritura"><img src="_static/instalacion/folder_5.png" class="align-center" alt="Carpeta resources, permiso de escritura"/></a>

6. Dar clic en `Aceptar` en las dos ventanas abiertas.

Luego de realizar esta configuración, ¡ya puedes utilizar el Asistente LADM-COL y la proyección Origen Nacional!

El siguiente GIF ilustra el proceso completo:

<a class="" data-lightbox="Habilitar proyección Origen Nacional" href="_static/instalacion/permisos_srs.gif" title="Habilitar proyección Origen Nacional" data-title="Habilitar proyección Origen Nacional"><img src="_static/instalacion/permisos_srs.gif" class="align-center" width="800px" alt="Habilitar proyección Origen Nacional"/></a>


### Diálogo de bienvenida

Al terminar la instalación del Asistente LADM-COL, obtendrás una diálogo como este:

<a class="" data-lightbox="Diálogo de bienvenida" href="_static/instalacion/dialogo_bienvenida.png" title="Diálogo de bienvenida" data-title="Diálogo de bienvenida"><img src="_static/instalacion/dialogo_bienvenida.png" class="align-center" alt="Diálogo de bienvenida"/></a>


En este diálogo puedes elegir rol (o perfil) con el cuál utilizarás el Asistente LADM-COL.

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>El rol elegido definirá el conjunto de módulos, barra de herramientas,  modelos e incluso, reglas de calidad, que tendrás a disposición desde la interfaz del Asistente LADM-COL.</p>
</div>

Por ejemplo, el rol `Básico` no tiene acceso a generar reportes, pero los roles `Gestor` y `Avanzado` si; el rol `Proveedor de insumos` tiene acceso al módulo de Gestión de insumos, pero el rol `Operador` no; el rol `Proveedor de insumos` solamente tiene acceso a los submodelos de Insumos, pero no tiene acceso al Modelo de Aplicación de Levantamiento Catastral, que si está disponible para otros roles.



Si bien el diálogo de bienvenida te permite elegir el rol que estará activo cuando empieces a usar el Asistente LADM-COL, siempre podrás configurar el rol activo desde el diálogo de [configuración](configuracion.html#avanzado).
