from Bio import SeqIO
import sys
import re
import argparse



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
               type="Carbamidomethyl",
               atom="C"):  # 计算偏移量
    # 返回一个[ [offset1,score1],[offset2,score2],[offset3,score3] ]"""
    # 字符串规整化（去除空格）

    x = line.split("\t")[index]
    x = x.replace(" ", "")
    c = type
    # 1xDeamidated [Q13(100)];1xCarbamidomethyl[C24(100)]
    offset_score_list = []
    if c in x:
        x = x.strip().split(c)[1]
        x = x.strip().split("[")[1]
        x = x.strip().split("]")[0]
        # 得到类似 C9(100); C14(100)
        offset_list = x.strip().split(";")  # 得到列表
        for offset_score in offset_list:  # "C9(100)"
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
        return window
    elif core < 10:  # *****---------                print(1)
        window = (10 - core) * "*" + seq[0:core + 11]
        # print("缺少的序列已用*补全：", window)
        return window
    elif length - 11 < core <= length + 9:  # ------******
        window = seq[core - 10:length] + (11 + core - length) * "*"
        # print("缺少的序列已用*补全：", window)
        return window
    else:
        
        return "-------------------"


def output(input_path,
           database_path,
           output_path,
           start_colname="Positions in Master Proteins",
           offset_colname="Modifications (all possible sites)", type="Carbamidomethyl", atom="C"):
    # 读取excel
    afile = open(input_path, "r")
    afile_context = afile.readlines()
    header = afile_context[0].strip().replace("\"", "") + "\tstart_position\t" + "score\t" + "window\n"
    afile_data_text = afile_context[1:]
    afile.close()
    # 输出文件
    output = open(output_path, "w")
    output.write(header)
    # 获得所有ID
    # all_idlist = get_allid(database_path)
    # 获得window并写result

    data = SeqIO.parse(database_path, "fasta")
    new_orchid_dict = {}
    for record in data.records:
        x = str(record.id).split("|")[1].replace(" ", "")
        y = str(record.seq)
        new_orchid_dict[x] = y
    del data

    for line in afile_data_text:
        line = line.replace("\"", "")
        start = get_start(line, auto_verify(header, start_colname))
        if start is None:
            continue
        index = auto_verify(header, offset_colname)
        offset = get_offset(line, index, type=type, atom=atom)
        for key in start.keys():
            if key in new_orchid_dict:
                pre_start = start[key]
                for i in range(len(offset)):
                    score = offset[i][1]
                    core = offset[i][0] + pre_start - 2
                    start_actual = core + 1
                    window = get_window(core, new_orchid_dict[key])
                    if len(window) != 21:
                        print(line + "\n 以上的可能提取错误，因为长度不是21个，提取的结果为{window}，建议手动提取。".format(window=window))
                    output.write(
                        line.rstrip("\n") + "\t" + str(start_actual) + "\t" + str(score) + "\t" + str(window) + "\n")
            else:
                print(key + "在库里没找到")
                sys.exit(1)

    output.close()

if __name__ == "__main__":
    # get_file()
    parser = argparse.ArgumentParser(description="修饰位点")
    parser.add_argument("-cf", action="store", dest="csv_file", required=True, default=None, help="表格文件")
    parser.add_argument("-sf", action="store", dest="fasta_file", required=True, default=None, help="FASTA序列文件")
    parser.add_argument("-type", action="store", dest="type", required=True, default=None, help="修饰类型")
    parser.add_argument("-atom", action="store", dest="atom", required=True, default=None, help="原子")
    parser.add_argument("-o", action="store", dest="output_path", required=True, default=None, help="输出文件名")

    p = parser.parse_args()
    data_file = p.csv_file
    seqdata_file = p.fasta_file
    output_path = fr"./{p.output_path}.txt"
    type_ = p.type
    atom = p.atom
    output(data_file, seqdata_file, output_path=output_path, type=type_, atom=atom)
    # print(data_file, seqdata_file, output, type_, atom)
    print("完成提取。")
