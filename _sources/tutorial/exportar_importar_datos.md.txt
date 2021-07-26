# Exportar e Importar Datos

En esta sección se describe el procedimiento que se debe seguir para exportar e importar la información que se ha generado en el modelo de levantamiento catastral a lo largo de este tutorial.

## Exportar datos

El objetivo de exportar datos es el de compartir o transferir los mismos con otra persona o suministrárselos a una entidad.

### Paso 1: Menú de Exportar Datos.

Para iniciar el proceso se debe seguir la ruta **Administración de Datos -> Exportar Datos**. Esta acción despliega un cuadro de diálogo dividido en tres (3) secciones:

- Fuente
- Destino
- Mostrar detalles

<a class="" data-lightbox="Paso 1: Menú de Exportar Datos" href="../_static/tutorial/exportar_importar_datos/cap12importexport1.gif" title="Paso 1: Menú de Exportar Datos" data-title="Paso 1: Menú de Exportar Datos"><img src="../_static/tutorial/exportar_importar_datos/cap12importexport1.gif" class="align-center" width="800px" alt="Paso 1: Menú de Exportar Datos"/></a>

### Paso 2: Selección de la Fuente.

En primera medida, se debe validar que la base de datos a la cual se hace referencia corresponde al archivo que se desea exportar al formato de intercambio **.xtf**. 

En caso de que ésta no sea correcta, puedes cambiar la conexión dando clic en `Configurar conexión`.

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>En la interfaz que se despliega al dar clic en <code class="docutils literal notranslate">Configurar conexión</code>, es posible deshabilitar las validaciones ingresando a la pestaña <b>Modelos</b> y quitando la selección de la casilla de verificación llamada <i>Validar datos cuando se importa o exporta un archivo XTF</i>. Deshabilitar las validaciones es útil cuando se quieren compartir datos que aún están en proceso de estructuración.</p>
</div>


<a class="" data-lightbox="Paso 2: Selección de la Fuente" href="../_static/tutorial/exportar_importar_datos/cap12importexport2.gif" title="Paso 2: Selección de la Fuente" data-title="Paso 2: Selección de la Fuente"><img src="../_static/tutorial/exportar_importar_datos/cap12importexport2.gif" class="align-center" width="800px" alt="Paso 2: Selección de la Fuente"/></a>

### Paso 3: Exportar XTF.

En la sección *Destino*, en el campo de *Archivo XTF* debes dar clic en el botón `...`, con esta acción procedes a definir la carpeta y el nombre del archivo *.xtf* a exportar, luego das clic en `Guardar` y finalmente en el botón `Exportar datos`. 

<a class="" data-lightbox="Paso 3: Exportar XTF" href="../_static/tutorial/exportar_importar_datos/cap12importexport3.gif" title="Paso 3: Exportar XTF" data-title="Paso 3: Exportar XTF"><img src="../_static/tutorial/exportar_importar_datos/cap12importexport3.gif" class="align-center" width="800px" alt="Paso 3: Exportar XTF"/></a>

### Paso 4: Verificación de la creación del XTF.

Una vez que termine el proceso de *Exportar Datos*, das clic en el botón `Cerrar` y verificas que el XTF se encuentre en la carpeta especificada.

## Importar datos

El objetivo de importar datos es el de llevar datos de un archivo de transferencia (*.xtf*) a una base de datos sobre la que se tenga permiso de acceso y creación de objetos.

Los datos *.xtf*  recibidos, pueden ser importados a cualquiera de las [bases de datos soportadas por el Asistente LADM-COL](../configuracion.html#conexion-a-base-de-datos), sin importar cuál fue el motor de base de datos en el cual estos fueron generados. Por ejemplo, es posible generar los datos en PostgreSQL/PostGIS, exportarlos, compartirlos a otra persona o entidad, y luego importarlos a una base de datos GeoPackage.

### Paso 1: Menú de Importar Datos.

Para iniciar el proceso se debe seguir la ruta **Administración de Datos -> Importar Datos**. Esta acción despliega un cuadro de diálogo dividido en tres (3) secciones:

- Fuente
- Destino
- Mostrar detalles

<a class="" data-lightbox="Paso 1: Menú de Importar Datos" href="../_static/tutorial/exportar_importar_datos/cap12importexport5.gif" title="Paso 1: Menú de Importar Datos" data-title="Paso 1: Menú de Importar Datos"><img src="../_static/tutorial/exportar_importar_datos/cap12importexport5.gif" class="align-center" width="800px" alt="Paso 1: Menú de Importar Datos"/></a>

### Paso 2: Selección de la Fuente.

En primera medida debes validar que el *Archivo XTF* que se va a importar sea el de tu interés. En caso de que desees modificarlo basta con cambiar la ruta del archivo *.xtf* dando clic en `...`.

<a class="" data-lightbox="Paso 2: Selección de la Fuente" href="../_static/tutorial/exportar_importar_datos/cap12importexport6.gif" title="Paso 2: Selección de la Fuente" data-title="Paso 2: Selección de la Fuente"><img src="../_static/tutorial/exportar_importar_datos/cap12importexport6.gif" class="align-center" width="800px" alt="Paso 2: Selección de la Fuente"/></a>

### Paso 3: Importar XTF.

En la sección de *Destino* debes verificar que la base de datos sobre la cual se va a importar la información del archivo *.xtf* (seleccionado previamente) sea correcta. En caso contrario, debes modificar la conexión dando clic en el botón `Configurar conexión` y seleccionar la base de datos a la cual se desea importar la información. Una vez que termines de configurar la conexión debes dar clic en el botón `Importar datos`.

<a class="" data-lightbox="Paso 3: Importar XTF" href="../_static/tutorial/exportar_importar_datos/cap12importexport7.gif" title="Paso 3: Importar XTF" data-title="Paso 3: Importar XTF"><img src="../_static/tutorial/exportar_importar_datos/cap12importexport7.gif" class="align-center" width="800px" alt="Paso 3: Importar XTF"/></a>

Al finalizar la importación aparecerá un aviso de confirmación en la ventana de *Importar Datos*, luego de su validación podrás dar clic en el botón `Cerrar`.