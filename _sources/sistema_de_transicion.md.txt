# Sistema de transición

El <a href="https://swisstierrascolombia.github.io/st-docs/index.html" target="_blank">Sistema de Transición</a>  es una herramienta en ambiente Web que permite apoyar la gestión de información necesaria para realizar las tareas del barrido predial en campo por parte de las entidades y actores involucrados en el proceso de Levantamiento Catastral en Colombia (Gestores y Operadores Catastrales). 

Una vez el Sistema de Transición recibe la solicitud de generación y entrega del insumo “Datos catastrales en modelo de insumos”, crea una tarea con sus respectivas credenciales para que un usuario con perfil técnico, asociado al área de trabajo Catastral del Proveedor IGAC, pueda autenticarse desde el **Asistente LADM-COL** e inicie la ejecución de la tarea.

<div class="note">
<p class="admonition-title">IMPORTANTE</p>
<p>Para poder utilizar esta funcionalidad desde el Asistente LADM-COL, se debe contar con las credenciales necesarias (usuario y contraseña), pues se requiere autenticación con el Sistema de Transición.</p>
</div>

## Autenticación

<a class="" data-lightbox="Autenticación en el Sistema de transición" href="_static/sistema_de_transicion/Autenticacion.gif" title="Autenticación en el Sistema de transición" data-title="Autenticación en el Sistema de transición"><img src="_static/sistema_de_transicion/Autenticacion.gif" class="align-center" width="800px" alt="Autenticación en el Sistema de transición"/></a>

Se tienen dos opciones: 

* Opción uno: En el menú desplegable del Asistente LADM-COL, hay un submenú llamado "Sistema de Transición". Se debe desplegar este submenú y dar clic en la opción "Autenticarse", la cual abrirá una ventana emergente. Al llenar el formulario con un usuario y contraseña, el Sistema de Transición valida los privilegios del usuario y permite el acceso o lo denega. En caso de ser aceptado, el Asistente LADM-COL carga un panel en la parte derecha de la interfaz donde se muestran las tareas asignadas al usuario autenticado.

* Opción dos: Dar clic en la barra de herramientas (menú "Sistema de Transición") y seguir las instrucciones descritas en el párrafo anterior.

## Ver tareas
<a class="" data-lightbox="Ver tareas disponibles" href="_static/sistema_de_transicion/Ver_tareas.gif" title="Ver tareas disponibles" data-title="Ver tareas disponibles"><img src="_static/sistema_de_transicion/Ver_tareas.gif" class="align-center" width="800px" alt="Ver tareas disponibles"/></a>

Después de haber realizado la autenticación en el Sistema de Transición, en el panel derecho de la interfaz de QGIS dar clic en “Ver tareas”. Si el usuario tiene tareas asignadas, estas aparecerán listadas. 

Al dar clic a una de las tareas llamadas “Generar insumo catastral” del municipio asignado y al dar clic en “Iniciar tarea" aparecerán los pasos de la tarea.

<a class="" data-lightbox="Panel de pasos de tarea iniciada" href="_static/sistema_de_transicion/Ver_pasos_tarea.png" title="Panel de pasos de tarea iniciada" data-title="Panel de pasos de tarea iniciada"><img src="_static/sistema_de_transicion/Ver_pasos_tarea.png" class="align-center" width="400px" alt="Panel de pasos de tarea iniciada"/></a>

<div class="seealso">
<p class="admonition-title">TIP</p>
    <p>Los pasos se ejecutan dando doble clic sobre cada paso. Una vez ejecutado un paso, cambiará su color a verde y su casilla de chequeo aparecerá marcada. Es posible marcar un paso como realizado sin haberlo ejecutado, para ello debe darse clic directamente en el <i>checkbox</i>. El boton "Cerrar Tarea" solo se activa para dar clic si todos pasos <b>obligatorios</b> estan chequeados.</p>
</div>


### Paso 1: Crear estructura submodelo de insumos

En la lista de pasos del panel derecho dar doble clic en el _paso 1_ "Crear estructura LADM-COL" y en la caja de dialogo que aparece, seleccionar la base de datos y el esquema en donde se importaran los datos. Luego, dar clic en el botón “Crear estructura”.

<a class="" data-lightbox="Paso 1: Crear estructura submodelo de insumos" href="_static/sistema_de_transicion/Crear_estructura_paso1.gif" title="Paso 1: Crear estructura submodelo de insumos" data-title="Paso 1: Crear estructura submodelo de insumos"><img src="_static/sistema_de_transicion/Crear_estructura_paso1.gif" class="align-center" width="800px" alt="Paso 1: Crear estructura submodelo de insumos"/></a>

### Paso 2: Ejecutar ETL de insumos

En la lista de pasos dar doble clic en el _paso 2_ “Ejecutar ETL de insumos” y en la ventana que aparece, seleccionar el sistema de proveniencia de los datos (COBOL o SNC). Posteriormente, cargar los archivos correspondientes en cada campo de acuerdo con su tipo (ver GIF). Los archivos a elegir dependen del sistema de origen elegido. Dar clic en el botón “Importar” y esperar a que se ejecute la ETL con éxito y se carguen las capas resultantes al panel de capas de QGIS.

