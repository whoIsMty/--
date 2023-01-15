import re
from Bio import SeqIO


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
        print("那种情况真的出现了,还是写一下吧")


def get_andoutput(database_path, path=""):
    # 序列转化为字典
    data = SeqIO.parse(database_path, "fasta")
    new_orchid_dict = {}
    for record in data.records:
        x = str(record.id)
        y = str(record.seq)
        new_orchid_dict[x] = y
    del data
    # 打开数据文件
    s = open(path, "r")
    s_context = s.readlines()[1:]
    outputpath = path + ".result.txt"
    o = open(outputpath, "w")
    o.write("name\twindow\tstatus\tstatus2\n")
    n = 1

    for line in s_context:
        x = line.strip().split("_")
        na = re.search(r"([A-Z])(\d+)", x[-1])
        atom = na[1]
        num = int(na[2]) - 1
        name = x[0]
        window = get_window(core=num, seq=new_orchid_dict[name])
        status = "OK"
        status2 = str(n)
        if window[10] != atom:
            status = str(line) + "有问题" + window
            o.write(name + "\t" + window + "\t" + status + "\t" + status2 +
                    "\n")

        else:
            o.write(name + "\t" + window + "\t" + status + "\t" + status2 +
                    "\n")
        n += 1
    o.close()
    s.close()


if __name__ == "__main__":
    database_path = r"C:\Users\leois\Desktop\新建文件夹 (2)\Ciona_savignyi.CSAV2.0.pep.all.fasta"
    path = r"C:\Users\leois\Desktop\新建文件夹 (2)\数据.txt"
    get_andoutput(database_path=database_path, path=path)
