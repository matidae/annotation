import sys
import xml.etree.cElementTree as et
import xml.dom.minidom

class Entry():
    def  __init__(self, matchType, idn=None, name=None, desc=None, evalue=None):
        self.matchType = matchType
        self.idn = idn
        self.name = name
        self.desc = desc
        self.evalue = evalue


def genericEntry(node, matchType):
    desc = ""
    evalue = ""
    idn = ""
    if "ac" in node[0].getchildren()[0].attrib:
        idn = node[0].getchildren()[0].attrib["ac"]
    elif "ac" in node.attrib:
        idn = node.getchildren()[0].attrib["ac"]
    if "evalue" in node.attrib:
        evalue = node.attrib["evalue"]
    if "desc" in node[0].getchildren()[0].attrib:
        desc = node[0].getchildren()[0].attrib["desc"]
    elif "name" in node[0].getchildren()[0].attrib:
        desc = node[0].getchildren()[0].attrib["name"]
    if desc != "" and "NOT NAMED" not in desc:
        return Entry(matchType, idn=idn, desc=desc, evalue=evalue)
    else:
        return None

def basicEntry(node, matchType):
    name = ""
    for n in node:
        if "signature" in n.tag:
            if "name" in n.attrib:
                name = n.attrib["name"]
            elif "ac" in n.attrib:
                name = n.attrib["ac"]
    return Entry(matchType, name=name)


def getTerms(node):
    term_list = []
    for child in entry:
        if "category" in child.attrib:
            db = "".join([i[0] for i in child.attrib["category"].split("_")])
            term = Entry("go" + db, idn = child.attrib["id"], desc = child.attrib["name"])
        else:
            term = Entry(child.attrib["db"].lower(), idn = child.attrib["id"], desc = child.attrib["name"])
        term_list.append(term)
    return term_list

def cleanList(matches_list):
    ids = []
    new_list = []
    sorted_list = sorted(matches_list, key=lambda x:x.matchType)
    for i in sorted_list:
        if i.idn not in ids:
            new_list.append(i)
            ids.append(i.idn)
    return new_list

def printNode(cds_node, matches_list):
    new_list = cleanList(matches_list)
    for i in new_list:
        if i.matchType in ["fingerprints", "hmmer3", "hmmer2", "panther", "superfamilyhmmer3"]:
            et.SubElement(cds_node, i.matchType, id = i.idn, desc = i.desc, evalue = i.evalue) 
        elif i.matchType in ["profilescan", "patternscan"]:
            et.SubElement(cds_node, i.matchType, id = i.idn, desc = i.desc) 
        elif i.matchType == "blastprodom":
            et.SubElement(cds_node, i.matchType, id = i.idn, desc = i.desc, evalue = i.evalue) 
        elif i.matchType in ["signalp", "phobius"]:
            et.SubElement(cds_node, i.matchType, name = i.name) 
        elif i.matchType in ["coils", "tmhmm"]:
            et.SubElement(cds_node, i.matchType, count = i.name) 
        else:
            et.SubElement(cds_node, i.matchType, id = i.idn, desc = i.desc) 

#starting point
root = et.parse(sys.argv[1]).getroot()
newroot = et.Element("annotation")

for node in root:
    protein = node.getchildren()
    sequence = protein[0].text
    cds_idn = protein[1].attrib['id']
    matches = protein[2].getchildren()
    cds_node = et.SubElement(newroot, "CDS", id = cds_idn)
    coilCounter = 0
    tmCounter = 0
    matches_list = []
    for hit in matches:
        matchType = hit.tag.split("}")[1].split("-")[0] 
        if matchType == "blastprodom":
            desc = hit.getchildren()[0].attrib["desc"]
            idn = hit.getchildren()[0].attrib["ac"]
            entry = hit.getchildren()[0].getchildren()[0]
            evalue = hit.getchildren()[1].getchildren()[0].attrib["evalue"]
            if "entry" in entry.tag:
                desc = entry.attrib["desc"]
                idn = entry.attrib["ac"]
                terms = getTerms(hit)
                matches_list += terms
            matches_list.append(Entry(matchType, idn = idn, desc = desc, evalue = evalue))
        if matchType in ["fingerprints", "hmmer3", "hmmer2", "panther", "superfamilyhmmer3"]:
            gentry = genericEntry(hit, matchType)
            if gentry:
                matches_list.append(gentry)
            entry = hit.getchildren()[0].getchildren()[0]
            if "entry" in entry.tag:
                terms = getTerms(hit)
                matches_list += terms
        if matchType in ["coils", "tmhmm"]:
            for n in hit:
                if "locations" in n.tag:
                    if int(n[0].attrib["end"]) - int(n[0].attrib["start"]) > 10:
                        if matchType == "coils":
                            coilCounter += 1
                        else:
                            tmCounter += 1
        if matchType in ["signalp", "phobius"]:
            bentry = basicEntry(hit, matchType)
            matches_list.append(bentry)
        if matchType in ["profilescan", "patternscan"]:
            desc = hit.getchildren()[0].attrib["desc"]
            idn = hit.getchildren()[0].attrib["ac"]
            entry = hit.getchildren()[0].getchildren()[0]
            if "entry" in entry.tag:
                desc = entry.attrib["desc"]
                idn = entry.attrib["ac"]
                terms = getTerms(hit)
                matches_list += terms
            matches_list.append(Entry(matchType, idn=idn, desc=desc))
            entry = hit.getchildren()[0].getchildren()[0]
            if "entry" in entry.tag:
                terms = getTerms(hit)
                matches_list += terms
    if coilCounter > 0:
        matches_list.append(Entry("coils", name = str(coilCounter)))
    if tmCounter > 0:
        matches_list.append(Entry("tmhmm", name = str(tmCounter)))
    printNode(cds_node, matches_list)

stringnewroot = et.tostring(newroot)
parsenewroot = xml.dom.minidom.parseString(stringnewroot)
print parsenewroot.toprettyxml()
