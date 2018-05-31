<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" simplifyAlgorithm="0" simplifyLocal="1" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" version="3.1.0-Master" readOnly="0" simplifyDrawingTol="1" simplifyMaxScale="1" maxScale="0" minScale="1e+08">
  <renderer-v2 symbollevels="0" type="singleSymbol" forceraster="0" enableorderby="0">
    <symbols>
      <symbol type="marker" alpha="1" clip_to_extent="1" name="0">
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,236,51,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="triangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="133,133,133,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.4"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2.8"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="86,86,86,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0.5"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="133,133,133,0"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="0.8"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory opacity="1" penWidth="0" maxScaleDenominator="1e+08" barWidth="5" lineSizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up" labelPlacementMethod="XHeight" scaleBasedVisibility="0" height="15" penColor="#000000" enabled="0" scaleDependency="Area" backgroundColor="#ffffff" sizeType="MM" minScaleDenominator="0" width="15" minimumSize="0" backgroundAlpha="255" lineSizeType="MM" penAlpha="255" sizeScale="3x:0,0,0,0,0,0" rotationOffset="270">
      <fontProperties style="" description="Noto Sans,9,-1,5,50,0,0,0,0,0"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" linePlacementFlags="18" placement="0" obstacle="0" priority="0" zIndex="0" showAll="1">
    <properties>
      <Option type="Map">
        <Option type="QString" value="" name="name"/>
        <Option name="properties"/>
        <Option type="QString" value="collection" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <fieldConfiguration>
    <field name="t_id">
      <editWidget type="Hidden">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="nombre_punto">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="exactitud_vertical">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option type="QString" value="1000" name="Max"/>
            <Option type="QString" value="0" name="Min"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="exactitud_horizontal">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option type="QString" value="1000" name="Max"/>
            <Option type="QString" value="0" name="Min"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipo_punto_control">
      <editWidget type="RelationReference">
        <config>
          <Option type="Map">
            <Option type="bool" value="true" name="OrderByValue"/>
            <Option type="QString" value="puntocontrol_tipo_punto_control_col_puntocontroltipo_ilicode" name="Relation"/>
            <Option type="bool" value="false" name="ShowForm"/>
            <Option type="bool" value="false" name="ShowOpenFormButton"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="confiabilidad">
      <editWidget type="CheckBox">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="posicion_interpolacion">
      <editWidget type="RelationReference">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="monumentacion">
      <editWidget type="RelationReference">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="puntotipo">
      <editWidget type="RelationReference">
        <config>
          <Option type="Map">
            <Option type="bool" value="true" name="OrderByValue"/>
            <Option type="QString" value="puntocontrol_puntotipo_la_puntotipo_ilicode" name="Relation"/>
            <Option type="bool" value="false" name="ShowForm"/>
            <Option type="bool" value="false" name="ShowOpenFormButton"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="p_espacio_de_nombres">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="p_local_id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ue_la_unidadespacial">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ue_la_espaciojuridicounidadedificacion">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ue_la_espaciojuridicoredservicios">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ue_servidumbrepaso">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ue_terreno">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ue_unidadconstruccion">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ue_construccion">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="comienzo_vida_util_version">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" value="true" name="calendar_popup"/>
            <Option type="QString" value="M/d/yy h:mm AP" name="display_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="fin_vida_util_version">
      <editWidget type="DateTime">
        <config>
          <Option type="Map">
            <Option type="bool" value="true" name="calendar_popup"/>
            <Option type="QString" value="M/d/yy h:mm AP" name="display_format"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="t_id" name="" index="0"/>
    <alias field="nombre_punto" name="" index="1"/>
    <alias field="exactitud_vertical" name="exactitud_vertical [cm]" index="2"/>
    <alias field="exactitud_horizontal" name="exactitud_horizontal [cm]" index="3"/>
    <alias field="tipo_punto_control" name="" index="4"/>
    <alias field="confiabilidad" name="" index="5"/>
    <alias field="posicion_interpolacion" name="Posicion_Interpolacion" index="6"/>
    <alias field="monumentacion" name="Monumentacion" index="7"/>
    <alias field="puntotipo" name="PuntoTipo" index="8"/>
    <alias field="p_espacio_de_nombres" name="p_Espacio_De_Nombres" index="9"/>
    <alias field="p_local_id" name="p_Local_Id" index="10"/>
    <alias field="ue_la_unidadespacial" name="" index="11"/>
    <alias field="ue_la_espaciojuridicounidadedificacion" name="" index="12"/>
    <alias field="ue_la_espaciojuridicoredservicios" name="" index="13"/>
    <alias field="ue_servidumbrepaso" name="" index="14"/>
    <alias field="ue_terreno" name="" index="15"/>
    <alias field="ue_unidadconstruccion" name="" index="16"/>
    <alias field="ue_construccion" name="" index="17"/>
    <alias field="comienzo_vida_util_version" name="" index="18"/>
    <alias field="fin_vida_util_version" name="" index="19"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="t_id" expression=""/>
    <default applyOnUpdate="0" field="nombre_punto" expression=""/>
    <default applyOnUpdate="0" field="exactitud_vertical" expression=""/>
    <default applyOnUpdate="0" field="exactitud_horizontal" expression=""/>
    <default applyOnUpdate="0" field="tipo_punto_control" expression=""/>
    <default applyOnUpdate="0" field="confiabilidad" expression=""/>
    <default applyOnUpdate="0" field="posicion_interpolacion" expression=""/>
    <default applyOnUpdate="0" field="monumentacion" expression=""/>
    <default applyOnUpdate="0" field="puntotipo" expression=""/>
    <default applyOnUpdate="0" field="p_espacio_de_nombres" expression=""/>
    <default applyOnUpdate="0" field="p_local_id" expression=""/>
    <default applyOnUpdate="0" field="ue_la_unidadespacial" expression=""/>
    <default applyOnUpdate="0" field="ue_la_espaciojuridicounidadedificacion" expression=""/>
    <default applyOnUpdate="0" field="ue_la_espaciojuridicoredservicios" expression=""/>
    <default applyOnUpdate="0" field="ue_servidumbrepaso" expression=""/>
    <default applyOnUpdate="0" field="ue_terreno" expression=""/>
    <default applyOnUpdate="0" field="ue_unidadconstruccion" expression=""/>
    <default applyOnUpdate="0" field="ue_construccion" expression=""/>
    <default applyOnUpdate="1" field="comienzo_vida_util_version" expression="now()"/>
    <default applyOnUpdate="0" field="fin_vida_util_version" expression=""/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" field="t_id" constraints="3" notnull_strength="1" unique_strength="1"/>
    <constraint exp_strength="0" field="nombre_punto" constraints="1" notnull_strength="1" unique_strength="0"/>
    <constraint exp_strength="0" field="exactitud_vertical" constraints="1" notnull_strength="1" unique_strength="0"/>
    <constraint exp_strength="0" field="exactitud_horizontal" constraints="1" notnull_strength="1" unique_strength="0"/>
    <constraint exp_strength="0" field="tipo_punto_control" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="confiabilidad" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="posicion_interpolacion" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="monumentacion" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="puntotipo" constraints="1" notnull_strength="1" unique_strength="0"/>
    <constraint exp_strength="0" field="p_espacio_de_nombres" constraints="1" notnull_strength="1" unique_strength="0"/>
    <constraint exp_strength="0" field="p_local_id" constraints="1" notnull_strength="1" unique_strength="0"/>
    <constraint exp_strength="0" field="ue_la_unidadespacial" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="ue_la_espaciojuridicounidadedificacion" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="ue_la_espaciojuridicoredservicios" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="ue_servidumbrepaso" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="ue_terreno" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="ue_unidadconstruccion" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="ue_construccion" constraints="0" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" field="comienzo_vida_util_version" constraints="1" notnull_strength="1" unique_strength="0"/>
    <constraint exp_strength="0" field="fin_vida_util_version" constraints="0" notnull_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="t_id" desc="" exp=""/>
    <constraint field="nombre_punto" desc="" exp=""/>
    <constraint field="exactitud_vertical" desc="" exp=""/>
    <constraint field="exactitud_horizontal" desc="" exp=""/>
    <constraint field="tipo_punto_control" desc="" exp=""/>
    <constraint field="confiabilidad" desc="" exp=""/>
    <constraint field="posicion_interpolacion" desc="" exp=""/>
    <constraint field="monumentacion" desc="" exp=""/>
    <constraint field="puntotipo" desc="" exp=""/>
    <constraint field="p_espacio_de_nombres" desc="" exp=""/>
    <constraint field="p_local_id" desc="" exp=""/>
    <constraint field="ue_la_unidadespacial" desc="" exp=""/>
    <constraint field="ue_la_espaciojuridicounidadedificacion" desc="" exp=""/>
    <constraint field="ue_la_espaciojuridicoredservicios" desc="" exp=""/>
    <constraint field="ue_servidumbrepaso" desc="" exp=""/>
    <constraint field="ue_terreno" desc="" exp=""/>
    <constraint field="ue_unidadconstruccion" desc="" exp=""/>
    <constraint field="ue_construccion" desc="" exp=""/>
    <constraint field="comienzo_vida_util_version" desc="" exp=""/>
    <constraint field="fin_vida_util_version" desc="" exp=""/>
  </constraintExpressions>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column type="field" width="-1" hidden="0" name="t_id"/>
      <column type="field" width="-1" hidden="0" name="nombre_punto"/>
      <column type="field" width="-1" hidden="0" name="exactitud_vertical"/>
      <column type="field" width="-1" hidden="0" name="exactitud_horizontal"/>
      <column type="field" width="-1" hidden="0" name="tipo_punto_control"/>
      <column type="field" width="-1" hidden="0" name="confiabilidad"/>
      <column type="field" width="-1" hidden="0" name="posicion_interpolacion"/>
      <column type="field" width="-1" hidden="0" name="monumentacion"/>
      <column type="field" width="-1" hidden="0" name="puntotipo"/>
      <column type="field" width="-1" hidden="0" name="p_espacio_de_nombres"/>
      <column type="field" width="-1" hidden="0" name="p_local_id"/>
      <column type="field" width="-1" hidden="0" name="ue_la_unidadespacial"/>
      <column type="field" width="-1" hidden="0" name="ue_la_espaciojuridicounidadedificacion"/>
      <column type="field" width="-1" hidden="0" name="ue_la_espaciojuridicoredservicios"/>
      <column type="field" width="-1" hidden="0" name="ue_servidumbrepaso"/>
      <column type="field" width="-1" hidden="0" name="ue_terreno"/>
      <column type="field" width="-1" hidden="0" name="ue_unidadconstruccion"/>
      <column type="field" width="-1" hidden="0" name="ue_construccion"/>
      <column type="field" width="-1" hidden="0" name="comienzo_vida_util_version"/>
      <column type="field" width="-1" hidden="0" name="fin_vida_util_version"/>
      <column type="actions" width="-1" hidden="1"/>
    </columns>
  </attributetableconfig>
  <editform></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer groupBox="0" columnCount="2" visibilityExpressionEnabled="0" visibilityExpression="" name="General" showLabel="1">
      <attributeEditorField name="nombre_punto" showLabel="1" index="1"/>
      <attributeEditorField name="exactitud_vertical" showLabel="1" index="2"/>
      <attributeEditorField name="exactitud_horizontal" showLabel="1" index="3"/>
      <attributeEditorField name="tipo_punto_control" showLabel="1" index="4"/>
      <attributeEditorField name="confiabilidad" showLabel="1" index="5"/>
      <attributeEditorField name="posicion_interpolacion" showLabel="1" index="6"/>
      <attributeEditorField name="monumentacion" showLabel="1" index="7"/>
      <attributeEditorField name="puntotipo" showLabel="1" index="8"/>
      <attributeEditorField name="p_espacio_de_nombres" showLabel="1" index="9"/>
      <attributeEditorField name="p_local_id" showLabel="1" index="10"/>
      <attributeEditorField name="ue_la_unidadespacial" showLabel="1" index="11"/>
      <attributeEditorField name="ue_la_espaciojuridicounidadedificacion" showLabel="1" index="12"/>
      <attributeEditorField name="ue_la_espaciojuridicoredservicios" showLabel="1" index="13"/>
      <attributeEditorField name="ue_servidumbrepaso" showLabel="1" index="14"/>
      <attributeEditorField name="ue_terreno" showLabel="1" index="15"/>
      <attributeEditorField name="ue_unidadconstruccion" showLabel="1" index="16"/>
      <attributeEditorField name="ue_construccion" showLabel="1" index="17"/>
      <attributeEditorField name="comienzo_vida_util_version" showLabel="1" index="18"/>
      <attributeEditorField name="fin_vida_util_version" showLabel="1" index="19"/>
      <attributeEditorField name="localizacion_original" showLabel="1" index="-1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="comienzo_vida_util_version" editable="1"/>
    <field name="confiabilidad" editable="1"/>
    <field name="exactitud_horizontal" editable="1"/>
    <field name="exactitud_vertical" editable="1"/>
    <field name="fin_vida_util_version" editable="1"/>
    <field name="monumentacion" editable="1"/>
    <field name="nombre_punto" editable="1"/>
    <field name="p_espacio_de_nombres" editable="1"/>
    <field name="p_local_id" editable="1"/>
    <field name="posicion_interpolacion" editable="1"/>
    <field name="puntotipo" editable="1"/>
    <field name="t_id" editable="1"/>
    <field name="tipo_punto_control" editable="1"/>
    <field name="ue_construccion" editable="1"/>
    <field name="ue_la_espaciojuridicoredservicios" editable="1"/>
    <field name="ue_la_espaciojuridicounidadedificacion" editable="1"/>
    <field name="ue_la_unidadespacial" editable="1"/>
    <field name="ue_servidumbrepaso" editable="1"/>
    <field name="ue_terreno" editable="1"/>
    <field name="ue_unidadconstruccion" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="comienzo_vida_util_version"/>
    <field labelOnTop="0" name="confiabilidad"/>
    <field labelOnTop="0" name="exactitud_horizontal"/>
    <field labelOnTop="0" name="exactitud_vertical"/>
    <field labelOnTop="0" name="fin_vida_util_version"/>
    <field labelOnTop="0" name="monumentacion"/>
    <field labelOnTop="0" name="nombre_punto"/>
    <field labelOnTop="0" name="p_espacio_de_nombres"/>
    <field labelOnTop="0" name="p_local_id"/>
    <field labelOnTop="0" name="posicion_interpolacion"/>
    <field labelOnTop="0" name="puntotipo"/>
    <field labelOnTop="0" name="t_id"/>
    <field labelOnTop="0" name="tipo_punto_control"/>
    <field labelOnTop="0" name="ue_construccion"/>
    <field labelOnTop="0" name="ue_la_espaciojuridicoredservicios"/>
    <field labelOnTop="0" name="ue_la_espaciojuridicounidadedificacion"/>
    <field labelOnTop="0" name="ue_la_unidadespacial"/>
    <field labelOnTop="0" name="ue_servidumbrepaso"/>
    <field labelOnTop="0" name="ue_terreno"/>
    <field labelOnTop="0" name="ue_unidadconstruccion"/>
  </labelOnTop>
  <widgets/>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <expressionfields/>
  <previewExpression>t_id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
