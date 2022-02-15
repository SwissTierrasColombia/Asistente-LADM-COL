import os.path
import re
import xml.etree.cElementTree as et

from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsVectorLayer,
                       QgsField,
                       QgsFeature)


def get_models_from_xtf(xtf_path):
    """
    Get model names from an XTF file. Since XTF can be very large, we follow this strategy:
    1. Parse line by line.
        1.a. Compare parsed line with the regular expression to get the Header Section.
        1.b. If found, stop parsing the XTF file and go to 2. If not found, append the new line to parsed lines and go
            to next line.
    2. Give the Header Section to an XML parser and extract models. Note that we don't give the full XTF file to the XML
       parser because it will read it completely, which may be not optimal.

    :param xtf_path: Path to an XTF file
    :return: List of model names from the XTF
    """
    model_names = list()
    pattern = re.compile(r'(<HEADERSECTION[^>]*.*</HEADERSECTION>)')

    text_found = "<foo/>"
    with open(xtf_path, 'r') as f:
        lines = ""
        for line in f:
            lines += line
            res = re.search(pattern, lines)
            if res:
                text_found = str(res.groups()[0])
                break

    if text_found:
        root = et.fromstring(text_found)
        element = root.find('MODELS')
        if element:
            for sub_element in element:
                if "NAME" in sub_element.attrib:
                    model_names.append(sub_element.attrib["NAME"])

    return sorted(model_names)


def get_layer_from_xtflog(xtf_path):
    # Parse an XTFLog (which is the result of a --validate operation and follows iliVErrors model).
    # Adapted from
    # https://github.com/GeoWerkstatt/qgis-xtf-log-checker/ (XTFLog_Checker_dialog.py#L75)

    if not os.path.exists(xtf_path):
        return None

    tree = et.parse(xtf_path)  # TODO try except
    root = tree.getroot()

    xtf_layer = QgsVectorLayer("NoGeometry", os.path.basename(xtf_path), "memory")
    provider = xtf_layer.dataProvider()

    # See https://github.com/claeis/ilivalidator/blob/master/docs/IliVErrors.ili
    provider.addAttributes([QgsField("ErrorId", QVariant.String),
                            QgsField("Type", QVariant.String),
                            QgsField("Message", QVariant.String),
                            QgsField("Tid", QVariant.String),
                            QgsField("ObjTag", QVariant.String),
                            QgsField("TechId", QVariant.String),
                            QgsField("UserId", QVariant.String),
                            QgsField("IliQName", QVariant.String),
                            QgsField("DataSource", QVariant.String),
                            QgsField("Line", QVariant.String),
                            QgsField("TechDetails", QVariant.String),
                            QgsField("CoordX", QVariant.Double),
                            QgsField("CoordY", QVariant.Double)])
    xtf_layer.updateFields()

    features = list()

    xmlns = '{http://www.interlis.ch/INTERLIS2.3}'
    for child in root.iter(xmlns + 'IliVErrors.ErrorLog.Error'):
        error_id = child.attrib["TID"]  # Sequential number for records

        attrs_dict = dict()
        for attr in  ["Type", "Message", "Tid", "ObjTag", "TechId", "UserId", "IliQName", "DataSource", "Line", "TechDetails"]:
            element = child.find(xmlns + attr)
            attrs_dict[attr] = element.text if element != None else None

        if not attrs_dict["Tid"]:  # Since we need to identify individual records
            continue

        if attrs_dict["Type"] == 'Error':  # Other values: 'Warning', 'Info', 'DetailInfo'
            feature = QgsFeature()
            attrs = [error_id]
            attrs.extend(list(attrs_dict.values()))

            geometry_element = child.find(xmlns + 'Geometry')
            if geometry_element:
                coords = geometry_element.find(xmlns + 'COORD');
                if coords:
                    x = coords.find(xmlns + 'C1')
                    y = coords.find(xmlns + 'C2')
                    if x is not None and y is not None:
                        attrs.extend([float(x.text), float(y.text)])

            feature.setAttributes(attrs)
            features.append(feature)

    provider.addFeatures(features)

    return xtf_layer
