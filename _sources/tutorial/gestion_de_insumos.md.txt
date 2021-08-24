# Gestión de Insumos

Para ejecutar esta sección es necesario que cambies al rol de Proveedor de insumos, para esto debes seguir la ruta: LADM-COL -> Configuración -> Pestaña Avanzado -> Rol Proveedor de insumos.

<a class="" data-lightbox="Configuración rol de Proveedor de insumos" href="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos0.gif" title="Configuración rol de Proveedor de insumos" data-title="Configuración rol de Proveedor de insumos"><img src="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos0.gif" class="align-center" width="800px" alt="Configuración rol de Proveedor de insumos"/></a>

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>Si es la primera vez que utilizas el Asistente LADM-COL, será necesario configurar una nueva base de datos como se menciona en el siguiente <a href="https://swisstierrascolombia.github.io/Asistente-LADM-COL/administracion_de_datos.html#crear-estructura-ladm-col">enlace</a>, pero en este caso, seleccionando los submodelos de insumos catastrales y registrales.</p>
</div>


## Ejecutar ETL de insumos COBOL

Esta sección tiene por objetivo ejecutar la *ETL de COBOL* para transferir los datos en la estructura de COBOL a la estructura del submodelo de insumos de levantamiento catastral.

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>El acrónimo <b>ETL</b> corresponde a <i>"Extract, Transform and Load"</i> (Extraer, Transformar y Cargar). Es ampliamente usado para describir los procesos que se llevan a cabo para migrar datos.</p>
</div>


### Paso 1: Abrir ETL de insumos

Para iniciar con el proceso debes dirigirte a la siguiente ruta **LADM-COL -->  Gestión de Insumos --> Ejecutar ETL de Insumos**.

<a class="" data-lightbox="Paso 1: Ejecutar ETL de Insumos" href="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos1.gif" title="Paso 1: Ejecutar ETL de Insumos" data-title="Paso 1: Ejecutar ETL de Insumos"><img src="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos1.gif" class="align-center" width="800px" alt="Paso 1: Ejecutar ETL de Insumos"/></a>

### Paso 2: Seleccionar ETL para datos de COBOL

Se despliega una interfaz en la cual debes seccionar la opción *ETL para datos COBOL* y dar clic en el botón `Siguiente`.

<a class="" data-lightbox="Paso 2: Seleccionar ETL para datos de Cobol" href="../_static/tutorial/\gestion_de_insumos/cap13gestioninsumos2.gif" title="Paso 2: Seleccionar ETL para datos de Cobol" data-title="Paso 2: Seleccionar ETL para datos de Cobol"><img src="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos2.gif" class="align-center" width="800px" alt="Paso 2: Seleccionar ETL para datos de Cobol"/></a>

### Paso 3: Seleccionar archivos para ejecutar la ETL para datos COBOL

En la ventana que se despliega se habilitan las opciones para configurar los datos fuente (cargar los datos de COBOL). Debes cargar cada uno de los archivos de extensión **.lis** que se encuentra en los datos proporcionados al inicio del tutorial y el archivo de extensión **.gdb** en el último recuadro. Una vez que estén cargados los archivos, se habilita el botón `Ejecutar ETL`.

<a class="" data-lightbox="Paso 3: Seleccionar archivos para ejecutar la ETL para datos Cobol" href="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos3.gif" title="Paso 3: Seleccionar archivos para ejecutar la ETL para datos Cobol" data-title="Paso 3: Seleccionar archivos para ejecutar la ETL para datos Cobol"><img src="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos3.gif" class="align-center" width="800px" alt="Paso 3: Seleccionar archivos para ejecutar la ETL para datos Cobol"/></a>

### Paso 4: Definir la conexión a la base de datos de insumos

Antes de ejecutar la ETL, es importante que verifiques que la base de datos de destino sea la correcta. Para ello puedes leer el nombre de la base de datos de destino y en caso de que no corresponda, puedes definir la conexión dando clic al botón `Configurar conexión`.

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>Recuerda que la base de datos destino debe tener la estructura LADM-COL correspondiente a los submodelos de insumos catastrales y registrales.</p>
</div>

### Paso 5: Ejecutar ETL para datos de COBOL

Al dar clic en el botón `Ejecutar ETL` se despliega un cuadro de diálogo en el que se te advierte que si la base de datos que seleccionaste ya tiene datos, podrían generarse datos inválidos al importarle datos nuevos. Si tu base de datos aún no tiene datos, puedes continuar con la operación dando clic en el botón **Sí**. Una vez que la ETL finalice su ejecución, debes dar clic en el botón `Siguiente`.

