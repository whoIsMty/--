import os
import argparse
import pandas as pd
import time


def stat_count(path):
    df = pd.read_excel(path, sheet_name="Sheet2", header=0)
    group_count = df.shape[0]
    return group_count


if __name__ == '__main__':
    # 传参
    parser = argparse.ArgumentParser(description="this program can get how many groups have been processed in the "
                                                 "specified time\n此程序可以将指定时间内处理过的组别数目进行统计。")
    parser.add_argument('-s', "--start_time", required=True, type=str, help='起始时间,形如2021-12-01')
    parser.add_argument('-o', "--over_time", required=True, type=str, help='结束时间，形如2021-12-31')

    args = parser.parse_args()
    start_time = args.start_time
    over_time = args.over_time
    # 找到某区间的文件名。保存到parameter_list
    os.system(r"find -maxdepth 2 -type f -name 'parameter*.xlsx' -newermt {start_time} ! -newermt {over_time} > parameter_list".
              format(start_time=start_time, over_time=over_time))
    count = 0
    s = open(r"./parameter_list", "r")
    print(1)
    for line in s.readlines():
        print(line)
        count += stat_count(line.strip())
    localtime = time.asctime(time.localtime(time.time()))
    print("the jobs are done at ", localtime)
    os.system("rm ./parameter_list")
    print("中间文件已经删除")
    print("group count:", count)
