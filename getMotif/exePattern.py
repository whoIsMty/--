from email import parser
import sys
import re
import os


def parse_fasta_to_dict(path, pattern="\|(\w+)\|"):
    def sequence_generator(path):
        f = open(path, "r", encoding="utf-8")
        sequence = ""
        name = ""

        while True:
            line = f.readline()
            if line:
                if ">" in line:
                    if sequence != "":
                        yield sequence, name
                        sequence, name = ("", re.search(pattern, line).group(1))

                    else:
                        try:
                            name = re.search(pattern, line).group(1)
                        except AttributeError:
                            print(line,pattern)
                            print("Fasta非常规，联系MTY。")
                            x = input("回车结束")
                            sys.exit(1)
                else:
                    sequence += line.strip()
            else:
                yield sequence, name
                break

    result = {}
    for sequence, name in sequence_generator(path):
        if name not in result:
            result[name] = sequence
    return result


def auto_verify(header: str, col_name: str):
    vir_list = header.strip().split("\t")
    for i in range(len(vir_list)):
        if col_name == vir_list[i]:
            return i
    print("名为{name}的列不存在".format(name=col_name))
    return


def get_start(line: str, index):  # 提取起始点，返回的是一个起始点数字。
    x = line.strip().split("\t")[index].replace(" ", "")
    accession = x.strip().split("[")[0]
    pattern = re.compile(r'\[(\w+)\-')
    """WP_011586482.1 [121-132"""
    y = re.findall(pattern, x)
    if len(y) == 0:
        print(line, "\n没有找到起始点数据，这条处理跳过")
        return None
    else:
        y = int(y[0])
    dic = {accession: y}
    return dic


def get_offset(line: str,
               index: int,
               type_="Carbamidomethyl",
               atom_list=[]):  # 计算偏移量
    # 返回一个[ [offset1,score1],[offset2,score2],[offset3,score3] ]"""
    # 字符串规整化（去除空格）

    x = line.split("\t")[index].replace(" ", "")
    c = type_
    # 1xDeamidated [Q13(100)];1xCarbamidomethyl[C24(100)]
    offset_score_list = []
    if c in x:
        x = x.strip().split(c)[1].replace(" ", "").replace("[", "").replace("]", "")
        offset_list = x.strip().split(";")  # 得到列表

        # 得到类似 C9(100); C14(100)
        # print(offset_list)
        for offset_score in offset_list:  # "C9(100)"
            atom = offset_score[0]
            if atom in atom_list:
                if offset_score.strip().split("(")[0] == 'N-Term':
                    continue
                offset = int(offset_score.strip().split("(")[0].replace(atom,
                                                                        ""))  # 得到9
                if len(offset_score.strip().split("(")) == 1:
                    score = "---"
                else:
                    score = str(offset_score.strip().split("(")[1].replace(
                        ")", ""))
                o_s = [offset, score]
                offset_score_list.append(o_s)
    return offset_score_list


def get_window(core=0, seq=""):
    seq = str(seq)
    length = len(seq)
    if 10 <= core <= length - 11:  # -----------
        window = seq[core - 10:core + 11]
        return window, seq[core]
    elif core < 10:  # *****---------                print(1)
        window = (10 - core) * "*" + seq[0:core + 11]
        # print("缺少的序列已用*补全：", window)
        return window, seq[core]
    elif length - 11 < core <= length + 9:  # ------******
        window = seq[core - 10:length] + (11 + core - length) * "*"
        # print("缺少的序列已用*补全：", window)
        return window, seq[core]
    else:
        return "-------------------"
        print("那种情况真的出现了,还是写一下吧")


def output(input_path,
           database_path,
           output_path,
           start_colname="Positions in Master Proteins",
           offset_colname="Modifications (all possible sites)", type_="Carbamidomethyl", atom_list=[], pattern=""):
    # 读取excel
    afile = open(input_path, "r")
    afile_context = afile.readlines()
    header = afile_context[0].strip().replace("\"",
                                              "") + "\tcore_Amino_acid"  "\tstart_position\t" + "score\t" + "13_acids\t" + "window\n"
    afile_data_text = afile_context[1:]
    afile.close()
    # 输出文件
    output = open(output_path, "w",encoding="utf8")
    output.write(header)
    new_orchid_dict = parse_fasta_to_dict(database_path, pattern=pattern)

    for line in afile_data_text:
        line = line.replace("\"", "")
        start = get_start(line, auto_verify(header, start_colname))
        if start is None:
            continue
        index = auto_verify(header, offset_colname)
        offset = get_offset(line, index, type_=type_, atom_list=atom_list)
        for key in start.keys():
            if key in new_orchid_dict:
                pre_start = start[key]
                for i in range(len(offset)):
                    score = offset[i][1]
                    core = offset[i][0] + pre_start - 2
                    start_actual = core + 1
                    window, core_anjisuan = get_window(core, new_orchid_dict[key])
                    if len(window) != 21:
                        print(line + "\n 以上的可能提取错误，因为长度不是21个，提取的结果为{window}，建议手动提取。".format(window=window))
                    output.write(
                        line.rstrip("\n") + "\t" + core_anjisuan + "\t" + str(start_actual) + "\t" + str(
                            score) + "\t" + str(window)[4:17] + "\t" + str(window) + "\n")
            else:
                print(key + "在库里没找到")
                sys.exit(1)

    output.close()


def get_file():
    fs = os.listdir(".")
    result = {}
    for f in fs:
        if f.endswith("PeptideGroups.txt"):
            result["Pep"] = f
        elif f.endswith("fasta"):
            result["fasta"] = f
        elif "meter" in f:
            result["parameter"] = f
    if len(result) < 3:
        print(f"缺少{3 - len(result)}个文件。需要有fasta,PeptideGroups.txt,以及一个参数文件。")
        x = input("回车结束")
        sys.exit(1)
    else:
        return result


def get_parameters(path):
    line = open(path, "r", encoding="utf-8").readline()
    if "(" not in line:
        print("parameter文件第一行形如Phospho(STY)           pattern=\|(\w+)\| ")
        x = input("回车结束")
        sys.exit(1)
    else:
        # print(line)

        try:
            result = re.search(r"^([A-Za-z]+)\(([A-Z]+)\)\s+pattern=(.*?)$", line)
            if result:
                type_ = result.group(1)
                atoms = list(result.group(2))
                pattern = result.group(3)
                # print(pattern,"pattern")
                result = [type_, atoms, pattern]
                return result
            else:
                print("匹配参数错误，检查parameter")
                x = input("回车结束")
                sys.exit(1)
        except Exception:
            print("parameter解析错误，检查源码或者parameter。")
            x = input("回车结束")
            sys.exit(1)


if __name__ == "__main__":
    # os.chdir(r"C:\Users\leois\Desktop\test")
    fs = get_file()
    params = get_parameters(fs["parameter"])
    if fs:
        output(fs["Pep"], fs["fasta"], output_path=fs["Pep"] + "_result.txt", type_=params[0], atom_list=params[1],
               pattern=params[2])
    print("Finish extracting the windows,please check the result file ")
    x = input("回车结束")
    sys.exit(1)
