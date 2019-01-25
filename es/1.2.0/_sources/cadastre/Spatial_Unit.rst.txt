Spatial Unit
=============

Create Plot
-----------

1. Selecting existing boundaries

  Choose this option if you want to create a **Plot** from existing *Boundaries*.

  **Plot** is a portion of land with a defined geographical extension.

  .. image:: ../static/_CREAR_TERRENO.gif
     :height: 500
     :width: 800
     :alt: Create Plot

2. From another QGIS Layer/table (setting a field mapping)

  Choose this option to open a window that allows you to import data from a source
  layer into the *LADM_COL* **terreno** layer.

  If the field structure of input and target layers differs, you can set a field
  mapping to define field transformations and correspondence.

  For use this function check this `LINK <../mapping_fields.html>`_.

Create Building
---------------

1. Digitizing

  Choose this option if you want to create a **Building** from existing *Survey Points*.

  **Building** is a type of legal space of the building unit of the LADM model that
  stores data specific of the resulting valuation.

  .. image:: ../static/crear_construccion.gif
     :height: 500
     :width: 800
     :alt: Create Building

2. From another QGIS Layer/table (setting a field mapping)

  Choose this option to open a window that allows you to import data from a source
  layer into the *LADM_COL* **construccion** layer.

  If the field structure of input and target layers differs, you can set a field
  mapping to define field transformations and correspondence.

  For use this function check this `LINK <../mapping_fields.html>`_.

Create Building Unit
---------------------

1. Digitizing

  Choose this option if you want to create a **Building Unit** from existing
  *Survey Points*.

  **Building Unit** is a group of consolidated materials within a Parcel that has
  specific characteristics in terms of physical constituent elements and their usage.

  .. image:: ../static/create_building_unit.gif
     :height: 500
     :width: 800
     :alt: Create building unit

2. From another QGIS Layer/table (setting a field mapping)

  Choose this option to open a window that allows you to import data from a source
  layer into the *LADM_COL* **unidadconstruccion** layer.

  If the field structure of input and target layers differs, you can set a field
  mapping to define field transformations and correspondence.

  For use this function check this `LINK <../mapping_fields.html>`_.

Create Right of Way
-------------------

1. Digitizing Centerline

  Choose this option if you want to create a **Right of Way** digitizing
  centerline using existing *Survey Points* and giving a width value.

  **Right of Way** is a type of spatial unit of the LADM model wich allows the
  representation of a Right of Way associated to a *LA_BAUnit*.

  .. image:: ../static/create_right_of_way_line.gif
     :height: 500
     :width: 800
     :alt: Create Right of Way Centerline

2. Digitizing Polygon

  Choose this option if you want to create a **Right of Way** digitizing a polygon
  using existing *Survey Points*.

  **Right of Way** is a type of spatial unit of the LADM model wich allows the
  representation of a Right of Way associated to a *LA_BAUnit*.

  .. image:: ../static/create_right_of_way_polygon.gif
     :height: 500
     :width: 800
     :alt: Create Right of Way Polygon

3. From another QGIS Layer/table (setting a field mapping)

  Choose this option to open a window that allows you to import data from a source
  layer into the *LADM_COL* **servidumbrepaso** layer.

  If the field structure of input and target layers differs, you can set a field
  mapping to define field transformations and correspondence.

  For use this function check this `LINK <../mapping_fields.html>`_.

4. Fill Right of way relations

  To know how to use this function go to this `LINK <../toolbar.html#fill-right-of-way-relations>`_.
