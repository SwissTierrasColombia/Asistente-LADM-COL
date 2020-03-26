import re
import xml.etree.cElementTree as et


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
            for sub_element in element.getchildren():
                if "NAME" in sub_element.attrib:
                    model_names.append(sub_element.attrib["NAME"])

    return sorted(model_names)