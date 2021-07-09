# Reportes

El Asistente LADM-COL permite generar reportes de forma masiva y de forma automatizada a partir de los datos que fueron recolectados del levantamiento catastral. Para tener acceso a esta funcionalidad debes ir al menú LADM-COL y seleccionar la opción reportes, para la cual se desplegarán dos opciones de reportes:

+ [Anexo 17](#anexo-17): Es un reporte basado en la información y esquema del anexo #17 del documento “Conceptualización y especificaciones para la operación del Catastro Multipropósito” generado por el Instituto Geográfico Agustín Codazzi, IGAC.
+ [Plano ANT](#plano-ant): Plano definido por la Agencia Nacional de Tierras, ANT que se utiliza para mostrar la información producto de la definición de cabida y linderos de los predios objeto del levantamiento catastral.

<a class="" data-lightbox="Menu reportes" href="_static/reportes/menu_reports.png" title="Menu reportes" data-title="Menu reportes"><img src="_static/reportes/menu_reports.png" class="align-center" width="500px" alt="Menu reportes"/></a>

<div class="warning">
<p class="admonition-title">ADVERTENCIA</p>
<p>En la actualidad, esta funcionalidad no soporta terrenos con agujeros internos.</p>
</div>

## Anexo 17

Esta opción permite generar un reporte de contigüidad, en formato PDF, para cada uno de los terrenos seleccionados en el mapa.

El informe de colindancia corresponde al documento donde se identifican por predio (con relaciones formales o informales de tenencia) cada uno de los linderos que lo constituyen y su correspondiente relación física y jurídica con sus predios circundantes.

Para generar el informe del anexo 17, sigue estos pasos:

1. Selecciona el o los terrenos a los cuales se les generará el reporte.
2. Ir  a `LADM-COL --> Reportes` y dar clic en el botón `Anexo 17`.
3. Descargar dependencias (automático). Este paso se realiza una sola vez, puede tardar algunos minutos y necesita una conexión a internet activa.
4. Se desplegara una ventana emergente en la cual se debe indicar el directorio donde se desean almacenar los reportes generados y dar clic en Aceptar.
5. Al terminar la generación de reportes se obtiene un enlace a la ruta donde se encuentran los archivos PDF.
6. Ir al directorio que se seleccionó en el paso 4 para verificar el resultado, que luce como en la siguiente imagen:

<a class="" data-lightbox="Generar reporte anexo 17" href="_static/reportes/report_annex17.gif" title="Generar reporte anexo 17" data-title="Generar reporte anexo 17"><img src="_static/reportes/report_annex17.gif" class="align-center" width="800px" alt="Generar reporte anexo 17"/></a>



## Plano ANT

El plano ANT muestra la información producto de la definición de cabida y linderos de los predios a los que se les ha realizado un levantamiento predial. 

Para generar el informe del plano ANT, sigue estos pasos:

1. Selecciona el o los terrenos a los cuales se les generará el reporte.

2. Ir  a `LADM-COL --> Reportes` y dar clic en el botón `Plano ANT`.

3. Descargar dependencias (automático). Este paso se realiza una sola vez, puede tardar algunos minutos y necesita una conexión a internet activa.

4. Se despliega una ventana de dialogo en la cual se deben diligenciar los campos solicitados y luego dar clic en el botón Generar.

   - **Zona**: Permite seleccionar la zona donde estan ubicados los datos. De acuerdo el apartado 7.3 de la resolución 388 de 2020 del IGAC, el área para predios en el suelo urbano se expresa en metros cuadrados (m<sup>2</sup>) con aproximación al decímetro cuadrado, en el suelo rural se expresa en hectáreas (ha) y fracción en metros cuadrados (m<sup>2</sup>) sin aproximación.

   - **Elaboró**: Permite diligenciar el nombre completo y matrícula profesional de la persona que elaboró el reporte.

   - **Revisó**: Permite diligenciar el nombre completo y matrícula profesional de la persona que revisó el reporte.

   - **Mapa base**: Permite seleccionar un mapa WMS, el cual servirá como mapa base en la localización general del reporte.

   - **Observaciones**: Permite registrar una observación acerca del reporte generado.

   - **Carpeta para almacenar los reportes**: Corresponde al directorio en el cual se almacenarán los reportes generados.

     <a class="" data-lightbox="Reporte plano ANT" href="_static/reportes/ant_report_dialog.png" title="Reporte plano ANT" data-title="Reporte plano ANT"><img src="_static/reportes/ant_report_dialog.png" class="align-center" width="400px" alt="Reporte plano ANT"/></a>

5. Al terminar la generación de reportes se obtiene un enlace a la ruta donde se encuentran los archivos PDF.

6. Ir al directorio que se seleccionó en el paso 4 para verificar el resultado, que luce como en la siguiente imagen:

<a class="" data-lightbox="Reporte plano ANT" href="_static/reportes/report_ant.gif" title="Reporte plano ANT" data-title="Reporte plano ANT"><img src="_static/reportes/report_ant.gif" class="align-center" width="800px" alt="Reporte plano ANT"/></a>

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>Para poder generar el reporte Plano ANT la base de datos debe tener implementado el Modelo de aplicación de Levantamiento Catastral v1.0 y el Submodelo de Cartografía Catastral v1.0.</p>
</div>
