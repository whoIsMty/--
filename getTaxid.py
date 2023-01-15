#!/bin/python3
import argparse
import requests
import os
import re
import sys


def get_file_urls(taxid="9606"):
    url = rf"https://cn.string-db.org/cgi/download?species_text={taxid}"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0"
    }
    try:
        
        response = requests.get(url, headers=headers)
        # print(response.text)
    except requests.exceptions.ConnectionError:
        print(f"请求超时，String数据库可能没有{taxid}的数据，或者稍后再试。")
        sys.exit(1)
    # print(response.text)
    try: # https://stringdb-static.org/download/protein.sequences.v11.5/4565.protein.sequences.v11.5.fa.gz
        protein_link_detaild = re.search(r"https://stringdb-static\.org/download/protein\.links.*?/\d+\.protein\.links.+?\.gz",
                                         response.text).group(0)
        protein_info = re.search(r"https://stringdb-static\.org/download.*?/\d+\.protein\.info.+?\.gz", response.text).group(
            0)
        protein_sequence = re.search(r"https://stringdb-static\.org/download/protein\.sequences\..*?/\d+\.protein\.sequences.+?\.fa\.gz",
                                     response.text).group(0)
        alias = re.search(r"https://stringdb-static\.org/download/protein.aliases.*?/\d+\.protein\.aliases.+?\.gz", response.text).group(0)
    except AttributeError:
        print("页面解析不到文件url，String数据库可能没有{taxid}的数据，建议手动检查一下。")
        sys.exit(1)
    return protein_link_detaild, protein_info, protein_sequence, alias


def download_file(url):
    name = url.split("/")[-1]
    print(f"开始下载{name}.")
    try:
        down = requests.get(url)
        open(f"./{name}","wb").write(down.content)
        print(f"{name}下载完成。")
    except Exception:
        print(f"下载{name}失败")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="这个程序用于获取特定taxid的string数据库文件，并且建库")
    parser.add_argument("-taxid", action="store", default=None, dest="taxid", help="需要下载安装的string数据库的taxid",required=True)
    parser.add_argument("-step", action="store", default=0, dest="step", help="选择从第几个文件开始下载。默认为0，从第一个下载到最后一个。",required=False)


    p = parser.parse_args()
    taxid = p.taxid
    print(type(p))
    step = int(p.step)

    protein_link_detaild, protein_info, protein_sequence, alias = get_file_urls(taxid=taxid)
    print("\n".join([protein_link_detaild,protein_info,protein_sequence,alias]))
    now_dir = os.getcwd()
    if not os.path.exists(f"{now_dir}/{taxid}_temp"):
        os.mkdir(f"{now_dir}/{taxid}_temp")

    os.chdir(f"{now_dir}/{taxid}_temp")
    url_list = [protein_link_detaild,protein_info,protein_sequence,alias]
    for i in range(step,len(url_list)):
        download_file(url_list[i])
    os.system(f"gunzip {taxid}*.gz")
    print(f"已经解压{taxid}*.gz")
    os.system(f"mv {taxid}* /home/bpadmin/PAA/bin/stringdata")
    print("下载的文件已经移动至 /home/bpadmin/PAA/bin/stringdata")
    os.chdir("/home/bpadmin/PAA/bin/stringdata")
    os.system(f"makeblastdb -in $(find . -name {taxid}.protein.sequence*fa -type f ) -dbtype prot -hash_index")
    print(f"{taxid}建库完成")
    os.system("cd - ")
