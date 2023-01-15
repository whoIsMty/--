import os




def get_kegg_code_protein():
    os.chdir("/usr/local/bio/kobas-3.0/seq_pep")
    code = []
    for root, dirs, files in os.walk(".", topdown=False):
        for file in files:
            if "pep" in file:
                code_ = file.split(".")[0]
                if code_ not in code:
                    code.append(code_)
    os.chdir("/data1/publicshare/")
    f = open("./database_summary/code_list(Protein).txt", "w", encoding="utf-8")
    for code_ in code:
        f.write(code_ + "\n")
    print("KEGG CODE LIST(Protein) WAS CREATED")

def get_taxid_protein():
    os.chdir("/home/bpadmin/PAA/bin/stringdata")
    taxid = []
    for root, dirs, files in os.walk(".", topdown=False):
        for file in files:
            if "protein" in file:
                taxid_ = file.split("protein")[0].split(".")[0]
                if taxid_ not in taxid:
                    taxid.append(taxid_)
    os.chdir("/data1/publicshare")
    f = open("./database_summary/taxid_list.txt", "w", encoding="utf-8")
    for taxid_ in taxid:
        f.write(taxid_ + "\n")
    print("TAXID LIST WAS CREATED")

def get_kegg_code_metabo():
    os.chdir("/home/bpadmin/MetaboBin/keggdb")
    code = []
    for root, dirs, files in os.walk(".", topdown=False):
        for file in files:
            if "cpdlink" in file:
                code_ = file.split(".")[0]
                if code_ not in code:
                    code.append(code_)
    os.chdir("/data1/publicshare/")
    f = open("./database_summary/code_list(Metabo).txt", "w", encoding="utf-8")
    for code_ in code:
        f.write(code_ + "\n")
    print("KEGG CODE LIST(Metabo) WAS CREATED")


if __name__ == '__main__':
    get_kegg_code_protein()
    get_kegg_code_metabo()
    get_taxid_protein()



