import sys
import xml.etree.cElementTree as et
import xml.dom.minidom

root=""
def merge(lista, blast, annot):
    root =  et.Element("annotation")
    parse_blast = et.parse(blast).getroot()
    parse_annot = et.parse(annot).getroot()
    for pb in parse_blast:
       name = pb.attrib["id"]
       for pa in parse_annot:
                    if pa.attrib["id"] == name:
                        annot_node_list = [subnode for subnode in pa.getchildren()]
                        for j in annot_node_list:
                            pb.append(j)
       root.append(pb)
    return root
        
if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as lista, open(sys.argv[2]) as blast, open(sys.argv[3]) as annot:
            root = merge(lista, blast, annot)
            stringnewroot = et.tostring(root)
            parsenewroot = xml.dom.minidom.parseString(stringnewroot)
            print parsenewroot.toprettyxml()

    except IOError as e:
            print e.strerror
