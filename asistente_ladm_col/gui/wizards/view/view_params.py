from asistente_ladm_col.gui.wizards.view.view_enum import EnumTypeOfOption


class OptionChangedParams:
    def __init__(self, selected_type: EnumTypeOfOption):
        self.selected_type = selected_type


class FeatureSelectedParams:
    def __init__(self, selected_type: EnumTypeOfOption):
        self.selected_type = selected_type
