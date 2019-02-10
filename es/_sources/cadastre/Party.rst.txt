Party
======

Create Party
--------------

1. Entering data manually using a form

  Choose this option if you want to create a **Party** using a form.

  **Party** is a natural or non-natural person who has rights or who is subject
  to restrictions or responsibilities related to one or more *Parcels*.

  .. image:: ../static/crear_interesado_natural.gif
     :height: 500
     :width: 800
     :alt: Create Party

2. From another QGIS layer/table (setting a field mapping)

  Choose this option to open a window that allows you to import data from a source
  table into the *LADM_COL* **col_interesado** table.

  If the field structure of input and target tables differs, you can set a field
  mapping to define field transformations and correspondence.

  For use this function check this `LINK <../mapping_fields.html>`_.


Group Party
-----------

1. Entering data manually using a form

  Choose this option if you want to create a **Group Party** using a form.

  **Group Party** registers parties that represents groups of people.
  The group itself is registered, independently of the persons separately.
  This is what happens, for example, with an ethnic group or a civil group.

  This **Group Party** has rights or is subject to restrictions or
  responsibilities related to one or more *Parcels*.

  You can insert fractions to have the percent correspondence in the **Group Party**,
  the sum of numerators divided by the sum of denominators must be 1, otherwise the 
  creation of the grouping will not be allowed.
  
  .. image:: ../static/group_party.gif
     :height: 500
     :width: 800
     :alt: Create Group Party
