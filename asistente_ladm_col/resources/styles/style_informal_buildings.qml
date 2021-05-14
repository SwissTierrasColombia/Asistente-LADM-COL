<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology" version="3.16.6-Hannover">
  <renderer-v2 enableorderby="1" type="RuleRenderer" symbollevels="0" forceraster="0">
    <rules key="{dd852e39-2e1d-4dae-a90a-3f2b45432537}">
      <rule filter="array_find(get_informal_buildings(), t_id) != -1" label="Construcciones informales" key="{fe3ba2a1-6862-4650-bb7d-fd153b1227f2}" symbol="0"/>
      <rule filter="ELSE" label="Construcciones formales" key="{61c68233-d751-4068-88f0-740251e1c3bc}" symbol="1"/>
    </rules>
    <symbols>
      <symbol type="fill" force_rhr="0" clip_to_extent="1" alpha="0.651" name="0">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="207,157,125,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,39,39,255" k="outline_color"/>
          <prop v="dot" k="outline_style"/>
          <prop v="0.8" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol type="fill" force_rhr="0" clip_to_extent="1" alpha="0.651" name="1">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="207,157,125,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="156,156,156,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.26" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
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
    <orderby>
      <orderByClause asc="0" nullsFirst="1">distance(  $geometry,  translate(    @map_extent_center,    1000 * @map_extent_width * cos( radians( @qgis_25d_angle + 180 ) ),    1000 * @map_extent_width * sin( radians( @qgis_25d_angle + 180 ) )  ))</orderByClause>
    </orderby>
  </renderer-v2>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerGeometryType>2</layerGeometryType>
</qgis>
