import requests
import json


def get_token():
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    params = {
        "corpid": "ww96d6fabb0cb642b7",
        "corpsecret": "yh6uI0JmkJUsBD6mHQswzTvKvUq-QQT8G5msvVu9R40"
    }
    r = requests.get(url, params=params)
    dict_result = (r.json())
    return dict_result['access_token']


def send_message(access_token: str,text=""):
    url = " https://qyapi.weixin.qq.com/cgi-bin/message/send"
    params = {"access_token": access_token}
    data = {
        "toparty": toparty,
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


if __name__ == "__main__":
    access_token = get_token()
    send_message(access_token=access_token,text="")
