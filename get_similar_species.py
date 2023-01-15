#!/usr/bin/python3
import os
import argparse


def get_taxid_no3(path):
    result = []
    with open(path, "r") as p:
        content = p.readlines()
        for line in content:
            taxid = line.strip().split("\t")[1].split(".")[0]
            result.append(int(taxid.replace(" ", "")))
    set01 = set(result)
    dict01 = {item: result.count(item) for item in set01}
    list_ = [[0, 0], [0, 0], [0, 0]]
    for key, value in dict01.items():
        if value > list_[0][1]:
            list_[0] = [key, value]
        elif value > list_[1][1]:
            list_[1] = [key, value]
        elif value > list_[2][1]:
            list_[2] = [key, value]
    return list_  # 返回一个列表，是前三的taxid和出现次数。


def get_name(taxid=[], path=""):
    # 解析speices

    with open(path, "r") as p:
        for line in p.readlines()[1:]:
            taxid_ = int(line.strip().split("\t")[0])
            NCBI_name = line.strip().split("\t")[3]
            if taxid[0][0] == taxid_:
                taxid[0].append(NCBI_name)
            elif taxid[1][0] == taxid_:
                taxid[1].append(NCBI_name)
            elif taxid[2][0] == taxid_:
                taxid[2].append(NCBI_name)
        for item in taxid:
            if len(item) == 2:
                print("taxid为"+str(item[0])+"的未找到对应的NCBI物种名称")
        return taxid


def ghostx(fasta_file="", output_name="", threads=10):
    os.system("date")
    os.system("ghostx aln -i {fasta_file} -d /data1/database/StringDB/stringv11 -o {output_name} -a {threads}".format(
        fasta_file=fasta_file, output_name=output_name, threads=threads))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="获得相近物种")
    parser.add_argument("-fasta", action="store",
                        dest="fasta_file", default=None, help="差异蛋白的fasta文件")
    parser.add_argument("-threads", action="store",
                        dest="threads", default=10, help="GhostX运行线程数，默认为10")
    parser.add_argument("-o", action="store", dest="output_filename",
                        default=None, help="GhostX软件的输出结果,以项目号命名")
    parser.add_argument("-spe", action="store", dest="species_path", required=False,
                        default="/data1/database/StringDB/species.v11.5.txt", help="species库")
    p = parser.parse_args()

    if p.output_filename is None:
        parser.print_help()
        exit()
    output_name = r"./"+p.output_filename
    threads = p.threads

    if os.path.exists(p.species_path) is None:
        print("species库不存在，检查是否在/data1/database/StringDB/species.v11.5.txt下")
        parser.print_help()
        exit()

    # ghostx run
    if p.fasta_file is None:
        print("要运行GhostX软件，fasta文件是必须的")
        parser.print_help()
        exit()

    fasta_path = r"./"+p.fasta_file

    if os.path.exists(fasta_path) is None:
        print("输入正确的fasta文件")
        parser.print_help()
        exit()
    ghostx(fasta_path, output_name, threads=threads)
    # 获取NCBI_物种名称""
    species_path = p.species_path
    list_ = get_taxid_no3(output_name)
    x = get_name(list_, species_path)
    print("相似度最高的3个物种为:\n")
    print(x)