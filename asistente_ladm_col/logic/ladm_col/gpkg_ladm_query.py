from asistente_ladm_col.logic.ladm_col.qgis_ladm_query import QGISLADMQuery


class GpkgLADMQuery(QGISLADMQuery):
    def __init__(self, qgis_utils):
        super(GpkgLADMQuery, self).__init__(qgis_utils)