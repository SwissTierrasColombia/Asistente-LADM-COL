Instalación
************

Requerimientos mínimos
-----------------------

Para usar el Asistente LADM_COL se requiere:

 - Sistema Operativo:
   - Windows 10
   - GNU/Linux
   - macOS
 - Software base:
   - QGIS v3.10.0-A Coruña o superior
   - Java v1.8
   - PostgreSQL 9.5 o superior (funciona PostgreSQL 10, 11 o 12).
   - PostGIS 2.4 o superior.
 - Complementos de QGIS (al instalar el Asistente LADM-COL usando el Administrador de Complementos de QGIS, las dependencias se instalarán automáticamente):
   - `QGIS Model Baker v6.1.1.4 <https://github.com/SwissTierrasColombia/QgisModelBaker/releases/download/v6.1.1.4/QgisModelBaker_6114.zip>`_.
   - MapSwipe Tool v1.2

Proceso de instalación
-----------------------

- Es necesario tener el Software QGIS versión 3 instalado, recomendamos usar la versión 3.10.0-A Coruña o superior, para obtener este diríjete a QGIS_
- El proceso puede ser observado graficamete en el siguiente GIF:

.. image:: _static/instalacion/instalation.gif
    :height: 500
    :width: 800
    :alt: Proceso de instalación del plugin
    :download: true
    :title: Proceso de instalación del plugin

- Asegúrate de tener la última versión del plugin QgisModelBaker, el Asistente LADM_COL
  depende de este plugin para funcionar, de lo contrario este mensaje aparecerá:

.. image:: _static/instalacion/error_asistente_qgis_model_baker.png
    :height: 500
    :width: 800
    :alt: Error de dependencia QgisModelBaker
    :download: true
    :title: Error de dependencia QgisModelBaker

- Si tienes un error, puedes instalar el plugin QgisModelBaker como en el siguiente gif:

.. image:: _static/instalacion/instalation_qgis_model_baker.gif
    :height: 500
    :width: 800
    :alt: Instalación de QgisModelBaker
    :download: true
    :title: Instalación de QgisModelBaker


Habilitar proyección con Origen Único Nacional
------------------------------------------------

Para poder usar la proyección con Origen Único Nacional antes de que esté oficialmente en la base de datos de Sistemas de Referencia de QGIS, debemos permitir que el Asistente LADM-COL configure dicha proyección.

Para ello, basta con otorgar estos dos permisos de escritura al usuario con el cual usamos QGIS:

.. image:: _static/instalacion/permisos_srs.gif
    :height: 500
    :width: 800
    :alt: Habilitar proyección con Origen Único Nacional
    :download: true
    :title: Habilitar proyección con Origen Único Nacional

Suscríbete a los lanzamientos del Asistente-LADM_COL
-----------------------------------------------------

1. Ingrese al siguiente ENLACE_
2. Busque Asistente-LADM_COL.
3. Seleccione ingrese correo electronico.
4. Inicia sesión o regístrate el correo electrónico y la contraseña.
5. Listo, estás suscrito a los lanzamientos del Asistente-LADM_COL.

.. image:: _static/instalacion/suscribe_notification_new_release.gif
    :height: 500
    :width: 800
    :alt: Suscribirse al lanzamiento de versiones Asistente LADM-COL
    :download: true
    :title: Suscribirse al lanzamiento de versiones Asistente LADM-COL

.. _ENLACE: https://gitpunch.com/
.. _QGIS: https://qgis.org/es/site/forusers/download.html