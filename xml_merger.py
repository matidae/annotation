import sys
import xml.etree.cElementTree as et
import xml.dom.minidom

rooot=""
def merge(lista, blast, annot):
    root =  et.Element("annotation")
    parse_blast = et.parse(blast).getroot()
    parse_annot = et.parse(annot).getroot()

    for i in lista:
        name = i.strip()
        blast_node = ""
        annot_node_list = []
        for node in parse_blast:
            if node.attrib["id"] == name:
                #blast_node == node    
                blast_node = root.subElement(node)
                for node2 in parse_annot:
                    if node2.attrib["id"] == name:
                        #annot_node_list == [subnode for subnode in node.getchildren()]
                        print node
        
        
if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as lista, open(sys.argv[2]) as blast, open(sys.argv[3]) as annot:
            merge(lista, blast, annot)
            stringnewroot = et.tostring(root)
            parsenewroot = xml.dom.minidom.parseString(stringnewroot)
            print parsenewroot.toprettyxml()

    except IOError as e:
            print e.strerror
