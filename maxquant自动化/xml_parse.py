#!/bin/python3
import re
import sys
import os

from bs4 import BeautifulSoup


class mqpar_parser:

    def __init__(self, xml_path="", fasta_path="", raw_path_list=[]):
        """构造函数"""
        self.xml_path = xml_path
        self.fasta_path = fasta_path
        self.raw_path_list = raw_path_list
        self.change_identifierParseRule()
        self.change_fasta_path_tag()
        self.change_raw_path()

    def change_fasta_path_tag(self):
        xml_path = self.xml_path
        # 解析该文件
        xml_file_handle = open(xml_path, "r", encoding="utf-8")
        mqpar_bs = BeautifulSoup(xml_file_handle, "xml")
        xml_file_handle.close()
        # 将fasta_path改为新的
        mqpar_bs.fastaFilePath.string = self.fasta_path
        # 输出并保存
        xml_result = mqpar_bs.prettify()  # <class 'str'>
        xml_file_handle = open(xml_path, "w", encoding="utf-8")
        xml_file_handle.write(xml_result)
        xml_file_handle.close()
        return self  # 实现链式调用

    def change_identifierParseRule(self):

        def get_fasta_description(path=self.fasta_path):
            with open(path, "r") as f:
                first_line = f.readlines()[0].strip()
                rule = (r'>.*\|(.*)\|', r'>(gi\|[0-9]*)', r'IPI:([^\|.]*)',
                        r'>(.*)', r'>([^ ]*)', r'>([^\t]*)')
                if len(re.findall(rule[0], first_line)) != 0:
                    return rule[0]
                elif len(re.findall(rule[1], first_line)) != 0:
                    return rule[1]
                elif len(re.findall(rule[2], first_line)) != 0:
                    return rule[2]
                elif len(re.findall(rule[3], first_line)) != 0:
                    return rule[3]
                elif len(re.findall(rule[4], first_line)) != 0:
                    return rule[4]
                elif len(re.findall(rule[5], first_line)) != 0:
                    return rule[5]
                else:
                    print("未解析出fasta文件的类型")
                    sys.exit()

        xml_path = self.xml_path
        # 解析该文件
        xml_file_handle = open(xml_path, "r", encoding="utf-8")
        mqpar_bs = BeautifulSoup(xml_file_handle, "xml")
        xml_file_handle.close()
        # 获取identifier
        __identifierParseRule__ = get_fasta_description()
        # 将identifierParseRule改为新的
        mqpar_bs.identifierParseRule.string = __identifierParseRule__
        # 输出并保存
        xml_result = mqpar_bs.prettify()  # <class 'str'>
        xml_file_handle = open(xml_path, "w", encoding="utf-8")
        xml_file_handle.write(xml_result)
        xml_file_handle.close()
        return self  # 实现链式调用

    def change_num_Threads(self):
        num_Threads = len(self.raw_path_list)

        xml_path = self.xml_path
        # 解析该文件
        xml_file_handle = open(xml_path, "r", encoding="utf-8")
        mqpar_bs = BeautifulSoup(xml_file_handle, "xml")
        xml_file_handle.close()
        # 将线程数改为新的
        mqpar_bs.numThreads.string = num_Threads
        # 输出并保存
        xml_result = mqpar_bs.prettify()  # <class 'str'>
        xml_file_handle = open(xml_path, "w", encoding="utf-8")
        xml_file_handle.write(xml_result)
        xml_file_handle.close()
        return self  # 实现链式调用

    def change_raw_path(self):

        def change_experiment(mqpar_bs: BeautifulSoup, self):
            raw_list = self.raw_path_list
            new_list = []
            for raw in raw_list:
                x = raw.split('\\')[-1].split('.')[0].strip()
                new_list.append(x)
            # 将节点清空
            mqpar_bs.experiments.string = ""

            for i in range(len(new_list)):
                new_raw_tag = mqpar_bs.new_tag('string')
                new_raw_tag.string = new_list[i]
                mqpar_bs.experiments.append(new_raw_tag)

        def change_fractions(mqpar_bs: BeautifulSoup, self):
            # 清空节点
            mqpar_bs.fractions.string = ""
            for i in range(len(self.raw_path_list)):
                new_raw_tag = mqpar_bs.new_tag('short')
                new_raw_tag.string = "32767"
                mqpar_bs.fractions.append(new_raw_tag)

        def change_ptms(mqpar_bs: BeautifulSoup, self):
            # 清空节点
            mqpar_bs.ptms.string = ""
            for i in range(len(self.raw_path_list)):
                new_raw_tag = mqpar_bs.new_tag('boolean')
                new_raw_tag.string = "False"
                mqpar_bs.ptms.append(new_raw_tag)

        def change_params_Groupindex(mqpar_bs: BeautifulSoup, self):
            # 清空节点
            mqpar_bs.paramGroupIndices.string = ""
            for i in range(len(self.raw_path_list)):
                new_raw_tag = mqpar_bs.new_tag('int')
                new_raw_tag.string = "0"
                mqpar_bs.paramGroupIndices.append(new_raw_tag)

        def change_referenceChannel(mqpar_bs: BeautifulSoup, self):
            mqpar_bs.referenceChannel.string = ""
            for i in range(len(self.raw_path_list)):
                new_raw_tag = mqpar_bs.new_tag('string')
                mqpar_bs.referenceChannel.append(new_raw_tag)

        raw_path_list = self.raw_path_list
        # 解析该文件
        if len(raw_path_list) == 0:
            print("raw文件缺失")
            sys.exit()
        else:
            xml_file_handle = open(self.xml_path, "r", encoding="utf-8")
            mqpar_bs = BeautifulSoup(xml_file_handle, "xml")
            xml_file_handle.close()
            # 将fasta_path改为新的
            # 将节点清空
            mqpar_bs.filePaths.string = ""

            for i in range(len(raw_path_list)):
                new_raw_tag = mqpar_bs.new_tag('string')
                new_raw_tag.string = raw_path_list[i]
                mqpar_bs.filePaths.append(new_raw_tag)

            # 类似项修改
            change_experiment(mqpar_bs, self)
            change_fractions(mqpar_bs, self)
            change_ptms(mqpar_bs, self)
            change_params_Groupindex(mqpar_bs, self)
            change_referenceChannel(mqpar_bs, self)
            # 输出并保存
            xml_result = mqpar_bs.prettify()  # <class 'str'>
            xml_file_handle = open(self.xml_path, "w", encoding="utf-8")
            xml_file_handle.write(xml_result)
            xml_file_handle.close()
            return self  # 实现链式调用


if __name__ == "__main__":
    # xml = r"C:\Users\Leo\Desktop\maxquant_test\mqpar.xml"
    # fasta_path = r"C:\Users\Leo\Desktop\maxquant_test\uniprot-Homo sapiens (Human) [9606]-204274-20220325.fasta"
    pwd = os.getcwd()
    xml = pwd + "/mqpar.xml"
    fasta_path = pwd + "/db.fasta"
    raw_path_list = []
    for root, dirs, files in os.walk(pwd, topdown=False):
        for file in files:
            if "raw" in file :
                raw_path_list.append(os.path.join(root,file))

    mqpar_xml = mqpar_parser(
        xml,
        fasta_path=fasta_path,
        raw_path_list=raw_path_list)
