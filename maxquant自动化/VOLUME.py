import json
import os
import time
import re
import requests

SERVER_TAG = "38"
BLANK = " " * 6


def get_token():
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    params = {
        "corpid": "ww96d6fabb0cb642b7",
        "corpsecret": "yh6uI0JmkJUsBD6mHQswzTvKvUq-QQT8G5msvVu9R40"
    }
    r = requests.get(url, params=params)
    dict_result = (r.json())
    return dict_result['access_token']


def send_message(access_token: str, text=""):
    url = " https://qyapi.weixin.qq.com/cgi-bin/message/send"
    params = {"access_token": access_token}
    data = {
        "toparty": 14,
        "totag": "@all",
        "msgtype": "text",
        "agentid": 1000006,
        "text": {
            "content": text
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    data = json.dumps(data, ensure_ascii=False)
    r = requests.post(url,
                      params=params,
                      data=data.encode("utf-8").decode("latin1"))


def get_volume():
    os.system("df -h -BG > ~/crontab/log/VOLUME.log")


def check_and_remind(mounted=[]):

    def generate_msg(info_dict="", status=1):
        time_txt = "时间:" + time.strftime('%Y-%m-%d %H:%M:%S',
                                         time.localtime(time.time())) + "\n"
        msg = "" + time_txt
        msg += "机器编号：" + SERVER_TAG + "\n"

        if status:
            for key, value in info_dict.items():
                msg += f"{key}目录已经使用了{value}%\n"
            msg += "存储空间不足，注意备份！"
        else:
            for key, value in info_dict.items():
                msg += f"{key}目录已经使用了{value}%\n"
            msg += "存储空间充足！"
        return msg


    info = open("/home/bpadmin/crontab/log/VOLUME.log", "r", encoding="utf-8").readlines()[1:]
    print(f"{BLANK}开始检查目录{' '.join(mounted)}的硬存")
    # 拿到所有硬盘信息
    all_info = {}
    need_process = {}
    for line in info:
        line = re.findall(r"(\d+)%.*?(/.*?)\s+$", line)
        use = int(line[0][0])
        mounted_ = line[0][1].strip()
        if mounted_ in mounted:
            all_info[mounted_] = use
        if mounted_ in mounted and use > 80:
            need_process[mounted_] = use
    # 需要提醒
    if need_process:
        msg = generate_msg(need_process, status=1)
        send_message(access_token=get_token(), text=msg)
    else:
        msg = generate_msg(all_info, status=0)
        send_message(access_token=get_token(), text=msg)


if __name__ == "__main__":
    get_volume()
    print(f"{BLANK}start")
    dir_list = ["/", "/data1"]
    check_and_remind(dir_list)
    print(f"{BLANK}done")