<a class="" data-lightbox="Paso 2: Ejecutar ETL de insumos" href="_static/sistema_de_transicion/Correr_ETL_insumos_paso2.gif" title="Paso 2: Ejecutar ETL de insumos" data-title="Paso 2: Ejecutar ETL de insumos"><img src="_static/sistema_de_transicion/Correr_ETL_insumos_paso2.gif" class="align-center" width="800px" alt="Paso 2: Ejecutar ETL de insumos"/></a>

### Paso 3: Generar archivo XTF

En la lista de pasos dar doble clic en el _paso 3_ “Generar XTF” para abrir una ventana en donde se debe seleccionar la ubicación de la carpeta donde se desea almacenar el archivo XTF. Luego se da clic en el botón “Exportar datos” y una vez terminado el proceso, dar clic en el botón “Cerrar”.

<a class="" data-lightbox="Paso 3: Generar archivo XTF" href="_static/sistema_de_transicion/Generar_XTF_paso3.gif" title="Paso 3: Generar archivo XTF" data-title="Paso 3: Generar archivo XTF"><img src="_static/sistema_de_transicion/Generar_XTF_paso3.gif" class="align-center" width="800px" alt="Paso 3: Generar archivo XTF"/></a>

### Pasos 4 y 5: Generar informe omisiones y comisiones _(paso opcional)_

Dependiendo el sistema que se haya elegido en el *paso 2*, en la lista de pasos dar doble clic sobre el _paso 4_ “Generar reporte (COBOL)” o sobre el *paso 5* "Generar reporte (SNC)" y en la ventana que aparece, escoger la ubicación de la carpeta dentro del equipo donde se deseen almacenar los archivos del reporte de omisiones y comisiones. Dar clic en el botón "Generar informe" para iniciar la ejecución del proceso.

<a class="" data-lightbox="Paso 4: Generar informe omisiones y comisiones" href="_static/sistema_de_transicion/Generar_infoOC_paso4.gif" title="Paso 4: Generar informe omisiones y comisiones" data-title="Paso 4: Generar informe omisiones y comisiones"><img src="_static/sistema_de_transicion/Generar_infoOC_paso4.gif" class="align-center" width="800px" alt="Paso 4: Generar informe omisiones y comisiones"/></a>

<div class="seealso">
<p class="admonition-title">TIP</p>
<p>El reporte de Omisiones y Comisiones es útil para gestores y operadores catastrales, pues a través de él pueden conocer el estado de los datos entregados en el submodelo de insumos (archivo XTF).</p>
</div>


### Pasos 6 y 7: Subir archivo XTF (y reporte) y terminar tarea

En la lista de pasos dar doble clic en el _paso 6_ “Subir XTF” para abrir una ventana en donde se elige la carpeta en donde se almacenaron tanto el archivo XTF como el reporte de Omisiones y Comisiones (este último es opcional). Se debe agregar una observación en el campo “Comentario” que se enviará al Sistema de Transición y al dar clic en el botón “OK” se inicia el proceso de envío. Al terminar, dar clic en el botón “Cerrar”.

Finalmente, dar clic en el botón "Finalizar tarea" para terminar. El Sistema de Transición toma unos minutos en validar los archivos enviados y en aceptarlos. Mientras ello sucede, no será posible finalizar la tarea. Si se requiere, es posible salir del Sistema de Transición para realizar otros procesos y, una vez que se ingrese de nuevo, el estado de la tarea se conservará en el Asistente LADM-COL.

<a class="" data-lightbox="Paso 5: Subir archivo XTF" href="_static/sistema_de_transicion/Subir_archivo.gif" title="Paso 5: Subir archivo XTF" data-title="Paso 5: Subir archivo XTF"><img src="_static/sistema_de_transicion/Subir_archivo.gif" class="align-center" width="800px" alt="Paso 5: Subir archivo XTF"/></a>

## Cancelar tarea

En el panel lateral donde se listan los pasos, se dispone de la opción "Cancelar tarea", la cual se utiliza en caso de no querer continuar con una tarea asignada y ya iniciada. Esta acción envía un mensaje al Sistema de Transición indicando que se cancela la tarea y que debe ser asignada de nuevo, posiblemente a otro usuario. Al cancelar una tarea, esta deja de listarse en las tareas asignadas.

<a class="" data-lightbox="Cancelar tarea iniciada" href="_static/sistema_de_transicion/Cancelar_tarea.gif" title="Cancelar tarea iniciada" data-title="Cancelar tarea iniciada"><img src="_static/sistema_de_transicion/Cancelar_tarea.gif" class="align-center" width="800px" alt="Cancelar tarea iniciada"/></a>

## Salir

Para salir del Sistema de Transición se da clic en el botón “Salir” y luego clic en el botón “Si” de la ventana de confirmación.

<a class="" data-lightbox="Salir del  Sistema de transición" href="_static/sistema_de_transicion/Salir.gif" title="Salir del  Sistema de transición" data-title="Salir del  Sistema de transición"><img src="_static/sistema_de_transicion/Salir.gif" class="align-center" width="800px" alt="Salir del  Sistema de transición"/></a>
