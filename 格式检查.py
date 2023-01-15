import pandas as pd
import os
import re
import numpy as np


def file_recognize(Peptides_path="", Proteins_path="", Parameter_path=""):
    """"这个函数可以自动识别目录里的parameter,proteins,peptides文件"""

    project_type = ""

    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if re.search(r"mete", name):
                Parameter_path = r"./{name}".format(name=name)
            if re.search(r"tein", name):
                Proteins_path = r"./{name}".format(name=name)
                project_type = "protein"
            if re.search(r"tide", name):
                Peptides_path = r"./{name}".format(name=name)
                project_type = "protein"
            if re.search(r"screenname2", name, re.I):
                Screenname2_path = r"./{name}".format(name=name)
                project_type = "non-target_metabo2"
            if re.search(r"Pos", name, re.I):
                Pos_path = r"./{name}".format(name=name)
                project_type = "non-target_metabo1"
            if re.search(r"Neg", name, re.I):
                Neg_path = r"./{name}".format(name=name)
                project_type = "non-target_metabo1"
            if re.search(r"peak", name, re.I):
                peaktable_path = r"./{name}".format(name=name)
                project_type = "target_metabo"
    if project_type == "protein":
        return project_type, Peptides_path, Proteins_path, Parameter_path
    elif project_type == "non-target_metabo2":
        return project_type, Parameter_path, Screenname2_path
    elif project_type == "non-target_metabo1":
        return project_type, Parameter_path, Pos_path, Neg_path
    elif project_type == "target_metabo":
        return project_type, Parameter_path, peaktable_path
    else:
        print("确保输入文件和检查程序在同一目录下，保证输入文件名是标准的，以使检查程序能识别。")
        return None
        finished()


def get_sample_name_list(parameter_path):
    # 获取列名，从parameter中去读
    df = pd.read_excel(parameter_path, sheet_name="Sheet1", names=["Sample", "Group"])
    gn_series = df["Sample"]
    list_ = gn_series.tolist()
    if len(list_) != len(list(set(list_))):
        print("检查样本名是否填重复了")
        finished()
    return list_


def check_parameter(Parameter_path, type=""):
    df = pd.read_excel(Parameter_path, sheet_name="Sheet1",
                       header=0, names=["Sample", "Group"])
    df2 = pd.read_excel(Parameter_path, sheet_name="Sheet2",
                        header=0, names=["Method", "Group1", "Group2"])
    sample_name = list(set(df.loc[:, "Sample"].tolist()))
    group_name = list(set(df.loc[:, "Group"].to_list()))
    group_name2 = df.loc[:, "Group"].to_list()

    # 检查每一组的样本数
    if type == "non-target_metabo1":
        for i in group_name:
            count = group_name2.count(i)
            if count < 3:
                print("非靶代谢项目，每组最少3个样本，检查是否填错。")
                finished()
    if type == "target_metabo":
        for i in group_name:
            count = group_name2.count(i)
            if count < 3:
                print("靶向代谢项目，每组最少3个样本，检查是否填错。")
                finished()
    if type == "protein":
        for i in group_name:
            count = group_name2.count(i)
            if count < 2:
                print("蛋白项目，每组最少2个样本，检查是否填错。")
                finished()
    # 检查是否少列
    if len(list(df.columns)) > 2:
        print("检查parameter的sheet1是否多了一列，应该为2列，依次填写")
        finished()
    if len(list(df2.columns)) > 3:
        print("检查parameter的sheet2是否有多余的列，应该为3列，填写Method、group1、group2")
        finished()
    # 检查组名、样本名中是否含有空格
    for gn in group_name:
        if " " in gn:
            print("组别{gn}在表格填写中含有空格".format(gn=gn))
            finished()
    for sn in sample_name:
        if " " in sn:
            print("组别{sn}在表格填写中含有空格".format(sn=sn))
            finished()

    # 检查是否填写了正确的类型名字,待选的有ttest、anova、pairedttest
    type_list = df2.loc[:, "Method"].to_list()
    for tn in type_list:
        type_candicate = ["ttest", "anova", "pairedttest"]
        if tn not in type_candicate:
            print(
                "类别名称{tn}填写有问题，待选的有ttest、anova、pairedttest，检查是否有空格或者输错".format(tn=tn))
            finished()
    # 非Anova的行挑出
    # 检查Sheet1和Sheet2 中的一致性
    # 检查ttest和pairedtest方法的组别是否设置正确

    ttest_paired_test1 = df2[df2["Method"] != "anova"]["Group1"]
    ttest_paired_test2 = df2[df2["Method"] != "anova"]["Group2"]
    # 第一组
    for gn in ttest_paired_test1:
        if gn not in group_name:
            print("sheet2中的组别名称{gn}填写和Sheet1不一致，检查是否有空格或者输错".format(gn=gn))
            finished()
        if " " in gn:
            print("组别{gn}在Sheet2填写中含有空格".format(gn=gn))
            finished()
    # 第二组
    for gn in ttest_paired_test2:
        if gn not in group_name:
            print("sheet2中的组别名称{gn}填写和Sheet1不一致，检查是否有空格或者输错".format(gn=gn))
            finished()
        if " " in gn:
            print("组别{gn}在Sheet2填写中含有空格".format(gn=gn))
            finished()

    # 对anova方法的参数进行检查
    df3 = df2[df2["Method"] == "anova"]
    if df3.shape[0] == 0:
        pass
    else:
        for item in df3.loc[:, "Group1"]:
            if len(item.split(";")) == 1:
                print("请确认anova行是否用分号分隔")
                finished()
            elif len(item.split(";")) == 2:
                print("请保证anova分析中至少有3个组")
                finished()

            # 
            not_found_list = []
            for subitem in item.split(";"):
                if subitem not in group_name:
                    not_found_list.append(subitem)
            print("anova中填写的{name}在sheet1中找不到".format(name=not_found_list))
            finished()

        for item in df3.loc[:, "Group2"]:
            if str(item) != "nan":
                print("parameter表2中的anova分析第二列应为空，请检查")
                finished()


