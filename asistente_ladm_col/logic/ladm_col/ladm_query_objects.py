from abc import ABC


class AbsFieldLADMQuery(ABC):
    def __init__(self, field_alias):
        super(AbsFieldLADMQuery, self).__init__()
        self.field_alias = field_alias


class OwnField(AbsFieldLADMQuery):
    def __init__(self, field_name, field_alias):
        super(OwnField, self).__init__(field_alias)
        self.field_name = field_name


class DomainOwnField(OwnField):
    def __init__(self, field_name, field_alias, domain_table):
        super(DomainOwnField, self).__init__(field_name, field_alias)
        self.domain_table = domain_table


class EvalExprOwnField(AbsFieldLADMQuery):
    def __init__(self, field_alias, expression):
        super(EvalExprOwnField, self).__init__(field_alias)
        self.expression = expression


class AbsRelatedFields(AbsFieldLADMQuery):
    def __init__(self, field_alias, relate_table, relate_table_filter_field):
        super(AbsRelatedFields, self).__init__(field_alias)
        self.relate_table = relate_table
        self.relate_table_filter_field = relate_table_filter_field


class RelatedOwnFieldObject(AbsRelatedFields):
    def __init__(self, field_alias, relate_table, relate_table_fields, relate_table_filter_field):
        super(RelatedOwnFieldObject, self).__init__(field_alias, relate_table, relate_table_filter_field)
        self.relate_table_fields = relate_table_fields


class RelatedOwnFieldValue(AbsRelatedFields):
    def __init__(self, field_alias, relate_table, relate_table_field, relate_table_filter_field):
        super(RelatedOwnFieldValue, self).__init__(field_alias, relate_table, relate_table_filter_field)
        self.relate_table_field = relate_table_field


class RelatedRemoteFieldObject(RelatedOwnFieldObject):
    def __init__(self, field_alias, relate_table, relate_table_fields, relate_table_filter_field, filter_sub_level):
        super(RelatedRemoteFieldObject, self).__init__(field_alias, relate_table, relate_table_fields, relate_table_filter_field)
        self.filter_sub_level = filter_sub_level


class RelatedRemoteFieldValue(RelatedOwnFieldValue):
    def __init__(self, field_alias, relate_table, relate_table_field, relate_table_filter_field, filter_sub_level):
        super(RelatedRemoteFieldValue, self).__init__(field_alias, relate_table, relate_table_field, relate_table_filter_field)
        self.filter_sub_level = filter_sub_level


class AbsFilterSubLevel(ABC):
    def __init__(self, required_field_sub_level_table, sub_level_table):
        super(AbsFilterSubLevel, self).__init__()
        self.required_field_sub_level_table = required_field_sub_level_table
        self.sub_level_table = sub_level_table


class FilterSubLevel(AbsFilterSubLevel):
    def __init__(self, required_field_sub_level_table, sub_level_table, filter_field_in_sub_level_table, filter_sub_level=None):
        super(FilterSubLevel, self).__init__(required_field_sub_level_table, sub_level_table)
        self.filter_field_in_sub_level_table = filter_field_in_sub_level_table
        self.filter_sub_level = filter_sub_level


class SpatialFilterSubLevel(AbsFilterSubLevel):
    def __init__(self, required_field_sub_level_table, sub_level_table, level_table, spatial_operation, filter_sub_level=None):
        super(SpatialFilterSubLevel, self).__init__(required_field_sub_level_table, sub_level_table)
        self.level_table = level_table
        self.spatial_operation = spatial_operation
        self.filter_sub_level = filter_sub_level

