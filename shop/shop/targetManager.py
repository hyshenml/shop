# -*- coding: utf-8 -*-
from db import MyDb
import time
class targetManager():
    @staticmethod
    def prepare_targets():
        urls=query_urls2()
        res=[]
        for url_data in urls:
            t=target()
            t.setType(url_data['type'])
            t.setUrl(url_data['url'])
            res.append(t)
        return res

class target():
    def setType(self,type):
        self.target_type=type
    def setUrl(self,url):
        self.url = url

    def record_update_time(self):
        now=int(time.time())
        sql="update urlItem set last_parse_time=%d where url ='%s'"%(now,self.url)
        with MyDb() as conn:
            c=conn.cursor()
            c.execute(sql)
            conn.commit()

def query_urls():
    res={'url':'http://www.dianping.com/citylistguonei?redir=aHR0cDovL3d3dy5kaWFucGluZy5jb20v','type':'root'}
    return [res]

def query_urls2(limit=34000):
    sql = "select * from urlItem where last_parse_time=0 order by target_type desc limit %d;"%limit
    res=[]
    with MyDb() as conn:
        c=conn.cursor()
        c.execute(sql)
        for row in c.fetchall():
            res.append({'url':row[0],'type':row[1]})
    return res

