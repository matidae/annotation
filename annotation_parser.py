import sys
import xml.etree.cElementTree as et

class CDS():
    def __init__(self, name, match=None):
        self.name = name
        self.match = match

class Entry():
    def  __init__(self, matchType, idn=None, name=None, desc=None, evalue=None, count=None):
        self.matchType = matchType
        self.idn = idn
        self.name = name
        self.desc = desc
        self.evalue = evalue
        self.count = count

root = et.parse(sys.argv[1]).getroot()
cds_matches = []

for node in root:
    name = node.attrib["id"]
    entry = ""
    for sub in node:
        if sub.tag in ["fingerprints", "hmmer3", "hmmer2", "panther", "superfamilyhmmer3"]:
            entry = Entry(sub.tag, idn=sub.attrib["id"], desc=sub.attrib["desc"], evalue=sub.attrib["evalue"])
        elif sub.tag in ["profilescan", "patternscan"]:
            entry = Entry(matchType=sub.tag, idn=sub.attrib["id"], desc=sub.attrib["desc"])
        elif sub.tag in  ["signalp", "phobius"]:
            entry = Entry(matchType=sub.tag, idn=sub.attrib["name"])
        elif sub.tag in ["coils", "tmhmm"]:
            entry = Entry(matchType=sub.tag, count=sub.attrib["count"])
        elif sub.tag == "blastprodom":
            entry = Entry(matchType=sub.tag, idn=sub.attrib["id"], desc=sub.attrib["desc"], evalue=sub.attrib["evalue"])
        else:
            entry = Entry(matchType=sub.tag, idn=sub.attrib["id"], desc=sub.attrib["desc"])
        cds_matches.append(CDS(name, entry))