<a class="" data-lightbox="Paso 4: Ejecutar ETL para datos de Cobol" href="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos4.gif" title="Paso 4: Ejecutar ETL para datos de Cobol" data-title="Paso 4: Ejecutar ETL para datos de Cobol"><img src="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos4.gif" class="align-center" width="800px" alt="Paso 4: Ejecutar ETL para datos de Cobol"/></a>

### Paso 6: Resultados de la ETL para datos Cobol

Finalmente, se despliega un cuadro de diálogo donde se muestra el resultado de la ejecución de la ETL, listando las tablas principales del submodelo de insumos y el número de registros que se cargaron en cada una de esas tablas. Haz clic en el botón `Finalizar` para terminar el proceso.

<a class="" data-lightbox="Paso 5: Resultados de la ETL para datos de Cobol" href="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos5.png" title="Paso 5: Resultados de la ETL para datos de Cobol" data-title="Paso 5: Resultados de la ETL para datos de Cobol"><img src="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos5.png" class="align-center" width="400px" alt="Paso 5: Resultados de la ETL para datos de Cobol"/></a>

## Identificación de novedades

Esta sección permite identificar los cambios entre la base de datos de los insumos (eso es, la base de datos suministrada por el gestor catastral) y la base de datos del levantamiento catastral (la cual corresponde a los datos adquiridos en campo). Estos cambios facilitan el reconocimiento de las novedades obtenidas en la captura de información.

### Paso 1: Configurar identificación de novedades

Para iniciar con el proceso debes dirigirte a la siguiente ruta **LADM-COL --> Identificación de novedades --> Configurar identificación de novedades**.

<a class="" data-lightbox="Paso 1: Abrir interfaz configurar identificación de novedades" href="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos8.gif" title="Paso 1: Abrir interfaz configurar identificación de novedades" data-title="Paso 1: Abrir interfaz configurar identificación de novedades"><img src="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos8.gif" class="align-center" width="800px" alt="Paso 1: Abrir interfaz configurar identificación de novedades"/></a>

### Paso 2: Configuración de conexiones

Considerando que todo el proceso a lo largo de este tutorial se ha desarrollado en una única base de datos, se debe seleccionar la misma base de datos para **Barrido predial** y para **Insumos**. Tan pronto hayas seleccionado la misma base de datos, haz clic en `Aceptar`, lo que genera un mensaje de confirmación que informa que el proceso fue ejecutado con éxito.

<a class="" data-lightbox="Paso 2: Configuracion de conexiones" href="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos9.gif" title="Paso 2: Configuracion de conexiones" data-title="Paso 2: Configuracion de conexiones"><img src="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos9.gif" class="align-center" width="800px" alt="Paso 2: Configuracion de conexiones"/></a>

### Paso 3: Abrir consulta masiva

Para la identificación de novedades es necesario hacer clic en el botón `Consulta masiva`, bien sea desde el mensaje de confirmación que se desplegó luego de realizar el paso anterior o desde el menú **LADM-COL --> Identificación de novedades --> Consulta masiva**.

<a class="" data-lightbox="Paso 3: Abrir consulta masiva" href="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos11.gif" title="Paso 3: Abrir consulta masiva" data-title="Paso 3: Abrir consulta masiva"><img src="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos11.gif" class="align-center" width="600px" alt="Paso 3: Abrir consulta masiva"/></a>

### Paso 4: Resultado consulta masiva

Se obtiene un resumen de novedades que corresponde a una comparación de los datos de Levantamiento Catastral contra los datos de Insumos. El resumen indica el número de novedades encontradas agrupadas por tipo de novedad.

Finalmente, en el panel de Identificación de Novedades, haz clic en el botón `Ver predios` de cualquiera de los tipos de novedad habilitados y selecciona un predio para ver las diferencias entre un predio en el submodelo de Insumos y el mismo predio en el modelo de aplicación Levantamiento Catastral.

<a class="" data-lightbox="Paso 4: Resultado consulta masiva" href="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos12.gif" title="Paso 4: Resultado consulta masiva" data-title="Paso 4: Resultado consulta masiva"><img src="../_static/tutorial/gestion_de_insumos/cap13gestioninsumos12.gif" class="align-center" width="800px" alt="Paso 4: Resultado consulta masiva"/></a>