## Captura de datos en campo

#### Recomendaciones para plantillas .QGS

Los archivos *.qgs* son archivos de proyectos de QGIS. Para guardar un proyecto como *.qgs*, ve a `Project -->Save as...` y selecciona el tipo de archivo de salida como *.QGS*.



Si deseas ajustar las plantillas que sugerimos o crear tu propia plantilla .QGS para usarla en un flujo de trabajo que incluya **Asignación de predios** y **Sincronización de datos de campo** desde el Asistente LADM-COL, ten en cuenta lo siguiente:

1. Asegúrate de guardar el proyecto con rutas relativas (`Project -->Properties --> General -->Save paths -->relative`).
2. Apunta a una base de datos GeoPackage llamada *data.gpkg*, que se encuentre en la misma carpeta del proyecto .QGS. 
3. Define valores automáticos para el campo `t_basket` de **todas** tus capas (excepto tablas de dominios). Define el valor automático como `9999` (no es necesario seleccionar la casilla de `Apply default value on update`).
4. (Opcional) El Coordinador de Grupo deberá encargarse de preparar el ráster que desea asignar a los reconocedores. Dicho ráster debe tener extensión *.tif*, debe llamarse *raster.tif* y debe usar el EPSG:9377 (proyección Origen Nacional).