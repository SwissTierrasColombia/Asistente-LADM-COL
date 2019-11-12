<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyDrawingHints="1" readOnly="0" simplifyMaxScale="1" simplifyLocal="1" version="3.1.0-Master" hasScaleBasedVisibilityFlag="0" simplifyAlgorithm="0" simplifyDrawingTol="1" maxScale="0" labelsEnabled="0" minScale="1e+08">
  <renderer-v2 type="25dRenderer">
    <symbol clip_to_extent="1" type="fill" alpha="1" name="symbol">
      <layer pass="0" class="SimpleFill" enabled="1" locked="1">
        <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
        <prop v="0,0,255,255" k="color"/>
        <prop v="bevel" k="joinstyle"/>
        <prop v="0,0" k="offset"/>
        <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
        <prop v="MM" k="offset_unit"/>
        <prop v="35,35,35,255" k="outline_color"/>
        <prop v="solid" k="outline_style"/>
        <prop v="0.26" k="outline_width"/>
        <prop v="MM" k="outline_width_unit"/>
        <prop v="solid" k="style"/>
        <effect type="effectStack" enabled="1">
          <effect type="outerGlow">
            <prop v="0" k="blend_mode"/>
            <prop v="5" k="blur_level"/>
            <prop v="0,0,255,255" k="color1"/>
            <prop v="0,255,0,255" k="color2"/>
            <prop v="0" k="color_type"/>
            <prop v="0" k="discrete"/>
            <prop v="2" k="draw_mode"/>
            <prop v="0" k="enabled"/>
            <prop v="0.5" k="opacity"/>
            <prop v="gradient" k="rampType"/>
            <prop v="17,17,17,255" k="single_color"/>
            <prop v="4" k="spread"/>
            <prop v="MapUnit" k="spread_unit"/>
            <prop v="3x:0,0,0,0,0,0" k="spread_unit_scale"/>
          </effect>
        </effect>
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
      </layer>
      <layer pass="0" class="GeometryGenerator" enabled="1" locked="0">
        <prop v="Fill" k="SymbolType"/>
        <prop v="order_parts(   extrude(    segments_to_lines( $geometry ),    cos( radians( eval( @qgis_25d_angle ) ) ) * eval( @qgis_25d_height ),    sin( radians( eval( @qgis_25d_angle ) ) ) * eval( @qgis_25d_height )  ),  'distance(  $geometry,  translate(    @map_extent_center,    1000 * @map_extent_width * cos( radians( @qgis_25d_angle + 180 ) ),    1000 * @map_extent_width * sin( radians( @qgis_25d_angle + 180 ) )  ))',  False)" k="geometryModifier"/>
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <symbol clip_to_extent="1" type="fill" alpha="1" name="@symbol@1">
          <layer pass="0" class="SimpleFill" enabled="1" locked="0">
            <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
            <prop v="119,119,119,255" k="color"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="0,0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="119,119,119,255" k="outline_color"/>
            <prop v="solid" k="outline_style"/>
            <prop v="0.26" k="outline_width"/>
            <prop v="MM" k="outline_width_unit"/>
            <prop v="solid" k="style"/>
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option type="Map" name="properties">
                  <Option type="Map" name="fillColor">
                    <Option value="true" type="bool" name="active"/>
                    <Option value="set_color_part(   @symbol_color, 'value',  40 + 19 * abs( $pi - azimuth(     point_n( geometry_n($geometry, @geometry_part_num) , 1 ),     point_n( geometry_n($geometry, @geometry_part_num) , 2 )  ) ) )" type="QString" name="expression"/>
                    <Option value="3" type="int" name="type"/>
                  </Option>
                </Option>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </layer>
      <layer pass="0" class="GeometryGenerator" enabled="1" locked="0">
        <prop v="Fill" k="SymbolType"/>
        <prop v="translate(  $geometry,  cos( radians( eval( @qgis_25d_angle ) ) ) * eval( @qgis_25d_height ),  sin( radians( eval( @qgis_25d_angle ) ) ) * eval( @qgis_25d_height ))" k="geometryModifier"/>
        <data_defined_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </data_defined_properties>
        <symbol clip_to_extent="1" type="fill" alpha="1" name="@symbol@2">
          <layer pass="0" class="SimpleFill" enabled="1" locked="0">
            <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
            <prop v="207,157,125,255" k="color"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="0,0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="207,157,125,255" k="outline_color"/>
            <prop v="solid" k="outline_style"/>
            <prop v="0.26" k="outline_width"/>
            <prop v="MM" k="outline_width_unit"/>
            <prop v="solid" k="style"/>
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </layer>
    </symbol>
  </renderer-v2>
</qgis>