def check_Proteins_NegPos(path="", sn_series=[], type_=""):
    # 检查第三列是否为GeneSymbol
    if type_ == "neg":
        type_ = "负离子"
        df = pd.read_csv(path, sep="\t", header=0, names=None)
        name = df.columns.tolist()
    if type_ == "pos":
        type_ = "正离子"
        df = pd.read_csv(path, sep="\t", header=0, names=None)
        name = df.columns.tolist()
    if type_ == "pro":
        type_ = "蛋白"
        df = pd.read_excel(path, header=0)
        name = df.columns.tolist()
        if name[0] != "Accession":
            print("蛋白表格的第1列应该为Accession,检查是否填错，没有也要加空列")
            finished()
        if name[1] != "Protein Name":
            print("蛋白表格的第2列应该为Protein Name,检查是否填错，没有也要加空列")
            finished()
        if name[2] != "Gene Symbol":
            print("蛋白表格的第3列应该为Gene Symbol,检查是否填错，没有也要加空列")
            finished()
        if name[3] != "Description":
            print("蛋白表格的第4列应该为Description，检查是否填错，没有也要加空列")
            finished()
    if type_ == "is2":
        type_ = "inputScreenName2"
        df = pd.read_csv(path, header=0, names=None, sep="\t", low_memory=False)
        name = df.columns.tolist()
        col_name = "MetaboName	Alignment ID	KEGGID	HMDBID	SuperClass	Class	SubClass	Average Rt(min)	Average Mz	Metabolite name	Adduct type	MS/MS assigned	Formula	Ontology	MS/MS matched	Total score	S/N average".split(
            "\t")
        # 检查列名
        for i in range(len(col_name)):
            if col_name[i] != name[i]:
                print(
                    "在input.screenName2文件中{i}列应该是{name}".format(i=i + 1, name=col_name[i]))
                finished()
            if col_name[i] not in name:
                print(
                    "{name}列在input.screenName2文件中是必须的列，检查列名是否错误或者缺列（缺数据用空列）。".format(name=name[i]))
                finished()
    if type_ == "peak":
        type_ = "peak"
        df = pd.read_excel(path, header=0, names=None)
        # 检查Proteins文件中的所有样本名和parameter中是否一致
        name = df.columns.tolist()

    for x in sn_series:
        a = 0
        for name2 in name:
            if x == name2:
                a = 1
            else:
                continue
        if a == 0:
            print(r"parameter中的样本名{name}未在{biao}表中找到".format(
                name=x, biao=type_))
    # 检查是否有多余列
    if name[-1] not in sn_series:
        print("检查是否有多余列")
        finished()


def pause():
    x = input("格式检查完成，输入任意键回车后结束")


def finished():
    print("格式检查出错，请改正存在问题，输入任意键回车后继续。")
    finish_ = input("按任意键退出")


if __name__ == '__main__':
    # os.chdir(r"C:\Users\Leo\Desktop\FC\non-target_metabo")
    os.chdir(r"C:\Users\Leo\Desktop\FC\non-target_metabo2")
    recognize_result = file_recognize()
    if recognize_result[0] != None:
        if recognize_result[0] == "protein":
            # 获取组别名字
            Parameter_path = recognize_result[3]
            Proteins_path = recognize_result[2]
            gn_series = get_sample_name_list(Parameter_path)

            # 检查parameter.xlsx
            check_parameter(Parameter_path, type="protein")
            # 检查Proteins.xlsx
            check_Proteins_NegPos(Proteins_path, sn_series=gn_series, type_="pro")
            # 检查Peptides.xlsx
        if recognize_result[0] == "non-target_metabo1":
            # 获取组别名字
            Parameter_path = recognize_result[1]
            Pos_path = recognize_result[2]
            Neg_path = recognize_result[3]
            gn_series = get_sample_name_list(Parameter_path)
            check_parameter(Parameter_path, type=recognize_result[0])
            check_Proteins_NegPos(path=Pos_path, sn_series=gn_series, type_="pos")
            check_Proteins_NegPos(path=Neg_path, sn_series=gn_series, type_="neg")

        if recognize_result[0] == "non-target_metabo2":
            Parameter_path = recognize_result[1]
            Screenname2_path = recognize_result[2]
            gn_series = get_sample_name_list(Parameter_path)
            check_parameter(Parameter_path, type=recognize_result[0])
            check_Proteins_NegPos(path=Screenname2_path,
                                  sn_series=gn_series, type_="is2")
        if recognize_result[0] == "target_metabo":
            parameter_path = recognize_result[1]
            peaktable_path = recognize_result[2]
            gn_series = get_sample_name_list(parameter_path)
            check_parameter(parameter_path, type=recognize_result[0])
            check_Proteins_NegPos(path=peaktable_path,
                                  sn_series=gn_series, type_="peak")

    pause()
