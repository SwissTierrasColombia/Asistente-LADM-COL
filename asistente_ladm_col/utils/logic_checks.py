from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication,
                              QVariant)
from qgis.core import (QgsApplication,
                       QgsGeometry,
                       QgsField,
                       QgsVectorLayerUtils,
                       QgsVectorLayer)
from ..config.table_mapping_config import (ID_FIELD,
                                           COL_PARTY_BUSINESS_NAME_FIELD,
                                           COL_PARTY_LEGAL_PARTY_FIELD,
                                           COL_PARTY_SURNAME_FIELD,
                                           COL_PARTY_FIRST_NAME_FIELD,
                                           COL_PARTY_DOC_TYPE_FIELD,
                                           PARCEL_TYPE_FIELD,
                                           PARCEL_TABLE)
from ..config.general_config import (DEFAULT_EPSG,
                                     translated_strings)

class LogicChecks(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.log = QgsApplication.messageLog()

    def get_parcel_right_relationship_errors(self, db, error_layer, table_name):

        query_parcels_with_no_right = db.logic_validation_queries['PARCELS_WITH_NO_RIGHT']['query']
        table = db.logic_validation_queries['PARCELS_WITH_NO_RIGHT']['table']
        parcels_no_right = db.execute_sql_query_dict_cursor(query_parcels_with_no_right)

        query_parcels_with_repeated_domain_right = db.logic_validation_queries['PARCELS_WITH_REPEATED_DOMAIN_RIGHT']['query']
        parcels_repeated_domain_right = db.execute_sql_query_dict_cursor(query_parcels_with_repeated_domain_right)

        parcel_no_right_ids = [sublist[0] for sublist in parcels_no_right]
        parcel_duplicated_domain_right_ids = [sublist[0] for sublist in parcels_repeated_domain_right]

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry?crs=EPSG:{}".format(DEFAULT_EPSG), table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField(QCoreApplication.translate("QGISUtils", "{table}_id").format(table=table), QVariant.Int),
                              QgsField(QCoreApplication.translate("QGISUtils", "error_type"), QVariant.String)])
            error_layer.updateFields()

        new_features = list()
        for parcel_id in parcel_no_right_ids:
            new_feature = QgsVectorLayerUtils().createFeature(
                error_layer,
                QgsGeometry(),
                {0: parcel_id,
                 1: translated_strings.ERROR_PARCEL_WITH_NO_RIGHT})
            new_features.append(new_feature)

        for parcel_id in parcel_duplicated_domain_right_ids:
            new_feature = QgsVectorLayerUtils().createFeature(
                error_layer,
                QgsGeometry(),
                {0: parcel_id,
                 1: translated_strings.ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        return len(new_features), error_layer

    def get_duplicate_records_in_a_table(self, db, table, fields, error_layer,  id_field=ID_FIELD):
        rule = 'DUPLICATE_RECORDS_IN_TABLE'
        query = db.logic_validation_queries[rule]['query']
        table_name = QCoreApplication.translate("LogicChecksConfigStrings", "Duplicate records in '{table}'").format(table=table)

        # config query
        query = query.format(schema=db.schema, table=table, fields=", ".join(fields), id=id_field)

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry?crs=EPSG:{}".format(DEFAULT_EPSG), table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField(QCoreApplication.translate("QGISUtils", "duplicate_ids"), QVariant.String),
                              QgsField(QCoreApplication.translate("QGISUtils", "count"), QVariant.Int)])
            error_layer.updateFields()

        records = db.execute_sql_query(query)

        new_features = list()
        for record in records:
            new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(), {0: record['duplicate_ids'], 1: record['duplicate_total']})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        return error_layer


    def get_fractions_which_sum_is_not_one(self, db, error_layer):
        rule = 'GROUP_PARTY_FRACTIONS_SHOULD_SUM_1'
        query = db.logic_validation_queries[rule]['query']
        table_name = db.logic_validation_queries[rule]['table_name']

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry?crs=EPSG:{}".format(DEFAULT_EPSG), table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField(QCoreApplication.translate("QGISUtils", "party_group"), QVariant.Int),
                              QgsField(QCoreApplication.translate("QGISUtils", "members"), QVariant.String),
                              QgsField(QCoreApplication.translate("QGISUtils", "fraction_sum"), QVariant.Double)])
            error_layer.updateFields()

        records = db.execute_sql_query(query)
        new_features = list()
        for record in records:
            new_feature = QgsVectorLayerUtils().createFeature(
                error_layer,
                QgsGeometry(),
                {0: record['agrupacion'],
                 1: ",".join([str(f) for f in record['miembros']]),
                 2: record['suma_fracciones']})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        return error_layer

    def col_party_type_natural_validation(self, db, rule, error_layer):
        query = db.logic_validation_queries[rule]['query']
        table_name = db.logic_validation_queries[rule]['table_name']
        table = db.logic_validation_queries[rule]['table']

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry?crs=EPSG:{}".format(DEFAULT_EPSG), table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField(QCoreApplication.translate("QGISUtils", "{table}_id").format(table=table), QVariant.Int),
                              QgsField(QCoreApplication.translate("QGISUtils", "error_type"), QVariant.String)])
            error_layer.updateFields()

        records = db.execute_sql_query(query)

        new_features = list()
        for record in records:
            errors_list = list()
            if record[COL_PARTY_BUSINESS_NAME_FIELD] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{business_name} must be NULL").format(business_name=COL_PARTY_BUSINESS_NAME_FIELD))
            if record[COL_PARTY_LEGAL_PARTY_FIELD] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{legal_party} must be NULL").format(legal_party=COL_PARTY_LEGAL_PARTY_FIELD))
            if record[COL_PARTY_SURNAME_FIELD] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{surname_party} must not be NULL and It must be filled in").format(surname_party=COL_PARTY_SURNAME_FIELD))
            if record[COL_PARTY_FIRST_NAME_FIELD] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{first_name_party} must not be NULL and It must be filled in").format(first_name_party=COL_PARTY_FIRST_NAME_FIELD))
            if record[COL_PARTY_DOC_TYPE_FIELD] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{doc_type} must be different from NIT").format(doc_type=COL_PARTY_DOC_TYPE_FIELD))

            mgs_error = ', '. join(errors_list)
            new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(), {0: record[ID_FIELD], 1:mgs_error})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        return len(new_features), error_layer

    def col_party_type_no_natural_validation(self, db, rule, error_layer):

        query = db.logic_validation_queries[rule]['query']
        table_name = db.logic_validation_queries[rule]['table_name']
        table = db.logic_validation_queries[rule]['table']

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry?crs=EPSG:{}".format(DEFAULT_EPSG), table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField(QCoreApplication.translate("QGISUtils", "{table}_id").format(table=table), QVariant.Int),
                              QgsField(QCoreApplication.translate("QGISUtils", "error_type"), QVariant.String)])
            error_layer.updateFields()

        records = db.execute_sql_query(query)

        new_features = list()
        for record in records:
            errors_list = list()
            if record[COL_PARTY_BUSINESS_NAME_FIELD] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{business_name} must not be NULL and It must be filled in").format(business_name=COL_PARTY_BUSINESS_NAME_FIELD))
            if record[COL_PARTY_LEGAL_PARTY_FIELD] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{legal_party} must not be NULL and It must be filled in").format(legal_party=COL_PARTY_LEGAL_PARTY_FIELD))
            if record[COL_PARTY_SURNAME_FIELD] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{surname_party} must be NULL").format(surname_party=COL_PARTY_SURNAME_FIELD))
            if record[COL_PARTY_FIRST_NAME_FIELD] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{first_name_party} must be NULL").format(first_name_party=COL_PARTY_FIRST_NAME_FIELD))
            if record[COL_PARTY_DOC_TYPE_FIELD] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{doc_type} must be equal to NIT or Secuencial_IGAC or Secuencial_SNR").format(doc_type=COL_PARTY_DOC_TYPE_FIELD))

            mgs_error = ', '. join(errors_list)
            new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(),{0: record[ID_FIELD], 1: mgs_error})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        return len(new_features), error_layer

    def parcel_type_and_22_position_of_parcel_number_validation(self, db, rule, error_layer):

        query = db.logic_validation_queries[rule]['query']
        table_name = db.logic_validation_queries[rule]['table_name']
        table = db.logic_validation_queries[rule]['table']

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry?crs=EPSG:{}".format(DEFAULT_EPSG), table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField(QCoreApplication.translate("QGISUtils", "{table}_id").format(table=table), QVariant.Int),
                              QgsField(QCoreApplication.translate("QGISUtils", "error_type"), QVariant.String)])
            error_layer.updateFields()

        records = db.execute_sql_query(query)

        new_features = list()
        for record in records:
            mgs_error =  None
            if record[PARCEL_TYPE_FIELD] == 'NPH':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is NPH the 22nd position of the property code must be 0").format(table=PARCEL_TABLE, parcel_type=PARCEL_TYPE_FIELD)
            elif record[PARCEL_TYPE_FIELD].find('PropiedadHorizontal.') != -1:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is {value} the 22nd position of the property code must be 9").format(table=PARCEL_TABLE, parcel_type=PARCEL_TYPE_FIELD, value=record[PARCEL_TYPE_FIELD])
            elif record[PARCEL_TYPE_FIELD].find('Condominio.') != -1:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is {value} the 22nd position of the property code must be 8").format(table=PARCEL_TABLE, parcel_type=PARCEL_TYPE_FIELD, value=record[PARCEL_TYPE_FIELD])
            elif record[PARCEL_TYPE_FIELD].find('ParqueCementerio.') != -1:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is {value} the 22nd position of the property code must be 7").format(table=PARCEL_TABLE, parcel_type=PARCEL_TYPE_FIELD, value=record[PARCEL_TYPE_FIELD])
            elif record[PARCEL_TYPE_FIELD] == 'Mejora':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is Mejora the 22nd position of the property code must be 5").format(table=PARCEL_TABLE, parcel_type=PARCEL_TYPE_FIELD)
            elif record[PARCEL_TYPE_FIELD] == 'Via':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is Via the 22nd position of the property code must be 4").format(table=PARCEL_TABLE, parcel_type=PARCEL_TYPE_FIELD)
            elif record[PARCEL_TYPE_FIELD] == 'BienUsoPublico':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is BienUsoPublico the 22nd position of the property code must be 3").format(table=PARCEL_TABLE, parcel_type=PARCEL_TYPE_FIELD)

            new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(), {0: record[ID_FIELD], 1: mgs_error})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        return len(new_features), error_layer

    def uebaunit_parcel_validation(self, db, rule, error_layer):
        query = db.logic_validation_queries[rule]['query']
        table_name = db.logic_validation_queries[rule]['table_name']
        table = db.logic_validation_queries[rule]['table']

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry?crs=EPSG:{}".format(DEFAULT_EPSG), table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField(QCoreApplication.translate("QGISUtils", "{table}_id").format(table=table), QVariant.Int),
                              QgsField(QCoreApplication.translate("QGISUtils", "associated_parcels"), QVariant.Int),
                              QgsField(QCoreApplication.translate("QGISUtils", "associated_buildings"), QVariant.Int),
                              QgsField(QCoreApplication.translate("QGISUtils", "associated_building_units"), QVariant.Int),
                              QgsField(QCoreApplication.translate("QGISUtils", "error_type"), QVariant.String)])
            error_layer.updateFields()

        records = db.execute_sql_query(query)

        new_features = list()
        for record in records:
            mgs_error = None

            plot_count = record['sum_t'] # count of plots associated to the parcel
            building_count = record['sum_c'] # count of buildings associated to the parcel
            building_unit_count = record['sum_uc'] # count of building units associated to the parcel

            if record[PARCEL_TYPE_FIELD] == 'NPH':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is 'NPH' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_unit_count=building_unit_count,table=PARCEL_TABLE, parcel_type=PARCEL_TYPE_FIELD)
            elif record[PARCEL_TYPE_FIELD] == 'PropiedadHorizontal.Matriz':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is 'PropiedadHorizontal.Matriz' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_unit_count=building_unit_count, table=PARCEL_TABLE,parcel_type=PARCEL_TYPE_FIELD)
            elif record[PARCEL_TYPE_FIELD] == 'Condominio.Matriz':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is 'Condominio.Matriz' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_unit_count=building_unit_count, table=PARCEL_TABLE,parcel_type=PARCEL_TYPE_FIELD)
            elif record[PARCEL_TYPE_FIELD] == 'ParqueCementerio.Matriz':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is 'ParqueCementerio.Matriz' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_unit_count=building_unit_count, table=PARCEL_TABLE,parcel_type=PARCEL_TYPE_FIELD)
            elif record[PARCEL_TYPE_FIELD] == 'BienUsoPublico':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is 'BienUsoPublico' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_unit_count=building_unit_count, table=PARCEL_TABLE,parcel_type=PARCEL_TYPE_FIELD)
            elif record[PARCEL_TYPE_FIELD] == 'Condominio.UnidadPredial':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is 'Condominio.UnidadPredial' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_unit_count=building_unit_count, table=PARCEL_TABLE,parcel_type=PARCEL_TYPE_FIELD)
            elif record[PARCEL_TYPE_FIELD] == 'Via':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is 'Via' you should have 1 plot and 0 building and 0 building unit but you have {plot_count} plot(s) and {building_count} building(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_count=building_count, building_unit_count=building_unit_count, table=PARCEL_TABLE,parcel_type=PARCEL_TYPE_FIELD)
            elif record[PARCEL_TYPE_FIELD] == 'ParqueCementerio.UnidadPrivada':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is 'ParqueCementerio.UnidadPrivada' you should have 1 plot and 0 building and 0 building unit but you have {plot_count} plot(s) and {building_count} building(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_count=building_count, building_unit_count=building_unit_count, table=PARCEL_TABLE,parcel_type=PARCEL_TYPE_FIELD)
            elif record[PARCEL_TYPE_FIELD] == 'PropiedadHorizontal.UnidadPredial':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is 'PropiedadHorizontal.UnidadPredial' you should have 0 plot and 0 building but you have {plot_count} plot(s) and {building_count} building(s)").format(plot_count=plot_count, building_count=building_count, table=PARCEL_TABLE,parcel_type=PARCEL_TYPE_FIELD)
            elif record[PARCEL_TYPE_FIELD] == 'Mejora':
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type} of {table} is 'Mejora' you should have 0 plot and 1 building and 0 building unit but you have {plot_count} plot(s) and {building_count} building(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_count=building_count, building_unit_count=building_unit_count, table=PARCEL_TABLE,parcel_type=PARCEL_TYPE_FIELD)

            new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(),
                                                              {0: record[ID_FIELD],
                                                               1: plot_count,
                                                               2: building_count,
                                                               3: building_unit_count,
                                                               4: mgs_error})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        return len(new_features), error_layer
