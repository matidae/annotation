import sys
import argparse
import xml.etree.cElementTree as et

class CDS():
    def __init__(self, name, matches=None):
        self.name = name
        self.matches = matches

class Entry():
    def  __init__(self, matchType, idn=None, name=None, desc=None, evalue=None, count=None):
        self.matchType = matchType
        self.idn = idn
        self.name = name
        self.desc = desc
        self.evalue = evalue
        self.count = count

def loadXML(xml):
    cds_all = []
    root = et.parse(xml).getroot()
    for node in root:
        name = node.attrib["id"]
        cds = CDS(name)
        cds_matches = []
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
            cds_matches.append(entry)
        cds.matches = cds_matches
        cds_all.append(cds)
    return cds_all

def parse_args():
    parser = argparse.ArgumentParser(description="Filter annotation") 
    parser.add_argument("-i", dest="filename",
                        help="XML file")
    parser.add_argument("-d", dest ="db",
                        help="Show dbs annotation")
    parser.add_argument("-all", action='store_true',
                        help="Show all annotations")
    return parser.parse_args()


def main(cds_all):
    match_list = parse_args().db.split(",")
    dbs =["fingerprints", "hmmer3", "hmmer2", "panther", "superfamilyhmmer3","profilescan", "patternscan","signalp", "phobius","coils", "tmhmm","blastprodom","goMF", "goCC", "goBP"]
    for cds in cds_all:
        name = cds.name
        line = ""
        if parse_args().all:
            for entry in cds.matches:
                line += entry.matchType + ":" +entry.idn + ":" + entry.desc.replace(" ","_") + "; "
        elif len(match_list) > 0:
            for i in match_list:
                if i not in dbs:
                    print "Wrong db: " + i
                    sys.exit()
            for entry in cds.matches:
                if entry.matchType in match_list:
                    line += entry.matchType + "=" +entry.idn + ":" + entry.desc.replace(" ","_") + "; "
        else:
            parse.print_help()
        if line:
            print name, line

if __name__ == "__main__":
    cds_all = []
    with open(parse_args().filename) as xml:
        cds_all = loadXML(xml)
    main(cds_all)
            
