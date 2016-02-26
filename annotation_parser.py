import sys
import xml.etree.cElementTree as et

root = et.parse(sys.argv[1]).getroot()
for node in root:
    name = node.attrib["id"]
    for sub in node:
        if sub.tag == "goMF":
            print name, sub.attrib["desc"]
            break

