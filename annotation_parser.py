import sys
import argparse
import xml.etree.cElementTree as et

class CDS():
    def __init__(self, name, matches=None):
        self.name = name
        self.matches = matches

class Blast():
    def __init__(self, matchType, desc, evalue, sp):
        self.matchType = matchType
        self.desc = desc
        self.evalue = evalue
        self.sp = sp

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
            if "blast_hit" in sub.tag:
                entry = Blast(sub.tag, desc=sub.attrib["desc"], evalue=sub.attrib["evalue"], sp=sub.attrib["sp"])
            elif sub.tag in ["fingerprints", "hmmer3", "hmmer2", "panther", "superfamilyhmmer3"]:
                entry = Entry(sub.tag, idn=sub.attrib["id"], desc=sub.attrib["desc"], evalue=sub.attrib["evalue"])
            elif sub.tag in ["profilescan", "patternscan"]:
                entry = Entry(matchType=sub.tag, idn=sub.attrib["id"], desc=sub.attrib["desc"])
            elif sub.tag in  ["signalp", "phobius"]:
                entry = Entry(matchType=sub.tag, name=sub.attrib["name"])
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
    parser.add_argument("-in", dest="filename",
                        help="XML input file")
    parser.add_argument("-db", dest ="db",
                        help="Show annotations of selected databases. Possible dbs: fingerprints, hmmer3, hmmer2, panther, superfamilyhmmer3, profilescan, patternscan, signalp, phobius, tmhmm, blastprodom, goMF, goCC, goBP, kegg, unipathway, reactome, metacyc, coils, blast_hit_(0-3)")
    parser.add_argument("-all", action='store_true',
                        help="Show annotations from all databases")
    parser.add_argument("-na", action='store_true',
                        help="Show also tn names of CDS without annotation")
    return parser.parse_args()

def check_args():
    dbs = ["fingerprints", "hmmer3", "hmmer2", "panther", "superfamilyhmmer3","profilescan", "patternscan","signalp", "phobius", "tmhmm","blastprodom","goMF", "goCC", "goBP", "kegg", "unipathway", "reactome", "metacyc", "coils", "blast_hit_0", "blast_hit_1", "blast_hit_2", "blast_hit_3"]
    if parse_args().all:
        return dbs
    elif parse_args().db:
        match_list = []
        for i in parse_args().db.split(","):
            if "blast_hit" in parse_args().db:
                match_list+=["blast_hit_0", "blast_hit_1", "blast_hit_2", "blast_hit_3"]
            else:
                if i in dbs:
                    match_list.append(i)
                else:
                    print "Wrong database: " + i
                    show_dbs = dbs[:-4]
                    show_dbs.append("blast_hit")
                    print "Databases are: \n" + ", ".join(show_dbs)
                    sys.exit()
        return match_list 
    else:
        parse.print_help()
        
def main(cds_all, dbs_sel):
    dbs = ["fingerprints", "hmmer3", "hmmer2", "panther", "superfamilyhmmer3","profilescan", "patternscan","signalp", "phobius", "tmhmm","blastprodom","goMF", "goCC", "goBP", "kegg", "unipathway", "reactome", "metacyc", "coils", "blast_hit"]
    for cds in cds_all:
        name = cds.name
        line = ""
        for entry in cds.matches:
            if entry.matchType in dbs_sel:
                if entry.matchType in ["fingerprints", "hmmer3", "hmmer2", "panther", "superfamilyhmmer3", "blastprodom"]:
                    line += entry.matchType + ":" + entry.idn + ":" + entry.desc.replace(" ","_") + ":" + entry.evalue + "; "
                elif entry.matchType in ["profilescan", "patternscan", "goMF", "goBP", "goCC","kegg", "unipathway", "reactome", "metacyc"]:
                    line += entry.matchType + ":" + entry.idn + ":" + entry.desc.replace(" ","_") + "; "
                elif entry.matchType[:-2] == "blast_hit":
                    line += entry.matchType + ":" + entry.desc.replace(" ","_") + ":" + entry.evalue + ":" + entry.sp.replace(" ","_") + "; "
                elif entry.matchType in ["coils", "tmhmm"]:
                    line += entry.matchType + ":" + entry.count + "; "
                elif entry.matchType in ["signalp", "phobius"]:
                    line += entry.matchType + ":" + entry.name.replace(" ","_") + "; "
        na = parse_args().na
        if line:
            print name, line
        elif na:
            print name, "NA"

if __name__ == "__main__":
    cds_all = []
    with open(parse_args().filename) as xml:
        cds_all = loadXML(xml)
    dbs_sel = check_args()
    main(cds_all, dbs_sel)
            
