from os import getenv
from datetime import datetime
from time import sleep

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from wechat_biz.send import *
from typing import Tuple
from faker import Factory

import requests as req


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


@err
def watcher(page: str, parser: BeautifulSoup=BeautifulSoup) -> BeautifulSoup:
    _headers = {'User-Agent': fake.user_agent()}
    _res = req.get(url=page, headers=_headers).text
    return parser(_res, "html.parser")


@err
def watch_tag(page: BeautifulSoup, tag: str, attrs: dict, **kwargs) -> str:
    tags = page.find_all(tag, attrs=attrs)
    paper, code = list(map(lambda x: x.find("a").get("href", None) if x.find("a") is not None else None,
                           tags))

    _msg = "DragDiffusion代码释出监控\n\n"
    if all(map(lambda x: x is None, tags)):
        _msg += f"{datetime.now()}：作者删文章跑路"

    if not code:
        _msg += f"{datetime.now()}：代码未释出，请耐心等待"

    if all([paper, code]):
        _msg += f"{datetime.now()}：代码已更新\n\n paper: {paper}\ncode:{code}"

    if kwargs:
        for k, v in kwargs.items():
            _msg += f"\n\n{k}: {v}"

    return _msg


if __name__ in "__main__":
    url = "https://yujun-shi.github.io/projects/dragdiffusion.html"
    corpid, corpsecret, agentid = get_env_vars()
    app = Sender(corpid=corpid,
                 corpsecret=corpsecret,
                 agentid=agentid)

    rounds = 1
    while True:
        soup = watcher(url)
        msg = watch_tag(page=soup, tag="div", attrs={"class": "links"}, rounds=rounds)
        app.send_text(message=msg, touser="wechat_nickname_in_enterprise_1|wechat_nickname_in_enterprise_2")
        rounds += 1
        sleep(900)
