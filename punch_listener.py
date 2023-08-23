from os import getenv
from datetime import datetime

from dotenv import load_dotenv
from wechat_biz.send import *
from typing import Tuple
from faker import Factory

from flask import Flask, request


fake = Factory().create('zh_CN')


def err(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e)
            print(f"{func.__name__} 运行错误..")
            result = f"{func.__name__} 运行错误..：{e}"
        return result

    return wrapper


def get_env_vars(dotenv_path: str= ".env") -> Tuple[str, str, str]:
    load_dotenv(dotenv_path)
    _corpid = getenv("corpid")
    _corpsecret = getenv("corpsecret")
    _agentid = getenv("agentid")
    return _corpid, _corpsecret, _agentid



app = Flask(__name__)  # 在当前文件下创建应用

corpid, corpsecret, agentid = get_env_vars()
wechat_app = Sender(corpid=corpid,
             corpsecret=corpsecret,
             agentid=agentid)

@app.route("/punch", methods=['GET'])
def index():
    args = request.args
    name = args.get('name')
    print(name)
    if name == "iPhone8_m":
        current_time = datetime.now()
        msg = f"【punch listener】 M Punch Succeeded: {current_time}"
        wechat_app.send_text(message=msg, touser="elias|ZhengHongHao")
        return "ok"
    elif name == "iPhone8_e":
        current_time = datetime.now()
        msg = f"【punch listener】 E Punch Succeeded: {current_time}"
        wechat_app.send_text(message=msg, touser="elias|ZhengHongHao")
        return "ok"
    else:
        msg = f"【punch listener】注意非法请求"
        wechat_app.send_text(message=msg, touser="elias|ZhengHongHao")
        return "Asshole"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=11451)
