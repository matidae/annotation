import sys
import xml.etree.cElementTree as et
import xml.dom.minidom

file_cds = sys.argv[1]
file_blast = sys.argv[2]
newroot = et.Element("annotation")

with open(file_cds) as fcds:
    for i in fcds:
        name = i.rstrip()
        count = 0
        repe = []
        with open(file_blast) as fblast:
            for j in fblast:
                if name == j.split()[0]:            
                    desc = j.replace(" ", "_").split()[15].split("[")[0]
                    idn = j.split()[2]
                    cov = j.split()[13]
                    evalue = j.split()[10]
                    species = "NA"
                    if len(j.replace(" ", "_").split()[15].split("[")) > 1:
                        species = j.replace(" ", "_").split()[15].split("[")[1].replace("]", "")
                    if count == 0:
                        cds_node = et.SubElement(newroot, "CDS", id = name)
                        et.SubElement(cds_node, "blast_hit_"+str(count), desc = desc.replace("_"," ").strip(), evalue = evalue, sp = species.replace("_"," "))
                        count += 1
                    elif count < 4:
                        if "hypothetical" not in desc.lower() and "unnamed" not in desc.lower() and "unknown" not in desc.lower() and "unspecified" not in desc.lower():
                            main_desc = desc.split("[")[0].lower().replace(",_putative_","_").replace("_1","")
                            if main_desc not in repe:
                                repe.append(main_desc)
                                et.SubElement(cds_node, "blast_hit_"+str(count), desc = desc.replace("_"," ").strip(), evalue = evalue, sp = species.replace("_"," "))
                                count += 1

stringnewroot = et.tostring(newroot)
parsenewroot = xml.dom.minidom.parseString(stringnewroot)
print parsenewroot.toprettyxml()

