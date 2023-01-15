import re


def get_fasta_description(path = ""):
    with open(path,"r") as f:
        first_line=f.readlines()[0].strip()
        if len(re.findall(r'>.*\|(.*)\|',first_line)) != 0 :
            return "Uniprot_identifier" 
        elif len(re.findall(r'>(gi\|[0-9]*)',first_line)) !=0 :
            return "NCBI_accession"
        elif len(re.findall(r'IPI:([^\|.]*)',first_line)) !=0:
            return "IPI_accession"
        elif len(re.findall(r'>([^ ]*)',first_line)) != 0 :
            return "Up_to_firt_space"
        elif len(re.findall(r'>([^\t]*)',first_line)) != 0 :
            return "Up_to_first_tab_character"
        else:
            return "Everything_after_'>'"
if __name__ == "__main__":
    path = r"C:\Users\Leo\Desktop\outseq.txt"
    fasta_description = get_fasta_description(path)
    print(fasta_description)
    