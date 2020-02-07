from abc import ABC


class AbsFieldGenericQuery(ABC):
    def __init__(self, field_alias):
        super(AbsFieldGenericQuery, self).__init__()
        self.field_alias = field_alias


class OwnField(AbsFieldGenericQuery):
    def __init__(self, field_name, field_alias):
        super(OwnField, self).__init__(field_alias)
        self.field_name = field_name


class DomainOwnField(OwnField):
    def __init__(self, field_name, field_alias, domain_table):
        super(DomainOwnField, self).__init__(field_name, field_alias)
        self.domain_table = domain_table


class RelateField(AbsFieldGenericQuery):
    def __init__(self, field_alias, relate_table, relate_table_fields, relate_table_filter_field):
        super(RelateField, self).__init__(field_alias)
        self.relate_table = relate_table
        self.relate_table_fields = relate_table_fields
        self.relate_table_filter_field = relate_table_filter_field


class FilterSubLevel:
    def __init__(self, required_field_sub_level_table, sub_level_table, filter_field_in_sub_level_table):
        self.required_field_sub_level_table  = required_field_sub_level_table
        self.sub_level_table = sub_level_table
        self.filter_field_in_sub_level_table = filter_field_in_sub_level_table
