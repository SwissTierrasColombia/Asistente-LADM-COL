# Asistente LADM_COL
Plugin de [QGIS](http://qgis.org) que ayuda a capturar y mantener datos conformes con [LADM_COL](https://github.com/AgenciaImplementacion/LADM_COL) y a generar archivos de intercambio de [INTERLIS](http://www.interlis.ch/index_e.htm) (.XTF).

Licencia: [GNU General Public License v3.0](https://github.com/AgenciaImplementacion/Asistente-LADM_COL/blob/master/LICENSE)


Un proyecto de: [Agencia de Implementación](https://www.proadmintierra.info/) ([BSF-Swissphoto AG](http://bsf-swissphoto.com/) - [INCIGE S.A.S](http://www.incige.com/))



## Funcionalidades

La versión actual (0.0.2) del Asistente LADM_COL permite:

 - Capturar datos para el modelo LADM_COL v2.2.0.
 - Agregar puntos a la capa `Punto Lindero` desde archivo CSV.
   - Validar para evitar insertar puntos superpuestos.
 - Definir `Linderos` digitalizando sobre el mapa.
   - Ayudas para la digitalización:
     - Configuración automática de snapping y de valores predeterminados para campos.
     - Partir líneas seleccionadas por segmento.
     - Unir líneas seleccionadas.
 - Crear `Terrenos`:
   - A partir de linderos seleccionados.
   - A partir de una capa fuente con la misma estructura de campos.
 - Llenar automáticamente tablas de topología:
   - `PuntosCCL` (relaciona `Punto Lindero` y `Lindero`)
   - `MasCCL`    (relaciona `Lindero` y `Terreno`)

## Pruebas automatizadas al software

- Linux: https://travis-ci.org/AgenciaImplementacion/Asistente-LADM_COL
- Windows: http://portal.proadmintierra.info:18000/
  
