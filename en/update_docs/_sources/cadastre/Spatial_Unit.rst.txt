Spatial Unit
=============

In this process you define the new spatial objects that you want to add to the
database with the structure of the *LADM_COL* model.


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


Create Building Unit
---------------------

. Digitizing

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
