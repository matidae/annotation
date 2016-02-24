import sys
import xml.etree.cElementTree as et
import xml.dom.minidom
root = et.parse(sys.argv[1]).getroot()
newroot = et.Element("annotation")

def genericEntry(node):
    db = node.tag.split("}")[1].split("-")[0]
    desc = ""
    evalue = ""
    if "evalue" in  node.attrib:
        evalue = node.attrib["evalue"]
    for n in node:
        if "signature" in n.tag:
            if "desc" in n.attrib:
                desc = n.attrib["desc"]
            elif "entry" in n[0].tag:
                desc = n[0].attrib["desc"]
            elif "name" in n.attrib:
                desc = n.attrib["name"]
    if desc != "":
        return [db, desc, evalue]
    else:
        return None
def getGOs(node):
    pass

for node in root:
    protein = node.getchildren()
    sequence = protein[0].text
    idn = protein[1].attrib['id']
#    cds = et.SubElement(newroot, "CDS", id = idn)
    matches = protein[2].getchildren()
    cds = et.SubElement(newroot, "CDS", id = idn)
    coilCounter = 0
    for hit in matches:
        matchType = hit.tag.split("}")[1].split("-")[0] 
        if matchType == "blastprodom":
            for n in hit:
                if "signature" in n.tag:
                    ac = n.attrib["ac"]
                    desc = n.attrib["desc"].replace(" ","_")
                elif "locations" in n.tag:
                    evalue = n[0].attrib["evalue"]
                    elem = et.SubElement(cds, "prodom", desc = desc, evalue = evalue)
        if matchType == "coils":
            for n in hit:
                if "locations" in n.tag:
                    if int(n[0].attrib["end"]) - int(n[0].attrib["start"]) > 10:
                        coilCounter +=1
        if matchType in ["fingerprints", "hmmer3", "hmmer2", "panther", "superfamilyhmmer3"]:
            data = genericEntry(hit)
            entry = hit.getchildren()[0].getchildren()[0]
            goBP = []
            goMF = []
            kegg = meta = uni = rea = []
            if "entry" in entry.tag:
                for child in entry:
                    if "category" in child.attrib:
                        if child.attrib["category"] == "BIOLOGICAL_PROCESS":
                            goBP = [child.attrib["id"], child.attrib["name"]]
                        if child.attrib["category"] == "MOLECULAR_FUNCTION":
                            goMF = [child.attrib["id"], child.attrib["name"]]
                    else:
                        if child.attrib["db"] == "KEGG":
                            kegg = [child.attrib["id"], child.attrib["name"]]
                        if child.attrib["db"] == "MetaCyc":
                            meta = [child.attrib["id"], child.attrib["name"]]
                        if child.attrib["db"] == "UniPathway":
                            uni = [child.attrib["id"], child.attrib["name"]]
                        if child.attrib["db"] == "Reactome":
                            rea = [child.attrib["id"], child.attrib["name"]]
            if data:
                elem = et.SubElement(cds, data[0], desc = data[1], evalue = data[2])
            if goBP:
                elem = et.SubElement(cds, "goBP", id = goBP[0], desc = goBP[1])
            if goMF:
                elem = et.SubElement(cds, "goMF", id = goMF[0], desc = goMF[1])
            if kegg:
                elem = et.SubElement(cds, "kegg", id = kegg[0], desc = kegg[1])
            if meta:
                elem = et.SubElement(cds, "metacyc", id = meta[0], desc = meta[1])
            if uni:
                elem = et.SubElement(cds, "unipathway", id = uni[0], desc = uni[1])
            if rea:
                elem = et.SubElement(cds, "reactome", id = rea[0], desc = rea[1])
    if coilCounter > 0:
        elem = et.SubElement(cds, "coils", n = str(coilCounter))
 
stringnewroot = et.tostring(newroot)
parsenewroot = xml.dom.minidom.parseString(stringnewroot)
print parsenewroot.toprettyxml()

