Surveying and Representation
*****************************

Create Point
=============

Boundary Point
--------------

Choose this option to load points to **Boundary Points** layer from *LADM_COL*
model.

**Boundary Point** is a specialized class of *LA_Point* which stores points that
define a boundary. Boundary is an instance of *LA_BoundaryFaceString* class and
its specializations.

1. From a CSV file with the required structure

  Add a Comma Separated Values file (CSV), choosing the delimiter and fields that
  contain point coordinates.

  .. image:: ../static/_CREAR_PUNTO_LINDERO_.gif
     :height: 500
     :width: 800
     :alt: Create Control Point

2. From another QGIS layer/table (setting a field mapping)

  Choose this option to open a window that allows you to import data from a source
  layer into the *LADM_COL* **puntolindero** layer.

  If the field structure of input and target layers differs, you can set a field
  mapping to define field transformations and correspondence.

  For use this function check this `LINK <../mapping_fields.html>`_.

Survey Point
------------

Choose this option to load points to **Survey Points** layer from *LADM_COL*
model.

**Survey Point** is a specialized class of *LA_Point* which represents a
building, right of way or auxiliary vertex.

1. From a CSV file with the required structure

  Add a Comma Separated Values file (CSV), choosing the delimiter and fields that
  contain point coordinates.

  .. image:: ../static/_CREAR_PUNTO_LINDERO_.gif
     :height: 500
     :width: 800
     :alt: Create Boundary Point

2. From another QGIS layer/table (setting a field mapping)

  Choose this option to open a window that allows you to import data from a source
  layer into the *LADM_COL* **puntolevantamiento** layer.

  If the field structure of input and target layers differs, you can set a field
  mapping to define field transformations and correspondence.

  For use this function check this `LINK <../mapping_fields.html>`_.

Control Point
-------------

Choose this option to load points to **Control Points** layer from *LADM_COL*
model.

**Control Point** is a specialized class of *LA_Point* which represents points
belonging to the local network, used in cadastre operation for surveying
physical information of the territorial objects.

1. From a CSV file with the required structure

  Add a Comma Separated Values file (CSV), choosing the delimiter and fields that
  contain point coordinates.

  .. image:: ../static/crear_punto_control.gif
     :height: 500
     :width: 800
     :alt: Create Boundary Point

2. From another QGIS layer/table (setting a field mapping)

  Choose this option to open a window that allows you to import data from a source
  layer into the *LADM_COL* **puntocontrol** layer.

  If the field structure of input and target layers differs, you can set a field
  mapping to define field transformations and correspondence.

  For use this function check this `LINK <../mapping_fields.html>`_.

Create Boundary
================

1. Digitizing

  Choose this option if you want to create a **Boundary** using QGIS digitizing
  tools.

  **Boundary** is a specialization of the *LA_CadenaCarasLindero* class to store
  boundaries that define plots. Two boundaries must not cross or overlap.

  .. image:: ../static/_CREAR_LINDERO.gif
     :height: 500
     :width: 800
     :alt: Create Boundary Point

2. From another QGIS Layer/table (setting a field mapping)

  Choose this option to open a window that allows you to import data from a source
  table into the *LADM_COL* **lindero** table.

  If the field structure of input and target tables differs, you can set a field
  mapping to define field transformations and correspondence.

  For use this function check this `LINK <../mapping_fields.html>`_.

  If you need to merge or explodes boundaries you can use the *merge* and *explode*
  buttons on Toolbar LADM_COL.

  .. image:: ../static/_UNIR_PARTIR_LINDERO.gif
     :height: 500
     :width: 800
     :alt: Create Boundary Point

|

  You can fill point bfs topology table using the button *Fill Point BFS* on
  Toolbar LADM_COL which makes automatic and faster this job. For use this
  function check this `LINK <../toolbar.html>`_.
