Surveying and Representation
*****************************

Create Point
=============

.. image:: ../static/06_CARGA_PUNTOS.gif
   :height: 500
   :width: 800
   :alt: add points

1. Boundary Point

Choose this option to load points to **Boundary Points** layer from *LADM_COL*
model.

**Boundary Point** is a specialized class of *LA_Point* which stores points that
define a boundary. Boundary is an instance of *LA_BoundaryFaceString* class and
its specializations.

2. Survey Point

Choose this option to load points to **Survey Points** layer from *LADM_COL*
model.

**Survey Point** is a specialized class of *LA_Point* which represents a
building, right of way or auxiliary vertex.


Create Boundary
================

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

.. image:: ../static/def_bndrs.png
   :height: 400
   :width: 400
   :alt: alternate text
