Surveying and Representation
*****************************

Create Point
=============

1. Boundary Point

.. image:: ../static/_CREAR_PUNTO_LINDERO_.gif
   :height: 500
   :width: 800
   :alt: Create Boundary Point

Choose this option to load points to **Boundary Points** layer from *LADM_COL*
model.

**Boundary Point** is a specialized class of *LA_Point* which stores points that
define a boundary. Boundary is an instance of *LA_BoundaryFaceString* class and
its specializations.

2. Survey Point

.. image:: ../static/crear_punto_levantamiento_csv.gif
   :height: 500
   :width: 800
   :alt: Crear Survey Points

Choose this option to load points to **Survey Points** layer from *LADM_COL*
model.

**Survey Point** is a specialized class of *LA_Point* which represents a
building, right of way or auxiliary vertex.


Create Boundary
================

.. image:: ../static/_CREAR_LINDERO.gif
   :height: 500
   :width: 800
   :alt: Create Boundary Point


1. Digitizing

Choose this option if you want to create a **Boundary** using QGIS digitizing
tools.

**Boundary** is a specialization of the *LA_CadenaCarasLindero* class to store
boundaries that define plots. Two boundaries must not cross or overlap.

2. From another QGIS Layer/table (setting a field mapping)

Choose this option to open a window that allows you to import data from a source
table into the *LADM_COL* **lindero** table.

If the field structure of input and target tables differs, you can set a field
mapping to define field transformations and correspondence.

.. image:: ../static/_LLENAR_TOPOLOGIAS.gif
   :height: 500
   :width: 800
   :alt: Create Boundary Point

.. image:: ../static/_UNIR_PARTIR_LINDERO.gif
   :height: 500
   :width: 800
   :alt: Create Boundary Point
