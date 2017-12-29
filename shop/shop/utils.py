# -*- coding: utf-8 -*-
import re

def get_start_urls():
    return ['http://www.dianping.com/citylistguonei?redir=Ly93d3cuZGlhbnBpbmcuY29t#']

def get_domain(url):
    p=re.compile("(^((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/))")
    try:
        return re.findall(p,url)[0][0]
    except Exception,e:
        return ''
