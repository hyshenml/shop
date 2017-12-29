# -*- coding: utf-8 -*-
import requests

def data5u_api():
    data5u_url="http://api.ip.data5u.com/dynamic/get.html?order=95c3615dcb357a583b04c7ab6403588f&sep=3"
    r = requests.get(url=data5u_url)  # 最基本的GET请求
    return r.text