#!/bin/python3
import argparse
import os
import sys
import re


def by_taxid(taxid):
    global p, pwd
    w = open(os.path.join(pwd, p.prefix + f".{taxid}.gomaping.txt"), "w", encoding="utf-8")
    # w.write("Accession\tGo\n")
    db = open(p.db_file, "r")
    result = dict()
    count = 0
    while True:
        line = db.readline()
        count +=1
        if count <=9:
            continue
        else:
            if line:
                if count%100000000 == 0 :
                    print(count,"行 ")
                line_list = line.strip().split("\t")
              #   print(line_list)
                taxid_ = line_list[12].split(":")[1].strip()
                if taxid_ == taxid:
                    accession = line_list[1]
                    go = line_list[4]
                    if accession not in result:
                        result[accession] = [go]
                    else:
                        result[accession].append(go)
            else:
                break
    for key, value in result.items():
        w.write(key + "\t" + ",".join(set(value)) + "\n")

    print("提取完成！")


def by_list():
    global p, pwd
    w = open(os.path.join(pwd, p.prefix + f".gomaping.txt"), "w", encoding="utf-8")
    db = open(p.db_file, "r")
    list_file = os.path.join(pwd,p.list_file)
    acc_list = [ line.strip for line in open(list_file,"r",encoding="utf-8").readlines() if line.strip() != ""]
    print(f"已经提取到List File中的{len(acc_list)}个accssionID")
    result = dict()
    count = 0
    while True:
        line = db.readline()
        count +=1
        if count <=9:
            continue
        else:
            if line:

                if count%100000000 == 0 :
                    print(count,"行 ")
                line_list = line.strip().split("\t")
                accession = line_list[1]
                print(accession)
                if accession in acc_list:
                    go = line_list[4]
                    if accession not in result:
                        result[accession] = [go]
                    else:
                        result[accession].append(go)
            else:
                break
    for key, value in result.items():
        w.write(key + "\t" + ",".join(set(value)) + "\n")
    print("提取完成！")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="用于从总的Go注释表中提取GO注释生成Go mapping文件。\n一共有三种功能。1、通过一个List。2.通过FASTA文件。3.通过Taxid。", )
    parser.add_argument("-taxid", action="store", default=None, dest="taxid", help="需要提取Go mapping的物种的Taxonomy ID",
                        required=False)
    parser.add_argument("-list", action="store", default=None, dest="list_file", help="需要提取的Accession List",
                        required=False)
    parser.add_argument("-prefix", action="store", default="db", dest="prefix",
                        help="输出文件前缀。生成prefix.gomapping.txt", required=True)
    # parser.add_argument("-fasta", action="store", default=None, dest="fasta_file",help="通过从FASTA文件中提取AccessionList并且得到gomapping.txt", required=True)
    parser.add_argument("-db", action="store", default="/data1/database/GO/goa_uniprot_all.gaf", dest="db_file",
                        help="总的Go数据库的绝对路径。有默认值。/data1/database/GO/goa_uniprot_all.gaf")

    p = parser.parse_args()
    pwd = os.getcwd()

    if p.taxid == "":
        parser.print_help()
        sys.exit(1)

    if p.taxid is not None:
        by_taxid(p.taxid)
    elif p.list_file is not None:
        by_list()
