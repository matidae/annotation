import sys
import xml.etree.cElementTree as et
import xml.dom.minidom

xml_file = et.parse(sys.argv[2]).getroot()
new_xml = et.Element("annotation")

with open(sys.argv[1]) as lista:
    for i in lista:
        name = i.rstrip()
        found = False
        for j in xml_file:
            if j.attrib["id"] == name:
                new_xml.append(j)
                found = True
        if not found:
            et.SubElement(new_xml, "CDS", id=name)

stringnewroot = et.tostring(new_xml)
parsenewroot = xml.dom.minidom.parseString(stringnewroot)
print parsenewroot.toprettyxml()
