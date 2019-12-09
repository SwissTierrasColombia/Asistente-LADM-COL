from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication,
                              QVariant)
from qgis.core import (QgsGeometry,
                       QgsField,
                       QgsVectorLayerUtils,
                       QgsVectorLayer)

from asistente_ladm_col.config.general_config import (ERROR_PARCEL_WITH_NO_RIGHT,
                                                      ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT)
from asistente_ladm_col.config.table_mapping_config import Names


class LogicChecks(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.names = Names()

    def get_parcel_right_relationship_errors(self, db, error_layer, table_name, translated_strings):
        logic_validation_queries = db.get_logic_validation_queries()

        query_parcels_with_no_right = logic_validation_queries['PARCELS_WITH_NO_RIGHT']['query']
        table = logic_validation_queries['PARCELS_WITH_NO_RIGHT']['table']
        parcels_no_right = db.execute_sql_query_dict_cursor(query_parcels_with_no_right)

        query_parcels_with_repeated_domain_right = logic_validation_queries['PARCELS_WITH_REPEATED_DOMAIN_RIGHT']['query']
        parcels_repeated_domain_right = db.execute_sql_query_dict_cursor(query_parcels_with_repeated_domain_right)

        parcel_no_right_ids = [sublist[0] for sublist in parcels_no_right]
        parcel_duplicated_domain_right_ids = [sublist[0] for sublist in parcels_repeated_domain_right]

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry", table_name, "memory")
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
                 1: translated_strings[ERROR_PARCEL_WITH_NO_RIGHT]})
            new_features.append(new_feature)

        for parcel_id in parcel_duplicated_domain_right_ids:
            new_feature = QgsVectorLayerUtils().createFeature(
                error_layer,
                QgsGeometry(),
                {0: parcel_id,
                 1: translated_strings[ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT]})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        return len(new_features), error_layer

    def get_duplicate_records_in_a_table(self, db, table, fields, error_layer, id_field):
        logic_validation_queries = db.get_logic_validation_queries()
        rule = 'DUPLICATE_RECORDS_IN_TABLE'
        query = logic_validation_queries[rule]['query']
        table_name = QCoreApplication.translate("LogicChecksConfigStrings", "Duplicate records in '{table}'").format(table=table)

        # config query
        query = query.format(schema=db.schema, table=table, fields=", ".join(fields), id=id_field)

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry", table_name, "memory")
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
        logic_validation_queries = db.get_logic_validation_queries()
        rule = 'GROUP_PARTY_FRACTIONS_SHOULD_SUM_1'
        query = logic_validation_queries[rule]['query']
        table_name = logic_validation_queries[rule]['table_name']

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry", table_name, "memory")
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
        logic_validation_queries = db.get_logic_validation_queries()
        query = logic_validation_queries[rule]['query']
        table_name = logic_validation_queries[rule]['table_name']
        table = logic_validation_queries[rule]['table']

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry", table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField(QCoreApplication.translate("QGISUtils", "{table}_id").format(table=table), QVariant.Int),
                              QgsField(QCoreApplication.translate("QGISUtils", "error_type"), QVariant.String)])
            error_layer.updateFields()

        records = db.execute_sql_query(query)

        new_features = list()
        for record in records:
            errors_list = list()
            if record[self.names.OP_PARTY_T_BUSINESS_NAME_F] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{business_name} must be NULL").format(business_name=self.names.OP_PARTY_T_BUSINESS_NAME_F))
            if record[self.names.OP_PARTY_T_SURNAME_1_F] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{surname_party} must not be NULL and It must be filled in").format(surname_party=self.names.OP_PARTY_T_SURNAME_1_F))
            if record[self.names.OP_PARTY_T_FIRST_NAME_1_F] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{first_name_party} must not be NULL and It must be filled in").format(first_name_party=self.names.OP_PARTY_T_FIRST_NAME_1_F))
            if record[self.names.OP_PARTY_T_DOCUMENT_TYPE_F] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{doc_type} must be different from NIT").format(doc_type=self.names.OP_PARTY_T_DOCUMENT_TYPE_F))

            mgs_error = ', '. join(errors_list)
            new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(), {0: record[self.names.T_ID_F], 1:mgs_error})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        return len(new_features), error_layer

    def col_party_type_no_natural_validation(self, db, rule, error_layer):
        logic_validation_queries = db.get_logic_validation_queries()
        query = logic_validation_queries[rule]['query']
        table_name = logic_validation_queries[rule]['table_name']
        table = logic_validation_queries[rule]['table']

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry", table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField(QCoreApplication.translate("QGISUtils", "{table}_id").format(table=table), QVariant.Int),
                              QgsField(QCoreApplication.translate("QGISUtils", "error_type"), QVariant.String)])
            error_layer.updateFields()

        records = db.execute_sql_query(query)

        new_features = list()
        for record in records:
            errors_list = list()
            if record[self.names.OP_PARTY_T_BUSINESS_NAME_F] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{business_name} must not be NULL and It must be filled in").format(business_name=self.names.OP_PARTY_T_BUSINESS_NAME_F))
            if record[self.names.OP_PARTY_T_SURNAME_1_F] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{surname_party} must be NULL").format(surname_party=self.names.OP_PARTY_T_SURNAME_1_F))
            if record[self.names.OP_PARTY_T_FIRST_NAME_1_F] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{first_name_party} must be NULL").format(first_name_party=self.names.OP_PARTY_T_FIRST_NAME_1_F))
            if record[self.names.OP_PARTY_T_DOCUMENT_TYPE_F] > 0:
                errors_list.append(QCoreApplication.translate("LogicChecksConfigStrings", "{doc_type} must be equal to NIT or Secuencial_IGAC or Secuencial_SNR").format(doc_type=self.names.OP_PARTY_T_DOCUMENT_TYPE_F))

            mgs_error = ', '. join(errors_list)
            new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(),{0: record[self.names.T_ID_F], 1: mgs_error})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        return len(new_features), error_layer

    def parcel_type_and_22_position_of_parcel_number_validation(self, db, rule, error_layer):
        logic_validation_queries = db.get_logic_validation_queries()
        query = logic_validation_queries[rule]['query']
        table_name = logic_validation_queries[rule]['table_name']
        table = logic_validation_queries[rule]['table']

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry", table_name, "memory")
            pr = error_layer.dataProvider()
            pr.addAttributes([QgsField(QCoreApplication.translate("QGISUtils", "{table}_id").format(table=table), QVariant.Int),
                              QgsField(QCoreApplication.translate("QGISUtils", "error_type"), QVariant.String)])
            error_layer.updateFields()

        records = db.execute_sql_query(query)

        new_features = list()
        for record in records:
            mgs_error =  None
            if record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 0").format(table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] in (self.names.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT, self.names.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT):
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 9").format(table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT + " or " + self.names.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] in (self.names.PARCEL_TYPE_CONDOMINIUM_PARENT, self.names.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT):
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 8").format(table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_CONDOMINIUM_PARENT + " or " + self.names.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] in (self.names.PARCEL_TYPE_CEMETERY_PARENT, self.names.PARCEL_TYPE_CEMETERY_PARCEL_UNIT):
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 7").format(table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_CEMETERY_PARENT + " or " + self.names.PARCEL_TYPE_CEMETERY_PARCEL_UNIT)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 5").format(table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 5").format(table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_ROAD:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 4").format(table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_ROAD)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_PUBLIC_USE:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is {parcel_type} the 22nd position of the property code must be 3").format(table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_PUBLIC_USE)

            new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(), {0: record[self.names.T_ID_F], 1: mgs_error})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        return len(new_features), error_layer

    def uebaunit_parcel_validation(self, db, rule, error_layer):
        logic_validation_queries = db.get_logic_validation_queries()
        query = logic_validation_queries[rule]['query']
        table_name = logic_validation_queries[rule]['table_name']
        table = logic_validation_queries[rule]['table']

        if error_layer is None:
            error_layer = QgsVectorLayer("NoGeometry", table_name, "memory")
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

            if record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_unit_count=building_unit_count, table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_unit_count=building_unit_count, table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_CONDOMINIUM_PARENT:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_unit_count=building_unit_count, table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_CONDOMINIUM_PARENT)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_CEMETERY_PARENT:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_unit_count=building_unit_count, table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_CEMETERY_PARENT)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_PUBLIC_USE:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_unit_count=building_unit_count, table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_PUBLIC_USE)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building unit but you have {plot_count} plot(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_unit_count=building_unit_count, table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_ROAD:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building and 0 building unit but you have {plot_count} plot(s) and {building_count} building(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_count=building_count, building_unit_count=building_unit_count, table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_ROAD)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_CEMETERY_PARCEL_UNIT:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 1 plot and 0 building and 0 building unit but you have {plot_count} plot(s) and {building_count} building(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_count=building_count, building_unit_count=building_unit_count, table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_CEMETERY_PARCEL_UNIT)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 0 plot and 0 building but you have {plot_count} plot(s) and {building_count} building(s)").format(plot_count=plot_count, building_count=building_count, table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 0 plot and 1 building and 0 building unit but you have {plot_count} plot(s) and {building_count} building(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_count=building_count, building_unit_count=building_unit_count, table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA)
            elif record[self.names.OP_PARCEL_T_PARCEL_TYPE_F] == self.names.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA:
                mgs_error = QCoreApplication.translate("LogicChecksConfigStrings", "When the {parcel_type_field} of {table} is '{parcel_type}' you should have 0 plot and 1 building and 0 building unit but you have {plot_count} plot(s) and {building_count} building(s) and {building_unit_count} building unit(s)").format(plot_count=plot_count, building_count=building_count, building_unit_count=building_unit_count, table=self.names.OP_PARCEL_T, parcel_type_field=self.names.OP_PARCEL_T_PARCEL_TYPE_F, parcel_type=self.names.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA)

            new_feature = QgsVectorLayerUtils().createFeature(error_layer, QgsGeometry(),
                                                              {0: record[self.names.T_ID_F],
                                                               1: plot_count,
                                                               2: building_count,
                                                               3: building_unit_count,
                                                               4: mgs_error})
            new_features.append(new_feature)

        error_layer.dataProvider().addFeatures(new_features)

        return len(new_features), error_layer
