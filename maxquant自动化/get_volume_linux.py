import os
import re


def get_volume():
    os.system("df -h -BG > VOLUME.log")


def check_and_remind(mounted):
    info = open("./VOLUME.log", "r", encoding="utf-8").readlines()[1:]
    print(f"    开始检查目录{mounted}的硬存")

    need_process = {}

    for line in info:
        mounted_ = line.strip().split("\t")[-1]
        use = int(line.strip().split("\t")[-2].replace("%", ""))

        if mounted_ == mounted and use > 80:
            need_process[mounted_] = use
    
    if need_process :
        for key,value in need_process.items():
            msg = f"{key}目录已经使用了{value}%,注意备份"
    else :
        remind()

        


if __name__ == "__main__":
    get_volume()
    dir_list = ["/", "/data1"]

    for dir in dir_list:
        check_and_remind(dir)
