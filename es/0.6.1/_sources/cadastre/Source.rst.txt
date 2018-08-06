Source
=======

Administrative Source
----------------------

1. Entering data manually using a form

  Choose this option if you want to create an **Administrative Source** using a
  form.

  **Administrative Source** is a specialization of the *COL_Fuente* class to store
  those sources corresponding to documents (mortgage document, notarial documents,
  historical documents, and the like) that document the relationship
  between parties and parcels.

  .. image:: ../static/crear_fuente_administrativa.gif
     :height: 500
     :width: 800
     :alt: Create Administrative Source

2. From another QGIS layer/table (setting a field mapping)

  Choose this option to open a window that allows you to import data from a source
  table into the *LADM_COL* **col_fuenteadministrativa** table.

  If the field structure of input and target tables differs, you can set a field
  mapping to define field transformations and correspondence.

  For use this function check this `LINK <../mapping_fields.html>`_.

Spatial Source
--------------

1. Entering data manually using a form

  Choose this option if you want to create a **Spatial Source** using a form.
  (Previously you have to select objects from the table terreno, lindero,
  puntolindero, puntolevantamiento, o punto control which will be associated
  with the new **Spatial Source**)

  **Spatial Source** is a specialization of the *COL_Fuente* class to store those
  sources corresponding to spatial data (geographic features, satellite imagery,
  photogrammetric flights, maps, coordinate listings, ancient or modern plans,
  location descriptions, and the like) that technically document the relationship
  between parties and parcels.

  .. image:: ../static/crear_fuente_espacial.gif
     :height: 500
     :width: 800
     :alt: Create Spatial Source

2. From another QGIS layer/table (setting a field mapping)

  Choose this option to open a window that allows you to import data from a source
  table into the *LADM_COL* **col_fuenteespacial** table.

  If the field structure of input and target tables differs, you can set a field
  mapping to define field transformations and correspondence.

  For use this function check this `LINK <../mapping_fields.html>`_.
